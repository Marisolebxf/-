#!/usr/bin/env node
// normalize-legacy-paths.mjs
// 把编排资产里的老根 / 老仓名 / 老 GitLab group 规范化为 ${GKX_ROOT} / 新仓名 / gkx-lumen。
// 幂等：可重复运行，已规范化的不重复改。
//
// 用法：
//   node scripts/normalize-legacy-paths.mjs --dry-run     # 预览将改动哪些文件 + 改动数
//   node scripts/normalize-legacy-paths.mjs --apply       # 执行替换
//   node scripts/normalize-legacy-paths.mjs --apply --path agent-delivery/task-registry.yaml  # 单文件
//
// 设计：
//   - 老根 E:/gkx_src（code_root 语义）→ ${GKX_ROOT}
//   - 老根 + 老仓（demo_ref 语义）→ ${GKX_ROOT}/repos/{新名}
//   - archived 仓（gkx_demo_python / gkx_ui_demo）→ ${GKX_LEGACY_ROOT}/repos/{老名} (archived)
//   - 老仓名（独立出现）→ 新名
//   - SZCGKX → gkx-lumen（GitLab group）
//   - 历史 RFC / ARCHIVE 文档：同样替换，但保留决策语义（用 ${GKX_LEGACY_ROOT} 占位老根）
//
// 关联：
//   - 00-path-resolution.mdc（路径真源铁律）
//   - paths.yaml#legacy.rename_map（权威改名表）
//   - verify-paths.sh（校验脚本，替换后应跑 --strict 通过）
//   - RFC-002 §7.3.2（10 仓改名表）

import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, extname } from 'node:path';

// ============================================================
// 替换映射表（权威来源：paths.yaml#legacy.rename_map + RFC-002 §7.3.2）
// ============================================================

// 老根 → 新根占位符（code_root 语义）
// 注意：老根下直接挂老仓名（如 E:\gkx_src\ent-analysis-demo）需补 repos/ 段
//       所以先做"老根 + 老仓名 → 新根 + repos/ + 新名"的完整路径替换，再做纯根替换
const ROOT_REPLACEMENTS = [
  // 老根 E:/gkx_src（正反斜杠都匹配）→ ${GKX_ROOT}
  [/(?:E|e):[\\/]+gkx_src/g, '${GKX_ROOT}'],
  // 新根硬编码 E:/gkx-lumen → ${GKX_ROOT}（verify-paths 检查项 2）
  [/(?:E|e):[\\/]+gkx-lumen/g, '${GKX_ROOT}'],
  // docs_root 老根 e:/实施/2025/智谱-深圳国科信 → ${GKX_DOCS_ROOT}
  [/(?:E|e):[\\/]实施[\\/]2025[\\/]智谱-深圳国科信/g, '${GKX_DOCS_ROOT}'],
];

// 仓改名映射（顺序重要：先替换带路径前缀的，再替换独立名）
// archived 仓不在此表，单独处理
// 第一组：老根 + 老仓名 → 新根 + repos/ + 新名（处理 E:\gkx_src\老仓 这种直接挂在老根下的路径）
const REPO_PATH_WITH_LEGACY_ROOT = [
  // 老根后直接跟老仓名（正反斜杠），替换为 ${GKX_ROOT}/repos/新名
  [/(?:E|e):[\\/]+gkx_src[\\/]+demo2(?=[\\/]|$|\b)/g, '${GKX_ROOT}/repos/demo-ui-science'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_lumen_backend/g, '${GKX_ROOT}/repos/lumen-svc-platform'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_lumen_fronted_pc/g, '${GKX_ROOT}/repos/lumen-ui-science-pc'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_lumen_fronted_topic/g, '${GKX_ROOT}/repos/lumen-ui-topic'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_lumen_fronted_mobile/g, '${GKX_ROOT}/repos/lumen-ui-science-mobile'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_service_demo/g, '${GKX_ROOT}/repos/demo-svc-platform'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_demo_ui/g, '${GKX_ROOT}/repos/demo-ui-system-test'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+innov-algo-demo/g, '${GKX_ROOT}/repos/demo-algo-science'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+ent-analysis-demo/g, '${GKX_ROOT}/repos/demo-algo-ent-analysis'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+topic_demo/g, '${GKX_ROOT}/repos/demo-ui-topic'],
];

// archived 仓路径（老根 + archived 仓）→ 保留为 ${GKX_LEGACY_ROOT} 占位
const ARCHIVED_PATH_REPLACEMENTS = [
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_demo_python/g, '${GKX_LEGACY_ROOT}/repos/gkx_demo_python (archived)'],
  [/(?:E|e):[\\/]+gkx_src[\\/]+gkx_ui_demo/g, '${GKX_LEGACY_ROOT}/repos/gkx_ui_demo (archived)'],
];

