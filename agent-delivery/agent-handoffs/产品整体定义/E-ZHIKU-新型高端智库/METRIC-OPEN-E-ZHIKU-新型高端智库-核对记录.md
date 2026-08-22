# METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录

> **起草**：AI（product-agent 角色，兼 algorithm/data-agent 角色代行）代 human:淮政玮 直出草稿；语义 Owner 何老师 / 合规 Owner 郭万迎未会签。
> **日期**：2026-08-04
> **适用性判定**：本模块含统计数字（如"我的报告任务总数""待发布审核任务数""案例总数""素材文件总数"等），**指标语义卡适用，非 N/A**。

> **LOOP Round 7 补登记（2026-08-22）**：任务 `ZHIKU-METRIC-OPEN-L01`。本轮**只补会签栏**（§6 / §7），**不从零重写** §1 ④ 指标语义卡、§2 算法项、§4 ⑤ 开放项。`owner_semantic=human:淮政玮`；公式 / `algorithm_type` = `pending_cosign: human:唐绍祖`。演示态 🔴 不得转正。Q-ZHIKU-* 保持待登客户决策清单（不升 🟢）。不改 seed。不另开 `E-ZHIKU-METRIC-OPEN-L01`。

---

## 1. 指标语义卡（当前已落地批次：S1 智能写作链路 + S2 研究需求/技术体系分析 + S3 技术趋势/领域技术线路 + S4 科技人才智慧服务 + S5 基础研究智能决策）

> 真源：`demo-ui-gaoduanzhiku-view/src/mock/metricSeed.ts`（原型阶段镜像；正式接口为 Java REST `/metrics/v1/catalog`，本项目尚未接入）。

