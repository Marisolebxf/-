#!/usr/bin/env node
/**
 * 一次性无头实勘 · P0-006 机构集合操作（加选/取消/移除）。产物落同目录；勿当 runner。
 * 只读行为勘察：不判验收，observed 记录现场事实。
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const baseUrl = 'http://10.50.69.111:30892/';
const route = '/service/institution-judgment?workspace=field&tab=coverage';
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

async function freshGoto(page) {
  await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  if (page.url().includes('/login')) {
    await ensureLogin(page);
    await page.goto(new URL(route.replace(/^\//, ''), baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await page.waitForTimeout(2000);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(400);
  }
}

async function openModal(page) {
  await page.getByRole('button', { name: '选择机构' }).first().click({ timeout: 8000 });
  const dialog = page.locator('.arco-modal:visible').filter({ hasText: '选择服务机构' }).first();
  await dialog.waitFor({ state: 'visible', timeout: 8000 });
  await page.waitForTimeout(600);
  return dialog;
}

function chipSnapshot(page) {
  return page.evaluate(() => {
    const main = document.querySelector('main');
    if (!main) return null;
    const text = main.innerText || '';
    const m = text.match(/已选机构（(\d+)\s*家）/);
    // 芯片 = 有直接文本节点且内容为 18+ 位大写字母/数字编码的可见元素（Arco tag 内含 icon 子节点，不能只看叶子）
    const codes = Array.from(main.querySelectorAll('*'))
      .filter((el) => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return false;
        return Array.from(el.childNodes).some((n) => n.nodeType === 3 && /^[0-9A-Z]{18,}$/.test(n.textContent.trim()));
      })
      .map((el) => ({ code: el.textContent.trim().slice(0, 24), cls: String(el.className).slice(0, 80) }))
      .slice(0, 20);
    return { count: m ? Number(m[1]) : null, codes, url: location.href };
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
const out = { surveyed_at: new Date().toISOString(), stages: {} };

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await freshGoto(page);

  // 阶段1：选第 1 家 → 回显 1 家；抓已选条目区 DOM（含移除控件）
  let dialog = await openModal(page);
  const checks = dialog.locator('.arco-checkbox:not(.arco-checkbox-disabled)');
  await checks.first().click({ timeout: 5000 });
  await page.waitForTimeout(300);
  await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const s1 = await chipSnapshot(page);
  const selAreaHtml = await page.evaluate(() => {
    const el = Array.from(document.querySelectorAll('main *')).find((n) => n.children.length === 0 && /已选机构（/.test(n.textContent || ''));
    if (!el) return null;
    let p = el.parentElement;
    for (let i = 0; i < 1 && p?.parentElement && p.parentElement.textContent.includes('已选机构'); i++) p = p.parentElement;
    return (p.outerHTML || '').slice(0, 4000);
  });
  await page.screenshot({ path: path.join(outDir, 'p006-after-1st.png') });
  out.stages.firstSelect = { snapshot: s1, selectedAreaHtml: selAreaHtml };
  if (!s1 || s1.count !== 1) throw new Error('首选回显异常: ' + JSON.stringify(s1));

  // 阶段2：再开弹窗加选另一家 → 回显 2 家、不重复；记录弹窗按钮组
  dialog = await openModal(page);
  const footerBtns = await dialog.locator('.arco-modal-footer button, .arco-modal-footer-plain button').allInnerTexts().catch(() => []);
  const checkedNow = dialog.locator('.arco-checkbox.arco-checkbox-checked:not(.arco-checkbox-disabled)');
  const checkedN = await checkedNow.count();
  const unchecked = dialog.locator('.arco-checkbox:not(.arco-checkbox-checked):not(.arco-checkbox-disabled)');
  if (!(await unchecked.count())) throw new Error('弹窗无可加选 checkbox');
  await unchecked.first().click({ timeout: 5000 });
  await page.waitForTimeout(300);
  await dialog.getByRole('button', { name: '确定', exact: true }).last().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  const s2 = await chipSnapshot(page);
  const dup = s2.codes.length !== new Set(s2.codes.map((c) => c.code)).size;
  await page.screenshot({ path: path.join(outDir, 'p006-after-2nd.png') });
  out.stages.addMore = { footerBtns, checkedBeforeAdd: checkedN, snapshot: s2, duplicates: dup };
  if (s2.count !== 2) throw new Error('加选后条数异常: ' + JSON.stringify(s2));

  // 阶段3：再开弹窗直接取消 → 集合不变；弹窗容器自 DOM 卸载（聚焦探针已验证口径）
  dialog = await openModal(page);
  await dialog.screenshot({ path: path.join(outDir, 'p006-modal-reopen.png') }).catch(() => {});
  const cancelLoc = dialog.locator('.arco-modal-footer button:visible').filter({ hasText: /^取消$/ });
  if (!(await cancelLoc.count())) throw new Error('弹窗 footer 无取消按钮');
  await cancelLoc.first().click({ timeout: 8000 });
  await page.waitForTimeout(1200);
  // X2：Arco 关闭后 container 卸载；用 container 计数做关闭证据（比 isVisible 强）
  const containerGone = await page.evaluate(() => !document.querySelector('.arco-modal-container'));
  const s3 = await chipSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'p006-after-cancel.png') });
  out.stages.cancel = {
    containerGone,
    snapshot: s3,
    unchanged: s3.count === 2 && JSON.stringify(s3.codes) === JSON.stringify(s2.codes),
  };
  if (!containerGone) throw new Error('取消后弹窗容器未卸载');
  if (s3.count !== 2) throw new Error('取消后集合被改: ' + JSON.stringify(s3));

  // 阶段4：点第 1 个已选条目的移除控件 → 回显 1 家
  const removeCandidates = await page.evaluate(() => {
    const main = document.querySelector('main');
    const label = Array.from(main.querySelectorAll('*')).find((n) => n.children.length === 0 && /已选机构（/.test(n.textContent || ''));
    // 已选区 = 从「已选机构（N 家）」标签向下、含机构芯片的容器
    let zone = label;
    for (let i = 0; i < 3 && zone?.parentElement; i++) {
      zone = zone.parentElement;
      if (/91440|MA[0-9A-Z]/.test(zone.textContent || '') && (zone.querySelectorAll('button, .arco-icon-close').length || 0) > 0) break;
    }
    const scope = zone || main;
    return {
      zoneCls: String(zone?.className || '').slice(0, 120),
      zoneHtml: (zone?.outerHTML || '').slice(0, 2500),
      hits: Array.from(scope.querySelectorAll('button, .arco-icon-close, [role=button]')).map((n) => {
        const r = n.getBoundingClientRect();
        return {
          tag: n.tagName,
          aria: n.getAttribute('aria-label'),
          text: (n.textContent || '').trim().slice(0, 20),
          cls: String(n.className).slice(0, 100),
          visible: r.width > 0 && r.height > 0,
        };
      }),
    };
  });
  const rm = page.locator('main button[aria-label="移除"]').first();
  const rmCount = await rm.count();
  let removedVia = 'button[aria-label=移除]';
  let target = rmCount ? rm : null;
  if (!target) {
    const fb = page.locator('main .arco-icon-close:visible');
    if (await fb.count()) {
      removedVia = '.arco-icon-close fallback';
      target = fb.first();
    }
  }
  if (!target) throw new Error('未找到已选条目移除控件: ' + JSON.stringify(removeCandidates.hits));
  // 弹窗若未关闭（拦截点击），先 Esc 再重试（公约 P4/探针公约：挡点击先 Esc）
  await target.click({ timeout: 8000 }).catch(async () => {
    await page.keyboard.press('Escape').catch(() => {});
    await page.waitForTimeout(500);
    await target.click({ timeout: 8000 });
  });
  await page.waitForTimeout(1200);
  const s4 = await chipSnapshot(page);
  await page.screenshot({ path: path.join(outDir, 'p006-after-remove.png') });
  out.stages.removeOne = { removeCandidates, removedVia, snapshot: s4, ok: s4.count === 1 };

  const stageOk = out.stages.cancel.unchanged && !out.stages.addMore.duplicates && out.stages.removeOne.ok;
  out.overall = stageOk ? 'pass' : 'observe';
  fs.writeFileSync(path.join(outDir, 'scout-p006.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ overall: out.overall, counts: [s1.count, s2.count, s3.count, s4.count], removedVia }, null, 2));
} catch (e) {
  out.overall = 'error';
  out.error = String(e).slice(0, 600);
  fs.writeFileSync(path.join(outDir, 'scout-p006.json'), JSON.stringify(out, null, 2));
  console.error(e);
  process.exitCode = 1;
} finally {
  await browser.close();
}
