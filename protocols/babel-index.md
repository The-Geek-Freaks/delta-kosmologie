# Babel Index Protocol

The Babel index family `B_d` is a set of domain-specific engineered features for
loss of productive difference.

It is not universal across domains. A `B_LLM` value cannot be compared directly
with a `B_OSS`, `B_market`, or `B_epoch` value without a domain-specific
calibration layer.

## Candidate Multiplicative Form

```text
B_d(t) = norm_d((C_d(t) * K_d(t) * M_d(t) * A_d(t) * V_d(t)) /
                (D_d(t) * H_d(t) + epsilon))
```

## Variables

| Symbol | Meaning | Expected direction |
| --- | --- | --- |
| `C_d` | coupling degree | Higher increases Babel risk. |
| `K_d` | convergence pressure / Gleichschaltung | Higher increases Babel risk. |
| `M_d` | resource or optimization pressure | Higher increases Babel risk. |
| `A_d` | autonomous actor / agent density | Higher can increase Babel risk. |
| `V_d` | information velocity | Higher can increase Babel risk. |
| `D_d` | differentiation capacity | Higher buffers Babel risk. |
| `H_d` | heterarchy, redundancy, modularity | Higher buffers Babel risk. |

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

## Falsification

The Babel-ratio structure is falsified for a domain if:

- `B_d` has no incremental signal after controlling for raw variables,
- signal disappears under time splits,
- signal depends on post-hoc threshold or epsilon tuning,
- one single proxy explains the effect,
- outcome labels are explainable by simpler local null models.
