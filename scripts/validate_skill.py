#!/usr/bin/env python3
"""Validate the headline skill package in a CI-friendly way."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/framework.md",
    "references/profile_schema.md",
    "references/review_rubric.md",
    "profiles/default_xiaohongshu.yaml",
    "profiles/example_bilibili.yaml",
    "scripts/hard_filter.py",
    "scripts/rhythm_scorer.py",
    "scripts/evaluate_candidates.py",
    "tests/golden_set.jsonl",
    "tests/test_headline_skill.py",
]

REQUIRED_PROFILE_KEYS = {
    "profile_name",
    "platform_rules",
    "audience_model",
    "tone_rules",
    "hook_families",
    "bad_patterns",
    "banned_words",
    "score_weights",
    "golden_examples",
    "negative_examples",
}

REQUIRED_AGENT_FIELDS = {
    "display_name",
    "short_description",
    "default_prompt",
}


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_frontmatter(skill_md: Path) -> list[str]:
    errors: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return ["SKILL.md is missing YAML frontmatter"]

    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        return ["SKILL.md frontmatter must be a mapping"]

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not re.match(r"^[a-z0-9-]+$", name):
        errors.append("SKILL.md frontmatter.name must be lower hyphen-case")
    if not isinstance(description, str) or len(description.strip()) < 20:
        errors.append("SKILL.md frontmatter.description must be a useful string")
    return errors


def validate_agents_yaml(path: Path) -> list[str]:
    errors: list[str] = []
    data = read_yaml(path)
    interface = data.get("interface")
    if not isinstance(interface, dict):
        return ["agents/openai.yaml must contain interface mapping"]

    missing = REQUIRED_AGENT_FIELDS - set(interface.keys())
    if missing:
        errors.append(f"agents/openai.yaml missing fields: {sorted(missing)}")

    default_prompt = interface.get("default_prompt", "")
    if "$headline-skill" not in str(default_prompt):
        errors.append("agents/openai.yaml default_prompt must mention $headline-skill")
    return errors


def validate_profile(path: Path) -> list[str]:
    errors: list[str] = []
    data = read_yaml(path)
    missing = REQUIRED_PROFILE_KEYS - set(data.keys())
    if missing:
        errors.append(f"{path.name} missing keys: {sorted(missing)}")

    hook_families = data.get("hook_families", [])
    if not isinstance(hook_families, list) or len(hook_families) < 3:
        errors.append(f"{path.name} must define at least 3 hook families")

    weights = data.get("score_weights", {})
    if not isinstance(weights, dict) or "rhythm" not in weights:
        errors.append(f"{path.name} score_weights must include rhythm")
    return errors


def validate_golden_set(path: Path) -> list[str]:
    errors: list[str] = []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 30:
        errors.append("tests/golden_set.jsonl must contain at least 30 rows")
    return errors


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_SKILL_FILES:
        target = skill_dir / relative
        if not target.exists():
            errors.append(f"missing required file: {relative}")

    if errors:
        return errors

    errors.extend(validate_frontmatter(skill_dir / "SKILL.md"))
    errors.extend(validate_agents_yaml(skill_dir / "agents" / "openai.yaml"))
    errors.extend(validate_profile(skill_dir / "profiles" / "default_xiaohongshu.yaml"))
    errors.extend(validate_profile(skill_dir / "profiles" / "example_bilibili.yaml"))
    errors.extend(validate_golden_set(skill_dir / "tests" / "golden_set.jsonl"))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate headline skill structure.")
    parser.add_argument("skill_dir", help="Path to headline_skill directory")
    args = parser.parse_args()

    errors = validate_skill_dir(Path(args.skill_dir))
    if errors:
        for item in errors:
            print(f"[ERROR] {item}")
        raise SystemExit(1)

    print("[OK] headline_skill validation passed")


if __name__ == "__main__":
    main()
