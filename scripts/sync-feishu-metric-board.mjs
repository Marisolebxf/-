#!/usr/bin/env node
/**
 * sync-feishu-metric-board.mjs —— 飞书「指标与数据开发进度」看板出站同步
 * ---------------------------------------------------------------------------
 * 任务：ORCH-METRIC-BOARD-L01 · 配置：agent-delivery/feishu/feishu-metric-board.yaml
 * 真源：metrics/registry/metric-readiness-matrix-*.yaml（四维）
 *       + metrics/registry/cfg_metric-*-seed.yaml（8 件套）
 *       + agent-handoffs 下各模块 data-gap-catalog.yaml（缺口文案）
 *       + metrics/request 专题系统、展示系统 pages yaml（合同集合推断）
 * 行为：自动建表/建列（单选列带预置选项）→ 按「指标ID」upsert；飞书只读投影，不回写。
 * 用法：node scripts/sync-feishu-metric-board.mjs [--dry-run]
 *       无 FEISHU_APP_ID/SECRET 时软失败（退出码 0）。
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadDotEnv } from './lib/feishu-bitable-config.mjs';
import { feishuTenantToken, feishuApi, listAllBitableRecords, bitableFieldToString } from './lib/feishu-open-api.mjs';
import { a2VerdictsByMetric, loadA2GapItems } from './lib/a2-gap-items.mjs';
import { domainZhOf, DOMAIN_ZH } from './lib/metric-registry-lib.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-metric-board.yaml');
const REGISTRY_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'metrics', 'registry');
const HANDOFFS_DIR = path.join(ORCH_ROOT, 'agent-delivery', 'agent-handoffs');

const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const DEF_ZH = { aligned: '已对齐', draft: '草案', missing: '未登记', unassessed: '待评估' };
const SCHEMA_ZH = { ready: '就绪', partial: '部分', missing: '缺失', pending: '待首评', 'n/a': '不适用', unassessed: '待评估' };
const ASSESSED_ZH = { provisional: '初判', verified: '已核验', none: '—' };
const SOURCE_ZH = { full: '齐备', partial: '部分缺口', none: '无源', pending_ods: '待ODS', 'n/a': '不适用', unassessed: '待评估' };
const INGEST_ZH = { mock: 'Mock', ingesting: '接入中', live: '已接真', 'n/a': '不适用' };
const OVERALL_ZH = {
  unregistered: '未登记',
  no_source: '无数据源',
  pending_definition: '待口径确认',
  pending_algorithm: '待算法实现',
  pending_schema: '待结构设计',
  pending_source: '待数据源',
  mock_waiting: '待接入（Mock）',
  ingesting: '接入中',
  live: '可上线',
};
const OWNER_ZH = {
  unregistered: '口径（淮政玮）',
  no_source: '甲方/数据采购（PM 跟踪）',
  pending_definition: '口径（淮政玮）+ 甲方决策清单',
  pending_algorithm: '算法（唐绍祖）',
  pending_schema: '架构（徐滕强/李伟）',
  pending_source: 'GDF（辜少彬）/ 甲方源侧',
  mock_waiting: '数据工厂（GDF 接入排期）',
  ingesting: '数据工厂（GDF）',
  live: '—',
};
const LIFE_ZH = {
  pre_register: '盘点未注册',
  identified: '已点名',
  open: '定义中',
  formula_signed: '公式已签',
  source_mapped: '源已对',
  kit_complete: '8件套齐',
  retired: '废止',
  unspecified: '未标',
};
const CONTRACT_ZH = { both: 'F∩L', func_only: 'F−L', lib_only: 'L−F', unsorted: '未分拣' };
const ALGO_TYPES = ['STAT', 'COMPUTE', 'MODEL', 'GRAPH', 'API', 'MIXED', 'UNKNOWN'];
const MODEL_TYPES = new Set(['MODEL', 'GRAPH', 'COMPUTE', 'MIXED']);
const STAGE_LABEL = { ods_synced: '源同步', dwd_loaded: 'DWD', es_indexed: 'ES', graph_loaded: '图谱', verified: '核验' };
const STAGE_ZH = { done: '✔', in_progress: '进行中', todo: '未开始', 'n/a': '不适用' };

function loadBoardConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  const get = (key) => (raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm')) || [])[1] || '';
  const fieldNames = {};
  const fnBlock = raw.match(/^field_names:\s*\r?\n((?:[ \t]+.+\r?\n)+)/m);
  if (fnBlock) {
    for (const line of fnBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s+([a-z_]+):\s*"([^"]+)"/);
      if (m) fieldNames[m[1]] = m[2];
    }
  }
  return { raw, appToken: get('app_token'), tableName: get('table_name'), tableId: get('table_id'), fieldNames };
}

function backfillTableId(tableId) {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  if (!/^\s+table_id:\s*""/m.test(raw)) return;
  fs.writeFileSync(CONFIG_PATH, raw.replace(/^(\s+table_id:\s*)""/m, `$1"${tableId}"`), 'utf8');
  console.log(`[config] table_id 已回填：${tableId}`);
}

function splitMetricBlocks(raw) {
  const blocks = [];
  let current = null;
  for (const line of raw.split(/\r?\n/)) {
    if (/^ {2}- metric_id:/.test(line)) {
      if (current) blocks.push(current);
      current = [line];
    } else if (current) {
      if (/^ {2}- /.test(line) || (/^\S/.test(line) && line.trim() !== '')) {
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

function fieldOf(block, key) {
  const m = block.match(new RegExp(`^\\s+${key}:\\s*(.+)$`, 'm'));
  if (!m) return '';
  let v = m[1].trim();
  if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1).replace(/\\"/g, '"');
  if (v.length > 1 && v.startsWith("'") && v.endsWith("'")) return v.slice(1, -1);
  if (v.startsWith('"') || v.startsWith("'")) return v.slice(1);
  const hash = v.indexOf(' #');
  if (hash >= 0) v = v.slice(0, hash).trim();
  return v;
}

function listFilesByGlobSuffix(dir, suffix) {
  const out = [];
  const walk = (d) => {
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, entry.name);
      if (entry.isDirectory()) walk(p);
      else if (entry.name.endsWith(suffix)) out.push(p);
    }
  };
  walk(dir);
  return out;
}

function parseCfgSeeds() {
  const seeds = new Map();
  const files = fs.readdirSync(REGISTRY_DIR).filter((f) => /^cfg_metric-.*-seed\.yaml$/.test(f));
  for (const file of files) {
    const raw = fs.readFileSync(path.join(REGISTRY_DIR, file), 'utf8');
    for (const block of splitMetricBlocks(raw)) {
      const id = fieldOf(block, '- metric_id') || fieldOf(block, 'metric_id');
      if (!id) continue;
      const algo = (fieldOf(block, 'algorithm_type') || 'UNKNOWN').toUpperCase();
      const domainCode = (file.match(/^cfg_metric-(.+)-seed\.yaml$/) || [])[1] || '';
      seeds.set(id, {
        metricId: id,
        name: fieldOf(block, 'metric_name_zh'),
        definition: fieldOf(block, 'definition'),
        updateFreq: fieldOf(block, 'update_freq'),
        mappingStatus: fieldOf(block, 'mapping_status'),
        pendingRef: fieldOf(block, 'pending_ref'),
        acceptanceUnit: fieldOf(block, 'acceptance_unit_id'),
        algorithmType: ALGO_TYPES.includes(algo) ? algo : 'UNKNOWN',
        domainCode,
      });
    }
  }
  return seeds;
}

function parseInlineStageMap(value) {
  const stages = {};
  const inner = value.replace(/^\{|\}$/g, '');
  for (const part of inner.split(',')) {
    const m = part.trim().match(/^([a-z_/]+):\s*(.+)$/);
    if (m) stages[m[1]] = m[2].trim();
  }
  return stages;
}

function parseReadinessMatrices() {
  const readiness = new Map();
  const files = fs.readdirSync(REGISTRY_DIR).filter((f) => /^metric-readiness-matrix-.*\.yaml$/.test(f));
  for (const file of files) {
    const raw = fs.readFileSync(path.join(REGISTRY_DIR, file), 'utf8');
    const headerModule = (raw.match(/^module:\s*(.+)$/m) || [])[1]?.trim() || '';
    for (const block of splitMetricBlocks(raw)) {
      const id = fieldOf(block, '- metric_id') || fieldOf(block, 'metric_id');
      if (!id) continue;
      const stagesRaw = fieldOf(block, 'd4_ingestion_stages');
      const life = fieldOf(block, 'lifecycle_stage') || 'unspecified';
      readiness.set(id, {
        module: fieldOf(block, 'module') || headerModule,
        name: fieldOf(block, 'metric_name_zh'),
        acceptanceUnit: fieldOf(block, 'acceptance_unit_id'),
        defStatus: fieldOf(block, 'd1_def_status'),
        pendingRef: fieldOf(block, 'd1_pending_ref'),
        defNote: fieldOf(block, 'd1_note'),
        schemaStatus: fieldOf(block, 'd2_schema_status'),
        schemaAssessed: fieldOf(block, 'd2_assessed') || 'provisional',
        schemaGap: (block.match(/^\s+gap:\s*"([^"]*)"/m) || [])[1] || '',
        sourceStatus: fieldOf(block, 'd3_source_mapping_status'),
        sourceGap: fieldOf(block, 'd3_gap'),
        ingestionStatus: fieldOf(block, 'd4_ingestion_status'),
        stages: stagesRaw.startsWith('{') ? parseInlineStageMap(stagesRaw) : {},
        lifecycleStage: LIFE_ZH[life] ? life : 'unspecified',
      });
    }
  }
  return readiness;
}

function parseGapCatalogs() {
  const hints = new Map();
  for (const file of listFilesByGlobSuffix(HANDOFFS_DIR, 'data-gap-catalog.yaml')) {
    const raw = fs.readFileSync(file, 'utf8');
    for (const block of splitMetricBlocks(raw)) {
      const id = fieldOf(block, '- metric_id') || fieldOf(block, 'metric_id');
      if (id) hints.set(id, fieldOf(block, 'pending_hint'));
    }
  }
  return hints;
}

function rollupAssessed(r) {
  if (r.defStatus === 'missing') return 'unregistered';
  if (r.sourceStatus === 'none') return 'no_source';
  if (r.defStatus === 'draft') return 'pending_definition';
  if (r.schemaStatus !== 'ready' && r.schemaStatus !== 'n/a') return 'pending_schema';
  if (r.sourceStatus === 'partial' || r.sourceStatus === 'pending_ods') return 'pending_source';
  if (r.ingestionStatus === 'ingesting') return 'ingesting';
  if (r.ingestionStatus === 'live') return 'live';
  return 'mock_waiting';
}

function rollupLegacy(seed) {
  const t = seed?.algorithmType || 'UNKNOWN';
  if (seed?.mappingStatus === '❌') return 'no_source';
  if (seed?.mappingStatus === '⚠️' || seed?.pendingRef) return 'pending_definition';
  if (seed?.mappingStatus === '🔧') {
    if (MODEL_TYPES.has(t)) return 'pending_algorithm';
    if (t === 'UNKNOWN') return 'pending_definition';
    return 'pending_schema'; // STAT / API：不是「待算法实现」
  }
  return 'mock_waiting';
}

function topicOwnerOf(id) {
  if (id.startsWith('M_ENT_') || id.startsWith('M_SYNTH_')) return '徐滕强';
  if (id.startsWith('M_CHAIN_')) return '李伟';
  if (id.startsWith('M_SVC_')) return '侯佳伟';
  if (id.startsWith('M_POLICY_')) return '淮政玮';
  return '—';
}

function contractOf(id, verdicts) {
  const set = verdicts.get(id);
  if (!set || !set.size) return 'unsorted';
  if (set.has('missing')) return 'func_only';
  if (set.has('mapped')) return 'both';
  return 'unsorted';
}

function blockerOwner(overallKey, algoType, topicOwner) {
  if (algoType === 'STAT' && (overallKey === 'pending_schema' || overallKey === 'pending_algorithm')) {
    const who = topicOwner && topicOwner !== '—' ? topicOwner : '模块负责人';
    return `STAT Java（${who}）+ GDF ADS`;
  }
  return OWNER_ZH[overallKey] || '—';
}

function moduleDisplay(id, r) {
  if (r?.module) {
    if (r.module.startsWith('ENT-')) return `E1 企业 · ${r.module.slice(4)}`;
    return r.module;
  }
  if (id.startsWith('M_ENT_')) return 'E1 企业（待四维评估）';
  if (id.startsWith('M_CHAIN_')) return 'E2 产业链（待四维评估）';
  if (id.startsWith('M_SVC_')) return '产业服务（待四维评估）';
  if (id.startsWith('M_POLICY_')) return 'E7 政策（待四维评估）';
  if (id.startsWith('M_SYNTH_')) return '综合（待四维评估）';
  if (id.startsWith('M_TNIE_')) return '科技动态（待四维评估）';
  return '其他';
}

function stagesText(stages) {
  const parts = [];
  for (const [key, label] of Object.entries(STAGE_LABEL)) {
    if (stages[key]) parts.push(`${label}:${STAGE_ZH[stages[key]] ?? stages[key]}`);
  }
  return parts.join(' | ');
}

function buildRows() {
  const seeds = parseCfgSeeds();
  const readiness = parseReadinessMatrices();
  const hints = parseGapCatalogs();
  const a2Items = loadA2GapItems(ORCH_ROOT);
  const verdicts = a2VerdictsByMetric(a2Items);
  const today = new Date().toISOString().slice(0, 10);
  const rows = [];

  const allIds = new Set([...seeds.keys(), ...readiness.keys()]);
  for (const id of allIds) {
    const seed = seeds.get(id);
    const r = readiness.get(id);
    const assessed = Boolean(r);
    const algoType = seed?.algorithmType || 'UNKNOWN';
    const overallKey = assessed ? rollupAssessed(r) : rollupLegacy(seed);
    const defStatus = assessed ? r.defStatus : seed?.pendingRef ? 'draft' : 'aligned';
    const legacySource = !seed ? 'unassessed' : seed.mappingStatus === '❌' ? 'none' : seed.mappingStatus === '✅' ? 'full' : 'unassessed';
    const definition = seed?.definition || r?.defNote || '';
    const sourceGap = (assessed ? r.sourceGap : '') || '';
    const topicOwner = topicOwnerOf(id);

    rows.push({
      metricId: id,
      fieldsZh: {
        metric_name: seed?.name || r?.name || id,
        domain: domainZhOf(seed?.domainCode || r?.module || ''),
        module: moduleDisplay(id, r),
        topic_owner: topicOwner,
        algorithm_type: algoType,
        contract_set: CONTRACT_ZH[contractOf(id, verdicts)],
        lifecycle_stage: LIFE_ZH[assessed ? r.lifecycleStage : 'unspecified'],
        acceptance_unit: seed?.acceptanceUnit || r?.acceptanceUnit || '—',
        readiness_assessed: assessed ? '已评估' : '待评估',
        def_status: DEF_ZH[defStatus] ?? '待评估',
        pending_ref: (assessed ? r.pendingRef : seed?.pendingRef) || '',
        schema_status: SCHEMA_ZH[assessed ? r.schemaStatus : 'unassessed'] ?? '待评估',
        schema_gap: assessed ? r.schemaGap : '',
        schema_assessed: assessed ? (ASSESSED_ZH[r.schemaAssessed] ?? '初判') : '—',
        source_status: SOURCE_ZH[assessed ? r.sourceStatus : legacySource] ?? '待评估',
        source_gap: sourceGap,
        ingestion_status: INGEST_ZH[assessed ? r.ingestionStatus : 'mock'] ?? 'Mock',
        ingestion_stages: assessed ? stagesText(r.stages) : '',
        overall: OVERALL_ZH[overallKey],
        blocker_owner: blockerOwner(overallKey, algoType, topicOwner),
        update_freq: seed?.updateFreq || '',
        definition_summary: definition.length > 120 ? `${definition.slice(0, 120)}…` : definition,
        gap_hint: hints.get(id) || '',
        synced_at: today,
      },
    });
  }
  rows.sort((a, b) =>
    (a.fieldsZh.domain + a.fieldsZh.module + a.metricId).localeCompare(
      b.fieldsZh.domain + b.fieldsZh.module + b.metricId,
      'zh-Hans-CN',
    ),
  );
  return rows;
}

function selectField(name, options) {
  return { field_name: name, type: 3, property: { options: options.map((n) => ({ name: n })) } };
}
function textField(name) {
  return { field_name: name, type: 1 };
}

function fieldDefs(fn, rows) {
  const moduleOptions = [...new Set(rows.map((r) => r.fieldsZh.module))].sort();
  return [
    textField(fn.metric_id),
    textField(fn.metric_name),
    selectField(fn.domain, Object.values(DOMAIN_ZH)),
    selectField(fn.module, moduleOptions),
    selectField(fn.topic_owner, ['徐滕强', '李伟', '侯佳伟', '淮政玮', '未点名', '—']),
    selectField(fn.algorithm_type, ALGO_TYPES),
    selectField(fn.contract_set, Object.values(CONTRACT_ZH)),
    selectField(fn.lifecycle_stage, Object.values(LIFE_ZH)),
    textField(fn.acceptance_unit),
    selectField(fn.readiness_assessed, ['已评估', '待评估']),
    selectField(fn.def_status, Object.values(DEF_ZH)),
    textField(fn.pending_ref),
    selectField(fn.schema_status, Object.values(SCHEMA_ZH)),
    textField(fn.schema_gap),
    selectField(fn.schema_assessed, Object.values(ASSESSED_ZH)),
    selectField(fn.source_status, Object.values(SOURCE_ZH)),
    textField(fn.source_gap),
    selectField(fn.ingestion_status, Object.values(INGEST_ZH)),
    textField(fn.ingestion_stages),
    selectField(fn.overall, Object.values(OVERALL_ZH)),
    textField(fn.blocker_owner),
    textField(fn.update_freq),
    textField(fn.definition_summary),
    textField(fn.gap_hint),
    textField(fn.synced_at),
  ].filter((d) => d.field_name);
}

async function ensureTable(cfg, token, rows) {
  if (cfg.tableId) return cfg.tableId;
  const list = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables?page_size=100`, token);
  const hit = (list.data?.items || []).find((t) => t.name === cfg.tableName);
  if (hit) {
    backfillTableId(hit.table_id);
    return hit.table_id;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] 将创建数据表「${cfg.tableName}」（${fieldDefs(cfg.fieldNames, rows).length} 列）`);
    return '';
  }
  const created = await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables`, token, {
    table: { name: cfg.tableName, default_view_name: '全量总览', fields: fieldDefs(cfg.fieldNames, rows) },
  });
  const tableId = created.data?.table_id;
  if (!tableId) throw new Error('建表失败：无 table_id 返回');
  console.log(`[table] 已创建「${cfg.tableName}」table_id=${tableId}`);
  backfillTableId(tableId);
  return tableId;
}

async function ensureFields(cfg, token, tableId, rows) {
  const data = await feishuApi('GET', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields?page_size=100`, token);
  const existing = new Set((data.data?.items || []).map((f) => f.field_name));
  for (const def of fieldDefs(cfg.fieldNames, rows)) {
    if (existing.has(def.field_name)) continue;
    if (DRY_RUN) {
      console.log(`[dry-run] 将补建列「${def.field_name}」`);
      continue;
    }
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/fields`, token, def);
    console.log(`[field] 已补建列「${def.field_name}」`);
    await sleep(200);
  }
}

async function upsertRows(cfg, token, tableId, rows) {
  const fn = cfg.fieldNames;
  const existing = await listAllBitableRecords({ appToken: cfg.appToken, tableId }, token);
  const byMetricId = new Map();
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.[fn.metric_id]).trim();
    if (id) byMetricId.set(id, rec.record_id);
  }

  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = { [fn.metric_id]: row.metricId };
    for (const [key, value] of Object.entries(row.fieldsZh)) {
      if (fn[key]) fields[fn[key]] = value ?? '';
    }
    const recordId = byMetricId.get(row.metricId);
    if (recordId) toUpdate.push({ record_id: recordId, fields });
    else toCreate.push({ fields });
  }

  console.log(`[plan] 共 ${rows.length} 条：新建 ${toCreate.length}，更新 ${toUpdate.length}`);
  if (DRY_RUN) return;

  for (let i = 0; i < toCreate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_create`, token, {
      records: toCreate.slice(i, i + 100),
    });
    await sleep(200);
  }
  for (let i = 0; i < toUpdate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${cfg.appToken}/tables/${tableId}/records/batch_update`, token, {
      records: toUpdate.slice(i, i + 100),
    });
    await sleep(200);
  }
  console.log('[done] 看板已同步');
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const cfg = loadBoardConfig();
  const rows = buildRows();
  const assessedN = rows.filter((r) => r.fieldsZh.readiness_assessed === '已评估').length;
  const pendingAlgoStat = rows.filter((r) => r.fieldsZh.overall === OVERALL_ZH.pending_algorithm && r.fieldsZh.algorithm_type === 'STAT');
  console.log(`[source] 指标 ${rows.length} 条（四维已评估 ${assessedN} 条；registry=${path.relative(ORCH_ROOT, REGISTRY_DIR)}）`);
  if (pendingAlgoStat.length) {
    console.warn(`[WARN] STAT 误入「待算法实现」${pendingAlgoStat.length} 条（应为 0）`);
  }
  if (!rows.length) throw new Error('未解析到任何指标，请检查 metrics/registry/cfg_metric-*-seed.yaml');
  if (DRY_RUN) {
    for (const id of ['M_ENT_MARKET_SHARE', 'M_ENT_PATENT_GRANT_COUNT', 'M_CHAIN_MARKET_SIZE']) {
      const row = rows.find((r) => r.metricId === id);
      if (row) console.log(`[sample] ${id} → ${JSON.stringify(row.fieldsZh, null, 0)}`);
    }
    const byOverall = {};
    const byAlgo = {};
    const byContract = {};
    for (const r of rows) {
      byOverall[r.fieldsZh.overall] = (byOverall[r.fieldsZh.overall] || 0) + 1;
      byAlgo[r.fieldsZh.algorithm_type] = (byAlgo[r.fieldsZh.algorithm_type] || 0) + 1;
      byContract[r.fieldsZh.contract_set] = (byContract[r.fieldsZh.contract_set] || 0) + 1;
    }
    console.log(`[rollup] overall=${JSON.stringify(byOverall)}`);
    console.log(`[rollup] algorithm_type=${JSON.stringify(byAlgo)}`);
    console.log(`[rollup] contract_set=${JSON.stringify(byContract)}`);
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → 软失败：看板未同步，请在配好 .env 的机器（如投影机）重跑本脚本');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  const tableId = await ensureTable(cfg, token, rows);
  if (!tableId) return;
  await ensureFields(cfg, token, tableId, rows);
  await upsertRows(cfg, token, tableId, rows);
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exitCode = 1;
});
