/**
 * 关闭「内部评审模式」。用例勘察、脚本复勘、机跑共用。
 * 人设菜单里有多个 switch，必须点 aria-label，禁止 first()。
 * @returns {'off'|'no-persona'|'no-switch'}
 */
export async function ensureReviewOff(page) {
  const menuBtn = page.locator('button.persona-switch').first();
  const sw = () => page.locator('button[role=switch][aria-label="内部评审模式"]').first();
  const visible = await sw().isVisible().catch(() => false);
  if (!visible) {
    if (!(await menuBtn.isVisible().catch(() => false))) return 'no-persona';
    await menuBtn.click({ timeout: 3000 });
    await page.waitForTimeout(200);
  }
  if (!(await sw().isVisible().catch(() => false))) return 'no-switch';
  if ((await sw().getAttribute('aria-checked')) === 'true') {
    await sw().click({ timeout: 3000 });
    await page.waitForTimeout(200);
  }
  await page.keyboard.press('Escape').catch(() => {});
  if (await page.locator('.persona-menu').first().isVisible().catch(() => false)) {
    await menuBtn.click({ timeout: 2000 }).catch(() => {});
  }
  return 'off';
}
