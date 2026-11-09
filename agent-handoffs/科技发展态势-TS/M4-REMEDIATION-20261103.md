# M4 全球创新监测 · 真实链路整改决策留痕（2026-11-03）

> 范围：`lumen-ui-science-pc/src/views/situation/global-innovation/`（M4）
> 约束：**不改前端既有样式与结构**，只允许换数据源、补空态、改口径文案
> 上游依据：久新库实测 + ADS_SCHEMA 6.30.0 + 指标台账 xlsx（最新版）+ 算法侧产物

---

## 一、输入基线（本轮亲自核对，非引用旧结论）

### 1.1 在线文档

| 项 | 结果 |
|---|---|
| 地址 | `https://github.com/leonlee723/sz-gkx-data-warehouse-docs/blob/main/ADS_SCHEMA.md`（及 `ADS_SCHEMA_RELEASE_NOTES.md`） |
| 本地副本 | `_local/dw-docs/ADS_SCHEMA.md`（491,449 B）、`ADS_SCHEMA_RELEASE_NOTES.md`（140,849 B） |
| 一致性 | 与 GitHub raw 重新下载的 SHA256 **完全一致**（`A0123813…` / `7CB80325…`） |
| 最新版本 | **6.30.0（2026-10-31）**，本轮无新版本 |

关键文档口径（决定本轮决策）：

- `ADS_SCHEMA.md:2962`：`ads_geo_yearly_index` **在公式批准前保持空表**；`:295` 标注「1.6.0 预留空表」。
- `ADS_SCHEMA.md:2744-2745`：`ads_geo_yearly_metrics` 2000–2014 论文字段为 NULL 且
  `paper_coverage_status='NOT_AVAILABLE'`；2026 为 `metrics_as_of_date=2026-09-18` 的未结束年度。
- `ADS_SCHEMA.md:2929-2931`：`ads_topic_country_snapshot` 的前端联调方式（按 `topic_id` 读全国、
  `output_rank` 排序、GeoJSON 走 `country_code`）。

### 1.2 久新库实测（host 47.93.119.170:29030 / gkx_technology_analysis_dev，只读）

| 表 | 实测 | 结论 |
|---|---|---|
| `ads_geo_yearly_metrics` | 171,736 行；COUNTRY 5,081 行 / **224 国** / 2000–2026 | 真实计数可用；`paper_coverage_status` COMPLETE 2,563 / **NOT_AVAILABLE 2,518** |
| `ads_geo_yearly_discipline_metrics` | **10,151,653 行**；4,468 Topic × 13,353 位置 | 领域×国家数据齐全，**全球页零引用** |
| `ads_topic_country_snapshot` | 209,517 行；4,467 Topic × 224 国；PARTIAL 99.87% | 真实全球分布，**全仓零引用** |
| `ads_geo_yearly_index` | **0 行** | 与文档一致：公式未批准，保持空表 |
| `ads_city_index` / `ads_carrier_index` | **表不存在** | 旧 innov mock ODS，后端 2026-10-29 已切原始字段 |
| `ads_location` | 22,229 行；COUNTRY 232 / CITY 19,729 / PROVINCE 2,252 | 含 `country_code`，可关联 GeoJSON |

### 1.3 算法侧（指标台账最新版）

`指标入库详情-合并-20261028-三系统.xlsx` 本地原为旧 blob（240,898 B / `82ffa3a9`），
已更新为远端最新（249,482 B / `4850a839`「790 行超链接重导 + 45 件三件套补迁」），
DS-04 登记 **29 条**（14 条算法侧 `M_INNOV_*` + 15 条 UI 回填 `M_SCIUI_INNOV_*`）。

算法侧 143 个 py 实现齐备，但产物口径经 `support_note` 逐条确认为**中国/广东口径**：

| 指标 | 产物实况 | 能否用于「全球」页 |
|---|---|---|
| `M_INNOV_CITY_RANK_GLOBAL` | cities 仅 3 条 | 否（原文：宇宙限粤三城，全球排名实为省内名次） |
| `M_INNOV_CITY_BENCHMARK_GLOBAL` | cities 仅 4 条 | 否（深圳 95,600 / 广州 49,605 / 东莞 33,590，北京 163） |
| `M_INNOV_IMPACT_SCORE` | 机构 4,039 家，top 25 | 否（中国机构口径，领域侧被引 null） |
| `M_INNOV_IMPACT_FORECAST` | 311 机构，专利侧明确拒绝拟合 | 否 |
| `M_INNOV_DS_04_MONITOR_001/002` | IPC 634 小类 / 9 候选 / top 33 | 否（论文侧只剩 2 候选） |

→ **结论：算法产物不能直接填「全球」页面，否则是以中国口径冒充全球结论。**

---

## 二、逐项决策（本轮已改）

| # | 决策 | 依据 | 落点 |
|---|---|---|---|
| D1 | 删除「创新价值评估」随机分与随机四维，改能力缺口说明 | 原实现 `Math.random()` 生成综合分 + 四维，并据随机分输出「属于高价值创新机会」；久新无价值模型，台账 `DS-04-MONITOR` seq 79 判 missing | `tabs/InnovationMonitor.vue` |
| D2 | 订阅规则不再生成推送记录（改为空集） | 每条规则拼一条「XX订阅更新 / 已生成最新成果监测摘要」并计入未读，属凭空造记录；久新无推送事件表 | `tabs/InnovationDetail.vue` |
| D3 | 城市推送记录改为「真实预警映射」 | 原按「订阅城市 × 监测配置」模板拼「城市创新能力周报」，无预警也照造 | `models/cityModel.ts` |
| D4 | 删除 `MockDataNotice` 组件及其死状态 | `usingMockAlerts` 恒 false，提示条永不出现；全仓已 0 引用 | 删除 `components/MockDataNotice.vue`、`index.vue` 注释同步 |
| D5 | 「创新影响预测」空壳改为「图谱操作说明」 | 该 section 只有标题 + 拖拽帮助，无任何预测内容；久新无影响预测表，算法侧专利侧 4 期不足拟合 | `tabs/InnovationRealtime.vue` |
| D6 | 「实体节点影响赋分」→「实体节点被引排行」 | `buildImpactRanking` 取的是 `node.value`（被引数），标题却写「赋分」，属口径误导 | 同上 |
| D7 | 「影响力指数」→「被引数」 | 同上，字段语义即被引次数 | 同上 |
| D8 | 图例「实测 / 预测」→「年度实测（久新按年统计）」 | 预测段永不存在；且「实测」未说明是年度口径 | 同上 |
| D9 | 补 4 处空态：城市监控、智能推送、趋势图、领域分布 | 原为纯白板，用户无法区分「没有」与「加载失败」 | `InnovationMonitor.vue` / `InnovationRealtime.vue` |
| D10 | 补实时错误态，并接后端 `caveat` / `emptyReason` | `realtimeError` 只写不渲染；后端已下发诚实说明却被丢弃 | `InnovationRealtime.vue` |
| D11 | 状态胶囊接 `latestStatYear` / `latestCitedYear` / `asOf` | 此前只显示写死的三条，用户不知道数字是哪一年、截止到哪天 | `InnovationRealtime.vue` |
| D12 | 「保存配置」与推送通道提示改为诚实话术 | 原 toast「配置已保存」+ hint「保存后写入推送记录」，实际不落库、不产生记录 | `InnovationMonitor.vue` |
| D13 | 创新点发现的「发现依据」改为类型翻译 | 原按 type 拼「阈值模型命中 / 关系模型命中 + 异常联动」，这些模型并不存在 | `InnovationMonitor.vue` |
| D14 | 「导出报告」按钮随假评估一并移除 | 评估能力不可用时无报告可导出，保留按钮即为死交互 | `InnovationMonitor.vue` |

