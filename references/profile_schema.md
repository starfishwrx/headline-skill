# Profile Schema

Profiles hold local taste. The workflow stays fixed.

## Purpose

Use a profile when you want the same skill to behave differently across platforms, brands, audiences, or editorial styles.

## File Format

Profiles may be YAML or JSON. The bundled examples use YAML.

## Required Top-Level Fields

- `profile_name`: human-readable profile identifier
- `platform_rules`: structured platform constraints
- `audience_model`: reader identity and emotional state
- `tone_rules`: voice and style constraints
- `hook_families`: allowed headline routes
- `bad_patterns`: patterns to reject or penalize
- `banned_words`: direct lexical bans
- `score_weights`: ranking weights
- `golden_examples`: positive examples with notes
- `negative_examples`: negative examples with notes

## Recommended Brief Schema

The title workflow should normalize incoming input into:

- `platform`
- `audience`
- `content_summary`
- `core_points`
- `desired_emotion`
- `hidden_thesis`
- `forbidden_angles`
- `length_range`
- `risk_level`
- `extra_context`

## `platform_rules`

Recommended fields:

- `language`
- `hard_length`
- `preferred_length`
- `route_count`
- `preferred_punctuation`
- `forbidden_punctuation`
- `summary_feel_patterns`
- `overpromise_patterns`
- `duplicate_similarity_threshold`

## `audience_model`

Recommended fields:

- `identity`
- `current_state`
- `desired_state`
- `sensitivity`
- `emotional_triggers`

## `tone_rules`

Recommended fields:

- `voice`
- `emotional_temperature`
- `preferred_register`
- `avoid_register`
- `summary_avoidance`
- `credibility_floor`

## `hook_families`

Each item should include:

- `name`
- `description`
- `preferred_use`
- `avoid_when`
- `prompt_hint`

## `score_weights`

Use normalized numeric weights. The merger script will normalize them again if needed.

Suggested dimensions:

- `emotional_tension`
- `concealment`
- `specificity`
- `platform_fit`
- `credibility`
- `curiosity_gap`
- `rhythm`

## `golden_examples` and `negative_examples`

Each example should include:

- `title`
- `why_it_works` or `why_it_fails`
- `hook_family`
- `concealment_pattern`

## Scorer Adapter Contract

Any custom scorer should return a list of objects with:

- `title`
- `score_name`
- `numeric_score`
- `pass_fail`
- `reason`

Scores should stay on a 0 to 100 scale.
