"""Provider-independent model access for ASTRA's first gateway milestone.

The gateway validates requests and exposes one common response shape. Provider
adapters hide provider-specific API details behind the ``ModelProvider``
protocol. The first real adapter targets a local Ollama server.
"""

import json
import time
from uuid import uuid4
from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import GatewaySettings
from .evidence import ModelCallRecord, ModelCallRecorder


_OLLAMA_THINKING_PREFILL = "<think>\n\n</think>\n\n"


class ModelGatewayError(ValueError):
    """Raised when a model request is invalid for the gateway."""


@dataclass(frozen=True)
class ModelRequest:
    """A bounded request sent from ASTRA to a model provider."""

    system_prompt: str
    user_prompt: str
    max_output_tokens: int = 512


@dataclass(frozen=True)
class ModelUsage:
    """Usage, timing and direct provider-cost metadata."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_duration_ns: int | None = None
    load_duration_ns: int | None = None
    prompt_eval_duration_ns: int | None = None
    eval_duration_ns: int | None = None
    estimated_cost_usd: float | None = None
    cost_basis: str | None = None


@dataclass(frozen=True)
class ModelResponse:
    """The provider-independent response returned by the gateway."""

    provider: str
    model: str
    content: str
    finish_reason: str = "stop"
    usage: ModelUsage = field(default_factory=ModelUsage)


class ModelProvider(Protocol):
    """Contract that a real provider adapter must implement."""

    name: str
    model: str

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Generate a response for a validated request."""


class ModelGateway:
    """The single controlled entry point for model requests."""

    def __init__(
        self,
        provider: ModelProvider,
        recorder: ModelCallRecorder | None = None,
    ) -> None:
        self.provider = provider
        self.recorder = recorder

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Validate a request and forward it through the provider adapter."""

        run_id = f"model-call-{uuid4().hex}"
        started_at = time.perf_counter_ns()

        try:
            self._validate(request)
            response = self.provider.complete(request)

            if not response.content.strip():
                raise ModelGatewayError("provider returned an empty response")
        except Exception as exc:
            self._record_error(run_id, started_at, exc)
            if isinstance(exc, ModelGatewayError):
                raise
            raise ModelGatewayError(f"provider call failed: {exc}") from exc

        self._record_success(run_id, started_at, response)

        return response

    def _record_success(
        self,
        run_id: str,
        started_at: int,
        response: ModelResponse,
    ) -> None:
        if self.recorder is None:
            return

        usage = response.usage
        self.recorder.record(
            ModelCallRecord(
                run_id=run_id,
                provider=response.provider,
                model=response.model,
                status="success",
                gateway_duration_ns=time.perf_counter_ns() - started_at,
                finish_reason=response.finish_reason,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_duration_ns=usage.total_duration_ns,
                load_duration_ns=usage.load_duration_ns,
                prompt_eval_duration_ns=usage.prompt_eval_duration_ns,
                eval_duration_ns=usage.eval_duration_ns,
                estimated_cost_usd=usage.estimated_cost_usd,
                cost_basis=usage.cost_basis,
            )
        )

    def _record_error(self, run_id: str, started_at: int, error: Exception) -> None:
        if self.recorder is None:
            return

        self.recorder.record(
            ModelCallRecord(
                run_id=run_id,
                provider=getattr(self.provider, "name", "unknown"),
                model=getattr(self.provider, "model", "unknown"),
                status="error",
                gateway_duration_ns=time.perf_counter_ns() - started_at,
                error=f"{type(error).__name__}: {error}",
            )
        )

    @staticmethod
    def _validate(request: ModelRequest) -> None:
        if not request.system_prompt.strip():
            raise ModelGatewayError("system_prompt cannot be empty")

        if not request.user_prompt.strip():
            raise ModelGatewayError("user_prompt cannot be empty")

        if request.max_output_tokens <= 0:
            raise ModelGatewayError("max_output_tokens must be greater than zero")


class DeterministicProvider:
    """A local provider used to test the gateway without AI or network access."""

    name = "deterministic"
    model = "fixture-v0"

    def complete(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            provider=self.name,
            model=self.model,
            content=f"Deterministic response for: {request.user_prompt}",
            usage=ModelUsage(
                estimated_cost_usd=0.0,
                cost_basis="deterministic_fixture",
            ),
        )


class OllamaProvider:
    """Adapter for Ollama's local ``/api/chat`` endpoint."""

    name = "ollama"

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float | None = None,
        settings: GatewaySettings | None = None,
    ) -> None:
        gateway_settings = settings or GatewaySettings.from_environment()
        self.model = model or gateway_settings.model
        self.base_url = (base_url or gateway_settings.ollama_base_url).rstrip("/")
        self.timeout_seconds = (
            gateway_settings.timeout_seconds
            if timeout_seconds is None
            else timeout_seconds
        )
        self.max_output_tokens = gateway_settings.max_output_tokens

        if self.timeout_seconds <= 0:
            raise ModelGatewayError("timeout_seconds must be greater than zero")

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Send a bounded request to the local Ollama server."""

        if request.max_output_tokens > self.max_output_tokens:
            raise ModelGatewayError(
                "request max_output_tokens exceeds the configured gateway limit"
            )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
                {"role": "assistant", "content": _OLLAMA_THINKING_PREFILL},
                {"role": "user", "content": request.user_prompt},
            ],
            "stream": False,
            "options": {"num_predict": request.max_output_tokens},
        }
        http_request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(http_request, timeout=self.timeout_seconds) as response:
                raw_body = response.read()
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ModelGatewayError(
                f"Ollama request failed with HTTP {exc.code}: {detail}"
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise ModelGatewayError(f"Ollama connection failed: {exc}") from exc

        try:
            result: dict[str, Any] = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelGatewayError("Ollama returned invalid JSON") from exc

        message = result.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise ModelGatewayError("Ollama response did not contain message.content")

        return ModelResponse(
            provider=self.name,
            model=str(result.get("model", self.model)),
            content=message["content"],
            finish_reason=str(result.get("done_reason", "stop")),
            usage=ModelUsage(
                prompt_tokens=_optional_int(result, "prompt_eval_count"),
                completion_tokens=_optional_int(result, "eval_count"),
                total_duration_ns=_optional_int(result, "total_duration"),
                load_duration_ns=_optional_int(result, "load_duration"),
                prompt_eval_duration_ns=_optional_int(
                    result, "prompt_eval_duration"
                ),
                eval_duration_ns=_optional_int(result, "eval_duration"),
                estimated_cost_usd=0.0,
                cost_basis="local_ollama_no_provider_charge",
            ),
        )


def _optional_int(payload: dict[str, Any], key: str) -> int | None:
    value = payload.get(key)
    return value if isinstance(value, int) else None
