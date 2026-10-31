# Gemini Prompt V2 Evaluation

## Methodology

- Locked human reference SHA-256: `595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2`
- Model: `gemini-3.5-flash-lite`
- Evaluation-set size: 40
- API calls: 1
- Prompt version: `evaluation_prompt_v2.md`
- Gemini received only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were validated and saved before comparison with human labels.

## Agreement by dimension

| Dimension | Agreement |
| --- | --- |
| Theme | 38/40 (95.0%) |
| Feedback Type | 36/40 (90.0%) |
| Sentiment | 21/40 (52.5%) |
| Severity | 33/40 (82.5%) |

## All-fields exact match

15/40 (37.5%)

## Clear vs Ambiguous agreement

| Reference group | Dimension | Agreement |
| --- | --- | --- |
| Clear | Theme | 31/32 (96.9%) |
| Clear | Feedback Type | 29/32 (90.6%) |
| Clear | Sentiment | 19/32 (59.4%) |
| Clear | Severity | 27/32 (84.4%) |
| Ambiguous | Theme | 7/8 (87.5%) |
| Ambiguous | Feedback Type | 7/8 (87.5%) |
| Ambiguous | Sentiment | 2/8 (25.0%) |
| Ambiguous | Severity | 6/8 (75.0%) |

## Theme confusion matrix

| Human \ Gemini | Document Requirements | Document Upload | Claim Submission & Form | Claim Status | Reimbursement | Login & Account | Customer Support | General Experience |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Document Requirements | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Document Upload | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Claim Submission & Form | 1 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| Claim Status | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| Reimbursement | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 |
| Login & Account | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| Customer Support | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| General Experience | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

## Feedback Type confusion matrix

| Human \ Gemini | Process Friction | Technical Issue | Improvement Request | Information Need | Compliment | General Feedback |
| --- | --- | --- | --- | --- | --- | --- |
| Process Friction | 9 | 0 | 0 | 0 | 0 | 1 |
| Technical Issue | 0 | 13 | 0 | 0 | 0 | 0 |
| Improvement Request | 0 | 0 | 4 | 0 | 0 | 0 |
| Information Need | 0 | 0 | 0 | 5 | 0 | 0 |
| Compliment | 0 | 0 | 0 | 0 | 2 | 1 |
| General Feedback | 0 | 0 | 1 | 0 | 1 | 3 |

## Sentiment confusion matrix

| Human \ Gemini | Positive | Neutral | Negative |
| --- | --- | --- | --- |
| Positive | 4 | 1 | 0 |
| Neutral | 1 | 5 | 0 |
| Negative | 0 | 17 | 12 |

## Severity confusion matrix

| Human \ Gemini | No Issue | Low | Medium | High |
| --- | --- | --- | --- | --- |
| No Issue | 6 | 1 | 0 | 0 |
| Low | 2 | 11 | 1 | 0 |
| Medium | 0 | 0 | 10 | 2 |
| High | 0 | 0 | 1 | 6 |

## Theme per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Document Requirements | 5 | 0.833 | 1.000 | 0.909 |
| Document Upload | 6 | 1.000 | 1.000 | 1.000 |
| Claim Submission & Form | 6 | 0.833 | 0.833 | 0.833 |
| Claim Status | 6 | 1.000 | 1.000 | 1.000 |
| Reimbursement | 5 | 1.000 | 1.000 | 1.000 |
| Login & Account | 5 | 1.000 | 1.000 | 1.000 |
| Customer Support | 6 | 1.000 | 1.000 | 1.000 |
| General Experience | 1 | 0.000 | 0.000 | 0.000 |

Theme macro F1: **0.843**

## Feedback Type per-class metrics

| Class | Support | Precision | Recall | F1 |
| --- | --- | --- | --- | --- |
| Process Friction | 10 | 1.000 | 0.900 | 0.947 |
| Technical Issue | 13 | 1.000 | 1.000 | 1.000 |
| Improvement Request | 4 | 0.800 | 1.000 | 0.889 |
| Information Need | 5 | 1.000 | 1.000 | 1.000 |
| Compliment | 3 | 0.667 | 0.667 | 0.667 |
| General Feedback | 5 | 0.600 | 0.600 | 0.600 |

Feedback Type macro F1: **0.850**

## Observed error patterns

- Severity overprediction: 4 record(s).

Detailed mismatches are preserved in `evaluation_gemini_prompt_v2_errors.csv`.

## Methodological caution and limitations

- This is iterative prompt development using the same 40 records that informed Prompt V2. Improvement must not be interpreted as unbiased generalization performance.
- A separate untouched holdout set is required for any final generalization claim.
- Dataset V2 is synthetic.
- The evaluation set was deliberately selected for coverage and challenge, not production representativeness.
- The human reference contains judgement calls, especially on Ambiguous examples.
- No customer incidence, business impact, or real-world prevalence can be inferred.
