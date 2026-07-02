# Delta Cosmology v1.0

**RDelta preformalism: dark-energy interpretation, boundary tangents, inner
time, and AGI as a layer transition.**

Status: speculative preformal framework, not established physics.

Authorial idea: Alexander Zuber-Jatzke / RIC context  
Repository edition: 2026-07-01

## Abstract

Delta Cosmology begins with the claim that neither difference nor recursion is
sufficient as a primitive on its own. Difference becomes stable only through
recursion. Recursion becomes distinguishable only through difference. Their
co-condition is called **RDelta**.

The framework reads the Big Bang not as an absolute beginning of being, but as a
local boundary of differentiation inside an emergent universe. Inner observers
experience the ordered processing of differences as time and the stable
projection of that order as causality.

The operational branch of the paper is the **Babel Index**: a domain-specific,
calibrated index family for loss of productive difference in bounded systems.
It is not thermodynamic entropy. It is not measured in joules per kelvin. It is
an empirical instrument candidate for systems such as software ecosystems,
institutions, markets, and LLM/agent runtimes.

## What The Paper Does Not Claim

- It does not prove that the universe is literally a breath of a higher
  substrate.
- It does not replace standard cosmology, thermodynamics, quantum mechanics, or
  evolutionary biology.
- It does not equate semantic Babel with thermodynamic entropy.
- It does not infer cosmological truth from successful software or LLM pilots.
- It does not allow post-hoc historical pattern reading without holdouts,
  blind coding, or negative controls.

## What The Paper Does Claim

- Difference and recursion jointly form a minimal operator for observable
  structure.
- Inner time is the ordering of stored or correlated differences inside an
  observing subsystem.
- Causality is a stable inner projection of that order along a gradient.
- Maintaining productive difference across system components requires information
  processing capacity. Query-response cycles, context retention, and routing
  decisions each consume finite resources. When resource pressure M_d exceeds
  differentiation capacity D_d, productive difference cannot be maintained
  regardless of initial configuration.
- Major transitions often involve changes in information storage or
  transmission.
- Babel is loss of productive difference through overcoupling or gradient
  exhaustion.
- Empirical use requires finite parameter budgets, countable coupling graphs,
  calibration, and model comparison against local null models.

## Two-Track Architecture

| Track | Status | Success criterion | What does not follow |
| --- | --- | --- | --- |
| Empirical instrument | Complexity science, OSS, LLMs, institutions | `B_d` and echo criteria beat strong baselines out of sample | No proof of Omega, Xi, or cosmic breath ontology |
| Natural philosophy | RDelta, inner time, recursion, difference | Conceptual coherence and no physics category errors | No standalone empirical confirmation |
| Cosmological test path | **Planned future work — not a current scientific claim.** Xi shadow models and dark-energy signatures are named as the intended test path but are not specified in v1.0. No Xi model definition, dataset, or registered test statistic exists yet. Success criterion (when specified): improvement over LambdaCDM, quintessence, modified gravity, and standard GR at finite parameter count. Planned for ROADMAP v1.4. | No validation from sociotechnical pilots |

## RDelta

```text
RDelta := <R, Delta | R becomes distinguishable through Delta,
                    Delta becomes stable through R>
```

`R` is recursion, return, memory, iteration, or echo.  
`Delta` is difference, distinction, boundary, or state separation.

The framework treats them as co-conditions rather than as a hierarchy. The
co-condition is not a circular assertion: it is a compressed statement of a
theorem derivable from a single axiom — "a distinction requires persistence,
and persistence requires distinction." Distinction without persistence collapses
to noise; persistence without distinction collapses to a constant. Neither pole
is stable alone, so both are jointly minimal. The mutual dependence is a
consequence, not a premise. Prior art: Bateson's "difference that makes a
difference" (*Steps to an Ecology of Mind*, 1972) and Spencer-Brown's cross and
re-entry operators (*Laws of Form*, 1969). Full derivation: `docs/foundations.md`.

## Babel Index Family

For a domain `d`:

```text
B_d = f_d(C_d, K_d, M_d, A_d, V_d, D_d, H_d)
```

Candidate multiplicative form (five stress terms after ratio substitution):

