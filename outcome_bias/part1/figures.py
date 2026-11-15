"""Figures for the pilot's write-up (docs/part1_pilot/blog_draft.md). Writes figures/part1/fig1..fig6.

  python -m outcome_bias.part1.figures

fig1_design.png     how one scenario becomes 8 transcripts and what the auditor returns
fig2_ceiling.png    per-scenario violation probability by set: blatant and subtle sit at the ceiling
fig3_which_side.png success vs no ending and failure vs no ending, per model, with 95% CIs
fig4_knife_edge.png Sonnet on cloud_budget across four set-1 runs and two set-2 runs, every sample
fig5_reasons.png    how often auditors' reasons mention the outcome, and how
fig6_v2.png         failure minus success on set 1 and on the longer set 2, per model
"""

import random
import statistics as st
from collections import defaultdict
from glob import glob

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from inspect_ai.log import read_eval_log

from outcome_bias.figures.style import (GRID, INK, INK_2, MODEL_COLOR, MODELS, MUTED, PANEL, SURFACE,
                                        arrow, box, tidy, title)
from outcome_bias.paths import FIGURES, LOGS as LOG_DIR

OUT = FIGURES / "part1"

LOGS = {
    "arguable": {
        "Haiku": ["Kf3XLX2D2KFbaFpGATTsbK", "hzt4NsyE969TaYsWLYfwhr", "eeKk6bZGdZAMw3wq9RS6Y4"],
        "Sonnet": ["LoTjJw24hjkqnhcpNvLzpx", "EH8oWTyMuXb25W8sfku8Vw"],
        "Opus": ["he9vZmvQyVi5xnAxxXR4zn", "noNoQjFoFkcZ4LRWYGeSyS"],
    },
    "blatant": {"Haiku": ["hLSLGPfUQ7eE7BkjSbnsWd"], "Sonnet": ["knFnuqFJzw8ocRB22F55YU"], "Opus": ["iXEofPZmChakS8xZJyCcfd"]},
    "subtle": {"Haiku": ["4jJ9Fzk5tMbVhLhfb7yjWk"], "Sonnet": ["VGEu88zBtXYnS45pdiCbWe"], "Opus": ["LmEXXGXHthu5SJqMAmUCFF"]},
    # v2: longer scenarios (docs/part1_pilot/results.md), two runs per model
    "v2": {
        "Haiku": ["8gu22GWU9oHU5a7t4PR4Xr", "aRJAZG4FRMCJJLtEn3YVZ3"],
        "Sonnet": ["7xjZNoWYR7KPUwBdgHec7G", "5PBs6cb2N8d7CUnMj6Mbk8"],
        "Opus": ["cpvYFw6L5K6rscFrP56tyZ", "NJmbTqeGqkogoE4umCvYmN"],
    },
}
VARIANT_NAMES = {"arguable": ("arguable",), "v2": ("v2_borderline",)}
# (panel title, log id, scenario id) for the cloud-budget figure; all Sonnet
KNIFE_PANELS = [
    ("Main set, run A", "9QSKs4kSaunaRypBsKoA65_rescored", "cloud_budget_arguable"),
    ("Main set, run B", "LoTjJw24hjkqnhcpNvLzpx", "cloud_budget_arguable"),
    ("Main set, run C", "EH8oWTyMuXb25W8sfku8Vw", "cloud_budget_arguable"),
    ("Main set, run D (rerun)", "8ywEVeFtVZTrvUJ3kiM6tn", "cloud_budget_arguable"),
    ("Longer set (v2), run 1", "7xjZNoWYR7KPUwBdgHec7G", "cloud_budget_v2"),
    ("Longer set (v2), run 2", "5PBs6cb2N8d7CUnMj6Mbk8", "cloud_budget_v2"),
]
TAG_LOG = "UaDWjbtSjfTW5yg6GWRVZD"



def log_path(log_id):
    return glob(str(LOG_DIR / f"*_{log_id}.eval"))[0]


def probabilities(log_ids, violation=True, variants=None):
    """{(scenario, outcome): [probabilities]} pooled over logs, optionally only some variants."""
    out = defaultdict(list)
    for log_id in log_ids:
        for s in read_eval_log(log_path(log_id)).samples or []:
            m = s.metadata
            meta = next(iter(s.scores.values())).metadata if s.scores else {}
            if variants and m.get("variant") not in variants:
                continue
            if m["violation"] == violation and meta.get("parsed") and isinstance(meta.get("probability"), (int, float)):
                out[(m["scenario"], m["outcome"])].append(meta["probability"])
    return out


