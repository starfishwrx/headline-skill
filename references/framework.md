# Universal Headline Framework

This framework treats a good headline as controlled asymmetry: hide the thesis, expose the emotional hook.

## Core Principle

Strong headlines rarely state the center idea in plain summary form. They release a feeling, a conflict, a cost, a tension, or a surprise. The click happens because the audience senses movement before they receive closure.

## Inputs to Extract From Any Brief

- `core_points`: what is actually true
- `conflict`: what rubs against intuition, cost, risk, identity, or desire
- `audience_identity`: who this title is speaking to
- `desired_emotion`: curiosity, relief, urgency, envy, recognition, fear, validation
- `hidden_thesis`: the real point that should stay partially concealed
- `forbidden_angles`: what would make the title sound fake, summary-like, preachy, or salesy

## Hook Families

Each candidate should belong to one hook family. Use several families in parallel.

- `curiosity-gap`: show the gap, hide the answer
- `identity-mirror`: make the right reader feel seen
- `tension-and-cost`: expose friction, tradeoff, or hidden price
- `unexpected-reversal`: flip a common assumption
- `specific-scene`: reveal a concrete moment instead of a conclusion
- `emotion-first`: lead with feeling, not concept
- `status-signal`: imply taste, judgment, experience, or insider awareness
- `practical-trigger`: point to a real use case without sounding like a tutorial title

## Concealment Patterns

- `hide-conclusion-show-tension`: keep the answer back, reveal the conflict
- `hide-framework-show-scene`: avoid naming the method, show the moment
- `hide-benefit-show-cost`: imply reward through the pain point
- `hide-lesson-show-mistake`: imply the takeaway through the failure
- `hide-claim-show-observation`: show an observation that makes the claim obvious later

## Bad Patterns

These patterns make titles collapse into summary copy:

- Naming the center idea too early
- Over-explaining the benefit
- Sounding like a course page or a consulting pitch
- Stacking abstractions without a scene
- Using generic self-media filler such as 干货, 分享, 教你, 保姆级 when the profile rejects them
- Generating five versions of the same sentence with light paraphrase

## Route Selection Rules

For one brief, pick 4 to 6 routes with visible structural separation.

- At least one route should lean emotional
- At least one route should lean scene or specificity
- At least one route should lean identity or judgment
- Do not let more than two routes share the same sentence skeleton

## Suggested LLM Prompt Skeleton

Use this as a working shape, not a fixed literal prompt:

1. Restate the brief in normalized fields.
2. Name the hidden thesis.
3. Name the emotion to surface.
4. Pick distinct hook families.
5. Generate by family, one compact cluster at a time.
6. After generation, review for summary-feel and over-exposure before any script runs.

## Final Review Questions

- Does the title leak the whole thesis too early
- Does it feel like a summary rather than a hook
- Does it sound like the target platform
- Would the right reader feel tension, recognition, or pull
- Is the promise credible
- Is the expression concrete enough to survive platform competition
