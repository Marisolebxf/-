#!/usr/bin/env node
/** P0-16 写稿一次性无头实勘：结果态「差距分析报告」入口与报告内容（优势/差距） */
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolsDir = path.resolve(__dirname, '../../../../../../tools');
const require = createRequire(path.join(toolsDir, 'package.json'));
const { chromium } = require('playwright');

const base = 'http://111.198.38.90:50892/';
const knownResult =
  'enterprise/evaluation?workspace=technology&mode=technology&enterprise_codes[]=0a2b82208071ce5a0e3bd562b80e263b&enterprise_codes[]=12ceab1a61c7d1e1e5cb61b78dd8f3aa&source=compare-basket&view=result&analysis_type=technology&task_id=EVAL-20261015-003';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto(base + 'login', { waitUntil: 'domcontentloaded' });
await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
await page.locator('input[type=password]').first().fill('123456');
const loginBtn = page.getByRole('button', { name: /登录/ });
if (await loginBtn.count()) await loginBtn.first().click();
else await page.keyboard.press('Enter');
await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 20000 });

const out = { surveyed_at: new Date().toISOString() };
const bodyRes = async () => {
  const t = await page.locator('body').innerText().catch(() => '');
  return /技术力评估结果/.test(t) && /\d+\s*分/.test(t);
};

// —— 路径 A：现场发起（篮有货）——
await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1200);
const closeB = page.locator('button[aria-label="关闭对比篮"]');
if (await closeB.count() && await closeB.first().isVisible().catch(() => false) && await closeB.first().isEnabled().catch(() => false)) {
  try { await closeB.first().click({ timeout: 1500 }); await page.waitForTimeout(300); } catch {}
}

let branch = null;
const openBtn = page.getByRole('button', { name: /前往对比篮选择企业|返回对比篮调整对象/ }).first();
if (await openBtn.isVisible().catch(() => false)) {
  try {
    await openBtn.click({ timeout: 8000 });
    await page.waitForTimeout(1000);
    let sels = page.locator('[aria-label^="选择 "]');
    let n = await sels.count();
    out.basket_count = n;
    // 篮空：点「新增」尝试搜企业入篮
    if (n < 2) {
      const addBtn = page.getByRole('button', { name: /^新增$/ }).first();
      if (await addBtn.isVisible().catch(() => false)) {
        await addBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1500);
        out.add_opened = true;
        const search = page.getByPlaceholder(/企业名称|搜索/).first();
        if (await search.isVisible().catch(() => false)) {
          await search.fill('华为');
          await page.keyboard.press('Enter');
          await page.waitForTimeout(2500);
        }
        // 勾选搜索结果（尽量通用）
        const addSels = page.locator('[aria-label^="选择 "], .arco-checkbox:not(.arco-checkbox-checked) input, input[type=checkbox]');
        out.add_sel_count = await addSels.count();
        for (let i = 0; i < Math.min(await addSels.count(), 2); i++) {
          try { await addSels.nth(i).click({ timeout: 2000 }); } catch {}
        }
        const confirmAdd = page.getByRole('button', { name: /确定|加入|完成/ }).first();
        if (await confirmAdd.isVisible().catch(() => false)) {
          try { await confirmAdd.click({ timeout: 5000 }); await page.waitForTimeout(1500); } catch {}
        }
        sels = page.locator('[aria-label^="选择 "]');
        n = await sels.count();
        out.basket_count_after_add = n;
      }
    }
    if (n >= 2) {
      await sels.nth(0).click();
      await sels.nth(1).click();
      await page.waitForTimeout(400);
      const okBtn = page.getByRole('button', { name: '确定' }).first();
      await okBtn.scrollIntoViewIfNeeded().catch(() => {});
      await okBtn.click({ timeout: 10000 });
      await page.waitForTimeout(2500);
      const start = page.getByRole('button', { name: '开始分析' });
      out.start_disabled = await start.isDisabled();
      if (!out.start_disabled) {
        await start.click();
        const t0 = Date.now();
        while (Date.now() - t0 < 5000) {
          if (await page.getByText(/技术力评估生成中|可视化分析过程/).first().isVisible().catch(() => false)) { branch = 'processing'; break; }
          if (/view=result/.test(page.url())) { branch = 'result'; break; }
          await page.waitForTimeout(300);
        }
        if (branch !== 'result') {
          const t1 = Date.now();
          while (Date.now() - t1 < 90000) {
            if (/view=result/.test(page.url())) { branch = 'result'; break; }
            if (await bodyRes()) { branch = 'inplace'; break; }
            await page.waitForTimeout(1000);
          }
        }
        const tw = Date.now();
        while (Date.now() - tw < 30000 && !(await bodyRes())) await page.waitForTimeout(1000);
      } else {
        out.precheck = (await page.locator('body').innerText()).includes('预检未返回企业明细');
      }
    } else {
      const cancel = page.getByRole('button', { name: '取消' }).first();
      if (await cancel.isVisible().catch(() => false)) try { await cancel.click({ timeout: 2000 }); } catch {}
    }
  } catch (e) {
    out.open_err = String(e && e.message || e).slice(0, 200);
  }
}

