# 科技发展态势 · 对接进度总台账（2026-11-03 实测）

> **性质**：只读核查留底。**零代码改动、零改绿、零 commit**。
> **口径**：所有「真实 / mock / 空 / 未对接」判定都以 **2026-11-03 11:15—11:20 实跑端点 + 直连库查行数** 为准，不引用历史结论。凡未实测的一律标「未验证」，不推测。
> **2026-11-03 13:00—14:00 补充实测**：`TrackingController` **13/13 端点全部跑通**（含本轮新增 `POST /report-remove`；`DELETE /parameter-templates/{key}` 15:20 补测：建临时模板 → 删除 `removed=true` → 列表回 5 条，`code=0`），结论回填 §五；mock 汇总表补「技术发展跟踪」行。
> **凭据**：久新 Doris `47.93.119.170:29030`（账号在 `_local/dw-docs/README.md`）、MySQL `10.50.11.76:3306/demo_gkxlumenx_ads|dim`（账号见 `gkxlumen-element/application-local.yml`）。**凭据不入任何仓内文件**。
> **配套台账**：mock 逐条清理清单见 `mock-ledger.md`（本文件只做状态汇总，不复制其清理动作列）；影响力专项见 `METRIC-LIB-ALGO-INFLUENCE-L01.md`；23 个算法指标可支持性见 `SITUATION-ENT-GAP-FILL-20261102.md` §十。

## 〇、范围声明

本台账覆盖 **`gkxlumen-display` 全部 13 个 controller（68 个端点）** + **11 个科创要素** + **566 个指标的就绪度**，以及前端 `lumen-ui-science-pc` 对应的展示页。

**不在本台账范围**（未验证，不臆断）：`gkxlumen-element` / `gkxlumen-innov` / `gkxlumen-datacatalog` 自身的内部端点、算法库 `demo-algo-science` 在线服务、`lumen-topic-py` / `lumen-algo-py` 的对外契约。

## 一、服务拓扑（2026-11-03 11:20 实测）

| 端口 | 服务 | 状态 | 本轮动作 |
|---|---|---|---|
| 7099 | `gkxlumen-display` | ✅ UP | 11:07 重打包（113.9 MB）+ 重启 |
| 7082 | `gkxlumen-element` | ✅ UP | 本轮拉起（此前 DOWN，导致企业卡被分区降级吞掉） |
| 7090 | `gkxlumen-innov` | ✅ UP | **本轮拉起**（此前 DOWN，导致 4 个端点假性空） |
| 7094 | topic-async-service | ✅ UP | 未动 |
| 8000 | 算法库 `demo-algo-science` | ✅ UP | 未动 |
| 8082 | show-py（久新门面） | ✅ UP | 未动 |
| 8080 | search-py | ❌ DOWN | 未动（关键词检索类能力不在验证范围） |
| 9200 | ES | 未测 | — |

> **重要教训**：`/events`、`/fields`、`/industry-domains`、`/subfields` 四个端点此前返回空，**不是没对接，是 `:7090` 没起**。判「缺口」前必须先确认依赖服务存活，否则会把环境问题写成数据缺口。

## 二、`/v1/situation` 十个端点（逐条实测）

`display` 侧 `SituationController`（class 注释明示「不直连 DB / 不直调 Python」，全部经 Feign 编排）。

