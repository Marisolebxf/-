#!/usr/bin/env node
/**
 * Generate thin client adapters for the canonical Feishu bug-fix Skill.
 *
 * Canonical package: .cursor/skills/feishu-bugfix/
 * Adapters:
 *   .codex/skills/feishu-bugfix/SKILL.md
 *   .trae/skills/feishu-bugfix/SKILL.md
 *
 * Usage:
 *   node .cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --check
 *   node .cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --write
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(skillRoot, '../../..');
const source = resolve(skillRoot, 'SKILL.md');
const targets = [
  resolve(repoRoot, '.codex/skills/feishu-bugfix/SKILL.md'),
  resolve(repoRoot, '.trae/skills/feishu-bugfix/SKILL.md'),
];
const write = process.argv.includes('--write');
const check = process.argv.includes('--check') || !write;

function frontmatterField(text, key) {
  const frontmatter = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatter) throw new Error('canonical SKILL.md has no YAML frontmatter');
  const match = frontmatter[1].match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
  if (!match) throw new Error(`canonical SKILL.md frontmatter is missing ${key}`);
  return match[1].trim();
}

if (!existsSync(source)) {
  console.error(`canonical Skill missing: ${source}`);
  process.exitCode = 1;
} else {
  const sourceText = readFileSync(source, 'utf8');
  const adapter = `---\nname: ${frontmatterField(sourceText, 'name')}\ndescription: ${frontmatterField(sourceText, 'description')}\n---\n\n# Feishu Bug Fix Client Adapter\n\nThe canonical Skill package is:\n\n\`\`\`text\n.cursor/skills/feishu-bugfix/\n\`\`\`\n\nBefore handling a Feishu Project bug:\n\n1. Read \`.cursor/skills/feishu-bugfix/SKILL.md\` and follow it as the authoritative Skill instructions.\n2. Resolve \`scripts/\`, \`references/\`, \`templates/\`, and \`policies/\` relative to the canonical Skill directory.\n3. Use \`agent-delivery/bugfix-runs/\` only for per-run state, evidence and reports.\n4. Do not create or maintain a second Skill implementation in this client directory.\n`;
  const expected = Buffer.from(adapter, 'utf8');
  const mismatches = targets.filter((target) => !existsSync(target) || !expected.equals(readFileSync(target)));

  if (write) {
    for (const target of targets) {
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, expected);
    }
    console.log(`wrote ${targets.length} thin client adapters from ${source}`);
  } else if (mismatches.length) {
    console.error('thin client adapters differ:');
    for (const target of mismatches) console.error(`- ${target}`);
    console.error('Run: node .cursor/skills/feishu-bugfix/scripts/sync-bugfix-skill.mjs --write');
    process.exitCode = 2;
  } else {
    console.log(`thin client adapters identical (${check ? 'check' : 'default'})`);
  }
}
