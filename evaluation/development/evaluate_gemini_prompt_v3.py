"""Run Prompt V3 on the locked 40-record development evaluation set.

Prepared only. Do not run until the targeted Prompt V3 wording is approved.
"""

import hashlib
import json
import os
from pathlib import Path

import pandas as pd
from google import genai
from google.genai import types

import evaluate_gemini_baseline as baseline


PROJECT_DIR = Path(__file__).resolve().parent
PROMPT_FILE = PROJECT_DIR / "evaluation_prompt_v3.md"
PREDICTIONS_FILE = PROJECT_DIR / "evaluation_gemini_prompt_v3_predictions.csv"
ERRORS_FILE = PROJECT_DIR / "evaluation_gemini_prompt_v3_errors.csv"
REPORT_FILE = PROJECT_DIR / "evaluation_gemini_prompt_v3_report.md"

FROZEN_DEVELOPMENT_HASHES = {
    "evaluate_gemini_baseline.py": "9ecce38a53b5382b8cdb65ad381ed223fb9279c1b6f4fdfa5c4b8fe2ad97f379",
    "evaluation_gemini_baseline_predictions.csv": "13c27d7a755d7c03ad47b3b8634f79f1a60022b41effa129283b674100f54c16",
    "evaluation_gemini_baseline_errors.csv": "22107026324d1f6efd6c2b21b57c99d42391d8ee2447995bb7101d225d00ea22",
    "evaluation_gemini_baseline_report.md": "e93414c05c8c219dbd0ef872d6b98fec49af493f25ba99f7e3c19c135dd84951",
    "evaluation_ground_truth_approved.csv": "595bbdf1b9195f2c119aac114362e2874dfd9ed1a875069775e5979d2eff1dc2",
    "evaluation_prompt_v2.md": "a646e9fc4214d690a57602cc565dfb58d0b8329add4185ae4990031d52db6d09",
    "evaluate_gemini_prompt_v2.py": "8eace9c76e568c5cb030c7327476ddf1499c28f18144b4f9a40a27bf89f978e3",
    "evaluation_gemini_prompt_v2_predictions.csv": "f645a2c95c2843a8346bba5edb271848a0075702656265789f4653df98033d51",
    "evaluation_gemini_prompt_v2_errors.csv": "40b2d0ba63d9bde0f9e0798561b224d40040c286f1727d2facc5f2ee31aa3e91",
    "evaluation_gemini_prompt_v2_report.md": "3358a9b5f9261c6046befdbf25e840a9704278a5ea7eae3d94aa2bb461f59854",
    "evaluation_prompt_v1_vs_v2_comparison.md": "6bad1cb87f5067230e7e810ee8a010e2fa247993b6f518bb5e26dc348afd7378",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_prompt() -> str:
    text = PROMPT_FILE.read_text(encoding="utf-8")
    start_marker = "<!-- PROMPT_START -->"
    end_marker = "<!-- PROMPT_END -->"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise ValueError("Prompt V3 markers are missing or duplicated.")
    prompt = text.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    if not prompt:
        raise ValueError("Prompt V3 is empty.")
    return prompt


def verify_frozen_development_artifacts() -> None:
    """Verify that every frozen V1/V2 development artifact is unchanged."""
    for name, expected_hash in FROZEN_DEVELOPMENT_HASHES.items():
        path = PROJECT_DIR / name
        if not path.exists() or sha256(path) != expected_hash:
            raise ValueError(f"Missing or changed frozen development artifact: {name}")


def preflight() -> tuple[pd.DataFrame, str]:
    verify_frozen_development_artifacts()

    existing = [
        path.name
        for path in [PREDICTIONS_FILE, ERRORS_FILE, REPORT_FILE]
        if path.exists()
    ]
    if existing:
        raise FileExistsError(
            "Prompt V3 output already exists; refusing to overwrite: "
            + ", ".join(existing)
        )

    ground_truth = pd.read_csv(
        baseline.GROUND_TRUTH_FILE,
        dtype=str,
        encoding="utf-8-sig",
        keep_default_na=False,
    )
    if len(ground_truth) != baseline.EVALUATION_SIZE:
        raise ValueError("The development reference must contain exactly 40 records.")
    if ground_truth["feedback_id"].duplicated().any():
        raise ValueError("The development reference contains duplicate feedback IDs.")
    return ground_truth, load_prompt()


def classify(items: list[dict[str, str]], instructions: str) -> list[dict[str, str]]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not available in this terminal.")

    client = genai.Client(api_key=api_key)
    prompt = (
        f"{instructions}\n\n"
        "Feedback items to classify (JSON):\n"
        f"{json.dumps(items, ensure_ascii=False)}"
    )
    response = client.models.generate_content(
        model=baseline.MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=baseline.SCHEMA,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned no classification text.")
    return json.loads(response.text)["classifications"]


def create_report(ground_truth: pd.DataFrame, predictions: pd.DataFrame) -> str:
    joined = ground_truth.merge(predictions, on="feedback_id", validate="one_to_one")
    agreements = baseline.agreement_table(joined)
    subgroup = baseline.subgroup_agreement(joined)
    full_match = pd.Series(True, index=joined.index)
    for human, predicted in [
        ("theme_ground_truth", "theme_prediction"),
        ("feedback_type_ground_truth", "feedback_type_prediction"),
        ("sentiment_ground_truth", "sentiment_prediction"),
        ("severity_ground_truth", "severity_prediction"),
    ]:
        full_match &= joined[human] == joined[predicted]
    exact = int(full_match.sum())

    errors = baseline.build_errors(joined)
    baseline.atomic_csv(errors, ERRORS_FILE)
    theme_metrics, theme_macro = baseline.class_metrics(
        joined, "theme_ground_truth", "theme_prediction", baseline.THEMES
    )
    type_metrics, type_macro = baseline.class_metrics(
        joined,
        "feedback_type_ground_truth",
        "feedback_type_prediction",
        baseline.FEEDBACK_TYPES,
    )

    agreement_frame = pd.DataFrame(agreements)
    agreement_frame["Agreement"] = agreement_frame.apply(
        lambda row: f"{int(row['correct'])}/40 ({row['percentage']:.1f}%)", axis=1
    )
    agreement_md = baseline.markdown_table(
        agreement_frame[["dimension", "Agreement"]].rename(columns={"dimension": "Dimension"})
    )
    subgroup_frame = pd.DataFrame(subgroup)
    subgroup_frame["Agreement"] = subgroup_frame.apply(
        lambda row: f"{int(row['correct'])}/{int(row['records'])} ({row['percentage']:.1f}%)",
        axis=1,
    )
    subgroup_md = baseline.markdown_table(
        subgroup_frame[["group", "dimension", "Agreement"]].rename(
            columns={"group": "Reference group", "dimension": "Dimension"}
        )
    )

    def metrics_md(frame: pd.DataFrame) -> str:
        shown = frame.copy()
        for column in ["Precision", "Recall", "F1"]:
            shown[column] = shown[column].map(lambda value: f"{value:.3f}")
        return baseline.markdown_table(shown)

    patterns = "\n".join(f"- {item}" for item in baseline.error_patterns(joined))
    return f"""# Gemini Prompt V3 Development Evaluation

## Methodology

- Locked development reference SHA-256: `{baseline.EXPECTED_GROUND_TRUTH_SHA256}`
- Model: `{baseline.MODEL}`
- Development-set size: 40
- API calls: 1
- Prompt version: `evaluation_prompt_v3.md`
- Gemini received only `feedback_id`, `feedback_text`, `channel`, and `journey_stage`.
- Predictions were validated and saved before comparison with human labels.

## Agreement by dimension

{agreement_md}

## All-fields exact match

{exact}/40 ({exact / 40 * 100:.1f}%)

## Clear vs Ambiguous agreement

{subgroup_md}

## Theme confusion matrix

{baseline.confusion_markdown(joined, "theme_ground_truth", "theme_prediction", baseline.THEMES)}

## Feedback Type confusion matrix

{baseline.confusion_markdown(joined, "feedback_type_ground_truth", "feedback_type_prediction", baseline.FEEDBACK_TYPES)}

## Sentiment confusion matrix

{baseline.confusion_markdown(joined, "sentiment_ground_truth", "sentiment_prediction", baseline.SENTIMENTS)}

## Severity confusion matrix

{baseline.confusion_markdown(joined, "severity_ground_truth", "severity_prediction", baseline.SEVERITIES)}

## Theme per-class metrics

{metrics_md(theme_metrics)}

Theme macro F1: **{theme_macro:.3f}**

## Feedback Type per-class metrics

{metrics_md(type_metrics)}

Feedback Type macro F1: **{type_macro:.3f}**

## Observed error patterns

{patterns}

Detailed mismatches are preserved in `{ERRORS_FILE.name}`.

## Interpretation caution

- These 40 records are a development evaluation set that informed Prompt V3.
- Results are not an unbiased final estimate of generalization.
- The separate locked holdout is reserved for one final evaluation after Prompt V3 is frozen.
- Dataset V2 is synthetic and the development set was selected for coverage and challenge.
"""


def main() -> None:
    ground_truth, instructions = preflight()
    items = baseline.build_blind_items(ground_truth)
    predictions = baseline.validate_predictions(
        classify(items, instructions), ground_truth["feedback_id"].tolist()
    )
    baseline.atomic_csv(predictions, PREDICTIONS_FILE)
    saved = pd.read_csv(PREDICTIONS_FILE, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    report = create_report(ground_truth, saved)
    temporary = REPORT_FILE.with_suffix(REPORT_FILE.suffix + ".tmp")
    temporary.write_text(report, encoding="utf-8")
    temporary.replace(REPORT_FILE)
    print(f"Model: {baseline.MODEL}")
    print("API calls: 1")
    print(f"Saved: {PREDICTIONS_FILE.name}")
    print(f"Saved: {ERRORS_FILE.name}")
    print(f"Saved: {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
