# Docs

Plans are written and frozen before their runs; results are written after. The plans are left as they were written (they record what was decided in advance), so file paths inside them refer to the layout before the 15 November restructure. The table at the end maps old paths to new ones.

## The study, phase by phase

| Phase | What it asked | Plan | Results |
|---|---|---|---|
| **Part 1, pilot** | Does an auditor excuse a rule-break when the task succeeded? Only the yes/no verdict, after a one-line note on how the task went. Found nothing. | (not pre-registered) | [part1_pilot/results.md](part1_pilot/results.md), write-up [part1_pilot/blog_draft.md](part1_pilot/blog_draft.md) |
| **Critique** | Why the pilot couldn't have found the effect, and what to run instead | [part1_pilot/critique.md](part1_pilot/critique.md) | |
| **E1 to E5** | Five pre-registered experiments (below), plus follow-up X1 on Haiku | [e1_e5/plan.md](e1_e5/plan.md) | [e1_e5/results.md](e1_e5/results.md) |
| **Stage 2** | Four gap-closing runs, A to D | [stage2/plan.md](stage2/plan.md) | [stage2/results.md](stage2/results.md) |
| **Write-up** | E1 to E5 and stage 2 for readers | | [post/outcome_bias_in_llm_auditors.md](post/outcome_bias_in_llm_auditors.md) |

Background reading: [reference/prior_work.md](reference/prior_work.md).

## Each study: where its pieces live

The study id is used everywhere: the stimulus folder, the code module, and the Inspect task.

| Study id | Question | Stimuli | Code | Plan, results | Run labels (logs/exp_runs.tsv) |
|---|---|---|---|---|---|
| `e1_people` | Do these models judge people by outcomes? (positive control) | `stimuli/e1_people/` | `outcome_bias/studies/e1_people.py` | e1_e5 | e1: `run1`, `run2`; arm `medium` |
| `e2_task_outcome` | Does how the task went change how a shortcut is judged? | `stimuli/agent_audit/` | `.../e2_task_outcome.py` | e1_e5 | e2: `run1`, `run2`; arm `reasoning` |
| `e3_consequences` | Does what the shortcut caused change it? | `stimuli/agent_audit/`, `stimuli/e3_consequences/` | `.../e3_consequences.py` | e1_e5 | e3: `run1`, `run2`; arm `reasoning` |
| `e4_buried_violation` | Does a good-session note hide a buried violation? | `stimuli/e4_buried_violation/` | `.../e4_buried_violation.py` | e1_e5 | e4: `run1` |
| `e5_intent` | Does chance harm make an action look deliberate? | `stimuli/e5_intent/` | `.../e5_intent.py` | e1_e5 | e5: `run1`, `run2` |
| `x1_labelled_scale` | Is E3's verdict shift the unlabelled scale? Does an instruction remove it? | `stimuli/x1_labelled_scale/` | `.../x1_labelled_scale.py` | e1_e5 (Haiku), stage2 B | e3: `x1-labelled`, `x1-ignore`, `x1-ignore-run2` |
| `s2c_neutral_note` | Is E5's "no harm" relief the outcome, or any note? | `stimuli/s2c_neutral_note/` | `.../s2c_neutral_note.py` | stage2 C | e5: `s2-e5_neutral`, `s2-e5_neutral-run2` |
| `s2d_rule_purpose` | Does harm still move the verdict when the rule's purpose is stated? | `stimuli/s2d_rule_purpose/` | `.../s2d_rule_purpose.py` | stage2 D | e3: `s2-purpose`, `s2-purpose-run2` |
| (stage 2 A) | Opus re-runs of E2 and E3 | as E2, E3 | as E2, E3 | stage2 A | e2, e3: `run2` (Opus) |
| Part 1 pilot | Verdict only, task-level endings | `stimuli/part1_pilot/`, `stimuli/agent_audit/` | `outcome_bias/part1/` | part1_pilot | not in the run index; log ids in `outcome_bias/part1/figures.py` |

