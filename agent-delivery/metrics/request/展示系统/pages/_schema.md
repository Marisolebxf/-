# 展示 A2.2 页面包产物 schema

每个子智能体只写 **一个** `pages/{page_id}.yaml`。禁止改总表、禁止改 seed、禁止覆盖半成品 xlsx。

态势模块按 **需规五级** 一页；其余展示模块按 **需规四级 / 产品四件套** 一页。

```yaml
version: 1
task: DS-ALGO-GAP-L01
page_id: DS-04-CITY
wave: DW4
updated: "YYYY-MM-DD"
ds_id: DS-04
level3: 科技发展态势
level4: 全球创新监测
level5: 城市创新能力分析   # 非态势叶可空
pack: agent-handoffs/产品整体定义/科技信息展示系统-完整详细设计/04-功能-科技发展态势.md
srs02: bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md
ponytail: off

semantic_layer:
  metric_open_status: present | missing | inherited_parent | n/a_documented
  metric_open_path: null
  pdr05: pass | fail | unknown
  pdr06: pass | fail | unknown
  trace_metrics: []
  wireframe_metric_ids: []
  algorithm_cards: []
  semi_xlsx_pages: []          # 半成品「页面」列匹配到的行，只消费不改 xlsx

demands: []                    # 同专题 _schema；metric_id 无则 null，禁止新造 M_*
semantic_debt: []
items: []
```

判定：先有语义层 ID（METRIC-OPEN / TRACE / WF 第6列 / 半成品已填口径），再对照 `A2-GAP-algo-catalog.yaml` 与 `srs/05`。

- B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*` 不得打 missing。
- 专题已 `missing` 的不重列；共有缺口 `缺口说明` 写 `also_in: TOPIC-…`。
- 半成品已标其它调用系统 → 默认 `other_system`。
- 教育核增默认 skip，不进本页。
