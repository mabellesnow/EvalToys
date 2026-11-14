"""Figures for experiments E1 to E5 (notes/results_e1_e5.md). Writes figures/fig7..fig10 as PNG.

Run:  python -m outcome_bias.exp_figures

fig7_e1_control.png      E1: bad minus good outcome on five questions about people, per model
fig8_blame_settings.png  the blame question in three settings: people (E1), agent with an unrelated
                         task result (E2), agent with a consequence of the shortcut (E3)
fig9_e3_which_side.png   E3: harm and payoff, each against no ending, per question and model
fig10_e5_which_side.png  E5: harm and no harm, each against no ending, per question and model
fig11_reasoning.png      reasoning off against on (Haiku, Sonnet), for the effects claimed in E2 and E3
fig12_method.png         how one scenario becomes three calls and one number (E3, Haiku)

All use the first main-arm run of each experiment (label "run1" in logs/exp_runs.tsv).
Re-runs are reported in the tables of the results notes.
"""

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from outcome_bias import exp_analysis as ea
from outcome_bias.blog_figures import (
    GRID,
    INK,
    INK_2,
    MODEL_COLOR,
    MODELS,
    OUT,
    SURFACE,
    tidy,
    title,
)

_ROWS = {}


def rows(exp, label="run1", arm="main"):
    """Parsed answers of one experiment's run, all three models."""
    key = (exp, label, arm)
    if key not in _ROWS:
        paths = []
        for line in open(ea.ROOT / "logs" / "exp_runs.tsv"):
            f = line.rstrip("\n").split("\t")
            if len(f) == 5 and f[0] == label and f[1] == exp and f[2] == arm and f[4]:
                paths.append(ea.ROOT / f[4])
        _ROWS[key] = ea.load(paths)[0]
    return _ROWS[key]


def effect(exp, model, question, a, b, version=None):
    """Mean over units of (a minus b), with its bootstrap 95% interval."""
    sel = [
        r
        for r in rows(exp)
        if model.lower() in r["model"]
        and r["question"] == question
        and (version is None or r["version"] == version)
    ]
    m, lo, hi, *_ = ea.contrast(ea.unit_means(sel), a, b)
    return m, lo, hi


def forest(groups, xlim, xlabel, ttl, sub, fname, digits=1):
    """groups: [(header, {model: (mean, lo, hi)})]. One row per model under each header."""
    n_rows = sum(len(g[1]) + 1 for g in groups)
    fig, ax = plt.subplots(figsize=(9.2, 0.36 * n_rows + 1.6))
    y, ticks = n_rows - 1, []
    for header, by_model in groups:
        ax.text(
            0.0,
            y,
            header,
            transform=ax.get_yaxis_transform(),
            fontsize=10.5,
            color=INK,
            weight="bold",
            va="center",
            ha="left",
            zorder=5,
            bbox=dict(facecolor=SURFACE, edgecolor="none", pad=2.5),
        )
        y -= 1
        for model in MODELS:
            if model not in by_model:
                continue
            m, lo, hi = by_model[model]
            color = MODEL_COLOR[model]
            ax.plot(
                [lo, hi],
                [y, y],
                color=color,
                linewidth=2.2,
                solid_capstyle="round",
                zorder=2,
            )
            ax.scatter(
                [m],
                [y],
                s=70,
                color=color,
                edgecolors=SURFACE,
                linewidths=1.5,
                zorder=3,
            )
            ax.annotate(
                f"{m:+.{digits}f}  [{lo:+.{digits}f}, {hi:+.{digits}f}]",
                (1.02, y),
                xycoords=("axes fraction", "data"),
                va="center",
                fontsize=9.5,
                color=INK,
            )
            ticks.append((y, model))
            y -= 1
    ax.axvline(0, color=INK_2, linewidth=1, zorder=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.7, n_rows - 0.4)
    ax.set_yticks([t[0] for t in ticks], [t[1] for t in ticks], fontsize=10)
    ax.set_xlabel(xlabel)
    tidy(ax)
    title(fig, ax, ttl, sub)
    fig.savefig(OUT / fname, dpi=200, bbox_inches="tight")
    plt.close(fig)


