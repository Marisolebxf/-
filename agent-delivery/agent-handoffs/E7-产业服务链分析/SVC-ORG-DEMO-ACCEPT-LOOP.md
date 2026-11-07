# SVC-ORG-DEMO-ACCEPT-LOOP · 服务机构分析演示样本反复验收（handoff，只追加）

- 任务：`SVC-ORG-DEMO-ACCEPT-LOOP`（Epic E7-产业服务链分析；agent=qa-agent；监管人=human:徐滕强；强度=ponytail full）
- 规程：`agent-delivery/产品实现规程.md` §6.5（一轮四步 §6.5.4，报告 §6.5.5）
- 计划：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/SVC-ORG-LOOP计划.md`

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md`（6 行可演，0 覆盖不到）
- 库：只读。database-mcp 组 `gkx-mysql` → 连接 `demo-gkxlumenx-ods`，跨库限定名查 `demo_gkxlumenx_dwd.svc_org_circle` / `demo_gkxlumenx_ads.svc_org_card` / `demo_gkxlumenx_ads.svc_metric_series` / `demo_gkxlumenx_ads.svc_tech_power_score` / `gkxlumenx_topic_enterprise.svc_compare_basket_item` / `gkxlumenx_topic_enterprise.analysis_task`。零写操作。
- 样本满足：**否**
- 停止：继续（缺口待派 + 待补签发；无 token/映射/重复缺口停止）

### 步① 探测

- token 文件存在且非空（值不入档）；`POST /tts/svcz/api/enterprise/topic/v1/recommend`（头 `authorization: Bearer <token>` + `systemcode: topic`，body `{"count":1}`）→ **HTTP 200，code=0**，返回 1 条机构卡（广州集趣…）。轮首探测通过，进样本对照。

### 步② 批次前置与库侧真值

| 核对项 | 实查 | 与用例/计划 | 结论 |
|---|---|---|---|
| `svc_org_circle` 批次 | 单批次 `svc-fseed-20261020`，43,296 行 | 同 | ✅ 无重灌 |
| `svc_tech_power_score` 批次 | `calc_batch_id=svcmodels_20261107_155402`（列名实况；计划写作 etl_batch_id 为同义笔误），300 行，`model_version=svc_proxy_v1.3` | 同 | ✅ 无重灌 |
| 机构集合 5 org_id（双奉/君智容/星诚优威/航羿/中科为） | 5/5 命中 `svc_org_card`，名称与类型候选（INNOV×3、IP×2）一致 | 同 | ✅ |
| 趋势 2022–2026（`svc_metric_series.M_SVC_ORG_NEW_COUNT`，列 `period`/`value`） | 2779 / 2330 / 1885 / 1251 / 36 | 同值同序 | ✅ |
| 评分两行（君智容/星诚优威） | score 均 40.0000，`SVC_INNOV_TECH_POWER`，weights 五维各 20，dimension_scores 0/1（cases=1、rdInvestment=1、其余 0），ext.name 同名 | 分值/权重/形态一致 | ✅ |
| **对比篮 `svc_compare_basket_item`（guest）** | **实查仅 2 行：id=62 东莞东劲新能源（0071aadf…）、id=63 东莞双奉（007050fc…）；用例期望 6 行（含君智容 id=60、星诚优威 id=61）缺 4 行** | **不一致** | ❌ DATA 缺口 |

### 步③ 逐行对照（接口值 vs 库值 vs 期望；本轮默认不签发，只读复用既有 success 快照）

