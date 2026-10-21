#!/usr/bin/env node
/**
 * svc-chain-graph 批次补齐二次探针（遗留点）：
 * A) 返回配置重新分析 的标签/角色与行为
 * B) 结果态大画布（非 icon svg）zoom/pan transform
 * C) 工作区切换草稿保留二次验证（选产业→验证→切→回→验证）
 * D) abort 构造失败态（同 context 免二次登录）
 * E) 当天同条件复用（选产业点开始分析看是否直接 view=result）
 * F) 密度悬停 tooltip
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
const safe = async (fn) => { try { return await fn(); } catch (e) { return { err: String(e && e.message || e).slice(0, 300) }; } };

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

async function pickIndustry(page, name) {
  const sel = page.locator('main .industry-catalog-select').first();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(700);
  const opt = page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: name }).first();
  await opt.click({ timeout: 8000 });
  await page.waitForTimeout(900);
  const val = await sel.locator('.arco-select-view-value').first().innerText().catch(() => '');
  return val.trim();
}

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

  // —— 进结果态（历史查看结果）——
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  await page.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(3500);

  // A) 返回配置重新分析：标签与行为
  OUT.back_btn = await safe(async () => {
    const hit = page.getByText('返回配置重新分析').first();
    const vis = await hit.isVisible();
    const info = await hit.evaluate((e) => {
      let n = e; const chain = [];
      for (let i = 0; i < 4 && n; i++, n = n.parentElement) chain.push(n.tagName + '|' + ((n.className || '').toString().slice(0, 50)));
      return { tag: e.tagName, role: e.getAttribute('role'), chain, clickable: !!e.closest('button, a, [role=button], .arco-btn') };
    });
    return { visible: vis, info };
  });
  OUT.back_action = await safe(async () => {
    const el = page.locator('button:has-text("返回配置重新分析"), a:has-text("返回配置重新分析"), [role=button]:has-text("返回配置重新分析")').first();
    if (!(await el.count())) { // fallback 点文本
      await page.getByText('返回配置重新分析').first().click({ timeout: 6000 });
    } else { await el.click({ timeout: 6000 }); }
    await page.waitForTimeout(1800);
    const url = page.url(); const body = await mainText(page);
    return { url, back_to_config: !/view=result/.test(url) && /分析配置|图谱滤镜/.test(body), body_head: body.slice(0, 200) };
  });

  // 重新进结果态做 B/F
  await page.getByRole('tab', { name: '分析记录', exact: true }).click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  await page.getByRole('button', { name: /查看结果/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(3000);

  // B) 大画布 zoom/pan：找 width>400 的 svg
  OUT.canvas = await safe(async () => {
    const bigs = await page.locator('main svg').evaluateAll((els) => els.map((e) => {
      const r = e.getBoundingClientRect();
      return { cls: (e.getAttribute('class') || '').slice(0, 60), w: Math.round(r.width), h: Math.round(r.height), vb: e.getAttribute('viewBox') };
    }).filter((x) => x.w > 400));
    if (!bigs.length) return { big_svgs: [], note: 'no big svg' };
    // 选第一个大 svg 做交互
    const svgEl = (await page.locator('main svg').all()).find(async () => false);
    const loc = page.locator('main svg').filter({ has: page.locator('g') }).nth(1);
    // 直接用 evaluate 找
    const handle = await page.evaluateHandle(() => {
      const els = [...document.querySelectorAll('main svg')];
      const big = els.find((e) => e.getBoundingClientRect().width > 400);
      return big || null;
    });
    if (!handle.asElement()) return { big_svgs: bigs, note: 'no element handle' };
    const el = handle.asElement();
    const box = await el.boundingBox();
    const readT = async () => await el.evaluate((n) => {
      const g = n.querySelector('g[transform]');
      return g ? g.getAttribute('transform') : null;
    });
    const t0 = await readT();
    const cx = box.x + box.width / 2, cy = box.y + box.height / 2;
    await page.mouse.move(cx, cy); await page.mouse.wheel(0, -300); await page.waitForTimeout(700);
    const t1 = await readT();
    await page.mouse.move(cx, cy); await page.mouse.down();
    await page.mouse.move(cx - 200, cy - 140, { steps: 10 }); await page.mouse.up();
    await page.waitForTimeout(700);
    const t2 = await readT();
    return { big_svgs: bigs.slice(0, 5), box: { x: Math.round(box.x), y: Math.round(box.y), w: Math.round(box.width), h: Math.round(box.height) }, t0, t1_zoom: t1, t2_pan: t2, zoom_moved: t0 !== t1, pan_moved: t1 !== t2 };
  });

  // F) 密度悬停
  OUT.density_hover = await safe(async () => {
    const dens = page.locator('main').getByText('机构子网密度').first();
    await dens.hover({ timeout: 5000 });
    await page.waitForTimeout(900);
    const tip = await page.locator('.arco-tooltip, [role=tooltip]').allInnerTexts().catch(() => []);
    return { tooltips: tip.map((t) => t.trim().slice(0, 120)).filter(Boolean) };
  });

  // C) 工作区切换草稿保留（二次验证）
  OUT.workspace_keep2 = await safe(async () => {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2200);
    await closeBasket(page);
    const picked = await pickIndustry(page, '新能源');
    const modeBefore = await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '');
    const menuStep = async (label) => {
      const m = page.getByRole('menuitem', { name: new RegExp(label) }).first();
      await m.click({ timeout: 8000 });
      await page.waitForTimeout(1800);
    };
    await menuStep('服务链短板分析');
    const chainUrl = page.url();
    await menuStep('服务链图谱分析');
    await page.waitForTimeout(1200);
    const selVal = await page.locator('main .industry-catalog-select .arco-select-view-value').first().innerText().catch(() => '');
    const modeAfter = await page.locator('main .arco-radio.arco-radio-checked').first().innerText().catch(() => '');
    const soft = /请先确认分析条件/.test(await mainText(page));
    return { picked_before_switch: picked, mode_before: modeBefore.trim(), chain_url: chainUrl, sel_after_back: selVal.trim(), mode_after: modeAfter.trim(), soft_gate_after: soft };
  });

  // E) 当天同条件复用：选「新一代信息技术」点开始分析
  OUT.reuse_today = await safe(async () => {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2200);
    await closeBasket(page);
    await pickIndustry(page, '新一代信息技术');
    await page.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 8000 });
    let url = ''; let body = '';
    for (let i = 0; i < 12; i++) {
      await page.waitForTimeout(1000);
      url = page.url(); body = await mainText(page);
      if (/view=result|view=processing/.test(url)) break;
    }
    return { url, in_result: /view=result/.test(url), in_processing: /view=processing/.test(url), has_result_headings: /服务生态关系图谱/.test(body), body_head: body.slice(0, 220) };
  });

  // D) abort 失败态（新 page 同 context，无需再登录）
  OUT.fail_state = await safe(async () => {
    const p2 = await ctx.newPage();
    await p2.route('**/svc/topic/v1/service/eco-graph**', (r) => r.abort());
    await p2.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await p2.waitForTimeout(2500);
    await closeBasket(p2);
    await pickIndustry(p2, '新一代信息技术');
    await p2.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 8000 });
    await p2.waitForTimeout(10000);
    const body = await mainText(p2);
    const retry = await p2.getByRole('button', { name: /重试|重新分析/ }).count().catch(() => 0);
    const anyRetryText = /重试|失败|错误|异常/.test(body);
    const r = { url: p2.url(), fail_words: ['失败', '错误', '异常', '重试'].filter((k) => body.includes(k)), retry_btn_role: retry, anyRetryText, body_slice: body.split('\n').filter(Boolean).slice(0, 30) };
    await p2.close();
    return r;
  });

  await page.screenshot({ path: path.join(__dirname, 'probe-batch32b-final.png') });
  dump('_probe-batch32b.json', OUT);
  await browser.close();
  console.log('DONE');
})().catch((e) => { dump('_probe-batch32b.json', { fatal: String(e) }); console.error(e); process.exit(1); });
