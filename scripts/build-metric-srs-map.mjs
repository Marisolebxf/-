#!/usr/bin/env node
/**
 * Build metrics/registry/metric-srs-map.yaml
 *
 * Demand provenance (not 8-piece kit):
 *   05 ← A1 requirements.yaml invert（含 TEMP_ALGO_* → M_{维}_{层}_{seq}_{n}）
 *   02/04/05 ← A2 items[] / demands[]（正则抽页，不走 parseYaml：A2 会在 page_ruling 后丢段）
 *
 * Does not invent M_*. Skips TEMP_ALGO_* as catalog keys. Re-run after A1/A2 updates.
 */
import fs from 'node:fs';
import path from 'node:path';
import { loadA2SrsRecords } from './lib/a2-gap-items.mjs';
import { ORCH_ROOT, parseYaml } from './lib/metric-registry-lib.mjs';
const A1_REQ = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'metrics',
  'algo-results',
  'ALGO-LIB-METRIC-DEPS-L01-requirements.yaml',
);
const OUT = path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'registry', 'metric-srs-map.yaml');

function isOfficialId(id) {
  return typeof id === 'string' && /^M_[A-Z0-9_]+$/.test(id.trim());
}

function clip(s, n = 80) {
  const t = String(s || '')
    .replace(/\s+/g, ' ')
    .trim();
  if (!t) return '';
  return t.length <= n ? t : `${t.slice(0, n)}…`;
}

