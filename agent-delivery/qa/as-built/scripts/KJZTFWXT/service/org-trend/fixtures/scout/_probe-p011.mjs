/**
 * P0-11（FUNC-00665 切换领域与对比曲线）一次性无头探针。产物 scout-p011-switch.json；勿当 runner。
 * 目标：
 *   1) 结果壳可达 + 诚实空 / 有年序列分支；
 *   2) 主领域 IndustryCatalogSelect（结果态 context）+ 「重新分析」；
 *   3) 对比领域入口 data-testid=svc-org-trend-compare（placeholder / disabled / 候选数）；
 *   4) 图例区 .svc-org-trend__legend 按钮数与末条 disabled（至少保留一条）。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://111.198.38.90:50892/';
const target = `${baseUrl.replace(/\/?$/, '')}/service/institution-judgment?workspace=trend&tab=trend`;
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
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.waitForTimeout(2000);
await closeBasket(page);

const out = { probed_at: new Date().toISOString(), url_entry: page.url() };

const recTab = page.locator('[role=tab][data-tab-key="records"]');
await recTab.waitFor({ state: 'visible', timeout: 12000 });
await recTab.click({ timeout: 8000 });
await page.waitForTimeout(1500);
const viewBtn = page.getByRole('button', { name: '查看结果' }).first();
await viewBtn.waitFor({ state: 'visible', timeout: 12000 });
await viewBtn.click({ timeout: 8000 });
await page.waitForTimeout(2500);
out.url_result = page.url();
const body = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.honest_empty = /当前结果快照没有年序列/.test(body);
out.has_trend_title = /服务机构新增数量趋势/.test(body);
out.has_reanalyze = await page.getByRole('button', { name: '重新分析' }).count();
out.has_start_on_result = await page.getByRole('button', { name: '开始分析' }).count();
out.has_back_config = await page.getByRole('button', { name: '返回配置' }).count();

out.main_domain_bar = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const ctx = main.querySelector('.svc-org-analysis-context--result') || main.querySelector('.svc-org-analysis-context');
  const label = (ctx?.innerText || '').replace(/\s+/g, ' ').slice(0, 200);
  const select = ctx?.querySelector('.industry-catalog-select, .arco-select');
  const boardLabel = [...main.querySelectorAll('.svc-org-analysis-context__label')]
    .map((el) => (el.textContent || '').trim())
    .filter(Boolean)
    .slice(0, 6);
  return {
    context_text: label,
    has_industry_select: !!select,
    board_labels: boardLabel,
  };
});

const compare = page.locator('[data-testid="svc-org-trend-compare"]');
out.compare = {
  count: await compare.count(),
  visible: await compare.first().isVisible().catch(() => false),
  disabled: await compare.locator('input, .arco-select-view').first().evaluate((el) => {
    const root = el.closest('.arco-select') || el;
    return root.classList.contains('arco-select-disabled') || !!root.getAttribute('disabled');
  }).catch(() => null),
  placeholder: await compare.locator('.arco-select-view-placeholder, input').first().getAttribute('placeholder').catch(async () => {
    return ((await compare.innerText().catch(() => '')) || '').trim().slice(0, 80);
  }),
};

// 尝试打开对比下拉（若未 disabled）
out.compare_open = { tried: false };
if (out.compare.count && out.compare.visible && out.compare.disabled === false) {
  out.compare_open.tried = true;
  try {
    await compare.locator('.arco-select-view').first().click({ timeout: 4000 });
    await page.waitForTimeout(600);
    const opts = page.locator('.arco-trigger-popup:visible .arco-select-option');
    out.compare_open.option_count = await opts.count();
    out.compare_open.options = (await opts.allTextContents()).map((s) => s.trim()).filter(Boolean).slice(0, 10);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
  } catch (e) {
    out.compare_open.error = String(e?.message || e).slice(0, 160);
  }
}

// 尝试切换主领域（结果态 IndustryCatalogSelect）并观察是否需重新分析
out.switch_main = { tried: false };
const industryHost = page.locator('.svc-org-analysis-context--result .industry-catalog-select, .svc-org-analysis-context .industry-catalog-select').first();
if (await industryHost.count()) {
  out.switch_main.tried = true;
  try {
    const before = ((await page.locator('main').first().innerText().catch(() => '')) || '').slice(0, 400);
    out.switch_main.before_main_label = (before.match(/主领域[：:]([^\n]+)/) || [])[1]?.trim()?.slice(0, 40) || null;
    await industryHost.click({ timeout: 5000 });
    await page.waitForTimeout(600);
    const opts = page.locator('.arco-trigger-popup:visible .arco-select-option');
    out.switch_main.option_count = await opts.count();
    const texts = (await opts.allTextContents()).map((s) => s.trim()).filter(Boolean);
    out.switch_main.options_head = texts.slice(0, 5);
    // 选一个与当前不同的选项（若有）
    let picked = null;
    for (const t of texts) {
      if (out.switch_main.before_main_label && t.includes(out.switch_main.before_main_label.replace(/^全部$/, ''))) continue;
      if (t === '全部' || !t) continue;
      picked = t;
      break;
    }
    if (!picked && texts.length) picked = texts.find((t) => t !== '全部') || texts[0];
    if (picked) {
      await opts.filter({ hasText: picked }).first().click({ timeout: 5000 });
      await page.waitForTimeout(800);
      out.switch_main.picked = picked;
      out.switch_main.url_after_pick = page.url();
      out.switch_main.auto_task = /view=processing|task_id=/.test(page.url()) && !/view=result/.test(page.url());
      const afterPick = ((await page.locator('main').first().innerText().catch(() => '')) || '');
      out.switch_main.context_after = (afterPick.match(/主领域[^\n]{0,60}/) || [])[0] || null;
      // 不点重新分析——只记录按钮可达
      const reBtn = page.getByRole('button', { name: '重新分析' }).first();
      out.switch_main.reanalyze_enabled = await reBtn.isEnabled().catch(() => null);
    } else {
      out.switch_main.no_pick = true;
      await page.keyboard.press('Escape').catch(() => {});
    }
  } catch (e) {
    out.switch_main.error = String(e?.message || e).slice(0, 200);
  }
}

out.legend = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const legend = main.querySelector('.svc-org-trend__legend');
  if (!legend) return { present: false, buttons: 0 };
  const btns = [...legend.querySelectorAll('button')].map((b) => ({
    text: (b.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 40),
    disabled: !!b.disabled || b.getAttribute('disabled') != null,
    title: b.getAttribute('title') || '',
    type: b.getAttribute('type') || b.className.slice(0, 60),
  }));
  return { present: true, buttons: btns.length, items: btns.slice(0, 6) };
});

out.limit_note = await page.getByText(/已达上限|最多同时对比|最多 3/).count();
out.board_slice = body.replace(/\s+/g, ' ').slice(0, 500);

await page.screenshot({ path: path.join(outDir, out.honest_empty ? 'scout-p011-empty.png' : 'scout-p011-series.png') });
out.shot = out.honest_empty ? 'scout-p011-empty.png' : 'scout-p011-series.png';

fs.writeFileSync(path.join(outDir, 'scout-p011-switch.json'), JSON.stringify(out, null, 2));
await browser.close();
console.log(JSON.stringify(out, null, 2));
console.log('probe ok →', outDir);
