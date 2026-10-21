#!/usr/bin/env node
/**
 * 一次性探针 P0-17（FUNC-01323 机构详情地址参数分享恢复）：
 * 深圳重点机构墙 → 点卡写 ?org= → 深链复进开抽屉 → 关闭清参。
 * 产物 probe-p017.json + 截图；禁止有头浏览器。
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
const outDir = __dirname;

const browser = await chromium.launch({ headless: true });
const page = await (
  await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  })
).newPage();
const report = {
  surveyed_at: new Date().toISOString(),
  case_id: 'P0-17',
  func_id: 'FUNC-01323',
  param_name_source: 'query.org (SvcPortalKeyOrgSection / readOrgQuery)',
};

try {
  await page.goto(new URL('login', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  const apiPromise = page
    .waitForResponse(
      (r) => /key-orgs|key_orgs|keyorg/i.test(r.url()) && r.request().method() !== 'OPTIONS',
      { timeout: 20000 },
    )
    .catch(() => null);

  await page.goto(new URL('service-portal/shenzhen', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(2800);
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }

  report.url_cold = page.url();
  report.empty_visible = (await page.getByText(/暂无重点机构/).count()) > 0;
  report.card_count = await page.locator('.svc-portal-keyorg-card').count();
  report.has_cards = report.card_count > 0;

  const api = await apiPromise;
  if (api) {
    report.api = { url: api.url(), status: api.status() };
    try {
      const body = await api.json();
      const d = body && body.data !== undefined ? body.data : body;
      report.api_empty = !!(d && (d.empty === true || (Array.isArray(d.items) && d.items.length === 0)));
      report.api_items_len = d && Array.isArray(d.items) ? d.items.length : null;
      report.api_sample_org =
        d && Array.isArray(d.items) && d.items[0]
          ? String(d.items[0].org_id || d.items[0].orgId || '').slice(0, 40)
          : null;
    } catch (e) {
      report.api_parse_err = String(e && e.message);
    }
  }

  // 对照：错误参数名 orgId 是否被识别（相对 P1-06 存量口径）
  await page.goto(new URL('service-portal/shenzhen?orgId=__PROBE_ORGID_NAME__', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(2000);
  report.orgId_param_probe = {
    url: page.url(),
    drawer_visible: await page.locator('.arco-drawer').first().isVisible().catch(() => false),
    note: '源码只读 query.org；orgId 应被忽略',
  };

  // 合法样名深链（墙空时预期非法清参，归 01327；此处只记现场）
  await page.goto(new URL('service-portal/shenzhen?org=org-live-1', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(2500);
  report.org_param_probe = {
    url_after: page.url(),
    has_org_query: /[?&]org=/.test(page.url()),
    drawer_visible: await page.locator('.arco-drawer').first().isVisible().catch(() => false),
    drawer_testid: await page.locator('[data-testid="svc-portal-keyorg-drawer"]').count(),
    toast_or_msg: await page
      .locator('.arco-message, .arco-notification')
      .allTextContents()
      .then((a) => a.slice(0, 4))
      .catch(() => []),
  };

  if (report.has_cards) {
    await page.goto(new URL('service-portal/shenzhen', baseUrl).toString(), {
      waitUntil: 'domcontentloaded',
    });
    await page.waitForTimeout(2000);
    const card = page.locator('.svc-portal-keyorg-card').first();
    report.first_card_aria = (await card.getAttribute('aria-label')) || '';
    await card.click({ timeout: 8000 });
    await page.waitForTimeout(1000);
    report.url_after_click = page.url();
    report.org_from_click = (() => {
      try {
        return new URL(page.url()).searchParams.get('org');
      } catch {
        return null;
      }
    })();
    report.drawer_after_click = await page.locator('.arco-drawer').first().isVisible().catch(() => false);

    if (report.org_from_click) {
      const sharePath = `/service-portal/shenzhen?org=${encodeURIComponent(report.org_from_click)}`;
      await page.goto(new URL(sharePath.replace(/^\//, ''), baseUrl).toString(), {
        waitUntil: 'domcontentloaded',
      });
      await page.waitForTimeout(2500);
      report.share_restore = {
        url: page.url(),
        drawer_visible: await page.locator('.arco-drawer').first().isVisible().catch(() => false),
        drawer_testid: await page.locator('[data-testid="svc-portal-keyorg-drawer"]').count(),
      };
      if (report.share_restore.drawer_visible) {
        const closeBtn = page.locator('.arco-drawer .arco-drawer-close-btn, .arco-drawer [aria-label="关闭"]').first();
        if (await closeBtn.count()) await closeBtn.click({ timeout: 3000 }).catch(() => {});
        else await page.keyboard.press('Escape');
        await page.waitForTimeout(800);
        report.after_close = {
          url: page.url(),
          org_cleared: !/[?&]org=/.test(page.url()),
          drawer_visible: await page.locator('.arco-drawer').first().isVisible().catch(() => false),
          active_tag: await page.evaluate(() => {
            const el = document.activeElement;
            if (!el) return null;
            return {
              tag: el.tagName,
              class: String(el.className || '').slice(0, 80),
              aria: el.getAttribute('aria-label') || '',
            };
          }),
        };
      }
    }
  }

  await page.screenshot({ path: path.join(outDir, 'probe-p017.png'), fullPage: false });
  report.screenshot = 'fixtures/scout/probe-p017.png';
  report.verdict_hint = report.has_cards
    ? 'cards_present — can assert share restore with ?org='
    : 'key_org_wall_honest_empty — allow_skip ENV-SVC-PORTAL-KEY-ORG-EMPTY；参数名 as-built=org（非 orgId）';
} catch (e) {
  report.error = String(e && e.stack ? e.stack : e);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p017.json'), JSON.stringify(report, null, 2));
  await browser.close();
  console.log(JSON.stringify(report, null, 2));
}
