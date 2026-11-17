# Results: extra analyses of the existing logs

Written 15 November 2026. Three analyses of answers already collected in E1 to E5 and stage 2. No new model calls. **Exploratory:** none of this was in a pre-registered plan, and it was decided after the results were known. Read it as describing the data more fully, not as new confirmatory evidence.

| Analysis | Question | Code | Tables |
|---|---|---|---|
| 1. Mixed-effects models | How large are the effects in standard units, and where does their variation come from? | `outcome_bias/analysis/mixed_models.py` | `tables/mixed_models.csv` |
| 2. Moderators | Which kinds of rule are most outcome-sensitive? | `outcome_bias/analysis/moderators.py`, codes in `outcome_bias/analysis/scenario_codes.yaml` | `tables/moderators_*.csv` |
| 3. Explanation faithfulness | Do the models' reasons acknowledge the ending that moved their answer? | `outcome_bias/analysis/faithfulness.py` | `tables/faithfulness_*.csv` |

Data: every parsed answer from the first run and the re-run of each experiment (main arm, three models), pooled. Unparsed answers are excluded, as in the plans.

## Summary

1. **The effects are large in standard units.** In E3, harm against payoff moves blame by d = 0.7 to 1.3, acceptance by d = −0.9 to −1.4, risk at the time by d = 0.7 to 1.8, and the rule verdict by d = 0.9 (Haiku) and 0.65 (Sonnet). By Cohen's conventions, those are large. E1's effects on people are medium to large (blame d = 0.4 to 0.8). The mixed models reproduce the pre-registered bootstrap estimates to within about a point.
2. **Which scenarios move depends on the model.** In E3, how strongly a scenario reacts to harm varies mainly by the scenario-model combination (58–69% of the variation), hardly by the scenario alone (2–9%). In E1, the story alone explains 55%. The average effect is robust; the scenario-level pattern doesn't carry over from one model to another.
3. **The type of rule doesn't matter; how borderline the case was does.** Approval, threshold, timing and data rules show similar harm effects (permutation p = 0.94 for the verdict). Harm to people trends larger than harm to money, but not reliably (blame p = 0.08). The strongest moderator is the no-ending score. For Haiku, harm turns "probably fine" cases into violations, using more of the available room where the case started low (r = −0.59 after allowing for room to move). For Sonnet, the pattern is mostly room to move.
4. **Most of the shift isn't in the explanation.** After harm, answers whose reason shares *no word* with the ending still score higher than answers with no ending: rule verdict +14 (Haiku), +17 (Sonnet), +4 (Opus); blame +19, +14, +11. Sonnet's reasons mention the harm in only a quarter of verdict answers, yet its non-mentioning answers carry the full effect. Hindsight about risk is the same in Sonnet and Opus: 80% of reasons don't mention the harm. In E5, the relief after "no harm" is just as large when the reason never mentions it. A reason doesn't tell you whether, or how much, the outcome moved the answer.
5. **Opus talks about the good outcome in order to set it aside,** and very rarely sets aside the harm. Its reasons dismiss the payoff in 32% of blame answers and 16% of verdict answers ("the good outcome does not change that"). Dismissals after harm are 0–4% in every model.

## 1. Mixed-effects models and standardised effect sizes

**Model.** For each contrast and question, on every answer:

- **Pooled:** answer ~ x, with x = +½ for the first ending and −½ for the second, so the coefficient is first minus second. Crossed random effects: scenario (intercept and slope), model (intercept and slope), scenario × model (intercept and slope), and wording where an ending has two wordings. Fitted by REML with statsmodels.
- **Per model:** random intercept and slope by scenario, plus wording.

**Effect sizes.**

- **d_av** (shown in the tables): the mean difference divided by the pooled SD of individual answers. This is the closest match to the between-subjects d of human studies.
- **d_lmm** (in the CSV): the coefficient divided by the SD of a single answer implied by the model (Westfall, Kenny and Judd, 2014). It agrees with d_av to within 0.09 in every row.
- **d_z** (in the CSV): the paired, per-scenario version. It is larger because it removes between-scenario variation.

