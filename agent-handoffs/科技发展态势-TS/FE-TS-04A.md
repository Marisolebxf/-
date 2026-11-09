# FE-TS-04A · 全球创新监测（M4）— 整页复刻与真实链路整改

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 整页复刻原由 frontend-agent 完成；2026-11-03 真实链路整改轮由本机会话执行 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 五大 Tab 全量对齐 demo 结构；本轮只换数据源与补空态，未跳过 D9 缺口标注 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 纯前端取数与文案整改，无存储流图变更 |
| 会签态 | N/A |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| Tab1 创新成果综合展示 | ✅ | `InnovationDetail.vue`：成果类型芯片 + 底座地图落点 + 列表联动；久新 `ads_institution_paper` / `ads_location` 真实计数 |
| Tab2 全球创新实时数据 | ✅ | `InnovationRealtime.vue`：4 KPI（按年真实去重）+ 年度趋势 + 领域分布；状态胶囊接 `latestStatYear` / `asOf` / `caveat` |
| Tab3 创新载体排行榜 | ✅ | `InnovationRanking.vue`：多维筛选 + 详情下钻；无源维度走 `NaN → 「—」`，不合成 |
| Tab4 创新监测与分析 | ✅ | `InnovationMonitor.vue`：创新点发现 / 城市监控 / 智能推送三块只在后端下发时展示，其余显式空态 |
| Tab5 城市创新能力分析 | ✅ | `CityInnovationAnalysis.vue`：真实计数 + 缺分项空态 |
| 数据链路 | ✅ | `GlobalInnovationController` → `RemoteShowPythonClient` → `gkx_show_service` → 久新 Doris（只读） |
| 路由 | ✅ | `/trend/global-innovation-monitor`，`menu.ts` + `fullBleed` |
| 构建 | ✅ | `npm run build-only` 绿（2026-11-03，1m25s） |

## 2026-11-03 整改明细

| # | 改动 | 文件 |
|---|------|------|
| 1 | 删除「创新价值评估」随机分与随机四维（含 70/65/60/55 写死初值），改为能力缺口说明 | `tabs/InnovationMonitor.vue` |
| 2 | 删除 `MockDataNotice` 死组件与恒 false 的 `usingMockAlerts` | `components/MockDataNotice.vue`（已删）、`index.vue` |
| 3 | 订阅规则不再拼装推送记录；`subscriptionPushRecords` 置空集 | `tabs/InnovationDetail.vue` |
| 4 | 城市推送记录改为真实预警映射，无预警城市不出记录 | `models/cityModel.ts` |
| 5 | 「创新影响预测」空壳 → 「图谱操作说明」并说明未接原因 | `tabs/InnovationRealtime.vue` |
| 6 | 「实体节点影响赋分」→「实体节点被引排行」；「影响力指数」→「被引数」 | 同上 |
| 7 | 图例「实测/预测」→「年度实测（久新按年统计）」 | 同上 |
| 8 | 补 4 处空态：城市监控、智能推送、趋势图、领域分布 | `InnovationMonitor.vue` / `InnovationRealtime.vue` |
| 9 | 实时错误态渲染 + 接后端 `caveat` / `emptyReason` | `InnovationRealtime.vue` |
| 10 | 状态胶囊改接 `latestStatYear` / `latestCitedYear` / `asOf` | 同上 |
| 11 | 保存配置与推送通道提示改为「不落库」诚实文案 | `InnovationMonitor.vue` |
| 12 | 创新点发现依据改为类型翻译，删除「阈值模型命中」等编造归因 | 同上 |
| 13 | 导出报告按钮随假评估一并移除（评估不可用时无报告可导出） | 同上 |

## 偏离说明

- **窗口期文案**：`InnovationMonitor` 评估弹窗原写「评估半年内介入的窗口期」等建议语，随假评估一并删除，未保留替代话术。
- **城市加权**：`cityModel.ts:340` 的 `0.7/0.3`、`0.55/0.45` 领域加权保留未改 —— 输入是真实计数而非随机数，改它会改变排序语义，列入待产品裁定（见决策文档 §三）。
- **未新增区块**：领域×国家、国家地图与覆盖率披露三项需要新契约，未在本轮实现，已建 `FE-TS-04B/04C/04D`。

