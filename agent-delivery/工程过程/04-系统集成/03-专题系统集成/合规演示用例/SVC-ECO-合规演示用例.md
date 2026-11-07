# SVC-ECO · 服务链生态域 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技专题服务系统 · 产业服务链分析 · 服务链生态（7.4 / 7.5 / 7.8）
- 需规序号：7.4.1–7.4.2 / 7.5.1–7.5.2 / 7.8.1–7.8.2
- 需规全文：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.7（L5047–5158）；结构化版 `agent-delivery/bid-reference/srs/04-科技专题服务系统/科技专题战略分析/产业服务链分析.md`（seq 117–132）
- 条件枚举真源：`SVCCHAIN-需规条目矩阵.md` §2.2（M1）；数据事实真源：`SVC-数据调研-20261107.md`（M2）
- 页面锚点：`/service/chain-analysis`（workspace=chain / graph / shenzhen；as-built `qa/as-built/scripts/KJZTFWXT/service/{chain-shortboard,chain-graph,sz}/`）
- 日期：2026-11-07
- 调度核对：见文末

as-built 实勘（chain-shortboard P0-06/07、chain-graph P0-08、sz P0-13）历史实测不改写。其中 2026-10-15 P0-07「结果态无环节行」与 P0-08 `ENV-SVCGRAPH-HANG-EMPTY-001`（hang 0 点 0 边）两项环境债已被 11 月批次补数覆盖（`svc_chain_gap` 现批次六行、11-07 图谱任务 `status=ads_ready`），本文按当前实查写，不改写历史文件。

## 查库

- 时间：2026-11-07 17:04–17:13（UTC+8）
- 入口连接 database-mcp 分组 `gkx-mysql` 的 `demo-gkxlumenx-ods`（主机 `10.50.11.76`，用户 `gkxlumenx`），跨库限定名只读 SELECT，未写任何表、未执行 `--apply`。
- 环节堵点面读 `demo_gkxlumenx_ads.svc_chain_gap`（批次 `svcmodels_20261107_155402`，`model_version=svc_proxy_v1.3`，`q061_pending_client=1` 全量）：研发与科研合作 28,842/93.0244、知识产权与标准 96/93.7500、技术转移与孵化 22/85.9091、**中试熟化 0（`avg_depth` NULL、`runtime_flag=blank`）**、检测认证 457/75.8753、市场化服务 4,229/75.0142。
- 图谱统计读 `demo_gkxlumenx_ads.svc_relation_chain`（51 行，同批次）：全网行（`org_id` NULL）`density=0.000046`、`hop_level=1`、`ext={node_count:43296, link_count:42740, q062:1}`；中心性 TOP5 首名深圳市创新投资集团有限公司 253。
- 挂链面 `demo_gkxlumenx_dwd.svc_org_graph_hang` 43,296 行、43,296 个机构、单空间 `demo_gkx_chain`、`tag_name` 单值；正式库 `gkxlumenx_dwd` 同名表 0 行（挂接只在 demo 面）。
- 任务面 `gkxlumenx_topic_enterprise.analysis_task`：三类均有 success 任务，结果 JSON 落 `target_params.result_payload`（`result_data` 为 NULL，资产指针 `res-{taskId}`）。本文引用：
  - `SVC-20261105-014`（shortboard，`industry=INB1309` 新一代信息技术，2026-11-05 10:22:38，guest）：`gap[]` 六行为 研发 29,120/92.94、知识产权 96/93.75、技术转移与孵化 0（blank）、中试熟化 0（blank）、检测认证 201/65.45、市场化 4,229/75.01（该批次快照；与现批次差异见 7.4.1 行注）。
  - `SVC-20261107-002`（graph，industry 空，2026-11-07 02:30:10，guest）：`status=ads_ready`、`space=demo_gkx_chain`、`engine=svcmodels`、`density_formula=2E/(N*(N-1))`、`relation_summary.ext={node_count:43296, link_count:42740}`、`yellow_gaps=["Q060","Q062","Q063","Q-SVC-010","Q-SVCCHAIN-03"]`、`list_cap=50`、`read_only=true`、`write=false`。
  - `SVC-20261107-022`（shenzhen，2026-11-07 08:49:56，guest）：`sz_compare`（framework_name=产业服务链统一评价框架，五城市四指标）、`tier={rank:1, tier:"T1", label:"T1 · 第一梯队（1/8）", gauge_value:77, total:8}`、`shenzhen={scale:14080, tech_benchmark:77, density:0.000046, completeness:0.833, blank_stages:["stage-pilot"]}`、`narration`（prompt_pack=svc.shenzhen.narrate，glm-5.3-flash，status=ok）、`own_gaps=["非深圳城市标量取 sz_city_benchmark 对标表，口径待 Q-SVC-010"]`。
