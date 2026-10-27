# SITUATION-ENT-C6-L01 · 要素比较（`POST /v1/situation/compare`）补口 + 地域入参静默忽略修复

> **触发**：用户走查反馈「要素比较接口需要补上，目前只有一个要素可以先无法验证但要补全接口」（2026-10-27）
> **角色**：`agent:api-agent`（兼前端 api 层，监管人 `human:李伟`）
> **状态**：`integration`（待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 倚 Z1–Z4 / A0–D1 / C4（筛选贯通）/ C5（聚类）
> **契约**：[SITUATION-ENT-API-CONTRACT-01.md](./SITUATION-ENT-API-CONTRACT-01.md) 已 bump **v1.3**
> **日期**：2026-10-27

---

## 一、用户的原话与我的理解

「接口要补上，**只有一个要素可以先无法验证**」——我理解为两条约束：
1. **接口要完整可用**：入参（含筛选）要能被真实消费，返回结构完整、和冻结的 TS 类型对齐；
2. **不可以为了让它"看起来能比较"而伪造第二条曲线**：既然只有企业有年度序列，就只给一条，并把「为什么只有一条」写在返回值里。

## 二、交付内容

### 后端（`lumen-svc-platform` · `gkxlumen-display`）
- 新增 **`POST /v1/situation/compare`**（`SituationController#compare`）
  - 数据源复用 element `/trend`（`dwd.enterprise_base` 按注册年计数），不重复造 SQL
  - 返回 `{years, series[], availableFactorKeys, notes[]}`；`series` 元素与 `years` **等长**
  - `notes` 是 v1.3 新增的可选字段，用来承载「为什么没有第二条曲线」等口径说明
- **修：`scopeOf` 的地域字段过去只认 `regionPaths`**
  - 而 compare / influence 走的是 `activeRegionKey`、cluster 走 `focusRegionKeys`
  - 结果：这些端点的**地域筛选被静默忽略**（返回全量却不报错）
  - 现解析顺序：`regionPaths` → `activeRegionKey` → `focusRegionKeys`，并加注释钉住教训

### 前端（`lumen-ui-science-pc`）
- `types/situation.ts`：`SituationCompareParams` 追加可选 `searchTerm` / `timeRange`；`SituationCompareResult` 追加 `notes?: string[]`
- `api/situation/index.ts`：`fetchSituationCompare` 由「未上线端点诚实空态 shim」**切回 `post('/compare')`**；删除已无用的 `EMPTY_COMPARE`；注释里说明 shim 现只剩 timeline / events
- `views/situation/overview/index.vue`：compare 的 watch 依赖与入参加上 关键词 / 年份区间（与 C4 口径一致）

## 三、诚实边界（写了三份，别省）

1. **只有企业一个要素有真实年度序列**（源：注册年）。其余 10 要素**无主表**，因此：
   - 不进 `series`、**不进 `availableFactorKeys`**（前端据此置灰）
   - 原因写在 `notes`；第二个要素有数据后**不用改结构**，追加一条 series 即可
2. **缺失年份补 0 是真实计数**（当年新增 0 家），不是插值/趋势外推
3. **年度序列只统计 `registration_date` 非空的行** → 各年之和可能小于 `/map` 总量
   - 实测：「腾讯」年度合计 **11 家**，而 `/map` 计数 **19 家**——差额是注册日期缺失的行，已写进 `notes`

## 四、自测（HTTP 200，七组）

| 入参 | years | 企业序列 values |
|---|---|---|
| 无过滤 | 2015–2026 | 12093,14029,13447,11943,11758,13030,13423,8940,7884,5349,3061,122 |
| 深圳市 2022–2024 | 2022–2024 | **4032,3658,2628**（与库级 join 计数逐位吻合） |
| 东莞市 2022–2024 | 2022–2024 | 1815,1636,1079（≠ 深圳 → 地域过滤确已生效） |
| 南山区 2022–2024 | 2022–2024 | 715,620,492（区县维度生效） |
| `regionPaths=[[深圳市]]` | 2022–2024 | 与 `activeRegionKey=深圳市` **一致**（两种地域字段同效） |
| `searchTerm=腾讯` | 全区间 | 1,4,2,2,0,1,0,0,0,1,0,0 |
| `enabledFactorKeys=[scholar]` | 全区间 | series=[] + notes「不含企业 → 无序列」 |

