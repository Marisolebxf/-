# P1-15 逐步实际操作

1. 结果态（智能搜索「人工智能」命中 4493），浏览结果摘要卡
2. 定位「当前条件」最小容器（flex min-w-0 行）：内容 = `当前条件` label + 1 枚 arco-tag `智能输入：人工智能`
3. 检查 chip 可关闭性：tag outerHTML 含 `<!--v-if-->` 双插槽但无 icon-close 渲染 → hasClose=false
4. 全页扫描反馈文案：`已匹配|匹配字段|多字段|兜底` → 唯一命中在输入框 placeholder（`…自动关联多字段匹配企业`），结果区 0 命中
5. hero 区与条件区之间 HTML 解析：tags = [人工智能, 集成电路, 中兴, 中心, 中]（均为最近检索 chips，非匹配字段反馈）
6. 判定：预期两分支（已匹配字段可关 chip / 兜底文案）均未出现 → **Fail（C1）**
7. 截图存 screenshots/no-match-feedback.png
