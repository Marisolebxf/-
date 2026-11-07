# SVC-REC-DEMO-ACCEPT-LOOP · 运行 handoff

- 验收单：`SVC-REC-DEMO-ACCEPT-LOOP`（tech_task，qa-agent，监管人 `human:徐滕强`）
- 规程：`agent-delivery/产品实现规程.md` §6.5；计划：`编排计划/SVC-REC-LOOP计划.md`；用例：`合规演示用例/SVC-REC-合规演示用例.md`
- 本文件只追加，每轮一节，不覆盖上一轮。

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-REC-合规演示用例.md`
- 库：只读（database-mcp `demo-gkxlumenx-ods`；跨库限定名 SELECT：`demo_gkxlumenx_ads.svc_attraction_recommend` / `demo_gkxlumenx_ads.svc_cultivation_recommend` / `demo_gkxlumenx_dwd.enterprise_industry_chain` / `gkxlumenx_topic_enterprise.analysis_task` / `gkxlumenx_topic_enterprise.svc_compare_basket_item`；未写任何库）
- 样本满足：否（1 条 QUERY 缺口，已建单；其余行全过）
- 停止：继续

### 探测

- token 文件在位（长度 32，未读取内容、未打印）；`POST /tts/svcz/api/enterprise/topic/v1/recommend {"count":1}` 带 `Authorization: Bearer` + `systemCode: topic` → **HTTP 200**（code=0，返回推荐 items）。进入样本对照。

### 7 行判定明细（对照用例覆盖表 + LOOP §1 通过线）

| # | 锚点 | 判定 | 证据 |
|---|---|---|---|
| 1 | 7.6.1 招引受理 | ✅ 过 | 当期成功任务 `SVC-20261107-032`（fp `svc\|attract\|*`，18:12）：`status=success`、`page_mode_hint=process_succeeded_wait_view`、summary.count=50、top_score=90=当期榜 `MAX(attraction_index)`、weights 35/30/20/15、own_gaps 含 Q-SVCCHAIN-05、yellow_gaps=[Q-SVCCHAIN-05]、narration.status=ok 且文案含「演示口径（Q-SVCCHAIN-05 待甲方确认）」「不作对外招商承诺」、pending_client_confirm=1。受理链路（Create→轮询→result）契约由 032/038/042/015 等多枚任务记录互证；本轮未新签发（指令：默认不签发不带 force，复用当天已成功任务） |
| 2 | 7.6.2 正样本切片（INB2503） | ✅ 过 | `SVC-20261107-042`（fp `svc\|attract\|CL-SEI-02.INB2503`，18:49）：status=ads_ready、summary.count=7=当期榜∩挂链 INB2503 去重机构数（表行：rank 5 玻思韬 90.0 / 13 迈景 90.0 / 15 云舟 90.0 / 30 石药明复乐 89.685 / 33 溪木源 89.65 / 44 瑞通 88.6 / 46 创尔 88.6）、top_score=90、narration ok 且点名 7 家与前三大并列 90.0、区间 88.6–89.685。届期快照 `SVC-20261107-010`（6 家 top 90.7805）为旧批次 `svcmodels_20261022_212916` 冻结值，用例已声明按届期对照，不计缺口 |
| 3 | 7.6.2 诚实空切片（INB1303） | ✅ 过（Job 面） | `SVC-20261107-015`（fp `svc\|attract\|CL-SEI-01.INB1303`，14:57）：status="empty"、empty=true、summary.count=0、top_score=null、attract=[]、narration.status="skipped"、source_tables=[ads.svc_attraction_recommend, dwd.enterprise_industry_chain]、own_gaps/yellow_gaps 同口径。挂链 INB1303/1306/1333 = 0 行（Q-SVC-011），诚实空是期望本身，不判缺不派修 |
| 4 | 7.7.1 培育受理与门控 | ✅ 过 | `SVC-20261107-007`（fp `svc\|cultivate\|*`，14:50）：status=success + wait_view、count=50；库内权重 Tag 双口径并存（见下节），页面 Tag=25/30/25/20 期望按用例锚定（本 LOOP 不开页面，Tag 期望由前端实勘源码 `ServiceRecommendCultivateWorkspace.vue` 模型区常量与用例 M1 勘误 2 承接）；禁用门控为页面实现（as-built rec-cultivate P0 系列已证） |
| 5 | 7.7.2 名单与建议 | ✅ 过（双口径） | 快照（007）：cultivate[0].ext={name:深圳市福中达投资控股有限公司, rank_no:1, industry:物业管理, metric_ref:M_SVC_REC_CULTIVATE_SCORE, dims_available:2, pending_client_confirm:1}、advice_gen="llm" 在 ext 内、summary.growth_stages=[]。读面（rec-list kind=cultivate）：items=50、首行 rank 1 深圳市 95.3634（表 MAX）、维度行现有规模 90.7669→90.8 / 市场缺口 99.96→100.0、innovation/effect 缺源整行省略；榜行 ext.suggestion_items（LLM 分组建议）经 `lumen-topic-py/gkx_svc_service/repo.py` L870-872 透传给前端 parseAdviceItems。快照 top_score=95.3614 vs 当期表 MAX=95.3634：007 签发于批次 `svc_rec_cultivate_wanghui_20261107_122355`，17:01 表滚动至 `svc_rec_cultivate_wanghui_20261107_170132`，属计划 §0.3「两榜表行滚动→先重签发再读当期」的届期差，字段结构不变，不计缺口 |
| 6 | I2-12 切条件不自动起任务 | ✅ 过（只读核对） | 库：今日 22 枚 REC 任务均为显式发起，无「切条件自动签发」形态。代码：`lumen-ui-topic/src/views/service/svcRecommendAttractWorkspace.vue` `setIndustry()` 仅 `job.patchQuery({industry})` 不建任务；as-built `rec-cultivate/P0-16`（01262 互证）同口径。本轮不发新 POST |
| 7 | I2-12 单飞复用 / 当天复用 / 重新分析 | ✅ 过（只读核对） | `decideAnalysisTaskGate`（`src/composables/analysisTaskGate.ts` L139-171）：同 (user, analysisType, fingerprint) 在跑→restore_processing、当天（上海时区）成功→restore_result、`forceCreate=true` 才新建；`useSvcAnalysisJob.startOrReuse` 复用即打复用提示（「该条件已有任务正在执行/今日已分析过相同条件」），结果页工具条「重新分析」= `startAnalysis(true)`（`ServiceRecommendAttractWorkspace.vue` L150-160/351）。复用证据：032/038 为同 fp `svc\|attract\|*` 两枚独立成功任务（038 于 032 后由用户显式重发或并行会话产生；**库层无条件级指纹幂等**，复用语义在前端门控 + 服务端 `created.reused` 提示，与 as-built P0-20（00798）「记录不膨胀/复用提示」口径一致）。sessionStorage：svc 两工作区无专用复用键，复用决策以任务列表 + 指纹比对实现（语义等价，as-built 同口径） |

**双口径说明（培育权重，本单登记的事实，不派修）**：页面/Job 快照 Tag=25/30/25/20（svc_proxy 同款；007 快照 weights={scale:25, effect:25, marketGap:20, innovation:30}）vs 培育榜当期批次 `svc_rec_cultivate_wanghui_20261107_170132`（`wanghui_v1_signed20261022`）等权 25×4。两口径各自成立即过（LOOP §0.4）；等权正式化走 Q-SVCCHAIN-05 甲方决策链。培育榜 priority_level=high 31/50 + mid 19/50（用例「全榜 high」为旧 3 行批次事实，已随批次滚动变化；growth_stage 全 NULL 同为批次事实，均不派修）。

**读面（rec-list）对照**：正确网关前缀 `/tts/svcz/api/svc/topic/v1/service/rec-list`（计划 §3 所写「剥 /svc」路径 `/api/enterprise/svc/...` 404，候选前缀一次试中）。kind=attract 全量 items=50 首行 rank 1 广东奥飞数据 90；INB2503 items=7 首行 rank 5 玻思韬 90；INB1303 HTTP 200 empty=true items=[]；kind=cultivate items=50 首行 rank 1 深圳市 95.3634。全量/切片读面与快照 summary 及榜表行一致（INB1303 语义缺口见下）。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `lumen-topic-py/gkx_svc_service/repo.py.ranking_list.zero_row_source_semantics` | QUERY | chain_codes 均为有效 INB 码但挂链交集零行时，rec-list 返回 data_source="demo_ads"（实测 INB1303）；前端 `chainEmptyDescription` 只在 `data_source` 以 `empty:chain_unmatched` 开头时才出「{产业}产业暂无已映射的服务机构…」点名文案，当前会落到通用「当前方向暂无高匹配外部机构」 | 产业切片零行时 data_source 带 `empty:chain_unmatched` 前缀（本文件 `_empty()`/unmapped 分支既有约定），HTTP 200 / empty=true / items=[] / 不回退全量 / 不造数不变 | ranking_list() 末尾组装处：codes 有效且 items 空 → source 置 `empty:chain_unmatched`；回归全量与 INB2503 切片 | `SVC-REC-DEMO-FIX-R20261107-QUERY`（bugfix，ready，algorithm-agent，repo=lumen-topic-py；注：派单默认 QUERY→lumen-svc-platform，实勘代码位置在 Python 读面，按实际位置建单） |

不派修项：Q-SVC-011（INB1303/1306/1333 挂链 0 行，诚实空是期望本身）；Q-SVCCHAIN-05（权重双口径并存）；培育 growth_stage 全 NULL / priority 分布 31 high + 19 mid（批次事实）；对比篮 guest 篮 2 行（用例 6 行为届期值，篮内容随演示操作滚动，非 §1 通过线项）；快照 95.3614 vs 表 MAX 95.3634（批次滚动届期差，字段结构不变）。

### 库侧基线核对

招引榜 50 行单批次 `svcmodels_20261107_155402`（svc_proxy_v1.3，weights 35/30/20/15，指数 88.60–90.00，priority 全 high，首行 rank 1 广东奥飞数据科技股份有限公司 90.0000）；培育榜 50 行单批次 `svc_rec_cultivate_wanghui_20261107_170132`（wanghui_v1_signed20261022，等权 25×4，指数 66.9095–95.3634，growth_stage 全 NULL，首行 rank 1 深圳市福中达投资控股有限公司 95.3634，dims_available=2）；挂链 INB2503 5,267 行（INB1303/1306/1333 = 0）；榜∩挂链：attract INB1309 50 / INB2503 7 / INB1303 0，cultivate 仅 INB1309 50。REC Job 成功：attract 62 / cultivate 37（今日 22 枚，较基线 91 自然增长，均为 success、0 失败）。SELECT 一次通过，无受阻。

### 子任务

- `SVC-REC-DEMO-FIX-R20261107-QUERY`：新建，bugfix，ready 待认领（不认领；验收轮不改库不改代码）。去重：task-query 无未完成的同缺口 FIX 单。

### 收尾

- 本轮样本未满足（1 条 QUERY 缺口），验收单退回 `ready`，不签 `done`；等待子任务完工后下一轮**重新签发** REC Job 读当期快照（本域口径）。
- 成本：本轮 qa 验收实际估算 actual_tokens≈80,000、model=glm-5.3-Flash、actual_cost≈$0.5、cost_warn=false（远低于 $10 阈值）。