def paired(probs, a, b, n_boot=10_000):
    scenarios = sorted({k[0] for k in probs})
    diffs = [st.mean(probs[(s, a)]) - st.mean(probs[(s, b)]) for s in scenarios if probs[(s, a)] and probs[(s, b)]]
    rng = random.Random(0)
    boots = sorted(st.mean(rng.choices(diffs, k=len(diffs))) for _ in range(n_boot))
    return st.mean(diffs), boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]


def fig1_design():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(0.1, 5.35, "One scenario becomes 8 transcripts. The auditor sees one at a time.", fontsize=13, color=INK)
    # versions
    box(ax, 0.1, 3.35, 2.5, 1.35, "Borderline version\nagent splits a \\$515 setup\ninto \\$480 + \\$35", weight="bold", size=9.5)
    box(ax, 0.1, 1.45, 2.5, 1.35, "Compliant version\nagent picks a \\$420\ninstance instead", size=9.5)
    ax.text(1.35, 1.05, "same policy, same task", ha="center", fontsize=9, color=INK_2)

    endings = [
        ("Success", "“The load test ran on Thursday\nas planned …”"),
        ("Failure", "“The load test was postponed\na week …”"),
        ("Neutral", "“The agent … closed its ticket.”"),
        ("No ending", "(transcript just stops)"),
    ]
    ys = [4.25, 3.3, 2.35, 1.4]
    for (name, text), y in zip(endings, ys):
        box(ax, 3.4, y, 3.0, 0.75, f"{name}\n{text}", size=8.8, align="left")
    # one container around the four endings: each version gets all four
    ax.add_patch(FancyBboxPatch((3.25, 1.25), 3.3, 3.9, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="none", ec=MUTED, lw=1, ls="--"))
    arrow(ax, 2.65, 4.02, 3.2, 3.6)
    arrow(ax, 2.65, 2.12, 3.2, 2.7)
    ax.text(2.92, 3.12, "× 4", ha="center", fontsize=10, color=INK_2)
    ax.text(4.9, 0.85, "each version gets all four endings;\nendings describe the task, never the violation",
            ha="center", fontsize=9, color=INK_2)

    # auditor
    box(ax, 7.2, 2.35, 1.4, 1.4, "Auditor\n(Haiku, Sonnet\nor Opus 5.5)\n\nsees policy +\none transcript", face="#e8f0fb", edge="#2a78d6", size=9)
    for y in ys:
        arrow(ax, 6.45, y + 0.37, 7.15, 3.05)
    arrow(ax, 8.65, 3.05, 9.0, 3.05)
    box(ax, 9.05, 1.75, 1.85, 2.6,
        "Returns\n\nviolation probability\n0–100\n\nviolation yes/no\n\nseverity 0–5\n\nhuman review yes/no\n\nreason",
        face=SURFACE, size=8.8)
    ax.text(5.5, 0.25,
            "Bias test: compare the auditor's answers on transcripts that differ only in the ending (same row, different column).",
            ha="center", fontsize=9.5, color=INK)
    fig.savefig(OUT / "fig1_design.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- fig 2
def fig2_ceiling():
    fig, ax = plt.subplots(figsize=(9, 3.9))
    rows = [("blatant", "Blatant violations\n(5 scenarios)"), ("subtle", "Subtle violations\n(5 scenarios)"),
            ("arguable", "Borderline cases\n(20 scenarios)")]
    jitter = random.Random(2)
    clean_all = []
    for i, (variant, label) in enumerate(rows):
        y = len(rows) - 1 - i
        for j, model in enumerate(MODELS):
            probs = probabilities(LOGS[variant][model])
            clean = probabilities(LOGS[variant][model], violation=False)
            clean_all += [st.mean(v) for k, v in clean.items() if k[1] == "none"]
            xs = [st.mean(v) for k, v in probs.items() if k[1] == "none"]
            ys = [y + (j - 1) * 0.16 + jitter.uniform(-0.04, 0.04) for _ in xs]
            ax.scatter(xs, ys, s=38, color=MODEL_COLOR[model], alpha=0.8, edgecolors=SURFACE, linewidths=1.2,
                       label=model if i == 0 else None, zorder=3)
    lo, hi = min(clean_all), max(clean_all)
    ax.axvspan(lo, hi, color=PANEL, zorder=1)
    ax.text((lo + hi) / 2, len(rows) - 0.42, "compliant\nversions", ha="center", va="bottom", fontsize=8.5, color=INK_2)
    ax.axvline(50, color=GRID, linewidth=1, zorder=1)
    ax.set_yticks(range(len(rows)), [r[1] for r in reversed(rows)])
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.set_xlabel("Violation probability with the neutral ending, mean per scenario (0–100)")
    tidy(ax)
    ax.legend(loc="lower left", frameon=False, ncol=3, fontsize=9.5, handletextpad=0.2, bbox_to_anchor=(0, -0.42))
    title(fig, ax, "Clear violations sit at the ceiling; only borderline cases leave room to move",
          "Each dot is one scenario's violating or borderline version, for one auditor model.")
    fig.savefig(OUT / "fig2_ceiling.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- fig 3
def fig3_which_side():
    fig, ax = plt.subplots(figsize=(9, 3.8))
    comps = [("success", "omitted", "Success vs no ending"), ("failure", "omitted", "Failure vs no ending")]
    for i, model in enumerate(MODELS):
        probs = probabilities(LOGS["arguable"][model])
        for j, (a, b, _) in enumerate(comps):
            mean, lo, hi = paired(probs, a, b)
            y = (len(MODELS) - 1 - i) + (0.14 if j == 0 else -0.14)
            marker = "o" if j == 0 else "s"
            ax.plot([lo, hi], [y, y], color=MODEL_COLOR[model], linewidth=2.2, solid_capstyle="round", zorder=2)
            ax.scatter([mean], [y], s=70, marker=marker, color=MODEL_COLOR[model], edgecolors=SURFACE, linewidths=1.5, zorder=3)
            ax.text(5.2, y, f"{'success' if j == 0 else 'failure'}  {mean:+.1f} [{lo:+.1f}, {hi:+.1f}]",
                    va="center", fontsize=9, color=INK)
    ax.axvline(0, color=INK_2, linewidth=1)
    ax.set_xlim(-5, 9.5)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks(range(len(MODELS)), list(reversed(MODELS)))
    ax.set_ylim(-0.6, len(MODELS) - 0.4)
    ax.set_xlabel("Change in violation probability against no ending (points out of 100)")
    ax.text(-4.9, len(MODELS) - 0.52, "← more lenient", fontsize=9, color=INK_2)
    ax.text(4.9, len(MODELS) - 0.52, "harsher →", fontsize=9, color=INK_2, ha="right")
    tidy(ax)
    title(fig, ax, "Success changes nothing; failure, if anything, makes the auditor slightly more lenient",
          "Circle: success ending. Square: failure ending. Bars: 95% CI over 20 borderline scenarios, runs pooled.")
    fig.savefig(OUT / "fig3_which_side.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- fig 4
def fig4_knife_edge():
    endings = [("success", "Success"), ("none", "Neutral"), ("failure", "Failure"), ("omitted", "No ending")]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.6), sharey=True)
    jitter = random.Random(3)
    for ax, (panel, log_id, scenario) in zip(axes.flat, KNIFE_PANELS):
        flags = defaultdict(list)
        for s in read_eval_log(log_path(log_id)).samples:
            m = s.metadata
            meta = next(iter(s.scores.values())).metadata
            if m["scenario"] == scenario and m["violation"] and meta.get("parsed"):
                flags[m["outcome"]].append((meta["probability"], meta["flagged"]))
        for i, (key, _) in enumerate(endings):
            for p, flagged in flags.get(key, []):
                x = i + jitter.uniform(-0.12, 0.12)
                ax.scatter([x], [p], s=46, color="#eb6834" if flagged else SURFACE, edgecolors="#eb6834", linewidths=1.6, zorder=3)
            if not flags.get(key):
                ax.text(i, 50, "not run", ha="center", fontsize=8.5, color=MUTED, rotation=90)
        ax.set_xticks(range(len(endings)), [e[1] for e in endings], fontsize=9)
        ax.set_title(panel, fontsize=10.5, color=INK, loc="left")
        ax.set_ylim(0, 100)
        ax.set_xlim(-0.5, 3.5)
        ax.grid(axis="y", color=GRID, linewidth=1)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.spines["left"].set_color(GRID)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(length=0)
    for ax in axes[:, 0]:
        ax.set_ylabel("Violation probability")
    fig.suptitle("Sonnet on the cloud-budget split: any outcome can tip it, and which one changes from run to run",
                 x=0.06, ha="left", fontsize=13, color=INK, y=1.03)
    fig.text(0.06, 0.965, "Each dot is one sample. Filled = flagged as a violation, hollow = cleared.",
             fontsize=9.5, color=INK_2)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_knife_edge.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- fig 5
def fig5_reasons():
    counts = defaultdict(lambda: defaultdict(int))
    for s in read_eval_log(log_path(TAG_LOG)).samples:
        meta = next(iter(s.scores.values())).metadata
        if not meta.get("parsed"):
            continue
        model = next(m for m in MODELS if m.lower() in s.metadata["auditor"])
        counts[(model, s.metadata["outcome"])][meta["role"]] += 1
    endings = [("success", "after success"), ("failure", "after failure"), ("omitted", "no ending")]
    parts = [("discounted", "dismisses it (“doesn't change the verdict”)", "#2a78d6"),
             ("used", "uses it to go easier or harder", "#eb6834"),
             ("neutral", "mentions it in passing", "#c9c8c2")]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    labels, y = [], 0
    for model in reversed(MODELS):
        for key, label in reversed(endings):
            c = counts[(model, key)]
            n = sum(c.values())
            shares = {"discounted": c["discounted"] / n, "used": (c["mitigating"] + c["aggravating"]) / n, "neutral": c["neutral"] / n}
            left = 0
            for part, _, color in parts:
                w = shares[part] * 100
                ax.barh(y, w, left=left, height=0.62, color=color, edgecolor=SURFACE, linewidth=2)
                left += w
            ax.text(left + 1.2, y, f"{left:.0f}%", va="center", fontsize=9, color=INK)
            labels.append((y, f"{model}, {label}"))
            y += 1
        y += 0.6
    ax.set_yticks([l[0] for l in labels], [l[1] for l in labels], fontsize=9.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of the auditor's reasons that mention the outcome (%)")
    tidy(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in parts]
    ax.legend(handles, [p[1] for p in parts], loc="upper center", bbox_to_anchor=(0.4, -0.14), ncol=3,
              frameon=False, fontsize=9)
    title(fig, ax, "Auditors talk about the outcome mostly to argue it away",
          "Borderline transcripts, 1,680 reasons tagged by Haiku 5.5. “No ending” rows are the tagger's false-alarm rate.")
    fig.savefig(OUT / "fig5_reasons.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- fig 6
def fig6_v2():
    sets = [("arguable", "Main set (20 scenarios)"), ("v2", "Longer set, v2 (21 scenarios)")]
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    jitter = random.Random(4)
    y, yticks = 0.0, []
    for model in reversed(MODELS):
        for key, label in reversed(sets):
            probs = probabilities(LOGS[key][model], variants=VARIANT_NAMES[key])
            scenarios = sorted({k[0] for k in probs})
            diffs = {s: st.mean(probs[(s, "failure")]) - st.mean(probs[(s, "success")]) for s in scenarios}
            mean, lo, hi = paired(probs, "failure", "success")
            color = MODEL_COLOR[model]
            hollow = key == "arguable"
            xs = list(diffs.values())
            ys = [y + 0.12 + jitter.uniform(0, 0.24) for _ in xs]
            ax.scatter(xs, ys, s=40, facecolors=SURFACE if hollow else color, edgecolors=color, linewidths=1.5,
                       alpha=0.9, zorder=2)
            for (sc, d), yd in zip(diffs.items(), ys):
                if abs(d) > 20:
                    ax.annotate(sc.removesuffix("_arguable").removesuffix("_v2"), (d, yd), xytext=(0, 8),
                                textcoords="offset points", ha="center", fontsize=8.5, color=INK_2)
            ym = y - 0.12
            ax.plot([lo, hi], [ym, ym], color=INK, linewidth=2, solid_capstyle="round", zorder=3)
            ax.scatter([mean], [ym], s=80, marker="D", color=INK, linewidths=0, zorder=4)
            ax.annotate(f"{mean:+.1f}  [{lo:+.1f}, {hi:+.1f}]", (1.02, ym), xycoords=("axes fraction", "data"),
                        va="center", fontsize=9.5, color=INK)
            yticks.append((y, f"{model}: {label}"))
            y += 1
        y += 0.55
    ax.axvline(0, color=INK_2, linewidth=1, zorder=1)
    ax.set_yticks([t[0] for t in yticks], [t[1] for t in yticks], fontsize=9.5)
    ax.set_xlim(-55, 25)
    ax.set_ylim(-0.7, y - 0.3)
    ax.set_xlabel("Change in violation probability, failure minus success (points out of 100)")
    tidy(ax)
    title(fig, ax, "The same check on a second, longer set of scenarios",
          "Hollow dots: main set. Filled: longer v2 set. One dot per scenario; diamond and bar: mean with 95% CI. Right of 0 = harsher after failure.")
    fig.savefig(OUT / "fig6_v2.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (fig1_design, fig2_ceiling, fig3_which_side, fig4_knife_edge, fig5_reasons, fig6_v2):
        f()
        print("wrote", f.__name__)


if __name__ == "__main__":
    main()