| metric_id | 中文名 | 口径定义 | 公式 | 源表 | 源系统 | 更新频率 | 版本 | mapping_status |
|---|---|---|---|---|---|---|---|---|
| `ZHIKU-S1-TASK-TOTAL` | 我的报告任务总数 | 当前账号下创建的全部报告创作任务数（研究/战略/洞察三态合计） | `count(report_task) where owner_id = current_user` | `ads_zhiku_writing_task`（拟） | Mock（S1 批次） | 实时 | 0.1.0 | 🟡 临时默认（前端 Mock，无三方源） |
| `ZHIKU-S1-TASK-PENDING-REVIEW` | 待发布审核任务数 | 状态为"待发布审核"的报告任务数 | `count(report_task) where status = pending_review and owner_id = current_user` | `ads_zhiku_writing_task`（拟） | Mock（S1 批次） | 实时 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S1-CASE-TOTAL` | 案例广场案例总数 | 案例广场当前可检索展示的战略咨询成果案例总数 | `count(strategy_case) where visibility = public` | `ads_zhiku_strategy_case`（拟） | Mock（S1 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S1-INSIGHT-TOTAL` | 洞察报告库报告总数 | 洞察报告库当前可检索展示的洞察报告总数 | `count(insight_report) where visibility = public` | `ads_zhiku_insight_report`（拟） | Mock（S1 批次） | 每月 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S1-MATERIAL-TOTAL` | 我的素材库文件总数 | 当前账号素材库中已上传并完成解析的素材文件总数 | `count(material_file) where owner_id = current_user and parse_status = done` | `ads_zhiku_material_file`（拟） | Mock（S1 批次） | 实时 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-ENTITY-TOTAL` | 科技实体清单总数 | 当前筛选条件下命中的科技实体总数 | `count(tech_entity) where filter_match = true` | `ads_zhiku_tech_entity`（拟） | Mock（S2 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-TREND-TECH-TOTAL` | 技术趋势分析·技术总量 | 技术趋势分析页宏观统计卡片覆盖的技术条目总数 | `count(distinct tech_id) from dwd_tech_trend_stat` | `ads_zhiku_tech_trend_stat`（拟） | Mock（S2 批次） | 每周 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-TECHSYS-TOTAL` | 技术体系总数 | 当前账号可见的技术体系（树形结构）总数 | `count(tech_system) where visibility = current_scope` | `ads_zhiku_tech_system`（拟） | Mock（S2 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-PAPER-TOTAL` | 论文分析总览·论文总数 | 论文分析总览页当前统计口径下的学术论文总数 | `count(paper) where indexed = true` | `ads_zhiku_paper_stat`（拟） | Mock（S2 批次） | 每周 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-PROJECT-TOTAL` | 科研项目统计·项目总数 | 科研项目统计分析仪表盘当前口径下的项目总数 | `count(research_project) where status != archived` | `ads_zhiku_research_project`（拟） | Mock（S2 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S2-NETWORK-NODE-TOTAL` | 社会网络分析·节点总数 | 社会网络可视化当前分析结果的节点（实体）总数 | `count(distinct node_id) from dwd_social_network_result` | `ads_zhiku_social_network_result`（拟） | Mock（S2 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S3-CLUSTER-TOTAL` | 聚类分析·簇总数 | 当前聚类任务结果中生成的簇（分组）总数 | `count(distinct cluster_id) from dwd_tech_cluster_result` | `ads_zhiku_tech_cluster_result`（拟） | Mock（S3 批次） | 每周 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S3-HOTSPOT-TOTAL` | 技术热点·热点词总数 | 当前统计周期内识别出的技术热点词条总数 | `count(distinct hotspot_term) from dwd_tech_hotspot_stat` | `ads_zhiku_tech_hotspot_stat`（拟） | Mock（S3 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S3-TREND-FORECAST` | 发展趋势·预测区间 | 前端演示态趋势外推区间（**非算法产出**，仅供 UI 演示，禁止用于对外决策展示） | 前端本地简单线性外推（非真实预测算法） | — | 前端 Mock 演示态（无源表） | — | 0.1.0 | 🔴 演示态（非真实指标，禁止转正生产） |
| `ZHIKU-S3-ALERT-PENDING` | 动态预警·未处理预警数 | 状态为"未处理"的技术动态预警事件数 | `count(tech_alert) where status = pending` | `ads_zhiku_tech_alert`（拟） | Mock（S3 批次） | 实时 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S3-DELPHI-COMPLETION` | 德尔菲问卷·完成率 | 当前问卷的专家回收完成率 | `count(respondent) where submitted = true / count(respondent) where invited = true` | `ads_zhiku_delphi_survey`（拟） | Mock（S3 批次） | 实时 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S3-ROADMAP-PROJECT-TOTAL` | 技术发展路线·在建项目数 | 当前技术发展路线图中状态为"在建"的路线图项目总数 | `count(roadmap_project) where status = in_progress` | `ads_zhiku_roadmap_project`（拟） | Mock（S3 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S4-TALENT-INFLUENCE-SCORE` | 人才关联信息·成果影响力/贡献度得分 | 学者成果影响力雷达图综合得分（被引/合作广度/产出速度/新颖度/权威度 5 维加权） | 前端本地等权重求和（演示态，非正式算法） | `ads_zhiku_talent_influence`（拟） | Mock（S4 批次） | 每周 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S4-TALENT-GROWTH-INDEX` | 人才行为信息·成长指数 | 学者科研成长轨迹综合指数（累计产出趋势加权） | 前端本地简化公式（演示态，非正式算法） | `ads_zhiku_talent_growth`（拟） | Mock（S4 批次） | 每月 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S4-TALENT-DOMAIN-NODE-TOTAL` | 人才库-领域分类·节点总数 | 九大类人才分类树当前展开范围内的节点（含子类/叶子）总数 | `count(distinct node_id) from dwd_talent_domain_tree` | `ads_zhiku_talent_domain_tree`（拟） | Mock（S4 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S4-TALENT-MAP-DIST-TOTAL` | 人才地图·分布总数 | 当前地图视图筛选条件下命中的人才/机构地理分布点总数 | `count(distinct point_id) from dwd_talent_map_dist where filter_match = true` | `ads_zhiku_talent_map_dist`（拟） | Mock（S4 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S4-TALENT-INDEX-SCORE` | 人才指数·综合得分 | 区域/产业人才支撑能力综合指数（数量/科研产出/学术影响力/产业贡献度/流动活跃度 5 维加权） | 前端本地权重求和（演示态，**权重算法定义卡未落地，见 §2 序号 76**） | `ads_zhiku_talent_index`（拟） | Mock（S4 批次） | 每周 | 0.1.0 | 🔴 演示态（算法未落地，禁止转正生产） |
| `ZHIKU-S4-TALENT-COCKPIT-ALERT` | 人才驾驶舱·统计卡+趋势预测 | 驾驶舱大屏顶部统计卡数值 + 趋势预测时间轴（预测区间**非算法产出**，仅供 UI 演示） | 统计卡：`count`/`sum` 聚合；预测：前端本地简单线性外推（非真实预测算法） | `ads_zhiku_talent_cockpit`（拟） | Mock（S4 批次） | 实时（统计卡）/ — （预测） | 0.1.0 | 🔴 演示态（预测部分禁止转正生产，统计卡部分待接入转 🟡） |
| `ZHIKU-S5-ISSUE-TOTAL` | 基础研究问题清单·问题总数 | 当前基础研究问题清单中已识别/在线发布的问题总数 | `count(basic_research_issue) where status = published` | `ads_zhiku_basic_research_issue`（拟） | Mock（S5 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S5-ISSUE-HEAT-SCORE` | 问题发展趋势·研究热度/潜力评估得分 | 单个基础研究问题的研究热度与潜力量化得分 | 前端本地简化打分（演示态，非正式"时序+文献引用+成果"综合模型） | `ads_zhiku_issue_trend`（拟） | Mock（S5 批次） | 每周 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S5-COMPETITION-INDEX` | 竞争格局报告·区域对比指数 | 国际/国家/深圳市三层次的研究热度/前沿引领性/投资力度/研究主体总量综合对比指数 | 前端统计聚合演示态（是否需独立权重算法待确认，见 §2 序号 84） | `ads_zhiku_competition_landscape`（拟） | Mock（S5 批次） | 每月 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S5-DEPLOY-TOTAL` | 深圳市基础研究部署清单·清单总数 | 深圳市基础研究部署清单当前收录的部署条目总数 | `count(deploy_item) where city = '深圳'` | `ads_zhiku_deploy_list`（拟） | Mock（S5 批次） | 每日 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S5-ORG-CAPABILITY-SCORE` | 组织实施分析·核心能力/资源保障得分 | 学科覆盖/人才品质/机构资源/经费投入/管理机制 5 维核心能力量化得分 | 前端本地等权重求和（演示态，非正式算法） | `ads_zhiku_org_capability`（拟） | Mock（S5 批次） | 每月 | 0.1.0 | 🟡 临时默认 |
| `ZHIKU-S5-EVAL-SCORE` | 基础研究成果评估·四维量化得分 | 应用性/理论价值性/创新性/学术影响力 4 维量化综合评价得分 | 前端本地等权重求和（**演示态，算法定义卡未落地，见 §2 序号 87**） | `ads_zhiku_research_eval`（拟） | Mock（S5 批次） | 每月 | 0.1.0 | 🔴 演示态（算法未落地，禁止转正生产） |

**国标/世标引用**：以上 28 项均为内部管理型统计指标（任务数/案例数/文件数/实体数/节点数/簇数/预警数/指数计数/评估得分），不涉及国标/世标口径，无需引用。

**数据裁剪说明**：原型阶段（`demo-ui-gaoduanzhiku-view` 为纯前端 Mock 原型，无后端依赖，已在原型规划方案 §1.2 确认）全部指标均为前端 Mock 直代，源表/源系统均为"拟"（尚未建表，仅记录未来 ADS 表命名意图），`mapping_status` 统一 🟡（`ZHIKU-S3-TREND-FORECAST`/`ZHIKU-S4-TALENT-INDEX-SCORE`/`ZHIKU-S4-TALENT-COCKPIT-ALERT`/`ZHIKU-S5-EVAL-SCORE` 例外，标 🔴 演示态，因其非真实算法产出或含预测区间，不适用"待接入转 ✅"路径，需在对应页面 UI 上明确禁止转正展示），待正式接入 `gkxlumen-metrics` 后其余 🟡 项转 ✅。

---

## 2. 算法/权重相关指标（本模块范围内识别，尚未落地）

拆解表中含评估/排名/综合得分类描述的功能项（后续批次落地时须补算法定义卡，本轮先行登记，不代表已完成）：

| 拆解表序号 | 功能名 | 涉及算法/权重 | 状态 |
|---|---|---|---|
| 76 | 人才指数 | 量化评估区域/产业人才支撑能力（数量/科研产出/学术影响力/产业贡献度/流动活跃度），支持权重定制化 | 🔴 UI 已按 Wireframe P61 落地（`ZHIKU-S4-TALENT-INDEX-SCORE` 前端等权重求和演示态），**正式算法定义卡仍未落地**，need algorithm-agent 补 `metric-spec-高端智库-人才指数-algorithm.yaml`（模型 ID/维度/权重/公式）后方可转正对外展示，当前 UI 已标注"演示态"禁止转正 |
| 87 | 基础研究成果评估 | 从应用性/理论价值/创新性/学术影响力四维量化分析与综合评价 | 🔴 未落地，S5 批次开工前需补算法定义卡 |
| 84 | 国内外竞争格局报告 | 研究热度/前沿引领性/投资力度/研究主体总量的统计与可视化对比 | 🟡 偏统计聚合，是否需要独立权重算法待 S5 批次与算法 Lead（唐绍祖）确认 |

---

## 3. 数据贴源与开放项适用性

| 项 | 结论 |
|---|---|
| 是否涉及贴源/Mapping/调度（PDR-13） | 原型阶段**不涉及**（纯前端 Mock，无 ODS/DWD 接入），`N/A`，依据：原型规划方案 §1.2 "纯前端可演示：单页应用 + Mock 数据，开箱即跑，无后端依赖" |
| `data-gap-catalog.yaml` | 本轮**未创建**，原因：原型阶段全部指标为 Mock，无三方源缺口需要挂 PendingBadge 文案（`MetricSpecCard` 已通过 `readinessSeed.ts` 统一标注 `source.status: none` + `ingestion.status: mock`），待接入 `gkxlumen-metrics` 后按 `data-lineage-policy.md` §5.1.4 补建 |

---

## 4. 开放项汇总（同步至客户决策清单跟踪表.md 前的草稿登记）

> **重要**：以下开放项**尚未由 human:郭万迎 同步至** `客户决策清单跟踪表.md`（该表为 PM 专属维护，AI 不代为写入，避免越权）。本记录作为待同步草稿，附 Q-ZHIKU-xx 临时编号，供 PM 复核后正式分配 Q0xx 编号。

| 临时编号 | 标题 | 影响范围 | 建议临时默认值 | 状态 |
|---|---|---|---|---|
| Q-ZHIKU-01 | 战略咨询/科技人才服务模块用户角色（R3）未在拆解表给出岗位 persona | US-ZHIKU-01/02/03/04/08/09/10/11（战略咨询智能支持 + 科技人才智慧服务全部故事） | 团队暂用"R3-待业务确认"占位，不展示为正式角色名 | 🟡 待业务确认 |
| Q-ZHIKU-02 | 拆解表条目 52（热点分析）/101（图表样式切换）/105（一键跳转原文）页面归属未在原型规划方案给出 | US-ZHIKU-05、US-ZHIKU-16 | 52→暂并入 P10 洞察详情；101→暂并入 writing/create；105→暂并入 strategy/report-mgmt（均已在 `docs/coverage-matrix-110.md` 标 ⚠） | 🟡 待核实 |
| Q-ZHIKU-03 | 权限体系 L0-L4 与本模块角色的映射拆解表未给出 | 全模块 IA §2 | 原型阶段不做登录/权限拦截 | 🟡 待业务确认 |
| Q-ZHIKU-04 | 人才指数（76）/竞争格局区域对比（84）/基础研究成果评估（87）的权重算法细节拆解表未给出计算公式 | US-ZHIKU-10、US-ZHIKU-15 | 暂用等权重占位（S4/S5 批次已落地为 Mock 演示态，`ZHIKU-S4-TALENT-INDEX-SCORE`/`ZHIKU-S5-COMPETITION-INDEX`/`ZHIKU-S5-EVAL-SCORE` 均标 🔴/🟡 明确禁止参与真实排名对外展示） | 🔴 未落地，阻断对应批次 PDR-05/06 闭合 |
| Q-ZHIKU-05 | 人才画像·心理信息（62：科研诚信/意识形态/舆情/文本情感分析）的采集范围与展示边界未在拆解表给出合规口径 | US-ZHIKU-04（人才画像） | S4 批次先以纯前端 Mock 结构演示（P56 Tab-4），UI 已标注"高敏感字段·演示态"提示，暂不接入真实数据源 | 🟡 待合规 Owner 郭万迎确认采集/展示边界后方可推进真实数据接入 |

---

## 5. 结论

| 检查点 | 结论 |
|---|---|
| PDR-05（统计字段有 metric_id） | S1（4 项）+ S2（6 项）+ S3（6 项）+ S4（6 项）+ S5（6 项）已落地 ✅；S6 未落地部分 `N/A`（页面未建），批次开工后需补 |
| PDR-06（指标语义卡含口径+数据裁剪） | S1+S2+S3+S4+S5 共 28 项已完成（本文件 §1，含 4 项演示态 🔴 明确标注禁止转正）；算法类（人才指数/竞争格局指数/成果评估）🔴 定义卡未完成，见 §2（相关 UI 已 Mock 落地但不代表算法闭合） |
| PDR-07（开放项已同步客户决策清单） | ❌ 尚未同步，本文件 §4 为草稿登记，需 human:郭万迎 复核后正式同步 |
| PDR-13（贴源/Mapping已对齐GDF） | `N/A`，依据见本文件 §3（纯前端 Mock 原型，无数据加工） |

> 本记录**不构成门 1 PDR 完整闭合**（PDR-07 未同步、部分算法定义卡未完成），仅作为 human:淮政玮 指令下的"五件套直出结果"之一，供团队内部工程推进与后续正式评审输入。

---

## 6. LOOP Round 7 会签栏（补登记 · 不重写 §1 / §4）

> 真源仍是上文 2026-08-04 草稿。本栏只补本工作流会签身份、A2 挂载指针与红线，**不改** §1 表内 29 枚 `ZHIKU-S*` 口径/公式/mapping_status，**不改** §4 `Q-ZHIKU-01`～`05` 原文。

| 会签项 | 值 | 说明 |
|--------|----|------|
| 任务 | `ZHIKU-METRIC-OPEN-L01` | LOOP Round 7；**不另开** `E-ZHIKU-METRIC-OPEN-L01` |
| 语义 Owner（本工作流） | `human:淮政玮` | `owner_semantic`；口径 / 8 件套身份 / 适用性。原起草栏「何老师未会签」仍保留，不回溯删除 |
| 公式共签 | `pending_cosign: human:唐绍祖` | 本 loop **不签**公式 / 权重 / `algorithm_type`；8/25 前不派唐绍祖开工本 loop |
| ④ 适用性 | **kit**（非整页 N/A） | 沿用文首判定；S1–S5 有统计数字 → 出卡。S6 未建页 → 仍 N/A（批次开工后补，不发明 ID） |
| ⑤ 开放项 | 已登记（§4 草稿） | `Q-ZHIKU-01`～`05` **保持待登** `客户决策清单跟踪表.md`（PDR-07 仍 ❌）；本叶不改该表、不升 🟢 |
| A2.2 消费页 | `page_id=E-ZHIKU` | `metrics/request/展示系统/pages/E-ZHIKU.yaml` + catalog DW16。10 子叶共用本父 OPEN，禁止再拆 10 页 |
| 专题 A2.1 catalog | **n/a** | 专题 catalog **无**智库页；不挂 `TOPIC-*` |
| 演示态 🔴 | **不得转正** | 见下表；差集保持 `n/a_ops`，禁止改 mapped / 写入 seed |
| seed | **未改** | 禁止发明 `M_ZHIKU_*` / 新 `ZHIKU-S*`；禁止把 `ZHIKU-S*` 当正式 `M_*` 进 `metrics/registry/` |

### 6.1 演示态 🔴 锁定（不得转正）

沿用 §1 `mapping_status`，本栏只锁定，不改原文色标。

| metric_id | 原文状态 | 本轮动作 |
|-----------|----------|----------|
| `ZHIKU-S3-TREND-FORECAST` | 🔴 演示态（非真实预测） | 保持 🔴；禁止转 ✅ / 禁止当生产指标 |
| `ZHIKU-S4-TALENT-INDEX-SCORE` | 🔴 演示态（算法定义卡未落地） | 保持 🔴；见 §2 序号 76 |
| `ZHIKU-S4-TALENT-COCKPIT-ALERT` | 🔴 演示态（预测部分禁止转正） | 保持 🔴；统计卡仍待接入，不在本叶转 🟡 |
| `ZHIKU-S5-EVAL-SCORE` | 🔴 演示态（算法未落地） | 保持 🔴；见 §2 序号 87 |

### 6.2 开放项保持（不升 🟢 · 不改 §4 原文）

| 临时编号 | 本轮 | 保持 |
|----------|------|------|
| Q-ZHIKU-01 | 不改挂、不关项 | 🟡 待业务确认 · 待登客户决策清单 |
| Q-ZHIKU-02 | 不改挂、不关项 | 🟡 待核实 · 待登 |
| Q-ZHIKU-03 | 不改挂、不关项 | 🟡 待业务确认 · 待登 |
| Q-ZHIKU-04 | 不改挂、不关项 | 原文 §4 为 🔴 未落地（阻断 PDR-05/06）；**不转正、不升 🟢**；待登清单 |
| Q-ZHIKU-05 | 不改挂、不关项 | 🟡 待合规 Owner 郭万迎确认 · 待登 |

### 6.3 A2 指针（本叶不改 catalog 正文）

本叶 **不改** `A2-GAP-page-catalog.yaml`、`pages/E-ZHIKU.yaml`、共享 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`、`LOOP-state.yaml`。指针写入 `_work/open-loop/ZHIKU-METRIC-OPEN-L01-a2-patch.yaml`，由 coordinator 合流。

