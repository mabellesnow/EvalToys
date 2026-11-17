"""Turn stimuli into the text the model sees, and wrap it as an Inspect sample.

Every prompt is a system message plus one user message:  <body>\\n\\nQUESTION: <question>
"""

import random
import re

from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageUser

from outcome_bias.stimuli import AgentScenario


def follow_up(text: str) -> str:
    return f"FOLLOW-UP NOTE: {text}"


def ask(body: str, question: str) -> str:
    return f"{body}\n\nQUESTION: {question}"


def agent_transcript(s: AgentScenario, follows_rule: bool, ending: str | None, policy_note: str | None = None) -> str:
    """POLICY, then the transcript, then the ending line if there is one.
    policy_note is added on a new line after the policy (follow-up D, followup_rule_purpose)."""
    policy = s.policy if policy_note is None else f"{s.policy}\n{policy_note}"
    lines = [f"USER: {s.task}", *s.steps(follows_rule)] + ([ending] if ending else [])
    return f"POLICY:\n{policy}\n\nTRANSCRIPT:\n" + "\n".join(lines)


def e5_transcript(action: dict, ending: str | None) -> str:
    """The transcript, the ending as a follow-up note, and the action under review."""
    lines = [f"USER: {action['task']}", *action["steps"]] + ([follow_up(ending)] if ending else [])
    return "TRANSCRIPT:\n" + "\n".join(lines) + f"\n\nREVIEW FOCUS: {action['focus']}."


def _renumber(steps, rng):
    """Give a reused routine ticket its own reference numbers (customer, claim, PR ids)."""
    offset = rng.randint(11, 899)

    def bump(m):
        return f"{m.group(1)}{int(m.group(2)) + offset}"

    return [re.sub(r"\b((?:C|A|E|CR|ACC|AL)-|id=|job |claim='E-)(\d{3,5})", bump, s) for s in steps]


def e4_session(target: dict, violating: bool, seed: int, fillers: list, n_filler: int):
    """Return (transcript, target ticket id, all ticket ids) for one session.

    The same seed gives the same session for the violating and compliant versions, apart from the
    target ticket's middle steps. The target sits in the middle third. With more than len(fillers)
    routine tickets, the pool is reused with fresh reference numbers.
    """
    rng = random.Random(f"{target['id']}-{seed}")
    picked = rng.sample(fillers, min(n_filler, len(fillers)))
    while len(picked) < n_filler:
        title, steps = rng.choice(fillers)
        picked.append((title, _renumber(steps, rng)))
    if n_filler > len(fillers):
        rng.shuffle(picked)
    total = n_filler + 1
    position = rng.randint(total // 3, 2 * total // 3)
    base = rng.randint(4100, 8800)
    middle = target["violation"] if violating else target["compliant"]
    target_ticket = (target["title"], [*target["common_before"], *middle, *target["common_after"]])
    tickets = picked[:position] + [target_ticket] + picked[position:]
    lines, ids = [], []
    for i, (title, steps) in enumerate(tickets):
        tid = f"OPS-{base + i}"
        ids.append(tid)
        lines.append(f"--- TICKET {tid}: {title} ---")
        lines.extend(steps)
    return "\n".join(lines), ids[position], ids


def item(exp, unit, version, cond, wording, question, system, user, lo, hi, **extra) -> Sample:
    """One prompt as an Inspect sample. The id and metadata are what the analysis groups by:

    exp      experiment code (e1 ... e5)      unit     scenario, vignette or target id
    version  borderline / clear / compliant / family / violating ...
    cond     the ending (good, bad, none, success, failure, omitted, payoff, harm, noharm, neutral)
    wording  which wording of that ending     question the question's short name
    lo, hi   the answer scale                 extra    seed, target ticket, study variant ...
    """
    return Sample(
        id=f"{exp}|{unit}|{version}|{cond}|{wording}|{question}" + (f"|{extra['seed']}" if "seed" in extra else ""),
        input=[ChatMessageSystem(content=system), ChatMessageUser(content=user)],
        target="",
        metadata=dict(exp=exp, unit=unit, version=version, cond=cond, wording=wording, question=question,
                      lo=lo, hi=hi, **extra),
    )
