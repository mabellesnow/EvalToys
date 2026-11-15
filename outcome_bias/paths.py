"""Where things live. Every other module takes its paths from here."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STIMULI = ROOT / "stimuli"  # everything the models read: scenarios, endings, questions, system prompts
DOCS = ROOT / "docs"  # plans, results, the write-up
FIGURES = ROOT / "figures"
LOGS = ROOT / "logs"  # Inspect logs (not in git)
RUN_INDEX = LOGS / "exp_runs.tsv"  # one row per run: label, exp, arm, model, log file
FREEZE = DOCS / "freeze.json"  # SHA-256 of every stimulus file, written when a plan is frozen
