# Portfolio Claim and Evidence Register

| Claim | Evidence | Source artifact | Status |
|---|---|---|---|
| The primary user is a Product Manager | The prototype workflow and product framing center PM investigation and decision ownership | `web-prototype/src/App.jsx` | Supported |
| The product could reduce manual effort spent organizing feedback before analysis | Product opportunity inferred from the PM workflow; not measured | Product hypothesis | Hypothesis |
| The product could provide earlier visibility into recurring friction | Product opportunity inferred from structured aggregation; not measured on real workflows | Product hypothesis | Hypothesis |
| Keeping patterns linked to customer evidence could support more traceable PM investigation | Prototype demonstrates traceability; decision-quality impact has not been measured | `web-prototype/src/App.jsx` | Hypothesis |
| The product turns unstructured feedback into structured signals | Classification outputs Theme, Feedback Type, Sentiment, and Severity | `evaluation_taxonomy_v2.md`, evaluator artifacts | Supported |
| AI outputs remain traceable to original feedback | Insight and evidence screens expose supporting records | `web-prototype/src/App.jsx` | Supported |
| The dataset contains 150 records | Dataset row count | `customer_feedback_v2.csv` and classified prototype dataset | Measured |
| The dataset is synthetic | Evaluation reports explicitly state this | `evaluation_final_holdout_report.md` | Limitation |
| The development set contains 40 human-reviewed records | Frozen evaluation methodology | `evaluation_gemini_baseline_report.md` | Measured |
| The final holdout contains 24 records | Frozen final report | `evaluation_final_holdout_report.md` | Measured |
| V1 Theme accuracy on development was 97.5% | 39 of 40 | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V1 Feedback Type accuracy on development was 85.0% | 34 of 40 | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V1 Sentiment accuracy on development was 82.5% | 33 of 40 | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V1 Severity accuracy on development was 92.5% | 37 of 40 | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V1 exact match on development was 67.5% | 27 of 40 | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V2 improved Feedback Type but caused regressions | Type rose to 90.0%; Sentiment fell to 52.5%; exact match fell to 37.5% | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| V3 recovered much of the loss but did not outperform V1 overall | V3 exact match 62.5%; Severity 85.0% | `evaluation_prompt_v1_v2_v3_comparison.md` | Measured |
| Baseline V1 was selected before holdout predictions | Final candidate lock records timing and rationale | `evaluation_final_candidate_lock.md` | Supported |
| Final holdout Theme accuracy was 100.0% | 24 of 24 | `evaluation_final_holdout_report.md` | Measured |
| Final holdout Feedback Type accuracy was 83.3% | 20 of 24 | `evaluation_final_holdout_report.md` | Measured |
| Final holdout Sentiment accuracy was 87.5% | 21 of 24 | `evaluation_final_holdout_report.md` | Measured |
| Final holdout Severity accuracy was 58.3% | 14 of 24 | `evaluation_final_holdout_report.md` | Measured |
| Final holdout all-fields exact match was 45.8% | 11 of 24 | `evaluation_final_holdout_report.md` | Measured |
| Severity overpredicted impact on the holdout | 9 overpredictions; 7 of 10 No Issue records predicted Low | `evaluation_final_holdout_report.md` | Measured |
| Medium and High Severity were identified correctly in the holdout | 6 of 6 Medium and 2 of 2 High | `evaluation_final_holdout_report.md` | Measured |
| Process Friction and Technical Issue remain a boundary | Two cross-confusions on holdout | `evaluation_final_holdout_report.md` | Measured |
| Severity should not autonomously determine priority | Product recommendation derived from weak Severity reliability | Final holdout evidence | Supported |
| Confidence and Needs Review states should be added | Proposed safeguard, not present in prototype | Evaluation interpretation | Hypothesis |
| Prototype supports filters and evidence review | Visible interactive controls and records | `web-prototype/src/App.jsx` | Supported |
| Prototype reflects the final V2 taxonomy | It uses seven themes, `Login & Access`, Severity `None`, and omits Feedback Type | Prototype inspection | Do not use |
| The project used real Harel customer data | No supporting artifact; dataset is synthetic | Evaluation reports | Do not use |
| Harel receives thousands of reviews monthly | No reliable project source | None | Do not use |
| The product reduced time to insight from 30 days to 24 hours | Not measured | None | Do not use |
| The product reduced claim friction by 20% | Not measured | None | Do not use |
| The system is production-ready | Small synthetic evaluation and weak Severity contradict this | `evaluation_final_holdout_report.md` | Do not use |
| A future pilot should measure PM time to a defensible insight | Proposed future metric | Product recommendation | Target |
| A future pilot should measure correction rate by dimension | Proposed model-quality metric | Product recommendation | Target |
