# Stimuli

Everything the models read, as data. No code here: `outcome_bias/stimuli.py` loads these files and `outcome_bias/prompts.py` assembles them into prompts. Each folder is named after the study that uses it (see `docs/README.md`).

These files are frozen: `docs/freeze.json` holds their hashes, and `python -m outcome_bias.verify` checks both the hashes and that every logged prompt still rebuilds exactly. Don't edit a file here once its study has run. Add a new file or folder for a new study instead.

| Folder | Used by | Contents |
|---|---|---|
| `agent_audit/` | E2, E3, X1, stage 2 D, Part 1 (set 2) | `scenarios_borderline.yaml` (21) and `scenarios_clear.yaml` (5): policy, task, shared `context`, the two middles (`borderline`, `compliant`), shared `wrapup`, and E2's task-level `endings`. `questions.yaml`: the seven questions and their scales. `system.txt`. |
| `e1_people/` | E1 | `vignettes.yaml`: 12 stories, each with a `good` and `bad` ending. `questions.yaml` (`{person}`, `{act}`, `{harm}` are filled in). `system.txt`. |
| `e3_consequences/` | E3, X1, stage 2 D | `endings.yaml`: per scenario, `payoff` and `harm` endings (two wordings each for borderline scenarios). |
| `e4_buried_violation/` | E4 | `policy.txt`, `targets.yaml` (10 targets with violating and compliant middles), `fillers.yaml` (24 routine tickets; order matters, as sessions are sampled from it with a fixed seed), `operator_notes.yaml`, `system.txt`. |
| `e5_intent/` | E5, stage 2 C | `actions.yaml`: 12 actions, each with steps, the review focus, and `harm` / `noharm` endings. `questions.yaml`, `system.txt`. |
| `x1_labelled_scale/` | X1 | `questions.yaml`: the labelled violation question and the "ignore what happened afterwards" prefix. |
| `s2c_neutral_note/` | stage 2 C | `notes.yaml`: two neutral follow-up notes. |
| `s2d_rule_purpose/` | stage 2 D | `purposes.yaml`: one "Why rule N exists" sentence per borderline scenario. |
| `part1_pilot/` | Part 1 | `scenarios_v1.yaml`: the pilot's first set (blatant, subtle, arguable, ambiguous, justified). `auditor_prompt.txt`. |

Endings are stored without the "FOLLOW-UP NOTE: " prefix where the code adds it (E3, E5, stage 2), and with it where it is part of the text (E2's `endings` in `agent_audit/`).
