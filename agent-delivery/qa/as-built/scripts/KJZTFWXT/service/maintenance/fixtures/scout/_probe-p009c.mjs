#!/usr/bin/env node
/**
 * P0-09 补探 C：人设菜单结构 + 精确点 switch（禁误点导航）+ 关评后是否真踢路由。
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
const route = '/service/maintenance';

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
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { probed_at: new Date().toISOString(), steps: [] };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(1500);
  out.steps.push({ id: 'landed', url: page.url() });

  // 开菜单，枚举菜单内元素
  const persona = page.locator('button.persona-switch').first();
  await persona.click({ timeout: 5000 });
  await page.waitForTimeout(700);
  const menuDump = await page.evaluate(() => {
    const menu = document.querySelector('.persona-menu') || document.querySelector('[class*=persona-menu]');
    if (!menu) return { menuFound: false };
    const items = Array.from(menu.querySelectorAll('a, button, [role=switch], [role=menuitem], [role=button], label, div')).slice(0, 40).map((el) => ({
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || '',
      aria: el.getAttribute('aria-label') || '',
      text: ((el.innerText || '') + '').replace(/\s+/g, ' ').trim().slice(0, 60),
      href: el.getAttribute('href') || '',
      checked: el.getAttribute('aria-checked') || '',
      cls: (el.className || '').toString().slice(0, 80),
    }));
    return { menuFound: true, menuText: (menu.innerText || '').replace(/\s+/g, ' ').slice(0, 400), items };
  });
  out.steps.push({ id: 'menu_dump', url: page.url(), ...menuDump });

  // 精确点内部评审 switch（force + 坐标）
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  const box = await sw.boundingBox();
  const before = await sw.getAttribute('aria-checked');
  out.steps.push({ id: 'switch_before', before, box, url: page.url() });

  // 用 mouse 点 switch 中心，避免点到相邻导航
  if (box) {
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
  } else {
    await sw.click({ timeout: 5000, force: true });
  }
  await page.waitForTimeout(1500);
  const afterClick = await sw.getAttribute('aria-checked').catch(() => null);
  out.steps.push({ id: 'after_switch_click', afterClick, url: page.url(), title: await page.title() });

  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(500);
  out.steps.push({ id: 'after_esc', url: page.url(), title: await page.title() });

  // 若仍在 maintenance，reload
  if (/\/service\/maintenance/.test(page.url())) {
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    out.steps.push({ id: 'after_reload_same_route', url: page.url(), title: await page.title() });
  }

  // 无论当前在哪，再深链试 maintenance
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);
  out.steps.push({
    id: 'deeplink_after_off',
    url: page.url(),
    title: await page.title(),
    h1: ((await page.getByRole('heading', { name: '维护管理', level: 1 }).innerText().catch(() => '')) || '').trim(),
  });

  fs.writeFileSync(path.join(__dirname, 'probe-p009c.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
} catch (e) {
  out.error = String(e && e.stack ? e.stack : e);
  fs.writeFileSync(path.join(__dirname, 'probe-p009c.json'), JSON.stringify(out, null, 2));
  console.error(out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
