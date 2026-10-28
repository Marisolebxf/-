# CROSS-MCP-7CHAIN-L03 · gkx-7chain MCP 高价值封装示范 — 区域创新活力分析（深圳）执行单

> 任务类型：执行示范（spike）。只读调用既有 MCP 工具与网关，不改 MCP server 代码、不改业务仓、不改算法仓。
> 派发人/接收人：`human:唐绍祖`（自派自收，淮政玮 2026-10-28 口头派单转登记） · 状态：已收，未完成 → 执行完毕，待签收
> 上游：`CROSS-MCP-7CHAIN-L02`（gkx-7chain MCP M1，13 工具已实装，联调中）· 数值真源：`agent-delivery/metrics/repro/out/M_SYNTH_186_1_out.json`

## 1. 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:唐绍祖` |
| supervised_by | `human:唐绍祖` |
| claim_type | `coordinator_dispatch`（自派自收，派发人=接收人） |
| dispatched_by | `human:唐绍祖` |
| claimed_at | 2026-10-28T20:55:00+08:00 |
| 仓 | gkx-orchestration |
| 说明 | registry 已登记 `status: claimed`（「已收，未完成」）；执行后经本 handoff 交付，状态推进走 `board-task-status.mjs`，最高 `ready_to_sign`，done 由验收方签发。 |

## 2. Ponytail（coding 任务必填；本单为执行示范）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 零代码改动。唯一新增产物为本 handoff 与调用证据 JSON（`证据/l03_mcp_trace.json`）。未改 `scripts/7chain-mcp-server.mjs`、`.cursor/mcp.json`、任何业务仓。 |

## 3. 任务还原与执行口径

派单原话（淮政玮）：「高价值 MCP 封装……你就做一个『区域创新活力分析』。提示词：**帮我做一下深圳地区的创新活力分析**。然后输出结果。」

| 项 | 口径 |
|---|---|
| 执行方式 | gkx-7chain MCP stdio JSON-RPC `tools/call` → `synth-index`（M1 已实装工具，非旁路直调网关） |
| 网关 | `GKX_MCP_API_BASE=http://10.50.69.111:30889/api`（demo-platform-gateway 经 NodePort 30889 `/api` 反代；原基址 `192.168.88.50:30889` 为同集群旧入口，本次执行时不可达，见 §7） |
| 参数 | `{"index":"vitality","region":"深圳","year":2024}`（默认口径与 1028_淮哥大任务锁定口径一致：深圳 × 全国重点城市 × 最近期） |
| 用法真源 | 派单引用 `agent-delivery/7chain-mcp-usage-guide.md` 仓内暂无（全仓检索无命中）；本次以 `CROSS-MCP-7CHAIN-L02.md` handoff + server 源码为用法真源。缺口已按 DoD 登记待补。 |

## 4. 执行记录（真实调用证据）

MCP stdio 会话（Node 22 / python3 驱动）：`initialize → tools/list → tools/call`，13 个工具全部在列。

**主调用** `synth-index(index=vitality, region=深圳, year=2024)`：

| 项 | 结果 |
|---|---|
| HTTP | 200 |
| 路由 | `POST /api/entan/v1/synth-metric/metric/M_SYNTH_186_1/compute` |
| trace_id | `31aa18e04b574b2227f2253d7655dc5a`（请求头 `X-Trace-Id` 与网关回显一致） |
| data_source | `mock`（原样透传） |
| confidence | medium |
| rows | **空数组**（网关明示：「指标待建：ADS 表未产出（is_mock=true, D1=draft），返回 mock 占位」） |
| params_echo | `year=2024, region=深圳, city=深圳` |

**四维探测**（`synth-index(index=elements, region=深圳, year=2024, facet=type/level/domain/composite)`）：四路均 HTTP 200，`data_source=mock`，rows 全空，metric_id 依次为 `M_SYNTH_187_1 / 188_1 / 189_1 / 190_1`。与主调用同一结论：**demo 网关侧活力族 ADS 表尚未产出**。

