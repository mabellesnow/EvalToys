"""E5: does chance harm make a questionable agent action look deliberate?

12 actions that could be an honest mistake or deliberate. The ending says whether harm followed
(2 wordings), that no harm followed (2 wordings), or nothing. Both are down to chance. A monitor rates
intent, suspicion and what should happen next.

Stimuli: stimuli/e5_intent/      Plan: docs/e1_e5/plan.md      Results: docs/e1_e5/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import ask, e5_transcript, item

EXP = "e5"


def endings(action, extra=()):
    """[(cond, wording, ending text)]: none first, then harm and noharm, then any extra (cond, [texts])."""
    cells = [("none", 0, None)]
    for cond, texts in (("harm", action["harm"]), ("noharm", action["noharm"]), *extra):
        for w, text in enumerate(texts):
            cells.append((cond, w, text))
    return cells


def build(extra_endings=(), **extra_metadata):
    items = []
    questions = stimuli.e5_questions()
    for a in stimuli.e5_actions():
        for cond, w, ending in endings(a, extra_endings):
            body = e5_transcript(a, ending)
            for q in questions.values():
                items.append(item(EXP, a["id"], "ambiguous", cond, w, q.name, stimuli.e5_system(),
                                  ask(body, q.text), q.lo, q.hi, **extra_metadata))
    return items