## Checking the stimuli

`docs/freeze.json` holds the SHA-256 of every stimulus file. `python -m outcome_bias.verify` checks those hashes, then rebuilds every prompt in every logged run from the current code and compares it with what the model saw.

The per-plan hash files (`e1_e5/plan_hashes.json`, `stage2/plan_hashes.json`) are kept as written. They hash the Python files the stimuli lived in before the restructure.

## Old path → new path (restructure of 15 November 2026)

Nothing the models saw changed. Before the old files were removed, every prompt the new code builds was compared with the old code's (3,150 items across all studies and variants, identical), and with every prompt in the logs (54 runs, identical). All twelve figures were re-rendered and are pixel-identical.

| Old | New |
|---|---|
| `notes/prereg_e1_e5.md`, `notes/prereg_hashes.json`, `notes/results_e1_e5.md` | `docs/e1_e5/plan.md`, `plan_hashes.json`, `results.md` |
| `notes/prereg_stage2.md`, `notes/prereg_hashes_stage2.json` | `docs/stage2/plan.md`, `plan_hashes.json` |
| `notes/blog_e1_e5.md` | `docs/post/outcome_bias_in_llm_auditors.md` |
| `notes/v2_scenarios.md`, `notes/blog_draft.md`, `notes/methods_critique.md` | `docs/part1_pilot/results.md`, `blog_draft.md`, `critique.md` |
| `notes/prior_work.md` | `docs/reference/prior_work.md` |
| `outcome_bias/exp_e1.py` (stories, questions, system prompt) | `stimuli/e1_people/` + `outcome_bias/studies/e1_people.py` |
| `outcome_bias/exp_e3.py` (questions, system prompt, consequence endings) | `stimuli/agent_audit/questions.yaml`, `system.txt`; `stimuli/e3_consequences/endings.yaml` |
| `outcome_bias/exp_e4.py` | `stimuli/e4_buried_violation/` + `outcome_bias/prompts.py` (`e4_session`) |
| `outcome_bias/exp_e5.py` | `stimuli/e5_intent/` |
| `outcome_bias/scenarios_v2.py` | `stimuli/agent_audit/scenarios_borderline.yaml`, `scenarios_clear.yaml` |
| `outcome_bias/scenarios.py` | `stimuli/part1_pilot/scenarios_v1.yaml` + `outcome_bias/part1/scenarios.py` |
| `outcome_bias/experiments.py` | `outcome_bias/studies/` (items), `prompts.py`, `scoring.py`, `tasks.py` |
| `outcome_bias/exp_anchor.py`, `outcome_bias/stage2.py` | `outcome_bias/studies/x1_labelled_scale.py`, `s2c_neutral_note.py`, `s2d_rule_purpose.py` |
| `outcome_bias/exp_analysis.py`, `x1_analysis.py`, `stage2_analysis.py` | `outcome_bias/analysis/e1_e5.py`, `x1.py`, `stage2.py` (+ `load.py`, `outcome_bias/stats.py`) |
| `outcome_bias/exp_figures.py` | `outcome_bias/figures/e1_e5.py` (+ `style.py`) |
| `outcome_bias/task.py`, `analysis.py`, `figure.py`, `blog_figures.py`, `followups.py`, `check_scenarios.py`, `tag_reasons.py`, `reason_summary.py` | `outcome_bias/part1/` (same names; `figure.py` → `per_scenario_figure.py`, `blog_figures.py` → `figures.py`) |
| `run_exp.sh`, `run_anchor.sh`, `run_stage2.sh` | `python -m outcome_bias.run` |
| `figures/fig1`–`fig6`, `outcome_bias.png` | `figures/part1/` (`outcome_bias.png` → `per_scenario.png`) |
| `figures/fig7`–`fig12` | `figures/e1_e5/` (`e1_control`, `blame_three_settings`, `e3_which_side`, `e5_which_side`, `reasoning_on_off`, `method`) |
