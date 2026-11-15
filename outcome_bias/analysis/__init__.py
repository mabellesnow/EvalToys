"""Analysis. One module per plan:

  e1_e5    the pre-registered contrasts of E1 to E5        python -m outcome_bias.analysis.e1_e5 e3
  stage2   stage 2 parts A to D (and B through x1)          python -m outcome_bias.analysis.stage2
  x1       the labelled-scale test, all arms and models     python -m outcome_bias.analysis.x1

Shared pieces: load.py (answers from logs), outcome_bias/stats.py (contrasts and intervals).
"""
