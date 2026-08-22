/**
 * 给人说明 §5 WBS + §8.0 点名任务 → 飞书「指标算法WBS」行。
 * 不把全文 / xlsx 当行；registry 状态由调用方注入。
 */
import fs from 'node:fs';

const PHASE = {
  0: 'WBS-0 治理与会合',
  1: 'WBS-1 合同盘点',
  2: 'WBS-2 产品定义',
  3: 'WBS-3 语义与血缘',
  4: 'WBS-4 实现分流',
  5: 'WBS-5 算法库合规',
  6: 'WBS-6 联调硬化',
};

const SCRAP = new Set([
  'TOPIC-METRIC-INVENTORY-L01',
  'TOPIC-METRIC-CLASSIFY-L01',
  'DS-METRIC-INVENTORY-L01',
  'DS-METRIC-CLASSIFY-L01',
]);

/** 给人说明 §8.1 / §8.2：该 WBS 编号最晚必须完成日（Asia/Shanghai 日历日）。无硬窗口则不写。 */
const WBS_DEADLINE = {
  '0.3': '2026-08-27',
  '0.4': '2026-08-23',
  '1.1': '2026-08-25',
  '1.1.1': '2026-08-23',
  '1.1.2': '2026-08-23',
  '1.1.3': '2026-08-24',
  '1.1.4': '2026-08-24',
  '1.1.5': '2026-08-24',
  '1.1.6': '2026-08-25',
  '1.1.7': '2026-08-25',
  '1.1.8': '2026-08-25',
  '1.1.9': '2026-08-25',
  '1.2.1': '2026-08-23',
  '1.2.2': '2026-08-23',
  '1.2.3': '2026-08-23',
  '1.3': '2026-08-27',
};

/** §8.0 点名叶：仅当 WBS 编号本身没有更细窗口时使用。 */
const TASK_DEADLINE = {
  'ALGO-LIB-METRIC-DEPS-L01': '2026-08-25',
  'TOPIC-ALGO-GAP-L01': '2026-08-23',
  'DS-ALGO-GAP-L01': '2026-08-23',
  'TOPIC-DS-METRIC-GAP-L01': '2026-08-23',
};

export function planDeadline(wbs, taskId) {
  if (wbs && WBS_DEADLINE[wbs]) return WBS_DEADLINE[wbs];
  if (taskId && TASK_DEADLINE[taskId]) return TASK_DEADLINE[taskId];
  return '';
}

const EXTRA_TASKS = [
  { wbs: '4.6', id: 'LUMEN-CHAIN-METRIC-SVC-L01', title: 'B 轨 CHAIN 入库（63 M_CHAIN_*）', owner: '算法/李伟' },
  { wbs: '4.6', id: 'LUMEN-SVC-METRIC-SVC-L01', title: 'B 轨 SVC 入库（29 M_SVC_*）', owner: '算法/侯佳伟' },
  { wbs: '4.6', id: 'TOPIC-CHAIN-METRIC-MIGRATE-L01', title: 'B 轨迁 demo 页 · 产业链', owner: '李伟' },
  { wbs: '4.6', id: 'TOPIC-SVC-METRIC-MIGRATE-L01', title: 'B 轨迁 demo 页 · 产业服务', owner: '侯佳伟' },
  { wbs: '5.1', id: 'SVC-ALGO-DESIGN-L01', title: '产业服务深度分析算法设计卡', owner: '唐绍祖' },
  { wbs: '5.1', id: 'COMP-ALGO-DESIGN-L01', title: '产业综合分析算法设计卡', owner: '唐绍祖' },
  { wbs: '5.2', id: 'LUMEN-ALGO-PLATFORM-UI-L01', title: '联调台 · 总览+企业', owner: '孔东' },
  { wbs: '5.2', id: 'LUMEN-UI-ALGO-APIVIEW-CHAIN-L01', title: '联调台 · 产业链', owner: '孔东' },
  { wbs: '5.2', id: 'LUMEN-UI-ALGO-APIVIEW-POLICY-L01', title: '联调台 · 政策', owner: '孔东' },
  { wbs: '5.2', id: 'LUMEN-UI-ALGO-APIVIEW-SVC-L01', title: '联调台 · 产业服务', owner: '孔东' },
  { wbs: '5.2', id: 'ALGO-LIB-UI-NAV-L01', title: '联调台 · demo 导航', owner: '孔东' },
];

const PENDING_PACKAGES = [
  {
    wbs: '4.6',
    rowId: 'WBS-4.6/pending-ent-synth',
    title: 'B 轨迁 demo 页 · 企业+综合（待建叶）',
    owner: '徐滕强',
    note: '对应指标入库后再 MCP 建单；不挡 8/25',
  },
  {
    wbs: '4.6',
    rowId: 'WBS-4.6/pending-policy',
    title: 'B 轨迁 demo 页 · 政策（待建叶）',
    owner: '淮政玮',
    note: '对应指标入库后再 MCP 建单；不挡 8/25',
  },
];

