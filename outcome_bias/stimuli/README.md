# Stimuli

Everything the models read, as data. `__init__.py` loads these files and `outcome_bias/prompts.py` assembles them into prompts. Each folder is named after the study that uses it (see `docs/README.md`).

These files are frozen: `hashes.json` holds their hashes, and `python -m outcome_bias.verify` checks both the hashes and that every logged prompt still rebuilds exactly. Don't edit a file here once its study has run. Add a new file or folder for a new study instead.

| Folder | Used by | Contents |
|---|---|---|
| `agent_transcripts/` | E2, E3, `followup_labelled_scale`, `followup_rule_purpose` | `scenarios_borderline.yaml` (21) and `scenarios_clear.yaml` (5): policy, task, shared `context`, the two middles (`borderline`, `compliant`), shared `wrapup`, and E2's task-level `endings`. `questions.yaml`: the seven questions and their scales. `system.txt`. |
| `e1_people/` | E1 | `vignettes.yaml`: 12 stories, each with a `good` and `bad` ending. `questions.yaml` (`{person}`, `{act}`, `{harm}` are filled in). `system.txt`. |
| `e3_consequences/` | E3, `followup_labelled_scale`, `followup_rule_purpose` | `endings.yaml`: per scenario, `payoff` and `harm` endings (two wordings each for borderline scenarios). |
| `e4_buried_violation/` | E4 | `policy.txt`, `targets.yaml` (10 targets with violating and compliant middles), `fillers.yaml` (24 routine tickets; order matters, as sessions are sampled from it with a fixed seed), `operator_notes.yaml`, `system.txt`. |
| `e5_intent/` | E5, `followup_neutral_note` | `actions.yaml`: 12 actions, each with steps, the review focus, and `harm` / `noharm` endings. `questions.yaml`, `system.txt`. |
| `followup_labelled_scale/` | `followup_labelled_scale` | `questions.yaml`: the labelled violation question and the "ignore what happened afterwards" prefix. |
| `followup_neutral_note/` | `followup_neutral_note` | `notes.yaml`: two neutral follow-up notes. |
| `followup_rule_purpose/` | `followup_rule_purpose` | `purposes.yaml`: one "Why rule N exists" sentence per borderline scenario. |

Endings are stored without the "FOLLOW-UP NOTE: " prefix where the code adds it (E3, E5, the follow-ups), and with it where it is part of the text (E2's `endings` in `agent_transcripts/`).
