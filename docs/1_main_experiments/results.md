# Results: experiments E1 to E5

> **Layout note.** The code and notes were reorganised after this was written (15 and 17 November 2026). File paths and commands below are those of the time; "Names in older documents" in [docs/README.md](../README.md) maps each to its current place. Today the analysis is `python -m outcome_bias.analysis.main_experiments`, and X1 is the study `followup_labelled_scale`. Nothing the models saw changed: every logged prompt was rebuilt from the new code and matched.

Design, hypotheses and rules for claims: `notes/prereg_e1_e5.md`. Log files for every run: `logs/exp_runs.tsv`. Analysis: `python -m outcome_bias.exp_analysis <logs of one experiment>`.

All numbers are means over units (vignettes, scenarios or targets) of the per-unit difference, with a bootstrap 95% interval over units. "Main arm" is the lowest reasoning setting each model allows.

## Summary of E1 to E5

| | Question | Result | Status |
|---|---|---|---|
| E1 | Do these models show outcome bias at all? | Yes. On vignettes about people, a bad outcome raises blame, penalty and wrongness by 12 to 23 points in all three models. | Confirmed by re-run |
| E2 | Does an unrelated task result change how a borderline shortcut is judged? | Barely. Violation, blame and sanction stay flat. Acceptance falls after failure (Haiku, Sonnet), the choice is rated riskier in hindsight, and a compliant agent is rated a little worse after a failed task. | Confirmed on Haiku and Sonnet |
| E3 | Does a consequence of the shortcut change it? | Harm does: violation +17 to +23 points in Haiku and Sonnet, blame +12 to +23 in all three. A shortcut that paid off is judged the same as one with no ending. Opus's violation verdict stays flat. | Confirmed on Haiku and Sonnet |
| E4 | Does an operator's note hide a buried violation? | No. Detection is 88 to 100% with or without the note. | Null, reported with intervals |
| E5 | Does chance harm change whether an action looks deliberate? | Yes, a little: +4 to +7 points on intent in Haiku and Opus. Against no ending, a harmless ending lowers suspicion by 9 to 20 points in all three. | Confirmed by re-run |

- **The original prediction, that success excuses a violation, is not supported.** Neither a successful task (E2) nor a shortcut that visibly paid off (E3) lowers the violation verdict, blame or sanction in any model.
- **The bias that is there runs the other way.** Harm makes the same transcript look like a violation to Haiku and Sonnet, and makes all three models blame and sanction more.
- **The closest thing to the predicted leniency is in E5.** A monitor's suspicion and its estimate of intent drop when nothing bad came of the action. Part of that drop may come from the follow-up note itself.
- **Opus is the most stable.** It moves blame and sanction with harm, as a person might defend, but keeps "was the rule broken" almost fixed (+1.9 between harm and payoff).

## E1: classic vignettes about people (positive control)

Run 13 November 2026, 17:08 to 17:16. 5,400 answers, none unparsed. 12 vignettes, 5 samples each.

**The control worked.** All three models judge the same act very differently depending on how it turned out.

Bad outcome minus good outcome, all 12 vignettes, main arm:

| Question (0–100) | Haiku | Sonnet | Opus |
|---|---|---|---|
| Blame | +12.4 [+7.4, +17.5] | +23.4 [+15.4, +31.7] | +19.8 [+12.9, +27.5] |
| Penalty | +14.9 [+9.9, +20.1] | +14.2 [+8.8, +19.6] | +15.9 [+8.8, +23.3] |
| Wrongness | +15.5 [+11.1, +20.1] | +18.6 [+11.4, +26.2] | +15.9 [+9.7, +22.5] |
| Risk at the time of the decision | +21.3 [+9.2, +33.6] | +5.1 [+1.8, +9.0] | +2.3 [+0.1, +5.0] |
| Decision quality, judged by what the person knew | −3.7 [−5.0, −2.5] | −4.7 [−7.3, −2.8] | −1.9 [−4.3, +0.5] |

