# METRIC-LIB-ALGO-INFLUENCE-L01 · 指标库口径对齐 + 算法库 precompute 优先接入

> **任务**：DS-01 科技全域态势 · 影响力 Tab（WBS-05-18-14，2026-11-02）
> **角色**：`agent:api-agent`（接手研发 Agent，`auto` 模型）· 监管人：`human:李伟`
> **状态**：`integration`（改动停本地，**未 commit / 未 push**，待人工验收）
> **挂接**：`WBS.md` §4.3（WBS-05-18-14）· `task-registry.yaml` `METRIC-LIB-ALGO-INFLUENCE-L01` · 台账 [mock-ledger.md](./mock-ledger.md)
> **前序**：`INFLUENCE-FIX-L01`（影响力 Tab 三缺陷修复，05-18-12）、`GRANULARITY-FIX-L01`（05-18-13）
> **建单路径留痕**：本会话无 `task-create` / `coordinator` MCP 工具，按 2026-11-02 交接任务 §八「参考 SITUATION-IM 路径 2（C2=①）」授权**直接更新 `task-registry.yaml`**（与 11-01 五单同径）；每份 handoff 与 commit 注明「无 MCP、经监管人当场指示，按文件直接更新」。

---

## 一、本轮目标与范围

1. 按指标库真源 `agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx`（sheet：科技专题算法库 / 科技展示系统）更新影响力指标的 `metric_id`、定义、支持度、更新频率、口径局限；
2. 把算法库 `demo-algo-science`（k8s 名 `gkxlumen-platform-innov-py`，:8000）**已有**的 `data/precompute/{metric_id}.json` 结果接入页面，替代原代码层 mock；
3. 每个统计数字旁挂 ⓘ（MetricSpecHint）或红色「?」，受 `@/review` 评审模式门控，关闭后 DOM 零泄漏。

> 本轮**不新增功能、不新增指标算法**：算法库没有 precompute 产物的指标一律保留 mock + 🧪，不造数、不把状态改绿。

## 二、指标库口径对照（xlsx → 契约 metricId）

| 卡 / 子类 | 契约 `metricId` | 指标名 | 支持度 | 更新频率 |
|---|---|---|---|---|
| 技术产出·期刊 | `M_INNOV_JOURNAL_INFLUENCE` | 期刊影响力 | 部分支持 | 待确认（pending） |
| 技术产出·论文 | `M_INNOV_PAPER_INFLUENCE` | 论文影响力 | 部分支持 | pending |
| 技术产出·专利 | `M_INNOV_PATENT_INFLUENCE` | 专利影响力 | 部分支持 | pending |
| 专家 | `M_INNOV_SCHOLAR_INFLUENCE` | 专家学者影响力 | 完全转换支持 | 待确认（pending） |
| 企业 | `M_INNOV_ENTERPRISE_INFLUENCE` | 企业影响力 | 部分支持 | 待确认（pending） |
| 科研机构 | `M_INNOV_ORG_INFLUENCE` | 科研机构影响力 | 部分支持 | 待确认（pending） |
| 服务项目 | `M_SVC_ORG_TECH_SCORE` | 服务机构影响力 | 部分支持（四档口径） | 按需 |
| 技术产出（卡级） | **无**（红「?」+ `metricGapNote`） | — | 卡为聚合，指标库无对应聚合指标 | — |

> 卡级 `metricGapNote` 字段名与「缺口只显治理引用、不显伪 8 件套」的 D9 §2.3 约定一致；前端 `InfluenceTab.vue` 以 `metricId` 有值与否二选一渲染 ⓘ / 红「?」。

## 三、取数口径对照表（务必保持，走查重点）

