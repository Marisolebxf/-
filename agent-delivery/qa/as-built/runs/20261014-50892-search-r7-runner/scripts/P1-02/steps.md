# P1-02 逐步实际操作（playwright-runner）

1. **evaluate** 确保初始推荐可见（承接 P1-01） — (observed 面，见截图/expect) ✓
2. **click** 开启内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
3. **assert_visible** 推荐区机制说明 — locator.waitFor: Timeout 6000ms exceeded. ✗
4. **click** 关闭内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
5. **evaluate** 机制说明消失且单企推荐理由保留 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✗ 开启后推荐区可见推荐机制与示例数据类说明 — expect visible 超时 8000ms | assert: const ps = page.locator('button.persona-switch'); if (!(await page.locator('.persona-menu').count())) { await ps.first()
- ✓ 关闭后机制类说明在推荐区消失且单企推荐理由保留

判定：**fail**
