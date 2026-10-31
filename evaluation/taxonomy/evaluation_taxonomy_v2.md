# Voice of Customer AI Copilot — Evaluation Taxonomy V2

This document defines the human-reference taxonomy used by `evaluation_ground_truth_approved.csv`.

The approved CSV is the locked reference for blind model evaluation. Its labels must not be changed because a model disagrees with them. Any future ground-truth change requires an explicitly documented human-review revision.

## Theme

Use exactly one primary Theme:

- Document Requirements
- Document Upload
- Claim Submission & Form
- Claim Status
- Reimbursement
- Login & Account
- Customer Support
- General Experience

Theme answers: “What product or customer-journey area is the feedback primarily about?”

- **Document Requirements:** Uncertainty about which documents, forms, receipts, or paperwork are required.
- **Document Upload:** Whether a submitted file was uploaded, sent, received, recognized, or continues to appear missing after submission.
- **Customer Support:** Use only when support itself is the primary problem. Contacting support as a consequence of another product problem does not make Customer Support the Theme.
- **Claim Status:** The progress or state of the claim itself.
- **Reimbursement:** Payment, payment timing, amount, or receipt of money.
- For multi-topic feedback, choose the primary customer problem and mark the record Ambiguous when another Theme is genuinely plausible.

### Approved Theme principle

General Experience is a fallback Theme. Do not use it when the feedback has a sufficiently specific primary subject covered by another Theme.

Theme describes what area the feedback is about, independently of whether the experience was positive, neutral, or negative.

## Feedback Type

Use exactly one primary Feedback Type:

- Process Friction
- Technical Issue
- Improvement Request
- Information Need
- Compliment
- General Feedback

- **Process Friction:** A non-technical obstacle, delay, repeated effort, unclear workflow, or difficult process.
- **Technical Issue:** An explicit error, malfunction, failed control, inconsistent system state, or unavailable functionality.
- **Improvement Request:** An explicit request or suggestion for a new capability or change.
- **Information Need:** The primary purpose is asking for information or clarification.
- **Compliment:** The primary purpose is praise or reporting a favorable experience.
- **General Feedback:** Factual, mixed, broad, or experiential feedback without another clearly dominant type.

### Approved Feedback Type principle

For mixed feedback, use Compliment when explicit praise is the dominant purpose and any inconvenience is clearly secondary. A minor inconvenience does not automatically make the record General Feedback.

## Sentiment

Use:

- Positive
- Neutral
- Negative

- **Positive:** Explicit favorable evaluation or satisfaction.
- **Negative:** Expressed dissatisfaction, failure, delay, a problem, or another clearly negative experience.
- **Neutral:** Information-seeking or factual feedback without enough evidence of positive or negative evaluation.

### Approved Sentiment principle

Uncertainty, confusion, or asking a question does not automatically imply Negative sentiment. A factual or information-seeking question may remain Neutral even when the customer lacks information.

## Severity

Use:

- No Issue
- Low
- Medium
- High

- **No Issue:** No adverse customer impact is described.
- **Low:** Limited inconvenience, uncertainty, or confusion, without evidence that the customer is meaningfully blocked.
- **Medium:** Meaningful delay, repeated effort, ongoing unresolved uncertainty, or required intervention or support.
- **High:** An important action is blocked, an account or function is inaccessible, a payment or process has materially failed, or a significant problem remains unresolved.

### Approved Severity principles

An Information Need does not automatically imply adverse customer impact. Use No Issue when the feedback does not describe an actual inconvenience, delay, repeated effort, blockage, failure, or other adverse impact.

Negative or emotional wording alone must not increase Severity. Severity must reflect explicit impact described in the feedback. Do not infer consequences that the customer did not state.
