# Voice of Customer AI Copilot — Presentation Content Source

This document is the textual source of truth for the portfolio deck. All quantitative claims come from frozen project artifacts. The dataset is synthetic.

## Main deck

### Slide 1 — Voice of Customer AI Copilot

**On-slide copy**

Voice of Customer AI Copilot

Turning unstructured insurance feedback into traceable product signals

AI Product Management case study · Synthetic dataset

**Recommended visual:** Cropped Overview prototype screen.

**Speaker notes:** Introduce the project as a Product Management case study. The product helps a PM move from raw feedback to a candidate pain point, supporting evidence, and an investigation decision. Explain that the dataset is synthetic and the prototype is local. The takeaway is that evaluation shaped the product boundaries. Do not imply deployment, real insurer data, or measured business impact. Likely follow-up: “What did you personally do?” Answer: defined the user problem, taxonomy, prototype workflow, human ground truth, prompt experiments, and final evaluation.

**Evidence:** `web-prototype/`, `evaluation_final_holdout_report.md`

### Slide 2 — The product problem

**On-slide copy**

Product Managers receive feedback as text, not decisions

Feedback arrives across channels with different wording and levels of detail.

The PM still has to answer:

- Which product area is involved?
- What kind of feedback is this?
- How much impact does the text actually describe?
- Which original records support the pattern?

The opportunity is faster evidence review, not automated prioritization.

**Recommended visual:** A field of short feedback excerpts converging into one structured record.

**Speaker notes:** Start with the PM problem before discussing the model. Unstructured feedback makes recurring patterns difficult to compare and verify. The PM needs structure and traceability before deciding what deserves investigation. This project did not measure current time spent or a reduction in time to insight. Likely follow-up: “Why not automate prioritization?” Answer: classification uncertainty, especially Severity, makes human judgment necessary.

**Evidence:** Product brief embodied in `web-prototype/src/App.jsx`; no external market-size claim used.

### Slide 3 — Product opportunity and value hypothesis

**On-slide copy**

Product hypothesis

If PMs can identify recurring friction and trace it back to customer evidence faster, they can spend less time organizing feedback and more time investigating the problems that deserve attention.

- Faster synthesis: Less manual effort organizing feedback before analysis.
- Earlier visibility: Recurring friction becomes easier to spot across many records.
- Evidence-backed investigation: Patterns remain linked to customer feedback before a PM acts.

Value hypothesis — To be validated with real PM workflows and production data.

**Recommended visual:** Three restrained value-lever cards that match the existing deck language.

**Speaker notes:** Explain that this is a product hypothesis, not a measured result. The company rationale is to reduce the manual setup around feedback analysis so PMs can spend more time investigating evidence. Do not claim measured time savings, cost reduction, customer outcomes, or revenue impact. Likely follow-up: “How would you validate the value?” Answer: observe real PM workflows and measure time to a defensible insight, evidence usage, and correction effort.

**Evidence:** Product hypothesis derived from the prototype workflow and project problem statement; no measured business outcome.

### Slide 4 — Primary user and job to be done

**On-slide copy**

Primary user

Product Manager

When reviewing a large feedback set, help me find recurring friction and inspect the evidence so I can decide what needs deeper investigation.

The PM owns the decision. The AI organizes the evidence.

**Recommended visual:** One PM role statement paired with a compact “AI assists / PM decides” division of responsibility.

**Speaker notes:** Keep the primary user focused on the Product Manager. Customer Service Manager could become a future secondary user, but adding another persona would weaken this MVP story. The core job is to move from many comments to a defensible investigation question. Do not claim that the AI discovers root causes. Likely follow-up: “Who else could use it?” Answer: research, support, or operations teams could use later versions, after PM workflow validation.

**Evidence:** `web-prototype/src/App.jsx`, prototype product principle.

### Slide 5 — Product workflow

**On-slide copy**

Customer feedback

AI classification

Structured signals

Candidate pain point

Customer evidence

PM investigation

AI structures and surfaces signals. It does not make the product decision.

**Recommended visual:** Editable horizontal process diagram.

