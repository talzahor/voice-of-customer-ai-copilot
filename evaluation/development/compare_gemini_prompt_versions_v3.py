"""Compare Baseline V1, Prompt V2, and Prompt V3 on the locked development set.

This script performs local analysis only. It does not call Gemini. Run it after
the Prompt V3 evaluation has produced its prediction file.
"""

from pathlib import Path

import pandas as pd

import evaluate_gemini_baseline as baseline
import evaluate_gemini_prompt_v3 as prompt_v3


PROJECT_DIR = Path(__file__).resolve().parent

V1_PREDICTIONS = PROJECT_DIR / "evaluation_gemini_baseline_predictions.csv"
V2_PREDICTIONS = PROJECT_DIR / "evaluation_gemini_prompt_v2_predictions.csv"
V3_PREDICTIONS = PROJECT_DIR / "evaluation_gemini_prompt_v3_predictions.csv"
OUTPUT_FILE = PROJECT_DIR / "evaluation_prompt_v1_v2_v3_comparison.md"

DIMENSIONS = {
    "Theme": ("theme_ground_truth", "theme_prediction", baseline.THEMES),
    "Feedback Type": (
        "feedback_type_ground_truth",
        "feedback_type_prediction",
        baseline.FEEDBACK_TYPES,
    ),
    "Sentiment": ("sentiment_ground_truth", "sentiment_prediction", baseline.SENTIMENTS),
    "Severity": ("severity_ground_truth", "severity_prediction", baseline.SEVERITIES),
}


def load_predictions(path: Path, expected_ids: list[str]) -> pd.DataFrame:
    """Load one prediction file and apply the evaluator's strict validation."""
    if not path.exists():
        raise FileNotFoundError(f"Required prediction file not found: {path.name}")

    predictions = pd.read_csv(path)
    records = predictions.to_dict(orient="records")
    baseline.validate_predictions(records, expected_ids)
    return predictions.set_index("feedback_id").loc[expected_ids]


def calculate_metrics(
    ground_truth: pd.DataFrame, predictions: pd.DataFrame
) -> dict[str, float]:
    """Calculate the same primary metrics used by the evaluators."""
    metrics: dict[str, float] = {}
    for dimension, (truth_column, prediction_column, _) in DIMENSIONS.items():
        metrics[f"{dimension} accuracy"] = float(
            ground_truth[truth_column].eq(predictions[prediction_column]).mean()
        )

    metrics["Exact-match accuracy"] = (
        pd.concat(
            [
                ground_truth[truth].eq(predictions[prediction])
                for truth, prediction, _ in DIMENSIONS.values()
            ],
            axis=1,
        )
        .all(axis=1)
        .mean()
    )
    joined = ground_truth.copy()
    for _, (_, prediction_column, _) in DIMENSIONS.items():
        joined[prediction_column] = predictions[prediction_column]
    _, metrics["Theme macro F1"] = baseline.class_metrics(
        joined,
        "theme_ground_truth",
        "theme_prediction",
        baseline.THEMES,
    )
    _, metrics["Feedback Type macro F1"] = baseline.class_metrics(
        joined,
        "feedback_type_ground_truth",
        "feedback_type_prediction",
        baseline.FEEDBACK_TYPES,
    )
    return metrics


def ambiguity_metrics(
    ground_truth: pd.DataFrame, predictions: pd.DataFrame
) -> list[dict[str, object]]:
    """Return exact-match results for Clear and Ambiguous development examples."""
    rows: list[dict[str, object]] = []
    exact_match = pd.concat(
        [
            ground_truth[truth].eq(predictions[prediction])
            for truth, prediction, _ in DIMENSIONS.values()
        ],
        axis=1,
    ).all(axis=1)
    for flag in ["Clear", "Ambiguous"]:
        mask = ground_truth["ambiguity_flag"].eq(flag)
        rows.append(
            {
                "Group": flag,
                "Records": int(mask.sum()),
                "Exact matches": int(exact_match[mask].sum()),
                "Exact-match accuracy": float(exact_match[mask].mean()),
            }
        )
    return rows


