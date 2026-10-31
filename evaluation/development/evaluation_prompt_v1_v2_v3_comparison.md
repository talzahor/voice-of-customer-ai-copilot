# Gemini Prompt V1 / V2 / V3 Development-Set Comparison

This report compares three prompt versions on the same locked 40-record development set. It is development evidence only; the untouched holdout is reserved for the final evaluation and must not be used to refine Prompt V3.

## Overall metrics

| Version | Theme accuracy | Feedback Type accuracy | Sentiment accuracy | Severity accuracy | Exact-match accuracy | Theme macro F1 | Feedback Type macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline V1 | 97.5% | 85.0% | 82.5% | 92.5% | 67.5% | 86.5% | 80.5% |
| Prompt V2 | 95.0% | 90.0% | 52.5% | 82.5% | 37.5% | 84.3% | 85.0% |
| Prompt V3 | 95.0% | 87.5% | 85.0% | 85.0% | 62.5% | 84.3% | 83.3% |

## Clear vs Ambiguous exact-match results

| Version | Group | Records | Exact matches | Exact-match accuracy |
| --- | --- | --- | --- | --- |
| Baseline V1 | Clear | 32 | 24 | 75.0% |
| Baseline V1 | Ambiguous | 8 | 3 | 37.5% |
| Prompt V2 | Clear | 32 | 13 | 40.6% |
| Prompt V2 | Ambiguous | 8 | 2 | 25.0% |
| Prompt V3 | Clear | 32 | 23 | 71.9% |
| Prompt V3 | Ambiguous | 8 | 2 | 25.0% |

## Field-level changes from Baseline V1 to Prompt V3

| feedback_id | field | ground_truth | V1 | V3 | outcome |
| --- | --- | --- | --- | --- | --- |
| V2F008 | Severity | High | High | Medium | V1-correct field regressed in V3 |
| V2F015 | Feedback Type | Information Need | Process Friction | Information Need | V1 error corrected by V3 |
| V2F023 | Feedback Type | Technical Issue | Technical Issue | Process Friction | V1-correct field regressed in V3 |
| V2F032 | Severity | No Issue | No Issue | Low | V1-correct field regressed in V3 |
| V2F049 | Severity | No Issue | No Issue | Low | V1-correct field regressed in V3 |
| V2F101 | Sentiment | Negative | Neutral | Negative | V1 error corrected by V3 |
| V2F127 | Feedback Type | Process Friction | Technical Issue | Process Friction | V1 error corrected by V3 |
| V2F050 | Theme | Claim Submission & Form | Claim Submission & Form | Document Requirements | V1-correct field regressed in V3 |

## Disposition of fields changed by Prompt V2

| feedback_id | field | V1 | V2 | V3 | disposition |
| --- | --- | --- | --- | --- | --- |
| V2F015 | Feedback Type | Process Friction | Information Need | Information Need | V2 change retained |
| V2F016 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F020 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F043 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F046 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F048 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F048 | Severity | Low | Medium | Low | V2 change rejected |
| V2F055 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F060 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F067 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F108 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F109 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F111 | Severity | Low | No Issue | Low | V2 change rejected |
| V2F117 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F127 | Feedback Type | Technical Issue | Process Friction | Process Friction | V2 change retained |
| V2F127 | Severity | Medium | High | Medium | V2 change rejected |
| V2F136 | Sentiment | Negative | Neutral | Negative | V2 change rejected |
| V2F137 | Feedback Type | Compliment | General Feedback | Compliment | V2 change rejected |
| V2F050 | Theme | Claim Submission & Form | Document Requirements | Document Requirements | V2 change retained |
| V2F075 | Feedback Type | Compliment | General Feedback | Compliment | V2 change rejected |
| V2F075 | Severity | Low | No Issue | Low | V2 change rejected |

## Interpretation constraint

These results describe performance on the development set used for prompt refinement. They must not be treated as an unbiased estimate of final performance. Only the separately locked, untouched holdout can serve that purpose.