| 层 | 路径 | 本叶要求 |
|----|------|----------|
| 核对记录 | **本文件**（补栏后） | `E-ZHIKU` 唯一 OPEN 真源；10 子叶共用 |
| A2 页 yaml | `展示系统/pages/E-ZHIKU.yaml` | 已 `metric_open_status: present`；Round 18 可补 `metric_open_task: ZHIKU-METRIC-OPEN-L01`。**库缺口 missing 不动**（本页 A=0） |
| A2.2 catalog | DW16 `E-ZHIKU` | 已有 `metric_open` 路径；合流时补 `metric_open_status: present` + task id。删「无 OPEN 叶」类句（本页本就有 OPEN） |
| 专题 catalog | — | **n/a**，无对应 page |

口径会签：`owner_semantic = human:淮政玮`；公式共签仍 `human:唐绍祖`。

---

## §赋号表（ID-ASSIGN 草稿 · 类型未签 · 2026-08-22）

> 本叶 **没有 `TEMP_*`**。非红身份 **保持 `ZHIKU-S*` 可追溯前缀**（ELEMENT=`COMMON` 只作卡面说明，**禁止**发明 `M_ZHIKU_*` / `M_TINDEX_*` / 新 `ZHIKU-S*`）。  
> `algorithm_type` = `suggested_unsigned`，未签。未写 seed / 展示 catalog / LOOP-state / 共享 QUESTIONS。库 missing 保持。禁止与 DS-30-THINKTANK、DS-13～16 混页。  
> 需求 29 枚（§1 表行；S1 实为 5 条，§5 旧写「S1（4 项）」不改原文）。

