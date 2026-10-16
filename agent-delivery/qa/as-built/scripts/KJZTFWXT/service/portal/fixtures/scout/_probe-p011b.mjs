#!/usr/bin/env node
/** 探针 b：region-map 接口鉴权/路径核查（对照 curl 401 定位真实 POST 前缀与鉴权要求）。产物 probe-p011b.json */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');
const baseUrl = 'http://111.198.38.90:50892/';
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
const report = {};
try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  // 登录态下取 local token 快照（鉴权头排查）
  report.token_keys = await page.evaluate(() => Object.keys(localStorage));
  report.token_preview = await page.evaluate(() => {
    const out = {};
    for (const k of Object.keys(localStorage)) { const v = String(localStorage.getItem(k) || ''); out[k] = v.length > 40 ? v.slice(0, 40) + '…(' + v.length + ')' : v; }
    return out;
  });

  // 登录态浏览器内 POST region-map（带页面同源 cookie 与可能的自定义头逻辑旁路——仅 fetch 原样）
  const resp = await page.evaluate(async () => {
    const r = await fetch('/svc/topic/v1/service-portal/region-map', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    const text = await r.text();
    return { status: r.status, head: text.slice(0, 200) };
  });
  report.in_page_post = resp;

  // 带 token 头的 POST（页面真实请求如何带鉴权——从 request.ts 逻辑外推，用常见头）
  const tok = await page.evaluate(() => { const v = localStorage.getItem('token') || ''; try { const o = JSON.parse(v); return o.token || o.access_token || v; } catch { return v; } });
  if (tok) {
    const resp2 = await page.evaluate(async (t) => {
      const r = await fetch('/svc/topic/v1/service-portal/region-map', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + t }, body: '{}' });
      const text = await r.text();
      return { status: r.status, head: text.slice(0, 200) };
    }, tok);
    report.in_page_post_bearer = resp2;
  }
  report.overall = 'done';
} catch (err) {
  report.overall = 'error'; report.error = String(err && err.message);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p011b.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
