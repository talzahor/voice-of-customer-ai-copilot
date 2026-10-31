# Voice of Customer AI Copilot — Interview and Project Defense Guide

## The project in plain English

Product Managers often receive feedback as free text. The comments contain useful evidence, but they are hard to compare at scale. I designed a local prototype that uses AI classification to organize feedback, surface candidate pain points, and keep every insight linked to the original records. The PM reviews the evidence and makes the product decision.

The project uses a synthetic insurance-feedback dataset. It does not use real insurer data and it is not a production system.

## Core concepts

### Voice of Customer

Voice of Customer means the collected feedback, needs, questions, complaints, and praise that describe how people experience a product or service. In this project, the feedback comes from synthetic channels such as app reviews, chat, surveys, and support calls.

### Taxonomy

A taxonomy is an agreed set of labels and definitions. It turns subjective classification into a more repeatable decision. This project separates four questions:

- Theme: what product area is involved?
- Feedback Type: what is the customer trying to communicate?
- Sentiment: what attitude or evaluation is expressed?
- Severity: what impact is explicitly described?

The separation matters. A request can be neutral and have no adverse impact. A negative comment can describe only a small inconvenience. Theme alone cannot describe intent or impact.

### Structured output

Structured output requires the model to return fields in a defined JSON shape instead of free-form prose. The schema restricts the allowed labels. Python then checks the record count, IDs, required fields, duplicates, and label values before saving results.

Structured output improves reliability of the data pipeline. It does not guarantee that the classification itself is correct.

### Ground truth

Ground truth is the human-reviewed reference used to evaluate the model. “Ground truth” does not mean every label is objectively perfect. Some feedback is genuinely ambiguous. The project records an ambiguity flag and preserves human decisions rather than changing labels after seeing model output.

### Development set

The 40-record development set supported the first baseline, error analysis, and Prompt V2/V3 experiments. Once I used those results to guide prompt work, the set stopped being an unbiased test of generalization.

### Holdout set

The 24-record holdout was created, human-reviewed, and locked separately. It remained untouched during prompt development. Baseline V1 was selected as the final candidate before generating holdout predictions. This makes the holdout the project’s final unseen-data evaluation.

### Confusion matrix

A confusion matrix compares human labels with model predictions. Rows show the human reference and columns show the model output. The Severity matrix revealed the key failure: seven of ten No Issue records were predicted Low.

### Precision

Precision asks: when the model predicts a label, how often is that prediction correct? Low precision creates false positives. For a high-impact state, poor precision could create false urgency.

### Recall

Recall asks: of all records that truly belong to a label, how many did the model find? Low recall means the model misses relevant records.

### F1

F1 balances precision and recall. It is useful when both missed cases and false positives matter.

### Macro F1

Macro F1 calculates F1 for every class and then averages them equally. A rare class counts as much as a common class. This helps expose weak performance that overall accuracy can hide.

### Exact match

Exact match requires all four fields for a feedback record to match the human reference. On the final holdout, 11 of 24 records matched on all fields, or 45.8%. This is a strict compound measure, not the system’s single general accuracy.

### Ambiguous examples

An Ambiguous record has another genuinely plausible label. Ambiguity does not mean the reference is missing. It documents that reasonable reviewers might disagree. On the holdout, exact match was 10 of 18 for Clear records and 1 of 6 for Ambiguous records.

### Overfitting

Overfitting happens when changes become too tailored to known examples and do not generalize. Repeatedly adjusting a prompt against the same 40 records can improve that set without improving new data. The holdout protects against that mistake.

### Regression

A regression occurs when a change improves one behavior but makes another worse. Prompt V2 improved Feedback Type to 90.0%, but Sentiment dropped to 52.5% and exact match dropped to 37.5%. Prompt V3 recovered performance, but Severity and exact match remained below V1.

### Calibration

Calibration describes whether a model’s level or confidence matches reality. Here, the model’s Severity threshold was too sensitive. It often treated a request or information need as Low impact even when the text described no adverse impact.

### False positives and false urgency

A false positive assigns a label that the human reference does not support. A Severity overprediction can create false urgency. If a PM dashboard ranks themes using that signal, ordinary requests could appear more serious than the evidence warrants.

