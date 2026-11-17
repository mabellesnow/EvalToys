"""Analysis. One module per phase, plus the extra analyses.

  main_experiments  the pre-registered contrasts of E1 to E5    python -m outcome_bias.analysis.main_experiments e3
  labelled_scale    the labelled-scale follow-up, all models     python -m outcome_bias.analysis.labelled_scale
  follow_ups        follow-up parts A to D                       python -m outcome_bias.analysis.follow_ups

Extra analyses, exploratory, on the existing logs (docs/3_extra_analyses/results.md):
  mixed_models   mixed-effects models and standardised effect sizes
  moderators     which kinds of rule are most outcome-sensitive (codes: scenario_codes.yaml, in this folder)
  faithfulness   whether the models' reasons acknowledge the ending that moved them

Shared pieces: load.py (answers from logs), outcome_bias/stats.py (contrasts and intervals).
"""