---

## 三、明确未做（含原因与去向）

| 项 | 原因 | 去向 |
|---|---|---|
| 领域×国家分布（1015 万行宽表） | 后端 `domain_distribution` **已支持 `location_id`**（`monitor_indicator.py:471-489`），缺的是前端「选中国家」入口 —— 加选择器即改结构，超出本轮边界 | **FE-TS-04B（WBS M4-26）** |
| 领域—国家地图与排行榜（6.1 快照） | 同上，且涉及 GeoJSON 联动 | **FE-TS-04C（WBS M4-27）** |
| 覆盖率披露（NOT_AVAILABLE 2,518 行） | 属图表口径改造，需与图例设计一起定 | **FE-TS-04D（WBS M4-34）** |
| 全球能力指数 / 五维雷达 | `ads_geo_yearly_index` 按文档保持空表（公式未批准），算法侧仅粤三城 | 维持空态，等上游公式批准 |
| `cityModel.ts:340` 的 `0.7/0.3`、`0.55/0.45` 领域加权 | 权重无来源，但输入是真实计数、非随机数；改它会改变排序语义 | **待产品裁定**，本轮不动 |
| M3（技术发展跟踪）type-check 报错 | 来自已提交 `e5c5085`，与本页无关 | 单独开工单，不在 M4 范围 |

---

## 四、验证结果

| 项 | 结果 |
|---|---|
| M4 文件 lint | 0 error / 0 warning（逐文件 `read_lints`） |
| `npm run build-only` | ✅ 成功（`✓ built in 1m 25s`） |
| `npm run type-check` | ❌ 失败，但**报错全部在 `src/mock/modules/tracking.ts` 与 `src/views/situation/tracking/`**（M3，提交 `e5c5085` 引入）；M4 零报错 |
| 全页 `Math.random` | 归零（仅剩注释中的历史说明） |

---

## 五、任务绑定

| WBS | 任务 id | 状态 |
|---|---|---|
| M4-01/02 DoD 与 handoff 修订 | `FE-TS-04A` | 已更新 |
| M4-11~14 / 21~25 本轮整改 | `FE-TS-04A` | 已完成（见 §二） |
| M4-26 领域×国家 | `FE-TS-04B` | 新建 pending |
| M4-27 领域—国家地图/榜单 | `FE-TS-04C` | 新建 pending |
| M4-34 覆盖率披露 | `FE-TS-04D` | 新建 pending |

---

## 六、第二轮审计与 A 组整改（2026-11-03 晚）

### 6.1 为什么要再审一遍

第一轮盯的是「`Math.random` / 假记录 / NaN 直出」——抓的是**随机**。
第二轮发现的问题不是随机产生的，而是**写死的常量与固定的权重**，`Math.random` 一个都扫不到。

审计方法：两个 code-explorer 子代理分头扫四个 Tab + 三个模型文件，所有 P0 由本机**逐行读源码复核**后才计入。

结论：**P0 约 20 处、P1 约 50 处**，其中 3 处会在**默认打开页面时**就显示假数据。

### 6.2 Mock 残留

全目录仅剩 1 处：

```
tabs/InnovationMonitor.vue:9 | import { giDomains } from '@/mock/modules/globalInnovation'
```

`giDomains` 是 8 个写死的领域名，**被当筛选器选项**。若后端真实 `discipline` 与这 8 个名字对不上，勾选不生效且无提示。**未在本轮修复**（需改为从真实数据提取领域名，涉及筛选器数据源，避免与既有交互冲突）→ 转入 `FE-TS-04F`。

### 6.3 A 组整改（已完成 8 项）

