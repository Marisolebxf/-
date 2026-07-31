# Wireframe-ENT-KEYENT.md

> **模块**：重点企业分析（E-20 / E-21 / E-22）
> **版本**：v2.0
> **对应 IA / USM / TRACE**：`IA-ENT-KEYENT.md` / `USM-ENT-KEYENT.md` / `TRACE-ENT-KEYENT.yaml`
> **阶段**：Track-MS 核心产品包；通过 UX/V1 首轮后作为门 1 PDR 输入
> **权威入口**：`/enterprise-center/key-enterprise-analysis`

## 1. Frame 清单

| Frame ID | Frame | 触发入口 | 目的 | review_mounts |
| --- | --- | --- | --- | --- |
| F-KEYENT-00 | 页面壳与分析类型 | 任一入口 | Tab 前置、替换专属输入、共享数据更新时间 | `ENT-KEYENT-F00-DATA-TRACE`、`ENT-KEYENT-F00-INPUT-OWNERSHIP` |
| F-KEYENT-01 | 类型与区域分析 | `view=type` | 按范围/产业/类型理解总体结构和空间分布 | `ENT-KEYENT-F01-TITLE-REQ`、`ENT-KEYENT-F01-TYPE-METRIC`、`ENT-KEYENT-F01-TYPE-PENDING`、`ENT-KEYENT-F01-GEO-REQ`、`ENT-KEYENT-F01-GEO-PENDING` |
| F-KEYENT-02 | 企业清单宽抽屉 | 区域洞察次级动作 | 查看当前范围企业并加入对比篮 | `ENT-KEYENT-F02-SOURCE-REQ` |
| F-KEYENT-03 | 分析对象上下文 | `view=domain` 或系统对比篮分发 | 以单一紧凑状态行确认 1～N 家企业及来源并原位打开对比篮 | `ENT-KEYENT-F03-OBJECT-REQ`、`ENT-KEYENT-F03-OBJECT-PENDING` |
| F-KEYENT-04 | 领域布局概览 | 对象校验成功 | 展示确定性领域摘要、企业覆盖和跨领域布局 | `ENT-KEYENT-F04-TITLE-REQ`、`ENT-KEYENT-F04-DOMAIN-METRIC`、`ENT-KEYENT-F04-DOMAIN-PENDING` |
| F-KEYENT-05 | 领域识别依据 | 点击关系或证据 | 核验业务/产品/技术证据 | `ENT-KEYENT-F05-EVIDENCE-REQ` |

## 2. Frame F-KEYENT-00：页面壳与输入所有权

