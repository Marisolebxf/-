# SITUATION-ENT · API 契约（v1.3）

> 状态：**草案（待 C3/D1 前冻结）**  
> 基准（U5 裁定）：**lumen 现实现为真源** —— `lumen-ui-science-pc/src/types/situation.ts` + `src/api/situation/index.ts` + `src/mock/modules/situation.ts` 双轨现状。  
> 上位：[`SITUATION-ENT-长任务总控.md`](./SITUATION-ENT-长任务总控.md)  
> 规则：改契约先 bump 本文件版本，再同步 `types/situation.ts` 与 mock 种子；**本文件不复制既有 6 端点全字段**（以 `types/situation.ts` 为准防两处漂移），只登记变更与新增。

---

## 1. 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-10-27 基线 | = `types/situation.ts` 现状（7 端点：map/timeline/overview/events/influence/cluster/compare；BASE `/display/v1/situation`；全部 POST；`USE_MOCK` 双轨） |
| v1.1 | 2026-10-27 | ① `/map` 的 `objectPoints` 由恒空改为真实企业点位（U3）；② `/influence` 后端实现规格（U1/U2，此前仅 mock）；③ 全局 `USE_MOCK=false` 后未实现端点的 404 空态约定（U4） |
| **v1.2** | 2026-10-27 | ⚠️ **修正 `/influence` 响应结构**：v1.1 §2 写成简化的 `{count, averageScore, items[]}`，与冻结的 `types/situation.ts` **不一致**（真实类型是 `InfluenceDataset`：`analyzableFactorCount/cards[]/defaultFactorType/totalCount`）。按 U5「lumen 现实现为真源」以 `types/situation.ts` 为准重写 §2，并补「过滤器支持矩阵」（哪些入参真实生效、哪些未应用必须诚实声明）。**无 delete 端点的字段变更，前端结构仍零改动** |
| **v1.3** | 2026-10-27 | ① **新增 `POST /display/v1/situation/compare`（C6 叶）**：响应在既有 `{years, series[], availableFactorKeys}` 上**追加可选 `notes?: string[]`**（口径备注，纯增量，视图不读也不影响既有渲染）；入参在既有 `{enabledFactorKeys, selectedFactorKeys, selectedFieldValues, activeRegionKey}` 上追加可选 `searchTerm` / `timeRange`（与 C4 的筛选语义同族）。② **地域入参字段统一**：`scopeOf` 此前只认 `regionPaths`，导致 compare/influence 传的 `activeRegionKey` 被**静默忽略**（返回全量却不报错）。现解析顺序 `regionPaths` → `activeRegionKey` → `focusRegionKeys`。详情与自测见 §6 |
| **v1.4** | 2026-10-28 | ① **`/influence` 地域入参并入 `scopeOf`**：此前本端点只认 `activeRegionKey`，用户在筛选栏选「地域范围」后榜单仍是全量（**静默忽略**），现与 `/map` `/overview` `/compare` 同源。② **`/cluster` 入参替换**：`focusRegionKeys` **废弃**（它是「地图上的区域列表」，取首项会把样本静默缩到一个城市），改收 `regionPaths` / `activeRegionKey` / `searchTerm` / `timeRange`；**响应新增可选 `scopeLabel`**（样本真实范围，UI 据此标注）。入出参同步进 `types/situation.ts`，**视图零改动**。详见 §7 |

## 6. 新增实现：`POST /display/v1/situation/compare`（C6 叶）

> **写作动机（用户 2026-10-27 反馈）**：「要素比较接口需要补上，目前只有一个要素可以先无法验证但要补全接口」。
> 即：接口要完整可用，**可用一条是一条**，但绝不为了「看起来能比较」伪造第二条曲线。

**入参**（`SituationCompareParams`，新增字段皆为可选）

| 字段 | 生效情况 |
|---|---|
| `enabledFactorKeys` | ✅ 生效：不含 enterprise 时企业序列不出（并给 note 说明） |
| `selectedFactorKeys` | ✅ 生效：非空时只返回被勾选要素的序列 |
| `activeRegionKey` | ✅ 生效（v1.3 修复前**被静默忽略**）→ 市区按 `city` / `district` 过滤 |
| `searchTerm`（新增） | ✅ 生效 → `enterprise_name LIKE` |
| `timeRange`（新增） | ✅ 生效 → 决定比较曲线横轴 `years` |
| `selectedFieldValues` | ❌ 不参与过滤（企业主表无逐行领域列），同 §2 过滤器支持矩阵 |

