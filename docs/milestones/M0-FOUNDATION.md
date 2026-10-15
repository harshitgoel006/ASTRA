# ASTRA M0 --- Foundation and Engineering Environment

**Status:** COMPLETE - Specification approved and Permission Boundary v0 verified on 14 October 2026

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

### Project structure

```text
ASTRA_Codex_Context_Pack/
├── astra-system/       # Python ASTRA control plane
├── test-repo/          # JavaScript/Node.js target repository
├── docs/               # Vision, architecture, milestones and evidence formats
└── CODEX.md            # Operating contract for implementation work
```

The two implementation areas will have separate responsibilities and separate tests. The working target location is `test-repo/`.

**Decision record:** M0 Step 2 - Separate the Python ASTRA system from the JavaScript target repository. Approved by the human developer on 13 October 2026.

**Progress record:** M0 Step 3 target baseline created on 13 October 2026. The seeded test produces one expected failure and is ready to become ASTRA's first bounded engineering task.

**Progress record:** M0 Step 3 baseline verified on 13 October 2026. The target test reports one expected failure because the completed task remains in the pending list.

**Progress record:** Permission Boundary v0 implemented and verified on 14
October 2026. The ASTRA test suite reports 10 passed tests covering the
control-plane identity, target path reads, Git observations, the allowlisted
test command, approval-gated writes, evidence paths and blocked actions.

**Completion record:** The M0 completion gate was accepted on 14 October 2026.
The thesis, separate systems, target task, permission boundary, evaluation
criteria, threat responses and evidence format are now the approved foundation
for M1 implementation.

**Progress record:** On 14 October 2026, the developer chose to delay the first
public LinkedIn post until ASTRA demonstrates a stronger end-to-end result. The
planned public demonstration is the first verified loop from repository
understanding through evidence, targeted at M7-M8.

**Updated public communication decision:** On 16 October 2026, the developer
approved a smaller M0 + M1 progress post after review of the verified evidence.
The M7-M8 end-to-end engineering loop remains the planned flagship public
demonstration.

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

The permission boundary is ASTRA's authority contract. It defines which
actions a future agent may request and which actions the control plane must
reject before execution.

### Locked prototype permission matrix

| Capability | Initial decision | Condition |
|---|---|---|
| Read target files | Allow | Only inside `test-repo/` |
| Read Git status | Allow | `git status --short`, only for the target repository |
| Read Git history and diff | Allow | Read-only Git inspection for the target repository |
| Run tests | Allow | Only `npm.cmd test` from the `test-repo/` directory, with a 60-second timeout |
| Write target files | Allow after approval | Only files included in the approved plan |
| Write run evidence | Allow | Only inside `astra-system/runs/` |
| Read outside the workspace | Deny | No home directory, credential store or unrelated project access |
| Read secrets | Deny | No environment secrets, tokens or private keys |
| Arbitrary shell commands | Deny | Only the commands listed in this matrix are allowed |
| Delete files | Deny initially | Requires a later, separately approved capability |
| Network access | Deny initially | Not needed for the first local vertical slice |
| Install dependencies | Deny initially | Prevents unapproved network and lockfile changes |
| Commit, push, merge or deploy | Deny | Outside the prototype scope |

**Decision record:** The developer approved and locked this prototype permission
boundary on 14 October 2026. The boundary applies to ASTRA's operations on the
target repository. The control plane can still read and write its own source,
tests and run evidence according to the project workflow.

### Boundary summary

The locked prototype allows only the capabilities listed in the matrix above.

The locked prototype denies:

- Reading files outside `test-repo/`.
- Reading environment secrets or credential stores.
- Deleting files, installing dependencies or using network access.
- Running commands outside the explicit allowlist.
- Committing, pushing, merging, deploying or changing production systems.
- Continuing after the timeout or retry budget is exhausted.

## 9. Initial success metrics

The following criteria are the initial evaluation contract for the first
vertical slice. They measure observable behavior; they do not measure whether
the model sounds intelligent.