### 2.1 线框图

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ [类型与区域分析] [领域分布分析]                数据更新至 YYYY-MM-DD  [◉] │
├────────────────────────────────────────────────────────────────────────────┤
│ view=type 专属输入：区域范围 │ 时间 │ 产业 │ 企业类型 │ 重置               │
│                 或                                                         │
│ view=domain 对象上下文：来源 │ 数量 │ 单行摘要 │ 原位打开对比篮             │
├────────────────────────────────────────────────────────────────────────────┤
│ 当前分析视图                                                               │
└────────────────────────────────────────────────────────────────────────────┘
```

`[◉]` 表示统一评审图标挂点，仅评审模式出现；业务模式不存在该节点与占位。

### 2.2 规则

| 项目 | 类型与区域分析 | 领域分布分析 | 是否共享 |
| --- | --- | --- | --- |
| 分析对象 | 条件命中的企业群体 | 明确选择的 1～N 家企业 | 否 |
| 输入 / 上下文 | 区域、时间、产业、企业类型 | 只读企业对象上下文、来源、原位调整动作 | 否 |
| 数据更新时间 | 页面级显示一次 | 页面级显示一次 | 是 |
| 内部追溯 | 评审图标浮层 | 评审图标浮层 | 评审模式共享 |

- Tab 必须位于输入区之前；切换 Tab 时整体替换输入区。
- 两个 Tab 各自缓存本次会话状态，但不相互改写。
- 业务模式没有普通“数据说明”入口；`calc_batch_id`、Mock、算法版本、来源系统只在评审浮层、审计或导出元数据中存在。
- 业务模式 DOM 禁止出现：产品解释、尚未接入、正式指标、Mock、GAP、Q010/Q012/Q013、`calc_batch_id`。

## 3. Frame F-KEYENT-01：类型与区域分析

### 3.1 线框图（中屏）

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 类型与区域分析 [REQ]                                                       │
│ 区域                 时间              产业          企业类型             │
│ [全国热门城市/深圳⌄] [近3年 2023—2026] [多选⌄]       [多选⌄]              │
├────────────────────────────────────────────────────────────────────────────┤
│ 匹配企业数 │ 覆盖企业类型数 │ 覆盖区域数                                  │
├─────────────────────────────────────────────────────┬──────────────────────┤
│ 重点企业空间分布 [REQ]           [地图视图][列表视图] │ 区域洞察             │
│ [范围根 / … / 当前区域] [返回上一级]                 │ 当前：深圳市   50家  │
│                                                     │ [查看企业清单（50）] │
│                                                     │ 企业规模 / 区域占比  │
│ 地图：聚合点 → 下钻 → 区县 → 企业点位               │ 当前区域类型结构     │
│ 或                                                  │                      │
│ 列表：固定名称列｜中间属性横滑｜固定操作列           │                      │
│       [在地图中查看] [查看画像]  每页 10 条           │                      │
│                                                     │ 同级区域分布*        │
│                                                     │ TOP N / 数量 / 占比  │
│ 图例：企业数量强度                                  │ [区域×类型矩阵]*     │
├─────────────────────────────────────────────────────┴──────────────────────┤
│ * 仅当真实同级区域数 ≥ 2 时出现；否则本区不占位                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 字段与指标

| 名称 | 来源 | 展示位置 | metric_id / 状态 |
| --- | --- | --- | --- |
| 区域范围 | 行政区划维表 | 专属输入区唯一 `RegionSelect` | context |
| 时间 | 页面数据上下文 | 专属输入区 | context |
| 目标产业 | 产业领域字典 | 专属输入区 | filter |
| 企业类型 | 资质/荣誉/规模/上市映射 | 专属输入区 | Q010 |
| 匹配企业数 | 条件后企业去重 | 顶部 KPI | `M_ENT_TYPE_MATCH_COUNT` |
| 覆盖企业类型数 | 当前结果中企业数大于 0 的类型标签去重数 | 顶部 KPI | 派生自 `M_ENT_TYPE_COUNT` |
| 覆盖区域数 | 顶部范围下一层级中企业数大于 0 的行政区域去重数 | 顶部 KPI | 派生自 `M_ENT_REGIONAL_COUNT` |
| 当前区域企业数量 | 当前地图区域聚合 | 区域洞察 | `M_ENT_REGIONAL_COUNT` |
| 当前区域企业类型结构 | 当前地图区域内各类型企业数及占比 | 区域洞察 | `M_ENT_TYPE_COUNT` / `M_ENT_TYPE_RATIO` |
| 区域企业规模 | 当前区域规模分布 | 有数据时在洞察/同级排行 | `GAP-KEYENT-REGIONAL-SCALE` |
| 区域企业占比 | 当前区域数 / 同层匹配企业数 | 有数据时在洞察/同级排行 | `GAP-KEYENT-REGIONAL-RATIO` |
| 企业密度 | 区域企业数 / 确认分母 | 口径闭合后 | `M_ENT_REGIONAL_DENSITY`（Q012） |
| 集聚指数 | 已确认算法 | 口径闭合后 | `M_ENT_AGGLOMERATION_INDEX`（Q012） |

业务模式降级：缺少规模、占比、密度或集聚指数时省略对应字段或显示“暂无数据”，不出现解释技术原因的 Alert，不用高企占比替代区域企业占比。

企业类型允许一企多标签。“覆盖企业类型数”只计算被覆盖的标签类别，不把各类型当作互斥分组；顶部不计算“主导类型企业数 / 主导类型占比”，类型数量和占比只在当前区域企业类型结构中展示。

类型分析专属输入采用字段标签在上、控件在下的上下结构；区域、时间、产业、企业类型四组条件仍在中屏横向排列，筛选语义和联动逻辑不变。

### 3.3 区域状态模型

```yaml
top_region_scope:
  owner: type_view_filter_bar
  editable: true
  effect_on_change: reset_map_to_scope_root
