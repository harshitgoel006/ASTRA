# ASTRA --- Prototype Roadmap and Milestone Workflow

**Status:** PROPOSED working plan; human approval is required before a milestone becomes a project decision.

**Purpose:** Define one incremental, testable build sequence for ASTRA and the workflow used to complete each milestone.

## 1. Roadmap principles

The 13 conceptual ASTRA layers describe the long-term design space. They do not define the implementation order.

The prototype will follow these principles:

- Build one small, measurable capability at a time.
- Prefer deterministic engineering tools for facts that tools can verify.
- Treat AI output as untrusted until it is checked by tools or human review.
- Define security boundaries before increasing autonomy.
- Record evidence, limitations and unresolved questions at every milestone.
- Publicly share completed milestones with a demonstration or reproducible result.
- Do not implement future milestones early because they appear in the long-term vision.

## 2. First prototype target

The first meaningful ASTRA proof should complete a bounded engineering task inside a controlled software repository:

```text
Human Goal
  -> Repository Understanding
  -> Task Understanding
  -> Plan
  -> Controlled Code Change
  -> Tests
  -> Observation
  -> Correction if needed
  -> Verification
  -> Evidence Report
```

The first prototype is successful when this loop produces reproducible observations, clear limits and an audit trail. Advanced capabilities such as predictive engineering, digital twins and organizational intelligence remain later research areas.

## 3. Proposed milestone sequence

### M0 --- Foundation and Engineering Environment

**Goal:** Establish the smallest safe environment in which ASTRA can inspect and operate on a sample repository.

**Scope:**

- Define the ASTRA thesis, prototype scope and non-goals.
- Define the control plane, agent runtime boundary and model access boundary.
- Select the sample repository and initial technology stack.
- Define configuration, storage, logging and workspace boundaries.
- Create an initial threat model and evaluation checklist.

**Completion gate:** An approved M0 specification states what the first vertical slice will demonstrate, what actions are prohibited and how success will be measured.

**Research focus:** AI engineering problem framing, SDLC workflow, threat modelling and evaluation design.

### M1 --- Model Gateway

**Goal:** Provide basic, controlled access to one AI model.

**Scope:**

- Model registration and metadata.
- Provider adapter and request/response normalization.
- Structured output contract.
- Configuration, timeout and basic error handling.
- Token, latency and cost logging.

Routing is not required here. One reliable model path is enough for the first experiment.

**Completion gate:** ASTRA can send a bounded request, receive a structured response and record what happened.

**Research focus:** LLMs, tokens, context windows, prompting, structured output, API design and tool calling.

### M2 --- Tool Execution and Sandbox

**Goal:** Allow an agent to use engineering tools through controlled permissions.

**Initial tools:**

- Filesystem read/write within an approved workspace.
- Git status, diff and history.
- Terminal commands with an allowlist.
- Test runner.
- Package manager only when explicitly approved.

**Conceptual flow:**

```text
Agent -> Tool Request -> Permission Check -> Sandbox -> Tool -> Observation -> Agent
```

**Completion gate:** Tool calls have permission checks, timeouts, workspace boundaries, audit records and a dry-run option.

**Research focus:** Process isolation, permissions, sandboxing, secrets, network controls and failure containment.

### M3 --- Agent Runtime and Orchestrator

**Goal:** Run one engineering agent through a bounded task loop.

**Scope:**

- Task state.
- Model interaction.
- Tool calls and observations.
- Iteration limits and token budgets.
- Timeout and cancellation.
- Basic failure handling.

Start with one engineering agent. A large multi-agent organization is not part of this milestone.

**Completion gate:** One agent can complete a small controlled interaction without exceeding its authority or execution budget.

**Research focus:** Agent loops, state machines, planning, retries, context engineering and orchestration.

### M4 --- Repository Understanding and World Model v0

**Goal:** Build a small, deterministic representation of repository reality.

**Initial facts:**

- Files and directories.
- Languages and frameworks.
- Classes and functions where a parser supports them.
- Routes and configuration.
- Dependencies and tests.
- Git information.

**Initial relationships:**

```text
API -> Controller -> Service -> Repository -> Database
```

This is a v0 representation, not the complete living software world model.

**Completion gate:** ASTRA can produce a repository summary whose facts can be traced to files, Git data or deterministic analysis output.

**Research focus:** ASTs, parsers, language servers, Git, dependency graphs and repository indexing.

### M5 --- Engineering Memory v0

**Goal:** Preserve useful project memory with provenance.

**Initial memory types:**

- Project facts.
- Architecture facts.
- Decisions.
- Previous tasks.
- Known issues.
- Failures.
- Verified facts.

Every stored item should record its source, timestamp, confidence and validity where practical.

**Completion gate:** ASTRA can retrieve a small set of verified project facts and distinguish them from unverified agent statements.

**Research focus:** Embeddings, vector search, RAG, provenance, validity and knowledge representation. Use the smallest mechanism that solves the current task.

### M6 --- Planning and Reasoning

**Goal:** Convert an engineering goal into an explicit, reviewable plan.

**Scope:**

- Understand the requirement.
- Inspect the repository.
- Identify affected components.
- Create a plan.
- Decompose the task.
- Identify dependencies and risks.
- Ask for approval when the task exceeds its authority.

**Completion gate:** ASTRA produces a plan whose affected files, dependencies, risks and success criteria can be reviewed before execution.

**Research focus:** Requirements analysis, task decomposition, planning, uncertainty, trade-offs and risk assessment.

### M7 --- First Autonomous Engineering Loop

