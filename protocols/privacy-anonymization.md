# Privacy and Anonymisation Protocol

Version: 0.1.0  
Status: DRAFT

## Purpose

Specify which fields MUST be pseudonymised or coarsened before a Babel-Index
window record is submitted to the research pool, and the implementation
reference for the transforms.

## Mandatory Pseudonymisation (HMAC-SHA256 truncated to 16 hex chars)

Apply `HMAC-SHA256(local_secret_salt, original_id)[0..8].to_hex()` to:

- `run_id`
- `session_id`
- `agent_id`
- `task_id`
- `window.id` (the local window UUID)

The truncation to 64 bits is sufficient for within-dataset de-duplication and
too short to reverse the HMAC given a reasonable salt.

## Mandatory Coarsening

| Original field | Coarsened form | Rule |
|----------------|---------------|------|
| `system.repo` | `{owner}/{repo}` slug | Strip scheme and host; keep only first two path segments after the host |
| `model` | `{provider}/{family}` | e.g., `anthropic/claude-3`. Strip any date or version suffix. |

## Fields That Must Not Appear in Submissions

- Raw prompt text, system prompts, or any LLM response content.
- API keys, tokens, or credential fragments.
- Operator names, user IDs, or email addresses.
- File system paths beyond the repo slug.
- IP addresses or hostname strings.
- Full model version strings (e.g., `claude-3-5-sonnet-20241022`).

## Minimum Window Duration

Windows shorter than 60 seconds MUST NOT be submitted.  Reason: short windows
can be re-identified by an adversary who observes task timing from another
side channel.

## Metrics Key Allow-List

The `metrics` object in window records may only contain keys from the
pre-approved list.  Any other key is silently dropped before submission.

Approved keys:
- `tokens_in_total`
- `tokens_out_total`
- `tool_calls_total`
- `fallback_attempts_total`
- `retry_events_total`
- `agent_dispatches_total`
- `context_used_ratio_max`
- `latency_ms_p99`

## Data Retention at the Aggregation Node

- Raw window records are retained for 90 days.
- After 90 days only aggregated statistics are kept (per-contributor AUROC,
  per-deployment-context feature distributions).
- Contributor IDs are retained indefinitely (needed for random-effects model).
- No PII is present in any schema field by design.

## GDPR Compliance Note

No personal data is collected by the schema design:

- Contributor IDs are pseudonyms derived from a local salt; the aggregation
  node holds only the derived ID, not the salt.
- No text content, no user identifiers, no location data.
- The local salt at `~/.neoth/babel/contributor.salt` is data the operator
  controls entirely and can delete at any time.

## Reference Implementation

`SRC/neothd/src/analytics/babel/anonymize.rs` in the NEOTH repository
implements all transforms defined here.  The functions `pseudonymise_id`,
`normalise_repo_slug`, `coarsen_model`, and `filter_metrics` are the
canonical v0 implementations.
