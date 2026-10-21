#!/usr/bin/env node
/**
 * P0-06（FUNC-01356 备选-占位说明文案语义）写前无头探针。
 * 验证点先验：①说明文案含「当前态」与「交付来源」两要素（机检关键词）；
 * ②全页（主区）无「开发中」笼统文案；③非空白页（壳/标题在）。
 * 附带回读占位区块全文 + E7 README 口径「三组 15 项壳」现场观察（记 observed 不判 Fail）。
 * 禁止当 runner；禁止有头 MCP。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/maintenance';
const outDir = __dirname;

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
  const closeAria = page.locator('[aria-label="关闭对比篮"]');
  if ((await closeAria.count()) && (await closeAria.first().isVisible().catch(() => false))) {
    await closeAria.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

const probe = { probed_at: new Date().toISOString(), entry_id: 'svc-maintenance', case: 'FUNC-01356 / P0-06', steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);
  await closeBasket(page);

  const heading = page.locator('section.diagnosis-page-heading, .diagnosis-page-heading').first();
  const headingText = ((await heading.innerText().catch(() => '')) || '').trim();
  const mainText = ((await page.locator('main').innerText().catch(() => page.locator('body').innerText())) || '');

  // ① 两要素机检关键词：当前态 = 入口已对齐 demo 路由（现状诚实描述）；交付来源 = 后续 US-SVC-* 叶交付
  const stateOk = /入口已对齐\s*demo\s*路由/.test(headingText);
  const sourceOk = /US-SVC-\*?\s*叶?交付|由后续\s*US-SVC/.test(headingText);
  // ② 主区无「开发中」笼统文案（对 previous work：对比篮 tab「区域 · 开发中」在浮层内非主区——本探针关浮层后读 main）
  const vagueDev = /开发中/.test(mainText);
  // ③ 非空白页：H1 + 占位区块 + 业务占位面板
  const h1Ok = (await page.getByRole('heading', { name: '维护管理', level: 1 }).isVisible().catch(() => false));
  const panelOk = (await page.locator('[aria-label="业务占位"], .svc-shell-panel').first().isVisible().catch(() => false));

  probe.steps.push({
    step: 'p006_semantics',
    url: page.url(),
    title: await page.title(),
    headingText,
    mainText_head: mainText.replace(/\s+/g, ' ').slice(0, 400),
    stateOk,
    sourceOk,
    vagueDevInMain: vagueDev,
    h1Ok,
    panelOk,
    // observed：E7 README 口径「复用 ENT-OPS 三组 15 项壳，字段服务机构域」为交付目标态描述；
    // 现场是否出现 15 项分组/分类壳结构（应无——现场为占位壳）
    entOpsShellWordsInMain: /门户内容（产业全景）|产业链实体生命周期|字段指标|模型规则|数据批次|维护工作区/.test(mainText),
  });

  await page.screenshot({ path: path.join(outDir, 'probe-p006.png'), fullPage: false });
  probe.shot = 'probe-p006.png';

  console.log(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p006.json'), JSON.stringify(probe, null, 2));
} catch (e) {
  probe.error = String(e);
  console.error(JSON.stringify(probe, null, 2));
  fs.writeFileSync(path.join(outDir, 'probe-p006.json'), JSON.stringify(probe, null, 2));
  process.exitCode = 1;
} finally {
  await browser.close();
}