## Why Baseline V1 was selected

V1 did not win every individual metric. V3 had slightly higher Feedback Type and Sentiment accuracy. V1 still had stronger Severity, Theme macro F1, and all-fields exact match. It provided the best overall trade-off for the four-dimensional product behavior.

The decision also demonstrates discipline: more prompt instructions did not automatically produce a better product.

## Why the holdout cannot be rerun after a prompt change

Once I inspect holdout errors and use them to change the prompt, the holdout has influenced development. It is no longer unseen. Rerunning the same records and calling the new score “final holdout performance” would overstate evidence. A future improved prompt needs a newly locked test set.

## Why Severity performed poorly

The final holdout had ten No Issue records. The model classified only three correctly and called seven Low. It also moved two Low records to Medium. Many of these records contained requests, questions, caveats, or technical context. The model appeared to treat the presence of friction-related language as impact even when the feedback did not state an adverse consequence.

At the same time, the model classified all six Medium and both High records correctly in this small holdout. That suggests the main boundary problem was distinguishing no stated impact from limited impact, not detecting explicit serious impact. The sample is too small to generalize this pattern confidently.

## Product implication

I would use Theme as an organizing and filtering signal. Feedback Type and Sentiment can support analysis with visible evidence. I would not let Severity autonomously rank roadmap priorities or trigger escalation. The interface should keep supporting records visible and require human review when impact affects prioritization.

Future safeguards could include a Needs Review state, confidence information, and reviewer correction workflows. These are recommendations, not implemented features.

## What I would do next with real customer data

1. Establish privacy, consent, retention, and access rules before ingestion.
2. Sample anonymized feedback across channels and time periods.
3. Create a larger reference set with at least two reviewers and an adjudication process.
4. Measure agreement between human reviewers before treating model disagreement as error.
5. Re-evaluate every dimension, especially Severity boundaries.
6. Run moderated usability sessions with Product Managers.
7. Define pilot metrics before deployment, including review time, correction rate, evidence usage, and decision usefulness.

## Likely interview questions

### “What was the main product decision?”

The main decision was not which prompt produced the highest isolated metric. It was what behavior the product could safely rely on. The holdout showed that Theme could support organization, while Severity needed human review.

### “Why use AI here?”

The input is unstructured language with context and ambiguous boundaries. AI can create consistent candidate labels and summaries faster than manual first-pass review. The product still preserves evidence because language classification remains uncertain.

### “Why not use keyword rules?”

The same words can express different intents. “Document” could refer to requirements, upload recognition, or a request for a new feature. Context matters. Keyword rules would also struggle with mixed feedback and implicit intent.

### “How did you avoid leaking ground truth?”

The evaluator created an allowlisted payload containing only ID, feedback text, channel, and journey stage. It saved validated predictions before comparing them with human labels. Human labels, ambiguity flags, and rationales never entered the model request.

### “Why was V1 better than V3?”

V3 improved Feedback Type and Sentiment slightly, but V1 was stronger on Severity and exact match. Since the product uses all four dimensions together, V1 offered the stronger overall trade-off.

### “Is 100% Theme accuracy convincing?”

It is encouraging evidence on this 24-record coverage-focused synthetic holdout. It is not proof of production accuracy. The sample contains three examples per Theme and does not represent real-world prevalence or language diversity.

### “What does 45.8% exact match mean?”

Eleven of 24 records matched the human reference on all four fields. It is deliberately strict. It should not replace the individual dimension metrics or be called the overall AI accuracy.

### “What would you change in the prototype?”

I would align the UI with the final eight-theme taxonomy, add Feedback Type, and introduce review states for uncertain or impact-sensitive classifications. I would keep the existing evidence-first workflow.

### “What did you learn as a Product Manager?”

An AI feature needs an explicit behavioral contract. Evaluation can change the product permissions, not only the prompt. A weak dimension should lead to a safer workflow, not a hidden caveat.

### “What would production readiness require?”

Real representative data, privacy controls, stronger human-reference methodology, larger and refreshed evaluations, drift monitoring, correction workflows, reliability targets by dimension, and PM usability evidence.

