#!/usr/bin/env node
/**
 * review-check.mjs — 自动验收引擎
 *
 * 对 status=review 的任务进行机械性检查：
 *   1. handoff 文件是否存在
 *   2. handoff 模板章节是否完整（范围与实现 / 偏离 / 产物 / 验收证据 / 架构合规 / Cost 回填）
 *   3. 架构合规自检 7 条是否逐条 ✅
 *   4. Cost 4 字段是否已回填（handoff + registry 双检查）
 *   5. PR 链接是否存在
 *   6. 偏离说明是否存在
 *
 * 用法：
 *   node scripts/review-check.mjs <task-id>          # 检查单个任务
 *   node scripts/review-check.mjs --batch            # 检查所有 review 状态的任务
 *   node scripts/review-check.mjs --batch --auto-fix # 检查通过后自动标记 review-passed
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  loadAllTasks,
  updateTaskFields,
  REGISTRY_PATH,
} from './lib/task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const HANDOFF_BASE = path.join(ORCH_ROOT, 'agent-delivery', 'agent-handoffs');

// ── Handoff 文件搜索路径 ──────────────────────────────────────────
// 按子目录 + 根目录搜索
const HANDOFF_SUBDIRS = [
  '',
  '企业战略分析-ENT',
  '平台基建-PLATFORM',
  '政策模块-E7',
  '产业链分析-CHAIN',
  '软科学成果展示-DS25',
  '科技人才态势-DS15',
  '产品整体定义',
  '产品整体定义/E-31-企业发展',
  '运维事件',
];

function findHandoffFile(taskId) {
  for (const sub of HANDOFF_SUBDIRS) {
    const p = sub
      ? path.join(HANDOFF_BASE, sub, `${taskId}.md`)
      : path.join(HANDOFF_BASE, `${taskId}.md`);
    if (fs.existsSync(p)) return p;
  }
  // 宽搜：在 handoff 文件中搜索任务 ID 引用
  try {
    const files = fs.readdirSync(HANDOFF_BASE, { recursive: true })
      .filter(f => f.endsWith('.md') && f !== 'README.md');
    for (const f of files) {
      const fullPath = path.join(HANDOFF_BASE, f);
      const content = fs.readFileSync(fullPath, 'utf-8');
      if (content.includes(`# ${taskId}`) || content.includes(`# Handoff — ${taskId}`)) {
        return fullPath;
      }
    }
  } catch { /* ignore */ }
  return null;
}

// ── 检查项 ────────────────────────────────────────────────────────

const REQUIRED_SECTIONS = [
  { key: 'scope',      heading: '范围与实现',       keywords: ['范围与实现', 'DoD', '证据'] },
  { key: 'deviation',  heading: '偏离',             keywords: ['偏离'] },
  { key: 'deliverable',heading: '产物清单',         keywords: ['产物清单', '产物'] },
  { key: 'evidence',   heading: '验收证据',         keywords: ['验收证据', '验收'] },
  { key: 'arch',       heading: '架构合规自检',     keywords: ['架构合规自检', '架构合规', '架构自检'] },
  { key: 'cost',       heading: 'Cost 回填',       keywords: ['Cost 回填', 'cost', 'actual_tokens'] },
];

