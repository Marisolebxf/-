/**
 * Story-driven implementation task proposals (gate-1 after PDR).
 * Writes only story-impl-proposals.yaml — never auto-merges task-registry.
 */
import fs from 'node:fs';
import path from 'node:path';
import { ORCH_ROOT, loadAllTasks } from './task-registry-lib.mjs';
import {
  loadLibrary,
  moduleMatches,
  nowIsoPlus8,
  yamlQuote,
} from './user-story-library.mjs';

export const STORY_IMPL_TEMPLATES_PATH = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'story-impl-templates.yaml',
);
export const STORY_IMPL_PROPOSALS_PATH = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'story-impl-proposals.yaml',
);

function parseInlineList(value) {
  const v = (value || '').trim();
  const m = v.match(/^\[(.*)\]$/);
  if (!m) return v ? [v.replace(/^["']|["']$/g, '')] : [];
  const inner = m[1].trim();
  if (!inner) return [];
  return inner.split(',').map((s) => s.trim().replace(/^["']|["']$/g, ''));
}

/** Lightweight YAML subset for story-impl-templates.yaml */
export function parseStoryImplTemplates(raw) {
  const doc = {
    module_map: {},
    story_driven_impl: {
      theme_size: 3,
      only_uncovered: true,
      suggested_leaves: [],
    },
  };

  const mapSection = raw.match(/module_map:\s*\r?\n([\s\S]*?)(?:\n# |\nstory_driven_impl:)/);
  if (mapSection) {
    let currentKey = null;
    for (const line of mapSection[1].split(/\r?\n/)) {
      const keym = line.match(/^  ([^:#]+):\s*$/);
      if (keym) {
        currentKey = keym[1].trim();
        doc.module_map[currentKey] = { usm_module: currentKey };
        continue;
      }
      if (!currentKey) continue;
      const fm = line.match(/^\s{4}(\w+):\s*(.+)\s*$/);
      if (fm) {
        doc.module_map[currentKey][fm[1]] = fm[2].trim().replace(/^["']|["']$/g, '');
      }
    }
  }

  const implSection = raw.match(/story_driven_impl:\s*\r?\n([\s\S]*?)$/);
  if (implSection) {
    const body = implSection[1];
    const ts = body.match(/theme_size:\s*(\d+)/);
    if (ts) doc.story_driven_impl.theme_size = Number(ts[1]);
    if (/only_uncovered:\s*false/.test(body)) doc.story_driven_impl.only_uncovered = false;

    const chunks = body.split(/\n\s+- suffix:/).slice(1);
    for (const chunk of chunks) {
      const leaf = { suffix: '', optional: false };
      const lines = (`suffix:${chunk}`).split(/\r?\n/);
      for (const line of lines) {
        const m = line.match(/^\s*(\w+):\s*(.+)\s*$/);
        if (!m) continue;
        const k = m[1];
        let v = m[2].trim().replace(/^["']|["']$/g, '');
        if (k === 'optional') leaf.optional = v === 'true';
        else leaf[k] = v;
      }
      if (leaf.suffix) doc.story_driven_impl.suggested_leaves.push(leaf);
    }
  }

  return doc;
}

export function loadStoryImplTemplates() {
  if (!fs.existsSync(STORY_IMPL_TEMPLATES_PATH)) {
    throw new Error(`Templates not found: ${STORY_IMPL_TEMPLATES_PATH}`);
  }
  return parseStoryImplTemplates(fs.readFileSync(STORY_IMPL_TEMPLATES_PATH, 'utf8'));
}

export function loadStoryModuleMap() {
  try {
    return loadStoryImplTemplates().module_map || {};
  } catch {
    return {};
  }
}

function resolveModuleMeta(moduleName, templates) {
  const map = templates.module_map || {};
  if (map[moduleName]) return { key: moduleName, ...map[moduleName] };
  for (const [key, meta] of Object.entries(map)) {
    if (moduleMatches(moduleName, key, map) || moduleMatches(key, moduleName, map)) {
      return { key, ...meta };
    }
  }
  // fallback: synthesize from module name
  const slug = String(moduleName)
    .replace(/^E-?\d+[_\w-]*-?/, '')
    .replace(/[^A-Za-z0-9\u4e00-\u9fff]/g, '')
    .slice(0, 12)
    .toUpperCase() || 'MOD';
  return {
    key: moduleName,
    slug,
    prefix: `ENT-MOD-${slug}-`,
    dg_task: `ENT-MOD-${slug}-DG-G3`,
    label: moduleName,
    synthesized: true,
  };
}

function chunkThemes(stories, size) {
  const themes = [];
  for (let i = 0; i < stories.length; i += size) {
    const pack = stories.slice(i, i + size);
    themes.push({
      id: `T${themes.length + 1}`,
      stories: pack.map((s) => s.id),
      titles: pack.map((s) => s.title),
    });
  }
  return themes;
}

function buildLeafYaml({ id, title, agent, repo, dependsOn, userStory, difficulty, effort }) {
  const lines = [
    `  - id: ${id}`,
    `    title: "${title.replace(/"/g, '\\"')}"`,
    `    status: backlog`,
    `    agent: ${agent}`,
    `    repo: ${repo}`,
    `    delivery_phase: implementation`,
    `    task_type: feature`,
    `    depends_on: [${dependsOn.map((d) => `"${d}"`).join(', ')}]`,
    `    user_story: "${userStory}"`,
    `    difficulty: ${difficulty || 'M'}`,
    `    effort_points: "${effort || '5'}"`,
    `    note: "故事驱动拆单草案（门1后）；须 PM 审阅后入库；ready 仍等门3 DG confirm"`,
  ];
  return lines.join('\n');
}

function registryHasTask(taskIndex, id) {
  return taskIndex.byId?.has(id) || false;
}

/**
 * Scan uncovered stories → propose implementation leaves + themes.
 */
export function scanStoryImplGaps({ moduleFilter = '', templates = null, includeCovered = false } = {}) {
  const tpl = templates || loadStoryImplTemplates();
  const aliases = tpl.module_map || {};
  const stories = loadLibrary().filter((s) => moduleMatches(s.module, moduleFilter, aliases));
  const onlyUncovered = includeCovered ? false : tpl.story_driven_impl.only_uncovered !== false;
  const themeSize = tpl.story_driven_impl.theme_size || 3;
  const taskIndex = loadAllTasks();

  const byModule = new Map();
  for (const s of stories) {
    const uncovered = !s.implementation_tasks || s.implementation_tasks.length === 0;
    if (onlyUncovered && !uncovered) continue;
    if (!byModule.has(s.module)) byModule.set(s.module, []);
    byModule.get(s.module).push(s);
  }

  const proposals = [];
  for (const [mod, modStories] of byModule) {
    const meta = resolveModuleMeta(mod, tpl);
    const themes = chunkThemes(modStories, themeSize);
    const storyIds = modStories.map((s) => s.id).join(',');
    const label = meta.label || mod;

    for (const leaf of tpl.story_driven_impl.suggested_leaves || []) {
      if (leaf.optional && modStories.length === 0) continue;
      const id = `${meta.prefix}${leaf.suffix}`;
      if (registryHasTask(taskIndex, id)) {
        proposals.push({
          kind: 'story_impl_exists',
          module: mod,
          suggested_task_id: id,
          reason: `registry 已有 ${id}；跳过新建，建议补 user_story=${storyIds}`,
          user_story: storyIds,
          themes,
          status: 'proposed',
          skip_create: true,
        });
        continue;
      }
      const title = (leaf.title || '{label} — impl').replace(/\{label\}/g, label);
      const dependsOn = meta.dg_task ? [meta.dg_task] : [];
      proposals.push({
        kind: 'story_impl_leaf',
        module: mod,
        slug: meta.slug,
        suggested_task_id: id,
        agent: leaf.agent,
        repo: leaf.repo,
        difficulty: leaf.difficulty,
        effort_points: leaf.effort_points,
        user_story: storyIds,
        themes,
        depends_on: dependsOn,
        reason: `门1后故事驱动拆单：模块 ${mod} 有 ${modStories.length} 条未覆盖故事 → 建议 ${id}`,
        suggested_yaml: buildLeafYaml({
          id,
          title,
          agent: leaf.agent,
          repo: leaf.repo,
          dependsOn,
          userStory: storyIds,
          difficulty: leaf.difficulty,
          effort: leaf.effort_points,
        }),
        status: 'proposed',
        skip_create: false,
        synthesized_prefix: !!meta.synthesized,
      });
    }

    // Always emit a theme summary proposal for coordinator handoff
    proposals.push({
      kind: 'story_theme_plan',
      module: mod,
      suggested_task_id: `${meta.prefix}THEME-PLAN`,
      reason: `模块 ${mod} Theme 草案（每包 ≤${themeSize} 故事）；供 Sprint Planning，不入库`,
      user_story: storyIds,
      themes,
      status: 'proposed',
      skip_create: true,
      suggested_yaml: '',
    });
  }

  return proposals;
}

function proposalId(p) {
  return `sip-${(p.suggested_task_id || p.module || 'x').replace(/[^A-Za-z0-9_-]/g, '_')}`;
}

export function loadStoryImplProposals() {
  if (!fs.existsSync(STORY_IMPL_PROPOSALS_PATH)) {
    return { version: 1, updated: nowIsoPlus8(), proposals: [] };
  }
  const raw = fs.readFileSync(STORY_IMPL_PROPOSALS_PATH, 'utf8');
  const proposals = [];
  let current = null;
  let inThemes = false;
  let theme = null;
  for (const line of raw.split(/\r?\n/)) {
    const idm = line.match(/^\s+- id:\s*"?([^"#]+)"?\s*$/);
    if (idm && line.match(/^\s{2}- /)) {
      current = { id: idm[1].trim(), themes: [] };
      proposals.push(current);
      inThemes = false;
      theme = null;
      continue;
    }
    if (!current) continue;
    if (/^\s{4}themes:\s*$/.test(line)) {
      inThemes = true;
      continue;
    }
    if (inThemes && /^\s{6}- id:\s*/.test(line)) {
      theme = { id: line.replace(/^\s{6}- id:\s*"?([^"#]+)"?.*/, '$1').trim(), stories: [] };
      current.themes.push(theme);
      continue;
    }
    if (inThemes && theme && /^\s{8}stories:\s*\[/.test(line)) {
      theme.stories = parseInlineList(line.replace(/^\s{8}stories:\s*/, ''));
      continue;
    }
    if (/^\s{4}\w+:/.test(line) && !/^\s{6}/.test(line)) inThemes = false;
    const km = line.match(/^\s{4}([a-z_]+):\s*"((?:[^"\\]|\\.)*)"/);
    if (km) {
      current[km[1]] = km[2];
      continue;
    }
    const bm = line.match(/^\s{4}(skip_create|synthesized_prefix):\s*(true|false)/);
    if (bm) {
      current[bm[1]] = bm[2] === 'true';
      continue;
    }
    if (/^\s{4}suggested_yaml:\s*\|/.test(line)) {
      current.suggested_yaml = '';
      continue;
    }
    if (current.suggested_yaml !== undefined && /^\s{6}/.test(line)) {
      current.suggested_yaml += `${line.replace(/^\s{6}/, '')}\n`;
    }
  }
  return { version: 1, updated: nowIsoPlus8(), proposals };
}

function serializeProposals(proposals) {
  const q = yamlQuote;
  const lines = [
    '# 故事驱动实现拆单提案队列（门1后）',
    '# 脚本：scripts/suggest-story-impl-tasks.mjs',
    '# 原则：只建议；PM/架构师审阅后手工并入 task-registry；禁止自动 merge；ready 仍等门3',
    '',
    'version: 1',
    `updated: ${q(nowIsoPlus8())}`,
    `proposal_count: ${proposals.length}`,
    'proposals:',
    '',
  ];
  for (const p of proposals) {
    lines.push(`  - id: ${p.id || proposalId(p)}`);
    lines.push(`    kind: ${q(p.kind || '')}`);
    lines.push(`    module: ${q(p.module || '')}`);
    lines.push(`    suggested_task_id: ${q(p.suggested_task_id || '')}`);
    lines.push(`    status: ${q(p.status || 'proposed')}`);
    lines.push(`    reason: ${q(p.reason || '')}`);
    if (p.user_story) lines.push(`    user_story: ${q(p.user_story)}`);
    if (p.agent) lines.push(`    agent: ${q(p.agent)}`);
    if (p.repo) lines.push(`    repo: ${q(p.repo)}`);
    if (p.depends_on?.length) {
      lines.push(`    depends_on: [${p.depends_on.map((d) => q(d)).join(', ')}]`);
    }
    lines.push(`    skip_create: ${p.skip_create ? 'true' : 'false'}`);
    if (p.themes?.length) {
      lines.push('    themes:');
      for (const t of p.themes) {
        lines.push(`      - id: ${q(t.id)}`);
        lines.push(`        stories: [${(t.stories || []).map((s) => q(s)).join(', ')}]`);
      }
    }
    if (p.suggested_yaml) {
      lines.push('    suggested_yaml: |');
      for (const ln of String(p.suggested_yaml).trimEnd().split('\n')) {
        lines.push(`      ${ln}`);
      }
    }
    lines.push('');
  }
  return lines.join('\n');
}

export function appendStoryImplProposals(gaps, { dryRun = false } = {}) {
  const existing = loadStoryImplProposals();
  const byKey = new Map(
    (existing.proposals || []).map((p) => [`${p.kind}|${p.suggested_task_id}`, p]),
  );
  const added = [];
  for (const g of gaps) {
    const key = `${g.kind}|${g.suggested_task_id}`;
    const prev = byKey.get(key);
    if (prev && prev.status === 'proposed') continue;
    const item = { ...g, id: proposalId(g), status: 'proposed' };
    byKey.set(key, item);
    added.push(item);
  }
  const all = [...byKey.values()];
  if (!dryRun) {
    fs.writeFileSync(STORY_IMPL_PROPOSALS_PATH, serializeProposals(all), 'utf8');
  }
  return { added, total: all.length };
}

export function printStoryImplSummary(gaps) {
  const byKind = {};
  for (const g of gaps) byKind[g.kind] = (byKind[g.kind] || 0) + 1;
  console.log('\nSummary:');
  for (const [k, n] of Object.entries(byKind)) console.log(`  ${k}: ${n}`);
}