## 验证

| 项 | 结果 |
|---|---|
| lint（M4 全目录） | 0 error / 0 warning |
| `npm run build-only` | ✅ 绿 |
| `npm run type-check` | M4 零报错；仓库基线存在 M3（`src/mock/modules/tracking.ts`、`src/views/situation/tracking/`）既有类型错误，来自提交 `e5c5085`，不在本页范围 |
| Math.random | 全页归零（仅剩注释） |

## 遗留与后续

| 项 | 任务 |
|---|---|
| 领域×国家分布（discipline 宽表 1015 万行） | `FE-TS-04B`（后端 `domain_distribution` 已支持 `location_id`，缺前端选中国家入口） |
| 领域—国家地图与排行榜（6.1 快照 20.9 万行） | `FE-TS-04C` |
| 覆盖率披露与年度口径标注 | `FE-TS-04D` |
| 全球能力指数 / 五维雷达 | 等上游公式批准（`ads_geo_yearly_index` 按文档保持空表） |

---

## 第三轮：七项走查问题整改（2026-11-03 深夜）

走查反馈七项（排行榜 2 条 / 聚焦机构专家空 / 项目经费无值 / 布局变形 / 内容占位文案 / 城市筛选 / 监测 tab 派生数据），逐项整改：

| # | 反馈 | 根因 | 改法 |
|---|------|------|------|
| 1 | 排行榜仍 2 条、年份选到 2010-2024 | `established_year` 实测 100/100 有值（min=976 千年名校，max=2019），`yearRange` 写死 2010-2024 只命中 2 家 | `yearRange` 改 computed 从数据推导；默认区间 = 数据 min/max |
| 2 | 聚焦机构空 | `kgData` 盲切 `slice(0,30)`，按被引排序时前 30 可能全为论文 | 分类配额采样 |
| 3 | 聚焦专家空 | （原判「久新无学者表」**结论错误**，见第四轮） | 接入 `ads_talent_profile` |
| 4 | 项目经费无值 | 数据在（JPY 265.3 亿等 5+ 币种，覆盖 12,998/74,097）但前端未格式化 | `formatAmount` 亿/万分位格式化；多币种保留不求和 |
| 5 | 实时 tab 布局变形 | CSS 高度未封顶 | `.gi-realtime-analysis-grid` `height: calc(100vh - 300px)`、`max-height: 900px`、右列 overflow |
| 6 | 「内容暂不完整显示」占位 | 硬编码文案 | 删除，如实空态 |
| 7 | 城市筛选中国城市不出现 | `country_code='CN'` 与 `'中国'/'CHN'` 不互认 | `cityModel` 兼容三种写法（实测 40 个中国城市） |

事故记录：`InnovationMonitor.vue` 曾被 PowerShell 批量替换清空，已从 `git show HEAD:` 骨架 + 会话修正片段完整重建，type-check / build / lint 全过。

## 第四轮：补领域 + 接学者 + 首次部署 + 图谱根因（2026-11-03 深夜～11-04 凌晨）

### 4.1 领域补齐（只补数据，不加筛选框 — human 明确）

| 类型 | 路径 | 结果 |
|---|---|---|
| 论文 | `ads_institution_paper.primary_topic_id` → `ads_discipline_topic.name_zh`（4516 行维表，IN 批量 0.1s） | **100%** |
| 项目 | `ads_project_profile.primary_topic_id` 同上 | **100%** |
| 专利 | 主表无 topic 列；唯一入口 `ads_patent_analysis_topic_patent` 1,240 万行，`IN(60)` 实测 25.2s | 放弃 |
| 机构 | `ads_institution_topic_entry` 3.36M 行单机构上千主题，改走机构论文表仍超时 | 放弃 |

