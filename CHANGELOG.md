# Changelog

## [Unreleased]

### Changed

- **FINDING-01 (CRITICAL):** Added `docs/foundations.md` — grounds the RDelta
  co-condition as a theorem derivable from the single axiom "distinction requires
  persistence and persistence requires distinction," with failure-mode proof sketch
  and citations to Bateson (1972) and Spencer-Brown (1969). Extended the RDelta
  section in `paper/delta-cosmology-v1.0.md` with a summary of the derivation and
  a reference to the new file. Updated `docs/glossary.md` entry for RDelta.
- **FINDING-02 (HIGH):** Epsilon governance pre-hoc selection rule was already
  fully specified in `protocols/babel-index.md` §Epsilon Governance. Marked the
  corresponding ROADMAP v1.1 item `[x]` to reflect the resolved state and prevent
  duplicate effort.
- **FINDING-03 (HIGH):** Downgraded the cosmological test path row in the
  two-track table (`paper/delta-cosmology-v1.0.md`) to "Planned future work — not
  a current scientific claim." Added a v1.4 cosmological milestone in `ROADMAP.md`
  with the minimum specification requirements for a valid Xi test (dataset,
  parameterization, pre-registered test statistic).
- **FINDING-04 (HIGH):** Added `## K_d Measurement Protocol (NEOTH)` subsection
  to `protocols/babel-index.md` defining the reference algorithm (mean pairwise
  cosine similarity of last w output embeddings), scale (0=diverse, 1=identical),
  null-value rule, reproducibility requirement (declare HuggingFace model ID in
  `algorithm_versions.K_embedding_model`), and an edit-distance fallback proxy.
- **FINDING-05 (MEDIUM):** Replaced the unanchored thermodynamic claim "Local
  order is not thermodynamically free" in `paper/delta-cosmology-v1.0.md` with a
  precise information-theoretic statement connecting resource pressure M_d and
  differentiation capacity D_d, consistent with the Babel formula and falsifiable
  in the NEOTH domain.
- **FINDING-06 (MEDIUM):** Added glossary entries for `Omega`, `Xi`, and
  `Cosmic breath` to `docs/glossary.md`, each stating their status
  (not claimed / undefined-placeholder / informal metaphor) and the conditions
  a valid Xi model would need to meet.
- **FINDING-07 (MEDIUM):** Replaced bare `A_d` and `V_d` numerator terms with
  conditional ratios `A_d / D_d` and `V_d / H_d` in the candidate multiplicative
  formula in both `protocols/babel-index.md` and `paper/delta-cosmology-v1.0.md`.
  Variable table direction rows updated from "Higher can increase Babel risk" to
  explicit conditional language. Log form updated accordingly.
- **FINDING-08 (MEDIUM):** Window schema (`neoth-babel-window.schema.json`) was
  already at v0.2.0 with `collapse_within_30m`, `collapse_at_next_task`, and
  `prediction_horizon_seconds` present. Finding verified resolved in current repo
  state; no changes required.
- **FINDING-09 (MEDIUM):** Added `tool_selection_failure` to the `collapse_label`
  enum in `neoth-babel-event.schema.json` (bumped to v0.1.1) and to both collapse
  kind enums in `neoth-babel-window.schema.json` (bumped to v0.2.1). Rewrote the
  Outcome Labels section in `docs/neoth-integration.md` as a schema-referenced
  table with 8 canonical labels; the schema is now the declared authoritative
  source.

## 1.0.0 - 2026-07-01

- Initial public repository structure.
- Added canonical paper PDF and extracted text.
- Added Babel index protocol.
- Added NEOTH Pilot Protocol B.
- Added NEOTH telemetry event schema and example window.
- Added contribution, security, and issue hygiene files.