### 非红 25 · 保持 `ZHIKU-S*` → 建议类型

| ZHIKU-S*（正式草稿身份） | 建议类型 | Q |
|--------------------------|----------|---|
| `ZHIKU-S1-TASK-TOTAL` | STAT | — |
| `ZHIKU-S1-TASK-PENDING-REVIEW` | STAT | — |
| `ZHIKU-S1-CASE-TOTAL` | STAT | — |
| `ZHIKU-S1-INSIGHT-TOTAL` | STAT | — |
| `ZHIKU-S1-MATERIAL-TOTAL` | STAT | — |
| `ZHIKU-S2-ENTITY-TOTAL` | STAT | — |
| `ZHIKU-S2-TREND-TECH-TOTAL` | STAT | — |
| `ZHIKU-S2-TECHSYS-TOTAL` | STAT | — |
| `ZHIKU-S2-PAPER-TOTAL` | STAT | — |
| `ZHIKU-S2-PROJECT-TOTAL` | STAT | — |
| `ZHIKU-S2-NETWORK-NODE-TOTAL` | GRAPH | Q-MO-ZHIKU-03 |
| `ZHIKU-S3-CLUSTER-TOTAL` | STAT | — |
| `ZHIKU-S3-HOTSPOT-TOTAL` | STAT | — |
| `ZHIKU-S3-ALERT-PENDING` | STAT | — |
| `ZHIKU-S3-DELPHI-COMPLETION` | STAT | — |
| `ZHIKU-S3-ROADMAP-PROJECT-TOTAL` | STAT | — |
| `ZHIKU-S4-TALENT-INFLUENCE-SCORE` | COMPUTE | — |
| `ZHIKU-S4-TALENT-GROWTH-INDEX` | COMPUTE | — |
| `ZHIKU-S4-TALENT-DOMAIN-NODE-TOTAL` | STAT | — |
| `ZHIKU-S4-TALENT-MAP-DIST-TOTAL` | STAT | Q-MO-ZHIKU-02 |
| `ZHIKU-S5-ISSUE-TOTAL` | STAT | — |
| `ZHIKU-S5-ISSUE-HEAT-SCORE` | MODEL | Q-MO-ZHIKU-01 |
| `ZHIKU-S5-COMPETITION-INDEX` | COMPUTE | Q-ZHIKU-04（已有，不新开、不升 🟢） |
| `ZHIKU-S5-DEPLOY-TOTAL` | STAT | — |
| `ZHIKU-S5-ORG-CAPABILITY-SCORE` | COMPUTE | — |

