/**
 * A2 页面指标差集：只读解析 metrics/request/{专题系统,展示系统}/pages/*.yaml 的 items[]。
 * 不读 _work/、不读 fan-in 索引 yaml、不读 semantic_debt / demands（语义欠账不进飞书）。
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

function extractItemsSection(raw) {
  const m = raw.match(/^items:\s*\r?\n/m);
  if (!m) return '';
  return raw.slice(m.index + m[0].length);
}

function splitItemBlocks(section) {
  const blocks = [];
  let current = null;
  for (const line of section.split(/\r?\n/)) {
    if (/^ {2}- row_id:/.test(line)) {
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
