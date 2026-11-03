# SITUATION-ENT-D · DS-01 全维度打通 任务单草案（v4）

> 状态：**已建单 3 张（`backlog`，2026-11-01）**，WBS §4.3 已回写 `WBS-05-18-09 / -10 / -11`；D-A～D-D 四项会签已裁定（见 §5）。跨项 D4 **不另建单**：已由既有 `SYSINT-INDDISC-02-L01`（`WBS-02-13`）覆盖，按指示**先跳过**（见 §3-D4）。
> **v4 修订日 2026-11-01**（v4 = v3 + D-A 探底结论 + D-B/D-C/D-D 裁定 + 实际任务号）。v3 修正了 v2 对「无源要素」的误判（§0-5）。
> 依据：① `human:李伟` 2026-11-01 指令「完全打通，没有的数据会找，实在没有会做接口 mock」② 2026-10-31 对齐会（`淮政玮` / `徐滕强` / `李拜六`）口径 ③ 久新库探底实测（§1 / §1.2）④ **数仓官方文档核对**（`ADS_SCHEMA.md` / `ADS_SCHEMA_RELEASE_NOTES.md`，版本 6.30.0，见 §1.1）⑤ `human:李伟` 2026-11-01 D-A～D-D 四项裁定（§5）。
> 范围：DS-01 科技全域态势（WBS-05-18）主范围；跨项 D4 复用既有 `SYSINT-INDDISC-02-L01`（`WBS-02-13`），不新建。

---

## §0 v1 → v2 → v3 → v4 的口径变更（七处）

| # | v1 / v2 / v3 写法 | v4 写法 | 依据 |
|---|---|---|---|
| 1 | 无源要素**一律诚实空态** | **先找 → 找不到再做代码层 mock** | 李伟 11-01 指令；淮政玮 15:01「新建任务并关联 WBS：我要把哪块数据做 mock」、15:03「库里没有对应的，就在方法里返回 mock 值」 |
| 2 | DoD 统一按「对象级点位」 | 按数据实际粒度**分档**（对象级 / 市域色阶），先探底再定 | 久新探底：只有机构表有经纬度 |
| 3 | 无跨项单 | 新增**产业领域 ↔ 学科领域挂钩**单，挂三要素 `WBS-02-02`，指派 `淮政玮` | 李拜六 15:06 + 淮 15:08「建任务指派给我，我在三要素集成中处理」 |
| 4 | 「必须新建任务单」 | 「**尽量**建单并关联 WBS」（现阶段不强制任务号对 WBS） | 淮 14:58「现在没有强硬要求执行的任务号必须都对应 WBS」 |
| 5 | 5 个无源要素全部做 mock | **按数仓文档核对后修正：课题、成果都有真表，只有期刊/会议需 mock；服务机构走 CMS `v_cms_svc`** | `ADS_SCHEMA.md` 6.30.0 核对（§1.1） |
| 6 | 机构「对象级点位（深圳 ≥120 点）」 | **机构不做点位**：实测深圳 129 家有坐标的机构去重后仅 1 个坐标（城市质心），改机构榜单 Top N + 市域色阶 | 李伟 D-A 裁定「实在挂不上可以接受」+ §1.2 探底 |
| 7 | D3 只提「评审模式 🧪 角标」 | 补 **D-B：非评审模式也正常展示**（不得看出是 mock），同时 handoff + 台账留底，便于后期去 mock 接真数 | 李伟 D-B 裁定（§5） |

---

## §1 找数结论（2026-11-01 久新库实测）

> 权限限制：`test2` 无 `information_schema` 查询权，无法列举全表；下表为**已知表结构实测**（`SELECT * LIMIT 1` 取列名）+ 候选表存在性探测。未列出的表不等于不存在。

