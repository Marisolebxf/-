# SITUATION-IM-C-SERIES-L01 · 三创新监测页后端 15 端点打通（C1–C15）＋ M6 前端接线

> **日期**：2026-10-28 · **监管人**：`human:李伟` · **执行**：本会话主 agent（无监管模式连续执行）
> **总控**：`SITUATION-IM-长任务总控.md`（U1–U13）
> **状态**：🟢 **后端 15/15 完成并端到端 200 验证**；🟢 **前端 M6+M5+M4 三页全部接线完成、type-check 0、build 通过**；🟡 **仅剩 R0 评审底座与 R1–R3 角标**
> **严禁 push**：保留 commit 形态（U11）

---

## 1. 运行时突破（本次最大前置阻塞，已解决）

`gkxlumen-innov` 此前**无法本地启动**，导致所有端点只能静态验证。根因有三层，逐层攻破：

| # | 阻塞 | 解法 | 落点 |
|---|---|---|---|
| 1 | `spring-boot` 插件 prefix 在 innov 模块下不可用 | 改用 `java -jar` 运行 boot repackage 后的 jar | — |
| 2 | `FeignClientsRegistrar` 拼 `http://127.0.0.1:${server.port}${server.servlet.context-path}`，占位符无法解析 → `Illegal character in authority` | **`server.servlet.context-path` 必须显式给值**（`""`） | `application-local.yml`（照 `element` 同款惯例新建） |
| 3 | `TenantContextHolderFilter` 从 Redis 读租户列表，命中其他项目遗留的 `com.topcomm.healthcare.*` 旧包名 → 反序列化失败 → **所有接口 500** | `spring.autoconfigure.exclude` 排除该 Filter | 同上 |

另需配置 `feign.innov.url=http://127.0.0.1:7090`（innov 未注册 Nacos，display 服务发现找不到它）。

**新增文件**：`gkxlumen-innov/src/main/resources/application-local.yml`；**修改**：`gkxlumen-display/src/main/resources/application-local.yml`（加 innov 直连）。
两者均只作用于 local profile，**不影响 K8s 部署**（helm 走 dev）。

---

## 2. 后端交付：15 个端点（全部 curl 200 + 真实数据）

### 2.1 M6 深圳（5 个）
| 端点 | 数据源 | 实测结果 |
|---|---|---|
| `POST /v1/situation/shenzhen-innovation/carriers` | `dim_carrier` + `ads_carrier_index` | 3 条（含真实经纬度、指数 51.9/50.2/46.6） |
| `/city-benchmark` | `dim_city`(is_benchmark) + `ads_city_index` | 32 城，含四维 + 5 期 history |
| `/operation-timeline` | `ads_innovation_event` | 深圳 17 条，含 type/time/heat/location |
| `/field-distribution` | `ads_node_influence` GROUP BY domain_id | 6 领域 + 头部节点 |
| `/indicator-systems` | `ads_city_index`(CN-4403) | 5 期 overall + 四维 + 基础量 |

### 2.2 M5 湾区（5 个）
| 端点 | 结果 |
|---|---|
| `/bay-innovation/achievements` | 34 条湾区事件 ✅ |
| `/capability` | **3 城**（广州 76.4 / 深圳 80.25 / 东莞 93.53） |
| `/indicators` | 3 城 × 5 期 ✅ |
| `/swot` | 空态 + `emptyReason=NO_SOURCE_COLUMN` ✅ 诚实 |
| `/alerts` | 空态 + U5 deferred 说明 ✅ 诚实 |

### 2.3 M4 全球（5 个）
| 端点 | 结果 |
|---|---|
| `/global-innovation/achievements` | 230 条 ✅ |
| `/realtime` | KPI(230 事件/10 城/均值 56.75) + 月度趋势 + 领域分布 ✅ |
| `/carriers` | 全球载体榜（含 rank） ✅ |
| `/cities` | 全球城市指数 ✅ |
| `/alerts` | 空态 ✅ 诚实 |

