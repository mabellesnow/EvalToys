"""The stimuli: everything the models read, as data files in this folder, and the functions that load them.
This module only reads files; how they become prompts is in prompts.py.

  agent_transcripts/        the 26 agent transcripts (E2, E3 and two follow-ups), their questions and system prompt
  e1_people/                E1 stories about people
  e3_consequences/          E3 endings (payoff, harm)
  e4_buried_violation/      E4 policy, target tickets, routine tickets, operator notes
  e5_intent/                E5 actions and monitor questions
  followup_labelled_scale/  the labelled violation question, and the "ignore what happened afterwards" instruction
  followup_neutral_note/    neutral follow-up notes (the control for E5)
  followup_rule_purpose/    one "why this rule exists" sentence per scenario
  hashes.json               SHA-256 of every file above, checked by python -m outcome_bias.verify
"""

from dataclasses import dataclass, field
from functools import cache

import yaml

from outcome_bias.paths import STIMULI


def _yaml(rel):
    return yaml.safe_load((STIMULI / rel).read_text(encoding="utf-8"))


def _text(rel):
    return (STIMULI / rel).read_text(encoding="utf-8")


@dataclass(frozen=True)
class Question:
    name: str
    text: str
    lo: float
    hi: float


def _questions(raw):
    return {name: Question(name, q["text"], q["min"], q["max"]) for name, q in raw.items()}


# ---------------------------------------------------------------- agent transcripts (E2, E3, two follow-ups)
@dataclass(frozen=True)
class AgentScenario:
    """One agent transcript in two versions that share a context and a wrap-up.

    kind is "borderline" (arguable shortcut, no ground truth) or "clear" (an obvious violation).
    endings holds E2's task-level endings: success, failure, none.
    """

    id: str
    kind: str
    policy: str
    task: str
    context: list = field(default_factory=list)
    borderline: list = field(default_factory=list)
    compliant: list = field(default_factory=list)
    wrapup: list = field(default_factory=list)
    endings: dict = field(default_factory=dict)

    def steps(self, follows_rule: bool) -> list[str]:
        middle = self.compliant if follows_rule else self.borderline
        return [*self.context, *middle, *self.wrapup]


@cache
def agent_scenarios() -> tuple[AgentScenario, ...]:
    """The 21 borderline scenarios, then the 5 clear violations, in their fixed order."""
    out = []
    for kind in ("borderline", "clear"):
        out += [AgentScenario(kind=kind, **s) for s in _yaml(f"agent_transcripts/scenarios_{kind}.yaml")]
    return tuple(out)


@cache
def agent_questions() -> dict[str, Question]:
    return _questions(_yaml("agent_transcripts/questions.yaml")["questions"])


@cache
def agent_questions_for_compliant() -> tuple[str, ...]:
    return tuple(_yaml("agent_transcripts/questions.yaml")["asked_of_compliant_version"])


@cache
def agent_system() -> str:
    return _text("agent_transcripts/system.txt")


@cache
def e3_endings() -> dict:
    """{scenario id: {"payoff": [wordings], "harm": [wordings]}}"""
    return _yaml("e3_consequences/endings.yaml")


# ---------------------------------------------------------------- E1
@cache
def e1_vignettes() -> list[dict]:
    return _yaml("e1_people/vignettes.yaml")


@cache
def e1_questions() -> dict[str, Question]:
    return _questions(_yaml("e1_people/questions.yaml"))


@cache
def e1_system() -> str:
    return _text("e1_people/system.txt")


# ---------------------------------------------------------------- E4
@cache
def e4_policy() -> str:
    return _text("e4_buried_violation/policy.txt")


@cache
def e4_operator_notes() -> dict:
    """{"success": note, "failure": note, "none": None}"""
    return _yaml("e4_buried_violation/operator_notes.yaml")


@cache
def e4_targets() -> list[dict]:
    return _yaml("e4_buried_violation/targets.yaml")


@cache
def e4_fillers() -> list[tuple[str, list[str]]]:
    """The routine tickets as (title, steps), in their fixed order (sessions are sampled from it)."""
    return [(f["title"], f["steps"]) for f in _yaml("e4_buried_violation/fillers.yaml")]


@cache
def e4_system() -> str:
    return _text("e4_buried_violation/system.txt")


# ---------------------------------------------------------------- E5
@cache
def e5_actions() -> list[dict]:
    return _yaml("e5_intent/actions.yaml")


@cache
def e5_questions() -> dict[str, Question]:
    return _questions(_yaml("e5_intent/questions.yaml"))


@cache
def e5_system() -> str:
    return _text("e5_intent/system.txt")


# ---------------------------------------------------------------- follow-ups
@cache
def followup_scale_questions() -> dict:
    """{"labelled": the labelled violation question, "ignore_prefix": the instruction put in front of it}"""
    return _yaml("followup_labelled_scale/questions.yaml")


@cache
def followup_neutral_notes() -> list[str]:
    return _yaml("followup_neutral_note/notes.yaml")


@cache
def followup_rule_purposes() -> dict[str, str]:
    return _yaml("followup_rule_purpose/purposes.yaml")
