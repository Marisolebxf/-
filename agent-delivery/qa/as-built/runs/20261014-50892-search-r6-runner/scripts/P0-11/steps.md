# P0-11 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search?mode=advanced ✓
2. **click** 字段 企业所属地区 ✓
3. **wait** 地区选择器展开 ✓
4. **snapshot**  ✓

## expect 逐条

- ✗ 选项含至少两个省级名称 — locator.innerText: Timeout 30000ms exceeded. | assert: const panel = page.locator('.arco-cascader-panel, .arco-cascader-panel-column, .arco-trigger-popup:visible .arco-cascade
- ✗ 非仅深圳区县作为唯一一层 — locator.innerText: Timeout 30000ms exceeded. | assert: const panelText = await page.locator('.arco-cascader-panel, .arco-cascader-panel-column').first().innerText(); const pro

判定：**fail**
