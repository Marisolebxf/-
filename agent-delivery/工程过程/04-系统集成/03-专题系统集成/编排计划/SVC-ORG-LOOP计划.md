# 服务机构分析（SVC-ORG）· LOOP 执行编排计划

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 任务：`SVCCHAIN-DC-M3-ORG-L01`（长任务总控 `SVCCHAIN-合规演示用例-长任务总控.md` §4；本计划为 M3a 产物，只写不建单）
- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-ORG-合规演示用例.md`
- 系统：科技信息展示系统 · 科技专题服务系统「产业服务链分析 · 服务机构分析」。不打开页面。
- 监管人：`human:徐滕强`
- 日期：2026-11-07

- 状态：**第 1 轮完成（2026-11-07）：6 行中 2 行对上（7.2.1 趋势 / 7.2.2 热度，接口+库双证逐点全等）/ 4 行部分对上（7.1.1、7.1.2 缺东莞双奉 82 深度证据=待补签发；7.3.1、7.3.2 同分展示序 26/50≠1/2 + 快照自报 v1.2≠批次 v1.3=ALGO）；DATA 缺口 1 条（对比篮 guest 实查 2 行 vs 期望 6 行，缺君智容/星诚优威 id=60/61）。子任务 SVC-ORG-DEMO-FIX-R20261107-DATA（demo-algo-ent-analysis，data-agent）/ -QUERY（lumen-svc-platform，api-agent，待监管人「签发」后执行）/ -ALGO（lumen-algo-py，algorithm-agent）已建并升 ready，等人说「可以派了」。批次无重灌（svc-fseed-20261020 / svcmodels_20261107_155402）；探测 200 通过；快照复用 SVC-20261107-019/020、SVC-20261106-008。样本未满足，验收单 SVC-ORG-DEMO-ACCEPT-LOOP 留 ready（不签 done）；报告已追加至 agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-ORG-DEMO-ACCEPT-LOOP.md「## 运行 2026-11-07」。**

覆盖表 6 行全部「可演」（期望值 = 2026-11-05/06/07 三天任务快照实值 + 库侧 ADS/dwd 实查值双证）。口径核对在按 LOOP 跑时才逐行做：深度（Q-SVCCHAIN-02）、热度（Q-SVCCHAIN-02 + GAP-SVC-ORG-HEAT）、技术力（Q-SVCCHAIN-01 + Q060）三处演示态口径行按「演示规则判定」核对，不判业务对错。不派数据单，不派算法单，不打探测。

## 1. 常驻验收单（建议 ID，本计划只写不建）

- 建议 ID：`SVC-ORG-DEMO-ACCEPT-LOOP`（§6.5.2；等人说「按 LOOP 跑」后由 coordinator 建，不把这张单签 `done`）
- 建单前置：总控 `SVCCHAIN-合规演示用例-长任务总控.md` 仍在授权期内；M3a 产物已签收
- 建单后必填：`claim_type=coordinator_dispatch`、`supervised_by=human:徐滕强`、`task_type=chore`（跑批性质，豁免签收）

## 2. 先决条件

1. 用例文件（上文路径）已签收且本轮未被改动；查库节时间戳之后 `svc_org_circle` / `svc_org_card` / `svc_tech_power_score` / `svc_metric_series` 无重新灌批（`etl_batch_id` 仍为 `svc-fseed-20261020` / `svcmodels_20261107_155402`）。若发生重灌，先重跑一轮探测再对照。
2. 库入口连接可用：database-mcp 组 `gkx-mysql` → `demo-gkxlumenx-ods`（跨库限定名查 `demo_gkxlumenx_ads` / `demo_gkxlumenx_dwd` / `gkxlumenx_topic_enterprise`）。**严格只读**；SELECT 失败 2 次 → 该步记受阻即停，禁止探活。
3. 前端真源只读对照仓 `repos/demo-ui-topic`（`src/app/pages/service-center/*`）在本地可用，仅作条件枚举/常量核对，不改代码。
4. 页面可达性探测属 LOOP 轮次内动作，本计划不预检。

## 3. 纯后端 token 熔断约定

- token 文件：`~/.gkx/topic-loop-token`
- 轮次内所有后端请求头带 `systemCode: topic`
- 每轮开工先校验 token 文件存在且未过期；缺失/过期 → 该轮记 ENV 缺口即停，不重试 token 获取
- token 值不入档、不写进报告（脱敏铁律）

## 4. 一轮四步（每轮）

| 步 | 动作 | 产物 |
|---|---|---|
| ① 探测 | 校验 token + `systemCode: topic` 后端会话可用；只探测本轮行清单涉及的分析链路端点（`POST /topicAsync/topic/v1/analysis/tasks` / `GET …/tasks/{taskId}` / `GET …/tasks/{taskId}/result`，svc 白名单 `svc:analysis:org_coverage\|org_trend\|tech_power`），不打全量 | 轮日志·探测节 |
| ② 只读库+调接口 | 按本轮行清单：SELECT 对应 dwd/ads/topic 面（只读）+ 按用例覆盖表逐行调接口（创建/详情/结果，只读性质；POST 仅限用例请求列写明的分析创建）+ 对照期望逐值核 | 轮日志·对照节（逐行 差值/一致） |
| ③ 对照 | 期望值 vs 实测值：逐行核对机构名/org_id/depth/stars/分值/rank_no（重点=7.1.x 矩阵行、7.2.2 依据行三行原文、7.3.x 40.0 恒分与并列序） | 差异清单（分缺口类型） |
| ④ 缺口分类 | 每条差值落 DATA / QUERY / ALGO / ENV 四类之一（§5 表），不新造编号，引用 Q-SVCCHAIN-01/02/09、Q060、GAP-SVC-ORG-HEAT、GAP-SVC-TREND-FIELD 既有集合 | 分类结论 → 决定是否开子任务 |

一轮四步走完即收轮；不做步⑤「顺手修」。每轮 ≤3 张子任务（见 §6）。

## 5. 缺口分类表（本轮预判，执行时按实测修正）

| 缺口现象（预期） | 分类 | 既有引用 | 处置 |
|---|---|---|---|
| 7.1.1/7.1.2 深度值（82/91/66 型）无库侧 ADS 面，仅任务快照承载，`svc_org_card` 无机构×领域深度列 | **DATA**（覆盖矩阵 ADS 面缺） | Q-SVCCHAIN-02 | 快照值与库实查对照登记；不建新表（建表=另行立项） |
| 7.2.2 研判星级/依据行为演示规则计算（近 3 年 vs 前 3 年增速分档），口径未过甲方 | **ALGO**（评级规则） | Q-SVCCHAIN-02、GAP-SVC-ORG-HEAT、快照 `yellow_gaps=GAP-SVC-TREND-FIELD/Q060` | 按「演示规则判定」核对，不判业务结论；等唐绍祖定义卡 |
| 7.2.1 曲线末端 2026=36 骤降（ADS `svc_metric_series` 2026 年值 36 vs 2025=1,251），趋势年份数据不完整 | **DATA**（年度数据未齐年） | Q-SVCCHAIN-02（趋势口径） | 登记末端年骤降差异；不灌数 |
| 7.3.1/7.3.2 `svc_tech_power_score` 恒定分 40/20 两档、无个体区分度；雷达多边形重合 | **ALGO**（评分模型区分度） | Q-SVCCHAIN-01、Q060、`model_version=svc_proxy_v1.3` | 按「演示态声明」核对并列序；模型升级不在 LOOP 内 |
| 7.3.1 `cap_w="25,25,20,20,10"`（前端默认）与库侧 `weights` 五维各 20（等权）不一致 | **DATA**（两轨权重口径） | Q060（项目临时基线=等权） | 登记两轨差；不改前端默认、不灌库 |
| `POST …/analysis/tasks` 创建失败 / Python `/internal/gkx-svc/*` 不可达（算法服务未上线，51 条 D4=mock 维持） | **ENV** | as-built `ENV-SVC-ORG-FIELD-CREATE-404` / `ENV-SVC-ORG-TREND-CREATE-404` | 任务链不可用时改读既有成功快照（org_coverage 57 / org_trend 28 / tech_power 27 条 success）对照；记受阻即停轮 |
| token 失效 / 库连接拒 | **ENV** | 总控 §5；ssh/库铁律 | 记受阻即停；不探活、不重试第三轮 |
| 机构集合行（7.1.1 三家 / 7.3.1 两家）在 `svc_org_card` 0 命中（批次重灌后 org_id 漂移） | **DATA**（主档漂移） | M2 §1.3 | 以当前批次重查机构键，更新用例行前先报监管人 |

## 6. 子任务规则

- 每轮最多 **3 张**，ID 形如 `SVC-ORG-DEMO-FIX-R{YYYYMMDD}-*`（R+轮次日期；`*`=缺口关键词，如 `DEPTH-SNAPSHOT` / `HEAT-RULE` / `TECH-CONST-SCORE`）
- 子任务只做核对/登记/报告，**不派修数单、不派算法单、不派前端改码单**（那是 LOOP 之外的正常任务流）
- **同缺口连续两轮不收敛 → 停**：第 3 轮起不再为该缺口开子任务，升级监管人 `human:徐滕强`，该缺口在报告挂「两轮停」标记
- 子任务创建动作（task-create）在建单之后由 coordinator 执行；本轮计划不建任何单

## 7. 库表清单（引用 M2 调研 + M3a 查库节）

| 面 | 表（跨库限定名） | 用途 |
|---|---|---|
| 机构池主档 | `demo_gkxlumenx_dwd.svc_org_circle`（43,296 行；`service_type_candidate` 六类 + `pending_client_confirm`） | 7.1.1 机构池/类型候选对照 |
| 机构卡面 | `demo_gkxlumenx_ads.svc_org_card`（43,343 行；`org_id`/`name_cn`/`city`/`area`/`service_type_candidate`） | 机构集合行真值、检索前置对照 |
| 对比篮 | `gkxlumenx_topic_enterprise.svc_compare_basket_item`（6 行 guest） | 7.1.1/7.3.1 篮选机构核对 |
| 任务面 | `gkxlumenx_topic_enterprise.analysis_task`（svc 类 `analysis_type` 前缀 `svc:analysis:*`；success 295） | 快照对照（`target_params.result_payload.matrix/series/heat/tech_power`） |
| 技术力评分 | `demo_gkxlumenx_ads.svc_tech_power_score`（300 行 6 模型×50 机构恒 40/20；`ext.name`/`weights`） | 7.3.1/7.3.2 分值与权重两轨核对 |
| 趋势序列 | `demo_gkxlumenx_ads.svc_metric_series`（`M_SVC_ORG_NEW_COUNT` 49 行 1978–2026） | 7.2.1 曲线末端值核对 |
| 区域（旁证） | `demo_gkxlumenx_ads.svc_region_dist`（sz_district 18 行） | 检索前置「高级筛选」地域字段旁证 |
| 前端枚举 | `repos/demo-ui-topic/src/app/pages/service-center/*`（只读：`CLUSTER_SEED`、`TrendView` 时间窗、`defaultEvalConfig` 权重） | 条件枚举真源核对 |

## 8. 报告与状态行

- 报告路径：`agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-ORG-DEMO-ACCEPT-LOOP.md`（与验收单同 ID；**只追加**，每轮一节，不回写历史节）
- 报告内容：轮次 / 四步结果 / 差异清单 / 缺口分类 / 子任务 ID 与状态 / 下一轮建议
- 脱敏：token、连接串、口令一律不入报告
- 状态行（本计划）：**覆盖已齐，未执行。等人说「按 LOOP 跑」。**