/** §8.4 甲/乙 建议 ID：现网没有才投影为「未建单」，禁止本脚本 MCP 建单。 */
const SUGGESTED_OPEN = [
  { id: 'SVCCHAIN-METRIC-OPEN-L01', title: '应补登 · 产业服务链 OPEN' },
  { id: 'TOPIC-ENT-METRIC-OPEN-L01', title: '应补登 · 专题企业 OPEN' },
  { id: 'TOPIC-TECH-METRIC-OPEN-L01', title: '应补登 · 专题技术链 OPEN' },
  { id: 'TOPIC-ORG-METRIC-OPEN-L01', title: '应补登 · 专题科研机构 OPEN' },
  { id: 'TOPIC-TALENT-METRIC-OPEN-L01', title: '应补登 · 专题人才 OPEN' },
  { id: 'TOPIC-QUERY-METRIC-OPEN-L01', title: '应补登 · 专题查询 OPEN' },
  { id: 'ZHIKU-METRIC-OPEN-L01', title: '应补登 · 智库 OPEN（核对记录已有）' },
  { id: 'DS13-16-TALENT-METRIC-OPEN-L01', title: '应补登 · 展示人才态势 OPEN' },
  { id: 'DS21-24-GRAPH-METRIC-OPEN-L01', title: '应补登 · 展示知识图谱 OPEN' },
  { id: 'DS25-29-ACHIEVE-METRIC-OPEN-L01', title: '应补登 · 展示科技成果 OPEN' },
  { id: 'DS30-SVC-METRIC-OPEN-L01', title: '应补登 · 展示服务全景 OPEN' },
];

