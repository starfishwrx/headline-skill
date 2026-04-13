#!/usr/bin/env python3
"""Deterministic headline hard filters."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


WHITESPACE_RE = re.compile(r"\s+")
SPLIT_RE = re.compile(r"[，,。.!！？?：:；;、/|]")
REPEATED_PUNCT_RE = re.compile(r"([!！?？,，.。:：])\1{1,}")


def load_structured_file(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def normalize_title(title: str) -> str:
    compact = WHITESPACE_RE.sub("", title)
    return compact.lower()


def title_length(title: str) -> int:
    return len(normalize_title(title))


def bigrams(text: str) -> set[str]:
    norm = normalize_title(text)
    if len(norm) < 2:
        return {norm} if norm else set()
    return {norm[index : index + 2] for index in range(len(norm) - 1)}


def similarity(left: str, right: str) -> float:
    left_grams = bigrams(left)
    right_grams = bigrams(right)
    if not left_grams or not right_grams:
        return 0.0
    overlap = len(left_grams & right_grams)
    union = len(left_grams | right_grams)
    return overlap / union if union else 0.0


def detect_failures(title: str, profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    platform_rules = profile.get("platform_rules", {})

    length = title_length(title)
    hard_length = platform_rules.get("hard_length", [0, 999])
    if length < hard_length[0] or length > hard_length[1]:
        failures.append(f"length-out-of-range:{length}")

    preferred_length = platform_rules.get("preferred_length", hard_length)
    if length < preferred_length[0] or length > preferred_length[1]:
        warnings.append(f"length-outside-preferred:{length}")

    for word in profile.get("banned_words", []):
        if word and word in title:
            failures.append(f"banned-word:{word}")

    for pattern in platform_rules.get("summary_feel_patterns", []):
        if pattern and pattern in title:
            warnings.append(f"summary-feel:{pattern}")

    for pattern in platform_rules.get("overpromise_patterns", []):
        if pattern and pattern in title:
            warnings.append(f"overpromise:{pattern}")

    for mark in platform_rules.get("forbidden_punctuation", []):
        if mark and mark in title:
            failures.append(f"forbidden-punctuation:{mark}")

    if REPEATED_PUNCT_RE.search(title):
        warnings.append("repeated-punctuation")

    chunks = [chunk for chunk in SPLIT_RE.split(title) if chunk]
    if chunks and max(len(chunk) for chunk in chunks) > max(18, int(length * 0.9)):
        warnings.append("single-heavy-chunk")

    return failures, warnings


def apply_hard_filters(
    candidates: list[dict[str, Any]], profile: dict[str, Any]
) -> list[dict[str, Any]]:
    threshold = float(
        profile.get("platform_rules", {}).get("duplicate_similarity_threshold", 0.82)
    )
    results: list[dict[str, Any]] = []

    for index, candidate in enumerate(candidates):
        title = candidate.get("title", "").strip()
        failures, warnings = detect_failures(title, profile)

        duplicate_of: str | None = None
        for previous in results:
            score = similarity(title, previous["title"])
            if score >= threshold:
                duplicate_of = previous["title"]
                failures.append(f"duplicate-of:{previous['title']}")
                warnings.append(f"duplicate-similarity:{score:.2f}")
                break

        risk_notes = list(candidate.get("risk_notes", []))
        risk_notes.extend(failures)
        risk_notes.extend(item for item in warnings if item not in risk_notes)

        enriched = {
            **candidate,
            "title": title,
            "hard_filter_result": {
                "passed": not failures,
                "failures": failures,
                "warnings": warnings,
                "title_length": title_length(title),
                "duplicate_of": duplicate_of,
            },
            "risk_notes": risk_notes,
        }
        results.append(enriched)
        _ = index

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic headline hard filters.")
    parser.add_argument("--profile", required=True, help="Path to YAML or JSON profile.")
    parser.add_argument("--input", required=True, help="Path to JSON candidate file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = load_structured_file(args.profile)
    payload = load_structured_file(args.input)
    candidates = payload.get("candidates", [])
    results = apply_hard_filters(candidates, profile)
    print(
        json.dumps(
            {"candidates": results},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
