# SCI-INT-Z01 handoff

- 任务：SCI-INT-Z01 · 角色：agent:architect-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：久新
- ponytail: N/A
- 日期：2026-10-19

## 范围

汇总 A01–A15、B01–B09、C01–C05、D01–D04。一卡一行。源 yaml 未改。

## Sheet 行数

- 页面：386
- 指标：93
- 数据：205
- 测试：398
- 对端接口需求：51
- 决策项草案：687
- 风险：620
- 结构升级项：57
- 跨域指标：163
- 判据：6
- 勘误：63

## 判据

- 1：差集 0；P00 283；A 段覆盖 283
- 2：指标 93/93；模式不符 0
- 3：差集 0；B 引用 38；未消费 13
- 4：检查 366；空链路 0
- 5：应覆盖 273；覆盖缺 0；契约降级缺 0
- 6：说明已齐，会签未做
- 勘误：63
- 判据 6：说明已齐，会签未做

## 产物

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-集成依赖总表.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-集成依赖总表.xlsx`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-久新接口需求说明.md`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/Z01-merge.py`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/Z01-check.py`

未改业务仓。未 commit，未 push。未点 ready_to_sign，未点 done。

## 架构合规

- 调用链：前端 → Java REST → Python `/internal` → 久新 / ADS / TRSGraph。✅
- Nebula 只作 TRSGraph，graphd `10.50.75.136:9669`。✅
- 算法只在 Python。✅
- D12：正式落点列写 lumen-algo-py / gkxlumen ADS；演示服务名只留在勘误或风险。✅
- 可观测：沿用各卡已有埋点，本叶不新造。✅

## 成本

- actual_tokens: 180000
- model_used: grok-4.7
- actual_cost: 4.50
- cost_warn: green

ponytail: N/A
