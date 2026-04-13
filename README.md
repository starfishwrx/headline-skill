# Headline Skill

Reusable title workflow for Codex. It turns headline generation into a portable system instead of a one-off prompt.

## What It Solves

Most AI-written titles fail for the same reason: they summarize too early. This skill uses a fixed workflow that separates:

- universal method
- local taste
- deterministic checks

The result is a skill package other teams can fork and adapt without rewriting the process.

## Core Design

The package is split into three layers:

1. Universal workflow
   - brief normalization
   - hook route selection
   - candidate generation
   - hard filtering
   - soft review
   - winner selection
2. Replaceable profiles
   - platform rules
   - audience model
   - tone rules
   - banned words
   - hook families
   - scoring weights
3. Pluggable scorers
   - rhythm scoring is bundled
   - custom scorers can be added if they follow the scorer contract

## Directory Layout

```text
headline_skill/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
├── profiles/
├── scripts/
└── tests/
```

## Included Profiles

- `profiles/default_xiaohongshu.yaml`
- `profiles/example_bilibili.yaml`

They exist to prove the workflow is portable. The skill is not tied to one platform.

## Quick Start

### 1. Prepare a candidate file

The scripts expect JSON shaped like:

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

### 2. Run the hard filter

```bash
python scripts/hard_filter.py \
  --profile profiles/default_xiaohongshu.yaml \
  --input candidates.json
```

### 3. Run the rhythm scorer

```bash
python scripts/rhythm_scorer.py \
  --profile profiles/default_xiaohongshu.yaml \
  --input candidates.json
```

### 4. Merge and rank

```bash
python scripts/evaluate_candidates.py \
  --profile profiles/default_xiaohongshu.yaml \
  --input candidates.json
```

## How to Adapt It

### Replace the profile

Start by copying a profile file and editing:

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

### Replace the taste layer

If your team has its own title samples, add them into:

- `golden_examples`
- `negative_examples`

That is the fastest way to align local style without touching the orchestration.

### Add a custom scorer

Any scorer adapter should return:

- `title`
- `score_name`
- `numeric_score`
- `pass_fail`
- `reason`

Scores should stay on a `0-100` scale.

## Validation

Local validation:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -p "test_*.py"
```

## GitHub Actions

This repository ships with `.github/workflows/headline-skill-ci.yml`.

The workflow runs on pushes, pull requests, and manual dispatch for this repository. It checks:

- skill package structure
- profile schema basics
- `agents/openai.yaml`
- Python tests

## Output Contract

The expected final selection structure is:

- `winner`
- `alternatives`
- `rejected`
- per title `hook_family`
- per title `concealment_pattern`
- per title `hard_filter_result`
- per title `soft_scores`
- per title `selection_reason`
- per title `risk_notes`

## Why This Is Open-Source Friendly

The workflow is fixed. The taste is configurable. The checks are scriptable.

That lets other teams bring their own:

- audience
- platform
- banned words
- examples
- scoring logic

without forking the whole generation process.
