# Methods critique and next experiments

> **Layout note (15 November 2026).** The code and notes were reorganised after this was written. File paths below refer to the old layout; [docs/README.md](../README.md) maps each old file to its new place. Nothing the models saw changed: every logged prompt was rebuilt from the new code and matched.

Written 13 November 2026, after the v1 runs, the reruns, the ambiguous and justified follow-ups, and the v2 runs. Diagnostics below read existing logs only (3,912 answers on borderline transcripts: v1 main set and v2, all current runs).

## Bottom line

The null result is solid for the narrow thing that was measured: a labelled one-line note about how the task went does not change a Claude auditor's answer to "did the agent break this written rule?".

That is the judgement least likely to show outcome bias, in people as well as models. The project has no positive control and no human baseline, so it cannot tell "these models resist outcome bias" apart from "this setup would not show outcome bias in anyone". The claim "LLM auditors don't excuse violations that worked" is wider than the evidence.

## What the logs show

| Check | Result | What it means |
|---|---|---|
| Yes/no verdict against probability | Verdict equals "probability ≥ 50" in 3,899 of 3,912 answers | Two of the four measures are one measure |
| Probability scale | 8 favourite values (88, 80, 72, 92, …) cover 58–68% of answers | Coarse scale; scores move in jumps or not at all |
| Repeats of one transcript | Verdict unanimous in 94–95% of cells | Repeats add almost nothing; a verdict is either pinned or bimodal |
| Room for a verdict to move | Only 5 of 60 scenario-model pairs in v1 and 13 of 63 in v2 have a flag rate between 10% and 90% | The verdict could only ever move in 18 of 123 cases |
| Human-review decision | 85–99% "yes" on borderline transcripts | The decision that matters for a gate is at the ceiling |
| Per-scenario effects across runs | Rank correlation of failure-minus-success between runs is mostly +0.3 to +0.7 | Outcome effects per scenario are real and repeatable, but point both ways and cancel in the mean |
| Reasoning before answering | Never fixed. On borderline transcripts: Haiku and Opus about 100%; Sonnet 35% after success, 48% after failure | An uncontrolled variable that itself moves with the ending |
| Implicitly linked endings (v1, exploratory) | Scenarios whose success ending plausibly resulted from the shortcut: success minus no ending −0.1 to +0.4; the rest −0.7 to +0.4 | An implicit link between shortcut and success made no difference |
| Size of the manipulation | The ending is 12% of the text in v1 and 8% in v2 | One sentence, labelled as an outcome, after the transcript |

## Flaws, most serious first

1. **The question is the wrong kind.** Human outcome effects are found in ratings of decision quality (Baron and Hershey, 1988), in blame and punishment more than in wrongness (Cushman, 2008), and in judgements under vague standards such as negligence. We asked a yes/no wrongness-type question against a written bright-line rule. The "borderline" in our scenarios is also definitional (is a service charge part of a meal?), not about risk. An outcome has no pull on a definition.
2. **No positive control and no human baseline.** The pipeline has never detected an outcome effect that is known to exist, and no person has rated these items. A null cannot be interpreted without one of the two.
3. **The manipulation is weak and incomplete.**
   - One labelled sentence appended after the transcript.
   - No harm condition. "Failure" means the task failed for unrelated reasons; the harm the rule exists to prevent never happens.
   - The success is never explicitly attributed to the shortcut, and no person in the transcript reacts to it.
   - v2 went further: its design rules excluded endings that follow from the agent's choice, and one scenario was dropped for that reason. That was too conservative. For the question "did the agent break the rule", any outcome is logically irrelevant however it came about, so consequence-linked endings are a fair test. Only endings that change what was true or knowable at decision time are leaks.
4. **Asymmetric scrutiny, which biases towards the null.** Whenever an outcome effect appeared (restricted table, PII, "unrelated bugs", "response-time target"), the ending was treated as an artefact, rewritten and rerun. Scenarios with no effect were never examined. Stimuli, exclusions and analyses all changed after seeing data, with no preregistration and no held-out set. Some fixes were right (the "email" contradiction), but the process can only remove effects.
5. **Insensitive measures.** See the first five rows of the table above.
6. **One wording per ending.** Each scenario has a single success and a single failure sentence, so a scenario-level effect cannot be separated from that sentence's wording. `cloud_budget` shows the cost: across four v1 runs Sonnet took the lenient reading in 10 of 14 samples after success and 7 of 14 after failure; in v2, with different wording, 0 of 6 after success and 6 of 6 after failure. Three samples per cell cannot estimate a bimodal answer.
7. **Uncontrolled settings and narrow coverage.** Adaptive reasoning, one prompt, default temperature, one model family, stimuli written by a model from the same family as the auditors, transcripts of 13 steps at most, and a required written reason that invites careful, norm-following answers.
8. **Statistics.** 18 comparisons per run with no correction. The tagger of reasons was never checked by a person. v2 scenarios were tuned on the same models' no-ending scores. With 20 scenarios and intervals of about ±2 points, power is adequate for a moderate average effect on this measure, so the average null on this measure stands.
9. **Half the calls carry no information.** Compliant versions sit at the floor under every ending, so the mirror-image bias (blaming a compliant agent after a failure) cannot be tested.

