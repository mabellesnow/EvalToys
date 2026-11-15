"""Read answers from Inspect logs into plain rows, one per parsed answer.

Row fields: exp, model, reasoning, unit, version, cond, question, answer, detected (E4),
others (E4: other tickets listed), thought (whether the model used reasoning tokens).
Unparsed answers are counted and left out, as pre-registered.
"""

from functools import cache

from inspect_ai.log import read_eval_log

from outcome_bias import runlog


@cache
def _load_one(path: str):
    rows, bad = [], 0
    log = read_eval_log(path)
    model = log.eval.model.split("/")[-1]
    reasoning = log.eval.task_args.get("reasoning", "none")
    for s in log.samples or []:
        md = s.metadata
        sm = next(iter(s.scores.values())).metadata if s.scores else {}
        if not sm.get("parsed"):
            bad += 1
            continue
        rows.append(dict(exp=md["exp"], model=model, reasoning=reasoning, unit=md["unit"], version=md["version"],
                         cond=md["cond"], question=md["question"], answer=sm["answer"],
                         detected=sm.get("detected"), others=sm.get("others_listed"),
                         thought=(getattr(s.output.usage, "reasoning_tokens", 0) or 0) > 0))
    return tuple(rows), bad


def load(paths):
    """(rows, number unparsed) for the given log files, pooled."""
    rows, bad = [], 0
    for p in paths:
        r, b = _load_one(str(p))
        rows += r
        bad += b
    return rows, bad


def answers(label, exp, model=None, arm="main"):
    """Rows for one labelled run in the run index, or (None, 0) if it has not been run."""
    paths = runlog.logs(label=label, exp=exp, arm=arm, model=model)
    return load(paths) if paths else (None, 0)


def select(rows, question=None, version=None, model=None):
    return [r for r in rows
            if (question is None or r["question"] == question) and (version is None or r["version"] == version)
            and (model is None or model in r["model"])]
