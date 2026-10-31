# Portfolio Presentation to File Map

The final presentation in `demo/Voice_of_Customer_AI_Copilot_Portfolio_Case_Study_Final_v4.pptx` is supported by the following repository artifacts. The dataset is synthetic.

| Presentation slide | Claim or purpose | Supporting artifacts |
|---|---|---|
| 1. Cover | Product framing: unstructured feedback to traceable product signals | `README.md`, `web-prototype/`, `demo/Voice_of_Customer_AI_Copilot_Portfolio_Case_Study_Final_v4.pdf` |
| 2. Product problem | PMs receive feedback as text, not decisions | `docs/presentation_content_source.md`, `web-prototype/src/App.jsx` |
| 3. Product opportunity and value hypothesis | Faster synthesis, earlier visibility, and traceable investigation are hypotheses | `docs/presentation_content_source.md`, `docs/portfolio_claim_evidence_register.md` |
| 4. Primary user and JTBD | Product Manager owns investigation and decision | `docs/presentation_content_source.md`, `web-prototype/src/App.jsx` |
| 5. Product workflow | Feedback -> classification -> signals -> evidence -> PM investigation | `docs/presentation_content_source.md`, `web-prototype/src/App.jsx` |
| 6. Prototype | Local interactive evidence-first experience | `web-prototype/src/App.jsx`, `web-prototype/src/styles.css`, `web-prototype/public/customer_feedback_classified.csv` |
| 7. Four dimensions | Theme, Feedback Type, Sentiment, and Severity are distinct product signals | `evaluation/taxonomy/evaluation_taxonomy_v2.md` |
| 8. Evaluation strategy | Development set, locked holdout, and selection timing | `evaluation/development/evaluation_final_candidate_lock.md`, `evaluation/holdout/evaluation_holdout_lock.md` |
| 9. Prompt experiments | V1/V2/V3 comparison and Baseline V1 selection | `evaluation/development/evaluation_prompt_v1_v2_v3_comparison.md`, `evaluation/development/evaluation_final_candidate_lock.md` |
| 10. Final holdout results | 24-record unseen evaluation; dimension-level results | `evaluation/holdout/evaluation_final_holdout_report.md`, `evaluation/holdout/evaluation_final_holdout_predictions.csv` |
| 11. Severity failure | No Issue -> Low and Low -> Medium boundary errors | `evaluation/holdout/evaluation_final_holdout_report.md`, `evaluation/holdout/evaluation_final_holdout_errors.csv` |
| 12. Product permissions | Different outputs earned different levels of trust; Severity remains a review signal | `evaluation/holdout/evaluation_final_holdout_report.md`, `docs/portfolio_claim_evidence_register.md` |
| 13. Evidence to PM action | AI summaries remain linked to original records; PM makes the decision | `web-prototype/src/App.jsx`, `docs/presentation_content_source.md` |
| 14. What I would validate next | Synthetic-data, evaluation, and usability limitations | `docs/presentation_content_source.md`, `docs/portfolio_project_defense_guide.md` |
| 15. Closing | Evaluation changed what the AI should be allowed to do | `evaluation/holdout/evaluation_final_holdout_report.md`, `docs/portfolio_project_defense_guide.md` |
| 16-17. Taxonomy appendix | Full V2 taxonomy and definitions | `evaluation/taxonomy/evaluation_taxonomy_v2.md` |
| 18. Dataset and prototype scope | 150 synthetic records, V2 dataset, earlier prototype taxonomy | `data/raw/customer_feedback.csv`, `data/v2/customer_feedback_v2.csv`, `web-prototype/README.md` |
| 19. Development comparison appendix | Full V1/V2/V3 comparison | `evaluation/development/evaluation_prompt_v1_v2_v3_comparison.md` |
| 20. Holdout matrices appendix | Feedback Type and Severity confusion matrices | `evaluation/holdout/evaluation_final_holdout_report.md` |
| 21. Representative errors appendix | Individual holdout mismatches | `evaluation/holdout/evaluation_final_holdout_errors.csv` |
| 22. Experiment integrity appendix | Hash locks, allowlisted inputs, validation, and prediction-first saving | `evaluation/holdout/evaluation_holdout_lock.md`, `evaluation/development/evaluation_final_candidate_lock.md`, `evaluation/holdout/evaluate_gemini_final_holdout.py` |
| 23. Metrics and technical implementation appendix | Python, pandas, Gemini Developer API, structured JSON, and local prototype | `requirements.txt`, `evaluation/development/evaluate_gemini_baseline.py`, `web-prototype/package.json` |