// archived 仓（不迁移，保留老名 + archived 标记）
// 仅当作为路径引用时替换为占位符；作为历史叙述时保留
const ARCHIVED_REPOS = ['gkx_demo_python', 'gkx_ui_demo'];

// 独立老仓名 → 新名（用于 title / 叙述性文本）
// 注意：archived 仓不替换
const STANDALONE_RENAME = [
  ['gkx_lumen_fronted_pc', 'lumen-ui-science-pc'],
  ['gkx_lumen_fronted_topic', 'lumen-ui-topic'],
  ['gkx_lumen_fronted_mobile', 'lumen-ui-science-mobile'],
  ['gkx_lumen_backend', 'lumen-svc-platform'],
  ['gkx_service_demo', 'demo-svc-platform'],
  ['gkx_demo_ui', 'demo-ui-system-test'],
  ['innov-algo-demo', 'demo-algo-science'],
  ['ent-analysis-demo', 'demo-algo-ent-analysis'],
  ['topic_demo', 'demo-ui-topic'],
  // demo2 作为仓名时替换（但避免误伤 "demo2 阶段" 等叙述——用词边界）
  // demo2 较特殊，单独处理见下
];

// SZCGKX → gkx-lumen（GitLab group）
// 同时处理路径形式（SZCGKX/）和叙述形式（SZCGKX 后跟空格/中文等）
const GITLAB_GROUP_REPLACEMENTS = [
  [/gitlab\.htmisoft\.net\/SZCGKX/g, 'gitlab.htmisoft.net/gkx-lumen'],
  [/SZCGKX\//g, 'gkx-lumen/'],
  // SZCGKX 后跟非字母数字（如空格、中文"下"、引号、句末），替换为 gkx-lumen
  // 注意：必须在 SZCGKX/ 之后处理，避免误改已替换的 gkx-lumen/
  [/SZCGKX(?=[^a-zA-Z0-9/-]|$)/g, 'gkx-lumen'],
];

// 排除目录（不扫描）
const EXCLUDE_DIRS = new Set([
  '.git', 'node_modules', '.trunk', '_old', 'dist', 'build',
]);

// 排除文件（历史决策文档 / 已完成 handoff / 校验脚本自身，保留原样以保真或保功能）
// - RFC-001/002/003：历史决策记录，老根 E:/gkx_src 是决策当时的客观事实，替换会反转语义
// - ARCHIVE-OLD-ROOT.md：老根归档清单，记录的是历史快照
// - agent-handoffs/：已完成任务的执行记录，路径是当时事实
// - verify-paths.sh：校验脚本自身的"老仓名检查列表"必须保留老名，否则校验失效
// - _tmp_diff.mjs：临时调试脚本，不参与替换
// 决策来源：用户 2026-07-28 确认（公约 §3.3 失败可逆 + 决策可追溯）
const EXCLUDE_FILE_PATTERNS = [
  /[/\\]RFC[/\\]RFC-001-git-workspace-redesign\.md$/,
  /[/\\]RFC[/\\]RFC-002-gkx-v2-greenfield-rebuild\.md$/,
  /[/\\]RFC[/\\]RFC-003-feishu-bitable-webhook\.md$/,
  /[/\\]ARCHIVE-OLD-ROOT\.md$/,
  /[/\\]agent-handoffs[/\\]/,  // 整个 handoffs 目录保留原样
  /[/\\]scripts[/\\]verify-paths\.sh$/,  // 校验脚本的老名列表需保留
  /[/\\]scripts[/\\]_tmp_diff\.mjs$/,    // 临时脚本
  /[/\\]scripts[/\\]normalize-legacy-paths\.mjs$/,  // 本脚本自身
];

// 处理的扩展名
const INCLUDE_EXTS = new Set([
  '.md', '.yaml', '.yml', '.json', '.ps1', '.sh', '.py', '.mdc', '.mjs',
]);

// ============================================================
// 核心替换逻辑
// ============================================================

function applyReplacements(content) {
  let result = content;
  const before = result;

  // 1a. archived 仓路径替换（先于普通根替换，避免 archived 仓被误匹配）
  for (const [pattern, replacement] of ARCHIVED_PATH_REPLACEMENTS) {
    result = result.replace(pattern, replacement);
  }

  // 1b. 老根 + 老仓名 → 新根 + repos/ + 新名（先于纯根替换，否则老仓名会丢失）
  for (const [pattern, replacement] of REPO_PATH_WITH_LEGACY_ROOT) {
    result = result.replace(pattern, replacement);
  }

  // 2. 纯根路径替换（E:/gkx_src → ${GKX_ROOT} 等，此时仓路径已处理完）
  for (const [pattern, replacement] of ROOT_REPLACEMENTS) {
    result = result.replace(pattern, replacement);
  }

  // 3. 独立老仓名替换（叙述性文本里的仓名，无路径前缀）
  //    用 split/join 避免 regex 转义问题；新名与老名无重叠，全局替换安全
  for (const [oldName, newName] of STANDALONE_RENAME) {
    if (ARCHIVED_REPOS.includes(oldName)) continue;
    const occurrences = result.split(oldName).length - 1;
    if (occurrences > 0) {
      result = result.split(oldName).join(newName);
    }
  }

  // 4. demo2 作为仓名替换（避免误伤 "demo2 阶段"/"demo2 沙箱" 等叙述）
  //    仅在路径上下文（如 /demo2、repos/demo2、E:/.../demo2）替换
  result = result.replace(/([\\/]|\brepos\/)demo2(?=[\\/]|\b)/g, '$1demo-ui-science');
  // "demo2_proto" → "demo-ui-science"（仓标识）
  result = result.replace(/\bdemo2_proto\b/g, 'demo-ui-science');

  // 5. GitLab group 替换
  //    SZCGKX/ → gkx-lumen/（路径形式）
  //    SZCGKX 后跟非斜杠（如 "SZCGKX 下创建"）→ gkx-lumen
  for (const [pattern, replacement] of GITLAB_GROUP_REPLACEMENTS) {
    result = result.replace(pattern, replacement);
  }

  return { content: result, changed: before !== result };
}

// ============================================================
// 文件遍历
// ============================================================

function walk(dir, files = []) {
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (EXCLUDE_DIRS.has(entry.name)) continue;
      walk(full, files);
    } else if (entry.isFile()) {
      if (INCLUDE_EXTS.has(extname(entry.name))) {
        // 排除历史决策文档 / 已完成 handoff（保留原样保真）
        const isExcluded = EXCLUDE_FILE_PATTERNS.some(p => p.test(full));
        if (isExcluded) continue;
        files.push(full);
      }
    }
  }
  return files;
}

