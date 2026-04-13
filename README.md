# Headline Skill

[中文版说明](./README.zh-CN.md)

A reusable Codex skill for generating, reviewing, and selecting strong headlines with configurable profiles and pluggable scorers.

## What This Does

Headline Skill turns headline writing into a portable workflow instead of a fragile one-off prompt. It is built for teams that want to reuse the same process across different platforms, audiences, and content types without locking everyone into one writing style.

The core idea is simple: good headlines usually reveal tension before they reveal the thesis. This skill helps you keep that logic stable while making the taste layer replaceable.

### Key Features

- Configurable Profiles
  - Platform rules, audience model, tone constraints, banned words, and example packs all live in profiles.
- Structured Review
  - Candidates are filtered, scored, and ranked instead of being dumped as a loose list.
- Pluggable Scorers
  - Rhythm scoring is bundled. Custom scorers can be added through the same contract.
- Portable Workflow
  - The same orchestration works for Xiaohongshu, Bilibili, and any future profile you add.
- Regression-Friendly
  - Golden set cases and tests make it possible to improve the system without guessing.

## Installation

### Use as a Skill

Clone the repo into your Codex skills directory:

```bash
git clone https://github.com/starfishwrx/headline-skill.git ~/.codex/skills/headline-skill
```

### Use as a Standalone Repo

Clone the repo anywhere and install the only Python dependency:

```bash
git clone https://github.com/starfishwrx/headline-skill.git
cd headline-skill
python -m pip install -r requirements.txt
```

## Usage

### Generate and Review Headlines

Prepare a candidate JSON file:

```json
{
  "candidates": [
    {
      "title": "真正能打的标题，第一眼往往不讲重点",
      "hook_family": "tension-and-cost",
      "concealment_pattern": "hide-conclusion-show-tension",
      "soft_scores": {
        "emotional_tension": 88,
        "concealment": 90,
        "specificity": 72,
        "platform_fit": 92,
        "credibility": 78,
        "curiosity_gap": 82
      },
      "selection_reason": "",
      "risk_notes": []
    }
  ]
}
```

Run the evaluation chain:

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

### Customize a Profile

Copy one of the profiles under `profiles/` and edit:

- `platform_rules`
- `audience_model`
- `tone_rules`
- `hook_families`
- `bad_patterns`
- `banned_words`
- `score_weights`
- `golden_examples`
- `negative_examples`

The schema is documented in `references/profile_schema.md`.

### Add Your Own Scorer

Any custom scorer should return:

- `title`
- `score_name`
- `numeric_score`
- `pass_fail`
- `reason`

Scores should stay on a `0-100` scale so they can be merged with the bundled evaluators.

## Included Profiles

### Xiaohongshu

- `profiles/default_xiaohongshu.yaml`
- Prioritizes emotional pull, platform-native phrasing, and anti-summary behavior

### Bilibili

- `profiles/example_bilibili.yaml`
- Leans toward discussion-driven, judgment-heavy, slightly denser headline styles

## Architecture

This skill follows progressive disclosure. The main `SKILL.md` stays short and procedural, while supporting files are only read when needed:

| File | Purpose | Loaded When |
| --- | --- | --- |
| `SKILL.md` | Core workflow and invocation rules | Always |
| `references/framework.md` | Universal headline method | During strategy and generation |
| `references/profile_schema.md` | Profile contract | When adapting a profile |
| `references/review_rubric.md` | Soft review criteria | During selection |
| `scripts/hard_filter.py` | Deterministic filtering | Evaluation |
| `scripts/rhythm_scorer.py` | Numeric rhythm scoring | Evaluation |
| `scripts/evaluate_candidates.py` | Merge and ranking | Evaluation |
| `tests/golden_set.jsonl` | Regression set | Testing |

## Philosophy

This project is built on a few strong opinions:

1. Good headlines do not explain too early. They create pull first.
2. Taste should be configurable. Workflow should be reusable.
3. Rules belong in scripts when possible. They should not all live inside prompts.
4. If a system cannot be regression-tested, it will drift back toward bland output.

## Validation

Run the bundled validator and tests:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -p "test_*.py"
```

The repository also ships with `.github/workflows/headline-skill-ci.yml` so the same checks run in GitHub Actions.