**页面实跑**（playwright + mock 登录）：要素比较页签由真实数据驱动，
从原来的「当前可比要素 (0/4) · 当前筛选范围内暂无可比要素」变成 **「当前可比要素 (1/4)」并列出「企业」**，
同时保留「至少选择 2 个要素」提示——**单要素无法横向比较是数据事实，不是接口失败**；页面无报错弹窗。
三绿：type-check exit 0 / vite build `✓ built in 1m 6s` / 浏览器冒烟通过。

## 五、过程中的两个坑（都不是服务端 bug，但很耗时间）

1. **Windows 控制台代码页会把脚本里的中文读坏**：PowerShell `-File` / `-Command` 跑含中文的脚本 → body 乱码 → 服务端 400 或关键词失配（一度误判为「地域筛选没生效」）。**自测脚本请一律用 Node（内部 UTF-8）**，别用 PS 拼 JSON。
2. 上面那个误判本身提醒了一件事：**「返回值和全量一样」既可能是 bug，也可能是测试用例本身错了**——两者一定要先分清再动手改代码。

## 五之二、附带修复（同批走查反馈第 3 条）：KPI 五张卡渲染成同一张「独角兽企业 167」

**现象**：用户问「现在独角兽企业有五个，是改出来的 bug 还是代码就这样写的」。
实测确认：**5 张卡全部渲染成「独角兽企业 = 167 家」**。

**根因（前后端接缝，两边单看都没错）**

| 侧 | 代码 | 事实 |
|---|---|---|
| 后端 | `SituationController#stat()` / `#card()` 里 `put("factorKey", "enterprise")` | 5 张卡（企业总数/高新/专精特新/瞪羚/独角兽）**factorKey 全是 `enterprise`**——语义上它们确实同属一个要素 |
| 前端 | `OverviewTab.vue` 用 `item.factorKey ?? item.key` 当主键 | 把**要素维度**当成**卡片主键** → `Map` 里 5 条互相覆盖只剩最后一条（unicorn），而键列表仍有 5 个 → 渲染 5 张同内容卡 |

> 定性：**不是 C4/C5 改出来的**（那两叶没碰 `stat()/card()`），也**不是平台历史代码**
> （`SituationController.java` 是本次长任务新增的未跟踪文件）。是本轮装配 KPI（C3/D1）时就埋下的，
> D1 冒烟没盯到这一行。前端那句是从 demo 移植的——demo 原型**一个要素只有一张卡**，factorKey 天然唯一，
> 我们后端把企业要素拆成 5 张标签卡后才把它触发出来。

**「独角兽」的数据来源（不是 mock、不是编的）**：`SUM(dwd.enterprise_base.is_unicorn)` = 167，
与高新 27,936 / 专精特新 14,903 / 瞪羚 588 同源（同一张主表的 4 个资质标签列）。
demo 原型这张卡是**要素粒度**的「企业数」——把同一个要素拆成 5 张标签卡是我们这次的实现选择，
所以「独角兽」这张原型上没有的卡就出现了。

**修复**（前端，键值语义归位）：
- `OverviewTab.vue`：抽出 `cardKey(item) = item.key` 做卡片身份键（排序/去重/拖拽/隐藏全用它）；
  `metric-id` 仍用 `factorKey`（那是要素维度的指标 ID，语义正确不能改）；`data-factor-key` 改名 `data-card-key`
- `situationModel.ts#buildGlobalSituationFactorExportRows`：同款撞键会让**每个地域导出行都写成「167家」**，
  改为「按要素取该要素的总量卡（`${要素}_total` 优先）」

