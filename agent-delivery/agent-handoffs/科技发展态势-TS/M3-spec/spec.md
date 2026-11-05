# SITUATION-TS-M3-REVIEW-L01 — M3 技术发展跟踪（技术评估）真实对接复核与收口

- **监管**：`supervised_by human:孔东`（改动停留本地工作区，孔东确认后再 commit/push）
- **页面**：M3 技术发展跟踪（原型卡片名「技术发展跟踪」；三阶段 `setup → running → result` + 五视图结果看板）
- **涉及仓**：`repos/lumen-ui-science-pc`（FE）、`repos/lumen-svc-platform`（gkxlumen-display + gkxlumen-topic-async-service）、`repos/lumen-topic-py`（gkx_show_service）
- **口径**：`USE_MOCK=false`，数据只读；不改前端样式与布局；不新增原型没有的历史能力；无源字段保持诚实空态。
- **结论先行**：M3 主链路（筛选 → 评估运行 → 五视图取数 → 报告生成/下载/落库）**已是真实接口 + 真实库表**，无 mock 填数；剩余问题只有 **1 处演示残留控件、1 处旧文案、2 个真实字段未消费、若干无源字段**，以及**运行环境未验证**（show-py 未启动、display 401）。

---

## 1. 已核验事实（证据）

| # | 事实 | 证据 |
|---|------|------|
| 1 | FE 全部请求走网关 `/display/v1/situation/tracking/*`，`USE_MOCK=false` | `src/api/situation/tracking.ts#L22`；`.env.development` |
| 2 | display 侧 13 个端点全部存在（meta/dataset/run/progress/result/tasks/parameter-templates/subfields/reports/report generate·download·delete） | `gkxlumen-display/.../controller/TrackingController.java#L191-L438` |
| 3 | show-py 三端点真实读久新 ADS：`ads_technology_potential_assessment`、`ads_technology_potential_dimension`、`ads_technology_stage_assessment`、`ads_technology_hotspot_yearly`、`ads_technology_graph_edge`、`ads_technology_profile` | `lumen-topic-py/gkx_show_service/views/tracking_evaluation.py` |
| 4 | 久新通道为 Doris `47.93.119.170:29030`，**仅 `GKX_JIUXIN_ENABLED=1` 时可用**，否则空态 | `gkx_show_service/jiuxin.py#L36-L61`；`.env.example#L25-L27` |
| 5 | 报告统一落库表已建：`gkxlumenx_topic_enterprise.report`（当前 0 行），旧表 `tech_evaluation_report` / `situation_report` 已废弃 | `db/migration/20261106_unified_report.sql`；DB 实测 |
| 6 | 评估历史 `tech_evaluation_history` 0 行、参数模板 `evaluation_template` 21 行 | DB 实测（10.50.11.76:3306 root） |
| 7 | 默认筛选项由后端下发：首个真实城市、首个在 Topic 桥有映射的产业领域、真实年份区间；不可用时留空不编造 | `TrackingController.java#L1059-L1106` |
| 8 | 产业领域 → 久新 topic 映射统一走 Topic 桥（`topicFromCluster` / `industry-subfields`），旧映射已废弃 | `TrackingController.java#L438`、`#L1064-L1104` |
| 9 | 指标四维就绪度：无已签注册指标 → D1 `missing` 红问号 + 治理引用，组件自闸 `reviewMode` | `components/MetricGapHint.vue#L62-L63` |
| 10 | 产业领域下拉选项为**冻结的治理目录快照** `sz-10+5-2026`（非 mock 造数），映射取数走真实后端 | `src/lib/industryCluster/seed.ts#L24` |
| 11 | 本地运行时探测：display `127.0.0.1:7099` 返回 401；show-py `127.0.0.1:8082` 超时（服务未起） | 本次实跑 |

---

## 2. 逐功能 / 逐指标核对矩阵

图例：✅ 真实接口 + 真实数据；🟡 真实接口但当前空/无源（诚实空态）；⚠️ 前端残留或真实字段未消费；⛔ 久新无源、不伪造；N/A 原型无该入口。