| 端点 | 数据源 | 实测返回（空 body） | 状态 |
|---|---|---|---|
| `POST /map` | element（企业区域/点位/级联）+ 久新 show-py（KPI/年序列/市域聚合/机构榜）+ mockProvider（3 要素） | `factorItems=11`、`regions=9`、`objectPoints=99`、`institutionRanking=20`，4.4s / 56 KB | ✅ 真实为主，3 要素 mock |
| `POST /overview` | element（概览/趋势/领域分布）+ 久新（KPI/年序列/地域要素）+ mockProvider | `stats=8`、`factorCards=8`、`trendSeries=3`、`domainRows=6`、`isEmpty=false` | ✅ 6 真 + 2 mock |
| `POST /timeline` | 完全委托 `/events` | 114 B | ✅ 随 `/events` |
| `POST /industry-domains` | innov `GET /v1/meta/industry-clusters` → MySQL `dim.industry_cluster` | `clusters=15` | ✅ 真实（15 = 表 `is_active=1` 全量） |
| `POST /subfields` | innov `GET /v1/meta/industry-clusters/industry-subfields` → `dim.subfield_topic_map` | 空 body：`items=0`、`mapped=false`、`emptyReason=未选择产业领域集群` | ✅ 已对接，需传 `clusterId/industryId`（表内 390 行） |
| `POST /fields` | innov `GET /v1/graph/domains` → `dim.tech_domain` | `fields=10` | ✅ 真实（10 = 表全量） |
| `POST /events` | innov `POST /internal/innov/v1/bay/achievements` → MySQL `ads.innovation_event` | `events=34`，时间轴 `2025—2026` | ✅ 真实（表 230 行，2024-12-16 ~ 2026-06-06） |
| `POST /influence` | 6 卡异源（见 §四） | `cards=6`、`totalCount=5,057,540`、`anyMock=true` | ⚠️ 3 真 + 1 混合 + 2 mock |
| `POST /cluster` | element `enterpriseCluster` → `enterprise_score` | `presets=4`、`scopedItems=200` | ✅ 真实，**但仅企业要素可聚类** |
| `POST /compare` | element（企业注册年）+ 久新（论文/人才/项目/机构年度序列） | `years=2015–2025`、`series=5 条`、`availableFactorKeys=[enterprise,paper,scholar,project,institution]` | ✅ 真实 5 条曲线 |

`/compare` 端点自带 `notes`（后端如实返回，非前端文案）：
- 2026 年为进行中年度，不计入对比（避免虚假断崖）
- 企业序列只统计 `registration_date` 非空的行
- 专利只有全局 KPI 无年度序列；期刊/会议真无源；课题/成果久新有真表

## 三、11 个科创要素真源矩阵

`/map` `factorItems` 实测（`source` 字段由后端如实给出）：

| 要素 | count（实测） | source | 判定 |
|---|---|---|---|
| scholar 专家 | 159,546 | 久新 `ads_geo_yearly_metrics` | ✅ 真实 |
| institution 机构 | 48,444 | 久新 `ads_geo_yearly_metrics` | ✅ 真实 |
| enterprise 企业 | 187,643 | `enterprise_base`（element） | ✅ 真实 |
| topic 课题 | 11 | 久新 `ads_research_problem_*` | ✅ 真实（量少：`ads_research_problem_profile` 406 行） |
| project 项目 | 392,032 | 久新 `ads_geo_yearly_metrics` | ✅ 真实 |
| paper 论文 | 858,620 | 久新 `ads_paper_profile`（按活跃口径） | ✅ 真实 |
| patent 专利 | 71,043 | 久新 `ads_patent_profile` | ✅ 真实 |
| result 成果 | 232 | 久新 `ads_research_outcome_*` | ✅ 真实 |
| **journal 期刊** | 7,200 | `mock` | ❌ **mock** |
| **meeting 会议** | 1,280 | `mock` | ❌ **mock** |
| **service 服务机构** | 6,200 | `mock` | ❌ **mock** |

> 8 真 / 3 mock。3 个 mock 要素的接替条件与清理动作见 `mock-ledger.md` D3 登记段。

## 四、影响力 Tab 六张卡（`/influence` 实测）

| # | 卡 | count | 均分 | 数据源 | 判定 |
|---|---|---|---|---|---|
| 1 | 技术产出 | 4,782,796 | 94.5 | `mockProvider.technologyOutputCard`（论文/专利 mock）+ 期刊子类改取算法库 `M_INNOV_JOURNAL_INFLUENCE`（2,796 刊） | ⚠️ **混合**：期刊真实、论文/专利 mock |
| 2 | 企业 | 188,775 | 37.8 | element `enterpriseInfluence` + `gbaScoredAggregate`（湾区 9 市加权） | ⚠️ **真实数、占位口径**：`enterprise_score` 0–100 占位评分，正式算法 `M_INNOV_ENTERPRISE_INFLUENCE` 未上线 |
| 3 | 科研机构 | null | 32.5 | 久新 `monitorCarrierList` | ✅ 真实（无全国总数，`count=null` 是诚实空） |
| 4 | 专家 | 21,316 | 50.0 | 算法库 `M_INNOV_SCHOLAR_INFLUENCE` | ✅ 真实 |
| 5 | 服务项目 | 6,200 | 82.8 | 纯 mock（`SituationMockProvider#influenceCard("service")`） | ❌ **mock** |
| 6 | 项目（含课题） | 58,453 | 42.9 | 算法库 `M_INNOV_PROJECT_INFLUENCE` | ✅ 真实（榜单为承担机构维度，产物无项目名） |