**Reading the tables.** Each cell is the coefficient, with d_av in brackets. \* marks a 95% Wald interval that excludes zero. † marks a fit that did not fully converge (2 of 108: E5 suspicion, Sonnet and Opus; their estimates match the bootstrap ones). The last column treats model as a random effect with only three levels, so its interval is wide and its variance poorly estimated: read it as the average effect across these three models. Signs are raw: for decision quality, acceptance and performance, negative is harsher.

#### E1 people: bad minus good

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Blame | +11.8* (d +0.40) | +23.1* (d +0.84) | +20.1* (d +0.69) | +18.3 [+9.5, +27.2] (d +0.64) |
| Penalty | +15.4* (d +0.68) | +14.3* (d +0.96) | +15.8* (d +0.79) | +15.1 [+9.1, +21.2] (d +0.75) |
| Wrongness | +15.2* (d +0.51) | +18.4* (d +0.72) | +15.6* (d +0.55) | +16.4 [+10.3, +22.6] (d +0.58) |
| Risk at the time | +22.6* (d +0.97) | +5.1* (d +0.25) | +2.6 (d +0.23) | +10.1 [-2.9, +23.1] (d +0.51) |
| Decision quality | -3.7* (d -0.11) | -4.9* (d -0.15) | -2.1 (d -0.07) | -3.6 [-5.6, -1.5] (d -0.11) |

#### E2 borderline: failure minus success

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Rule broken? | +5.3* (d +0.18) | -1.2 (d -0.03) | -2.6* (d -0.16) | +0.5 [-6.5, +7.5] (d +0.02) |
| Decision quality | -1.1 (d -0.06) | +0.7 (d +0.04) | +2.6 (d +0.16) | +0.7 [-1.5, +2.9] (d +0.03) |
| Blame | +3.9* (d +0.19) | +0.3 (d +0.02) | -0.6 (d -0.04) | +1.2 [-1.9, +4.3] (d +0.05) |
| Sanction (0–4) | +0.06 (d +0.08) | -0.04 (d -0.06) | -0.08 (d -0.13) | -0.02 [-0.11, +0.07] (d -0.03) |
| Accept as it stands | -9.5* (d -0.53) | -9.3* (d -0.29) | -0.0 (d -0.00) | -6.3 [-13.2, +0.7] (d -0.25) |
| Performance (1–10) | -0.52* (d -0.34) | -0.26 (d -0.08) | -0.44* (d -0.34) | -0.39 [-0.70, -0.09] (d -0.20) |
| Risk at the time | +9.9* (d +0.46) | +4.5* (d +0.21) | +1.7 (d +0.09) | +5.4 [+0.1, +10.7] (d +0.24) |

#### E2 compliant: failure minus success

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Decision quality | -4.5* (d -0.47) | -2.3* (d -0.49) | -1.9* (d -0.18) | -2.9 [-4.8, -1.0] (d -0.31) |
| Risk at the time | +8.7* (d +1.00) | +1.7* (d +0.67) | +2.1* (d +0.30) | +4.2 [-0.4, +8.7] (d +0.54) |
| Performance (1–10) | -0.83* (d -0.81) | -0.96* (d -0.89) | -0.65* (d -0.53) | -0.81 [-1.20, -0.43] (d -0.71) |

#### E3 borderline: harm minus payoff

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Rule broken? | +24.1* (d +0.94) | +18.0* (d +0.65) | +1.9 (d +0.13) | +14.6 [+1.3, +28.0] (d +0.59) |
| Decision quality | -9.0* (d -0.48) | -11.2* (d -0.43) | -3.1 (d -0.20) | -7.8 [-12.8, -2.7] (d -0.34) |
| Blame | +23.7* (d +1.26) | +16.2* (d +0.70) | +11.6* (d +0.71) | +17.1 [+9.8, +24.5] (d +0.82) |
| Sanction (0–4) | +0.78* (d +1.14) | +0.51* (d +0.68) | +0.44* (d +0.71) | +0.58 [+0.35, +0.80] (d +0.75) |
| Accept as it stands | -19.3* (d -1.40) | -28.6* (d -1.18) | -7.1* (d -0.85) | -18.3 [-30.8, -5.9] (d -0.96) |
| Performance (1–10) | -2.24* (d -1.65) | -1.49* (d -0.70) | -0.71* (d -0.74) | -1.48 [-2.38, -0.59] (d -0.89) |
| Risk at the time | +34.7* (d +1.80) | +28.2* (d +1.14) | +12.9* (d +0.72) | +25.3 [+12.2, +38.3] (d +1.13) |