map_browse_state:
  owner: key_enterprise_map
  editable_by: [map_region_click, list_region_action, map_breadcrumb, map_back]
  allowed_within: top_region_scope
  writes_back_to_top_region_scope: false
  affects: [map_viewport, list_rows, selected_region, region_insight, enterprise_list_scope]
distribution_view:
  default: map
  values: [map, list]
  shares_browse_state: map_browse_state
  replaces: left_main_stage_only
```

- 页面内只允许一个可编辑区域选择器。
- 顶部范围变化会重置地图；地图浏览不反写顶部。
- 地图面包屑显示局部路径，不冒充顶部筛选值。
- 地图/列表切换只替换左侧主工作区，不改变面包屑、当前区域、已选类型或右侧区域洞察。

### 3.4 地图展示与下钻

| 当前地图层 | 地图对象 | 点击结果 | 同级洞察对象 |
| --- | --- | --- | --- |
| 国家 | 省级聚合 | 进入省 | 当前国家内的省；至少 2 个才比较 |
| 省 | 城市聚合 | 进入市 | 当前省内的城市；至少 2 个才比较 |
| 市 | 区县聚合 | 进入区县展示层 | 当前市内区县；属产品解释 |
| 区县 | 企业点位 | 选中企业/查看轻量信息 | 不新增区县指标验收层 |

- Bid 直接需求的分析层级为国家、省、市；区县与企业点位只深化地图展示。
- `DEC-KEYENT-DISTRIBUTION-DUAL-VIEW-20260723`：空间分布默认地图，可切换当前层级同一批对象的列表；切换不改变 `map_browse_state` 或右侧区域洞察。列表每页 10 条，名称首列固定、操作尾列固定，中间属性列只在表格内部横向滚动。
- 地图复用企业总览的浅色底图、聚合点、企业点位、选中反馈、缩放/复位/全屏工具，不复用企业总览的业务指标或“进入企业查询”。
- 地图有效高度：1440×900 视口下不低于 520px；大屏时填充 Tab、输入区和 KPI 之外的剩余可用高度。
- 主区建议 17～18/24 栅格，洞察区 6～7/24；两区等高。
- 列表与地图读取同一当前层级对象：国家/省/市显示下一级区域聚合行，区县显示企业行。地域行“在地图中查看”调用地图同一下钻状态并切换地图；企业行同名动作选中企业点位，企业“查看画像”打开当前页统一宽幅企业详情 Drawer。
- 默认 `map`；不跨会话持久化，不把企业清单 Drawer 合并进列表视图。

### 3.5 区域洞察

| 区块 | 显示条件 | 行为 |
| --- | --- | --- |
| 当前区域概览 | 始终 | 展示区域名、企业数和已接入有效字段 |
| 企业清单动作 | 当前范围企业数 > 0 | 标题区紧凑次级动作，文案含范围/类型与数量 |
| 当前区域类型结构 | 有类型聚合 | 点击只更新类型上下文，不打开列表 |
| 同级区域分布/排行 | `sibling_count >= 2` | 全国比省、省比市；明确比较集合 |
| 区域×类型矩阵 | `sibling_count >= 2` 且有真实矩阵数据 | 侧栏切换或地图下方折叠，不固定占位 |

- 删除独立固定的“区域结构比较”卡片和单行表。
- 只有广东省→深圳市单链数据时，不显示同级排行或矩阵。
- “查看企业清单（N）”不是整个洞察卡片的总结按钮，不使用全宽主色按钮。
- 类型结构图下不显示“当前类型：全部重点企业类型 / 当前类型：某类型”状态行；顶部企业类型筛选不在洞察区复述，图表局部选择由“查看某类型清单（N）”反馈。

### 3.6 交互

| 触发 | 页面行为 | 禁止行为 |
| --- | --- | --- |
| 修改顶部区域 | 重置地图至新范围根并刷新结果 | 保留越界局部选择 |
| 点击地图区域 | 在允许范围内下钻，更新洞察 | 反向修改顶部区域；直接打开企业列表 |
| 切换地图/列表 | 只替换左侧主工作区，保留浏览层级和洞察 | 重置面包屑；隐藏右侧洞察 |
| 点击列表地域“在地图中查看” | 复用地图区域点击下钻、切换地图并更新洞察 | 建立第二套列表层级状态 |
| 点击列表企业“在地图中查看” | 切换地图并选中对应企业点位 | 新增行政层级；反写顶部范围 |
| 点击列表企业“查看画像” | 在当前页打开统一宽幅企业详情 Drawer，关闭后保留列表页码与层级 | 跳转离开页面；把列表视图替代为企业清单 Drawer |
| 点击企业点位 | 选中并显示轻量信息 | 无提示替换整页 |
| 点击类型结构/矩阵 | 更新当前分析上下文 | 直接打开企业清单；把缺失当 0 |
| 点击“查看企业清单（N）” | 打开 F-KEYENT-02 宽 Drawer | 使用全宽主按钮或跳转离开分析页 |
| 切换到领域分析 | 替换为领域专属输入 | 自动带入全部匹配企业 |

### 3.7 状态

| 状态 | 表现 |
| --- | --- |
| 加载 | 输入区保持；KPI、地图、洞察显示稳定骨架 |
| 空数据 | 显示当前条件无匹配企业，不自动放宽 |
| 下级无数据 | 地图保留返回路径，局部提示暂无数据 |
| 同级不足 | 不渲染排行/矩阵且不留空白容器 |
| 企业点位不可定位 | 保留聚合数，点位层提示暂无可定位企业 |
| 错误 | 标明失败区块和重试入口，内部批次只写日志 |
| 无权限 | 隐藏敏感明细，保留返回/申请入口 |

## 4. Frame F-KEYENT-02：企业清单宽抽屉

```text
┌──────────────────── 深圳市企业清单 · 50家（右侧宽 Drawer）──────────────┐
│ 来源：区域范围 / 地图当前区域 / 产业 / 类型 / 时间 [REQ]                │
├──────────────────────────────────────────────────────────────────────────┤
│ 搜索企业名称、统一社会信用代码、产业或区域                               │
│ □ 企业名称 │ 类型 │ 地域 │ 产业 │ 规模 │ 查看画像                     │
├──────────────────────────────────────────────────────────────────────────┤
│ [全选当前结果] 已选 N 家          [打开对比篮] [加入对比篮]             │
└──────────────────────────────────────────────────────────────────────────┘
```

- 来源摘要必须区分顶部区域范围和地图当前区域。
- 全选仅对当前清单结果生效；存在搜索词时只选中/取消当前搜索结果，全选框支持未选、部分选中和全选三态。
- 全选控件放在底部操作栏并与批量动作同组；选择数量只显示一次“已选 N 家”，内容区不再重复显示“当前 N 家”。
- 关闭后恢复顶部条件、地图层级/选中、洞察状态和滚动位置。
- 加入对比篮汇总成功、重复、超限、无效数量；不把加入成功当作领域分析完成。

## 5. Frame F-KEYENT-03：分析对象上下文

```text
有对象（约 64px）
┌──────────────────────────────────────────────────────────────────────────┐
│ [REQ] 来自对比篮 · 5 家  企业 A、企业 B、企业 C 等 5 家                  │
│                                              [打开对比篮调整对象]         │
└──────────────────────────────────────────────────────────────────────────┘

