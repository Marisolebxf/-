#!/usr/bin/env node
/**
 * 把当日 WBS 汇总 xlsx 的指定 sheet 投影到飞书同名表。
 * 按「工作细项任务号」upsert。只写文本列和数字列；单选/多选仅在选项已存在时写入。
 * 不删除已有任务行。删掉该表里没有任务号的空行。
 *
 * 用法：node scripts/sync-feishu-wbs-sheets.mjs [--date YYYY-MM-DD] [--dry-run]
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';
import {
  feishuTenantToken,
  feishuApi,
  listAllBitableRecords,
  bitableFieldToString,
} from './lib/feishu-open-api.mjs';

const APP_TOKEN = 'P0DdbN6Iia3BxXsSusycQCyunIh';
const SHEETS = ['图数据库集成', 'GDF 数据治理集成'];
const DRY_RUN = process.argv.includes('--dry-run');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function resolveDate() {
  const i = process.argv.indexOf('--date');
  if (i >= 0 && process.argv[i + 1]) return process.argv[i + 1];
  const dir = path.join(ORCH_ROOT, 'agent-delivery', '工程过程', '当日进展');
  const files = fs.readdirSync(dir).filter((f) => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort();
  return files[files.length - 1].replace(/\.md$/, '');
}

function readSheet(xlsxPath, sheetName) {
  const code = `
import json, sys, openpyxl
p, sheet = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb[sheet]
headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1, max_col=18))]
rows, carry = [], {}
for raw in ws.iter_rows(min_row=2, max_col=18, values_only=True):
    item = {}
    for i, h in enumerate(headers):
        if not h:
            continue
        v = raw[i]
        if v is None and h in ("工作项", "工作目标", "WBS"):
            v = carry.get(h)
        elif v is not None and h in ("工作项", "工作目标", "WBS"):
            carry[h] = v
        if isinstance(v, str):
            v = v.strip()
        item[h] = v
    if item.get("工作细项任务号"):
        rows.append(item)
json.dump(rows, sys.stdout, ensure_ascii=False)
`;
  const run = spawnSync('python', ['-c', code, xlsxPath, sheetName], {
    encoding: 'utf8',
    maxBuffer: 20 * 1024 * 1024,
  });
  if (run.status !== 0) {
    throw new Error(run.stderr || `读取 sheet 失败：${sheetName}`);
  }
  return JSON.parse(run.stdout);
}

function feishuName(excelName, fieldByName) {
  if (fieldByName.has(excelName)) return excelName;
  const piped = excelName.replaceAll('/', '|');
  if (fieldByName.has(piped)) return piped;
  return '';
}

function assignField(fields, meta, value) {
  if (value === null || value === undefined || value === '') return;
  const text = String(value);
  if (meta.type === 1) {
    fields[meta.field_name] = text;
    return;
  }
  if (meta.type === 2) {
    const n = Number(value);
    if (!Number.isNaN(n)) fields[meta.field_name] = n;
    return;
  }
  const options = new Set((meta.property?.options || []).map((o) => o.name));
  if (!options.has(text)) return;
  if (meta.type === 3) fields[meta.field_name] = text;
  if (meta.type === 4) fields[meta.field_name] = [text];
}

async function pushSheet(token, table, rows) {
  const fieldData = await feishuApi(
    'GET',
    `/bitable/v1/apps/${APP_TOKEN}/tables/${table.table_id}/fields?page_size=100`,
    token,
  );
  const metas = fieldData.data?.items || [];
  const fieldByName = new Map(metas.map((f) => [f.field_name, f]));
  const idMeta = fieldByName.get('工作细项任务号');
  if (!idMeta) throw new Error(`${table.name} 没有「工作细项任务号」列`);

  const existing = await listAllBitableRecords({ appToken: APP_TOKEN, tableId: table.table_id }, token);
  const byId = new Map();
  const emptyIds = [];
  for (const rec of existing) {
    const id = bitableFieldToString(rec.fields?.['工作细项任务号']).trim();
    if (id) byId.set(id, rec.record_id);
    else emptyIds.push(rec.record_id);
  }

  const toCreate = [];
  const toUpdate = [];
  for (const row of rows) {
    const fields = {};
    for (const [excelName, value] of Object.entries(row)) {
      const name = feishuName(excelName, fieldByName);
      if (!name) continue;
      assignField(fields, fieldByName.get(name), value);
    }
    const id = String(row['工作细项任务号']).trim();
    const rid = byId.get(id);
    if (rid) toUpdate.push({ record_id: rid, fields });
    else toCreate.push({ fields });
  }

  console.log(
    `[wbs] ${table.name} 工作簿 ${rows.length} 行：新建 ${toCreate.length}，更新 ${toUpdate.length}，空行 ${emptyIds.length}`,
  );
  if (DRY_RUN) return;

  for (let i = 0; i < toCreate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${APP_TOKEN}/tables/${table.table_id}/records/batch_create`, token, {
      records: toCreate.slice(i, i + 100),
    });
    await sleep(200);
  }
  for (let i = 0; i < toUpdate.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${APP_TOKEN}/tables/${table.table_id}/records/batch_update`, token, {
      records: toUpdate.slice(i, i + 100),
    });
    await sleep(200);
  }
  for (let i = 0; i < emptyIds.length; i += 100) {
    await feishuApi('POST', `/bitable/v1/apps/${APP_TOKEN}/tables/${table.table_id}/records/batch_delete`, token, {
      records: emptyIds.slice(i, i + 100),
    });
    await sleep(200);
  }
}

export async function pushNamedWbsSheets(token, date) {
  const xlsxPath = path.join(ORCH_ROOT, 'agent-delivery', '工程过程', '当日进展', `WBS汇总-${date}.xlsx`);
  if (!fs.existsSync(xlsxPath)) {
    console.warn(`[WARN] 没有 ${xlsxPath}，WBS 分表未投影`);
    return;
  }
  const list = await feishuApi('GET', `/bitable/v1/apps/${APP_TOKEN}/tables?page_size=100`, token);
  const tables = list.data?.items || [];
  for (const name of SHEETS) {
    const table = tables.find((t) => t.name === name);
    if (!table) {
      console.warn(`[WARN] 飞书没有表「${name}」`);
      continue;
    }
    const rows = readSheet(xlsxPath, name);
    await pushSheet(token, table, rows);
  }
}

async function main() {
  loadDotEnv(ORCH_ROOT);
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    console.warn('[WARN] FEISHU_APP_ID/SECRET 缺失 → WBS 分表未投影');
    return;
  }
  const token = await feishuTenantToken(appId, appSecret);
  await pushNamedWbsSheets(token, resolveDate());
  console.log('[done] WBS 分表已投影');
}

const isDirect = process.argv[1] && process.argv[1].endsWith('sync-feishu-wbs-sheets.mjs');
if (isDirect) {
  main().catch((err) => {
    console.error(`[ERROR] ${err.message}`);
    process.exitCode = 1;
  });
}
