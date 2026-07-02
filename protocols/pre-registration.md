# Pre-Registration Protocol

Version: 0.1.0  
Status: DRAFT

## Purpose

Implement a lightweight pre-registration equivalent that prevents post-hoc
adaptation of the analysis plan to the data.  All confirmatory tests must be
specified BEFORE the contributor accesses the pooled dataset or their own
collapse labels.

## Mechanism

Pre-registration documents are committed to the branch `preregistrations/` in
this repository.  The Git commit SHA is the timestamp; the commit date is the
freeze date.

No analysis accessing pooled outcome labels may begin before the contributor's
pre-registration commit has been merged or recorded.

## Pre-Registration Template

File: `templates/preregistration.md` in this repository.

Required sections:

1. **Prediction horizon**: e.g., `collapse_within_30m` (primary), `collapse_within_5m` (secondary).
2. **Window granularity**: e.g., 15-minute primary, 5-minute secondary.
3. **Collapse labels**: which of the 7 defined labels are included in the outcome.
4. **Normalization method**: z-score within-instance (required) + any additional.
5. **Epsilon governance rule**: log form (recommended) or `0.01_median_buffer_ratio_calibration` (multiplicative).
6. **K_d measurement algorithm**: `K_d_v0` or `K_d_v0_bleu2` (fallback).
7. **H_d sub-component**: `H_structural` (required primary) or `H_empirical`.
8. **M0 covariates**: list of baseline controls.
9. **M1–M4 model specifications**: feature sets and estimation method.
10. **Primary falsification criterion**: e.g., "AUROC improvement > 0.03 with Bonferroni correction".
11. **Minimum dataset size**: must meet the requirements in `pooled-analysis.md`.
12. **Holdout regime**: LOIO cross-validation (required); time split (optional secondary).

## Registry

All registered pre-registrations are listed in `protocols/pre-registration-registry.md`
with the commit SHA, freeze date, and analysis start date.

## Verification

Any reader can verify a pre-registration by running:
```
git show <commit-sha>
```
and comparing the frozen specification to the published analysis report.

Deviations from the frozen specification MUST be labelled "exploratory" and
reported separately from the confirmatory results.

## Protocol Freeze Checklist

Before data collection begins, a Git Release tag `protocol-freeze-v1.0` must
be created from a commit where ALL of the following are specified and consistent
across the three documents:

- [ ] Normalization method (this file + `babel-index.md`)
- [ ] Epsilon value or log-form decision (this file + `babel-index.md`)
- [ ] K_d measurement algorithm (`feature-extraction-spec.md`)
- [ ] D_d measurement algorithm (`feature-extraction-spec.md`)
- [ ] H_d aggregation rule (`feature-extraction-spec.md`)
- [ ] Collapse label detection functions (`collapse-label-definitions.md`)
- [ ] Model comparison specifications (this file)
- [ ] Minimum dataset size (`pooled-analysis.md`)
- [ ] Holdout regime (this file)

The SHA of that commit becomes the canonical protocol reference cited in all
publications.
