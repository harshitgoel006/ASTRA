"""Provider-independent model access for ASTRA's first gateway milestone.

The gateway validates requests and exposes one common response shape. Provider
adapters hide provider-specific API details behind the ``ModelProvider``
protocol. The first real adapter targets a local Ollama server.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


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
    """Provider usage and timing metadata when the provider supplies it."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_duration_ns: int | None = None
    load_duration_ns: int | None = None
    prompt_eval_duration_ns: int | None = None
    eval_duration_ns: int | None = None


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

    def __init__(self, provider: ModelProvider) -> None:
        self.provider = provider

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Validate a request and forward it through the provider adapter."""

        self._validate(request)
        response = self.provider.complete(request)

        if not response.content.strip():
            raise ModelGatewayError("provider returned an empty response")

        return response

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
        )


class OllamaProvider:
    """Adapter for Ollama's local ``/api/chat`` endpoint."""

    name = "ollama"

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.model = model or os.getenv("ASTRA_MODEL", "qwen3:4b")
        self.base_url = (
            base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        ).rstrip("/")
        self.timeout_seconds = timeout_seconds

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Send a bounded request to the local Ollama server."""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
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
            ),
        )


def _optional_int(payload: dict[str, Any], key: str) -> int | None:
    value = payload.get(key)
    return value if isinstance(value, int) else None