**响应**（`SituationCompareResult`）

- `years: string[]` —— 横轴（默认起 2015，止于当前年）
- `series: CompareFactorSeries[]` —— `{key,name,color,unit,values:number[]}`，与 `years` **等长**
- `availableFactorKeys: string[]` —— 当前范围内真正有年度序列的要素
- `notes?: string[]` —— **v1.3 新增**：口径备注（见下）

**诚实边界（必须随接口一起读，否则会被误认为 bug）**

1. **只有 `enterprise` 一个要素有真实年度序列**（源：`dwd.enterprise_base.registration_date` 按年计数）。
   其余 10 要素（专家学者/会议/组织机构/论文/专利/…）element 侧**无主表**，故：不进 `series`、**不进 `availableFactorKeys`**，
   原因写在 `notes`。→ UI 会停在「当前可比要素 (1/4) · 至少选择 2 个要素」，**这是数据现状，不是接口没做完**。
   第二个要素一旦有数据源，本端点无需改结构，追加一条 series 即可。
2. **缺失年份补 0 的性质**：某年无企业注册时 SQL GROUP BY 不出该行，补的 0 是「当年新增 0 家」的真实计数，不是插值。
3. **年度序列只统计 `registration_date` 非空的行** → 各年之和可能小于 `/map` 的总量计数
   （实测：关键词「腾讯」年度合计 11 家，/map 计数 19 家，差额即注册日期缺失的行）。该口径写在 `notes` 里。

**自测（2026-10-27，HTTP 200）**

| 入参 | years | 企业序列 values |
|---|---|---|
| 无过滤 | 2015–2026 | 12093,14029,13447,11943,11758,13030,13423,8940,7884,5349,3061,122 |
| 深圳市 2022–2024 | 2022–2024 | 4032,3658,**2628**（与库 join 计数逐位吻合） |
| 东莞市 2022–2024 | 2022–2024 | 1815,1636,1079（与深圳不同 → 地域过滤确已生效） |
| 南山区 2022–2024 | 2022–2024 | 715,620,492（区县维度生效） |
| `searchTerm=腾讯` | 全区间 | 1,4,2,2,0,1,0,0,0,1,0,0 |
| `enabledFactorKeys=[scholar]` | 全区间 | series=[] + notes（不含企业 → 无序列） |

**前端接线**：`api/situation/index.ts` 的 `fetchSituationCompare` 由「未上线端点诚实空态」切回 `post('/compare')`；
至此该 shim 只剩 timeline / events 两个端点。

## 2. 新增实现：`POST /display/v1/situation/influence`（C3 叶）

> **v1.2 重写说明**：v1.1 此处写的是简化结构 `{count, averageScore, items[]}`，与 `types/situation.ts` 冻结的 `InfluenceDataset` **不符**。按 U5（lumen 现实现为真源）修正如下，**前端仍零结构改动**。

- **请求体**：对齐前端 `SituationInfluenceParams`（`types/situation.ts`：`activeRegionKey` / `regionPaths` / `timeRange` / `selectedFieldValues` / `enabledFactorKeys` / `searchTerm`），不新增字段。
- **响应**：`InfluenceDataset`（逐字对齐 `types/situation.ts`）
  - `analyzableFactorCount: int`（有数据的要素卡数，当前为 1）
  - `cards[]: InfluenceCard[]` —— `{ factorType, factorLabel, count:int, averageScore:number, rank:int, rankScope, source, items: InfluenceItem[] }`
    - `items[]`：`{ factorType, name, score:number, rank:int, rankScope, regionKey }`，Top-N 高分企业（默认 50，score desc，同分按 `org_id` 稳定）
    - 只有 `enterprise` 一张卡：其余 10 要素无数据源，**不生成空卡**（不造空 UI），与其在 `/map` factorItems 里 count=0 的呈现约定不同，按 cards 结构语义处理
  - `defaultFactorType: string | null`（有卡时为 `enterprise`）
  - `totalCount: int`（= Σ card.count，demo `buildInfluenceAnalysisDataset` 口径）
- **数据源**：`display` Feign → `GET /v1/element/enterprise/influence`（`limit/city/district/name`）→ `ads.enterprise_score` join `dwd.enterprise_base`（join 显式 `COLLATE`）。
- **过滤器支持矩阵（必须诚实声明，不静默假装已过滤）**