**两处降级行为必须知道**：
- 企业卡：element 调不通时**该卡不出现**（`catch` 后跳过，不回落 mock）——本轮 element 起来前，页面只有 4 卡。
- 专家卡：算法库取不到时**回落 mock**；项目卡取不到时**不出卡**（无 mock 兜底）。两者策略不同，是有意为之。

## 五、其他 12 个 controller（68 端点的探测结论）

> 探测方式：空 body 直接调 `:7099`。**400 = 缺必填参数（不代表未对接）**，401 = 需登录。因短时间 68 次请求打满本地动态端口，部分请求出现假性 `10061 连接拒绝`，**不代表服务故障**（复查 6 个服务均 UP）。

| Controller | 端点 | 结论 |
|---|---|---|
| `BayInnovationController` | 5 | ✅ 全 OK 且无 mock（achievements 40 KB / indicators 26 KB 为真实据） |
| `GlobalInnovationController` | 7 | ✅ 已对接（同源 innov → `ads_innovation_event`） |
| `ShenzhenInnovationController` | 5 | ✅ 已对接 |
| `InnovationEvaluationController` | 2 | ✅ 已对接 |
| `TechIndexController` | 1 | 已对接（需参数） |
| `SituationFactorSearchController` | 1 | 已对接 |
| `DisplayAggregateController` | 2 | ✅ `health` / `capabilities` 均 OK（聚合探针） |
| `CommunicationController` | 3 | ⚠️ list/sync OK，`detail` 需参数 |
| `CompetitionController` | 4 | ⚠️ list OK，其余 3 个需参数 |
| `ExchangeController` | 6 | ⚠️ overview OK，其余需参数 |
| `TrackingController` | 13 | ✅ **13/13 已接真源，2026-11-03 13:00–14:00 逐条实测**（11:20 时标「未验证」已作废）：`POST /meta` ✅（含 `globalFilterDefaults.fieldScope` 真实默认值）· `POST /dataset` ✅（`records=20`、`heatMatrix`、`relations`、`scopeEffectNote` 三维度回传）· `GET /parameter-templates` ✅（从库回读）· `POST /parameter-templates` / `POST /parameter-templates-remove` ✅（保存/删除，前端走 remove）· `POST /report` ✅（HTML/PDF 落库 + 复用 `reused`）· `GET /reports` ✅（上限 5）· `POST /report-remove` ✅（**本轮新增**：`status=deleted` 留痕 + 删本地产物）· `GET /report/{id}/download` ✅（文件流 + 中文名）· `POST /evaluation/run` ✅ · `GET /evaluation/{taskId}/progress` ✅ · `GET /evaluation/{taskId}/result` ✅。⚠️ 仅 `DELETE /parameter-templates/{key}` 本轮未复测（前端不使用该形态，改走 `-remove`） |
| `UserBehaviorController` | 12 | ⚠️ 需登录（401「访问令牌不存在」）+ 部分依赖 Redis；未验证 |

## 六、mock 清单（汇总，明细见 `mock-ledger.md`）

