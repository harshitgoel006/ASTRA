"""Reusable runtime wiring for ASTRA's local model call."""

from pathlib import Path

from .config import GatewaySettings
from .evidence import JsonlModelCallRecorder
from .model_gateway import (
    ModelGateway,
    ModelProvider,
    ModelRequest,
    ModelResponse,
    OllamaProvider,
)


DEFAULT_EVIDENCE_PATH = (
    Path(__file__).resolve().parents[3] / "astra-system" / "runs" / "model_calls.jsonl"
)
DEFAULT_SYSTEM_PROMPT = "You are an ASTRA local model test assistant."
DEFAULT_USER_PROMPT = "Reply with exactly: ASTRA runtime works"


def build_gateway(
    *,
    settings: GatewaySettings | None = None,
    evidence_path: Path | None = None,
    provider: ModelProvider | None = None,
) -> ModelGateway:
    """Build one configured gateway with prompt-free evidence recording."""

    active_settings = settings or GatewaySettings.from_environment()
    active_provider = provider or OllamaProvider(settings=active_settings)
    recorder = JsonlModelCallRecorder(evidence_path or DEFAULT_EVIDENCE_PATH)
    return ModelGateway(active_provider, recorder=recorder)


def run_model_call(
    user_prompt: str = DEFAULT_USER_PROMPT,
    *,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    max_output_tokens: int | None = None,
    settings: GatewaySettings | None = None,
    evidence_path: Path | None = None,
    provider: ModelProvider | None = None,
) -> ModelResponse:
    """Run one bounded model call through the configured ASTRA gateway."""

    active_settings = settings or GatewaySettings.from_environment()
    output_limit = (
        active_settings.max_output_tokens
        if max_output_tokens is None
        else max_output_tokens
    )
    gateway = build_gateway(
        settings=active_settings,
        evidence_path=evidence_path,
        provider=provider,
    )
    return gateway.complete(
        ModelRequest(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_output_tokens=output_limit,
        )
    )
