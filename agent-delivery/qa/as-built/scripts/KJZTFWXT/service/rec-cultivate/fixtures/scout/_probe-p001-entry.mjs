// P0-01（FUNC-01260 入口与路由）无头探针：直达路由 + title + 双 Tab
// 公约：agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md §4
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(path.resolve(__dirname, '../../../../../../tools'), 'package.json'));
const { chromium } = require('playwright');

const BASE = 'http://111.198.38.90:50892';
const PATH = '/service/institution-decision?workspace=cultivate&tab=cultivate';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080, deviceScaleFactor: 1 } });
const out = { surveyed_at: new Date().toISOString(), probe: '_probe-p001-entry.mjs', base_url: BASE, path: PATH };

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
  await page.waitForTimeout(2000);

  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
  }

  out.url = page.url();
  out.title = await page.title();
  out.url_has_workspace = /workspace=cultivate/.test(out.url);
  out.url_has_tab = /tab=cultivate/.test(out.url);
  out.url_has_path = /\/service\/institution-decision/.test(out.url);

  const main = page.locator('[role=tab][data-tab-key="cultivate"]');
  const rec = page.locator('[role=tab][data-tab-key="records"]');
  out.tab_main = {
    count: await main.count(),
    visible: await main.first().isVisible().catch(() => false),
    text: (await main.first().innerText().catch(() => '')).trim().replace(/\s+/g, ' '),
    aria_selected: await main.first().getAttribute('aria-selected'),
    class: await main.first().getAttribute('class'),
  };
  out.tab_records = {
    count: await rec.count(),
    visible: await rec.first().isVisible().catch(() => false),
    text: (await rec.first().innerText().catch(() => '')).trim().replace(/\s+/g, ' '),
    aria_selected: await rec.first().getAttribute('aria-selected'),
  };

  // role=tab fallback sample
  const tabs = page.getByRole('tab');
  const n = await tabs.count();
  out.role_tabs = [];
  for (let i = 0; i < Math.min(n, 6); i++) {
    const t = tabs.nth(i);
    out.role_tabs.push({
      text: (await t.innerText().catch(() => '')).trim().replace(/\s+/g, ' ').slice(0, 80),
      aria: await t.getAttribute('aria-selected'),
      data_key: await t.getAttribute('data-tab-key'),
    });
  }

  await page.screenshot({ path: path.join(__dirname, 'scout-p001-entry.png'), fullPage: false });
} catch (e) {
  out.error = String(e).slice(0, 500);
}
await browser.close();
fs.writeFileSync(path.join(__dirname, 'scout-p001-entry.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
