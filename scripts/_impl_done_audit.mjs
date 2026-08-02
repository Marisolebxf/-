#!/usr/bin/env node
/**
 * 审计：交付阶段=实现 且 状态=done 的任务
 * 这些任务应该改回 integration（联调中）
 */
import { loadAllTasks } from './lib/task-registry-lib.mjs';

function main() {
  const { byId } = loadAllTasks();
  const candidates = [];
  const alreadyIntegration = [];
  const doneNotImpl = [];

  for (const t of byId.values()) {
    if (t.delivery_phase !== 'implementation') {
      // done 但不是 implementation 的，记录对照
      if (t.status === 'done') doneNotImpl.push(t);
      continue;
    }
    if (t.status === 'integration') {
      alreadyIntegration.push(t);
    } else if (t.status === 'done') {
      candidates.push(t);
    }
  }

  console.log(`=== 审计：交付阶段=实现 的任务 ===\n`);
  console.log(`A. 已在 integration: ${alreadyIntegration.length}`);
  console.log(`B. 状态=done（需改回 integration）: ${candidates.length}`);
  console.log(`C. done 但 delivery_phase≠implementation: ${doneNotImpl.length}\n`);

  console.log(`--- B 类详情（需要改回 integration）---`);
  for (const t of candidates) {
    const tt = t.task_type || '?';
    console.log(`   ${t.id.padEnd(36)} [${tt.padEnd(10)}] ${t.title.slice(0,60)}`);
  }

  // 按 task_type 统计
  const byType = {};
  for (const t of candidates) {
    const tt = t.task_type || '?';
    byType[tt] = (byType[tt] || 0) + 1;
  }
  console.log(`\n按 task_type 统计:`);
  for (const [tt, n] of Object.entries(byType).sort((a,b) => b[1]-a[1])) {
    console.log(`   ${tt.padEnd(14)} ${n}`);
  }
}

main();
