"""E1, positive control: are short stories about people judged by how they turned out?

12 stories (4 risky decisions with stated odds, 4 skipped duties, 4 acts of carelessness), each with a
good ending, a bad ending, or none. Five questions: decision quality, wrongness, blame, penalty, risk.

Stimuli: outcome_bias/stimuli/e1_people/      Plan: docs/1_main_experiments/plan.md      Results: docs/1_main_experiments/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import ask, item

EXP = "e1"
CONDITIONS = ("good", "bad", "none")


def build():
    items = []
    questions = stimuli.e1_questions()
    for v in stimuli.e1_vignettes():
        for cond in CONDITIONS:
            story = v["text"] if cond == "none" else f"{v['text']} {v[cond]}"
            for q in questions.values():
                text = q.text.format(person=v["person"], act=v["act"], harm=v["harm"])
                items.append(
                    item(
                        EXP,
                        v["id"],
                        v["family"],
                        cond,
                        0,
                        q.name,
                        stimuli.e1_system(),
                        ask(story, text),
                        q.lo,
                        q.hi,
                    )
                )
    return items
