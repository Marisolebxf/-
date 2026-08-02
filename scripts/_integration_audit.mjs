#!/usr/bin/env node
/**
 * 审计 v2：用 handoff 文件存在性判定"实现已完成"
 *
 * 判定逻辑：
 *   - status ∈ {in_progress, review, pending_test}  （实现中/旧评审/旧测试态）
 *   - 且 task_type ∈ {feature, tech_task, bugfix}  （需要联调的类型）
 *   - 且 handoff 文件存在  （实现已交付）
 * → 建议推进到 integration
 *
 * 同时列出：
 *   - 已在 integration 的任务
 *   - 实现中但无 handoff 的任务（暂不动）
 *   - definition/spike/chore 类型在 in_progress/review 的（走各自路径，不进 integration）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks } from './lib/task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const HANDOFF_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'agent-handoffs');

function handoffExists(taskId) {
  // 常见命名：{taskId}.md 或 {taskId-lower}.md
  const candidates = [
    path.join(HANDOFF_DIR, `${taskId}.md`),
    path.join(HANDOFF_DIR, `${taskId.toLowerCase()}.md`),
  ];
  return candidates.some(p => fs.existsSync(p));
}

function main() {
  const { byId } = loadAllTasks();
  const alreadyIntegration = [];
  const promoteCandidates = [];
  const noHandoff = [];
  const otherTypeInProgress = [];

  for (const t of byId.values()) {
    if (t.status === 'integration') {
      alreadyIntegration.push(t);
      continue;
    }
    // 只看"实现中"或"旧评审/旧测试"态
    if (!['in_progress', 'review', 'pending_test'].includes(t.status)) continue;

    const tt = t.task_type || 'feature';
    if (['feature', 'tech_task', 'bugfix'].includes(tt)) {
      if (handoffExists(t.id)) {
        promoteCandidates.push(t);
      } else {
        noHandoff.push(t);
      }
    } else {
      otherTypeInProgress.push(t);
    }
  }

  console.log(`=== 联调推进审计 v2（基于 handoff 文件存在性）===\n`);

  console.log(`A. 已在 integration: ${alreadyIntegration.length}`);
  for (const t of alreadyIntegration) {
    console.log(`   ${t.id.padEnd(36)} [${t.task_type||'?'}] ${t.title.slice(0,50)}`);
  }

  console.log(`\nB. 实现已交付（in_progress/review/pending_test + handoff 存在）→ 建议推进 integration: ${promoteCandidates.length}`);
  for (const t of promoteCandidates) {
    console.log(`   ${t.id.padEnd(36)} [${t.status.padEnd(14)}] ${t.task_type||'?'} | ${t.title.slice(0,50)}`);
  }

  console.log(`\nC. 实现中但无 handoff（暂不动）: ${noHandoff.length}`);
  for (const t of noHandoff) {
    console.log(`   ${t.id.padEnd(36)} [${t.status.padEnd(14)}] ${t.task_type||'?'} | ${t.title.slice(0,50)}`);
  }

  console.log(`\nD. definition/spike/chore 在 in_progress/review（走各自路径，不进 integration）: ${otherTypeInProgress.length}`);
  for (const t of otherTypeInProgress) {
    console.log(`   ${t.id.padEnd(36)} [${t.status.padEnd(14)}] ${t.task_type||'?'} | ${t.title.slice(0,50)}`);
  }

  console.log(`\n汇总：B 类 ${promoteCandidates.length} 个建议推进到 integration。`);
  if (promoteCandidates.length > 0) {
    console.log(`\n推进命令（复制执行）：`);
    console.log(`node -e "const{updateTaskFields}=require('./lib/task-registry-lib.mjs');${JSON.stringify(promoteCandidates.map(t=>t.id))}.forEach(id=>{try{updateTaskFields(id,{status:'integration',note:(require('./lib/task-registry-lib.mjs').parseTaskBlock?'':'')+'存量推进：实现已交付(handoff)，进入联调'})}catch(e){console.error(id,e.message)}});console.log('done')"`);
  }
}

main();
