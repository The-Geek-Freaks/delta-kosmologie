# Pilot Protocol B: NEOTH LLM/Agent Runtime

This protocol translates the paper's LLM/agent ecosystem pilot into a concrete
NEOTH runtime experiment.

## Research Question

Does a structured Babel feature predict near-future runtime degradation in an
agentic LLM system better than raw telemetry features alone?

## System

- Runtime: [NEOTH](https://github.com/The-Geek-Freaks/NEOTH)
- Domain: local LLM/agent orchestration
- Unit of analysis: rolling telemetry window
- Suggested windows: 5 minutes, 15 minutes, 60 minutes, or last 1,000 inference
  calls

## Prediction Target

Predict whether a collapse/degradation event occurs in the next horizon `h`.

Suggested horizons:

- `h = 5 minutes` for operational warnings,
- `h = 30 minutes` for system-level drift,
- `h = next task run` for agent benchmark episodes.

## Candidate Collapse Labels

| Label | Definition sketch |
| --- | --- |
| `agent_loop` | repeated state/action pattern without progress |
| `retry_storm` | abnormal retry density in a short window |
| `tool_timeout_cascade` | multiple dependent tool timeouts in one task graph |
| `tool_selection_failure` | wrong, rejected, or inapplicable tool selected at call boundary |
| `context_limit_failure` | truncation or crash at context boundary |
| `fallback_failure` | primary route fails and fallback fails or degrades objective |
| `semantic_degradation` | high self-similarity plus falling task score |
| `objective_failure` | task not completed under predefined success criteria |

## Features

Raw feature set:

```text
F = {C, K, M, A, V, D, H}
```

Candidate Babel features (three defined forms):

| Form | Formula | Primary use |
| --- | --- | --- |
| `B_neoth_log` | `log(C)+log(K)+log(M)+log(A/D)+log(V/H)` | **Primary** — cross-instance pooling (natural log, no epsilon) |
| `B_neoth_mult` | `norm((C×K×M) / ((D/A)×(H/V)+ε))` | Interpretability variant (requires pre-registered epsilon) |
| `B_neoth_bottleneck` | `min(C,K,M,A,V) / max(D,H)` | Structural stress test |

`B_neoth_log` is the primary form for all pooled analyses.
`B_neoth_mult` is the interpretability variant; epsilon MUST be pre-registered before data collection.
`B_neoth_bottleneck` is the structural stress test form.

## Baselines

At minimum:

- last-event baseline,
- task type baseline,
- queue/load baseline,
- raw-feature logistic regression,
- regularized regression,
- gradient boosting or random forest,
- flexible interaction model.

## Evidence Standard

The protocol supports the Babel feature only if a pre-registered `B_neoth_*`
variant, led by `B_neoth_log`, improves prediction after controlling for raw
features and basic operational controls.

Valid evidence:

- cross-validated AUROC/AUPRC or calibration gain,
- permutation importance that stays above noise,
- likelihood-ratio improvement,
- bootstrap interval excluding zero incremental gain,
- stable direction across time splits.

Invalid evidence:

- post-hoc threshold tuning,
- a single impressive chart,
- public benchmark degradation alone,
- runtime crash caused by a known implementation bug,
- success on NEOTH used as proof of cosmological ontology.
