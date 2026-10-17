#!/usr/bin/env node
/** P0-15 REWORK：确认「最近评估→恢复结果」在 tech 壳可用 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = { surveyed_at: new Date().toISOString(), purpose: 'P0-15-REWORK-restore-result' };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);

const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}

await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
await page.waitForTimeout(1500);
const restore = page.getByRole('button', { name: /恢复结果|查看结果/ });
out.restore_count = await restore.count();
out.restore_labels = [];
for (let i = 0; i < Math.min(out.restore_count, 5); i++) {
  out.restore_labels.push((await restore.nth(i).innerText().catch(() => '')).trim());
}
out.body_slice = (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 400);

if (out.restore_count >= 1) {
  await restore.first().click({ timeout: 8000 });
  const t0 = Date.now();
  let ok = false;
  while (Date.now() - t0 < 60000) {
    const t = await page.locator('body').innerText().catch(() => '');
    if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) { ok = true; break; }
    await page.waitForTimeout(1000);
  }
  out.after_restore = {
    ok,
    ms: Date.now() - t0,
    url: page.url(),
    has_rank: /技术力加权排名/.test(await page.locator('body').innerText().catch(() => '')),
  };
}

fs.writeFileSync(path.join(__dirname, 'probe-p015-restore.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({ restore_count: out.restore_count, restore_labels: out.restore_labels, after_restore: out.after_restore }, null, 2));
await browser.close();
