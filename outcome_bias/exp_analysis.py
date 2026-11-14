"""Analysis for E1 to E5. Pass the logs of one experiment (any models); runs of the same
model and reasoning setting are pooled.

  python -m outcome_bias.exp_analysis logs/a.eval logs/b.eval ...

For each model, version and question it prints the mean per condition and the pre-registered
contrasts: the mean over units (scenarios or vignettes) of the per-unit difference, a bootstrap
95% interval over units, and how many units moved up or down. Wordings are pooled within a unit.
It first checks that the stimulus files still match the hashes frozen in notes/prereg_hashes.json.
"""

import hashlib
import json
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

ROOT = Path(__file__).resolve().parent.parent
STIMULI = ["outcome_bias/exp_e1.py", "outcome_bias/exp_e3.py", "outcome_bias/exp_e4.py", "outcome_bias/exp_e5.py",
           "outcome_bias/scenarios_v2.py", "outcome_bias/scenarios.py", "outcome_bias/experiments.py"]
MODEL_ORDER = ("haiku", "sonnet", "opus")

CONTRASTS = {
    "e1": [("bad", "good"), ("bad", "none"), ("good", "none")],
    "e2": [("failure", "success"), ("success", "omitted"), ("failure", "omitted")],
    "e3": [("harm", "payoff"), ("payoff", "omitted"), ("harm", "omitted")],
    "e4": [("failure", "success"), ("success", "none"), ("failure", "none")],
    "e5": [("harm", "noharm"), ("harm", "none"), ("noharm", "none")],
}
COND_ORDER = {
    "e1": ("good", "none", "bad"), "e2": ("success", "omitted", "failure"), "e3": ("payoff", "omitted", "harm"),
    "e4": ("success", "none", "failure"), "e5": ("noharm", "none", "harm"),
}


def file_hashes():
    return {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in STIMULI}


def check_freeze():
    frozen_path = ROOT / "notes" / "prereg_hashes.json"
    if not frozen_path.exists():
        print("NOTE: no frozen hashes found (notes/prereg_hashes.json).")
        return
    frozen = json.loads(frozen_path.read_text())["files"]
    changed = [f for f, h in file_hashes().items() if frozen.get(f) != h]
    print("Stimulus files match the frozen versions." if not changed else f"WARNING: changed since freeze: {changed}")


def boot(values, n=5000, seed=0):
    rng = random.Random(seed)
    means = sorted(st.mean(rng.choices(values, k=len(values))) for _ in range(n))
    return st.mean(values), means[int(0.025 * n)], means[int(0.975 * n) - 1]


def load(paths):
    rows, bad = [], 0
    for p in paths:
        log = read_eval_log(str(p))
        model = log.eval.model.split("/")[-1]
        reasoning = log.eval.task_args.get("reasoning", "none")
        for s in log.samples or []:
            md = s.metadata
            sm = next(iter(s.scores.values())).metadata if s.scores else {}
            if not sm.get("parsed"):
                bad += 1
                continue
            rows.append(dict(exp=md["exp"], model=model, reasoning=reasoning, unit=md["unit"], version=md["version"],
                             cond=md["cond"], question=md["question"], answer=sm["answer"],
                             detected=sm.get("detected"), others=sm.get("others_listed"),
                             thought=(getattr(s.output.usage, "reasoning_tokens", 0) or 0) > 0))
    return rows, bad


def unit_means(rows, value="answer"):
    cells = defaultdict(list)
    for r in rows:
        cells[(r["unit"], r["cond"])].append(float(r[value]))
    return {k: st.mean(v) for k, v in cells.items()}


def contrast(um, a, b):
    units = sorted({u for u, c in um if c == a} & {u for u, c in um if c == b})
    diffs = [um[(u, a)] - um[(u, b)] for u in units]
    if len(diffs) < 2:
        return None
    m, lo, hi = boot(diffs)
    tol = 0.02 * (max(um.values()) - min(um.values()) or 1)
    return m, lo, hi, sum(d > tol for d in diffs), sum(d < -tol for d in diffs), len(diffs)


