# 派单说明 · SYSINT-03-04B-L01

查单时间：2026-10-23。只生成话术，未认领、未改注册表。

## 派单前

本单注册表状态是 `ready`，`claimed_by` 为空，监管人按备注为 `human:淮政玮`。现在不要 `task-claim`，不要开工。

1. 2026-10-23 已去掉对 `SYSINT-SCHEME-03-L01` 的 `depends_on`。该方案单仍是 `in_progress`，不再挡住本单认领。
2. WBS-03-04b 另写依赖 `PORTAL-CMS-METRIC-COVER-L01` 政策段。该单当前 `claimed`（`claimed_by` / `supervised_by` 均为 `human:唐绍祖`），政策段未完成。注册表 `depends_on` 没有这一条。方案第 4 段写明政策扶持与指标库逐条对齐还没有。
3. 注册表执行人是 `algorithm-agent`，仓是 `lumen-algo-py`。WBS 写的仓是 `lumen-ui-topic`、专题 Java、`lumen-algo-py`，协作人是 `frontend-agent`、`api-agent`。下面这段 `/goal` 只派算法。页面空态和 Java 读接口不在本会话改。菜单注册在 `SYSINT-03-18-L01`。八个菜单的相对路径方案里仍是还没有，本单不编路径、不写主机名。
4. 契约 `PORTAL-CMS-政策扶持.md` 仍是草案。按草案消费，不改字段。
5. `M_POLICY_INTENSITY_SCORE` 种子里已有，`pending_ref` 为 `QPOL-02`（待甲方）。本单不改种子、不改就绪度矩阵、不把权重写成已定稿。
6. 2026-10-23 `metric-query`（domain=政策）返回 35 条，全部是种子有、就绪度矩阵无。本叶缺项以契约和 WBS 为准。种子里的相近 ID 写进缺项表，不写成已对齐。

`M_POLICY_INTENSITY_SCORE` 在 `lumen-algo-py` 已有计算入口：`vendor/entan-py/polan/eval/intensity.py`，目录项在 `vendor/entan-py/polan/metrics/catalog.py`。正式链路只用 `lumen-algo-py` 的 `/internal/*`。目录里 `algo_server_location` 仍指向 `demo-algo-ent-analysis`，实现时不得把 Java 或前端指到 demo 服务。

## 话术