def field_change_analysis(
    ground_truth: pd.DataFrame,
    v1: pd.DataFrame,
    v2: pd.DataFrame,
    v3: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Describe V1-to-V3 outcomes and whether V2 changes persisted in V3."""
    v1_to_v3_rows: list[dict[str, str]] = []
    v2_change_rows: list[dict[str, str]] = []

    for feedback_id in ground_truth.index:
        for field, (truth_column, prediction_column, _) in DIMENSIONS.items():
            truth = ground_truth.at[feedback_id, truth_column]
            value_v1 = v1.at[feedback_id, prediction_column]
            value_v2 = v2.at[feedback_id, prediction_column]
            value_v3 = v3.at[feedback_id, prediction_column]

            if value_v1 != value_v3:
                if value_v1 != truth and value_v3 == truth:
                    outcome = "V1 error corrected by V3"
                elif value_v1 == truth and value_v3 != truth:
                    outcome = "V1-correct field regressed in V3"
                else:
                    outcome = "Changed, but V3 is still incorrect"
                v1_to_v3_rows.append(
                    {
                        "feedback_id": feedback_id,
                        "field": field,
                        "ground_truth": truth,
                        "V1": value_v1,
                        "V3": value_v3,
                        "outcome": outcome,
                    }
                )

            if value_v2 != value_v1:
                if value_v3 == value_v2:
                    disposition = "V2 change retained"
                elif value_v3 == value_v1:
                    disposition = "V2 change rejected"
                else:
                    disposition = "Different V3 outcome"
                v2_change_rows.append(
                    {
                        "feedback_id": feedback_id,
                        "field": field,
                        "V1": value_v1,
                        "V2": value_v2,
                        "V3": value_v3,
                        "disposition": disposition,
                    }
                )

    return pd.DataFrame(v1_to_v3_rows), pd.DataFrame(v2_change_rows)


def markdown_table(data: pd.DataFrame) -> str:
    """Render a small Markdown table without requiring an extra dependency."""
    if data.empty:
        return "_No rows._"

    display = data.copy()
    for column in display.columns:
        if "accuracy" in column.lower() or "f1" in column.lower():
            display[column] = display[column].map(
                lambda value: f"{value:.1%}" if isinstance(value, (float, int)) else value
            )

    headers = [str(column) for column in display.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in display.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    """Create the comparison report after all three development runs exist."""
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing comparison report: {OUTPUT_FILE.name}"
        )

    prompt_v3.verify_frozen_development_artifacts()
    ground_truth = pd.read_csv(baseline.GROUND_TRUTH_FILE).set_index("feedback_id")
    expected_ids = ground_truth.index.tolist()

    predictions = {
        "Baseline V1": load_predictions(V1_PREDICTIONS, expected_ids),
        "Prompt V2": load_predictions(V2_PREDICTIONS, expected_ids),
        "Prompt V3": load_predictions(V3_PREDICTIONS, expected_ids),
    }

    metric_rows = []
    ambiguity_rows = []
    for version, frame in predictions.items():
        metric_rows.append({"Version": version, **calculate_metrics(ground_truth, frame)})
        for row in ambiguity_metrics(ground_truth, frame):
            ambiguity_rows.append({"Version": version, **row})

    v1_to_v3, v2_changes = field_change_analysis(
        ground_truth,
        predictions["Baseline V1"],
        predictions["Prompt V2"],
        predictions["Prompt V3"],
    )

    report = f"""# Gemini Prompt V1 / V2 / V3 Development-Set Comparison

This report compares three prompt versions on the same locked 40-record development set. It is development evidence only; the untouched holdout is reserved for the final evaluation and must not be used to refine Prompt V3.

## Overall metrics

{markdown_table(pd.DataFrame(metric_rows))}

## Clear vs Ambiguous exact-match results

{markdown_table(pd.DataFrame(ambiguity_rows))}

## Field-level changes from Baseline V1 to Prompt V3

{markdown_table(v1_to_v3)}

## Disposition of fields changed by Prompt V2

{markdown_table(v2_changes)}

## Interpretation constraint

These results describe performance on the development set used for prompt refinement. They must not be treated as an unbiased estimate of final performance. Only the separately locked, untouched holdout can serve that purpose.
"""
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Saved comparison report: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
