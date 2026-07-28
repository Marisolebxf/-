#!/usr/bin/env node
/**
 * coordinator-loop.mjs — Graph Engineering 轻量 Mayor 循环（B4 MVP）
 *
 * 设计决策（Path A light · 2026-07-28）：
 *  - 不调用 Cursor SDK 自动开 agent 会话（避免无人监管烧 token）
 *  - 串联：lease 回收 → ready-engine → convoy 检测 → 监管亲和建议 → dispatch scan → 输出派单建议包
 *  - 人审确认后才 confirm / 开会话（决策不外包；本机 Cursor 会话≤4 ≠ 派单上限）
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
    proposeDispatch: false,
    noNotify: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--apply-leases') out.applyLeases = true;
    else if (a === '--json') out.json = true;
    else if (a === '--limit') out.limit = Number(argv[++i] || 8);
    else if (a === '--skip-scan') out.skipScan = true;
    else if (a === '--propose-dispatch') out.proposeDispatch = true;
    else if (a === '--no-notify') out.noNotify = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  if (process.env.COORDINATOR_LOOP_PROPOSE_DISPATCH === '1') out.proposeDispatch = true;
  if (process.env.COORDINATOR_LOOP_NO_NOTIFY === '1') out.noNotify = true;
  return out;
}

function agentRole(agent) {
  return String(agent || '').replace(/^agent:/, '').replace(/-agent$/, '') || agent;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(`Usage:
  node scripts/coordinator-loop.mjs [--apply-leases] [--limit N] [--json] [--skip-scan]
  node scripts/coordinator-loop.mjs --propose-dispatch [--no-notify]

Steps:
  1) recover-expired-leases (dry or --apply-leases)
  2) coordinator-dispatch ready-engine
  3) detect-convoy-conflicts
  4) find ready tasks + convoy gate + supervisor slot → 派单建议
  5) coordinator-dispatch scan (unless --skip-scan)
  6) optional --propose-dispatch: pending + 派单门控待确认 + IM 通知淮政玮
  不自动开 Cursor agent / 不自动 confirm（confirm 由飞书门控「已确认」webhook 完成）`);
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
    const slot = slots[0] || null;
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
      supervisor_registry_load: slot?.load ?? null,
      supervisor_local_session_cap: slot?.capacity ?? null,
      next: !gate.ok ? 'blocked_by_convoy' : 'ready_to_dispatch_human_confirm',
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

  // 6) propose dispatch gate + IM（可选）
  if (opts.proposeDispatch) {
    const { proposeMayorLoopDispatch } = await import('./lib/mayor-loop-propose.mjs');
    const candidates = report.recommendations.filter((r) => r.next === 'ready_to_dispatch_human_confirm');
    try {
      report.steps.propose_dispatch = await proposeMayorLoopDispatch(candidates, {
        dryRun: false,
        notify: !opts.noNotify,
      });
    } catch (e) {
      report.steps.propose_dispatch = { ok: false, error: e.message };
    }
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
      const flag = r.next === 'ready_to_dispatch_human_confirm' ? '✓' : '✗ convoy';
      console.log(`  ${flag}  ${r.id}`);
      console.log(`      agent=${r.agent}  subcoord=${r.subcoord || '-'}  repo=${r.repo || '-'}`);
      console.log(
        `      supervised_by→ ${r.suggested_supervised_by || '(none)'}  next=${r.next}` +
          (r.supervisor_registry_load != null
            ? `  (registry_load=${r.supervisor_registry_load}/${r.supervisor_local_session_cap} 参考非门禁)`
            : ''),
      );
      if (r.convoy_conflicts?.length) {
        for (const c of r.convoy_conflicts) console.log(`      conflict: ${c.reason}`);
      }
    }
    if (report.steps.propose_dispatch) {
      const p = report.steps.propose_dispatch;
      console.log('');
      console.log('propose-dispatch:');
      console.log(`  confirm_by=${p.confirm_by || '-'}  enqueued=${(p.enqueued || []).join(',') || '(none)'}`);
      if (p.notify) {
        console.log(
          `  notify: ${p.notify.ok ? 'ok' : 'FAIL'} ${p.notify.error || p.notify.message_id || ''}`,
        );
      }
    }
    console.log('');
    console.log('下一步:');
    if (opts.proposeDispatch) {
      console.log('  1. 淮政玮在飞书将「派单门控」改为「已确认」→ webhook confirm');
      console.log('  2. confirm 后开 worker 会话（手册 §9）；本机会话≤max_agent_concurrency');
    } else {
      console.log('  1. 确认建议 → 写 claimed_by/supervised_by/subcoord/touched_files');
      console.log('  2. node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:真名');
      console.log('  3. 或加 --propose-dispatch 走飞书门控 + IM 通知淮政玮');
    }
    if (report.steps.dispatch_scan?.preview?.length) {
      console.log('');
      console.log('dispatch scan 预览:');
      for (const line of report.steps.dispatch_scan.preview) console.log(`  ${line}`);
    }
  }

  const hardFail = (report.steps.convoy.hard || 0) > 0 && report.recommendations.every((r) => !r.convoy_ok);
  process.exit(hardFail ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
