# Final Gemini Holdout Evaluation

## Methodology

- Final candidate: frozen Baseline V1
- Model: `gemini-3.5-flash-lite`
- Holdout records: 24
- API calls: 1
- Approved holdout SHA-256: `a4e4f05216afab3c44768e00db81054807ad5f52ed742a940ed3bbe8ab557bab`
- Frozen V1 instructions SHA-256: `e8d09795f14e9acd79d01d046e2b796d92f4b402858b9fda651d980cefbf6619`
- Gemini received only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were schema-constrained, strictly validated, and saved before comparison with human labels.

The 40-record development set was used during prompt analysis and iteration, so its results are not unbiased generalization estimates. This 24-record holdout was locked before final-candidate selection and was not used for prompt refinement; it provides this project's final unseen-data evaluation.

## Accuracy by dimension

| Dimension | Correct | Accuracy |
| --- | --- | --- |
| Theme | 24 | 100.0% |
| Feedback Type | 20 | 83.3% |
| Sentiment | 21 | 87.5% |
| Severity | 14 | 58.3% |

## All-fields exact match

11/24 (45.8%)

## Clear vs Ambiguous exact match

| Reference group | Records | Exact matches | Exact-match accuracy |
| --- | --- | --- | --- |
| Clear | 18 | 10 | 0.5555555555555556 |
| Ambiguous | 6 | 1 | 0.16666666666666666 |

## Theme confusion matrix

| Human \ Gemini | Document Requirements | Document Upload | Claim Submission & Form | Claim Status | Reimbursement | Login & Account | Customer Support | General Experience |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Document Requirements | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Document Upload | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claim Submission & Form | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| Claim Status | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| Reimbursement | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| Login & Account | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 |
| Customer Support | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| General Experience | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

## Feedback Type confusion matrix

| Human \ Gemini | Process Friction | Technical Issue | Improvement Request | Information Need | Compliment | General Feedback |
| --- | --- | --- | --- | --- | --- | --- |
| Process Friction | 3 | 2 | 0 | 0 | 0 | 0 |
| Technical Issue | 0 | 5 | 0 | 0 | 0 | 0 |
| Improvement Request | 0 | 0 | 6 | 0 | 0 | 0 |
| Information Need | 0 | 0 | 0 | 3 | 0 | 0 |
| Compliment | 0 | 0 | 0 | 0 | 3 | 0 |
| General Feedback | 1 | 0 | 0 | 0 | 1 | 0 |

## Sentiment confusion matrix

| Human \ Gemini | Positive | Neutral | Negative |
| --- | --- | --- | --- |
| Positive | 3 | 0 | 0 |
| Neutral | 1 | 9 | 2 |
| Negative | 0 | 0 | 9 |

## Severity confusion matrix

| Human \ Gemini | No Issue | Low | Medium | High |
| --- | --- | --- | --- | --- |
| No Issue | 3 | 7 | 0 | 0 |
| Low | 1 | 3 | 2 | 0 |
| Medium | 0 | 0 | 6 | 0 |
| High | 0 | 0 | 0 | 2 |

## Theme per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Document Requirements | 3 | 1.000 | 1.000 | 1.000 |
| Document Upload | 3 | 1.000 | 1.000 | 1.000 |
| Claim Submission & Form | 3 | 1.000 | 1.000 | 1.000 |
| Claim Status | 3 | 1.000 | 1.000 | 1.000 |
| Reimbursement | 3 | 1.000 | 1.000 | 1.000 |
| Login & Account | 3 | 1.000 | 1.000 | 1.000 |
| Customer Support | 3 | 1.000 | 1.000 | 1.000 |
| General Experience | 3 | 1.000 | 1.000 | 1.000 |

Theme macro F1: **1.000**

## Feedback Type per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Process Friction | 5 | 0.750 | 0.600 | 0.667 |
| Technical Issue | 5 | 0.714 | 1.000 | 0.833 |
| Improvement Request | 6 | 1.000 | 1.000 | 1.000 |
| Information Need | 3 | 1.000 | 1.000 | 1.000 |
| Compliment | 3 | 0.750 | 1.000 | 0.857 |
| General Feedback | 2 | 0.000 | 0.000 | 0.000 |

Feedback Type macro F1: **0.726**

## Observed error patterns

- Process Friction vs Technical Issue: 2 cross-confusion(s).
- Neutral classified as Negative: 2 record(s).
- Severity overprediction: 9 record(s).

The mismatch artifact lists individual disagreements descriptively. Human labels were not changed.

## Limitations

- Dataset V2 is synthetic.
- The holdout contains only 24 records and was designed for taxonomy coverage rather than real-world prevalence.
- Some human labels involve judgment, including records marked Ambiguous.
- These metrics must not be interpreted as production accuracy or evidence that the system is production-ready.
- No customer incidence, causation, business impact, or real-world prevalence can be inferred.

## No post-holdout optimization

The holdout results must not be used to modify Baseline V1 and rerun this same holdout as though it remained unseen. Any future prompt or model improvement requires a new untouched test set for another unbiased evaluation.