- svc 表无 `is_mock` 列；演示态由 `data_source` / `pending_client_confirm` / `q061_pending_client` / `rule_version` / `runtime_flag` 承载（M2 §0.4、§8.6），覆盖表不写 `is_mock=1`。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 7.4.1 全链路可视化呈现 | 服务链短板分析（workspace=chain）· 全周期服务链路地铁图 | 产业集群选「新一代信息技术」（`industry=INB1309`）。六环节字典=研发与科研合作/知识产权与标准/技术转移与孵化/中试熟化/检测认证/市场化服务 | 点「开始分析」；同条件已签发任务直接「查看结果」（本次引用 SVC-20261105-014） | `GET /api/topicAsync/topic/v1/analysis/tasks/SVC-20261105-014/result?user_id=guest` | `analysisType=svc:analysis:shortboard`（任务键 `svcan.shortboard.v0`）、`industry=INB1309`、`analysis_fp=svc\|chain\|INB1309`、`workspace=chain`、`user_id=guest` | `result_payload.gap[]` 六行：研发与科研合作 29,120 家/92.94、知识产权与标准 96 家/93.75、技术转移与孵化 0 家/`runtime_flag=blank`、中试熟化 0 家/`runtime_flag=blank`、检测认证 201 家/65.45、市场化服务 4,229 家/75.01。页面六站地铁图逐站标依赖服务类型与机构数/平均深度；中试熟化站呈空态（0 家、平均深度 —），`avg_depth` 缺失不伪造 0。响应带 `q061_pending_client=1`（Q061 演示口径）。环节统计为全库词表代理口径，不随产业领域真实切片。另起新任务按现批次 `svc_chain_gap`（svcmodels_20261107_155402：28,842/93.02、96/93.75、22/85.91、0/blank、457/75.88、4,229/75.01）核对，中试熟化 0 恒定 | 可演（演示态声明）。产业级切片覆盖不到：缺环节成员事实表（GAP-SVC-CHAIN-SEGMENT） |
| 7.4.2 瓶颈堵点智能识别 | 同 7.4.1 · 瓶颈堵点识别面板 | 同 7.4.1 条件。演示规则三判定（Q-SVCCHAIN-03 临时默认）：机构数 0→服务空白（红）、≤1→薄弱（橙）、平均深度<55→瓶颈（橙红） | 分析完成 → 链路图高亮 + 识别面板逐条读判定与依据行 | 同 7.4.1（同一结果截面） | 同 7.4.1 | 该快照下「服务空白」=技术转移与孵化、中试熟化（两环节 0 家）进面板红档，依据行为规则文本（如「环节内该环节服务机构数 = 0（演示规则：0 家 → 服务空白）」样式）；图区带「演示规则判定」可读声明（as-built P0-07 现场字面；用例原文「专家知识库演示态」与现场不一致已记 D1，历史不改写）。现批次下空白环节=中试熟化 1 个。薄弱/瓶颈两档现库无实例（各非零环节机构数均 >1 且平均深度 ≥55），面板不合成伪警示 | 可演（「演示规则判定」声明口径；判定口径 Q-SVCCHAIN-03 未定，不作正式业务结论） |
| 7.5.1 关系网络构建 | 服务链图谱分析（workspace=graph）· 服务生态关系图谱 | 分析模式选「② 机构+关联主体」（`eco_filter=orgs_and_actors`；「① 仅机构」为对照模式）。关系类型枚举=投资/合作/竞争/人才流动（bid 7.5.1；现环境边型经 `edge_map` 归并为 `participates` 单型） | 模式确认后点「开始分析」/复用已签发任务（本次引用 SVC-20261107-002） | `POST /api/svc/topic/v1/service/eco-graph` | `{"filter":"orgs_and_actors"}`（`industry`/`industry_id` 可带、Python 可忽略） | 图谱空间 `demo_gkx_chain` 构建成功：节点 43,296 / 边 42,740（`relation_summary.ext`），`status=ads_ready`、`engine=svcmodels`、`data_source=demo_ads`、`density_formula=2E/(N*(N-1))`、`list_cap=50`、`read_only=true`、`write=false`、`model_version=svc_proxy_v1.3`；`yellow_gaps=["Q060","Q062","Q063","Q-SVC-010","Q-SVCCHAIN-03"]` 随响应；`pending_client_confirm=1`。挂链源 `svc_org_graph_hang` 43,296 行单空间单 tag；四类关系在图上归并 `participates` 单边型（演示态声明）。43,296/42,740 为全网口径，非产业切片 | 可演（演示态声明）。产业级图谱切片覆盖不到（挂链无产业维度，Q060/Q062/Q063 未定） |
| 7.5.2 图谱探索与统计 | 同 7.5.1 · 统计面板 + 节点下钻 | 统计三件：网络密度（公式 2E/(N(N-1))）、度中心性 TOP5、生态影响力评分；机构节点 click 开画像抽屉，关联主体仅摘要不下钻 | 结果态统计面板读数；过滤/聚焦变化重算 | `GET /api/topicAsync/topic/v1/analysis/tasks/SVC-20261107-002/result?user_id=guest` | `user_id=guest`（读 `relation_summary` / `relation_top`） | 网络密度=0.000046（N=43,296、E=42,740）。TOP5 依序：深圳市创新投资集团有限公司 度 253、深圳市引导基金投资有限公司 174、深圳市高新投创业投资有限公司 172、深圳市招商平安资产管理有限责任公司 114、深圳市中小担创业投资有限公司 104（各行 density 恒 0.000046）。生态影响力评分区块显诚实缺失声明（无算法定义卡不输出伪分；GAP-SVC-GRAPH-INFLUENCE / Q-SVCCHAIN-03），响应与页面均不得出现影响力伪分数 | 可演（密度/TOP5 为实查值；影响力子项以诚实缺失声明承载） |
| 7.8.1 深圳服务链现状分析 · 统一评价框架 | 深圳服务链现状分析（workspace=shenzhen）· 统一评价框架说明卡 | 深圳现状页签。框架指标构成（lumen 演示口径四指标）=机构规模/平均技术分/网络密度/服务链完整度（framework_name=产业服务链统一评价框架，`pending_client_confirm=1`）。demo 沙箱（demo-ui-topic）为三指标+完整度诚实排除的另一演示态，两态均带 Q-SVCCHAIN-04 声明 | 页签「开始分析」/复用已签发任务（本次引用 SVC-20261107-022） | `GET /api/topicAsync/topic/v1/analysis/tasks/SVC-20261107-022/result?user_id=guest` | `analysisType=svc:analysis:shenzhen`（任务键 `svcan.shenzhen.v0`）、`analysis_fp=svc\|shenzhen\|*`、`user_id=guest` | `sz_compare.framework_name=产业服务链统一评价框架`、`caliber=同一产业、同一统计周期、同一指标口径（尺度/技术力/密度/完整度）`、`metric_order=["scale","tech","density","completeness"]`。深圳四指标：机构规模 14,080 家（ads.svc_org_card 城市切片）、平均技术分 77（dwd.sz_city_benchmark 对标值，Q-SVC-010 待核）、网络密度 0.000046（ads.svc_relation_chain 全局密度，城市级待 Q062）、服务链完整度 0.833（=非空环节占比 5/6，ads.svc_chain_gap，Q-SVCCHAIN-04 未定）。`own_gaps=["非深圳城市标量取 sz_city_benchmark 对标表，口径待 Q-SVC-010"]`。四项均须带演示态/待确认声明，不作为正式评价结论 | 可演（演示态声明口径；统一评价框架 Q-SVCCHAIN-04 未定，完整度为演示合成值） |
| 7.8.2 横向对比分析 | 同 7.8.1 · 五城市柱状图 + 梯队仪表盘 + 结论 | 对比城市五档=深圳/全国平均/北京/上海/广州；对比指标勾选（默认全选）。梯队演示规则（lumen 实态）=8 城对标表平均技术力排序 | 勾选对比指标 → 读柱状图、梯队仪表盘与结论文案 | 同 7.8.1（同一结果截面） | 同 7.8.1 | 五城市逐指标（`sz_compare.cities`）：机构规模 深圳 14,080 / 广州 19,600 / 全国平均 11,228 / 北京 3 / 上海无在库行（null）；平均技术分 深圳 77 / 北京 74 / 上海 73 / 广州 71 / 全国平均 72.9；网络密度仅深圳 0.000046（其余 null=missing）；完整度 深圳 0.833 / 北京 0.72 / 上海 0.71 / 广州 0.69 / 全国平均 null。梯队：`rank=1`、`tier=T1`、label=`T1 · 第一梯队（1/8）`、`gauge_value=77`、`total=8`、basis=`对标基准表 8 城平均技术力排序：深圳 > 北京 > 杭州 > 上海 > 成都 > 苏州 > 广州 > 全国`（pending Q-SVCCHAIN-04）。结论 narration（prompt_pack=svc.shenzhen.narrate）含原文「深圳处于T1 · 第一梯队（1/8）。机构数量方面，深圳为14080家，高于全国平均的11228.0家，低于广州的19600家…」且数值与 sz_compare 同源。上海机构规模 null 呈现无数据，不造 0 | 可演（演示态声明口径；非深圳城市标量为对标参考值 Q-SVC-010 待核） |