**代码位置**
- innov：`ShenzhenController.java` / `BayInnovationController.java` / `GlobalInnovationController.java`（均 `@Inner(value=false)`）
- display：`ShenzhenInnovationController.java` / `BayInnovationController.java` / `GlobalInnovationController.java` + `RemoteInnovClient`（9 个 `@NoToken` 方法与下游 `@Inner` 配对）

---

## 3. 踩到并已固化的坑（**后续接续务必先看**）

1. **`ERROR 1267` 排序规则冲突**：`ads.*`(utf8mb4_0900_ai_ci) 与 `dim.*`(general_ci) 不能直接 JOIN → 全部 JOIN 显式写 `COLLATE utf8mb4_general_ci`。**已写代码注释禁止删除**。
   残留：现役 `CarrierController.rank/compare/detail` 同款缺陷，超出本管线范围，建议另开单。
2. **`Map.of` 不接受 null**：某期缺分维时抛 NPE 表现为 500 → 改用 `LinkedHashMap`，并把「为何不用 Map.of」写进注释。
3. **SQL 占位符顺序**：JOIN 里的 `?` 在 `WHERE IN (?)` **之前**，参数顺序写反会「查出来全空且不报错」。
4. **`node_influence.domain_id = 'ALL'` 是汇总行**，混入聚合会让领域占比翻倍。
5. **`city_code` 双形态**（`CN-4403` / `CN4403`）→ 统一取 `LIKE '%-%'` 一组。
6. **平台 Jackson 全局把 Long 序列化成字符串**（实测 innov 返回 `"total":"3"`）→ display 侧必须 `num()/dbl()` 强转，否则前端拿到字符串画不出曲线且无报错。
7. **前端 `request()` 已经剥壳**：`utils/request.ts:125-129` 的 `handleResponse` 在成功时返回的是 **`R.data` 而不是完整信封**。
   装配时不要写成 `res.data.data`，否则全是 undefined 且不报错。这一条是靠读源码确认的，照别处的写法抄会踩。

---

## 4. 数据边界（诚实，不许假装更多）

| 事实 | 影响 |
|---|---|
| 湾区 9 市中 **`dim_city` 只收录 3 城**（广州/深圳/东莞） | `/capability` 最多返回 3 城，且**不是过滤写错** |
| 深圳载体只有 3 条且 `admin_code` 全为 `440300`（市本级） | 按行政区筛选**必然查不到**，只能空态 |
| `indicator_values.source = ods_mock` / `benchmark_manual_pack` | **D4=mock 必现**，评审层须标 🧪 |
| `cfg_index_weight` 仅 2 行 | 撑不起 10 系三级指标树 → `/indicator-systems` 只给真实可得序列 |

---

## 5. 前端改造进度（M6 / D1）

**已完成**
- `types/shenzhenInnovation.ts`：无源字段改**可选**（不是必填补 0）；补录 `incubator` 与 `national/provincial` 两个真实值域
- `api/situation/shenzhenInnovation.ts`：裸 fetch → `Promise.allSettled` 拉 4 端点装配 `SzInnovationDataset`（**index.vue 零改动**）
- `models/szInnovationModel.ts`：clusterPoints/enterprises/patents/rdInvestment/talents 的 undefined 适配（含新增 `hasDomainMetricValue` 区分「0」与「无数据」）
- `mock/modules/shenzhenInnovation.ts`：`szCarrierTypes` 补 incubator；成果综合分/declineItems/description 的 undefined 适配

**✅ view 层 25 处已于 2026-10-28 全部修完**（`npm run type-check` → **0 错误**；`eslint` 改动文件 → **0 问题**）

