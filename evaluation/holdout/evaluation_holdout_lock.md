# Holdout Evaluation Lock

## Approval record

- Approval date: 2026-10-05
- Approved records: 24
- IDs: `HOLD001` through `HOLD024`
- Approved artifact: `evaluation_holdout_ground_truth_approved.csv`
- Combined source-field SHA-256: `d51c2981b13a496308332a66750eb7180def071bc4be4d7937bbe9cd51a36b8f`
- Approved-file SHA-256: `a4e4f05216afab3c44768e00db81054807ad5f52ed742a940ed3bbe8ab557bab`

The candidate set underwent human review before approval. The approved CSV preserves the reviewed feedback IDs, text, channels, journey stages, labels, and ambiguity flags exactly.

## Human-review corrections incorporated before locking

- `HOLD011` Feedback Type: Technical Issue → Process Friction
- `HOLD015` Sentiment: Positive → Neutral
- `HOLD023` Feedback Type: General Feedback → Compliment

No other approved label changed during the final candidate correction.

## Final distributions

### Theme

| Theme | Count |
| --- | ---: |
| Document Requirements | 3 |
| Document Upload | 3 |
| Claim Submission & Form | 3 |
| Claim Status | 3 |
| Reimbursement | 3 |
| Login & Account | 3 |
| Customer Support | 3 |
| General Experience | 3 |

### Feedback Type

| Feedback Type | Count |
| --- | ---: |
| Improvement Request | 6 |
| Process Friction | 5 |
| Technical Issue | 5 |
| Information Need | 3 |
| Compliment | 3 |
| General Feedback | 2 |

### Sentiment

| Sentiment | Count |
| --- | ---: |
| Neutral | 12 |
| Negative | 9 |
| Positive | 3 |

### Severity

| Severity | Count |
| --- | ---: |
| No Issue | 10 |
| Low | 6 |
| Medium | 6 |
| High | 2 |

### Ambiguity

| Review status | Count |
| --- | ---: |
| Clear | 18 |
| Ambiguous | 6 |

## Experimental protection

- Prompt V3 did not exist when the holdout was created, human-reviewed, and locked.
- No Gemini or other model prediction had been generated for these 24 records before locking.
- The holdout must not be used to design, tune, or refine Prompt V3.
- The approved holdout inputs and labels must remain unchanged until final evaluation.
- Future holdout evaluation scripts must verify the approved-file SHA-256 before running.
- Any later human revision must be explicitly documented as a new version; the locked artifact must not be silently overwritten.