服务地址：`http://10.50.69.111:30892`。请求头 `systemCode: topic`。上表 GET 必须带 `user_id=guest`（任务归属校验）。demo-ui-topic 沙箱（React demo2）的确定性演示基准（五城市 1,240/460/1,580/1,350/890 等）是另一套演示数据，本用例期望一律以专题系统线上载荷为准。

## 一条主路径

按下面顺序走可演的行，全部复用已签发任务结果，不新起任务。条件不另做排列组合。

1. 服务链短板分析（workspace=chain）：产业集群「新一代信息技术」，打开 SVC-20261105-014 结果。GET `…/analysis/tasks/SVC-20261105-014/result?user_id=guest`。六站地铁图：研发 29,120/92.94、知识产权 96/93.75、技术转移 0（blank）、中试熟化 0（blank，空态）、检测认证 201/65.45、市场化 4,229/75.01；识别面板红色「服务空白」=技术转移与孵化、中试熟化，图区带「演示规则判定」声明。
2. 服务链图谱分析（workspace=graph）：模式「② 机构+关联主体」，打开 SVC-20261107-002（或 POST `/api/svc/topic/v1/service/eco-graph`，body `{"filter":"orgs_and_actors"}`）。图谱空间 `demo_gkx_chain`：节点 43,296 / 边 42,740；统计面板密度 0.000046，TOP5 首名「深圳市创新投资集团有限公司」度 253；生态影响力区块显诚实缺失声明。
3. 深圳服务链现状分析（workspace=shenzhen）：打开 SVC-20261107-022。框架说明卡（产业服务链统一评价框架，演示口径）；深圳 14,080 家 / 技术分 77 / 密度 0.000046 / 完整度 0.833；五城市对比（广州 19,600 高于深圳，上海规模无在库行）；梯队仪表盘 `T1 · 第一梯队（1/8）`（gauge 77）；结论含「深圳处于T1 · 第一梯队（1/8）…」且数值与图同源。

## 调度核对

需规 7.4.1–7.8.2 各一行，共 6 行。可演 6 行（全部带演示态声明，不作为正式业务结论）。覆盖不到 0 行（产业级切片、图谱产业维度、影响力评分三处以缺口声明承载并入行内说明，不另立行）。设计无资源 0 行。主路径只串可演行。本文不建演示样本循环验收单（LOOP 计划见 `编排计划/SVC-ECO-LOOP计划.md`），不派数据单，不派算法单。