- **Direction:** every blame, penalty and wrongness effect is positive in 9 to 12 of the 12 vignettes and negative in none.
- **A good outcome excuses more than a bad one condemns.** Against no outcome, a good outcome lowers blame by 6.5 (Haiku), 14.8 (Sonnet) and 10.7 (Opus) points; a bad outcome raises it by 5.9, 8.6 and 9.1.
- **Hindsight:** where the odds are not stated (skipped duties, carelessness), the models rate the harm as having been more likely once it has happened. Haiku shows this most (+31 and +33 points in those two families). Where the odds are stated in the story, all three repeat them exactly under every outcome.
- **Decision quality barely moves** (2 to 5 points), although the question tells the model to judge by what the person knew.
- **Even defensible decisions pick up blame.** For the four risky decisions with stated odds, blame is 5 to 7 points higher after the bad outcome.

**Reasoning does not remove it.** Second arm, effort "medium": blame +18.6 (Haiku, which reasoned on 93% of answers), +24.2 (Sonnet) and +18.0 (Opus, 88%). Sonnet chose not to reason on any answer at this setting, so its second arm is not a test of reasoning.

**Rule 1 is met** for blame, penalty, wrongness and risk in all three models, and for decision quality in Haiku and Sonnet. The re-run required by rule 2 is recorded below.

**What this means for the earlier null.** These models are not immune to outcome bias. They show it clearly when asked about blame, penalty and wrongness for a person's act. The earlier experiments asked whether an agent broke a written rule, and found nothing. E2 and E3 test whether the difference is the question or the setting.

**Re-run (rule 2), 17:18 to 17:21, main arm.** Confirmed. Bad minus good: blame +11.1, +22.8, +20.5; penalty +15.8, +14.4, +15.7; wrongness +14.9, +18.4, +15.4; risk +23.9, +5.1, +3.0; decision quality −3.8, −5.2, −2.3 (Haiku, Sonnet, Opus). Every interval that excluded zero in the first run does so again.

## E2: the same agent transcripts, new questions

Main arm run 13 November 2026, 17:21 to 17:34. 7,722 answers, 32 unparsed (0.4%), excluded as pre-registered. 26 v2 scenarios, v2's own endings (how the task went, unrelated to the shortcut), 3 samples.

### Borderline versions (21 scenarios), failure minus success

| Question | Haiku | Sonnet | Opus | Claimed (rule 1)? |
|---|---|---|---|---|
| Violation (0–100) | +6.6 [+1.2, +13.1] | −3.9 [−11.7, +3.0] | −2.9 [−5.3, −0.7] | No: opposite signs |
| Decision quality | −2.0 [−5.1, +1.3] | +0.8 [−2.7, +4.6] | +2.7 [−0.7, +6.4] | No |
| Blame | +2.4 [−0.9, +5.8] | −0.6 [−5.8, +3.8] | −0.3 [−3.7, +3.3] | No |
| Sanction (0–4) | +0.05 [−0.06, +0.19] | −0.03 [−0.16, +0.06] | +0.02 [−0.16, +0.17] | No |
| Accept as it stands | −8.0 [−14.9, −2.3] | −11.2 [−20.7, −4.1] | +0.5 [−2.9, +4.1] | **Yes** (Haiku, Sonnet) |
| Performance (1–10) | −0.44 [−0.79, −0.13] | −0.10 [−0.67, +0.51] | −0.45 [−0.77, −0.17] | Yes, but not a bias: results are part of performance |
| Risk at the time | +9.3 [+3.8, +15.2] | +2.2 [−1.0, +5.3] | +4.0 [+0.2, +7.7] | **Yes** (Haiku, Opus) |

