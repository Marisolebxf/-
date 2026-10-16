#!/usr/bin/env node
/**
 * 一次性无头探针（P0-07 写稿用）：对比篮三入口与带入交互。
 * ① 三入口（去检索加入对比篮/管理对比篮/从对比篮带入）可见性 + DOM 形态；
 * ② 对比对象区基线（当前几家、机构名）；③ 带入一家 → 对象区回显；重复带入行为；
 * ④ 对象区移除按钮 → 移除仅作用本次（篮不消失），还原基线。
 * 产物落 scout-p007.json + scout-p007-*.png；勿当 runner。不点「开始评估」，不改篮内勾选（只读篮浮层文本）。
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
const target = `${baseUrl}service/institution-judgment?workspace=capability&tab=capability`;
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

const out = { probed_at: new Date().toISOString(), path: '/service/institution-judgment?workspace=capability&tab=capability', steps: {} };
const dump = () => fs.writeFileSync(path.join(outDir, 'scout-p007.json'), JSON.stringify(out, null, 2));

try {
  await page.goto(`${baseUrl}login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.waitForTimeout(2000);
  await closeBasket(page);
  await page.waitForTimeout(800);

  // ① 三入口形态：文本按钮 role/aria/class + 可见性 + DOM 存在性
  const entryProbe = await page.evaluate(() => {
    const names = ['去检索加入对比篮', '管理对比篮', '从对比篮带入'];
    const all = Array.from(document.querySelectorAll('main button, main a, main [role=button]'));
    const btns = all.map((b) => ({ text: (b.innerText || '').replace(/\s+/g, ' ').trim(), aria: b.getAttribute('aria-label') || '', cls: String(b.className || '').slice(0, 90), disabled: !!b.disabled, visible: !!(b.offsetWidth || b.offsetHeight) }));
    const hits = {};
    for (const n of names) hits[n] = btns.filter((b) => b.text.includes(n) || b.aria.includes(n));
    // 含篮/检索/带入关键词的全部按钮（防文案变体）
    const kw = btns.filter((b) => /对比篮|检索|带入|管理/.test(b.text + b.aria));
    return { hits, kw: kw.slice(0, 20) };
  });
  out.steps.entries = entryProbe;
  await page.screenshot({ path: path.join(outDir, 'scout-p007-entries.png') });
  dump();

  // ② 对比对象区基线：含「对比机构」文案 + 对象行
  const baseText = await page.locator('main').first().innerText();
  out.steps.baseline = {
    countLine: (baseText.match(/对比机构（[^\n）]*）[^\n]*/) || [''])[0],
    bodyHead: baseText.replace(/\s+/g, ' ').slice(0, 700),
    startDisabled: await (async () => { const b = page.getByRole('button', { name: '开始评估' }); return (await b.count()) ? await b.first().isDisabled().catch(() => 'n/a') : 'no-btn'; })(),
  };
  dump();

  // ③ 带入：点「从对比篮带入」→ 弹层形态（条目名/勾选态/确认钮）
  const importBtn = page.getByRole('button', { name: '从对比篮带入' }).first();
  const importAlt = page.getByText('从对比篮带入', { exact: true }).first();
  const t3 = (await importBtn.count()) ? importBtn : importAlt;
  await t3.click({ timeout: 5000 });
  await page.waitForTimeout(1200);
  const modal = await page.evaluate(() => {
    const ov = document.querySelector('.arco-modal:not([style*="display: none"]), .arco-drawer:not([style*="display: none"]), [role=dialog]');
    if (!ov) return { found: false, text: '' };
    const rows = Array.from(ov.querySelectorAll('label, .arco-checkbox, [role=checkbox], li, tr')).map((r) => ({ text: (r.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 60), cls: String(r.className || '').slice(0, 60) })).filter((r) => r.text);
    const checks = Array.from(ov.querySelectorAll('input[type=checkbox]')).map((c) => ({ checked: c.checked, disabled: c.disabled, aria: c.getAttribute('aria-label') || '' }));
    const btns = Array.from(ov.querySelectorAll('button')).map((b) => ({ text: (b.innerText || '').trim(), disabled: !!b.disabled }));
    return { found: true, text: (ov.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 900), rows: rows.slice(0, 24), checks: checks.slice(0, 20), btns: btns.slice(0, 12) };
  });
  out.steps.importModal = modal;
  await page.screenshot({ path: path.join(outDir, 'scout-p007-modal.png') });
  dump();

  // ④ 勾选一家未带入的机构 → 确认 → 对象区回显
  if (modal.found) {
    const cbs = modal.checks || [];
    const uncheckedIdx = cbs.findIndex((c) => !c.checked && !c.disabled);
    out.steps.pick = { uncheckedIdx, totalChecks: cbs.length };
    if (uncheckedIdx >= 0) {
      const box = page.locator('.arco-modal input[type=checkbox], [role=dialog] input[type=checkbox]').nth(uncheckedIdx);
      const boxVisible = await box.first().isVisible().catch(() => false);
      if (boxVisible) { await box.first().click({ force: true, timeout: 4000 }); }
      else { // input 隐藏（Arco checkbox 自闸）：点可见容器
        const wrap = page.locator('.arco-modal .arco-checkbox, [role=dialog] .arco-checkbox').nth(uncheckedIdx);
        await wrap.click({ timeout: 4000 });
      }
      await page.waitForTimeout(500);
      const confirm = page.locator('.arco-modal button, [role=dialog] button').filter({ hasText: /确定|导入|带入|加入/ }).first();
      if (await confirm.count()) { await confirm.click({ timeout: 4000 }); }
      else await page.keyboard.press('Escape');
      await page.waitForTimeout(1500);
      const afterText = await page.locator('main').first().innerText();
      out.steps.afterImport = {
        countLine: (afterText.match(/对比机构（[^\n）]*）[^\n]*/) || [''])[0],
        startDisabled: await (async () => { const b = page.getByRole('button', { name: '开始评估' }); return (await b.count()) ? await b.first().isDisabled().catch(() => 'n/a') : 'no-btn'; })(),
        bodyHead: afterText.replace(/\s+/g, ' ').slice(0, 700),
      };
      await page.screenshot({ path: path.join(outDir, 'scout-p007-after-import.png') });
    }
  }
  dump();

  // ⑤ 对象区形态：找移除按钮（行内 icon/删除）
  const objZone = await page.evaluate(() => {
    const m = document.querySelector('main');
    if (!m) return null;
    const zone = Array.from(m.querySelectorAll('section, div')).find((d) => /对比机构（/.test(d.innerText || '') && d.querySelectorAll('button, .arco-icon').length > 0 && d.innerText.length < 900);
    if (!zone) return { found: false };
    const btns = Array.from(zone.querySelectorAll('button, .arco-icon-hover, [role=button], .arco-icon')).map((b) => ({ tag: b.tagName, aria: b.getAttribute('aria-label') || '', cls: String(b.className && b.className.baseVal !== undefined ? b.className.baseVal : b.className || '').slice(0, 70), text: (b.innerText || '').trim().slice(0, 20) }));
    return { found: true, zoneCls: String(zone.className || '').slice(0, 90), btns: btns.slice(0, 16), text: (zone.innerText || '').replace(/\s+/g, ' ').slice(0, 400) };
  });
  out.steps.objectZone = objZone;
  dump();

  // ⑥ 还原：如带入成功（count 变 2 或对象区新增行），点移除钮还原 0；校验基线文案
  const after = out.steps.afterImport;
  if (after && after.countLine && after.countLine !== out.steps.baseline.countLine) {
    const rm = page.locator('.svc-org-cap-obj button, .svc-org-cap-obj .arco-icon-hover, main section button, main .arco-icon-close, main .arco-icon-delete').filter({ hasNot: page.locator('xpath=self::*[contains(text(),"开始")]') });
    // 直接找对象区行内 close/delete 图标
    const rmIcon = page.locator('.arco-icon-close, .arco-icon-delete').first();
    if (await rmIcon.count()) {
      await rmIcon.click({ force: true, timeout: 4000 }).catch(() => {});
      await page.waitForTimeout(1000);
    } else {
      const anyBtn = page.locator('main button').filter({ hasText: /^移除$|^删除$/ }).first();
      if (await anyBtn.count()) await anyBtn.click({ timeout: 4000 }).catch(() => {});
      await page.waitForTimeout(1000);
    }
    const restText = await page.locator('main').first().innerText();
    out.steps.restored = {
      countLine: (restText.match(/对比机构（[^\n）]*）[^\n]*/) || [''])[0],
      equalBaseline: (restText.match(/对比机构（[^\n）]*）[^\n]*/) || [''])[0] === out.steps.baseline.countLine,
      startDisabled: await (async () => { const b = page.getByRole('button', { name: '开始评估' }); return (await b.count()) ? await b.first().isDisabled().catch(() => 'n/a') : 'no-btn'; })(),
    };
    await page.screenshot({ path: path.join(outDir, 'scout-p007-restored.png') });
  }
  dump();

  console.log('probe ok');
  console.log(JSON.stringify(out.steps, null, 2).slice(0, 5000));
} catch (e) {
  out.error = String(e).slice(0, 400);
  dump();
  console.error('probe fail:', out.error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