| Metric | Pass condition for the first slice |
|---|---|
| Repository understanding | The relevant test and the four source files in the target flow are identified with paths and a reason for each. |
| Plan quality | The plan states the suspected cause, proposed file change, verification command and scope. A human can approve it before writing. |
| Change boundary | The final diff contains only files approved in the plan. Any out-of-scope path causes the run to stop. |
| Test result | `npm.cmd test` runs from `test-repo/`, finishes within 60 seconds and exits with code `0` after the fix. |
| Evidence completeness | The run records the goal, observations, approval, changed files, command, exit code, result and limitation. |
| Safety behavior | A prohibited action is rejected before execution and recorded as a denied action. |
| Reproducibility | A second run against the same repository state produces the same test result and an explainable diff. |
| Resource use | The run stays within the configured command timeout and retry limit. Model token and monetary budgets will be set when M1 begins. |

For the first vertical slice, all rows must pass. A partial result is reported
as failed or incomplete; it cannot be reported as a successful engineering
change merely because the model produced a plausible explanation.

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

### M0 threat responses

| Situation | Required prototype response |
|---|---|
| Model requests a prohibited command | Reject it before execution, record the reason and continue only if a safe next action exists. |
| Repository content contains malicious instructions | Treat repository text as untrusted data. Project files cannot override ASTRA's system policy or permission boundary. |
| Test command hangs | Stop it at the 60-second timeout, record the timeout and mark verification as failed. |
| Agent repeats the same action | Stop after three attempts for the same action and record the retry limit. |
| Patch changes an unapproved file | Reject the patch before applying it and record the out-of-scope path. |
| Model reports success but the test fails | Trust the deterministic test result; mark the run failed and include the failure output. |
| Task needs a missing permission | Pause before execution and require a new human decision. |
| Human needs to stop execution | Support cancellation before the next tool action; a cancelled run cannot be reported as successful. |

These responses are specification requirements until they are enforced by the
tool execution layer and covered by tests.

## 11. Initial evidence report format

Every ASTRA run will produce a machine-readable record and a human-readable
summary. The initial record uses this structure:

```json
{
  "run_id": "run-YYYYMMDD-HHMMSS",
  "goal": "Human task statement",
  "target_root": "test-repo",
  "baseline": {
    "git_status": "...",
    "git_revision": "..."
  },
  "observations": [
    {
      "path": "server/services/taskService.js",
      "location": "completeTask",
      "fact": "The completed copy is returned without being saved."
    }
  ],
  "plan": {
    "summary": "Save the completed task through the repository.",
    "approved": true,
    "approved_files": ["server/services/taskService.js"]
  },
  "actions": [
    {
      "type": "write",
      "path": "server/services/taskService.js",
      "status": "allowed"
    },
    {
      "type": "test",
      "command": "npm.cmd test",
      "exit_code": 0
    }
  ],
  "changed_files": ["server/services/taskService.js"],
  "verification": {
    "result": "passed",
    "tests": {"passed": 1, "failed": 0}
  },
  "final_status": "success",
  "limitations": []
}
```

The evidence report must connect each claim to an observation, action, diff or
deterministic command result. A model response by itself is not evidence.

## 12. Research required for M0

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

## 13. M0 deliverables

- This specification, updated after discussion.
- Selected sample repository and stack.
- Selected bounded engineering task.
- Initial permission matrix.
- Initial threat model.
- Evaluation checklist.
- Evidence report outline.
- Public milestone post outline.

The M0 result will be documented internally first. A public post will be
prepared after the first verified end-to-end engineering loop has evidence that
others can inspect. The post will describe the target task, changed files,
test result and current limitations.

## 14. Completion gate

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

**Gate result:** Complete. M1 implementation may proceed. M1 provider selection
and model-specific integration remain separate decisions under the M1 scope.

## 15. Open decisions

These decisions remain open until reviewed together:

- Which sample repository will be used?
- Will the first task be a failing-test fix or a small feature?
- Which model provider will be used for M1?
- Should the first tool boundary use a local workspace only or add Docker immediately?
- What exact budget should apply to one task run?