| 要素 | 久新可获数据 | 粒度结论 | 证据 |
|---|---|---|---|
| `enterprise` 企业 | element 企业库坐标 | **对象级**（已上线） | 现状 `objectPoints=101` |
| `institution` 机构 | `ads_institution_profile` 有 `latitude` / `longitude`，83,745 行；深圳 135 家、**129 家有坐标（95.6%）** | **坐标不可用于点位**（全部落在城市质心，见 §1.2）→ 改机构榜单 + 市域色阶 | 实测 |
| `scholar` 人才 | `ads_talent_profile` **100,000 行**，有 `city` / `city_location_id` / `district_location_id`，**无经纬度** | 市/区级色阶 | 实测 |
| `paper` 论文 | `ads_paper_profile` **无 location、无坐标**；地域量在 `ads_geo_yearly_metrics.paper_count` | 市/区级色阶 | 实测 |
| `patent` 专利 | `ads_patent_profile` **无 location、无坐标** | 市/区级色阶 | 实测 |
| `project` 项目 | `ads_project_profile` **无 location、无坐标**（有 `institution_count`） | 市/区级色阶（须经机构归属口径，属新口径，必须声明） | 实测 |
| `topic` 课题 | `ads_research_problem_profile` **406**；`ads_research_problem_region_yearly_metrics` **156,613**（CITY 81,269 / PROVINCE 54,259 / COUNTRY 20,366 / DISTRICT 719，含论文/专利/项目/机构/企业年计数与份额）；`_event` 11,657；`_discipline` 3,584；`_institution` 67,672 | **真实可上（市/区色阶）**；无经纬度 → 非对象级 | `ADS_SCHEMA.md` 5.2/5.3 节 + 实测 |
| `result` 成果 | `ads_research_outcome_profile` **342**（MVP 评估集，全部 `outcome_type=PAPER`）；`_dimension` 1,368；`_metric` 3,420；`_yearly_metric` 9,055；`_scope_yearly` 41,153（GLOBAL/DOMAIN/FIELD/TOPIC/INSTITUTION） | **真实可上（市/域色阶 + 榜单）**；⚠️ 四维分/综合分 `is_synthetic=1`、`review_status=PENDING_REVIEW`，期刊影响因子 `SYNTHETIC_SIMULATION`，**必须标注为演示分**；342 条是子集非全量 | `ADS_SCHEMA.md` §48 + 实测 |
| `journal` 期刊 / `meeting` 会议 | `ads_venue_profile` / `ads_conference_profile` / `ads_journal_profile` **三表均不存在**；`ads_talent_research_achievement` 902,667 行 **`COUNT(DISTINCT venue)=0`**（venue 列全空）；文档 §24.10 已把「顶级会议/期刊名单」列为**缺失数据项** | **真无源 → 代码层 mock** | 文档 §24.10 + 实测 |
| `service` 服务机构 | 久新 ADS **无服务机构表**（文档全文仅 1 处「服务机构视图」，指建议表筛法）；展示系统 CMS 侧有 `v_cms_svc`（圈定池 `svc_org_circle` ∪ 虚拟） | **走 CMS 口径，不做 mock** | `db/9x_gkxlumenx_cms.sql` 第 374 行 |
| 落点底座 | `ads_location` 22,229 行，含 `latitude` / `longitude` / `name_zh` / `location_level` | 市/区级落点可用 | 实测 |
| 学科领域 | `ads_geo_yearly_discipline_metrics` **10,151,653 行**，含 `domain_id` / `domain_name_zh` / `field_id` / `field_name_zh` / `subfield_id` | 学科维度**真实存在** | 实测（深圳 2024 Top：物理科学/工程学 3,397 · 计算机科学 2,240 · 医学 2,162） |

**一句话结论**：11 要素里 **9 项有真实源**——企业已通；机构有真表但**坐标是城市质心，不做点位、改榜单 + 市域色阶**（§1.2）；论文/专利/人才/项目/课题可补（市/区色阶）；成果可补（342 条 MVP 子集 + 榜单）；服务机构走 CMS `v_cms_svc`。**只有期刊 / 会议两项真无源**（文档 §24.10 明列缺失 + `venue` 全空），才做代码层 mock。学科领域有 1,015 万行真数据，**缺的不是数据，是「产业领域 ↔ 学科领域」对照关系**。

### §1.1 数仓官方文档核对（`ADS_SCHEMA.md` **6.30.0** · 2026-10-31）

> 来源：`https://github.com/leonlee723/sz-gkx-data-warehouse-docs/blob/main/ADS_SCHEMA.md`（指标定义与算法）
> 更新日志：`.../ADS_SCHEMA_RELEASE_NOTES.md` → 顶部最新版本 **6.30.0 / 2026-10-31**，无更新版本。
> 核对方式：按 6.25.0～6.30.0 新增表清单逐表 `SELECT COUNT(*)` 实测（久新只读通道）。

