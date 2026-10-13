"""Provider-independent model access for ASTRA's first gateway milestone.

The gateway validates requests and exposes one common response shape. A provider
adapter hides provider-specific API details behind the ``ModelProvider``
protocol. This module does not call a real model provider yet.
"""

from dataclasses import dataclass
from typing import Protocol


class ModelGatewayError(ValueError):
    """Raised when a model request is invalid for the gateway."""


@dataclass(frozen=True)
class ModelRequest:
    """A bounded request sent from ASTRA to a model provider."""

    system_prompt: str
    user_prompt: str
    max_output_tokens: int = 512


@dataclass(frozen=True)
class ModelResponse:
    """The provider-independent response returned by the gateway."""

    provider: str
    model: str
    content: str
    finish_reason: str = "stop"


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
