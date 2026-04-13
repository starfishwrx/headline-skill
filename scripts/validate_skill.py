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
    "profiles/default_xiaohongshu.editorial_playbook.md",
    "profiles/default_xiaohongshu.benchmark_titles.txt",
    "profiles/example_bilibili.yaml",
    "profiles/example_bilibili.editorial_playbook.md",
    "profiles/example_bilibili.benchmark_titles.txt",
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
    "review_tests",
    "golden_examples",
    "negative_examples",
    "editorial_playbook",
    "benchmark_titles",
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

    review_tests = data.get("review_tests", [])
    if not isinstance(review_tests, list) or len(review_tests) < 2:
        errors.append(f"{path.name} must define at least 2 review_tests")
    else:
        names = {item.get("name") for item in review_tests if isinstance(item, dict)}
        for required_name in {"honesty", "shareability"}:
            if required_name not in names:
                errors.append(f"{path.name} review_tests must include {required_name}")

    for key in ("editorial_playbook", "benchmark_titles"):
        target = data.get(key)
        if not isinstance(target, str) or not target.strip():
            errors.append(f"{path.name} must define {key}")
    return errors


def validate_golden_set(path: Path) -> list[str]:
    errors: list[str] = []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 30:
        errors.append("tests/golden_set.jsonl must contain at least 30 rows")
    return errors


def validate_profile_assets(skill_dir: Path, profile_path: Path) -> list[str]:
    errors: list[str] = []
    data = read_yaml(profile_path)

    playbook = skill_dir / str(data.get("editorial_playbook", ""))
    if not playbook.exists():
        errors.append(f"{profile_path.name} editorial_playbook target is missing")
    elif len(playbook.read_text(encoding="utf-8").strip()) < 80:
        errors.append(f"{profile_path.name} editorial_playbook looks too short")

    benchmark = skill_dir / str(data.get("benchmark_titles", ""))
    if not benchmark.exists():
        errors.append(f"{profile_path.name} benchmark_titles target is missing")
    else:
        lines = [line for line in benchmark.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) < 5:
            errors.append(f"{profile_path.name} benchmark_titles should contain at least 5 titles")

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
    xhs_profile = skill_dir / "profiles" / "default_xiaohongshu.yaml"
    bili_profile = skill_dir / "profiles" / "example_bilibili.yaml"
    errors.extend(validate_profile(xhs_profile))
    errors.extend(validate_profile(bili_profile))
    errors.extend(validate_profile_assets(skill_dir, xhs_profile))
    errors.extend(validate_profile_assets(skill_dir, bili_profile))
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
