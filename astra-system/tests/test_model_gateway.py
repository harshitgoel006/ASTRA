import pytest

from astra.model_gateway import (
    DeterministicProvider,
    ModelGateway,
    ModelGatewayError,
    ModelRequest,
)


def make_request() -> ModelRequest:
    return ModelRequest(
        system_prompt="You are an ASTRA planning assistant.",
        user_prompt="Explain the first bounded engineering task.",
    )


def test_gateway_returns_a_normalized_provider_response() -> None:
    gateway = ModelGateway(DeterministicProvider())

    response = gateway.complete(make_request())

    assert response.provider == "deterministic"
    assert response.model == "fixture-v0"
    assert response.content == (
        "Deterministic response for: Explain the first bounded engineering task."
    )
    assert response.finish_reason == "stop"


def test_gateway_rejects_an_empty_system_prompt() -> None:
    gateway = ModelGateway(DeterministicProvider())
    request = ModelRequest(system_prompt=" ", user_prompt="valid request")

    with pytest.raises(ModelGatewayError, match="system_prompt"):
        gateway.complete(request)


def test_gateway_rejects_an_empty_user_prompt() -> None:
    gateway = ModelGateway(DeterministicProvider())
    request = ModelRequest(system_prompt="valid system", user_prompt=" ")

    with pytest.raises(ModelGatewayError, match="user_prompt"):
        gateway.complete(request)


def test_gateway_rejects_a_non_positive_output_limit() -> None:
    gateway = ModelGateway(DeterministicProvider())
    request = ModelRequest(
        system_prompt="valid system",
        user_prompt="valid request",
        max_output_tokens=0,
    )

    with pytest.raises(ModelGatewayError, match="max_output_tokens"):
        gateway.complete(request)


def test_gateway_rejects_an_empty_provider_response() -> None:
    class EmptyProvider(DeterministicProvider):
        def complete(self, request: ModelRequest):
            response = super().complete(request)
            return response.__class__(
                provider=response.provider,
                model=response.model,
                content=" ",
            )

    gateway = ModelGateway(EmptyProvider())

    with pytest.raises(ModelGatewayError, match="empty response"):
        gateway.complete(make_request())
