#!/usr/bin/env python3
"""Numeric rhythm scorer for headlines."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

import yaml


PUNCTUATION_CHARS = ",.!?:;/?|"
UNICODE_PUNCTUATION = "\uFF0C\u3002\uFF01\uFF1F\uFF1A\uFF1B\u3001"
SPLIT_RE = re.compile(r"[\uFF0C,\u3002\.!\uFF01\uFF1F\?\uFF1A:\uFF1B;\u3001/|]")


def load_structured_file(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def compact_length(text: str) -> int:
    return len("".join(text.split()))


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def length_score(title: str, preferred: list[int]) -> tuple[float, str]:
    length = compact_length(title)
    center = sum(preferred) / 2
    tolerance = max(1.0, (preferred[1] - preferred[0]) / 2)
    distance = abs(length - center)
    score = 35.0 - min(35.0, (distance / max(1.0, tolerance)) * 20.0)
    reason = f"length={length}, preferred={preferred}"
    return score, reason


def chunk_score(title: str) -> tuple[float, str]:
    chunks = [chunk for chunk in SPLIT_RE.split(title) if chunk]
    if not chunks:
        chunks = [title]
    lengths = [compact_length(chunk) for chunk in chunks]
    if len(lengths) == 1:
        score = 18.0 if 8 <= lengths[0] <= 18 else 10.0
        return score, f"single-chunk:{lengths[0]}"
    avg = sum(lengths) / len(lengths)
    variance = sum((value - avg) ** 2 for value in lengths) / len(lengths)
    std = math.sqrt(variance)
    score = 25.0 - min(18.0, std * 3.0) - max(0.0, len(lengths) - 3) * 4.0
    return score, f"chunks={lengths}"


def punctuation_score(title: str, preferred_punctuation: list[str]) -> tuple[float, str]:
    used = [mark for mark in preferred_punctuation if mark in title]
    punctuation_count = sum(
        1 for char in title if char in (PUNCTUATION_CHARS + UNICODE_PUNCTUATION)
    )
    score = 20.0
    if punctuation_count == 0:
        score -= 6.0
    elif punctuation_count > 3:
        score -= (punctuation_count - 3) * 4.0
    if used:
        score += min(6.0, len(used) * 3.0)
    return score, f"punctuation_count={punctuation_count}, preferred_hits={len(used)}"


def texture_score(title: str) -> tuple[float, str]:
    unique_chars = len(set(title))
    length = max(1, len(title))
    ratio = unique_chars / length
    score = 20.0
    if ratio < 0.45:
        score -= 8.0
    if re.search(r"(.)\1{2,}", title):
        score -= 10.0
        return score, f"unique_ratio={ratio:.2f}, repeated-char"
    return score, f"unique_ratio={ratio:.2f}"


def score_title(title: str, profile: dict[str, Any]) -> dict[str, Any]:
    rules = profile.get("platform_rules", {})
    preferred = rules.get("preferred_length", [12, 24])
    preferred_punctuation = rules.get("preferred_punctuation", [])

    length_component, length_reason = length_score(title, preferred)
    chunk_component, chunk_reason = chunk_score(title)
    punctuation_component, punctuation_reason = punctuation_score(
        title, preferred_punctuation
    )
    texture_component, texture_reason = texture_score(title)

    numeric_score = clamp(
        length_component + chunk_component + punctuation_component + texture_component
    )
    pass_fail = numeric_score >= 60.0
    reason = "; ".join(
        [
            length_reason,
            chunk_reason,
            punctuation_reason,
            texture_reason,
        ]
    )
    return {
        "title": title,
        "score_name": "rhythm",
        "numeric_score": round(numeric_score, 2),
        "pass_fail": pass_fail,
        "reason": reason,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score title rhythm.")
    parser.add_argument("--profile", required=True, help="Path to YAML or JSON profile.")
    parser.add_argument("--input", required=True, help="Path to JSON candidate file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = load_structured_file(args.profile)
    payload = load_structured_file(args.input)
    candidates = payload.get("candidates", [])
    results = [score_title(item.get("title", ""), profile) for item in candidates]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
