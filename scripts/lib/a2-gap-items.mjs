/**
 * A2 页面指标差集：只读解析 metrics/request/{专题系统,展示系统}/pages/*.yaml。
 * items[] 给飞书差集看板（不读 semantic_debt）。
 * demands[] + 未截断 取数依据 给 SRS map（自定义 parseYaml 会在 page_ruling 后停住）。
 * 不读 _work/、不读 fan-in 索引 yaml。
 */
import fs from 'node:fs';
import path from 'node:path';

const SYSTEMS = [
  { folder: '专题系统', system: '专题' },
  { folder: '展示系统', system: '展示' },
];

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export function yamlScalar(raw) {
  let v = (raw || '').trim();
  if (!v || v === 'null' || v === '~' || v === 'undefined') return '';
  if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1).replace(/\\"/g, '"');
  if (v.length > 1 && v.startsWith("'") && v.endsWith("'")) return v.slice(1, -1);
  if (v.startsWith('"') || v.startsWith("'")) return v.slice(1);
  const hash = v.indexOf(' #');
  if (hash >= 0) v = v.slice(0, hash).trim();
  return v;
}

export function fieldOf(block, key) {
  const m = block.match(new RegExp(`^\\s+${escapeRe(key)}:\\s*(.*)$`, 'm'));
  if (!m) return '';
  const v = m[1].trim();
  if (v === '|' || v === '>' || v === '|-' || v === '>') return '';
  return yamlScalar(v);
}

function fieldMultiline(block, key) {
  const lines = block.split(/\r?\n/);
  const re = new RegExp(`^(\\s+)${escapeRe(key)}:\\s*(.*)$`);
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(re);
    if (!m) continue;
    const indent = m[1].length;
    let v = m[2].trim();
    if (v === '|' || v === '>' || v === '|-' || v === '>') {
      const parts = [];
      for (let j = i + 1; j < lines.length; j++) {
        if (!lines[j].trim()) {
          if (parts.length) break;
          continue;
        }
        const lead = lines[j].match(/^(\s*)/)[1].length;
        if (lead <= indent) break;
        parts.push(lines[j].trim());
      }
      return parts.join(' ');
    }
    return yamlScalar(v);
  }
  return '';
}

function extractKeyedSection(raw, key) {
  const m = raw.match(new RegExp(`^${escapeRe(key)}:\\s*\\r?\\n`, 'm'));
  if (!m) return '';
  const start = m.index + m[0].length;
  const rest = raw.slice(start);
  const next = rest.search(/^\S/m);
  return next >= 0 ? rest.slice(0, next) : rest;
}

function extractItemsSection(raw) {
  return extractKeyedSection(raw, 'items');
}

function splitDashBlocks(section, dashKey) {
  const startRe = new RegExp(`^ {2}- ${escapeRe(dashKey)}:`);
  const blocks = [];
  let current = null;
  for (const line of section.split(/\r?\n/)) {
    if (startRe.test(line)) {
      if (current) blocks.push(current);
      current = [line];
    } else if (current) {
      if (/^\S/.test(line) && line.trim() !== '') {
        blocks.push(current);
        current = null;
      } else {
        current.push(line);
      }
    }
  }
  if (current) blocks.push(current);
  return blocks.map((lines) => lines.join('\n'));
}

function splitItemBlocks(section) {
  return splitDashBlocks(section, 'row_id');
}

function clip(s, n) {
  const t = (s || '').replace(/\s+/g, ' ').trim();
  return t.length > n ? `${t.slice(0, n)}…` : t;
}

export function loadA2GapItems(orchRoot) {
  const requestDir = path.join(orchRoot, 'agent-delivery', 'metrics', 'request');
  const items = [];
  for (const sys of SYSTEMS) {
    const pagesDir = path.join(requestDir, sys.folder, 'pages');
    if (!fs.existsSync(pagesDir)) continue;
    for (const name of fs.readdirSync(pagesDir)) {
      if (!name.endsWith('.yaml')) continue;
      const file = path.join(pagesDir, name);
      const raw = fs.readFileSync(file, 'utf8');
      const pageId = yamlScalar((raw.match(/^page_id:\s*(.+)$/m) || [])[1] || '') || name.replace(/\.ya?ml$/, '');
      for (const block of splitItemBlocks(extractItemsSection(raw))) {
        const rowId = fieldOf(block, '- row_id') || fieldOf(block, 'row_id');
        if (!rowId) continue;
        items.push({
          rowId,
          system: sys.system,
          pageId,
          module: fieldOf(block, '模块'),
          page: fieldOf(block, '页面'),
          main: fieldOf(block, '主项'),
          sub: fieldOf(block, '子项'),
          meaning: clip(fieldMultiline(block, '指标含义') || fieldOf(block, '指标含义'), 200),
          caliber: clip(fieldOf(block, '建议取值/取值口径'), 160),
          basisType: fieldOf(block, '取值依据类型'),
          callSystem: fieldOf(block, '调用系统'),
          callModule: fieldOf(block, '调用模块'),
          basis: clip(fieldOf(block, '取数依据'), 160),
          verdict: fieldOf(block, '差集判定'),
          a1Req: fieldOf(block, 'A1需规ID'),
          a1Leaf: fieldOf(block, 'A1指标叶ID'),
          metricId: fieldOf(block, 'metric_id'),
          gapNote: clip(fieldMultiline(block, '缺口说明'), 200),
          dispose: fieldOf(block, '处置桶'),
        });
      }
    }
  }
  items.sort((a, b) => (a.system + a.rowId).localeCompare(b.system + b.rowId, 'zh-Hans-CN'));
  return items;
}

