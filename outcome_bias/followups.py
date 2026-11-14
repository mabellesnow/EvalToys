"""Analysis for the two follow-up experiments. Pass every relevant log; runs of the
same model are pooled and the script works out which variant each sample belongs to.

  python -m outcome_bias.followups logs/a.eval logs/b.eval ...

1. Ambiguous policies (variant "ambiguous", needs -T no_ending=true runs).
   Do outcomes move the verdict, in EITHER direction, more than a neutral sentence does?
   Compared with the borderline ("arguable") set as a reference, if those logs are passed too.

2. Justified violations (variant "justified"). Pass the justified logs AND the base logs
   (blatant and arguable) for the same model. For each justified scenario vs its base:
   - persuasion effect: violation probability with the justification minus without (neutral ending)
   - outcome effect with vs without the justification: (failure - success) justified minus base
"""

import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

MODEL_ORDER = ("haiku", "sonnet", "opus")


def boot(values, n=10_000, seed=0):
    if not values:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(seed)
    means = sorted(st.mean(rng.choices(values, k=len(values))) for _ in range(n))
    return st.mean(values), means[int(0.025 * n)], means[int(0.975 * n) - 1]


def fmt(r, digits=1):
    m, lo, hi = r
    return f"{m:+.{digits}f} [{lo:+.{digits}f}, {hi:+.{digits}f}]"


def load(paths):
    """{model: {(variant, scenario, outcome): {"p": [...], "flag": [...]}}} for violating/borderline versions."""
    data = defaultdict(lambda: defaultdict(lambda: {"p": [], "flag": []}))
    for path in paths:
        log = read_eval_log(str(path))
        model = log.eval.model.split("/")[-1]
        for s in log.samples or []:
            m = s.metadata
            meta = next(iter(s.scores.values())).metadata if s.scores else {}
            if not m["violation"] or not meta.get("parsed") or not isinstance(meta.get("probability"), (int, float)):
                continue
            cell = data[model][(m.get("variant", "blatant"), m["scenario"], m["outcome"])]
            cell["p"].append(meta["probability"])
            cell["flag"].append(bool(meta["flagged"]))
    return data


def mean_p(cells, key):
    return st.mean(cells[key]["p"]) if cells.get(key) and cells[key]["p"] else None


def majority(cells, key):
    f = cells[key]["flag"] if cells.get(key) else []
    return (sum(f) / len(f) >= 0.5) if f else None


def ambiguous_report(model, cells):
    variants = [v for v in ("ambiguous", "arguable") if any(k[0] == v and k[2] == "omitted" for k in cells)]
    if "ambiguous" not in variants:
        return
    print(f"\n=== {model}: does an outcome destabilise the verdict? (vs no ending) ===")
    print(f"{'set':<11}{'n':>4}  {'|success-none|':>22}{'|failure-none|':>22}{'|neutral-none|':>22}{'excess shift':>22}  flips s/f/neutral")
    for v in variants:
        scen = sorted({k[1] for k in cells if k[0] == v})
        abs_s, abs_f, abs_n, excess, flips = [], [], [], [], [0, 0, 0]
        for sc in scen:
            base = mean_p(cells, (v, sc, "omitted"))
            vals = {o: mean_p(cells, (v, sc, o)) for o in ("success", "failure", "none")}
            if base is None or None in vals.values():
                continue
            ds, df, dn = (abs(vals[o] - base) for o in ("success", "failure", "none"))
            abs_s.append(ds); abs_f.append(df); abs_n.append(dn)
            excess.append((ds + df) / 2 - dn)
            b = majority(cells, (v, sc, "omitted"))
            for i, o in enumerate(("success", "failure", "none")):
                flips[i] += int(majority(cells, (v, sc, o)) != b)
        print(f"{v:<11}{len(excess):>4}  {fmt(boot(abs_s)):>22}{fmt(boot(abs_f)):>22}{fmt(boot(abs_n)):>22}{fmt(boot(excess)):>22}  {flips[0]}/{flips[1]}/{flips[2]}")
    print("  excess shift = mean of |success-none| and |failure-none|, minus |neutral-none|, per scenario.")
    print("  Positive = an outcome moves the verdict more than a neutral sentence does. 'none' here = no ending.")
    print("  flips = scenarios whose majority verdict differs from the no-ending verdict.")

    print(f"\n  {model}, ambiguous scenarios: mean violation probability (flag rate)")
    print(f"  {'scenario':<30}" + "".join(f"{o:>16}" for o in ("success", "neutral", "failure", "no ending")))
    for sc in sorted({k[1] for k in cells if k[0] == "ambiguous"}):
        row = ""
        for o in ("success", "none", "failure", "omitted"):
            c = cells.get(("ambiguous", sc, o))
            row += f"{st.mean(c['p']):>9.1f} ({sum(c['flag']) / len(c['flag']):.0%})" if c and c["p"] else f"{'-':>16}"
        print(f"  {sc.removesuffix('_ambiguous'):<30}{row}")


