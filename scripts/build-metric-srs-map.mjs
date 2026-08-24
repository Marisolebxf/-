#!/usr/bin/env node
/**
 * Build metrics/registry/metric-srs-map.yaml
 *
 * Demand provenance (not 8-piece kit):
 *   05 ← A1 requirements.yaml invert
 *   02/04 ← A2 page items with metric_id + "SRS seq N"
 *   05 extra ← A2 demands with A1需规ID (page-specific M_* reusing an algo leaf)
 *
 * Does not invent M_*. Skips TEMP_ALGO_*. Re-run after A1/A2 updates.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ORCH_ROOT, parseYaml } from './lib/metric-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const A1_REQ = path.join(
  ORCH_ROOT,
  'agent-delivery',
  'metrics',
  'algo-results',
  'ALGO-LIB-METRIC-DEPS-L01-requirements.yaml',
);
const A2_DIRS = [
  { book: '02', dir: path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'request', '展示系统', 'pages') },
  { book: '04', dir: path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'request', '专题系统', 'pages') },
];
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

function extractSrsSeq(text) {
  if (!text) return null;
  const s = String(text);
  const m =
    s.match(/SRS\s*seq\s*(\d+)/i) ||
    s.match(/seq\s+(\d+)/) ||
    s.match(/对上\s*(?:05\s+)?seq\s*(\d+)/);
  return m ? Number(m[1]) : null;
}

function extractExcelRow(text) {
  if (!text) return null;
  const m = String(text).match(/excel_row\s*[:=]?\s*(\d+)/i);
  return m ? Number(m[1]) : null;
}

function relSrs(p) {
  if (!p) return '';
  const n = String(p).replace(/\\/g, '/');
  const i = n.indexOf('bid-reference/');
  return i >= 0 ? n.slice(i) : n.replace(/^agent-delivery\//, '');
}

/** @type {Map<string, {req: object}>} */
const algoByReqId = new Map();
/** @type {Map<string, Map<string, object>>} metric_id → (book|seq → ref) */
const byMetric = new Map();

function ensureMetric(id) {
  const key = String(id).trim();
  if (!byMetric.has(key)) byMetric.set(key, new Map());
  return byMetric.get(key);
}

function addRef(metricId, ref) {
  if (!isOfficialId(metricId)) return;
  const book = String(ref.book);
  const seq = Number(ref.seq);
  const excelRow = ref.excel_row == null || ref.excel_row === '' ? null : Number(ref.excel_row);
  if (!book || !Number.isFinite(seq)) return;
  const bucket = ensureMetric(metricId);
  const k = `${book}|${seq}`;
  const prev = bucket.get(k) || {};
  const pages = new Set([...(prev.page_ids || []), ...(ref.page_ids || [])].filter(Boolean));
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
  });
}

function loadA1() {
  const doc = parseYaml(fs.readFileSync(A1_REQ, 'utf8'));
  const reqs = Array.isArray(doc.requirements) ? doc.requirements : [];
  let n = 0;
  for (const req of reqs) {
    const reqId = req.requirement_id;
    if (reqId) algoByReqId.set(String(reqId), req);
    const metrics = Array.isArray(req.metrics) ? req.metrics : [];
    const excerpt = clip(req.requirement_excerpt, 80);
    const name = req.requirement_title || '';
    const briefBase = excerpt || clip(`${req.dimension || ''} / ${req.layer || ''}：${name}`, 80);
    for (const m of metrics) {
      const id = m.metric_id;
      if (!isOfficialId(id)) continue;
      const zh = m.metric_name_zh || '';
      addRef(id, {
        book: '05',
        seq: req.seq,
        excel_row: req.excel_row ?? null,
        name,
        brief: clip(zh ? `${briefBase} 本指标：${zh}。` : briefBase, 100),
        file: relSrs(req.srs_path),
        requirement_id: reqId,
        role: 'algo_leaf',
      });
      n++;
    }
  }
  return { reqs: reqs.length, links: n };
}

function walkA2() {
  let files = 0;
  let itemLinks = 0;
  let demandLinks = 0;
  for (const { book, dir } of A2_DIRS) {
    if (!fs.existsSync(dir)) continue;
    for (const name of fs.readdirSync(dir).filter((n) => n.endsWith('.yaml'))) {
      files++;
      const full = path.join(dir, name);
      const doc = parseYaml(fs.readFileSync(full, 'utf8'));
      const pageId = doc.page_id || path.basename(name, '.yaml');
      const items = Array.isArray(doc.items) ? doc.items : [];
      for (const it of items) {
        const id = it.metric_id;
        if (!isOfficialId(id)) continue;
        const evidence = String(it['取数依据'] || it.取数依据 || '');
        const m05 = evidence.match(/05\s*seq\s*(\d+)/i);
        const mSrs = evidence.match(/SRS\s*seq\s*(\d+)/i);
        if (m05) {
          const req = [...algoByReqId.values()].find((r) => Number(r.seq) === Number(m05[1]));
          addRef(id, {
            book: '05',
            seq: Number(m05[1]),
            excel_row: req?.excel_row ?? extractExcelRow(evidence),
            name: req?.requirement_title || it['主项'] || it.主项 || '',
            brief: clip(it['指标含义'] || it.指标含义 || evidence, 80),
            file: relSrs(req?.srs_path || ''),
            requirement_id: req?.requirement_id || null,
            role: 'algo_leaf',
            page_ids: [pageId],
          });
          itemLinks++;
        } else if (mSrs) {
          addRef(id, {
            book,
            seq: Number(mSrs[1]),
            excel_row: extractExcelRow(evidence),
            name: it['主项'] || it.主项 || it.metric_name_zh || '',
            brief: clip(it['指标含义'] || it.指标含义 || evidence, 80),
            file: relSrs(doc.srs02 || doc.srs04 || ''),
            role: 'page_use',
            page_ids: [pageId],
          });
          itemLinks++;
        }
      }
      const demands = Array.isArray(doc.demands) ? doc.demands : [];
      for (const d of demands) {
        const id = d.metric_id || d.metric_id_impl;
        if (!isOfficialId(id)) continue;
        const reqId = d.A1需规ID || d['A1需规ID'];
        if (reqId && algoByReqId.has(String(reqId))) {
          const req = algoByReqId.get(String(reqId));
          addRef(id, {
            book: '05',
            seq: req.seq,
            excel_row: req.excel_row ?? null,
            name: req.requirement_title || '',
            brief: clip(`页面 ${pageId} 复用算法库叶。本指标：${d.metric_name_zh || id}。`, 100),
            file: relSrs(req.srs_path),
            requirement_id: reqId,
            role: 'algo_leaf',
            page_ids: [pageId],
          });
          demandLinks++;
        }
      }
    }
  }
  return { files, itemLinks, demandLinks };
}

function dumpYaml(stats) {
  const ids = [...byMetric.keys()].sort();
  const lines = [];
  lines.push('# 指标需求来源（需规叶子）。不是 8 件套。禁止手改当第二真源：改 A1/A2 后重新生成。');
  lines.push('# 生成：node scripts/build-metric-srs-map.mjs');
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
