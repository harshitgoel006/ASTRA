# ASTRA System

This directory will contain the ASTRA control plane.

## Planned responsibilities

- Model gateway
- Agent runtime and orchestration
- Tool permissions
- Repository inspection
- Test execution controls
- Logs and evidence reports

## Proposed baseline

- Python 3.12+
- Command-line interface first
- pytest for ASTRA tests
- SQLite and JSONL for initial local state

M0 foundation decisions are complete. M1 now implements a provider-independent
model gateway before a real provider is selected.

## Current foundation skeleton

The first control-plane package is intentionally small. It currently exposes a deterministic system identity so that the Python package and test workflow can be verified before AI models and tools are added.

Run the tests from the project root:

```powershell
.\astra-system\.venv\Scripts\python.exe -m pytest astra-system
```

To see the exact test name instead of only the summary count:

```powershell
.\astra-system\.venv\Scripts\python.exe -m pytest astra-system -vv
```

Run the control-plane entry point:

```powershell
Set-Location astra-system
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m astra
```

The current output is:

```text
[ASTRA control plane] identity: ASTRA 0.1.0
[ASTRA control plane] status: foundation
[ASTRA control plane] target repository access: not connected yet
```

This is a foundation check only. It verifies the Python control-plane identity;
it does not mean that ASTRA can use an AI model or modify a repository yet.

## Permission Boundary v0

`src/astra/permissions.py` contains the first deterministic permission policy.
It returns an allow or deny decision with a reason; it does not execute
commands or modify files.

The checks currently cover:

- reads inside the approved `test-repo/` target;
- read-only Git observations;
- the exact `npm.cmd test` command from the target root;
- writes that have both human approval and an approved file path;
- evidence writes inside `astra-system/runs/`;
- blocked actions such as install, network, deletion and push.

Verify the permission policy with:

```powershell
.\astra-system\.venv\Scripts\python.exe -m pytest astra-system -vv
```

Current result: `10 passed` on 14 October 2026.

## Model Gateway v0

`src/astra/model_gateway.py` defines the first controlled model boundary:

```text
ASTRA request -> ModelGateway -> ModelProvider adapter -> ModelResponse
```

`DeterministicProvider` is a local test adapter. It makes no network request
and represents no real AI capability. `OllamaProvider` is the local HTTP
adapter for the installed Ollama server. The current M1 tests verify request
validation, normalized responses, Ollama payload mapping, provider errors and
environment-backed gateway limits.

Full offline ASTRA verification currently reports `31 passed` on 14 October
2026. A live request through `ModelGateway(OllamaProvider())` also returned
`ASTRA gateway works` with token and timing metadata. Persistent model-call
evidence logging is implemented as `JsonlModelCallRecorder`; tests verify
success and error records without storing prompt content.

Gateway configuration is now environment-backed:

```text
ASTRA_MODEL=qwen3:4b
OLLAMA_BASE_URL=http://127.0.0.1:11434
ASTRA_MODEL_TIMEOUT_SECONDS=60
ASTRA_MAX_OUTPUT_TOKENS=512
```

The defaults work with the local Ollama setup. Invalid values and requests over
the configured output limit are rejected before the provider call.

The reusable runtime command is:

```powershell
Set-Location .\astra-system
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m astra model-call
```

It creates the configured local gateway, records prompt-free evidence and
prints the model response. The command requires Ollama to be running.

The complete milestone specification is available at:

```text
docs/milestones/M1-MODEL-GATEWAY.md
```
