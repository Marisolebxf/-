#!/usr/bin/env node
/**
 * extract-user-stories.mjs — 从产品定义阶段 USM handoff 提取用户故事，生成用户故事库索引。
 *
 * 真源：agent-delivery/agent-handoffs/产品整体定义/ 下全部 USM-*.md（定义阶段产物）
 * 输出：agent-delivery/user-story-library.yaml（索引 + 覆盖状态，implementation_tasks 由 check-story-coverage 回填）
 *
 * 用法：
 *   node scripts/extract-user-stories.mjs                         # dry-run：全量摘要
 *   node scripts/extract-user-stories.mjs --write                 # 全量重写库
 *   node scripts/extract-user-stories.mjs --module E1-企业查询     # 仅该模块 dry-run
 *   node scripts/extract-user-stories.mjs --module SEARCH --write # 按模块增量合并写入
 *   node scripts/extract-user-stories.mjs --detail
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  DEFINITION_ROOT,
  LIBRARY_PATH,
  loadLibrary,
  moduleMatches,
  walkUsmFiles,
  writeLibrary,
} from './lib/user-story-library.mjs';
import { loadStoryModuleMap } from './lib/story-impl-suggest.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

const STORY_HEADING_RE = /^#{3,4}\s+(US-[\w-]+)\s*(.*)$/;
const STORY_BODY_RE =
  /^(?:[>\s]*(?:\*\*)?作为(?:\*\*)?)(.+?)[，,]\s*(?:\*\*)?(?:我想|我想要|我希望)(?:\*\*)?(.+?)[，,]\s*(?:\*\*)?(?:以便|以)(?:\*\*)?(.+?)(?:[。.])?\s*$/;
const ROLE_TABLE_RE = /^\|\s*`ROLE-[\w-]+`\s*\|\s*([^|]+?)\s*\|/;

function parseStories(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const lines = raw.split(/\r?\n/);
  const module = path.basename(path.dirname(file));
  const stories = [];
  let roles = [];
  let inRolesSection = false;
  let current = null;

  for (const line of lines) {
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
        status: 'defined',
        implementation_tasks: [],
      };
      stories.push(current);
      continue;
    }

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

function parseCli(argv) {
  const out = { write: false, detail: false, module: '', help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--write') out.write = true;
    else if (a === '--detail') out.detail = true;
    else if (a === '--module' || a === '-m') out.module = argv[++i] || '';
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function usage() {
  console.log(`Usage:
  node scripts/extract-user-stories.mjs [--module NAME] [--write] [--detail]

  --module   USM 目录名 / 故事 module / ENT-MOD slug（如 E1-企业查询、SEARCH）
  --write    写入 user-story-library.yaml（有 --module 时增量合并，否则全量重写）
  --detail   逐故事打印`);
}

function main() {
  const opts = parseCli(process.argv.slice(2));
  if (opts.help) {
    usage();
    process.exit(0);
  }

  const aliases = loadStoryModuleMap();
  let files = walkUsmFiles(DEFINITION_ROOT);
  if (opts.module) {
    files = files.filter((f) => {
      const dir = path.basename(path.dirname(f));
      return moduleMatches(dir, opts.module, aliases);
    });
    if (!files.length) {
      console.error(`No USM files matched --module ${opts.module}`);
      process.exit(1);
    }
  }
  if (files.length === 0) {
    console.error(`No USM files found under ${DEFINITION_ROOT}`);
    process.exit(1);
  }

  const all = [];
  for (const file of files) all.push(...parseStories(file));

  const seen = new Set();
  const stories = all.filter((s) => {
    if (seen.has(s.id)) return false;
    seen.add(s.id);
    return true;
  });
  stories.sort((a, b) => a.id.localeCompare(b.id));

  const existing = loadLibrary();
  const coverage = new Map(existing.map((s) => [s.id, s]));
  for (const s of stories) {
    const prev = coverage.get(s.id);
    if (prev) {
      s.status = prev.status || 'defined';
      s.implementation_tasks = prev.implementation_tasks || [];
      if (!s.roles?.length && prev.roles?.length) s.roles = prev.roles;
    }
  }

  const withText = stories.filter((s) => s.text);
  const withoutText = stories.filter((s) => !s.text);

  console.log(`USM files scanned : ${files.length}${opts.module ? ` (module=${opts.module})` : ''}`);
  console.log(
    `Stories extracted  : ${stories.length} (${withText.length} with text, ${withoutText.length} without)`,
  );
  console.log(`Modules           : ${[...new Set(stories.map((s) => s.module))].join(' / ')}`);

  if (withoutText.length) {
    console.log('\n[WARN] 以下故事未提取到正文（可能是表格/占位格式，需人工确认）：');
    for (const s of withoutText) console.log(`  - ${s.id}  ${s.title}  (${s.source})`);
  }

  if (opts.detail) {
    for (const s of stories) {
      console.log(`\n[${s.id}] ${s.title}`);
      console.log(`  text  : ${s.text || '(无正文)'}`);
      console.log(`  source: ${s.source}`);
      if (s.roles?.length) console.log(`  roles : ${s.roles.join(' / ')}`);
    }
  }

  if (opts.write) {
    let merged;
    if (opts.module) {
      const touchedModules = new Set(stories.map((s) => s.module));
      const kept = existing.filter(
        (s) => !touchedModules.has(s.module) && !stories.some((n) => n.id === s.id),
      );
      const byId = new Map();
      for (const s of [...kept, ...stories]) byId.set(s.id, s);
      merged = [...byId.values()].sort((a, b) => a.id.localeCompare(b.id));
    } else {
      merged = stories;
    }
    writeLibrary(merged);
    console.log(
      `\nLibrary written: ${LIBRARY_PATH} (${merged.length} stories${opts.module ? ', merged' : ''})`,
    );
  } else {
    console.log('\n(dry-run, add --write to generate/update the library)');
  }
}

main();
