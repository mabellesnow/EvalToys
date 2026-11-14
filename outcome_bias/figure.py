"""Headline figure: does the auditor's violation probability move with the outcome?

One row per auditor model. Each dot is one borderline scenario's change in mean
violation probability (failure minus success, in points). The black mark is the
mean over scenarios with a bootstrap 95% CI. Right of zero means harsher after
failure, which is the outcome-bias direction.

Run:  python -m outcome_bias.figure                      (latest arguable log per model in ./logs)
      python -m outcome_bias.figure a.eval b.eval ...    (specific logs; several logs of one model are pooled)
      add --exclude incident_report_arguable to drop scenarios
Writes figures/outcome_bias.png and figures/outcome_bias.csv (the table view).
"""

import argparse
import csv
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from inspect_ai.log import read_eval_log

# reference palette (light mode): surface, ink, one series hue, recessive grid
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
DOT = "#2a78d6"


def latest_arguable_logs(log_dir="logs"):
    """Newest log per model whose samples are arguable scenarios (pass logs explicitly to pool several)."""
    newest = {}
    for path in sorted(Path(log_dir).glob("*.eval"), key=lambda p: p.stat().st_mtime):
        header = read_eval_log(str(path), header_only=True)
        if header.status != "success" or header.eval.task_args.get("variant") != "arguable":
            continue
        newest[header.eval.model] = path  # later files overwrite earlier ones
    return list(newest.values())


def add_probabilities(path, probs, exclude):
    """Add one log's borderline probabilities to probs[(scenario, outcome)]; return its model."""
    log = read_eval_log(str(path))
    for s in log.samples or []:
        m = s.metadata
        if not m["violation"] or m.get("variant") not in ("arguable", "v2_borderline") or m["scenario"] in exclude:
            continue
        meta = next(iter(s.scores.values())).metadata if s.scores else {}
        if meta.get("parsed") and isinstance(meta.get("probability"), (int, float)):
            probs[(m["scenario"], m["outcome"])].append(meta["probability"])
    return log.eval.model


def per_scenario_diffs(probs, a, b):
    scenarios = sorted({k[0] for k in probs})
    diffs = {
        sc: st.mean(probs[(sc, a)]) - st.mean(probs[(sc, b)])
        for sc in scenarios
        if probs[(sc, a)] and probs[(sc, b)]
    }
    return diffs


def bootstrap_ci(values, n_boot=10_000, seed=0):
    rng = random.Random(seed)
    boots = sorted(st.mean(rng.choices(values, k=len(values))) for _ in range(n_boot))
    return boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="*")
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--compare", default="failure,success", help="two outcomes, a,b: plots a minus b")
    ap.add_argument("--out", default="figures/outcome_bias")
    args = ap.parse_args()
    a, b = args.compare.split(",")
    paths = [Path(p) for p in args.logs] or latest_arguable_logs()
    if not paths:
        raise SystemExit("No arguable logs found in logs/")

    # pool every log of the same model: more samples per transcript, one row per model
    probs_by_model, logs_by_model = defaultdict(lambda: defaultdict(list)), defaultdict(list)
    for path in paths:
        probs = defaultdict(list)
        model = add_probabilities(path, probs, set(args.exclude))
        for k, v in probs.items():
            probs_by_model[model][k].extend(v)
        logs_by_model[model].append(path.name)

    rows = []
    for model, probs in probs_by_model.items():
        diffs = per_scenario_diffs(probs, a, b)
        if not diffs:
            print(f"skip {model}: no '{a}' and '{b}' data")
            continue
        vals = list(diffs.values())
        lo, hi = bootstrap_ci(vals)
        rows.append({"model": model.split("/")[-1], "diffs": diffs, "mean": st.mean(vals), "lo": lo, "hi": hi,
                     "log": "; ".join(logs_by_model[model])})
    size = {"haiku": 0, "sonnet": 1, "opus": 2}  # small to large; other models after, by name
    rows.sort(key=lambda r: (next((v for k, v in size.items() if k in r["model"]), 9), r["model"]))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out.with_suffix(".csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "scenario", f"p_viol_{a}_minus_{b}", "log"])
        for r in rows:
            for sc, d in sorted(r["diffs"].items()):
                w.writerow([r["model"], sc, f"{d:.2f}", r["log"]])
            w.writerow([r["model"], "MEAN", f"{r['mean']:.2f}", f"95% CI [{r['lo']:.2f}, {r['hi']:.2f}]"])

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 11, "text.color": INK,
                         "axes.labelcolor": INK_2, "xtick.color": INK_2, "ytick.color": INK})
    fig, ax = plt.subplots(figsize=(9, 1.6 + 1.0 * len(rows)), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    jitter = random.Random(1)
    for i, r in enumerate(rows):
        y = len(rows) - 1 - i
        xs = list(r["diffs"].values())
        ys = [y + 0.12 + jitter.uniform(0, 0.24) for _ in xs]  # dots in a band above the mean
        ax.scatter(xs, ys, s=42, color=DOT, alpha=0.55, edgecolors=SURFACE, linewidths=1.5, zorder=2)
        # label only the extremes (more than 15 points), so the reader can find them in the table
        for (sc, d), yd in zip(r["diffs"].items(), ys):
            if abs(d) > 15:
                ax.annotate(sc.removesuffix("_arguable"), (d, yd), xytext=(0, 9), textcoords="offset points",
                            ha="center", fontsize=9, color=INK_2)
        ym = y - 0.12
        ax.plot([r["lo"], r["hi"]], [ym, ym], color=INK, linewidth=2, solid_capstyle="round", zorder=3)
        ax.scatter([r["mean"]], [ym], s=80, marker="D", color=INK, edgecolors=INK, linewidths=0, zorder=4)
        # CI label in its own column right of the plot, so it never collides with dots
        ax.annotate(f"{r['mean']:+.1f}  [{r['lo']:+.1f}, {r['hi']:+.1f}]", (1.02, ym), xycoords=("axes fraction", "data"),
                    va="center", fontsize=10, color=INK)

    lim = max(10, max(abs(d) for r in rows for d in r["diffs"].values()) + 2)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks(range(len(rows)), [r["model"] for r in reversed(rows)])
    ax.axvline(0, color=INK_2, linewidth=1, zorder=1)
    ax.grid(axis="x", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    ax.set_xlabel(f"Change in violation probability, {a} minus {b} (points out of 100)")
    n = len(rows[0]["diffs"]) if rows else 0
    ax.set_title(f"Same borderline transcript, different ending: {n} scenarios per model",
                 loc="left", fontsize=12, color=INK, pad=22)
    ax.text(0, 1.02, "Dots: one scenario each.  Diamond and bar: mean with 95% CI.  Right of 0 = harsher after failure.",
            transform=ax.transAxes, fontsize=9, color=INK_2)
    fig.tight_layout()
    fig.savefig(out.with_suffix(".png"), dpi=200, facecolor=SURFACE)
    print(f"Wrote {out.with_suffix('.png')} and {out.with_suffix('.csv')}")
    for r in rows:
        print(f"  {r['model']:<20} {r['mean']:+.1f} [{r['lo']:+.1f}, {r['hi']:+.1f}]  from {r['log']}")


if __name__ == "__main__":
    main()
