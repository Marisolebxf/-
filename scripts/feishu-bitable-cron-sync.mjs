#!/usr/bin/env node
/**
 * K8s CronJob entry: Node-only board sync (replaces board-sync-watch.ps1 + pwsh).
 *
 * 1. git pull
 * 2. inbound pull all (Feishu → registry, warn transitions)
 * 3. outbound watch (--skip-kanban-fields: project supervised_by / Agent / Handoff)
 * 4. git push registry
 * 5. coordinator-dispatch scan
 */

import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { loadBitableConfig, loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';
import { runInboundPullAll } from './lib/feishu-bitable-inbound.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG_PATH = path.join(ORCH_ROOT, 'agent-delivery', '_tmp', 'board-sync-watch.log');

function log(msg) {
  const line = `[${new Date().toISOString()}] cron-sync: ${msg}`;
  console.log(line);
  try {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
    fs.appendFileSync(LOG_PATH, `${line}\n`, 'utf8');
  } catch {
    /* ignore */
  }
}

function gitPull() {
  if (!fs.existsSync(path.join(ORCH_ROOT, '.git'))) {
    log('WARN: not a git repo; skip pull');
    return true;
  }
  const branch = spawnSync('git', ['rev-parse', '--abbrev-ref', 'HEAD'], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
  }).stdout?.trim();
  if (!branch) return false;
  log(`git pull --rebase origin ${branch}`);
  const r = spawnSync('git', ['pull', '--rebase', 'origin', branch], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
  });
  if (r.status !== 0) {
    log(`ERROR git pull: ${r.stderr || r.stdout}`);
    return false;
  }
  return true;
}

function gitPush() {
  const sh = path.join(ORCH_ROOT, 'scripts', 'lib', 'git-push-registry.sh');
  if (process.platform === 'win32') {
    const ps1 = path.join(ORCH_ROOT, 'scripts', 'lib', 'git-push-registry.ps1');
    spawnSync('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], {
      cwd: ORCH_ROOT,
      encoding: 'utf8',
    });
    return;
  }
  if (fs.existsSync(sh)) {
    spawnSync('bash', [sh], { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env });
  }
}

function dispatchScan() {
  const mjs = path.join(ORCH_ROOT, 'scripts', 'coordinator-dispatch.mjs');
  if (!fs.existsSync(mjs)) return;
  log('coordinator-dispatch scan');
  const r = spawnSync(process.execPath, [mjs, 'scan'], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
    env: process.env,
  });
  if (r.stdout) log(r.stdout.trim());
  if (r.stderr) log(r.stderr.trim());
}

function readCurrentSprint() {
  const scrum = path.join(ORCH_ROOT, 'agent-delivery', 'scrum-sprint.yaml');
  if (!fs.existsSync(scrum)) return '';
  const raw = fs.readFileSync(scrum, 'utf8');
  const m = raw.match(/^\s*current_sprint:\s*"?([^"\r\n]+)"?/m);
  return m ? m[1].trim() : '';
}

async function main() {
  loadDotEnv();
  const dryRun = process.argv.includes('--dry-run');
  log(`start dryRun=${dryRun}`);

  if (!gitPull()) process.exit(1);

  const cfg = loadBitableConfig();
  const inbound = await runInboundPullAll(cfg, { dryRun });
  log(`inbound: ${JSON.stringify(inbound)}`);

  const sprintId = readCurrentSprint();
  const mjs = path.join(ORCH_ROOT, 'scripts', 'lib', 'board-task-status.mjs');
  const args = [mjs, '--watch-outbound', '--skip-kanban-fields'];
  if (sprintId) args.push('--sprint-id', sprintId);
  if (dryRun) args.push('--dry-run');
  log(`outbound: node ${args.slice(1).join(' ')}`);
  const out = spawnSync(process.execPath, args, { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env });
  if (out.stdout) process.stdout.write(out.stdout);
  if (out.stderr) process.stderr.write(out.stderr);
  if (out.status !== 0) log(`WARN outbound exit=${out.status}`);

  if (!dryRun) {
    gitPush();
    dispatchScan();
  }

  log('done');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
