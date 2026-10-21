#!/usr/bin/env node
/**
 * P0-19 补探：经「分析记录→查看结果」进结果态（不依赖 fresh POST），核环节行 / 暂无供给机构 / 机构0家。
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
const OUT = { probed_at: new Date().toISOString(), case: 'P0-19b / FUNC-00702 via records' };
const dump = () =>
  fs.writeFileSync(path.join(__dirname, '_probe-p019b.json'), JSON.stringify(OUT, null, 2), 'utf8');

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();
try {
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.goto(BASE + ROUTE, { waitUntil: 'domcontentloaded' });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click({ timeout: 1500 }).catch(() => {});
  }
  const rec = page.getByRole('tab', { name: '分析记录', exact: true });
  await rec.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const viewBtn = page
    .getByRole('button', { name: /查看结果/ })
    .filter({ hasNot: page.locator('.arco-btn-disabled') })
    .first();
  OUT.has_view_result = (await viewBtn.count()) > 0;
  if (!OUT.has_view_result) throw new Error('无可用查看结果');
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
  const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  OUT.url = page.url();
  OUT.view_result = /view=result/.test(page.url());
  OUT.stations = await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0);
  OUT.blankStations = await page.locator('.svc-eco-metro-station--blank').count().catch(() => 0);
  OUT.zeroOrgCards = await page
    .locator('.svc-eco-metro-station')
    .filter({ hasText: /机构\s*0\s*家/ })
    .count()
    .catch(() => 0);
  OUT.has_case_copy = /暂无供给机构/.test(body);
  OUT.has_机构0家 = /机构\s*0\s*家/.test(body);
  OUT.has_honest_empty = /该产业服务供给数据不足，暂无法判定/.test(body);
  OUT.has_no_fake_note = /不把 count=0 写成短板|不补固定六卡|不补六张空卡/.test(body);
  OUT.body_head = body.slice(0, 500).replace(/\n+/g, ' | ');
  await page.screenshot({ path: path.join(__dirname, 'probe-p019b-result.png') });
  OUT.verdict = {
    constructable_zero_org_stage: OUT.blankStations > 0 || OUT.zeroOrgCards > 0 || OUT.has_机构0家,
    any_stage_rows: OUT.stations > 0,
    case_copy_seen: OUT.has_case_copy,
    recommendation:
      OUT.stations < 1
        ? 'B档 allow_skip + D4-SVCSHORT-STAGES-EMPTY'
        : OUT.blankStations > 0 || OUT.zeroOrgCards > 0
          ? '可实跑 as-built 机构0家/blank'
          : '有环节行无 count=0，扩探或 keep skip',
  };
} catch (e) {
  OUT.err = String((e && e.message) || e).slice(0, 400);
}
dump();
await browser.close();
console.log(JSON.stringify(OUT.verdict || OUT, null, 2));
