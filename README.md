# Delta-Kosmologie

[![Paper artifact check](https://github.com/The-Geek-Freaks/delta-kosmologie/actions/workflows/paper-artifact-check.yml/badge.svg)](https://github.com/The-Geek-Freaks/delta-kosmologie/actions/workflows/paper-artifact-check.yml)
[![Markdown hygiene](https://github.com/The-Geek-Freaks/delta-kosmologie/actions/workflows/markdown-hygiene.yml/badge.svg)](https://github.com/The-Geek-Freaks/delta-kosmologie/actions/workflows/markdown-hygiene.yml)

**RDelta-Praeformalismus: extrinsische dunkle Energie, Randtangenten,
Innenzeit und AGI als Layerwechsel.**

This repository hosts the public working version of the Delta-Kosmologie paper
and its empirical test protocols.

The project is intentionally split into two layers:

1. **Paper layer:** a preformal theoretical framework around recursion,
   difference, inner time, Babel dynamics, and domain-specific index models.
2. **Instrument layer:** operational protocols that can be tested in bounded
   technical domains without claiming proof of the cosmological interpretation.

## Paper

- PDF: `paper/delta-kosmologie-v1.0.pdf` *(canonical artifact, staged locally until binary upload/release is available)*
- Extracted text: [paper/delta-kosmologie-v1.0.txt](paper/delta-kosmologie-v1.0.txt)
- Paper notes: [paper/README.md](paper/README.md)

## Core Claim Boundary

Delta-Kosmologie is not presented as established physics. The paper separates:

- physical equations with units,
- dimensionless domain indices,
- heuristic operators and structural readings.

The Babel index is therefore **not** thermodynamic entropy in joules per kelvin.
It is a domain-specific, calibrated index family for loss of productive
difference inside a bounded system.

## NEOTH Pilot

[NEOTH](https://github.com/The-Geek-Freaks/NEOTH) will be used as the first
agentic LLM runtime for testing the framework's **Pilot Protocol B:
LLM/agent ecosystems**.

The NEOTH integration is planned as an asynchronous telemetry probe. It must not
sit in the critical inference path. Its job is to observe runtime events, compute
rolling Babel-window features, and test whether a structured Babel score provides
incremental predictive signal for agent failures, loop states, tool fragility,
context degeneration, and fallback collapse.

See:

- [docs/neoth-integration.md](docs/neoth-integration.md)
- [protocols/pilot-b-neoth.md](protocols/pilot-b-neoth.md)
- [protocols/babel-index.md](protocols/babel-index.md)

## Repository Map

| Path | Purpose |
| --- | --- |
| `paper/` | Canonical PDF and extracted text snapshot |
| `docs/` | Explanatory notes and integration design |
| `protocols/` | Empirical protocols, null models, and falsification criteria |
| `schemas/` | Machine-readable telemetry/event schemas |
| `examples/` | Example telemetry windows and expected fields |
| `.github/` | CI, issue templates, contribution hygiene |

## Babel Index Sketch

For a domain `d`, the paper treats the multiplicative Babel form as one
candidate engineered feature:

```text
B_d(t) = norm_d((C_d * K_d * M_d * A_d * V_d) / (D_d * H_d + epsilon))
```

with:

- `C_d`: coupling degree
- `K_d`: convergence pressure / semantic concentration
- `M_d`: resource, optimization, or queue pressure
- `A_d`: autonomous actor or agent density
- `V_d`: information velocity
- `D_d`: differentiation capacity / semantic separability
- `H_d`: heterarchy, redundancy, modularity

The repository treats this as a falsifiable engineered feature, not a magic
whole-model.

## Falsification Standard

A strong result requires that a Babel feature provides out-of-sample incremental
signal after controlling for the raw variables, trivial size/activity metrics,
and flexible baselines.

If `B_d` becomes irrelevant after controlling for `{C,K,M,A,V,D,H}`, the
specific Babel-ratio structure is falsified for that domain.

## Citation

Use [CITATION.cff](CITATION.cff) for citation metadata.
