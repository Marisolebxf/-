# P1-07 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** tab 查企业 ✓
3. **evaluate** 确认查企业下可见热门场景 — (observed 面，见截图/expect) ✓
4. **click** 热门场景任一 chip ✓
5. **wait** 高级筛选结果 ✓

## expect 逐条

- ✓ 页面进入高级筛选结果而非停留查企业结果
- ✓ 出现该场景条件摘要

判定：**pass**