### 红四枚 · 不得转正（demo_lock · 不赋正式号）

| metric_id | 本轮动作 | 建议类型 |
|-----------|----------|----------|
| `ZHIKU-S3-TREND-FORECAST` | **不得转正**；禁止 `M_*` 替换、禁止改 mapped | 不赋 |
| `ZHIKU-S4-TALENT-INDEX-SCORE` | **不得转正**；禁止发明 `M_TINDEX_*`；不与影响力得分合并 | 不赋 |
| `ZHIKU-S4-TALENT-COCKPIT-ALERT` | **不得转正**；统计卡不在本叶转 🟡；不拆新号 | 不赋 |
| `ZHIKU-S5-EVAL-SCORE` | **不得转正**；禁止 `M_*` 替换、禁止改 mapped | 不赋 |

**计数**：非红 25 · 红锁 4 · reuse 0 · 新编 `M_*` 0 · 叶级 Q-MO 3（另 Q-ZHIKU-01～05 待登不升 🟢）· STAT 19 / COMPUTE 4 / GRAPH 1 / MODEL 1。  
**禁止改挂**：`M_CHAIN_HOTSPOT_*` / `M_CHAIN_ACADEMIC_POWER` / `M_TALENT_*` / `M_ENT_GROWTH_POTENTIAL` / `M_SYNTH_VIT_*` / DS-30 / DS-13～16。  
**机器卡**：`metrics/request/_work/id-assign/ZHIKU-METRIC-OPEN-L01.yaml`；叶级 Q：`id-assign/ZHIKU-METRIC-OPEN-L01-questions.yaml`。

---

## 7. 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner（本工作流） | 淮政玮 | _口径草稿已有（2026-08-04）；补登记会签栏；适用性：E-ZHIKU **kit**；**赋号草稿** 非红 25 条保持 `ZHIKU-S*`（类型未签）见 §赋号表；红四枚 **不得转正**；S6 未建页 N/A；**未从零重写** ④⑤；零 `M_ZHIKU_*` / `M_TINDEX_*` 进 seed_ | 2026-08-22 |
| 公式 / `algorithm_type` | 唐绍祖 | _pending_cosign（8/25 前不派本 loop）_ | |
| 甲方 Q-ZHIKU-01…05 | — | 保持待登客户决策清单；不升 🟢；本叶不改跟踪表 | |
