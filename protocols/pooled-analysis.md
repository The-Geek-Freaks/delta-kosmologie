# Pooled Analysis Protocol

Version: 0.1.0  
Status: DRAFT

## Purpose

Specify how raw window records from different NEOTH instances (and future
registered runtimes) are combined into a joint dataset for testing the
delta-kosmologie theorem.

## Minimum Dataset Requirements

Before any cross-instance claim may be made:

- At least 3 independent operator instances with non-overlapping calendar time.
- At least 30 positive-label (collapse) windows per instance.
- At least 500 total windows per instance (or instance is classified as
  "low-event" and excluded from primary falsification — retained for negative
  control reference).
- At least 10% of each instance's submission must be non-collapse windows
  (enforced by the sampling rule in `distributed-collection.md`).

## Normalization Rule

Within each instance, z-score each raw feature before pooling:

```
z(feature_x, instance_i) = (x - mean_i(x)) / (std_i(x) + 1e-9)
```

This z-scoring is applied to raw {C, K, M, A, V, D, H} values.

B_d in its ratio/multiplicative form is NOT pooled directly.  The log form
`B_log` is the exception: because it is additive over z-scored features it
is poolable without a separate normalisation step.

## Meta-Analysis Tier (Primary)

Rather than pooling raw records, combine per-instance AUROC estimates using
DerSimonian–Laird random-effects meta-analysis.  This avoids pseudo-replication
from correlated within-instance windows.

Steps:
1. Run M0–M4 model ladder within each instance separately.
2. Compute per-instance AUROC (with bootstrap confidence interval).
3. Combine per-instance AUROC estimates via DL random-effects.
4. Report the pooled AUROC with 95% CI.
5. Report I² statistic.

## Heterogeneity Test

If I² > 50%, the pooled estimate is NOT the primary result.  Instead report:
- Subgroup breakdown by `deployment_context`.
- Subgroup breakdown by `primary_model_family`.
- A statement that cross-instance heterogeneity is too large for a single
  pooled estimate to be meaningful.

## Data Manifest

Each contributing instance must submit a manifest entry to
`manifests/pool-manifest.json` (via PR) listing:

```json
{
  "contributor_id": "<64-char hex>",
  "submission_date_range": {"start": "2026-07-01", "end": "2026-09-01"},
  "window_count": 1200,
  "collapse_event_count": 87,
  "deployment_context": "single-user",
  "primary_model_family": "anthropic/claude-3",
  "normalization_parameters": {
    "C_mean": 0.41, "C_std": 0.18,
    "K_mean": 0.55, "K_std": 0.21
  }
}
```

## Joint Model Specification

The primary confirmatory model for cross-instance pooled analysis is:

```
logit(P(collapse_within_30m)) ~
    B_log                        # primary Babel predictor (log form, poolable)
  + deployment_context           # fixed covariate
  + primary_model_family         # fixed covariate
  + (1 | contributor_id)         # random effect per instance
```

This is a mixed-effects logistic regression.  The sign constraint on B_log
(positive coefficient expected if the hypothesis holds) is specified in the
pre-registration document before the analysis runs.

## Leave-One-Instance-Out Validation

The primary test split is leave-one-instance-out (LOIO) cross-validation.
Report AUROC for each left-out instance and the mean LOIO AUROC.

## Domain Firewall

B_d values from different domains (NEOTH LLM agent, OSS ecosystem, market,
epoch) MUST NOT be pooled without a published calibration function.  Score keys
are prefixed with the domain: `B_neoth_log`, `B_neoth_mult`, not `B_log`.
Comparing `B_neoth_*` to `B_oss_*` without calibration constitutes invalid
evidence.
