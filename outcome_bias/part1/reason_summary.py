"""Summarise a tag_reasons log: how often auditors' reasons mention the outcome, and how.

Run:  python -m outcome_bias.reason_summary              (latest tag_reasons log in ./logs)
      python -m outcome_bias.reason_summary tags.eval    (a specific one)
"""

import sys
from collections import Counter, defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

from outcome_bias.paths import LOGS

OUTCOMES = ("success", "none", "failure", "omitted")
ROLES = ("discounted", "mitigating", "aggravating", "neutral")


def latest_tag_log(log_dir=LOGS):
    logs = sorted(Path(log_dir).glob("*tag-reasons*.eval"), key=lambda p: p.stat().st_mtime)
    if not logs:
        sys.exit(f"No tag_reasons logs in {log_dir}/: run `inspect eval outcome_bias/tag_reasons.py` first")
    return logs[-1]


def avg(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else latest_tag_log()
    log = read_eval_log(str(path))
    print(f"Tag log: {path.name}   tagger: {log.eval.model}\n")

    cells = defaultdict(Counter)  # (auditor, outcome) -> role counts
    probs = defaultdict(list)  # (auditor, outcome, role) -> auditor probabilities
    examples = defaultdict(list)  # (outcome, role) -> quotes
    unparsed = 0
    for s in log.samples or []:
        m = s.metadata
        meta = next(iter(s.scores.values())).metadata if s.scores else {}
        if not meta.get("parsed"):
            unparsed += 1
            continue
        role = meta["role"]
        cells[(m["auditor"], m["outcome"])][role] += 1
        if isinstance(m.get("probability"), (int, float)):
            probs[(m["auditor"], m["outcome"], role)].append(m["probability"])
        quote = next(iter(s.scores.values())).explanation
        if role != "none" and quote and len(examples[(m["outcome"], role)]) < 2:
            examples[(m["outcome"], role)].append(f"{m['auditor']}, {m['scenario']}: \"{quote}\"")

    auditors = sorted({k[0] for k in cells}, key=lambda a: (["haiku", "sonnet", "opus"].index(next((x for x in ("haiku", "sonnet", "opus") if x in a), "opus")), a))
    print("Share of borderline reasons that mention the outcome, and how they use it")
    print(f"{'auditor':<20}{'outcome':<9}{'n':>5}{'mention':>9}" + "".join(f"{r:>12}" for r in ROLES))
    for a in auditors:
        for o in OUTCOMES:
            c = cells[(a, o)]
            n = sum(c.values())
            if not n:
                continue
            mention = 1 - c["none"] / n
            print(f"{a:<20}{o:<9}{n:>5}{mention:>9.0%}" + "".join(f"{c[r] / n:>12.0%}" for r in ROLES))
        print()

    print("Mean violation probability by how the reason uses the outcome (success and failure endings)")
    print(f"{'auditor':<20}{'outcome':<9}" + "".join(f"{r:>14}" for r in ("none",) + ROLES))
    for a in auditors:
        for o in ("success", "failure"):
            row = ""
            for r in ("none",) + ROLES:
                xs = probs[(a, o, r)]
                row += f"{avg(xs):>9.1f} ({len(xs):>2})" if xs else f"{'-':>14}"
            print(f"{a:<20}{o:<9}{row}")
    print("(n in brackets; compare within a row, and only where n is not tiny)")

    print("\nExample quotes")
    for (o, r), qs in sorted(examples.items()):
        for q in qs:
            print(f"  [{o}, {r}] {q}")

    if unparsed:
        print(f"\n{unparsed} tags unparsed; see `inspect view`.")


if __name__ == "__main__":
    main()
