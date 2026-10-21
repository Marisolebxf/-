// 一次性只读探针：P0-17 observed 落盘（记录列表行快照 + 切回主 Tab 配置草稿回显）
// 公约：batch32-method-patch §4（独立无头，非 IDE 共享有头；失败落盘后继续不卡死）
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(HERE, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');
const OUT = path.join(HERE, 'scout-p017-observed.json');
const BASE = 'http://10.50.69.111:30892';
const URL0 = BASE + '/service/institution-decision?workspace=cultivate&tab=cultivate';

const browser = await chromium.launch({ headless: true });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
const out = { probed_at: new Date().toISOString(), entry_id: 'svc-rec-cultivate', case: 'P0-17', url: URL0, steps: [] };
try {
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(800);
  if (page.url().includes('/login')) {
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    await page.keyboard.press('Enter'); await page.waitForTimeout(1500);
    if (page.url().includes('/login')) { await page.locator('button[type=submit], button:has-text("登录")').first().click().catch(() => {}); }
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 10000 });
  }
  await page.goto(URL0, { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(2500);
  // 构造与脚本同款非默认草稿（权重 30 / 高校取消 / 中试取消 / 新一代信息技术），验切回保留
  await page.getByRole('button', { name: '恢复默认权重', exact: true }).click().catch(() => {}); await page.waitForTimeout(700);
  const sc = page.locator('[aria-label="现有规模权重"] [role=spinbutton]').first();
  if (await sc.count()) { await sc.click(); await sc.fill('30'); await sc.blur().catch(() => {}); await page.waitForTimeout(700); }
  const sel = page.locator('.industry-catalog-select').first();
  await sel.click({ timeout: 8000 }); await page.waitForTimeout(800);
  await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '新一代信息技术' }).first().click({ timeout: 8000 }); await page.waitForTimeout(1200);
  const g = page.locator('main .arco-checkbox').filter({ hasText: '高校' }).first();
  if ((await g.locator('input').isChecked().catch(() => null)) === true) { await g.click(); await page.waitForTimeout(700); }
  const stageView = page.locator('.arco-select-view-multiple').filter({ hasText: '上游·研发' }).first();
  let stageBefore = '';
  if (await stageView.count()) {
    stageBefore = ((await stageView.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    if (/\+8/.test(stageBefore)) {
      await stageView.click({ timeout: 8000 }); await page.waitForTimeout(900);
      await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '中游·中试' }).first().click({ timeout: 5000 }); await page.waitForTimeout(800);
      await page.keyboard.press('Escape'); await page.waitForTimeout(300);
      stageBefore = ((await stageView.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim();
    }
  }
  // 记录 Tab
  await page.locator('[role=tab][data-tab-key="records"]').first().click({ timeout: 8000 }); await page.waitForTimeout(2500);
  let rows = [];
  const grabRows = async () => {
    const loc = page.locator('tr, [role="row"], .arco-table-tr').filter({ hasText: /SVC-\d{8}-\d+/ });
    const n = Math.min(await loc.count(), 30); const arr = [];
    for (let i = 0; i < n; i++) arr.push((((await loc.nth(i).innerText().catch(() => '')) || '')).replace(/\s+/g, ' ').trim().slice(0, 160));
    return arr;
  };
  rows = await grabRows();
  if (!rows.length) { await page.reload({ waitUntil: 'domcontentloaded' }); await page.waitForTimeout(3000); rows = await grabRows(); }
  const recTab = page.locator('[role=tab][data-tab-key="records"]').first();
  const mainTab = page.locator('[role=tab][data-tab-key="cultivate"]').first();
  out.steps.push({
    step: 'records-tab', rows: rows.length, row_sample: rows.slice(0, 12),
    records_tab_aria_selected: await recTab.getAttribute('aria-selected').catch(() => null),
    main_tab_aria_selected: await mainTab.getAttribute('aria-selected').catch(() => null),
    cluster_select_visible_on_records: await page.locator('.industry-catalog-select').first().isVisible().catch(() => false),
    main_innerText_head: (((await page.locator('main').first().innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 300)),
  });
  // 切回主 Tab
  await mainTab.click({ timeout: 8000 }); await page.waitForTimeout(1800);
  const org = {};
  for (const n of ['高校', '科研院所', '企业']) org[n] = await page.locator('main .arco-checkbox').filter({ hasText: n }).first().locator('input').isChecked().catch(() => null);
  const weights = {};
  for (const n of ['现有规模', '技术创新能力', '服务成效', '市场缺口']) {
    const s = page.locator('[aria-label="' + n + '权重"] [role=spinbutton]').first();
    weights[n] = await s.count() ? String(await s.inputValue().catch(() => '')) : null;
  }
  out.steps.push({
    step: 'back-to-main-tab', url: page.url(),
    industry_echo: ((await sel.locator('.arco-select-view-value').first().innerText().catch(() => '')) || '').trim(),
    org_checked: org,
    stage_view: (await stageView.count()) ? ((await stageView.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim() : null,
    stage_before: stageBefore,
    weights_after_tab_roundtrip: weights,
  });
  // 收尾复位防污染
  await page.getByRole('button', { name: '恢复默认权重', exact: true }).click().catch(() => {}); await page.waitForTimeout(600);
  if (org['高校'] === false) { await g.click().catch(() => {}); await page.waitForTimeout(600); }
  if (/\+7/.test(stageBefore)) {
    await stageView.click({ timeout: 8000 }); await page.waitForTimeout(900);
    await page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option').filter({ hasText: '中游·中试' }).first().click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(700);
    await page.keyboard.press('Escape').catch(() => {});
  }
  out.ok = true;
} catch (e) { out.ok = false; out.err = String(e.message).split('\n')[0]; }
await page.screenshot({ path: path.join(HERE, 'scout-p017-observed.png').replace(/\/[^/]*$/, '/') ? path.join(HERE, 'scout-p017-observed.png') : '' }).catch(() => {});
await browser.close();
fs.writeFileSync(OUT, JSON.stringify(out, null, 2));
console.log('probe done →', OUT, 'ok=' + out.ok, 'err=' + (out.err || ''));
