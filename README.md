# Outcome bias in LLM auditors

Does an LLM that reviews an AI agent's work judge the same behaviour differently depending on how things turned out?

Every experiment uses the same move: show the model a transcript that is word-for-word identical except for its last line (how things turned out), ask one question per call, and compare the answers across endings, scenario by scenario. The write-up is [docs/post/outcome_bias_in_llm_auditors.md](docs/post/outcome_bias_in_llm_auditors.md).

## Layout

```
stimuli/          what the models read: scenarios, endings, questions, system prompts (data only)
outcome_bias/     the code
  studies/        one module per study: builds that study's prompts from stimuli/
  analysis/       one module per plan: the pre-registered contrasts
  figures/        figure code (style.py is shared)
  part1/          the pilot, archived
docs/             plans (written before the runs), results, the write-up; docs/README.md is the index
figures/          rendered figures, by phase
logs/             Inspect logs and the run index logs/exp_runs.tsv (not in git)
```

The study id is the same everywhere. `e3_consequences`, for example, names its stimuli (`stimuli/e3_consequences/`), its module (`outcome_bias/studies/e3_consequences.py`) and its Inspect task (`tasks.py@e3_consequences`). [docs/README.md](docs/README.md) has the table of studies, plans, results and run labels.

### Code, module by module

| Module | Job |
|---|---|
| `paths.py` | where stimuli, docs, figures and logs live |
| `stimuli.py` | load the files in `stimuli/` |
| `prompts.py` | assemble prompts (transcripts, endings, E4 sessions) and wrap them as Inspect samples |
| `studies/` | one `build()` per study; `studies/__init__.py` lists them all |
| `tasks.py` | the Inspect task for each study |
| `scoring.py` | parse the JSON answer |
| `models.py` | model names and the reasoning setting of each arm |
| `run.py` | run a study on several models and record each run in the run index |
| `runlog.py` | read and write the run index |
| `stats.py` | per-scenario means, paired differences, bootstrap intervals |
| `analysis/` | `load.py` reads answers from logs; `e1_e5.py`, `x1.py`, `stage2.py` report each plan |
| `verify.py` | check stimulus hashes, and rebuild every logged prompt to confirm it is unchanged |

## Setup

```bash
uv sync
```

Put your API key in `.env` as `ANTHROPIC_API_KEY=...` (and `OPENAI_API_KEY=...` for OpenAI models). Run every command from this folder: Inspect reads `.env` from where it starts.

On Python 3.14 for macOS, `uv sync` can hide the editable install's `.pth` file. If you see `No module named 'outcome_bias'`, run:

```bash
chflags nohidden .venv/lib/python3.*/site-packages/*.pth
```

## Running a study

```bash
python -m outcome_bias.run e3_consequences --batch
```

This runs the study on Haiku, Sonnet and Opus in their main arm (the lowest reasoning each allows) through the batch API, and records each run as `run1`. Options:

| Option | Meaning |
|---|---|
| `--models haiku sonnet opus` | which models (see `models.py`) |
| `--arm main`, `medium` or `reasoning` | the reasoning setting |
| `--label run2` | the run's label in the run index (use it for re-runs) |
| `--set variant=ignore` | a study parameter (`x1_labelled_scale`: `variant`; `e4_buried_violation`: `n_filler`) |
| `--limit 3` | a smoke test on the first 3 items, written to `logs/smoke/` and not recorded |

## Analysing

```bash
python -m outcome_bias.analysis.e1_e5 e3
```

```bash
python -m outcome_bias.analysis.e1_e5 e3 --label run2
```

```bash
python -m outcome_bias.analysis.stage2
```

```bash
python -m outcome_bias.figures.e1_e5
```

```bash
python -m outcome_bias.verify
```

`inspect view` browses every transcript and answer.
