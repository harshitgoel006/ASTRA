# ASTRA --- Project Progress and Learning Log

ASTRA is an AI-native software engineering platform. This README is the single progress tracker for the project.

It records:

- what has been built;
- what has been verified;
- which ASTRA and AI concepts have been explained;
- which project decisions have been approved;
- what is currently being implemented;
- what the next task is;
- which result can become a public LinkedIn milestone.

The long-term ASTRA vision remains broad. Implementation proceeds through small, measurable milestones.

## Current status

**Date:** 14 October 2026

**Current milestone:** M1 - Model Gateway

**Status:** M0 complete; M1 gateway v0 verified; provider integration remains

**Current result:** ASTRA has a verified deterministic permission layer and a
provider-independent model gateway contract. The JavaScript target repository
baseline remains a separate intentionally failing engineering task.

## Project structure

```text
ASTRA_Codex_Context_Pack/
├── astra-system/       # Python ASTRA control plane
├── test-repo/          # JavaScript/Node.js target repository
├── docs/               # Vision, architecture, research and milestones
├── CODEX.md            # Codex operating contract
└── README.md           # This progress and learning log
```

ASTRA and the target repository are separate systems:

- `astra-system/` is the system we are building.
- `test-repo/` is the external project ASTRA will inspect and modify.

This separation lets us test ASTRA as an engineering system instead of giving it special access to its own source code.

## Documentation map

- [Operating contract](CODEX.md)
- [Master context](docs/00-ASTRA-MASTER-CONTEXT.md)
- [Vision and philosophy](docs/01-VISION-AND-PHILOSOPHY.md)
- [13-layer architecture](docs/02-13-LAYER-ARCHITECTURE.md)
- [External feedback](docs/03-MANMEET-SIR-FEEDBACK.md)
- [Research status](docs/04-RESEARCH-STATUS.md)
- [Prototype roadmap](docs/05-PROTOTYPE-ROADMAP.md)
- [M0 foundation specification](docs/milestones/M0-FOUNDATION.md)
- [M1 model gateway specification](docs/milestones/M1-MODEL-GATEWAY.md)

## Approved M0 decisions

### M0 Step 1 - Prototype thesis

**Approved on 13 October 2026.**

> A controlled AI engineering system can inspect a small software repository, understand a bounded engineering task, create a reviewable plan, make a limited code change, run deterministic checks and produce evidence for its result.

In simple terms: ASTRA should safely fix one small software problem and prove what it did.

### M0 Step 2 - Separate systems

**Approved on 13 October 2026.**

- ASTRA control plane: Python.
- Target repository: JavaScript/Node.js, with a MERN-style structure where useful.
- The two systems remain in separate directories.

## Technology baseline

### ASTRA system

- Python 3.13.3 available locally.
- Python virtual environment: `astra-system/.venv/`.
- Command-line interface first.
- pytest for ASTRA tests.
- SQLite and JSONL for initial local state and logs.
- One model provider behind an adapter when M1 begins.

### Target repository

- JavaScript and Node.js.
- MERN-style repository structure where it helps produce a realistic engineering task.
- A bounded backend task will be used first.
- The first test task will be local and deterministic, without production data or secrets.

## Work completed

### Environment

- Python 3.13.3 verified.
- Node.js 22.15.1 verified.
- npm 11.5.2 verified through `npm.cmd`.
- Git 2.49.0 verified.
- GitHub remote configured for the ASTRA repository.

### Python environment

The local virtual environment contains pytest and its supporting packages:

- `pytest` - Python test runner.
- `pluggy` - pytest plugin system.
- `iniconfig` - configuration parsing support.
- `packaging` - package and version handling.
- `colorama` - Windows terminal color support.
- `Pygments` - readable syntax-highlighted output.

No AI-specific SDK or agent framework has been added yet. Dependencies will be introduced only when a milestone needs them.

### ASTRA foundation skeleton