无对象（同一位置、同一高度）
┌──────────────────────────────────────────────────────────────────────────┐
│ 尚未选择分析对象                                      [打开对比篮]        │
└──────────────────────────────────────────────────────────────────────────┘
```

- 输入对象为去重后的 `enterprise_codes[]`，最少 1 家。
- 本 Frame 是只读对象上下文，不提供企业下拉选择器、可删除 Tag、逐项移除或“返回对比篮”。对象选择、增删与勾选归 `ENT-COMPARE`。
- 有对象时显示“来自对比篮 · N 家”、单行企业名称摘要和“打开对比篮调整对象”；摘要溢出以“等 N 家”收纳，不增加行高。
- 无对象时只显示“尚未选择分析对象”和唯一主动作“打开对比篮”；F-KEYENT-04/F-KEYENT-05 不渲染，不再显示第二个空态 CTA。由此入口展开对比篮后，“选择分析任务”预选“领域分布分析”，但仍须点击“下一步：前往配置”才分发。
- 两个动作均通过 `open_compare_basket=1` 在当前页面原位展开系统对比篮，不跳转 `/enterprise-center/basket`，不新建页内 Drawer/Modal 选企器。
- 对象校验中保持 64px 高度并局部 loading；部分对象无效时移除无效编码、汇总提示并继续；全部无效时回到无对象态。
- 再次成功分发以本次 `analysis_type` 和 `enterprise_codes[]` 更新当前配置草稿并收起对比篮；不得覆盖已启动任务或报告快照。

## 6. Frame F-KEYENT-04：领域布局概览

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 领域布局概览 [REQ]                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ 已覆盖领域 │ 涉及企业 │ 跨领域企业 │ 识别依据                           │
├─────────────────────────────────────┬────────────────────────────────────┤
│ 企业领域覆盖                        │ 跨领域布局                         │
│ 企业 A ● ● ○                        │ 企业—领域—证据关系                 │
├─────────────────────────────────────┴────────────────────────────────────┤
│ 重点领域分布：产业领域｜涉及企业｜识别依据｜代表企业｜查看识别依据       │
└──────────────────────────────────────────────────────────────────────────┘
```

