#!/usr/bin/env node
/**
 * 把 T0X 已赋正式 M_* 回写到 A2 pages 里仍为 metric_id: null 的 items/demands。
 * 不改 差集判定。缺口说明含「不消费 {该ID}」的 demand 不写。
 * 不编造 05 seq。幂等。
 *
 * 用法（仓根）：
 *   node scripts/apply-t0x-a2-metric-ids.mjs --dry-run
 *   node scripts/apply-t0x-a2-metric-ids.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { loadA2SrsRecords } from './lib/a2-gap-items.mjs';
import { ORCH_ROOT } from './lib/metric-registry-lib.mjs';

const PLAN = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'metrics',
  'request',
  '_work',
  'ALGO-LIB-T0X-REGISTER-L01-plan.json',
);
const DRY = process.argv.includes('--dry-run');

function isOfficialId(id) {
  return typeof id === 'string' && /^M_[A-Z0-9_]+$/.test(id.trim());
}

function loadT0xByRowId() {
  const plan = JSON.parse(fs.readFileSync(PLAN, 'utf8'));
  const byRow = new Map();
  for (const row of [...(plan.fl_rows || []), ...(plan.c_rows || [])]) {
    if (!row?.row_id || !isOfficialId(row.metric_id)) continue;
    if (!byRow.has(row.row_id)) byRow.set(String(row.row_id), String(row.metric_id).trim());
  }
  return byRow;
}

function forbidsId(gapNote, metricId) {
  const t = String(gapNote || '');
  if (!t.includes('不消费')) return false;
  if (t.includes(metricId)) return true;
  const prefix = metricId.replace(/_[A-Z0-9]+$/, '');
  if (prefix.startsWith('M_ENT') && /不消费\s*M_ENT/.test(t)) return true;
  return false;
}

function sliceBlock(raw, marker) {
  const start = raw.indexOf(marker);
  if (start < 0) return null;
  const after = start + marker.length;
  const rest = raw.slice(after);
  const m = rest.match(/\n  - (?:row_id|demand_id):|\n(?=\S)/);
  const end = m ? after + m.index : raw.length;
  return { start, end, text: raw.slice(start, end) };
}

function patchSlice(text, metricId) {
  if (!/\n    metric_id: null\b/.test(text)) return { text, changed: false };
  return { text: text.replace(/\n    metric_id: null\b/, `\n    metric_id: ${metricId}`), changed: true };
}

function apply() {
  const byRow = loadT0xByRowId();
  const { pages, items, demands } = loadA2SrsRecords(ORCH_ROOT);
  const pageMeta = new Map(pages.map((p) => [p.pageId, p]));
  const stats = { itemWrite: 0, demandWrite: 0, skipHasId: 0, skipForbid: 0, skipMissing: 0, files: 0 };
  const originals = new Map();
  const fileEdits = new Map();

  function queue(pageId, marker, metricId, kind) {
    const meta = pageMeta.get(pageId);
    if (!meta) {
      stats.skipMissing++;
      return;
    }
    const full = path.join(
      ORCH_ROOT,
      'agent-delivery',
      'metrics',
      'request',
      meta.folder,
      'pages',
      meta.file,
    );
    if (!fileEdits.has(full)) {
      const raw0 = fs.readFileSync(full, 'utf8');
      originals.set(full, raw0);
      fileEdits.set(full, raw0);
    }
    let raw = fileEdits.get(full);
    const block = sliceBlock(raw, marker);
    if (!block) {
      stats.skipMissing++;
      return;
    }
    const next = patchSlice(block.text, metricId);
    if (!next.changed) {
      stats.skipHasId++;
      return;
    }
    fileEdits.set(full, raw.slice(0, block.start) + next.text + raw.slice(block.end));
    if (kind === 'item') stats.itemWrite++;
    else stats.demandWrite++;
  }

  for (const it of items) {
    const id = byRow.get(it.rowId);
    if (!id) continue;
    if (isOfficialId(it.metricId)) {
      stats.skipHasId++;
      continue;
    }
    if (forbidsId(it.gapNote, id)) {
      stats.skipForbid++;
      continue;
    }
    queue(it.pageId, `  - row_id: ${it.rowId}`, id, 'item');
  }

  const itemNameToId = new Map();
  for (const it of items) {
    const id = byRow.get(it.rowId) || (isOfficialId(it.metricId) ? it.metricId : '');
    if (!id || !it.main) continue;
    itemNameToId.set(`${it.pageId}|${it.main}`, id);
  }

  for (const d of demands) {
    const id = itemNameToId.get(`${d.pageId}|${d.main}`);
    if (!id) continue;
    if (isOfficialId(d.metricId)) {
      stats.skipHasId++;
      continue;
    }
    if (forbidsId(d.gapNote, id)) {
      stats.skipForbid++;
      continue;
    }
    queue(d.pageId, `  - demand_id: ${d.demandId}`, id, 'demand');
  }

  let files = 0;
  for (const [full, raw] of fileEdits) {
    if (raw === originals.get(full)) continue;
    files++;
    if (!DRY) fs.writeFileSync(full, raw, 'utf8');
  }
  stats.files = files;

  console.log(
    JSON.stringify(
      {
        ok: true,
        dry_run: DRY,
        t0x_rows: byRow.size,
        ...stats,
      },
      null,
      2,
    ),
  );
}

apply();
