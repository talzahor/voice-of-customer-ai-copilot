# File Inventory and Inclusion Decisions

This is a GitHub-ready copy of the portfolio project. The original working folder was left unchanged. “Safe for GitHub” means no hard-coded secret or real customer data was found in the inspected artifact; the included datasets are synthetic.

## Included artifacts

| File or folder | Purpose | Category | Presentation use | Safe for GitHub | Notes |
|---|---|---|---|---|---|
| `README.md` | Repository overview and evidence boundaries | Documentation | Yes | Yes | Created from inspected project and presentation artifacts only |
| `requirements.txt` | Python dependency declaration | Setup | Yes | Yes | Includes `pandas` and `google-genai`; no key value |
| `data/raw/customer_feedback.csv` | Original 150-record synthetic feedback dataset | Data | Yes | Yes | Five raw source fields; original contents copied unchanged |
| `data/processed/customer_feedback_classified.csv` | Earlier seven-theme classifier output used by the prototype | Data | Yes | Yes | Preserves the prototype’s earlier taxonomy state |
| `data/v2/customer_feedback_v2.csv` | Synthetic Dataset V2 used to construct development and holdout evaluation sets | Data | Yes | Yes | 150 records |
| `src/exploratory/analyze_feedback.py` | Initial pandas exploration | Source | Context | Yes | Early analysis script, copied unchanged |
| `src/initial-classifier/classify_feedback.py` | Earlier 150-record Gemini classifier | Source | Context | Yes | Uses environment variable `GEMINI_API_KEY`; not the V2 evaluator |
| `src/validation/validate_customer_feedback_v2.py` | Deterministic Dataset V2 validation | Source | Context | Yes | Supports dataset integrity |
| `evaluation/taxonomy/evaluation_taxonomy_v2.md` | Approved Theme, Feedback Type, Sentiment, and Severity definitions | Evaluation | Yes | Yes | Canonical V2 taxonomy |
| `evaluation/development/evaluation_ground_truth_approved.csv` | Human-approved 40-record development reference | Evaluation | Yes | Yes | Used only for development prompt experiments |
| `evaluation/development/evaluate_gemini_baseline.py` | Baseline V1 evaluator, structured output, local validation, metrics | Evaluation source | Yes | Yes | Reads `GEMINI_API_KEY` from environment; no value stored |
| `evaluation/development/evaluate_gemini_prompt_v2.py` | Prompt V2 development evaluator | Evaluation source | Yes | Yes | Experimental iteration |
| `evaluation/development/evaluate_gemini_prompt_v3.py` | Prompt V3 development evaluator | Evaluation source | Yes | Yes | Experimental iteration |
| `evaluation/development/compare_gemini_prompt_versions_v3.py` | Compares frozen V1/V2/V3 predictions | Evaluation source | Yes | Yes | Generates the final development comparison if not already present |
| `evaluation/development/evaluation_prompt_v2.md` | Prompt V2 specification | Evaluation | Yes | Yes | Development artifact |
| `evaluation/development/evaluation_prompt_v3.md` | Prompt V3 specification | Evaluation | Yes | Yes | Development artifact |
| `evaluation/development/evaluation_gemini_baseline_*` | Frozen V1 predictions, errors, and report | Evaluation | Yes | Yes | Baseline development results |
| `evaluation/development/evaluation_gemini_prompt_v2_*` | Frozen V2 predictions, errors, and report | Evaluation | Yes | Yes | Development results, not final candidate |
| `evaluation/development/evaluation_gemini_prompt_v3_*` | Frozen V3 predictions, errors, and report | Evaluation | Yes | Yes | Development results, not final candidate |
| `evaluation/development/evaluation_prompt_v1_v2_v3_comparison.md` | Final V1/V2/V3 comparison | Evaluation | Yes | Yes | Main evidence for Baseline V1 selection |
| `evaluation/development/evaluation_final_candidate_lock.md` | Baseline V1 selection record and frozen hashes | Evaluation integrity | Yes | Yes | Confirms selection before holdout prediction |
| `evaluation/holdout/evaluation_holdout_ground_truth_approved.csv` | Locked 24-record human reference | Evaluation | Yes | Yes | Must not be changed to match model output |
| `evaluation/holdout/evaluation_holdout_lock.md` | Holdout approval record and hashes | Evaluation integrity | Yes | Yes | Documents human review and lock |
| `evaluation/holdout/evaluate_gemini_final_holdout.py` | Final holdout evaluator | Evaluation source | Yes | Yes | Verifies frozen V1 and holdout before a run |
| `evaluation/holdout/evaluation_final_holdout_predictions.csv` | Frozen final holdout predictions | Evaluation | Yes | Yes | Saved before label comparison |
| `evaluation/holdout/evaluation_final_holdout_errors.csv` | Final holdout mismatch records | Failure analysis | Yes | Yes | Supports Severity and Feedback Type analysis |
| `evaluation/holdout/evaluation_final_holdout_report.md` | Final holdout metrics and confusion matrices | Evaluation | Yes | Yes | Primary evidence for final metric claims |
| `web-prototype/` | Local React/Vite PM prototype source | Prototype | Yes | Yes | Source, lock file, and synthetic CSV included; dependencies/build output excluded |
| `docs/presentation_content_source.md` | Slide content and evidence sources | Documentation | Yes | Yes | Supports final deck narration |
| `docs/portfolio_claim_evidence_register.md` | Claim-by-claim evidence and constraints | Documentation | Yes | Yes | Marks hypotheses and prohibited claims |
| `docs/portfolio_project_defense_guide.md` | Case-study explanation and interview prep | Documentation | Supporting | Yes | Not required to run the project |
| `docs/portfolio_file_map.md` | Slide-to-artifact map | Documentation | Yes | Yes | Created for this GitHub-ready copy |
| `docs/file_inventory.md` | Artifact inventory and inclusion decisions | Documentation | Yes | Yes | This file |
| `demo/Voice_of_Customer_AI_Copilot_Portfolio_Case_Study_Final_v4.pptx` | Final portfolio deck | Demo | Yes | Yes | Copied from the project presentation folder |
| `demo/Voice_of_Customer_AI_Copilot_Portfolio_Case_Study_Final_v4.pdf` | Viewable version of final portfolio deck | Demo | Yes | Yes | Copied from the project presentation folder |

