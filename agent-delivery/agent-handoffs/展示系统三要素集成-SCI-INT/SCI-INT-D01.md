# SCI-INT-D01 handoff：测试策略与环境

- 任务：SCI-INT-D01 · 角色：agent:qa-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：北京久新
- ponytail: N/A（分析叶，不写业务代码）
- 日期：2026-10-19

## 1. 范围与实现

对照总派单 §4「D01 测试策略与环境」，以及展示系统三要素集成的测试策略范围（科技信息展示系统；本叶只定策略，不新增功能、不改业务仓）。

产物 `产物/SCI-INT-D01.yaml`：17 张卡，号段 `INT-D-X-001`…`INT-D-X-017`，`layer=test`，`dimension=[NONE_3E]`，`scope_count=17`，`card_count=17`，`gap: []`。

1. **001–013**：一一对应 13 个集成模式。`integration_pattern` 使用该模式编号，不另起一套。必测项由 B01 已有 `test_points` 改写，每条写明测什么、通过条件、失败时页面表现（空态、角标，禁止伪造数值）。
2. **014**：契约测试方式。对端用 Mock；对端测试环境可录制并脱敏回放；契约文件建议放在 `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/contracts/`，不进业务仓。本叶不出具体用例。
3. **015**：环境划分为 dev、联调、对端测试环境。lumen 调用链只走 `gkxlumen-platform-gateway` 到 `gkxlumen-*`，算法只到 `lumen-algo-py` / `lumen-etl-es-py` 的 `/internal`。禁止测试回落 `demo-svc-platform`、`demo-algo-*`（含 `demo-algo-science`）、`demo-svc-topic-py`。
4. **016**：测试数据。总派单写明用 Demo 库 `demo_gkxlumenx_*`、禁正式库；架构 D12 禁止 lumen 运行时读写 `demo_*`。两条都写入卡片，本叶不拍板。见决策项 **DN-D01-01**。
5. **017**：准入与准出。准入：契约文件可解析、Mock 可起、测试数据不是正式库。准出：该模式必测项全过，降级路径有证据，无伪造数值。

必须写入必测项的约束：

- 久新 API：鉴权失败、超时、熔断后为空态或最近快照加「数据更新中」；久新凭据只在 Python 侧，不到前端。
- 无来源：空态 + 待确认角标；禁止随机数或 fixture 填数充当通过。
- 异步任务：切条件不自动起任务；同用户同条件只一条在跑；当天已成功直接打开结果。同步推理同样不得因切条件自动发起。
- Mock 开关：`USE_MOCK` 关闭时禁止 fixture 填数。
- 图谱：只许 TRSGraph，禁止 Neo4j；禁止测试回落 `demo-algo-science`。
- 可观测：每张卡的必测项包含前端 observability、Java Agent、Python instrument 的 trace 校验点（某层不参与时，校验点是该层不应出现推理 span）。不写埋点代码。

快照测试只引用 B01 已有候选表 `ads_sci_result_snapshot`，不新开表，`structure_escalation` 全部为 false。

## 2. 偏离说明

- `card_count=17` 是策略卡张数，不是 93 个指标的逐条用例。逐接口用例、逐指标对账不在本叶。
- `algorithm_type` 沿用 B01 模式上已写的类型，本叶未重查指标目录。没有单一类型的卡写 `null`。`d1_d4` 写 `null`，不自填就绪度。
- 测试数据落点不裁断，只登记 DN-D01-01。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-D01.yaml`
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-D01.md`（本 handoff）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D01-check.py`

无业务仓改动。未 commit，未 push。

## 4. 验收证据

自检（PowerShell，工作目录 `gkx-orchestration`）：

`$env:PYTHONIOENCODING="utf-8"; python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/D01-check.py"`

结果：`OK`。差集 0。断言覆盖卡数 17、号段 1–17 连续、13 个模式编号各出现一次、无 TBD/skeleton、每张 `test_points` 非空、调用链文本不含 `demo-`。

本叶不改页面，未做浏览器走查。

## 5. 架构合规自检

- 调用链：策略要求前端只经 `gkxlumen-platform-gateway` 调 Java，Java 再调 Python `/internal`。本叶不改代码。✅
- Nebula：只许 TRSGraph（graphd `10.50.75.136:9669`），禁止 Neo4j。✅
- 算法只在 Python：推理、抽取、久新 API 适配都在 `lumen-algo-py`；Java 只读 ADS 或转发。✅
- D12：测试禁止回落原型平台与原型算法服务。正式链路不得把 `demo_*` 当数据源；与总派单 Demo 库字样的冲突记在 DN-D01-01，不在本叶拍板。✅
- 可观测：每条链路的必测项含前端、Java Agent、Python instrument 三类校验点，无埋点实现。✅

## 成本

- actual_tokens: 120000
- model_used: grok-4.7
- actual_cost: 2.50
- cost_warn: green

估算低于 $10 暂停线，因此未中止、未再扩写。

ponytail: N/A