| 卡 / 子类 | 数据源 | `mock` | 本轮实测 | 为什么这么取 |
|---|---|---|---|---|
| 期刊 | **算法库 precompute** `M_INNOV_JOURNAL_INFLUENCE` | `false`（无 mock 字段） | `count=2796`、`avg=4.1`、`items=15` | 算法库已有全库中文刊可评分结果；口径局限写明「影响指数维缺失、英文刊无被引量列、全库口径不随筛选变化」 |
| 专家 | **算法库 precompute** `M_INNOV_SCHOLAR_INFLUENCE` | `false`（无 mock 字段） | `count=21316`、`avg=50.0`、`items=46` | 算法库已有 21,316 位学者全库评分 + Top 榜；`score_stats.mean=49.9769` 与页面 50.0 对齐 |
| 论文 | 代码层 mock（`influence-v1`） | `true` + 🧪 | `count=3433600`、`avg=94.6`、`items=6` | 算法库**无 precompute 产物**，无可做全库排名的结果；挂 `M_INNOV_PAPER_INFLUENCE` + 缺口说明 |
| 专利 | 代码层 mock（`influence-v1`） | `true` + 🧪 | `count=2111200`、`avg=97.0`、`items=6` | 算法库截图仅 **0.012% 样本覆盖**，不能做全库排名；挂 `M_INNOV_PATENT_INFLUENCE` + 缺口说明 |
| 企业 | 可筛真实源（`enterprise_score`，经 display 聚合） | `false` | `count=114904`、`avg≈36.96`、`items=50` | **保留筛选联动**：算法库为全国全库静态值，替换会丢地域 / 领域 / 年份联动；补 `metricId` 与口径局限 |
| 科研机构 | 可筛真实源（久新 `carrier-list` + `M_INNOV_ORG_INFLUENCE` 归一化范式） | `false` | `count=null`（显示「—」）、`avg=32.5`、`items=50` | 同上；对象总数无统计源，**不补 0** |
| 服务项目 | 代码层 mock（`influence-v1`） | `true` + 🧪 | `count=7192`、`avg=83.6`、`items=3` | 算法库无 `M_SVC_ORG_TECH_SCORE` precompute 产物、CMS 数据源未接；挂 `M_SVC_ORG_TECH_SCORE` |
| 技术产出（卡级） | 三子类聚合 | `true` + 🧪 | `count=5547596`、`avg=95.5` | 卡级本身无指标库条目 → 红「?」+ `metricGapNote`；子类各自挂自己的 `metricId` |

> 降级策略：算法库 `:8000` 不可达时，期刊 / 专家降级回 mock **并挂缺口说明**（`attachMetric` 的 `metricLimitations` 写明「算法库本次取数失败，数值为代码层 mock」），不静默出数。

## 四、改动清单（2 仓 7 文件，停本地未提交）

### 后端 `lumen-svc-platform` / `gkxlumen-display`

| 文件 | 改动 |
|---|---|
| `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemoteAlgoScienceClient.java` | **新增**。`@FeignClient(contextId="displayRemoteAlgoScienceClient", name="gkxlumen-platform-innov-py", url="${gkxlumen.algo.python-base-url:}")`，`POST /v1/innov/metric/{metricId}/compute`（`@NoToken`，`Map` 包络原文）。本地 profile 关 Nacos，靠 `url` 直连；生产不配 → 走服务发现 |
| `gkxlumen-display/src/main/resources/application-local.yml` | 新增 `gkxlumen.algo.python-base-url: http://127.0.0.1:8000` |
| `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/SituationController.java` | 七个指标常量；`/influence` 期刊子类与专家卡改取算法库 precompute；论文 / 专利保留 mock + 🧪 + `metricId` + 缺口；企业 / 机构沿用可筛真实源补指标元数据与口径局限；服务项目挂 `M_SVC_ORG_TECH_SCORE`。新增 `algoValueOf` / `subMap` / `attachMetric` / `markMock` / `buildTechnologyOutputCard` / `journalSubFactor` / `buildScholarInfluenceCard` |

### 前端 `lumen-ui-science-pc`

