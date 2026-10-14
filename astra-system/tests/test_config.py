import pytest

from astra.config import ConfigurationError, GatewaySettings


def test_gateway_settings_have_safe_local_defaults() -> None:
    settings = GatewaySettings.from_environment({})

    assert settings.model == "qwen3:4b"
    assert settings.ollama_base_url == "http://127.0.0.1:11434"
    assert settings.timeout_seconds == 60.0
    assert settings.max_output_tokens == 512


def test_gateway_settings_read_environment_overrides() -> None:
    settings = GatewaySettings.from_environment(
        {
            "ASTRA_MODEL": "qwen3:8b",
            "OLLAMA_BASE_URL": "http://localhost:11434/",
            "ASTRA_MODEL_TIMEOUT_SECONDS": "15.5",
            "ASTRA_MAX_OUTPUT_TOKENS": "256",
        }
    )

    assert settings.model == "qwen3:8b"
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.timeout_seconds == 15.5
    assert settings.max_output_tokens == 256


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("ASTRA_MODEL", "", "ASTRA_MODEL"),
        ("OLLAMA_BASE_URL", "localhost:11434", "OLLAMA_BASE_URL"),
        ("ASTRA_MODEL_TIMEOUT_SECONDS", "zero", "must be a number"),
        ("ASTRA_MAX_OUTPUT_TOKENS", "zero", "must be an integer"),
        ("ASTRA_MODEL_TIMEOUT_SECONDS", "0", "greater than zero"),
        ("ASTRA_MAX_OUTPUT_TOKENS", "0", "greater than zero"),
    ],
)
def test_invalid_gateway_settings_are_rejected(
    key: str,
    value: str,
    message: str,
) -> None:
    with pytest.raises(ConfigurationError, match=message):
        GatewaySettings.from_environment({key: value})
