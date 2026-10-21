#!/usr/bin/env node
/**
 * 一次性无头探针 · svc-chain-shortboard P0-19（FUNC-00702 环节供给诚实空态「暂无供给机构」）。
 * 探：能否构造含无在库机构（count=0）环节的产业集群；现场是否出现「暂无供给机构」文案。
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
const CLUSTERS = ['新一代信息技术', '未来健康', '海洋'];
const OUT = {
  probed_at: new Date().toISOString(),
  entry: 'svc-chain-shortboard',
  case: 'P0-19 / FUNC-00702',
  clusters: {},
};
const dump = () =>
  fs.writeFileSync(path.join(__dirname, '_probe-p019.json'), JSON.stringify(OUT, null, 2), 'utf8');
const safe = async (fn) => {
  try {
    return await fn();
  } catch (e) {
    return { err: String((e && e.message) || e).slice(0, 300) };
  }
};
const mainText = async (page) => ((await page.locator('main').first().innerText().catch(() => '')) || '');

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

async function freshToResult(page, cluster) {
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
  if (!(await start.isEnabled())) return { err: '开始分析不可点', cluster };
  await start.click({ timeout: 8000 });
  const pollTask = async (ms) => {
    for (let i = 0; i < Math.ceil(ms / 1000); i++) {
      await page.waitForTimeout(1000);
      const u = page.url();
      if (/view=processing|view=result/.test(u)) {
        const m = /[?&]task_id=(SVC-[0-9-]+)/.exec(u);
        if (m) return m[1];
      }
    }
    return null;
  };
  let taskId = await pollTask(12000);
  if (!taskId) {
    const s2 = page.getByRole('button', { name: '开始分析', exact: true }).first();
    if (
      (await s2.count()) &&
      (await s2.isVisible().catch(() => false)) &&
      (await s2.isEnabled().catch(() => false)) &&
      !/[?&]view=/.test(page.url())
    ) {
      await s2.click({ timeout: 8000 });
      taskId = await pollTask(12000);
    }
  }
  if (!taskId) return { err: '未进任务态', cluster, url: page.url() };
  for (let i = 0; i < 10; i++) {
    if (/分析结果已生成/.test(await mainText(page))) break;
    await page.waitForTimeout(1000);
  }
  const vr = page
    .getByRole('button', { name: /查看结果/ })
    .filter({ hasNot: page.locator('.arco-btn-disabled') })
    .first();
  if (!(await vr.count())) return { err: '无查看结果', cluster, taskId };
  await vr.click({ timeout: 8000 });
  await page.waitForTimeout(3000);
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
  const body = await mainText(page);
  const stations = await page.locator('[data-stage-id], .svc-eco-metro-station').count().catch(() => 0);
  const blankStations = await page.locator('.svc-eco-metro-station--blank').count().catch(() => 0);
  const zeroOrgText = await page.locator('.svc-eco-metro-station').filter({ hasText: /机构\s*0\s*家/ }).count().catch(() => 0);
  return {
    cluster,
    taskId,
    url: page.url(),
    view_result: /view=result/.test(page.url()),
    stations,
    blankStations,
    zeroOrgText,
    has_case_copy_暂无供给机构: /暂无供给机构/.test(body),
    has_asbuilt_机构0家: /机构\s*0\s*家/.test(body),
    has_honest_empty: /该产业服务供给数据不足，暂无法判定/.test(body),
    has_no_fake_zero_note: /不把 count=0 写成短板|不补固定六卡|不补六张空卡/.test(body),
    body_head: body.slice(0, 420).replace(/\n+/g, ' | '),
  };
}

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();
await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
await ensureLogin(page);

for (const c of CLUSTERS) {
  OUT.clusters[c] = await safe(() => freshToResult(page, c));
  dump();
}

const anyStations = Object.values(OUT.clusters).some((r) => r && r.stations > 0);
const anyZeroOrg = Object.values(OUT.clusters).some(
  (r) => r && (r.blankStations > 0 || r.zeroOrgText > 0 || r.has_asbuilt_机构0家),
);
const anyCaseCopy = Object.values(OUT.clusters).some((r) => r && r.has_case_copy_暂无供给机构);
OUT.verdict = {
  constructable_zero_org_stage: anyZeroOrg,
  any_stage_rows: anyStations,
  case_copy_暂无供给机构_seen: anyCaseCopy,
  recommendation: !anyStations
    ? 'B档 allow_skip + ticket D4-SVCSHORT-STAGES-EMPTY（无环节行，不可构造无在库机构环节）'
    : anyZeroOrg
      ? '可实跑：有 blank/机构0家 环节；用例文案「暂无供给机构」现场未见则跟 as-built「机构 0 家」+服务空白（D1）'
      : '有环节行但无 count=0：仍不可构造 00702 前置，keep allow_skip 或扩探产业',
};
await page.screenshot({ path: path.join(__dirname, 'probe-p019-last.png') }).catch(() => {});
dump();
await browser.close();
console.log(JSON.stringify(OUT.verdict, null, 2));
