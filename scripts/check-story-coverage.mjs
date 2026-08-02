#!/usr/bin/env node
/**
 * check-story-coverage.mjs — 用户故事「定义 → 实现」覆盖检查。
 *
 * 输入：
 *   - agent-delivery/user-story-library.yaml   用户故事库（extract-user-stories 生成）
 *   - agent-delivery/task-registry.yaml        任务注册表（经 task-registry-lib 读取）
 *
 * 检查项：
 *   1. [ERROR] 任务 user_story 引用了库中不存在的故事 ID（引用完整性）
 *   2. [WARN]  库中「defined」故事没有任何实现任务引用（定义→实现遗漏风险）
 *   3. [WARN]  feature 类型任务未关联任何用户故事（实现→定义缺失）
 *
 * 用法：
 *   node scripts/check-story-coverage.mjs          # 只读报告
 *   node scripts/check-story-coverage.mjs --write  # 回填库的 implementation_tasks/status
 *   node scripts/check-story-coverage.mjs --strict # 有 ERROR/WARN 时 exit 1（可接入 CI）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks } from './lib/task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const LIBRARY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'user-story-library.yaml');

const nowIsoPlus8 = () =>
  new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
    .format(new Date())
    .replace(/(\d{4})-(\d{2})-(\d{2}), (\d{2}):(\d{2}):(\d{2})/, '$1-$2-$3T$4:$5:$6+08:00');

function parseLibrary(text) {
  const stories = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"([^"]+)"/);
    if (idm) {
      current = { id: idm[1], title: '', text: '', module: '', source: '', status: 'defined', implementation_tasks: [] };
      stories.push(current);
      continue;
    }
    if (!current) continue;
    const km = line.match(/^\s{4}([a-z_]+):\s*"((?:[^"\\]|\\.)*)"/);
    if (km) {
      current[km[1]] = km[2];
      continue;
    }
    const lm = line.match(/^\s{4}implementation_tasks:\s*\[(.*)\]\s*$/);
    if (lm) {
      const inner = lm[1].trim();
      current.implementation_tasks = inner
        ? inner.split(/,\s*/).map((s) => s.replace(/^"|"$/g, '')).filter(Boolean)
        : [];
    }
  }
  return stories;
}

function buildLibrary(stories, updated) {
  const q = (s) => `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
  const rows = [];
  for (const s of stories) {
    rows.push(`  - id: ${q(s.id)}`);
    rows.push(`    title: ${q(s.title)}`);
    rows.push(`    text: ${q(s.text)}`);
    rows.push(`    module: ${q(s.module)}`);
    rows.push(`    source: ${q(s.source)}`);
    if (s.roles && s.roles.length) {
      rows.push(`    roles: [${s.roles.map((r) => q(r)).join(', ')}]`);
    }
    rows.push(`    status: ${q(s.status || 'defined')}`);
    rows.push(`    implementation_tasks: [${(s.implementation_tasks || []).map((t) => q(t)).join(', ')}]`);
    rows.push('');
  }
  return [
    '# 用户故事库（User Story Library）',
    '# 内容真源：产品定义阶段 USM（agent-delivery/agent-handoffs/产品整体定义/**/USM-*.md）',
    '# 本文件由 scripts/extract-user-stories.mjs 生成索引；implementation_tasks/status 由 scripts/check-story-coverage.mjs 回填。',
    '# 任务 user_story 字段填写本库故事 ID（多个用逗号分隔），禁止直接写故事全文。',
    '',
    `version: 1`,
    `updated: ${q(updated)}`,
    `source_glob: "agent-delivery/agent-handoffs/产品整体定义/**/USM-*.md"`,
    `story_count: ${stories.length}`,
    'stories:',
    '',
    ...rows,
  ].join('\n');
}

function main() {
  const args = process.argv.slice(2);
  const write = args.includes('--write');
  const strict = args.includes('--strict');

  if (!fs.existsSync(LIBRARY_PATH)) {
    console.error(`Library not found: ${LIBRARY_PATH}`);
    console.error('Run `node scripts/extract-user-stories.mjs --write` first.');
    process.exit(2);
  }

  const stories = parseLibrary(fs.readFileSync(LIBRARY_PATH, 'utf8'));
  const byId = new Map(stories.map((s) => [s.id, s]));

  const { byId: tasksById } = loadAllTasks();
  const tasks = [...tasksById.values()];

  const referenced = new Map(); // storyId -> [taskIds]
  const noStoryTasks = [];
  for (const task of tasks) {
    const ref = (task.user_story || '').trim();
    if (!ref) {
      const type = task.task_type || 'feature';
      if (type === 'feature' && !['done', 'backlog'].includes(task.status)) {
        noStoryTasks.push(task);
      }
      continue;
    }
    for (const sid of ref.split(/[,，]/).map((s) => s.trim()).filter(Boolean)) {
      if (!referenced.has(sid)) referenced.set(sid, []);
      referenced.get(sid).push(task.id);
      if (!byId.has(sid)) {
        console.log(`[ERROR] 任务 ${task.id} 引用了库中不存在的故事 ID: ${sid}`);
      }
    }
  }

  const orphanStories = stories.filter((s) => !referenced.has(s.id));

  console.log('User Story Coverage Report');
  console.log('==========================');
  console.log(`Library stories   : ${stories.length}`);
  console.log(`Feature tasks     : ${tasks.filter((t) => (t.task_type || 'feature') === 'feature').length}`);
  console.log(`Tasks w/ story ref: ${[...referenced.values()].flat().length} refs on ${referenced.size} stories\n`);

  if (orphanStories.length) {
    console.log(`[WARN] 定义未实现（${orphanStories.length} 个故事没有任何实现任务引用，可能存在拆单遗漏）：`);
    for (const s of orphanStories) {
      console.log(`  ${s.id}  ${s.title}  (${s.module})`);
    }
    console.log('');
  } else {
    console.log('[OK] 所有定义的故事均有实现任务承接\n');
  }

  if (noStoryTasks.length) {
    console.log(`[WARN] feature 任务未关联用户故事（${noStoryTasks.length} 个，建议补齐 user_story=故事ID）：`);
    for (const t of noStoryTasks.slice(0, 30)) {
      console.log(`  ${t.id}  ${t.title}  [${t.status}]`);
    }
    if (noStoryTasks.length > 30) console.log(`  … 等共 ${noStoryTasks.length} 个`);
    console.log('');
  } else {
    console.log('[OK] 所有 feature 任务均已关联用户故事\n');
  }

  const orphanCount = orphanStories.length;
  const errorCount = [...referenced.entries()].filter(([sid]) => !byId.has(sid)).length;
  const noStoryCount = noStoryTasks.length;
  console.log(`Summary: story_orphans=${orphanCount} bad_refs=${errorCount} feature_no_story=${noStoryCount}`);

  if (write) {
    for (const [sid, taskIds] of referenced) {
      const s = byId.get(sid);
      if (!s) continue;
      const merged = [...new Set([...(s.implementation_tasks || []), ...taskIds])].sort();
      s.implementation_tasks = merged;
      s.status = merged.length ? 'implemented' : 'defined';
    }
    fs.writeFileSync(LIBRARY_PATH, buildLibrary(stories, nowIsoPlus8()), 'utf8');
    console.log(`\nLibrary updated: ${LIBRARY_PATH}`);
  }

  if (strict && (orphanCount + errorCount + noStoryCount) > 0) process.exit(1);
}

main();