实现约束：**必须两步**（先取数 → topic_id IN 查维表）。主 SQL 直接 LEFT JOIN 会把 project 分支从 0.17s 拖到 15.1s（Doris join 后 ORDER BY LIMIT 优化失效）。

### 4.2 学者接入（推翻「久新无学者表」旧结论）

- 久新 ADS 层 48 张 talent 表，主表 `ads_talent_profile` **10 万条**：中文名 100%、机构 49.3%、城市坐标 38.5%（经 `ads_location` 22,229 行维表）、h 指数 99.4%
- 新增 `POST /internal/gkx-show/monitor/talent-list`（Python）+ `/v1/situation/global-innovation/talents`（Java），支持 `with_location=true` 只返回有坐标者（图谱落点）
- 领域取 `discipline_fields`（field 级）；`discipline_domains` 每人恒四条域且首项「健康科学」，无区分度

### 4.3 ⚠️ 部署真相：三仓库关键代码此前从未提交

本地 Java（7099）与线上镜像跑的一直是**旧代码**：`GlobalInnovationController.java`、`achievement_indicator.py`、`monitor_indicator.py`、`entdb.py` 全是 git 未跟踪文件——**这是此前所有「页面没数据」反馈的总根源**，不是数据源问题。

已提交并推送（CI 自动发版）：

| 仓库 | 提交 | 内容 |
|---|---|---|
| lumen-topic-py | `cc77099` + `97cd284` | show 五类成果/监控指标/专家/领域 + entdb + k8s 凭证走 Secret |
| lumen-svc-platform | `b453975` + `a0f9e46` | GlobalInnovationController 六端点 + talent 坐标修复 |

顺带修正：k8s `dev-show-py.yaml` 原含明文 MySQL/ES 密码（违反 D14），改为 `gkxlumen-jx-ads` Secret key 映射。

### 4.4 端到端验证（Java 7099 → show 8082 → 久新）

- talents（withLocation）：100 条、100% 有坐标
- achievements paper：标题+坐标+领域
- carriers：100/100
- **项目经费端到端**：`/realtime` KPI `project_funding` 11 币种（JPY 265.3 亿在前），Java `byCurrency` 透传 ✓，前端 `formatAmount` ✓ —— 详情页实测显示「资助金额 18174.8 万元」

### 4.5 图谱「全部」视图展示异常不可点击 — 双根因

Playwright + mock 数据实测（生产构建 + dev 各一轮）：

1. **`.gi-knowledge-graph__body` 沿用了 demo 原版两列 grid**（`minmax(0,1fr) 280px`，画布+详情面板），而 realtime 版已把面板移到 body 外同级——画布被压进 `546-280-14=252px` 第一列，且 grid 行高被 canvas `max-height:760` 撑到溢出 body。修复：realtime 作用域改 `grid-template-columns: minmax(0,1fr); grid-template-rows: minmax(0,1fr)` + canvas `max-height:none`（画布恢复 544px 宽）
2. **`ts-knowledge-graph__controls` 工具条（6 按钮 216px 宽、z-index:4）横在画布顶部**——画布 252px 时几乎盖满全部宽度，点节点全命中按钮层。修复：容器 `pointer-events:none; width:fit-content`，仅按钮 `pointer-events:auto`

辅助修正：
- G6 初始化改为「容器有稳定尺寸才 new Graph，否则等 ResizeObserver 首次回调」（tab 切换动画中 250px 中间态会把 canvas 钉死在错误尺寸）
- `zoomRange` 下限 0.5 → 0.15（35 节点 radial 内容直径远超画布时 fitView 被 clamp，节点溢出且命中检测错位）
- 「全部」视图节点配额降为 6 专家+8 机构+8 成果+3 其它 = 25；`layoutOverrides` 环距收紧（linkDistance 240→130）
- 成果 `name` 组装兜底 `row.title`（Java 出参键为 title，原读 name 全空白）

验证：`npm run type-check` ✅ · `eslint`（4 文件）✅ · `npm run build-only` ✅ · Playwright 实测图谱 25 节点正常网络布局、项目经费/领域标签/地图落点全渲染。