| # | 问题 | 改法 | 文件 |
|---|---|---|---|
| 1 | `clampScore` 的 `Number(value \|\| 0)` 把 `NaN` 压成 0 → 城市列表默认每行「综合创新指数 0」+ 8% 假进度条 | 非有限值返回 `NaN`；排序时 NaN 沉底；`rank` 不再按 0 分重排（改用后端真实 rank） | `models/cityModel.ts:155, 353-357` |
| 2 | `Math.max(8, …)` 保证 0 分也画进度条；`Number(c.score \|\| 0)` | `maxCityScore` 只取有限值；模板无源时传 `NaN`（RankingCard 已支持不画）；新增 `formatCityScore` 出「—」 | `tabs/CityInnovationAnalysis.vue:188, 726-728` |
| 3 | 假保存 toast 4 处（「区域订阅规则已保存」「已保存 N 个城市订阅」「权重配置已更新」「导出任务已创建」） | 改为「仅本次会话有效，未接保存接口」/「已下载」等如实表述 | `InnovationDetail.vue`、`CityInnovationAnalysis.vue`、`cityModel.ts` |
| 4 | `showToast(msg)` 收了文案却丢弃，模板固定渲染「操作成功！」 | 新增 `configSaveMessage`，模板渲染真实文案 | `tabs/InnovationDetail.vue:494, 1907` |
| 5 | 硬编码一条 `createdAt: 2026-05-24` 的「全部区域」订阅规则，初始即进 `subscriptionRules` | 删除常量，初始为空，由「暂无已订阅区域」空态承接 | `tabs/InnovationDetail.vue:118-130, 211` |
| 6 | 口径说明造假：`formula: 'Σ(维度得分×权重)'`、`standardization: '分位归一化'`、`sources: [WIPO, Scopus, 各国统计年鉴…]` | 如实描述：不计算综合指数、保留原始计数、数据来自久新两张表；载体指数标注「前端本地试算，权重与基数未经权威口径确认」并写明基数 `/5000 /2000 /500 /6` | `models/cityModel.ts:300-306`、`models/carrierRankingModel.ts:93-97` |
| 7 | 实时图右轴标「金额(亿美元)」，实际挂人才数/项目数 | 左轴「论文 / 被引数」、右轴「人才 / 项目数」 | `models/realtimeModel.ts:288-305` |
| 8 | 缺坐标兜底 `[116, 39]`（北京） | 改 `[NaN, NaN]`，不把无位置成果画到地图 | `models/realtimeModel.ts:491` |
| 9 | `getNodeRealtimeStatus` 用 150/80 阈值与 `year 前缀` 造「高影响/升温/新增」 | 只输出真实年份（「2024 年数据」），无依据返回空串 + 模板 `v-if` 隐藏 | `models/realtimeModel.ts:456`、`InnovationRealtime.vue:299` |
| 10 | 关键词编辑区 `v-if="has('keywords')"` 但 `getRuleConditionFields()` 不返回 keywords → 永久不渲染，而默认又带着 `['量子计算','大模型']` | 补 `keywords` 字段；默认值改 `[]`；`metrics` 移除无源的 `investment` | `models/detailMonitorModel.ts:508-540` |
| 11 | `block()` 分块失败只 `console.warn` 后返回空数组 → 页面层「部分数据挂了」显示成「暂无数据」 | `block()` 收集 `blockErrors`，`GlobalInnovationDataset` 新增字段，页面顶部出橙色提示条 + 重试 | `api/situation/globalInnovation.ts`、`types/situation.ts`、`index.vue` |

### 6.4 B 组（待裁定，未动）

| 项 | 现状 | 需要谁定 |
|---|---|---|
| 载体指数权重 `35/25/25/15` 与折算基数 `专利/5000、论文/2000、项目/500、成果/6` | 仍在算，但口径文案已改「前端本地试算，未经权威口径确认」 | 产品/算法：给依据，或整块按无源撤下 |
| 城市加权 `0.7/0.3`、`0.55/0.45` | 仍在算（仅在选了领域筛选时生效） | 同上 |
| 订阅功能 | 无写接口（U5 二期），已全部改为「仅本次会话有效」 | 产品：是否二期补接口 |

### 6.5 仍未做的 P1（转任务）

- `InnovationRealtime` 聚焦机构/专家筛选**永远为空**（节点类型永不产出 expert/org），空态文案却说「实时流中暂无」
- `RealtimeKnowledgeGraph` 关系边 `weight: 0.72` 硬编码 + 按索引取模强连
- `MonitorRuleDrawer` 成果类型/订阅载体 checkbox 写死或错误绑定、口径模板卡片无 `@click`
- `InnovationRanking` 权重配置 `appliedWeights` 从不回写、`Math.max(8, NaN)` 产 `width:NaN%`
- `CityInnovationAnalysis` 趋势年度 allSettled 失败落 `[]`、政策接口 catch 返回 `[]` 与「暂无政策数据」文案矛盾
- `InnovationDetail` 时间范围默认 2020–2026 静默剔除更早成果、地图 `slice(0,200)` 静默截断、图例 5 类但只有 2 类有点位

### 6.6 验证

| 项 | 结果 |
|---|---|
| `npm run type-check` | ✅ 全绿 |
| `npm run build-only` | ✅ 绿（1m 33s） |
| M4 目录 + `api/situation/globalInnovation.ts` lint | 0 error / 0 warning |

---

## 七、第三轮：需规逐条对照后的三项处置（2026-11-03 夜）

### 7.1 需规覆盖情况

SRS《全球创新监测》共 33 叶（seq 56–88），分 6 组；页面 5 个 Tab
（组1+组2 合并为「创新成果综合展示」）。

| 判定 | 数量 | 说明 |
|---|---|---|
| 符合 | 8 | 57 地理可视化、58 重点突出、61 GIS 标注、62 范围筛选、64 关联载体、68 图表切换、69 图谱落图、75 排名筛选 |
| 部分 | 18 | 多为「有形状无口径」：59 价值排序用被引数、67 缺投资金额、73 指数自造、83/85/86 维度缺源 |
| 缺失 | 7 | 60/72 实时更新、70 节点赋分、71 影响预测、78 创新点发现、79 价值评估、82 智能推送 |

**关键结论：7 个缺失里有 6 个是上游模型缺失（A2 差集标 `missing`），不是前端未实现。**
真正属于前端该补而未补的只有「内容分类层级」与「城市维度基金/投入」。

### 7.2 本轮三项

| 项 | 结论 | 处置 |
|---|---|---|
| 1. 成果分类按需求四类 | 原五项平铺为「专利/论文/资讯/机构/企业」统称「成果分类」，把需求的四个**内容大类**压成同一层级 | 已改：label 标出所属大类（论文/专利=创新成果，资讯=创新资讯，机构=创新机构，企业=企业动态）；`value` 不变，筛选与默认全选逻辑不受影响；未接入项标注由「（无数据）」改为「· 未接入」（机构与企业属载体，在载体排行有真实数据，说「无数据」不准确） |
| 2. 「城市创新数据监控」标题 | 该面板渲染的是 `alerts`（后端预警列表，空态「暂无城市创新预警」），顶着 seq 83 的名字 | 已改为「创新预警」。内容属本 Tab，**不搬动** |
| 3. 城市维度创新基金/投资规模 | **做不了**：`ads_geo_yearly_metrics` 仅 paper/talent/project/institution 四个计数列，无金额列；`/global-innovation/cities` 只返回 5 个计数 | 登记 `BE-TS-04G`（data-agent），要求按币种分组 + 覆盖度 + 无金额返 null |

### 7.3 一处判断纠正

第二轮我判断「城市创新数据监控」是**位置错误**（该从监测 Tab 移到城市 Tab）。
第三轮读源码后纠正：**是标题错贴，不是位置错**。该块内容为预警事件流，本就属于监测 Tab；
需求 seq 83 的「城市创新数据监控」（基金/投资/投入/成果）在页面上**完全未实现**，属上游缺数。

### 7.4 验证

`npm run type-check` ✅ · `npm run build-only` ✅（1m 24s） · `task-registry.yaml` YAML 解析通过

---

## 八、新增成果类型 project（创新资讯：基金 / 课题）