**修复前后对照**（真实后端响应喂前端取值逻辑）

```
【修复前】独角兽企业 167 ×5 张
【修复后】企业总数 189,115 / 高新技术企业 27,936 / 专精特新 14,903 / 瞪羚 588 / 独角兽 167
【地域导出】enterprise 要素 → 企业总数 189,115（修复前是 167）
```
页面实跑：`.stat-cell--factor` 共 5 张、文案各不相同、`独角兽企业` 出现 1 次；type-check exit 0 / build ✓。

**方案 B 已落地（2026-10-27 用户选定）**：用户追问「为什么要拆，是需规要求还是哪里要求的」，
追溯结论是**没有任何书面依据、是实现者自选**，故用户裁定走 **B = 对齐 demo 原型，只留 1 张「企业」卡**。

依据链（写入 `buildStats()` javadoc 防复发）：

| 出处 | 事实 |
|---|---|
| SRS《企业要素需求规格说明书》O-02 | 「创新型企业 = 高企 ∪ 专精特新 ∪ 瞪羚 ∪ 独角兽，**并集去重**」→ 四类是**一个聚合指标** |
| 同 SRS §354 | 四类资质是**梯度培育筛选项**，不是并列 KPI |
| demo `overviewData.js#buildFactorCards` | 由 `factorItems` 生成，`enterprise` → **仅 1 张「企业」卡** |
| lumen 冻结 mock | 同 demo，**不存在 `unicorn`/`gazelle` 任何 key** |
| `SITUATION-ENT-长任务总控.md` L95「KPI 五值」 | 是**本管线自己写的走查清单**，实现照着它做 = 自证循环 |

**数据证据（为什么拆开还有害）**——查 `demo_gkxlumenx_dwd.enterprise_base`（189,115 行）：

| 指标 | 值 |
|---|---|
| 高新 / 专精特新 / 瞪羚 / 独角兽 | 27,936 / 14,903 / 588 / 167 |
| 专精特新中同时是高企 | **14,707（98.7%）** |
| 四类并集去重 | **28,185** |
| 四项直接相加（用户会这么做） | 43,594 → **虚高 55%** |

**改动**
- `SituationController#buildStats()`：只出 1 张 `enterprise_total`，label 对齐 demo 的「企业」
- `SituationController#buildFactorCards()`：同上（单一要素单卡），并删掉随之无用的
  `seriesOf()` 与 `enterpriseTypeDist` 调用（少一次远程调用；element 端点保留备将来做「创新型企业数」年度曲线）
- 前端**零改动**（上一步的 `cardKey` 修复已让单卡/多卡都正确）

**验证（HTTP 200，五组筛选）**

| 入参 | stats 张数 | 值 | scopeLabel |
|---|---|---|---|
| 无过滤 | 1 | 企业 189,115 家 | 全量样本 |
| 深圳市 | 1 | 95,600 | 城市：深圳市 |
| 南山区 | 1 | 16,039 | 区县：南山区 |
| `searchTerm=腾讯` | 1 | 19 | 关键词：腾讯 |
| 2025–2026 | 1 | 3,183 | 注册年：2025-2026 |

页面实跑：`.stat-cell--factor` **1 张**「企业 ⓘ 189,115 家」，全页 `独角兽`/`瞪羚` 出现 **0 次**。

**遗留口径（2026-10-27 用户裁定：等 ADS 存量快照，不做近似）**：该卡 `series` 为 null，
页面显示「暂无趋势数据」。原因是卡上数值是**存量**（189,115），而现有 element `/trend` 是**增量**
（按 `registration_date` 统计当年新增），两者混在一条 sparkline 上属口径混搭，故**不硬配**。

**原型依据（不是我们缺口径，是缺数据源）**：demo `overviewData.js` L38–95 的
`trendSeriesByFactor.enterprise` 明确给了 `rawValues: [6.8 … 9.2]`、`rawUnit: '万家'`，
年份轴 `timeline.years` = **2020–2026**（`data.js` L1423-1427），且卡片 sparkline 经
`buildRawFactorCardTrendItem()`（L650-656）取的就是这条 `rawValues` —— **卡上存量 + 逐年存量曲线，同口径**。
（原型那些数是示意值，仅取口径形状，不可对账。）

