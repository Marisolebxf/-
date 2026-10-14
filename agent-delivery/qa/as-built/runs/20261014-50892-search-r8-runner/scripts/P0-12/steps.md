# P0-12 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search?mode=advanced ✓
2. **evaluate** 构造任一条件（如经营状态=在营） — (observed 面，见截图/expect) ✓
3. **click** 保存为查询方案 — locator.click: Timeout 3000ms exceeded. ✗
4. **fill** 弹层名称输入框 — locator.fill: Timeout 5000ms exceeded. ✗
5. **click** 确定 — locator.click: Timeout 3000ms exceeded. ✗
6. **click** 清空条件 ✓
7. **click** 使用查询方案 ✓
8. **click** 方案 qa-r2-1013 — locator.click: Timeout 3000ms exceeded. ✗
9. **wait** 条件恢复或结果直出 ✓

## expect 逐条

- ✗ 方案可保存并命名 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-modal:visible, [role=dialog]:visible').first().waitFor({ state: 'visible', timeout: 8000 }); a
- ✓ 使用后条件恢复为可识别状态（已选条件大于 0 或直接进入高级筛选结果）
- ⚠ 恢复内容不含关键词与企业名单

判定：**fail**