**Goal:** Demonstrate the complete controlled loop on one real bounded task.

**Target:**

```text
Goal -> Understand -> Plan -> Execute -> Observe -> Reason -> Correct -> Verify
```

**Example tasks:**

- Fix a failing test.
- Implement a small bounded feature.
- Reproduce and patch a contained bug.

**Completion gate:** A repeatable demo completes the selected task inside the controlled environment and records the full execution trace.

**Research focus:** Agent reliability, long-horizon failure modes, test-driven engineering and reproducibility.

### M8 --- Verification and Evidence

**Goal:** Connect engineering claims to observations and evidence.

**Evidence pattern:**

```text
Claim -> Source -> Test or Check -> Observation -> Result
```

**Example:**

```text
Claim: Authentication bug fixed.
Evidence: Changed files + relevant test + observed test result + reviewable diff.
```

**Completion gate:** ASTRA can produce an evidence report that separates what the agent believed, what the system observed and what was verified.

**Research focus:** Evaluation design, test oracles, quality checks, observability, metrics and evidence graphs.

### M9 --- Security and Governance

**Goal:** Add controls required for safe engineering-agent operation.

**Scope:**

- Agent identity and capability permissions.
- Least privilege.
- Sandbox controls.
- Network policy.
- Secret isolation.
- Prompt and tool injection awareness.
- Audit trail.
- Human approval points.
- Risk levels and escalation.
- Emergency stop.

This milestone covers both developmental security and post-deployment security concerns relevant to the prototype.

**Completion gate:** ASTRA can explain, enforce and audit what the agent is allowed to do.

**Research focus:** Agent security, prompt injection, tool misuse, sandbox escape, supply-chain security, DevSecOps and incident response.

### M10 --- Model Routing and Fallback

**Goal:** Choose and recover between models using engineering signals.

**Scope:**

- Task capability.
- Complexity.
- Risk.
- Privacy and policy.
- Cost and latency.
- Availability.
- Retry and fallback limits.
- Escalation when verification fails.

Fallback must not bypass privacy, security or model restrictions and must not create runaway retries or costs.

**Completion gate:** ASTRA can compare a selected model result with a fallback path and record quality, cost, latency and verification outcomes.

**Research focus:** Model routing, cascading, fallback design, evaluation metrics and engineering economics.

### M11 --- Multi-Agent Engineering

**Goal:** Introduce specialized roles only after the single-agent loop is understandable and testable.

**Possible roles:**

- Architect.
- Planner.
- Developer.
- QA.
- Security reviewer.
- Code reviewer.
- Debugger.

Each agent must have an explicit role, input, output, authority, constraints and success criteria.

**Completion gate:** A small multi-agent experiment demonstrates a measurable benefit over the single-agent baseline and has conflict and escalation handling.

**Research focus:** Agent contracts, shared state, coordination, disagreement, scheduling and human escalation.

### M12 --- Continuous Engineering

**Goal:** Extend one-shot task execution toward a controlled feedback loop.

```text
Build -> Deploy -> Observe -> Detect -> Investigate -> Fix -> Verify -> Continue
```

**Completion gate:** A controlled experiment shows how ASTRA receives an observation, investigates it, proposes or applies a bounded change and verifies the result.

**Research focus:** CI/CD, logs, metrics, traces, OpenTelemetry, deployment controls and incident workflows.

### M13 --- Advanced ASTRA Research

**Goal:** Explore advanced capabilities after the core engineering loop has evidence.

**Research areas:**

- Predictive engineering.
- Digital twin and simulation.
- Counterfactual engineering.
- Organizational intelligence.
- Autonomous research.

These are not first-prototype requirements.

**Completion gate:** Each advanced capability must have a separate research question, experiment design and evaluation plan before implementation.

## 4. Fixed workflow for every milestone

Before moving to the next milestone:

1. Explain the problem and why the milestone exists.
2. Define scope, non-goals, dependencies and security boundaries.
3. Identify the AI and engineering concepts that need research.
4. Review relevant documentation, research or established tools.
5. Compare reasonable implementation alternatives.
6. Select an approach with explicit trade-offs.
7. Implement only the approved scope.
8. Run deterministic checks and tests.
9. Record evidence, limitations and unresolved questions.
10. Update the project documentation.
11. Prepare a public milestone summary.
12. Review the completion gate before starting the next milestone.

## 5. Public milestone format

Each public update should communicate a concrete result:

- What problem was addressed.
- What ASTRA can now do.
- What evidence was collected.
- What failed or remains limited.
- What the next milestone will test.

The project should be shared after meaningful, reviewable milestones rather than after broad claims about the complete vision.

## 6. Cost and resource principles

The prototype should be local-first and budget-controlled.

- M0 and most deterministic parts of M2-M5 can run with existing local tools and no model API cost.
- M1, M3, M6 and M7 may create API usage costs depending on the selected model and number of runs.
- API calls must have token budgets, iteration limits, retry limits and spending limits.
- Cloud databases, hosted runners, monitoring and GPU resources should be introduced only when a milestone requires them.
- Cost, latency and quality should be recorded as evidence once model routing is introduced.

The exact cost estimate will be decided after the sample repository, model provider and execution frequency are selected.

## 7. Current next milestone

The next milestone is **M0 --- Foundation and Engineering Environment**.

M0 should produce a short, approved specification covering:

- ASTRA's first prototype thesis.
- The first sample repository and technology stack.
- The first bounded engineering task.
- Scope and non-goals.
- Security boundaries.
- Success metrics.
- Evidence format.
- Public demonstration plan.

Only after M0 is approved should implementation begin.
