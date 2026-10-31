# Final Candidate Lock

## Selection record

- Selection date: 2026-10-05 (Asia/Jerusalem)
- Selected prompt: Baseline V1
- Model: `gemini-3.5-flash-lite`
- Development set: locked 40-record development evaluation
- Selection timing: completed before any model predictions were generated for the locked holdout

Prompt V2 and Prompt V3 remain experimental development iterations. They are not the selected final candidate and must not be used by the final holdout evaluator.

## Development-set results used for selection

| Metric | Baseline V1 | Prompt V3 |
| --- | ---: | ---: |
| Theme accuracy | 97.5% | 95.0% |
| Feedback Type accuracy | 85.0% | 87.5% |
| Sentiment accuracy | 82.5% | 85.0% |
| Severity accuracy | 92.5% | 85.0% |
| All-fields exact-match accuracy | 67.5% | 62.5% |
| Theme macro F1 | 86.5% | 84.3% |
| Feedback Type macro F1 | 80.5% | 83.3% |

Prompt V3 improved Feedback Type and Sentiment performance on the development set, but introduced regressions—particularly in Severity—and reduced all-fields exact-match accuracy. Baseline V1 was selected because it provides the stronger overall trade-off across the four classification dimensions.

The 40-record set is now a development set: it was used during prompt analysis and iteration, so these metrics are not unbiased estimates of generalization. No further prompt optimization should be performed on it for this experiment.

## Frozen Baseline V1 hashes

- Exact canonical `INSTRUCTIONS` UTF-8 SHA-256: `e8d09795f14e9acd79d01d046e2b796d92f4b402858b9fda651d980cefbf6619`
- `evaluate_gemini_baseline.py`: `9ecce38a53b5382b8cdb65ad381ed223fb9279c1b6f4fdfa5c4b8fe2ad97f379`
- `evaluation_ground_truth_approved.csv`: `595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2`
- `evaluation_taxonomy_v2.md`: `2a7841777f60bca31672ada32da26d6d305b552a47c496c4d66a3acd0c63a98f`
- `evaluation_gemini_baseline_predictions.csv`: `13c27d7a755d7c03ad47b3b8634f79f1a60022b41effa129283b674100f54c16`
- `evaluation_gemini_baseline_errors.csv`: `22107026324d1f6efd6c2b21b57c99d42391d8ee2447995bb7101d225d00ea22`
- `evaluation_gemini_baseline_report.md`: `e93414c05c8c219dbd0ef872d6b98fec49af493f25ba99f7e3c19c135dd84951`

## Experimental protection

- The approved 24-record holdout remains untouched and unseen by the selected model candidate.
- The holdout must be evaluated once using the frozen Baseline V1 candidate.
- Holdout results must not be used to modify Baseline V1 and rerun the same holdout as if it were still unseen.
- Any future prompt or model improvement requires a new untouched test set for another unbiased final evaluation.