**① 文档版本与库内物化一致（行数与发布说明逐项吻合）**

| 版本 | 新增表（本次相关） | 文档发布数 | 库内实测 | 一致 |
|---|---|---|---|---|
| 6.30.0 | `ads_research_outcome_yearly_evidence` / `_scope_yearly` / `_trend_case` / `_scope_forecast` | 1,811 / 41,153 / 22,881 / 10,944 | 同 | ✅ |
| 6.29.0 | 成果评估 10 表（`_release` / `_profile` / `_dimension` / `_metric` / `_yearly_metric` / `_forecast` / `_recommendation` / `_problem` / `_discipline` / `_institution`） | 342 篇 MVP | 1 / 342 / 1,368 / 3,420 / 9,055 / 5,130 / 1,026 / 342 / 342 / 1,220 | ✅ |
| 6.28.0 | `ads_resource_optimization_recommendation` / `_evidence` | 4,625 / 7,952 | 同 | ✅ |
| 6.26.0 | `ads_recommendation_*` 7 表 | 1 run / 3 论文 / 3 人才 / 3 Topic 方向 / 78 Technology 方向 / 87 证据 / 3 信号 | 同 | ✅ |
| 6.25.0 | `ads_resource_benchmark_city` / `ads_city_subfield_resource_yearly` / `ads_institution_subfield_resource_yearly` | 十城 / 2015–2025 网格 | 10 / 27,720 / 985,555 | ✅ |
| — | `ads_venue_profile` / `ads_conference_profile` / `ads_journal_profile` | 文档未列（§24.10 明列为缺失数据项） | **表不存在** | ✅ 真无源 |

**② 指标计算方法以文档为准（实现时直接引用，不自行推导）**

| 要素 | 指标 | 文档口径 |
|---|---|---|
| 论文 / 专利 / 项目 | 地域年度计数 | `ads_geo_yearly_metrics` 的 `paper_count` / `patent_count` / `project_count`，按 `location_level + location_id + statistics_year` |
| 课题 | 地区年度五计数 + 份额 | `ads_research_problem_region_yearly_metrics`：论文/专利/项目/机构/企业，粒度 COUNTRY / PROVINCE / CITY / DISTRICT |
| 成果 | 引用 / FWCI / 关联专利 / 关联项目 | **观测或确定性派生**，可当真实值展示 |
| 成果 | 四维分 / 综合分 / 历史轨迹 / 预测 | **模拟**（`is_synthetic=1`、`review_status=PENDING_REVIEW`）；`simulated_journal_impact_factor` 标 `SYNTHETIC_SIMULATION`。文档明令「不得作为专家结论、真实期刊影响因子、投资承诺」 |
| 机构 | 技术力评分 | `ads_institution_technology_power`（64,698 行） |
| 期刊 / 会议 | 顶级名单 | 文档 §24.10 列为缺失，需外部补 Venue 稳定 ID / 级别 / 学科 / 有效期 / 来源版本 |

**③ 文档与代码注释冲突（失真陈述，需修）**

`SituationController` 共 5 处（第 1045 / 1157 / 1160 / 1649 / 1931 行）把「会议 / 期刊 / 服务机构 / 课题 / 成果」一并写成「久新无表 / 无数据源」。按文档与实测：**课题、成果都有真表真数据**，只有期刊 / 会议真无源，服务机构走 CMS。这属于「把有数说成无源」，会误导后续实现与验收，已于 **D-D 会签裁定「①随 D2 一并修」**（只改注释与说明文案，不改逻辑、不改 UI，随 `SITUATION-ENT-D2-L01` 实施）。

### §1.2 D-A 探底：要素能否挂到企业/机构形成地图点（2026-11-01 实测）

