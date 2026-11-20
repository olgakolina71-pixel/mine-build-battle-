# Architecture and build battle flow

## Components

1. **Architect** — API service sends a structured prompt to an OpenAI-compatible model endpoint and requests a voxel blueprint.
2. **Validator** — checks schema version, dimensions, coordinate range, duplicate positions, block allow-list and limits. Invalid designs are rejected.
3. **Blueprint artifact** — portable JSON; model/provider is not coupled to Minecraft.
4. **Bedrock executor** — behavior pack prototype places a local sample in tick batches. Generated blueprint transfer is not wired yet.
5. **QA loop (planned)** — capture a screenshot, compare against theme/blueprint, produce correction plan; human confirms before another build.
6. **Battle mode (planned)** — equal plots, theme, timer, same block budget; player build and AI build revealed after timer. YouTube viewers vote in comments.

## Current limitations

- Architect API is a separate service; it does not call the game yet.
- In-game script uses embedded starter blueprint.
- No automated image-based assessment yet.
- Avoid placing secrets in public repositories or Minecraft packs.

## Suggested battle rules

- Theme announced at start, fixed time limit.
- Same plot dimensions and optional block palette for both competitors.
- AI receives only the theme and constraints, not the player's build.
- No destructive actions; separate plots and backup world.
- Reveal both builds together; audience votes by comments.
