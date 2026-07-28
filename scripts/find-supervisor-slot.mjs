#!/usr/bin/env node
/**
 * find-supervisor-slot.mjs
 * 按 team-roster 亲和 + registry 活跃挂载（仅参考）推荐 supervised_by。
 *
 * 用法（在 gkx-orchestration/ 根目录）：
 *   node scripts/find-supervisor-slot.mjs
 *   node scripts/find-supervisor-slot.mjs --agent frontend
 *   node scripts/find-supervisor-slot.mjs --subcoord ui-subcoord
 *   node scripts/find-supervisor-slot.mjs --agent api --json
 *
 * 语义（2026-07-28 澄清）：
 *   max_agent_concurrency = 本机 Cursor agent 会话上限（≠ 派单上限、≠ registry 挂载上限）。
 *   本脚本的 load/free 来自 registry 活跃挂载，仅作亲和参考；**不得**因 free≤0 拒派。
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
  // 始终可列出全部可监管人；--all 语义保留；默认也展示全表（free 仅参考）
  const show = rows;

  if (opts.json) {
    console.log(
      JSON.stringify(
        {
          query: { agent: opts.agent, subcoord: opts.subcoord || rows[0]?.preferredSub || null },
          note: 'max_agent_concurrency=本机Cursor会话上限；load/free=registry参考，非派单门禁',
          recommendation: rows[0]
            ? {
                supervised_by: rows[0].registry_name,
                free: rows[0].free,
                load: rows[0].load,
                capacity: rows[0].capacity,
                team: rows[0].team,
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
  console.log('=== find-supervisor-slot（亲和参考 · 非派单门禁）===');
  console.log(`查询: agent=${opts.agent || '-'}  subcoord=${pref || '-'}`);
  console.log(
    `可监管人: ${members.filter((m) => m.can_supervise_agent).length}  · registry 参考有空位: ${available.length}`,
  );
  console.log(
    '说明: max_agent_concurrency=本机 Cursor 会话上限；load/free 为 registry 挂载参考，不得因 free=0 拒派',
  );
  console.log('');

  if (!rows.length) {
    console.log('⚠️  花名册无 can_supervise_agent=true 的成员。');
    process.exit(1);
  }

  if (!available.length) {
    console.log(
      'ℹ️  所有监管人 registry 参考水位已满——仍可派单；本机开会话请各自遵守 max_agent_concurrency。',
    );
    console.log('');
  }

  console.log(`推荐 supervised_by: ${rows[0].registry_name}`);
  console.log(
    `  registry_load ${rows[0].load}/${rows[0].capacity}  free=${rows[0].free}  team=${rows[0].team}` +
      (rows[0].affinityHit && pref ? `  affinity✓` : ''),
  );
  console.log('');

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
