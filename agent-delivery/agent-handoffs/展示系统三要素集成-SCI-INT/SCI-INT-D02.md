# SCI-INT-D02 handoff：契约测试用例集

- 任务：SCI-INT-D02 · 角色：agent:qa-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：北京久新
- ponytail: N/A
- 日期：2026-10-19

## 范围

A01–A15、B02–B09 中 counterpart 不是 none / null / 空的源卡 273 张，各 1 张测试卡。B04 命中 0，未编用例。差集 0。`scope_count=273`，`card_count=273`，`gap: []`。号段 `INT-D-X-100`…`INT-D-X-372`。

按模式：IP-01 69、IP-02 5、IP-04 7、IP-05 15、IP-06 16、IP-07 22、IP-08 60、IP-09 62、IP-10 10、IP-11 1、IP-12 3、IP-13 3。

## 产物

- `产物/SCI-INT-D02.yaml`（由 `产物/_work/D02-build.py` 生成）
- `产物/_work/D02-check.py`
- 本 handoff

未 commit，未 push。未改业务仓。

## 自检

`$env:PYTHONIOENCODING="utf-8"; python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D02-check.py"`

结果：覆盖数 273，OK。差集 0。

## 架构合规

- 调用链：测试卡照抄源卡 `call_chain`（前端 → Java → Python `/internal`）。✅
- 禁止 demo-：降级用例写明禁止回落 `demo-algo-science` / `demo-svc-*` / `demo_*` 库；出现 `demo-` 时同时有「禁止」。✅
- 空态不伪造数值：IP-10 正常项改为空态；降级为空态加角标，禁止伪造数值。✅
- 可观测：用例文本含 `trace`。✅

## 成本

- actual_tokens: 100000
- model_used: grok-4.7
- actual_cost: 2.00
- cost_warn: green

未超过 $10，未中止。