function checkHandoffContent(filePath) {
  const text = fs.readFileSync(filePath, 'utf-8');
  const lines = text.split('\n');

  // 1. 检查必需章节
  const sections = {};
  for (const s of REQUIRED_SECTIONS) {
    const found = s.keywords.some(kw => text.includes(kw));
    sections[s.key] = { found, heading: s.heading };
  }

  // 2. 架构合规自检 — 统计 ✅ 数量
  let archCheckmarks = 0;
  let archMissing = [];
  const archMatch = text.match(/架构合规自检[\s\S]*?(?=\n## |$)/);
  if (archMatch) {
    const archBlock = archMatch[0];
    archCheckmarks = (archBlock.match(/✅/g) || []).length;
    // 检查是否有 ❌
    const hasFail = archBlock.includes('❌');
    if (hasFail) archMissing.push('存在 ❌ 标记的项');
    if (archCheckmarks < 7) archMissing.push(`仅 ${archCheckmarks}/7 项 ✅`);
  } else {
    archMissing.push('未找到架构合规自检章节');
  }

  // 3. Cost 字段检查
  const costFields = ['actual_tokens', 'model_used', 'actual_cost', 'cost_warn'];
  const costInHandoff = {};
  for (const f of costFields) {
    costInHandoff[f] = text.includes(f);
  }
  const costAllInHandoff = costFields.every(f => costInHandoff[f]);

  // 4. PR 链接检查
  const hasPrLink = /(github\.com|gitlab|PR|pull|merge\s*request|pipeline|CI)/i.test(text);

  // 5. 偏离说明
  const hasDeviation = text.includes('偏离') || /deviation/i.test(text);

  return {
    sections,
    arch: { checkmarks: archCheckmarks, pass: archCheckmarks >= 7 && !archMissing.length, missing: archMissing },
    cost: { fields: costInHandoff, all_present: costAllInHandoff },
    has_pr_link: hasPrLink,
    has_deviation: hasDeviation,
  };
}

function checkRegistryCost(task) {
  const fields = ['actual_tokens', 'model_used', 'actual_cost', 'cost_warn'];
  const result = {};
  let allFilled = true;
  for (const f of fields) {
    const v = task[f];
    const filled = v !== undefined && v !== null && v !== '';
    result[f] = { value: v, filled };
    if (!filled) allFilled = false;
  }
  result.all_filled = allFilled;
  return result;
}

// ── 主检查逻辑 ────────────────────────────────────────────────────

export function runReview(taskId) {
  const { byId } = loadAllTasks();
  const task = byId.get(taskId);
  if (!task) return { error: `Task not found: ${taskId}`, task_id: taskId };

  const report = {
    task_id: taskId,
    title: task.title,
    status: task.status,
    checks: {},
    passed: false,
    summary: [],
  };

  // 1. Handoff 文件存在性
  const handoffPath = findHandoffFile(taskId);
  report.checks.handoff_exists = !!handoffPath;
  report.checks.handoff_path = handoffPath || null;
  if (!handoffPath) {
    report.summary.push('❌ handoff 文件不存在');
  } else {
    report.summary.push('✅ handoff 文件存在');
  }

  // 2. Handoff 内容检查
  if (handoffPath) {
    const content = checkHandoffContent(handoffPath);
    report.checks.handoff_content = content;

    // 章节检查
    for (const [key, s] of Object.entries(content.sections)) {
      if (s.found) {
        report.summary.push(`  ✅ 章节 "${s.heading}" 存在`);
      } else {
        report.summary.push(`  ❌ 章节 "${s.heading}" 缺失`);
      }
    }

    // 架构合规
    if (content.arch.pass) {
      report.summary.push(`  ✅ 架构合规自检 ${content.arch.checkmarks}/7 项 ✅`);
    } else {
      report.summary.push(`  ❌ 架构合规自检: ${content.arch.missing.join('; ')}`);
    }

    // 链接
    report.summary.push(`  ${content.has_pr_link ? '✅' : '❌'} PR/CI 链接${content.has_pr_link ? '' : ' 缺失'}`);
    report.summary.push(`  ${content.has_deviation ? '✅' : '❌'} 偏离说明${content.has_deviation ? '' : ' 缺失'}`);
  }

  // 3. Registry cost 字段检查
  const regCost = checkRegistryCost(task);
  report.checks.registry_cost = regCost;
  if (regCost.all_filled) {
    report.summary.push('✅ registry cost 4 字段已回填');
  } else {
    const costFieldNames = ['actual_tokens', 'model_used', 'actual_cost', 'cost_warn'];
    const missing = costFieldNames
      .filter(k => !regCost[k].filled)
      .map(k => k);
    report.summary.push(`❌ registry cost 字段缺失: ${missing.join(', ')}`);
  }

  // 4. 综合判定
  const handoffOk = report.checks.handoff_exists;
  const archOk = handoffPath ? report.checks.handoff_content.arch.pass : false;
  const costOk = regCost.all_filled;
  const sectionsOk = handoffPath
    ? Object.values(report.checks.handoff_content.sections).every(s => s.found)
    : false;

  const allPassed = handoffOk && sectionsOk && archOk && costOk;
  report.passed = allPassed;
  report.checks.detail = {
    handoff_ok: handoffOk,
    sections_ok: sectionsOk,
    arch_ok: archOk,
    cost_ok: costOk,
  };

  if (allPassed) {
    report.summary.unshift('▶ 判定: ✅ 全部通过，可验收');
  } else {
    report.summary.unshift('▶ 判定: ❌ 存在未通过项，需修复');
  }

  return report;
}

// ── CLI 入口 ──────────────────────────────────────────────────────

function printReport(report) {
  console.log('='.repeat(60));
  console.log(`任务: ${report.task_id} — ${report.title}`);
  console.log(`状态: ${report.status}`);
  console.log('='.repeat(60));
  if (report.error) {
    console.log(`错误: ${report.error}`);
    return;
  }
  for (const line of report.summary) {
    console.log(line);
  }
  console.log();
}

function main() {
  const args = process.argv.slice(2);
  const isBatch = args.includes('--batch');
  const autoFix = args.includes('--auto-fix');

  if (isBatch) {
    const { byId } = loadAllTasks();
    const reviewTasks = [];
    for (const task of byId.values()) {
      if (task.status === 'review') {
        reviewTasks.push(task);
      }
    }
    console.log(`\n共 ${reviewTasks.length} 个 review 状态任务，开始检查...\n`);

    let passed = 0, failed = 0;
    for (const task of reviewTasks) {
      const report = runReview(task.id);
      printReport(report);

      if (report.passed) {
        passed++;
        if (autoFix) {
          try {
            updateTaskFields(task.id, {
              status: 'review-passed',
              note: `auto-review: ${new Date().toISOString().slice(0, 10)} 全部通过`,
            });
            console.log(`  → 已自动标记为 review-passed`);
          } catch (e) {
            console.log(`  → 自动标记失败: ${e.message}`);
          }
        }
      } else {
        failed++;
      }
    }

    console.log('='.repeat(60));
    console.log(`检查完成: ${passed} 通过, ${failed} 未通过`);
    if (autoFix) {
      console.log(`通过的任务已自动标记为 review-passed`);
    }
    console.log('='.repeat(60));
  } else {
    const taskId = args.find(a => !a.startsWith('--'));
    if (!taskId) {
      console.error('用法: node scripts/review-check.mjs <task-id> [--batch] [--auto-fix]');
      process.exit(1);
    }
    const report = runReview(taskId);
    printReport(report);
    process.exit(report.passed ? 0 : 1);
  }
}

if (process.argv[1] && (process.argv[1].endsWith('review-check.mjs'))) {
  main();
}