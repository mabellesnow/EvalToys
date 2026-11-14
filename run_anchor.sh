#!/bin/zsh
# Exploratory follow-up X1 (notes/prereg_e1_e5.md): E3's violation question with a labelled scale.
# Usage: [MODELS="haiku sonnet opus"] [BATCH=1] ./run_anchor.sh <labelled|ignore>
# Main-arm settings: Haiku and Sonnet without reasoning, Opus at "low".
# Appends "x1-<arm> e3 main <model> <log file>" to logs/exp_runs.tsv ("failed"/"partial" if it did not finish).
cd "$(dirname "$0")"
arm=$1
extra=(); [[ -n $BATCH ]] && extra=(--batch=1000)
for m in ${=MODELS:-haiku sonnet opus}; do
  if [[ $m == opus ]]; then r=low; else r=none; fi
  log=$(env -u ANTHROPIC_BASE_URL .venv/bin/inspect eval outcome_bias/exp_anchor.py --model anthropic/claude-$m-5-5 \
        -T arm=$arm -T epochs=3 -T reasoning=$r $extra --display plain 2>&1 | grep -oE 'logs/[^ ]+\.eval' | tail -1)
  state=$(.venv/bin/python -c "
import sys
from inspect_ai.log import read_eval_log
l = read_eval_log(sys.argv[1]); n = sum(1 for s in (l.samples or []) if s.scores)
print(sys.argv[2] if l.status == 'success' else ('partial' if n > 50 else 'failed'))" "$log" "x1-$arm" 2>/dev/null)
  echo "${state:-failed}\te3\tmain\t$m\t$log" | tee -a logs/exp_runs.tsv
  [[ ${state:-failed} == failed ]] && { echo "STOPPING: $m x1-$arm failed (see $log)"; exit 1; }
done
exit 0
