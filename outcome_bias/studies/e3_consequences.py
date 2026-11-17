"""E3: does it matter what the agent's shortcut caused?

The rule-bending version of the 26 agent transcripts, ending with a consequence of the shortcut: it
paid off (2 wordings), the harm the rule guards against happened (2 wordings), or no ending
("omitted"). Clear violations have one wording of each. Seven questions.

Stimuli: outcome_bias/stimuli/agent_transcripts/, outcome_bias/stimuli/e3_consequences/
Plan: docs/1_main_experiments/plan.md      Results: docs/1_main_experiments/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import agent_transcript, ask, follow_up, item

EXP = "e3"


def endings(scenario_id):
    """[(cond, wording, ending line)]: no ending first, then each payoff and harm wording."""
    cells = [("omitted", 0, None)]
    for cond in ("payoff", "harm"):
        for w, text in enumerate(stimuli.e3_endings()[scenario_id][cond]):
            cells.append((cond, w, follow_up(text)))
    return cells


def build():
    items = []
    questions = stimuli.agent_questions()
    for s in stimuli.agent_scenarios():
        for cond, w, ending in endings(s.id):
            for q in questions.values():
                items.append(
                    item(
                        EXP,
                        s.id,
                        s.kind,
                        cond,
                        w,
                        q.name,
                        stimuli.agent_system(),
                        ask(agent_transcript(s, False, ending), q.text),
                        q.lo,
                        q.hi,
                    )
                )
    return items