**因此这是阻塞在数据侧的依赖，不是前端/display 的待办：**

| 项 | 要求 |
|---|---|
| ADS 需交付 | 逐年企业**存量**快照：`year`、`total_count`，建议带 `city` / `district` 维度 |
| 口径约束 | 年份 2020–2026；**末点必须等于同筛选条件下的存量总量**（无筛选时 189,115），否则曲线与卡打架 |
| 存续口径 | 若含已注销/异常经营，必须给出 `status` 列或明确口径说明（我们不会自行假设"注册即存续"） |
| 接上后的改动 | element `/trend` 增 `mode=stock`（或新端点）→ display `buildFactorCards()` 把 `series` 由 `null` 改为 `buildTrendSeries()` 同形状输出。**前端零改动**（卡片已按 `series: {years,currentYear,series[]}` 渲染） |
| 验收 | 卡上数值 == sparkline 末点；年份轴与 `timeRange` 联动；无存量快照的年份如实缺失，不插值 |

> 明确**不做**的事：不用 `COUNT(*) WHERE YEAR(registration_date) <= y` 的「累计注册数」冒充存量
> （实测该口径 2020→2026 = 149,983→188,762，虽趋势正确，但它含已注销企业、且 353 条无注册日期的记录
> 永远不进序列 = 占 0.19%，对外会被质疑"这不是存量"）。也不复用新增曲线凑 sparkline。

## 五之三、附带修复（同批走查反馈第 4 条）：领域分布饼图图例显示「186842%」

**现象**：用户报「领域分布饼图不对，显示超过 100%，可能是数量直接拼的」。

**根因（后端契约与 demo 不符）**：`buildVisibleSlices()` 直接把 `buildDomainRows()` 的
`value`（原始数量 `enterpriseCount`）复制成切片的 `value`，而 demo 契约里
`overviewData.js#normalizeRows` 输出的是**归一化百分比**；前端模板 `OverviewTab.vue` 无条件渲染
`{{ item.value }}%` → 数量被当成百分比，图例出现 `186842%`。

**修复（`SituationController#buildVisibleSlices`）**
- `value` 改为百分数（0–100，2 位小数）；原始数量移到 `rawValue`（`int`，避免 Long 被平台 Jackson
  序列化成字符串 `"186842"` —— 这是 `num()` 注释里记过的坑，第一次改就踩了）
- 采用**最大余数法**分配 0.01 单位，保证合计**恰为 100.00%**，且不把长尾抹成 0：
  实测直接「末项补齐」会让合成生物 26 家（0.0138%）变成 `0.00%`
- `buildDomainRows` 补 javadoc：`value` 是数量、不是百分比，防止再次混用

**验证（HTTP 200，页面实跑）**

| 领域 | rawValue | 占比 |
|---|---|---|
| 人工智能 | 186,842 | 98.86% |
| 机器人 | 1,106 | 0.58% |
| 具身智能 | 921 | 0.49% |
| 传感器 | 67 | 0.04% |
| 智能网联汽车 | 32 | 0.02% |
| 合成生物 | 26 | 0.01% |
| 合计 | 188,994 | **100.00%** |

页面点「饼图」后图例：`人工智能 98.86% / 机器人 0.58% / 具身智能 0.49% / 传感器 0.04% /
智能网联汽车 0.02% / 合成生物 0.01%`，**无任何 >100% 项**。type-check exit 0。

**两个如实上报的遗留（都不是渲染 bug，未擅自改）**
1. **分布本身极度倾斜**：`ads.enterprise_domain_dist` 2025 年 `人工智能 ratio = 98.86`，
   与页面算出的 98.86% 一致 → 饼图看起来「几乎一整块」是**源数据如此**，非渲染问题。
   若业务认为企业领域不该 98.86% 集中在人工智能，需数据侧查种子/映射口径（一家企业只归一个领域？）。