```text
astra-system/
├── .gitignore
├── pyproject.toml
├── README.md
├── src/
│   └── astra/
│       ├── __init__.py
│       ├── __main__.py
│       └── control_plane.py
└── tests/
    └── test_control_plane.py
```

Current behavior:

```text
[ASTRA control plane] identity: ASTRA 0.1.0
[ASTRA control plane] status: foundation
[ASTRA control plane] target repository access: not connected yet
```

Verification result:

```text
1 passed
```

This `1 passed` belongs only to
`astra-system/tests/test_control_plane.py`. The test name is
`test_control_plane_reports_foundation_identity_only`; it confirms that the
Python package reports the expected ASTRA identity. It does not read or modify
`test-repo/`.

Use `-vv` to see the exact test name:

```powershell
.\astra-system\.venv\Scripts\python.exe -m pytest astra-system -vv
```

### JavaScript target repository baseline

The target repository now contains a small backend flow:

```text
Controller -> Service -> Repository -> Model -> Test
```

The seeded task is:

> After a task is completed, it must not appear in the pending-task list.

Baseline test evidence:

```text
1 test
0 passed
1 failed
```

Observed failure: the completed task remains in the pending list. This is an intentional baseline defect for ASTRA's first engineering task.

## Concepts covered so far

### Control plane

The control plane is ASTRA's central coordinator. Later it will coordinate:

```text
Goal -> Model -> Tools -> Permissions -> Observations -> Verification -> Evidence
```

### Target repository

The target repository is the software project that ASTRA will inspect and modify. It is separate from ASTRA's own source code.

### Virtual environment

`.venv` is an isolated Python environment. It keeps ASTRA's Python packages separate from the system Python installation.

### Python package

`src/astra/` is the importable ASTRA package. `__init__.py` identifies the package and stores its version.

### Entry point

`__main__.py` allows ASTRA to run with:

```powershell
python -m astra
```

### Dependency

A dependency is an external package used by ASTRA. pytest is currently the only development dependency.

### Deterministic foundation check

The current system identity is deterministic: it returns a predictable result without asking an AI model. Deterministic tools will be preferred whenever they can provide a reliable fact.

## How to verify the current ASTRA system

From the project root:

```powershell
.\astra-system\.venv\Scripts\python.exe -m pytest astra-system
```

Expected result:

```text
1 passed
```

To run the control-plane entry point:

```powershell
Set-Location astra-system
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m astra
```

Expected result:

```text
[ASTRA control plane] identity: ASTRA 0.1.0
[ASTRA control plane] status: foundation
[ASTRA control plane] target repository access: not connected yet
```

## Current task

### M0 Step 3 - JavaScript target repository baseline

**Status:** Complete on 13 October 2026.

The target repository has been defined and scaffolded. Its structure, baseline failure and reproducibility have been verified.

The target repository must have:

- a clear folder structure;
- a small backend flow;
- tests;
- an intentionally failing behavior;
- no production credentials;
- no external dependency required for the first test run;
- a task that can be completed within a controlled workspace.

The task will be designed so ASTRA can later:

```text
Inspect -> Identify relevant files -> Plan -> Request approval -> Modify -> Test -> Report evidence
```

Current evidence:

- `test-repo/server/controllers/taskController.js` exists.
- `test-repo/server/services/taskService.js` exists.
- `test-repo/server/repositories/taskRepository.js` exists.
- `test-repo/server/models/task.js` exists.
- `test-repo/test/taskController.test.js` reproduces the expected failure.

### M0 Step 4 - ASTRA permission boundary and success metrics

**Current task:** Define what the future ASTRA agent may read, write and execute, then define how its engineering result will be measured.

