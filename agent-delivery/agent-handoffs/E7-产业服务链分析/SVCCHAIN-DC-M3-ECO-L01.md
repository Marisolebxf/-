# SVCCHAIN-DC-M3-ECO-L01 · Handoff

- 任务：`SVCCHAIN-DC-M3-ECO-L01`（长任务总控 `SVCCHAIN-合规演示用例-长任务总控.md` 段 M3b）
- agent / 监管人：doc-agent / human:徐滕强
- 日期：2026-11-07
- ponytail: full（无新依赖、无新代码；两份文档+本 handoff，公式与规则文本全部引自仓内真源不另造）
- 依赖门：M1 `SVCCHAIN-需规条目矩阵.md` §2.2 + M2 `SVC-数据调研-20261107.md`（均已落盘）✅

## 1. 范围与实现

产出两份文件（对照总控 §1.7 产物清单）：

1. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ECO-合规演示用例.md` — ECO 域 6 行覆盖表（8 列金样格式）+ 查库节 + 一条主路径 + 调度核对。
2. `agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ECO-LOOP计划.md` — 常驻验收单建议 ID `SVC-ECO-DEMO-ACCEPT-LOOP`（只登记不建单）、token 约定（`~/.gkx/topic-loop-token` + `systemCode: topic`）、一轮四步、缺口分类 DATA/QUERY/ALGO/ENV、每轮≤3 张（`SVC-ECO-DEMO-FIX-R{YYYYMMDD}-*`）、同缺口两轮停、报告路径 `agent-handoffs/E7-产业服务链分析/SVC-ECO-DEMO-ACCEPT-LOOP.md`（只追加）、状态行「覆盖已齐，未执行。等人说『按 LOOP 跑』」。

## 2. 6 行覆盖核对（M3 完成门）

| 需规序号 | 行 | 数据情况 | 期望值来源 |
|---|---|---|---|
| 7.4.1 全链路可视化呈现 | ✅ | 可演（演示态声明）；产业级切片另注覆盖不到（GAP-SVC-CHAIN-SEGMENT） | `SVC-20261105-014.result_payload.gap[]` 六行实测 + `demo_gkxlumenx_ads.svc_chain_gap` 现批次六行实测 |
| 7.4.2 瓶颈堵点智能识别 | ✅ | 可演（演示规则判定声明，Q-SVCCHAIN-03） | 同上截面；空白档=0 家环节（快照：技术转移+中试；现批次：中试）；as-built P0-07「演示规则判定」声明形态引用 |
| 7.5.1 关系网络构建 | ✅ | 可演（演示态声明）；产业切片另注（Q060/Q062/Q063） | `SVC-20261107-002.result_payload`（status=ads_ready、43,296/42,740、yellow_gaps 五项）+ `POST /svc/topic/v1/service/eco-graph` 契约（lumen paths.ts/types.ts） |
| 7.5.2 图谱探索与统计 | ✅ | 可演；影响力子项诚实缺失声明（GAP-SVC-GRAPH-INFLUENCE） | `svc_relation_chain` 全网行 density=0.000046 + 中心性 TOP5 实测（253/174/172/114/104）；矩阵 REQ-SVC-ECO-GRAPH-BUILD metrics=[] 未硬挂指标 ⓘ |
| 7.8.1 深圳服务链现状分析·统一评价框架 | ✅ | 可演（演示态声明口径，Q-SVCCHAIN-04） | `SVC-20261107-022`：sz_compare 框架名/caliber/metric_order + 深圳 14,080/77/0.000046/0.833 + own_gaps Q-SVC-010 |
| 7.8.2 横向对比分析 | ✅ | 可演（演示态声明口径） | 同上截面：五城市 cities 全值 + tier=T1·第一梯队（1/8）gauge 77 + narration 原文引用 |

调度核对合计：可演 6 / 覆盖不到 0 / 设计无资源 0；主路径只串可演行。6/6 零缺行。

## 3. 主路径摘要

复用已签发任务结果、不新起任务：① chain 工作区 INB1309 打开 `SVC-20261105-014`（六站地铁图 + 中试熟化空态 + 识别面板服务空白×2 + 演示规则判定声明）；② graph 工作区模式② `SVC-20261107-002`（43,296 节点/42,740 边、密度 0.000046、TOP5 首名深圳市创新投资集团 253、影响力诚实缺失）；③ shenzhen 工作区 `SVC-20261107-022`（框架卡 + 深圳 14,080/77/0.000046/0.833 + 五城市对比 + T1 第一梯队 1/8 + narration 同源）。

## 4. 查库证据（只读）

- 入口连接 `demo-gkxlumenx-ods`（组 gkx-mysql，主机 10.50.11.76，用户 gkxlumenx），跨库限定名 SELECT，零写操作，未 `--apply`。
- 实查清单：`demo_gkxlumenx_ads.svc_chain_gap`（15 列结构 + 6 行全值）、`demo_gkxlumenx_ads.svc_relation_chain`（51 行内全网行 + TOP5 + weights.edge_map）、`demo_gkxlumenx_dwd.svc_org_graph_hang`（COUNT/DISTINCT：43,296/43,296/1 空间/1 tag）、`gkxlumenx_topic_enterprise.analysis_task`（三类 success 任务近 12 条 + 三条代表任务 `target_params.result_payload` 逐键解析：gap[]/sz_compare/tier/shenzhen/own_gaps/narration/relation_summary/relation_top/density_formula/yellow_gaps）。
- SQL 方言受阻 1 次（`SHOW COLUMNS` 不兼容 MCP LIMIT 注入 → 改 information_schema），非数据受阻；其余查询一次通过。

## 5. 偏离说明

1. **接口地址前缀**：任务类接口写 `GET /api/topicAsync/topic/v1/analysis/tasks/{taskId}/result?user_id=guest`（金样《深圳政策现状分析-合规演示用例》同款，真源 `lumen-ui-topic/src/api/enterprise/paths.ts` TOPIC_ASYNC_V1=`/topicAsync/topic/v1`）；图谱面写 `POST /api/svc/topic/v1/service/eco-graph`（真源 `src/api/service/paths.ts` SVC_TOPIC_V1=`/svc/topic/v1`，注释明示「禁止 /api/svc」指 `SVC_TOPIC_V1` 常量值本身勿写成 /api/svc，完整 URL 前缀网关 /api）。如网关路由与本文前缀不符，按 LOOP 探测 404 分支处理（ENV，不判补数缺口）。
2. **深圳域期望以专题系统线上载荷为准**：demo-ui-topic 沙箱为另一套确定性演示基准（五城市 1,240/460/1,580/1,350/890、梯队三档规则），与 lumen 实态（对标表 8 城、深圳 14,080、T1·1/8）并存。用例/LOOP 对照物统一取专题系统（matrix §2.2 ECO 行的真源锚点即 lumen 路由），沙箱基准在两文中的差异已显式声明，不混用。
3. **「覆盖不到」0 行的判定**：总控要求「现有数据演不到的行写覆盖不到」。本域 6 行页面主链路均有真实数据可演（六环节行、图谱行、深圳对比行俱在），产业级切片/图谱产业维度/影响力评分三项子能力演不到——以缺口声明并入对应行内（数据情况列注明），不另立行也不改判整行；依据 M2 §8（缺口为「维度层」而非「行层」）。若监管人判定应整行降级「覆盖不到」，改动限于覆盖表数据情况列，一行一改。
4. **as-built 历史文件不改写**：P0-07（2026-10-15 结果态无环节行）与 P0-08 `ENV-SVCGRAPH-HANG-EMPTY-001`（hang 0 点 0 边）两项环境债已被 11 月批次覆盖（svc_chain_gap 现批次六行、graph 任务 ads_ready 且节点边非零）；用例文头声明「按当前实查写、不改写历史」，实勘目录零改动。
5. **svc 表无 is_mock 列**：演示态由 `q061_pending_client`/`pending_client_confirm`/`runtime_flag`/`rule_version` 承载，覆盖表未写 `is_mock=1`（M2 §0.4/§8.6 口径）。

## 6. 产物清单

- `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ECO-合规演示用例.md`（新增）
- `agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ECO-LOOP计划.md`（新增）
- 本 handoff（新增）
- 未建 LOOP 验收单（task-query 复核 `SVC-ECO-DEMO-ACCEPT-LOOP` 不存在）、未派修数单、未跑 LOOP 轮次、未改 registry seed/业务仓/as-built 历史文件。

## 7. 缺口引用清单（零新造编号）

Q-SVCCHAIN-02 / 03 / 04 / 08、Q060 / Q061 / Q062 / Q063、Q-SVC-010、Q-SVC-011（未直接引用，列入 LOOP 既有集合）、GAP-SVC-CHAIN-SEGMENT、GAP-SVC-CHAIN-BOTTLENECK、GAP-SVC-GRAPH-INFLUENCE、GAP-SVC-SZ-CHAIN-COMPLETENESS。

## 8. 架构合规自检

| 项 | 判定 |
|---|---|
| D12 demo/lumen 隔离 | ✅ 未改任何业务仓代码；只读消费 lumen-ui-topic / demo-ui-topic 源码作契约与枚举真源 |
| 只读库 | ✅ 全程 SELECT/information_schema，零写表，未 --apply |
| 不造数 | ✅ 期望值全部来自库实查/已签发任务载荷/前端确定性数据集引用，逐值注明来源；无编造数值 |
| 不建 LOOP 单 / 不跑 LOOP / 不派修数单 | ✅ 建议 ID 只写进计划；状态行保留 |
| 历史文件不改写 | ✅ as-built 实勘、既有 POL/深圳政策产物零改动 |
| cicd: skip | ✅ 纯编排仓文档，无 CI 触发 |
| commit 规约 | ✅ 本任务不 commit（铁律禁止 git commit/push）；落盘停在本地工作区，由监管人确认后处理 |

## 9. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ≈180,000（input+output 估算，会话级读表为主） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.20（估算，<$10 阈值） |
| cost_warn | false |
