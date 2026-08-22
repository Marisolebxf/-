# 专题 A2 页面包产物 schema

每个子智能体只写 **一个** `pages/{page_id}.yaml`。禁止改总表、禁止改 seed、禁止覆盖半成品 xlsx。

```yaml
version: 1
task: TOPIC-ALGO-GAP-L01
page_id: CHAIN-TOPIC-PANORAMA
wave: W1
updated: "YYYY-MM-DD"
pack: agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-TOPIC-PANORAMA-产业链全景图谱/

semantic_layer:
  metric_open_status: inherited_parent | present | missing | n/a_documented
  metric_open_path: "..."
  pdr05: pass | fail | unknown
  pdr06: pass | fail | unknown
  trace_metrics: [M_CHAIN_NODE_COUNT]
  wireframe_metric_ids: []
  algorithm_cards: []          # 路径；无则 []

# A=库缺口 B=语义欠账 C=已覆盖
demands:
  - demand_id: PAN-D01
    metric_id: M_CHAIN_NODE_COUNT   # 无正式 ID 则 null，禁止新造 M_*
    metric_name_zh: 产业链节点数
    source: METRIC-OPEN | TRACE | wireframe_col6
    差集判定: mapped | missing | third_party | other_system | n/a_ops
    A1需规ID: null                  # A1 未交则空
    algo_lib_leaf: "产业链/深度分析.md#产业链全景模型构建"
    metric_id_impl: M_CHAIN_NODE_COUNT
    缺口说明: null                  # missing 必填；B 类写语义欠账原因

semantic_debt: []                   # B 类：页上有统计/评估但无 METRIC-OPEN 有据

items: []                           # 可选：按 A2-GAP-schema 15 列展开的本页行
```

判定：先有语义层 ID，再对照 `metrics/request/A2-GAP-algo-catalog.yaml` 与 `srs/05`。B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*` 不得打成 missing。
