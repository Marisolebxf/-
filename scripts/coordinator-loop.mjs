#!/usr/bin/env node
/**
 * coordinator-loop.mjs — Graph Engineering 轻量 Mayor 循环（B4 MVP）
 *
 * 设计决策（Path A light · 2026-07-28）：
 *  - 不调用 Cursor SDK 自动开 agent 会话（避免无人监管烧 token）
 *  - 串联：lease 回收 → ready-engine → convoy 检测 → 监管空位 → dispatch scan → 输出派单建议包
 *  - 人审确认后才 confirm / 开会话（符合公约：决策不外包、监管并发≤4）
 *
 * 用法：
 *   node scripts/coordinator-loop.mjs                 # dry 建议包
 *   node scripts/coordinator-loop.mjs --apply-leases   # 回收过期 claimed
 *   node scripts/coordinator-loop.mjs --json
 *   node scripts/coordinator-loop.mjs --limit 5
 *
 * 关联：ORCH-L03 · orchestration-maturity-and-roadmap.md Phase 3 · 手册 §十六
 */

import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks, isDoneStatus, depsSatisfied, buildDoneIdSet } from './lib/task-registry-lib.mjs';
import { loadTasksWithTouchedFiles, canClaim } from './lib/convoy-lib.mjs';
import {
  loadRosterMembers,
  supervisorsWithCapacity,
  AGENT_SUBCOORD_DEFAULT,
} from './lib/team-roster-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

function runNode(script, args = []) {
  const r = spawnSync(process.execPath, [path.join(ORCH_ROOT, 'scripts', script), ...args], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
  });
  return {
    status: r.status ?? 1,
    stdout: (r.stdout || '').trim(),
    stderr: (r.stderr || '').trim(),
  };
}

function parseArgs(argv) {
  const out = {
    applyLeases: false,
    json: false,
    limit: 8,
    help: false,
    skipScan: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--apply-leases') out.applyLeases = true;
    else if (a === '--json') out.json = true;
    else if (a === '--limit') out.limit = Number(argv[++i] || 8);
    else if (a === '--skip-scan') out.skipScan = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function agentRole(agent) {
  return String(agent || '').replace(/^agent:/, '').replace(/-agent$/, '') || agent;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/coordinator-loop.mjs [--apply-leases] [--limit N] [--json] [--skip-scan]

Steps:
  1) recover-expired-leases (dry or --apply-leases)
  2) coordinator-dispatch ready-engine
  3) detect-convoy-conflicts
  4) find ready tasks + convoy gate + supervisor slot → 派单建议
  5) coordinator-dispatch scan (unless --skip-scan)
  不自动开 Cursor agent / 不自动 confirm`);
    process.exit(0);
  }

  const report = {
    at: new Date().toISOString(),
    mode: 'path_a_light_no_cursor_sdk',
    steps: {},
    recommendations: [],
  };

  // 1) leases
  const leaseArgs = opts.applyLeases ? ['--apply'] : ['--dry-run'];
  const lease = runNode('recover-expired-leases.mjs', leaseArgs);
  report.steps.leases = { status: lease.status, preview: lease.stdout.split('\n').slice(0, 12) };

  // 2) ready-engine
  const ready = runNode('coordinator-dispatch.mjs', ['ready-engine']);
  report.steps.ready_engine = { status: ready.status, stdout: ready.stdout };

  // 3) convoy scan
  const convoy = runNode('detect-convoy-conflicts.mjs', ['--json']);
  let convoyJson = { conflicts: [], soft_warns: [] };
  try {
    convoyJson = JSON.parse(convoy.stdout || '{}');
  } catch {
    /* keep empty */
  }
  report.steps.convoy = {
    status: convoy.status,
    hard: convoyJson.conflicts?.length || 0,
    soft: convoyJson.soft_warns?.length || 0,
  };

  // 4) recommendations
  const { byId, convoyGroups } = loadTasksWithTouchedFiles();
  const doneIds = buildDoneIdSet(byId);
  const members = loadRosterMembers();
  const readyTasks = [...byId.values()]
    .filter((t) => t.status === 'ready' && !t.claimed_by)
    .filter((t) => depsSatisfied(t, doneIds))
    .slice(0, opts.limit);

  for (const t of readyTasks) {
    const gate = canClaim(t.id, byId, convoyGroups);
    const role = agentRole(t.agent);
    const slots = supervisorsWithCapacity(members, byId, {
      agent: role,
      subcoord: t.subcoord || AGENT_SUBCOORD_DEFAULT[role] || null,
    });
    const slot = slots.find((s) => s.free > 0) || null;
    report.recommendations.push({
      id: t.id,
      title: t.title,
      agent: t.agent,
      repo: t.repo,
      subcoord: t.subcoord || AGENT_SUBCOORD_DEFAULT[role] || null,
      convoy_ok: gate.ok,
      convoy_conflicts: gate.conflicts,
      convoy_soft: gate.soft_warns,
      suggested_supervised_by: slot?.registry_name || null,
      supervisor_free: slot?.free ?? 0,
      next:
        !gate.ok
          ? 'blocked_by_convoy'
          : !slot
            ? 'blocked_by_supervisor_capacity'
            : 'ready_to_dispatch_human_confirm',
    });
  }

  // 5) dispatch scan
  if (!opts.skipScan) {
    const scan = runNode('coordinator-dispatch.mjs', ['scan']);
    report.steps.dispatch_scan = {
      status: scan.status,
      preview: scan.stdout.split('\n').slice(0, 15),
    };
  } else {
    report.steps.dispatch_scan = { skipped: true };
  }

  if (opts.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log('=== coordinator-loop (Path A light) ===');
    console.log(`at: ${report.at}`);
    console.log(`leases: exit=${report.steps.leases.status}  (apply=${opts.applyLeases})`);
    console.log(`ready-engine: ${report.steps.ready_engine.stdout || '(ok)'}`);
    console.log(`convoy: hard=${report.steps.convoy.hard} soft=${report.steps.convoy.soft}`);
    console.log('');
    console.log(`派单建议（最多 ${opts.limit} 条 ready）:`);
    if (!report.recommendations.length) {
      console.log('  （无 ready 可派）');
    }
    for (const r of report.recommendations) {
      const flag =
        r.next === 'ready_to_dispatch_human_confirm'
          ? '✓'
          : r.next === 'blocked_by_convoy'
            ? '✗ convoy'
            : '✗ capacity';
      console.log(`  ${flag}  ${r.id}`);
      console.log(`      agent=${r.agent}  subcoord=${r.subcoord || '-'}  repo=${r.repo || '-'}`);
      console.log(
        `      supervised_by→ ${r.suggested_supervised_by || '(none)'}  next=${r.next}`,
      );
      if (r.convoy_conflicts?.length) {
        for (const c of r.convoy_conflicts) console.log(`      conflict: ${c.reason}`);
      }
    }
    console.log('');
    console.log('下一步（人工）:');
    console.log('  1. 确认建议 → 写 claimed_by/supervised_by/subcoord/touched_files');
    console.log('  2. node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:真名');
    console.log('  3. 新开 agent 会话粘贴手册 §9 话术（不由本脚本自动开）');
    if (report.steps.dispatch_scan?.preview?.length) {
      console.log('');
      console.log('dispatch scan 预览:');
      for (const line of report.steps.dispatch_scan.preview) console.log(`  ${line}`);
    }
  }

  const hardFail = (report.steps.convoy.hard || 0) > 0 && report.recommendations.every((r) => !r.convoy_ok);
  process.exit(hardFail ? 1 : 0);
}

main();