function stripMd(s) {
  return (s || '')
    .replace(/\*\*/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}

function splitRow(line) {
  const cells = line.split('|').map((c) => c.trim());
  return cells.slice(1, cells.length - 1);
}

function extractTaskIds(text) {
  const ids = [];
  const re = /`([A-Z][A-Za-z0-9-]+)`/g;
  let m;
  while ((m = re.exec(text || ''))) {
    const id = m[1];
    if (id.includes('*') || id.includes('{') || id.includes('MODULE')) continue;
    if (!/-L\d+$/.test(id)) continue;
    ids.push(id);
  }
  return [...new Set(ids)];
}

function phaseOf(wbsNum) {
  const n = Number(String(wbsNum).split('.')[0]);
  return PHASE[n] || '其他';
}

function kindOf(wbsNum, taskIds, note) {
  if (taskIds[0] && SCRAP.has(taskIds[0])) return '废作';
  if (/不另建单/.test(note)) return '维内步骤';
  if (/\{MODULE\}/.test(note) || /现网 0 条/.test(note)) return '工作包';
  if (!taskIds.length) return '未建单';
  return '工作包';
}

function trackOf(wbs) {
  if (wbs === 'scrap') return '勿再派';
  if (wbs === '1.1' || /^1\.1\.\d+$/.test(wbs)) return '8/25硬路径';
  return '不挡8/25';
}

export function parseWbsSection(raw) {
  const start = raw.search(/^## 5\. WBS/m);
  const end = raw.search(/^## 6\./m);
  if (start < 0) throw new Error('给人说明缺少 §5 WBS');
  const body = raw.slice(start, end > start ? end : undefined);
  const rows = [];
  let phaseTitle = PHASE[0];
  let header = null;

  for (const line of body.split(/\r?\n/)) {
    const h = line.match(/^###\s+WBS-(\d+)\s+(.+)$/);
    if (h) {
      phaseTitle = `WBS-${h[1]} ${stripMd(h[2])}`;
      header = null;
      continue;
    }
    if (!line.trim().startsWith('|')) {
      header = null;
      continue;
    }
    const cells = splitRow(line);
    if (!cells.length) continue;
    if (/^:?-{3,}/.test(cells[0])) continue;
    if (cells[0] === 'ID' || /^ID\b/.test(cells[0])) {
      header = cells;
      continue;
    }
    if (!header) continue;
    const id = stripMd(cells[0]);
    if (!/^\d+(\.\d+)*$/.test(id)) continue;
    const pack = stripMd(cells[1] || '');
    const owner = stripMd(cells[2] || '');
    const rest = cells.slice(3).join(' | ');
    const note = stripMd(rest);
    const taskIds = extractTaskIds(cells.join(' '));
    rows.push({
      rowId: `WBS-${id}`,
      wbs: id,
      phase: phaseTitle || phaseOf(id),
      title: pack,
      owner,
      taskIds,
      note,
      kind: kindOf(id, taskIds, note),
    });
  }

  if (!rows.some((r) => r.wbs === '6' || String(r.wbs).startsWith('6.'))) {
    rows.push({
      rowId: 'WBS-6',
      wbs: '6',
      phase: PHASE[6],
      title: '联调硬化（门 I1 → I2 → I3；I2-04 / 附录 D/E）',
      owner: '联调',
      taskIds: [],
      note: '§5 无表；按实现规程门 I',
      kind: '未建单',
    });
  }
  return rows;
}

function inheritLoopSteps(packs) {
  const parent = packs.find((r) => r.wbs === '1.1');
  if (!parent?.taskIds?.length) return packs;
  for (const r of packs) {
    if (/^1\.1\.\d+$/.test(r.wbs) && !r.taskIds.length) {
      r.taskIds = [...parent.taskIds];
      r.kind = '维内步骤';
      if (!/不另建单/.test(r.note)) r.note = `${r.note}；不另建单`.replace(/^；/, '');
    }
  }
  return packs;
}

export function extraTaskRows() {
  return EXTRA_TASKS.map((t) => ({
    rowId: `WBS-${t.wbs}/${t.id}`,
    wbs: t.wbs,
    phase: phaseOf(t.wbs),
    title: t.title,
    owner: t.owner,
    taskIds: [t.id],
    note: '§8.0 点名任务',
    kind: '任务叶',
  }));
}

export function scrapRows() {
  return [...SCRAP].map((id) => ({
    rowId: `WBS-scrap/${id}`,
    wbs: 'scrap',
    phase: '勿再派',
    title: id,
    owner: '—',
    taskIds: [id],
    note: '废作四叶，不标 done、不继续',
    kind: '废作',
  }));
}

export function openLeafRows(registryIds) {
  return registryIds
    .filter((id) => id.endsWith('-METRIC-OPEN-L01'))
    .filter((id) => !id.includes('READINESS'))
    .sort()
    .map((id) => ({
      rowId: `WBS-2.2/${id}`,
      wbs: '2.2',
      phase: PHASE[2],
      title: `METRIC-OPEN · ${id.replace(/-METRIC-OPEN-L01$/, '')}`,
      owner: '淮政玮口径 / 唐绍祖公式',
      taskIds: [id],
      note: 'WBS-2.2 现网叶；不挡 8/25',
      kind: '任务叶',
    }));
}

function suggestedOpenRows(registryIds) {
  const have = new Set(registryIds);
  return SUGGESTED_OPEN.filter((t) => !have.has(t.id)).map((t) => ({
    rowId: `WBS-2.2/pending/${t.id}`,
    wbs: '2.2',
    phase: PHASE[2],
    title: t.title,
    owner: '淮政玮 / 唐绍祖',
    taskIds: [],
    note: `建议 ID ${t.id}；确认后才 MCP 建单，本投影不建单`,
    kind: '未建单',
  }));
}

function pendingPackageRows() {
  return PENDING_PACKAGES.map((t) => ({
    rowId: t.rowId,
    wbs: t.wbs,
    phase: phaseOf(t.wbs),
    title: t.title,
    owner: t.owner,
    taskIds: [],
    note: t.note,
    kind: '未建单',
  }));
}

function expandMultiTaskPacks(packs) {
  const out = [];
  for (const p of packs) {
    if (p.kind === '任务叶' || p.kind === '废作') {
      out.push({ ...p, taskId: p.taskIds[0] || '' });
      continue;
    }
    if (p.taskIds.length <= 1) {
      out.push({ ...p, taskId: p.taskIds[0] || '' });
      continue;
    }
    out.push({
      ...p,
      taskId: '',
      note: `${p.note}；子行 ${p.taskIds.join(' / ')}`,
    });
    for (const id of p.taskIds) {
      out.push({
        rowId: `WBS-${p.wbs}/${id}`,
        wbs: p.wbs,
        phase: p.phase,
        title: `${p.title} · ${id}`,
        owner: p.owner,
        taskIds: [id],
        taskId: id,
        note: p.note,
        kind: '任务叶',
      });
    }
  }
  return out;
}

export function loadWbsWorkpacks(sourcePath, registryIds = []) {
  const raw = fs.readFileSync(sourcePath, 'utf8');
  const packs = inheritLoopSteps(parseWbsSection(raw));
  const seenTasks = new Set(packs.flatMap((r) => r.taskIds));
  const extras = extraTaskRows().filter((r) => !r.taskIds.some((id) => seenTasks.has(id)));
  extras.forEach((r) => r.taskIds.forEach((id) => seenTasks.add(id)));
  const opens = openLeafRows(registryIds).filter((r) => !seenTasks.has(r.taskIds[0]));
  opens.forEach((r) => seenTasks.add(r.taskIds[0]));
  const suggested = suggestedOpenRows(registryIds);
  const pending = pendingPackageRows();
  const scraps = scrapRows().filter((r) => !seenTasks.has(r.taskIds[0]));
  return expandMultiTaskPacks([...packs, ...extras, ...opens, ...suggested, ...pending, ...scraps]).map((r) => ({
    ...r,
    track: trackOf(r.wbs),
    deadline: planDeadline(r.wbs, r.taskId),
  }));
}

export { PHASE, SCRAP, trackOf, WBS_DEADLINE, TASK_DEADLINE };
