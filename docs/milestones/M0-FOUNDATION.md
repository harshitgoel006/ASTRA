# ASTRA M0 --- Foundation and Engineering Environment

**Status:** IN PROGRESS - Step 1 approved; remaining M0 decisions open

**Milestone purpose:** Define the first small, safe and measurable ASTRA prototype before implementation begins.

## 1. What M0 is

M0 is the foundation contract for ASTRA. It answers five questions:

1. ASTRA ka first prototype kis problem ko solve karega?
2. ASTRA kis repository aur technology stack par kaam karega?
3. ASTRA ko kaunse actions ki permission hogi?
4. ASTRA ko kaunse actions se rokna hoga?
5. Hum kaise prove karenge ki prototype ne sahi kaam kiya?

M0 ka output working agent nahi hai. M0 ka output ek approved, testable specification hai jiske basis par M1 se implementation start hogi.

## 2. First prototype thesis

**Proposed thesis:**

> A controlled AI engineering system can inspect a small software repository, understand a bounded engineering task, create a reviewable plan, make a limited code change, run deterministic checks and produce evidence for its result.

This is a hypothesis for ASTRA to test. It is not yet a validated claim.

**Decision record:** M0 Step 1 - Prototype thesis approved by the human developer on 13 October 2026.

## 3. Proposed first vertical slice

The first demonstrable task will follow this loop:

```text
Human Goal
  -> Repository Understanding
  -> Task Plan
  -> Human Review
  -> Controlled Code Change
  -> Test Run
  -> Observation
  -> Correction if needed
  -> Evidence Report
```

### Proposed task

Use a small local sample repository containing an intentionally failing test. ASTRA should:

1. Inspect the repository.
2. Identify the relevant files and test.
3. Explain the likely cause.
4. Produce a bounded plan.
5. Wait for approval before changing code.
6. Apply a limited patch inside the approved workspace.
7. Run the relevant test.
8. Report changed files, command output and final result.

The exact JavaScript sample repository and failure will be selected before M0 is approved.

## 4. Two separate technology choices

ASTRA itself and the repository that ASTRA operates on are separate systems.

### ASTRA control plane

The ASTRA control plane will be built with Python. It will contain the model gateway, agent runtime, tool permissions, orchestration, logs and evidence generation.

### Target sample repository

The first repository operated on by ASTRA will use JavaScript with Node.js. This repository is the test subject for ASTRA; it is not the ASTRA implementation itself.

Keeping these systems separate lets us verify that ASTRA can work on a repository through its tools instead of relying on special access to its own source code.

## 5. Proposed technology baseline

| Area | Proposed choice | Reason |
|---|---|---|
| Control plane | Python 3.12+ | Fast iteration and strong automation ecosystem |
| Initial interface | Command-line interface | Keeps the first system easy to inspect and test |
| ASTRA tests | pytest | Clear test discovery, assertions and fixtures |
| Repository operations | Git CLI and Python filesystem APIs | Deterministic repository facts |
| Initial storage | SQLite and JSONL | Simple local persistence and readable logs |
| Model access | One provider behind an adapter | Avoids early multi-provider complexity |
| Repository parsing | Add Tree-sitter when M4 begins | Structured source analysis after the basic loop exists |
| Isolation | Approved workspace, allowlisted commands and timeouts | First controlled execution boundary |
| Target repository | JavaScript with Node.js and npm test | Matches the human developer's current stack and tests ASTRA across a different codebase |

These are proposed prototype choices. They can be changed with a documented reason before implementation.

## 6. Initial scope

M0 will define:

- ASTRA's first prototype thesis.
- One sample repository.
- One technology stack.
- One bounded engineering task.
- One local execution boundary.
- Initial tool permissions.
- Initial success metrics.
- Initial threat model.
- Evidence report fields.
- Public demonstration plan.

## 7. Explicit non-goals

The first prototype will not attempt to build:

- A complete 13-layer ASTRA system.
- A multi-agent organization.
- Production deployment automation.
- Autonomous internet access.
- Access to real secrets or production credentials.
- Automatic merge or deployment.
- Predictive engineering.
- Digital twin simulation.
- A complete long-term memory fabric.
- A general-purpose coding product for every language.

## 8. Initial permission boundary

### Allowed in the proposed prototype

- Read files inside the approved sample repository.
- Inspect Git status, history and diff.
- Run explicitly allowed test commands.
- Write files only inside the approved workspace after approval.
- Create logs and evidence reports inside the ASTRA run directory.

### Prohibited in the proposed prototype

- Reading files outside the approved workspace.
- Reading environment secrets or credential stores.
- Deleting arbitrary files.
- Running unrestricted shell commands.
- Network access unless a later milestone explicitly enables it.
- Changing production systems.
- Deploying or merging changes automatically.
- Continuing after the iteration, time or cost budget is exhausted.

## 9. Proposed success metrics

M0 will define the measurement method for the following metrics:

1. **Repository understanding:** Can ASTRA identify relevant files and tests, with source references?
2. **Plan quality:** Can a human review the plan before execution?
3. **Change boundary:** Did ASTRA modify only approved files?
4. **Test result:** Did the relevant test run, and what did it report?
5. **Evidence completeness:** Are the claim, diff, command and result connected?
6. **Safety behavior:** Were prohibited actions blocked?
7. **Reproducibility:** Can the same task be rerun and inspected?
8. **Resource use:** Were iterations, tokens, time and cost within budget?

M0 will not claim a success percentage until the first evaluation procedure is defined.

## 10. Initial threat model questions

M0 must answer these questions before tool execution is implemented:

- What happens if the model requests a prohibited command?
- What happens if repository content contains malicious instructions?
- What happens if a test command hangs?
- What happens if the agent repeatedly retries the same action?
- What happens if a patch changes files outside the approved scope?
- What happens if the model reports success but the test fails?
- What happens if a task needs a permission that was not granted?
- How can the human stop execution immediately?

The threat model will be small and prototype-focused. It will expand in M2 and M9.

## 11. Research required for M0

M0 research should be targeted rather than broad:

- LLM and agent terminology needed for the prototype.
- Tool calling and structured model output.
- Repository-level software engineering workflow.
- Test-based verification.
- Process boundaries and least privilege.
- Prompt and repository instruction injection.
- Basic cost and token budgeting.

For each topic, the workflow is:

```text
Learn the concept -> Run a small experiment -> Record the decision -> Continue
```

## 12. M0 deliverables

- This specification, updated after discussion.
- Selected sample repository and stack.
- Selected bounded engineering task.
- Initial permission matrix.
- Initial threat model.
- Evaluation checklist.
- Evidence report outline.
- Public milestone post outline.

## 13. Completion gate

M0 is complete when the human developer approves:

- the first prototype thesis;
- the sample repository;
- the technology baseline;
- the bounded task;
- the permission boundary;
- the success metrics;
- the threat model questions;
- the evidence format;
- the public demonstration plan.

Only after this gate should ASTRA implementation begin.

## 14. Open decisions

These decisions remain open until reviewed together:

- Which sample repository will be used?
- Will the first task be a failing-test fix or a small feature?
- Which model provider will be used for M1?
- Should the first tool boundary use a local workspace only or add Docker immediately?
- What exact budget should apply to one task run?
