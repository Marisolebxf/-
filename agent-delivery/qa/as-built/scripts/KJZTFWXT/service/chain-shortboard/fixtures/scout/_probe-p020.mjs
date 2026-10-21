#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-20（FUNC-00703 识别结果为空「未发现明显短板」）。
 * 探：经分析记录→查看结果（及可选 fresh）能否出现有环节行且 no-hit 空态。
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
const CLUSTERS = ['新一代信息技术', '新能源'];
const OUT = {
  probed_at: new Date().toISOString(),
  entry: 'svc-chain-shortboard',
  case: 'P0-20 / FUNC-00703',
  target_copy: '当前演示规则下未发现明显短板',
  hist: null,
  clusters: {},
};
const dump = () =>
  fs.writeFileSync(path.join(__dirname, '_probe-p020.json'), JSON.stringify(OUT, null, 2), 'utf8');

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
  return {
    label,
    url: page.url(),
    view_result: /view=result/.test(page.url()),
    stations: await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0),
    noHit: await page.locator('[data-testid="svc-eco-shortboard-no-hit"]').count().catch(() => 0),
    problems: await page.locator('[data-testid="svc-eco-shortboard-problems"]').count().catch(() => 0),
    warnTags: await page
      .locator('.svc-eco-metro-station--blank, .svc-eco-metro-station--weak, .svc-eco-metro-station--bottleneck')
      .count()
      .catch(() => 0),
    hasNoHitCopy: /当前演示规则下未发现明显短板/.test(body),
    hasDataShort: /该产业服务供给数据不足，暂无法判定/.test(body),
    body_head: body.slice(0, 420).replace(/\n+/g, ' | '),
  };
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();
try {
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2500);
  await closeBasket(page);

  // hist path
  try {
    const rec = page.getByRole('tab', { name: '分析记录', exact: true });
    await rec.click({ timeout: 10000 });
    await page.waitForTimeout(1500);
    const viewBtn = page
      .getByRole('button', { name: /查看结果/ })
      .filter({ hasNot: page.locator('.arco-btn-disabled') })
      .first();
    if (!(await viewBtn.count())) {
      OUT.hist = { err: '无可用查看结果' };
    } else {
      await viewBtn.click({ timeout: 8000 });
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
      OUT.hist = await snapResult(page, 'hist-view-result');
      await page.screenshot({ path: path.join(__dirname, 'probe-p020-hist.png') }).catch(() => {});
    }
  } catch (e) {
    OUT.hist = { err: String((e && e.message) || e).slice(0, 400) };
  }
  dump();

  for (const cluster of CLUSTERS) {
    try {
      await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
      await ensureLogin(page);
      await page.waitForTimeout(2000);
      await closeBasket(page);
      if (/view=processing|view=result/.test(page.url())) {
        await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);
      }
      const sel = page.locator('.industry-catalog-select').first();
      await sel.click({ timeout: 8000 });
      await page.waitForTimeout(800);
      await page
        .locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option')
        .filter({ hasText: cluster })
        .first()
        .click({ timeout: 8000 });
      await page.waitForTimeout(1200);
      const start = page.getByRole('button', { name: '开始分析', exact: true }).first();
      if (!(await start.isEnabled())) {
        OUT.clusters[cluster] = { err: '开始分析不可点' };
        dump();
        continue;
      }
      await start.click({ timeout: 8000 });
      let taskId = null;
      for (let i = 0; i < 18; i++) {
        await page.waitForTimeout(1000);
        const m = /[?&]task_id=(SVC-[0-9-]+)/.exec(page.url());
        if (m) {
          taskId = m[1];
          break;
        }
      }
      if (!taskId) {
        OUT.clusters[cluster] = { err: '未进任务态', url: page.url() };
        dump();
        continue;
      }
      for (let i = 0; i < 12; i++) {
        const t = ((await page.locator('main').first().innerText().catch(() => '')) || '');
        if (/分析结果已生成|查看结果/.test(t)) break;
        await page.waitForTimeout(1000);
      }
      const vr = page
        .getByRole('button', { name: /查看结果/ })
        .filter({ hasNot: page.locator('.arco-btn-disabled') })
        .first();
      if (!(await vr.count())) {
        OUT.clusters[cluster] = { err: '引导态无查看结果', taskId };
        dump();
        continue;
      }
      await vr.click({ timeout: 8000 });
      await page.waitForTimeout(3000);
      const snap = await snapResult(page, 'fresh-' + cluster);
      snap.taskId = taskId;
      OUT.clusters[cluster] = snap;
    } catch (e) {
      OUT.clusters[cluster] = { err: String((e && e.message) || e).slice(0, 400) };
    }
    dump();
  }

  const snaps = [OUT.hist, ...Object.values(OUT.clusters)].filter((s) => s && !s.err);
  const anyStations = snaps.some((s) => s.stations > 0);
  const anyNoHit = snaps.some((s) => s.noHit > 0 || s.hasNoHitCopy);
  OUT.verdict = {
    any_stage_rows: anyStations,
    any_no_hit_empty: anyNoHit,
    constructable_00703: anyStations && anyNoHit,
    recommendation: !anyStations
      ? 'B档 allow_skip + D4-SVCSHORT-STAGES-EMPTY（无环节行，不可构造「有行全不命中」）'
      : anyNoHit
        ? '可实跑 no-hit 空态'
        : '有环节行但均命中问题，非 00703 对象；扩探或 keep skip',
  };
} catch (e) {
  OUT.fatal = String((e && e.message) || e).slice(0, 400);
} finally {
  dump();
  await browser.close();
  console.log(JSON.stringify(OUT.verdict || OUT, null, 2));
}