## 关联文档

- 决策留痕：`agent-handoffs/科技发展态势-TS/M4-REMEDIATION-20261103.md`
- 需求基线：`agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/全球创新监测.md`（33 叶）
- 指标缺口：`agent-delivery/metrics/request/展示系统/pages/DS-04-*.yaml`（6 个）
- 库侧规约：`_local/dw-docs/久新数仓-资料同步与取数规约.md`

---

## 第二轮审计与 A 组整改（2026-11-03 晚）

第一轮抓的是随机数，第二轮抓的是**写死的常量与固定权重** —— 后者用 `Math.random` grep 一个都扫不到。
审计结论：P0 约 20 处、P1 约 50 处，**A 组 11 项已完成**，B 组 3 项待裁定。

### 已完成（A 组）

| # | 问题 | 改法 |
|---|---|---|
| 1 | `clampScore` 的 `Number(value \|\| 0)` 把 NaN 压成 0 → 城市列表默认每行「综合创新指数 0」 | 非有限值返回 NaN；排序 NaN 沉底；`rank` 不再按 0 分重排 |
| 2 | `Math.max(8, …)` 给 0 分也画 8% 假进度条 | 无源传 NaN（RankingCard 已支持不画）；新增 `formatCityScore` 出「—」 |
| 3 | 4 处假保存/假导出 toast | 改「仅本次会话有效，未接保存接口」/「已下载」 |
| 4 | `showToast(msg)` 丢弃文案，模板固定渲染「操作成功！」 | 新增 `configSaveMessage`，渲染真实文案 |
| 5 | 硬编码 `createdAt: 2026-05-24` 的「全部区域」订阅规则初始即存在 | 删除，初始为空，走「暂无已订阅区域」空态 |
| 6 | 口径说明宣称 `Σ(维度得分×权重)` + `分位归一化` + WIPO/Scopus 数据源 | 如实描述：不计算综合指数、保留原始计数、数据来自久新两张表 |
| 7 | 载体指数口径写「更新 2026-05」「归一化到 0-100」 | 标注「前端本地试算，权重与基数未经权威口径确认」，写明基数 `/5000 /2000 /500 /6` |
| 8 | 实时图右轴标「金额(亿美元)」实挂人才数/项目数 | 左轴「论文/被引数」、右轴「人才/项目数」 |
| 9 | 缺坐标兜底 `[116, 39]`（北京） | 改 `[NaN, NaN]`，不把无位置成果画到地图 |
| 10 | `getNodeRealtimeStatus` 用 150/80 阈值造「高影响/升温/新增」 | 只输出真实年份，无依据返回空串 + `v-if` 隐藏 |
| 11 | 关键词编辑区永不渲染（`getRuleConditionFields` 缺 keywords），默认却带两个关键词 | 补 keywords 字段；默认 `[]`；`metrics` 移除无源 `investment` |
| 12 | `block()` 分块失败只 `console.warn` → 页面显示「暂无数据」 | 收集 `blockErrors`，页面顶部橙色提示 + 重试 |

### 待裁定（B 组，未动）

| 项 | 现状 |
|---|---|
| 载体指数权重 `35/25/25/15` 与基数 `5000/2000/500/6` | 仍在算，口径文案已标「前端本地试算」 |
| 城市加权 `0.7/0.3`、`0.55/0.45` | 仍在算（仅领域筛选时生效） |
| 订阅功能 | 无写接口，已统一改「仅本次会话有效」 |

### 未修（转任务）

- `giDomains` 8 个写死领域名当筛选选项（`InnovationMonitor.vue:9`）→ `FE-TS-04F`
- 聚焦机构/专家筛选恒空、关系边 `weight:0.72` 强连、checkbox 空实现、权重配置不回写、`width:NaN%`、时间范围静默剔除、地图 `slice(0,200)` → `FE-TS-04F`

### 验证

`npm run type-check` ✅ 全绿 · `npm run build-only` ✅ 绿（1m 33s） · M4 lint 0/0
