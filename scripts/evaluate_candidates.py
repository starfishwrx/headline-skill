#!/usr/bin/env python3
"""Merge hard filters and scorer outputs into ranked title results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from hard_filter import apply_hard_filters, load_structured_file  # noqa: E402
from rhythm_scorer import score_title  # noqa: E402


def normalize_weights(raw_weights: dict[str, float]) -> dict[str, float]:
    total = sum(float(value) for value in raw_weights.values()) or 1.0
    return {key: float(value) / total for key, value in raw_weights.items()}


def compute_weighted_score(candidate: dict[str, Any], weights: dict[str, float]) -> float:
    score_map = dict(candidate.get("soft_scores", {}))
    rhythm = candidate.get("scorer_results", {}).get("rhythm", {})
    if rhythm:
        score_map["rhythm"] = rhythm.get("numeric_score", 0.0)

    total = 0.0
    for name, weight in weights.items():
        total += float(score_map.get(name, 0.0)) * weight
    return round(total, 2)


def evaluate(candidates: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    filtered = apply_hard_filters(candidates, profile)
    weights = normalize_weights(profile.get("score_weights", {"rhythm": 1.0}))

    ranked: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate in filtered:
        rhythm_result = score_title(candidate["title"], profile)
        enriched = {
            **candidate,
            "scorer_results": {
                "rhythm": rhythm_result,
            },
        }
        total_score = compute_weighted_score(enriched, weights)
        enriched["total_score"] = total_score
        if candidate["hard_filter_result"]["passed"]:
            ranked.append(enriched)
        else:
            rejected.append(enriched)

    ranked.sort(
        key=lambda item: (
            item["total_score"],
            item["scorer_results"]["rhythm"]["numeric_score"],
            -len(item.get("risk_notes", [])),
        ),
        reverse=True,
    )

    return {
        "winner": ranked[0] if ranked else None,
        "alternatives": ranked[1:4],
        "rejected": rejected + ranked[4:],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate headline candidates.")
    parser.add_argument("--profile", required=True, help="Path to YAML or JSON profile.")
    parser.add_argument("--input", required=True, help="Path to JSON candidate file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = load_structured_file(args.profile)
    payload = load_structured_file(args.input)
    candidates = payload.get("candidates", [])
    print(json.dumps(evaluate(candidates, profile), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
