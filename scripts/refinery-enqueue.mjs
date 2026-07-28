#!/usr/bin/env node
/**
 * refinery-enqueue.mjs — soft-record only（B5 脚手架）
 * 不执行 git push / rebase。启用门槛见 agent-delivery/refinery-merge-queue.md
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(__dirname, '..');
const QUEUE_PATH = path.join(ORCH, 'agent-delivery', 'refinery-queue.yaml');

function loadQueue() {
  if (!fs.existsSync(QUEUE_PATH)) {
    return { version: 1, enabled: false, policy: 'soft_record_only', queues: {} };
  }
  const raw = fs.readFileSync(QUEUE_PATH, 'utf8');
  // minimal parse: keep file mostly as-is for list; for write we rebuild simple YAML
  const enabled = /enabled:\s*true/.test(raw);
  const queues = {};
  const qSection = raw.match(/queues:\s*\r?\n([\s\S]*)$/);
  if (qSection && !/^\s*\{\}\s*$/m.test(qSection[1])) {
    // parse repo keys
    for (const m of qSection[1].matchAll(/^  ([^\s:#][^:]*):\s*$/gm)) {
      queues[m[1]] = [];
    }
    // entries under each repo — best effort
    let current = null;
    for (const line of qSection[1].split(/\r?\n/)) {
      const repo = line.match(/^  ([^\s:#][^:]*):\s*$/);
      if (repo) {
        current = repo[1];
        if (!queues[current]) queues[current] = [];
        continue;
      }
      const id = line.match(/^\s+- id:\s*(.+)\s*$/);
      if (id && current) {
        queues[current].push({ id: id[1].trim() });
      }
      if (current && queues[current].length) {
        const last = queues[current][queues[current].length - 1];
        const task = line.match(/^\s+task_id:\s*(.+)\s*$/);
        if (task) last.task_id = task[1].trim().replace(/^["']|["']$/g, '');
        const st = line.match(/^\s+status:\s*(\S+)/);
        if (st) last.status = st[1];
        const at = line.match(/^\s+enqueued_at:\s*(.+)\s*$/);
        if (at) last.enqueued_at = at[1].trim().replace(/^["']|["']$/g, '');
      }
    }
  }
  return { version: 1, enabled, policy: 'soft_record_only', queues };
}

function saveQueue(state) {
  const lines = [
    '# Refinery 合并队列状态（脚手架 · 由 refinery-enqueue.mjs 写入）',
    '# 真源说明：agent-delivery/refinery-merge-queue.md',
    '',
    'version: 1',
    `updated: "${new Date().toISOString()}"`,
    `enabled: ${state.enabled ? 'true' : 'false'}`,
    'policy: soft_record_only',
    '',
    'queues:',
  ];
  const repos = Object.keys(state.queues);
  if (!repos.length) {
    lines.push('  {}');
  } else {
    for (const repo of repos) {
      lines.push(`  ${repo}:`);
      for (const e of state.queues[repo]) {
        lines.push(`    - id: ${e.id}`);
        lines.push(`      task_id: ${e.task_id}`);
        lines.push(`      enqueued_at: "${e.enqueued_at}"`);
        lines.push(`      status: ${e.status}`);
        if (e.note) lines.push(`      note: "${String(e.note).replace(/"/g, '\\"')}"`);
      }
    }
  }
  lines.push('');
  fs.writeFileSync(QUEUE_PATH, lines.join('\n'), 'utf8');
}

function parseArgs(argv) {
  const out = { repo: null, task: null, list: false, dryRun: false, help: false, note: '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--repo') out.repo = argv[++i];
    else if (a === '--task') out.task = argv[++i];
    else if (a === '--list') out.list = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--note') out.note = argv[++i] || '';
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/refinery-enqueue.mjs --list
  node scripts/refinery-enqueue.mjs --repo lumen-svc-platform --task ENT-X [--dry-run]
说明：仅写入 refinery-queue.yaml；不执行 git。enabled=false 时仍可 soft-record。`);
    process.exit(0);
  }

  const state = loadQueue();

  if (opts.list) {
    console.log(JSON.stringify(state, null, 2));
    process.exit(0);
  }

  if (!opts.repo || !opts.task) {
    console.error('需要 --repo 与 --task（或 --list）');
    process.exit(2);
  }

  const id = `rf-${opts.task}-${new Date().toISOString().replace(/[-:]/g, '').slice(0, 15)}`;
  const entry = {
    id,
    task_id: opts.task,
    enqueued_at: new Date().toISOString(),
    status: 'waiting',
    note: opts.note || 'soft_record_only; no git push',
  };

  console.log('=== refinery-enqueue ===');
  console.log(`enabled=${state.enabled}  policy=${state.policy}`);
  console.log(`enqueue: repo=${opts.repo} task=${opts.task} id=${id}`);

  if (opts.dryRun) {
    console.log('[DRY] 未写入');
    process.exit(0);
  }

  if (!state.queues[opts.repo]) state.queues[opts.repo] = [];
  state.queues[opts.repo].push(entry);
  saveQueue(state);
  console.log(`✅ 已写入 ${QUEUE_PATH}`);
  console.log('注意：未执行 git push。启用完整 Refinery 需 PM+架构师双签（见 refinery-merge-queue.md §5）。');
}

main();
