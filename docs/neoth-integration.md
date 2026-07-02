# NEOTH Integration

[NEOTH](https://github.com/The-Geek-Freaks/NEOTH) is planned as the first
runtime-level testbed for the LLM/agent branch of the Delta-Kosmologie
framework.

## Design Rule

The Babel probe must be asynchronous telemetry. It should observe the NEOTH
orchestration layer and must not block inference, tool calls, or agent routing.

Recommended placement:

- event stream observer in the orchestration layer,
- rolling-window feature reducer,
- offline evaluation job,
- optional dashboard export.

Non-goal:

- no direct steering of model output in the first phase,
- no hard runtime kill switch based only on `B_NEOTH`,
- no claim that operational predictive value proves the cosmological layer.

## Runtime Signals

| Paper variable | NEOTH proxy | Notes |
| --- | --- | --- |
| `C_d` | tool/agent coupling graph density | Count edges and dependency chains, not only calls. |
| `K_d` | semantic concentration / output self-similarity | Loop risk rises when variance collapses and similarity rises. |
| `M_d` | context, queue, latency, cost, timeout pressure | Captures resource stress. |
| `A_d` | active autonomous sessions and subagents | Count effective actors, not idle handles. |
| `V_d` | requests, tokens, events per time window | Use rolling windows. |
| `D_d` | prompt/tool separability and role distinction | Estimate via schema conflicts and embedding separation. |
| `H_d` | successful fallback and modular route redundancy | Existing fallback is not enough; it must work. |

## Outcome Labels

`Y(t+h)` should be defined before evaluation. The authoritative label enum is
defined in `schemas/neoth-babel-event.schema.json` (`collapse_label`). Always
reference the schema as the canonical source; this list is a human-readable
summary only.

| Schema value | Human label | Description |
| --- | --- | --- |
| `agent_loop` | Agent loop | Repeated state/action pattern without progress |
| `retry_storm` | Retry storm | Abnormal retry density in a short window |
| `tool_timeout_cascade` | Tool timeout cascade | Multiple dependent tool timeouts in one task graph |
| `tool_selection_failure` | Tool selection failure | Wrong tool chosen; tool call rejected or inapplicable |
| `context_limit_failure` | Context-limit crash | Truncation or crash at context boundary |
| `semantic_degradation` | Answer degeneration | High self-similarity plus falling task score under context pressure |
| `fallback_failure` | Fallback route failure | Primary route fails and fallback also fails or degrades objective |
| `objective_failure` | Task objective failure | Task not completed under predefined success criteria in a longitudinal run |

## Evaluation Shape

The correct test is nested:

```text
Base:     Y ~ controls + f(C,K,M,A,V,D,H)
Extended: Y ~ controls + f(C,K,M,A,V,D,H) + B_NEOTH
```

Evidence for the Babel feature requires out-of-sample incremental signal:

- likelihood-ratio improvement,
- cross-validation improvement,
- stable permutation importance,
- bootstrap confidence intervals above noise,
- robustness under time splits and version splits.

## First Implementation Phase

1. Emit structured telemetry events.
2. Aggregate rolling windows.
3. Compute raw features and candidate Babel forms.
4. Store collapse labels separately from feature extraction where possible.
5. Evaluate offline against strong baselines.
