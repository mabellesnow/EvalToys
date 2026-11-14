"""Analysis for exploratory follow-up X1 (labelled scale for E3's violation question).

  python -m outcome_bias.x1_analysis

Reads logs/exp_runs.tsv. For each model, on E3's 21 borderline scenarios, violation question only:
  - mean score per ending, and harm - payoff, harm - none, payoff - none, for E3's main arm and each X1 arm
  - change in harm - payoff from E3's main arm (first run) to each X1 arm, paired by scenario
  - the same change from E3's first run to its re-run (Haiku, Sonnet), as a yardstick for run-to-run noise
"""

from outcome_bias import exp_analysis as ea

ARMS = [("E3 main, run 1", "run1"), ("E3 main, re-run", "run2"),
        ("Labelled scale", "x1-labelled"), ("Labelled + instruction", "x1-ignore")]


def logs(label, model):
    out = []
    for line in open(ea.ROOT / "logs" / "exp_runs.tsv"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 5 and f[0] == label and f[1] == "e3" and f[2] == "main" and f[3] == model and f[4]:
            out.append(ea.ROOT / f[4])
    return out


def scores(label, model):
    """{(scenario, ending): mean violation score} on borderline versions, and the unparsed count."""
    paths = logs(label, model)
    if not paths:
        return None, 0
    rows, bad = ea.load(paths)
    rows = [r for r in rows if r["question"] == "violation" and r["version"] == "borderline"]
    return ea.unit_means(rows), bad


def per_scenario(um, a, b):
    units = sorted({u for u, c in um if c == a} & {u for u, c in um if c == b})
    return {u: um[(u, a)] - um[(u, b)] for u in units}


def show(c):
    m, lo, hi = c[:3]
    return f"{m:+6.1f} [{lo:+6.1f}, {hi:+6.1f}]{' *' if lo > 0 or hi < 0 else '  '}"


def main():
    ea.check_freeze()
    for model in ("haiku", "sonnet", "opus"):
        print(f"\n===== {model}  (violation question, 21 borderline scenarios)")
        base, _ = scores("run1", model)
        for name, label in ARMS:
            um, bad = scores(label, model)
            if um is None:
                continue
            means = "  ".join(f"{c} {sum(v for (u, cc), v in um.items() if cc == c) / sum(1 for (u, cc) in um if cc == c):5.1f}"
                              for c in ("payoff", "omitted", "harm"))
            print(f"\n  {name}  ({bad} unparsed in these logs)   {means}")
            for a, b in (("harm", "payoff"), ("harm", "omitted"), ("payoff", "omitted")):
                print(f"      {a + ' - ' + b:<18} {show(ea.contrast(um, a, b))}")
            if label != "run1":
                d_new, d_base = per_scenario(um, "harm", "payoff"), per_scenario(base, "harm", "payoff")
                units = sorted(set(d_new) & set(d_base))
                change = [d_new[u] - d_base[u] for u in units]
                print(f"      change in harm - payoff from E3 run 1: {show(ea.boot(change))}  "
                      f"({sum(c < -5 for c in change)} scenarios down by >5, {sum(c > 5 for c in change)} up by >5)")
    print("\n* = 95% interval excludes zero. Exploratory: no re-run planned.")


if __name__ == "__main__":
    main()