def fmt(c, digits):
    m, lo, hi, up, down, n = c
    star = " *" if lo > 0 or hi < 0 else ""
    return f"{m:+.{digits}f} [{lo:+.{digits}f}, {hi:+.{digits}f}] {up}up/{down}dn{star}"


def report(rows):
    exp = rows[0]["exp"]
    groups = sorted({(r["model"], r["reasoning"]) for r in rows},
                    key=lambda g: (next((i for i, k in enumerate(MODEL_ORDER) if k in g[0]), 9), g[1]))
    for model, reasoning in groups:
        R = [r for r in rows if r["model"] == model and r["reasoning"] == reasoning]
        thought = st.mean(r["thought"] for r in R)
        print(f"\n===== {exp.upper()}  {model}  reasoning={reasoning}  ({len(R)} answers; reasoning tokens used in {thought:.0%})")
        versions = sorted({r["version"] for r in R})
        if exp == "e1":
            versions = ["all"] + versions
        for version in versions:
            V = R if version == "all" else [r for r in R if r["version"] == version]
            if exp == "e4":
                value = "detected"
                questions = ["detect"]
            else:
                value = "answer"
                questions = list(dict.fromkeys(r["question"] for r in V))
            n_units = len({r["unit"] for r in V})
            print(f"\n  -- {version} ({n_units} units)")
            for q in questions:
                Q = [r for r in V if r["question"] == q]
                um = unit_means(Q, value)
                digits = 2 if (exp == "e4" or q in ("sanction", "action", "performance")) else 1
                means = "  ".join(f"{c} {st.mean(v for (u, cc), v in um.items() if cc == c):.{digits}f}"
                                  for c in COND_ORDER[exp] if any(cc == c for _, cc in um))
                label = "listed target" if exp == "e4" else q
                print(f"  {label:<13} {means}")
                for a, b in CONTRASTS[exp]:
                    c = contrast(um, a, b)
                    if c:
                        print(f"      {a + ' - ' + b:<20} {fmt(c, digits)}")
            if exp == "e4":
                um = unit_means(V, "others")
                print("  other tickets listed per session: " + "  ".join(
                    f"{c} {st.mean(v for (u, cc), v in um.items() if cc == c):.2f}" for c in COND_ORDER[exp]))
        if exp == "e2":
            # difference-in-differences on the performance score: the cost of the shortcut by outcome
            P = [r for r in R if r["question"] == "performance" and r["version"] in ("borderline", "compliant")]
            cells = defaultdict(list)
            for r in P:
                cells[(r["unit"], r["version"], r["cond"])].append(r["answer"])
            units = sorted({k[0] for k in cells if k[1] == "borderline"})
            # keep units that have every cell (a cell can be empty if all its answers were unparsed)
            units = [u for u in units if all(cells.get((u, v, c)) for v in ("borderline", "compliant")
                                             for c in ("success", "failure", "omitted"))]
            pen = {c: [st.mean(cells[(u, "compliant", c)]) - st.mean(cells[(u, "borderline", c)]) for u in units]
                   for c in ("success", "failure", "omitted")}
            did = [s - f for s, f in zip(pen["success"], pen["failure"])]
            m, lo, hi = boot(did)
            print("\n  -- performance score: cost of the shortcut (compliant minus borderline), by ending")
            print("  " + "  ".join(f"{c} {st.mean(v):.2f}" for c, v in pen.items()))
            print(f"      cost after success - cost after failure   {m:+.2f} [{lo:+.2f}, {hi:+.2f}]"
                  f"{' *' if lo > 0 or hi < 0 else ''}   (negative = the shortcut costs less when the task succeeded)")


def main():
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        sys.exit(__doc__)
    check_freeze()
    rows, bad = load(paths)
    print(f"{len(rows)} parsed answers, {bad} unparsed or errored.")
    for exp in sorted({r["exp"] for r in rows}):
        report([r for r in rows if r["exp"] == exp])
    print("\n* = 95% interval excludes zero. Per the pre-registration, an effect is claimed only when this holds "
          "in the same direction for at least two of the three models.")


if __name__ == "__main__":
    main()
