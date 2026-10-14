# P0-05 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **click** 指标说明：综合竞争力得分 ✓
6. **wait** 说明卡弹出（popover 可见） ✓
7. **assert_visible** 说明卡中文指标名 ✓
8. **press** Escape ✓
9. **wait** 说明卡关闭 ✓
10. **evaluate** 检查结果列表可见文本不含缺口编号前缀字样（GAP-/Q0xx） — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 弹出含中文指标名的说明卡
- ✓ 关闭后结果列表可见文本不含缺口编号前缀字样

判定：**pass**