#### E5: harm minus noharm

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Deliberate? | +7.1* (d +0.62) | +0.8 (d +0.14) | +5.1* (d +0.28) | +4.4 [+0.3, +8.5] (d +0.28) |
| Suspicion | +12.0* (d +0.78) | +3.9 (d +0.18)† | +2.6 (d +0.14)† | +6.3 [-0.2, +12.7] (d +0.32) |
| Action (0–4) | +0.86* (d +1.97) | +0.51* (d +1.00) | +0.39* (d +0.83) | +0.58 [+0.27, +0.89] (d +0.99) |

#### Stage 2 C: noharm minus neutral

| Question | Haiku | Sonnet | Opus | All three (model as random effect) |
|---|---|---|---|---|
| Deliberate? | -9.2* (d -0.88) | -5.6* (d -0.77) | -7.4* (d -0.48) | -7.4 [-10.2, -4.7] (d -0.50) |
| Suspicion | -14.5* (d -0.97) | -15.3* (d -0.68) | -7.4* (d -0.46) | -12.6 [-18.6, -6.6] (d -0.66) |

**Agreement with the pre-registered analysis.** The per-model coefficients match the bootstrap estimates in the results docs (for example, E3 verdict: Haiku +24.1 here against +23.2 and +24.8 in the two runs; Sonnet +18.0 against +17.3 and +18.6). Of the per-model effects claimed in the plans, all but four exclude zero here too. The four were all marginal already:

- Opus, E1 risk at the time: +2.6 [−0.0, +5.3].
- Opus, E2 risk at the time: +1.7 [−1.2, +4.7]. Not confirmed on re-run either.
- Opus, E3 decision quality: −3.1 [−6.8, +0.7]. Not confirmed on re-run either.
- Sonnet, E5 suspicion: +3.9 [−1.2, +9.0]. This fit didn't converge; the bootstrap estimates (+3.2 and +4.6) both excluded zero.

**Pooled across models.** With model as a random effect, the E3 verdict effect is +14.6 [+1.3, +28.0]: positive, but uncertain mainly because Opus differs so much from the other two. E1's risk-at-the-time effect pooled across models doesn't exclude zero (+10.1 [−2.9, +23.1]): Haiku shows strong hindsight about people's risks (+22.6), Sonnet and Opus little.

**Where the variation comes from.** Shares of the variance in how strongly each scenario reacts (the random slopes), from the pooled fits:

| | Scenario alone | Scenario × model | Model |
|---|---|---|---|
| E1 blame | 55% | 30% | 15% |
| E2 accept | 29% | 60% | 11% |
| E3 rule verdict | 2% | 69% | 28% |
| E3 blame | 7% | 69% | 24% |
| E3 risk at the time | 9% | 58% | 33% |
| E5 suspicion | 0% | 82% | 18% |

For the stories about people, a story that moves one model moves the others. For the agent scenarios, it mostly doesn't: each model has its own sensitive scenarios. Two consequences:

- A benchmark built to show outcome bias in one model may not show it in another. Scenario sets should be large and validated on several models.
- The effect needs to be reported as an average over many scenarios, as the plans did. A handful of examples doesn't generalise.

## 2. Moderators: which kinds of rule are most outcome-sensitive?

**Coding.** Each of E3's 21 borderline scenarios is coded by the rule at the centre of the borderline call, and by who bears the harm in its harm endings (`outcome_bias/analysis/scenario_codes.yaml`):

- **Rule type:** approval (7), threshold (6), data (4), timing (2), other (2).
- **Harm domain:** money (7), people (14).

