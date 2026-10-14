# P1-10 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 选择区域控件 ✓
7. **wait** 级联/下拉展开 ✓
8. **snapshot** 记录选项清单（observed） ✓

## expect 逐条

- ⚠ 控件占位为「选择区域」
- ✗ 展开后可见不少于一级可选项（热门城市/省/市） — expect visible 超时 8000ms | assert: const panel = page.locator('.arco-cascader-panel, .arco-select-dropdown').first(); await expect(panel).toBeVisible({ tim

判定：**fail**