### 8.1 背景

需求 seq 56 的「创新资讯（创新基金、创新研究课题等）」在久新对应 `ads_project_profile`，
但成就接口白名单只有 `paper` / `patent`，前端只能请求两类，导致「创新资讯」整类无数据。

口径裁定（human）：**排序字段用 `amount_cny`**，改造按**影响最小**方式。

### 8.2 跨三仓库改动

| 层 | 文件 | 改动 |
|---|---|---|
| Python | `gkx_show_service/views/achievement_indicator.py` | 新增 `SOURCE_PROJECT` / `PROJECT_FIELDS` / `_dedup_by_project()`；`achievement_list` 加 `elif kind == "patent"` + `else`(project) 分支；白名单加 `project`；排序/去重按类型分派；`_shape` 加 project 专属字段 |
| Java | `GlobalInnovationController.java` | `importance` 对 null 原样透传（见 8.3-④）；`time` 用 `publish_year` 兜底；新增 `description` / `amountCny` / `amountCnyValueType` 三个出参 |
| 前端 | `api/situation/globalInnovation.ts` | `types` 加 `project`；`description` 兼容 `description ?? summary`；映射 `amountCny` |
| 前端 | `types/situation.ts` | `InnovationItem` 加可选 `amountCny` / `amountCnyValueType` |
| 前端 | `tabs/InnovationDetail.vue` | 新增 `formatAchievementValue()` / `achievementValueLabel()`，替换 6 处直接输出 `item.value`；project 不画进度条；关联载体入口对 project 禁用 |
| 前端 | `models/giSharedModel.ts`、`displayDictionaries.ts` | 补 project 的配色、图例文案、`GI_TYPES` |

**未动**：`PAPER_FIELDS`、`PATENT_FIELDS`、`_dedup_by_achievement`、`order_by` 默认值、
`achievement_relations`、`carrier_detail`。

### 8.3 五个必须踩过的坑

**① `else` 必须改成 `elif kind == "patent"`**
原实现用 `else` 兜底专利。直接加 `elif project` 会让 project 落进专利分支（拿项目 ID 查专利表）。

**② 去重必须独立实现**
`_dedup_by_achievement` 按 `institution_authorship_count` / `patent_rank` 比较，项目表两者皆无。
塞进同一函数会把论文/专利去重改坏 → 新增 `_dedup_by_project`，按 `evidence_paper_count` 大者保留。

**③ `amount_cny` 可能是模拟值**
`ADS_SCHEMA.md:2593-2620`：`amount_cny_value_type = SIMULATED_SHENZHEN_MEDIAN_V1` 时，金额是按
深圳项目中位数 `581,984.8125` 元确定性模拟的，**不是真实拨款**。
故 Python/Java/前端三层都必须透传并展示 `value_type`，前端文案对模拟值加「（模拟）」后缀。

**④ `dbl(null)` 返回 0，会让项目显示「创新价值 0」**
`GlobalInnovationController` 的 `dbl()` 实现是 `o == null ? 0d : ...`。
项目 `value` 恒为 null → 若直接 `dbl(row.get("value"))`，页面就是「创新价值 0」，
与 FE-TS-04A 刚修掉的 `clampScore` 是同一类错误。改为 null 原样透传。

**⑤ 项目没有 `publish_date`，`time` 为空会被前端时间筛选剔除**
`detailMonitorModel.ts:175` 用 `String(item.date).slice(0,4)` 取年份，
`time` 为空 → `Number('')` 为 0 → 不在 2020–2026 → **项目全被过滤，表现为「加了类型但一条都没有」**。
改为 Java 侧 `time` 用 `publish_year` 兜底。

### 8.4 失败隔离

项目 SQL 用到的 `p.name_zh` / `p.description` / `p.amount_cny_value_type` / `pi.evidence_paper_count`
均依据 `ADS_SCHEMA.md` 文档推断，**未连库实测**。原有 `except jiuxin.JiuxinUnavailable` 覆盖不到
「列不存在」这类错误，会导致整个成果列表 500（论文/专利一起失败）。
已加：project 分支的其它异常只跳过该类型并记日志，不影响 paper/patent。

### 8.5 验证

| 项 | 结果 |
|---|---|
| `python -m py_compile achievement_indicator.py` | ✅ |
| `mvn -pl gkxlumen-display -am compile`（JDK17） | ✅ |
| `npm run type-check` | ✅ |
| `npm run build-only` | ✅ 1m 23s |

> 注：本机 `JAVA_HOME` 指向 JDK 1.8，而项目 target 17，编译需临时把 `JAVA_HOME` 指向
> `C:\Program Files\Java\jdk-17`（`java -version` 显示 17 但 Maven 读 `JAVA_HOME`）。

### 8.6 遗留（未做，已明确）

| 项 | 说明 |
|---|---|
| SQL 连库实测 | 列名来自文档，需在久新实跑一次确认；失败会被 8.4 的隔离兜住，表现为「项目为空」 |
| `geo_basis` 语义 | 仍返回 `first_author_institution`，对项目应为「项目机构」；混合请求下无法区分，前端角标文案对项目不准确 |
| 前端金额展示细化 | 目前仅在卡片/表格/对比/详情显示「资助 X 万元（模拟）」；未做金额筛选、金额排序选项 |
| 关联载体 | `achievement_relations` 无 project 分支，前端对 project 禁用入口并提示原因 |
| 订阅/监测类型选项 | `detailMonitorModel.ts:488-545`、`InnovationMonitor.vue:260` 的成果类型清单仍是 paper/patent，用户暂时无法订阅项目 |
| 部署 | Python 服务与 Java 服务需重新部署后生效 |

---

## 九、事故复盘：加入 project 后「所有成果消失」（2026-11-03 夜）

### 9.1 现象

页面成果列表全空。直接请求 Python 门面：

```json
{"items":[],"empty_reason":"no_source",
 "detail":"未知成果类型: project","available_types":["paper","patent"]}
```

### 9.2 根因（三层，逐层暴露）

**第一层：前后端版本错配导致「全灭」**
前端已改为请求 `types: ["paper","patent","project"]`，而运行中的 Python 仍是旧代码。
旧白名单对**未识别类型直接整体返回 `no_source`**，于是论文、专利一起消失。
→ 一个新增的可选类型，把既有全部数据打空。这是设计缺陷，不是数据问题。

**第二层：project 查询本身跑不出来**
服务重启（加载新代码）后仍为空：

```
detail: 久新库查询失败：(2013, 'Lost connection to MySQL server during query (timed out)')
```