**Speaker notes:** Walk through the system from feedback to investigation. Four classifications create consistent facets. Aggregation reveals patterns, while the evidence layer preserves traceability. The final screen asks the PM to edit the problem statement and choose an investigation status. Likely follow-up: “Where is the AI summary?” Answer: it synthesizes a candidate problem statement, clearly labeled as a starting point rather than a proven cause.

**Evidence:** `web-prototype/src/App.jsx`, `evaluation_taxonomy_v2.md`

### Slide 6 — The prototype makes every insight traceable

**On-slide copy**

Dashboard → insight → evidence → product action

- Overview ranks candidate signals from the classified dataset
- Insight view separates volume, share, and representative evidence
- Evidence view returns to individual feedback records
- Product action keeps the PM responsible for framing and status

Workflow prototype · Earlier seven-theme UI taxonomy

**Recommended visual:** Large Overview screenshot plus a small strip of the other three screens.

**Speaker notes:** Demonstrate the clickable local prototype. Its strongest design choice is the evidence path: the PM can inspect the records behind a summary before acting. Be explicit that the UI reflects an earlier seven-theme classified dataset and does not yet display the V2 Feedback Type dimension. The evaluation taxonomy evolved after the prototype. Likely follow-up: “Would you update it?” Answer: yes, align the prototype with the final eight-theme taxonomy and add Feedback Type and model-review states.

**Evidence:** `web-prototype/`, `customer_feedback_classified.csv`, screenshots captured from the local prototype.

### Slide 7 — Four dimensions create more useful product signals

**On-slide copy**

Theme
What product area is involved?

Feedback Type
What is the customer trying to communicate?

Sentiment
What attitude or evaluation is expressed?

Severity
What customer impact is explicitly described?

Separating subject, intent, attitude, and impact prevents one label from carrying four meanings.

**Recommended visual:** Four-column taxonomy composition with one example label per dimension.

**Speaker notes:** Explain why a single label is insufficient. A document upload comment can be an information need, technical issue, request, or compliment. Sentiment and impact are also separate: emotional wording alone should not increase Severity. The taxonomy uses exactly one primary value per dimension. Likely follow-up: “How did you handle multi-topic feedback?” Answer: choose the primary customer problem and flag genuinely plausible alternatives as Ambiguous in the human reference.

**Evidence:** `evaluation_taxonomy_v2.md`

### Slide 8 — Development and holdout served different purposes

**On-slide copy**

150 synthetic records

40-record development set
Human-reviewed ground truth · prompt analysis and iteration

Baseline V1 → Prompt V2 → Prompt V3

Final candidate lock
Baseline V1 selected before holdout predictions

24-record locked holdout
One final unseen evaluation

**Recommended visual:** Editable evaluation pipeline with development and holdout lanes.

**Speaker notes:** This slide establishes experiment integrity. The development set supported error analysis and prompt iteration, so its results cannot estimate generalization. The separate 24-record holdout was human-reviewed and locked before final model evaluation. Baseline V1 was selected before holdout predictions. Likely follow-up: “Why only 24?” Answer: it is a small portfolio holdout designed for taxonomy coverage, not prevalence; that limits confidence and motivates a larger future evaluation.

**Evidence:** `evaluation_holdout_lock.md`, `evaluation_final_candidate_lock.md`, evaluation reports.

### Slide 9 — More prompt detail did not improve overall performance

**On-slide copy**

Development set · n = 40

| Prompt | Theme | Type | Sentiment | Severity | Exact |
|---|---:|---:|---:|---:|---:|
| V1 | 97.5% | 85.0% | 82.5% | 92.5% | 67.5% |
| V2 | 95.0% | 90.0% | 52.5% | 82.5% | 37.5% |
| V3 | 95.0% | 87.5% | 85.0% | 85.0% | 62.5% |

V2 improved Feedback Type but caused major regressions. V3 recovered much of the loss, yet V1 retained the strongest overall trade-off.

Final candidate: Baseline V1

**Recommended visual:** Editable comparison table with restrained row highlighting.

