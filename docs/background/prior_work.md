# Prior work

Searched 13 November 2026. Items marked (unverified) were seen only in search snippets.

## Closest work

1. **Outcome bias in people.** Baron and Hershey (1988). A pre-registered replication (Aiyer et al., 2023, N = 692) found a larger effect than the original, and it held even among participants who said outcomes should not count. [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12372742/)
2. **Classic vignettes on chat models.** This is the overlap the plan flagged.
   - Almeida et al. (2024, *Artificial Intelligence*) replicated eight experiments on GPT-4, Claude 2.1, Gemini Pro and Llama 2, including moral luck in legal judgements and judgements of rule violations. [arXiv 2308.01264](https://arxiv.org/abs/2308.01264)
   - Kneer and Baumgartner (2026, *JITE* 182(1), "Debiasing Legal Judgment: Outcome Effects in Open-Source LLMs") report little to no outcome bias in current open-source models, unlike people and older models (unverified: full text not read). [Mohr Siebeck](https://www.mohrsiebeck.com/en/article/debiasing-legal-judgment-outcome-effects-in-open-source-llms-101628jite-2026-0017/)
3. **Catalogues of LLM-judge biases.** CoBBLEr (Koo et al., 2024) covers six biases and CALM ("Justice or Prejudice?", 2024) covers twelve, including position, verbosity, authority and self-enhancement. As far as we could see, neither includes outcome bias. [CoBBLEr](https://arxiv.org/html/2309.17012v2), [CALM](https://arxiv.org/pdf/2410.02736)
4. **Monitoring agents.**
   - SHADE-Arena (Kutasov et al., 2025) evaluates monitors on sabotage, without varying the outcome. [paper](https://assets.anthropic.com/m/4fb35becb0cd87e1/original/SHADE-Arena-Paper.pdf)
   - Za et al. (2026) find that agents' justifications can persuade monitors to approve policy violations, and that letting the monitor see the agent's chain of thought raised approval of harmful actions by 9.5% on average. This is the nearest neighbour to our "justified violation" extension. [arXiv 2607.08066](https://arxiv.org/abs/2607.08066)
   - "Gaming the Judge" (2026): editing only an agent's chain of thought pushes LLM judges towards calling the run a success. [arXiv 2601.14691](https://arxiv.org/pdf/2601.14691)
   - "trajectory-judge": judges that see only outcomes miss faults in the process. Our design keeps the process visible and varies only the outcome. [ResearchGate](https://www.researchgate.net/publication/413883513_trajectory-judge_What_Outcome-Only_LLM_Judges_Miss_on_Agent_Trajectories)

## What's new here

Outcome bias is one of the best-replicated findings in human judgement, and recent work has run classic outcome and moral-luck vignettes on chat models, with newer models showing little effect (Almeida et al., 2024; Kneer and Baumgartner, 2026). Lists of LLM-judge biases cover position, verbosity, authority and self-preference, but not outcome. Work on agent monitors has studied evasion and persuasion, not outcomes. This project tests outcome bias where it matters for oversight: an LLM auditor reviewing agent transcripts with tool calls against an explicit policy, where only the ending varies. Violations are labelled by construction, and a set of borderline cases measures whether the ending changes the verdict on an identical transcript, with no ground truth needed. Measures match how release gates use auditors: flag, severity, escalation and a violation probability.

Provisional, pending the second auditor model: so far, Sonnet 5.5 shows no bias in the expected direction. After failure it is slightly more lenient (−2.4 points on 100, 95% CI [−5.3, −0.4], 20 scenarios), which suggests frontier auditors may overcorrect for outcomes rather than excuse what worked.
