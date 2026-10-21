#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-21（FUNC-00704 供给不足判定）。
 * 探：结果态是否出现「该产业服务供给数据不足，暂无法判定」+ 链路图壳保留结构。
 * 公约：独立无头；产物只落本目录；失败落 json 继续；不动业务仓。
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
const ROUTE = '/service/chain-analysis?workspace=chain&tab=chain';
const OUT = {
  probed_at: new Date().toISOString(),
  entry: 'svc-chain-shortboard',
  case: 'P0-21 / FUNC-00704',
  target_copy: '该产业服务供给数据不足，暂无法判定',
  hist: null,
  fresh: null,
};
const dump = () =>
  fs.writeFileSync(path.join(__dirname, '_probe-p021.json'), JSON.stringify(OUT, null, 2), 'utf8');

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
    await close.first().click({ timeout: 1500 }).catch(() => {});
    await page.waitForTimeout(300);
  }
}
async function snapResult(page, label) {
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  const noStages = page.locator('[data-testid="svc-eco-shortboard-no-stages"]');
  const noStagesN = await noStages.count().catch(() => 0);
  const noStagesVis =
    noStagesN > 0 && (await noStages.first().isVisible().catch(() => false));
  const six = ['研发支持', '技术转移与知识产权', '中试与检测', '孵化育成', '产业化推广', '投融资与人才'];
  return {
    label,
    url: page.url(),
    view_result: /view=result/.test(page.url()),
    stations: await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0),
    noStagesN,
    noStagesVis,
    hasDataShort: /该产业服务供给数据不足，暂无法判定/.test(body),
    boardTitle: /全周期服务链路/.test(body),
    metroShell: /地铁轨道图|只画当前结果快照|不补六张空卡|只认 payload/.test(body),
    fakeSix: six.every((n) => body.includes(n)),
    body_head: body.slice(0, 480).replace(/\n+/g, ' | '),
  };
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await ctx.newPage();
try {
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // hist path（P0-06 同款）
  try {
    const rec = page.getByRole('tab', { name: '分析记录', exact: true });
    await rec.click({ timeout: 10000 });
    await page.waitForTimeout(1500);
    const btns = page.getByRole('button', { name: /查看结果/ });
    const n = await btns.count();
    let clicked = false;
    for (let i = 0; i < n; i++) {
      const b = btns.nth(i);
      const dis = await b.isDisabled().catch(() => true);
      const cls = (await b.getAttribute('class').catch(() => '')) || '';
      if (!dis && !/arco-btn-disabled/.test(cls)) {
        await b.click({ timeout: 8000 });
        clicked = true;
        break;
      }
    }
    if (!clicked) {
      OUT.hist = { err: '无可用查看结果', button_count: n };
    } else {
      await page.waitForTimeout(3500);
      if (/view=processing/.test(page.url())) {
        const vr2 = page
          .getByRole('button', { name: /查看结果/ })
          .filter({ hasNot: page.locator('.arco-btn-disabled') })
          .first();
        if (await vr2.count()) {
          await vr2.click({ timeout: 5000 }).catch(() => {});
          await page.waitForTimeout(2500);
        }
      }
      OUT.hist = await snapResult(page, 'hist');
    }
  } catch (e) {
    OUT.hist = { err: String(e).slice(0, 400) };
  }
  dump();

  // fresh path
  try {
    await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    await closeBasket(page);
    const sel = page.locator('.industry-catalog-select').first();
    await sel.click({ timeout: 8000 });
    await page.waitForTimeout(800);
    await page
      .locator(
        '.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option',
      )
      .filter({ hasText: '新一代信息技术' })
      .first()
      .click({ timeout: 8000 });
    await page.waitForTimeout(1500);
    const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (!(await start.count()) || !(await start.isEnabled())) {
      OUT.fresh = { err: '开始分析不可用' };
    } else {
      await start.click({ timeout: 8000 });
      let taskId = null;
      for (let i = 0; i < 15; i++) {
        await page.waitForTimeout(1000);
        const m = /[?&]task_id=(SVC-[0-9-]+)/.exec(page.url());
        if (m) {
          taskId = m[1];
          break;
        }
      }
      if (!taskId) {
        OUT.fresh = { err: '未进任务态', url: page.url() };
      } else {
        let body = '';
        for (let i = 0; i < 20; i++) {
          body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
          if (/分析结果已生成/.test(body)) break;
          await page.waitForTimeout(1000);
        }
        const vr = page
          .getByRole('button', { name: /查看结果/ })
          .filter({ hasNot: page.locator('.arco-btn-disabled') })
          .first();
        if (await vr.count()) {
          await vr.click({ timeout: 8000 });
          await page.waitForTimeout(3000);
        }
        OUT.fresh = { ...(await snapResult(page, 'fresh')), taskId };
      }
    }
  } catch (e) {
    OUT.fresh = { err: String(e).slice(0, 400) };
  }

  const hits = [OUT.hist, OUT.fresh].filter(
    (x) => x && x.view_result && x.hasDataShort && x.boardTitle,
  );
  OUT.verdict = {
    constructable_00704: hits.length > 0,
    structure_ok: hits.some((h) => h.metroShell && !h.fakeSix && h.noStagesVis),
    recommendation: hits.length
      ? 'B档实跑（当前环境即供给不足诚实空；无需 allow_skip）'
      : '若不可达则 B档 allow_skip + ticket；勿假绿',
  };
  dump();
} finally {
  await browser.close();
}
console.log(JSON.stringify(OUT.verdict || OUT, null, 2));
