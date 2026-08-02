/**
 * Shared helpers for user-story-library.yaml (parse / write / module filter).
 */
import fs from 'node:fs';
import path from 'node:path';
import { ORCH_ROOT } from './task-registry-lib.mjs';

export const LIBRARY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'user-story-library.yaml');
export const DEFINITION_ROOT = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'agent-handoffs',
  '产品整体定义',
);

export function nowIsoPlus8() {
  return new Intl.DateTimeFormat('en-CA', {
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
}

export function yamlQuote(s) {
  return `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

export function parseLibrary(text) {
  const stories = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"([^"]+)"/);
    if (idm) {
      current = {
        id: idm[1],
        title: '',
        text: '',
        module: '',
        source: '',
        roles: [],
        status: 'defined',
        implementation_tasks: [],
      };
      stories.push(current);
      continue;
    }
    if (!current) continue;
    const rolesm = line.match(/^\s{4}roles:\s*\[(.*)\]\s*$/);
    if (rolesm) {
      const inner = rolesm[1].trim();
      current.roles = inner
        ? inner.split(/,\s*/).map((s) => s.replace(/^"|"$/g, '')).filter(Boolean)
        : [];
      continue;
    }
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

export function loadLibrary() {
  if (!fs.existsSync(LIBRARY_PATH)) return [];
  return parseLibrary(fs.readFileSync(LIBRARY_PATH, 'utf8'));
}

export function buildLibraryYaml(stories, updated = nowIsoPlus8()) {
  const q = yamlQuote;
  const rows = [];
  for (const s of stories) {
    rows.push(`  - id: ${q(s.id)}`);
    rows.push(`    title: ${q(s.title || '')}`);
    rows.push(`    text: ${q(s.text || '')}`);
    rows.push(`    module: ${q(s.module || '')}`);
    rows.push(`    source: ${q(s.source || '')}`);
    if (s.roles && s.roles.length) {
      rows.push(`    roles: [${s.roles.map((r) => q(r)).join(', ')}]`);
    }
    rows.push(`    status: ${q(s.status || 'defined')}`);
    rows.push(
      `    implementation_tasks: [${(s.implementation_tasks || []).map((t) => q(t)).join(', ')}]`,
    );
    rows.push('');
  }
  return [
    '# 用户故事库（User Story Library）',
    '# 内容真源：产品定义阶段 USM（agent-delivery/agent-handoffs/产品整体定义/**/USM-*.md）',
    '# 本文件由 scripts/extract-user-stories.mjs 生成索引；implementation_tasks/status 由 scripts/check-story-coverage.mjs 回填。',
    '# status 细粒度：defined|sprint_planned|developing|dev_complete|integrating|testing|done（scripts/lib/story-progress.mjs）。',
    '# 任务 user_story 字段填写本库故事 ID（多个用逗号分隔），禁止直接写故事全文。',
    '# 门1 PDR 完整闭合后可按模块增量写入（extract --module … --write）；见 gkx-story-library-ingest skill。',
    '',
    'version: 1',
    `updated: ${q(updated)}`,
    'source_glob: "agent-delivery/agent-handoffs/产品整体定义/**/USM-*.md"',
    `story_count: ${stories.length}`,
    'stories:',
    '',
    ...rows,
  ].join('\n');
}

export function writeLibrary(stories) {
  fs.writeFileSync(LIBRARY_PATH, buildLibraryYaml(stories), 'utf8');
  return LIBRARY_PATH;
}

/**
 * Match USM dirname / story.module / ENT-MOD slug alias.
 * Filter may be: exact USM dir, slug (SEARCH), or ENT-MOD-SEARCH / ENT-MOD-SEARCH-.
 */
export function moduleMatches(candidate, filter, aliases = {}) {
  if (!filter) return true;
  const f = String(filter).trim();
  const c = String(candidate || '').trim();
  if (!c) return false;
  if (c === f) return true;

  const filterMeta = aliases[f];
  if (filterMeta) {
    return c === f || c === filterMeta.usm_module;
  }

  const candMeta = aliases[c];
  if (candMeta) {
    const slug = candMeta.slug || '';
    const prefix = (candMeta.prefix || '').replace(/-$/, '');
    if (
      f === slug ||
      f === candMeta.label ||
      f === candMeta.prefix ||
      f === prefix ||
      f === `ENT-MOD-${slug}` ||
      f === `ENT-MOD-${slug}-`
    ) {
      return true;
    }
  }

  for (const [mod, meta] of Object.entries(aliases)) {
    const slug = meta.slug || '';
    const prefix = (meta.prefix || '').replace(/-$/, '');
    if (
      f === slug ||
      f === meta.prefix ||
      f === prefix ||
      f === `ENT-MOD-${slug}` ||
      f === `ENT-MOD-${slug}-`
    ) {
      return c === mod || c === meta.usm_module;
    }
  }

  // Long substring fallback (avoid short slug false positives)
  if (f.length >= 6 && (c.includes(f) || f.includes(c))) return true;
  return false;
}

export function walkUsmFiles(dir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkUsmFiles(full, acc);
    else if (/^USM-.+\.md$/.test(entry.name)) acc.push(full);
  }
  return acc;
}