| 文件 | 修法（均保持「无源字段可选」，**无一处置 0**） |
|---|---|
| `tabs/CarrierTab.vue` | `carrierIconMap` 补 `incubator`；地图热力/飞线改为**跳过缺坐标点**（不落 (0,0)）；`compareCellClass` 取值器放宽为 `number \| undefined`（缺失仅按 0 参与「谁领先」的比较，不影响展示）；模板改 `c.patents ?? '—'` |
| `tabs/DomainTab.vue` | `domainShareWidth` 缺失给最小宽度 8%；模板改 `domain.enterprises?.toLocaleString() ?? '—'` |
| `tabs/IndicatorTab.vue` | `yoy` / `unit` 缺失显示「—」且**不着涨跌色**（避免给「无数据」染上升绿的误导）；`formatSzIndicatorCompareValue(_, row.unit ?? '')` |
| 顺带清理 4 个未使用 import（`getSzCompareCityColor` / `szCompareCitySampleGroups` / `SHENZHEN_COMPARE_CITY` / `getSzIndicatorDepth`） | 其余 lint 干净 |

**✅ 端到端链路已跑通（2026-10-28 实测）**
```
vite dev(3000) → /api/display/v1/situation/** → rewrite 剥 /display → display(7099) → Feign → innov(7090)
POST /api/display/v1/situation/shenzhen-innovation/carriers  →  HTTP 200
  CARd559d3e49db1  深圳科技大学        university  national    51.88  rank 10
  CARINCCN4403     深圳科创孵化器      incubator   provincial  50.23  rank 12
  CAR63a241d95261  中科院深圳先进技术研究院 research …         rank …
```
> ⚠️ **踩坑记录**：vite proxy 的监听 key 是 `VITE_APP_BASE_API`（即 `/api`），前端 `BASE` 会拼在其后成为
> `/api/display/v1/situation/**`。本地直连（无网关）时 rewrite 才会剥掉 `/display`。
> 直接用 `curl localhost:3000/display/...` 会 404 ——**不是接口没通，是少写了 `/api`**。

**✅ M5 / M4 前端已完成（2026-10-28）**

`bayAreaInnovation.ts` / `globalInnovation.ts` 原本裸 fetch 到**根本不存在**的路径
（`/situation/v1/bay-area/innovation/dataset`、`/situation/v1/innovation/dataset`），现改为调用真实 REST。

| 页 | 装配来源 | 有源 ✅ | 无源留空 ⬜ |
|---|---|---|---|
| M5 湾区 | achievements(34) / capability(3城) / indicators(3城×5期) | cities、points、capacities.score + 分维 + history | mechanismIndex / trend / alertLevel / district / institution / alerts / swotData / indicators |
| M4 全球 | achievements(230) / carriers(28) / cities | innovations、carriers.score+rank、cities.score+rank+radarData | dimensions 全嵌套、patents/papers/projects/createYear、policySuggestions、alerts |

**两处需要特别留意的判断（别改回来）**
1. **前端 `BayAreaPointType` 原本 6 档**（patent/paper/news/…），真实 `event_type` 实测 **12 档**
   （financing52 / fund_project38 / bid27 / invest23 / policy20 / biz_dynamic14 / ma14 / achievement13 /
   award8 / industry_event8 / tech_break7 / talent_flow6），**既不一一对应也不存在包含关系**
   → 照 M6 处理 incubator 的原则**补录真实值域**，而非塞进 patent/paper/news。
