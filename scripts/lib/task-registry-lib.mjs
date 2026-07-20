#!/usr/bin/env node
/**
 * task-registry.yaml parse / mutate helpers (coordinator dispatch + ready engine).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const REGISTRY_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'task-registry.yaml');

export function readRegistryText() {
  return fs.readFileSync(REGISTRY_PATH, 'utf8');
}

export function writeRegistryText(text) {
  const out = text.endsWith('\n') ? text : `${text}\n`;
  fs.writeFileSync(REGISTRY_PATH, out, 'utf8');
}

export function findTaskBlocks(lines) {
  const blocks = [];
  let inTasks = false;
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (/^tasks:\s*$/.test(lines[i])) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    if (/^\s+- id:\s*/.test(lines[i])) {
      if (start >= 0) blocks.push({ start, end: i });
      start = i;
    }
  }
  if (start >= 0) blocks.push({ start, end: lines.length });
  return blocks;
}

export function findTaskBlock(lines, taskId) {
  const esc = taskId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  for (let i = 0; i < lines.length; i++) {
    if (new RegExp(`^\\s+- id:\\s*${esc}\\s*$`).test(lines[i])) {
      let end = lines.length;
      for (let j = i + 1; j < lines.length; j++) {
        if (/^\s+- id:\s*/.test(lines[j])) {
          end = j;
          break;
        }
      }
      return { start: i, end };
    }
  }
  return null;
}

export function parseInlineList(value) {
  const v = (value || '').trim();
  const m = v.match(/^\[(.*)\]$/);
  if (!m) return v ? [v] : [];
  const inner = m[1].trim();
  if (!inner) return [];
  return inner.split(/,\s*/).map((s) => s.trim().replace(/^["']|["']$/g, ''));
}

export function getScalar(blockLines, key) {
  const re = new RegExp(`^\\s+${key}:\\s*(.+?)\\s*$`);
  for (const line of blockLines) {
    const m = line.match(re);
    if (m) {
      return m[1].replace(/^["']|["']$/g, '').replace(/\s+#.*$/, '').trim();
    }
  }
  return '';
}

export function getListField(blockLines, key) {
  for (let i = 0; i < blockLines.length; i++) {
    const m = blockLines[i].match(new RegExp(`^\\s+${key}:\\s*(.+)$`));
    if (!m) continue;
    const rest = m[1].trim();
    if (rest.startsWith('[')) return parseInlineList(rest);
    const items = [];
    if (rest && rest !== '[]') items.push(rest.replace(/^["']|["']$/g, ''));
    for (let j = i + 1; j < blockLines.length; j++) {
      const li = blockLines[j].match(/^\s+-\s+(.+)$/);
      if (!li) break;
      items.push(li[1].trim().replace(/^["']|["']$/g, ''));
    }
    return items;
  }
  return [];
}

export function parseTaskBlock(blockLines) {
  const id =
    getScalar(blockLines, 'id') ||
    (blockLines[0].match(/id:\s*(.+)/) || [])[1]?.trim().replace(/^["']|["']$/g, '');
  return {
    id,
    title: getScalar(blockLines, 'title'),
    status: getScalar(blockLines, 'status'),
    agent: getScalar(blockLines, 'agent'),
    epic: getScalar(blockLines, 'epic'),
    sprint_id: getScalar(blockLines, 'sprint_id'),
    supervised_by: getScalar(blockLines, 'supervised_by'),
    claimed_by: getScalar(blockLines, 'claimed_by'),
    priority: getScalar(blockLines, 'priority'),
    blocked_by: getScalar(blockLines, 'blocked_by'),
    delivery_phase: getScalar(blockLines, 'delivery_phase'),
    effort_points: getScalar(blockLines, 'effort_points'),
    difficulty: getScalar(blockLines, 'difficulty'),
    estimated_tokens: getScalar(blockLines, 'estimated_tokens'),
    record_id: getScalar(blockLines, 'feishu_bitable_record_id'),
    depends_on: getListField(blockLines, 'depends_on'),
    collaborators: getListField(blockLines, 'collaborators'),
    definition_of_done: getListField(blockLines, 'definition_of_done'),
    design_refs: getListField(blockLines, 'design_refs'),
    note: getScalar(blockLines, 'note'),
  };
}

export function loadAllTasks() {
  const lines = readRegistryText().split(/\r?\n/);
  const blocks = findTaskBlocks(lines);
  const byId = new Map();
  for (const { start, end } of blocks) {
    const blockLines = lines.slice(start, end);
    const task = parseTaskBlock(blockLines);
    if (task.id) {
      task._loc = { start, end };
      byId.set(task.id, task);
    }
  }
  return { lines, byId };
}

export function upsertField(blockLines, key, value) {
  const re = new RegExp(`^(\\s+)${key}:\\s*`);
  const scalar =
    typeof value === 'number' ? String(value) : `"${String(value).replace(/"/g, '\\"')}"`;
  for (let i = 0; i < blockLines.length; i++) {
    if (re.test(blockLines[i])) {
      blockLines[i] = `${blockLines[i].match(/^(\s+)/)[1]}${key}: ${scalar}`;
      return;
    }
  }
  const indent = blockLines[0]?.match(/^(\s+)/)?.[1] || '    ';
  blockLines.splice(1, 0, `${indent}${key}: ${scalar}`);
}

export function upsertListItem(blockLines, key, item) {
  const items = getListField(blockLines, key);
  if (items.includes(item)) return;
  items.push(item);
  const re = new RegExp(`^\\s+${key}:\\s*`);
  let idx = -1;
  for (let i = 0; i < blockLines.length; i++) {
    if (re.test(blockLines[i])) {
      idx = i;
      break;
    }
  }
  const indent = blockLines[0]?.match(/^(\s+)/)?.[1] || '    ';
  const listIndent = `${indent}  `;
  if (idx < 0) {
    blockLines.splice(1, 0, `${indent}${key}:`, `${listIndent}- ${item}`);
    return;
  }
  let end = idx + 1;
  while (end < blockLines.length && /^\s+-\s+/.test(blockLines[end])) end++;
  blockLines.splice(end, 0, `${listIndent}- ${item}`);
}

export function applyBlockUpdate(lines, loc, blockLines) {
  return [...lines.slice(0, loc.start), ...blockLines, ...lines.slice(loc.end)];
}

export function updateTaskFields(taskId, patch, dryRun = false) {
  const text = readRegistryText();
  const lines = text.split(/\r?\n/);
  const loc = findTaskBlock(lines, taskId);
  if (!loc) throw new Error(`Task not found: ${taskId}`);
  const block = lines.slice(loc.start, loc.end);
  const before = parseTaskBlock(block);
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined || v === null) continue;
    upsertField(block, k, v);
  }
  const after = parseTaskBlock(block);
  if (dryRun) return { before, after, changed: false };
  const newLines = applyBlockUpdate(lines, loc, block);
  writeRegistryText(newLines.join('\n'));
  return { before, after, changed: true };
}

export function isDoneStatus(status) {
  return status === 'done' || status === 'completed';
}

export function depsSatisfied(task, doneIds) {
  const deps = (task.depends_on || []).filter(Boolean);
  if (deps.length === 0) return true;
  return deps.every((d) => doneIds.has(d));
}

export function buildDoneIdSet(byId) {
  const done = new Set();
  for (const t of byId.values()) {
    if (isDoneStatus(t.status)) done.add(t.id);
  }
  return done;
}

export function modulePrefixFromTaskId(taskId, suffix) {
  if (!taskId.endsWith(suffix)) return null;
  return taskId.slice(0, -suffix.length);
}
