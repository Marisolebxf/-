# P0-13 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态（智能搜索「人工智能」或最近检索恢复） — (observed 面，见截图/expect) ✓
6. **click** 排序下拉 ✓
7. **assert_visible** 四类排序选项 ✓
8. **select_option** 排序 — locator.selectOption: Error: Element is not a <select> element ✗
9. **wait** 列表刷新 ✓
10. **select_option** 排序 — locator.selectOption: Error: Element is not a <select> element ✗
11. **select_option** 排序 — locator.selectOption: Error: Element is not a <select> element ✗
12. **select_option** 排序 — locator.selectOption: Error: Element is not a <select> element ✗

## expect 逐条

- ✗ 排序选项含综合竞争力优先、有效专利数、最新营收、成立时间四类 — 缺少排序选项: 综合竞争力优先 | assert: const sortSel = page.locator('.arco-select-view').filter({ hasText: '综合竞争力优先' }).first(); await sortSel.click({ timeout:
- ✓ 每次切换后仍可见结果列表或明确空态

判定：**fail**