| 业务摘要 / 指标 | metric_id / 计算 | 业务可见性 |
| --- | --- | --- |
| 已覆盖领域 | `M_ENT_DOMAIN_COVERAGE_COUNT` | 可见 |
| 涉及企业 | 当前 `enterprise_codes[]` 去重计数 | 可见；输入摘要，不解释为领域算法指标 |
| 跨领域企业 | 当前关系集中关联至少 2 个领域的企业去重计数 | 可见；确定性关系摘要 |
| 识别依据 | 当前企业—领域关系下证据条目计数 | 可见；确定性关系摘要 |
| 覆盖广度 | `M_ENT_DOMAIN_COVERAGE_BREADTH` / Q013 | 仅评审模式，业务模式不占位 |
| 参与深度 | `M_ENT_DOMAIN_COVERAGE_DEPTH` / Q013 | 仅评审模式，业务模式不占位 |
| 多元化指数 | `M_ENT_DIVERSIFICATION_INDEX` / Q013 | 仅评审模式，业务模式不占位 |

- KPI、矩阵、图谱和领域列表必须使用同一对象集。
- 跨领域布局图例直接使用企业节点与产业领域节点的实际类别色，不得出现图例色与节点色脱节。
- 重点领域分布使用分页表格；首列“产业领域”和尾列“操作”固定，中间列在容器内横向滑动，禁止造成页面级横向滚动。
- 点击矩阵单元或领域节点打开 F-KEYENT-05；无证据时不显示“已覆盖”强结论。
- `DEC-KEYENT-DOMAIN-PRODUCT-LANGUAGE-20260723`：业务标题不得直接使用 Frame 名、组件名或数据结构名。
- Q013 未闭合的覆盖广度、参与深度和多元化指数只在指标定义与 Pending 中保留，**业务模式不占位**；不得用连续“暂不可用”卡片占据业务主视图。
- 业务模式不显示 Q013、临时公式或 Mock 字样；评审模式通过指标挂点说明。