| 文件 | 改动 |
|---|---|
| `src/types/situation.ts` | `InfluenceItem` 增加 `metricId` / `metricName` / `metricSupport` / `metricUpdateFreq` / `metricDefinition` / `metricSource` / `metricLimitations` / `metricGapNote`（8 件套 + 缺口说明） |
| `src/components/lineage/MetricSpecHint.vue` | 新增 `limitations` prop 与「口径局限」行（空则不渲染） |
| `src/views/situation/overview/models/metricCatalog.ts` | 新增 `INFLUENCE_METRIC_SOURCE`（xlsx 真源标注）与 `INFLUENCE_GAP_NOTE`（后端未给 `metricId` 时的兜底文案）；**前端不手写指标 ID** |
| `src/views/situation/overview/components/InfluenceTab.vue` | 卡头与子类行加 ⓘ / 红「?」（`.influence-metric-missing`）+ 🧪 `MockBadge`，全部包在 `isReviewFeatureEnabled()` 门控内；图标显式 import |

> 契约字段一律后端透传；`USE_MOCK=false` 下未使用 `@/mock/**` 或 demo fixture 填数；计数走 `num()` 返回 int（平台 Jackson 会把 Long 序列化成字符串）。

## 五、验收证据

### 5.1 服务与探针（2026-11-02 接手复跑，原始数值）

| 项 | 结果 |
|---|---|
| 端口存活 | `:7099` LISTEN(pid 32708) · `:8000` LISTEN(pid 75648) · `:3000` LISTEN(pid 61692) |
| 算法库 `POST :8000/v1/innov/metric/M_INNOV_SCHOLAR_INFLUENCE/compute` | `STATUS=200`、`LEN=16498`、`code=0`；`coverage.n_scholars=21316`、`distinct_scholar_id=21316`；`score_stats: n=21316, mean=49.9769, median=51.66, min=0.0, max=98.74`；`tiers: T1=168 / T2=4285 / T3=12902 / T4=3137 / T5=824` |
| 影响力 `POST :7099/v1/situation/influence` | `STATUS=200`、`LEN=25963`、`code=0`、`analyzableFactorCount=5`、`cards=5`；见下表 |

**五卡逐项（同一响应解析）**

| 卡 | `mock` | `count` | `averageScore` | `items` | `metricId` |
|---|---|---|---|---|---|
| technologyOutput | `true` | 5547596 | 95.5 | 3 | 无（卡级 `metricGapNote`） |
| ├ paper | `true` | 3433600 | 94.6 | 6 | `M_INNOV_PAPER_INFLUENCE` |
| ├ journal | 无（false） | **2796** | **4.1** | 15 | `M_INNOV_JOURNAL_INFLUENCE` |
| └ patent | `true` | 2111200 | 97.0 | 6 | `M_INNOV_PATENT_INFLUENCE` |
| enterprise | 无 | 114904 | 36.9625 | 50 | `M_INNOV_ENTERPRISE_INFLUENCE` |
| institution | 无 | `null`（「—」） | 32.5 | 50 | `M_INNOV_ORG_INFLUENCE` |
| scholar | 无 | **21316** | **50.0** | **46** | `M_INNOV_SCHOLAR_INFLUENCE` |
| service | `true` | 7192 | 83.6 | 3 | `M_SVC_ORG_TECH_SCORE` |

> 与交接期望逐项比对：**journal 2796 / 4.1 且无 mock ✓、scholar 21316 / 50.0 / 46 项且无 mock ✓、paper/patent/service mock=true ✓、五卡各带 metricId 或卡级 metricGapNote ✓、无回归**。
> 契约字段名复核：`technologyOutput` 卡级键含 `metricGapNote`（非 `gapNote`）；`journal` 子类键含 `metricId/metricName/metricSupport/metricUpdateFreq/metricDefinition/metricSource/metricLimitations/countNote`。

### 5.2 前端三绿

| # | 命令 | 结果 |
|---|---|---|
| ① | `node_modules\.bin\vue-tsc.cmd --build` | ✅ `TSC_EXIT=0`（无输出即无错误） |
| ② | `node_modules\.bin\vite.cmd build` | ✅ `built in 1m 13s`，`exit 0`（仅 Node 20.18.0 / caniuse 旧 / chunk >500kB 三条既有告警） |
| ③ | 页面实跑 | ✅ `:3000` 存活 + 两探针 `200` 全数值对齐；沿用 11-02 上一轮已留浏览器证据：影响力 Tab `.metric-hint-btn` 7 处、`.influence-metric-missing` 1 处（技术产出卡级）、`.mock-badge` 4 处，子类 论文/专利 `mock=true`、期刊 `mock=false`，控制台无报错 |

