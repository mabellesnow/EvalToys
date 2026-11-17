"""E4: does an operator's note about how a session went hide a violation buried in it?

10 target tickets, each placed in 3 sessions of 25 tickets (24 routine ones around it), in a violating
and a compliant version. Before the session, an operator note says it went well, badly, or nothing.
The model lists every ticket that broke a rule; the measure is whether it lists the target.

Stimuli: outcome_bias/stimuli/e4_buried_violation/      Plan: docs/1_main_experiments/plan.md      Results: docs/1_main_experiments/results.md
"""

from outcome_bias import stimuli
from outcome_bias.prompts import e4_session, item

EXP = "e4"
SEEDS = (1, 2, 3)
N_FILLER = 24  # routine tickets per session, set by calibration on the no-note baseline


def build(n_filler: int = N_FILLER):
    items = []
    for t in stimuli.e4_targets():
        for seed in SEEDS:
            for violating in (True, False):
                transcript, target_id, ids = e4_session(t, violating, seed, stimuli.e4_fillers(), n_filler)
                for cond, note in stimuli.e4_operator_notes().items():
                    note = note.replace("All 25 tickets", f"All {len(ids)} tickets") if note else note
                    head = f"{stimuli.e4_policy()}\n\n" + (f"{note}\n\n" if note else "")
                    user = f"{head}SESSION TRANSCRIPT ({len(ids)} tickets)\n{transcript}"
                    items.append(item(EXP, t["id"], "violating" if violating else "compliant", cond, 0, "detect",
                                      stimuli.e4_system(), user, 0, 100, seed=seed, target_ticket=target_id,
                                      tickets=ids))
    return items
