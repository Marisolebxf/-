#!/usr/bin/env node
/** 一次性无头探针：登录 → /enterprise/search → dump 对比篮入口 → 点击打开浮层再 dump */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'http://10.50.69.111:30892/';
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const log = [];
const push = (m) => { log.push(m); console.log(m); };

page.on('console', (msg) => {
  if (msg.type() === 'error') push(`[console.error] ${msg.text().slice(0, 200)}`);
});

await page.goto(baseUrl + 'login', { waitUntil: 'domcontentloaded', timeout: 60000 });
push(`after goto login: ${page.url()}`);
await page.waitForTimeout(800);
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
await loginBtn.first().click();
try {
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
  push(`login ok: ${page.url()}`);
} catch (e) {
  push(`login wait failed: ${page.url()} · ${e.message}`);
  await page.screenshot({ path: path.join(outDir, 'probe-login-fail.png'), fullPage: true });
  fs.writeFileSync(path.join(outDir, 'probe-log.txt'), log.join('\n'));
  await browser.close();
  process.exit(1);
}

await page.goto(baseUrl + 'enterprise/search', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
await page.waitForTimeout(3000);
push(`on search: ${page.url()} title=${await page.title()}`);

const entryDump = await page.evaluate(() => {
  const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  const all = [...document.querySelectorAll('button, [role=button], a, [class*=float], [class*=basket], [class*=compare]')];
  const hits = all
    .map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: textOf(el),
      aria: el.getAttribute('aria-label') || '',
      title: el.getAttribute('title') || '',
      class: (typeof el.className === 'string' ? el.className : '').slice(0, 160),
      id: el.id || '',
    }))
    .filter((x) => /对比|篮|compare|basket|共\s*\d+\s*项/i.test(`${x.text} ${x.aria} ${x.title} ${x.class} ${x.id}`));
  const fixed = [...document.querySelectorAll('[style*=fixed], [class*=fixed], [class*=fab], [class*=float]')]
    .slice(0, 30)
    .map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: textOf(el).slice(0, 80),
      class: (typeof el.className === 'string' ? el.className : '').slice(0, 160),
      aria: el.getAttribute('aria-label') || '',
    }));
  return { hits, fixed, bodySample: (document.body.innerText || '').slice(0, 500) };
});
fs.writeFileSync(path.join(outDir, 'probe-entry.json'), JSON.stringify(entryDump, null, 2));
push(`entry hits: ${entryDump.hits.length}`);
entryDump.hits.slice(0, 20).forEach((h) => push(`  HIT: ${h.text || h.aria || h.title} · ${h.class.slice(0, 80)}`));

// try click strategies
const strategies = [
  () => page.getByRole('button', { name: /对比篮|打开对比篮|共\s*\d+\s*项/ }),
  () => page.locator('[aria-label*="对比篮"], [aria-label*="打开对比篮"]'),
  () => page.locator('button, [role=button]').filter({ hasText: /对比篮|共\s*\d+\s*项/ }),
  () => page.locator('[class*=compare], [class*=basket], [class*=CompareBasket]').first(),
];

let opened = false;
for (let i = 0; i < strategies.length; i++) {
  const loc = strategies[i]();
  const n = await loc.count().catch(() => 0);
  push(`strategy ${i}: count=${n}`);
  if (!n) continue;
  try {
    await loc.first().click({ timeout: 5000 });
    await page.waitForTimeout(2000);
    opened = true;
    push(`clicked strategy ${i}`);
    break;
  } catch (e) {
    push(`strategy ${i} click fail: ${e.message.slice(0, 120)}`);
  }
}

const panelDump = await page.evaluate(() => {
  const textOf = (n) => (n.innerText || n.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 100);
  const collect = (sel, limit = 50) =>
    [...document.querySelectorAll(sel)].slice(0, limit).map((el) => ({
      tag: el.tagName.toLowerCase(),
      text: textOf(el),
      attrs: (() => {
        const o = {};
        for (const n of ['id', 'placeholder', 'aria-label', 'role', 'type', 'title']) {
          if (el.getAttribute(n)) o[n] = el.getAttribute(n).slice(0, 120);
        }
        if (el.className && typeof el.className === 'string') o.class = el.className.slice(0, 140);
        return o;
      })(),
    }));
  return {
    url: location.href,
    title: document.title,
    headings: [...document.querySelectorAll('h1,h2,h3,[role=heading]')].slice(0, 40).map(textOf),
    tabs: collect('[role=tab], .arco-tabs-header-title, .arco-tabs-tab'),
    buttons: collect('button, [role=button], .arco-btn'),
    textboxes: collect('input, textarea, [role=textbox], .arco-select-view'),
    checkboxes: collect('[role=checkbox], .arco-checkbox'),
    dialogs: collect('.arco-drawer, .arco-modal, [role=dialog], [class*=Basket], [class*=basket], [class*=compare-panel]'),
    visibleTextHas: {
      企业: !!document.body.innerText.includes('企业'),
      发起分析: !!document.body.innerText.includes('发起分析'),
      清空对比篮: !!document.body.innerText.includes('清空对比篮'),
      去企业查询: !!document.body.innerText.includes('去企业查询'),
      开发中: !!document.body.innerText.includes('开发中'),
    },
  };
});

await page.screenshot({ path: path.join(outDir, 'page-open.png'), fullPage: true });
fs.writeFileSync(path.join(outDir, 'scout-open.json'), JSON.stringify({ opened, surveyed_at: new Date().toISOString(), ...panelDump }, null, 2));

// also write scout.md style summary
const md = [
  `# 对比篮浮层实勘（probe）`,
  ``,
  `- opened: ${opened}`,
  `- url: ${panelDump.url}`,
  `- title: ${panelDump.title}`,
  ``,
  `## headings`,
  ...panelDump.headings.map((h) => `- ${h}`),
  ``,
  `## tabs`,
  ...panelDump.tabs.slice(0, 20).map((t) => `- ${t.text} · ${JSON.stringify(t.attrs)}`),
  ``,
  `## buttons (截断)`,
  ...panelDump.buttons.slice(0, 40).map((b) => `- ${b.text} · ${JSON.stringify(b.attrs)}`),
  ``,
  `## textboxes`,
  ...panelDump.textboxes.slice(0, 20).map((t) => `- ${t.text || t.attrs.placeholder || ''} · ${JSON.stringify(t.attrs)}`),
  ``,
  `## visibleTextHas`,
  JSON.stringify(panelDump.visibleTextHas, null, 2),
].join('\n');
fs.writeFileSync(path.join(outDir, 'scout-open.md'), md);
fs.writeFileSync(path.join(outDir, 'probe-log.txt'), log.join('\n'));
push('done');
await browser.close();