### 2.1 Setup 阶段（条件设置）

| 功能/指标 | 数据源 | 状态 |
|---|---|---|
| 区域范围级联 + 默认值 | `meta.regionCascadeOptions` ← 久新城市列表（monitor） | ✅（仅含有论文的城市，非行政区划全量） |
| 时间范围 + 默认区间 | `meta.timeline` ← `monitorYearlyTrend`（剔除进行中年） | ✅ |
| 技术领域/产业领域选项 | 冻结治理目录 `CL-*`（seed 快照） | ✅（选项为真源快照，非接口下发，见 D3） |
| 产业领域 → 久新主题映射 | `topicFromCluster` 桥 | ✅ |
| 评估方法（4 种） | 前端内置系统方法论常量 | ✅（系统口径，不参与 scoring，UI 已说明） |
| 参数预设（权重/阈值/维度） | 内置 19 + 自定义模板（DB 回读 21 行） | ✅ |
| 推荐组合 / 优化建议 | 由真实评估历史派生（当前 0 条 → 空） | 🟡 |
| 知识库案例 / 最佳实践 | 久新无案例表 | ⛔ |

### 2.2 Running 阶段（评估运行）

| 功能 | 实现 | 状态 |
|---|---|---|
| 任务发起 `evaluation/run` | display → topic-async 异步任务 | ✅ |
| 4 段进度轮询 `evaluation/progress` | 真实 `completedSteps/totalSteps` | ✅ |
| 失败重试 | 后端 `status=failed` 驱动 | ✅ |
| 「演示用状态切换 / 模拟失败」控件 | RunningStage 内手写演示件 | ⚠️ 需收口（C1） |

### 2.3 Result 阶段（五视图 + 榜单）

| 功能/指标 | 数据源 | 状态 |
|---|---|---|
| 热力图 | `ads_technology_hotspot_yearly` | ✅ |
| 地理分布地图 | `monitorCityList` + 经纬度 | ✅（仅国家/城市层；阶段/趋势/证据来源无源 ⛔） |
| 气泡矩阵（六维） | `ads_technology_potential_assessment` + yearly | ✅（`maturity`/`investment` 无源置空） |
| 雷达（六维评分） | `ads_technology_potential_dimension` | ✅ |
| 弦线关联图 | `ads_technology_graph_edge`（HIGH 边） | ✅ |
| 时间轴播放 | 逐年真实值 | ✅ |
| Hero「综合热度指数」 | `records.potential` | ✅ |
| 技术评估 Top20 榜单 | `records` | ✅ |
| 维度摘要 / 阶段对比 / 方法对比 | 真实评估历史（当前 0 → 空态） | 🟡 |
| 详情抽屉数值 | 真实字段 | ✅（文案仍写「模拟数据」⚠️ C2） |
| `dataset.metrics`（overview KPI） | `monitorOverviewKpi` 已返回 | ⚠️ 前端未消费（D2 默认不接） |
| `meta.bubbleAxisOptions` | 后端已返回 | ⚠️ 前端未消费（D2） |
| 成熟度 / 投资额 / 事件时间轴 / 能力项 / 技术类型 / 评估方法 / 知识库 / historyMatrix / workflow / summary / sliceSummary | 久新无源 | ⛔ |

### 2.4 报告

| 功能 | 实现 | 状态 |
|---|---|---|
| HTML+PDF 生成（美化模板 + 图表 PNG） | Thymeleaf 模板 → OSS/本地 | ✅ |
| 落库 | 统一表 `report`（`report_type=tech-tracking`、`condition_key=run_id`） | ✅ |
| 同条件复用 | 同 `runId + format` 直接复用，不重复生成 | ✅（口径见 D4） |
| 最近报告列表 / 删除 | `evaluation/reports`（上限 5）+ 逻辑删除 + 文件清理 | ✅（仅最近 5 条，见 D5） |
| 每次分析必落库、可查历史 | 落库 ✅；历史查询入口仅「最近 5 条」 | 🟡 |

