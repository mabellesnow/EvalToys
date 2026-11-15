"""Automatic checks on the v2 scenarios. Run:  python -m outcome_bias.check_scenarios

Fails loudly on anything that broke a v1 run: duplicate ids, endings of unequal length,
versions of very different length, an ending that shares a distinctive word with only one
version of the transcript (a possible leak), or a version that differs from the other
outside its middle section.
"""

import re
import sys

from outcome_bias.part1.scenarios import V2_SCENARIOS

STOP = set("agent about after again agent's before being could every first other their there these those which while would should under until where still since".split())


def words(text):
    return {w for w in re.findall(r"[a-z][a-z'-]{4,}", text.lower()) if w not in STOP}


def main():
    problems = []
    ids = [s.id for s in V2_SCENARIOS]
    if len(ids) != len(set(ids)):
        problems.append("duplicate scenario ids")
    print(f"{'scenario':<26}{'steps b/c':>10}{'chars b/c':>12}{'endings s/f/n':>16}")
    for s in V2_SCENARIOS:
        v, c = s.steps_violation, s.steps_clean
        # shared prefix and suffix
        pre = 0
        while pre < min(len(v), len(c)) and v[pre] == c[pre]:
            pre += 1
        suf = 0
        while suf < min(len(v), len(c)) - pre and v[-1 - suf] == c[-1 - suf]:
            suf += 1
        only_v = " ".join(v[pre:len(v) - suf])
        only_c = " ".join(c[pre:len(c) - suf])
        if pre < 2 or suf < 1:
            problems.append(f"{s.id}: versions share only {pre} opening and {suf} closing steps")
        lv, lc = sum(map(len, v)), sum(map(len, c))
        if abs(lv - lc) / max(lv, lc) > 0.25:
            problems.append(f"{s.id}: version lengths differ by more than 25% ({lv} vs {lc})")
        if set(s.endings) != {"success", "failure", "none"}:
            problems.append(f"{s.id}: endings must be success, failure, none")
        lens = [len(s.endings[k]) for k in ("success", "failure", "none")]
        if max(lens) - min(lens) > 10:
            problems.append(f"{s.id}: ending lengths differ by {max(lens) - min(lens)} characters {lens}")
        for k, e in s.endings.items():
            if not e.startswith("FOLLOW-UP NOTE: "):
                problems.append(f"{s.id}: {k} ending lacks the FOLLOW-UP NOTE prefix")
            shared = words(" ".join(v[:pre] + v[len(v) - suf:]) + " " + s.task + " " + s.policy)
            leak_v = (words(e) & words(only_v)) - words(only_c) - shared
            leak_c = (words(e) & words(only_c)) - words(only_v) - shared
            if leak_v or leak_c:
                problems.append(f"{s.id}: {k} ending shares words with one version only: {sorted(leak_v | leak_c)}")
        for step in v + c:
            if not step.startswith(("TOOL CALL: ", "TOOL RESULT: ", "AGENT: ")):
                problems.append(f"{s.id}: step has no known prefix: {step[:40]}")
        print(f"{s.id:<26}{len(v):>5}/{len(c):<4}{lv:>6}/{lc:<5}{'/'.join(map(str, lens)):>16}")
    print(f"\n{len(V2_SCENARIOS)} scenarios checked.")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("No problems found.")


if __name__ == "__main__":
    main()
