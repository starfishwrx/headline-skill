# Review Rubric

Use this rubric after hard filters pass.

## Soft Score Dimensions

- `emotional_tension`: does the title create pull
- `concealment`: does it hide the thesis while surfacing the hook
- `specificity`: does it use a scene, a cost, a number, or a sharp detail
- `platform_fit`: does it sound native to the target platform
- `credibility`: is the promise believable
- `curiosity_gap`: does it create an open loop without becoming empty bait
- `rhythm`: does the line read with pace and shape

## Scoring Guidance

Use a 0 to 100 scale per dimension.

- `90-100`: strong, immediately usable
- `75-89`: viable, needs minor trimming
- `60-74`: promising but unstable
- `0-59`: weak or off-profile

## Automatic Rejection Rules

Reject a candidate even if its soft score is high when:

- it states the hidden thesis directly
- it reads like a summary, lesson, or chapter heading
- it contains banned words
- it makes an implausible promise
- it duplicates another stronger candidate
- it uses a tone the active profile forbids

## Human Review Prompts

Ask these questions in order:

1. What is being hidden
2. What is being surfaced
3. What exact feeling is doing the click work
4. Would the intended audience self-select into this line
5. Does the line still hold up if the reader is skeptical

## Output Standard

For each final candidate, keep:

- `title`
- `hook_family`
- `concealment_pattern`
- `hard_filter_result`
- `soft_scores`
- `selection_reason`
- `risk_notes`

The final output should include one winner, two to four alternatives, and the rejected list with reasons.
