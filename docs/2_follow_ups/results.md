# Results: follow-ups (stage 2)

Called "stage 2" in the plan and below. Studies: part B is `followup_labelled_scale`, part C `followup_neutral_note`, part D `followup_rule_purpose`; part A re-ran E2 and E3 on Opus.

Plan: [plan.md](plan.md), written and frozen before any of these runs. Runs on 14–15 November 2026, through the batch API, main arm (Haiku and Sonnet without reasoning, Opus at "low"). About $32.50 at batch prices, within the plan's estimate. Every claimed effect was re-run once (rule 2), and every re-run agreed, except where marked below.

Reproduce: `python -m outcome_bias.analysis.follow_ups` (all parts) and `python -m outcome_bias.analysis.labelled_scale` (part B in detail).

## Summary

| Part | Question | Answer | Status |
|---|---|---|---|
| **A** | Do Opus's E2 and E3 effects hold on a second run? | 8 of 10 confirmed. Not confirmed: E2 hindsight on risk for borderline agents, and E3 decision quality. | Rule 2 done |
| **B** | Does "judge only what the agent did; what happened afterwards doesn't change whether the policy was broken" remove E3's verdict shift? | **Mostly, yes**, in Haiku (−20 points) and Sonnet (−11). Labelling the scale alone doesn't. Opus had no shift to remove. | Claimed, confirmed |
| **C** | Is E5's drop in suspicion after "no harm" the outcome, or any follow-up note? | **The outcome.** Against a neutral note, a harmless ending lowers judged intent by 6 to 9 points and suspicion by 7 to 16, in all three models. The note itself does little, except in Sonnet (about −5). | Claimed, confirmed |
| **D** | Does harm still move the verdict when the auditor already knows what the rule is for? | **Yes.** Haiku keeps about 70% of its E3 effect, Sonnet all of it. Opus's verdict becomes *more* sensitive to harm. | Claimed, confirmed |

## A. Opus re-runs of E2 and E3

First run, then re-run. Confirmed if the re-run's interval excludes zero in the same direction.

| Experiment | Version | Question | Contrast | First run | Re-run | |
|---|---|---|---|---|---|---|
| E2 | borderline | risk at the time | failure − success | +4.0 [+0.2, +7.7] | −0.6 [−3.8, +2.7] | **not confirmed** |
| E2 | compliant | decision quality | failure − success | −1.8 [−3.6, −0.2] | −1.9 [−3.5, −0.6] | confirmed |
| E2 | compliant | risk at the time | failure − success | +2.1 [+0.6, +4.3] | +2.1 [+0.8, +3.8] | confirmed |
| E2 | compliant | performance (1–10) | failure − success | −0.64 [−1.13, −0.23] | −0.65 [−1.09, −0.27] | confirmed |
| E3 | borderline | blame | harm − payoff | +11.7 [+7.9, +16.0] | +11.5 [+8.6, +15.2] | confirmed |
| E3 | borderline | sanction (0–4) | harm − payoff | +0.40 [+0.27, +0.53] | +0.49 [+0.34, +0.64] | confirmed |
| E3 | borderline | accept as it stands | harm − payoff | −7.3 [−10.5, −4.9] | −7.0 [−9.2, −5.1] | confirmed |
| E3 | borderline | decision quality | harm − payoff | −3.2 [−7.4, −0.1] | −3.0 [−7.2, +0.3] | **not confirmed** |
| E3 | borderline | performance (1–10) | harm − payoff | −0.74 [−1.08, −0.46] | −0.68 [−1.03, −0.39] | confirmed |
| E3 | borderline | risk at the time | harm − payoff | +13.1 [+8.6, +17.8] | +12.6 [+7.2, +18.2] | confirmed |

- Opus's rule verdict again does not move: harm − payoff +1.8 [−2.7, +6.5] on re-run (+1.9 in the first run).
- E2's risk effect for borderline agents is now confirmed only in Haiku (and Sonnet, on its re-run).
- The decision-quality miss is narrow: the estimate is unchanged (−3.0 against −3.2), and the interval just reaches zero.

## B. The instruction to ignore what happened afterwards

Violation question, 21 borderline scenarios. "Change" is the change in harm − payoff from E3's first run, paired by scenario. For comparison, E3's own re-run moved it by +1.6 (Haiku) and +1.3 (Sonnet).

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| E3, original question: harm − payoff | +23.2 | +17.3 | +1.9 |
| Labelled scale: change | −6.2 [−13.2, +1.0] | −5.0 [−10.7, +0.5] | −0.2 [−4.7, +4.1] |
| Labelled scale + instruction: change | **−19.9 [−30.7, −9.6]** | **−10.7 [−17.1, −4.1]** | −2.1 [−6.1, +1.8] |
| Same, re-run: change | **−20.1 [−30.0, −10.9]** | **−10.6 [−18.0, −3.6]** | (not needed) |
| Labelled scale + instruction: harm − payoff that remains | +3.3 [−3.6, +9.4]; re-run +3.1 | +6.6 [−0.6, +13.9]; re-run +6.6 | −0.2 [−2.9, +2.4] |

