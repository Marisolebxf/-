/**
 * P0-12（FUNC-00666 时间窗切换刻度同步）一次性无头探针。产物 scout-p012-window.json；勿当 runner。
 * 目标：
 *   1) 结果壳可达 + 诚实空 / 有年序列分支；
 *   2) 时间窗控件形态（radio / select / button）与选项文案（近 N 年）；
 *   3) 切换时间窗后选中态、URL/正文变化、图表/明细是否同步（有序列才深验）。
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
const body0 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
out.honest_empty = /当前结果快照没有年序列/.test(body0);
out.has_trend_title = /服务机构新增数量趋势/.test(body0);
out.body_snip = body0.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 40);

out.time_window = await page.evaluate(() => {
  const main = document.querySelector('main') || document.body;
  const text = (main.innerText || '').replace(/\s+/g, ' ');
  const labels = [];
  const re = /近\s*\d+\s*年/g;
  let m;
  while ((m = re.exec(text))) labels.push(m[0].replace(/\s+/g, ''));
  const uniq = [...new Set(labels)];

  const radioGroup = main.querySelector('.arco-radio-group, [role=radiogroup]');
  const radios = [...main.querySelectorAll('.arco-radio, .arco-radio-button, [role=radio]')]
    .map((el) => {
      const t = (el.innerText || el.textContent || '').trim().replace(/\s+/g, '');
      const checked =
        el.classList.contains('arco-radio-checked') ||
        el.classList.contains('arco-radio-button-checked') ||
        el.getAttribute('aria-checked') === 'true' ||
        !!el.querySelector('input:checked');
      return { text: t, checked, tag: el.tagName, cls: (el.className || '').toString().slice(0, 100) };
    })
    .filter((r) => /近\d+年/.test(r.text));

  const testids = [...main.querySelectorAll('[data-testid*="time"], [data-testid*="range"], [data-testid*="window"], [data-testid*="year"]')]
    .map((el) => ({
      tid: el.getAttribute('data-testid'),
      text: (el.innerText || '').trim().slice(0, 80),
      cls: (el.className || '').toString().slice(0, 80),
    }));

  const board = main.querySelector('[data-testid="svc-org-trend-board"]');
  const boardTime = board
    ? [...board.querySelectorAll('button, .arco-radio, .arco-radio-button, [role=radio], .arco-tag')]
        .map((el) => (el.innerText || '').trim().replace(/\s+/g, ''))
        .filter((t) => /近\d+年/.test(t))
        .slice(0, 12)
    : [];

  return {
    labels_in_text: uniq,
    radio_group: !!radioGroup,
    radios,
    testids,
    board_year_controls: boardTime,
    has_near_3: uniq.includes('近3年') || radios.some((r) => r.text.includes('近3年')),
    has_near_5: uniq.includes('近5年') || radios.some((r) => r.text.includes('近5年')),
    has_near_8: uniq.includes('近8年') || radios.some((r) => r.text.includes('近8年')),
    has_near_10: uniq.includes('近10年') || radios.some((r) => r.text.includes('近10年')),
  };
});

// 尝试点击「近 8 年」或非当前选中项
out.switch = { tried: false };
const candidates = ['近 8 年', '近8年', '近 3 年', '近3年', '近 5 年', '近5年'];
const currentChecked = (out.time_window.radios || []).find((r) => r.checked)?.text || '';
let clickTarget = null;
for (const c of candidates) {
  const norm = c.replace(/\s+/g, '');
  if (currentChecked && currentChecked.replace(/\s+/g, '') === norm) continue;
  const loc = page.getByText(c, { exact: false }).first();
  if (await loc.count()) {
    const vis = await loc.isVisible().catch(() => false);
    if (vis) {
      clickTarget = c;
      break;
    }
  }
}
if (clickTarget) {
  out.switch.tried = true;
  out.switch.target = clickTarget;
  out.switch.before_url = page.url();
  out.switch.before_checked = currentChecked;
  out.switch.before_honest = out.honest_empty;
  const canvasBefore = await page.locator('main canvas, main [_echarts_instance_]').count().catch(() => 0);
  out.switch.canvas_before = canvasBefore;
  try {
    // 优先点 radio-button / 含文案的可点节点
    const btn = page.locator('.arco-radio-button, .arco-radio, button, [role=radio]').filter({ hasText: clickTarget.replace(/\s+/g, ' ') }).first();
    if (await btn.count()) await btn.click({ timeout: 5000 });
    else await page.getByText(clickTarget).first().click({ timeout: 5000 });
    await page.waitForTimeout(1200);
  } catch (e) {
    out.switch.click_error = String(e).slice(0, 200);
  }
  const body1 = ((await page.locator('main').first().innerText().catch(() => '')) || '');
  out.switch.after_url = page.url();
  out.switch.after_honest = /当前结果快照没有年序列/.test(body1);
  out.switch.after_checked = await page.evaluate((want) => {
    const main = document.querySelector('main') || document.body;
    const radios = [...main.querySelectorAll('.arco-radio, .arco-radio-button, [role=radio]')];
    const hit = radios.find((el) => {
      const t = (el.innerText || '').replace(/\s+/g, '');
      return t.includes(want.replace(/\s+/g, ''));
    });
    if (!hit) return null;
    return {
      text: (hit.innerText || '').trim(),
      checked:
        hit.classList.contains('arco-radio-checked') ||
        hit.classList.contains('arco-radio-button-checked') ||
        hit.getAttribute('aria-checked') === 'true' ||
        !!hit.querySelector('input:checked'),
    };
  }, clickTarget);
  out.switch.canvas_after = await page.locator('main canvas, main [_echarts_instance_]').count().catch(() => 0);
  out.switch.detail_empty = /暂无主领域年度明细/.test(body1);
  out.switch.body_has_target = body1.replace(/\s+/g, '').includes(clickTarget.replace(/\s+/g, ''));
}

await page.screenshot({ path: path.join(outDir, 'scout-p012-window.png'), fullPage: false });
out.screenshot = 'fixtures/scout/scout-p012-window.png';

fs.writeFileSync(path.join(outDir, 'scout-p012-window.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
await browser.close();