**Speaker notes:** I compared three prompt versions on the same 40-record development set. V2 improved Feedback Type but caused major regressions. V3 recovered much of that loss, but V1 still had the strongest overall trade-off, so I selected V1 before touching the holdout. These are development results, not final generalization estimates. Likely follow-up: “Why not choose the newest prompt?” Answer: the product uses all four dimensions, and V1 performed better across the combined behavior.

**Evidence:** `evaluation_prompt_v1_v2_v3_comparison.md`, `evaluation_final_candidate_lock.md`

### Slide 10 — The unseen holdout revealed uneven reliability

**On-slide copy**

Final holdout · n = 24

Theme 100.0%

Feedback Type 83.3%

Sentiment 87.5%

Severity 58.3%

All four fields correct: 11 of 24 records · 45.8%

Exact match is strict. It does not represent a single overall “AI accuracy.”

**Recommended visual:** Four editable bars plus a separate exact-match annotation.

**Speaker notes:** Present the final unseen evaluation without averaging away the weak dimension. Theme performed perfectly on this small, balanced holdout. Feedback Type and Sentiment were useful but imperfect. Severity was materially weaker. Exact match means all four fields must agree, so one Severity error makes the record non-exact. Do not describe 45.8% as general AI accuracy or production performance. Likely follow-up: “Why did development and holdout differ?” Answer: the small holdout exposed a different mix of boundaries, especially No Issue versus Low.

**Evidence:** `evaluation_final_holdout_report.md`

### Slide 11 — Severity was the weakest signal on unseen data

**On-slide copy**

Human Severity → Gemini prediction

No Issue: 3 correct · 7 predicted Low

Low: 3 correct · 1 predicted No Issue · 2 predicted Medium

Medium: 6 of 6 correct

High: 2 of 2 correct

The model recognized explicit Medium and High impact in this sample, but frequently created false urgency for records with no stated impact.

**Recommended visual:** Editable Severity confusion matrix with the No Issue → Low cell emphasized.

**Speaker notes:** This is the central failure-analysis slide. Seven of ten human No Issue records became Low. The model also moved two Low records to Medium. It correctly classified all six Medium and both High records in this holdout, but the sample is small. The product risk is false urgency: a PM could over-prioritize requests or factual questions. Likely follow-up: “Why call it calibration?” Answer: the ordering is often plausible, but the model’s threshold for adverse impact is too low.

**Evidence:** `evaluation_final_holdout_report.md`, `evaluation_final_holdout_errors.csv`

### Slide 12 — Evaluation changed what I would let the AI decide

**On-slide copy**

Theme
Use to organize and filter feedback

Sentiment
Use as supporting context

Feedback Type
Use with review around Process Friction and Technical Issue

Severity
Use as a review cue, not an autonomous priority score

Product recommendation: expose evidence and require PM review when impact affects prioritization.

**Recommended visual:** Four trust bands mapped to product behavior.

**Speaker notes:** The holdout changed my product recommendation. I would use Theme for organization, keep Sentiment as supporting context, review known Feedback Type boundaries, and never use Severity as an autonomous priority score. A future version could show confidence or “Needs Review,” but those are recommendations, not current prototype features. Likely follow-up: “Would you remove Severity?” Answer: no; retain it as assistive metadata while improving calibration and requiring evidence review.

**Evidence:** `evaluation_final_holdout_report.md`, `evaluation_final_holdout_errors.csv`

### Slide 13 — Evidence stays attached to the product decision

**On-slide copy**

Candidate insight

“Customers may lack confidence that uploaded documents were received or recognized.”

Traceable evidence
Original feedback records remain available for review and filtering.

PM action
The PM edits the problem statement, records investigation questions, and selects a decision status.

The AI proposes a frame. The PM decides whether the evidence supports it.

**Recommended visual:** Insight, Evidence, and Product Action screenshots in sequence.

