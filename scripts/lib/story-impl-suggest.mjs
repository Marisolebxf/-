/**
 * Story-driven implementation task proposals (gate-1 after PDR).
 * Writes only story-impl-proposals.yaml — never auto-merges task-registry.
 */
import fs from 'node:fs';
import path from 'node:path';
import {
  ORCH_ROOT,
  loadAllTasks,
  findTaskBlock,
  writeRegistryText,
  parseTaskBlock,
  getScalar,
  upsertField,
  touchUpdateTime,
} from './task-registry-lib.mjs';
import { yamlFragmentToRegistryBlock } from './registry-gap-suggest.mjs';
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
    `    epic: E-ENT-SCRUM-PDR`,
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
    `    note: "故事驱动拆单（门1后）；飞书「建单已采纳」入库；ready 仍等门3 confirm"`,
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
  let inYaml = false;

  for (const line of raw.split(/\r?\n/)) {
    if (/^\s{2}- id:\s*/.test(line)) {
      current = { id: line.replace(/^\s{2}- id:\s*"?([^"#]+)"?.*/, '$1').trim(), themes: [] };
      proposals.push(current);
      inThemes = false;
      inYaml = false;
      theme = null;
      continue;
    }
    if (!current) continue;

    if (/^\s{4}suggested_yaml:\s*\|/.test(line)) {
      current.suggested_yaml = '';
      inYaml = true;
      inThemes = false;
      continue;
    }
    if (inYaml) {
      if (/^\s{6}/.test(line) || line.trim() === '') {
        current.suggested_yaml += `${line.replace(/^\s{6}/, '')}\n`;
        continue;
      }
      inYaml = false;
    }

    if (/^\s{4}themes:\s*$/.test(line)) {
      inThemes = true;
      continue;
    }
    if (inThemes && /^\s{6}- id:\s*/.test(line)) {
      theme = { id: line.replace(/^\s{6}- id:\s*"?([^"#]+)"?.*/, '$1').trim(), stories: [] };
      current.themes.push(theme);
      continue;
    }
    if (inThemes && theme && /^\s{8}stories:\s*/.test(line)) {
      theme.stories = parseInlineList(line.replace(/^\s{8}stories:\s*/, ''));
      continue;
    }
    if (/^\s{4}\w+:/.test(line)) inThemes = false;

    if (/^\s{4}depends_on:\s*/.test(line)) {
      current.depends_on = parseInlineList(line.replace(/^\s{4}depends_on:\s*/, ''));
      continue;
    }

    const boolm = line.match(
      /^\s{4}(skip_create|synthesized_prefix|registry_merged):\s*(true|false)\s*$/,
    );
    if (boolm) {
      current[boolm[1]] = boolm[2] === 'true';
      continue;
    }

    const qm = line.match(/^\s{4}([a-z_]+):\s*"((?:[^"\\]|\\.)*)"\s*$/);
    if (qm) {
      current[qm[1]] = qm[2];
      continue;
    }
    const um = line.match(/^\s{4}([a-z_]+):\s*(.+?)\s*$/);
    if (um && !['themes', 'depends_on', 'suggested_yaml'].includes(um[1])) {
      current[um[1]] = um[2].replace(/^["']|["']$/g, '');
    }
  }
  return { version: 1, updated: nowIsoPlus8(), proposals };
}

export function saveStoryImplProposals(doc) {
  fs.writeFileSync(
    STORY_IMPL_PROPOSALS_PATH,
    serializeProposals(doc.proposals || []),
    'utf8',
  );
}

function serializeProposals(proposals) {
  const q = yamlQuote;
  const lines = [
    '# 故事驱动实现拆单提案队列（门1后）',
    '# 脚本：scripts/suggest-story-impl-tasks.mjs',
    '# 飞书：派单门控「待审建单」→「建单已采纳」= merge registry backlog；ready 仍等门3 confirm',
    '# 规程：task-creation-guide.md §16',
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
    if (p.feishu_record_id) lines.push(`    feishu_record_id: ${p.feishu_record_id}`);
    if (p.feishu_projected_at) lines.push(`    feishu_projected_at: ${q(p.feishu_projected_at)}`);
    if (p.reviewed_by) lines.push(`    reviewed_by: ${p.reviewed_by}`);
    if (p.reviewed_at) lines.push(`    reviewed_at: ${q(p.reviewed_at)}`);
    if (p.review_note) lines.push(`    review_note: ${q(p.review_note)}`);
    if (p.registry_merged) lines.push('    registry_merged: true');
    if (p.registry_task_id) lines.push(`    registry_task_id: ${p.registry_task_id}`);
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
    if (prev && prev.status === 'proposed') {
      // refresh yaml/themes but keep feishu + review meta
      byKey.set(key, {
        ...prev,
        ...g,
        id: prev.id,
        status: 'proposed',
        feishu_record_id: prev.feishu_record_id,
        feishu_projected_at: prev.feishu_projected_at,
      });
      continue;
    }
    if (prev && prev.status !== 'proposed') continue;
    const item = { ...g, id: proposalId(g), status: 'proposed' };
    byKey.set(key, item);
    added.push(item);
  }
  const all = [...byKey.values()];
  if (!dryRun) saveStoryImplProposals({ proposals: all });
  return { added, total: all.length };
}

export function printStoryImplSummary(gaps) {
  const byKind = {};
  for (const g of gaps) byKind[g.kind] = (byKind[g.kind] || 0) + 1;
  console.log('\nSummary:');
  for (const [k, n] of Object.entries(byKind)) console.log(`  ${k}: ${n}`);
  const doc = loadStoryImplProposals();
  const proposed = (doc.proposals || []).filter(
    (p) => p.status === 'proposed' && !p.skip_create && p.kind === 'story_impl_leaf',
  );
  console.log(`projectable (待审建单): ${proposed.length}`);
}

export function findStoryImplProposalById(doc, id) {
  return (doc.proposals || []).find((p) => p.id === id || p.suggested_task_id === id);
}

export function resolveStoryImplProposal(ref = {}) {
  const doc = loadStoryImplProposals();
  if (ref.proposalId) return findStoryImplProposalById(doc, ref.proposalId);
  if (ref.recordId) {
    return (doc.proposals || []).find((p) => p.feishu_record_id === ref.recordId) || null;
  }
  if (ref.taskId) {
    return (
      (doc.proposals || []).find(
        (p) => p.suggested_task_id === ref.taskId && p.kind === 'story_impl_leaf',
      ) ||
      (doc.proposals || []).find((p) => p.suggested_task_id === ref.taskId) ||
      null
    );
  }
  return null;
}

export function buildVirtualTaskFromStoryProposal(proposal) {
  const title =
    proposal.suggested_yaml?.match(/^\s*title:\s*"?(.+?)"?\s*$/m)?.[1]?.trim() ||
    proposal.reason ||
    proposal.suggested_task_id;
  return {
    id: proposal.suggested_task_id,
    title,
    status: 'backlog',
    agent: proposal.agent || '',
    epic: 'E-ENT-SCRUM-PDR',
    delivery_phase: 'implementation',
    priority: 'P0',
    record_id: proposal.feishu_record_id || '',
    user_story: proposal.user_story || '',
    note: `[故事拆单 ${proposal.id}] ${proposal.reason || ''}`,
  };
}

export function upsertStoryImplFeishuMeta(proposalId, meta, dryRun = false) {
  const doc = loadStoryImplProposals();
  const p = findStoryImplProposalById(doc, proposalId);
  if (!p) throw new Error(`story-impl proposal not found: ${proposalId}`);
  Object.assign(p, meta);
  if (!dryRun) saveStoryImplProposals(doc);
  return p;
}

export function reviewStoryImplProposals(opts) {
  const { action, ids = [], all = false, approvedBy, note = '', dryRun = false } = opts;
  if (!['accept', 'reject'].includes(action)) {
    throw new Error(`invalid action: ${action}`);
  }
  const doc = loadStoryImplProposals();
  const { byId } = loadAllTasks();
  const idSet = new Set(ids);
  const targets = (doc.proposals || []).filter((p) => {
    if (p.status !== 'proposed') return false;
    if (p.skip_create || p.kind === 'story_theme_plan') return false;
    if (all) return true;
    return idSet.has(p.id) || idSet.has(p.suggested_task_id);
  });
  if (!targets.length) {
    throw new Error('no matching proposed story-impl leaf proposals');
  }
  const now = new Date().toISOString();
  for (const p of targets) {
    p.status = action === 'accept' ? 'accepted' : 'rejected';
    p.reviewed_by = approvedBy;
    p.reviewed_at = now;
    if (note) p.review_note = note;
    if (action === 'accept' && byId.has(p.suggested_task_id)) {
      p.registry_merged = true;
      p.registry_task_id = p.suggested_task_id;
    }
  }
  if (!dryRun) saveStoryImplProposals(doc);
  return { doc, updated: targets, action };
}

export function mergeStoryImplProposalIntoRegistry(proposal, opts = {}) {
  const { dryRun = false, allowMissingDeps = true } = opts;
  if (proposal.skip_create || proposal.kind === 'story_theme_plan') {
    throw new Error(`proposal ${proposal.id} is not creatable (skip_create / theme plan)`);
  }
  if (!proposal?.suggested_yaml?.trim()) {
    throw new Error(`proposal ${proposal?.id || '?'} has no suggested_yaml`);
  }

  const taskId = proposal.suggested_task_id;
  const { lines, byId } = loadAllTasks();
  if (byId.has(taskId)) {
    return { action: 'noop', taskId, reason: 'already_in_registry' };
  }

  const blockLines = yamlFragmentToRegistryBlock(proposal.suggested_yaml);
  const parsed = parseTaskBlock(blockLines);
  if (parsed.id !== taskId) {
    throw new Error(`suggested_yaml id ${parsed.id} != ${taskId}`);
  }

  const deps = proposal.depends_on?.length ? proposal.depends_on : parsed.depends_on || [];
  const missingDeps = [];
  for (const dep of deps) {
    if (dep && !byId.has(dep)) missingDeps.push(dep);
  }
  if (missingDeps.length && !allowMissingDeps) {
    throw new Error(`depends_on missing in registry: ${missingDeps.join(', ')}`);
  }

  if (proposal.feishu_record_id) {
    upsertField(blockLines, 'feishu_bitable_record_id', proposal.feishu_record_id);
  }
  if (proposal.user_story) {
    upsertField(blockLines, 'user_story', proposal.user_story);
  }
  const mergeTag = `story-impl ${proposal.id} merged ${new Date().toISOString().slice(0, 10)}`;
  const missNote = missingDeps.length ? ` | deps_pending=${missingDeps.join(',')}` : '';
  const prevNote = getScalar(blockLines, 'note');
  upsertField(
    blockLines,
    'note',
    prevNote ? `${prevNote} | ${mergeTag}${missNote}` : `${mergeTag}${missNote}`,
  );
  touchUpdateTime(blockLines);

  let insertAt = lines.length;
  const anchor = deps.find((d) => byId.has(d)) || deps[0];
  if (anchor && byId.has(anchor)) {
    const loc = findTaskBlock(lines, anchor);
    if (loc) insertAt = loc.end;
  }

  if (dryRun) {
    return { action: 'dry_run', taskId, insertAt, blockLines, missingDeps };
  }

  const newLines = [...lines.slice(0, insertAt), ...blockLines, ...lines.slice(insertAt)];
  writeRegistryText(newLines.join('\n'));
  return { action: 'merged', taskId, insertAt, anchor: anchor || '', missingDeps };
}

export function acceptStoryImplWithMerge(proposal, opts = {}) {
  const mergeResult = mergeStoryImplProposalIntoRegistry(proposal, opts);
  const reviewResult = reviewStoryImplProposals({
    action: 'accept',
    ids: [proposal.id],
    approvedBy: opts.approvedBy,
    note: opts.note || '',
    dryRun: opts.dryRun,
  });
  if (!opts.dryRun && (mergeResult.action === 'merged' || mergeResult.action === 'noop')) {
    const doc = loadStoryImplProposals();
    const p = findStoryImplProposalById(doc, proposal.id);
    if (p) {
      p.registry_merged = true;
      p.registry_task_id = proposal.suggested_task_id;
      saveStoryImplProposals(doc);
    }
  }
  return { mergeResult, reviewResult };
}
