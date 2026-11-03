#!/usr/bin/env node
/**
 * review-check.mjs — 自动验收引擎 v2
 *
 * 状态机 v3 的自动验收触发点：
 *   AV-0: in_progress + push + CI绿 + handoff齐 → integration
 *   AV-1: integration + handoff内容完整 + 联调确认 → pending_test (impl) / ready_to_sign (def)
 *   AV-3: ready_to_sign → done（由 task-update-status 闸门校验，非自动）
 *
 * runReview(taskId)        — 向后兼容：检查任务能否通过当前阶段的验收
 * runAutoVerify(taskId)    — 新：按当前状态自动选择验收规则，返回 { target_status, passed, report }
 *
 * 用法：
 *   node scripts/review-check.mjs <task-id>              # 检查单个任务
 *   node scripts/review-check.mjs --batch                # 检查所有可自动验收的任务
 *   node scripts/review-check.mjs --batch --auto-fix     # 检查通过后自动流转状态
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  loadAllTasks,
  updateTaskFields,
  REGISTRY_PATH,
  AV0_TARGET,
  AV1_TARGET,
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
  '算法库联调-ALGO-LIB',
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
  // 按标题行定位章节（正文/表格里提前提及「架构合规自检」不再误截前文片段）；
  // 无标题式写法时回退旧的首次出现匹配（兼容旧 handoff）。
  let archBlock = null;
  const headingIdx = lines.findIndex(l => /^#{1,6}\s.*架构合规自检/.test(l));
  if (headingIdx >= 0) {
    let end = lines.length;
    for (let i = headingIdx + 1; i < lines.length; i++) {
      if (/^#{1,6}\s/.test(lines[i])) { end = i; break; }
    }
    archBlock = lines.slice(headingIdx, end).join('\n');
  } else {
    const archMatch = text.match(/架构合规自检[\s\S]*?(?=\n## |$)/);
    if (archMatch) archBlock = archMatch[0];
  }
  let archCheckmarks = 0;
  let archMissing = [];
  if (archBlock !== null) {
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

// ── 自动验收引擎 v2 ────────────────────────────────────────────────

/**
 * 联调确认关键词（note 里出现即认为联调方已确认）
 */
const INTEGRATION_CONFIRM_KEYWORDS = [
  '联调通过', '联调完成', '联调确认',
  '会签通过', '会签完成', '会签确认',
  '集成测试通过', '集成确认',
  '前后端联调', '数据联调', '三方联调',
];

/**
 * 按当前状态自动选择验收规则。
 *   in_progress  → AV-0 → integration
 *   integration  → AV-1 → pending_test (impl) / ready_to_sign (def/crosscut)
 *   其他状态     → 不自动验收
 *
 * 返回 { task_id, status, target_status, passed, report, reason }
 */
