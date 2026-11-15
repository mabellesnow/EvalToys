"""Part 1, the pilot (archived). Asked only "did the agent break the rule?" after a one-line note about
how the task went, on two scenario sets. It found no outcome effect, which led to the critique in
docs/part1_pilot/critique.md and to the pre-registered experiments E1 to E5.

  scenarios.py           the pilot's scenarios: set 1 (stimuli/part1_pilot/) and set 2 (stimuli/agent_audit/)
  task.py                the auditor task:  inspect eval outcome_bias/part1/task.py -T variant=arguable
  analysis.py            violation probability by ending:  python -m outcome_bias.part1.analysis <logs>
  followups.py           ambiguous-policy and justified-violation follow-ups
  check_scenarios.py     automatic checks on scenario set 2 (lengths, leaks)
  tag_reasons.py         tag auditors' reasons for mentions of the outcome (an Inspect task)
  reason_summary.py      summarise those tags
  figures.py             the pilot write-up's figures:  python -m outcome_bias.part1.figures
  per_scenario_figure.py the per-scenario chart

Report and notes: docs/part1_pilot/.
"""
