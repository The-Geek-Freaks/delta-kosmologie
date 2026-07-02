# Collapse Label Definitions

Version: 0.1.0 (v0 — pre-registration equivalent)  
Status: DRAFT — freeze commit SHA required; labels MUST NOT change after data collection begins.

Every label is a deterministic computable function of the WAL event stream.
Labels are applied to the primary (15-minute) window.  All functions are
implementable from existing schema fields in `neoth-babel-event.schema.json`.

Any change to these definitions after the freeze date MUST be declared as a
new exploratory analysis, not an update to the primary falsification test.

## Label 1: `agent_loop`

**Detection rule**: `event_type=retry` appears ≥ 3 times with identical
`(tool, agent_id)` tuple within any 60-second sub-window of the session.

**Computable from**: `event_type`, `tool`, `agent_id`, `timestamp` fields.

**Notes**: The identical-tuple requirement distinguishes an agent retry loop
(same action repeated) from a retry storm (many different actions failing).
The 60-second sub-window is a sliding window; the label fires as soon as
the third retry is detected.

## Label 2: `retry_storm`

**Detection rule**: `event_type=retry` events exceed 5 in any 30-second
sub-window across all agents.

**Computable from**: `event_type`, `timestamp` fields.

**Notes**: Unlike `agent_loop`, this label does not require the same
`(tool, agent_id)` tuple — it captures system-wide retry pressure regardless
of the source.  The two labels can co-occur.

## Label 3: `tool_timeout_cascade`

**Detection rule**: `event_type=tool_call_end` with `success=false` and
`error_kind` containing "timeout" (case-insensitive), for more than 3 distinct
`tool` values in the window.

**Computable from**: `event_type`, `success`, `error_kind`, `tool` fields.

**Notes**: A tool that times out once does not trigger this label; the cascade
requires failure across ≥ 4 distinct tools.  Tool-selection errors are tracked
separately by `tool_selection_failure`.

## Label 4: `tool_selection_failure`

**Detection rule**: `event_type=tool_call_end` with `success=false` and
`error_kind` matching one of `wrong_tool`, `invalid_tool`, `inapplicable_tool`,
`tool_schema_mismatch`, `tool_not_allowed`, `permission_denied_for_tool`, or
containing "selection" (case-insensitive).

**Computable from**: `event_type`, `success`, `error_kind`, `tool`,
`agent_id` fields.

**Notes**: This label is distinct from `tool_timeout_cascade`.  It captures
wrong, unavailable, rejected, or inapplicable tool choice before or at the
tool-call boundary.  It can co-occur with `retry_storm`, but should not be
merged with timeout failures unless both error classes are explicitly emitted.

## Label 5: `context_limit_failure`

**Detection rule**: `context_used_ratio >= 0.95` in a `context_boundary` event
followed by an error event with `error_kind` containing "context" or "truncation"
within the same session.

**Computable from**: `event_type`, `context_used_ratio`, `error_kind`,
`session_id` fields.

**Notes**: The ordering requirement (near-limit event precedes the error event)
prevents false positives from unrelated context errors.

## Label 6: `semantic_degradation`

**Detection rule**: K_d (as defined in `feature-extraction-spec.md`,
`K_d_v0`) exceeds 0.90 for 3 or more consecutive 5-minute sub-windows
within the primary 15-minute window.

**Computable from**: the K_d feature series, computed by the window aggregator.

**Notes**: This is the only label that depends on a derived feature (K_d)
rather than raw event fields.  The K_d algorithm version used for detection
MUST match the one reported in the window record.

## Label 7: `fallback_failure`

**Detection rule**: a `fallback_attempt` event is NOT followed by a
`fallback_result` event with `success=true` for the same session within
60 seconds.

**Computable from**: `event_type`, `success`, `session_id`, `timestamp` fields.

**Notes**: This labels the FAILURE of the fallback mechanism, not the mere
occurrence of a fallback attempt.  A successful fallback (attempt followed
by success=true) does not trigger this label.

## Label 8: `objective_failure`

**Detection rule**: a `collapse_label` event with `collapse_label=objective_failure`
is present in the session, OR a manual label is applied via
`neoth babel label <window_id> objective_failure`.

**Computable from**: `event_type`, `collapse_label` fields, or operator action.

**Notes**: This is the only label that requires operator input.  It is
appropriate for longitudinal tasks where success/failure can only be determined
at task completion, not from the event stream alone.

## Negative Controls

Negative controls are windows from sessions where collapse is structurally
impossible.  They must be tagged with `labels.negative_control = true` and
an appropriate `labels.negative_control_type`.

At least 10% of submitted windows from each instance must be
negative-control-tagged windows.

### Negative Control Types

| Type | Description | Expected B_d |
|------|-------------|-------------|
| `synthetic_stable` | Single-agent, single-tool, no-retry, bounded deterministic task | Near minimum of B_d distribution |
| `isolated_run` | Multi-agent but no tool sharing, no fallbacks configured | Low C_d, H_d structural = 1.0 |
| `replay_deterministic` | Exact replay of a known-stable historical session | Below collapse-window B_d |

### Negative Control Falsification Trip-Wire

If B_d on negative-control windows is statistically indistinguishable from
B_d on normal pre-collapse windows (p < 0.05), this is evidence that the
index is detecting a confound (e.g., session length, task type) rather than
Babel dynamics.  The analysis MUST report this result prominently rather than
ignoring the negative controls.
