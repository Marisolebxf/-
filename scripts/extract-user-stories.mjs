#!/usr/bin/env node
/**
 * extract-user-stories.mjs — 从产品定义阶段 USM handoff 提取用户故事，生成用户故事库索引。
 *
 * 真源：agent-delivery/agent-handoffs/产品整体定义/ 下全部 USM-*.md（定义阶段产物）
 * 输出：agent-delivery/user-story-library.yaml（索引 + 覆盖状态，implementation_tasks 由 check-story-coverage 回填）
 *
 * 用法：
 *   node scripts/extract-user-stories.mjs              # dry-run：仅输出提取摘要
 *   node scripts/extract-user-stories.mjs --write      # 生成/更新用户故事库
 *   node scripts/extract-user-stories.mjs --detail     # 逐故事打印（配合 --write 使用）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const DEFINITION_ROOT = path.join(ORCH_ROOT, 'agent-delivery', 'agent-handoffs', '产品整体定义');
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

// 故事标题：兼容 `### US-X｜标题`、`### US-X 标题`、`#### US-X 标题`、`### US-X:标题`
const STORY_HEADING_RE = /^#{3,4}\s+(US-[\w-]+)\s*(.*)$/;

// 故事正文：兼容 `作为…，我想/我想要/我希望…，以便…。` 与 `**作为**…，**我想要**…，**以便**…。`
const STORY_BODY_RE =
  /^(?:[>\s]*(?:\*\*)?作为(?:\*\*)?)(.+?)[，,]\s*(?:\*\*)?(?:我想|我想要|我希望)(?:\*\*)?(.+?)[，,]\s*(?:\*\*)?(?:以便|以)(?:\*\*)?(.+?)(?:[。.])?\s*$/;

// 产品角色表格行：`| \`ROLE-GOV-DECISION\` | 政府科技管理与产业决策人员 | ...`
const ROLE_TABLE_RE = /^\|\s*`ROLE-[\w-]+`\s*\|\s*([^|]+?)\s*\|/;

function walkUsmFiles(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkUsmFiles(full, acc);
    } else if (/^USM-.+\.md$/.test(entry.name)) {
      acc.push(full);
    }
  }
  return acc;
}

function parseStories(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const lines = raw.split(/\r?\n/);
  const module = path.basename(path.dirname(file));
  const stories = [];
  let roles = [];
  let inRolesSection = false;
  let current = null;

  for (const line of lines) {
    // 故事标题优先：避免「…产业链角色」等 ### US- 标题被误判为角色区
    const hm = line.match(STORY_HEADING_RE);
    if (hm) {
      inRolesSection = false;
      current = {
        id: hm[1],
        title: hm[2].trim().replace(/^[｜|:：\s]+/, ''),
        module,
        source: path.relative(ORCH_ROOT, file).replace(/\\/g, '/'),
        text: '',
        roles: [...new Set(roles)],
      };
      stories.push(current);
      continue;
    }

    // 角色区：仅 ##（二级）标题含「角色」时进入；###/#### 故事标题不参与
    if (/^##\s+.*角色/.test(line)) {
      inRolesSection = true;
      continue;
    }
    if (inRolesSection && /^##\s+/.test(line) && !/角色/.test(line)) {
      inRolesSection = false;
    }
    if (inRolesSection) {
      const rm = line.match(ROLE_TABLE_RE);
      if (rm) roles.push(rm[1].trim());
    }
    if (current && !current.text) {
      const trimmed = line.trim();
      if (trimmed === '' || /^[-|>]/.test(trimmed)) continue;
      const bm = line.match(STORY_BODY_RE);
      if (bm) {
        const clean = (s) => String(s).replace(/\*\*/g, '').trim();
        current.text = `作为${clean(bm[1])}，我想${clean(bm[2])}，以便${clean(bm[3])}。`;
      }
    }
  }
  return stories;
}

