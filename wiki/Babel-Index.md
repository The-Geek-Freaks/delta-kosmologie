# Babel Index

![Babel Index pipeline](https://raw.githubusercontent.com/The-Geek-Freaks/delta-kosmologie/main/assets/babel-index-pipeline.svg)

The Babel Index is a domain-specific feature family for measuring loss of
productive difference.

## Candidate Form

```text
B_d(t) = norm_d((C_d * K_d * M_d * A_d * V_d) / (D_d * H_d + epsilon))
```

## Variables

| Symbol | Meaning | NEOTH Runtime Proxy |
| --- | --- | --- |
| C | Coupling degree | Tool/agent dependency graph density |
| K | Convergence pressure | Output self-similarity, loop proximity |
| M | Resource pressure | Queue load, context pressure, timeout pressure |
| A | Agent density | Active autonomous sessions and subagents |
| V | Information velocity | Requests, tokens, events per rolling window |
| D | Differentiation capacity | Role, prompt, and tool-schema separability |
| H | Heterarchy/redundancy | Working fallback routes and modular alternatives |

## Required Comparison

The score must be tested against:

- raw features C, K, M, A, V, D, H,
- simple operational baselines,
- null labels,
- shuffled/permuted controls,
- time-split holdouts,
- bootstrap intervals.

## Useful Only If

The Babel feature is useful only if it adds out-of-sample signal after raw
telemetry and simpler controls are already in the model.