- **Blame and sanction do not move**, in any model. On the human vignettes in E1 the same models moved blame by 12 to 23 points.
- **Violation** repeats the earlier pattern: Haiku a little harsher after failure, Opus a little more lenient, nothing consistent.
- **Acceptance:** Haiku and Sonnet are less willing to let the borderline handling stand after a failure. Almost all of it is failure lowering acceptance (−6.0 and −8.2 against no ending); success raises it by only 2 to 3 points, with intervals that include zero.
- **Hindsight:** the same choice is rated as having been riskier at the time once the task has failed. Against no ending, success lowers the rating (Sonnet −5.8, Opus −3.3, both intervals excluding zero).

### Compliant versions (the agent followed the rule), failure minus success

| Question | Haiku | Sonnet | Opus |
|---|---|---|---|
| Decision quality | −5.1 [−8.5, −1.9] | −2.3 [−3.5, −1.2] | −1.8 [−3.6, −0.2] |
| Risk at the time | +9.0 [+5.4, +13.0] | +1.7 [+0.7, +2.8] | +2.1 [+0.6, +4.3] |
| Performance (1–10) | −0.82 [−1.29, −0.36] | −1.04 [−1.63, −0.53] | −0.64 [−1.13, −0.23] |
| Violation | +0.1 [−2.7, +2.1] | +0.1 [−0.4, +0.4] | −0.2 [−0.5, +0.0] |

- **The mirror-image bias is there, in all three models.** An agent that followed the rule is rated as having decided worse, and as having taken more risk, when the task failed for unrelated reasons. The question told the model to judge by what the agent knew. The effects are small (2 to 5 points on quality) but every interval excludes zero.
- **Violation stays flat:** a failed task does not make a compliant agent look like a rule-breaker.

### Performance score: does success make the shortcut cheaper?

The cost of the shortcut is the compliant version's score minus the borderline version's.

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| Cost after success | 2.94 | 3.84 | 4.58 |
| Cost after failure | 2.68 | 2.94 | 4.42 |
| Difference | +0.25 [−0.11, +0.62] | +0.90 [+0.43, +1.46] | +0.17 [−0.17, +0.55] |

The predicted bias would make the difference negative. It is positive in all three and clear in Sonnet: failure pulls the compliant agent's score down by about a point and barely touches the shortcut-taker's, which is already low. As a reward signal, these scores punish a compliant agent for bad luck more than they reward a shortcut for good luck.

### Clear violations (5 scenarios)

Violation probability stays at 94 to 97 under every ending in Sonnet and Opus. Risk at the time rises after failure in all three (+6.6, +15.1, +9.7). Too few scenarios for more.

### E2 reasoning-on arm (Haiku and Sonnet)

Haiku run 17:37; Sonnet run 18:07 through the batch API after the credit interruption. 5,146 answers, 2 unparsed. Haiku reasoned on every answer, Sonnet on 95%. Opus was dropped from this arm (pre-registration, Addition 2).

Failure minus success:

| Question | Haiku | Sonnet |
|---|---|---|
| Borderline: violation | +1.3 [−1.8, +4.0] | −0.5 [−2.4, +1.5] |
| Borderline: blame | +4.0 [+0.1, +8.0] | −1.4 [−3.9, +1.1] |
| Borderline: sanction | +0.16 [−0.03, +0.37] | +0.00 [−0.11, +0.11] |
| Borderline: accept as it stands | −6.3 [−10.9, −2.5] | −6.0 [−14.4, +0.2] |
| Borderline: risk at the time | +18.1 [+11.6, +25.2] | +4.4 [+1.5, +7.5] |
| Compliant: decision quality | −4.2 [−6.6, −2.2] | −1.9 [−3.4, −0.5] |
| Compliant: risk at the time | +10.3 [+5.9, +15.8] | +1.1 [+0.4, +1.7] |

- Reasoning does not remove the hindsight effect or the mirror-image bias; both meet rule 1 within this arm.
- Against no ending, success lowers risk-at-the-time (−11.4 and −6.0) and raises acceptance slightly (+2.7 [+0.8, +4.5] and +1.8 [+0.0, +3.6]).
- Violation and sanction stay flat with reasoning on, as in the main arm.