> 诚实说明：本轮为**核验 + 登记**任务，未新增业务代码；三绿中 ①② 为本会话实跑，③ 的服务与接口层为本会话实跑、浏览器 DOM 证据沿用上一轮留痕，未重复造证据。

## 六、局限与未做项（如实声明，不伪闭合）

1. **论文 / 专利 / 服务项目仍为代码层 mock**：算法库无对应 precompute 产物（专利仅 0.012% 样本，不能全库排名）；去 mock 路径与接替条件已登记 [mock-ledger.md](./mock-ledger.md)「影响力登记」。
2. **企业 / 机构不换算法库全国静态值**：保留地域 / 领域 / 年份筛选联动是产品口径；算法库截图值为全库静态，替换即丢联动，故只补指标元数据与口径局限。
3. **算法库本地用临时 mini harness 起 `:8000`**：全量 `api.main:app` 因缺 `python-multipart` 起不来，上轮只挂 `/v1/innov` 路由；harness / 8000 端口进程属临时联调环境，**不在交付物内**，用毕清理。生产走服务发现 `gkxlumen-platform-innov-py`。
4. **机构对象总数 `count=null`**：无统计源，页面显示「—」+ 口径说明，不以 0 冒充。
5. **`BE-TS-IMPL-01` / `BE-TS-DATA-01` 未开工**：依赖 `BE-TS-CONTRACT-01` 冻结 REST；该单 M0 三方评审未召开（`BE-TS-CONTRACT-01.md` §2 DoD 2 是唯一未闭合项），本轮不动。
6. **`DS-01-METRIC-OPEN-L01` 指标语义卡待签**：赋号草稿、类型未签、公式 pending `human:唐绍祖` 共签，本轮不改状态。
7. **评审层关闭 DOM 零泄漏**：本轮复核了字段名与门控调用点，未重复做开关回归；如需可随 6 单合并走查一并验。

## 七、走查准备

6 条 `integration` 单的本地 diff 清单见 [WBS-05-18-走查准备-20261102.md](./WBS-05-18-走查准备-20261102.md)，交 `human:李伟` 走查；**走查通过后才 commit / push（`origin/dev`）**。

## 八、Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 算法库有产物的指标（期刊 / 专家）才接真值，无产物的一律保留 mock + 🧪 不造数；企业 / 机构按产品口径保留可筛真源不误替；五卡全挂真实 metric_id 或卡级红「?」+ 缺口，全部受 `@/review` 门控；`count=null` 不以 0 冒充；不可达降级回 mock 仍挂缺口说明；两个探针逐字段比对无回归 |

## 九、Cost（成本四字段，估算）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 90000 |
| actual_tokens | ~120000（核验 + 两探针复跑 + 三绿 + 文档登记） |
| model_used | Auto |
| actual_cost | ~$1.2（估算） |
| cost_warn | green（< $5） |

## 十、改动停本地（人工验收闸门）

- 后端 `lumen-svc-platform`、前端 `lumen-ui-science-pc`、编排 `gkx-orchestration` 三仓本轮改动**未 commit / 未 push**，停本地等 `human:李伟` 走查。
- 服务状态：`display :7099` / `算法库 :8000`（临时 harness）/ `前端 :3000` 均运行中；走查时可直接复跑 §5.1 两个探针。
- 本文件与 `WBS.md` §4.3 / §1、`task-registry.yaml` 的登记同步落盘，均停本地。

---

## 十一、2026-11-03 增补：新增「项目（含课题）影响力」卡（第 6 卡）