| 入参 | 是否生效 | 依据 |
|------|---------|------|
| `searchTerm` | ✅ 生效 | 企业名 `LIKE '%term%'` |
| `activeRegionKey` | ✅ 部分 | 以「市」结尾→城市过滤；以「区/县」结尾→区县过滤；其余值忽略 |
| `enabledFactorKeys` | ✅ 生效 | 非空且不含 `enterprise` → 企业要素出局，返回空 cards |
| `timeRange` / `selectedFieldValues` / `regionPaths` | ❌ **未应用** | 分数表无注册年份/领域落筛列；由前端如实呈现，后端不撒谎、不静默忽略 |

- **口径注释（必须落在代码注释与 handoff）**：正式指标 `M_INNOV_ENTERPRISE_INFLUENCE` 算法未上线（D4=mock），本端点为 `enterprise_score` **占位实现**，不等价正式指标口径，也不触发任何就绪度翻转。
- **序列化铁律**：`count/rank/totalCount/analyzableFactorCount` 为 int（禁 Long/BigDecimal 直出），`score/averageScore` 为 number。

## 3. 变更：`POST /display/v1/situation/map`（C1/C2 叶）

- `objectPoints[]`（v1.0 恒空）改为真实企业点位：
  - 字段沿用 v1.0：`key, parentRegionKey, objectTypeKey('enterprise'), value, level, coordinates, detail{...}`
  - `detail.properties` / `relatedElements` 结构沿用 demo 种子语义（`types/situation.ts` 冻结，不改）
  - 来源：`ads.enterprise_score` Top-N（join `enterprise_base` 经纬度）；**脏坐标（空/越界）剔除不出点**；数量与 N 的口径写入代码注释
- `objectPointsEmptyReason`：仅 Feign 降级（element 不可达）时保留并填 UNREACHABLE 语义；正常路径不再出现。
- 其余字段（factorItems/regions/cascade/viewport）不变；其余 10 要素 count=0 为**期望值**，不造假。

> **C1 实现备注（2026-10-27，`SITUATION-ENT-C1-L01`；不属契约变更，不 bump 版本）**
> - 数据来源端点：`GET /v1/element/enterprise/points`（element 侧，`@Inner` + display 侧 `@NoToken` 配对），
>   Top-N 默认 **100 / 硬顶 500**（工程口径，非业务口径），支持 `city` / `district` 过滤，排序 `score_total DESC`。
> - `key` = `object-{org_id}`；`parentRegionKey` 填**行政区划中文名**（demo 种子为拼音 slug，两级联动差异由 C2/D1 消化，不算 bug）。
> - `relatedElements` **只含 `patents`**（源 `patent_grant_count` 授权专利，0–325 / 均值 40.58）；
>   原 `patent_valid_count` 在 DWD 里**整列 NULL**，故不采用；当源值为 NULL 时 `relatedElements` 整体省略——**未知 != 0**。
>   前端若依赖 papers/projects/achievements，属 demo 种子语义、本管线无数据源，不在 объектов 层补全。

## 4. 空态约定（U4：全局 `USE_MOCK=false`）

| 端点 | 后端状态 | 前端表现 |
|------|---------|---------|
| map / overview / influence | lumen 已实现 | 真实数据 |
| cluster / compare | lumen 已实现（C5 / C6 叶） | 真实数据；仅 `enterprise` 有数据源（cluster 只有企业样本、compare 只有企业年度序列），其余要素不伪造 |
| timeline / events | **无后端 → 404** | api 层收敛为诚实空态（对应区块空、无报错弹窗、不白屏）；错误处理**只许在 `src/api/`** 实现，不动视图 |
| map.objectPoints（element 降级时） | 200 + 空 + emptyReason | 空态 |

## 5. 冻结清单（C3 叶后不得再改，改则 bump v1.2 走变更记录）

1. influence 响应字段名与类型（§2）
2. objectPoints 字段与脏坐标剔除规则（§3）
3. 404 空态收敛位置（§4）

## 7. 变更：`/influence` 地域入参与 `/cluster` 入出参（v1.4，2026-10-28）

> **动机**：走查分析发现两个「筛选框勾了、数据一动不动」的静默忽略点。两处都是
> **同一类根因：端点各认一半入参，没有并入唯一翻译层 `scopeOf`**。修复方式是并入，不是"多认一个字段"。

### 7.1 `/influence`：地域入参并入 `scopeOf`

