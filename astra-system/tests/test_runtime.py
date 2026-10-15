import json

from astra.config import GatewaySettings
from astra.model_gateway import DeterministicProvider
from astra.runtime import run_model_call


def test_runtime_connects_provider_gateway_and_evidence_recorder(tmp_path):
    evidence_path = tmp_path / "runs" / "model_calls.jsonl"

    response = run_model_call(
        "Inspect the bounded runtime path",
        settings=GatewaySettings(max_output_tokens=64),
        evidence_path=evidence_path,
        provider=DeterministicProvider(),
    )

    assert response.content == "Deterministic response for: Inspect the bounded runtime path"
    record = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert record["provider"] == "deterministic"
    assert record["model"] == "fixture-v0"
    assert record["status"] == "success"
    assert record["estimated_cost_usd"] == 0.0
    assert record["cost_basis"] == "deterministic_fixture"
    assert "Inspect the bounded runtime path" not in json.dumps(record)