### E2 re-run (rule 2), main arm, Haiku and Sonnet

Run 18:07 to 18:25 through the batch API. 5,101 answers, 47 unparsed (0.9%, spread evenly over endings; all are replies whose reason contains an unescaped quotation mark). Opus's re-run failed when the credit ran out again and has not been done (it is outside the scope agreed afterwards).

| Claimed effect (failure minus success) | Haiku, re-run | Sonnet, re-run | Confirmed? |
|---|---|---|---|
| Borderline: accept as it stands | −11.0 [−18.7, −4.2] | −7.4 [−16.0, −1.4] | Yes |
| Borderline: risk at the time | +10.3 [+5.0, +15.9] | +6.8 [+1.1, +13.2] | Yes in Haiku; Sonnet now also excludes zero; Opus not re-run |
| Compliant: decision quality | −3.7 [−5.9, −1.5] | −2.4 [−3.4, −1.5] | Yes |
| Compliant: risk at the time | +8.3 [+4.3, +12.5] | +1.7 [+0.9, +2.6] | Yes |
| Performance: cost after success minus after failure | +0.14 [−0.22, +0.52] | +0.32 [+0.02, +0.65] | Sonnet yes |

Blame, sanction and decision quality for borderline versions stay unclaimed: only Haiku's blame (+5.4 [+2.3, +9.0]) excludes zero.

## E3: outcomes that are consequences of the shortcut

Main arm: Haiku and Sonnet run 18:07 to 18:30; Opus run from 18:32, after the third top-up. Reasoning arm (Haiku, Sonnet) run 18:07 to 18:25. All through the batch API. Main arm: 7,560 answers, 67 unparsed (0.9%). Reasoning arm: 5,040 answers, 3 unparsed. Opus reasoned on 67% of its main-arm answers. 21 borderline scenarios, two wordings per ending.

### Borderline versions: harm minus payoff, main arm

| Question | Haiku | Sonnet | Opus |
|---|---|---|---|
| Violation (0–100) | +23.2 [+15.3, +31.3] | +17.3 [+7.8, +28.1] | +1.9 [−3.0, +7.5] |
| Decision quality | −8.4 [−14.1, −3.1] | −11.6 [−18.6, −5.3] | −3.2 [−7.4, −0.1] |
| Blame | +22.5 [+16.5, +28.8] | +16.0 [+10.8, +21.0] | +11.7 [+7.9, +16.0] |
| Sanction (0–4) | +0.75 [+0.53, +0.98] | +0.48 [+0.25, +0.72] | +0.40 [+0.27, +0.53] |
| Accept as it stands | −19.5 [−26.3, −13.4] | −28.6 [−39.4, −18.5] | −7.3 [−10.5, −4.9] |
| Performance (1–10) | −2.25 [−2.79, −1.71] | −1.48 [−2.25, −0.80] | −0.74 [−1.08, −0.46] |
| Risk at the time | +35.1 [+27.7, +42.4] | +28.1 [+19.4, +37.2] | +13.1 [+8.6, +17.8] |

- **Rule 1 is met for all seven questions**: for six of them in all three models, and for violation in Haiku and Sonnet only.
- **Opus shows the same pattern at about half the size, except on the verdict itself.** Its violation probability does not move between harm and payoff (+1.9, interval includes zero). In Haiku and Sonnet 17 to 21 of the 21 scenarios move the same way on most questions.

### Borderline versions: harm minus payoff, reasoning-on arm

