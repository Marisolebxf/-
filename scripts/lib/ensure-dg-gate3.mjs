/**
 * On 建单已采纳 (gap / story-impl merge): if depends_on includes *-DG-G3
 * and that leaf is missing from task-registry, auto-create a Gate-3 task
 * for human:淮政玮 to confirm (status=ready, delivery_phase=definition).
 *
 * Does NOT mark DG done. Does NOT auto-ready implementation leaves.
 */
import {
  loadAllTasks,
  findTaskBlock,
  writeRegistryText,
  nowIsoPlus8,
} from './task-registry-lib.mjs';

const DG_SUFFIX_RE = /-DG-G3$/;
const DEFAULT_SUPERVISOR = 'human:淮政玮';
const DEFAULT_AGENT = 'product-agent';
const DEFAULT_EPIC = 'E-ENT-SCRUM-PDR';

/** @returns {string[]} unique *-DG-G3 ids from depends list */
export function extractDgGate3Ids(dependsOn = []) {
  const out = [];
  for (const d of dependsOn || []) {
    const id = String(d || '').trim();
    if (id && DG_SUFFIX_RE.test(id) && !out.includes(id)) out.push(id);
  }
  return out;
}

/** ENT-MOD-SEARCH-DG-G3 → { prefix: ENT-MOD-SEARCH-, slug: SEARCH, labelHint } */
export function parseDgGate3Id(dgId) {
  const m = String(dgId).match(/^(ENT-MOD-([A-Z0-9]+)-)DG-G3$/);
  if (m) {
    return { prefix: m[1], slug: m[2], label: m[2] };
  }
  const m2 = String(dgId).match(/^(.+)-DG-G3$/);
  return {
    prefix: m2 ? `${m2[1]}-` : `${dgId}-`,
    slug: m2 ? m2[1].replace(/^ENT-MOD-/, '') : dgId,
    label: dgId,
  };
}

function buildDgBlock({ dgId, causeTaskId, proposalId, label }) {
  const title = `门3 DG · ${label}拍板`;
  const note =
    `建单已采纳自动创建（缺门3锚点）· cause=${causeTaskId || '-'} · proposal=${proposalId || '-'}；` +
    `待 human:淮政玮 确认/拍板后改 done；见产品定义评审规程 §7；不自动 ready 实现轨`;
  const now = nowIsoPlus8();

  return [
    `  - id: ${dgId}`,
    `    epic: ${DEFAULT_EPIC}`,
    `    delivery_phase: definition`,
    `    task_type: definition`,
    `    title: "${title}"`,
    `    agent: ${DEFAULT_AGENT}`,
    `    repo: agent-delivery`,
    `    depends_on: []`,
    `    status: ready`,
    `    priority: P0`,
    `    cicd: skip_design_only`,
    `    supervised_by: ${DEFAULT_SUPERVISOR}`,
    `    definition_of_done:`,
    `      - DG-{模块}-拍板纪要.md 结论批准或批准附条件`,
    `      - 三类拍板（范围/临时默认/体验偏离）已记录`,
    `    estimated_tokens: 30000`,
    `    effort_points: "1"`,
    `    difficulty: S`,
    `    note: "${note}"`,
    `    update_time: "${now}"`,
  ];
}

/**
 * Ensure each *-DG-G3 in dependsOn exists in registry.
 * @returns {{ ensured: Array<{dgId, action}>, created: string[] }}
 */
export function ensureDgGate3ForDeps(dependsOn = [], opts = {}) {
  const {
    dryRun = false,
    causeTaskId = '',
    proposalId = '',
    labelMap = {},
  } = opts;

  const dgIds = extractDgGate3Ids(dependsOn);
  if (!dgIds.length) {
    return { ensured: [], created: [] };
  }

  let { lines, byId } = loadAllTasks();
  const ensured = [];
  const created = [];

  for (const dgId of dgIds) {
    if (byId.has(dgId)) {
      ensured.push({
        dgId,
        action: 'exists',
        status: byId.get(dgId).status,
      });
      continue;
    }

    const meta = parseDgGate3Id(dgId);
    const label = labelMap[dgId] || labelMap[meta.slug] || meta.label;
    const block = buildDgBlock({
      dgId,
      causeTaskId,
      proposalId,
      label,
    });

    // Insert near related module leaf if any
    let insertAt = lines.length;
    const anchorCandidates = [
      causeTaskId,
      `${meta.prefix}PDR-G1`,
      `${meta.prefix}PACK-L01`,
      `${meta.prefix}V1-FINAL`,
    ].filter(Boolean);
    for (const a of anchorCandidates) {
      const loc = findTaskBlock(lines, a);
      if (loc) {
        insertAt = loc.end;
        break;
      }
    }

    if (dryRun) {
      ensured.push({ dgId, action: 'would_create', insertAt, block });
      created.push(dgId);
      continue;
    }

    lines = [...lines.slice(0, insertAt), ...block, ...lines.slice(insertAt)];
    writeRegistryText(lines.join('\n'));
    // refresh index for next dg in same batch
    ({ lines, byId } = loadAllTasks());
    ensured.push({ dgId, action: 'created', status: 'ready' });
    created.push(dgId);
  }

  return { ensured, created };
}

/**
 * Collect depends_on from proposal object + suggested_yaml.
 */
export function collectProposalDepends(proposal = {}) {
  const fromField = Array.isArray(proposal.depends_on) ? [...proposal.depends_on] : [];
  const yaml = proposal.suggested_yaml || '';
  const m = yaml.match(/depends_on:\s*\[([^\]]*)\]/);
  if (m) {
    const inner = m[1].trim();
    if (inner) {
      for (const part of inner.split(',')) {
        const id = part.trim().replace(/^["']|["']$/g, '');
        if (id && !fromField.includes(id)) fromField.push(id);
      }
    }
  }
  return fromField;
}
