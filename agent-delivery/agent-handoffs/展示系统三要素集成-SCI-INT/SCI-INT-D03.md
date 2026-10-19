# SCI-INT-D03 handoff：数据对账与就绪度升级标准

- 任务：SCI-INT-D03 · 角色：agent:qa-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：久新
- ponytail: N/A
- 日期：2026-10-19

## 范围

B02–B09 源卡 93，对账卡 93，差集 0。号段 `INT-D-X-400`–`INT-D-X-492`。无法对账 7 条（IP-10，均写了 reason）。

产物 `产物/SCI-INT-D03.yaml`。`layer=test`。`reconcile` 含方法、容差（草案，未拍板）、证据格式、就绪度、升级路径 `mock→ingesting→live`、主键命中率。物理名只按 int_id 查 C05 `canonical.physical`。`demo_` 库不得作为通过条件。D4=mock 的对账结果未写成 live。本批无 D3=none。

## 产物

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-D03.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D03-build.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D03-check.py`
- 本 handoff

未 commit，未 push。

## 验收

`$env:PYTHONIOENCODING="utf-8"; python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D03-check.py"`

结果：`OK`。差集 0。本叶不改页面，未做浏览器走查。

## 架构合规

- 调用链：对账标准只读 ADS / 父快照 / 图投影，不改代码。✅
- Nebula：IP-05 对图投影行数与 ADS；不写 Neo4j。✅
- 算法只在 Python：本叶不写算法。✅
- D12：`demo_` 库不得作为通过条件。✅
- 可观测：本叶不改埋点。✅
- D9：升级路径 mock→ingesting→live；D4=mock 不写成 live；主键未齐先不计通过。✅

## 成本

- actual_tokens: 140000
- model_used: grok-4.7
- actual_cost: 2.90
- cost_warn: green

低于 $10，未中止。

ponytail: N/A