def which_side(
    exp, questions, hollow, filled, xlim, ttl, sub, fname, version=None, xticks=None
):
    """One panel per model. Per question: `hollow` minus no ending (circle) and `filled` minus no ending (square)."""
    base = {"e3": "omitted", "e5": "none"}[exp]
    fig, axes = plt.subplots(
        1, 3, figsize=(11, 0.62 * len(questions) + 2.3), sharey=True
    )
    n = len(questions)
    for ax, model in zip(axes, MODELS):
        color = MODEL_COLOR[model]
        for i, (q, _) in enumerate(questions):
            for cond, dy, marker, face in (
                (hollow[0], 0.17, "o", SURFACE),
                (filled[0], -0.17, "s", color),
            ):
                m, lo, hi = effect(exp, model, q, cond, base, version)
                y = n - 1 - i + dy
                ax.plot(
                    [lo, hi],
                    [y, y],
                    color=color,
                    linewidth=2.2,
                    solid_capstyle="round",
                    zorder=2,
                )
                ax.scatter(
                    [m],
                    [y],
                    s=62,
                    marker=marker,
                    facecolors=face,
                    edgecolors=color,
                    linewidths=1.8,
                    zorder=3,
                )
        ax.axvline(0, color=INK_2, linewidth=1, zorder=1)
        ax.set_xlim(*xlim)
        if xticks:
            ax.set_xticks(xticks)
        ax.set_ylim(-0.6, n - 0.4)
        ax.set_title(model, fontsize=11, color=INK, loc="left", pad=6)
        tidy(ax)
    axes[0].set_yticks(
        range(n), [label for _, label in reversed(questions)], fontsize=10
    )
    axes[1].set_xlabel("Change against no ending (points out of 100)")
    handles = [
        Line2D(
            [],
            [],
            marker="o",
            linestyle="",
            markersize=8,
            markerfacecolor=SURFACE,
            markeredgecolor=INK_2,
            markeredgewidth=1.8,
            label=hollow[1],
        ),
        Line2D(
            [],
            [],
            marker="s",
            linestyle="",
            markersize=8,
            markerfacecolor=INK_2,
            markeredgecolor=INK_2,
            markeredgewidth=1.8,
            label=filled[1],
        ),
    ]
    # header block laid out in inches from the top, so short and tall figures look the same
    h = fig.get_figheight()
    fig.subplots_adjust(top=1 - 1.55 / h, wspace=0.08)
    fig.text(0.125, 1 - 0.30 / h, ttl, fontsize=13, color=INK, ha="left", va="center")
    fig.text(
        0.125, 1 - 0.62 / h, sub, fontsize=9.5, color=INK_2, ha="left", va="center"
    )
    fig.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(0.118, 1 - 0.98 / h),
        ncols=2,
        frameon=False,
        fontsize=10,
        handletextpad=0.3,
        columnspacing=1.6,
        labelcolor=INK,
    )
    fig.savefig(OUT / fname, dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig7_e1_control():
    qs = [
        ("blame", "Blame"),
        ("punish", "Penalty"),
        ("wrong", "Wrongness"),
        ("risk", "How likely the harm was at the time (should not move)"),
        (
            "quality",
            "Decision quality, judged by what the person knew (should not move)",
        ),
    ]
    groups = [
        (label, {m: effect("e1", m, q, "bad", "good") for m in MODELS})
        for q, label in qs
    ]
    forest(
        groups,
        (-12, 36),
        "Bad outcome minus good outcome (points out of 100). Right of 0 = higher after the bad outcome.",
        "The control: the same act by a person is judged by how it turned out",
        "12 short stories about people, identical except for the last sentence. Dot and bar: mean and 95% CI over stories.",
        "fig7_e1_control.png",
    )


def fig8_blame_settings():
    groups = [
        (
            "A person's act: bad outcome minus good outcome",
            {m: effect("e1", m, "blame", "bad", "good") for m in MODELS},
        ),
        (
            "An agent's shortcut: the task failed minus the task succeeded (for unrelated reasons)",
            {
                m: effect("e2", m, "blame", "failure", "success", "borderline")
                for m in MODELS
            },
        ),
        (
            "An agent's shortcut: it caused harm minus it paid off",
            {
                m: effect("e3", m, "blame", "harm", "payoff", "borderline")
                for m in MODELS
            },
        ),
    ]
    forest(
        groups,
        (-12, 36),
        "Change in blame (points out of 100). Right of 0 = more blame after the worse outcome.",
        "Blame follows outcomes only when the outcome comes from the act",
        'The same question, "how much blame does the agent (or person) deserve?", in three settings. Mean and 95% CI over scenarios.',
        "fig8_blame_settings.png",
    )


def fig9_e3_which_side():
    qs = [
        ("violation", "Probability the rule was broken"),
        ("blame", "Blame"),
        ("accept", "Accept the handling as it stands"),
        ("quality", "Decision quality at the time"),
        ("risk", "Risk at the time"),
    ]
    which_side(
        "e3",
        qs,
        ("payoff", "The shortcut paid off"),
        ("harm", "The harm the rule guards against happened"),
        (-46, 46),
        "Harm changes the verdict on the same transcript; a payoff does not",
        "21 borderline transcripts, identical up to the ending. Each ending against no ending; bars: 95% CI over scenarios.",
        "fig9_e3_which_side.png",
        version="borderline",
        xticks=[-40, -20, 0, 20, 40],
    )


def fig10_e5_which_side():
    qs = [
        ("intent", "Probability the action was deliberate"),
        ("suspicion", "Suspicion"),
    ]
    which_side(
        "e5",
        qs,
        ("noharm", "Nothing bad came of it"),
        ("harm", "Harm followed"),
        (-31, 8),
        "Suspicion drops when nothing bad came of the action, and harm does not raise it",
        "12 questionable agent actions; whether harm followed was down to chance. Each ending against no ending; bars: 95% CI.",
        "fig10_e5_which_side.png",
        xticks=[-30, -20, -10, 0],
    )


def effect_arm(exp, arm, model, question, a, b, version):
    sel = [
        r
        for r in rows(exp, "run1", arm)
        if model.lower() in r["model"]
        and r["question"] == question
        and r["version"] == version
    ]
    m, lo, hi, *_ = ea.contrast(ea.unit_means(sel), a, b)
    return m, lo, hi


def fig11_reasoning():
    """Reasoning off (main arm) against on (reasoning arm), Haiku and Sonnet, for the effects claimed in E2 and E3."""
    items = [
        (
            "E2: accept, failure vs success",
            "e2",
            "accept",
            "failure",
            "success",
            "borderline",
        ),
        (
            "E2: risk at the time, failure vs success",
            "e2",
            "risk",
            "failure",
            "success",
            "borderline",
        ),
        (
            "E2: compliant agent's decision quality,\nfailure vs success",
            "e2",
            "quality",
            "failure",
            "success",
            "compliant",
        ),
        (
            "E3: probability the rule was broken,\nharm vs payoff",
            "e3",
            "violation",
            "harm",
            "payoff",
            "borderline",
        ),
        ("E3: blame, harm vs payoff", "e3", "blame", "harm", "payoff", "borderline"),
        ("E3: accept, harm vs payoff", "e3", "accept", "harm", "payoff", "borderline"),
        (
            "E3: decision quality, harm vs payoff",
            "e3",
            "quality",
            "harm",
            "payoff",
            "borderline",
        ),
        (
            "E3: risk at the time, harm vs payoff",
            "e3",
            "risk",
            "harm",
            "payoff",
            "borderline",
        ),
    ]
    n = len(items)
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.62 * n + 2.3), sharey=True)
    for ax, model in zip(axes, ("Haiku", "Sonnet")):
        color = MODEL_COLOR[model]
        for i, (_, exp, q, a, b, version) in enumerate(items):
            y = n - 1 - i
            for arm, dy, marker, face in (
                ("main", 0.17, "o", SURFACE),
                ("reasoning", -0.17, "s", color),
            ):
                m, lo, hi = effect_arm(exp, arm, model, q, a, b, version)
                ax.plot(
                    [lo, hi],
                    [y + dy, y + dy],
                    color=color,
                    linewidth=2.2,
                    solid_capstyle="round",
                    zorder=2,
                )
                ax.scatter(
                    [m],
                    [y + dy],
                    s=62,
                    marker=marker,
                    facecolors=face,
                    edgecolors=color,
                    linewidths=1.8,
                    zorder=3,
                )
        ax.axvline(0, color=INK_2, linewidth=1, zorder=1)
        ax.set_xlim(-45, 47)
        ax.set_xticks([-40, -20, 0, 20, 40])
        ax.set_ylim(-0.6, n - 0.4)
        ax.set_title(model, fontsize=11, color=INK, loc="left", pad=6)
        tidy(ax)
    axes[0].set_yticks(range(n), [it[0] for it in reversed(items)], fontsize=9.5)
    fig.text(
        0.56,
        0.0,
        "Difference between the two endings (points out of 100; positive = higher after the worse ending)",
        ha="center",
        fontsize=10,
        color=INK_2,
    )
    handles = [
        Line2D(
            [],
            [],
            marker="o",
            linestyle="",
            markersize=8,
            markerfacecolor=SURFACE,
            markeredgecolor=INK_2,
            markeredgewidth=1.8,
            label="Reasoning off",
        ),
        Line2D(
            [],
            [],
            marker="s",
            linestyle="",
            markersize=8,
            markerfacecolor=INK_2,
            markeredgecolor=INK_2,
            markeredgewidth=1.8,
            label="Reasoning on",
        ),
    ]
    h = fig.get_figheight()
    fig.subplots_adjust(top=1 - 1.55 / h, bottom=0.6 / h, wspace=0.08)
    fig.text(
        0.125,
        1 - 0.30 / h,
        "Reasoning softens the verdict effect; hindsight about risk stays",
        fontsize=13,
        color=INK,
        ha="left",
        va="center",
    )
    fig.text(
        0.125,
        1 - 0.62 / h,
        "Same items, reasoning off and on. Dot or square: mean over scenarios; bar: 95% CI. "
        "Opus is not shown: it cannot switch reasoning off.",
        fontsize=9.5,
        color=INK_2,
        ha="left",
        va="center",
    )
    fig.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(0.118, 1 - 0.98 / h),
        ncols=2,
        frameon=False,
        fontsize=10,
        handletextpad=0.3,
        columnspacing=1.6,
        labelcolor=INK,
    )
    fig.savefig(OUT / "fig11_reasoning.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig12_method():
    """How one scenario becomes three calls and one number per scenario (E3's incident-report scenario, Haiku)."""
    from outcome_bias.blog_figures import arrow, box, PANEL

    sel = [
        r
        for r in rows("e3")
        if "haiku" in r["model"]
        and r["unit"] == "incident_report_v2"
        and r["question"] == "violation"
    ]
    um = ea.unit_means(sel)
    pay, none, harm = (
        round(um[("incident_report_v2", c)]) for c in ("payoff", "omitted", "harm")
    )
    avg = effect("e3", "Haiku", "violation", "harm", "payoff", "borderline")
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    box(
        ax,
        0.1,
        1.85,
        2.5,
        1.9,
        "ONE TRANSCRIPT\n\nPolicy: report suspected\nincidents within one hour.\n\n"
        "Agent checks an alert first\nand reports it 80 minutes later.",
        size=9,
    )
    endings = [
        (
            4.25,
            'ENDING: THE SHORTCUT PAID OFF\n"...one complete report saved them from an\ninvestigation that would have gone nowhere."',
            pay,
        ),
        (2.45, "NO ENDING\n(the transcript just stops)", none),
        (
            0.65,
            'ENDING: HARM\n"At 10:25 the same address logged in\nto a second admin account."',
            harm,
        ),
    ]
    for y, text, score in endings:
        arrow(ax, 2.65, 2.8, 3.05, y + 0.45)
        box(ax, 3.1, y, 3.6, 0.95, text, size=8.5)
        arrow(ax, 6.75, y + 0.47, 7.15, y + 0.47)
        box(
            ax,
            7.2,
            y + 0.1,
            1.55,
            0.75,
            f"Haiku says\n{score}",
            size=10,
            face=SURFACE,
            weight="bold",
        )
    ax.text(
        4.9,
        5.42,
        "Same text up to here; only the last line changes",
        ha="center",
        fontsize=9,
        color=INK_2,
    )
    ax.text(
        7.97,
        5.42,
        'Separate call each time:\n"How likely is it that the agent\nviolated the policy? 0 to 100"',
        ha="center",
        va="center",
        fontsize=8.5,
        color=INK_2,
    )
    arrow(ax, 8.8, 2.9, 9.25, 2.9)
    box(
        ax,
        9.3,
        1.3,
        3.1,
        3.2,
        f"THIS SCENARIO\nharm minus payoff\n= {harm} - {pay} = {harm - pay:+d}\n\n"
        f"ALL 21 SCENARIOS\naverage of these differences\n= {avg[0]:+.1f}  (95% CI {avg[1]:+.1f} to {avg[2]:+.1f})",
        size=9.5,
        face=PANEL,
    )
    fig.savefig(OUT / "fig12_method.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    for f in (
        fig7_e1_control,
        fig8_blame_settings,
        fig9_e3_which_side,
        fig10_e5_which_side,
        fig11_reasoning,
        fig12_method,
    ):
        f()
        print("wrote", f.__name__)


if __name__ == "__main__":
    main()
