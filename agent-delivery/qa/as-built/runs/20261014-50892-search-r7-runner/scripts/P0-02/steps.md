# P0-02 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** 示例查询任一 chip（默认「人工智能」） ✓
3. **assert_visible** 搜索框 ✓

## expect 逐条

- ✓ 搜索框回填该示例词
- ✓ 页面维持初始引导态且无检索结果标题

判定：**pass**
