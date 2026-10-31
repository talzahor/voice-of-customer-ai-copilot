"""Run the one-time final holdout evaluation with the frozen Baseline V1 prompt.

Preparation note: importing this module or running local_preflight() makes no API
call. Running main() performs the single precommitted Gemini holdout call.
"""

import hashlib
import json
import os
from pathlib import Path

import pandas as pd
from google import genai
from google.genai import types

import evaluate_gemini_baseline as baseline_v1


PROJECT_DIR = Path(__file__).resolve().parent
HOLDOUT_FILE = PROJECT_DIR / "evaluation_holdout_ground_truth_approved.csv"
PREDICTIONS_FILE = PROJECT_DIR / "evaluation_final_holdout_predictions.csv"
ERRORS_FILE = PROJECT_DIR / "evaluation_final_holdout_errors.csv"
REPORT_FILE = PROJECT_DIR / "evaluation_final_holdout_report.md"

MODEL = "gemini-3.5-flash-lite"
HOLDOUT_SIZE = 24
EXPECTED_IDS = [f"HOLD{number:03d}" for number in range(1, HOLDOUT_SIZE + 1)]
SOURCE_COLUMNS = ["feedback_id", "feedback_text", "channel", "journey_stage"]
EXPECTED_HOLDOUT_SHA256 = "a4e4f05216afab3c44768e00db81054807ad5f52ed742a940ed3bbe8ab557bab"
EXPECTED_SOURCE_SHA256 = "d51c2981b13a496308332a66750eb7180def071bc4be4d7937bbe9cd51a36b8f"
EXPECTED_INSTRUCTIONS_SHA256 = "e8d09795f14e9acd79d01d046e2b796d92f4b402858b9fda651d980cefbf6619"

FROZEN_V1_HASHES = {
    "evaluate_gemini_baseline.py": "9ecce38a53b5382b8cdb65ad381ed223fb9279c1b6f4fdfa5c4b8fe2ad97f379",
    "evaluation_ground_truth_approved.csv": "595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2",
    "evaluation_taxonomy_v2.md": "2a7841777f60bca31672ada32da26d6d305b552a47c496c4d66a3acd0c63a98f",
    "evaluation_gemini_baseline_predictions.csv": "13c27d7a755d7c03ad47b3b8634f79f1a60022b41effa129283b674100f54c16",
    "evaluation_gemini_baseline_errors.csv": "22107026324d1f6efd6c2b21b57c99d42391d8ee2447995bb7101d225d00ea22",
    "evaluation_gemini_baseline_report.md": "e93414c05c8c219dbd0ef872d6b98fec49af493f25ba99f7e3c19c135dd84951",
}

PREDICTION_COLUMNS = baseline_v1.PREDICTION_COLUMNS
SCHEMA = baseline_v1.SCHEMA
INSTRUCTIONS = baseline_v1.INSTRUCTIONS


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def source_field_hash(frame: pd.DataFrame) -> str:
    """Reproduce the canonical source-field hash used when locking the holdout."""
    rows = ["\x1f".join(row) for row in frame[SOURCE_COLUMNS].itertuples(index=False, name=None)]
    return sha256_bytes("\n".join(rows).encode("utf-8"))


