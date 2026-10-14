# P0-09 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** tab 高级筛选 ✓
3. **assert_visible** 字段库区域 ✓
4. **evaluate** 无条件时点应用筛选，记录禁用/无结果两种形态之一 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 字段库呈现「企业所属地区」「经营状态」等字段标签
- ✓ Footer 含「保存为查询方案」「使用查询方案」「清空条件」「应用筛选」
- ✓ 无条件时「应用筛选」为禁用或点击无结果

判定：**pass**
