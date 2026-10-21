#!/usr/bin/env node
/**
 * svc-chain-graph 批次补齐一次性无头探针（P0-06~P0-25 写前实勘）。
 * 只读探测 + 少量真实交互（评审开关/切Tab/查看结果/侧栏切换/abort构造失败），产物落本目录。
 * 公约：无头；禁硬点 disabled；单点失败落 json 继续。
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

async function mainText(page) {
  return ((await page.locator('main').first().innerText().catch(() => '')) || '');
}

// —— 评审模式开关探测 ——
async function reviewSwitchProbe(page) {
  const r = { switch_present: false, opened_via: null, review_on: false };
  const sw = page.locator('[aria-label="内部评审模式"]').first();
  if (await sw.isVisible().catch(() => false)) { r.switch_present = true; r.opened_via = 'already-visible'; }
  if (!r.switch_present) {
    const cands = [
      ['persona-class', () => page.locator('[class*="persona" i]').first()],
      ['avatar', () => page.locator('.arco-avatar, header img[class*="avatar" i], [class*="user-info" i]').first()],
      ['admin-btn', () => page.getByRole('button', { name: /admin|管理员|人设/i }).first()],
    ];
    for (const [tag, loc] of cands) {
      const ok = await safe(async () => {
        const el = loc();
        await el.click({ timeout: 2500 });
        await page.waitForTimeout(800);
        return await sw.isVisible();
      });
      if (ok === true) { r.switch_present = true; r.opened_via = tag; break; }
    }
  }
  if (r.switch_present) {
    r.switch_html = await safe(async () => {
      const el = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
      const t = el.count() ? el.first() : sw;
      return ((await t.first().getAttribute('class')) || '') + ' | checked=' + (await t.first().getAttribute('aria-checked'));
    });
    r.review_on = /arco-switch-checked|aria-checked="true"/.test(String(r.switch_html));
  }
  return r;
}

async function setReview(page, on) {
  const sw = page.locator('[aria-label="内部评审模式"]').first();
  if (!(await sw.isVisible().catch(() => false))) return { ok: false, why: 'switch-not-visible' };
  const holder = sw.locator('xpath=ancestor-or-self::*[contains(@class,"arco-switch")][1]');
  const target = (await holder.count()) ? holder.first() : sw;
  const before = /checked/.test((await target.getAttribute('class')) || '');
  if (before !== on) {
    await target.click({ timeout: 3000 });
    await page.waitForTimeout(800);
  }
  const after = /checked/.test((await target.getAttribute('class')) || '');
  return { ok: after === on, before, after };
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

  // 1) 评审开关探测（当前态）
  OUT.review_probe = await safe(async () => await reviewSwitchProbe(page));

  // 2) 评审开启态：追溯按钮
  OUT.trace_buttons_on = await safe(async () => {
    const p = await reviewSwitchProbe(page);
    if (!p.review_on) { const s = await setReview(page, true); await page.waitForTimeout(800); }
    const body = await mainText(page);
    const btns = await page.locator('button, [role="button"], a').evaluateAll((els) =>
      els.map((e) => ({ tag: e.tagName, text: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 40), cls: (e.className || '').toString().slice(0, 80) }))
        .filter((x) => /追溯/.test(x.text + x.cls)).slice(0, 20)
    );
    return { review_on_now: p.review_on, btns, has_text_trace_in_body: /需求追溯/.test(body) };
  });

  // 3) 关评审 → 刷新 → 泄漏扫描
  OUT.leak_after_off = await safe(async () => {
    const s = await setReview(page, false);
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(500);
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    await closeBasket(page);
    const body = await mainText(page);
    const leaks = ['需求追溯', 'metric_id', 'GAP-', 'Q062', '评审'].filter((k) => body.includes(k));
    const swNow = await page.locator('[aria-label="内部评审模式"]').first().isVisible().catch(() => false);
    return { setResult: s, leaks_in_main: leaks, switch_visible_after_reload: swNow, body_head: body.slice(0, 400) };
  });

  // 4) 切 records → 查看结果 → 结果态详勘
  OUT.result_state = await safe(async () => {
    // 先重开评审（回到勘察常态）再进结果
    await reviewSwitchProbe(page);
    await setReview(page, true).catch(() => {});
    const rec = page.getByRole('tab', { name: '分析记录', exact: true });
    await rec.click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    const listText = await mainText(page);
    const viewBtn = page.getByRole('button', { name: /查看结果/ }).first();
    await viewBtn.click({ timeout: 8000 });
    await page.waitForTimeout(3500);
    const url = page.url();

    // 图例/过滤器探测
    const legend = {};
    for (const k of ['投资', '合作', '竞争', '人才流动', '企业', '高校', '资本', '机构', '聚焦']) {
      legend[k] = await safe(async () => {
        const hit = page.locator('main').getByText(k, { exact: false }).first();
        const vis = await hit.isVisible().catch(() => false);
        if (!vis) return { visible: false };
        const chain = await hit.evaluate((e) => {
          const a = []; let n = e;
          for (let i = 0; i < 6 && n; i++, n = n.parentElement) a.push(n.tagName + '.' + ((n.className && n.className.baseVal !== undefined ? n.className.baseVal : n.className) || '').toString().slice(0, 60));
          return a.join(' < ');
        });
        return { visible: true, ancestors: chain };
      });
    }

    // checkbox / switch / tag 类过滤器控件
    const filterControls = await safe(async () => await page.locator('main .arco-checkbox, main .arco-switch, main .arco-radio, main .arco-tag, main .arco-select').evaluateAll((els) =>
      els.slice(0, 40).map((e) => ({ tag: e.tagName, cls: (e.className || '').toString().slice(0, 60), text: (e.innerText || '').trim().slice(0, 40) }))
    ));

    // 画布探测：svg 容器 + wheel/drag transform
    const canvasProbe = await safe(async () => {
      const firstSvg = page.locator('main svg').first();
      const box = await firstSvg.boundingBox();
      const before = await firstSvg.evaluate((e) => {
        const g = e.querySelector('g[transform], g');
        return { svg_cls: e.getAttribute('class') || '', parent_cls: (e.parentElement && e.parentElement.className || '').toString().slice(0, 60), g_transform: g ? g.getAttribute('transform') : null, viewBox: e.getAttribute('viewBox') };
      });
      const cx = (box && box.x + box.width / 2) || 960, cy = (box && box.y + box.height / 2) || 500;
      await page.mouse.move(cx, cy);
      await page.mouse.wheel(0, -240);
      await page.waitForTimeout(600);
      const afterWheel = await firstSvg.evaluate((e) => { const g = e.querySelector('g[transform], g'); return g ? g.getAttribute('transform') : null; });
      await page.mouse.move(cx, cy);
      await page.mouse.down();
      await page.mouse.move(cx - 180, cy - 120, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(600);
      const afterDrag = await firstSvg.evaluate((e) => { const g = e.querySelector('g[transform], g'); return g ? g.getAttribute('transform') : null; });
      return { box, before, afterWheel, afterDrag, zoom_moved: before.g_transform !== afterWheel, pan_moved: afterWheel !== afterDrag };
    });

    // 影响力红问号
    const influence = await safe(async () => {
      const sec = page.locator('main').getByText('生态影响力').first();
      const parent = sec.locator('xpath=ancestor::div[3]');
      const txt = await parent.innerText().catch(() => '');
      const qBtns = await parent.locator('[class*="question" i], [class*="missing" i], [aria-label*="?"], .arco-icon-question-circle').count().catch(() => 0);
      return { section_text: txt.slice(0, 200), question_icon_count: qBtns };
    });

    // 返回配置重新分析
    const backBtn = await safe(async () => {
      const b = page.getByRole('button', { name: /返回配置重新分析/ }).first();
      const vis = await b.isVisible().catch(() => false);
      return { visible: vis };
    });

    const fullText = await mainText(page);
    return {
      url, legend, filterControls, canvasProbe, influence, backBtn,
      headings_present: ['服务生态关系图谱', '双密度并排', '网络统计', '规模与密度', '度中心性 TOP5', '生态影响力'].filter((h) => fullText.includes(h)),
      records_list_head: listText.slice(0, 500),
    };
  });

  // 5) 返回配置重新分析 行为
  OUT.back_to_config = await safe(async () => {
    const b = page.getByRole('button', { name: /返回配置重新分析/ }).first();
    if (!(await b.count())) return { err: 'no back btn' };
    await b.click({ timeout: 6000 });
    await page.waitForTimeout(1500);
    const url = page.url();
    const body = await mainText(page);
    return { url, has_config: /分析配置/.test(body), has_processing: /view=processing/.test(url), body_head: body.slice(0, 300) };
  });

  // 6) org 无效参数
  OUT.org_invalid = await safe(async () => {
    await page.goto(BASE + '/service/chain-analysis?workspace=graph&tab=records&view=result&demo_state=result&task_id=SVC-20260903-001&org=NONEXIST-XYZ-999', { waitUntil: 'domcontentloaded' });
    await ensureLogin(page);
    await page.waitForTimeout(3000);
    await closeBasket(page);
    const body = await mainText(page);
    const drawer = await page.locator('.arco-drawer:visible').count().catch(() => 0);
    const url = page.url();
    return { url, org_kept: /org=/.test(url), drawer_open: drawer, hint: ['机构不存在', '不存在', '无效'].filter((k) => body.includes(k)), body_head: body.slice(0, 300) };
  });

  // 7) 工作区切换（chain→shenzhen→graph）
  OUT.workspace_switch = await safe(async () => {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await ensureLogin(page);
    await page.waitForTimeout(2500);
    // 先选产业制造草稿
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 6000 });
    await page.waitForTimeout(600);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新能源' }).first().click({ timeout: 6000 });
    await page.waitForTimeout(800);
    const step = async (menuText) => {
      const m = page.getByRole('menuitem', { name: new RegExp(menuText) }).first();
      let ok = await m.isVisible().catch(() => false);
      if (!ok) {
        const alt = page.locator(`aside, nav, .arco-menu`).getByText(menuText, { exact: false }).first();
        ok = await alt.isVisible().catch(() => false);
        if (ok) { await alt.click({ timeout: 5000 }); }
      } else { await m.click({ timeout: 5000 }); }
      await page.waitForTimeout(1800);
      const body = await mainText(page);
      return { clicked: menuText, url: page.url(), has_graph_result: /服务生态关系图谱|双密度并排/.test(body), title_like: body.split('\n').slice(0, 8).join(' | ').slice(0, 200) };
    };
    const chain = await step('服务链短板分析');
    const sz = await step('深圳服务链现状');
    const back = await step('服务链图谱分析');
    const bodyAfter = await mainText(page);
    const selVal = await safe(async () => {
      const s2 = page.locator('.industry-catalog-select .arco-select-view-value').first();
      return (await s2.innerText().catch(() => '')) || '';
    });
    return { chain, sz, back, cluster_kept: selVal, url_final: page.url(), body_head: bodyAfter.slice(0, 300) };
  });

  // 8) abort 构造失败态
  OUT.fail_state = await safe(async () => {
    const page2 = await ctx.newPage();
    await page2.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
    await ensureLogin(page2);
    await page2.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await ensureLogin(page2);
    await page2.waitForTimeout(2500);
    await closeBasket(page2);
    await page2.route('**/svc/topic/v1/service/eco-graph**', (r) => r.abort());
    const sel = page2.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 6000 });
    await page2.waitForTimeout(600);
    await page2.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 6000 });
    await page2.waitForTimeout(800);
    await page2.getByRole('button', { name: '开始分析', exact: true }).first().click({ timeout: 6000 });
    await page2.waitForTimeout(9000);
    const body = await mainText(page2);
    const retry = await page2.getByRole('button', { name: /重试|重新分析/ }).count().catch(() => 0);
    const r = { url: page2.url(), has_fail_text: ['失败', '错误', '异常', '重试'].filter((k) => body.includes(k)), retry_btn: retry, body_head: body.slice(0, 400) };
    await page2.close();
    return r;
  });

  await page.screenshot({ path: path.join(__dirname, 'probe-batch32-final.png') });
  dump('_probe-batch32.json', OUT);
  await browser.close();
  console.log('DONE ->', path.join(__dirname, '_probe-batch32.json'));
})().catch((e) => { dump('_probe-batch32.json', { fatal: String(e) }); console.error(e); process.exit(1); });