export function runAutoVerify(taskId) {
  const { byId } = loadAllTasks();
  const task = byId.get(taskId);
  if (!task) return { task_id: taskId, error: `Task not found: ${taskId}` };

  const status = task.status;
  const taskType = task.task_type || 'feature'; // default feature

  // AV-0: in_progress → AV0_TARGET[task_type]
  if (status === 'in_progress') {
    const targetStatus = AV0_TARGET[taskType] || 'integration';
    const handoffPath = findHandoffFile(taskId);
    const hasHandoff = !!handoffPath;
    const hasEvidence = !!(task.evidence && task.evidence !== '-' && task.evidence !== '');
    // chore 类型不需要 handoff（杂项任务）
    const needsHandoff = taskType !== 'chore';
    const passed = (!needsHandoff || hasHandoff) && hasEvidence;
    return {
      task_id: taskId,
      title: task.title,
      status,
      task_type: taskType,
      av: 'AV-0',
      target_status: targetStatus,
      passed,
      checks: { handoff_exists: hasHandoff, evidence_set: hasEvidence, handoff_path: handoffPath },
      reason: passed
        ? `handoff/evidence 就绪 → ${targetStatus} (task_type=${taskType})`
        : `未通过: handoff_exists=${hasHandoff}, evidence_set=${hasEvidence} (task_type=${taskType})`,
    };
  }

  // AV-1: integration → AV1_TARGET[task_type]
  if (status === 'integration') {
    const report = runReview(taskId);
    const note = task.note || '';
    const hasConfirmKeyword = INTEGRATION_CONFIRM_KEYWORDS.some(kw => note.includes(kw));

    const targetStatus = AV1_TARGET[taskType] || 'ready_to_sign';
    const passed = report.passed && hasConfirmKeyword;

    return {
      task_id: taskId,
      title: task.title,
      status,
      task_type: taskType,
      av: 'AV-1',
      target_status: targetStatus,
      passed,
      checks: {
        handoff_pass: report.passed,
        integration_confirmed: hasConfirmKeyword,
        detail: report.checks,
      },
      reason: passed
        ? `handoff 验收通过 + 联调确认 → ${targetStatus} (task_type=${taskType})`
        : `未通过: handoff_pass=${report.passed}, integration_confirmed=${hasConfirmKeyword}（note 需含联调确认关键词如: ${INTEGRATION_CONFIRM_KEYWORDS.slice(0, 3).join('/')}）`,
    };
  }

  // 其他状态不自动验收
  return {
    task_id: taskId,
    title: task.title,
    status,
    task_type: taskType,
    av: null,
    target_status: null,
    passed: false,
    reason: `状态 ${status} 无自动验收规则（AV-0=in_progress, AV-1=integration）`,
  };
}

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
  const targetStatus = args.find(a => a.startsWith('--target='))?.split('=')[1] || null;

  if (isBatch) {
    const { byId } = loadAllTasks();
    // 收集所有可自动验收的任务（in_progress + integration）
    const candidates = [];
    for (const task of byId.values()) {
      if (task.status === 'in_progress' || task.status === 'integration') {
        if (!targetStatus) {
          candidates.push(task);
        } else {
          const av = runAutoVerify(task.id);
          if (av.target_status === targetStatus) candidates.push(task);
        }
      }
    }
    console.log(`\n共 ${candidates.length} 个可自动验收任务（in_progress + integration）${targetStatus ? ` 目标=${targetStatus}` : ''}，开始检查...\n`);

    let passed = 0, failed = 0, skipped = 0;
    for (const task of candidates) {
      const av = runAutoVerify(task.id);
      console.log('='.repeat(60));
      console.log(`任务: ${task.id} — ${task.title}`);
      console.log(`状态: ${av.status} → 目标: ${av.target_status || '(无)'} | AV: ${av.av || 'N/A'}`);
      console.log(`判定: ${av.passed ? '✅ 通过' : '❌ 未通过'}`);
      console.log(`原因: ${av.reason}`);
      if (av.checks?.detail) {
        const d = av.checks.detail;
        console.log(`  handoff_ok=${d.handoff_ok} sections_ok=${d.sections_ok} arch_ok=${d.arch_ok} cost_ok=${d.cost_ok}`);
      }
      console.log();

      if (av.passed) {
        passed++;
        if (autoFix && av.target_status) {
          try {
            updateTaskFields(task.id, {
              status: av.target_status,
              note: `auto-verify ${av.av}: ${new Date().toISOString().slice(0, 10)} ${av.reason}`,
            });
            console.log(`  → 已自动流转到 ${av.target_status}`);
          } catch (e) {
            console.log(`  → 自动流转失败: ${e.message}`);
          }
        }
      } else {
        failed++;
      }
    }

    console.log('='.repeat(60));
    console.log(`检查完成: ${passed} 通过, ${failed} 未通过`);
    if (autoFix) {
      console.log(`通过的任务已自动流转状态`);
    }
    console.log('='.repeat(60));
  } else {
    const taskId = args.find(a => !a.startsWith('--'));
    if (!taskId) {
      console.error('用法: node scripts/review-check.mjs <task-id> [--batch] [--auto-fix] [--target=pending_test]');
      process.exit(1);
    }
    const av = runAutoVerify(taskId);
    console.log('='.repeat(60));
    console.log(`任务: ${av.task_id} — ${av.title || ''}`);
    console.log(`状态: ${av.status} → 目标: ${av.target_status || '(无)'} | AV: ${av.av || 'N/A'}`);
    console.log(`判定: ${av.passed ? '✅ 通过' : '❌ 未通过'}`);
    console.log(`原因: ${av.reason}`);
    if (av.checks?.detail) {
      const d = av.checks.detail;
      console.log(`  handoff_ok=${d.handoff_ok} sections_ok=${d.sections_ok} arch_ok=${d.arch_ok} cost_ok=${d.cost_ok}`);
    }
    console.log('='.repeat(60));
    process.exit(av.passed ? 0 : 1);
  }
}

if (process.argv[1] && (process.argv[1].endsWith('review-check.mjs'))) {
  main();
}