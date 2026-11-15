"""The pilot's scenarios, loaded from stimuli/ into the pilot's Scenario shape.

Set 1 (stimuli/part1_pilot/scenarios_v1.yaml): blatant, subtle, arguable, ambiguous and justified variants.
Set 2 ("v2"): the 26 agent transcripts in stimuli/agent_audit/, later reused by E2 and E3.
Endings describe how the task went, never a consequence of the violation.
"""

from dataclasses import dataclass

from outcome_bias import stimuli

OUTCOMES = ("success", "failure", "none")


@dataclass
class Scenario:
    id: str
    policy: str
    task: str
    steps_violation: list[str]
    steps_clean: list[str]
    endings: dict[str, str]  # success, failure, none
    variant: str = "blatant"


ALL_SCENARIOS = [Scenario(**s) for s in stimuli.part1_scenarios_v1()]
V2_SCENARIOS = [
    Scenario(id=s.id, policy=s.policy, task=s.task, steps_violation=s.steps(False), steps_clean=s.steps(True),
             endings=s.endings, variant=f"v2_{s.kind}")
    for s in stimuli.agent_scenarios()
]
V2_BORDERLINE = [s for s in V2_SCENARIOS if s.variant == "v2_borderline"]
V2_CLEAR = [s for s in V2_SCENARIOS if s.variant == "v2_clear"]
EVERY_SCENARIO = ALL_SCENARIOS + V2_SCENARIOS