“企业详情”在当前页打开与深圳企业现状分析一致的完整企业详情宽幅抽屉，不跳转企业画像页。进入企业评估或风险洞察时，动作必须携带当前关系所属企业编码、`source=key-enterprise-analysis`、`source_tab=domain` 和当前页面 `return_to`；目标页以传入对象初始化，不得展示默认对象状态。

## 7. Frame F-KEYENT-05：领域识别依据

```text
┌──────────────────────── 领域识别依据 Drawer ───────────────────────────┐
│ 为什么识别为「集成电路」                                                │
│ 企业 A                                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ 业务范围 │ 摘要 │ 来源位置 │ 时间/版本                                 │
│ 产品线   │ 产品名称 │ 领域标签 │ 来源位置                              │
│ 技术/专利│ 摘要 │ 标签 │ 来源位置                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ [查看企业画像] [进入其他研判]                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

- 映射状态持久化使用 `pending_source / mapped / verified`；业务 UI 可映射友好文案，不得过载状态表示 Mock 或降级。
- 展示来源位置、摘要、证据类型和版本；来源待确认时不生成强结论。

## 8. 对比篮跨模块契约

```text
选择分析任务
├─ 重点企业领域分布分析（1～N 家）
├─ 企业评估
└─ 风险洞察
```

- 不提供“重点企业类型分析”篮内任务：E-21 输入是范围条件，不是篮内指定对象。
- 成功分发后对比篮收起为系统入口；目标页 F-KEYENT-03 是唯一对象调整入口并在原位重新展开浮层。
- 路由与会话参数以 IA §6 为准，权威字段为 `analysis_type`、`enterprise_codes[]` 与 `return_context_id`。
- ENT-COMPARE v2.8 已登记“重点企业分析 → 领域分布分析”，正式使用 `analysis_type=key-enterprise-domain`，并以 `replace_domain_configuration_draft` 应用当前勾选对象；本节已授权进入 V1 实现。

## 9. 响应式与视觉约束

- **screen_tier**：仅 `medium_1440_1920`；科技专题服务系统不声明 `small_reflow`。
- **1920 / 1680 / 1440**：Tab→专属输入或对象状态行→主工作区；F-KEYENT-03 保持约 64px，企业摘要单行截断，动作始终可见且不产生页面级横向滚动。
- **组件**：顶部区域使用共享 `RegionSelect`；地图内部只用面包屑/返回，不放第二个级联选择器或 Radio Group。
- **评审模式**：所有追溯使用统一评审 icon/marker；禁止显示“产品解释”文字按钮。
- **评审挂点归位**：同一区块挂点集中在标题之后；不得散落在 KPI 右下、地图面包屑、内容区、业务动作或 Drawer Footer。产品解释并入需求追溯子模块，不设独立挂点。
- **业务模式**：评审节点不进入 DOM，不保留空图标、空容器或技术 Alert。
- **禁止**：不混入 E-25/E-33，不新增导出、权重编辑、企业排名或智能推荐。

## 10. review_trace_contract

```yaml
review_trace_contract:
  - mount_id: ENT-KEYENT-F00-DATA-TRACE
    frame_id: F-KEYENT-00
    host_label: 页面共享标题行（数据更新时间后）
    marker_type: mock_badge
    source_relation: product_interpretation
    trace_refs: [PI-KEYENT-05, DEC-KEYENT-REVIEW-BUSINESS-BOUNDARY-20260722]
    required_payload: [display_updated_at, calc_batch_id, source_systems, mock_until, algorithm_version, planned_tier]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F00-INPUT-OWNERSHIP
    frame_id: F-KEYENT-00
    host_label: 页面共享标题行（分析类型 Tab 后）
    marker_type: requirement_trace
    source_relation: product_interpretation
    trace_refs: [PI-KEYENT-09, DEC-KEYENT-TAB-INPUT-OWNERSHIP-20260722]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F01-TITLE-REQ
    frame_id: F-KEYENT-01
    host_label: 类型与区域分析标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-01, E-20, E-21]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F01-TYPE-METRIC
    frame_id: F-KEYENT-01
    host_label: 类型与区域分析标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-01]
    required_payload: [metric_id, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F01-TYPE-PENDING
    frame_id: F-KEYENT-01
    host_label: 类型与区域分析标题
    marker_type: pending_badge
    source_relation: direct_requirement
    trace_refs: [Q010]
    required_payload: [pending_ref, owner, temporary_default, deadline]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F01-GEO-REQ
    frame_id: F-KEYENT-01
    host_label: 重点企业空间分布标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-02, E-21]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F01-GEO-PENDING
    frame_id: F-KEYENT-01
    host_label: 重点企业空间分布标题
    marker_type: pending_badge
    source_relation: direct_requirement
    trace_refs: [Q012, GAP-KEYENT-REGIONAL-SCALE, GAP-KEYENT-REGIONAL-RATIO]
    required_payload: [pending_ref, owner, temporary_default, deadline]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F02-SOURCE-REQ
    frame_id: F-KEYENT-02
    host_label: 企业清单 Drawer 标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-02, E-21]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F03-OBJECT-REQ
    frame_id: F-KEYENT-03
    host_label: 分析对象上下文状态行
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-03, US-KEYENT-04, E-22, PI-KEYENT-18, DEC-KEYENT-COMPARE-INPLACE-20260731]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F03-OBJECT-PENDING
    frame_id: F-KEYENT-03
    host_label: 分析对象上下文状态行
    marker_type: pending_badge
    source_relation: product_interpretation
    trace_refs: [US-KEYENT-04]
    required_payload: [unresolved_count, resolution, open_mode, object_selection_owner]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F04-TITLE-REQ
    frame_id: F-KEYENT-04
    host_label: 领域布局概览标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-03, E-22]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F04-DOMAIN-METRIC
    frame_id: F-KEYENT-04
    host_label: 领域布局概览标题
    marker_type: metric_spec
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-03]
    required_payload: [metric_id, definition, formula, source_tables, source_systems, update_freq, version]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F04-DOMAIN-PENDING
    frame_id: F-KEYENT-04
    host_label: 领域布局概览标题
    marker_type: pending_badge
    source_relation: direct_requirement
    trace_refs: [Q013]
    required_payload: [pending_ref, owner, temporary_default, deadline]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-KEYENT-F05-EVIDENCE-REQ
    frame_id: F-KEYENT-05
    host_label: 领域识别依据标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [US-KEYENT-05, E-22]
    required_payload: [source_location, source_summary, current_placement, source_relation, interpretation_submodules]
    review_mode: present
    business_mode: absent