| 数据块 | mock 点位 | 版本 | 可否去 mock |
|---|---|---|---|
| `/map` 要素 chips | `journal` / `meeting` / `service` | `d3-v1` | ❌ 数据侧无源 |
| `/overview` stats + factorCards | `journal_total` / `meeting_total` | `d3-v1` | ❌ 同上 |
| `/map` 区域图层 `layerKeys` | `journal` / `meeting` / `service`（仅图层标记，**不给城市编值**） | `d3-v1` | ❌ 同上 |
| `/influence` 技术产出卡 | 论文 / 专利 两个子类 | `influence-v1` | ⚠️ 论文无 precompute；专利仅 0.012% 覆盖 |
| `/influence` 服务项目卡 | `service` | `influence-v1` | ❌ 算法库无 `M_SVC_ORG_TECH_SCORE` 产物 + display 无服务域源 |
| 前端 `MockBadge` | 消费 `mock=true` 卡片 | `d3-v1` | 后端字段消失即无角标 |
| 技术发展跟踪（DS-03）整页 | 仅前端演示轨 `src/mock/modules/tracking.ts`（meta/dataset + 评估流程模拟）；**后端零 mock 种子** | `fe-ts-03a-v1` | ✅ **真源已全接**，删 mock 属上线前清理；报告/模板类 6 个 API 演示轨无注册（显式抛错，不造伪数据）—— 明细见 `mock-ledger.md`「技术发展跟踪登记」 |

**去 mock 的硬前提（6.30.0 文档 §24.10 + 库侧双重确认）**：期刊/会议名单仍是「当前缺失数据项」，久新 223 张表里 `journal` / `conference` / `service` 命中 **0 张**，`ads_paper_profile` 无 `publication_type` 列。**接替条件未达成，维持 mock 不改绿。**

## 七、缺口清单（真实无源，不是没做）

| 缺口 | 证据 | 影响 |
|---|---|---|
| 会议实体 | 久新 223 表零命中；MySQL `innovation_event` 是事件不是会议；三方 `gkx` 库 `dwd_conference*` 零命中 | 会议影响力/会议趋势**无序列可建**；`M_INNOV_CONFERENCE_INFLUENCE` 判「完全不支持」 |
| 期刊名录 | 6.30.0 §24.10 列缺失；`dwd_zh_journal` 是名录且 `publication_type` 全为「期刊」 | 期刊要素只能 mock |
| 服务机构 | `service/svc/cms` 表零命中；CMS `v_cms_svc` 无计数端点 | 服务项目卡只能 mock |
| 专利年度序列 | `/compare` 后端 notes 明示「专利只有全局 KPI 无年度序列」 | 专利不能进对比曲线 |
| 专利全库排名 | 被引副表按 `pn` 只对上 355 件 = 语料 0.0121% | 只能样本级分布 |
| 事件流 | `innovation_event` 仅 **230 行**、时间窗 2024-12 ~ 2026-06、`topic_burst` 仅 2 行 | 事件类只能做小样本时间轴，不能做热度演化 |
| 企业正式影响力算法 | `M_INNOV_ENTERPRISE_INFLUENCE` 未上线，现用 `enterprise_score` 占位 | 企业卡口径是「占位评分」，非算法结果 |
| 聚类仅企业 | `/cluster` 其它要素 `clusterSupported=false` | 专家/机构/项目无聚类 |
| 项目对象级榜单 | 产物 `top10_v2` 只有 UUID 无项目名 | 项目卡榜单只能出承担机构维度 |
| 趋势预测窄口径 | 仅论文 16 期、项目 13 期可做 Holt；专利 6 期 < 8 期门槛；期刊/会议无年度件数 | `M_INNOV_FACTOR_FORECAST` 部分支持 |

## 八、等算法上线（566 个指标，d4 全 mock）

**全局事实（2026-11-03 统计 `metric-readiness-matrix-*.yaml`）**：

| 模块 | 指标数 | d1 | d3 | d4 |
|---|---|---|---|---|
| CHAIN | 100 | aligned 100 | partial 84 / none 8 / full 8 | **mock 100** |
| COMMON | 1 | aligned 1 | partial 1 | **mock 1** |
| ENT | 96 | aligned 96 | full 33 / partial 60 / none 3 | **mock 96** |
| INNOV | 143 | aligned 143 | partial 122 / full 9 / none 12 | **mock 143** |
| ORG | 22 | aligned 22 | partial 22 | **mock 22** |
| POLICY | 35 | aligned 35 | partial 31 / full 4 | **mock 35** |
| SVC | 51 | aligned 51 | partial 43 / none 3 / full 5 | **mock 51** |
| SYNTH | 46 | aligned 46 | partial 38 / full 8 | **mock 46** |
| TALENT | 32 | aligned 32 | partial 26 / none 3 / full 3 | **mock 32** |
| TECH | 39 | aligned 39 | partial 36 / none 1 / full 2 | **mock 39** |
| TNIE | 1 | aligned 1 | partial 1 | **mock 1** |
| **合计** | **566** | **aligned 566** | full 74 / partial 442 / none 38 | **mock 566** |

