import json

import pytest

import astra.model_gateway as model_gateway

from astra.model_gateway import (
    DeterministicProvider,
    ModelGateway,
    ModelGatewayError,
    ModelRequest,
    OllamaProvider,
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


class FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeHTTPResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def test_ollama_provider_normalizes_local_api_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = OllamaProvider(model="qwen3:4b", base_url="http://localhost:11434")
    ollama_payload = {
        "model": "qwen3:4b",
        "message": {"role": "assistant", "content": "ASTRA API works"},
        "done": True,
        "done_reason": "stop",
        "total_duration": 100,
        "prompt_eval_count": 18,
        "eval_count": 33,
    }

    def fake_urlopen(request: object, timeout: float) -> FakeHTTPResponse:
        assert timeout == 60.0
        assert getattr(request, "full_url") == "http://localhost:11434/api/chat"
        body = json.loads(getattr(request, "data").decode("utf-8"))
        assert body["model"] == "qwen3:4b"
        assert body["stream"] is False
        assert body["options"]["num_predict"] == 512
        return FakeHTTPResponse(ollama_payload)

    monkeypatch.setattr(model_gateway, "urlopen", fake_urlopen)

    response = provider.complete(make_request())

    assert response.provider == "ollama"
    assert response.model == "qwen3:4b"
    assert response.content == "ASTRA API works"
    assert response.usage.prompt_tokens == 18
    assert response.usage.completion_tokens == 33


def test_ollama_provider_converts_connection_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = OllamaProvider()

    def failed_urlopen(request: object, timeout: float) -> None:
        raise OSError("server is offline")

    monkeypatch.setattr(model_gateway, "urlopen", failed_urlopen)

    with pytest.raises(ModelGatewayError, match="connection failed"):
        provider.complete(make_request())


def test_ollama_provider_rejects_a_malformed_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = OllamaProvider()

    monkeypatch.setattr(
        model_gateway,
        "urlopen",
        lambda request, timeout: FakeHTTPResponse({"done": True}),
    )

    with pytest.raises(ModelGatewayError, match="message.content"):
        provider.complete(make_request())