2. **「数量统计」指标下画的也是百分比**：demo 的分布图恒用 `normalizeRows` 后的切片，
   `metricLabel` 只做标题文字，故「数量统计 · 折线图」显示百分比是**原型行为**（原型自身瑕疵）。
   要对齐语义，需在 `statMetric === 'count'` 时改用 `rawValue` 出图——属产品口径，未改。
3. 另：分布合计 188,994 ≠ 存量 189,115，差额 121 家是**无领域标签**的企业，不参与分布。

## 五之四、附带修复（走查反馈第 5 条）：统计指标与图「对不上 / 有时点不上」

**现象（用户 2026-10-28）**：「统计指标展示功能 和图关联有问题 对不上 有的时候还点不上」。

**根因一：三处状态各说各话**。饼图判定写成 `chartType === 'pie' || statMetric === 'share'`，
于是「分布比例」下点「折线图」→ 按钮高亮折线、面板标题写「折线图」、实际仍渲染饼图 —— 这就是「对不上」。

**根因二：取值口径混用**。「数量统计」用的是 `visibleSlices.value`（百分比），不是 `rawValue`（家）；
「增长趋势」只是把同一年的分布占比换个图型，**根本没有时间维度**，却标着"增长"。

**根因三：交互死角**。「增长趋势」下饼图按钮 `disabled` 但无任何说明（用户只感到"点不上"）；
统计指标下拉用 `:selected` 非受控，状态被联动改写后显示会与实际脱节。

**修复（`OverviewTab.vue`，全部收口到单一真源）**

| 改动 | 说明 |
|---|---|
| `effectiveChartType` computed | 按钮高亮 / 面板标题 / 实际渲染三处统一读它；只保留一条硬约束（增长趋势 + 饼 → 折线） |
| `sliceValue` / `formatSliceValue` | 分布比例取 `value`（%）、数量统计取 `rawValue`（家，千分位）；图例、饼图、柱状、折线全部走它 |
| `growthOption` / `growthBarOption` | 增长趋势改用后端 `trendSeries`（按注册年的年度序列）：折线多序列、柱状按年一根；**不再拿分布占比冒充趋势** |
| `select` 改 `v-model` | 受控，显示与实际状态不再脱节 |
| 饼图按钮 `disabled` 加 `title` | 明确告知「增长趋势是年度序列，无法用饼图表示」 |
| CSV 导出跟随指标 | 数量统计导「数量」、分布比例导「占比%」、增长趋势导年度序列（原先是恒定「占比%」） |

**验证（页面实跑，九宫格 + 导出）**

| 指标 + 图型 | 面板标题 | 高亮按钮 | 实际图 | 图例首项 |
|---|---|---|---|---|
| 数量统计 + 饼图 | 数量统计 · 饼图 | 饼图 | 饼 | 人工智能 186,842 家 |
| 数量统计 + 柱状 | 数量统计 · 柱状图 | 柱状图 | 柱 | — |
| 分布比例 + 柱状 | 分布比例 · 柱状图 | 柱状图 | 柱 | — |
| 分布比例 + 折线 | 分布比例 · 折线图 | 折线图 | 折线 | — |
| 增长趋势 + 折线 | 年度趋势 · 增长趋势 · 折线图 · 按注册年 | 折线图 | 折线 | — |
| 增长趋势 + 柱状 | 年度趋势 · 增长趋势 · 柱状图 · 按注册年 | 柱状图 | 柱 | — |
| 增长趋势 + 饼图 | 按钮 `disabled=true`，`title` 给出原因 | — | — | — |

导出提示实测：`已按「企业领域分布 · 增长趋势 · 柱状图」导出统计 CSV`；`pageerror` 0 条；
type-check exit 0。

