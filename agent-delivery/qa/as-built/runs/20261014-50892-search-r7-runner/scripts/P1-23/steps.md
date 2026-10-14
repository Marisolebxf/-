# P1-23 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态且已选排序项 — (observed 面，见截图/expect) ✓
6. **click** 切换排序方向按钮 ✓
7. **wait** 列表刷新 ✓
8. **click** 切换排序方向按钮 ✓
9. **wait** 列表刷新 ✓
10. **evaluate** 列表可见无白屏 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 每次切换后列表仍可见且无白屏

判定：**pass**
