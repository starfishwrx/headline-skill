# Profile Schema

Profiles hold local taste. The workflow stays fixed.

## Purpose

Use a profile when you want the same skill to behave differently across platforms, brands, audiences, or editorial styles.

## File Format

Profiles may be YAML or JSON. The bundled examples use YAML.

## Core Bundle Fields

Bundled profiles are not only a YAML file. They are a small bundle: one structured profile plus optional long-form references that the workflow loads at different stages.

## Required Top-Level Fields

- `profile_name`: human-readable profile identifier
- `platform_rules`: structured platform constraints
- `audience_model`: reader identity and emotional state
- `tone_rules`: voice and style constraints
- `hook_families`: allowed headline routes
- `bad_patterns`: patterns to reject or penalize
- `banned_words`: direct lexical bans
- `score_weights`: ranking weights
- `review_tests`: final gate questions with fail conditions
- `golden_examples`: positive examples with notes
- `negative_examples`: negative examples with notes

## Strongly Recommended Bundle Fields

- `editorial_playbook`: repo-relative path to a long-form markdown playbook
- `benchmark_titles`: repo-relative path to a plain-text title benchmark file

The workflow should still run without these files, but bundled profiles should provide them.

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
- `anchor_artifacts`

`anchor_artifacts` is a list of objects. Use it when you already know what the audience will see early, such as:

- highlights
- opening hook
- cover copy
- quoted lines

Each item should include:

- `type`
- `content`
- `notes`

If `anchor_artifacts` exist, generation should reason from those anchors outward.

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

## `review_tests`

Each item should include:

- `name`
- `question`
- `fail_if`

Bundled profiles should always include at least:

- `honesty`: does the content truly cash the title check
- `shareability`: would a discerning user feel good forwarding it

## `golden_examples` and `negative_examples`

Each example should include:

- `title`
- `why_it_works` or `why_it_fails`
- `hook_family`
- `concealment_pattern`

## `editorial_playbook`

Use markdown. This file is the long-form cognition layer for the profile.

Good playbooks usually include:

- who the audience is when they arrive
- what they want emotionally and cognitively
- what the title is responsible for
- how titles should split work with anchor assets, covers, or openings
- common failure modes
- notes about platform-native pacing or tone

Keep it judgment-heavy. This is not a generic style guide.

## `benchmark_titles`

Use plain text with one real or representative title per line.

Good benchmark files usually:

- contain 10 to 30 titles
- reflect the actual performance bar for this profile
- cover multiple routes instead of one sentence pattern
- bias toward titles that really worked, not titles that merely sound clever

Use this file in review, not as a first-pass imitation template.

## Scorer Adapter Contract

Any custom scorer should return a list of objects with:

- `title`
- `score_name`
- `numeric_score`
- `pass_fail`
- `reason`

Scores should stay on a 0 to 100 scale.