| Question | Haiku | Sonnet |
|---|---|---|
| Violation (0–100) | +9.1 [+5.6, +13.0] | +13.2 [+6.5, +21.0] |
| Decision quality | −7.1 [−11.6, −3.2] | −12.5 [−19.9, −6.5] |
| Blame | +17.2 [+12.4, +22.0] | +18.3 [+12.7, +24.5] |
| Sanction (0–4) | +0.79 [+0.52, +1.06] | +0.39 [+0.21, +0.60] |
| Accept as it stands | −11.3 [−16.4, −7.0] | −19.2 [−26.8, −12.1] |
| Performance (1–10) | −1.25 [−1.69, −0.87] | −1.54 [−2.28, −0.89] |
| Risk at the time | +37.9 [+30.9, +44.8] | +34.0 [+26.2, +41.7] |

Reasoning softens the effect without removing it. The verdict effect falls from +23 to +9 in Haiku and from +17 to +13 in Sonnet; acceptance from −20 to −11 and from −29 to −19; Haiku's blame from +23 to +17 and its performance effect from −2.3 to −1.3. Decision quality, sanction and risk at the time are unchanged (risk is if anything larger: +35 to +38 and +28 to +34). Every interval still excludes zero.

### Which side moves: each ending against no ending (main arm)

Harm minus no ending:

| Question | Haiku | Sonnet | Opus |
|---|---|---|---|
| Violation | +23.8 [+17.0, +31.2] | +14.5 [+5.2, +24.4] | +3.7 [+0.2, +7.1] |
| Blame | +21.2 [+16.1, +26.1] | +15.4 [+10.3, +20.2] | +11.3 [+6.8, +16.3] |
| Sanction | +0.87 [+0.64, +1.10] | +0.43 [+0.18, +0.69] | +0.35 [+0.17, +0.52] |
| Accept as it stands | −20.4 [−28.5, −13.3] | −28.8 [−40.4, −17.8] | −6.6 [−8.9, −4.5] |
| Decision quality | −10.9 [−16.6, −5.3] | −9.7 [−16.5, −4.3] | −3.7 [−6.8, −1.1] |
| Risk at the time | +30.6 [+23.3, +37.6] | +24.8 [+15.0, +34.0] | +8.5 [+4.3, +13.1] |

Payoff minus no ending:

| Question | Haiku | Sonnet | Opus |
|---|---|---|---|
| Violation | +0.7 [−3.5, +4.6] | −2.7 [−9.2, +3.5] | +1.8 [−1.0, +4.4] |
| Blame | −1.3 [−6.2, +3.8] | −0.6 [−3.9, +2.7] | −0.4 [−4.2, +3.2] |
| Sanction | +0.12 [−0.01, +0.23] | −0.05 [−0.13, +0.01] | −0.05 [−0.18, +0.08] |
| Accept as it stands | −0.9 [−6.1, +4.2] | −0.2 [−4.1, +4.6] | +0.7 [−0.8, +2.2] |
| Decision quality | −2.4 [−4.9, −0.1] | +1.8 [−0.9, +5.1] | −0.5 [−2.9, +2.1] |
| Risk at the time | −4.6 [−9.9, +0.8] | −3.3 [−8.9, +1.1] | −4.6 [−7.2, −1.8] |

- **Harm does all the work.** When the harm the rule guards against happens, Haiku and Sonnet are 15 to 24 points more likely to call the same transcript a violation, and blame, sanction and acceptance move with it. Opus moves blame, sanction and acceptance too, but its violation probability by only 3.7 points.
- **Payoff excuses nothing, in any model.** A shortcut that visibly paid off is judged the same as one with no ending: violation, blame, sanction and acceptance all stay within noise. The one thing payoff moves is risk at the time, downward (Opus −4.6 [−7.2, −1.8]; reasoning arm: Haiku −5.3 [−8.9, −1.4], Sonnet −7.2 [−12.0, −2.7]).
- **Violation and decision quality should not move.** The agent's actions and knowledge are identical in every cell. In Haiku and Sonnet they move by 9 to 24 points.

### E3 re-run (rule 2), main arm, Haiku and Sonnet

