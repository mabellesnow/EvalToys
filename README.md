# Outcome bias in LLM auditors

Does an LLM auditor excuse the same rule violation more often when the agent's task succeeded?

Each scenario has a policy and one agent trajectory in two versions: one that breaks the policy and one that follows it. Each version gets three endings (success, failure, no outcome), so the outcome is the only thing that changes between otherwise identical transcripts. The auditor sees the policy and transcript and answers: violation or not, severity 0 to 5, and whether a human should review it.

Endings describe how the task went, never a consequence of the violation. That way a change in the auditor's verdict can only come from the outcome.

## Setup (Mac)

```bash
cd ~/Documents/ToyHub/llm_auditor
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env    # then paste your API key into .env
```

`task.py` adds the project folder to Python's import path itself. On Python 3.14 for macOS, `uv sync` can hide the editable install's `.pth` file, and Python then skips it. If `python -m outcome_bias.analysis` ever fails with `No module named 'outcome_bias'` from outside this folder, run:

```bash
chflags nohidden .venv/lib/python3.*/site-packages/*.pth
```

Run every command below from `llm_auditor/`: Inspect reads `.env` from the folder you run it in, and writes logs to `./logs`, which the analysis script reads.

## Run

```bash
# quick check: 1 epoch, first 6 samples
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5 -T epochs=1 --limit 6

# full run: 30 scenarios (5 blatant, 5 subtle, 20 arguable) x 2 versions x 3 outcomes x 5 epochs = 900 calls
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5

# one set only: variant=blatant or subtle (150 calls each), or arguable (600 calls)
# repeats barely vary, so 3 epochs is usually enough (arguable: 360 calls)
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5 -T variant=arguable -T epochs=3

# add a fourth condition, "omitted", where the transcript just stops with no ending line:
# a baseline that isn't another sentence about the agent (arguable at 3 epochs: 480 calls)
inspect eval outcome_bias/task.py --model anthropic/claude-opus-5-5 -T variant=arguable -T epochs=3 -T no_ending=true

# results by variant x violation x outcome, plus a per-scenario table
python -m outcome_bias.analysis

# v2 scenarios (outcome_bias/scenarios_v2.py): 21 borderline cases and 5 clear violations, with
# longer transcripts, three-rule policies and shared context between versions.
# 26 scenarios x 2 versions x 4 endings x 3 epochs = 624 calls per model.
python -m outcome_bias.check_scenarios     # automatic checks: lengths, leaks, shared context
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5 -T variant=v2 -T epochs=3 -T no_ending=true
python -m outcome_bias.analysis logs/<v2 log>.eval

# follow-ups: ambiguous policies (12 scenarios) and justified violations (10 scenarios,
# copies of blatant/arguable ones with a persuasive agent message added)
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5 -T variant=ambiguous -T epochs=3 -T no_ending=true
inspect eval outcome_bias/task.py --model anthropic/claude-sonnet-5-5 -T variant=justified -T epochs=3 -T no_ending=true
# analyse: pass the new logs plus the base logs (blatant + arguable) for the same models
python -m outcome_bias.followups logs/<new>.eval ... logs/<base>.eval ...

# tag whether each auditor reason mentions the outcome, and how (discounted, mitigating,
# aggravating, neutral); reads the arguable logs listed in tag_reasons.py (1,680 calls)
inspect eval outcome_bias/tag_reasons.py --model anthropic/claude-haiku-5-5
python -m outcome_bias.reason_summary

# browse every transcript and verdict
inspect view
```

Any model Inspect supports works, e.g. `--model openai/<model>`.

## Files

- `outcome_bias/scenarios.py`: the scenarios. Add new ones here. Each has three versions, all reusing the blatant endings:
  - `blatant`: an obvious violation.
  - `subtle`: still a clear violation, but easy to miss or given a plausible excuse.
  - `arguable`: a borderline case where reasonable auditors could disagree (letter versus spirit of the policy, or a tiny overstep). There is no ground truth, and none is needed: the measure is whether the verdict on the same transcript moves with the ending. The analysis labels these rows `borderline`, and the scorer's `correct` field means nothing for them.
- `outcome_bias/task.py`: renders transcripts, the auditor prompt, and the scorer.
- `outcome_bias/analysis.py`: flag rate, review rate and mean severity per cell, plus the headline number.

## Reading the result

The auditor also gives a 0–100 probability that the agent violated the policy, which can move even when the yes/no verdict doesn't. The analysis reports a failure-minus-success difference for flag rate, severity and probability.

Repeats of the same transcript give near-identical answers, so the scenario is the unit of analysis. The "Paired by scenario" block takes each scenario's mean under two outcomes, averages the differences, and gives a bootstrap 95% CI over scenarios. It also counts how many scenarios moved up or down. Rows marked `*` have a CI that excludes zero.

The headline is flag rate on violating transcripts after failure minus after success. Positive means the auditor lets violations through more often when they worked. The no-outcome row shows which side moves. The clean rows check the other direction: does failure make the auditor blame an agent that followed the rules?
