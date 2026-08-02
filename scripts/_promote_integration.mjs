#!/usr/bin/env node
/**
 * 批量推进存量任务到 integration
 * 范围：B + C 类共 12 个（in_progress/review/pending_test + feature/tech_task/bugfix）
 */
import { updateTaskFields, loadAllTasks } from './lib/task-registry-lib.mjs';

const PROMOTE_IDS = [
  // B 类：有 handoff
  'ENT-MOD-EVAL-READINESS-UI-L01',
  'ENT-MOD-EVAL-TEST-TRIAGE-L01',
  // C 类：review 态旧任务
  'CHAIN-DATA-L01',
  'CHAIN-API-L01',
  'E-PERM-L03a',
  // C 类：in_progress
  'E-PLATFORM-ORCH-L01',
  'E-PERM-L01',
  'E-PERM-L02',
  'E-PERM-L03',
  'ENT-ES-ETL-L01',
  // C 类：pending_test 无 handoff
  'E-ENT-KEYENT-UI-L01',
  'E-ENT-SZSTATUS-UI-L01',
];

function main() {
  const { byId } = loadAllTasks();
  let ok = 0, fail = 0, skip = 0;
  for (const id of PROMOTE_IDS) {
    const t = byId.get(id);
    if (!t) { console.error(`  NOT FOUND ${id}`); fail++; continue; }
    if (t.status === 'integration') { console.log(`  SKIP ${id} (已是 integration)`); skip++; continue; }
    try {
      updateTaskFields(id, {
        status: 'integration',
        note: (t.note ? t.note + ' | ' : '') + '存量推进：实现阶段已完成，进入联调（2026-08-03）',
      });
      console.log(`  OK ${id.padEnd(36)} ${t.status} → integration`);
      ok++;
    } catch (e) {
      console.error(`  FAIL ${id}: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n完成：${ok} 成功, ${skip} 跳过, ${fail} 失败`);
}

main();
