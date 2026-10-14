"""Environment-backed configuration for ASTRA's model gateway."""

import os
from dataclasses import dataclass
from typing import Mapping


class ConfigurationError(ValueError):
    """Raised when gateway configuration is missing or invalid."""


@dataclass(frozen=True)
class GatewaySettings:
    """Bounded settings used by the local model gateway."""

    model: str = "qwen3:4b"
    ollama_base_url: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 60.0
    max_output_tokens: int = 512

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] | None = None,
    ) -> "GatewaySettings":
        values = os.environ if environ is None else environ
        model = values.get("ASTRA_MODEL", cls.model).strip()
        base_url = values.get("OLLAMA_BASE_URL", cls.ollama_base_url).strip().rstrip("/")

        if not model:
            raise ConfigurationError("ASTRA_MODEL cannot be empty")
        if not base_url.startswith(("http://", "https://")):
            raise ConfigurationError("OLLAMA_BASE_URL must start with http:// or https://")

        timeout_seconds = cls._parse_float(
            values.get("ASTRA_MODEL_TIMEOUT_SECONDS", str(cls.timeout_seconds)),
            "ASTRA_MODEL_TIMEOUT_SECONDS",
        )
        max_output_tokens = cls._parse_int(
            values.get("ASTRA_MAX_OUTPUT_TOKENS", str(cls.max_output_tokens)),
            "ASTRA_MAX_OUTPUT_TOKENS",
        )

        if timeout_seconds <= 0:
            raise ConfigurationError("ASTRA_MODEL_TIMEOUT_SECONDS must be greater than zero")
        if max_output_tokens <= 0:
            raise ConfigurationError("ASTRA_MAX_OUTPUT_TOKENS must be greater than zero")

        return cls(
            model=model,
            ollama_base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )

    @staticmethod
    def _parse_float(value: str, name: str) -> float:
        try:
            return float(value)
        except ValueError as exc:
            raise ConfigurationError(f"{name} must be a number") from exc

    @staticmethod
    def _parse_int(value: str, name: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise ConfigurationError(f"{name} must be an integer") from exc
