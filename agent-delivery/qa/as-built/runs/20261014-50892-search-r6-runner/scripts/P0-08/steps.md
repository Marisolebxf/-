# P0-08 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓

## expect 逐条

- ✓ 页面再次呈现该次检索的结果标题与命中条数
- ✓ 智能搜索与查企业区无「查询方案」入口

判定：**pass**
