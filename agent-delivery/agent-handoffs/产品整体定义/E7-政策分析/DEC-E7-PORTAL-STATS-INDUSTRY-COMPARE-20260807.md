# DEC-E7-PORTAL-STATS-INDUSTRY-COMPARE · 概况产业锚点与同级对照

| 字段 | 值 |
|---|---|
| id | `DEC-E7-PORTAL-STATS-INDUSTRY-COMPARE-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认统一方案；同日续确认对照同级 / 地图无对照 / 产业级联） |
| approval_status | `approved` |
| source_relation | product_interpretation |
| 上级 | `DEC-E7-PORTAL-STATS-MAP-DENSITY-20260807` · `DEC-E7-PORTAL-NO-GLOBAL-FILTER-20260807` |
| Bid | P-17（§1.1.1.1.1.1.2.1） |

## 决策（已确认）

门户「政策概览」stats / map 共用查询上下文，承接招标「相关产业」数量/连续性与省/市「对比」：

### 1. 产业锚点
- 工具条挂 **产业 / 产业链左右 Cascader**（产业 → 细分环节；`industryChainCascadeOptions`）。
- **默认一个产业**（Demo：`合成生物`）；**禁止空选**。
- 可选到产业根或下钻细分环节；URL `industry=` 为 `合成生物` 或 `合成生物.生物制造`；KPI/Mock 口径取根节点。
- 「全部产业」**不**作为 V1 必选。

### 2. 地域 + 同级对照（仅 stats）
- 地域：四级 Cascader（无全球），`geo=` 决定档位。
- **对照候选与地域同级**（跨档切换清空 `compare`）：
  | 焦点档 | 对照候选 | 说明 |
  |---|---|---|
  | 全国 / 仅「区域」根 | 关闭 | 提示先下钻 |
  | 区域（京津冀/长三角/粤港澳） | 其他区域 | 同级区域对照 |
  | 省 | 其他省 | — |
  | 市 | 其他市 | — |
- **上限 5（不含当前焦点）**；焦点参与对照视图高亮。
- **对照仅概况统计（stats）工具条展示**；**政策地图不展示对照控件、不点选入对照**（地图只下钻列表）。

### 3. 筛选条 UI
- 标签上、控件下（对齐重点企业分析 `fieldLayout=stacked`）。
- **stats**：一行三列——产业 / 地域 / 对照。
- **map**：一行两列——产业 / 地域（无对照）。
- 区块标题去掉括号说明文案（如「点选标题查看画像」类提示）。

### 4. 呈现
- **stats**：KPI（数量、连续性、有效占比）+ 时序；同级对照区 Segmented：数量对比 | 连续性对比 | 时序叠加；条形对比按当前指标**从高到低**。
- **map**：同产业、同 geo 的件数热力；右侧政策列表可开画像抽屉、加入系统对比篮；列表分页默认 15。
- **rank**：不绑 industry/compare（见 `DEC-E7-PORTAL-RANK-PRESENTATION`）。

### 5. 边界
- 仍为概览**本地控件**，不上页级 ContextBar。
- 门户「对照」= 展示层横向对照，**不**发起专题分析；分析仍经系统对比篮。

### 6. URL
`?tab=overview&view=stats|map&industry={path}&geo={path}&compare={id1,id2}`  
`industry` / `geo` 在 stats↔map 共享；切到 map 可不展示但可保留 `compare` 参数（回 stats 仍可用）。

## scope_effect

不增删 Bid 叶子；补齐 P-17「相关产业」与同级数量·连续性对比合同；地图与对照解耦。
