#!/bin/zsh
# Run one pre-registered experiment and record the log files.
# Usage: [MODELS="haiku sonnet opus"] [BATCH=1] ./run_exp.sh <exp> <epochs> [main|medium|reasoning] [label]
#   main      = lowest reasoning each model allows (Haiku none, Sonnet none, Opus low)
#   medium    = reasoning effort "medium" on all three (E1's second arm)
#   reasoning = the lowest effort at which each model reasons on every answer
#               (Haiku high, Sonnet xhigh, Opus high)
#   MODELS    = which models to run (default: all three)
#   BATCH=1   = send requests through the batch API (half price, slower)
# Appends "<label> <exp> <arm> <model> <log file>" to logs/exp_runs.tsv, with the label
# "failed" or "partial" when the run did not finish.
cd "$(dirname "$0")"
exp=$1; epochs=$2; arm=${3:-main}; label=${4:-run1}
extra=(); [[ -n $BATCH ]] && extra=(--batch=1000)
for m in ${=MODELS:-haiku sonnet opus}; do
  if [[ $arm == medium ]]; then r=medium
  elif [[ $arm == reasoning ]]; then if [[ $m == sonnet ]]; then r=xhigh; else r=high; fi
  elif [[ $m == opus ]]; then r=low; else r=none; fi
  log=$(env -u ANTHROPIC_BASE_URL .venv/bin/inspect eval outcome_bias/experiments.py --model anthropic/claude-$m-5-5 \
        -T exp=$exp -T epochs=$epochs -T reasoning=$r $extra --display plain 2>&1 | grep -oE 'logs/[^ ]+\.eval' | tail -1)
  state=$(.venv/bin/python -c "
import sys
from inspect_ai.log import read_eval_log
l = read_eval_log(sys.argv[1]); n = sum(1 for s in (l.samples or []) if s.scores)
print(sys.argv[2] if l.status == 'success' else ('partial' if n > 50 else 'failed'))" "$log" "$label" 2>/dev/null)
  echo "${state:-failed}\t$exp\t$arm\t$m\t$log" | tee -a logs/exp_runs.tsv
  [[ ${state:-failed} == failed ]] && { echo "STOPPING: $m $exp $arm failed (see $log)"; exit 1; }
done
exit 0
