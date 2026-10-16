// probe-p022.mjs — P0-22（FUNC-01266）写稿前无头实证探针
// 验证：模型区标题/说明行、四维度名与顺序、四权重初值（inputValue+aria-valuenow 双口径）、上下调节钮存在性
import { chromium } from '/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration/agent-delivery/qa/as-built/tools/node_modules/playwright/index.mjs';

const BASE = 'http://111.198.38.90:50892';
const out = { route: BASE + '/service/institution-decision?workspace=cultivate&tab=cultivate', steps: [] };

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080, deviceScaleFactor: 1 } });
  // 登录（同 run-scripts.mjs ensureLogin 口径：admin/123456，Enter 后仍停 /login 则显式点「登录」按钮兜底）
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(800);
  if (page.url().includes('/login')) {
    await page.locator('input[placeholder*=用户名], input[type=text]').first().fill('admin');
    await page.locator('input[type=password]').first().fill('123456');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1200);
    if (page.url().includes('/login')) {
      await page.locator('button[type=submit], button:has-text("登录"), button:has-text("登 录")').first().click().catch(() => {});
    }
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 10000 });
    out.steps.push('login done, url=' + page.url());
  }
  await page.goto(BASE + '/service/institution-decision?workspace=cultivate&tab=cultivate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2600);
  out.steps.push('goto done, url=' + page.url());

  const close = page.locator('button[aria-label="关闭对比篮"]');
  if (await close.count() && await close.first().isVisible().catch(() => false)) {
    try { await close.first().click({ timeout: 1500 }); await page.waitForTimeout(300); out.steps.push('closed compare basket'); } catch {}
  }

  const m = (await page.locator('main').first().innerText().catch(() => '')) || '';
  out.main_has_title = m.includes('培育评估模型（演示模型口径）');
  out.main_has_note = m.includes('四维度与招标一致');
  const i = m.indexOf('培育评估模型');
  out.model_body_head = i >= 0 ? m.slice(i, i + 200).replace(/\s+/g, ' ') : '(模型区未命中)';
  const j = m.indexOf('四维度与招标一致');
  out.note_context = j >= 0 ? m.slice(Math.max(0, j - 60), j + 120).replace(/\s+/g, ' ') : '(说明行未命中)';

  const dims = ['现有规模', '技术创新能力', '服务成效', '市场缺口'];
  out.model = [];
  for (const d of dims) {
    const holder = page.locator(`[aria-label="${d}权重"]`).first();
    const cnt = await holder.count();
    if (!cnt) { out.model.push({ dim: d, holder_found: false }); continue; }
    const spin = holder.locator('[role=spinbutton]').first();
    const spinVis = await spin.isVisible().catch(() => false);
    const val = spinVis ? String(await spin.inputValue().catch(() => '')) : '';
    const aria = String((await spin.getAttribute('aria-valuenow').catch(() => null)) ?? '');
    const label = ((await holder.innerText().catch(() => '')) || '').replace(/\s+/g, ' ').trim().slice(0, 80);
    out.model.push({ dim: d, holder_found: true, spin_visible: spinVis, input_value: val, aria_valuenow: aria, holder_text_head: label });
  }
  // 调节钮：DOM 结构直接数
  out.step_buttons = await page.evaluate(() => {
    const dims = ['现有规模', '技术创新能力', '服务成效', '市场缺口'];
    return dims.map((d) => {
      const holder = document.querySelector(`[aria-label="${d}权重"]`);
      if (!holder) return { dim: d, holder: false };
      const btns = [...holder.querySelectorAll('.arco-input-number-step-button')];
      const inc = btns.filter(b => (b.className || '').includes('increment')).length;
      const dec = btns.filter(b => (b.className || '').includes('decrement')).length;
      const spin = holder.querySelector('[role=spinbutton]');
      return { dim: d, holder: true, total: btns.length, increment: inc, decrement: dec,
        input_value: spin ? spin.value : null, aria_valuenow: spin ? spin.getAttribute('aria-valuenow') : null,
        visible: !!(spin && spin.offsetParent !== null) };
    });
  });
  out.conclusion_pending = 'fill after real run';
} catch (e) {
  out.error = String(e && e.stack || e);
} finally {
  await browser.close();
}
console.log(JSON.stringify(out, null, 2));
