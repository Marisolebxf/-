#!/usr/bin/env node
/**
 * team-roster.yaml parse helpers (supervisor capacity + find-supervisor-slot).
 * Line-based parse — no yaml dependency (aligned with coordinator-dispatch.mjs).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const ROSTER_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'team-roster.yaml');

/** Default agent → preferred subcoord (Graph Engineering §十六) */
export const AGENT_SUBCOORD_DEFAULT = {
  devops: 'platform-subcoord',
  api: 'platform-subcoord',
  integration: 'platform-subcoord',
  data: 'data-algo-subcoord',
  algorithm: 'data-algo-subcoord',
  ux: 'ui-subcoord',
  ui: 'ui-subcoord',
  frontend: 'ui-subcoord',
  qa: 'assurance-subcoord',
  doc: 'doc-subcoord',
  architect: 'lineage-subcoord', // gate / review; override per task
  coordinator: null,
};

/** Soft preference: team → subcoords they usually supervise */
export const TEAM_SUBCOORD_AFFINITY = {
  leadership: ['platform-subcoord', 'data-algo-subcoord', 'lineage-subcoord', 'metric-subcoord', 'ui-subcoord', 'assurance-subcoord', 'doc-subcoord'],
  pm: ['platform-subcoord', 'doc-subcoord', 'assurance-subcoord', 'metric-subcoord'],
  ux: ['ui-subcoord'],
  frontend: ['ui-subcoord'],
  backend: ['platform-subcoord'],
  architect: ['lineage-subcoord', 'data-algo-subcoord', 'metric-subcoord', 'platform-subcoord'],
  algorithm: ['data-algo-subcoord', 'metric-subcoord', 'lineage-subcoord'],
  metrics: ['metric-subcoord', 'lineage-subcoord'],
  gdf: ['lineage-subcoord', 'data-algo-subcoord'],
  display_large: ['ui-subcoord'],
};

export function loadRosterMembers(rosterPath = ROSTER_PATH) {
  if (!fs.existsSync(rosterPath)) {
    throw new Error(`team-roster not found: ${rosterPath}`);
  }
  const raw = fs.readFileSync(rosterPath, 'utf8');
  const members = [];
  const memberBlocks = raw.split(/\n\s+- registry_name:/).slice(1);
  for (const block of memberBlocks) {
    const body = `registry_name:${block}`;
    const registry_name = body.match(/^registry_name:\s*(.+)$/m)?.[1]?.trim();
    if (!registry_name) continue;
    const name = body.match(/^\s+name:\s*(.+)$/m)?.[1]?.trim() || registry_name.replace(/^human:/, '');
    const team = body.match(/^\s+team:\s*(\S+)/m)?.[1]?.trim() || '';
    const role = body.match(/^\s+role:\s*(\S+)/m)?.[1]?.trim() || '';
    const title = body.match(/^\s+title:\s*(.+)$/m)?.[1]?.trim() || '';
    const can_supervise_agent = /can_supervise_agent:\s*true/.test(body);
    const maxRaw = body.match(/^\s+max_agent_concurrency:\s*(\d+)/m)?.[1];
    const max_agent_concurrency = maxRaw ? Number(maxRaw) : can_supervise_agent ? 4 : 0;
    const preferred = [];
    const prefBlock = body.match(/preferred_subcoords:\s*\r?\n((?:\s+-\s+\S+\r?\n?)+)/);
    if (prefBlock) {
      for (const m of prefBlock[1].matchAll(/-\s+(\S+)/g)) preferred.push(m[1]);
    }
    members.push({
      registry_name,
      name,
      team,
      role,
      title,
      can_supervise_agent,
      max_agent_concurrency,
      preferred_subcoords: preferred,
    });
  }
  return members;
}

/**
 * Count registry active supervised mount (claimed|in_progress|review).
 * Advisory only — NOT local Cursor session count, NOT a dispatch hard gate.
 * max_agent_concurrency = local Cursor agent sessions per person.
 */
export function countActiveLoad(tasks, supervisedBy) {
  const active = new Set(['claimed', 'in_progress', 'review']);
  let n = 0;
  const list = tasks instanceof Map ? [...tasks.values()] : tasks;
  for (const t of list) {
    if (!active.has(t.status)) continue;
    if ((t.supervised_by || '').trim() === supervisedBy) n += 1;
  }
  return n;
}

export function supervisorsWithCapacity(members, tasks, { subcoord = null, agent = null } = {}) {
  const preferredSub =
    subcoord ||
    (agent ? AGENT_SUBCOORD_DEFAULT[agent.replace(/^agent:/, '')] : null) ||
    null;

  const rows = [];
  for (const m of members) {
    if (!m.can_supervise_agent) continue;
    const load = countActiveLoad(tasks, m.registry_name);
    const capacity = m.max_agent_concurrency || 0;
    const free = capacity - load;
    const affinity = m.preferred_subcoords?.length
      ? m.preferred_subcoords
      : TEAM_SUBCOORD_AFFINITY[m.team] || [];
    const affinityHit = preferredSub ? affinity.includes(preferredSub) : true;
    rows.push({
      ...m,
      load,
      capacity,
      free,
      affinity,
      affinityHit,
      preferredSub,
    });
  }

  // Sort: has free slots first, then affinity match, then more free, then name
  rows.sort((a, b) => {
    const aOk = a.free > 0 ? 0 : 1;
    const bOk = b.free > 0 ? 0 : 1;
    if (aOk !== bOk) return aOk - bOk;
    if (preferredSub) {
      const aAff = a.affinityHit ? 0 : 1;
      const bAff = b.affinityHit ? 0 : 1;
      if (aAff !== bAff) return aAff - bAff;
    }
    if (b.free !== a.free) return b.free - a.free;
    return a.name.localeCompare(b.name, 'zh');
  });

  return rows;
}