function yamlQuote(s) {
  return `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

function loadExistingCoverage() {
  // 保留库中已回填的覆盖状态（status / implementation_tasks），提取重跑不丢覆盖信息
  const map = new Map();
  if (!fs.existsSync(LIBRARY_PATH)) return map;
  const text = fs.readFileSync(LIBRARY_PATH, 'utf8');
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"([^"]+)"/);
    if (idm) {
      current = { id: idm[1], status: 'defined', implementation_tasks: [] };
      map.set(current.id, current);
      continue;
    }
    if (!current) continue;
    const sm = line.match(/^\s{4}status:\s*"([^"]+)"/);
    if (sm) { current.status = sm[1]; continue; }
    const lm = line.match(/^\s{4}implementation_tasks:\s*\[(.*)\]\s*$/);
    if (lm) {
      const inner = lm[1].trim();
      current.implementation_tasks = inner
        ? inner.split(/,\s*/).map((s) => s.replace(/^"|"$/g, '')).filter(Boolean)
        : [];
    }
  }
  return map;
}

function buildLibrary(stories, existingCoverage) {
  const q = (s) => `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
  const rows = [];
  for (const s of stories) {
    const prev = existingCoverage.get(s.id);
    const status = prev?.status || 'defined';
    const impl = prev?.implementation_tasks || [];
    rows.push(`  - id: ${q(s.id)}`);
    rows.push(`    title: ${q(s.title)}`);
    rows.push(`    text: ${q(s.text)}`);
    rows.push(`    module: ${q(s.module)}`);
    rows.push(`    source: ${q(s.source)}`);
    if (s.roles && s.roles.length) {
      rows.push(`    roles: [${s.roles.map((r) => q(r)).join(', ')}]`);
    }
    rows.push(`    status: ${q(status)}`);
    rows.push(`    implementation_tasks: [${impl.map((t) => q(t)).join(', ')}]`);
    rows.push('');
  }
  return [
    '# 用户故事库（User Story Library）',
    '# 内容真源：产品定义阶段 USM（agent-delivery/agent-handoffs/产品整体定义/**/USM-*.md）',
    '# 本文件由 scripts/extract-user-stories.mjs 生成索引；implementation_tasks/status 由 scripts/check-story-coverage.mjs 回填。',
    '# 任务 user_story 字段填写本库故事 ID（多个用逗号分隔），禁止直接写故事全文。',
    '# source 为仓库相对路径；飞书投影（agent-delivery/feishu-user-story-board.yaml#handoff_link）自动转 GitLab blob 直链。',
    '',
    `version: 1`,
    `updated: ${q(nowIsoPlus8())}`,
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
  const detail = args.includes('--detail');

  const files = walkUsmFiles(DEFINITION_ROOT);
  if (files.length === 0) {
    console.error(`No USM files found under ${DEFINITION_ROOT}`);
    process.exit(1);
  }

  const all = [];
  for (const file of files) {
    all.push(...parseStories(file));
  }

  // 去重（同一故事 ID 可能出现在多个 USM 中，保留第一个）
  const seen = new Set();
  const stories = all.filter((s) => {
    if (seen.has(s.id)) return false;
    seen.add(s.id);
    return true;
  });
  stories.sort((a, b) => a.id.localeCompare(b.id));

  const withText = stories.filter((s) => s.text);
  const withoutText = stories.filter((s) => !s.text);

  console.log(`USM files scanned : ${files.length}`);
  console.log(`Stories extracted  : ${stories.length} (${withText.length} with text, ${withoutText.length} without)`);
  console.log(`Modules           : ${[...new Set(stories.map((s) => s.module))].join(' / ')}`);

  if (withoutText.length) {
    console.log('\n[WARN] 以下故事未提取到正文（可能是表格/占位格式，需人工确认）：');
    for (const s of withoutText) console.log(`  - ${s.id}  ${s.title}  (${s.source})`);
  }

  if (detail) {
    for (const s of stories) {
      console.log(`\n[${s.id}] ${s.title}`);
      console.log(`  text  : ${s.text || '(无正文)'}`);
      console.log(`  source: ${s.source}`);
      if (s.roles.length) console.log(`  roles : ${s.roles.join(' / ')}`);
    }
  }

  if (write) {
    const existingCoverage = loadExistingCoverage();
    fs.writeFileSync(LIBRARY_PATH, buildLibrary(stories, existingCoverage), 'utf8');
    console.log(`\nLibrary written: ${LIBRARY_PATH} (${stories.length} stories)`);
  } else {
    console.log('\n(dry-run, add --write to generate the library)');
  }
}

main();