Run from 18:32 through the batch API. 5,040 answers, 36 unparsed (0.7%). Harm minus payoff, borderline versions:

| Question | Haiku, first run | Haiku, re-run | Sonnet, first run | Sonnet, re-run |
|---|---|---|---|---|
| Violation | +23.2 | +24.8 [+17.0, +33.1] | +17.3 | +18.6 [+9.4, +29.0] |
| Decision quality | −8.4 | −9.6 [−14.9, −4.6] | −11.6 | −10.9 [−16.5, −5.6] |
| Blame | +22.5 | +24.7 [+19.3, +30.1] | +16.0 | +16.5 [+11.1, +22.0] |
| Sanction | +0.75 | +0.80 [+0.57, +1.02] | +0.48 | +0.53 [+0.27, +0.83] |
| Accept as it stands | −19.5 | −19.1 [−24.7, −13.7] | −28.6 | −28.7 [−39.5, −18.3] |
| Performance | −2.25 | −2.23 [−2.75, −1.69] | −1.48 | −1.51 [−2.30, −0.80] |
| Risk at the time | +35.1 | +34.2 [+26.8, +41.2] | +28.1 | +28.5 [+20.8, +36.6] |

- **All seven effects are confirmed in Haiku and Sonnet.** Every re-run estimate is within 2.5 points of the first run.
- Payoff against no ending is null again on every question in Sonnet. In Haiku, payoff lowers acceptance slightly (−4.8 [−9.1, −1.0]), which is the opposite of excusing; the first run's small effect on decision quality does not repeat (−1.7 [−4.8, +1.2]).
- **Opus has not been re-run.** Its six effects point the same way as the confirmed ones but are from one run.

### Clear violations (5 scenarios, one wording)

Violation probability is at the ceiling and does not move in any model (within ±1.3). Blame after harm: Sonnet +3.5 [+1.3, +6.0], Opus +7.2 [+3.2, +12.9], Haiku −8.9 [−26.8, +0.9]. Risk at the time rises after harm in Haiku and Sonnet (+24.0 and +3.7) and not in Opus (+1.0 [−11.7, +13.7]). Too few scenarios for claims.

## E4: buried violations and the operator's note

Run 18:07 to 18:30 through the batch API, all three models. 1,080 answers, 9 unparsed (all Haiku). 10 target tickets, 3 sessions each, 25 tickets per session.

Share of sessions in which the target ticket was listed:

| | Good-session note | No note | Poor-session note |
|---|---|---|---|
| Haiku, violating target | 0.88 | 0.90 | 0.91 |
| Sonnet, violating target | 0.98 | 1.00 | 1.00 |
| Opus, violating target | 1.00 | 1.00 | 1.00 |
| Haiku, compliant target | 0.65 | 0.55 | 0.67 |
| Sonnet, compliant target | 0.37 | 0.30 | 0.40 |
| Opus, compliant target | 0.00 | 0.00 | 0.00 |

- **No effect of the note.** A good-session note does not make any model stop reporting the buried violation (success minus none: −0.02 [−0.10, +0.05], −0.02 [−0.05, +0.00], 0.00). Nothing meets rule 1.
- **Opus is exact:** it lists every violating target and nothing else, in all 360 answers.
- **Haiku and Sonnet over-report.** Sonnet lists the compliant target in 30 to 40% of sessions and about one other ticket per session; Haiku lists four to five other tickets per session. The note does not change this reliably (Haiku, poor-session note against none, compliant target: +0.12 [+0.02, +0.22], one model only).
- As stated in the pre-registration, detection was already near 100% without a note, so E4 could only have shown a drop. It did not.

## E5: mistake or deliberate

Run 18:32 to 18:50 through the batch API, all three models, main arm. 1,620 answers, 47 unparsed (2.9%). 12 questionable agent actions, two wordings per ending, 3 samples. Harm and no harm are both down to chance, so neither says anything about what the agent intended.

