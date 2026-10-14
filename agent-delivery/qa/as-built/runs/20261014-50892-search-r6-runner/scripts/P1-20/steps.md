# P1-20 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **assert_absent** 表格/卡片视图切换控件 ✓
7. **evaluate** 结果为横向长卡形态 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 结果为横向长卡且无「表格视图」「卡片视图」切换控件

判定：**pass**
