#!/usr/bin/env node
/**
 * Convoy / touched_files helpers — same-repo parallel conflict detection.
 * No external deps (no minimatch). Glob overlap is prefix/segment heuristic.
 *
 * Policy:
 *  - Explicit task.convoy == same group + serial → conflict when peer is active
 *  - Same repo + overlapping touched_files → conflict (auto Convoy)
 *  - Same repo + both missing touched_files → soft warn (cannot prove safe)
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadAllTasks, getListField, getScalar, findTaskBlocks } from './task-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const DISPATCH_QUEUE_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'dispatch-queue.yaml');

export const ACTIVE_STATUSES = new Set(['claimed', 'in_progress', 'review']);

/** 编排文档仓：同仓缺 touched_files 不发 soft_warn（非代码冲突面） */
export const SOFT_WARN_SKIP_REPOS = new Set(['agent-delivery']);

/** Static prefix before first glob metachar (* ? [) */
export function staticPrefix(glob) {
  const g = String(glob || '').replace(/\\/g, '/').replace(/^\.\//, '');
  const m = g.match(/^([^[*?]*)/);
  let p = (m ? m[1] : g).replace(/\/+$/, '');
  // drop trailing incomplete segment after last /
  if (p.includes('/') && !g.slice(p.length).startsWith('/')) {
    // e.g. src/views/top* → prefix src/views
    const i = p.lastIndexOf('/');
    if (i >= 0) p = p.slice(0, i);
  }
  return p;
}

/** Two globs likely touch the same tree */
export function globsOverlap(a, b) {
  if (!a || !b) return false;
  const A = String(a).replace(/\\/g, '/');
  const B = String(b).replace(/\\/g, '/');
  if (A === B) return true;
  const pa = staticPrefix(A);
  const pb = staticPrefix(B);
  if (!pa || !pb) {
    // one is fully wildcard — treat as whole-repo risk only if other also empty/full
    return !pa && !pb;
  }
  if (pa === pb) return true;
  if (pa.startsWith(pb + '/') || pb.startsWith(pa + '/')) return true;
  // shared first two path segments e.g. src/views/...
  const sa = pa.split('/').filter(Boolean);
  const sb = pb.split('/').filter(Boolean);
  if (sa.length >= 2 && sb.length >= 2 && sa[0] === sb[0] && sa[1] === sb[1]) {
    return true;
  }
  return false;
}

export function listsOverlap(listA = [], listB = []) {
  for (const a of listA) {
    for (const b of listB) {
      if (globsOverlap(a, b)) return { a, b };
    }
  }
  return null;
}

export function loadConvoyGroups(filePath = DISPATCH_QUEUE_PATH) {
  if (!fs.existsSync(filePath)) return {};
  const raw = fs.readFileSync(filePath, 'utf8');
  const groups = {};
  // crude parse of convoy_groups: NAME: ... repo: ... serial: ... tasks: [...]
  const section = raw.match(/convoy_groups:\s*\r?\n([\s\S]*?)(?:\nqueue:|\n# coordinator|\ntrigger_policy:|$)/);
  if (!section) return groups;
  const body = section[1];
  const blocks = body.split(/\n  ([A-Z0-9][A-Z0-9_-]*):\s*\r?\n/).slice(1);
  for (let i = 0; i < blocks.length; i += 2) {
    const name = blocks[i];
    const chunk = blocks[i + 1] || '';
    const repo = chunk.match(/^\s+repo:\s*(\S+)/m)?.[1]?.trim();
    const serial = /serial:\s*true/.test(chunk);
    const tasksInline = chunk.match(/^\s+tasks:\s*\[([^\]]*)\]/m)?.[1] || '';
    const tasks = tasksInline
      .split(/,\s*/)
      .map((s) => s.trim())
      .filter(Boolean);
    groups[name] = { id: name, repo, serial, tasks };
  }
  return groups;
}

/** Enrich parseTaskBlock fields not yet on default snapshot */
export function loadTasksWithTouchedFiles() {
  const { lines, byId } = loadAllTasks();
  const blocks = findTaskBlocks(lines);
  for (const { start, end } of blocks) {
    const block = lines.slice(start, end);
    const id =
      getScalar(block, 'id') ||
      (block[0].match(/id:\s*(.+)/) || [])[1]?.trim().replace(/^["']|["']$/g, '');
    if (!id || !byId.has(id)) continue;
    const t = byId.get(id);
    t.touched_files = getListField(block, 'touched_files');
    t.convoy = getScalar(block, 'convoy');
    t.repo = getScalar(block, 'repo');
    t.worktree_branch = getScalar(block, 'worktree_branch');
  }
  return { lines, byId, convoyGroups: loadConvoyGroups() };
}

/**
 * Detect conflicts among active tasks (+ optional candidate task).
 * @returns {{ conflicts: Array, soft_warns: Array }}
 */
export function detectConflicts(byId, convoyGroups, { candidate = null, activeStatuses = ACTIVE_STATUSES } = {}) {
  const active = [...byId.values()].filter((t) => activeStatuses.has(t.status));
  if (candidate) {
    // treat candidate as would-be active
    active.push({ ...candidate, status: candidate.status || 'claimed', _candidate: true });
  }

  const conflicts = [];
  const soft_warns = [];

  for (let i = 0; i < active.length; i++) {
    for (let j = i + 1; j < active.length; j++) {
      const a = active[i];
      const b = active[j];

      // explicit convoy group
      if (a.convoy && b.convoy && a.convoy === b.convoy) {
        const g = convoyGroups[a.convoy];
        if (!g || g.serial !== false) {
          conflicts.push({
            type: 'convoy_serial',
            convoy: a.convoy,
            repo: g?.repo || a.repo || b.repo,
            a: a.id,
            b: b.id,
            reason: `同 Convoy 组 ${a.convoy} 要求串行`,
          });
          continue;
        }
      }

      const repoA = a.repo || '';
      const repoB = b.repo || '';
      if (!repoA || !repoB || repoA !== repoB) continue;

      const filesA = a.touched_files || [];
      const filesB = b.touched_files || [];

      if (!filesA.length || !filesB.length) {
        if (!SOFT_WARN_SKIP_REPOS.has(repoA)) {
          soft_warns.push({
            type: 'missing_touched_files',
            repo: repoA,
            a: a.id,
            b: b.id,
            missing: [
              !filesA.length ? a.id : null,
              !filesB.length ? b.id : null,
            ].filter(Boolean),
            reason: '同仓并行但缺少 touched_files，无法证明无冲突',
          });
        }
        continue;
      }

      const hit = listsOverlap(filesA, filesB);
      if (hit) {
        conflicts.push({
          type: 'touched_files_overlap',
          repo: repoA,
          a: a.id,
          b: b.id,
          pattern_a: hit.a,
          pattern_b: hit.b,
          reason: `touched_files 重叠: ${hit.a} ↔ ${hit.b}`,
          suggested_convoy: `AUTO-${repoA.replace(/[^a-zA-Z0-9]+/g, '-').toUpperCase()}`,
        });
      }
    }
  }

  return { conflicts, soft_warns, active_count: active.length };
}

/** Can candidate be claimed without hard convoy conflict? */
export function canClaim(taskId, byId, convoyGroups) {
  const task = byId.get(taskId);
  if (!task) return { ok: false, reason: `task not found: ${taskId}` };
  const { conflicts, soft_warns } = detectConflicts(byId, convoyGroups, {
    candidate: { ...task, status: 'claimed' },
  });
  const hard = conflicts.filter((c) => c.a === taskId || c.b === taskId);
  return {
    ok: hard.length === 0,
    conflicts: hard,
    soft_warns: soft_warns.filter((w) => w.a === taskId || w.b === taskId),
  };
}