| 检查项 | 实测结果 | 结论 |
|---|---|---|
| 机构坐标可用性（深圳） | `ads_institution_profile` 深圳 129 家有坐标，`COUNT(DISTINCT CONCAT(latitude,',',longitude)) = 1`；坐标值 22.54554 / 114.0683 = **城市质心**；`location_resolution_method` = `amap_poi_first` 124 家 + `exact_geonames` 5 家 | **无法形成对象级点位** |
| 机构坐标可用性（全国） | `country_code='CN'` 4,707 家有坐标，去重仅 **426 个点位** | 同上，非逐机构点位 |
| 论文挂机构 | `ads_institution_paper` 707,290 行 / 64,698 机构（其中有坐标 707,171 / 64,689）；深圳 2,049 行 / 124 机构 | **数字挂得上**（可做机构榜单 + 市域色阶） |
| 专利挂机构 | `ads_institution_patent` 100,358 行 / 11,324 机构；深圳 638 行 / 57 机构 | 同上 |
| 课题挂机构 | `ads_research_problem_institution` 67,672 行 / 14,386 机构；深圳 642 行 / 65 机构 | 同上 |
| 成果挂机构 | `ads_research_outcome_institution` 1,220 行 / 643 机构；深圳 576 行 / 31 机构 | 同上 |
| 项目挂机构 | `ads_project_institution` 22,571,355 行；深圳 114 机构（含 `paper 115,063` / `talent 21,656` / `project 148,340`） | 同上（按机构归属口径，须声明） |
| 人才挂机构 | `ads_talent_profile.current_institution_ids` JSON 数组；深圳人才 512 人 | 同上 |
| 机构间合作 | `ads_talent_institution_cooperation` **0 行**（文档标注「预留」） | 不实现 |
| 机构技术力 | `ads_institution_technology_power` 64,698 行；深圳 124 家 | 可作榜单排序依据 |

**结论（D-A）**：数字层面要素→机构**挂得上**，坐标层面**挂不上**（机构经纬度=城市质心，非对象级）。按 `human:李伟`「实在挂不上可以接受」→ **接受方案：市域色阶 + 机构榜单，不做对象级点位**；不得把 Top20 代表集当机构总数展示。

---

## §2 从 2026-10-31 对齐会提炼的流程约束（本单必须遵守）

1. **建单由人类说明目标效果**，AI 建任务时写「创建任务并关联到 WBS：<目标>」（淮 14:44 / 14:59）。
2. **执行会话开局先校验派单提示词**与目标是否一致，有明显不一致先改再干（淮 14:44）。
3. **三段式推进**：出方案 → ①人类确认 → 开发到算法中台（`system-ui-test`）→ ②人类点界面验证 → lumen 复刻 → ③人工验收（淮 14:44）。本草案即第 1 段的「方案」产物。
4. **会话分支里只建任务、不当场干活**：如「更新 storage 存储设计」「给 GDF 派单」，把上下文总结作为任务背景，执行可延后（淮 14:44）。
5. **mock 只做代码层**（李拜六 15:04「数据源层 mock 做不了」）；做法是「封装方法先读库里现有可覆盖的指标结果，库里没有才在方法里返回 mock 值」（淮 15:03）。**禁止在数据源造数冒充真实数据**。
6. **必须有 handoff**（淮 14:58）；纯 mock 改动也要建任务留痕（淮 15:01「不是说没写代码就没价值」）。
7. 现阶段不强制任务号对 WBS，但「尽量都写」；丢信息才是问题（淮 14:59）。

---

## §3 任务单（已建 3 张 · `backlog` · 2026-11-01）

### D2 · 要素落点分档打通

| 项 | 内容 |
|---|---|
| 草案号 · 任务 ID | `WBS-05-18-09` · `SITUATION-ENT-D2-L01` |
| 目标效果（人类口径） | DS-01 地图上，除企业外的要素不再「卡片有数、地图无反应」：**机构做榜单（§1.2 实测坐标不可用）**；论文/专利/人才/项目/课题出市域色阶；成果出榜单 + 市域色阶（演示分须标注）；服务机构走 CMS 口径；图例随要素切换联动；顺带修正 `SituationController` 5 处失真注释（D-D） |
| 监管人 | `human:李伟`（`supervised_by` 已补写） |
| 仓 | `lumen-svc-platform`（`/map` + Feign）、`lumen-topic-py`（`gkx_show_service` 新增要素聚合端点） |
| 状态 | `backlog`（2026-11-01 建单） |
| 依赖 | 久新通道 `up`（已满足）；`SITUATION-ENT-C2-L01`（点位接线范式） |
| 边界铁律 | 沿用 ENT：**可改接口契约，不可改 UI 与实现效果**（`views/situation/**` 与 `styles/*.css` diff 为零） |

**分档 DoD（按 §1 实测粒度，不虚诺对象级）**