```

### 10.1 挂载规则

- 所有 Frame 均有具名挂点；`mount_id` 唯一。
- 产品解释是需求追溯的子模块，收纳在对应 `requirement_trace` 的分组内容中；禁止定义或渲染独立 `review_copy` 挂点。
- 同一业务区块的挂点集中在标题旁，顺序为“需求追溯（含产品解释子模块）→ 指标说明 → Mock → Pending”；内容区、面包屑、操作区和 Drawer Footer 禁止挂载。
- `metric_spec` 只挂指标组；`pending_badge` 与 `mock_badge` 不合并。
- 业务模式移除全部挂点节点，不保留空图标、空白间距或技术 Alert。

## 11. metric_id 清单

| metric_id / gap_id | 状态 | 开放项 |
| --- | --- | --- |
| `M_ENT_TYPE_MATCH_COUNT` | 已登记 | — |
| `M_ENT_TYPE_COUNT` | 已登记；口径待确认 | Q010 |
| `M_ENT_TYPE_RATIO` | 已登记 | Q010 |
| `M_ENT_REGIONAL_COUNT` | 已登记 | Q012 |
| `M_ENT_REGIONAL_DENSITY` | 公式待闭合 | Q012 |
| `M_ENT_AGGLOMERATION_INDEX` | 公式待闭合 | Q012 |
| `GAP-KEYENT-REGIONAL-SCALE` | 正式 metric_id 待登记 | 何老师/辜少彬 |
| `GAP-KEYENT-REGIONAL-RATIO` | 正式 metric_id 待登记 | 何老师/辜少彬 |
| `M_ENT_DOMAIN_COVERAGE_COUNT` | 已登记 | — |
| `M_ENT_DOMAIN_COVERAGE_BREADTH` | 公式待闭合 | Q013 |
| `M_ENT_DOMAIN_COVERAGE_DEPTH` | 公式待闭合 | Q013 |
| `M_ENT_DIVERSIFICATION_INDEX` | 公式待闭合 | Q013 |

## 12. Demo 验收测试清单

- [ ] Tab 位于专属输入区之前；两个 Tab 条件集合不同。
- [ ] 页面只有一个可编辑区域选择器。
- [ ] 顶部区域变化重置地图；地图下钻不修改顶部区域。
- [ ] 地图具备局部面包屑/返回，并在区县层展示企业点位。
- [ ] 1440×900 下地图有效高度≥520px，主区与洞察区约 17～18:6～7。
- [ ] 同级区域数<2 时，排行和区域×类型矩阵不渲染且不占位。
- [ ] 企业清单使用紧凑次级动作打开宽 Drawer；关闭后上下文保持。
- [ ] 类型条件、地图、KPI、区域洞察和 Drawer 来源摘要结果一致。
- [ ] 顶部 KPI 为“匹配企业数 / 覆盖企业类型数 / 覆盖区域数”，且业务 DOM 不出现“主导类型企业数 / 主导类型占比”。
- [ ] 当前区域企业类型结构下方不出现“当前类型”重复状态行，图表点击后清单入口仍能反馈局部类型选择。
- [ ] 领域 KPI、矩阵、图谱只使用传入的 `enterprise_codes[]`。
- [ ] 无对象时仅 F-KEYENT-03 显示一次“打开对比篮”，结果区与页面其他位置不存在第二个 CTA。
- [ ] 有对象时 F-KEYENT-03 只显示来源、数量、单行摘要和“打开对比篮调整对象”；页内企业选择器、可删除 Tag 与“返回对比篮”均不存在。
- [ ] 两个对比篮动作均在当前页原位展开系统浮层；成功分发后面板收起并更新配置草稿。
- [ ] 领域业务使用紧凑分析对象上下文及“领域布局概览 / 企业领域覆盖 / 跨领域布局 / 重点领域分布 / 领域识别依据”，不平铺 Frame 或数据结构名称。
- [ ] Q013 未闭合指标在业务模式不渲染占位卡；评审模式仍可查看指标定义与 Pending。
- [ ] 业务模式内部禁用词计数为 0；评审挂点关闭后 DOM 和间距均不存在。
- [ ] 同一区块评审挂点全部位于标题旁；内容区、面包屑、操作区和 Footer 挂点计数为 0；独立 `review_copy` 挂点计数为 0，产品解释只存在于需求追溯子模块。
- [ ] 指针测试覆盖 RegionSelect、地图下钻、企业点位、清单 Drawer 和对比篮发起。

## 13. Wireframe 自检

- [x] 6 个 Frame 均对应 IA 节点、USM 路径和 TRACE 挂点。
- [x] Tab 前置与专属输入所有权已固化。
- [x] 顶部范围与地图局部下钻不再双向同步。
- [x] 地图主工作区、区域洞察和条件式同级比较已固化。
- [x] 固定区域比较表已移除，企业清单入口语义明确。
- [x] 业务/评审模式边界可自动化验收。
- [x] F-KEYENT-03 已归一为单一紧凑对象状态行，消除重复选企能力与双 CTA。
- [x] 直接需求、产品解释和产品增强分层；产品增强为 0。
