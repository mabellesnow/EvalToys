"""Summarise the latest eval log by variant x violation x outcome.

Run:  python -m outcome_bias.analysis                  (latest log in ./logs)
      python -m outcome_bias.analysis a.eval b.eval ...  (one log, or several pooled, e.g. repeat runs)
"""

import random
import sys
from collections import defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

OUTCOME_ORDER = ("success", "none", "failure", "omitted")  # "omitted" only in runs with -T no_ending=true
COMPARISONS = (
    ("failure", "success"), ("failure", "none"), ("success", "none"),
    ("success", "omitted"), ("failure", "omitted"), ("none", "omitted"),
)


def latest_log(log_dir: str = "logs") -> Path:
    logs = sorted(Path(log_dir).glob("*.eval"), key=lambda p: p.stat().st_mtime)
    if not logs:
        sys.exit(f"No .eval logs found in {log_dir}/")
    return logs[-1]


def new_cell():
    return {"n": 0, "flagged": 0, "severity": [], "probability": [], "review": 0, "unparsed": 0}


def add(cell, meta):
    if not meta.get("parsed"):
        cell["unparsed"] += 1
        return
    cell["n"] += 1
    cell["flagged"] += int(meta["flagged"])
    cell["review"] += int(bool(meta.get("human_review")))
    if isinstance(meta.get("severity"), (int, float)):
        cell["severity"].append(meta["severity"])
    if isinstance(meta.get("probability"), (int, float)):  # missing in logs from before it was asked
        cell["probability"].append(meta["probability"])


def rate(num, den):
    return num / den if den else float("nan")


def avg(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def paired_by_scenario(by_scenario, scenarios, measure, a, b, n_boot=10_000):
    """Mean of per-scenario differences (a minus b) with a bootstrap 95% CI over scenarios.

    Repeats of one transcript are nearly identical, so the scenario is the unit:
    each contributes one difference between its mean under outcome a and outcome b.
    """
    diffs = []
    for s in scenarios:
        ca, cb = by_scenario[(s, a)], by_scenario[(s, b)]
        if measure == "flag rate":
            va, vb = rate(ca["flagged"], ca["n"]), rate(cb["flagged"], cb["n"])
        else:
            va, vb = avg(ca[measure]), avg(cb[measure])
        if va == va and vb == vb:  # skip nan
            diffs.append(va - vb)
    if not diffs:
        return None
    rng = random.Random(0)
    boots = sorted(avg(rng.choices(diffs, k=len(diffs))) for _ in range(n_boot))
    lo, hi = boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]
    tol = 0.5 if measure == "probability" else 0.05  # ignore differences smaller than this when counting
    up, down = sum(d > tol for d in diffs), sum(d < -tol for d in diffs)
    return avg(diffs), lo, hi, up, down, len(diffs)


def main():
    paths = [Path(a) for a in sys.argv[1:]] or [latest_log()]
    samples, models = [], set()
    for path in paths:  # several logs are pooled, e.g. repeat runs of one model
        log = read_eval_log(str(path))
        samples.extend(log.samples or [])
        models.add(log.eval.model)
        print(f"Log: {path.name}   model: {log.eval.model}")
    if len(models) > 1:
        print(f"WARNING: pooling different models: {', '.join(sorted(models))}")

    cells = defaultdict(new_cell)  # (variant, violation, outcome)
    by_scenario = defaultdict(new_cell)  # (scenario, outcome), violating transcripts only
    variant_of = {}
    for sample in samples:
        m = sample.metadata
        variant = m.get("variant", "blatant")  # logs from before variants existed
        meta = (next(iter(sample.scores.values())).metadata or {}) if sample.scores else {}
        add(cells[(variant, m["violation"], m["outcome"])], meta)
        if m["violation"]:
            add(by_scenario[(m["scenario"], m["outcome"])], meta)
            variant_of[m["scenario"]] = variant

    present = {k[2] for k in cells}
    outcomes = [o for o in OUTCOME_ORDER if o in present]
    comparisons = [(a, b) for a, b in COMPARISONS if a in present and b in present]

    for variant in sorted({k[0] for k in cells}):
        print(f"\n== {variant} ==")
        print(f"{'transcript':<10} {'outcome':<8} {'n':>4} {'flag rate':>10} {'review rate':>12} {'severity':>9} {'p(viol)':>8} {'unparsed':>9}")
        rates, sevs, probs = {}, {}, {}
        for violation in (True, False):
            for outcome in outcomes:
                c = cells[(variant, violation, outcome)]
                rates[(violation, outcome)] = flag = rate(c["flagged"], c["n"])
                sevs[(violation, outcome)] = sev = avg(c["severity"])
                probs[(violation, outcome)] = prob = avg(c["probability"])
                review = rate(c["review"], c["n"])
                # arguable sets have no ground truth: the "violation" version is the borderline one
                label = ("borderline" if variant in ("arguable", "ambiguous", "v2_borderline") else "violation") if violation else "clean"
                print(f"{label:<10} {outcome:<8} {c['n']:>4} {flag:>10.2f} {review:>12.2f} {sev:>9.2f} {prob:>8.1f} {c['unparsed']:>9}")
        rows = "borderline" if variant in ("arguable", "ambiguous", "v2_borderline") else "violations"
        print(f"Outcome bias, flag rate ({rows}, failure minus success): {rates[(True, 'failure')] - rates[(True, 'success')]:+.2f}")
        print(f"Outcome bias, severity  ({rows}, failure minus success): {sevs[(True, 'failure')] - sevs[(True, 'success')]:+.2f}")
        print(f"Outcome bias, p(viol)   ({rows}, failure minus success): {probs[(True, 'failure')] - probs[(True, 'success')]:+.1f} points")

        scenarios = [s for s, v in variant_of.items() if v == variant]
        print(f"\nPaired by scenario ({rows}, n = {len(scenarios)} scenarios): mean difference [95% CI], scenarios up / down")
        for label, measure in (("flag rate", "flag rate"), ("severity", "severity"), ("p(viol)", "probability")):
            for a, b in comparisons:
                r = paired_by_scenario(by_scenario, scenarios, measure, a, b)
                if r is None:
                    continue
                mean_d, lo, hi, up, down, n = r
                fmt = "+.1f" if measure == "probability" else "+.2f"
                mark = "  *" if lo > 0 or hi < 0 else ""
                print(f"  {label:<10}{a + ' - ' + b:<20}{mean_d:{fmt}}  [{lo:{fmt}}, {hi:{fmt}}]  {up:>2} up / {down:>2} down{mark}")
        print("  * CI excludes zero")

    print("\nViolating (or borderline) transcripts by scenario: flag rate / mean severity / mean p(viol)")
    print(f"{'scenario':<26}" + "".join(f"{o:>21}" for o in outcomes))
    for scenario in dict.fromkeys(k[0] for k in by_scenario):
        row = ""
        for outcome in outcomes:
            c = by_scenario[(scenario, outcome)]
            row += f"{rate(c['flagged'], c['n']):>8.2f} / {avg(c['severity']):.1f} / {avg(c['probability']):>5.1f}"
        print(f"{scenario:<26}{row}")

    if errored := sum(1 for s in samples if not s.scores):
        print(f"\n{errored} samples errored; see `inspect view` for details.")


if __name__ == "__main__":
    main()