// ============================================================
// 主逻辑
// ============================================================

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const apply = args.includes('--apply');
const pathArgIdx = args.indexOf('--path');
const singlePath = pathArgIdx >= 0 ? args[pathArgIdx + 1] : null;

if (!dryRun && !apply) {
  console.error('用法: node scripts/normalize-legacy-paths.mjs --dry-run | --apply [--path <file>]');
  process.exit(1);
}

const root = process.cwd();
if (!statSync(join(root, 'agent-delivery')).isDirectory()) {
  console.error('❌ 请在 gkx-orchestration/ 根目录执行');
  process.exit(1);
}

const files = singlePath
  ? [join(root, singlePath)]
  : walk(root).filter(f => !f.includes(join('scripts', 'normalize-legacy-paths')));

let totalChanged = 0;
let totalFiles = 0;
const changedFiles = [];

for (const file of files) {
  let content;
  try {
    content = readFileSync(file, 'utf8');
  } catch (e) {
    continue; // 二进制 / 编码问题跳过
  }

  const { content: newContent, changed } = applyReplacements(content);
  if (changed) {
    totalFiles++;
    const rel = relative(root, file);
    // 统计该文件改动行数（粗略：diff 行）
    const oldLines = content.split('\n');
    const newLines = newContent.split('\n');
    let diffLines = 0;
    const maxLen = Math.max(oldLines.length, newLines.length);
    for (let i = 0; i < maxLen; i++) {
      if (oldLines[i] !== newLines[i]) diffLines++;
    }
    totalChanged += diffLines;
    changedFiles.push({ file: rel, diffLines });

    if (apply) {
      writeFileSync(file, newContent, 'utf8');
    }
  }
}

// 输出报告
console.log('=== normalize-legacy-paths ===');
console.log(`模式: ${apply ? 'APPLY（已执行）' : 'DRY-RUN（预览）'}`);
console.log(`改动文件: ${totalFiles}`);
console.log(`改动行数: ${totalChanged}`);
console.log('');
console.log('改动文件清单（按改动行数降序，前 30）:');
changedFiles
  .sort((a, b) => b.diffLines - a.diffLines)
  .slice(0, 30)
  .forEach(f => console.log(`  ${f.diffLines.toString().padStart(4)} 行  ${f.file}`));
if (changedFiles.length > 30) {
  console.log(`  ... 还有 ${changedFiles.length - 30} 个文件`);
}
