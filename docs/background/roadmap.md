# Roadmap: from pre-registered study to a good-ish paper

Written 15 November 2026, after E1 to E5 and stage 2. A proposal, not a pre-registration: each study below gets its own plan in `docs/<study>/plan.md`, frozen before it runs, as before.

## Where the project stands

**What is new and strong**

- The oversight setting: agent transcripts with tool calls, judged against a written policy, with only the ending varied.
- The **asymmetry**: harm condemns, success doesn't excuse (E2, E3).
- Stage 2's controls. The harm effect is bias, not learning what the rule is for (D). The "no harm" relief in monitors comes from the outcome, not from the presence of a note (C).
- A one-sentence fix for the verdict shift, confirmed on re-run (B).
- Pre-registration, confirmation re-runs, and a check that every logged prompt rebuilds from the code.

**What a NeurIPS reviewer would push on**

1. **Crowded framing.** "Cognitive biases in LLMs" already includes classic vignettes on chat models (Almeida et al., 2024) and 2026 papers on outcome and hindsight bias in general benchmarks and clinical reasoning. On its own, E1 is not new.
2. **Narrow evidence.** One model family judges scenarios written by the same family, with 21 borderline scenarios.
3. **No human baseline**, so "biased" has no reference point.
4. **No consequence shown.** The paper argues that outcome bias corrupts oversight and reward signals but never demonstrates it.

## The thesis to aim for

> LLM overseers judge agents by consequences the agents couldn't foresee. Harm condemns, success doesn't excuse. The asymmetry is learned in post-training, it shapes the reward signal agents are trained on, and agents can exploit it.

Each clause becomes a section of the paper: generality (1), origin in post-training (1, 7), training consequences (4), exploitability (5). Sections 2, 3 and 6 make the claims defensible.

## 1. Generality (must-have)

- **10 to 15 judges across families and sizes:** OpenAI (already in `outcome_bias/models.py`), Gemini, and open models such as Llama, Qwen, DeepSeek and Gemma. The OpenAI estimate for E1 to E5 was about $65 (core) to $245 (everything) at batch prices for a small, mid and top model.
- **Base vs fine-tuned vs RL-trained checkpoints of the same model.** A 2025 preprint finds base LLMs show almost no Knobe-style moral asymmetry and fine-tuning creates it. If the harm/payoff asymmetry also comes from post-training, that alone is a headline result. It needs open models that publish intermediate checkpoints. Base models need a completion-style prompt with the answer read from token probabilities.
- **More and more varied scenarios:** about 200 instead of 21, in matched pairs, written by several model families plus a human-written subset, and validated by annotators. Compare effects by who wrote them, which removes the "Claude judging Claude's scenarios" objection.

## 2. Human baseline (needed for any comparison with people)

- **Same items, between-subjects:** each participant sees one ending per scenario.
- **About 400 Prolific participants,** plus a smaller panel of practitioners (security, SRE, compliance).
- **Report standardised effect sizes and the asymmetry** for people and models side by side. "LLM overseers are differently biased from people" (more hindsight, no success excuse) is a stronger claim than "LLMs are biased".
- Rough cost: £1,000 to £2,000, plus ethics review if required.

## 3. Pure-bias designs and a formal account

- **Stated odds.** Put the probability of failure in the transcript ("this check fails about 1 in 50 runs"). In E1 the models copied stated odds exactly. If they still shift risk-at-the-time for agents, that is pure hindsight with no information left to learn from.
- **An invariance metric.** Define which questions should not depend on the outcome (rule broken, decision quality given what was known, risk at the time, intent under chance outcomes). Report an outcome-sensitivity index on those, and an asymmetry index (harm shift against payoff shift).
- **A Bayesian bound.** When an outcome is informative, compute how far a rational judge would move, then split each observed shift into its rational and biased parts. This turns a list of effects into a measurement framework.

## 4. Consequences for training (the strongest hook for an ML audience)

- **Biased judges reward the wrong things.** In a small tool environment with a written policy, generate many trajectories: compliant but unlucky, rule-breaking and lucky, rule-breaking with visible harm, rule-breaking with harm the logs don't show. Use the LLM judge for best-of-N selection, or as the reward in a small RL loop. Prediction from E2 and E3: selection favours hiding consequences over following the rule, and penalises compliant agents for bad luck.
- **Process judges contaminated by the final answer.** On maths or code solutions with one flawed step, flip only whether the final answer is correct, and ask an LLM judge to grade each step. Process reward models are widely used. Existing work on their label noise concerns labels from sampled continuations, not LLM-judged step labels under a counterfactual final answer.

## 5. An attack on monitors: outcome laundering