| 要素 | DoD |
|---|---|
| `institution` | **不做对象级点位**（久新坐标为城市质心，§1.2）；改「机构榜单 Top N（可按 `ads_institution_technology_power` 排序）+ 市域色阶」；`regions[*].layerKeys` 含 `institution`；`notes` 明写「久新机构经纬度为城市质心，不支持对象级落点」；**不得把 Top20 代表集当机构总数** |
| `paper` / `patent` / `scholar` / `project` | 按市/区聚合出色阶（`regions[*].metrics` 落值），`layerKeys` 含对应 key；**`notes` 明写「久新无坐标列，按市域聚合，不支持对象级落点」**；可选叠机构归属榜单（§1.2 桥接表） |
| `topic` 课题 | 按 CITY 级出色阶（`ads_research_problem_region_yearly_metrics`，CITY 81,269 行）；`notes` 明写「问题口径（基础研究问题），不是学科口径」 |
| `result` 成果 | 榜单（引用 / FWCI / 关联专利为真实值）+ 市域色阶；四维分 / 综合分带 **「演示分」** 标注（`is_synthetic=1`），**不参与排名与计分**；`notes` 明写「342 条为 MVP 评估子集，非全量成果」 |
| `service` 服务机构 | 走 CMS `v_cms_svc` 口径（圈定池 ∪ 虚拟），不占久新通道、不做 mock；CMS 不可达 → 200 + 空 + `emptyReason=no_source` |
| `SituationController` 注释（D-D） | 修正第 1045 / 1157 / 1160 / 1649 / 1931 行「课题 / 成果 / 服务机构久新无表」的失真陈述；**只改注释与说明文案，不改逻辑、不改 UI** |
| 共性 | 每要素抽 1 城做库级 join 校验，计数逐位一致；下游不可达仍 200 + 空 + `emptyReason`，不补 0、不回落 mock；`type-check` / `build` 过；视图零 diff |

**明令禁止**：拿企业坐标代填其它要素坐标；拿市域聚合数伪装成对象级点位。

---

### D3 · 真无源 2 要素（期刊 / 会议）代码层 mock

| 项 | 内容 |
|---|---|
| 草案号 · 任务 ID | `WBS-05-18-10` · `SITUATION-ENT-D3-L01` |
| 目标效果（人类口径） | **期刊 / 会议**两要素在页面上**有可演示的数据**；**非评审模式也正常展示、从界面看不出是 mock**（D-B 裁定），但 handoff + mock 台账留底，便于后期去 mock 接真数。课题 / 成果 / 服务机构**不做 mock**（前两者走 D2 真实源，后者走 CMS） |
| 监管人 | `human:李伟`（`supervised_by` 已补写） |
| 仓 | `lumen-topic-py`（`gkx_show_service` 方法内 mock）或 `lumen-svc-platform`（display 层 Provider），二选一，**集中在单一模块** |
| 状态 | `backlog`（2026-11-01 建单） |
| 依赖 | 无（可与 D2 并行）；台账单 `SITUATION-ENT-MOCK-LEDGER-L01` 做登记 |
| 边界铁律 | 同 ENT；mock **不得写入任何数据库**，不得改数据源 |

**DoD（可观测）**

1. mock 集中单一模块（如 `SituationMockProvider` / `mock_provider.py`），每项带 `source="mock"`、`mock_reason="数仓文档 §24.10 列为缺失：顶级会议/期刊名单未接入"`、`mock_version`；**业务组件内零散落 mock**。mock 范围只限 `journal` / `meeting` 两个 key。
2. **非评审模式正常展示**（D-B 裁定）：页面上不得出现「mock / 示例数据 / 模拟」等字样，不得靠角标或置灰暴露；与真实要素**视觉一致**、可参与正常展示与筛选。
3. **评审模式下**命中 mock 的每个数字旁显示 🧪 `MockBadge`（D9 §2 契约，D4=mock 态）；关闭评审模式后 DOM 不出现 `metric_id` / `Q0xx` / `GAP-*` / 就绪度字样，也**不得出现 mock 痕迹**。
4. `USE_MOCK=false` 时**仍能出 mock**（因为走代码层），但 `source` 字段必须回传 mock，前端不得把 mock 当真实值参与排名/计分/导出。
5. **留底**：handoff 逐项列出 mock 值来源与生成规则；同步登记 `agent-handoffs/科技发展态势-TS/mock-ledger.md`（见下），供后期「去 mock → 接真实表」时按条目清理。

