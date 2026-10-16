#!/usr/bin/env node
/**
 * 无头实勘探针（独立 Chromium，可多进程并行，不抢 IDE 浏览器焦点）。
 * 用法（在 tools/ 目录）：
 *   node survey-page.mjs --path '/enterprise/key-enterprise-analysis?view=domain' --out ../scripts/KJZTFWXT/enterprise/key-domain/fixtures/scout
 *
 * 只做：登录 → goto → 抽控件清单 + 截图 + JSON。禁止当 runner；不写 runs/。
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function arg(name, def) {
  const i = process.argv.indexOf(`--${name}`);
  if (i >= 0 && process.argv[i + 1]) return process.argv[i + 1];
  return def;
}

const baseUrl = (arg('base-url', 'http://111.198.38.90:50892/') || '').replace(/\/?$/, '/');
const pagePath = arg('path', '/');
const user = arg('user', 'admin');
const pass = arg('pass', '123456');
const outDir = path.resolve(__dirname, arg('out', './_scout-out'));
const waitMs = Number(arg('wait-ms', '2500')) || 2500;
const clickName = arg('click', ''); // 可选：进入页后点击该 role/name（如「对比篮」）

fs.mkdirSync(outDir, { recursive: true });

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  const userBox = page.locator('input[placeholder*=用户名], input[type=text]').first();
  const passBox = page.locator('input[type=password]').first();
  await userBox.waitFor({ state: 'visible', timeout: 15000 });
  await passBox.waitFor({ state: 'visible', timeout: 15000 });
  await userBox.fill(user);
  await passBox.fill(pass);
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

const target = new URL(pagePath.replace(/^\//, ''), baseUrl).toString();
// 先显式登录再深链，避免深链 redirect 半屏无 password 超时
await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
await ensureLogin(page);
if (page.url().includes('/login')) {
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
}
await page.waitForTimeout(waitMs);
if (clickName) {
  const loc = page.getByRole('button', { name: new RegExp(clickName) });
  if (await loc.count()) await loc.first().click();
  else await page.getByText(clickName, { exact: false }).first().click();
  await page.waitForTimeout(waitMs);
}

const snapshot = await page.evaluate(() => {
  const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
  const collect = (sel, limit = 40) =>
    [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: textOf(el),
      attrs: (() => {
        const o = {};
        for (const n of ['id', 'name', 'placeholder', 'aria-label', 'role', 'type', 'title']) {
          if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 120);
        }
        if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 120);
        return o;
      })(),
    }));
  return {
    url: location.href,
    title: document.title,
    h1: [...document.querySelectorAll('h1')].map(textOf),
    headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 30).map(textOf),
    buttons: collect('button, [role=button], .arco-btn'),
    textboxes: collect('input, textarea, [role=textbox], .arco-select-view, .arco-input, span.sci-arco-cascader'),
    switches: collect('[role=switch], .arco-switch'),
    menus: collect('[role=menuitem], .arco-menu-item'),
    sections: collect('section, [aria-label]', 25),
  };
});

const shotPath = path.join(outDir, 'page.png');
await page.screenshot({ path: shotPath, fullPage: true });

const out = {
  surveyed_at: new Date().toISOString(),
  base_url: baseUrl,
  path: pagePath,
  headless: true,
  ...snapshot,
  screenshot: path.relative(process.cwd(), shotPath),
};

const jsonPath = path.join(outDir, 'scout.json');
const mdPath = path.join(outDir, 'scout.md');
fs.writeFileSync(jsonPath, JSON.stringify(out, null, 2), 'utf8');
fs.writeFileSync(
  mdPath,
  [
    `# 无头实勘 ${pagePath}`,
    '',
    `- url: ${out.url}`,
    `- title: ${out.title}`,
    `- h1: ${out.h1.join(' | ') || '(无)'}`,
    `- screenshot: page.png`,
    '',
    '## headings',
    ...out.headings.map((t) => `- ${t}`),
    '',
    '## buttons (截断)',
    ...out.buttons.slice(0, 25).map((b) => `- ${b.text || '(无文案)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## textboxes / selects',
    ...out.textboxes.slice(0, 25).map((b) => `- ${b.text || b.attrs.placeholder || '(空)'} · ${JSON.stringify(b.attrs)}`),
    '',
    '## switches',
    ...out.switches.map((b) => `- ${b.text || '(switch)'} · ${JSON.stringify(b.attrs)}`),
  ].join('\n'),
  'utf8',
);

await browser.close();
console.log(`scout ok → ${jsonPath}`);
console.log(`md      → ${mdPath}`);
console.log(`png     → ${shotPath}`);