def justified_report(model, cells):
    pairs = sorted({k[1] for k in cells if k[0] == "justified"})
    if not pairs:
        return
    persuasion, outcome_j, outcome_b, interaction, flag_shift = [], [], [], [], []
    rows = []
    for sj in pairs:
        base = sj.removesuffix("_justified")
        bvar = "arguable" if base.endswith("_arguable") else "blatant"
        pj = {o: mean_p(cells, ("justified", sj, o)) for o in ("success", "none", "failure")}
        pb = {o: mean_p(cells, (bvar, base, o)) for o in ("success", "none", "failure")}
        if None in pj.values() or None in pb.values():
            rows.append((sj, None))
            continue
        persuasion.append(pj["none"] - pb["none"])
        fj, fb = pj["failure"] - pj["success"], pb["failure"] - pb["success"]
        outcome_j.append(fj); outcome_b.append(fb); interaction.append(fj - fb)
        flag_j = sum(cells[("justified", sj, "none")]["flag"]) / len(cells[("justified", sj, "none")]["flag"])
        flag_b = sum(cells[(bvar, base, "none")]["flag"]) / len(cells[(bvar, base, "none")]["flag"])
        flag_shift.append(flag_j - flag_b)
        rows.append((sj, (pb["none"], pj["none"], fb, fj, flag_b, flag_j)))
    print(f"\n=== {model}: justified violations vs their base scenarios ===")
    if not persuasion:
        print("  No base data for these scenarios: pass the blatant and arguable logs for this model too.")
        return
    print(f"  n = {len(persuasion)} scenario pairs (CIs over pairs; small n, read with care)")
    print(f"  persuasion effect, p(viol) justified minus base, neutral ending: {fmt(boot(persuasion))}")
    print(f"  flag rate justified minus base, neutral ending:                {fmt(boot(flag_shift), 2)}")
    print(f"  failure minus success, base:                                    {fmt(boot(outcome_b))}")
    print(f"  failure minus success, justified:                               {fmt(boot(outcome_j))}")
    print(f"  difference (does a justification open the door to outcome bias?): {fmt(boot(interaction))}")
    print("  Positive difference = with a justification, success helps the agent more than without.")
    print(f"\n  {'scenario':<34}{'p base':>8}{'p just':>8}{'F-S base':>10}{'F-S just':>10}{'flag base':>11}{'flag just':>11}")
    for sj, r in rows:
        if r is None:
            print(f"  {sj:<34}  (missing base or justified data)")
        else:
            print(f"  {sj:<34}{r[0]:>8.1f}{r[1]:>8.1f}{r[2]:>+10.1f}{r[3]:>+10.1f}{r[4]:>11.0%}{r[5]:>11.0%}")


def main():
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        sys.exit(__doc__)
    data = load(paths)
    for model in sorted(data, key=lambda m: next((i for i, k in enumerate(MODEL_ORDER) if k in m), 9)):
        ambiguous_report(model, data[model])
        justified_report(model, data[model])


if __name__ == "__main__":
    main()
