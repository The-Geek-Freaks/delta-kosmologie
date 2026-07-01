# Falsification Standard

Delta Cosmology only becomes scientifically useful where it risks being wrong.

For the Babel Index branch, the key falsification test is simple:

> If the structured Babel feature has no incremental out-of-sample signal after
> controlling for the raw variables, the Babel-ratio structure is falsified for
> that domain.

## Minimum Model Ladder

| Model | Features | Purpose |
| --- | --- | --- |
| `M0` | Size, age, activity, task type, load | Beat trivial operational controls |
| `M1` | Raw `{C,K,M,A,V,D,H}` | Beat the direct ingredients |
| `M2` | Raw features plus regularized interactions | Beat simple learned interactions |
| `M3` | Gradient boosting / random forest | Check that the engineered score is not irrelevant |
| `M4` | `M1 + B_variant` | Test incremental Babel signal |

## Valid Evidence

- out-of-sample AUROC/AUPRC improvement,
- log-loss or Brier-score improvement,
- likelihood-ratio improvement,
- non-zero permutation importance,
- stable bootstrap intervals,
- stable sign and direction across time splits.

## Invalid Evidence

- a single appealing chart,
- post-hoc threshold tuning,
- selecting epsilon after seeing outcomes,
- treating public benchmark saturation as system degradation,
- using NEOTH success as proof of cosmological ontology,
- hiding negative controls.
