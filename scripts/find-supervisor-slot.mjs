#!/usr/bin/env node
/**
 * find-supervisor-slot.mjs
 * 按 team-roster 的 max_agent_concurrency + 当前 registry 活跃负载，推荐 supervised_by。
 *
 * 用法（在 gkx-orchestration/ 根目录）：
 *   node scripts/find-supervisor-slot.mjs
 *   node scripts/find-supervisor-slot.mjs --agent frontend
 *   node scripts/find-supervisor-slot.mjs --subcoord ui-subcoord
 *   node scripts/find-supervisor-slot.mjs --agent api --json
 *
 * 监管并发 ≠ 派单上限：本脚本查的是「人类监管人」容量，不是 coordinator 派单吞吐。
 * 真源：智能体编排与派单手册 §13.1 / §十六 · Graph-Engineering-ODS解耦-会话纪要-2026-07-28.md
 */

import {
  loadRosterMembers,
  supervisorsWithCapacity,
  AGENT_SUBCOORD_DEFAULT,
} from './lib/team-roster-lib.mjs';
import { loadAllTasks } from './lib/task-registry-lib.mjs';

function parseArgs(argv) {
  const out = { agent: null, subcoord: null, json: false, help: false, all: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--agent') out.agent = argv[++i];
    else if (a === '--subcoord') out.subcoord = argv[++i];
    else if (a === '--json') out.json = true;
    else if (a === '--all') out.all = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/find-supervisor-slot.mjs [--agent ROLE] [--subcoord ID] [--all] [--json]

Options:
  --agent     worker agent 角色（frontend / api / algorithm ...），用于默认 subcoord 亲和
  --subcoord  显式子协调域（platform-subcoord / ui-subcoord / ...）
  --all       列出全部可监管人（含已满）
  --json      JSON 输出

默认 agent→subcoord 映射:
${Object.entries(AGENT_SUBCOORD_DEFAULT)
  .filter(([, v]) => v)
  .map(([k, v]) => `  ${k} → ${v}`)
  .join('\n')}`);
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    usage();
    process.exit(0);
  }

  const members = loadRosterMembers();
  const { byId } = loadAllTasks();
  const rows = supervisorsWithCapacity(members, byId, {
    agent: opts.agent,
    subcoord: opts.subcoord,
  });

  const available = rows.filter((r) => r.free > 0);
  const show = opts.all ? rows : available;

  if (opts.json) {
    console.log(
      JSON.stringify(
        {
          query: { agent: opts.agent, subcoord: opts.subcoord || rows[0]?.preferredSub || null },
          recommendation: available[0]
            ? {
                supervised_by: available[0].registry_name,
                free: available[0].free,
                load: available[0].load,
                capacity: available[0].capacity,
                team: available[0].team,
              }
            : null,
          slots: show.map((r) => ({
            supervised_by: r.registry_name,
            name: r.name,
            team: r.team,
            load: r.load,
            capacity: r.capacity,
            free: r.free,
            affinityHit: r.affinityHit,
          })),
        },
        null,
        2,
      ),
    );
    return;
  }

  const pref = opts.subcoord || (opts.agent ? AGENT_SUBCOORD_DEFAULT[opts.agent] : null);
  console.log('=== find-supervisor-slot ===');
  console.log(`查询: agent=${opts.agent || '-'}  subcoord=${pref || '-'}`);
  console.log(`可监管人: ${members.filter((m) => m.can_supervise_agent).length}  · 有空位: ${available.length}`);
  console.log('');

  if (!show.length) {
    console.log('⚠️  无可用监管人空位。请：');
    console.log('  1) 跑 recover-expired-leases.mjs 回收过期 claimed');
    console.log('  2) 或提高某成员 max_agent_concurrency（需 PM 批准）');
    console.log('  3) 或等待 in_progress 任务进入 review/done');
    process.exit(1);
  }

  if (available[0]) {
    console.log(`推荐 supervised_by: ${available[0].registry_name}`);
    console.log(
      `  load ${available[0].load}/${available[0].capacity}  free=${available[0].free}  team=${available[0].team}` +
        (available[0].affinityHit && pref ? `  affinity✓` : ''),
    );
    console.log('');
  }

  console.log('名册（按推荐序）:');
  console.log('  free  load/cap  affinity  supervised_by');
  for (const r of show) {
    const aff = pref ? (r.affinityHit ? '✓' : '·') : '-';
    console.log(
      `  ${String(r.free).padStart(4)}  ${String(r.load).padStart(2)}/${String(r.capacity).padStart(2)}     ${aff}        ${r.registry_name}`,
    );
  }
}

main();
