# ASTRA M1 --- Model Gateway

**Status:** COMPLETE - Gateway, Ollama adapter, evidence recorder, configuration, runtime wiring and cost policy verified on 15 October 2026

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
- `DeterministicProvider`;
- `OllamaProvider` for the local `http://127.0.0.1:11434/api/chat` endpoint.

The Ollama adapter includes a Qwen-compatible empty thinking prefill so a
bounded response can reach the final `content` field instead of exhausting its
output limit in reasoning tokens.

`astra-system/src/astra/config.py` contains `GatewaySettings`, which loads and
validates the model name, Ollama base URL, request timeout and maximum output
tokens from environment variables.

`astra-system/src/astra/evidence.py` contains `JsonlModelCallRecorder`, which
stores prompt-free provider and timing metadata in an ASTRA run file.

Cost policy: local Ollama and deterministic fixture calls record
`estimated_cost_usd: 0.0` with an explicit `cost_basis`. This is direct provider
billing only; electricity and hardware costs are outside the prototype
measurement.

### Current behavior

The gateway currently:

1. rejects an empty system prompt;
2. rejects an empty user prompt;
3. rejects a non-positive output token limit;
4. forwards valid requests to the provider adapter;
5. rejects an empty provider response;
6. returns a normalized response for a valid call;
7. applies validated environment-backed timeout and output limits;
8. records prompt-free model-call evidence when a recorder is supplied.

### Verification

The M1 test files contain twenty-one tests covering the gateway contract,
Ollama adapter, configuration, evidence recorder and runtime wiring. The full
ASTRA suite contains these twenty-one M1 tests plus the ten M0 tests.

```text
31 passed in 0.35s
```

This proves the gateway contract, validation behavior, Ollama response handling,
configuration validation, runtime wiring, cost metadata and prompt-free evidence
recording with deterministic adapter tests.

### Live smoke test

On 15 October 2026, ASTRA successfully sent a request through
`ModelGateway(OllamaProvider())` to the local `qwen3:4b` server.

Observed response:

```text
ASTRA gateway works
ModelUsage(
  prompt_tokens=31,
  completion_tokens=82,
  total_duration_ns=25268392200,
  load_duration_ns=55336900,
  prompt_eval_duration_ns=4002336000,
  eval_duration_ns=21080930000
)
```

This validates the live provider adapter and confirms that Ollama usage and
timing metadata can reach ASTRA's normalized response. The current runtime
also produced a prompt-free JSONL record under
`astra-system/runs/model_calls.jsonl` with `status: success`,
`finish_reason: stop`, `estimated_cost_usd: 0.0` and
`cost_basis: local_ollama_no_provider_charge`.

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

The current implementation satisfies request validation, normalization,
empty-response handling, Ollama adapter behavior, environment-backed limits,
live smoke testing, prompt-free JSONL evidence tests, reusable runtime wiring
and explicit local cost policy. The fresh live evidence record was verified on
15 October 2026, so the M1 completion gate is satisfied.

## 13. M1 completion and next milestone

The reusable command is:

```powershell
Set-Location .\astra-system
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m astra model-call
```

It constructs `GatewaySettings`, `OllamaProvider` and
`JsonlModelCallRecorder` together, then produces one real local Ollama call
record under `astra-system/runs/` and prints the response. The record stores
provider, model, usage, timing, result status and errors without storing secret
keys or prompt content.

M1 is complete. The next major milestone is M2 - Tool Execution and Sandbox, beginning with
controlled `ToolRequest` and `ToolResult` contracts around the already tested
permission decisions.
