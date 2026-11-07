# SVC-ECO-DEMO-ACCEPT-LOOP · 验收 handoff

- 类型：`tech_task` · 执行 `qa-agent` · 监管人 `human:徐滕强`
- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ECO-合规演示用例.md`
- 计划：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ECO-LOOP计划.md`
- 本文件为常驻验收单 handoff，每轮一节「运行 YYYY-MM-DD」，只追加，不覆盖既有章节。token 与口令不进本文件。

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ECO-合规演示用例.md`
- 库：只读。database-mcp 分组 `gkx-mysql` 入口 `demo-gkxlumenx-ods`（主机 `10.50.11.76`，用户 `gkxlumenx`）跨库限定名 SELECT：`demo_gkxlumenx_ads.svc_chain_gap` / `svc_relation_chain` / `svc_org_card`、`demo_gkxlumenx_dwd.svc_org_graph_hang`、`sz_city_benchmark`（仅经 information_schema 验列，未取数）、`gkxlumenx_ads`（正式库对照）、`gkxlumenx_topic_enterprise.analysis_task`。未写任何表，未执行 `--apply`。
- 样本满足：是
- 停止：通过

### 探测

- `POST https://edu.itic-sci.com/tts/svcz/api/enterprise/topic/v1/recommend`，body `{"count":1}`，头 `authorization` + `systemcode: topic` → **HTTP 200**（`code=0`，返回企业推荐条目，首条广州市软件开发企业）。token 有效，进入样本对照。

### 六行判定

| 行 | 接口（均 200） | 判定 | 关键证据 |
|---|---|---|---|
| 7.4.1 全链路可视化呈现 | GET `/topicAsync/topic/v1/analysis/tasks/SVC-20261105-014/result?user_id=guest` | ✅ 对上 | `result_payload.gap[]` 六环节齐：研发与科研合作 29,120/92.94、知识产权与标准 96/93.75、技术转移与孵化 0/blank、中试熟化 0（`avg_depth=NULL`、`runtime_flag=blank`，未补 0）、检测认证 201/65.45、市场化服务 4,229/75.01；`pending_client_confirm=1`（Q061 演示口径）在位；`status=ads_ready` |
| 7.4.2 瓶颈堵点智能识别 | 同 7.4.1 截面 | ✅ 对上 | `shortboard.rule=Q-SVCCHAIN-03`；`blank_count=2`（技术转移与孵化、中试熟化，均 0 家）进 red 档（bottlenecks 列两环节）；`weak_count=0`、`bottleneck_count=0`，未合成薄弱/瓶颈伪警示；`own_gaps` 短板阈值声明在位 |
| 7.5.1 关系网络构建 | POST `/svc/topic/v1/service/eco-graph` body `{"filter":"orgs_and_actors"}` | ✅ 对上 | `space=demo_gkx_chain`、`status=ads_ready`、`density_formula=2E/(N*(N-1))`、`write=false`、`writes_ads=false`、`mock=false`、`pending_client_confirm=1`、`gap=["Q060","Q062","Q063","Q-SVC-010","Q-SVCCHAIN-03"]`、`allowed_edges` 四型（图上归并 participates 演示态声明）；节点 43,296/边 42,740 与库挂链面及 7.5.2 快照一致 |
| 7.5.2 图谱探索与统计 | GET `…/analysis/tasks/SVC-20261107-002/result?user_id=guest` | ✅ 对上 | `relation_summary`：密度 0.000046、`ext={node_count:43296, link_count:42740, q062:1}`；`relation_top` TOP5 依序：深圳市创新投资集团有限公司 253、深圳市引导基金投资有限公司 174、深圳市高新投创业投资有限公司 172、深圳市招商平安资产管理有限责任公司 114、深圳市中小担创业投资有限公司 104（各行 density 恒 0.000046）；载荷无影响力键、`yellow_gaps` 五项在位，无伪分 |
| 7.8.1 深圳现状 · 统一评价框架 | GET `…/analysis/tasks/SVC-20261107-022/result?user_id=guest` | ✅ 对上 | `sz_compare.framework_name=产业服务链统一评价框架`、`caliber` 与 `metric_order=["scale","tech","density","completeness"]` 齐；`shenzhen={scale:14080, tech_benchmark:77, density:0.000046, completeness:0.833, blank_stages:["stage-pilot"]}`；`own_gaps=["非深圳城市标量取 sz_city_benchmark 对标表，口径待 Q-SVC-010"]` 在位；`pending_client_confirm=1` |
| 7.8.2 横向对比分析 | 同 7.8.1 截面 | ✅ 对上 | 五城市 cities 齐：深圳 14,080/77/4.6e-05/0.833、广州 19,600/71/—/0.69、全国平均 11,228/72.9/—/—、北京 3/74/—/0.72、上海 null/73/—/0.71；`tier={rank:1, tier:"T1", label:"T1 · 第一梯队（1/8）", gauge_value:77, total:8, basis:"对标基准表 8 城平均技术力排序…", pending:"Q-SVCCHAIN-04"}`；narration（`svc.shenzhen.narrate`，status=ok）含「深圳处于T1 · 第一梯队（1/8）」且 14080/19600/11228/72.9/74/73/71 七值与 sz_compare 同源 |

