#!/usr/bin/env node
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const script = join(here, 'revalidation-plan.mjs');
const dir = mkdtempSync(join(tmpdir(), 'bugflow-revalidation-'));

function git(args, cwd = dir) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}
function write(rel, value) {
  const path = join(dir, rel);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, value);
}
function commit(message) {
  git(['add', '.']);
  git(['commit', '-m', message]);
}
function plan(ref, status = 'success', premerge = true) {
  const args = [script, '--repo-dir', dir, '--candidate-ref', 'candidate', '--remote-ref', ref, '--remote-pipeline-status', status, '--json'];
  if (premerge) args.push('--premerge-checks-passed');
  return JSON.parse(execFileSync(process.execPath, args, { encoding: 'utf8' }));
}

try {
  git(['init', '-b', 'main']);
  git(['config', 'user.name', 'Selfcheck']);
  git(['config', 'user.email', 'selfcheck@example.invalid']);
  write('src/views/base.vue', 'base\n');
  write('README.md', 'base\n');
  commit('base');

  git(['checkout', '-b', 'candidate']);
  write('src/views/map.css', 'marker { left: 1px; }\n');
  commit('candidate');

  git(['checkout', 'main']);
  git(['checkout', '-b', 'remote-disjoint']);
  write('src/views/other.vue', 'other\n');
  commit('remote disjoint');

  git(['checkout', 'main']);
  git(['checkout', '-b', 'remote-sensitive']);
  write('src/types/shared.ts', 'export type Shared = string;\n');
  commit('remote sensitive');

  git(['checkout', 'main']);
  git(['checkout', '-b', 'remote-overlap']);
  write('src/views/map.css', 'marker { left: 2px; }\n');
  commit('remote overlap');

  assert.equal(plan('remote-disjoint').decision, 'targeted');
  assert.equal(plan('remote-disjoint', 'success', false).decision, 'full');
  assert.equal(plan('remote-sensitive').decision, 'full');
  assert.equal(plan('remote-overlap').decision, 'full');
  assert.equal(plan('remote-disjoint', 'failed').decision, 'block');
  console.log('revalidation-plan selfcheck ok');
} finally {
  rmSync(dir, { recursive: true, force: true });
}