function yamlScalar(v) {
  if (v == null || v === '') return 'null';
  if (typeof v === 'number') return String(v);
  const t = String(v);
  if (/[:#{}[\],&*?!|>%@`'"]|^\s|\s$|\n/.test(t) || t !== t.trim()) {
    return JSON.stringify(t);
  }
  return t;
}

function extractExcelRow(text) {
  if (!text) return null;
  const m = String(text).match(/需规\s*excel_row\s*[:=]?\s*(\d+)/i) || String(text).match(/excel_row\s*[:=]?\s*(\d+)/i);
  return m ? Number(m[1]) : null;
}

function relSrs(p) {
  if (!p) return '';
  const n = String(p).replace(/\\/g, '/');
  const i = n.indexOf('bid-reference/');
  return i >= 0 ? n.slice(i) : n.replace(/^agent-delivery\//, '');
}

/** TEMP_ALGO_ALGO-ENT-GRAPH-108_1 → M_ENT_GRAPH_108_1（T0X 赋号约定，不读 _work） */
function derivedOfficialFromTemp(tempId) {
  const m = String(tempId || '').match(/^TEMP_ALGO_ALGO-([A-Z]+)-([A-Z]+)-(\d+)_(\d+)$/);
  if (!m) return null;
  const id = `M_${m[1]}_${m[2]}_${m[3]}_${m[4]}`;
  return isOfficialId(id) ? id : null;
}

function parseEvidenceRefs(text, defaultBook) {
  const refs = [];
  if (!text) return refs;
  const s = String(text);
  const seen = new Set();
  const add = (book, seq) => {
    const n = Number(seq);
    if (!book || !Number.isFinite(n) || n <= 0) return;
    const k = `${book}|${n}`;
    if (seen.has(k)) return;
    seen.add(k);
    refs.push({ book, seq: n });
  };
  const addMaybeRange = (book, a, b) => {
    const start = Number(a);
    const end = b == null || b === '' ? start : Number(b);
    if (!Number.isFinite(start)) return;
    if (!Number.isFinite(end) || end < start) {
      add(book, start);
      return;
    }
    if (end - start > 2) return;
    for (let i = start; i <= end; i++) add(book, i);
  };
  for (const m of s.matchAll(/srs\/0*2\s*seq\s*(\d+)/gi)) add('02', m[1]);
  for (const m of s.matchAll(/srs\/0*4\s*seq\s*(\d+)/gi)) add('04', m[1]);
  for (const m of s.matchAll(/(?:^|[^/\d])02\s*seq\s*(\d+)(?:\s*[–\-]\s*(\d+))?/g)) addMaybeRange('02', m[1], m[2]);
  for (const m of s.matchAll(/(?:^|[^/\d])04\s*seq\s*(\d+)(?:\s*[–\-]\s*(\d+))?/g)) addMaybeRange('04', m[1], m[2]);
  for (const m of s.matchAll(/05\s*seq\s*(\d+)/gi)) add('05', m[1]);
  if (defaultBook === '02' || defaultBook === '04') {
    for (const m of s.matchAll(/\bSRS\s*seq\s*(\d+)/gi)) add(defaultBook, m[1]);
  }
  return refs;
}

function extractLeaf(text) {
  if (!text) return '';
  const m = String(text).match(/(?:05\s+)?([^\s；;]+\/[^\s#]+\.md#[^\s；;]+)/);
  return m ? m[1].replace(/^05\s+/, '') : '';
}

/** @type {Map<string, object>} */
const algoByReqId = new Map();
/** @type {Map<number, object>} */
const algoBySeq = new Map();
/** @type {Map<string, Map<string, object>>} metric_id → (book|seq → ref) */
const byMetric = new Map();

function ensureMetric(id) {
  const key = String(id).trim();
  if (!byMetric.has(key)) byMetric.set(key, new Map());
  return byMetric.get(key);
}

function addRef(metricId, ref) {
  if (!isOfficialId(metricId)) return false;
  const book = String(ref.book);
  const seq = Number(ref.seq);
  const excelRow = ref.excel_row == null || ref.excel_row === '' ? null : Number(ref.excel_row);
  if (!book || !Number.isFinite(seq)) return false;
  const bucket = ensureMetric(metricId);
  const k = `${book}|${seq}`;
  const prev = bucket.get(k) || {};
  const pages = new Set([...(prev.page_ids || []), ...(ref.page_ids || [])].filter(Boolean));
  const systems = new Set([...(prev.systems || []), ...(ref.systems || [])].filter(Boolean));
  bucket.set(k, {
    book,
    seq,
    excel_row: Number.isFinite(excelRow) ? excelRow : prev.excel_row ?? null,
    name: ref.name || prev.name || '',
    brief: ref.brief || prev.brief || '',
    file: ref.file || prev.file || '',
    requirement_id: ref.requirement_id || prev.requirement_id || null,
    role: ref.role === 'algo_leaf' || prev.role === 'algo_leaf' ? 'algo_leaf' : ref.role || prev.role || 'page_use',
    page_ids: [...pages].sort(),
    systems: [...systems].sort(),
  });
  return true;
}

function findReqByLeaf(leaf) {
  const t = String(leaf || '')
    .replace(/\\/g, '/')
    .trim();
  if (!t) return null;
  const [filePart, anchor] = t.split('#');
  const fileNorm = filePart.replace(/^.*科技专题服务算法库\//, '');
  return (
    [...algoByReqId.values()].find((r) => {
      const p = String(r.srs_path || '').replace(/\\/g, '/');
      const fileOk = fileNorm && p.endsWith(fileNorm);
      const titleOk = !anchor || String(r.requirement_title || '') === anchor;
      return fileOk && titleOk;
    }) || null
  );
}

function addAlgoLeaf(metricId, req, extra = {}) {
  if (!req) return false;
  return addRef(metricId, {
    book: '05',
    seq: req.seq,
    excel_row: req.excel_row ?? extra.excel_row ?? null,
    name: req.requirement_title || extra.name || '',
    brief: extra.brief || clip(`${req.dimension || ''} / ${req.layer || ''}：${req.requirement_title || ''}`, 100),
    file: relSrs(req.srs_path),
    requirement_id: req.requirement_id,
    role: 'algo_leaf',
    page_ids: extra.page_ids || [],
    systems: extra.systems || [],
  });
}

function loadA1() {
  const doc = parseYaml(fs.readFileSync(A1_REQ, 'utf8'));
  const reqs = Array.isArray(doc.requirements) ? doc.requirements : [];
  let n = 0;
  for (const req of reqs) {
    const reqId = req.requirement_id;
    if (reqId) algoByReqId.set(String(reqId), req);
    if (req.seq != null && Number.isFinite(Number(req.seq))) algoBySeq.set(Number(req.seq), req);
    const metrics = Array.isArray(req.metrics) ? req.metrics : [];
    const excerpt = clip(req.requirement_excerpt, 80);
    const name = req.requirement_title || '';
    const briefBase = excerpt || clip(`${req.dimension || ''} / ${req.layer || ''}：${name}`, 80);
    for (const m of metrics) {
      const ids = [];
      if (isOfficialId(m.metric_id)) ids.push(m.metric_id);
      const derived = derivedOfficialFromTemp(m.metric_id);
      if (derived) ids.push(derived);
      const zh = m.metric_name_zh || '';
      for (const id of [...new Set(ids)]) {
        if (
          addRef(id, {
            book: '05',
            seq: req.seq,
            excel_row: req.excel_row ?? null,
            name,
            brief: clip(zh ? `${briefBase} 本指标：${zh}。` : briefBase, 100),
            file: relSrs(req.srs_path),
            requirement_id: reqId,
            role: 'algo_leaf',
          })
        ) {
          n++;
        }
      }
    }
  }
  return { reqs: reqs.length, links: n };
}

function catalogIdOf(row) {
  if (isOfficialId(row.metricId)) return row.metricId.trim();
  if (isOfficialId(row.metricIdImpl)) return row.metricIdImpl.trim();
  return '';
}

function walkA2() {
  const { pages, items, demands } = loadA2SrsRecords(ORCH_ROOT);
  let itemLinks = 0;
  let demandLinks = 0;
  let book02 = 0;
  let book04 = 0;
  const applyRow = (row, counter) => {
    const id = catalogIdOf(row);
    if (!id) return;
    const evidence = [row.basis, row.gapNote].filter(Boolean).join(' ； ');
    const excelRow = extractExcelRow(evidence);
    const pageIds = row.pageId ? [row.pageId] : [];
    const systems = row.a2_system ? [row.a2_system] : [];
    let hit = false;
    if (row.a1Req && algoByReqId.has(String(row.a1Req))) {
      if (
        addAlgoLeaf(id, algoByReqId.get(String(row.a1Req)), {
          brief: clip(`页面 ${row.pageId || ''} 复用算法库叶。本指标：${row.main || id}。`, 100),
          page_ids: pageIds,
          systems,
        })
      ) {
        hit = true;
      }
    }
    const leaf = row.leaf || extractLeaf(evidence);
    if (leaf) {
      const req = findReqByLeaf(leaf);
      if (req && addAlgoLeaf(id, req, { brief: clip(row.meaning || evidence, 80), page_ids: pageIds, systems })) hit = true;
    }
    for (const ev of parseEvidenceRefs(evidence, row.book)) {
      if (ev.book === '05') {
        const req = algoBySeq.get(ev.seq);
        if (
          addRef(id, {
            book: '05',
            seq: ev.seq,
            excel_row: req?.excel_row ?? excelRow,
            name: req?.requirement_title || row.main || '',
            brief: clip(row.meaning || evidence, 80),
            file: relSrs(req?.srs_path || ''),
            requirement_id: req?.requirement_id || null,
            role: 'algo_leaf',
            page_ids: pageIds,
            systems,
          })
        ) {
          hit = true;
        }
        continue;
      }
      const file = ev.book === '02' ? row.srs02 : row.srs04;
      if (
        addRef(id, {
          book: ev.book,
          seq: ev.seq,
          excel_row: excelRow,
          name: row.main || '',
          brief: clip(row.meaning || evidence, 80),
          file: relSrs(file || ''),
          role: 'page_use',
          page_ids: pageIds,
          systems,
        })
      ) {
        hit = true;
        if (ev.book === '02') book02++;
        if (ev.book === '04') book04++;
      }
    }
    if (hit) counter.value += 1;
  };
  const itemCounter = { value: 0 };
  const demandCounter = { value: 0 };
  for (const row of items) applyRow(row, itemCounter);
  for (const row of demands) applyRow(row, demandCounter);
  itemLinks = itemCounter.value;
  demandLinks = demandCounter.value;
  return {
    files: pages.length,
    itemLinks,
    demandLinks,
    book02,
    book04,
  };
}

function dumpYaml(stats) {
  const ids = [...byMetric.keys()].sort();
  const lines = [];
  lines.push('# 指标需求来源（需规叶子）。不是 8 件套。禁止手改当第二真源：改 A1/A2 后重新生成。');
  lines.push('# 生成：node scripts/build-metric-srs-map.mjs（导出 skill / MCP 会先跑本脚本）');
  lines.push('# 查询：MCP metric-get → extras.srs_refs（book + seq + name + brief）');
  lines.push('version: 1');
  lines.push('updated: "2026-08-25"');
  lines.push('model: data-lineage-policy.md §2.1.2 srs_refs');
  lines.push(`a1_requirements: ${stats.a1.reqs}`);
  lines.push(`a1_official_links: ${stats.a1.links}`);
  lines.push(`a2_page_files: ${stats.a2.files}`);
  lines.push(`metrics_with_refs: ${ids.length}`);
  lines.push('book_note: "seq 只在 book 内唯一；02/04/05 的同一数字不是同一条需规。"');
  lines.push('metrics:');
  for (const id of ids) {
    const refs = [...byMetric.get(id).values()].sort((a, b) =>
      a.book === b.book ? a.seq - b.seq : String(a.book).localeCompare(String(b.book)),
    );
    lines.push(`  - metric_id: ${id}`);
    lines.push('    srs_refs:');
    for (const r of refs) {
      lines.push(`      - book: ${yamlScalar(r.book)}`);
      lines.push(`        seq: ${r.seq}`);
      if (r.excel_row != null) lines.push(`        excel_row: ${r.excel_row}`);
      lines.push(`        name: ${yamlScalar(r.name)}`);
      lines.push(`        brief: ${yamlScalar(r.brief)}`);
      if (r.file) lines.push(`        file: ${yamlScalar(r.file)}`);
      if (r.requirement_id) lines.push(`        requirement_id: ${yamlScalar(r.requirement_id)}`);
      lines.push(`        role: ${yamlScalar(r.role)}`);
      if (r.page_ids && r.page_ids.length) {
        lines.push(`        page_ids: [${r.page_ids.map(yamlScalar).join(', ')}]`);
      }
      if (r.systems && r.systems.length) {
        lines.push(`        systems: [${r.systems.map(yamlScalar).join(', ')}]`);
      }
    }
  }
  lines.push('');
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, lines.join('\n'), 'utf8');
  return { out: OUT, metrics: ids.length };
}

const a1 = loadA1();
const a2 = walkA2();
const written = dumpYaml({ a1, a2 });
const rel = path.relative(ORCH_ROOT, written.out).replace(/\\/g, '/');
console.log(
  JSON.stringify(
    {
      ok: true,
      yaml: rel,
      metrics_with_refs: written.metrics,
      a1,
      a2,
    },
    null,
    2,
  ),
);
