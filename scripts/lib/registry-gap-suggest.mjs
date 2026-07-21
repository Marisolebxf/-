#!/usr/bin/env node
/**
 * Registry gap detection: missing definition/implementation leaves, broken depends_on.
 * Does NOT write task-registry.yaml — only suggests via registry-gap-proposals.yaml.
 */

import fs from 'node:fs';
import path from 'node:path';
import {
  ORCH_ROOT,
  loadAllTasks,
  isDoneStatus,
} from './task-registry-lib.mjs';

export const TEMPLATES_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'registry-gap-templates.yaml');
export const PROPOSALS_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'registry-gap-proposals.yaml');

function parseInlineListYaml(value) {
  const v = (value || '').trim();
  const m = v.match(/^\[(.*)\]$/);
  if (!m) return v ? [v.replace(/^["']|["']$/g, '')] : [];
  const inner = m[1].trim();
  if (!inner) return [];
  return inner.split(',').map((s) => s.trim().replace(/^["']|["']$/g, ''));
}

function parseLeafBlock(body) {
  const leaf = { required: true, depends_suffixes: [] };
  const get = (k) => body.match(new RegExp(`^\\s*${k}:\\s*(.+)$`, 'm'))?.[1]?.trim();
  if (get('suffix')) leaf.suffix = get('suffix').replace(/^["']|["']$/g, '');
  if (/required:\s*false/.test(body)) leaf.required = false;
  if (get('agent')) leaf.agent = get('agent');
  if (get('repo')) leaf.repo = get('repo');
  const repos = get('repos');
  if (repos) leaf.repos = parseInlineListYaml(repos);
  if (get('title')) leaf.title = get('title').replace(/^["']|["']$/g, '');
  if (get('cicd')) leaf.cicd = get('cicd');
  if (/optional:\s*true/.test(body)) leaf.optional = true;
  const dep = get('depends_suffixes');
  if (dep) leaf.depends_suffixes = parseInlineListYaml(dep);
  const alts = get('alternates');
  if (alts) leaf.alternates = parseInlineListYaml(alts);
  const altsOk = get('alternates_exist_ok');
  if (altsOk) leaf.alternates_exist_ok = parseInlineListYaml(altsOk);
  const v1g = body.match(/depends_suffix_groups:\s*\r?\n\s+v1:\s*\[(.*?)\]/);
  if (v1g) leaf.depends_suffix_groups = { v1: parseInlineListYaml(`[${v1g[1]}]`) };
  return leaf;
}

export function parseGapTemplates(raw) {
  const doc = {
    definition_chain: { anchor_suffix: 'PACK-L01', leaves: [] },
    implementation_recommended: {
      dg_suffix: 'DG-G3',
      min_impl_tasks_after_dg_done: 1,
      suggested_leaves: [],
    },
    slug_labels: {},
  };

  const anchor = raw.match(/anchor_suffix:\s*(\S+)/);
  if (anchor) doc.definition_chain.anchor_suffix = anchor[1];

  const defSection = raw.match(/definition_chain:\s*\r?\n([\s\S]*?)(?:\n# |\nimplementation_recommended:)/);
  if (defSection) {
    const chunks = defSection[1].split(/\n\s+- /).slice(1);
    for (const chunk of chunks) {
      doc.definition_chain.leaves.push(parseLeafBlock(chunk));
    }
  }

  const implSection = raw.match(/implementation_recommended:\s*\r?\n([\s\S]*?)(?:\nslug_labels:)/);
  if (implSection) {
    const ib = implSection[1];
    const dg = ib.match(/dg_suffix:\s*(\S+)/);
    if (dg) doc.implementation_recommended.dg_suffix = dg[1];
    const min = ib.match(/min_impl_tasks_after_dg_done:\s*(\d+)/);
    if (min) doc.implementation_recommended.min_impl_tasks_after_dg_done = Number(min[1]);
    const chunks = ib.split(/\n\s+- suffix:/).slice(1);
    for (const chunk of chunks) {
      doc.implementation_recommended.suggested_leaves.push(parseLeafBlock(`suffix:${chunk}`));
    }
  }

  const slugBlock = raw.match(/slug_labels:\s*\r?\n([\s\S]*?)$/);
  if (slugBlock) {
    for (const m of slugBlock[1].matchAll(/^\s+(\w+):\s*(.+)$/gm)) {
      doc.slug_labels[m[1]] = m[2].trim();
    }
  }
  return doc;
}

export function loadGapTemplates() {
  if (!fs.existsSync(TEMPLATES_PATH)) {
    throw new Error(`Templates not found: ${TEMPLATES_PATH}`);
  }
  return parseGapTemplates(fs.readFileSync(TEMPLATES_PATH, 'utf8'));
}

export function loadGapProposals() {
  if (!fs.existsSync(PROPOSALS_PATH)) {
    return { version: 1, proposals: [] };
  }
  const raw = fs.readFileSync(PROPOSALS_PATH, 'utf8');
  const proposals = [];
  if (!/proposals:\s*\[\]/.test(raw)) {
    const chunks = raw.split(/\n\s+- id:/).slice(1);
    for (const chunk of chunks) {
      const body = `id:${chunk}`;
      const get = (k) => body.match(new RegExp(`^\\s*${k}:\\s*(.+)$`, 'm'))?.[1]?.trim().replace(/^["']|["']$/g, '') || '';
      proposals.push({
        id: get('id'),
        status: get('status') || 'proposed',
        kind: get('kind'),
        suggested_task_id: get('suggested_task_id'),
        module_prefix: get('module_prefix'),
        module_slug: get('module_slug'),
        delivery_phase: get('delivery_phase'),
        reason: get('reason'),
        trigger: get('trigger'),
        agent: get('agent'),
        suggested_yaml: get('suggested_yaml'),
        created_at: get('created_at'),
      });
    }
  }
  return { version: 1, updated: new Date().toISOString().slice(0, 10), proposals };
}

export function saveGapProposals(doc) {
  doc.updated = new Date().toISOString().slice(0, 10);
  const lines = [
    '# registry 建单建议队列（PM 审阅后手工并入 task-registry.yaml）',
    '# 由 scripts/suggest-registry-tasks.mjs --write 追加；勿自动 merge',
    '# 规程：agent-delivery/task-creation-guide.md §13',
    '',
    'version: 1',
    `updated: "${doc.updated}"`,
    'doc: agent-delivery/task-creation-guide.md',
  ];
  if (!doc.proposals?.length) {
    lines.push('proposals: []');
  } else {
    lines.push('proposals:');
    for (const p of doc.proposals) {
      lines.push(`  - id: ${p.id}`);
      lines.push(`    status: ${p.status || 'proposed'}`);
      lines.push(`    kind: ${p.kind}`);
      lines.push(`    suggested_task_id: ${p.suggested_task_id}`);
      lines.push(`    module_prefix: "${p.module_prefix || ''}"`);
      lines.push(`    module_slug: ${p.module_slug || ''}`);
      lines.push(`    delivery_phase: ${p.delivery_phase || ''}`);
      lines.push(`    reason: "${(p.reason || '').replace(/"/g, '\\"')}"`);
      lines.push(`    trigger: ${p.trigger || ''}`);
      if (p.agent) lines.push(`    agent: ${p.agent}`);
      if (p.depends_on?.length) {
        lines.push('    depends_on:');
        for (const d of p.depends_on) lines.push(`      - ${d}`);
      }
      if (p.suggested_yaml) {
        lines.push('    suggested_yaml: |');
        for (const ln of p.suggested_yaml.split('\n')) lines.push(`      ${ln}`);
      }
      lines.push(`    created_at: "${p.created_at || new Date().toISOString()}"`);
    }
  }
  lines.push('');
  fs.writeFileSync(PROPOSALS_PATH, lines.join('\n'), 'utf8');
}

export function discoverModulePrefixes(byId, filterPrefix = '') {
  const prefixes = new Map();
  for (const task of byId.values()) {
    const m = task.id.match(/^(ENT-MOD-[A-Z]+-)/);
    if (!m) continue;
    const prefix = m[1];
    if (filterPrefix && !prefix.startsWith(filterPrefix) && prefix !== filterPrefix) continue;
    const slug = prefix.replace(/^ENT-MOD-|-$/g, '');
    prefixes.set(prefix, slug);
  }
  return prefixes;
}

function slugLabel(templates, slug) {
  return templates.slug_labels?.[slug] || slug;
}

function taskExists(byId, taskId) {
  return byId.has(taskId);
}

function resolveDepends(prefix, leafSpec, byId) {
  const deps = [];
  for (const suf of leafSpec.depends_suffixes || []) {
    if (leafSpec.depends_suffix_groups?.v1 && suf === 'V1-HIFI') {
      const alts = leafSpec.depends_suffix_groups.v1;
      const found = alts.find((s) => taskExists(byId, `${prefix}${s}`));
      deps.push(`${prefix}${found || suf}`);
      continue;
    }
    deps.push(`${prefix}${suf}`);
  }
  return deps.filter(Boolean);
}

function leafSatisfied(prefix, leafSpec, byId) {
  if (leafSpec.alternates?.length) {
    return leafSpec.alternates.some((s) => taskExists(byId, `${prefix}${s}`));
  }
  if (leafSpec.suffix) {
    if (taskExists(byId, `${prefix}${leafSpec.suffix}`)) return true;
    for (const alt of leafSpec.alternates_exist_ok || []) {
      if (taskExists(byId, `${prefix}${alt}`)) return true;
    }
  }
  return false;
}

export function buildSuggestedYaml(taskId, leafSpec, prefix, slug, templates, byId, epic = 'E-ENT-SCRUM-PDR') {
  const phase = leafSpec.delivery_phase || 'definition';
  const label = slugLabel(templates, slug);
  const title = (leafSpec.title || '').replace('{slug_label}', label);
  const deps = resolveDepends(prefix, leafSpec, byId);
  const repo = leafSpec.repo || leafSpec.repos?.[0] || 'agent-delivery';
  const lines = [
    `  - id: ${taskId}`,
    `    epic: ${epic}`,
    `    delivery_phase: ${phase}`,
    `    title: ${title}`,
    `    agent: ${leafSpec.agent}`,
  ];
  if (leafSpec.repos?.length) {
    lines.push(`    repos: [${leafSpec.repos.join(', ')}]`);
  } else {
    lines.push(`    repo: ${repo}`);
  }
  lines.push(`    depends_on: [${deps.join(', ')}]`);
  lines.push('    status: backlog');
  lines.push('    priority: P0');
  if (leafSpec.cicd) lines.push(`    cicd: ${leafSpec.cicd}`);
  lines.push('    note: "PM 采纳 proposals 后入库；unlock 走 scan → confirm"');
  return lines.join('\n');
}

export function scanDefinitionGaps(prefix, slug, byId, templates) {
  const gaps = [];
  const chain = templates.definition_chain;
  if (!chain?.leaves) return gaps;

  const anchor = chain.anchor_suffix || 'PACK-L01';
  if (!taskExists(byId, `${prefix}${anchor}`)) return gaps;

  for (const leafSpec of chain.leaves) {
    if (leafSpec.suffix === anchor) continue;
    if (leafSpec.required === false) continue;
    if (leafSatisfied(prefix, leafSpec, byId)) continue;

    const primarySuffix = leafSpec.suffix || leafSpec.alternates?.[0];
    const taskId = `${prefix}${primarySuffix}`;
    const alts = leafSpec.alternates || [leafSpec.suffix];
    gaps.push({
      kind: 'missing_definition_leaf',
      suggested_task_id: taskId,
      module_prefix: prefix,
      module_slug: slug,
      delivery_phase: 'definition',
      reason: `定义轨缺 leaf：已有 ${prefix}${anchor}，缺 ${(alts || [primarySuffix]).join(' | ')}`,
      depends_on: resolveDepends(prefix, leafSpec, byId),
      agent: leafSpec.agent,
      trigger: 'definition_chain_gap',
      suggested_yaml: buildSuggestedYaml(taskId, leafSpec, prefix, slug, templates, byId),
    });
  }
  return gaps;
}

export function countImplementationTasksForModule(byId, slug) {
  let count = 0;
  for (const task of byId.values()) {
    if (task.delivery_phase !== 'implementation') continue;
    if (
      task.id.includes(`ENT-MOD-${slug}-`) ||
      task.id.includes(`ENT-JAVA-${slug}-`) ||
      task.id.includes(`ENT-${slug}-`)
    ) {
      count++;
    }
  }
  return count;
}

export function scanImplementationGaps(prefix, slug, byId, templates) {
  const gaps = [];
  const impl = templates.implementation_recommended;
  if (!impl) return gaps;

  const dgSuffix = impl.dg_suffix || 'DG-G3';
  const dgId = `${prefix}${dgSuffix}`;
  const dgTask = byId.get(dgId);
  if (!dgTask) return gaps;

  const implCount = countImplementationTasksForModule(byId, slug);
  const minTasks = impl.min_impl_tasks_after_dg_done ?? 1;

  if (isDoneStatus(dgTask.status) && implCount < minTasks) {
    for (const leaf of impl.suggested_leaves || []) {
      if (leaf.optional) continue;
      const tid = `${prefix}${leaf.suffix}`;
      if (taskExists(byId, tid)) continue;
      const leafSpec = {
        ...leaf,
        delivery_phase: 'implementation',
        depends_suffixes: [dgSuffix],
      };
      gaps.push({
        kind: 'missing_implementation_leaf',
        suggested_task_id: tid,
        module_prefix: prefix,
        module_slug: slug,
        delivery_phase: 'implementation',
        reason: `${dgId} 已 done，模块 ${slug} 缺 implementation leaf ${tid}`,
        depends_on: [dgId],
        agent: leaf.agent,
        trigger: 'impl_gate3_gap',
        suggested_yaml: buildSuggestedYaml(tid, leafSpec, prefix, slug, templates, byId),
      });
    }
  } else {
    for (const leaf of impl.suggested_leaves || []) {
      const tid = `${prefix}${leaf.suffix}`;
      if (taskExists(byId, tid)) continue;
      if (leaf.optional) continue;
      const leafSpec = {
        ...leaf,
        delivery_phase: 'implementation',
        depends_suffixes: [dgSuffix],
      };
      gaps.push({
        kind: 'missing_implementation_leaf',
        suggested_task_id: tid,
        module_prefix: prefix,
        module_slug: slug,
        delivery_phase: 'implementation',
        reason: `实现轨推荐 leaf 缺失：${tid}（${dgId} 已登记）`,
        depends_on: [dgId],
        agent: leaf.agent,
        trigger: 'implementation_template_gap',
        optional: true,
        suggested_yaml: buildSuggestedYaml(tid, leafSpec, prefix, slug, templates, byId),
      });
    }
  }
  return gaps;
}

export function scanBrokenDependencies(byId) {
  const gaps = [];
  for (const task of byId.values()) {
    for (const dep of task.depends_on || []) {
      if (!dep || /^待/.test(dep)) continue;
      if (!byId.has(dep)) {
        gaps.push({
          kind: 'broken_dependency',
          suggested_task_id: task.id,
          module_prefix: task.id.match(/^(ENT-MOD-[A-Z]+-)/)?.[1] || '',
          module_slug: task.id.match(/^ENT-MOD-([A-Z]+)-/)?.[1] || '',
          delivery_phase: task.delivery_phase || '',
          reason: `${task.id} 依赖不存在的 ${dep}`,
          depends_on: [dep],
          trigger: 'broken_dep',
          missing_dependency: dep,
          suggested_yaml: '',
        });
      }
    }
  }
  return gaps;
}

export function scanUnlockTargetGaps(byId, confirmTriggers) {
  const gaps = [];
  for (const trigger of confirmTriggers || []) {
    for (const task of byId.values()) {
      if (!isDoneStatus(task.status)) continue;
      if (!trigger.taskDoneSuffix || !task.id.endsWith(trigger.taskDoneSuffix)) continue;
      const prefix = task.id.slice(0, -trigger.taskDoneSuffix.length);
      for (const suf of trigger.unlockSuffixes || []) {
        const tid = `${prefix}${suf}`;
        if (byId.has(tid)) continue;
        gaps.push({
          kind: 'unlock_target_missing',
          suggested_task_id: tid,
          module_prefix: prefix,
          module_slug: prefix.replace(/^ENT-MOD-|-$/g, ''),
          delivery_phase: trigger.deliveryPhase || 'definition',
          reason: `${task.id} 已 done；规则 ${trigger.id} 期望存在 ${tid}`,
          depends_on: [task.id],
          trigger: trigger.id,
          suggested_yaml: '',
        });
      }
    }
  }
  return gaps;
}

export function scanRegistryGaps(opts = {}) {
  const {
    modulePrefix = '',
    phase = 'all',
    includeBrokenDeps = true,
    includeUnlockTargets = true,
    confirmTriggers = [],
    templates = null,
  } = opts;

  const tpl = templates || loadGapTemplates();
  const { byId } = loadAllTasks();
  const prefixes = discoverModulePrefixes(byId, modulePrefix);
  const all = [];

  if (includeBrokenDeps) all.push(...scanBrokenDependencies(byId));
  if (includeUnlockTargets) all.push(...scanUnlockTargetGaps(byId, confirmTriggers));

  for (const [prefix, slug] of prefixes) {
    if (phase === 'all' || phase === 'definition') {
      all.push(...scanDefinitionGaps(prefix, slug, byId, tpl));
    }
    if (phase === 'all' || phase === 'implementation') {
      all.push(...scanImplementationGaps(prefix, slug, byId, tpl));
    }
  }

  const seen = new Set();
  let result = all.filter((g) => {
    const key = `${g.kind}:${g.suggested_task_id}:${g.reason}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  if (modulePrefix) {
    const norm = modulePrefix.endsWith('-') ? modulePrefix : `${modulePrefix}-`;
    result = result.filter(
      (g) =>
        (g.module_prefix && g.module_prefix.startsWith(norm)) ||
        g.suggested_task_id.startsWith(norm),
    );
  }

  const byTask = new Map();
  for (const g of result) {
    const prev = byTask.get(g.suggested_task_id);
    if (!prev || (!prev.suggested_yaml && g.suggested_yaml)) {
      byTask.set(g.suggested_task_id, g);
    }
  }
  return [...byTask.values()];
}

function proposalEntry(gap) {
  const stamp = Date.now().toString(36);
  return {
    id: `gap-${gap.suggested_task_id}-${stamp}`.slice(0, 80),
    status: 'proposed',
    kind: gap.kind,
    suggested_task_id: gap.suggested_task_id,
    module_prefix: gap.module_prefix || '',
    module_slug: gap.module_slug || '',
    delivery_phase: gap.delivery_phase || '',
    reason: gap.reason,
    depends_on: gap.depends_on || [],
    agent: gap.agent || '',
    trigger: gap.trigger || '',
    suggested_yaml: gap.suggested_yaml || '',
    created_at: new Date().toISOString(),
  };
}

export function appendGapProposals(gaps, opts = {}) {
  const doc = loadGapProposals();
  const existing = new Set(
    (doc.proposals || []).filter((p) => p.status === 'proposed').map((p) => p.suggested_task_id),
  );
  const added = [];
  for (const gap of gaps) {
    if (existing.has(gap.suggested_task_id)) continue;
    const entry = proposalEntry(gap);
    doc.proposals.push(entry);
    existing.add(gap.suggested_task_id);
    added.push(entry);
  }
  if (added.length && !opts.dryRun) {
    saveGapProposals(doc);
  }
  return { added, total: doc.proposals.length };
}