## Intentionally excluded artifacts

| File or folder | Reason excluded | Notes |
|---|---|---|
| `.venv/`, `web-prototype/node_modules/` | Local dependencies | Recreated from dependency manifests; never commit |
| `web-prototype/dist/` | Generated frontend build output | Rebuilt with Vite; not needed for source review |
| `.idea/`, `.DS_Store`, `__pycache__/` | IDE, operating-system, and Python cache files | Local machine artifacts |
| `.deck-build/`, `.chart-data-*`, `.codex-finalizer/` | Temporary deck-rendering and chart build artifacts | Not part of the portfolio source story |
| `portfolio-presentation/Voice_of_Customer_AI_Copilot_Portfolio_Case_Study*.pptx/pdf` older versions | Superseded presentation versions | Final V4 is included in `demo/` |
| `customer_feedback_test_results.csv`, `document_theme_validation_results.csv` | Early 10-record pilot outputs | Useful historical work, but not necessary for the final case-study narrative |
| `validate_document_themes.py` | Early document-theme validation script | Superseded by V2 taxonomy/evaluation story |
| `debug_gemini_request.py`, `debug_gemini_batch_scaling.py` | API debugging diagnostics | Not needed to explain final methodology |
| `compare_gemini_prompt_versions.py`, `evaluation_prompt_v1_vs_v2_comparison.md` | Earlier V1/V2-only comparison | Superseded by the final V1/V2/V3 comparison |
| `evaluation_baseline_v1_summary.md`, `evaluation_baseline_v1_error_analysis.md` | Interim Baseline V1 analysis | Final comparison and holdout reports are more complete |
| `evaluation_ground_truth_proposed.csv` | Pre-approval development reference | Approved development ground truth is included instead |
| `evaluation_holdout_candidate.csv`, `evaluation_holdout_candidate_review.md` | Pre-lock holdout candidate and review workpapers | Final approved holdout and lock are included instead |
| `~$*.pptx` | Temporary Microsoft Office lock file | Never commit |

## Sensitive-information review

- No `.env`, private key, credential file, hard-coded Gemini key, OpenAI key, or authentication token was found in the included source files.
- Gemini-related scripts reference `GEMINI_API_KEY` through `os.getenv`; the environment variable value is not stored in this repository copy.
- The datasets are explicitly synthetic. No real customer or production data was identified.

## Naming ambiguity noted

The requested presentation filename `Voice_of_Customer_AI_Copilot_Portfolio_Case_Study_Final_v4(2).pptx` was not found. Two V4 PPTX copies were found: one in the project presentation folder and one in the user home folder. Their slide and speaker-note content matched when inspected, but their full-file hashes differ because of package-level metadata. The repository includes the V4 copy from the project’s `portfolio-presentation/` folder because it is paired with the project’s V4 PDF and is the canonical project-location copy.
