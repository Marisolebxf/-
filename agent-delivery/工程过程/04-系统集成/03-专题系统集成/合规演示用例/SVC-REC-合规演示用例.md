# SVC-REC · 机构招引培育 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技专题服务系统 · 产业服务链分析 · 机构招引培育（bid §1.1.1.2.4.2.7.6/7.7）
- 需规序号：7.6.1 / 7.6.2 / 7.7.1 / 7.7.2（`SVCCHAIN-需规条目矩阵.md` §2.3 四行）
- 页面锚点：`/service/institution-decision`（workspace=attract / cultivate 双工作区，每工作区「主 Tab + 分析记录」双页签）
- 部署真身：`lumen-ui-topic`（线上 `edu.itic-sci.com/tts/svcz`，as-built `rec-attract/` `rec-cultivate/` 实勘对象；demo-ui-topic 侧为同构 UX 真源，条件枚举不抄 demo 本地模型值）
- 任务：`SVCCHAIN-DC-M3-REC-L01`（长任务总控 §2 M3c；agent=doc-agent；监管人=human:徐滕强；强度 ponytail full）
- 日期：2026-11-07
- 调度核对：见文末

历史集成测试记录与 as-built 实勘记录保持原文件不改写。这里只写基于现有数据选定的一组输入。

## 用例口径（先读）

1. **双面数据面**：本域数据面分两层，期望按层分别落——
 - **Job 异步面**（analysisType `service_recommend_attract` / `service_recommend_cultivate`，库键 `svc:analysis:attract|cultivate`）：结果快照**不落独立表**，随任务记录存于 `gkxlumenx_topic_enterprise.analysis_task.target_params.result_payload`（M2 受阻项④，本次实查证实 `result_data` 列全空）。Job 期望按「受理成功 + wait_view 终态 + `result_payload` 字段对照」写，字段结构对照 `SVC-20261107-010`（attract 正样本）与 `SVC-20261107-015/018`（INB1303 empty 样本）实测。
 - **结果读面**（前端「查看结果」后调 Java `POST /svc/topic/v1/service/rec-list` kind=attract|cultivate → Feign `POST /internal/gkx-svc/portal/ranking` → Python 读 `demo_gkxlumenx_ads.svc_attraction_recommend` / `svc_cultivation_recommend`）：期望按本日实查表行写具体值。
2. **I2-12 约束**（异步分析工作区）：切条件**不自动**起任务；条件栏显式「开始分析 / 生成招引名单 / 生成培育名单」；同用户同条件单飞（指纹 `svc|attract|{path}` / `svc|cultivate|{path}`，重复发起返回既有任务）；当天已成功直接打开结果；结果页另提供「重新分析」（强制新任务）。成功终态停 wait_view（`page_mode_hint=process_succeeded_wait_view`），须显式点「查看结果」才进结果态。
3. **演示态声明**：招引/培育推荐模型正式口径未定（`Q-SVCCHAIN-05` 🟡，2026-10-22 试点口径已会签：王惠四维＋等权默认）。UI 模型区常驻「演示口径」声明；名单不作对外招商承诺；`pending_client_confirm=1` 全量。
4. **诚实空**：产业切片无挂链机构时名单诚实空（`Q-SVC-011`），不回退全量、不造数。
5. 覆盖表请求列为**后端实际受理契约**（lumen 真身 Create 体与 rec-list 请求体；demo 沙箱 localStorage 任务单形态不同，不混写）。

## 查库