### 2.5 其它

| 功能 | 说明 | 状态 |
|---|---|---|
| 收藏 / 订阅推送 | M3 原型无收藏、无订阅入口 | N/A（按「原来没有的不要加戏」不新增） |
| 指标四维就绪度角标 | D1 missing 红问号 + GAP 治理引用，`reviewMode` 自闸 | ✅ |
| 关闭评审模式 DOM 零泄漏 | 角标组件自闸 | ✅ |

---

## 3. 本次收口改动（代码）

> 仅 2 个前端文件，不改样式、不加新展示位、不动后端。

### C1 `components/RunningStage.vue`：演示控件按评审模式隐藏

- 引入 `useReviewStore`，`v-if="!review.reviewMode"` 包裹 `.tracking-evaluation-run-demo`。
- 失败态仍由 `evaluationProgress.status === 'failed'` 驱动（`index.vue#L578` 已优先该状态）。
- 关闭评审模式 → DOM 不出现「演示用状态切换 / 模拟失败」。

### C2 `models/trackingModel.ts#L828`：旧文案改真实口径

- `'该对象来自技术发展跟踪模拟数据，用于展示详情查询接口返回后的页面装配方式。'`
- → `'该对象来自技术发展跟踪真实评估结果，数值与结论由评估任务返回。'`

### C3 统一报告表实测验证（不改代码）

- 触发一次真实评估 → 生成 HTML/PDF → 断言 `report` 表新增 1 行（`report_type='tech-tracking'`、`condition_key=run_id`）；
- 同 `runId + format` 再生成 → 不新增行、复用；
- 删除 → `status=deleted` + 本地/OSS 文件清理（`fileDeleted`）。

### C4 保留 `run_id` 作为复用键（D4 默认决策）

- 评估报告是「一次评估快照」，跨 run 复用会把旧报告挂到新结论；因此同条件重跑仍生成新报告。与「相同条件复用」的差异在 §6 登记。

---

## 4. 验证清单（执行阶段必跑）

| # | 验证 | 通过标准 |
|---|---|---|
| V1 | `pnpm type-check`（lumen-ui-science-pc） | 0 error |
| V2 | `pnpm build`（lumen-ui-science-pc） | 成功 |
| V3 | 起 show-py（`GKX_JIUXIN_ENABLED=1`、host/port 按 .env.example） | `/health` 可达 |
| V4 | display 本地鉴权 | 带有效 token 调 `POST /display/v1/situation/tracking/meta` 返回 200 |
| V5 | 进入页面默认筛选 | 区域/产业领域/年份非空；数据集非空（久新有数据时） |
| V6 | 五视图逐个切换 | 不报错、图表有真实数据或诚实空态 |
| V7 | 发起评估 → running → result | 进度真实推进；结果与 ADS 表一致 |
| V8 | 生成报告 → 下载 → 再次生成 | `report` 表 +1；二次不 +1；下载 200 |
| V9 | 关闭评审模式 | DOM 无「演示用状态切换」、无 `GAP-*` |
| V10 | `git status` | 仅 C1/C2 两个文件改动，无其它副作用 |

---

## 5. 明确不做（非目标）

1. 不接 `dataset.metrics` / `meta.bubbleAxisOptions` 到新展示位（会改布局，违反「不改样式」）。
2. 不把产业领域选项改为后端下发（现为真源快照，映射已走真实 Topic 桥；如需动态目录另开单）。
3. 不扩「最近报告 5 条」为全量历史页（原型无该入口，按「不要加戏」）。
4. 不伪造成熟度 / 投资额 / 事件时间轴 / 能力项 / 技术类型 / 方法 / 知识库 / historyMatrix 等久新无源字段。
5. 不让评估方法选择影响评分（久新无权重/阈值入参，UI 已诚实说明）。
6. 不新增收藏 / 订阅（原型无）。

---

