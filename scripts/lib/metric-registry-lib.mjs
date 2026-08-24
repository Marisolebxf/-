#!/usr/bin/env node
/**
 * Read-only loader for metrics/registry seed + readiness matrix.
 * Join key = metric_id. Does not write YAML.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const REGISTRY_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'registry');

export const KIT_FIELDS = [
  'metric_id',
  'metric_name_zh',
  'definition',
  'formula',
  'algorithm_type',
  'source_tables',
  'source_systems',
  'update_freq',
  'version',
];

const READINESS_FIELDS = [
  'd1_def_status',
  'd1_pending_ref',
  'd1_note',
  'd2_schema_status',
  'd2_schema_detail',
  'd2_assessed',
  'd3_source_mapping_status',
  'd3_gap',
  'd4_ingestion_status',
  'd4_ingestion_stages',
  'lifecycle_stage',
  'legacy_mapping_status',
];

let cache = null;

export function invalidateMetricCache() {
  cache = null;
}

function fileMtime(p) {
  try {
    return fs.statSync(p).mtimeMs;
  } catch {
    return 0;
  }
}

export const SRS_MAP_FILE = 'metric-srs-map.yaml';

export function listRegistryFiles() {
  if (!fs.existsSync(REGISTRY_DIR)) {
    throw new Error(`metrics registry dir not found: ${REGISTRY_DIR}`);
  }
  const names = fs.readdirSync(REGISTRY_DIR).filter((n) => n.endsWith('.yaml'));
  return {
    seeds: names.filter((n) => n.startsWith('cfg_metric-') && n.endsWith('-seed.yaml')).sort(),
    matrices: names.filter((n) => n.startsWith('metric-readiness-matrix-')).sort(),
    srsMap: names.includes(SRS_MAP_FILE) ? SRS_MAP_FILE : null,
  };
}

function relRegistry(name) {
  return `metrics/registry/${name}`;
}

// ── YAML subset (indent maps/lists + flow []/{} + > / |) ─────────

function stripBom(text) {
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

function isBlankOrComment(line) {
  const t = line.trim();
  return !t || t.startsWith('#');
}

function indentOf(line) {
  const m = line.match(/^( *)/);
  return m ? m[1].length : 0;
}

function findUnquotedHash(s) {
  let q = null;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) {
      if (c === '\\' && q === '"') {
        i++;
        continue;
      }
      if (c === q) q = null;
      continue;
    }
    if (c === '"' || c === "'") {
      q = c;
      continue;
    }
    if (c === '#' && (i === 0 || /\s/.test(s[i - 1]))) return i;
  }
  return -1;
}

function unquote(s) {
  if (s.length >= 2 && ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'")))) {
    const inner = s.slice(1, -1);
    if (s.startsWith('"')) {
      return inner.replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\\\/g, '\\');
    }
    return inner;
  }
  return s;
}

function splitTopLevel(s, sep) {
  const out = [];
  let buf = '';
  let depthBrace = 0;
  let depthBrack = 0;
  let q = null;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) {
      buf += c;
      if (c === '\\' && q === '"') {
        i++;
        if (i < s.length) buf += s[i];
        continue;
      }
      if (c === q) q = null;
      continue;
    }
    if (c === '"' || c === "'") {
      q = c;
      buf += c;
      continue;
    }
    if (c === '{') depthBrace++;
    else if (c === '}') depthBrace--;
    else if (c === '[') depthBrack++;
    else if (c === ']') depthBrack--;
    if (c === sep && depthBrace === 0 && depthBrack === 0) {
      out.push(buf.trim());
      buf = '';
      continue;
    }
    buf += c;
  }
  if (buf.trim()) out.push(buf.trim());
  return out;
}

function parseFlowSeq(s) {
  const inner = s.slice(1, -1).trim();
  if (!inner) return [];
  return splitTopLevel(inner, ',').map(parseScalar);
}

function parseFlowMap(s) {
  const inner = s.slice(1, -1).trim();
  if (!inner) return {};
  const obj = {};
  for (const part of splitTopLevel(inner, ',')) {
    const idx = part.indexOf(':');
    if (idx < 0) continue;
    const k = part.slice(0, idx).trim();
    const v = part.slice(idx + 1).trim();
    obj[k] = parseScalar(v);
  }
  return obj;
}

function parseScalar(raw) {
  if (raw == null) return null;
  let s = String(raw).trim();
  if (!s) return '';
  const hash = findUnquotedHash(s);
  if (hash >= 0) s = s.slice(0, hash).trim();
  if (!s || s === '~' || s === 'null') return null;
  if (s === 'true') return true;
  if (s === 'false') return false;
  if ((s.startsWith('[') && s.endsWith(']')) || (s.startsWith('{') && s.endsWith('}'))) {
    if (s.startsWith('[')) return parseFlowSeq(s);
    return parseFlowMap(s);
  }
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    return unquote(s);
  }
  return s;
}

function nextContentIndex(lines, i) {
  let j = i;
  while (j < lines.length && isBlankOrComment(lines[j])) j++;
  return j;
}

function parseNode(lines, start, minIndent) {
  const i0 = nextContentIndex(lines, start);
  if (i0 >= lines.length) return { value: null, next: i0 };
  const line = lines[i0];
  const ind = indentOf(line);
  if (ind < minIndent) return { value: null, next: i0 };
  const trimmed = line.trim();
  if (trimmed.startsWith('- ')) {
    return parseList(lines, i0, ind);
  }
  return parseMap(lines, i0, ind);
}

function parseMap(lines, start, mapIndent) {
  const obj = {};
  let i = start;
  while (i < lines.length) {
    if (isBlankOrComment(lines[i])) {
      i++;
      continue;
    }
    const ind = indentOf(lines[i]);
    if (ind < mapIndent) break;
    if (ind > mapIndent) break;
    const trimmed = lines[i].trim();
    if (trimmed.startsWith('- ')) break;
    const colon = trimmed.indexOf(':');
    if (colon < 0) {
      i++;
      continue;
    }
    const key = trimmed.slice(0, colon).trim();
    const rest = trimmed.slice(colon + 1);
    const hash = findUnquotedHash(rest);
    const rhs = (hash >= 0 ? rest.slice(0, hash) : rest).trim();
    i++;
    if (rhs === '>' || rhs === '|') {
      const folded = [];
      const blockIndent = mapIndent + 2;
      while (i < lines.length) {
        if (isBlankOrComment(lines[i]) && indentOf(lines[i]) <= mapIndent) break;
        if (!isBlankOrComment(lines[i]) && indentOf(lines[i]) < blockIndent) break;
        if (isBlankOrComment(lines[i]) && !lines[i].trim()) {
          folded.push('');
          i++;
          continue;
        }
        folded.push(lines[i].slice(blockIndent));
        i++;
      }
      obj[key] = rhs === '|' ? folded.join('\n') : folded.join(' ').replace(/\s+/g, ' ').trim();
      continue;
    }
    if (rhs !== '') {
      obj[key] = parseScalar(rhs);
      continue;
    }
    const peek = nextContentIndex(lines, i);
    if (peek >= lines.length) {
      obj[key] = null;
      continue;
    }
    const pInd = indentOf(lines[peek]);
    const pTrim = lines[peek].trim();
    if (pTrim.startsWith('- ') && pInd === mapIndent) {
      const nested = parseList(lines, peek, pInd);
      obj[key] = nested.value;
      i = nested.next;
      continue;
    }
    if (pInd <= mapIndent) {
      obj[key] = null;
      continue;
    }
    const nested = parseNode(lines, peek, pInd);
    obj[key] = nested.value;
    i = nested.next;
  }
  return { value: obj, next: i };
}

function parseList(lines, start, listIndent) {
  const arr = [];
  let i = start;
  while (i < lines.length) {
    if (isBlankOrComment(lines[i])) {
      i++;
      continue;
    }
    const ind = indentOf(lines[i]);
    if (ind < listIndent) break;
    if (ind > listIndent) break;
    const trimmed = lines[i].trim();
    if (!trimmed.startsWith('- ')) break;
    const afterDash = trimmed.slice(2);
    i++;
    if (afterDash.includes(':') && !afterDash.startsWith('"') && !afterDash.startsWith("'") && !afterDash.startsWith('[') && !afterDash.startsWith('{')) {
      const fake = `${' '.repeat(listIndent + 2)}${afterDash}`;
      const restLines = [fake, ...lines.slice(i)];
      const nested = parseMap(restLines, 0, listIndent + 2);
      arr.push(nested.value);
      i += nested.next - 1;
      continue;
    }
    if (afterDash === '' || afterDash === '>' || afterDash === '|') {
      const nested = parseNode(lines, i, listIndent + 2);
      arr.push(nested.value);
      i = nested.next;
      continue;
    }
    arr.push(parseScalar(afterDash));
  }
  return { value: arr, next: i };
}

export function parseYaml(text) {
  const lines = stripBom(text).split(/\r?\n/);
  return parseMap(lines, 0, 0).value || {};
}

export function parseMetricsYaml(text) {
  const doc = parseYaml(text);
  const metrics = Array.isArray(doc.metrics) ? doc.metrics : [];
  const header = { ...doc };
  delete header.metrics;
  return { header, metrics };
}

function domainFromSeedName(name) {
  const m = name.match(/^cfg_metric-(.+)-seed\.yaml$/);
  return m ? m[1] : '';
}

function domainFromMatrixName(name) {
  const m = name.match(/^metric-readiness-matrix-(.+)\.yaml$/);
  return m ? m[1] : '';
}

function pick(obj, keys) {
  const out = {};
  if (!obj) return out;
  for (const k of keys) {
    if (obj[k] !== undefined) out[k] = obj[k];
  }
  return out;
}

function extrasFrom(rec) {
  const skip = new Set([...KIT_FIELDS, ...READINESS_FIELDS, 'metric_id', 'srs_refs']);
  const out = {};
  for (const src of [rec.seed, rec.matrix]) {
    if (!src) continue;
    for (const [k, v] of Object.entries(src)) {
      if (skip.has(k) || out[k] !== undefined) continue;
      out[k] = v;
    }
  }
  out.srs_refs = (Array.isArray(rec.srs_refs) ? rec.srs_refs : []).map((r) => ({
    ...r,
    seq: r.seq == null || r.seq === '' ? r.seq : Number(r.seq),
    excel_row: r.excel_row == null || r.excel_row === '' ? r.excel_row : Number(r.excel_row),
  }));
  return out;
}

export function loadCatalog(force = false) {
  const listed = listRegistryFiles();
  const stamp = [...listed.seeds, ...listed.matrices, listed.srsMap || '']
    .map((n) => `${n}:${fileMtime(path.join(REGISTRY_DIR, n))}`)
    .join('|');
  if (!force && cache && cache.stamp === stamp) return cache;

  const byId = new Map();
  const seedFiles = [];
  const matrixFiles = [];

  function ensure(id) {
    const key = String(id || '').trim();
    if (!key) return null;
    if (!byId.has(key)) {
      byId.set(key, {
        metric_id: key,
        seed: null,
        matrix: null,
        seed_file: null,
        matrix_file: null,
        seed_domain: null,
        matrix_domain: null,
        srs_refs: [],
      });
    }
    return byId.get(key);
  }

  for (const name of listed.seeds) {
    const full = path.join(REGISTRY_DIR, name);
    const parsed = parseMetricsYaml(fs.readFileSync(full, 'utf8'));
    const domain = parsed.header.domain || domainFromSeedName(name);
    seedFiles.push({
      file: relRegistry(name),
      domain,
      declared_total: parsed.header.total_metrics ?? null,
      parsed: parsed.metrics.length,
    });
    for (const row of parsed.metrics) {
      const rec = ensure(row.metric_id);
      if (!rec) continue;
      rec.seed = row;
      rec.seed_file = relRegistry(name);
      rec.seed_domain = domain;
    }
  }

  for (const name of listed.matrices) {
    const full = path.join(REGISTRY_DIR, name);
    const parsed = parseMetricsYaml(fs.readFileSync(full, 'utf8'));
    const domain = parsed.header.module || parsed.header.domain || domainFromMatrixName(name);
    matrixFiles.push({
      file: relRegistry(name),
      domain,
      parsed: parsed.metrics.length,
    });
    for (const row of parsed.metrics) {
      const rec = ensure(row.metric_id);
      if (!rec) continue;
      rec.matrix = row;
      rec.matrix_file = relRegistry(name);
      rec.matrix_domain = domain;
    }
  }

  let srsMapFile = null;
  let srsMapParsed = 0;
  if (listed.srsMap) {
    const full = path.join(REGISTRY_DIR, listed.srsMap);
    const parsed = parseMetricsYaml(fs.readFileSync(full, 'utf8'));
    srsMapFile = relRegistry(listed.srsMap);
    srsMapParsed = parsed.metrics.length;
    for (const row of parsed.metrics) {
      const key = String(row.metric_id || '').trim();
      let rec = byId.get(key);
      if (!rec) {
        const lower = key.toLowerCase();
        for (const [id, existing] of byId) {
          if (id.toLowerCase() === lower) {
            rec = existing;
            break;
          }
        }
      }
      if (!rec) continue;
      rec.srs_refs = Array.isArray(row.srs_refs) ? row.srs_refs : [];
    }
  }

  const byIdLower = new Map();
  for (const [id, rec] of byId) {
    byIdLower.set(id.toLowerCase(), rec);
  }

  cache = {
    stamp,
    byId,
    byIdLower,
    seedFiles,
    matrixFiles,
    srsMapFile,
    srsMapParsed,
  };
  return cache;
}

function kitFrom(rec) {
  const row = rec.seed || {};
  const kit = {};
  for (const k of KIT_FIELDS) {
    kit[k] = row[k] !== undefined ? row[k] : null;
  }
  kit.metric_id = rec.metric_id;
  if (kit.metric_name_zh == null && rec.matrix?.metric_name_zh) {
    kit.metric_name_zh = rec.matrix.metric_name_zh;
  }
  if (kit.algorithm_type === 'API') kit.algorithm_type = 'third_party';
  if (kit.algorithm_type == null || kit.algorithm_type === '') {
    kit.algorithm_type = 'UNKNOWN';
    kit.algorithm_type_inferred = true;
  }
  return kit;
}

function readinessFrom(rec) {
  const row = rec.matrix || {};
  const r = pick(row, READINESS_FIELDS);
  if (r.lifecycle_stage == null || r.lifecycle_stage === '') {
    r.lifecycle_stage = 'unspecified';
    r.lifecycle_stage_inferred = true;
  }
  if (!rec.matrix && rec.seed) {
    r.d1_def_status = r.d1_def_status || null;
    r.note = 'matrix_missing';
  }
  if (rec.matrix && !rec.seed) {
    r.note = r.note || 'seed_missing';
  }
  return r;
}

export function presentMetric(rec, fields = 'full') {
  const found = {
    seed: Boolean(rec.seed),
    matrix: Boolean(rec.matrix),
    srs_map: Array.isArray(rec.srs_refs) && rec.srs_refs.length > 0,
  };
  const kit = kitFrom(rec);
  const readiness = readinessFrom(rec);
  const summary = {
    metric_id: rec.metric_id,
    metric_name_zh: kit.metric_name_zh || rec.matrix?.metric_name_zh || '',
    domain: rec.seed_domain || rec.matrix_domain || '',
    algorithm_type: kit.algorithm_type,
    d1: readiness.d1_def_status ?? null,
    d4: readiness.d4_ingestion_status ?? null,
    srs_ref_count: Array.isArray(rec.srs_refs) ? rec.srs_refs.length : 0,
    found,
  };
  if (fields === 'summary') return summary;
  return {
    ...summary,
    kit,
    readiness,
    extras: extrasFrom(rec),
    sources: {
      seed_file: rec.seed_file,
      matrix_file: rec.matrix_file,
      srs_map_file: loadCatalog().srsMapFile,
    },
  };
}

export function getMetric(id) {
  const catalog = loadCatalog();
  const key = String(id || '').trim();
  if (!key) return { error: 'metric_id required' };
  const rec = catalog.byId.get(key) || catalog.byIdLower.get(key.toLowerCase());
  if (!rec) {
    const hits = queryMetrics({ q: key, limit: 8, fields: 'summary' });
    return {
      error: `Metric not found: ${key}`,
      suggestions: hits.metrics,
    };
  }
  return presentMetric(rec, 'full');
}

function matchText(rec, q) {
  if (!q) return true;
  const kw = String(q).trim().toLowerCase();
  if (!kw) return true;
  const kit = kitFrom(rec);
  const name = (kit.metric_name_zh || rec.matrix?.metric_name_zh || '').toLowerCase();
  const id = rec.metric_id.toLowerCase();
  const def = String(kit.definition || '').toLowerCase();
  return id.includes(kw) || name.includes(kw) || def.includes(kw) || id === kw.toUpperCase();
}

export function queryMetrics(args = {}) {
  const {
    q,
    domain,
    d1,
    d4,
    algorithm_type,
    found,
    limit = 20,
    fields = 'summary',
  } = args;
  const catalog = loadCatalog();
  let results = [];
  for (const rec of catalog.byId.values()) {
    if (domain) {
      const d = (rec.seed_domain || rec.matrix_domain || '').toUpperCase();
      if (d !== String(domain).toUpperCase()) continue;
    }
    if (!matchText(rec, q)) continue;
    const shown = presentMetric(rec, 'full');
    if (d1 && String(shown.readiness.d1_def_status || '') !== String(d1)) continue;
    if (d4 && String(shown.readiness.d4_ingestion_status || '') !== String(d4)) continue;
    if (algorithm_type && String(shown.kit.algorithm_type || '') !== String(algorithm_type)) continue;
    if (found === 'seed' && !shown.found.seed) continue;
    if (found === 'matrix' && !shown.found.matrix) continue;
    if (found === 'both' && !(shown.found.seed && shown.found.matrix)) continue;
    if (found === 'seed_only' && !(shown.found.seed && !shown.found.matrix)) continue;
    if (found === 'matrix_only' && !(!shown.found.seed && shown.found.matrix)) continue;
    results.push(fields === 'full' ? shown : presentMetric(rec, 'summary'));
  }
  results.sort((a, b) => String(a.metric_id).localeCompare(String(b.metric_id)));
  const matched = results.length;
  const cap = Number(limit) > 0 ? Number(limit) : results.length;
  results = results.slice(0, cap);
  return {
    total_in_registry: catalog.byId.size,
    matched,
    returned: results.length,
    metrics: results,
  };
}

function bump(map, key) {
  const k = key || 'unknown';
  map[k] = (map[k] || 0) + 1;
}

export function summarizeMetrics(domain) {
  const catalog = loadCatalog();
  const byDomain = {};
  const byD1 = {};
  const byD4 = {};
  const byType = {};
  let seedOnly = 0;
  let matrixOnly = 0;
  let both = 0;
  let total = 0;
  let withSrs = 0;
  for (const rec of catalog.byId.values()) {
    const d = rec.seed_domain || rec.matrix_domain || 'unknown';
    if (domain && d.toUpperCase() !== String(domain).toUpperCase()) continue;
    total++;
    bump(byDomain, d);
    const shown = presentMetric(rec, 'full');
    bump(byD1, shown.readiness.d1_def_status);
    bump(byD4, shown.readiness.d4_ingestion_status);
    bump(byType, shown.kit.algorithm_type);
    if (shown.found.seed && shown.found.matrix) both++;
    else if (shown.found.seed) seedOnly++;
    else matrixOnly++;
    if (shown.found.srs_map) withSrs++;
  }
  return {
    total,
    coverage: { both, seed_only: seedOnly, matrix_only: matrixOnly },
    srs_refs: {
      with_refs: withSrs,
      without_refs: total - withSrs,
      map_file: catalog.srsMapFile,
      map_parsed: catalog.srsMapParsed,
    },
    by_domain: byDomain,
    by_d1: byD1,
    by_d4: byD4,
    by_algorithm_type: byType,
    files: { seeds: catalog.seedFiles, matrices: catalog.matrixFiles },
  };
}
