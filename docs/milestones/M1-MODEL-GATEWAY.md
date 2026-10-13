# ASTRA M1 --- Model Gateway

**Status:** IN PROGRESS - Gateway contract v0 implemented and verified; real provider integration remains

**Milestone purpose:** Give ASTRA one controlled and provider-independent way
to request model output before tools, repository access or autonomous actions
are introduced.

## 1. What M1 is

M1 answers one focused question:

> Can ASTRA send a bounded request to a model through one controlled interface
> and receive a predictable response shape?

The Model Gateway is ASTRA's single door to model providers. Other ASTRA
components will call the gateway instead of calling an AI provider directly.

```text
ASTRA component
    -> Model Gateway
        -> Provider Adapter
            -> Model Provider
        <- Normalized Model Response
```

The gateway is an infrastructure boundary. It does not decide which files to
edit, execute shell commands or grant tools to a model.

## 2. Why M1 comes after M0

M0 defined ASTRA's authority boundary and evidence rules. M1 now defines how
ASTRA talks to a model while keeping those model calls separate from tool
execution.

This separation matters because a model response is an observation or proposal.
It is not permission to read, write or execute anything.

## 3. M1 terminology

### Model request

The bounded input sent to the gateway. The current request contains:

- `system_prompt` - ASTRA's instruction context;
- `user_prompt` - the current task or question;
- `max_output_tokens` - an output limit.

### Provider adapter

A small implementation that translates ASTRA's common request into the API
shape required by one provider and translates that provider's result back into
ASTRA's common response shape.

### Model gateway

The controlled entry point that validates requests, calls the selected adapter
and rejects invalid or empty responses.

### Normalized model response

A provider-independent result containing:

- provider name;
- model name;
- response content;
- finish reason.

### Deterministic provider

A local fixture used to test the gateway without an AI model, network access,
API key or cost. It validates the architecture, not model intelligence.

## 4. Current implementation

### Source code

`astra-system/src/astra/model_gateway.py` contains:

- `ModelRequest`;
- `ModelResponse`;
- `ModelProvider` protocol;
- `ModelGateway`;
- `ModelGatewayError`;
- `DeterministicProvider`.

### Current behavior

The gateway currently:

1. rejects an empty system prompt;
2. rejects an empty user prompt;
3. rejects a non-positive output token limit;
4. forwards valid requests to the provider adapter;
5. rejects an empty provider response;
6. returns a normalized response for a valid call.

### Verification

`astra-system/tests/test_model_gateway.py` contains five M1 tests. The full
ASTRA suite contains the five M1 tests plus the ten M0 tests.

```text
15 passed in 0.08s
```

This proves the gateway contract and validation behavior. It does not prove
that a real AI provider can produce a useful engineering answer.

## 5. M1 scope

M1 will include:

- one provider-independent request and response contract;
- one provider adapter interface;
- one selected real provider adapter;
- configuration through environment variables or a local configuration layer;
- timeout and basic provider error handling;
- bounded output limits;
- token, latency and estimated cost metadata;
- evidence for each model call.

## 6. Explicit non-goals

M1 will not attempt to build:

- repository reading;
- file writing;
- shell or test execution;
- autonomous planning;
- multi-agent coordination;
- model routing or fallback;
- long-term memory;
- production deployment;
- unrestricted model access to tools;
- a claim that the model understands software engineering reliably.

## 7. Provider selection decision

The provider is intentionally not locked yet. The selection must consider:

- API quality for code and structured output;
- cost per bounded request;
- latency;
- privacy and data handling;
- availability of a local or free development path;
- JavaScript repository task performance.

The deterministic provider remains the default for local contract tests. A real
provider will be enabled only through an adapter and configuration, without
changing the gateway interface.

## 8. M1 permission and safety boundary

The model gateway may:

- receive bounded text input;
- call the configured provider adapter;
- return normalized model output;
- record call metadata and errors.

The model gateway may not:

- read the target repository directly;
- write files;
- execute commands;
- access secrets beyond the configured provider credential;
- bypass the permission policy;
- silently retry beyond its configured limit.

## 9. M1 success metrics

| Metric | Pass condition |
|---|---|
| Request validation | Invalid prompts and invalid output limits are rejected before the provider call. |
| Response normalization | A provider response is returned in the common `ModelResponse` shape. |
| Provider isolation | ASTRA code depends on the gateway contract, not provider-specific response objects. |
| Error handling | Empty responses and provider failures become explicit gateway errors. |
| Bounded output | Every request has a positive output limit. |
| Observability | Provider, model, latency, token and estimated cost metadata can be recorded. |
| Safety separation | The gateway has no direct file, shell or target-repository access. |
| Reproducibility | Contract tests pass with the deterministic provider without network access. |

## 10. M1 threat questions

- What happens when the provider is unavailable?
- What happens when the provider returns malformed output?
- What happens when a request exceeds its output limit?
- How are API keys kept out of prompts, logs and evidence?
- What data is allowed to leave the local workspace?
- How are provider retries bounded?
- How is provider cost recorded per run?
- How do we distinguish model claims from deterministic observations?

These questions will be answered before the real provider adapter is used for
engineering tasks.

## 11. M1 deliverables

- This M1 specification.
- Provider-independent request and response types.
- Provider adapter contract.
- Deterministic provider for offline tests.
- Selected real provider adapter.
- Configuration and secret handling rules.
- Timeout, error and retry behavior.
- Token, latency and cost metadata.
- Model call evidence record.
- M1 verification report.

## 12. Completion gate

M1 is complete when ASTRA can:

1. create a bounded model request;
2. validate it before sending;
3. send it through the provider adapter;
4. receive a normalized structured response;
5. handle timeout and provider errors safely;
6. record provider, model, latency, token, cost and result metadata;
7. prove the behavior with deterministic tests;
8. keep model access separate from repository tools and permissions.

The current implementation satisfies the request validation, normalization,
empty-response handling and offline-test portions. Real provider integration,
observability and final safety validation remain open.

## 13. Next M1 step

Before connecting a real provider, choose the development provider and define
the configuration and data-handling rules. Then implement one adapter without
changing the gateway contract.
