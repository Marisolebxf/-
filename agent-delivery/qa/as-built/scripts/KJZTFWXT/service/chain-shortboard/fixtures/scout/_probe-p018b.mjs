#!/usr/bin/env node
/**
 * _probe-p018b.mjs — P0-18 落局探针 b（补强 s3：resultData 深挖 stages/gap 环节行）。
 * 复用 _probe-p018.json 里 s1 实测 task_id，只读 GET result（无 POST 副作用）；
 * parse resultData（字符串 JSON）→ 找 stages/gap/links/segments/shortboard/models/items/rows 环节行。
 * 产物合并写 _probe-p018.json 的 s3b 字段（保留原 s1/s2/s3 证据）。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const prev = JSON.parse(fs.readFileSync(path.join(__dirname, '_probe-p018.json'), 'utf8'));
const taskId = prev.s1_fresh_to_result && prev.s1_fresh_to_result.task_id;
if (!taskId) { console.error('no taskId in _probe-p018.json'); process.exit(1); }

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await ctx.newPage();
await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
await page.keyboard.press('Enter');
await page.waitForTimeout(1800);

const out = await page.evaluate(async (tid) => {
  const r = await fetch('/api/topicAsync/topic/v1/analysis/tasks/' + encodeURIComponent(tid) + '/result?user_id=guest');
  const j = await r.json().catch(() => null);
  const t = j && (j.data || j);
  const res = { status: r.status, task_status: t && t.status, stage_rows: [] };
  const rdRaw = t && (t.resultData ?? t.result_data);
  res.resultData_type = rdRaw == null ? 'null' : typeof rdRaw;
  let root = null;
  if (typeof rdRaw === 'string') { try { root = JSON.parse(rdRaw); } catch (e) { res.rd_parse_err = String(e).slice(0, 80); } }
  else if (rdRaw && typeof rdRaw === 'object') root = rdRaw;
  if (root) {
    const d = root.data && typeof root.data === 'object' ? root.data : root;
    res.payload_keys = Object.keys(d).slice(0, 24);
    for (const k of ['stages', 'gap', 'links', 'segments', 'shortboard', 'items', 'rows', 'models']) {
      const v = d[k];
      if (Array.isArray(v) && v.length) res.stage_rows.push({ key: k, len: v.length, sample: JSON.stringify(v[0]).slice(0, 240) });
      else if (v != null) res.stage_rows.push({ key: k, type: Array.isArray(v) ? 'array(' + v.length + ')' : typeof v });
    }
  }
  return res;
}, taskId);

prev.s3b_result_data_deep = { probed_at: new Date().toISOString(), task_id: taskId, ...out };
fs.writeFileSync(path.join(__dirname, '_probe-p018.json'), JSON.stringify(prev, null, 2));
console.log(JSON.stringify(prev.s3b_result_data_deep, null, 2));
await browser.close();
