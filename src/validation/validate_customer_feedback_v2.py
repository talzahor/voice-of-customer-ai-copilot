"""Deterministic validation for the synthetic Dataset V2.

This script does not call an AI model and does not modify the CSV. It checks
the dataset structure, allowed source values, uniqueness, dates, and basic
feedback-text statistics.
"""

import csv
import statistics
from collections import Counter
from datetime import date
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_DIR / "customer_feedback_v2.csv"

REQUIRED_COLUMNS = [
    "feedback_id",
    "date",
    "channel",
    "journey_stage",
    "feedback_text",
]
VALID_CHANNELS = {
    "Post-Service Survey",
    "Chat",
    "App Review",
    "Support Call",
}
VALID_JOURNEY_STAGES = {
    "Claim Submission",
    "Claim Tracking",
    "Login & Account",
    "General Support",
    "Reimbursement",
}
EXPECTED_RECORDS = 150


def load_rows() -> list[dict[str, str]]:
    """Load V2 as text without altering values."""
    with INPUT_FILE.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(
                f"Expected columns {REQUIRED_COLUMNS}, found {reader.fieldnames}."
            )
        return list(reader)


def validate(rows: list[dict[str, str]]) -> dict[str, object]:
    """Run deterministic structural and quality checks."""
    if len(rows) != EXPECTED_RECORDS:
        raise ValueError(f"Expected {EXPECTED_RECORDS} rows, found {len(rows)}.")

    blank_cells = [
        (row_number, column)
        for row_number, row in enumerate(rows, start=2)
        for column in REQUIRED_COLUMNS
        if not row[column].strip()
    ]
    if blank_cells:
        raise ValueError(f"Missing required values: {blank_cells[:10]}")

    ids = [row["feedback_id"] for row in rows]
    if len(ids) != len(set(ids)):
        duplicates = [value for value, count in Counter(ids).items() if count > 1]
        raise ValueError(f"Duplicate feedback IDs: {duplicates}")

    invalid_channels = sorted({
        row["channel"] for row in rows if row["channel"] not in VALID_CHANNELS
    })
    if invalid_channels:
        raise ValueError(f"Invalid channels: {invalid_channels}")

    invalid_stages = sorted({
        row["journey_stage"]
        for row in rows
        if row["journey_stage"] not in VALID_JOURNEY_STAGES
    })
    if invalid_stages:
        raise ValueError(f"Invalid journey stages: {invalid_stages}")

    parsed_dates = []
    for row in rows:
        try:
            parsed_dates.append(date.fromisoformat(row["date"]))
        except ValueError as exc:
            raise ValueError(
                f"Invalid ISO date for {row['feedback_id']}: {row['date']}"
            ) from exc

    texts = [row["feedback_text"] for row in rows]
    unique_text_count = len(set(texts))
    duplicate_count = len(texts) - unique_text_count
    lengths = [len(text) for text in texts]
    word_counts = [len(text.split()) for text in texts]

    return {
        "records": len(rows),
        "unique_feedback_ids": len(set(ids)),
        "unique_feedback_texts": unique_text_count,
        "exact_duplicate_count": duplicate_count,
        "exact_duplicate_percentage": round(duplicate_count / len(rows) * 100, 1),
        "channels": dict(sorted(Counter(row["channel"] for row in rows).items())),
        "journey_stages": dict(
            sorted(Counter(row["journey_stage"] for row in rows).items())
        ),
        "date_range": [min(parsed_dates).isoformat(), max(parsed_dates).isoformat()],
        "text_length_characters": {
            "minimum": min(lengths),
            "median": round(statistics.median(lengths), 1),
            "mean": round(statistics.mean(lengths), 1),
            "maximum": max(lengths),
        },
        "text_length_words": {
            "minimum": min(word_counts),
            "median": round(statistics.median(word_counts), 1),
            "mean": round(statistics.mean(word_counts), 1),
            "maximum": max(word_counts),
        },
    }


def main() -> None:
    results = validate(load_rows())
    print("Dataset V2 validation passed")
    for label, value in results.items():
        print(f"{label}: {value}")


if __name__ == "__main__":
    main()