- 时间：2026-11-07 16:35–17:35（UTC+8；M2 调研 16:35–16:55 + 本叶补充实查）
- 主机 `10.50.11.76`，连接走 database-mcp 分组 `gkx-mysql` 的 `demo-gkxlumenx-ods` 入口，跨库限定名只读 SELECT；**未执行任何写操作**。
- **招引榜 `demo_gkxlumenx_ads.svc_attraction_recommend`：50 行**，单批次 `svcmodels_20261107_155402`、`model_version=svc_proxy_v1.3`、`weights={industryFit:35,techLead:30,potential:20,willingness:15}`、`priority_level` 全 `high`、指数区间 88.60–90.00。`rank_no` 列 1–50 连续；机构名在 `ext.name`。首行：rank_no=1 广东奥飞数据科技股份有限公司（广州）90.0000。
- **培育榜 `demo_gkxlumenx_ads.svc_cultivation_recommend`：50 行**。⚠️ **本叶实查（17:0x）与 M2 §2.6 记录（3 行）不一致**：M2 定稿后 17:01 该表被新批次 `svc_rec_cultivate_wanghui_20261107_170132`（`model_version=wanghui_v1_signed20261022`）覆盖为 **50 行**（指数 66.9095–95.3634，`growth_stage` 全 NULL）。批次 `weights={scale:25,effect:25,marketGap:25,innovation:25}`（**等权 25×4**，王惠签核默认），与前端页面展示权重 **25/30/25/20**（svc_proxy_v1.3 同款）**并存不一致**，本叶不改任何一方，用例按各层真源写期望并在行内声明。首行：rank_no=1 深圳市福中达投资控股有限公司 95.3634（`dimension_scores={scale:90.7669, marketGap:99.96, innovation:null, effect:null}`，`dims_available=2`）。培育榜 50 家经 `svc_org_card` JOIN `city`：深圳市 43 + 无 city 7（本土语义以 Python 侧圈定为准，此处仅记录事实）。
- **Job 受理记录 `gkxlumenx_topic_enterprise.analysis_task`**（`analysis_type IN ('svc:analysis:attract','svc:analysis:cultivate')`）：成功 91（attract 56 / cultivate 35）、失败 0 / 取消 0，`result_data` 列全 NULL（快照不落独立表）。今日锚点：`SVC-20261107-007`（cultivate 全量 cnt=50 top 95.3614）、`SVC-20261107-008`（attract 全量 cnt=50 top 90.784）、`SVC-20261107-010`（attract@INB2503 cnt=6 top 90.7805，narration ok）、`SVC-20261107-015/018`（INB1303 empty cnt=0）。
- **链挂接 `demo_gkxlumenx_dwd.enterprise_industry_chain`**（按 chain_code 分组）：INB1309 人工智能 186,964 / INB2503 生物医药 5,267 / INB1354 具身智能 921 / INB170102 人工智能与应用 186,964 / INB170201 生物医药与生命健康 5,267 / INB170503 智能机器人 2,031 / INB170601 智能网联新能源汽车 32 / INB180101 生物制造 51 / INB1204 机器人 1,110（另有 2 行 `chain_name='电池'` 的 INB1204 脏行）/ INB1209 智能网联汽车 32 / INB1323 传感器 67 / INB2505 合成生物 51。**INB1303 集成电路 / INB1306 软件与信息服务 / INB1333 智能终端 = 0 行**（Q-SVC-011 现状未变）。
- **候选交集**：招引榜 50 家 ∩ 挂链 = INB1309 50 家、INB2503 7 家、INB1303/1306/1333 0 家；培育榜 50 家 ∩ 挂链 = 仅 INB1309 50 家（INB2503 为 0）。
- 码表 `demo_gkxlumenx_dim.industry_cluster_map`（15 行活跃映射）与前端产业目录一致；`CL-SEI-02`→INB2503 生物医药（sort_order 1）。
- 指标 8 件套（MCP `metric-registry` 只读）：`M_SVC_REC_ATTRACT_SCORE` / `M_SVC_REC_CULTIVATE_SCORE` 均 **D1=aligned、D2=partial（provisional）、D3=partial（部分支持）、D4=mock**（LUMEN 页内红问号注释与矩阵现状不符，以 registry 为准；本域 UI 角标按 ⓘ 呈现，D2 provisional 须带「待核验」字样）。
- 模型口径登记（`客户决策清单跟踪表.md` Q-SVCCHAIN-05）：正式口径未定；2026-10-22 唐绍祖会签试点口径＝王惠四维＋**维度内/维度间等权默认**（培育缺维按可用维均值、维数<2 不入榜；两套维度名待甲方裁定 REC-B01/REC-B02）；名单阈值/建议规则/量化来源仍待甲方。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 7.6.1 招引模型与指标 | `/service/institution-decision?workspace=attract&tab=attract` 配置区 | 产业方向选「新一代信息技术」（集群 `CL-SEI-01`，只选集群、不下钻 L0）。权重为内置固定 Tag 只读展示：产业匹配度 35% / 技术领先性 30% / 发展潜力 20% / 对外合作意愿 15% | 点「生成招引名单」 | `POST /topicAsync/topic/v1/analysis/tasks` | `{"user_id":"guest","analysisType":"svc:analysis:attract","analysis_fp":"svc\|attract\|CL-SEI-01","params":{"industry":"","workspace":"attract","org_ids":[],"analysis_fp":"svc\|attract\|CL-SEI-01","object_summary":"产业方向：新一代信息技术"}}`（权重不进 CREATE params、不进指纹） | 受理成功返回 `taskId`（形态 `SVC-YYYYMMDD-NNN`）与 `status=queued`；URL 带 `task_id` 进入过程页。权重 Tag 原样展示 35/30/20/15；模型区带演示口径声明与 ⓘ（`M_SVC_REC_ATTRACT_SCORE`，D1 aligned / D2 provisional 待核验 / D4 mock 🧪）。同条件重复点击不新建（返回既有任务） | 可演。分析记录表既有同型成功任务可佐证（如 `SVC-20261107-008`）。`CL-SEI-01` 集群层切片=全 5 条 L0 并集（2026-10-22 口径） |
| 7.6.2 推荐名单生成（正样本切片） | 同上页结果区 | 产业方向选「生物产业 → 生物医药」（`CL-SEI-02.INB2503`）→「生成招引名单」→ 等待完成后「查看结果」 | 点「生成招引名单」，完成后点「查看结果」 | ① `POST /topicAsync/topic/v1/analysis/tasks`（fp=`svc\|attract\|CL-SEI-02.INB2503`）→ ② 轮询 `GET /topicAsync/topic/v1/analysis/tasks/{task_id}`（带 `user_id=guest`）→ ③ `GET /topicAsync/topic/v1/analysis/tasks/{task_id}/result` → ④ `POST /svc/topic/v1/service/rec-list` | ① Create 体同 7.6.1（industry=`INB2503`，fp=`svc\|attract\|CL-SEI-02.INB2503`，object_summary=`产业方向：生物产业`）→ ④ `{"kind":"attract","limit":50,"chain_codes":["INB2503"]}` | **任务态**：轮询至 `status=success`，`page_mode_hint=process_succeeded_wait_view`、`viewed=false`（停过程页不自动跳）。**结果快照**（字段实测 `SVC-20261107-010`）：`status="ads_ready"`、`empty=false`、`summary.count=6`、`summary.top_score=90.7805`、`summary.priority_levels=["high"]`、`selected_industry="INB2503"`、`data_source="demo_ads"`、`weights={industryFit:35,techLead:30,potential:20,willingness:15}`、`own_gaps` 含「Q-SVCCHAIN-05 待甲方确认，当前 35/30/20/15」、`yellow_gaps=["Q-SVCCHAIN-05"]`、`pending_client_confirm=1`、`narration.status="ok"`（文案点名 6 家并列名首「广州市金圻睿生物科技有限责任公司」90.7805，且含「推荐权重为演示口径（Q-SVCCHAIN-05 待甲方确认）；确认前名单不作对外招商承诺」）。**读面名单**：`items=6` 行按 rank 升序——19 广州市金圻睿生物科技有限责任公司 90.7805 / 20 广州仁恒医药科技股份有限公司 90.7805 / 22 广州玻思韬控释药业有限公司 90.7801 / 25 广东壹健康健康产业集团股份有限公司 90.7798 / 31 广州迈景基因医学科技有限公司 90.7784 / 34 云舟生物科技（广州）股份有限公司 90.778；四指标分 `industryFit≈95.08 / techLead=100 / potential=100 / willingness=50`；行带 🧪 MockBadge 与「推荐理由（演示口径）」。页头「共 6 家候选」；导出 CSV 首行 `#` 声明含 Q-SVCCHAIN-05 演示口径与产业上下文「生物产业」，表头=名次，机构，城市，服务环节，综合分，招引指数，产业匹配度，技术领先性，发展潜力，对外合作意愿，推荐理由 | 可演。⚠️ 结果快照数值冻结自 2026-11-07 旧批次 `svcmodels_20261022_212916`（top 90.7805）；当日新批次 `svcmodels_20261107_155402` 后同切片的届时期望=重签发后按新表行实测（当前表值：19 名 90.0000 … 46 名 88.6000，共 7 行）。LOOP 轮内以「先重签发再读表」为准，本行快照字段结构不变 |
| 7.6.2 推荐名单生成（诚实空切片） | 同上页结果区 | 产业方向选「新一代信息技术 → 集成电路」（`CL-SEI-01.INB1303`）→「生成招引名单」→「查看结果」 | 同上 | ① `POST /topicAsync/topic/v1/analysis/tasks` → ②/③ 轮询与 result 同 7.6.2 → ④ `POST /svc/topic/v1/service/rec-list` | industry=`INB1303`，fp=`svc\|attract\|CL-SEI-01.INB1303`；④ `{"kind":"attract","limit":50,"chain_codes":["INB1303"]}` | **任务态**：受理成功 `SVC-20261107-015` 同型，`status=success` + wait_view。**结果快照**（字段实测 `SVC-20261107-015`）：`status="empty"`、`empty=true`、`summary.count=0`、`summary.top_score=null`、`attract=[]`、`selected_industry="INB1303"`、`own_gaps` 同上、`yellow_gaps=["Q-SVCCHAIN-05"]`、`narration.status="skipped"`、`source_tables=["demo_gkxlumenx_ads.svc_attraction_recommend","demo_gkxlumenx_dwd.enterprise_industry_chain"]`。**读面**：`rec-list` 返回 `empty=true`、`items=[]`（`enterprise_industry_chain` 该链 0 行，缺口=Q-SVC-011）；页面诚实空「集成电路产业暂无已映射的服务机构，切其他产业或查看全量名单」，HTTP 200 不报 5xx、不回退全量、不造数 | 可演（诚实空是本行期望本身）。缺口真源：Q-SVC-011（INB1303/1306/1333 共 0 行挂链）；数据情况按「覆盖不到→但空态可演」判定 |
| 7.7.1 培育模型与筛选 | `/service/institution-decision?workspace=cultivate&tab=cultivate` 配置区 | 产业方向默认全量（不选=全量名单）；机构类型默认全选 3 类＝高校 / 科研院所 / 企业（闭集 `CULTIVATE_ORG_TYPES`）；服务环节默认全选 11 项＝上游·研发 / 上游·标准 / 上游·知识产权 / 上游·科研合作 / 中游·中试 / 中游·检测 / 中游·孵化 / 中游·技术转移 / 下游·投融资 / 下游·人才 / 下游·数字化（闭集 `CULTIVATE_SEGMENTS`）。权重 Tag 只读展示：现有规模 25% / 技术创新能力 30% / 服务成效 25% / 市场缺口 20% | 点「生成培育名单」 | `POST /topicAsync/topic/v1/analysis/tasks` | `{"user_id":"guest","analysisType":"svc:analysis:cultivate","analysis_fp":"svc\|cultivate\|*","params":{"industry":"","workspace":"cultivate","org_ids":[],"analysis_fp":"svc\|cultivate\|*","object_summary":"产业方向：产业服务（筛选与权重不进指纹）"}}`（机构类型/环节筛选不进 CREATE、不进指纹） | 受理成功 `taskId` + `status=queued`；成功终态停 wait_view。权重 Tag 原样 25/30/25/20（页面内置；⚠️ 与今日库内培育榜批次等权 25×4 并存，见查库节声明，本行期望只锚页面 Tag）。筛选清空任一组（类型或环节=0 项）时「生成培育名单」禁用，提示「机构类型与服务环节须至少各选 1 项，否则无法开始分析」。ⓘ 挂 `M_SVC_REC_CULTIVATE_SCORE`（D1 aligned / D2 provisional 待核验 / D4 mock 🧪） | 可演。`SVC-20261107-007` 同条件成功任务在库（top 95.3614，cnt=50）。**培育权重不一致处置**：USM 文档 20/30/25/25 已由 M1 矩阵 §3.2 勘误 2 登记为「以代码+实勘双证 25/30/25/20 为准」；今日库内新批次等权 25×4 属算法侧正式化动作，两者并存期页面期望仍锚 25/30/25/20，等权切换另行走 Q-SVCCHAIN-05 甲方决策，本叶不改前端不改算法 |
| 7.7.2 培育名单与建议 | 同上页结果区 | 保持 7.7.1 条件（全量切片 `svc\|cultivate\|*`）→「生成培育名单」→ 完成后「查看结果」→ 名单行展开培育建议；行内「加入对比篮」 | 点「生成培育名单」→「查看结果」→ 展开首行建议 | ① 同 7.7.1 Create → ②/③ 轮询与 result 同 7.6.2 → ④ `POST /svc/topic/v1/service/rec-list` | ④ `{"kind":"cultivate","limit":50,"chain_codes":[]}` | **任务态**：`SVC-20261107-007` 同型 success + wait_view。**结果快照**：`summary.count=50`、`summary.top_score=95.3614`、`summary.growth_stages=[]`、`cultivate[0]={ext:{name:"深圳市福中达投资控股有限公司",rank_no:1,industry:"物业管理",metric_ref:"M_SVC_REC_CULTIVATE_SCORE",dims_available:2,pending_client_confirm:1}, …}`、`own_gaps` 含「四维权重（Q-SVCCHAIN-05）待甲方确认，当前 25/30/25/20」。**读面名单**：`items=50` 行；首行=rank 1 深圳市福中达投资控股有限公司（物业管理），综合分 95.4（`95.3634` 保留一位小数），维度行呈现现有规模 90.8 / 市场缺口 100.0（`innovation/effect` 源缺整行省略，诚实空）；培育建议 `advice_gen="llm"`（LLM 生成，🧪），展开后按扶持维分组呈现建议文本（载体对接/规模提升等，含「服务台账与成效案例」类建议），行建议与机构一一对应且引用该行维度短板数值；第 2 名深圳万城节能股份有限公司 92.6（现有规模 85.2 / 市场缺口 100.0）、第 3 名深圳市比达文化传媒有限公司 89.3（现有规模 78.6 / 市场缺口 100.0）；全榜 `priority_level=high`、`growth_stage` 列空。行内「加入对比篮」可入系统篮（`gkxlumenx_topic_enterprise.svc_compare_basket_item`，现库 6 行 guest）；导出 CSV 表头=排名，机构名称，类型，服务环节，现有规模，技术创新能力，服务成效，市场缺口，综合评分，培育建议，首行 `#` 声明含演示口径与产业上下文 | 可演。维度空值诚实呈现（`innovation/effect` 缺源=整行省略该维，不写 0 分）。CSV 导出为前端本地动作，不新增接口 |
| 7.6.2 × 切条件不自动起任务（I2-12） | 同页配置区/结果区 | 已有 7.6.2 正样本成功任务；在结果页把产业方向切成「新一代信息技术」（集群层）或「集成电路」（`INB1303`） | 切产业选择器（不点开始） | 不发出请求 | 无请求体 | 切条件后不出新任务：URL 指纹变为 `svc\|attract\|CL-SEI-01(.INB1303)`，不自动 `POST tasks`；须再显式点「生成招引名单」才起新任务 | 可演。浏览器网络面板 0 次 Create 请求为过；对照 as-built `rec-cultivate/P0-16`（01262 互证） |
| 7.7.2 × 同用户同条件单飞（I2-12） | 同页配置区 | 保持 7.7.1 条件（fp `svc\|cultivate\|*`）；当天已有成功任务 | 再次点「生成培育名单」 | `POST /topicAsync/topic/v1/analysis/tasks` | 同 7.7.1 Create（服务端幂等，fp `svc\|cultivate\|*`） | 服务端按（user_id, analysisType, analysis_fp）复用：返回同一 `taskId`（今日锚点=`SVC-20261107-007`），不新增记录行；`analysis_task` 当日 cultivate 记录数不因重复点击增加；提示「该条件已有任务正在执行/今日已分析过相同条件」。结果页工具条另有「重新分析」（`force=true`）可强制新任务，新任务为新 `taskId` | 可演。as-built `rec-attract/P0-20`（00798）、`rec-cultivate/P0-18/P0-13` 实勘口径一致 |