- **d1 定义 100% 对齐**（8 件套齐），**d3 源映射 87% 部分支持**，**d4 接入 0% 上线** —— 全部 566 条 `d4_ingestion_status=mock`，`d4_note` 统一为「算法服务未上线，保持 mock」。
- **翻转条件**（policy §7.6）：算法服务上线 → 按接入清单翻 `d4`，`verified` 由 QA 四段链路核验。**前端/后端都无权自行改绿。**
- 具体到本项目已接线的 6 个算法指标（`M_INNOV_ORG_INFLUENCE` / `SCHOLAR_INFLUENCE` / `JOURNAL_INFLUENCE` / `PROJECT_INFLUENCE` / `PAPER_INFLUENCE` / `PATENT_INFLUENCE`）：**均仍为 `d4=mock`**，因为走的是**离线 precompute 静态快照经通用 `/compute` 壳返回**，不是在线的对象级影响力服务。

## 九、本轮状态变更（相对 2026-11-02）

| 项 | 变化 |
|---|---|
| display | 重打包 113.9 MB 并重启（含新增项目影响力卡） |
| element | 拉起（此前 DOWN → 企业卡恢复） |
| innov | 拉起（此前 DOWN → `/events` `/fields` `/industry-domains` `/subfields` 四个端点恢复真实数据） |
| 久新库表数 | **216 → 223**（新增 7 张，均为 `ads_*`；本台账相关表未变） |
| 影响力卡数 | 5 → **6**（新增「项目（含课题）」，真实数据） |
| 数值类型 | 修掉 4 处 `Long`→JSON 字符串（`project.item.score`、`enterprise.count`、`service.count`、`dataset.totalCount`）+ 企业均分取整 |

**新增 7 张表未逐个核查**（`SHOW TABLES` 只给了表名），若涉及本台账要素需下一轮复核。

## 十、复现命令（走查用）

```bash
# 端点（需 6 个服务在跑）
curl -X POST http://127.0.0.1:7099/v1/situation/influence -H "Content-Type: application/json" -d '{}'
curl -X POST http://127.0.0.1:7099/v1/situation/map       -H "Content-Type: application/json" -d '{}'
curl -X POST http://127.0.0.1:7099/v1/situation/events    -H "Content-Type: application/json" -d '{}'

# 库侧（凭据在 _local/dw-docs/README.md，勿入仓）
#   久新 Doris : SHOW TABLES → 223 张
#   MySQL      : demo_gkxlumenx_ads.innovation_event = 230 行
#                demo_gkxlumenx_dim.tech_domain      = 10 行
#                demo_gkxlumenx_dim.industry_cluster = 15 行（is_active=1）
```

## 十一、明确未做（不是遗漏）

1. **没有改任何 `d4`**：566 条仍 `mock`，离线 precompute ≠ 在线服务。
2. **没有去 mock**：期刊/会议/服务机构接替条件未达成。
3. **UserBehavior（12 端点）未验证**：需登录令牌 + 部分依赖 Redis，如实标「未验证」，不写结论。
   ~~Tracking 未逐条验证~~ → **2026-11-03 已验证 13/13**（13:00–14:00 批量 + 15:20 补测 `DELETE /parameter-templates/{key}`），结论见 §五 `TrackingController` 行。
4. **没有核查新增 7 张久新表**的字段与用途。
5. **页面级截图未做**：前端 `/trend/tech-overall-situation` 跳登录，依赖 upms（未启动），无演示账号。
6. **未 commit / 未 push**：改动（`SituationController.java`、`SituationMockProvider.java`）停本地等人工走查。
