# Falsification Standard

![Claim boundary](https://raw.githubusercontent.com/The-Geek-Freaks/delta-kosmologie/main/assets/claim-boundary.svg)

## Boundary

A NEOTH result can validate the local LLM/agent telemetry instrument. It does
not prove the cosmological interpretation.

## Falsified For A Domain If

- the Babel score has no incremental signal after controlling for raw features,
- signal disappears under time splits,
- signal depends on post-hoc threshold or epsilon tuning,
- one proxy explains the whole effect,
- labels are explainable by simpler local null models,
- performance does not survive out-of-sample evaluation.

## Supported Only If

- cross-validated AUROC/AUPRC or calibration improves,
- likelihood-ratio or nested-model tests improve,
- permutation importance stays above noise,
- bootstrap intervals exclude zero incremental gain,
- direction remains stable across time splits.

## Forbidden Claim

Do not treat a successful NEOTH pilot as proof of cosmological ontology.
