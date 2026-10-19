# SCI-INT-D04 handoff：端到端链路与非功能

- 任务：SCI-INT-D04 · 角色：agent:qa-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：久新
- ponytail: N/A
- 日期：2026-10-19

## 范围

A01–A15 各 1 条端到端用例，共 15 条。号段 `INT-D-X-600`–`INT-D-X-614`。全景展示/维护、全球监测两半、4 个人才子页各自一条。

`scope_count=15`，`card_count=15`，差集 0。

代表卡：该叶第一张 `call_chain.java` 非空的卡。本批 15 叶均有非空 Java，未出现「链路未实现」。

## 产物

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-D04.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D04-build.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D04-check.py`
- 本 handoff

未改业务仓。未 commit，未 push。

## 验收

`$env:PYTHONIOENCODING="utf-8"; python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D04-check.py"`

结果：`OK`。差集 0。

## 架构合规

- 调用链：前端 observability → Java 网关 → Python `/internal`；无在线 Python 的读链标明 Java 读 ADS。✅
- 算法只在 Python；Java 不写推理。✅
- D12：超时或上游失败 → 空态 + 角标，禁止伪造数值，禁止回落 `demo-algo-science` / `demo-svc-*` / `demo_*`。✅
- 可观测：每张卡含前端、Java、Python 三处检查点名称（不适用处写明）。✅
- 超时预算与性能只标草案、待确认。✅

## 成本

- actual_tokens: 100000
- model_used: grok-4.7
- actual_cost: 2.50
- cost_warn: green

ponytail: N/A
