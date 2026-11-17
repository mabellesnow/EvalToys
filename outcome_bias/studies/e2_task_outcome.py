"""E2: does it matter how the task went, when the agent's shortcut didn't cause it?

26 agent transcripts (21 borderline, 5 clear violations), each in a rule-bending and a compliant
version, with E2's task-level endings: success, failure, or none ("omitted"). Seven questions for the
rule-bending version; four for the compliant one.

Stimuli: outcome_bias/stimuli/agent_transcripts/     Plan: docs/1_main_experiments/plan.md      Results: docs/1_main_experiments/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import agent_transcript, ask, item

EXP = "e2"
CONDITIONS = ("success", "failure", "omitted")


def build():
    items = []
    questions = stimuli.agent_questions()
    for s in stimuli.agent_scenarios():
        for follows_rule in (False, True):
            version = "compliant" if follows_rule else s.kind
            for cond in CONDITIONS:
                ending = None if cond == "omitted" else s.endings[cond]
                for q in questions.values():
                    if (
                        follows_rule
                        and q.name not in stimuli.agent_questions_for_compliant()
                    ):
                        continue
                    items.append(
                        item(
                            EXP,
                            s.id,
                            version,
                            cond,
                            0,
                            q.name,
                            stimuli.agent_system(),
                            ask(agent_transcript(s, follows_rule, ending), q.text),
                            q.lo,
                            q.hi,
                        )
                    )
    return items
