#!/usr/bin/env node
/**
 * 一次性探针 P0-18（FUNC-01326 无映射产业空态）：
 * 逐个扫 15 集群 → 选产业后展开产业链，记选项数 / 「无相关产业数据」文案 / 产业选中是否回落。
 * 产物 probe-p018.json + 截图；禁止有头浏览器。
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
  case_id: 'P0-18',
  func_id: 'FUNC-01326',
  empty_copy_target: '无相关产业数据',
};

async function closeBasket() {
  const close = page.locator('[aria-label="关闭对比篮"]');
  if ((await close.count()) && (await close.first().isVisible().catch(() => false))) {
    await close.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }
}

try {
  await page.goto(new URL('login', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
  await page.locator('input[type=password]').first().fill('123456');
  await page.getByRole('button', { name: /登录/ }).first().click();
  await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

  // 顺带抄 catalog API：按 parentIndustryId 判真无映射（UI 层可能回落全量链）
  const catalogBody = await page
    .evaluate(async () => {
      const paths = [
        '/api/topic/v1/meta/industry-catalog',
        '/api/topic/v1/industry/catalog',
        '/topic/v1/meta/industry-catalog',
      ];
      for (const p of paths) {
        try {
          const r = await fetch(p, { credentials: 'include' });
          if (!r.ok) continue;
          return { path: p, status: r.status, json: await r.json() };
        } catch {
          /* try next */
        }
      }
      return null;
    })
    .catch(() => null);
  if (catalogBody) {
    const data = catalogBody.json?.data ?? catalogBody.json;
    const inds = data?.industries || [];
    const chs = data?.chains || [];
    report.catalog_api = {
      path: catalogBody.path,
      status: catalogBody.status,
      industry_n: inds.length,
      chain_n: chs.length,
      per_industry_chain_counts: inds.map((i) => ({
        id: i.id,
        label: i.label,
        chain_n: chs.filter((c) => c.parentIndustryId === i.id).length,
      })),
    };
    report.api_unmapped = (report.catalog_api.per_industry_chain_counts || []).filter(
      (r) => r.chain_n === 0,
    );
  }

  await page.goto(new URL('service-portal/overview', baseUrl).toString(), {
    waitUntil: 'domcontentloaded',
  });
  await page.waitForTimeout(2500);
  await closeBasket();
  await page.locator('.arco-spin-mask').first().waitFor({ state: 'hidden', timeout: 15000 }).catch(() => {});

  // 选中后 placeholder 会变；筛条内固定两 select（nth）
  const filter = page.locator('[aria-label="筛选条"], .svc-portal-filter').first();
  const ind = () => filter.locator('.arco-select-view').nth(0);
  const chain = () => filter.locator('.arco-select-view').nth(1);

  async function safeClick(loc) {
    await page.locator('.arco-spin-mask').first().waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
    try {
      await loc.click({ timeout: 5000 });
    } catch {
      await loc.click({ force: true, timeout: 5000 });
    }
  }

  await safeClick(ind());
  await page.waitForTimeout(500);
  const options = await page.locator('.arco-trigger-popup:visible .arco-select-option').allTextContents();
  report.industry_count = options.length;
  report.industry_options = options.map((t) => t.trim()).filter(Boolean);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);

  const perCluster = [];
  let unmapped = null;
  // 探针提速：只扫前 5 + 未来* 5（共最多 10）；全量由 API 侧已覆盖
  const scanNames = [
    ...report.industry_options.filter((n) => !n.startsWith('未来')).slice(0, 5),
    ...report.industry_options.filter((n) => n.startsWith('未来')),
  ];
  report.ui_scan_names = scanNames;
  for (const name of scanNames) {
    await closeBasket();
    await safeClick(ind());
    await page.waitForTimeout(400);
    const opt = page.locator('.arco-trigger-popup:visible .arco-select-option').filter({ hasText: name });
    if (!(await opt.count())) {
      perCluster.push({ name, err: 'option_missing' });
      await page.keyboard.press('Escape').catch(() => {});
      continue;
    }
    await opt.first().click();
    await page.waitForTimeout(1200);
    await page.locator('.arco-spin-mask').first().waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});

    const indText = (await ind().innerText().catch(() => '')).trim();
    const qIndustry = (() => {
      try {
        return new URL(page.url()).searchParams.get('industry');
      } catch {
        return null;
      }
    })();
    const chainDisabled = await chain()
      .evaluate((el) => el.className.includes('disabled'))
      .catch(() => null);
    let chainOptCount = null;
    let emptyCopyInPopup = false;
    let emptyPlaceholder = false;
    let popupTexts = [];
    if (chainDisabled === false) {
      await safeClick(chain());
      await page.waitForTimeout(500);
      const popup = page.locator('.arco-trigger-popup:visible');
      popupTexts = (await popup.allTextContents()).map((t) => t.trim()).filter(Boolean);
      chainOptCount = await popup.locator('.arco-select-option').count();
      emptyCopyInPopup =
        (await page.getByText('无相关产业数据').count()) > 0 ||
        popupTexts.some((t) => /无相关产业数据/.test(t));
      const chainPh = await chain()
        .locator('input')
        .getAttribute('placeholder')
        .catch(() => '');
      emptyPlaceholder = /无相关产业数据/.test(chainPh || '');
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(200);
    } else {
      const chainPh = await chain()
        .locator('input')
        .getAttribute('placeholder')
        .catch(() => '');
      emptyPlaceholder = /无相关产业数据/.test(chainPh || '');
    }
    const pageEmptyCopy = (await page.getByText('无相关产业数据').count()) > 0;
    const row = {
      name,
      ind_selected_text: indText.slice(0, 80),
      retained: indText.includes(name) || Boolean(qIndustry),
      query_industry: qIndustry,
      chain_disabled: chainDisabled,
      chain_opt_count: chainOptCount,
      empty_copy_popup: emptyCopyInPopup,
      empty_placeholder: emptyPlaceholder,
      empty_copy_page: pageEmptyCopy,
      popup_sample: popupTexts.slice(0, 3),
    };
    perCluster.push(row);
    if (
      (chainOptCount === 0 || emptyCopyInPopup || emptyPlaceholder || pageEmptyCopy) &&
      !unmapped
    ) {
      unmapped = row;
    }
  }

  report.per_cluster = perCluster;
  report.unmapped_found = Boolean(unmapped);
  report.unmapped_sample = unmapped;
  report.all_have_chain_opts = perCluster.every(
    (r) => typeof r.chain_opt_count === 'number' && r.chain_opt_count > 0 && !r.empty_copy_popup,
  );

  await page.screenshot({
    path: path.join(outDir, 'probe-p018.png'),
    fullPage: false,
  });
  report.screenshot = 'probe-p018.png';
} catch (e) {
  report.error = String(e && e.stack ? e.stack : e);
} finally {
  fs.writeFileSync(path.join(outDir, 'probe-p018.json'), JSON.stringify(report, null, 2));
  console.log(
    JSON.stringify(
      {
        industry_count: report.industry_count,
        unmapped_found: report.unmapped_found,
        all_have_chain_opts: report.all_have_chain_opts,
        error: report.error || null,
      },
      null,
      2,
    ),
  );
  await browser.close();
}