> 触发：`human:李伟` 2026-11-03 裁定「新增『项目（含课题）影响力』卡」。
> 背景：`M_INNOV_PROJECT_INFLUENCE` 算法库**早有 precompute 产物**，但 `SituationController` 里搜不到该 ID，影响力 Tab 5 卡中**根本没有项目卡**（算法侧有、页面零接线）。

### 11.1 改动（后端 1 文件，前端零改动）

`lumen-svc-platform/gkxlumen-display/.../controller/SituationController.java`：

| 位置 | 改动 |
|---|---|
| 常量区 | 新增 `PROJECT_INFLUENCE_METRIC = "M_INNOV_PROJECT_INFLUENCE"`、`PROJECT_FACTOR = "project"` |
| `/influence` 第 6 段 | `factorInScope(enabled, "project")` 守门 → `algoValueOf(PROJECT_INFLUENCE_METRIC)` → `buildProjectInfluenceCard`；**不可达不出卡**（本卡无 mock 种子，不伪造） |
| 新方法 | `buildProjectInfluenceCard(value, keyword)`，照 `buildScholarInfluenceCard` 同款模式 |
| `totalDefinition` | 补「项目为算法库全库国内项目池」 |

前端 `InfluenceTab.vue` **不需要改**：卡片通用渲染（`v-for card in visibleCards`），`factorType` 是 string，`project` 天然支持；默认勾选集合 `getDefaultEnabledFactorKeys` 走 `GEO_FACTOR_ORDER`（含 `project`），卡会出现。也**未动 mock 种子**（demo 冻结 5 卡，不新造数据）。

### 11.2 数据与口径（真实产物，非 mock）

`/v1/innov/metric/M_INNOV_PROJECT_INFLUENCE/compute` 实测返回 `data_source=precompute`，`value` 即 payload 全量：

- `count = 58,453`（国内项目，全部国家自然科学基金，1986—2021 真实年窗）
- `averageScore = 42.9`（`score.v2` 缺测重归一：mean 42.883 / median 51.397 / p10 1.071 / p90 53.789）
- `metricId = M_INNOV_PROJECT_INFLUENCE`、`metricSupport = 部分支持`（与矩阵 `d3=partial` 一致）

**⚠️ 榜单口径的硬约束（必须随卡披露）**：产物 `score.top10_v2` **只有项目 UUID、无项目名**，快照明细 `_snapshots21/probe_infl_20261022/*.json` 未随产物落盘。拿 UUID 当项目名是不可读的假对象 → 榜单改出 `institution_top_zh` 的**承担机构维度**（按承担项目数），条目名后缀显式加「（承担项目）」，并在 `caliberNote` + `metricLimitations` **双处**写清「不是项目对象级榜单」。

`metricLimitations` 共 6 条（全部来自产物 `gaps` + 本次实测）：
1. 中文项目 100% 为国家自然科学基金单一来源，不代表全部科技项目
2. 参与机构数维不可算（`participating_institution` 为单值依托单位），该维不参与合计
3. 结题状态列整列为空，结题完备用 `final_report_abstract` 长度代理（填充 81.09%）
4. 英文项目 19,919 条金额量纲与国内差 4 个数量级，独立归一、未并入本卡
5. 榜单为承担机构维度（按项目数），产物无项目名，不出项目对象级榜
6. 算法库为全库口径，不随本页地域 / 领域 / 年份筛选变化；关键词仅在承担机构 Top10 内过滤

### 11.3 验证（实跑证据）

| 项 | 结果 |
|---|---|
| `read_lints`（SituationController.java） | **0 错误** |
| `javac`（display 模块 30 个源文件 + lombok `-proc:full`，m2 全量 classpath） | **EXIT=0，0 error**（仅既有 unchecked 提示） |
| 反射调用 `buildProjectInfluenceCard`（真实 payload） | keyword=null → count=**58453 Integer**、averageScore=**42.9 Double**、items=**10 条**、limitations=6；keyword="中山" → items=**1**（中山大学）；keyword 无命中 → items=**0**（**卡仍出**，count/均分不依赖关键词）；缺 `score` 字段 → **返回 null**（不伪造） |

