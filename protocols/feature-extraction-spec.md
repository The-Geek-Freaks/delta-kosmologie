# Feature Extraction Specification

Version: 0.1.0 (v0 reference algorithms)  
Status: DRAFT — freeze commit SHA required before cross-instance pooling begins.

Every feature is labelled with its algorithm version.  Contributors report
`algorithm_versions.{C,K,M,A,V,D,H}` in each window record so between-version
sensitivity analysis is possible.

## C_d — Tool/Agent Coupling Density

**Algorithm**: `C_d_v0`  
**Unit**: dimensionless ratio [0, 1]  
**Valid range**: [0, 1]  
**Aggregation**: computed once per window over all events in the window

Build bipartite graph G = (agents ∪ tools, edges) from co-occurrence of
`0xC0 MCP_TOOL_CALLED` and `0xFC AGENT_DISPATCHED` WAL events within 500 ms
windows of the same session:

```
C_d = |distinct (agent, tool) edges| / (|agents| * |tools|)
```

Special case — single agent:
```
C_d = |distinct tools called| / total_tools_available
```

where `total_tools_available` is the count of distinct tools exposed by all
active MCP servers during the window.

**Baseline**: C_d = 0.0 when no tool calls occurred.

## K_d — Semantic Convergence Pressure

**Algorithm**: `K_d_v0`  
**Unit**: dimensionless [0, 1]  
**Valid range**: [0, 1] (0 = maximum diversity, 1 = all outputs identical)  
**Aggregation**: mean pairwise cosine similarity over the window

Compute token-frequency histograms for each LLM response in the window
(token IDs hashed to 32-bit integers for compactness).  K_d = mean pairwise
cosine similarity of all histogram pairs.

Minimum 3 responses required; return 0.0 (maximum diversity) otherwise.

**v0 fallback**: BLEU-2 overlap when histograms are unavailable.  Report
algorithm version as `K_d_v0_bleu2` when using the fallback.

**k_d_embedding_model**: when a sentence-transformer model is available,
report the HuggingFace model ID in the window's
`algorithm_versions.K_embedding_model` field.  The v0 reference uses no
external embedding model.

## M_d — Resource / Context Pressure

**Algorithm**: `M_d_v0`  
**Unit**: dimensionless [0, 1]  
**Valid range**: [0, 1]  
**Aggregation**: max over the window

```
M_d = max(context_used_ratio, vram_pct / 100.0, budget_consumed_ratio)
```

Sources:
- `context_used_ratio`: from `0x20 LLM_REQUEST` WAL events.
- `vram_pct`: from `0x47` GPU memory events (0.0 when no GPU is active).
- `budget_consumed_ratio = (cap - remaining) / cap`: from `0x2F BUDGET_UPDATE`.

Using `max` rather than `mean`: M_d should fire when ANY resource is exhausted,
not only when average pressure is high.

## A_d — Autonomous Agent Density

**Algorithm**: `A_d_v0`  
**Unit**: dimensionless [0, 1]  
**Valid range**: [0, 1]  
**Aggregation**: computed once per window

```
A_d = count(distinct agent_id in AGENT_DISPATCHED events) / autonomy_scalar / 8.0
```
clamped to [0, 1].

`autonomy_scalar`: Strict=1, Standard=2, Elevated=3, Full=4 from AutonomyLevel.

This separates A_d from V_d (`tokens_per_sec`): A_d counts autonomous actors
normalised by the permission level; V_d counts the information throughput.

## V_d — Information Velocity

**Algorithm**: `V_d_v0`  
**Unit**: dimensionless [0, 1]  
**Valid range**: [0, 1]  
**Aggregation**: snapshot at window close

```
V_d = tokens_per_sec() / V_MAX
```
clamped to [0, 1].

`V_MAX` = p99 of `tokens_per_sec` over the past 7 days from `idx_babel_norm`.  
Cold-start default: `v_max_default = 150.0` tokens/sec (configurable in
`FreedomConfig :: babel.v_max_default`).

Source: `cluster::local_load::tokens_per_sec()` (existing EWMA gauge).

## D_d — Differentiation Capacity

**Algorithm**: `D_d_v0`  
**Unit**: dimensionless (0, 1]  
**Valid range**: (0, 1] — must be strictly positive (schema: `exclusiveMinimum: 0`)  
**Aggregation**: computed once per window

v0 proxy: binary flag for "any tool schema conflict detected in window".

```
D_d = 1.0   (no schema conflicts)
D_d = 0.3   (one or more schema conflicts detected)
```

A schema conflict is defined as: two or more active MCP tools share a required
parameter name but declare incompatible types for it.

**v1 target**: Jensen–Shannon divergence between the token-frequency distributions
of distinct tool schemas active in the window.

## H_d — Heterarchy / Redundancy

**Algorithm**: `H_d_v0`  
**Unit**: dimensionless (0, 1] — must be strictly positive  
**Valid range**: (0, 1]  
**Aggregation**: computed once per window

H_d is split into two sub-components; `H_structural` is used as the primary
B_d input; `H_empirical` is a calibration check when fallback data is available.

**H_structural (primary)**: routes to alternative provider/tool paths that
exist in the router configuration, regardless of whether they were exercised.
```
H_structural = (count distinct non-overlapping fallback routes in config) /
               (count primary routes + 1)
```
Range (0, 1], with 1.0 meaning "at least as many fallback routes as primary".

**H_empirical (calibration only)**:
```
H_empirical = count(distinct successful fallback routes in window) /
              (count(distinct sole-path endpoints in window) + 1)
```
Default: 1.0 when no fallback attempts were made (neutral — absence of observed
fallback attempts does not imply absence of redundancy).

Report which sub-component was used in `algorithm_versions.H`.

## Cross-Instance Comparability

Before pooling across instances, each raw feature {C,K,M,A,V,D,H} is
z-scored within each instance.  B_d is not pooled in its normalised form;
only raw features are pooled and the score is re-derived from the pooled
normalised features.

The exception is `B_log` (the log form): because it is additively constructed
from per-instance z-scored features, it is directly poolable without a
separate normalisation pass.
