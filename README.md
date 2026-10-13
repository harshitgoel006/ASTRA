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

**Date:** 13 October 2026

**Current milestone:** M0 - Foundation and Engineering Environment

**Status:** In progress

**Current result:** ASTRA's Python control-plane skeleton is working and its first test passes.

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
ASTRA 0.1.0 - foundation
```

Verification result:

```text
1 passed
```

This foundation check confirms that the Python package, test discovery and basic control-plane entry point work. It does not mean that ASTRA can use an AI model or modify a repository yet.

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
ASTRA 0.1.0 - foundation
```

## Current task

### M0 Step 3 - Define the JavaScript target repository

The next task is to define the small JavaScript/MERN-style project that ASTRA will inspect later.

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