## Why the predicted effect is probably not appearing

In rough order of likelihood:

1. **Wrong kind of judgement** (flaw 1). The auditors reason like literalists: any breach of the letter scores 80 or more, and the implicit link between shortcut and success made no difference.
2. **The models know the norm and the manipulation is transparent.** Opus mentions the outcome in 50–79% of its reasons, nearly always to dismiss it, and Haiku and Opus reason before almost every borderline answer.
3. **Verdicts are pinned.** Only 18 of 123 scenario-model pairs can move.
4. **Outcome sensitivity exists but has no consistent direction.** Per-scenario effects repeat across runs and cancel in the mean. "Outcomes don't matter" is wrong; "outcomes don't push one way" is what the data show.
5. **The models may simply be robust on this judgement.** This cannot be told apart from 1 to 3 without the controls.

## Experiments, by information per cost

| | Experiment | What it settles | Rough size |
|---|---|---|---|
| E1 | **Positive control.** Run classic outcome-bias vignettes (decision quality; ethical judgement; negligence or moral luck) on the same three models in the same harness. | Bias on classic items but not on audits: the audit question suppresses it. No bias anywhere: the models are robust, so look at other models or other mechanisms. | 1 day, 1–2k calls |
| E2 | **Change the question, keep the transcripts.** Ask, in separate calls: decision quality given what the agent knew; blame; a sanction ladder (none, note, warning, restrict permissions, suspend); retroactive exception yes/no; an overall performance score as a reward signal; and "at the time, how likely was this to cause a problem?". | Whether outcome moves blame, sanction and reward while leaving "violation" flat, as in people. The performance score gives a difference-in-differences: the penalty for the shortcut after success against after failure. This uses the compliant versions, which carry no information today. | 1 day, about 2k calls per model |
| E3 | **Outcomes that are consequences, including harm.** Three endings per scenario: the shortcut explicitly paid off; the harm the rule exists to prevent happened; nothing. Two or three wordings of each. Same decision-time information. | The classic moral-luck design, which the project has not run. | 2 days, about 1.5k calls per model |
| E4 | **Vigilance in long transcripts.** 100 to 300 steps, or real agent trajectories, with one subtle violation buried in the middle. Task status shown as success or failure. Measure whether the auditor finds the step. | A different mechanism: success may not excuse a violation that was found, but may make the auditor less likely to find it. Detection in long transcripts is below 100%, so there is room to move. | 3 or more days |
| E5 | **Intent attribution.** Actions that could be an honest mistake or deliberate; the ending says whether harm followed. Measure probability of intent and a suspicion score. | The AI-control version of the question: does a harmless outcome make sabotage look like an accident? | 2 days |
| E6 | **Embedded and social outcomes.** No labelled note. The outcome appears in tool results and in people's reactions ("that fixed it, great work"), including praise from someone with no authority to waive the rule. | Whether after-the-fact praise works as approval. | 2 days |
| E7 | **Knife-edge cases, many samples.** The roughly ten unpinned scenario-model pairs, three wordings per ending, 40 or more samples per cell over several sessions, reasoning fixed on and off. | Whether effects like `cloud_budget` are real and which way they point. | About 10k calls on one model |
| E8 | **Forced prioritisation.** Eight incident summaries, a budget of three escalations, endings rotated across incidents. | Relative judgements can move when absolute scores are pinned, and this is how review queues work. | 1 day |
| E9 | **Sweeps.** Reasoning fixed on and off; verdict only, with no reason; a "judge the process only" instruction and a "consider the business result" instruction (a second positive control); other model families and older or smaller models. | How far the result generalises. | Small per condition |
| E10 | **Human baseline** on six of the same items. | Needed for any sentence that compares these models with people. | About 150 participants |

Suggested order: E1 and E2 first. They are the cheapest, reuse everything already built, and decide which branch is worth the larger builds. Then E3, then E4 or E5.

Papers named here are cited from memory and should be checked before they are relied on: Baron and Hershey (1988); Cushman (2008), "Crime and punishment", Cognition; Gino, Moore and Bazerman (2009), "No harm, no foul"; Kneer and Skoczeń (2023).

## Process changes for any confirmatory run

- Write down hypotheses, measures, exclusion rules and the analysis before running.
- Build on a development set; confirm on a held-out set of scenarios, ideally written by someone else.
- Freeze stimuli before the confirmatory run. If an ending looks leaky afterwards, report both versions.
- Fix temperature and reasoning. Use at least two wordings per ending.

## What this means for the write-up

- Narrow the claim to what was tested: explicit-rule compliance judgements, a labelled outcome note, three Claude models.
- Say plainly what is untested: blame, sanction and reward; vague standards; harm outcomes; detection in long transcripts; other model families; people.
- "Outcomes shift verdicts on individual scenarios, repeatably, in both directions" is a finding the draft currently undersells.