```text
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法工程师。算法只在 Python，结果可复现，口径只消费指标库。本单不新编 metric_id，不替甲方拍板 QPOL-02。
强度：ponytail full（默认）。禁止用 YAGNI 跳过可观测、调用链和架构铁律。禁止跳过缺口空态去补假数。
上下文：headroom 推荐（MCP 按需 compress 大日志/检索；有 Proxy 则保持常驻）。禁止用压缩替代契约、方案、WBS 和指标口径原文。未挂载可跳过，handoff 注明 headroom: skip。
图：必含 SYSINT-SCHEME-03-SEQ。统计数字的计算只在 Python /internal/*，Java 只读 ADS。不另画全局拓扑。先对上方案 §2 时序再改代码。

任务：SYSINT-03-04B-L01
标题：政策扶持指标页（WBS-03-04b）
Epic：E-PM-DELIVERY
监管人：human:淮政玮
执行：agent:algorithm-agent
仓：${GKX_ROOT}/repos/lumen-algo-py，分支 dev。只改这个仓。
协作人登记为 frontend-agent、api-agent。本会话不改 lumen-ui-topic，不改专题 Java，不改 gkx-orchestration 的方案和 WBS。
开始时间：无开始时间。完成日期要求：2026-11-05。这是计划日期，不是对端承诺。
预估：estimated_tokens 80000；effort_points 5；difficulty L。

开工前用 MCP task-get 再核对本单。注册表已无 SYSINT-SCHEME-03-L01 依赖。COVER 政策段仍须已有核对结论，未满足就停，不要 task-claim。禁止读 task-registry.yaml。

目标：政策力度排名只消费已有的 M_POLICY_INTENSITY_SCORE。省级、城市都没有单独的排名 ID，按该评分聚合，不另注册排名 ID。下面缺项清单里的行，接口不返回数。CMS 不提供名次，不提供力度分，算法不接受 CMS 覆盖分。

政策维度缺项（2026-10-23 用 MCP metric-get / metric-query 核对。handoff 必须原样列出这 10 行，结论保持「缺口」。种子有相近 ID 的，写出 ID 和不能顶替的原因。不得改种子，不得把矩阵未覆盖写成已对齐）：

1. stats · 全国政策数量及连续性。缺口。禁止顶替：M_POLICY_TOTAL_COUNT（政策总数，种子有、矩阵无）、M_POLICY_TIMESERIES（含发布量，连续性公式仍是 pending_algorithm，矩阵无）、M_POLICY_OPPORTUNITY_COUNT（政策机遇数，不顶替数量）。
2. stats · 省级政策数量及连续性。缺口。禁止顶替：M_POLICY_LEVEL_DIST（按国/省/市/区层级计数，不是省级数量加连续性）、M_POLICY_TOTAL_COUNT、M_POLICY_TIMESERIES。
3. stats · 市级政策数量及连续性。缺口。禁止顶替与第 2 行相同。
4. map · 全国发布密度。缺口。没有发布密度 ID。禁止顶替：M_POLICY_NATIONAL_DIST（按省的政策计数与占比，不是发布密度；种子有、矩阵无）。
5. map · 省发布密度。缺口。没有发布密度 ID。
6. map · 市发布密度。缺口。没有发布密度 ID。
7. coverage · 产业链节点上的政策覆盖。缺口。禁止顶替：M_POLICY_INDUSTRY_COVERAGE（种子有「政策产业覆盖度」，公式 pending_algorithm，矩阵无，需求来源空）。COVER 未完成前不把它写成节点覆盖已对齐。
8. shenzhen · 深圳政策数量及趋势。缺口。禁止顶替：M_POLICY_SZ_DIST、M_POLICY_TIMESERIES、M_POLICY_TOTAL_COUNT。
9. shenzhen · 深圳各区发布情况。缺口。禁止顶替：M_POLICY_SZ_DIST（种子是各区计数、占比和增长趋势，矩阵无）。COVER 未完成前不拿它填各区发布。
10. shenzhen · 深圳产业链节点覆盖。缺口。禁止顶替：M_POLICY_INDUSTRY_COVERAGE。

排名（不是上面的数量缺口，单独写明）：
- rank · 省级政策力度排名。没有省级排名 ID。排序只用 M_POLICY_INTENSITY_SCORE（政策力度评分，单条有效政策 0–100，种子有、矩阵无，pending_ref=QPOL-02，is_mock）。禁止用 M_POLICY_INTENSITY_INDEX 充当省级排名。
- rank · 城市政策力度排名。没有城市排名 ID。按 M_POLICY_INTENSITY_SCORE 聚合。M_POLICY_INTENSITY_INDEX 是按城市的力度指数，本叶不拿它替换该评分。

不在本单缺项表里：page_key=news 的最新政策，以及 shenzhen 里的深圳最新政策。那是政策主数据，属于 SYSINT-03-04C-L01。

范围（契约草案 PORTAL-CMS-政策扶持.md，不改字段）：
- page_key=rank：只做上面两条排名。复用 lumen-algo-py 里已有计算（vendor/entan-py/polan/eval/intensity.py）。不把 demo-algo-ent-analysis 接进 lumen 调用链。
- page_key=stats / map / coverage，以及 shenzhen 的三条指标：按缺项清单保持无数。
- page_key=news 与深圳最新政策：本单不做。

明确不做：
- 不新编 metric_id，不改指标种子，不改就绪度矩阵，不把「对齐还没有」写成已对齐。
- 不用缺项清单里点名的相近 ID，也不用 M_POLICY_SUPPORT_STRENGTH、M_POLICY_INDUSTRY_FIT、M_POLICY_EFFECT_SCORE 填这些行。政策域其余种子 ID 同样不拿来补洞。
- 不拍板 QPOL-02 的权重。handoff 写明该评分仍待甲方确认。
- 不做政策扶持 CMS 表单，不回写 DWD 富文本。无 CMS 的确认在 PORTAL-CMS-DWD-WRITEBACK-POL-L01，本单不收口那张定义单。
- 不做 WBS-03-08 政策扶持可视化。
- 不做统一用户中心菜单注册。相对路径仍还没有。本单不写 https://next.itic-sci.com/，不编路径字符串。
- 页面空态和 Java 读接口由协作人另派。本单只保证 Python 侧：排名能按 M_POLICY_INTENSITY_SCORE 取出；缺项清单 10 行不返回顶替数。

DoD（与注册表一致，算法侧可验收的部分）：
1. 力度排名用 M_POLICY_INTENSITY_SCORE。没有单独的省级排名 ID、城市排名 ID。
2. 缺项清单 10 行保持无数。M_POLICY_OPPORTUNITY_COUNT 不顶替数量。结果里没有 CMS 填入的名次或分数。handoff 附这 10 行，每行含区块、要的数、结论=缺口、禁止顶替的 metric_id。
3. 菜单相对路径不在本仓实现。handoff 写「路径还没有，注册见 SYSINT-03-18-L01」，不编 URL。

必读：
- agent-delivery/architecture-baseline.md §2 调用链、D12
- agent-delivery/data-lineage-policy.md（只消费指标库）
- agent-delivery/工程过程/04-系统集成/03-专题系统集成/技术方案.md §2 时序、§4.2 政策扶持、§5.2 WBS-03-04b
- agent-delivery/工程过程/04-系统集成/03-专题系统集成/WBS.md WBS-03-04
- agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md
- lumen-algo-py 内 M_POLICY_INTENSITY_SCORE 的现有计算与 /internal 路由
指标 8 件套只用 MCP metric-get。禁止直接读 metrics/registry 的 seed 和矩阵 YAML。

交付：
1. handoff：agent-delivery/agent-handoffs/SYSINT-03-04B-L01.md（templates/handoff-template.md）。ponytail: full。正文含政策维度缺项 10 行。证据含 Python 调用结果：排名走 M_POLICY_INTENSITY_SCORE；缺项清单里至少抽全国数量、发布密度、节点覆盖各一次，返回里没有 TOTAL_COUNT、OPPORTUNITY_COUNT、NATIONAL_DIST、INDUSTRY_COVERAGE 或其他 ID 的数。
2. 调用链：只暴露 Python /internal/*。Java 不在本单修改。禁止 lumen 调用任何 demo-* 服务。
3. 可观测：该计算路径带现有 Python instrument。
4. 完工后停在本地工作区，不自行 commit / push。状态由 coordinator 按认领流程推进。不要把本单标 done。
5. 阻塞写进 handoff 后停止。不要为了补齐页面去改前端或 Java。
```