// —— 路径 B：最近评估 Tab ——
if (!(await bodyRes())) {
  const tab = page.getByRole('tab', { name: /最近评估/ }).first();
  if (await tab.isVisible().catch(() => false)) {
    try { await tab.click({ timeout: 3000 }); await page.waitForTimeout(2000); } catch {}
  }
  const bodyTab = await page.locator('body').innerText().catch(() => '');
  out.recent_sample = bodyTab.replace(/\s+/g, ' ').slice(0, 400);
  let tid = (/task_id=(EVAL-\d{8}-\d{3})/.exec(page.url()) || [])[1]
    || (/EVAL-\d{8}-\d{3}/.exec(bodyTab) || [])[0];
  out.fallback_tid = tid || null;
  if (tid) {
    await page.goto(base + 'enterprise/evaluation?workspace=technology&mode=technology&view=result&analysis_type=technology&task_id=' + tid, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);
    branch = branch || 'result_via_recent';
  }
}

// —— 路径 C：已知当日任务深链（仅写稿实勘；正式脚本不以冷深链为主）——
if (!(await bodyRes())) {
  await page.goto(base + knownResult, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  branch = branch || 'known_deeplink';
  out.deeplink_body_ready = await bodyRes();
  if (!(await bodyRes())) {
    out.deeplink_body_head = (await page.locator('body').innerText().catch(() => '')).slice(0, 500);
  }
}

out.branch = branch;
out.url = page.url();
out.body_ready = await bodyRes();
await page.screenshot({ path: path.join(__dirname, 'result-before-report.png'), fullPage: true });

if (!(await bodyRes())) {
  fs.writeFileSync(path.join(__dirname, 'probe-p016.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify({ blocked: true, reason: '无结果态可达', ...out }, null, 2));
  await browser.close();
  process.exit(0);
}

const body = await page.locator('body').innerText();
out.hits = {
  report_section: body.includes('评估报告'),
  view_html: body.includes('查看 HTML 报告'),
  gap_diag: body.includes('技术指标与差距诊断'),
  adv_col: body.includes('领先差距与优势短板'),
  report_lines: (body.match(/[^\n]*(报告|优势|差距|短板)[^\n]*/g) || []).slice(0, 20),
  report_block: (() => {
    const i = body.indexOf('评估报告');
    return i >= 0 ? body.slice(i, i + 280) : null;
  })(),
  gap_block: (() => {
    const i = body.indexOf('技术指标与差距诊断');
    return i >= 0 ? body.slice(i, i + 400) : null;
  })(),
};

const entryCandidates = [];
const anyClick = page.locator('button, a, [role="button"]').filter({ hasText: /查看\s*HTML\s*报告|查看报告|差距分析报告|HTML 报告/ });
out.entry_any_count = await anyClick.count();
for (let i = 0; i < Math.min(await anyClick.count(), 6); i++) {
  const el = anyClick.nth(i);
  entryCandidates.push({
    idx: i,
    tag: await el.evaluate((e) => e.tagName).catch(() => '?'),
    text: (await el.innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 80),
    visible: await el.isVisible().catch(() => false),
    enabled: await el.isEnabled().catch(() => false),
    aria: await el.getAttribute('aria-label').catch(() => null),
    href: await el.getAttribute('href').catch(() => null),
  });
}
out.entryCandidates = entryCandidates;

const clickTarget = page.getByRole('button', { name: /查看\s*HTML\s*报告/ }).first();
const clickAlt = anyClick.first();
let clicked = false;
const popupPromise = page.waitForEvent('popup', { timeout: 10000 }).catch(() => null);
try {
  if (await clickTarget.isVisible().catch(() => false)) {
    await clickTarget.scrollIntoViewIfNeeded().catch(() => {});
    await clickTarget.click({ timeout: 5000 });
    clicked = true;
    out.click_via = 'role=button';
  } else if (await clickAlt.isVisible().catch(() => false)) {
    await clickAlt.scrollIntoViewIfNeeded().catch(() => {});
    await clickAlt.click({ timeout: 5000 });
    clicked = true;
    out.click_via = 'filter-text';
  }
} catch (e) {
  out.click_err = String(e && e.message || e).slice(0, 200);
}
out.clicked = clicked;
await page.waitForTimeout(2500);
const popup = await popupPromise;
out.popup = !!popup;
if (popup) {
  await popup.waitForLoadState('domcontentloaded').catch(() => {});
  await popup.waitForTimeout(2000);
  out.popup_url = popup.url();
  out.popup_title = await popup.title().catch(() => '');
  const pt = await popup.locator('body').innerText().catch(() => '');
  out.popup_len = pt.length;
  out.popup_hits = {
    advantage: /优势|领先/.test(pt),
    gap: /差距|短板|不足/.test(pt),
    tech: /技术/.test(pt),
    sample: pt.replace(/\s+/g, ' ').slice(0, 600),
  };
  await popup.screenshot({ path: path.join(__dirname, 'report-popup.png'), fullPage: true }).catch(() => {});
}

out.after_click = {
  url: page.url(),
  drawer: await page.locator('.arco-drawer:visible').count().catch(() => 0),
  modal: await page.locator('.arco-modal:visible').count().catch(() => 0),
  iframe: await page.locator('iframe').count().catch(() => 0),
};
await page.screenshot({ path: path.join(__dirname, 'result-after-report-click.png'), fullPage: true });

fs.writeFileSync(path.join(__dirname, 'probe-p016.json'), JSON.stringify(out, null, 2), 'utf8');
console.log(JSON.stringify({
  branch: out.branch,
  body_ready: out.body_ready,
  basket_count: out.basket_count,
  basket_count_after_add: out.basket_count_after_add,
  hits: out.hits,
  clicked: out.clicked,
  click_via: out.click_via,
  popup: out.popup,
  popup_url: out.popup_url,
  popup_hits: out.popup_hits,
  entryCandidates: out.entryCandidates,
  after_click: out.after_click,
}, null, 2));
await browser.close();
