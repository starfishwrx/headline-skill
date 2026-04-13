---
name: headline-skill
description: "Create, review, and select high-performing content titles or headlines from a structured brief. Use when the user wants titles for Xiaohongshu, Bilibili, articles, videos, hooks, or reusable headline workflows with configurable profiles and scorer adapters."
metadata:
  requires:
    bins: ["python"]
---

# Headline Skill

Use this skill when the user wants a repeatable title workflow rather than a one-off title suggestion.

## What This Skill Owns

- Turn a brief into multiple headline candidates
- Keep the workflow reusable across platforms and audiences
- Separate universal process from local taste
- Run deterministic hard filters before final selection
- Return structured outputs, not only a single winner

## Skill Layout

- `profiles/*.yaml`: platform and audience profiles
- `references/framework.md`: universal title method
- `references/profile_schema.md`: how to define a new profile
- `references/review_rubric.md`: soft review rubric and rejection rules
- `scripts/hard_filter.py`: banned words, length, duplicate, summary-feel checks
- `scripts/rhythm_scorer.py`: numeric rhythm scorer
- `scripts/evaluate_candidates.py`: merge hard checks and scorer outputs into ranked results
- `scripts/validate_skill.py`: CI-friendly package validator
- `tests/golden_set.jsonl`: portable regression set

## Default Workflow

1. Pick a profile.
   - If the user provides a profile path, use it.
   - Otherwise default to `profiles/default_xiaohongshu.yaml`.
2. Read the brief and normalize it to the schema in `references/profile_schema.md`.
3. Read `references/framework.md` and extract:
   - core points
   - conflict
   - audience identity
   - desired emotion
   - hidden thesis
   - forbidden angles
4. Choose 4 to 6 hook routes from the active profile.
5. Generate candidates route by route.
   - Each route should feel structurally distinct.
   - Avoid synonym shuffling.
6. Run hard checks:

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

7. Run scorer adapters:

```bash
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

8. Merge and rank:

```bash
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

9. Use `references/review_rubric.md` for final soft review.
10. Return structured output with:
    - `winner`
    - `alternatives`
    - `rejected`
    - per-title `hook_family`
    - per-title `concealment_pattern`
    - per-title `hard_filter_result`
    - per-title `soft_scores`
    - per-title `selection_reason`
    - per-title `risk_notes`

## Operating Rules

- Read the profile before reading the long references.
- Do not dump the full profile into one huge prompt. Pull only the active constraints.
- Keep generation and review separate. First broaden, then filter, then review.
- If the user wants a reusable setup for their own brand, guide them to copy and edit a profile instead of rewriting the workflow.
- If the user brings their own scorer, keep the scorer contract unchanged.

## Structured Candidate Input

The scripts expect a JSON file shaped like this:

```json
{
  "candidates": [
    {
      "title": "这条内容为什么一发就有人转发",
      "hook_family": "curiosity-gap",
      "concealment_pattern": "hide-conclusion-show-tension",
      "soft_scores": {
        "emotional_tension": 84,
        "concealment": 88,
        "specificity": 70,
        "platform_fit": 92,
        "credibility": 66
      },
      "selection_reason": "",
      "risk_notes": []
    }
  ]
}
```

## When to Read More

- Need title strategy details: `references/framework.md`
- Need to define a custom profile: `references/profile_schema.md`
- Need final review rules: `references/review_rubric.md`
- Need deterministic scoring details: `scripts/*.py`
