"""Follow-up B (called X1 when it ran on Haiku): is E3's harm effect on the verdict a product of the unlabelled 0-100 scale?

E3's items, violation question only, asked in one of two ways:
  labelled   each range of the scale described (0-10 clearly followed ... 91-100 clearly broke it)
  ignore     the same, after: "Judge only what the agent did ... What happened afterwards does not
             change whether the policy was broken."

Stimuli: outcome_bias/stimuli/followup_labelled_scale/ (plus E3's)
Plan: docs/1_main_experiments/plan.md (follow-up X1) and docs/2_follow_ups/plan.md (part B)
Results: docs/1_main_experiments/results.md (Haiku) and docs/2_follow_ups/results.md (Sonnet, Opus, re-run)
"""

from outcome_bias import stimuli
from outcome_bias.prompts import agent_transcript, ask, item
from outcome_bias.studies.e3_consequences import endings

EXP = "e3"
VARIANTS = ("labelled", "ignore")


def question(variant):
    q = stimuli.followup_scale_questions()
    return q["labelled"] if variant == "labelled" else q["ignore_prefix"] + q["labelled"]


def build(variant: str = "labelled"):
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}")
    items = []
    for s in stimuli.agent_scenarios():
        for cond, w, ending in endings(s.id):
            items.append(item(EXP, s.id, s.kind, cond, w, "violation", stimuli.agent_system(),
                              ask(agent_transcript(s, False, ending), question(variant)), 0, 100,
                              study="x1", variant=variant))
    return items
