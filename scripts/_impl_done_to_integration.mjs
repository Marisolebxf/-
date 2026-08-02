#!/usr/bin/env node
/**
 * 批量：交付阶段=实现 且 状态=done → 改回 integration
 */
import { loadAllTasks, updateTaskFields } from './lib/task-registry-lib.mjs';

function main() {
  const { byId } = loadAllTasks();
  const candidates = [];

  for (const t of byId.values()) {
    if (t.delivery_phase === 'implementation' && t.status === 'done') {
      candidates.push(t);
    }
  }

  console.log(`推进 ${candidates.length} 个任务：done → integration\n`);
  let ok = 0, fail = 0;
  for (const t of candidates) {
    try {
      updateTaskFields(t.id, {
        status: 'integration',
        note: (t.note ? t.note + ' | ' : '') + '存量修正：交付阶段=实现，done→integration（联调未完成，2026-08-03）',
      });
      console.log(`  OK ${t.id.padEnd(36)} done → integration`);
      ok++;
    } catch (e) {
      console.error(`  FAIL ${t.id}: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n完成：${ok} 成功, ${fail} 失败`);
}

main();
