#!/usr/bin/env node
/**
 * P0-17 无头实勘：加入企业 → 切访客只读 VISIT → 开对比篮 → 勾选 → 发起分析
 * 观察评估类任务是否保留+置灰+说明权限原因（FUNC-00510）
 * 产物：p0-17-recon.json + p0-17-*.png
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
const out = { surveyed_at: new Date().toISOString(), steps: [] };
const push = (m, extra) => {
  const row = { t: new Date().toISOString(), m, ...(extra || {}) };
  out.steps.push(row);
  console.log(m, extra ? JSON.stringify(extra).slice(0, 240) : '');
};

async function ensureLogin(page) {
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const btn = page.getByRole('button', { name: /登录/ });
  if (await btn.count()) await btn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
}

async function switchVisit(page) {
  const menu = page.locator('.persona-menu');
  if (!(await menu.count()) || !(await menu.first().isVisible().catch(() => false))) {
    await page.locator('button.persona-switch').first().click({ timeout: 8000 });
    await page.waitForTimeout(500);
  }
  const sw = page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first();
  await sw.waitFor({ state: 'visible', timeout: 8000 });
  if ((await sw.getAttribute('aria-checked')) !== 'true') {
    await sw.click({ timeout: 4000 });
    await page.waitForTimeout(400);
  }
  const visit = page.locator('.persona-menu button').filter({ hasText: /访客只读/ }).first();
  await visit.waitFor({ state: 'visible', timeout: 8000 });
  await visit.click({ timeout: 5000 });
  await page.waitForTimeout(1000);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  return ((await page.locator('button.persona-switch').first().innerText().catch(() => '')) || '')
    .replace(/\s+/g, ' ')
    .trim();
}

async function openBasket(page) {
  const dock = page.getByRole('button', { name: /打开对比篮/ });
  if (await dock.count()) await dock.first().click({ timeout: 8000 });
  else await page.getByRole('button', { name: /^对比篮$/ }).first().click({ timeout: 8000 });
  await page.locator('.system-compare-panel').waitFor({ state: 'visible', timeout: 10000 });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

try {
  await page.goto(new URL('login', baseUrl).toString(), { waitUntil: 'domcontentloaded', timeout: 60000 });
  await ensureLogin(page);
  await page.goto(new URL('enterprise/search', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await ensureLogin(page);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
  push('on_search', { url: page.url() });

  // 空篮时先从查询页加入一家
  let addBtns = page.getByRole('button', { name: /加入对比篮/ });
  if (!(await addBtns.count())) {
    // 可能已在结果态；尝试搜索触发
    const box = page.getByRole('textbox').first();
    if (await box.count()) {
      await box.fill('华为');
      const searchBtn = page.getByRole('button', { name: '搜索', exact: true });
      if (await searchBtn.count()) await searchBtn.first().click();
      await page.waitForTimeout(2500);
    }
    addBtns = page.getByRole('button', { name: /加入对比篮/ });
  }
  const addCount = await addBtns.count();
  push('add_btns', { addCount });
  if (addCount) {
    await addBtns.first().click({ timeout: 8000 });
    await page.waitForTimeout(1000);
  }
  out.add_attempted = addCount > 0;

  await openBasket();
  const panel = page.locator('.system-compare-panel');
  push('basket_open_admin');
  out.panel_admin_head = ((await panel.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 300);
  let checks = panel.locator('.ent-compare-item-card__check');
  let checkCount = await checks.count();
  push('cards_admin', { checkCount });

  if (checkCount) {
    const cancel = panel.getByRole('button', { name: '取消选择' });
    if (await cancel.count() && !(await cancel.isDisabled())) await cancel.click().catch(() => {});
    await page.waitForTimeout(200);
    await checks.first().click({ timeout: 8000 });
    await page.waitForTimeout(300);
  }

  const closeBtn = page.locator('[aria-label="关闭对比篮"]');
  if (await closeBtn.count()) await closeBtn.first().click({ timeout: 3000 }).catch(() => {});
  await page.waitForTimeout(400);

  const persona = await switchVisit(page);
  out.persona = persona;
  push('switched_persona', { persona });
  await page.screenshot({ path: path.join(__dirname, 'p0-17-visit.png'), fullPage: false });

  await openBasket();
  push('basket_open_visit');
  out.panel_visit_head = ((await panel.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').slice(0, 300);
  checks = panel.locator('.ent-compare-item-card__check');
  checkCount = await checks.count();
  push('cards_visit', { checkCount });

  if (checkCount) {
    const cancel2 = panel.getByRole('button', { name: '取消选择' });
    if (await cancel2.count() && !(await cancel2.isDisabled())) await cancel2.click().catch(() => {});
    await page.waitForTimeout(200);
    await checks.first().click({ timeout: 8000 });
    await page.waitForTimeout(300);
  }

  const launch = panel.getByRole('button', { name: '发起分析' });
  const launchDis = await launch.isDisabled().catch(() => true);
  const launchCls = (await launch.getAttribute('class').catch(() => '')) || '';
  push('launch_state_visit', { launchDis, launchCls: launchCls.slice(0, 80), checkCount });

  if (!checkCount || launchDis || /arco-btn-disabled/.test(launchCls)) {
    // 访客空篮或无法发起：再以 admin 视角开任务浮层核对「权限 UI 是否存在」
    await page.keyboard.press('Escape');
    // 切回专业 L2（点 persona 菜单里非访客项）
    const menu = page.locator('.persona-menu');
    if (!(await menu.count()) || !(await menu.first().isVisible().catch(() => false))) {
      await page.locator('button.persona-switch').first().click({ timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(400);
    }
    const pro = page.locator('.persona-menu button').filter({ hasText: /专业|L2|政务|GOV/ }).first();
    if (await pro.count()) {
      await pro.click({ timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(800);
      await page.keyboard.press('Escape');
    }
    out.fallback_admin_modal = true;
    await openBasket();
    checks = panel.locator('.ent-compare-item-card__check');
    checkCount = await checks.count();
    if (checkCount) {
      await checks.first().click({ timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(300);
      await panel.getByRole('button', { name: '发起分析' }).click({ timeout: 8000 });
    }
  } else {
    await launch.click({ timeout: 8000 });
  }
  await page.waitForTimeout(600);

  const modal = page.locator('.arco-modal:visible').filter({ hasText: '选择分析任务' }).first();
  const modalVisible = await modal.isVisible().catch(() => false);
  push('modal', { modalVisible });
  await page.screenshot({ path: path.join(__dirname, 'p0-17-modal.png'), fullPage: false });

  if (modalVisible) {
    const body = ((await modal.innerText()) || '').replace(/\s+/g, ' ');
    const evalTasks = ['技术力评估', '商业力评估', '综合竞争力评估'];
    const taskStates = [];
    for (const t of evalTasks) {
      const opt = modal.locator('.ent-compare-analysis-option').filter({ hasText: t }).first();
      const present = (await opt.count()) > 0;
      let radioDisabled = null;
      let hint = '';
      if (present) {
        const radio = opt.locator('.arco-radio').first();
        const cls = (await radio.getAttribute('class').catch(() => '')) || '';
        radioDisabled = /arco-radio-disabled/.test(cls) || (await radio.locator('input').isDisabled().catch(() => false));
        hint = ((await opt.locator('.ent-compare-analysis-option__hint').innerText().catch(() => '')) || '').trim();
      }
      taskStates.push({ task: t, present, radioDisabled, hint });
    }
    const permHints = /权限|无权限|能力不足|缺少|不可用|locked/i.test(body);
    out.modal = {
      body_head: body.slice(0, 500),
      taskStates,
      permHints,
      allEvalPresent: taskStates.every((x) => x.present),
      anyEvalDisabled: taskStates.some((x) => x.radioDisabled),
      anyPermHint: taskStates.some((x) => /权限|能力|缺少/.test(x.hint)) || permHints,
      under_visit: /访客|VISIT|L0/i.test(persona || ''),
    };
    push('eval_tasks', out.modal);

    const first = modal.locator('.ent-compare-analysis-option').filter({ hasText: '技术力评估' }).first();
    if (await first.count()) {
      await first.click({ timeout: 3000 }).catch(() => {});
      await page.waitForTimeout(300);
      out.click_tech = {
        selected: ((await first.getAttribute('class')) || '').includes('is-selected'),
        radioChecked: await first.locator('.arco-radio-checked').count(),
      };
      push('click_tech', out.click_tech);
    }
    await modal.getByRole('button', { name: '取消' }).click({ timeout: 5000 }).catch(() => {});
  }

  out.conclusion =
    out.modal?.anyEvalDisabled || out.modal?.anyPermHint
      ? 'PERM_UX_PRESENT'
      : out.modal?.allEvalPresent
        ? 'EVAL_TASKS_FULLY_ENABLED_NO_PERM_HINT'
        : modalVisible
          ? 'PARTIAL'
          : 'MODAL_UNREACHABLE';
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.conclusion = out.conclusion || 'ERROR';
  await page.screenshot({ path: path.join(__dirname, 'p0-17-error.png'), fullPage: false }).catch(() => {});
} finally {
  fs.writeFileSync(path.join(__dirname, 'p0-17-recon.json'), JSON.stringify(out, null, 2));
  console.log('CONCLUSION', out.conclusion);
  await browser.close();
}