def schema_contains_key(value: object, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(schema_contains_key(item, key) for item in value.values())
    if isinstance(value, list):
        return any(schema_contains_key(item, key) for item in value)
    return False


def verify_frozen_v1() -> None:
    """Verify the selected evaluator, development reference, and V1 results."""
    for filename, expected_hash in FROZEN_V1_HASHES.items():
        path = PROJECT_DIR / filename
        if not path.exists() or sha256_file(path) != expected_hash:
            raise ValueError(f"Missing or changed frozen Baseline V1 artifact: {filename}")
    if MODEL != baseline_v1.MODEL:
        raise ValueError("The final model differs from frozen Baseline V1.")
    if sha256_bytes(INSTRUCTIONS.encode("utf-8")) != EXPECTED_INSTRUCTIONS_SHA256:
        raise ValueError("The canonical Baseline V1 instructions have changed.")
    if schema_contains_key(SCHEMA, "minItems") or schema_contains_key(SCHEMA, "maxItems"):
        raise ValueError("The API schema must not contain minItems or maxItems.")


def verify_holdout() -> pd.DataFrame:
    """Verify the locked holdout without constructing a model request."""
    if not HOLDOUT_FILE.exists() or sha256_file(HOLDOUT_FILE) != EXPECTED_HOLDOUT_SHA256:
        raise ValueError("The approved holdout file is missing or its SHA-256 changed.")
    frame = pd.read_csv(HOLDOUT_FILE, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    if len(frame) != HOLDOUT_SIZE:
        raise ValueError(f"Expected exactly {HOLDOUT_SIZE} holdout records.")
    if frame["feedback_id"].tolist() != EXPECTED_IDS:
        raise ValueError("Holdout IDs must be HOLD001 through HOLD024 in order.")
    if frame["feedback_id"].duplicated().any():
        raise ValueError("The approved holdout contains duplicate IDs.")
    if frame.isna().any().any() or frame.eq("").any().any():
        raise ValueError("The approved holdout contains a missing required value.")
    if source_field_hash(frame) != EXPECTED_SOURCE_SHA256:
        raise ValueError("The approved holdout source-field SHA-256 changed.")
    label_checks = [
        ("theme_ground_truth", baseline_v1.THEMES),
        ("feedback_type_ground_truth", baseline_v1.FEEDBACK_TYPES),
        ("sentiment_ground_truth", baseline_v1.SENTIMENTS),
        ("severity_ground_truth", baseline_v1.SEVERITIES),
        ("ambiguity_flag", ["Clear", "Ambiguous"]),
    ]
    for column, allowed in label_checks:
        if not frame[column].isin(allowed).all():
            raise ValueError(f"The approved holdout contains an invalid value in {column}.")
    return frame


def build_blind_items(ground_truth: pd.DataFrame) -> list[dict[str, str]]:
    """Construct and verify the exact allowlisted Gemini payload records."""
    items = ground_truth[SOURCE_COLUMNS].to_dict(orient="records")
    expected_keys = set(SOURCE_COLUMNS)
    if len(items) != HOLDOUT_SIZE:
        raise ValueError(f"Expected {HOLDOUT_SIZE} outgoing records.")
    if any(set(item) != expected_keys for item in items):
        raise ValueError("Outgoing records contain non-allowlisted fields.")
    return items


def verify_output_paths() -> None:
    existing = [path.name for path in [PREDICTIONS_FILE, ERRORS_FILE, REPORT_FILE] if path.exists()]
    if existing:
        raise FileExistsError("Refusing to overwrite final holdout output: " + ", ".join(existing))


def local_preflight() -> tuple[pd.DataFrame, list[dict[str, str]]]:
    """Run every preparation safeguard without making an API call."""
    verify_frozen_v1()
    ground_truth = verify_holdout()
    items = build_blind_items(ground_truth)
    verify_output_paths()
    return ground_truth, items


def classify(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Make the single precommitted holdout call using frozen Baseline V1."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is unavailable. No API call was made.")
    client = genai.Client(api_key=api_key)
    prompt = (
        f"{INSTRUCTIONS}\n\n"
        "Feedback items to classify (JSON):\n"
        f"{json.dumps(items, ensure_ascii=False)}"
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=SCHEMA,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned no classification text.")
    return json.loads(response.text)["classifications"]


def validate_predictions(predictions: list[dict[str, str]]) -> pd.DataFrame:
    """Strictly validate all 24 predictions before saving or comparison."""
    if len(predictions) != HOLDOUT_SIZE:
        raise ValueError(f"Expected exactly {HOLDOUT_SIZE} predictions.")
    frame = pd.DataFrame(predictions)
    if set(frame.columns) != set(PREDICTION_COLUMNS):
        raise ValueError("Prediction fields do not match the required schema.")
    frame = frame[PREDICTION_COLUMNS]
    if frame.isna().any().any() or frame.eq("").any().any():
        raise ValueError("One or more prediction fields are missing.")
    if frame["feedback_id"].duplicated().any():
        raise ValueError("Gemini returned duplicate feedback IDs.")
    if set(frame["feedback_id"]) != set(EXPECTED_IDS):
        raise ValueError("Gemini returned missing or unexpected feedback IDs.")
    checks = [
        ("theme_prediction", baseline_v1.THEMES),
        ("feedback_type_prediction", baseline_v1.FEEDBACK_TYPES),
        ("sentiment_prediction", baseline_v1.SENTIMENTS),
        ("severity_prediction", baseline_v1.SEVERITIES),
    ]
    for column, allowed in checks:
        if not frame[column].isin(allowed).all():
            raise ValueError(f"Gemini returned an invalid value in {column}.")
    return frame.set_index("feedback_id").loc[EXPECTED_IDS].reset_index()


def agreement_rows(joined: pd.DataFrame) -> list[dict[str, object]]:
    dimensions = [
        ("Theme", "theme_ground_truth", "theme_prediction"),
        ("Feedback Type", "feedback_type_ground_truth", "feedback_type_prediction"),
        ("Sentiment", "sentiment_ground_truth", "sentiment_prediction"),
        ("Severity", "severity_ground_truth", "severity_prediction"),
    ]
    return [
        {
            "Dimension": name,
            "Correct": int(joined[truth].eq(joined[prediction]).sum()),
            "Accuracy": joined[truth].eq(joined[prediction]).mean(),
        }
        for name, truth, prediction in dimensions
    ]


def subgroup_rows(joined: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for flag in ["Clear", "Ambiguous"]:
        subset = joined[joined["ambiguity_flag"].eq(flag)]
        exact = (
            subset["theme_ground_truth"].eq(subset["theme_prediction"])
            & subset["feedback_type_ground_truth"].eq(subset["feedback_type_prediction"])
            & subset["sentiment_ground_truth"].eq(subset["sentiment_prediction"])
            & subset["severity_ground_truth"].eq(subset["severity_prediction"])
        )
        rows.append(
            {
                "Reference group": flag,
                "Records": len(subset),
                "Exact matches": int(exact.sum()),
                "Exact-match accuracy": exact.mean(),
            }
        )
    return rows


def format_percent_table(frame: pd.DataFrame) -> str:
    shown = frame.copy()
    for column in shown.columns:
        if "Accuracy" in column:
            shown[column] = shown[column].map(lambda value: f"{value:.1%}")
    return baseline_v1.markdown_table(shown)


def format_class_metrics(frame: pd.DataFrame) -> str:
    shown = frame.copy()
    for column in ["Precision", "Recall", "F1"]:
        shown[column] = shown[column].map(lambda value: f"{value:.3f}")
    return baseline_v1.markdown_table(shown)


def build_report(ground_truth: pd.DataFrame, predictions: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Compare locally only after the validated prediction artifact is saved."""
    joined = ground_truth.merge(predictions, on="feedback_id", validate="one_to_one")
    agreements = pd.DataFrame(agreement_rows(joined))
    exact = (
        joined["theme_ground_truth"].eq(joined["theme_prediction"])
        & joined["feedback_type_ground_truth"].eq(joined["feedback_type_prediction"])
        & joined["sentiment_ground_truth"].eq(joined["sentiment_prediction"])
        & joined["severity_ground_truth"].eq(joined["severity_prediction"])
    )
    errors = baseline_v1.build_errors(joined)
    theme_metrics, theme_macro = baseline_v1.class_metrics(
        joined, "theme_ground_truth", "theme_prediction", baseline_v1.THEMES
    )
    type_metrics, type_macro = baseline_v1.class_metrics(
        joined,
        "feedback_type_ground_truth",
        "feedback_type_prediction",
        baseline_v1.FEEDBACK_TYPES,
    )
    patterns = "\n".join(
        f"- {item.replace('this 40-record set', 'this 24-record holdout')}"
        for item in baseline_v1.error_patterns(joined)
    )
    report = f"""# Final Gemini Holdout Evaluation

## Methodology

- Final candidate: frozen Baseline V1
- Model: `{MODEL}`
- Holdout records: {HOLDOUT_SIZE}
- API calls: 1
- Approved holdout SHA-256: `{EXPECTED_HOLDOUT_SHA256}`
- Frozen V1 instructions SHA-256: `{EXPECTED_INSTRUCTIONS_SHA256}`
- Gemini received only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were schema-constrained, strictly validated, and saved before comparison with human labels.

The 40-record development set was used during prompt analysis and iteration, so its results are not unbiased generalization estimates. This 24-record holdout was locked before final-candidate selection and was not used for prompt refinement; it provides this project's final unseen-data evaluation.

## Accuracy by dimension

{format_percent_table(agreements)}

## All-fields exact match

{int(exact.sum())}/{HOLDOUT_SIZE} ({exact.mean():.1%})

## Clear vs Ambiguous exact match

{format_percent_table(pd.DataFrame(subgroup_rows(joined)))}

## Theme confusion matrix

{baseline_v1.confusion_markdown(joined, "theme_ground_truth", "theme_prediction", baseline_v1.THEMES)}

## Feedback Type confusion matrix

{baseline_v1.confusion_markdown(joined, "feedback_type_ground_truth", "feedback_type_prediction", baseline_v1.FEEDBACK_TYPES)}

## Sentiment confusion matrix

{baseline_v1.confusion_markdown(joined, "sentiment_ground_truth", "sentiment_prediction", baseline_v1.SENTIMENTS)}

## Severity confusion matrix

{baseline_v1.confusion_markdown(joined, "severity_ground_truth", "severity_prediction", baseline_v1.SEVERITIES)}

## Theme per-class metrics

{format_class_metrics(theme_metrics)}

Theme macro F1: **{theme_macro:.3f}**

## Feedback Type per-class metrics

{format_class_metrics(type_metrics)}

Feedback Type macro F1: **{type_macro:.3f}**

## Observed error patterns

{patterns}

The mismatch artifact lists individual disagreements descriptively. Human labels were not changed.

## Limitations

- Dataset V2 is synthetic.
- The holdout contains only 24 records and was designed for taxonomy coverage rather than real-world prevalence.
- Some human labels involve judgment, including records marked Ambiguous.
- These metrics must not be interpreted as production accuracy or evidence that the system is production-ready.
- No customer incidence, causation, business impact, or real-world prevalence can be inferred.

## No post-holdout optimization

The holdout results must not be used to modify Baseline V1 and rerun this same holdout as though it remained unseen. Any future prompt or model improvement requires a new untouched test set for another unbiased evaluation.
"""
    return errors, report


def atomic_text(text: str, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(destination)


def main() -> None:
    ground_truth, items = local_preflight()
    raw_predictions = classify(items)
    predictions = validate_predictions(raw_predictions)

    # Prediction-first safeguard: save validated predictions before reading labels for metrics.
    baseline_v1.atomic_csv(predictions, PREDICTIONS_FILE)

    locked_reference = verify_holdout()
    saved_predictions = pd.read_csv(
        PREDICTIONS_FILE, dtype=str, encoding="utf-8-sig", keep_default_na=False
    )
    errors, report = build_report(locked_reference, saved_predictions)
    baseline_v1.atomic_csv(errors, ERRORS_FILE)
    atomic_text(report, REPORT_FILE)
    print(f"Model: {MODEL}")
    print("API calls: 1")
    print(f"Saved: {PREDICTIONS_FILE.name}")
    print(f"Saved: {ERRORS_FILE.name}")
    print(f"Saved: {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
