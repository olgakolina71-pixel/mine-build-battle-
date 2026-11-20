import { world, system } from "@minecraft/server";

const MAX_BLOCKS = 2000;
const BATCH_SIZE = 40;
const MAX_AXIS = 64;
const ALLOWED = new Set([
  "minecraft:air", "minecraft:oak_planks", "minecraft:oak_log", "minecraft:glass",
  "minecraft:stone", "minecraft:cobblestone", "minecraft:bricks", "minecraft:stone_bricks",
  "minecraft:oak_door", "minecraft:oak_leaves", "minecraft:torch", "minecraft:lantern",
  "minecraft:white_wool", "minecraft:red_wool", "minecraft:blue_wool",
  "minecraft:grass_block", "minecraft:dirt", "minecraft:sand", "minecraft:water"
]);

// Embedded MVP blueprint. Later the architect adapter will supply validated JSON.
const blueprint = {
  version: 1,
  name: "Starter House",
  size: { x: 9, y: 6, z: 9 },
  blocks: (() => {
    const out = [];
    for (let x = 0; x < 9; x++) for (let z = 0; z < 9; z++) {
      out.push({ x, y: 0, z, block: "minecraft:oak_planks" });
      if (x === 0 || x === 8 || z === 0 || z === 8)
        for (let y = 1; y <= 3; y++) out.push({ x, y, z, block: "minecraft:oak_planks" });
    }
    for (let x = 2; x <= 6; x++) for (let z = 2; z <= 6; z++)
      out.push({ x, y: 4, z, block: "minecraft:glass" });
    for (let x = 0; x < 9; x++) for (let z = 0; z < 9; z++)
      out.push({ x, y: 5, z, block: "minecraft:oak_planks" });
    // Door opening
    for (let y = 1; y <= 2; y++) out.push({ x: 4, y, z: 0, block: "minecraft:air" });
    return out;
  })()
};

function validate(bp) {
  if (!bp || bp.version !== 1 || !Array.isArray(bp.blocks)) throw new Error("Invalid blueprint format");
  const s = bp.size;
  if (!s || [s.x, s.y, s.z].some(n => !Number.isInteger(n) || n < 1 || n > MAX_AXIS))
    throw new Error("Dimensions must be integers from 1 to " + MAX_AXIS);
  if (bp.blocks.length > MAX_BLOCKS) throw new Error("Build exceeds " + MAX_BLOCKS + " blocks");
  const seen = new Set();
  for (const b of bp.blocks) {
    if (![b.x, b.y, b.z].every(Number.isInteger) || b.x < 0 || b.y < 0 || b.z < 0 ||
        b.x >= s.x || b.y >= s.y || b.z >= s.z) throw new Error("Block coordinate outside blueprint bounds");
    if (!ALLOWED.has(b.block)) throw new Error("Block not allowed: " + b.block);
    const key = b.x + "," + b.y + "," + b.z;
    if (seen.has(key)) throw new Error("Duplicate coordinate: " + key);
    seen.add(key);
  }
  return bp.blocks;
}

function startBuild(player) {
  let blocks;
  try { blocks = validate(blueprint); }
  catch (e) { player.sendMessage("§cBlueprint rejected: " + e.message); return; }

  const dim = player.dimension;
  const origin = {
    x: Math.floor(player.location.x) + 2,
    y: Math.floor(player.location.y),
    z: Math.floor(player.location.z) + 2
  };
  player.sendMessage("§aBuilding " + blueprint.name + " (" + blocks.length + " blocks)…");
  let i = 0;
  const runId = system.runInterval(() => {
    try {
      const end = Math.min(i + BATCH_SIZE, blocks.length);
      for (; i < end; i++) {
        const b = blocks[i];
        const pos = { x: origin.x + b.x, y: origin.y + b.y, z: origin.z + b.z };
        dim.getBlock(pos)?.setType(b.block);
      }
      if (i >= blocks.length) {
        system.clearRun(runId);
        player.sendMessage("§aDone! Blueprint placed.");
      }
    } catch (e) {
      system.clearRun(runId);
      player.sendMessage("§cBuild stopped: " + e.message);
    }
  }, 1);
}

world.afterEvents.chatSend.subscribe(({ message, sender }) => {
  if (message.trim().toLowerCase() === "!build") startBuild(sender);
});
world.afterEvents.playerSpawn.subscribe(({ player, initialSpawn }) => {
  if (initialSpawn) player.sendMessage("§eMine Build Battle: type §f!build§e to place the prototype.");
});
