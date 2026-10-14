# P0-06 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** 热门场景任一 chip ✓
3. **wait** 高级筛选结果标题或明确空态 ✓

## expect 逐条

- ✓ 页面切换为高级筛选且出现该场景条件摘要
- ✓ 结果标题为高级筛选结果且含命中条数或明确空态
- ✓ 高级筛选页无蓝色搜索主视觉

判定：**pass**
