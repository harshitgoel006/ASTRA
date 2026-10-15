"""Evidence records for ASTRA model calls."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ModelCallRecord:
    """A prompt-free, machine-readable record of one model call."""

    run_id: str
    provider: str
    model: str
    status: str
    gateway_duration_ns: int
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_duration_ns: int | None = None
    load_duration_ns: int | None = None
    prompt_eval_duration_ns: int | None = None
    eval_duration_ns: int | None = None
    estimated_cost_usd: float | None = None
    cost_basis: str | None = None
    error: str | None = None


class ModelCallRecorder(Protocol):
    """Destination contract for model call evidence."""

    def record(self, record: ModelCallRecord) -> None:
        """Persist one model call record."""


class JsonlModelCallRecorder:
    """Append model call records as one JSON object per line."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def record(self, record: ModelCallRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as evidence_file:
            evidence_file.write(json.dumps(asdict(record), sort_keys=True))
            evidence_file.write("\n")