### 11.3.1 部署与端到端（2026-11-03 11:07 完成）

- `mvn -o -pl gkxlumen-display -am -DskipTests package`（**JAVA_HOME 必须切到 `jdk-17`**，默认环境的 `JAVA_HOME=jdk1.8.0_321` 会编不过）→ BUILD SUCCESS，`gkxlumen-display.jar` = **113.9 MB**。
  - 坑：`repackage` 阶段要 rename 旧 jar，**旧进程未停会直接失败**；中断后 jar 会被覆盖成 0.2 MB 空壳，必须删掉重打。
- `display :7099` 已用新 jar 重启，`element :7082` 也已拉起（此前 DOWN，导致企业卡被分区降级吞掉）。两者 `stderr` 均空、日志 **0 条 ERROR**。
- `/v1/situation/influence` 实测（`enabledFactorKeys=[]`）：

| factorType | count | averageScore | mock | metricId |
|---|---|---|---|---|
| technologyOutput | 4782796 (int) | 94.5 | true | — |
| enterprise | 188775 (int) | 37.8 | — | M_INNOV_ENTERPRISE_INFLUENCE |
| institution | null | 32.5 | — | M_INNOV_ORG_INFLUENCE |
| scholar | 21316 (int) | 50.0 | — | M_INNOV_SCHOLAR_INFLUENCE |
| service | 6200 (int) | 82.8 | true | M_SVC_ORG_TECH_SCORE |
| **project** | **58453 (int)** | **42.9** | — | **M_INNOV_PROJECT_INFLUENCE** |

- 守门 / 过滤实测：`enabled=[project]` → 1 卡；`enabled=[enterprise]` → 1 卡；`enabled=[]` → 6 卡；`searchTerm=中山` → project items=**1**；`searchTerm=不存在XYZ` → items=**0** 但卡仍出。
- **页面级截图未做**：前端 `/trend/tech-overall-situation` 跳 `/login`，登录依赖 upms（本轮未启），不掌握演示账号；后端契约已验证，页面需走查时用已登录会话刷新确认。

### 11.3.2 顺带修掉 4 处「Long 被序列化成字符串」

部署后实测发现数字字段类型不一致（前端 `toLocaleString` 不出千分位、排序退化成字典序）。根因是平台 Jackson 全局注册了 `Long.class → ToStringSerializer`（见 `num()` 注释）：

| 字段 | 修复前 | 修复后 | 归属 |
|---|---|---|---|
| `project.items[].score` | `"3484"` | `3484` | **本次引入**，`item.put("score", num(projects))` |
| `enterprise.count` | `"188775"` | `188775` | 既有，`num(scoredCount)` |
| `service.count` / 技术产出子类 `count` | `"6200"` | `6200` | 既有，`SituationMockProvider.baseCard` / `technologyOutputCard` 收窄为 int |
| `dataset.totalCount` | `"5057540"` | `5057540` | 既有，`num(totalCount)` |

另修 `enterprise.averageScore` 由 `37.77889874188849` → `37.8`（`round1`，原实现裸出加权均值）。

### 11.4 明确未做（不是遗漏）

1. **`d4` 未改绿**：`M_INNOV_PROJECT_INFLUENCE` 在就绪度矩阵仍为 `d4=mock`「算法服务未上线」。离线 precompute ≠ 在线服务，保持诚实态，由责任方在服务上线后翻转。
2. **未新增 mock 种子**：demo 冻结 5 卡，`USE_MOCK=true` 时不会出现项目卡（符合「mock 种子冻结自 demo，禁新造」）。
3. **未做项目对象级榜单**：产物无项目名，需算法侧把项目名/标题落进产物后才能出项目榜（当前只能出承担机构维度）。
4. **未 commit / 未 push**：按人工验收闸门停本地，等 `human:李伟` 走查。
5. 会议 / 期刊 / 服务机构 3 个 mock 未动：6.30.0 文档 §24.10 + 库侧实测双侧确认仍无真源（详见 `SITUATION-ENT-GAP-FILL-20261102.md` §十）。