project 走三表 JOIN，30s `read_timeout` 到期；而 `except JiuxinUnavailable` 分支仍会
`return _unavailable(...)` —— **同样把 paper/patent 一起返回成 no_source**。

**第三层：即使不报错，也要固定等 30 秒**
把 project 异常改为跳过之后，数据回来了（75 条），但**每次请求 31.4s**，
因为要等 project 查询超时 30s 才跳过。

### 9.3 上游实测数据（决定 project 是否可行）

| 探测 | 耗时 | 结论 |
|---|---|---|
| `ads_project_profile` 单表 `LIMIT 300` | 0.10s | 快 |
| 项目按 `amount_cny` 排序取 300 | 0.14s / 0.68s | 快 |
| `ads_project_institution WHERE project_id = ?` | 0.06s | 快（单值命中） |
| 三表 JOIN `LIMIT 2` | 11.60s | 极慢 |
| 三表 JOIN + `WHERE latitude IS NOT NULL` | 30s 超时 | 不可用 |
| 三表 JOIN + `ORDER BY amount_cny` | 30s 超时 | 不可用 |
| 两步法：`IN (300 个 project_id)` 查机构关系 | 8.07s | 慢 |
| 两步法：`IN (机构 ID)` 查机构坐标 | >45s 超时 | 不可用 |

**结论：`ads_project_institution` / `ads_institution_profile` 按 ID 批量检索都是全表扫描，
当前 Doris 环境不存在能让 project 落点的访问路径。**（单值命中快，批量不行）

### 9.4 顺带纠正的四处事实

| 项 | 此前认知 | 实测 |
|---|---|---|
| 项目表规模 | 文档提到 2063 条 | **183.9 万条** |
| `START_YEAR` | 用它做年度 | 填充率仅 4%；`effective_start_year` 才 99.99% |
| 项目名称 | 首两行是编号 `2018R1A2A1A19019281`，误判为「无名称」 | `name` 是真实项目名（`Peer Instruction for Quantum Mechanics`）；`name_zh`/`name_en` 全空 |
| `amount_cny_value_type` | 只有 `SIMULATED_SHENZHEN_MEDIAN_V1` | 实为三种，且 `SIMULATED_GLOBAL_SHENZHEN_MEDIAN_V1` 占 91%（167.8 万）、`SOURCE_CONVERTED` 仅 6.3 万 |
| `ads_project_institution` 角色列 | `role` | **无 `role` 列**，实为 `relation_type` / `institution_role_code`；且 `role` 是 Doris 保留字，裸写会语法错误 |

另：按 `amount_cny DESC` 排序的 Top 300 **全部是模拟值项目**（91% 的金额是模拟的），
若将来恢复 project，"按金额排序"的头部将是模拟数据，需要真实金额优先或显著标注。

### 9.5 处置

| 层 | 改动 |
|---|---|
| Python 白名单 | 未知类型由「整体拒绝」改为「丢弃并继续」，并记日志 —— 版本错配不再导致全灭 |
| Python 异常隔离 | project 的 `JiuxinUnavailable` 与其它异常都只跳过自身；论文/专利失败语义不变 |
| Python 开关 | 新增 `PROJECT_QUERY_ENABLED = False`，project 分支在构建 SQL 前直接短路，不再白等 30s |
| 前端 | `types` 回退为 `['paper','patent']`，注释写明恢复条件 |

保留未删：`PROJECT_FIELDS`、`_dedup_by_project`、project 分支代码、前端 project 配色与文案函数
—— 待上游性能达标后，把开关置 `True` 并恢复前端 `types` 即可。

### 9.6 验证

| 项 | 结果 |
|---|---|
| `paper+patent` 请求 | **1.66s / 75 条** |
| `paper+patent+project` 请求 | **0.01s（命中缓存）/ 75 条**，无 30s 等待 |
| `python -m py_compile` | ✅ |
| `npm run type-check` | ✅ |

### 9.7 服务与环境的副作用（已修复/已记录）

- 重启 show 服务时一度丢失 `GKX_JIUXIN_*` 环境变量（`Start-Process` 未继承用户级变量），
  表现为「久新通道未启用」。已改为先注入用户级变量再启动；**重启该服务的正确姿势：
  先 `[Environment]::GetEnvironmentVariables('User')` 注入 `GKX_JIUXIN*`，再拉起 uvicorn**。
- 本机 JDK：用户级 `JAVA_HOME` 与 PATH 已指向 `C:\Program Files\Java\jdk-17`
  （机器级仍为 1.8，需管理员权限，未改；用户级覆盖机器级，新开终端即生效）。
  项目 target 为 17，`JAVA_HOME` 指向 1.8 时 Maven 报「无效目标发行版: 17」。

---

## 十、内容大类落地：标签简化 / 机构接入 / 企业库分工（2026-11-03 深夜）

### 10.1 三项指示与落实

| 指示 | 落实 |
|---|---|
| 筛选标签去掉括号注释 | `论文（创新成果）` → `论文` 等，六项全部简化；「· 未接入」「· 上游优化中」标注保留 |
| 企业查企业库，其余查久新 | 论文/专利/机构 → 久新（机构本轮接入）；项目 → 久新（BE-TS-04H）；企业 → 企业库（**BE-TS-04I**，本轮登记） |
| 需规是否有领域筛选 | 见 10.3 |

### 10.2 机构类接入（本轮完成）

`ads_institution_profile` **单表自带经纬度**（68226 个有坐标机构，单表 0.05s），
完全避开 project 踩过的 JOIN 超时坑。改动：

- Python：`INSTITUTION_FIELDS` 常量 + `elif kind == "institution"` 单表分支；
  异常隔离与 project 同规则（只跳过自己）
- 口径三处决策：
  1. `value = cited_by_count`（机构累计被引）——与论文「被引数」同族但量纲不同（单篇 vs 累计）；
  2. `publish_date = metrics_as_of_date`（指标快照日）——机构无「发布时间」，取快照日保证
     time 非空（空值会被前端时间筛选整类剔除，`detailMonitorModel.ts:175` 的
     `Number('') = 0 < startYear`）；**后端年份过滤对 institution 跳过**（快照日无年份语义）；
  3. `primary_carrier = 机构自身`（表别名 i 复用 INST_FIELDS 所致，属预期）
- 实测：四类型混合请求 **0.83s / 55 条**，机构条目（中国科学院 478 万被引、Harvard、清华）
  中文名、坐标、时间俱全
- 前端：types 加 `institution`；选项有数据后「· 未接入」标注自动消失

