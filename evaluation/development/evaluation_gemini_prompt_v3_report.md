# Gemini Prompt V3 Development Evaluation

## Methodology

- Locked development reference SHA-256: `595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2`
- Model: `gemini-3.5-flash-lite`
- Development-set size: 40
- API calls: 1
- Prompt version: `evaluation_prompt_v3.md`
- Gemini received only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were validated and saved before comparison with human labels.

## Agreement by dimension

| Dimension | Agreement |
| --- | --- |
| Theme | 38/40 (95.0%) |
| Feedback Type | 35/40 (87.5%) |
| Sentiment | 34/40 (85.0%) |
| Severity | 34/40 (85.0%) |

## All-fields exact match

25/40 (62.5%)

## Clear vs Ambiguous agreement

| Reference group | Dimension | Agreement |
| --- | --- | --- |
| Clear | Theme | 31/32 (96.9%) |
| Clear | Feedback Type | 29/32 (90.6%) |
| Clear | Sentiment | 30/32 (93.8%) |
| Clear | Severity | 27/32 (84.4%) |
| Ambiguous | Theme | 7/8 (87.5%) |
| Ambiguous | Feedback Type | 6/8 (75.0%) |
| Ambiguous | Sentiment | 4/8 (50.0%) |
| Ambiguous | Severity | 7/8 (87.5%) |

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
| Technical Issue | 1 | 12 | 0 | 0 | 0 | 0 |
| Improvement Request | 0 | 0 | 4 | 0 | 0 | 0 |
| Information Need | 0 | 0 | 0 | 5 | 0 | 0 |
| Compliment | 0 | 0 | 0 | 0 | 3 | 0 |
| General Feedback | 0 | 0 | 1 | 0 | 2 | 2 |

## Sentiment confusion matrix

| Human \ Gemini | Positive | Neutral | Negative |
| --- | --- | --- | --- |
| Positive | 4 | 1 | 0 |
| Neutral | 1 | 5 | 0 |
| Negative | 0 | 4 | 25 |

## Severity confusion matrix

| Human \ Gemini | No Issue | Low | Medium | High |
| --- | --- | --- | --- | --- |
| No Issue | 4 | 3 | 0 | 0 |
| Low | 0 | 14 | 0 | 0 |
| Medium | 0 | 0 | 11 | 1 |
| High | 0 | 0 | 2 | 5 |

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
| Process Friction | 10 | 0.900 | 0.900 | 0.900 |
| Technical Issue | 13 | 1.000 | 0.923 | 0.960 |
| Improvement Request | 4 | 0.800 | 1.000 | 0.889 |
| Information Need | 5 | 1.000 | 1.000 | 1.000 |
| Compliment | 3 | 0.600 | 1.000 | 0.750 |
| General Feedback | 5 | 0.667 | 0.400 | 0.500 |

Feedback Type macro F1: **0.833**

## Observed error patterns

- Process Friction vs Technical Issue: 1 cross-confusion(s).
- Severity overprediction: 4 record(s).

Detailed mismatches are preserved in `evaluation_gemini_prompt_v3_errors.csv`.

## Interpretation caution

- These 40 records are a development evaluation set that informed Prompt V3.
- Results are not an unbiased final estimate of generalization.
- The separate locked holdout is reserved for one final evaluation after Prompt V3 is frozen.
- Dataset V2 is synthetic and the development set was selected for coverage and challenge.