```text
B_d(t) = norm_d((C_d(t) * K_d(t) * M_d(t)) /
                ((D_d(t) / A_d(t)) * (H_d(t) / V_d(t)) + epsilon))
```

Agent density `A_d` and information velocity `V_d` appear as load/capacity
ratios. An ensemble of independent specialised agents increases `A_d` while
simultaneously increasing `D_d` and `H_d`; treating `A_d` as unconditionally
risk-increasing would contradict this. The ratio `A_d / D_d` (agent density
per unit of role differentiation) and `V_d / H_d` (velocity per unit of
redundant capacity) make risk depend on load/capacity mismatch rather than load
alone. See `protocols/babel-index.md` for the full derivation and log form.

| Symbol | Meaning | Direction |
| --- | --- | --- |
| `C_d` | Coupling degree | Higher increases risk. |
| `K_d` | Coherence pressure / convergence pressure | Higher increases risk. |
| `M_d` | Competition, resource, or optimization pressure | Higher increases risk. |
| `A_d` | Autonomous actor or agent density | Risk-increasing conditional on `D_d`. Use as `A_d / D_d`. |
| `V_d` | Information velocity | Risk-increasing conditional on `H_d`. Use as `V_d / H_d`. |
| `D_d` | Differentiation capacity / semantic separability | Higher buffers risk. |
| `H_d` | Heterarchy, redundancy, modularity | Higher buffers risk. |

`B_d` is not universal. A `B_LLM` score cannot be directly compared with a
`B_OSS`, `B_market`, or `B_epoch` score without domain-specific calibration.

## Pilot Protocol B: LLM/Agent Ecosystems

LLM and agent ecosystems are a high-risk but high-value test domain because they
provide operational telemetry:

- inference calls,
- tool calls,
- retries,
- context-window pressure,
- queue pressure,
- subagent counts,
- fallback attempts,
- task outcomes,
- semantic self-similarity.

A Babel degradation is not a bad public benchmark score. It requires a
portfolio-style degradation definition and controls for contamination,
benchmark saturation, Goodharting, distribution shift, and architecture limits.

## NEOTH Runtime Test

[NEOTH](https://github.com/The-Geek-Freaks/NEOTH) is the first planned runtime
testbed for this branch.

The NEOTH probe should:

1. Observe orchestration events asynchronously.
2. Aggregate rolling telemetry windows.
3. Compute raw `{C,K,M,A,V,D,H}` features.
4. Compute candidate Babel variants.
5. Predict near-future collapse labels.
6. Compare against strong baselines.

Candidate NEOTH collapse labels:

- agent loop,
- retry storm,
- tool timeout cascade,
- context-limit failure,
- fallback failure,
- semantic degradation,
- objective failure.

## Nested Feature Test

The multiplicative Babel form is not a magic term. Log-transformed, it is a
log-linear special case with fixed signs and coefficients:

```text
log B_mult ~= log C + log K + log M + log(A/D) + log(V/H)
           = log C + log K + log M + log A - log D + log V - log H
```

The correct question is not whether a zero-parameter index beats all flexible
models. The correct question is whether the engineered Babel feature adds
incremental signal beyond the raw features.

```text
Base:     Y ~ controls + f(C,K,M,A,V,D,H)
Extended: Y ~ controls + f(C,K,M,A,V,D,H) + B_variant(F)
```

Valid evidence:

- likelihood-ratio improvement,
- cross-validated AUC/AUPRC, Brier, or log-loss improvement,
- non-zero permutation importance,
- stable bootstrap confidence intervals,
- stable sign across time splits.

## Falsification Points

The Babel Index loses value if:

- it fails against trivial size or activity metrics,
- it fails out of sample,
- it becomes irrelevant after controlling for raw features,
- epsilon must be selected after seeing outcomes,
- one single proxy explains the full effect,
- LLM degradation is fully explained by benchmark saturation, contamination,
  architecture limits, or Goodharting.

If sociotechnical pilots work but cosmological Xi tests fail, RDelta narrows to
a useful cybernetic framework. The cosmology is not co-validated.

## One-Sentence Compression

The universe appears through stored difference; difference becomes stable only
through recursion; inner time is the ordering of those stored differences;
causality is their inner projection; Babel is the loss of productive difference;
and AGI/agent systems are a late technical layer where this loss can be measured
with operational telemetry.
