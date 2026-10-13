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

Implementation begins after the M0 foundation decisions are approved.

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