2. **M4 `InnovationCity.dimensions` 是「投入/产出/环境/绩效」四组嵌套**，源表是
   output/resource/environment/**institution** 四个平铺键，**不同构也不同义**
   → 不硬拆八个 slot，全部留 NaN，只在 `radarData` 原样给能确证的四维。

**统一占位纪律**：无源字段数值用 **`NaN`** 而不是 0 —— 0 会渲染成「0 件/0 分」这种像真的一样的假数据，
而 NaN 会让 ECharts 直接跳过该点（不画假曲线）。`alertLevel` 加 `'unknown'` 档，**不回落 'normal'**
（回落等于宣称「检查过且正常」）。

**验收结果**
- `npm run type-check` → **0 错误**（全项目）
- `npm run build` → **✓ built in 1m 19s**，dist 产出正常
- 三页 `index.vue` **均零改动**（U4 要求达成）
- 链路实测：`/api/display/v1/situation/{bay-innovation,global-innovation}/*` 经 vite proxy **全部 200**
- lint：本次改动文件**全部干净**；剩余 14 处为**既有技术债**（`index.vue` 命名规则 ×3、
  `InnovationMonitor.vue` 的 `alerts` 重复键、`InnovationRanking.vue` 未用 emit，等），
  均不在我改动的文件内，`--fix` 无法自动处理，需另开单清理。

**✅ R0 评审底座 + R1–R3 角标已完成（2026-10-28）**

照 `lumen-ui-topic/src/review/` 的组织方式做集中单目录管理：

| 文件 | 作用 |
|---|---|
| `src/review/feature.ts` | 总开关 `REVIEW_FEATURE.enabled`，`isReviewFeatureEnabled()` |
| `src/review/readiness.ts` | readiness 只读镜像，**每条评级都附可复核 SQL** |
| `src/review/index.ts` | 集中出口，外部统一 `@/review` 导入 |
| `src/review/README.md` | 上线清理清单（5 步 + 检索校验项） |
| `src/components/common/DataSourceBadge.vue` | 角标组件，根部 `v-if` 门控 |

三页 `index.vue` 各加 1 处挂载（右上角），另有 import。

### 定级依据（实测，不是照矩阵抄的）

| 数据源 | 标记列 | 实测取值 | 定级 |
|---|---|---|---|
| `ads.city_index`（365 行/73 城/5 期） | `weight_version` | `w_v1.0-demo` | **D4 🧪** |
| `ads.innovation_event`（230 条） | `model_version` | `weighted_score_v0.1-demo` | **D4 🧪** |
| `dim.carrier`（28 条） | `source` | `v1_approx` | **D2 🟡 近似** |

> ⚠️ **这里纠了自己一个错**：我先前把 `carrier` 按 mock 处理，实际它是 `v1_approx`（近似值），
> **没有** demo 标记，两者对外含义差别很大 —— 已按实际改判 D2 并在 `readiness.ts` 里留了警示注释。

### 关于「DOM 零泄漏」要说清楚（别过度承诺）

关闭开关能保证的是 **DOM 里不出现角标节点**（`v-if` 求值为 false，组件根本不创建，
不是 CSS 隐藏）；但**组件 JS 仍会留在 bundle 里** —— `isReviewFeatureEnabled()` 是运行时函数调用，
Rollup 不会在构建期消除。想彻底清干净，走 README 清理清单第 3 步删文件。
这个区别在 README 和此处都写明了，不接受含糊。

### 验收
- `npm run type-check` → **0 错误**
- `npm run build` → **✓ built in 1m 11s**，EXIT=0
- lint：本次改动文件**全部干净**；仅剩 3 处既有的 `index.vue` 命名规则告警（非本次引入）

**至此 C 系列原本列出的工作全部完成**：后端 15/15 端点、前端三页接线、R0 底座、R1–R3 角标。
剩余未完成项只有一项：**既有 lint 技术债**（14 处，均不在本次改动文件内，`--fix` 无法自动处理，需另开单清理）。

---

## 6. 待办清单（按优先级）

1. **修 view 层 25 处类型错误** → 使 `npm run type-check` 通过
2. 浏览器走查 M6 页面（需 dev server 3000 + display 7099 + innov 7090）
3. M5 / M4 前端接线（复刻 M6 模式）
4. R0 评审底座 + R1–R3 角标挂载
5. 契约 §7 实装对照表回填 + registry/WBS 逐叶留痕

## 7. cost 四字段

| 字段 | 值 |
|---|---|
| `cost_warn` | `amber`（任务未完：后端完整，前端 partial） |
| `actual_cost` | 12.5 |
| `model_used` | `auto` |
| `actual_tokens` | 2400000 |