> 主路径与 LOOP 轮内口径：Job 期望中的 `result_payload` 数值为**当日/届期签发实例的快照**（示例锚点 SVC-20261107-010/015/018）；快照不落独立表（M2 受阻项④），表行滚动后（如培育榜 11-07 17:01 新批次）按「重签发→读新快照」对齐，字段结构不变。

## 一条主路径

按下面顺序走可演的行，一次演示串完。条件不另做排列组合。

1. **7.6.1 受理**：打开 `/service/institution-decision?workspace=attract&tab=attract`。产业方向选「新一代信息技术」（集群层）。确认权重 Tag 35/30/20/15 与演示口径声明、ⓘ（D4 mock 🧪）在位。点「生成招引名单」→ 进入过程页，URL 带 `task_id`；五阶段推进（任务提交与推荐条件冻结 → 权限与配置校验 → 候选机构数据汇聚 → 推荐算法计算 → 招引推荐名单组装）。
2. **7.6.2 结果（诚实空）**：在「新一代信息技术」内改选「集成电路」（`INB1303`）→ 显式点「生成招引名单」→ 新任务（新指纹 `svc|attract|CL-SEI-01.INB1303`）→ 完成后点「查看结果」→ 诚实空态「集成电路产业暂无已映射的服务机构，切其他产业或查看全量名单」（缺口=Q-SVC-011）。
3. **7.6.2 结果（正样本）**：产业方向改选「生物产业 → 生物医药」（`INB2503`）→ 显式点「生成招引名单」→「查看结果」→ 名单 6 行（届期值：19 金圻睿 90.7805 / 20 仁恒医药 90.7805 / 22 玻思韬 90.7801 / 25 壹健康 90.7798 / 31 迈景基因 90.7784 / 34 云舟生物 90.778），行带四指标分、🧪 角标与演示口径推荐理由；页头「共 6 家候选」。点「导出名单」得 CSV（首行 `#` 声明 + 11 列表头）。
4. **7.7.1 培育配置**：切「培育服务机构推荐分析」工作区（`workspace=cultivate`）。确认机构类型 3 类与服务环节 11 项默认全选、权重 Tag 25/30/25/20、ⓘ（🧪）。把服务环节清空 → 「生成培育名单」禁用且出拦截文案；恢复全选。
5. **7.7.2 培育名单**：点「生成培育名单」→（当天同条件已成功则直接打开既有结果，如 `SVC-20261107-007`）→「查看结果」→ 名单 50 行、首行深圳市福中达投资控股有限公司 95.4（规模 90.8 / 市场缺口 100.0，两维诚实省略）、建议按扶持维分组展开且引用行内短板数值；点首行「加入对比篮」成功入系统篮。
6. **I2-12 复用**：回到招引工作区，保持 `INB2503` 条件再点「生成招引名单」→ 服务端复用当天既有任务（不新增记录行、直开结果）；结果页工具条「重新分析」可见（本主路径不点）。

