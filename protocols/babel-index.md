# Babel Index Protocol

The Babel index family `B_d` is a set of domain-specific engineered features for
loss of productive difference.

It is not universal across domains. A `B_LLM` value cannot be compared directly
with a `B_OSS`, `B_market`, or `B_epoch` value without a domain-specific
calibration layer.

## Candidate Multiplicative Form

```text
B_d(t) = norm_d(C_d(t) * K_d(t) * M_d(t) * (A_d(t) / D_d(t)) * (V_d(t) / H_d(t)))
```

The ratio form is undefined (null) when `D_d` or `H_d` is zero; for
computation use the simplified form below, which regularizes the combined
buffer denominator with `epsilon`.

Agent density `A_d` and information velocity `V_d` appear as load/capacity
ratios rather than bare numerator terms. An ensemble of independent specialised
agents increases `A_d` but simultaneously increases `D_d` and `H_d`. Treating
`A_d` as unconditionally risk-increasing contradicts the hedged direction in the
variable table. The ratio form `A_d / D_d` ("agent density per unit of role
differentiation") and `V_d / H_d` ("velocity per unit of redundant capacity")
make risk depend on load/capacity mismatch rather than load alone.

**Simplified five-factor form** (collapsing the ratios):

```text
B_d(t) = norm_d((C_d(t) * K_d(t) * M_d(t)) /
                ((D_d(t) / A_d(t)) * (H_d(t) / V_d(t)) + epsilon))
```

Both forms are algebraically equivalent. The five-factor simplified form is
preferred for interpretability.

**Log form** (primary form for cross-instance pooled analysis):

```text
B_log = log(C) + log(K) + log(M) + log(A) - log(D) + log(V) - log(H)
      = log(C) + log(K) + log(M) + log(A/D) + log(V/H)
```

No epsilon required. `B_log` is undefined (null) when any numerator variable
is zero.

## Variables

| Symbol | Meaning | Expected direction |
| --- | --- | --- |
| `C_d` | coupling degree | Higher increases Babel risk. |
| `K_d` | convergence pressure / Gleichschaltung | Higher increases Babel risk. |
| `M_d` | resource or optimization pressure | Higher increases Babel risk. |
| `A_d` | autonomous actor / agent density | Higher increases risk *conditional on* `D_d` not increasing proportionally. Use as `A_d / D_d`. |
| `V_d` | information velocity | Higher increases risk *conditional on* `H_d` not increasing proportionally. Use as `V_d / H_d`. |
| `D_d` | differentiation capacity | Higher buffers Babel risk. |
| `H_d` | heterarchy, redundancy, modularity | Higher buffers Babel risk. |

## K_d Measurement Protocol (NEOTH)

`K_d` is the convergence pressure / output self-similarity variable. It is the
most novel variable in the Babel Index and requires an explicit measurement
algorithm to produce reproducible, comparable values across NEOTH deployments.

**Algorithm (reference implementation):**

```text
K_d(t, w) = mean pairwise cosine similarity of the last w output
             token-sequence embeddings within the rolling window
```

Where:

- `w` is the comparison window in turns (default: all turns in the current
  rolling window, minimum 2).
- Embeddings are computed from the final assistant response per turn (not the
  full context).
- The embedding model MUST be declared in the `algorithm_versions.K_embedding_model`
  field of each window record as a HuggingFace model ID (e.g.,
  `sentence-transformers/all-MiniLM-L6-v2`) or, for runtime-native embeddings,
  as `runtime:{runtime_id}:{version}`.

**Scale:**

- `K_d = 0`: maximum diversity — all outputs are orthogonal in embedding space.
- `K_d = 1`: all outputs within the window are identical in embedding space.

**Baseline / null value:**

- If fewer than 2 turns are available in the window, set `K_d = null` (do not
  impute zero or one).

**Reproducibility requirement:**

Two NEOTH deployments using different embedding models produce incomparable K_d
values. Cross-instance pooled analysis MUST stratify or correct for
`K_embedding_model`. The `neoth-babel-window` schema enforces this via the
`algorithm_versions.K_embedding_model` field.

**Alternative proxy (when no embedding model is available):**

Normalized edit distance between successive assistant responses (character
level, mean over the window). This is a weaker proxy; analysis using it MUST
declare `K_algorithm_version = edit_distance_v1` and MUST NOT be pooled with
cosine-similarity measurements without a declared calibration function.

## Required Controls

Every empirical application must define:

- domain `d`,
- feature extraction rules,
- normalization method,
- `epsilon` governance or an epsilon-free log form,
- prediction horizon,
- collapse/outcome labels,
- negative controls,
- time split or holdout regime.

## Nested Feature Test

The multiplicative form is a log-linear special case with fixed signs and
coefficients. It should therefore be tested as an engineered feature.

Required comparison:

```text
M0: controls only
M1: controls + raw features
M2: controls + raw features + B_d
M3: controls + raw features + learned interactions
```

`B_d` is useful only if it contributes stable out-of-sample signal beyond raw
features and trivial size/activity controls.

## Epsilon Governance

The log form is the **primary form for cross-instance pooled analysis**:

```
B_log = log(C) + log(K) + log(M) + log(A/D) + log(V/H)
      = log(C) + log(K) + log(M) + log(A) − log(D) + log(V) − log(H)
```

No epsilon is required.  B_log is undefined when any numerator variable is
zero (returns null, not zero).

If the multiplicative form is used for interpretability reporting, epsilon
MUST be set BEFORE examining any outcome labels:

```
epsilon = 0.01 × median((D / A) × (H / V))   over the first 10% of the instance's data
```

(The median is taken over the simplified form's actual buffer denominator
`(D/A) × (H/V)` — not over the raw `D × H` product, which lives on a
different scale once `A` and `V` enter as ratios.)

The epsilon value is then frozen.  Any change constitutes a new analysis.

When `B_neoth_mult` is present in a window record, `B_neoth_mult_epsilon`
and `B_neoth_mult_epsilon_rule` are required.

## Candidate Score Forms

Three forms are defined for the NEOTH domain.  All are domain-prefixed:

| Key | Formula | Primary use |
| --- | --- | --- |
| `B_neoth_log` | `log(C)+log(K)+log(M)+log(A/D)+log(V/H)` | Cross-instance pooling (no epsilon) |
| `B_neoth_mult` | `norm((C×K×M) / ((D/A)×(H/V)+ε))` | Interpretability; five-factor form |
| `B_neoth_bottleneck` | `min(C,K,M,A,V) / max(D,H)` | Structural stress test |

(The bottleneck form deliberately uses the RAW variables — it asks "what is
the weakest amplifier against the strongest buffer", so the load/capacity
ratio substitution does not apply here. A ratio-based bottleneck variant
`min(C,K,M,A/D,V/H) / max(D,H)` may be pre-registered as an additional M4
candidate form.)

B_d values across domains (`B_neoth_*` vs `B_oss_*`) MUST NOT be compared
without a published calibration function.

## Negative Controls

Every data collection run must include negative-control windows.  See
`protocols/collapse-label-definitions.md` for the negative-control
specification and the falsification trip-wire.

At minimum: permuted-label control, synthetic-stable control, temporal-null
control.

## Falsification

The Babel-ratio structure is falsified for a domain if:

- `B_d` has no incremental signal after controlling for raw variables,
- signal disappears under time splits,
- signal depends on post-hoc threshold or epsilon tuning,
- one single proxy explains the effect,
- outcome labels are explainable by simpler local null models,
- negative controls show B_d indistinguishable from positive windows.
