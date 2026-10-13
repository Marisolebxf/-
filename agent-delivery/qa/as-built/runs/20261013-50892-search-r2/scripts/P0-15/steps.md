# P0-15 逐步实际操作

1. 结果态第 1 页，click 第 1、2 张卡复选框 → 批量条「已选 2 家」
2. click .arco-pagination 第 2 页项
3. 核对：批量条消失（已选文案 0 处）、checkedNow=0、第 2 页 9 卡、activePage=2、URL 不变
4. 判定：已选计数条消失/清零 ✅ + 勾选不跨页 ✅ → Pass