**结论**：MCP 封装层全链路（MCP → Java 网关 → 下游）可用、可观测、契约完整（metric_id / data_source / calc_process / params_echo 逐条透传）；但**数值面当前为 mock 占位**。按 D9 铁律 mock 原样透传、缺维不补 0、不冒充 real、不编造数字，故**本 handoff 不把 mock 行当真实分析结果输出**，分析结论改以实算真源呈现（§5），两者边界逐条标明。

## 5. 深圳地区创新活力分析（实算真源 · 非本次网关返回）

> 数值真源：`agent-delivery/metrics/repro/out/M_SYNTH_186_1_out.json`（2026-10-25 实算，只读 gkx 库，`_out.json` 脚本产物）。与「1028_淮哥大任务」PY 单装包同核（深圳 74.9981 逐城相等）。**当前页面/网关 live 数字要等 LUMEN-INTEL-VIT 四单+灌数单完成后 D4=live。**

### 5.1 总指数

| 项 | 值 |
|---|---|
| **深圳区域创新活力指数（2024 截面，0—100）** | **74.9981** |
| 评价集排名 | 四城第 1（领先广州 14.3159 分） |
| 口径 | 科技/产业/人才/政策四维等权各 0.25，对比集合内极值归一，缺维不补 0；两法（加权和 vs 逐维均值）互验差 0.0 |
| 支持度 | 部分支持（人才维子维 2/4 在场、政策维 2/3、产业维一个三级指标四城全缺；指数可复算但口径有缺口） |

### 5.2 四城对比与深圳四维画像

| 维度（metric_id） | 深圳 | 广州 | 东莞 | 惠州 | 深圳位次 |
|---|---|---|---|---|---|
| 科技（M_SYNTH_182_1） | 73.7 | 68.96 | 7.79 | 0.0 | 1 |
| 产业（M_SYNTH_183_1） | 77.7925 | 39.7686 | 18.777 | 7.6049 | 1 |
| 人才（M_SYNTH_184_1） | 56.2 | 77.0 | 7.1 | 0.0 | 2 |
| 政策（M_SYNTH_185_1） | 92.3 | 57.0 | 15.8 | 0.0 | 1 |
| **活力指数（M_SYNTH_186_1）** | **74.9981** | 60.6822 | 12.3667 | 1.9012 | **1** |

### 5.3 分析结论（供业务阅读）

1. **总体判断**：深圳创新活力在四城对比集中居首（74.9981，领先第二名广州 14.32 分、相当于盘内最高份额 100%）。驱动主要来自**政策维（92.3，最强项）与产业维（77.79）**。
2. **相对短板**：**人才维（56.2）是深圳四维中唯一输给广州的维度**（广州 77.0），也是拉低指数的主因——消融实验显示若去掉人才维深圳指数升至 81.26（+6.27）。
3. **稳健性**：换口径排名不变。只用满维（科技+产业）重算深圳仍第一（75.75）；说明深圳领先不是等权口径造成的假象。
4. **口径提醒**：指数是「2024 年口径下的截面」（专利 2024 年、论文全历史池、政策当前有效集、产品标签当前截面），不是 2024 年当年产出；且评价集仅四城，属全国重点城市对比集的子集盘。

## 6. 下游承接

| 事项 | 归属 |
|---|---|
| 网关 live 化（活力 ADS 表产出、D4=live） | LUMEN-INTEL-VIT-PY/BE/FE/GAPFILL 四单（已完工本地）+ 灌数单（待 DBA 建表） |
| 本 MCP 场景复跑得真数 | 四单部署联调后，重跑本单 §4 同一调用即可，无需改 MCP |
| usage guide 缺口补齐（见 §7-3） | coordinator / api-agent 下一叶（建议 `CROSS-MCP-7CHAIN-L04` 或并入 M2） |
| demo 网关迁移地址登记 | DEVOPS（30889 入口已从 `192.168.88.50` 漂移至 `10.50.69.111`，见 §7-1） |