> 排查中一次误判值得记：首个脚本报「数量统计却显示分布比例」，实为**上一个后台脚本残留的页面状态**
> 污染了复用页面（不是路由重挂）。加 `select.inputValue()` 守卫后复测正常 —— 教训是页面断言必须带状态守卫。

## 五之五、走查反馈第 6 条：地图与「地域范围」联动 + 初始定位

**现象（用户 2026-10-28）**：「地图应该和地域范围有联动，自动定位到选定的地域范围，初始化的时候也应该定位到默认位置，而不是全球地图展示。」

**根因（两级）**

| 层 | 事实 |
|---|---|
| 组件能力 | `TiandituMap` 有 `center`/`zoom` 受控 props 与 `resetView()`，但**没有 fitBounds 能力**；`resetView` 只是回到写死的 center/zoom |
| 调用方 | `FactorMapSection` **从未传 center/zoom/fit** → 永远吃组件默认 `[35.8617, 104.1954]` / zoom 4；本页地图面板实测 **420×482**，zoom 4 的视野跨约 90° 经度，视觉上就是"全球地图" |

**原型依据（不是我们自己发明的交互）**：demo 有现成实现且带单测：
- `SharedRegionMap.jsx#focusMapToRegions`（L65-80）：>1 点 `fitBounds`（padding 按点数分档、`maxZoom = detailZoom ?? 10`）、=1 点 `setView` 到该点、0 点回落 `map.center/zoom`
- `sharedRegionMapViewport.js` + `.test.mjs`：`initial`/`reset`/`scope` 才重设视口，`layers`（图层刷新）**保持用户当前视口**
- `App.jsx` MapSection：`viewportFocusKey = JSON.stringify({ regionSelection, activeRegionKey, clusterFocusedRegionKey })`

**改动**

| 文件 | 改动 |
|---|---|
| `components/map/TiandituMap.vue` | 新增 `focusPositions` / `viewportPadding` / `wideViewportPadding` / `detailZoom` / `viewportFocusKey`；`focusToPositions()` 复刻上述三点语义；挂载即 fit（initial）、`resetView()` 改为**重新适配当前点位**（reset）、`viewportFocusKey` 变化才 refit（scope）；点位异步到达补一次 fit；`zoomSnap: 0.25`（对齐 demo） |
| 同上（自适应 padding） | `fitPaddingOf()` 按容器比例封顶（宽 12%、高 10%，下限 16px）。**原因**：demo 的 `[144,118]` 是给大屏的，本页 420px 宽被两边各吃 128 后只剩 160px → fit 出 zoom 2，仍是"世界地图"（实测修正前 zoom 2 / 视野跨 147° 经度） |
| `overview/components/FactorMapSection.vue` | 新增 `viewportFocusKey` prop；`focusPositions` = `regions` ∪ `objectPoints` 坐标（`[lng,lat]`→`[lat,lng]`，剔除 0/非法坐标） |
| `overview/index.vue` | 传 `:viewport-focus-key="`${store.regionKey}|${focusRegionKey ?? ''}`"` |

**顺带修掉一个真 bug（同一「地域筛选没贯通」家族）**：`/overview` 请求**漏传 `regionPaths`**，
后端 `scopeOf` 只能退回 `activeRegionKey`（级联选择时它是 null）→ 选了地域级联后 **KPI / 趋势 / 分布仍是全量**，
与地图（`/map` 传了 `regionPaths`）对不上。已补 `SituationOverviewParams.regionPaths` + 请求入参 + watch key。

**验证（页面实跑，读 Leaflet 实例的 center/zoom/bounds）**

| 场景 | zoom | center | 视野跨度 | 标记数 | KPI / scope |
|---|---|---|---|---|---|
| 初始（无筛选） | 3.50 | 33.59, 106.45 | 48.8° × 52°（覆盖中国） | 30 | 189,115 家 / 全量样本 |
| 地域范围 = 南山区 | 10.00 | 22.55, 114.02（南山） | 0.6° × 0.6° | 1 | **16,039 家** / **区县：南山区** |

