"""Every study the project has run, in one table. Each study module builds its items from stimuli/.

  study id             exp  question                                                   plan
  e1_people            e1   do these models judge people by outcomes? (positive control) docs/e1_e5
  e2_task_outcome      e2   does how the task went change how a shortcut is judged?      docs/e1_e5
  e3_consequences      e3   does what the shortcut caused change it?                     docs/e1_e5
  e4_buried_violation  e4   does a good-session note hide a buried violation?            docs/e1_e5
  e5_intent            e5   does chance harm make an action look deliberate?             docs/e1_e5
  x1_labelled_scale    e3   is E3's verdict shift the unlabelled scale? does an instruction remove it?
                                                                                         docs/e1_e5, docs/stage2
  s2c_neutral_note     e5   is E5's "no harm" relief the outcome or any note?           docs/stage2
  s2d_rule_purpose     e3   does harm still move the verdict when the rule's purpose is stated?  docs/stage2

"exp" is the code written into every item's metadata and the run index (logs/exp_runs.tsv); the
analysis groups by it. Stage 2 A (the Opus re-runs) re-ran e2 and e3; it has no study of its own.
The Part 1 pilot lives in outcome_bias/part1/.
"""

from dataclasses import dataclass, field
from typing import Callable

from outcome_bias.studies import (
    e1_people,
    e2_task_outcome,
    e3_consequences,
    e4_buried_violation,
    e5_intent,
    s2c_neutral_note,
    s2d_rule_purpose,
    x1_labelled_scale,
)


@dataclass(frozen=True)
class Study:
    id: str
    exp: str
    build: Callable
    epochs: int  # samples per item, as pre-registered
    plan: str
    results: str
    params: dict = field(default_factory=dict)  # extra task parameters and their defaults


STUDIES = {
    s.id: s
    for s in [
        Study("e1_people", "e1", e1_people.build, 5, "docs/e1_e5/plan.md", "docs/e1_e5/results.md"),
        Study("e2_task_outcome", "e2", e2_task_outcome.build, 3, "docs/e1_e5/plan.md", "docs/e1_e5/results.md"),
        Study("e3_consequences", "e3", e3_consequences.build, 3, "docs/e1_e5/plan.md", "docs/e1_e5/results.md"),
        Study("e4_buried_violation", "e4", e4_buried_violation.build, 2, "docs/e1_e5/plan.md", "docs/e1_e5/results.md",
              {"n_filler": e4_buried_violation.N_FILLER}),
        Study("e5_intent", "e5", e5_intent.build, 3, "docs/e1_e5/plan.md", "docs/e1_e5/results.md"),
        Study("x1_labelled_scale", "e3", x1_labelled_scale.build, 3, "docs/stage2/plan.md", "docs/stage2/results.md",
              {"variant": "labelled"}),
        Study("s2c_neutral_note", "e5", s2c_neutral_note.build, 3, "docs/stage2/plan.md", "docs/stage2/results.md"),
        Study("s2d_rule_purpose", "e3", s2d_rule_purpose.build, 3, "docs/stage2/plan.md", "docs/stage2/results.md"),
    ]
}
