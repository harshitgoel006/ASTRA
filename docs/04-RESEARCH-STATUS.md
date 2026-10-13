# ASTRA --- Research Status

## Purpose

This file records what has been discussed/researched so far so Codex
does not repeatedly rediscover the same context.

## Multi-Model Support

Status: ESTABLISHED / FEASIBLE at the basic integration level.

Discussed components: - model interface; - model gateway; - model
registry; - provider/runtime adapters; - request/response
normalization; - capability awareness.

The ASTRA-specific challenge is not simply connecting multiple models.
It is integrating model access with routing, memory, security,
verification, performance and cost.

## Model Routing

Status: ESTABLISHED as a general industry/research concept;
ASTRA-specific architecture remains PROPOSED.

Discussed routing approaches: - rule-based; - score-based; - learned; -
cascading.

Important signals: - task capability; - complexity; - risk; -
privacy/policy; - cost; - latency; - expected quality; - availability.

Proposed ASTRA flow:

Task -\> Project Context -\> Capability -\> Complexity -\> Risk -\>
Privacy/Policy -\> Hard Constraint Filtering -\> Model Ranking -\>
Execution -\> Verification -\> Escalation -\> Performance Memory

Research discussed: - OpenRouter model/provider selection and fallback
concepts; - RouteLLM learned routing; - research on dynamic
routing/cascading; - research on small-language-model front-door
routers; - current router designs that classify tasks and consider
cost/restrictions/fallback.

Open question: How much routing should be deterministic versus learned,
and how can ASTRA learn from engineering outcomes without becoming
unpredictable or unsafe?

Potential experiment: Compare: - strongest-model baseline; -
cheapest-model baseline; - rule-based; - score-based; - learned; -
hybrid ASTRA routing.

Metrics: - quality; - verification pass rate; - cost; - latency; -
failure rate; - escalation rate; - cost per successful verified outcome.

## Model Fallback

Status: CONCEPTUAL / next candidate capability, but not yet locked as
the immediate implementation milestone.

Fallback can address: - model unavailability; - timeout; - rate
limits; - provider failure; - malformed output; - verification
failure; - policy restriction.

Distinction: - routing chooses the initial model; - fallback decides
what happens after the chosen path fails.

Potential flow:

Selected Model -\> Execute -\> Result -\> Failure Analysis -\> Retry or
Fallback -\> Another Model -\> Verify -\> Success / Escalate

Security requirement: Fallback must not bypass privacy, policy or model
restrictions and must not create runaway retries or costs.

Memory should record failures and outcomes so future routing can
improve.

## ASTRA concept-document technology foundation

The concept documentation identifies broad technology areas including:

-   LLM APIs and open-source models;
-   embeddings;
-   routing;
-   agent frameworks;
-   Node/Python/Go;
-   queues/events;
-   PostgreSQL/vector/graph/object/event storage;
-   AST parsers;
-   language servers;
-   static analysis;
-   dependency graphs;
-   Git;
-   Docker/Kubernetes/cloud;
-   logs/metrics/traces/OpenTelemetry;
-   sandbox/IAM/secrets/network/policy/security scanners.

These are candidate foundations, not a final technology stack.

## Research discipline

For every future capability, distinguish:

ESTABLISHED -\> existing technology/research supports the mechanism.

PROPOSED -\> ASTRA's architecture/hypothesis.

VALIDATED -\> ASTRA experiment demonstrates it.

OPEN QUESTION -\> unresolved.

Do not present proposed architecture as already implemented.
