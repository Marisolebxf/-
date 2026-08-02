#!/usr/bin/env node
/**
 * 存量任务批量标注 task_type
 *
 * 推断规则（按优先级从高到低）：
 *   1. 已有 task_type 的跳过
 *   2. chore: ORCH-* / PM-DECISION-* / GDF-* / *-BOARD-* / *BACKFILL*
 *   3. definition: *-PDR-* / *-PACK-* / *-METRIC-OPEN-* / *-UX-L0* / *-V1-HIFI* / *-V1-FINAL* / *PDR-MINUTES*
 *   4. tech_task: *-JAVA-* / *-API-* / *-ARCH-API* / *-ES-ETL* / *-ES-* / *-DATA-IMPL* / *-DATA-PATH* / *-ALGO-*ASYNC* / *-PY-* / *-GRAPH-*
 *   5. spike: *-DATA-ANALYSIS* / *-REALDATA-* / *-READINESS-MATRIX* / DECIDE-* / *-PROBE*
 *   6. bugfix: FIX-* / *-TRIAGE*
 *   7. feature: ENT-MOD-*-V2-LUMEN-* / FE-ENT-* / *-UI-L0* / 其他 ENT-MOD-*
 *   8. 默认: feature
 *
 * 用法：
 *   node scripts/backfill-task-type.mjs --dry-run    # 仅出报告
 *   node scripts/backfill-task-type.mjs --apply      # 写入 registry
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks, updateTaskFields } from './lib/task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

// 推断规则（顺序 = 优先级）
const RULES = [
  // chore: 看板/编排/杂项
  { type: 'chore', re: /^(ORCH-|PM-DECISION-|GDF-|.*-BOARD-|.*BACKFILL)/, label: '看板/编排/补录' },
  { type: 'chore', re: /-LIVE-PROBE/i, label: '周期复核' },

  // bugfix: 修复
  { type: 'bugfix', re: /^(FIX-|.*-TRIAGE-)/, label: '缺陷修复/排查' },

  // definition: PDR/USM/Wireframe/产品定义
  { type: 'definition', re: /(-PDR-|-PDR-G|-PACK-L|-METRIC-OPEN|-UX-L0|-V1-HIFI|-V1-FINAL|PDR-MINUTES|G2-SIGNOFF|DG-G3)/, label: 'PDR/定义' },
  { type: 'definition', re: /-V2-DEMO$/, label: 'V2 Demo 会签' },

  // tech_task: 接口/ETL/算法框架
  { type: 'tech_task', re: /(-JAVA-|-API-|-ARCH-API|-ES-ETL|-ES-|-DATA-IMPL|-DATA-PATH|-ALGO-.*ASYNC|-PY-|-GRAPH-)/, label: '接口/ETL/算法框架' },
  { type: 'tech_task', re: /^(ENT-ARCH-|ENT-DATA-|DATA-ENT-)/, label: '架构/数据契约' },
  { type: 'tech_task', re: /-DB-DESIGN|DB-DESIGN/, label: '数据库设计' },

  // spike: 调研/分析/探针
  { type: 'spike', re: /(-DATA-ANALYSIS|-REALDATA-|-READINESS-MATRIX|DECIDE-|-PROBE|INST-DATA)/, label: '调研/分析' },
  { type: 'spike', re: /^ENT-ALGO-DEMO/, label: '算法 Demo 探针' },

  // feature: 用户故事级功能
  { type: 'feature', re: /(-V2-LUMEN-|FE-ENT-|UE-ENT-|PM-ENT-|ENT-MOD-)/, label: '用户故事级功能' },
  { type: 'feature', re: /-UI-L0[12349]?$/, label: '前端页面' },
  { type: 'feature', re: /^CHAIN-(UX|FE|MOD)-/, label: '产业链功能' },
  { type: 'feature', re: /^POLICY-PROTO-/, label: '政策原型' },
  { type: 'feature', re: /^E-TECH-NEWS-/, label: '科技新闻功能' },
  { type: 'feature', re: /^E-ENT-(KEYENT|SZSTATUS)-/, label: '企业分析功能' },
];

function inferTaskType(taskId, title) {
  for (const rule of RULES) {
    if (rule.re.test(taskId)) {
      return { type: rule.type, label: rule.label };
    }
  }
  return { type: 'feature', label: '默认(功能)' };
}

async function main() {
  const apply = process.argv.includes('--apply');
  const { byId } = loadAllTasks();

  const stats = {};
  const report = [];
  let alreadyTyped = 0;

  for (const task of byId.values()) {
    if (task.task_type) {
      alreadyTyped++;
      continue;
    }
    const { type, label } = inferTaskType(task.id, task.title);
    stats[type] = (stats[type] || 0) + 1;
    report.push({ id: task.id, title: task.title, inferred_type: type, label, status: task.status });
  }

  // 输出统计
  console.log(`=== task_type 推断报告 ===`);
  console.log(`已有 task_type: ${alreadyTyped}（跳过）`);
  console.log(`待标注: ${report.length}\n`);
  console.log('按类型统计:');
  for (const [type, count] of Object.entries(stats).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${type.padEnd(14)} ${count}`);
  }

  // 按类型分组输出
  console.log('\n=== 详细列表（按类型分组）===\n');
  for (const [type, count] of Object.entries(stats).sort((a, b) => b[1] - a[1])) {
    const items = report.filter(r => r.inferred_type === type);
    console.log(`【${type}】 ${count} 个`);
    for (const r of items) {
      console.log(`  ${r.id.padEnd(36)} [${r.status.padEnd(14)}] ${r.label} | ${r.title.slice(0, 50)}`);
    }
    console.log();
  }

  // 应用
  if (apply) {
    console.log(`\n=== 写入 registry ===`);
    let ok = 0, fail = 0;
    for (const r of report) {
      try {
        updateTaskFields(r.id, { task_type: r.inferred_type });
        ok++;
      } catch (e) {
        console.error(`  FAIL ${r.id}: ${e.message}`);
        fail++;
      }
    }
    console.log(`完成: ${ok} 成功, ${fail} 失败`);
  } else {
    console.log(`\n(dry-run 模式，未写入 registry。加 --apply 执行)`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