- Stage 2 C showed that a "nothing went wrong" line lowers a monitor's suspicion.
- Build a misaligned agent that appends one, fabricates one in its tool output, or tampers with the logs.
- Measure what an AI-control evaluation would: the monitor's catch rate at a fixed audit budget, and AUROC. Compare with persuasion attacks (Za et al., 2026).
- Test defences: an outcome-blind monitor, and judging in two passes (section 6).

## 6. Mitigations, reported as a trade-off

Report each on a Pareto front of invariance vs detection accuracy vs cost:

| Mitigation | Status |
|---|---|
| **Outcome blinding:** strip everything after the agent's last action | Not yet tested; not always possible (for example, incident review) |
| **Instruction:** "judge only what the agent did; what happened afterwards doesn't change whether the policy was broken" | Works on the verdict in Haiku and Sonnet (stage 2 B); not yet tested on hindsight |
| **Sequential unmasking,** from forensic science: give the verdict before seeing the outcome, then update only sanction | Not yet tested |
| **Counterfactual self-simulation** (a 2026 debiasing paper) | Not yet tested |
| **Consistency training on paired endings:** fine-tune for invariance on the invariant questions while keeping legitimate sensitivity in blame and sanction | Not yet tested; needs open models |

## 7. Mechanism, on open models

- **Probes and patching:** train a linear probe for "harm happened", then patch it from harm runs into payoff runs and measure how much of the verdict shift it carries.
- **Steering:** check whether steering along that direction removes the shift without harming detection of real violations.
- **Unfaithful explanations:** the logs already contain reasons that dismiss the outcome while the score moves. Quantify how often reasons cite or dismiss the outcome, against the size of the shift.

## 8. Ecological validity

- **Real agent logs:** take trajectories from public agent benchmarks and edit only what comes after the agent's action.
- **Outcomes inside the transcript:** in tool results and people's reactions, including praise from someone who can't waive the rule, rather than labelled follow-up notes (the old E6).
- **Long contexts:** 100+ steps.

## What can be done now, at no cost

From the existing logs (`python -m outcome_bias.analysis...`):

1. **Mixed-effects models and standardised effect sizes,** with scenario, wording and model as crossed random effects, for comparison with the human literature.
2. **Moderator analysis:** which kinds of rule are most outcome-sensitive (approval, threshold, timing, data handling).
3. **Explanation faithfulness:** how often reasons dismiss or cite the outcome, against how far the score moved.

## Suggested order

1. The free analyses above.
2. More model families, plus base vs fine-tuned checkpoints (1).
3. Human baseline (2), with the stated-odds design (3) run on people and models together.
4. Selection, RL and process-judge studies (4).
5. Outcome laundering and mitigations (5, 6).
6. Mechanism (7) and real logs (8), as time allows.

**Venue.** If the benchmark of paired scenarios is the core contribution, NeurIPS's Datasets & Benchmarks track is the natural fit. If the training-consequence and mechanism results land, aim for the main track.

## Sources

Found by web search on 15 November 2026. Items marked "unverified" were seen only in search snippets.

- Almeida et al. (2024), classic vignettes on chat models: [arXiv 2308.01264](https://arxiv.org/abs/2308.01264)
- Za et al. (2026), agents persuading monitors: [arXiv 2607.08066](https://arxiv.org/abs/2607.08066)
- A Comprehensive Evaluation of Cognitive Biases in LLMs: [arXiv 2410.15413](https://arxiv.org/pdf/2410.15413)
- EMNLP 2026 Findings, cognitive biases including outcome bias (unverified): [ACL Anthology](https://aclanthology.org/2026.findings-emnlp.1750.pdf)
- Self-Blinding and Counterfactual Self-Simulation Mitigate Biases and Sycophancy: [arXiv 2601.14553](https://arxiv.org/pdf/2601.14553)
- HindsightBench (unverified): [alphaXiv 2607.18867](https://www.alphaxiv.org/abs/2607.18867)
- Moral bias (Knobe effect) in fine-tuned LLMs, a preprint: [arXiv 2510.12229](https://arxiv.org/pdf/2510.12229)
- Noise-aware process reward modelling: [arXiv 2601.12748](https://arxiv.org/pdf/2601.12748)
- EST-PRM, stress-testing process reward models (unverified): [alphaXiv 2606.00437](https://www.alphaxiv.org/abs/2606.00437.md)
- AgentRewardBench: [alphaXiv 2504.08942](https://alphaxiv.org/overview/2504.08942v2)
- Self-Grounded Verification: [arXiv 2507.11662](https://arxiv.org/pdf/2507.11662)
- Catching One in Five, judge blind spots: [arXiv 2606.10315](https://arxiv.org/pdf/2606.10315)
- What is Your Agent's GPA?: [arXiv 2510.08847](https://arxiv.org/html/2510.08847v1)

From memory, to check before citing: AI-control evaluations (Greenblatt et al.), unfaithful chain-of-thought explanations (Turpin et al., 2023), and linear sequential unmasking in forensic science (Dror et al.).