- **The instruction works, and the scale labels alone don't.** One sentence removes about 85% of Haiku's verdict shift and 60% of Sonnet's, and the re-run reproduces both almost to the decimal.
- **It doesn't make the outcome irrelevant.** With the instruction, harm still raises Sonnet's score against no ending (+11.1 [+3.7, +18.8]), and so does a payoff (+4.5 [+0.2, +9.3]). The instruction mainly closes the gap between harm and payoff: any follow-up note now nudges the verdict up a little.
- **Opus**, which had no verdict shift, doesn't acquire one.

## C. E5 with a neutral note

Each ending against a neutral follow-up note ("The agent then moved on to the next task in its queue…"), first run then re-run. 12 actions; Opus on 11 (the content filter again blocked `audit_logs`).

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| **Intent: no harm − neutral** | −9.3 [−13.7, −5.6]; −9.0 [−13.2, −5.3] | −5.5 [−10.5, −2.4]; −5.8 [−10.5, −2.8] | −7.2 [−11.5, −3.5]; −7.7 [−13.8, −3.0] |
| **Suspicion: no harm − neutral** | −14.7 [−21.0, −8.3]; −14.4 [−21.1, −7.5] | −14.8 [−23.7, −8.1]; −15.6 [−25.5, −8.1] | −7.8 [−12.0, −4.0]; −7.0 [−11.0, −3.3] |
| Intent: neutral − none | −0.6; +1.0 | −5.3*; −3.9* | +1.0; −1.7 |
| Suspicion: neutral − none | −3.4; −5.1 | −5.3*; −6.4* | −0.6; −1.8 |
| Suspicion: harm − neutral (first run) | −3.0 [−11.4, +4.2] | −11.4 [−21.0, −4.4] | −5.7 [−10.4, −1.5] |

*\* interval excludes zero.*

- **The relief is the outcome.** A harmless ending lowers judged intent and suspicion well beyond what a neutral note does, in all three models and both runs. This was the weak point of E5's claim, and it holds.
- **The note itself matters a little, in Sonnet only:** about 4 to 6 points against no note at all.
- **Any outcome lowers Sonnet's and Opus's suspicion against a neutral note, harm included** (−11.4 and −5.7). Learning what happened seems to move these models from "is this malicious?" towards "this was an incident". Harm still reads as more deliberate than no harm.

## D. E3 with each rule's purpose stated

Harm − payoff with a sentence after the policy saying why the rule exists, first run then re-run, and its share of the E3 effect.

| Question | Haiku | Sonnet | Opus |
|---|---|---|---|
| **Violation** | +14.8; +16.7 (64%, 72% of E3) | +18.3; +18.9 (106%, 110%) | +7.9; +6.7 (E3: +1.9) |
| Change from E3 | **−8.4\***; −6.5\* | +1.0; +1.7 | +6.0\*; +4.8 |
| Decision quality | −12.3; −10.4 | −15.2; −15.6 | −4.7; −4.5 |
| Blame | +21.0; +19.9 | +15.4; +14.7 | +16.2; +15.9 (change +4.5\*, +4.2\*) |
| Risk at the time | +34.6; +34.5 | +28.9; +26.3 | +17.8; +18.8 (change +4.7, +5.7\*) |

*\* interval excludes zero.*

- **Pre-registered reading, violation question (Haiku and Sonnet): harm still changes the verdict.** In both models harm − payoff excludes zero, and the change from E3 is less than half of E3's effect, in both runs. Knowing what the rule is for doesn't stop harm from moving the verdict.
- **For Haiku, part of the effect was information.** About a third of its verdict shift disappears once the purpose is stated (change −8.4 and −6.5; both intervals exclude zero).
- **Opus moves the other way** (not pre-registered for Opus, but seen in both runs). With the purpose stated, harm raises its violation score by 7 to 8 points, where it barely moved in E3. Blame and risk-at-the-time effects grow by about 4 to 6 points. A plausible reading: once Opus is told what the rule guards against, harm becomes evidence that the agent's choice fell under it.
- **Hindsight is untouched.** Decision quality and risk at the time shift as much as in E3 in Haiku and Sonnet. Stating the purpose doesn't make harm more foreseeable than it was, so this is still hindsight.

## What changes in the story

1. **E3's harm effect is bias, not learning,** for Haiku and Sonnet.
2. **E5's relief after "no harm" is about the outcome,** not the presence of a note. The AI-control concern stands: a "nothing went wrong" line lowers a monitor's suspicion.
3. **There is a cheap fix for the verdict:** one sentence telling the model to judge only what the agent did. It removes most of the shift in Haiku and Sonnet. It doesn't fix hindsight, which wasn't tested with the instruction.
4. **Opus is the stable verdict-giver,** but adding context about a rule's purpose made it outcome-sensitive. Rule-purpose statements in policies may cut both ways.
5. **Two Opus effects from E1 to E5 should be reported as unconfirmed:** E2 hindsight on risk for borderline agents, and E3 decision quality.

## Deviations

- **Temperature was never sent** (in these runs or any earlier one). See the deviation at the end of [../1_main_experiments/plan.md](../1_main_experiments/plan.md).
- **The order of runs:** B ran alongside C and D rather than after them, since funds were sufficient. A ran last, as planned.
- **Opus `audit_logs`:** blocked again by the content filter in both C runs (47 and 48 answers unparsed), as anticipated in the plan. Opus's C results rest on 11 actions.