**Permission boundary:** Locked on 14 October 2026. ASTRA may inspect only
`test-repo/`, run the allowlisted test command `npm.cmd test` from that
directory with a 60-second timeout, and write only approved target files after
human approval. It may write run evidence only to `astra-system/runs/`.
Secrets, outside-workspace reads, arbitrary shell commands, dependency
installation, deletion, network access, commits, pushes, merges and deployment
are blocked in the prototype.

**M0 evaluation contract:** The first run must identify the relevant files,
produce an approved plan, modify only approved files, run `npm.cmd test`, record
the result and produce complete evidence. Prohibited actions, timeouts,
repeated actions and out-of-scope patches must be rejected and recorded.

**Evidence contract:** A run record connects the human goal, repository
observations, approval, actions, changed files, test result, final status and
limitations. A model response alone is not evidence.

### Permission Boundary v0 implementation

`astra-system/src/astra/permissions.py` now evaluates the locked M0 rules
without executing commands. Its tests cover target path reads, Git read
operations, the exact test command, approval-gated writes, evidence paths and
blocked actions.

Verification on 14 October 2026:

```text
10 passed in 0.05s
```

This validates the permission decision layer only. It does not yet execute
commands, inspect the target repository through ASTRA or modify target files.

### M0 completion

M0 was completed on 14 October 2026 after the thesis, target repository,
permission boundary, success metrics, threat responses and evidence format were
specified and reviewed. The completion evidence includes 10 passing ASTRA
permission and foundation tests.

### M1 Model Gateway v0

`astra-system/src/astra/model_gateway.py` now provides:

- `ModelRequest` for bounded model input;
- `ModelProvider` as the provider adapter contract;
- `ModelGateway` as the single validated model entry point;
- `ModelResponse` as the normalized response shape;
- `DeterministicProvider` for local tests without AI, network or cost.

M1 verification on 14 October 2026:

```text
15 passed in 0.08s
```

This validates the gateway contract and request validation. It does not call a
real AI provider yet. Provider selection, configuration, timeout behavior and
token/latency/cost logging remain in the next M1 slice.

The complete M1 specification is in
[M1-MODEL-GATEWAY.md](docs/milestones/M1-MODEL-GATEWAY.md). M1 is currently in
progress; the deterministic gateway contract is verified, while real provider
integration remains open.

The first public LinkedIn post is intentionally deferred until ASTRA completes a
stronger end-to-end engineering loop with inspectable evidence. The planned
first public demonstration is targeted at M7-M8:

```text
Human Goal -> Repository Understanding -> Plan -> Controlled Change -> Test -> Evidence Report
```

## Next ASTRA concepts

The next concepts will be explained inline while implementation continues:

1. Model gateway.
2. Provider adapter.
3. Structured model response.
4. Tool request and tool result.
5. Agent state.
6. Observation.
7. Permission boundary.
8. Evidence report.

No separate theory session is required. Each concept will be explained when it appears in the code.

## Milestone workflow

For every milestone:

1. Explain the concept and problem.
2. Define scope and non-goals.
3. Compare reasonable approaches.
4. Implement the approved scope.
5. Run tests and deterministic checks.
6. Record evidence and limitations.
7. Update this README and the relevant milestone document.
8. Prepare a LinkedIn-ready summary.

## LinkedIn milestone output

Each public update should include:

- the problem addressed;
- what ASTRA can now do;
- evidence or a short demo;
- test results;
- current limitations;
- the next milestone;
- a collaboration invitation when appropriate.

The first strong public engineering post will follow the first verified end-to-end loop, targeted at M7-M8:

```text
Human Goal -> Repository Understanding -> Plan -> Controlled Change -> Test -> Evidence Report
```

## Status labels

- **PROPOSED** - ASTRA design or hypothesis.
- **ESTABLISHED** - supported by existing technology or research.
- **VALIDATED** - demonstrated by an ASTRA experiment.
- **OPEN QUESTION** - unresolved.
- **DECISION** - explicitly approved project choice.
- **EXTERNAL FEEDBACK** - perspective from an outside person.