| 入参 | 修复前 | 修复后 |
|------|--------|--------|
| `regionPaths`（地域范围级联） | ❌ **被忽略**（页面主地域筛选，勾了不动） | ✅ 生效 |
| `activeRegionKey`（地图点选 / 关键词候选） | ✅ 生效 | ✅ 生效（与 `regionPaths` 同源，解析顺序 `regionPaths` → `activeRegionKey`） |
| `searchTerm` / `timeRange` | ✅ 生效 | ✅ 生效（此前地域是端点自己解析、年份却借 `scopeOf`，同一端点两套来源 = 一半生效的根源） |
| `selectedFieldValues`（学科领域） | ❌ 不参与 | ❌ 不参与（企业主表无领域列，诚实声明） |

自测（2026-10-28，本地 element :7082 + display :7099，HTTP 200）

| 入参 | cards | count | avg |
|---|---|---|---|
| `{}` | 1 | **189,115** | 37.78 |
| `regionPaths=[["深圳市"]]` | 1 | **95,600** | 37.47 |
| `regionPaths=[["深圳市","南山区"]]` | 1 | **16,039** | 37.78 |
| `activeRegionKey=南山区` | 1 | **16,039** | 37.78（与级联一致 → 同源已成立） |
| `searchTerm=腾讯` | 1 | **19** | 38.32 |

### 7.2 `/cluster`：废弃 `focusRegionKeys`，改收显式筛选入参

**⚠️ 废弃 `focusRegionKeys` 的理由（必须写清，否则后来人会加回来）**：

它是前端「当前地图上的区域列表」，不是用户选中的范围。无筛选时列表是 30 个城市，
后端 `firstRegionKey()` 取首项 = 数据量最大的城市 → **聚类样本被静默缩到一个市**，
而页面文案只写「当前筛选范围」。教训：**列表型入参不是范围选择**——
宁可不过滤，也别拿一个没人选过的默认值偷偷过滤。

| 入参 | 修复前 | 修复后 |
|------|--------|--------|
| `focusRegionKeys` | 取首项当范围（**静默缩样**） | **废弃**（后端不再消费，前端不再传） |
| `regionPaths` / `activeRegionKey` | ❌ 未传 | ✅ 生效（走 `scopeOf`，与另四个端点同源） |
| `searchTerm` | ❌ 固定传 `null`（聚类不响应关键词） | ✅ 生效 |
| `timeRange` | ❌ 未传 | ✅ 生效（默认随页面时间范围 2020–2026） |

**响应新增（可选字段，纯增量）**：`scopeLabel: string` —— 当前筛选下样本的真实范围，
无筛选时为「全量样本」，与 `/overview` 的 `scopeLabel` 同口径。用途：让聚类 Tab 标注这批样本的来源，
否则用户对着不知来源的散点做判断。

自测（2026-10-28，HTTP 200，`startYear/endYear` 为前端默认 2020–2026）

| 入参 | items | scopeLabel | 涉及地域数 |
|---|---|---|---|
| `{}` | 200 | 全量样本 | **6**（修复前恒为 1） |
| `timeRange=2020-2026` | 200 | 注册年：2020-2026 | 4 |
| `regionPaths=[["深圳市"]]` | 200 | 城市：深圳市 · 注册年：2020-2026 | 1 |
| `regionPaths=[["深圳市","南山区"]]` | 200 | 区县：南山区 · 注册年：2020-2026 | 1 |
| `activeRegionKey=广州市` | 200 | 城市：广州市 · 注册年：2020-2026 | 1 |
| `searchTerm=腾讯` | **2** | 关键词：腾讯 · 注册年：2020-2026 | — |
| 深圳市 + 腾讯 | **2** | 城市：深圳市 · 关键词：腾讯 · 注册年：2020-2026 | — |

> 注：`cluster` 的 200 条是**当前筛选范围内的影响力 Top-N**（工程口径），
> 不是全库前 N；四维度中 `growth` 仍为**空桶 + emptyReason**（`revenue_growth_rate` 整列 NULL）。

### 7.3 前端改动面（视图零 diff）

| 文件 | 改动 |
|---|---|
| `src/types/situation.ts` | `SituationClusterParams` 用 `regionPaths`/`activeRegionKey`/`searchTerm`/`timeRange` 替换 `focusRegionKeys`；`ClusterDataset` 新增可选 `scopeLabel` |
| `src/views/situation/overview/index.vue` | cluster 请求改传上述字段 + watch 依赖加地域/关键词/时间；聚类范围文案改用后端 `scopeLabel` |
| `src/mock/modules/situation.ts` | 双轨同语义（地域/关键词过滤 + 返回 `scopeLabel`），保证 `USE_MOCK=true` 可切回 |

