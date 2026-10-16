#!/usr/bin/env node
/** P0-19 独立实勘：结果态「调整配置」→ 返回配置态 */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const out = {
  surveyed_at: new Date().toISOString(),
  purpose: 'P0-19-adjust-config',
  CASE_ID: 'P0-19',
  FUNC_ID: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00923',
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

try {
  await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  const loginBtn = page.getByRole('button', { name: /登录/ });
  if (await loginBtn.count()) await loginBtn.first().click();
  else await page.keyboard.press('Enter');
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });
  out.login = true;

  await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(1500);

  const closeB = page.locator('button[aria-label="关闭对比篮"]');
  if (
    (await closeB.count()) &&
    (await closeB.first().isVisible().catch(() => false)) &&
    (await closeB.first().isEnabled().catch(() => false))
  ) {
    try {
      await closeB.first().click({ timeout: 1500 });
      await page.waitForTimeout(300);
    } catch {}
  }

  // 路径 A：最近评估 → 恢复结果（P0-15 空壳收口同型，避免冷深链）
  await page.getByRole('tab', { name: /最近评估/ }).first().click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  const restore = page.getByRole('button', { name: '恢复结果' });
  out.restore_count = await restore.count();
  out.path = 'restore';

  if (out.restore_count < 1) {
    out.error = '最近评估无「恢复结果」';
  } else {
    await restore.first().click({ timeout: 8000 });
    const t0 = Date.now();
    let ok = false;
    while (Date.now() - t0 < 60000) {
      const t = await page.locator('body').innerText().catch(() => '');
      if (/技术力评估结果/.test(t) && /\d+\s*分/.test(t)) {
        ok = true;
        break;
      }
      await page.waitForTimeout(1000);
    }
    out.after_restore = {
      ok,
      ms: Date.now() - t0,
      url: page.url(),
    };
    if (!ok) {
      out.error = '恢复结果后无结果正文';
    } else {
      const body = await page.locator('body').innerText();
      const adjustBtn = page.getByRole('button', { name: '调整配置' });
      out.adjust = {
        count: await adjustBtn.count(),
        visible: await adjustBtn.first().isVisible().catch(() => false),
        enabled: await adjustBtn.first().isEnabled().catch(() => false),
        body_has_text: /调整配置/.test(body),
      };
      out.url_before = page.url();
      out.has_view_result_before = /view=result/.test(page.url());

      if (out.adjust.count >= 1 && out.adjust.visible) {
        await adjustBtn.first().click({ timeout: 8000 });
        await page.waitForTimeout(2000);
        const bodyAfter = await page.locator('body').innerText();
        out.url_after = page.url();
        out.has_view_result_after = /view=result/.test(page.url());
        out.has_view_processing_after = /view=processing/.test(page.url());
        out.has_view_report_after = /view=report/.test(page.url());
        out.config_signals = {
          eval_object: /评估对象/.test(bodyAfter),
          start_btn: await page.getByRole('button', { name: '开始分析' }).count(),
          start_visible: await page
            .getByRole('button', { name: '开始分析' })
            .first()
            .isVisible()
            .catch(() => false),
          basket_cta: /前往对比篮选择企业|返回对比篮调整对象/.test(bodyAfter),
          still_result_title: /技术力评估结果/.test(bodyAfter) && !/开始分析/.test(bodyAfter),
          adjust_still: await page.getByRole('button', { name: '调整配置' }).count(),
          reanalyze_still: await page.getByRole('button', { name: '重新分析' }).count(),
          body_slice: bodyAfter.replace(/\s+/g, ' ').slice(0, 500),
        };
        // screenshot
        await page.screenshot({
          path: path.join(__dirname, 'probe-p019-after-adjust.png'),
          fullPage: false,
        });
        out.screenshot = 'probe-p019-after-adjust.png';
      } else {
        out.error = '结果态无可见「调整配置」按钮';
      }
    }
  }
} catch (e) {
  out.error = String(e && e.message ? e.message : e);
  out.stack = String(e && e.stack ? e.stack : '');
} finally {
  fs.writeFileSync(path.join(__dirname, 'probe-p019.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
}
