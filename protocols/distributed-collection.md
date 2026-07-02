# Distributed Collection Protocol

Version: 0.1.0  
Status: DRAFT — not yet frozen. Freeze commit SHA must be added before data collection begins.

## Purpose

This document specifies how NEOTH instances (single-operator clusters and
stranger instances) submit anonymised Babel-Index telemetry windows to the
delta-kosmologie shared research pool for joint testing of the delta-kosmologie
theorem.

## Transport

**Primary**: iroh QUIC dial-by-key transport.

The delta-kosmologie aggregation node publishes a stable `EndpointAddr` in
`metadata/aggregation-node.yml`.  Any NEOTH instance with `cluster-iroh`
enabled dials this address using ALPN `delta-kosmologie/babel-federation/0.1`.

**Fallback**: if iroh is unavailable, batch files accumulate on disk as
`~/.neoth/babel/pending/<batch_id>.jsonl.gz` and can be submitted manually
via the GitHub Issues upload template at
`.github/ISSUE_TEMPLATE/neoth_pilot.md`.

## Wire Format

One submission = one gzip-compressed JSONL file, one window record per line.
Each line is a valid `babel-federation-window/0.2.0` JSON object (a superset
of the existing `neoth-babel-window.schema.json` with federation fields added).

### Required HTTP-equivalent headers (encoded as the first JSON line)

```json
{
  "type": "batch_header",
  "schema_version": "neoth-federation/0.1.0",
  "runtime_version": "<semver>",
  "contributor_id": "<64-char hex SHA-256>",
  "batch_id": "<UUID v4>",
  "window_count": 42,
  "signature_hex": "<Ed25519 signature over SHA-256(compressed_batch_bytes)>",
  "signer_fingerprint": "<first 16 hex chars of Ed25519 pubkey SHA-256>"
}
```

### Window record fields (delta over `neoth-babel-window.schema.json`)

Added fields (all optional for backward compat in v0.1, required in v0.2):

| Field | Type | Description |
|-------|------|-------------|
| `contributor_id` | string — 64-char hex | SHA-256(local_secret_salt \|\| repo_slug). Pseudonymous, stable. |
| `submission_metadata.deployment_context` | enum | `single-user`, `multi-user`, `ci`, `benchmark` |
| `submission_metadata.hardware_tier` | enum | `laptop`, `workstation`, `server`, `cloud-small`, `cloud-large` |
| `submission_metadata.primary_model_family` | string | Provider+family: `anthropic/claude-3` |
| `submission_metadata.avg_tasks_per_day_bucket` | integer | Bucketed task count |
| `submission_metadata.protocol_version` | string const | `neoth-federation/0.1.0` |
| `submission_metadata.runtime_class` | string | `llm-agent-orchestrator` |
| `algorithm_versions` | object | Per-feature algorithm id (`C_d_v0`, etc.) |
| `labels.collapse_within_30m` | boolean or null | Secondary 30-minute horizon label |
| `labels.collapse_at_next_task` | boolean or null | Next-task-run horizon label |
| `labels.negative_control` | boolean | True for deliberately stable runs |
| `labels.negative_control_type` | string or null | `synthetic_stable`, `isolated_run`, `replay_deterministic` |
| `pseudonymised_session_id` | string — 16 hex | HMAC-SHA256(salt, session_id) truncated |

### Submission receipt (aggregation node reply)

```json
{
  "batch_id": "<UUID v4>",
  "accepted_count": 40,
  "rejected_count": 2,
  "rejection_reasons": ["window_too_short", "schema_validation_failed"],
  "suspicious_count": 1
}
```

## Contributor ID Derivation

```
contributor_id = SHA-256(local_secret_salt || "\0" || repo_slug)
```

- `local_secret_salt`: 32 bytes of random data generated at first launch,
  stored at `~/.neoth/babel/contributor.salt` (mode 600, never exported).
- `repo_slug`: `The-Geek-Freaks/NEOTH` (or the equivalent for other runtimes).

The contributor ID is stable across submissions from the same installation
(enables per-instance random effects in the mixed-effects model) but cannot
be linked to operator identity without the salt.

## Rate Limits

- Maximum 1 batch per 5 minutes per contributor_id.
- Maximum 500 windows per batch.
- Batches larger than 10 MB compressed are rejected.

## Consent Requirements

Before a NEOTH instance may submit, all of the following must be true:

1. `freedom.yaml :: babel.federate = true` (explicit opt-in).
2. `AutonomyLevel >= Elevated` (level 3, set at operator onboarding).
3. At least 50 calibration windows have been generated locally (epsilon frozen).
4. The submission is a random sample: minimum 10% of all windows, with
   non-collapse windows numbering at least as many as collapse windows.

Withdrawing consent (`babel.federate = false`) immediately stops submissions.
Already-submitted pseudonymous records cannot be recalled.

## New Runtime Registration

A runtime other than NEOTH wishing to contribute must:

1. Open a PR adding an entry to `metadata/registered-runtimes.yml`.
2. Document the feature extraction method for each of C, K, M, A, V, D, H.
3. Use a runtime-specific ALPN suffix: `delta-kosmologie/babel-federation/0.1/<runtime_id>`.
4. Name event schemas as `<runtime>-babel-event.schema.json` (the universal
   window schema `babel-federation-window.schema.json` applies unchanged).
