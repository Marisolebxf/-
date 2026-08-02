#!/usr/bin/env node
/**
 * 审计存量 review 状态任务，给出迁移建议
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks } from './lib/task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const HANDOFF_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'agent-handoffs');

function handoffExists(taskId) {
  return [`${taskId}.md`, `${taskId.toLowerCase()}.md`]
    .some(f => fs.existsSync(path.join(HANDOFF_DIR, f)));
}

function main() {
  const { byId } = loadAllTasks();
  const reviewTasks = [];

  for (const t of byId.values()) {
    if (t.status !== 'review') continue;
    reviewTasks.push(t);
  }

  console.log(`=== 存量 review 状态审计 ===\n`);
  console.log(`总数: ${reviewTasks.length}\n`);

  // 按 task_type 分组 + 迁移建议
  const groups = {};
  for (const t of reviewTasks) {
    const tt = t.task_type || 'feature';
    if (!groups[tt]) groups[tt] = [];
    groups[tt].push(t);
  }

  for (const [tt, tasks] of Object.entries(groups)) {
    console.log(`【${tt}】 ${tasks.length} 个`);
    for (const t of tasks) {
      const hf = handoffExists(t.id) ? '✅有handoff' : '❌无handoff';
      const tt2 = t.task_type || 'feature';
      let target;
      if (['definition', 'spike', 'chore'].includes(tt2)) {
        target = 'ready_to_sign';
      } else if (handoffExists(t.id)) {
        target = 'integration';
      } else {
        target = 'in_progress（退回，未完成）';
      }
      console.log(`   ${t.id.padEnd(36)} | ${hf} | → ${target} | ${t.title.slice(0,50)}`);
    }
    console.log();
  }
}

main();