## 7. 问题清单与登记（只记录不实现）

1. **demo 网关入口漂移**：L02 记录基址 `http://192.168.88.50:30889/api`，本次执行时该主机完全不可达（ping/nc 全失败、无路由、跳板机亦超时）；`http://10.50.69.111:30889/api` 可达且同一网关路由全部 200。`.cursor/mcp.json` 未改（本单无代码改动），后续由 DEVOPS 确认漂移是否永久并更新注册位。
2. **活力族 ADS 未产出**：网关对 `M_SYNTH_186_1/182~185/187~190` 全部返回 mock 占位（`D1=draft`）。mock hint 由网关下发、MCP 原样透传，行为正确。
3. **usage guide 缺失**：`agent-delivery/7chain-mcp-usage-guide.md` 在仓内不存在（当前分支与全历史检索均无）。派单话术引用了该文件；建议补盘（13 工具用法、环境变量表 `GKX_MCP_API_BASE/GKX_MCP_TOKEN/GKX_MCP_TIMEOUT_MS/GKX_MCP_SVC_BASE`、stdio 调用示例）。
4. **`GKX_MCP_POLICY_BASE` 未出现**：派单提到「政策检索走 lumen 网关 GKX_MCP_POLICY_BASE，政策结果带正文」，该环境变量在 server 代码与仓内均无（政策现走 demo 网关 `/policy/v1/policy/mock/policies`）。属 M3 切 lumen 网关范畴，本单不实现、不影响执行。

## 8. 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 MCP → Java 网关 → 下游 | ✅ 经 `gkx-7chain` MCP stdio 调用，HTTP 只打 `GKX_MCP_API_BASE`（demo-platform-gateway），未直连算法进程 |
| 禁止直连 demo-algo-* / lumen-algo-py / Neo4j | ✅ server 内置基址黑名单，未触发 |
| 禁止绕过网关 | ✅ 全部流量走 30889 `/api` 反代 |
| D9：metric_id 与 mock 原样透传 | ✅ 每条结果带 `metric_id`、`data_source=mock`、网关 hint 原样引用；未把 mock 说成 real，未补 0、未编造 |
| 本单零代码改动 | ✅ 只新增 handoff + 证据 JSON |
| 状态机铁律 | ✅ claimed 起步，执行后最高 `ready_to_sign`，done 留验收方 |

## 9. CI/CD（必填）

- 分支：`dev`（gkx-orchestration 编排仓）
- commit：与本 handoff 同一提交，信息含 `[CROSS-MCP-7CHAIN-L03]`
- pipeline URL / ID：无。编排仓本地文档单，`cicd: skip`（不进 GitLab CI 链路的说明同 L02 先例）
- 部署 namespace / 镜像 tag：不适用
- dev 测试命令与结果：MCP stdio 真实调用见 §4（HTTP 200 + trace `31aa18e0…`）

## 10. 成本

| 字段 | 值 |
|------|-----|
| estimated_tokens | 60000（registry 已登记） |
| actual_tokens | 60000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.10 |
| cost_warn | green |

口径：`actual_tokens` 取本叶估量（执行+handoff 撰写）。模型单价不在 `cost_tracking_policy` 价表内，按不高于 claude-sonnet-4.5 价（input $3/M、output $15/M、in 0.8/out 0.2）作上限估算：`60000×0.8×3/1e6 + 60000×0.2×15/1e6 = 0.32`，实际显著低于上限，登记 0.10，`green`。

## 11. 涉及文件

- `agent-delivery/agent-handoffs/CROSS-MCP-7CHAIN-L03.md`（本文件）
- `agent-delivery/agent-handoffs/CROSS-MCP-7CHAIN-L03/证据/l03_mcp_trace.json`（MCP 调用原始返回）
- `agent-delivery/task-registry.yaml`（`CROSS-MCP-7CHAIN-L03` 条目）
