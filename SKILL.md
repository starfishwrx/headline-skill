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
- Let anchor assets constrain title promises before generation
- Run deterministic hard filters before final selection
- Return structured outputs, not only a single winner

## Skill Layout

- `profiles/*.yaml`: structured profile bundles
- `profiles/*.editorial_playbook.md`: audience psychology, title role split, failure modes
- `profiles/*.benchmark_titles.txt`: external benchmark titles for review
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
2. Read the profile first.
   - Note `editorial_playbook`, `benchmark_titles`, and `review_tests`.
   - Load the playbook before generation when the profile provides one.
   - Save benchmark titles for the review stage. Do not stuff them into the first generation prompt.
3. Read the brief and normalize it to the schema in `references/profile_schema.md`.
   - Preserve `anchor_artifacts` when present.
   - Common anchors: highlights, opening hook, cover copy, quoted lines, first-screen text.
4. Read `references/framework.md` and extract:
   - core points
   - conflict
   - audience identity
   - desired emotion
   - hidden thesis
   - forbidden angles
   - anchor contract
5. If `anchor_artifacts` exist, do an anchor-first pass before route selection.
   - Name what the anchor already proves.
   - Name what the title still needs to promise.
   - Name what the title must not repeat or spoil.
   - Frame the larger unresolved problem behind the anchor instead of describing the anchor itself.
6. Choose 4 to 6 hook routes from the active profile.
7. Generate candidates route by route.
   - Each route should feel structurally distinct.
   - Avoid synonym shuffling.
8. Run hard checks:

```bash
python scripts/hard_filter.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

9. Run scorer adapters:

```bash
python scripts/rhythm_scorer.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

10. Merge and rank:

```bash
python scripts/evaluate_candidates.py --profile profiles/default_xiaohongshu.yaml --input candidates.json
```

11. Use `references/review_rubric.md` for final soft review.
    - Apply profile `review_tests`, especially honesty and shareability.
    - If a benchmark file exists, compare the candidate pool against those real titles.
    - Diagnose missing routes, weak phrasing, or candidates that only sound good in isolation.
12. Return structured output with:
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
- Treat anchor assets as constraints, not inspiration fluff.
- When anchors exist, titles should create a larger question that the anchor validates, not a paraphrase of the anchor.
- When benchmark titles exist, prefer external comparison over model self-congratulation.
- If the user wants a reusable setup for their own brand, guide them to copy and edit a profile instead of rewriting the workflow.
- If the user brings their own scorer, keep the scorer contract unchanged.

## Structured Candidate Input

The scripts expect a JSON file shaped like this:

```json
{
  "brief": {
    "platform": "xiaohongshu",
    "audience": "内容创业者",
    "content_summary": "为什么好的标题不能一上来讲中心思想",
    "core_points": [
      "好标题先放情绪钩子",
      "总结腔会削弱点击"
    ],
    "desired_emotion": "被说破",
    "hidden_thesis": "标题应该隐藏中心思想",
    "forbidden_angles": [
      "教学目录感"
    ],
    "length_range": [
      14,
      22
    ],
    "risk_level": "medium",
    "extra_context": "偏方法论",
    "anchor_artifacts": [
      {
        "type": "opening_hook",
        "content": "上来先讲结论的视频，往往最容易被划走",
        "notes": "标题不要重复这句话本身，要往更大的判断上提"
      }
    ]
  },
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
