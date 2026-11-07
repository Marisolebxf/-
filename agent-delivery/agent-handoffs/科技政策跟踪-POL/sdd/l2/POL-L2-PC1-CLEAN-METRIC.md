# POL-L2-PC1-CLEAN-METRIC · 政策数据治理 · 系统引用政策源数据清洗 · 后台指标设计

- 任务：`POL-L2-PC1-CLEAN-METRIC`
- 日期：2026-11-08
- 监管：`human:淮政玮`
- 认领：`agent:algorithm-agent`
- 强度：ponytail off
- 上游：`POL-L2-PC1-CLEAN-ARCH.md`、`sdd/指标与501.md` 治理节、总控 §1.2
- SRS：**602**

## 1. 挂接结论

| 展示点 | metric_id | 判定 | 说明 |
|---|---|---|---|
| 页眉「库内政策数」 | `M_POLICY_TOTAL_COUNT` | 可接统计读面 | STAT；D4=mock；对齐前数值仍 mock。不替代清洗质量 |
| 清洗质量聚合 / 明细 | （无） | 跨项索引呈现 | 按 `script_state.status` 行聚合。**不新造**清洗质量指标 |
| `M_POLICY_VALIDITY_RATE` | — | **不挂** | 口径是有效率、挂点在全景；禁止改挂治理清洗 KPI |

未注册模型不在本叶。不写可算出数的假公式。不改 D4。

## 2. 三档

- 可接：仅页眉附卡 `M_POLICY_TOTAL_COUNT`
- 501：无（602 同步读面，不因未见清洗模型改 501）
- 跨项索引：质量计数与明细

## 3. 明确不做

不注册新 `metric_id`；不把有效率指标挪到本页；不把 D4 改绿。
