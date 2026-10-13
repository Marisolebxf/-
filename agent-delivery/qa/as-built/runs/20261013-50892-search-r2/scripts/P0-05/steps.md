# P0-05 逐步实际操作

1. 承接 P0-04：点击 .arco-drawer 关闭按钮 → 抽屉关闭，结果态保留（智能搜索结果标题仍在，36 复选框）
2. 定位 button.metric-spec-card（9 个可见，首卡竞争力列；aria-label=指标说明：综合竞争力得分）
3. scrollIntoView + click → popover 未出；补 dispatchEvent mouseenter/mouseover + click → .arco-popover 弹出
4. popover 内容确认：中文指标名「综合竞争力得分」+ 指标ID M_ENT_COMPETITIVENESS_SCORE + 口径定义/计算公式/源表
5. （核对口径）关闭后扫描结果列表可见文本：无 GAP- 前缀、无 Q0xx 字样
6. 判定：说明卡弹出含中文指标名 ✅、关闭后无缺口编号泄漏 ✅ → Pass