---

### 台账 · mock 台账（跨页公共）

| 项 | 内容 |
|---|---|
| 草案号 · 任务 ID | `WBS-05-18-11` · `SITUATION-ENT-MOCK-LEDGER-L01` |
| 目标效果（人类口径） | 建立**跨页可复用的 mock 台账**：哪块数据做了 mock、mock 在哪个文件/方法、生成规则、真实源接替条件；后期去 mock 接真数时按台账逐条清理，避免「mock 藏在代码里没人知道」 |
| 监管人 | `human:李伟`（`supervised_by` 已补写） |
| 仓 | `gkx-orchestration`（`agent-handoffs/科技发展态势-TS/mock-ledger.md`，待 D3 执行时创建） |
| 状态 | `backlog`（2026-11-01 建单） |
| 依赖 | `SITUATION-ENT-D3-L01`（首条登记来源） |
| 边界 | 只登记不实现；不复制代码；真源仍以代码 `source="mock"` 字段为准 |

---

### D4 · 产业领域 ↔ 学科领域挂钩（**已有任务，不另建**）

| 项 | 内容 |
|---|---|
| 草案号 · 任务 ID | **`WBS-02-13` · `SYSINT-INDDISC-02-L01`**（既有任务，已存在，非本草案新建） |
| 目标效果（人类口径） | 展示系统的「产业领域」能与久新「学科领域」建立稳定对照，使 DS-01 领域筛选可穿透到学科维度真实数据 |
| 指派 | **`淮政玮`**（15:08 明确认领「我在三要素集成中处理」） |
| 仓 | `gkx-orchestration`（口径与映射方案；落地仓待该叶结论） |
| 状态 | `backlog`（registry 实测，`update_time=2026-10-31T16:10:08+08:00`） |
| 当前阻塞 | 依赖 `SYSINT-SURVEY-02-L01` 仍为 `in_progress` 且 `lock_until=2026-10-22T20:36`（过期租约）；`SYSINT-TFMAP-02-L01` 已 `done`；`note` 要求「解锁走 scan → confirm」 |
| 现状处置 | **`human:李伟` 2026-11-01 指示：先跳过本任务**，不回收租约、不改状态、不新建替代单；D2 / D3 不依赖它，可并行推进 |
| 依据 | 李拜六 15:06「大部分数据与久新做关联，但展示系统的产业领域无法和学科领域做挂钩」 |
| 供给事实 | 学科侧已有真数据：`ads_geo_yearly_discipline_metrics` 1,015 万行，`domain_id/domain_name_zh/field_id/field_name_zh/subfield_id` 齐全 |

**DoD（沿用既有任务定义，由淮政玮确认）**

1. 产出一份可版本化的对照关系（产业领域 → 学科 domain/field 映射），来源可追溯，不硬编码在页面里。
2. DS-01 领域筛选选中产业领域后，能返回对应学科维度的真实计数（或明确声明不可映射 + 原因）。
3. 建单后**在群里回报任务号**（淮 15:08 明确要求）——该任务号已存在（`SYSINT-INDDISC-02-L01`）。

> **2026-11-02 补充**：产业领域 ↔ 学科领域 ↔ 三要素的**关联现状总览与展示/专题一致性检查清单**已整理为 [INDUSTRY-DISCIPLINE-FACTOR-LINKAGE-20261102.md](./INDUSTRY-DISCIPLINE-FACTOR-LINKAGE-20261102.md)（同目录）。要点：当前唯一打通通道 = `subfield_topic_map`（WBS-02-08，子学科→产业节点，DS-01 `/subfields` 与专题全景同读此表）；领域对领域仍**无可确认映射**，维持本叶结论不变；「产业领域」展示侧五处出处真源仍待 `human:李伟` 指定。

---

## §4 WBS 子任务行（DS-01 部分，**已于 2026-11-01 回写 §4.3**）

