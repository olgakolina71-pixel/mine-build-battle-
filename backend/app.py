"""Blueprint API: generation, validation and export."""
import json
import os
import re
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from exporter import to_mcfunction

app = FastAPI(title="Mine Build Battle Architect", version="0.1.0")
MAX_BLOCKS = 2000
MAX_AXIS = 64
ALLOWED = {
    "minecraft:air", "minecraft:oak_planks", "minecraft:oak_log", "minecraft:glass",
    "minecraft:stone", "minecraft:cobblestone", "minecraft:bricks", "minecraft:stone_bricks",
    "minecraft:oak_door", "minecraft:oak_leaves", "minecraft:torch", "minecraft:lantern",
    "minecraft:white_wool", "minecraft:red_wool", "minecraft:blue_wool", "minecraft:grass_block",
    "minecraft:dirt", "minecraft:sand", "minecraft:water", "minecraft:spruce_planks"
}

class GenerateRequest(BaseModel):
    theme: str = Field(min_length=2, max_length=160)
    style: str = Field(default="detailed fantasy", max_length=80)
    size: int = Field(default=20, ge=5, le=40)
    block_budget: int = Field(default=1500, ge=50, le=MAX_BLOCKS)

def validate_blueprint(bp: dict) -> dict:
    if bp.get("version") != 1 or not isinstance(bp.get("blocks"), list):
        raise ValueError("Expected blueprint version 1 with blocks array")
    size = bp.get("size") or {}
    if any(type(size.get(k)) is not int or not 1 <= size[k] <= MAX_AXIS for k in "xyz"):
        raise ValueError("Size axes must be integers between 1 and 64")
    blocks = bp["blocks"]
    if len(blocks) > MAX_BLOCKS:
        raise ValueError("Block cap exceeded")
    seen = set()
    for b in blocks:
        if not isinstance(b, dict) or any(type(b.get(k)) is not int for k in "xyz"):
            raise ValueError("Coordinates must be integers")
        if any(b[k] < 0 or b[k] >= size[k] for k in "xyz"):
            raise ValueError("Coordinate out of bounds")
        if b.get("block") not in ALLOWED:
            raise ValueError(f"Block not allow-listed: {b.get('block')}")
        pos = (b["x"], b["y"], b["z"])
        if pos in seen:
            raise ValueError("Duplicate coordinate")
        seen.add(pos)
    return bp

@app.get("/health")
def health():
    return {"status": "ok", "provider_configured": bool(os.getenv("ARCHITECT_API_URL") and os.getenv("ARCHITECT_MODEL"))}

@app.post("/validate")
def validate(payload: dict):
    try:
        return {"valid": True, "blueprint": validate_blueprint(payload)}
    except ValueError as e:
        raise HTTPException(422, str(e))

@app.post("/export/mcfunction")
def export_mcfunction(payload: dict):
    try:
        content = to_mcfunction(payload)
        return {"filename": "generated_build.mcfunction", "content": content, "command_count": len(payload["blocks"])}
    except ValueError as e:
        raise HTTPException(422, str(e))

@app.post("/generate")
async def generate(req: GenerateRequest):
    api_url = os.getenv("ARCHITECT_API_URL")
    model = os.getenv("ARCHITECT_MODEL")
    key = os.getenv("ARCHITECT_API_KEY")
    if not api_url or not model:
        raise HTTPException(503, "Architect provider not configured. Set ARCHITECT_API_URL and ARCHITECT_MODEL.")
    prompt = f'''Create a Minecraft Bedrock build blueprint as JSON only. Theme: {req.theme}. Style: {req.style}. Dimensions: max {req.size} on each axis, origin at bottom corner. Total blocks <= {req.block_budget}. Use ONLY these block IDs: {sorted(ALLOWED)}. Format: {{"version":1,"name":"...","size":{{"x":N,"y":N,"z":N}},"blocks":[{{"x":0,"y":0,"z":0,"block":"minecraft:stone"}}]}}. Make it coherent, detailed, with foundation, walls, roof, entrances, windows, decoration. Coordinates integer and in bounds. Do not include duplicate coordinates or explanatory text.'''
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    body = {"model": model, "messages": [{"role": "system", "content": "You are an expert voxel architect. Return valid JSON and obey constraints."}, {"role": "user", "content": prompt}], "temperature": 0.7}
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(api_url, headers=headers, json=body)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise ValueError("Model response did not contain JSON")
        bp = validate_blueprint(json.loads(match.group(0)))
        if len(bp["blocks"]) > req.block_budget:
            raise ValueError("Generated blueprint exceeds requested block budget")
        return {"blueprint": bp, "validated": True, "block_count": len(bp["blocks"])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"Architect error: {type(e).__name__}: {e}")
