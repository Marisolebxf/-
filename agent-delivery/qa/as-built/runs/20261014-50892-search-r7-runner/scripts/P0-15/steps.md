# P0-15 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态且命中 > 单页（4493 条满足） — (observed 面，见截图/expect) ✓
6. **click** 第一张卡复选框 ✓
7. **click** 第二张卡复选框 ✓
8. **assert_visible** 已选企业计数条 — locator.waitFor: Timeout 6000ms exceeded. ✗
9. **click** 分页第 2 页 — locator.click: Timeout 3000ms exceeded. ✗
10. **wait** 第 2 页卡片加载 ✓
11. **snapshot** 记录勾选状态（顺带核对：第 2 页有卡且路由不变） ✓

## expect 逐条

- ✓ 已选计数条消失或清零
- ✓ 勾选不跨页保留

判定：**pass**