| 草案号 · 任务 ID | 子项 | 监管人 | 仓 | 状态 | 完成情况 · handoff | 依赖 · 可对端 | 完成日期要求 |
|---|---|---|---|---|---|---|---|
| WBS-05-18-09 · `SITUATION-ENT-D2-L01` | 要素落点分档：机构→榜单 + 市域色阶（久新坐标为城市质心，不做点位）；论文/专利/人才/项目/课题→市/区色阶并声明不支持对象级；成果→榜单 + 演示分标注；服务机构→CMS `v_cms_svc`；`regions.layerKeys` + 图例联动；顺带修 `SituationController` 5 处失真注释（D-D） | 李伟 | `lumen-svc-platform` + `lumen-topic-py` | **backlog**（2026-11-01 建单） | 本草案 §3-D2；执行后补 handoff | `SITUATION-ENT-C2-L01`、久新通道 up | 无截至时间 |
| WBS-05-18-10 · `SITUATION-ENT-D3-L01` | 真无源 2 要素（期刊/会议）代码层 mock：非评审模式正常展示（D-B）、评审模式 🧪 MockBadge、集中单一 Provider、handoff 留底 | 李伟 | `lumen-topic-py` 或 `lumen-svc-platform`（择一） | **backlog**（2026-11-01 建单） | 本草案 §3-D3 | 无 | 无截至时间 |
| WBS-05-18-11 · `SITUATION-ENT-MOCK-LEDGER-L01` | mock 台账（跨页公共）：哪块数据 mock / 在哪个文件方法 / 生成规则 / 真实源接替条件，后期按台账去 mock | 李伟 | `gkx-orchestration` | **backlog**（2026-11-01 建单） | 本草案 §3-台账；台账文件 `科技发展态势-TS/mock-ledger.md` 待建 | `SITUATION-ENT-D3-L01` | 无截至时间 |

> D4 不写在本表（挂 `WBS-02-02` 三要素，不在展示页 WBS 行）；本轮**未建单**，叶号与任务 ID 待 coordinator 按三要素表编号。

---

## §5 会签结论（4 项 · 已由 `human:李伟` 2026-11-01 裁定）

| # | 事项 | 选项 | 裁定 |
|---|---|---|---|
| D-A | 论文/专利/人才/项目/课题**只有市（区）域粒度**；机构有经纬度但为城市质心（§1.2），是否接受色阶（而非对象级点位）？ | ①接受色阶 ②该要素只保留卡片计数、不上图 | **①接受色阶 + 机构榜单**（原话「先查找是否能挂到企业或者机构上形成地图点，如果实在挂不上可以接受」）；实测挂不上点位，按接受处理 |
| D-B | mock 数据在**非评审模式**下如何表达？ | ①非评审模式也正常展示 ②仅评审模式可见 ③置灰不出值 | **①非评审模式也正常展示、不能看出是 mock**；同时 handoff + 新建 `SITUATION-ENT-MOCK-LEDGER-L01` 台账任务并关联 WBS 留底，便于后期去 mock 接真数 |
| D-C | 建单路径：MCP `task-create`（本会话未加载该 MCP）或 CLI 通道 | ①MCP `task-create` ②应急 CLI ③等 coordinator | **已检查脚本存在**：`scripts/task-mcp-server.mjs`（MCP stdio，v1.1.0）+ `scripts/task-mcp-cli.mjs`（应急 CLI），无需新建；本会话 MCP 未加载 → 走 CLI（同一 `createTask` 代码路径），已建 3 单成功 |
| D-D | `SituationController` 第 1045 / 1157 / 1160 / 1649 / 1931 行注释失真 | ①随 D2 一并修 ②另开单 ③暂不改 | **①随 D2 一并修**，已写入 `SITUATION-ENT-D2-L01` 的 DoD，不单独提前改 |

---

## §6 授权句（已按建单结果更新）

> `human:李伟` 2026-11-01 授权 DS-01 全维度打通长任务（`SITUATION-ENT-D2-L01` / `-D3-L01` / `-MOCK-LEDGER-L01`，挂 `WBS-05-18-09/10/11`）：**后续认领不必再问**。口径按 §5 裁定：缺数先找，找不到做代码层 mock；机构坐标不可用 → 市域色阶 + 机构榜单；mock 非评审模式正常展示、评审模式 🧪、台账留底；验收沿用 ENT 口径（本地联调 + 人工走查，**改动停本地等人工验收，不自动 commit/push**），边界铁律不变（可改接口契约，不可改 UI 与实现效果）。跨项 `SITUATION-CORE-DOMAIN-MAP-L01`（D4）待 coordinator 编号后另签。
