#!/usr/bin/env node
/**
 * GDF 账号提交路径门禁（gusb / husq / caizz；旧登录名 husenquan 兼容）。
 * 允许前缀见 ALLOW_PREFIXES；精确文件见 ALLOW_FILES。
 * 本地：node scripts/gdf-author-path-guard.mjs
 * CI：CI_COMMIT_BEFORE_SHA + CI_COMMIT_SHA
 */
import { execSync } from 'node:child_process';
import fs from 'node:fs';

const ALLOW_PREFIXES = [
  'agent-delivery/data/GDF/',
  '.cursor/skills/gkx-gdf-cdc-workpack/',
  '.codex/skills/gkx-gdf-cdc-workpack/',
  'scripts/gdf-cdc/',
  'agent-delivery/agent-handoffs/',
];

const ALLOW_FILES = new Set(['agent-delivery/task-registry.yaml']);

function git(args) {
  return execSync(`git ${args}`, { encoding: 'utf8' }).trim();
}

function listChanged() {
  const fromFile = process.argv.includes('--from-file')
    ? process.argv[process.argv.indexOf('--from-file') + 1]
    : '';
  if (fromFile) {
    return fs.readFileSync(fromFile, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  }
  const sha = process.env.CI_COMMIT_SHA || git('rev-parse HEAD');
  const before = process.env.CI_COMMIT_BEFORE_SHA || '';
  if (!before || /^0+$/.test(before)) {
    return git(`diff-tree --no-commit-id --name-only -r ${sha}`)
      .split(/\r?\n/)
      .filter(Boolean);
  }
  return git(`diff --name-only ${before} ${sha}`).split(/\r?\n/).filter(Boolean);
}

function allowed(file) {
  const p = file.replace(/\\/g, '/');
  if (ALLOW_FILES.has(p)) return true;
  return ALLOW_PREFIXES.some((prefix) => p.startsWith(prefix));
}

const files = listChanged();
const bad = files.filter((f) => !allowed(f));
if (bad.length) {
  console.error('gdf-author-path-guard: GDF 账号不得提交白名单外路径：');
  for (const f of bad) console.error(`  - ${f}`);
  console.error('允许：agent-delivery/data/GDF/ · skills/gkx-gdf-cdc-workpack · scripts/gdf-cdc/ · task-registry.yaml · agent-handoffs/');
  process.exit(1);
}
console.log(`gdf-author-path-guard: ok (${files.length} files)`);
