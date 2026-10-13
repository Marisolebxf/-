# P0-08 · 勾选产业后筛选栏回显且看板按新条件刷新（00387）

1. 会话保持类型分析页；发现 P0-12 关抽屉后残留透明 mask（opacity 0 但占位 1206×1061）拦截坐标点击
   → CDP 置 .arco-drawer-mask display:none 后正常交互（现象记 retro R12）
2. 点击产业下拉（textbox 全部产业）→ 展开 multiple 选项面板（8 产业项）
3. 坐标点击 li 被面板 pointer-events:none 分组层拦截 → CDP DOM click 可见项「人工智能」
4. 核对：筛选栏回显 arco-tag「人工智能」；KPI 区块重新渲染（数据态 0/0/0）
5. 判定：回显 + 刷新 2 点满足 → Pass