**Speaker notes:** Show how the interface operationalizes human oversight. The summary is labeled as AI-assisted and explicitly says it is not a proven root cause. The PM can return to original records, then edit the problem statement and set “Needs Investigation.” Do not claim the prototype stores decisions in a production database; it is a local interactive demo. Likely follow-up: “What makes this different from a dashboard?” Answer: traceability and an explicit decision workflow connect aggregates to evidence and PM judgment.

**Evidence:** `web-prototype/src/App.jsx`, local prototype screenshots.

### Slide 14 — What I would validate next

**On-slide copy**

Current limits

- Synthetic feedback, not real customer data
- Final holdout contains 24 coverage-focused records
- Human reference labels include judgment
- Prototype taxonomy predates the final V2 evaluation taxonomy
- No PM usability study or business outcome measurement

Next validation

- Test with anonymized real-world feedback under governance controls
- Expand and stratify the evaluation set
- Investigate Severity thresholds and review states
- Test the workflow with Product Managers
- Define pilot success metrics before deployment

**Recommended visual:** Two-column limits and next-validation composition.

**Speaker notes:** The current evidence is useful but limited. My next step would be to test the workflow with real Product Managers, use governed anonymized feedback, expand the human-reviewed evaluation set, and investigate the Severity boundary with a new locked test set. The next product step is not another prompt tweak on the same holdout. Likely follow-up: “What success metric would you choose?” Answer: PM time to a defensible insight, correction rate by dimension, evidence usage, and decision usefulness, defined before a pilot.

**Evidence:** `evaluation_final_holdout_report.md`, prototype inspection.

### Slide 15 — The harder decision was what to trust

**On-slide copy**

Building the classifier produced outputs.

Evaluation produced the product decision.

Trust Theme for organization.

Treat Severity as a review signal.

Keep customer evidence and PM judgment in the loop.

**Recommended visual:** Minimal closing slide with one evidence-to-decision line and prototype detail.

**Speaker notes:** Close on product judgment. The project’s value is not that an API generated labels. The work defined behavior, created human ground truth, preserved a holdout, accepted regressions, and translated failure modes into product constraints. Do not claim the model is production-ready. Likely follow-up: “What are you most proud of?” Answer: resisting the temptation to choose the newest prompt and using evaluation to narrow what the AI should control.

**Evidence:** Final comparison, candidate lock, final holdout report.

## Appendix

### Slide 16 — Full Theme taxonomy

**On-slide copy:** Eight themes and concise definitions from `evaluation_taxonomy_v2.md`.

**Visual:** Editable two-column taxonomy table.

### Slide 17 — Feedback Type, Sentiment, and Severity

**On-slide copy:** Six Feedback Types, three Sentiments, and four Severity levels with concise definitions.

**Visual:** Editable taxonomy table.

### Slide 18 — Dataset and prototype scope

**On-slide copy:** 150 synthetic feedback records; July–August 2026; source fields; prototype classified dataset uses earlier seven-theme taxonomy; no incidence denominator; no production backend.

**Visual:** Scope diagram and prototype screenshot.

### Slide 19 — Full development comparison

**On-slide copy:** V1/V2/V3 metrics including Theme macro F1 and Feedback Type macro F1.

**Visual:** Editable comparison table.

### Slide 20 — Holdout confusion matrices

**On-slide copy:** Feedback Type and Severity confusion matrices from the frozen holdout report.

**Visual:** Two editable matrices.

### Slide 21 — Representative holdout errors

**On-slide copy:** HOLD003, HOLD011, HOLD015, and HOLD021 with shortened feedback excerpts, human labels, predictions, and interpretation.

**Visual:** Editable evidence table.

### Slide 22 — Experiment integrity safeguards

**On-slide copy:** Human-reviewed ground truth; locked hashes; allowlisted input fields; structured schema; prediction-first saving; candidate selected before holdout; no post-holdout rerun.

**Visual:** Checklist and artifact lineage.

### Slide 23 — Metrics and technical implementation

**On-slide copy:** Plain definitions of accuracy, precision, recall, F1, macro F1, exact match; Python, pandas, Gemini Developer API, structured JSON, local React prototype.

**Visual:** Compact glossary and architecture footer.
