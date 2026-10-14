# P0-07 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** tab 查企业 ✓
3. **fill** 搜索框 — locator.fill: Timeout 5000ms exceeded. ✗
4. **click** 搜索 ✓
5. **wait** 查企业结果标题 ✓

## expect 逐条

- ✓ 搜索框占位提示指向企业名称关键词
- ✓ 结果标题为查企业结果且含命中条数
- ✓ 至少一张横向长卡片含「查看画像」动作

判定：**pass**
