# P0-04 逐步实际操作

1. 会话保持类型分析页（地图视图默认态），CDP 确认 .leaflet-container=true
2. 点击 button「列表视图」→ CDP 复核：.leaflet-container=false（地图容器不再展示）；
   空间分布区出现「当前区域暂无可展示对象」（默认筛选零数据 → 列表空态，顺带覆盖 P1-09 场景）
3. 点击 button「地图视图」→ CDP 复核：.leaflet-container=true，空态文案消失
4. 核对往返后筛选四组默认值保持 + H3 区域洞察/清单按钮保持
5. 判定：互斥 / 恢复 / 状态保持 3 点全部满足 → Pass