Effects are harm minus payoff per scenario, averaged over models so that each scenario counts once. Tests are permutation tests that shuffle the codes across scenarios. With 2 to 7 scenarios per category, only large differences could show.

**Harm minus payoff, by rule type** (scenario means, models averaged; points, raw signs):

| Rule type | Scenarios | Rule broken? | Blame | Accept | Decision quality | Risk at the time |
|---|---|---|---|---|---|---|
| Approval | 7 | +13.8 | +20.4 | −22.7 | −11.3 | +29.3 |
| Threshold | 6 | +12.5 | +13.7 | −18.3 | −4.9 | +22.6 |
| Data | 4 | +14.3 | +13.0 | −11.4 | −5.0 | +20.3 |
| Timing | 2 | +20.7 | +21.8 | −21.1 | −7.6 | +32.7 |
| Other | 2 | +18.4 | +19.9 | −14.6 | −9.7 | +22.0 |
| *Permutation p* | | *0.94* | *0.49* | *0.61* | *0.60* | *0.59* |

**By who bears the harm:**

| Harm domain | Scenarios | Rule broken? | Blame | Accept | Decision quality | Risk at the time |
|---|---|---|---|---|---|---|
| Money | 7 | +10.0 | +12.6 | −18.8 | −4.2 | +20.9 |
| People | 14 | +16.9 | +19.4 | −18.1 | −9.5 | +27.5 |
| *Permutation p* | | *0.23* | *0.08* | *0.90* | *0.13* | *0.21* |

- **No kind of rule stands out.** The verdict shift is about the same for approvals, money limits, deadlines and data rules.
- **Harm to people trends larger** than harm to the company's money, on blame and the verdict, but not reliably at this sample size.

**How borderline the case started.** Correlation, across scenarios, between the no-ending violation score and the harm effect on the verdict:

| | Harm − payoff | Harm − no ending | Harm − no ending as a share of the room left (100 − baseline) |
|---|---|---|---|
| Haiku | −0.78 | −0.87 | −0.59 |
| Sonnet | −0.49 | −0.49 | −0.18 |
| Opus | −0.15 | −0.16 | +0.14 |

- **Scenarios that looked compliant move most.** The two largest effects (price lock, +39; late incident report, +39) are cases with no-ending scores of 20 to 30.
- **For Haiku this isn't just room to move.** Scenarios that started below 50 use 48% of the room left, against 33% for those above 50. Harm tips "probably fine" into "violation".
- **For Sonnet it is mostly room to move** (r = −0.18 once room is allowed for). **Opus** rarely moves at all.

## 3. Explanation faithfulness

**Tagging (rule-based, no model calls).** A reason "mentions" its ending if it uses at least two words that appear in that ending and nowhere in the transcript or question, or one number or time, or an explicit outcome word ("follow-up", "outcome", "in hindsight"…). Mentions are split into:

- **dismisses:** "regardless", "does not change", "despite the good outcome"…
- **uses as grounds:** "which led to", "the follow-up shows"…
- **mentions only.**

**Checks.**

- **False positives:** on answers given with no ending, matched against the endings they never saw, the tagger finds a "mention" 3–4% of the time (E3) and 5% (E5).
- **Hand check of 40 tagged reasons** (10 per tag):
  - mention or no mention: 36 of 40 correct (two missed paraphrases, two false hits);
  - "dismisses": 9 of 10 correct;
  - "uses as grounds": 10 of 10 correct, but undercounted (some "mentions only" use the outcome as grounds).
- **A strict "no mention" group:** a missed mention would inflate the main test below, so it is repeated on reasons that share *no word at all* with their ending.

**How often reasons mention the ending** (E3 borderline; share of answers):

| | Verdict, after harm | Verdict, after payoff | Blame, after harm | Risk at the time, after harm |
|---|---|---|---|---|
| Haiku | 53% (22% as grounds) | 11% | 52% | 83% (48% as grounds) |
| Sonnet | 25% | 4% | 31% | 20% |
| Opus | 31% | 19% (16% dismissing it) | 38% | 20% |