判定口径：6 行均带演示态声明（Q061 演示口径 / 演示规则判定 Q-SVCCHAIN-03 / `pending_client_confirm=1` / Q-SVC-010 / Q-SVCCHAIN-04），按声明字段在位性核对，不判业务对错；中试熟化空态是期望本身，不判缺。

### 库侧证据（只读 SELECT）

- `demo_gkxlumenx_ads.svc_chain_gap` 六行（批次 `svcmodels_20261107_155402`，`svc_proxy_v1.3`，`q061_pending_client=1` 全量）：研发 28,842/93.0244、知识产权 96/93.7500、技术转移与孵化 22/85.9091、**中试熟化 0（avg_depth NULL、runtime_flag=blank）**、检测认证 457/75.8753、市场化 4,229/75.0142。与用例「另起新任务按现批次核对」一致；中试熟化 0 恒定 ✅。
- `demo_gkxlumenx_ads.svc_relation_chain` 51 行、单批次：全网行（org_id NULL）密度 0.000046、`ext.node_count=43296`、`ext.link_count=42740` ✅；中心性 TOP5 与接口一致 ✅。
- `demo_gkxlumenx_dwd.svc_org_graph_hang` 43,296 行、43,296 机构、单空间 `demo_gkx_chain`、单 tag ✅；正式库 `gkxlumenx_dwd` 同名表 0 行（挂接只在 demo 面）、`gkxlumenx_ads` 图谱面 0 行，符合 D12 demo 隔离。
- `demo_gkxlumenx_ads.svc_org_card` 城市切片：深圳市 14,080、广州市 19,600、北京市 3，上海无在库行（null 呈现不造 0）✅，与 sz_compare 五城市值同源。
- `gkxlumenx_topic_enterprise.analysis_task`：`SVC-20261105-014`（shortboard）、`SVC-20261107-002`（graph）、`SVC-20261107-022`（shenzhen）三条均 `status=success`、`user_id=guest`、`result_payload.status=ads_ready`；`result_data` 全 NULL（资产指针口径）。
- `sz_city_benchmark` 仅验列（8 城对标表结构在位），未取数。

### 探测与接口说明

- 服务主用入口 `https://edu.itic-sci.com/tts/svcz/api/`（网关前缀），四笔均 200；用例标注的 `http://10.50.69.111:30892` 为同网关集群地址，本轮未再重复打。
- 7.4.1 快照为 2026-11-05 批次（29,120/201/0·0），现库批次为 28,842/457/22/0·0——计划 §2 排除项「批次间非零值差异按当时实查核对，不追平历史值」，按快照值判定通过。
- 7.5.1 POST 响应 `nodes=[]`、`edges=[]`、`empty=true`（reason=demo_ads）：在线构图为只读空集（`write=false`），空间/边数/密度/声明与 7.5.2 快照一致，按计划 §4「读图谱面」语义采用快照与库侧行值判定，不判 ENV。
- 上海机构规模 null、生态影响力诚实缺失（载荷无 influence 键）、图谱 participates 单边型、环节统计全库词表代理口径：计划 §2「保持现状」排除项，不判缺、不建子任务。

### 缺口

（无。6 行全部对上，本轮不建 DATA/QUERY/ALGO 子任务。）

### 子任务

（无。）

### 收尾

- 验收单 `SVC-ECO-DEMO-ACCEPT-LOOP` 状态拨回 `ready`（不签 `done`），note 已附本轮摘要。
- LOOP 计划状态行已回写本轮结果。
- 样本满足，等人说「按 LOOP 跑」再开下一轮；签收收尾按规程 §6.5.7 由监管人确认。
