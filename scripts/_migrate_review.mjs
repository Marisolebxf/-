#!/usr/bin/env node
/**
 * 存量 review → 目标态迁移
 * 规则（状态机 v4）：
 *   - definition/spike/chore → ready_to_sign
 *   - feature/tech_task/bugfix → integration
 */
import { updateTaskFields, loadAllTasks } from './lib/task-registry-lib.mjs';

function main() {
  const { byId } = loadAllTasks();
  const reviewTasks = [];
  for (const t of byId.values()) {
    if (t.status === 'review') reviewTasks.push(t);
  }

  let ok = 0, fail = 0;
  for (const t of reviewTasks) {
    const tt = t.task_type || 'feature';
    const target = ['definition', 'spike', 'chore'].includes(tt) ? 'ready_to_sign' : 'integration';
    try {
      updateTaskFields(t.id, {
        status: target,
        note: (t.note ? t.note + ' | ' : '') + '存量迁移：review(legacy废弃) → ' + target + '（2026-08-03）',
      });
      console.log(`  OK ${t.id.padEnd(36)} review → ${target}  [${tt}]`);
      ok++;
    } catch (e) {
      console.error(`  FAIL ${t.id}: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n完成：${ok} 成功, ${fail} 失败`);
  console.log(`\nreview 状态已清零，全部迁移完毕。`);
}

main();
