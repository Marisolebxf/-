#!/usr/bin/env node
/**
 * Lightweight worktree guard.
 * Checks that each repo worktree still exists and is a real git worktree.
 * Does not repair or modify anything.
 *
 * Usage:
 *   node worktree-guard.mjs --repo-dir <path> [--repo-dir <path> ...] [--json]
 */
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { parseArgs } from 'node:util';

const { values } = parseArgs({
  options: {
    'repo-dir': { type: 'string', multiple: true },
    json: { type: 'boolean', default: false },
    help: { type: 'boolean', short: 'h' },
  },
});

const dirs = values['repo-dir'] ?? [];
if (values.help || dirs.length === 0) {
  process.stdout.write(`Usage: node worktree-guard.mjs --repo-dir <path> [--repo-dir <path> ...] [--json]\n`);
  process.exit(values.help ? 0 : 2);
}

function git(dir, args) {
  return execFileSync('git', ['-C', dir, ...args], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

const results = dirs.map((dir) => {
  if (!existsSync(dir)) return { path: dir, ok: false, reason: 'path missing' };
  if (!existsSync(join(dir, '.git'))) return { path: dir, ok: false, reason: 'not a git worktree (.git missing)' };
  try {
    const sha = git(dir, ['rev-parse', 'HEAD']);
    const branch = git(dir, ['rev-parse', '--abbrev-ref', 'HEAD']);
    const dirty = git(dir, ['status', '--porcelain']);
    return { path: dir, ok: true, sha, branch, dirty: Boolean(dirty) };
  } catch (error) {
    return { path: dir, ok: false, reason: String(error.message || error) };
  }
});

if (values.json) {
  process.stdout.write(`${JSON.stringify(results, null, 2)}\n`);
} else {
  for (const row of results) {
    process.stdout.write(row.ok
      ? `OK   ${row.path} ${row.branch} ${row.sha}${row.dirty ? ' (dirty)' : ''}\n`
      : `FAIL ${row.path} ${row.reason}\n`);
  }
}
if (results.some((row) => !row.ok)) process.exitCode = 1;
