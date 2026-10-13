# P1-08 · 零匹配时清单抽屉空态且全选与对比篮动作状态正确（00401）

1. goto `/enterprise/key-enterprise-analysis?view=type`；默认筛选下「查看企业清单（0）」→ 天然零匹配态（N=0）。
2. 点击「查看企业清单（0）」（ref e17），抽屉打开（snapshot 出现 Close e79 / 搜索框 e80 / 加入对比篮 e82 disabled / 全选当前结果 e83）。
3. CDP 核验抽屉：
   - 空态 = `arco-empty` 组件，主文案「当前搜索条件无匹配企业」；
   - 「全选当前结果」checkbox：`arco-checkbox arco-checkbox-disabled`；
   - 「加入对比篮」：`button.disabled=true`，class 含 `arco-btn-disabled`；
   - 「打开对比篮」：`button.disabled=false`，正常态 class。

判定：三条预期（空态文案 / 全选与加入禁用 / 对比篮入口可用）均成立 → Pass（非 N/A：默认态即零匹配）。
