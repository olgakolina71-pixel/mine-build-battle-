# Mine Build Battle

An AI Minecraft Bedrock build-battle project: an architect produces a neutral JSON blueprint, a validator checks it, and a Bedrock behavior pack places the blocks.

## Current MVP
- Blueprint format: `blueprint.json`
- Validation: bounds, block allow-list, duplicates, and block-count limits
- Bedrock behavior pack with a sample build
- In-world trigger: type `!build` in chat to place the sample at the executor's location
- Placement is batched to avoid freezing the world

## Quick start (Bedrock)
1. Copy `bedrock-pack` into your Minecraft development_behavior_packs folder (or package it as a .mcpack).
2. Enable the behavior pack in a test world and enable Script API experiments if your version requires them.
3. Open the world and type `!build` in chat.

The MVP places the sample blueprint relative to the player. This is a prototype; use a backup world when testing.

## Blueprint format
```json
{
  "version": 1,
  "name": "Starter House",
  "size": {"x": 9, "y": 6, "z": 9},
  "blocks": [{"x": 0, "y": 0, "z": 0, "block": "minecraft:stone"}]
}
```
Coordinates are local, non-negative integers. The origin is the southwest-bottom corner.

## Roadmap
1. [x] Neutral blueprint schema + sample
2. [x] Bedrock batched executor prototype
3. [x] Blueprint validation and safety caps
4. [ ] Architect adapter (model/API)
5. [ ] Screenshot-based visual QA and repair loop
6. [ ] Battle timer, plots, and export/import

## Safety limits
The executor refuses builds above 2,000 blocks and limits each tick's batch. Only blocks in its allow-list are accepted.