## 调度核对

需规 7.6.1–7.7.2 各有主行（4 行），另有 3 行 I2-12 行为补充行（挂 7.6.2 / 7.7.2 名下，不占需规新行）。可演 4 行（7.6.1、7.6.2×2 切片、7.7.1、7.7.2）；覆盖不到 0 行（INB1303/1306/1333 产业切片以「诚实空」作为可演期望落行，缺口引用 Q-SVC-011）；设计无资源 0 行。主路径只串可演行。本文不建演示样本循环验收单，不派数据单，不派算法单，不跑 LOOP。

## 数据情况判定依据（逐行）

- 7.6.1：可演——分析记录既有成功任务（SVC-20261107-008 等 56 条 attract success）佐证受理链路；模型区/ⓘ/角标为前端既有实现。
- 7.6.2（正样本）：可演——快照锚点 SVC-20261107-010 + rec-list 表行实查；生物切片 7 家有挂链（届期快照 6 家）。全量切片 50 行亦同演（锚点 SVC-20261107-008，top 90.784）。
- 7.6.2（诚实空）：可演（空态本身）——INB1303 挂链 0 行为已登记事实（Q-SVC-011），空态文案与 `empty=true` 均实测在案（SVC-20261107-015）。
- 7.7.1：可演——`SVC-20261107-007` 同条件成功任务在库；筛选门控为页面实现（as-built rec-cultivate P0 系列）。
- 7.7.2：可演——培育榜 50 行实查（首行 95.3634 等），建议结构 `advice_gen=llm` + `suggestion_items` 实测；入篮目标表现存 6 行 guest 记录。
- 无一行依赖不存在的表（`svc_search_history` / `svc_favorite` / `svc_analysis_job` 不落本域 4 条需规；svc 域无收藏/历史需规行）。