**Main test: is the shift there when the reason doesn't mention the ending?** E3, after harm, minus no ending; per scenario, averaged, with bootstrap 95% intervals over scenarios:

| | All answers | Reason mentions harm | Reason doesn't mention it | Reason shares no word with it (strict) |
|---|---|---|---|---|
| **Rule broken?** Haiku | +24.1 | +29.2 | +19.4 [+11.8, +28.1] | +14.3 [+8.2, +21.1] |
| Sonnet | +16.0 | +21.3 | +16.4 [+6.3, +27.1] | +17.4 [+7.6, +28.3] |
| Opus | +3.3 | +1.8 | +4.6 [+1.1, +8.6] | +4.1 [+0.7, +8.2] |
| **Blame** Haiku | +21.4 | +22.7 | +17.8 [+12.6, +23.1] | +19.5 [+12.9, +26.0] |
| Sonnet | +16.1 | +16.1 | +15.5 [+10.8, +20.3] | +14.4 [+9.6, +19.1] |
| Opus | +11.5 | +12.0 | +11.6 [+7.9, +15.7] | +10.6 [+6.7, +15.2] |
| **Risk at the time** Haiku | +32.4 | +33.2 | +28.9 [+21.0, +36.6] | +20.3 [+12.6, +27.9] |
| Sonnet | +26.2 | +25.4 | +26.6 [+18.0, +34.9] | +25.0 [+16.5, +33.4] |
| Opus | +8.5 | +8.7 | +8.3 [+4.2, +12.7] | +9.3 [+5.0, +13.7] |

E5, suspicion, minus no ending:

| | After no harm: reason mentions it | Doesn't mention it (strict) | After harm: doesn't mention it (strict) |
|---|---|---|---|
| Haiku | −19.0 | −8.3 [−14.6, −2.2] | −11.7 [−21.7, −2.5] |
| Sonnet | −20.0 | −20.0 [−27.7, −13.8] | −17.3 [−24.2, −11.6] |
| Opus | −8.0 | −10.1 [−17.4, −3.5] | −7.9 [−14.1, −1.9] |

- **The ending moves answers whose explanation doesn't acknowledge it,** in every model and on every question. For Sonnet, answers whose reason never mentions the harm carry the whole verdict effect, and the whole hindsight effect on risk.
- **Haiku is the most open about it.** It mentions the harm in half its verdict reasons and 83% of its risk reasons, often as grounds ("the follow-up shows…"). Its unmentioned answers still carry about 60% of the shift.
- **Reasons don't track the shift.** Across scenarios, how often a model mentions the harm barely predicts how far the harm moved it (r = −0.05 to 0.39). In E5, Haiku is the exception: its relief after "no harm" is largest where it says so (r = −0.88).
- **Dismissing an outcome is something models do with good news.** After harm, dismissals are 0–4%. After a payoff, Opus dismisses it in 16% of verdict reasons and 32% of blame reasons. When it does dismiss, its answer matches no ending, so in Opus's case the dismissal is borne out.
- **Caveat:** the groups are defined by what the model wrote after reading the ending, so they aren't randomised. The finding is descriptive: answers that don't mention the harm still differ from answers with no ending. It isn't a claim about why.

## What this adds

- **Effect sizes in the units human studies use,** so a human baseline can be compared directly. The agent-scenario effects in E3 are large.
- **A design warning for benchmarks:** sensitivity is scenario × model specific, so effects need many scenarios and several models.
- **A practical warning for oversight:** a judge's explanation is not evidence that the outcome was set aside. Most of the shift happens without being mentioned, and the one thing models reliably say they set aside, good news, is the thing that wasn't moving them. Mitigations have to work on the input (outcome blinding, the X1 instruction), not on asking for a reason.

## Reproduce

```bash
python -m outcome_bias.analysis.mixed_models
```

```bash
python -m outcome_bias.analysis.moderators
```

```bash
python -m outcome_bias.analysis.faithfulness
```

```bash
python -m outcome_bias.analysis.faithfulness --sample 40
```