| 需规行 | 复用快照（HTTP） | 期望（用例） | 接口实测（result 载荷，经 target_params.result_payload） | 库值 | 判定 |
|---|---|---|---|---|---|
| 7.1.1 覆盖分析 | `SVC-20261107-019`（coverage，200/success，同型 2 家） | 3 家 matrix：双奉 82 / 君智容 91 / 星诚优威 66；`org_count=3`、`avg_breadth≈2.24` | matrix 4 格：君智容 INB1309/INB170102 均 **91**、星诚优威均 **66**；summary `avg_breadth=2.24`；`yellow_gaps=[Q-SVCCHAIN-02, GAP-SVC-MATRIX-SRC]`、`pending_client_confirm=1` | 3 家 org_id 全在 `svc_org_card`；**双奉 82 无任何库侧/快照承载面**（含 007050fc… 的 success coverage 任务 5 条全是 2026-10-21/22 旧波，`matrix=[]`） | 部分：君智容 91 / 星诚 66 / breadth ✅；**双奉 82 无证据 → 待补签发（监管人说「签发」后按用例请求列 POST 一次）** |
| 7.1.2 矩阵图 | 同 019（读同 taskId，200） | 四象限 3 点：广度 2 × 深度 82/91/66；切回热力图同源 | 同一份 matrix：每家广度=2 格、深度 91/66 实值；`avg_depth=480.56`（快照原始累计口径，用例已注明两口径差） | 同上 | 部分：随 7.1.1（缺第三家点）；已载值 ✅ |
| 7.2.1 新增趋势 | `SVC-20261106-008`（trend，200/success，INB1309 行） | 9 曲线 × 17 点；2010=1,501；2022–2026=2779/2330/1885/1251/36；window_hint 全量截窗 | series 9 曲线×17 点；「全部」「人工智能」两曲线 2010=1501、近窗五点 **逐点全等**；`window_hint` 逐字一致；`yellow_gaps=[GAP-SVC-TREND-FIELD, Q060]` | ADS `svc_metric_series` 五点同值同序 | ✅ 对上（接口+库双证） |
| 7.2.2 市场热度 | 同 06-008（读同 taskId） | INB1309 1 星低迷三行原文（1057.3 / 2938.7 / -64.0%）；INB2503 1 星低迷 -67.5%；INB1204 insufficient 不评级 | heat 段 INB1309 / INB2503 / INB1204 三行 **逐字一致**（含「序列仅 2 个年度点，不足 3 点不评级」、stars=null） | 同快照 yellow_gaps + pending=1 | ✅ 对上（演示规则判定口径，🧪） |
| 7.3.1 技术力评估 | `SVC-20261107-020`（tech_power，200/success，同 2 家） | INNOV 两行 score 恒 40.0 **同分并列 rank_no 1/2**；批次 v1.3；weights 五维等权 20 | 两行 score=40.0 ✅、dimension_scores 0/1 ✅、weights 等权 20 ✅；**但 rank_no=26 / 50（全池 300 行全局序，非选定集合展示序 1/2）**；**payload 自报 `model_version=svc_proxy_v1.2`（库批次行是 v1.3）** | `svc_tech_power_score` 两行 40.0、weights 等权、批次 `svcmodels_20261107_155402` + `svc_proxy_v1.3` | 部分：分值/权重 ✅；**rank 展示序 + 版本自报 ❌ → ALGO** |
| 7.3.2 雷达对比 | 同 020（读同 taskId） | 五维 0/1 归一后重合（演示态）；同分稳定序 1/2 | dimension_scores 0/1 两行一致（归一后重合实情成立）；并列序同 7.3.1 问题（26/50） | 库 dimension_scores 两行一致 | 部分：多边形重合 ✅；**并列序随 ALGO 单** |

输入前置（非需规行）：7.1.1/7.3.1 的「从对比篮直勾 id 57/60/61」在当前库不可复现（见步②对比篮缺口）。

### 步④ 缺口分类与子任务

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `gkxlumenx_topic_enterprise.svc_compare_basket_item.user_id=guest.{004671cd…,007d0adc…}` | DATA | 篮内仅 2 行（id=62 东劲、id=63 双奉），君智容/星诚优威及另 2 行缺失 | 用例查库节 6 行（含 id=60/61） | 按 2026-11-05 操作语义补回缺行（source=对比篮新增；行 id 允许漂移） | `SVC-ORG-DEMO-FIX-R20261107-DATA`（ready） |
| `analysis_task.svc:analysis:org_coverage.{三家组合}` | QUERY | 含三家 org_ids 的 success 任务 0 条；双奉 82 深度无承载面 | 7.1.1 三家 matrix（82/91/66） | 监管人明确说「签发」后按用例请求列 POST 一次，新快照核 depths（依赖 DATA 单先修篮） | `SVC-ORG-DEMO-FIX-R20261107-QUERY`（ready；本轮未 POST） |
| `analysis_task.SVC-20261107-020.result_payload.tech_power.rows.rank_no / model_version` | ALGO | 同分两行 rank_no=26/50（全池序）；payload 自报 v1.2 | 选定集合内并列 rank_no 1/2；自报版本与批次 v1.3 一致 | 快照装配层按选定集合重排展示序；model_version 自报取源表批次值。**不改库内 40/20 恒分**（Q-SVCCHAIN-01+Q060 演示态声明） | `SVC-ORG-DEMO-FIX-R20261107-ALGO`（ready） |

- 去重：`task-query` 无同缺口键既有未完成单（现存 DEMO-FIX 单均为政策模块），3 张均新建。
- 按计划 §6：子任务只核对/登记/报告；本轮只建单升 ready、不认领、不改库、不改代码、未签发新分析任务。

### 结论与下一轮建议

- 6 行：2 行对上（7.2.1 / 7.2.2）、4 行部分（7.1.1 / 7.1.2 / 7.3.1 / 7.3.2），样本未满足，验收单留 `ready`。
- 顺序建议：先派 DATA 修篮 → 监管人「签发」后 QUERY 单建三机构快照 → ALGO 单修展示序与版本自报 → 重开第 2 轮验收。
- 成本：本轮远低于 $10 告警线（cost_warn=green）。
- 脱敏：本轮无口令、token 入档；token 文件只读未改。