function headerField(raw, key) {
  const m = raw.match(new RegExp(`^${escapeRe(key)}:\\s*(.*)$`, 'm'));
  if (!m) return '';
  return yamlScalar(m[1]);
}

/**
 * A2 items + demands，取数依据/缺口说明不截断。给 metric-srs-map，不给飞书差集看板。
 * 绕开 metric-registry-lib parseYaml：A2 页在 page_ruling / srs05_leaf_map 后会丢 demands/items。
 */
export function loadA2SrsRecords(orchRoot) {
  const requestDir = path.join(orchRoot, 'agent-delivery', 'metrics', 'request');
  const pages = [];
  const items = [];
  const demands = [];
  for (const sys of SYSTEMS) {
    const pagesDir = path.join(requestDir, sys.folder, 'pages');
    if (!fs.existsSync(pagesDir)) continue;
    const book = sys.folder === '展示系统' ? '02' : '04';
    for (const name of fs.readdirSync(pagesDir)) {
      if (!name.endsWith('.yaml')) continue;
      const file = path.join(pagesDir, name);
      const raw = fs.readFileSync(file, 'utf8');
      const pageId = headerField(raw, 'page_id') || name.replace(/\.ya?ml$/, '');
      const srs02 = headerField(raw, 'srs02');
      const srs04 = headerField(raw, 'srs04');
      pages.push({ pageId, book, a2_system: sys.system, folder: sys.folder, srs02, srs04, file: name });
      for (const block of splitItemBlocks(extractItemsSection(raw))) {
        const rowId = fieldOf(block, '- row_id') || fieldOf(block, 'row_id');
        if (!rowId) continue;
        items.push({
          kind: 'item',
          rowId,
          pageId,
          book,
          a2_system: sys.system,
          srs02,
          srs04,
          main: fieldOf(block, '主项'),
          meaning: fieldMultiline(block, '指标含义') || fieldOf(block, '指标含义'),
          basis: fieldMultiline(block, '取数依据') || fieldOf(block, '取数依据'),
          a1Req: fieldOf(block, 'A1需规ID'),
          leaf: fieldOf(block, 'algo_lib_leaf'),
          metricId: fieldOf(block, 'metric_id'),
          metricIdImpl: fieldOf(block, 'metric_id_impl'),
          gapNote: fieldMultiline(block, '缺口说明'),
        });
      }
      for (const block of splitDashBlocks(extractKeyedSection(raw, 'demands'), 'demand_id')) {
        const demandId = fieldOf(block, '- demand_id') || fieldOf(block, 'demand_id');
        if (!demandId) continue;
        demands.push({
          kind: 'demand',
          demandId,
          pageId,
          book,
          a2_system: sys.system,
          srs02,
          srs04,
          main: fieldOf(block, 'metric_name_zh'),
          meaning: '',
          basis: '',
          a1Req: fieldOf(block, 'A1需规ID'),
          leaf: fieldOf(block, 'algo_lib_leaf'),
          metricId: fieldOf(block, 'metric_id'),
          metricIdImpl: fieldOf(block, 'metric_id_impl'),
          gapNote: fieldMultiline(block, '缺口说明'),
        });
      }
    }
  }
  return { pages, items, demands };
}

/** metric_id → 差集判定集合（合同集合推断用；无 ID 的 missing 不进指标对象表） */
export function a2VerdictsByMetric(items) {
  const map = new Map();
  for (const it of items) {
    if (!it.metricId) continue;
    if (!map.has(it.metricId)) map.set(it.metricId, new Set());
    if (it.verdict) map.get(it.metricId).add(it.verdict);
  }
  return map;
}
