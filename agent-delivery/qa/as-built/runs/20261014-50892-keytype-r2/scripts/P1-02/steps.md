# P1-02 · 显示热力开关可关闭与重开且热力层随之变化（00393）

1. 地图默认态：switch「显示热力」aria-checked=true
2. 合成 click 不触发 React 受控 switch（多次尝试 st 不变）→ 改真实 ref click
3. 真实 click 开关 → aria-checked=false（热力关）；snapshot 复核 states 无 checked
4. 再次真实 click → aria-checked=true（热力开，恢复；终态不污染后续）
5. 判定：关 / 重开 2 点满足 → Pass（零数据态像素不核，按开关状态与图层增删 DOM 判定）
