"""The models, and the reasoning setting each uses in each arm.

  main       the lowest reasoning the model allows (thinking off where possible)
  medium     effort "medium" for all (E1's second arm; Sonnet did not reason at this setting)
  reasoning  the lowest effort at which the model reasons on every answer (E2, E3 second arm)

Opus 5.5 cannot switch reasoning off, so its main arm is effort "low".
OpenAI entries are set up but not yet run: gpt-6-astra and gpt-6.1-sol always reason (Inspect drops
temperature for them), so their main arm is "low"; check with a one-call run before a full run.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    provider_id: str
    arms: dict
    batch_price: tuple[float, float]  # USD per million input, output tokens, batch API
    tested: bool = True


MODELS = {
    "haiku": Model("anthropic/claude-haiku-5-5", {"main": "none", "medium": "medium", "reasoning": "high"}, (0.05, 0.25)),
    "sonnet": Model("anthropic/claude-sonnet-5-5", {"main": "none", "medium": "medium", "reasoning": "xhigh"}, (1.0, 5.0)),
    "opus": Model("anthropic/claude-opus-5-5", {"main": "low", "medium": "medium", "reasoning": "high"}, (2.0, 10.0)),
    # OpenAI, not yet run
    "gpt-6-luna": Model("openai/gpt-6-luna", {"main": "none", "reasoning": "high"}, (0.05, 0.25), tested=False),
    "gpt-6.1-terra": Model("openai/gpt-6.1-terra", {"main": "none", "reasoning": "high"}, (0.50, 2.50), tested=False),
    "gpt-6.1-sol": Model("openai/gpt-6.1-sol", {"main": "low", "reasoning": "high"}, (1.00, 5.00), tested=False),
    "gpt-6-astra": Model("openai/gpt-6-astra", {"main": "low", "reasoning": "high"}, (5.00, 25.00), tested=False),
}

CLAUDE = ("haiku", "sonnet", "opus")
