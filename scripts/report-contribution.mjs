#!/usr/bin/env node
/**
 * Aggregate contribution points by person (claimed_by / supervised_by).
 *
 *   node scripts/report-contribution.mjs                  # current sprint, done
 *   node scripts/report-contribution.mjs --all-done       # all done tasks
 *   node scripts/report-contribution.mjs --sprint 2026-W28
 *   node scripts/report-contribution.mjs --include-open   # include non-done
 *   node scripts/report-contribution.mjs --person 高颖 --include-open --detail
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(__dirname, '..');
const REGISTRY = path.join(ORCH, 'agent-delivery', 'task-registry.yaml');
const SCRUM = path.join(ORCH, 'agent-delivery', 'scrum-sprint.yaml');

const args = process.argv.slice(2);
const allDone = args.includes('--all-done');
const includeOpen = args.includes('--include-open');
const detail = args.includes('--detail');
let sprint = '';
let person = '';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--sprint') sprint = args[++i] || '';
  if (args[i] === '--person') person = args[++i] || '';
}

function currentSprint() {
  if (!fs.existsSync(SCRUM)) return '';
  const m = fs
    .readFileSync(SCRUM, 'utf8')
    .match(/^\s*current_sprint:\s*"?([^"\r\n]+)"?/m);
  return m ? m[1].trim() : '';
}

function parseTasks(text) {
  const lines = text.split(/\r?\n/);
  const tasks = [];
  let inTasks = false;
  let cur = null;
  const flush = () => {
    if (cur) tasks.push(cur);
    cur = null;
  };
  for (const line of lines) {
    if (/^tasks:\s*$/.test(line)) {
      inTasks = true;
      continue;
    }
    if (!inTasks) continue;
    const idM = line.match(/^\s+- id:\s*(.+)\s*$/);
    if (idM) {
      flush();
      cur = {
        id: idM[1].trim().replace(/^["']|["']$/g, ''),
        status: '',
        sprint_id: '',
        claimed_by: '',
        supervised_by: '',
        effort_points: 0,
        difficulty: '',
        title: '',
      };
      continue;
    }
    if (!cur) continue;
    const kv = line.match(/^\s+(\w+):\s*(.+?)\s*$/);
    if (!kv) continue;
    const k = kv[1];
    const v = kv[2].replace(/^["']|["']$/g, '').replace(/\s+#.*$/, '').trim();
    if (k === 'status') cur.status = v;
    else if (k === 'sprint_id') cur.sprint_id = v;
    else if (k === 'claimed_by') cur.claimed_by = v;
    else if (k === 'supervised_by') cur.supervised_by = v;
    else if (k === 'difficulty') cur.difficulty = v;
    else if (k === 'title') cur.title = v;
    else if (k === 'effort_points') {
      const n = Number(v.replace(/_/g, ''));
      cur.effort_points = Number.isFinite(n) ? n : 0;
    }
  }
  flush();
  return tasks;
}

const sid = sprint || (allDone ? '' : currentSprint());
const tasks = parseTasks(fs.readFileSync(REGISTRY, 'utf8')).filter((t) => {
  if (sid && t.sprint_id !== sid) return false;
  if (!includeOpen && t.status !== 'done') return false;
  return true;
});

const byPerson = new Map();
const uncredited = [];
const personTasks = [];

function creditWho(t) {
  const raw = t.claimed_by || t.supervised_by || '';
  return raw.replace(/^human:/, '').replace(/^agent:/, '');
}

for (const t of tasks) {
  const who = creditWho(t);
  if (!who) {
    uncredited.push(t);
    continue;
  }
  if (person && !who.includes(person)) continue;
  personTasks.push({ ...t, who });
  if (!byPerson.has(who)) {
    byPerson.set(who, {
      name: who,
      points: 0,
      tasks: 0,
      byDiff: { S: 0, M: 0, L: 0, XL: 0 },
      ids: [],
    });
  }
  const row = byPerson.get(who);
  row.points += t.effort_points || 0;
  row.tasks += 1;
  if (t.difficulty && row.byDiff[t.difficulty] != null) {
    row.byDiff[t.difficulty] += 1;
  }
  row.ids.push(`${t.id}(${t.effort_points || 0}${t.difficulty || ''})`);
}

const rows = [...byPerson.values()].sort((a, b) => b.points - a.points);
const scope = sid
  ? `sprint=${sid}`
  : allDone
    ? 'all-done'
    : includeOpen
      ? 'all'
      : 'done';
const statusScope = includeOpen ? 'all-status' : 'done-only';
const personScope = person ? `, person=${person}` : '';

console.log(`# Contribution report (${scope}, ${statusScope}${personScope})`);
console.log(`tasks=${person ? personTasks.length : tasks.length} people=${rows.length}`);
console.log('');
console.log('| Rank | Person | Points | Tasks | S | M | L | XL |');
console.log('|-----:|--------|-------:|------:|--:|--:|--:|---:|');
rows.forEach((r, i) => {
  console.log(
    `| ${i + 1} | ${r.name} | ${r.points} | ${r.tasks} | ${r.byDiff.S} | ${r.byDiff.M} | ${r.byDiff.L} | ${r.byDiff.XL} |`,
  );
});

if (detail && personTasks.length) {
  console.log('');
  console.log('| Task ID | Status | Sprint | Points | Diff | Credit | Title |');
  console.log('|---------|--------|--------|-------:|------|--------|-------|');
  for (const t of personTasks.sort((a, b) => (b.effort_points || 0) - (a.effort_points || 0))) {
    const title = (t.title || '').replace(/\|/g, '/').slice(0, 48);
    console.log(
      `| ${t.id} | ${t.status} | ${t.sprint_id || '-'} | ${t.effort_points || 0} | ${t.difficulty || '-'} | ${t.who} | ${title} |`,
    );
  }
}

if (!person && uncredited.length) {
  console.log('');
  console.log(
    `Uncredited (no claimed_by): ${uncredited.length} — e.g. ${uncredited
      .slice(0, 5)
      .map((t) => t.id)
      .join(', ')}`,
  );
}
