"""Shared figure style: palette, fonts, and small helpers used by every figure module."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from outcome_bias.paths import FIGURES  # noqa: E402

# reference palette, light mode
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e4e3df"
PANEL = "#f1f0ec"
MODEL_COLOR = {"Haiku": "#2a78d6", "Sonnet": "#eb6834", "Opus": "#1baf7a"}  # categorical slots 1-3
MODELS = ("Haiku", "Sonnet", "Opus")
OUT = FIGURES

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11, "text.color": INK, "axes.labelcolor": INK_2,
    "xtick.color": INK_2, "ytick.color": INK, "axes.edgecolor": GRID, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})


def tidy(ax, xgrid=True):
    """No box, no tick marks, a light vertical grid."""
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=1)
        ax.set_axisbelow(True)


def title(fig, ax, text, sub):
    ax.set_title(text, loc="left", fontsize=13, color=INK, pad=26)
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9.5, color=INK_2)


def box(ax, x, y, w, h, text, face=PANEL, edge=GRID, size=9.5, color=INK, weight="normal", align="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=face, ec=edge, lw=1))
    tx = x + w / 2 if align == "center" else x + 0.12
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=size, color=color, weight=weight, linespacing=1.4)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, shrinkA=0, shrinkB=0))


def save(fig, rel):
    """Save under figures/<rel> at 200 dpi."""
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path