一个调试弯路：SQL 别名先写成 `AS value`，而 `_shape` 读 `row.get("cited_by_count")`，
表现为机构条目 value=None 但排序正常（排序在 SQL 层、取值在 Python 层，两处列名不一致）。

### 10.3 需规领域筛选结论

SRS《全球创新监测》33 条中，「创新成果综合展示」部分（seq 56-66）**没有独立条目要求
成果列表按领域筛选**。涉及「领域」的仅三处：

| seq | 需求原文 | 现状 |
|---|---|---|
| 58 | 高亮条件可设「特定领域」 | 已实现（highlightCondition.domains） |
| 66 | 成果对比展示「技术领域」差异 | 上游无源（久新成果无 domain 字段） |
| 65/81 | 订阅 / 关注点条件含领域 | 内存实现 |

前端成果 Tab 现有的「领域」筛选器是**超出需规**的，且因久新无 domain 已做诚实处理
（`hasDomainSource` 恒 false 时不过滤 + placeholder 标注「当前数据源无领域，暂不生效」）。

### 10.4 企业库分工（登记 BE-TS-04I）

企业库（gkx_search_service :8080，ES gkx_enterprise）现有接口全部是「检索企业」或
「单企业详情」视角，**没有跨企业动态流聚合端点**。任务要点：

1. search service 新增 `/internal/gkx-search/enterprise-dynamics`（时间倒序跨企业动态流）；
2. 出参与成果条目同构（type='enterprise'），前端列表/地图直接复用；
3. Java Feign 有先例（RemoteFactorSearchPythonClient 直连 search service）。

### 10.5 验证

| 项 | 结果 |
|---|---|
| `python -m py_compile` | ✅ |
| 四类型混合请求 | 0.83s / 55 条（paper+patent+institution；project 短路跳过） |
| `npm run type-check` | ✅ |
| `npm run build-only` | ✅ 1m 37s |
| 两个改动文件 lint | 0 error / 0 warning |
| `task-registry.yaml` | YAML 解析通过（BE-TS-04G/H/I 就位） |

### 10.6 追加（同日）：撤除领域筛选器 + 企业库探查

**撤除成果列表的「领域」筛选器**（human 裁定「撤掉这个筛选器」）：
依据 10.3 的需规结论（创新成果综合展示无领域筛选条目）+ 久新成果无 domain 字段
（该筛选器永远不生效）。删除 `IndustrySelect` 组件、`selectedIndustry`、`hasDomainSource`
及其 filter 逻辑、`legacyDomainInScope` 导入。**保留**需规内的领域能力：
高亮条件（seq 58）、成果对比（seq 66）、订阅设置（seq 65/81）。
验证：type-check ✅ · build-only ✅ 1m18s · lint 0/0。

**企业无数据的完整原因**（实测）：
1. 数据源分工裁定：企业动态走企业库（ES `gkx_enterprise` @10.50.11.76:9200），不查久新 ——
   成果接口目前只连久新，`enterprise` 类型从未接入（即 BE-TS-04I 的内容）；
2. 企业库现有接口全是「检索企业 / 单企业详情」视角，无跨企业动态流聚合端点；
3. 本机接入的现实障碍：`gkx_search_service`（:8080）本地未运行；ES 要求认证，
   `.env.example` 样例密码 `htrfadmin` 实测 401，用户级无 `GKX_ES_PASSWORD` ——
   **启动 BE-TS-04I 前需先拿到正确的 ES 凭据（或确认 search 服务部署位置）**。

### 10.7 追加（同日）：企业动态口径裁定与数据源实查

群聊裁定（2026-11-03 21:07-21:09，human 郭万迎 / 淮政玮）：
- 郭万迎提议「企业动态用资讯充」→ 淮政玮**否决**：企业动态就是投融资事件、发展历程；
- 淮政玮定性：**「对于宏观来说，企业获得的融资就是成果」**。

落实为 BE-TS-04I 口径：enterprise 条目 = 一次融资事件，value = 融资金额
（与 project 的 amount_cny 同族），time = 完成日期，地理 = 企业注册地。

数据源实查（结论：**数据已存在，不是从零建**）：
1. ES `gkx_enterprise` 每条企业文档已带 `financings` nested
   （`completion_date` / `funding_amount` / `funding_round`），由 ETL 从
   `gkx_dwd_org_financing_info` 灌入（ENT-ES-ETL-L01-handoff §3）；
2. MySQL 侧另有 `svc_org_finance_event`（dwd，15,755 条投融资事件），
   疑似淮政玮所说「李拜六有表」，待确认；
3. search service 已有单企业视角 `/profile/financings`（读 nested，按完成日期倒序），
   缺的只是**跨企业动态流聚合端点**。

障碍不变：本机无 ES 凭据（样例密码 401）、search service 本地未运行。
BE-TS-04I 的 note 已按此口径更新。

### 10.8 追加（同日深夜）：企业动态落地 —— 走企业库 MySQL + 四大类展示改造

用户裁定（2026-11-03）：
- 数据通路：**走 MySQL**（不走 ES），「三要素查久新库，企业维度查自己库，接口层聚合」；
- 展示口径：筛选器与分类展示**只列四大内容大类**（创新成果 / 创新资讯 / 创新机构 / 企业动态），
  「传给后台的时候再匹配」——创新成果→论文+专利、创新资讯→项目、机构→创新机构。

#### 数据源选型（同实例 10.50.11.76:3306，全只读实测）

| 候选表 | 行数 | 日期 | 金额 | 结论 |
|---|---|---|---|---|
| demo_gkxlumenx_dwd.enterprise_financing | 17,174 | 100% | **仅 2 条** | 不可用 |
| **gkxlumenx_dwd.enterprise_financing** | **25,654** | **100%** | **34%（8,826）** | **采用** |
| svc_org_finance_event（dwd） | 15,755 | **全空** | 有 | seed 数据，排除 |
| ES financings nested | — | — | — | 需 ES 凭据（401 阻塞），弃 |

坐标：gkxlumenx_dwd.enterprise_extra.lng/lat 100% 填充（189,116/189,116）；
enterprise_base.headquarters_lat 正式库全空，不能用。城市/省份 100%。

#### 实现（三段，全部通过）

1. **`gkx_show_service/entdb.py`（新建）**：企业库 MySQL 只读通道，与 jiuxin.py 完全对称
  （SELECT 白名单、线程连接复用、120s TTL 缓存；凭据 GKX_ENTDB_* 可覆盖，
   默认与 conf/settings.yaml db 段一致）。不 import gkx_common.db（依赖 sqlalchemy，
   本机未装且 show 服务从未用过它）。
