# Babel Score Computation — Step-by-Step Arithmetic

This document shows the exact arithmetic for each candidate score form using
the feature values from `neoth-babel-window.example.json`.  It exists so the
example file is a reproducibility check rather than illustrative fiction.

## Input Features

```
C = 0.62   (coupling density)
K = 0.71   (convergence pressure)
M = 0.56   (resource pressure)
A = 0.48   (agent density)
V = 0.68   (velocity)
D = 0.44   (differentiation capacity)
H = 0.39   (heterarchy / redundancy)
```

## Form 1: B_log (Primary — epsilon-free, poolable)

```
B_log = log(C) + log(K) + log(M) + log(A) + log(V) − log(D) − log(H)
```

```
log(0.62) = −0.4780
log(0.71) = −0.3425
log(0.56) = −0.5798
log(0.48) = −0.7340
log(0.68) = −0.3857

log(0.44) = −0.8210
log(0.39) = −0.9416

B_log = (−0.4780 + −0.3425 + −0.5798 + −0.7340 + −0.3857)
        − (−0.8210 + −0.9416)
      = −2.5200 − (−1.7626)
      = −2.5200 + 1.7626
      = −0.7574   (natural log)
```

Note: Using natural log throughout.  The example file reports
`B_neoth_log = -0.7574` and `B_neoth_log_base = "e"`.
Cross-instance pooling requires the same base — use natural log.

## Form 2: B_neoth_mult (Multiplicative — requires calibrated epsilon)

```
B_neoth_mult_raw = (C × K × M) / ((D / A) × (H / V) + ε)
```

```
numerator = 0.62 × 0.71 × 0.56
          = 0.62 × 0.71 = 0.4402
            × 0.56 = 0.2465

buffer_ratio_1 = D / A = 0.44 / 0.48 = 0.9167
buffer_ratio_2 = H / V = 0.39 / 0.68 = 0.5735

denominator = 0.9167 × 0.5735 + ε
            = 0.5257 + ε
```

With ε = 0.01 × median((D/A)×(H/V) over calibration batch) — must be
pre-registered. For this example, ε = null (epsilon not yet calibrated;
`B_neoth_mult = null`).

## Form 3: B_neoth_bottleneck

```
B_bottleneck = min(C, K, M, A, V) / max(D, H)
```

```
numerator_min = min(0.62, 0.71, 0.56, 0.48, 0.68) = 0.48
denominator_max = max(0.44, 0.39) = 0.44

B_bottleneck = 0.48 / 0.44 = 1.0909
```

Range is not bounded to [0,1] because the bottleneck amplifier can exceed the
buffer.  Normalise before comparing across instances.

## Normalization

All forms are normalised within-instance before cross-instance pooling:

```
z(B_log) = (B_log − mean_instance(B_log)) / std_instance(B_log)
```

The raw (unnormalised) score is always stored; the normalised value is derived
at analysis time.
