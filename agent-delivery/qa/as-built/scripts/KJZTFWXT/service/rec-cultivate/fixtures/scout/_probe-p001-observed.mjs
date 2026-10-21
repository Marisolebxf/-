// P0-01（金样重铺·FUNC-01261）无头探针：入口路由可达 + 配置区构成 + 产业集群下拉展开后选项数/清单 + placeholder
// 公约：agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §4（无头探针，不占 IDE 浏览器）
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://10.50.69.111:30892';
const PATH = '/service/institution-decision?workspace=cultivate&tab=cultivate';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080, deviceScaleFactor: 1 } });
const out = { surveyed_at: new Date().toISOString(), probe: '_probe-p001-observed.mjs', base_url: BASE, path: PATH };

try {
  await page.goto(BASE + PATH, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  if (page.url().includes('/login')) {
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1200);
    if (page.url().includes('/login')) {
      await page.locator('button[type=submit], button:has-text("登录"), button:has-text("登 录")').first().click().catch(() => {});
    }
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 10000 });
    await page.goto(BASE + PATH, { waitUntil: 'domcontentloaded' });
  }
  await page.waitForTimeout(2500);

  // 关对比篮（可见才关）
  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }

  out.url = page.url();
  out.title = await page.title();

  // 配置区构成：集群下拉 + Tag 组 + 开始分析按钮
  const main = page.locator('main').first();
  const body = (await main.innerText().catch(() => '')) || '';
  out.config_visible = {
    分析配置: body.includes('分析配置'),
    重点产业方向: body.includes('重点产业方向'),
    机构类型: body.includes('机构类型'),
    服务环节: body.includes('服务环节'),
    开始分析按钮_role: await page.getByRole('button', { name: '开始分析', exact: true }).count(),
    开始分析软文案: /请先确认分析条件，再点击「开始分析」/.test(body),
  };
  const ph = page.getByPlaceholder('选择产业集群');
  out.placeholder_count = await ph.count();
  out.placeholder_visible = await ph.first().isVisible().catch(() => false);

  // 展开下拉（P7：点可见容器）
  const sel = page.locator('.industry-catalog-select').first();
  out.cluster_select_count = await page.locator('.industry-catalog-select').count();
  await sel.click({ timeout: 8000 });
  await page.waitForTimeout(900);
  const opts = page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-select-popup-visible .arco-select-option');
  const texts = (await opts.allTextContents().catch(() => [])).map((t) => t.trim().replace(/\s+/g, ' ')).filter(Boolean);
  out.dropdown_options_raw = texts;
  await page.screenshot({ path: 'scout-p001-observed-options.png', fullPage: false });
  await page.keyboard.press('Escape').catch(() => {});
} catch (e) {
  out.error = String(e).slice(0, 500);
}
await browser.close();
console.log(JSON.stringify(out, null, 2));
