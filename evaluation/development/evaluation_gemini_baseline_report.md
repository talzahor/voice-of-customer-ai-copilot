# Gemini V2 Blind Baseline Evaluation

## Methodology

- Locked human reference: `evaluation_ground_truth_approved.csv`
- Ground-truth SHA-256: `595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2`
- Gemini model: `gemini-3.5-flash-lite`
- API calls: 1
- Evaluation-set size: 40 records
- The request included only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were schema-constrained and locally validated before being saved or compared with the human reference.
- No prompt refinement or rerun was performed after observing errors.

## Agreement by dimension

| Dimension | Agreement |
| --- | --- |
| Theme | 39/40 (97.5%) |
| Feedback Type | 34/40 (85.0%) |
| Sentiment | 33/40 (82.5%) |
| Severity | 37/40 (92.5%) |

## All-fields exact match

27/40 (67.5%) records matched on all four dimensions.

## Clear vs Ambiguous agreement

| Reference group | Dimension | Agreement |
| --- | --- | --- |
| Clear | Theme | 32/32 (100.0%) |
| Clear | Feedback Type | 27/32 (84.4%) |
| Clear | Sentiment | 29/32 (90.6%) |
| Clear | Severity | 30/32 (93.8%) |
| Ambiguous | Theme | 7/8 (87.5%) |
| Ambiguous | Feedback Type | 7/8 (87.5%) |
| Ambiguous | Sentiment | 4/8 (50.0%) |
| Ambiguous | Severity | 7/8 (87.5%) |

## Theme confusion matrix

Rows are human labels; columns are Gemini predictions.

| Human \ Gemini | Document Requirements | Document Upload | Claim Submission & Form | Claim Status | Reimbursement | Login & Account | Customer Support | General Experience |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Document Requirements | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Document Upload | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claim Submission & Form | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| Claim Status | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| Reimbursement | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 |
| Login & Account | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| Customer Support | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| General Experience | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

## Feedback Type confusion matrix

Rows are human labels; columns are Gemini predictions.

| Human \ Gemini | Process Friction | Technical Issue | Improvement Request | Information Need | Compliment | General Feedback |
| --- | --- | --- | --- | --- | --- | --- |
| Process Friction | 8 | 1 | 0 | 0 | 0 | 1 |
| Technical Issue | 0 | 13 | 0 | 0 | 0 | 0 |
| Improvement Request | 0 | 0 | 4 | 0 | 0 | 0 |
| Information Need | 1 | 0 | 0 | 4 | 0 | 0 |
| Compliment | 0 | 0 | 0 | 0 | 3 | 0 |
| General Feedback | 0 | 0 | 1 | 0 | 2 | 2 |

## Sentiment confusion matrix

Rows are human labels; columns are Gemini predictions.

| Human \ Gemini | Positive | Neutral | Negative |
| --- | --- | --- | --- |
| Positive | 4 | 1 | 0 |
| Neutral | 1 | 5 | 0 |
| Negative | 0 | 5 | 24 |

## Severity confusion matrix

Rows are human labels; columns are Gemini predictions.

| Human \ Gemini | No Issue | Low | Medium | High |
| --- | --- | --- | --- | --- |
| No Issue | 6 | 1 | 0 | 0 |
| Low | 0 | 14 | 0 | 0 |
| Medium | 0 | 0 | 11 | 1 |
| High | 0 | 0 | 1 | 6 |

## Theme per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Document Requirements | 5 | 1.000 | 1.000 | 1.000 |
| Document Upload | 6 | 1.000 | 1.000 | 1.000 |
| Claim Submission & Form | 6 | 0.857 | 1.000 | 0.923 |
| Claim Status | 6 | 1.000 | 1.000 | 1.000 |
| Reimbursement | 5 | 1.000 | 1.000 | 1.000 |
| Login & Account | 5 | 1.000 | 1.000 | 1.000 |
| Customer Support | 6 | 1.000 | 1.000 | 1.000 |
| General Experience | 1 | 0.000 | 0.000 | 0.000 |

Theme macro F1: **0.865**

## Feedback Type per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Process Friction | 10 | 0.889 | 0.800 | 0.842 |
| Technical Issue | 13 | 0.929 | 1.000 | 0.963 |
| Improvement Request | 4 | 0.800 | 1.000 | 0.889 |
| Information Need | 5 | 1.000 | 0.800 | 0.889 |
| Compliment | 3 | 0.600 | 1.000 | 0.750 |
| General Feedback | 5 | 0.667 | 0.400 | 0.500 |

Feedback Type macro F1: **0.805**

## Observed error patterns

- Process Friction vs Information Need: 1 cross-confusion(s).
- Process Friction vs Technical Issue: 1 cross-confusion(s).
- Severity overprediction: 2 record(s).

Detailed mismatches are preserved in `evaluation_gemini_baseline_errors.csv`. Labels were not changed during analysis.

## Limitations

- Dataset V2 is synthetic.
- The 40-record set was deliberately selected for coverage and challenge rather than random representativeness.
- The human reference contains judgement calls, particularly on records marked Ambiguous.
- These metrics describe only this evaluation set and must not be interpreted as production accuracy.
- No customer incidence, business impact, or real-world prevalence can be inferred from this evaluation.
