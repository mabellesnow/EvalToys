"""Follow-up D: does harm still move the verdict when the auditor already knows what the rule is for?

E3's 21 borderline transcripts and endings, with one sentence after the policy saying why the relevant
rule exists. Four questions: violation, decision quality, blame, risk at the time.

Stimuli: outcome_bias/stimuli/followup_rule_purpose/ (plus E3's)
Plan: docs/2_follow_ups/plan.md (part D)      Results: docs/2_follow_ups/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import agent_transcript, ask, item
from outcome_bias.studies.e3_consequences import endings

EXP = "e3"
QUESTIONS = ("violation", "quality", "blame", "risk")


def build():
    items = []
    questions = stimuli.agent_questions()
    purposes = stimuli.followup_rule_purposes()
    for s in stimuli.agent_scenarios():
        if s.kind != "borderline":
            continue
        for cond, w, ending in endings(s.id):
            for name in QUESTIONS:
                q = questions[name]
                body = agent_transcript(s, False, ending, policy_note=purposes[s.id])
                items.append(item(EXP, s.id, "borderline", cond, w, q.name, stimuli.agent_system(),
                                  ask(body, q.text), q.lo, q.hi, study="s2d"))
    return items
