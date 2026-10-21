#!/usr/bin/env node
/**
 * svc-chain-graph 三次探针：
 * A) 后端 500 恢复情况（直接查看结果）
 * B) 「返回配置重新分析」正常态行为
 * C) 失败态：route abort eco-graph 后点「查看结果」
 * D) 侧栏菜单 DOM（menuitem 折叠/展开态）
 * E) 刷新后 radio 模式保留（00709 第3点）
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
const ROUTE = '/service/chain-analysis?workspace=graph&tab=graph';
const OUT = {};
const dump = (n, d) => { fs.writeFileSync(path.join(__dirname, n), JSON.stringify(d, null, 2), 'utf8'); };
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String(e && e.message || e).slice(0, 260) }; } };
async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}
async function closeBasket(page) {
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}
async function mainText(page) { return ((await page.locator('main').first().innerText().catch(() => '')) || ''); }

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // D) 侧栏菜单结构
  OUT.sidebar = await safe(async () => {
    return await page.evaluate(() => {
      const items = [...document.querySelectorAll('[role=menuitem], .arco-menu-item, .arco-menu-inline-header')];
      return items.slice(0, 40).map((e) => ({
        tag: e.tagName, role: e.getAttribute('role'), text: (e.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 30),
        cls: (e.className || '').toString().slice(0, 70), visible: !!(e.offsetWidth || e.offsetHeight),
      }));
    });
  });

  // A) 查看结果（后端 500 是否恢复）
  OUT.view_result_check = await safe(async () => {
    await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    await page.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
    await page.waitForTimeout(4000);
    const body = await mainText(page);
    return {
      url: page.url(),
      has_500: /Request failed|status code 500/.test(body),
      has_shell: /服务生态关系图谱/.test(body),
      has_hang_empty_note: /当前 hang 无可见点边|无可见点边/.test(body),
      trace_btn_visible: await page.getByText('返回配置重新分析').first().isVisible().catch(() => false),
    };
  });

  // B) 返回配置重新分析（正常态）
  OUT.back_normal = await safe(async () => {
    const el = page.getByText('返回配置重新分析').first();
    if (!(await el.isVisible().catch(() => false))) return { err: 'not visible' };
    await el.click({ timeout: 6000 });
    await page.waitForTimeout(2000);
    const url = page.url(); const body = await mainText(page);
    return {
      url, back_ok: !/view=result/.test(url) && /分析配置/.test(body),
      has_500: /Request failed|status code 500/.test(body),
      body_head: body.split('\n').filter(Boolean).slice(0, 16),
    };
  });

  // E) 刷新后模式保留
  OUT.mode_reload = await safe(async () => {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2200);
    await closeBasket(page);
    await page.getByText('② 机构+关联主体', { exact: true }).first().click({ timeout: 6000 });
    await page.waitForTimeout(600);
    const before = await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    const after = await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '');
    return { before: before.trim(), after: after.trim(), kept: before.trim() === after.trim() && /②/.test(after) };
  });

  // C) 失败态构造：abort 后查看结果
  OUT.fail_on_view = await safe(async () => {
    const p2 = await ctx.newPage();
    await p2.route('**/svc/topic/v1/service/eco-graph**', (r) => r.abort());
    await p2.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await p2.waitForTimeout(2500);
    await closeBasket(p2);
    await p2.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
    await p2.waitForTimeout(1500);
    await p2.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
    await p2.waitForTimeout(6000);
    const body = await mainText(p2);
    const r = {
      url: p2.url(),
      fail_words: ['失败', '错误', '异常', '重试', 'Request failed', '网络'].filter((k) => body.includes(k)),
      retry_btn: await p2.getByRole('button', { name: /重试|重新分析/ }).count().catch(() => 0),
      shell_kept: /服务生态关系图谱|双密度并排/.test(body),
      config_kept: /产业领域|图谱滤镜/.test(body),
      body_lines: body.split('\n').filter(Boolean).slice(0, 24),
    };
    await p2.close();
    return r;
  });

  await page.screenshot({ path: path.join(__dirname, 'probe-batch32c-final.png') });
  dump('_probe-batch32c.json', OUT);
  await browser.close();
  console.log('DONE');
})().catch((e) => { dump('_probe-batch32c.json', { fatal: String(e) }); console.error(e); process.exit(1); });