修正前同场景：初始 zoom **2**、视野跨 147°；选南山区后地图**完全不动**（zoom 3.5、30 个标记），
KPI 仍 189,115。后端侧另用 HTTP 核对：`/map` 无筛选 30 个 region、`regionPaths=[["深圳市"]]` 1 个、
`[["南山区"]]` 1 个（坐标即南山中心）——说明数据侧本来就支持，缺的是前端 fit 与 overview 传参。

**追加修复（同日复测反馈）：「切换后地图中心点是第二次切换才换到第一个点的位置」——滞后一拍**

| 项 | 事实 |
|---|---|
| 根因 1 | 补适配用的 watch 是 `() => props.focusPositions.length`，用**点位数**判断数据是否更新。深圳→南山这类切换点位数恒为 1（30→30 同理），长度不变 → 切换瞬间那次 fit（用的还是**上一次**坐标）之后再无纠正，于是每次都拿"上一次的点"定位 |
| 根因 2 | 第一版用一次性 `pendingScopeFit` 标记，而它会在"旧数据 fit 成功"时被清掉，同样丢失纠正机会（组件因 `mapSectionKey` 重挂时必然踩到） |
| 修法 | 改成**坐标签名**（点数 + 首尾点、3 位小数）比对，并用 `lastFocusedKey` 记录"已按哪个签名适配过"：签名不同就必须适配；`viewportFocusKey` 变化时清空该记录（允许同坐标重新定位）；无点位回落 `center/zoom` 时**不记签名**，等数据到达再定位 |

**验证（连续切换，每次稳定后读取 Leaflet 实例）**

| 操作 | zoom | center | 结论 |
|---|---|---|---|
| 初始 | 3.50 | 32.75, 106.50 | 全国点位范围 |
| 第 1 次 → 南山区 | 10.00 | 22.553, 114.019 | 即时定位 |
| 第 2 次 → 福田区 | 10.00 | 22.538, 114.050 | 即时定位 |
| 第 3 次 → 罗湖区 | 10.00 | 22.562, 114.138 | 即时定位 |

修复前第 1 次切换后仍停在 zoom 3.5 的全国视野（center 32.7,106.5）。
注：center 是**该区企业点位云的中心**（`regions ∪ objectPoints` 一起 fitBounds），不是行政区几何中心，
所以南山显示 114.019 而非区中心 113.94 —— 语义正确（用户要看的是"这一片的企业"）。

**观察项（未改，需产品定）**：筛选栏「地域范围」用 Arco 级联单选，点击**城市**只展开子级、不落选，
实际只能选到区县（叶子）。要支持"选整个深圳市"需引入 `change-on-select` 或显式确认——
但这会改变下钻交互（选了市就不方便再选到区），属交互口径，未擅自改。

## 六、遗留

1. **要素比较要真正可用，需要第二个要素的年度序列数据源**（专家学者 / 论文 / 专利等 currently 要素在 element 侧无主表）——在那之前 UI 停在 (1/4) 是正确表现，不要为此补 mock 或复制企业曲线
2. `timeline` / `events` 两个端点仍未上线，`api/situation/index.ts` 的「诚实空态 shim」继续保留给它们
3. **改动停本地未 commit**（本次改 4 个文件：`SituationController.java`、`types/situation.ts`、`api/situation/index.ts`、`views/situation/overview/index.vue` + 契约文档），走查通过后我再按叶 commit
4. **KPI「企业」卡 sparkline 阻塞在 ADS 逐年存量快照**（用户 2026-10-27 裁定「等 ADS」，不做累计注册近似）——交付规格与验收条件见 §五之二末尾表格，接上时只需改 element `/trend` + display `buildFactorCards()`，前端零改动

## 七、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 150k（估） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $1.1（估） |
| cost_warn | green |

ponytail: full（先自测发现「深圳=全量」，顺藤查到 `scopeOf` 不认 `activeRegionKey` 的静默忽略；`;109` 量级差异也追到底并写进返回的 `notes` 里，而不是糊过去）