2. **`achievement_indicator.py`**：enterprise 分支走 entdb 单库三表 JOIN
  （financing × base × extra，全限定表名跨 schema 不跨实例），
  achievement_id = org_id+日期+轮次（同标识去重，源表有成对重复行），
  value = amount AS cited_by_count（对齐 _shape 读取键），
  country 恒「中国」，primary_carrier = 企业自身；失败只跳过自身。
3. **前端四大类**：giSharedModel.ts 加 CONTENT_GROUPS / contentGroupOf / contentGroupLabelOf
  （成果=紫、资讯=青、机构=绿、企业=红）；InnovationDetail.vue 筛选器改大类
  （勾选后 selectedDetailTypes 展开细类过滤）、列表/卡片/详情/对比/图例标签全部大类化，
  订阅抽屉保持细类口径（SUBSCRIPTION_RESULT_TYPES）；请求 types 加 enterprise。
   Java 透传 financeRound/investors/currency。

#### 验证

| 项 | 结果 |
|---|---|
| enterprise 单独（cited 排序） | 1.9s / 50→去重 41 条，深圳尚水智能（股权投资 9998 万，投资方欣旺达等） |
| 五类型混合 year_from=2024 | 2.5s / 883 条（paper 288 + institution 300 + enterprise 295） |
| 城市过滤（深圳市） | 0.95s / 17 条，全部为深圳市 |
| patent year_from=2024 → 0 条 | 数据现状（最新专利 2023-01-24），非 bug |
| py_compile / mvn compile / vue-tsc / eslint（改动文件） | 全部 0 错误 |

⚠️ 部署提醒：Java（GlobalInnovationController）需重新编译部署后 enterprise 字段
（financeRound/investors/currency）才透传；不部署也能出列表（name/city/value 同构字段不受影响）。

## 第十一章：创新资讯放开 + 七项 UI/数据修复（2026-11-03 深夜）

### 11.1 创新资讯（project）恢复 —— 单表模式（BE-TS-04H 部分解除）

实测推翻了"必须等物化表"的判断：
- `ads_project_profile` 单表（183 万行）recent/cited 排序 50 条 **0.19s**；
- `ads_project_institution` 按 project_id **等值点查 0.05s**（2257 万行，Doris 列存裁剪）；
- 点查出的 institution_id IN(≤20) 查 `ads_institution_profile` 坐标 **0.08s**。

改造（`achievement_indicator.py`）：
- PROJECT_QUERY_ENABLED=False → True；base 改单表（去掉 pi/i JOIN）；
- 时间列 start_year（4% 填充）→ **observed_start_year**（100%）；
- 单表无城市/国家列 → geo_where 对 project 分支跳过（kind_args 同步去参，防 %s 错位）；
- **项目条目无坐标（location=null）**：列表可见、地图不落点（不造 (0,0)）；
- `/relations` 新增 project 分支：两步点查（project_id → 关系表 → 机构坐标），
  basis 标注「项目参与机构（证据论文 N 篇）」。

前端配套：`InnovationItem.location` 类型改 `[number, number] | null`；
api 组装不再丢弃无坐标条目；地图点位/热力/飞线构造处 Array.isArray 判空。

### 11.2 载体关系按钮按类型显示（human：只有成果类有该按钮）

- paper / patent / **project**（新放开）→ 显示「查看载体关系」；
- institution / enterprise → **不显示**（载体即自身，查询必然 0 条属假查询）；
- getCarrierRelationState 与 ensureCarrierRelations 同步拦截。

### 11.3 七项 UI/数据修复

| # | 问题 | 根因 | 修复 |
|---|---|---|---|
| 1 | 详情抽屉"内容暂不完整显示" | 占位文案 | 删除 |
| 2 | 载体排行榜只剩 2 条 | 默认年份过滤把 createYear=NaN（久新无成立年份列）全剔除 | NaN 保留（InnovationRanking.vue 年份过滤） |
| 3 | 实时数据图谱被压扁、页面超长 | 分析区行高无界（右列 1000px+ 撑开整行） | 行高封顶 `calc(100vh-300px)`/max 900px，右列内部滚动 |
| 4 | 城市筛选"选国际显示中国、选中国 0 条" | Java 出 `country_code`='CN'，前端比较 `=== '中国'` | 匹配兼容 '中国'/'CN'/'CHN'（cityModel.ts） |
| 5 | 监测 tab 完全无数据 | 预警/推送事件表无源（诚实空态） | "创新点发现"改由**真实成果数据派生**（最近 8 条，口径如实标注），预警区保持空态 |
| 6 | project 无载体按钮 | relations 未支持 | 见 11.1（两步点查） |
| 7 | 载体按钮在机构/企业上假查询 | 无拦截 | 隐藏按钮（见 11.2） |

⚠️ 事故记录：InnovationMonitor.vue 在批量 sed 时被误清空，已从 git HEAD 骨架 +
会话内读到的修正片段完整重建（诚实性修正全部重放），type-check/build/lint 全过。

验证：project 单独 0.17s/20 条（value=amount_cny，value_type=SIMULATED 占 91%）；
project relations 0.21s；五类型混合 recent 0.1s/1483 条（缓存命中）；
全量 type-check ✅、build-only ✅ 1m31s、eslint（8 个改动文件）0 错误。

## 第十二章：补领域 + 接学者 + 首次部署（2026-11-03 深夜续）

### 12.1 领域（domain）补齐 —— 只补数据，不加筛选框（human 明确）

| 类型 | 路径 | 结果 |
|---|---|---|
| 论文 | `ads_institution_paper.primary_topic_id` → `ads_discipline_topic.name_zh`（4516 行维表，IN 批量 0.1s） | 100% |
| 项目 | `ads_project_profile.primary_topic_id` 同上 | 100% |
| 专利 | ❌ 主表无 topic 列；唯一入口 `ads_patent_analysis_topic_patent` 1,240 万行，`patent_id IN(60)` 实测 **25.2s** | 留空 |
| 机构 | ❌ `ads_institution_topic_entry` 3.36M 行，PRIMARY_TOPIC 单机构上千主题，IN(100) 返回 204,902 行/23.1s；改走机构论文表 IN(100) 读超时 | 留空 |

实现要点：**必须两步**（主查询先取数 → topic_id IN 查维表）。直接在主 SQL `LEFT JOIN` 维表会把 project 分支从 0.17s 拖到 **15.1s**（Doris join 后 ORDER BY LIMIT 优化差）。