## 6. 待确认决策（默认按推荐执行，可否决）

| ID | 决策点 | 推荐 | 备选 |
|---|---|---|---|
| D1 | 演示状态切换控件 | 评审模式外隐藏（C1） | 直接删除 / 保留 |
| D2 | 未消费真实字段（overview KPI、气泡轴） | 登记为缺口，不接 | 接入现有 KPI 区（需改布局） |
| D3 | 产业领域选项来源 | 保留冻结治理目录 | 改为 `innov /v1/meta/industry-clusters` 下发 |
| D4 | 报告复用键 | 保留 `run_id`（评估快照语义） | 改为条件哈希（同条件跨 run 复用） |
| D5 | 历史报告入口 | 保留最近 5 条 | 新增全量历史列表（改 UI） |

---

## 7. 影响面与回滚

- 改动文件：`RunningStage.vue`、`trackingModel.ts`（共 2 个）。
- 无 DB 写、无接口契约变更、无后端改动。
- 回滚：`git checkout -- <2 files>` 即可；不影响已跑通的 M3 主链路。

---

## 8. 交付留痕

- 完成 C1/C2 后：`pnpm type-check` + `pnpm build` 绿；
- 生成一次真实报告验证 §C3；
- 本 spec + `tasks.md` 留档于 `agent-handoffs/科技发展态势-TS/M3-spec/`；
- 按孔东监管规则：**停留本地不 push**，待孔东确认。

---

## 9. 2026-11-06 复核更新（本轮，覆盖 §2.3 中已过时口径）

| 项 | 旧口径（本文档前文） | 现口径 | 证据 |
|---|---|---|---|
| 规模（论文） | `hotspot_yearly.paper_count` = 当年新增，top20 多为 0 | `profile.paper_count` **累计**（top20 10~30 全覆盖）；时间轴气泡改用 `evolution_yearly.cumulative_paper_count` | Feign 实测 `records[].scale` 20/20 非 0 |
| 成熟度 maturity | ⛔ 久新无源、恒空 | `graph_node.current_development_phase` 派生；`NO_PUBLICATION_OBSERVED`（top20 17 个）回落 `stage_assessment.stage_code`（20/20 `INDUSTRIALIZATION` → 75） | 实测 `records/hotTopics` maturity 空值 0 条 |
| 并排对比期数 | 最近 8 期 | **最近 3 期**（用户口径 2026-11-05）：`ResultDashboard` `slice(-3)`、后端 `HISTORY_MATRIX_PERIODS=3` | `meta.historyMatrix.periods` = 3 |
| 评估历史 | 0 行、空态 | 库内 14 条回读；`meta.historyMatrix` 由真实评估运行存档派生 | BFF 日志「已从库读取评估历史 14 条」 |
| 详情抽屉 | 气泡详情不展示成熟度 | 展示「成熟度」；「论文数」更名「累计论文数」（口径随累计） | `ResultDashboard.buildBubbleDetail`、`trackingModel` tooltip |
| 应用案例 / 簇群角色 | 未接入 | 已接入（应用案例全库为**资助科研项目证据**，`market_verified=false`；角色 CORE/BRIDGE/MEMBER） | `records.applicationCaseSummary / communityRole` |

**仍受外部条件限制（非本轮可闭合）**：

1. D9 D2/D3/D4 角标：`src/review/readinessSeed.ts` 无 tracking 模块条目（指标库无已签收 DS-03 指标），按 D9 §1 不得前端自填，维持 D1 `missing` 红问号 + 治理引用；
2. `指标入库详情.xlsx` 台账错挂（`M_TECH_*` 为另一套且 `is_mock=true`）需台账侧订正，不属代码改动；
3. 报告链路（§C3 / V8）本轮未重跑。

**本轮验证**：`records` 20 条 scale 非 0；`hotTopics` maturity 20/20；`bubbles[].yearly[].scale` 逐年递增（2020=7 → 2025=21）；`meta.historyMatrix.periods=3`；`pnpm type-check` exit 0。
