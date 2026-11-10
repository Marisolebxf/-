#!/usr/bin/env node
/**
 * Keep the three client adapters byte-identical.
 * Source of truth: agent-delivery/bugfix-runs/SKILL.md.
 *
 * Usage:
 *   node scripts/sync-bugfix-skill.mjs --check
 *   node scripts/sync-bugfix-skill.mjs --write
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = resolve(root, 'agent-delivery/bugfix-runs/SKILL.md');
const targets = [
  resolve(root, '.codex/skills/feishu-bugfix/SKILL.md'),
  resolve(root, '.cursor/skills/feishu-bugfix/SKILL.md'),
  resolve(root, '.trae/skills/feishu-bugfix/SKILL.md'),
];
const write = process.argv.includes('--write');
const check = process.argv.includes('--check') || !write;

if (!existsSync(source)) {
  console.error(`source missing: ${source}`);
  process.exitCode = 1;
} else {
  const expected = readFileSync(source);
  const mismatches = targets.filter((target) => !existsSync(target) || !expected.equals(readFileSync(target)));
  if (write) {
    for (const target of targets) writeFileSync(target, expected);
    console.log(`synced ${targets.length} Skill copies from ${source}`);
  } else if (mismatches.length) {
    console.error('Skill copies differ:');
    for (const target of mismatches) console.error(`- ${target}`);
    console.error('Run: node scripts/sync-bugfix-skill.mjs --write');
    process.exitCode = 2;
  } else {
    console.log(`Skill copies identical (${check ? 'check' : 'default'})`);
  }
}