### 12.2 学者（talent）接入 —— 推翻「久新无学者表」的旧结论

核查结论（在线文档 + 久新实测）：
- 文档：Person ← `dwd_scholar` / `dwd_zh_author` / `dwd_en_author`；`dwd_scholar_work_experience`；`dwd_scholar_coauthor`
- 久新：test2 只开放 `gkx_technology_analysis_dev`（231 表全 ADS 层，DWD 未开放），但 **ADS 层有 48 张 talent 表**，主表 `ads_talent_profile` **10 万条**：
  中文名 100%、当前机构 49.3%、城市坐标 38.5%（经 `ads_location` 22,229 行维表）、h 指数 99.4%
- 领域取 `discipline_fields`（field 级）；`discipline_domains` 每人固定四条域，首项恒「健康科学」无区分度

新增 `POST /internal/gkx-show/monitor/talent-list`（Python）+ `/v1/situation/global-innovation/talents`（Java），字段：姓名/机构/城市/国家/论文/被引/h 指数/专利/项目/领域/坐标/院士标记。`with_location=true` 时只返回有坐标者（图谱落点用）。

### 12.3 ⚠️ 部署真相：三个仓库的关键代码此前从未提交

本地 Java（7099，13:37 启动）与线上镜像跑的仍是旧代码：`GlobalInnovationController.java`、`achievement_indicator.py`、`monitor_indicator.py`、`entdb.py`、`geo_indicator.py` 全部是 git 未跟踪文件。**这是「页面没数据」的总根源**，不是数据源问题。

本次已提交并推送（CI 自动发版）：
| 仓库 | 提交 | 内容 |
|---|---|---|
| lumen-topic-py | `cc77099` + `97cd284` | show 五类成果/监控指标/专家/领域 + entdb + k8s 凭证走 Secret |
| lumen-svc-platform | `b453975` + `a0f9e46` | GlobalInnovationController 六端点 + talent 坐标修复 |

顺带修正：k8s `dev-show-py.yaml` 原含**明文 MySQL/ES 密码**（违反 D14「凭证走 Secret」），已改为 `gkxlumen-jx-ads` Secret key 映射，CI 对 show-py 也应用该 Secret。

### 12.4 本地端到端验证（Java 7099 → show 8082 → 久新）

| 项 | 结果 |
|---|---|
| talents（withLocation） | 100 条、100% 有坐标（York/Toronto/Melbourne…）、姓名/机构/h 指数/领域齐全 |
| achievements paper | 标题 + 坐标 + 领域（如「荟萃分析与系统综述」） |
| carriers | 100/100 |
| 前端 | `row.name ?? row.title` 兜底（Java 出参键为 title，原读 name → 标题空白）；type-check ✅ |

⚠️ 遗留：前端 `lumen-ui-science-pc` 的改动（本轮七项修复 + 学者节点 + name 兜底）仍在本地未提交，验收走本机 vite dev（3000）时可热更新；若要发测试环境，需单独提交推送前端仓库。

## 第十三章：图谱「全部」视图异常不可点击 + 项目经费复验（2026-11-04 凌晨）

### 13.1 图谱双根因（Playwright + mock 数据实测，非推测）

| # | 根因 | 证据 | 修复 |
|---|---|---|---|
| 1 | `.gi-knowledge-graph__body` 沿用 demo 原版**两列 grid**（`minmax(0,1fr) 280px` 画布+面板），realtime 版面板已移出 body —— 画布被压进 **252px** 第一列；grid 行高又被 canvas `max-height:760` 撑到溢出 body（432px） | elementFromPoint 实测 stage 宽 250、canvas 250×758 | realtime 作用域 `grid-template-columns: minmax(0,1fr); grid-template-rows: minmax(0,1fr)`，canvas `max-height:none` → 画布恢复 544px |
| 2 | `ts-knowledge-graph__controls` 工具条（6 按钮，**216×40px、z-index:4**）横在画布顶部 —— 画布 252px 时工具条盖满大半，**点节点全部命中按钮层** | elementFromPoint(470,383) 返回 `BUTTON.ts-kg-control-btn--wide` | 容器 `pointer-events:none; width:fit-content`，按钮 `pointer-events:auto` |

辅助修正（`KnowledgeGraphCanvas.vue`）：
- G6 初始化改为**容器有稳定尺寸才 new Graph**（tab 切换动画中 250px 中间态会把 canvas 钉死在错误尺寸；`autoResize:false` 不跟随）
- `zoomRange` 下限 0.5→0.15：35 节点 radial 内容直径远超画布时 fitView 被 clamp，节点溢出偏左上、命中检测错位
- 「全部」视图配额 35→25（6 专家+8 机构+8 成果+3 其它）；环距 `linkDistance 240→130`、`unitRadiusRatio 0.26→0.32`
- 成果 `name` 组装兜底 `row.title`（Java 出参键为 title，原读 name 全空白——**存量 bug**，第一轮走查未暴露因列表主要用 title 兜底处）

### 13.2 项目经费「还是空」的判定：数据链路全程正常，属前端未拿到新代码

逐层实测（2026-11-04）：
- Python `/monitor/overview-kpi`：`project_funding.by_currency` 11 币种（JPY 265.3 亿、EUR、USD…）
- Java `/realtime`：`byCurrency` 数组原样透传 ✓
- 前端组装 `amountCny` + `formatAmount` ✓；详情页实测显示「资助金额 18174.8 万元」
- 判定：用户浏览器仍跑旧 JS。根因是本轮频繁写文件把 vite HMR 打入损坏态（#app 渲染 `<!---->`、auth store 反复安装的 full-reload 循环），**已重启 dev server 并实测恢复**

> 教训：多 agent 并行改同一 dev server 下的文件时，验收前先确认 `#app` 渲染正常，否则「还是空」类反馈会把代码问题误判为数据问题。

### 13.3 决策清单（本轮新增）

| 决策 | 内容 |
|---|---|
| D15-R1 | 专利/机构领域放弃：专利唯一入口 1,240 万行关联表 IN(60)=25.2s；机构主题表 3.36M 行单机构上千主题。除非上游出「对象→主领域」预聚合表 |
| D15-R2 | 图谱「全部」视图节点配额降为 25，不再随数据量增长 |
| D15-R3 | 工具条 pointer-events 穿透（demo 全景页同款组件受同一问题影响，待观察） |
| D15-R4 | G6 实例创建延后到容器尺寸稳定；zoomRange 下限 0.15 |