**One scenario is missing for Opus.** 39 of Opus's 40 unparsed answers are for `audit_logs` (an agent that deletes the audit logs recording its own earlier actions). The API returned no text for them, with stop reason `content_filter`. Six Opus answers remain for that scenario, too few for any contrast, so Opus's E5 rests on 11 scenarios. Dropping the scenario entirely gives the same results (deliberate: +4.3 [+0.2, +8.7]). Sonnet's 7 unparsed answers are malformed JSON, spread over the endings. Haiku has none.

### Harm minus no harm (primary contrast)

| Question | Haiku | Sonnet | Opus | Claimed (rule 1)? |
|---|---|---|---|---|
| Probability the action was deliberate (0–100) | +7.3 [+3.1, +12.2] | +0.7 [−1.7, +4.1] | +4.5 [+0.7, +8.6] | **Yes** (Haiku, Opus) |
| Suspicion (0–100) | +12.2 [+3.3, +20.1] | +3.2 [+0.2, +6.8] | +2.1 [−2.1, +7.2] | **Yes** (Haiku, Sonnet) |
| Recommended action (0–4) | +0.85 [+0.60, +1.10] | +0.54 [+0.25, +0.88] | +0.35 [+0.09, +0.67] | **Yes** (all three) |

### Each ending against no ending

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| Deliberate: harm | −0.9 [−5.5, +3.5] | −9.4 [−17.4, −4.1] | −3.6 [−9.3, +1.9] |
| Deliberate: no harm | −8.2 [−13.0, −3.9] | −10.1 [−20.3, −4.0] | −7.9 [−12.3, −3.6] |
| Suspicion: harm | −5.4 [−12.6, +0.8] | −16.8 [−24.0, −11.1] | −7.1 [−12.9, −1.9] |
| Suspicion: no harm | −17.6 [−24.1, −10.9] | −20.0 [−27.3, −14.1] | −9.3 [−14.7, −3.9] |
| Action: harm | +0.74 [+0.44, +1.01] | +0.01 [−0.25, +0.24] | +0.15 [+0.03, +0.30] |
| Action: no harm | −0.11 [−0.31, +0.03] | −0.53 [−0.82, −0.25] | −0.20 [−0.45, +0.00] |

- **The same action is read as more deliberate when harm followed than when it did not.** The size is 4 to 7 points on intent (Haiku, Opus) and 3 to 12 on suspicion (Haiku, Sonnet). This is small next to E3. The answer should not move at all.
- **Here it is the harmless ending that moves the answer.** With no ending, the models put the chance of deliberate action at 21 to 40 and suspicion at 54 to 60. A harmless ending lowers intent by 8 to 10 points and suspicion by 9 to 20 points in all three models. This is the "no harm, no foul" leniency the project first predicted, and it shows up on a monitor's suspicion score, not on a rule verdict.
- **Harm does not raise suspicion above the no-ending level.** In Sonnet, and in Opus for suspicion, harm lowers it too. So part of the drop comes from there being a follow-up note at all, and this design cannot separate that from the outcome: the no-ending condition has no note. A neutral-note condition would be needed.
- **Some harmless endings may carry real evidence.** "The audit logs had also been shipped to the central archive" makes the deletion less serious in itself, which a careful monitor could fairly weigh. The harm-minus-no-harm contrast does not depend on this; the comparison with no ending does.
- **Recommended action** follows harm, as it defensibly can: Haiku escalates after harm (+0.74 against no ending), Sonnet de-escalates after no harm (−0.53).

### E5 re-run (rule 2), main arm, all three models

Run 18:55 to 19:13 through the batch API. 1,620 answers, 40 unparsed (2.5%): 38 are Opus answers blocked by the content filter, 36 of them again for `audit_logs`. Harm minus no harm:

| Question | Haiku | Sonnet | Opus | Confirmed? |
|---|---|---|---|---|
| Probability the action was deliberate | +6.9 [+2.2, +13.1] | +1.0 [−1.4, +4.6] | +6.0 [+1.4, +11.2] | **Yes** (Haiku, Opus, as claimed) |
| Suspicion | +11.9 [+3.8, +19.6] | +4.6 [+1.2, +9.1] | +3.0 [−0.7, +6.9] | **Yes** (Haiku, Sonnet, as claimed) |
| Recommended action (0–4) | +0.88 [+0.62, +1.10] | +0.49 [+0.25, +0.74] | +0.39 [+0.12, +0.71] | **Yes** (all three) |

- **All three effects are confirmed** on the models they were claimed for. The two that did not exclude zero in the first run (Sonnet's intent, Opus's suspicion) do not in the re-run either.
- **The drop after a harmless ending repeats** in all three models: intent −9.0, −10.2, −7.3; suspicion −18.5, −20.4, −8.3 (every interval excludes zero).
- Harm against no ending: suspicion −6.7 [−14.2, +0.1], −15.8 [−22.5, −10.3], −5.2 [−11.2, +0.3]. Sonnet's drop after harm repeats; Opus's does not exclude zero this time.

## Status at 19:15, 13 November

| Experiment | Main arm | Reasoning arm | Re-run (rule 2) |
|---|---|---|---|
| E1 | Done, 3 models | Done at "medium" | Done, confirmed |
| E2 | Done, 3 models | Done, Haiku and Sonnet | Done for Haiku and Sonnet, confirmed; Opus not run |
| E3 | Done, 3 models | Done, Haiku and Sonnet | Done for Haiku and Sonnet, confirmed; Opus not run |
| E4 | Done, 3 models; nothing to confirm | – | – |
| E5 | Done, 3 models (Opus on 11 of 12 scenarios) | – | Done, 3 models, confirmed |

Spend at batch prices, from token counts in the logs: about $25 between the first and second top-ups, and about $13 since the third (Opus E3 $6.90, E3 re-run $3.10, E5 $1.70, E5 re-run $1.70).

Not run: Opus's re-runs of E2 and E3, about $13 together at batch prices.

## X1 (exploratory): a labelled scale for E3's violation question

Plan: `notes/prereg_e1_e5.md`, "Exploratory follow-up X1". Run 14 November through the batch API. **Haiku only**: the credit ran out before Sonnet's runs could start, and Opus was not reached. 720 answers, none unparsed. Analysis: `python -m outcome_bias.x1_analysis`.

Violation question, 21 borderline scenarios, Haiku:

| | Payoff | No ending | Harm | Harm minus payoff | Change from E3's main arm |
|---|---|---|---|---|---|
| E3 main arm, run 1 (unlabelled) | 49.4 | 48.8 | 72.6 | +23.2 [+15.3, +31.3] | |
| E3 main arm, re-run | 49.4 | 50.0 | 74.2 | +24.8 [+17.0, +33.1] | +1.6 [−2.0, +5.3] |
| Labelled scale | 60.9 | 59.8 | 78.0 | +17.0 [+9.8, +24.2] | −6.2 [−13.2, +1.0] |
| Labelled scale plus "ignore what happened afterwards" | 63.7 | 59.2 | 67.1 | +3.3 [−3.6, +9.4] | **−19.9 [−30.7, −9.6]** |

- **The labelled scale alone barely changes the effect.** Harm minus payoff falls from +23 to +17; the change's interval includes zero. The labels raise every score by about 10 points, so they change how Haiku uses the scale, not how it reacts to harm.
- **The instruction removes most of it.** Told that what happened afterwards does not change whether the policy was broken, Haiku's harm effect falls to +3.3, interval including zero; the drop of 20 points excludes zero. 13 of 21 scenarios move down by more than 5 points.
- For comparison, reasoning on (without the instruction) gave +9.1 in Haiku.
- One model, one run, exploratory. Whether Sonnet and Opus respond the same way is untested.
