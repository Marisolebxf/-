# P0-04 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **click** 结果中任一企业名称 — locator.click: Timeout 3000ms exceeded. ✗
6. **wait** .arco-drawer 可见 ✓
7. **assert_visible** .arco-drawer — locator.waitFor: Timeout 6000ms exceeded. ✗
8. **assert_url**  ✓
9. **snapshot**  ✓

## expect 逐条

- ✗ 抽屉在当前页打开且路由不变 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-drawer').first().waitFor({ state: 'visible', timeout: 8000 }); await expect(page).toHaveURL(/e
- ✗ 抽屉含企业头部且默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer')).toContainText('工商概况'); await expect(page.locator('.arco-drawer .arco-tabs-tab
- ✗ 页签共十项齐全（清单见用例册附录A） — expect visible 超时 8000ms | assert: const drawer = page.locator('.arco-drawer'); for (const t of ['工商概况','主要团队','资质荣誉','知识产权','经营财务','供应链关系','关系图谱','舆情动态','

判定：**fail**
