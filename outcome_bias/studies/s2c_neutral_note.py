"""Stage 2 C: is E5's drop in suspicion after "no harm" an effect of the outcome, or of any follow-up note?

All of E5, plus a fourth ending: a neutral follow-up note that says nothing about harm (2 wordings).
All four endings run together, so they can be compared within one run.

Stimuli: stimuli/s2c_neutral_note/ (plus E5's)
Plan: docs/stage2/plan.md (part C)      Results: docs/stage2/results.md
"""

from outcome_bias import stimuli
from outcome_bias.studies import e5_intent

EXP = "e5"


def build():
    return e5_intent.build(extra_endings=(("neutral", stimuli.s2c_neutral_notes()),), study="s2c")
