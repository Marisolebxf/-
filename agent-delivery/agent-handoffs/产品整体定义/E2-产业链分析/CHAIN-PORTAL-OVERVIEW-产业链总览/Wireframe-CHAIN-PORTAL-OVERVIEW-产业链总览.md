# Wireframe-CHAIN-PORTAL-OVERVIEW-产业链总览

> **模块**：CHAIN-PORTAL-OVERVIEW / 产业链总览  
> **版本**：v1.5-portal-panorama-scope  
> **日期**：2026-08-06  
> **对应 IA**：`IA-CHAIN-PORTAL-OVERVIEW-产业链总览.md`  
> **对应 USM / TRACE**：`USM-CHAIN-PORTAL-OVERVIEW-产业链总览.md` / `TRACE-CHAIN-PORTAL-OVERVIEW-产业链总览.yaml`  
> **验收功能点索引（非原始需求编号）**：IC-30、IC-38～IC-41  
> **阶段**：Track-MS V1 高保真首轮输入；门 1 PDR 尚未闭合  
> **本版决策**：`DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806`；`DEC-CHAIN-PORTAL-OVERVIEW-PANORAMA-SCOPE-20260806`

## 1. 页面 / Frame 清单

> **v1.5 线框修订**：门户全景仅 IC-39（结构图 + 简介/企业列表）；无演进控件；无核心技术/科研机构/市场规模 Tab。F-01 选 L0；F-02 默认 L1 并可结构下钻；F-04 废止。

| Frame ID | Frame | 触发入口 | 用户目的 | 原始需求 / TRACE |
| --- | --- | --- | --- | --- |
| F-CHAIN-OV-01 | 当前 L0 产业上下文与 Tab 壳层 | 进入 `/industry-center/overview` | 确定唯一 L0 产业、切换 Tab、加入产业对比篮 | IC-38；US-CHAIN-OV-01/10；DEC-…-L0-L1 |
| F-CHAIN-OV-02 | 产业链全景默认态（L1） | 默认 Tab 或点击“产业链全景” | 看清 L0 下 L1 子链、上下游与语义关系 | IC-39、IC-30；US-CHAIN-OV-02；DEC-…-L0-L1 |
| F-CHAIN-OV-03 | 右侧对象详情面板 | 点击细分产业节点或关系 | 查看节点基础信息、简介、企业列表或关系摘要 | IC-39；US-CHAIN-OV-03；DEC-…-PANORAMA-SCOPE |
| F-CHAIN-OV-04 | ~~产业链演进态~~（废止） | — | 门户不承接；归专题全景 | DEC-…-PANORAMA-SCOPE |
| F-CHAIN-OV-05 | 产业资讯事件线 | 点击“产业资讯” | 筛选事件并追到原始报道 | IC-40；US-CHAIN-OV-05 |
| F-CHAIN-OV-06 | 产业整体概况 | 点击“产业整体概况” | 查看整链介绍和主体数量 | IC-41；US-CHAIN-OV-06 |
| F-CHAIN-OV-07 | 区域分布地图 / 列表态 | 操作整体概况地域卡片 | 浏览全球/全国空间布局 | IC-41；US-CHAIN-OV-07 |
| F-CHAIN-OV-08 | 产业发展历程 | 点击“产业发展历程” | 查看阶段、里程碑、影响和证据 | IC-38；US-CHAIN-OV-08 |
| F-CHAIN-OV-09 | 深圳产业现状 | 点击“深圳产业现状” | 查看深圳指标、各区布局和特色研判 | IC-38；US-CHAIN-OV-09 |
| F-CHAIN-OV-10 | 共享对比篮状态交接 | 点击顶部加入/移出产业对比篮 | 更新 `industry` 共享对象域；浮层由系统入口自行打开 | PI-CHAIN-OV-12；US-CHAIN-OV-10 |

## 2. F-CHAIN-OV-01：当前 L0 产业上下文与 Tab 壳层

### 2.1 结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 产业链总览                                                               │
│ [当前产业(L0)：可检索下拉________________________ ▾] [加入/移出产业对比篮] │
│  选项示例：集成电路 · 生物医药 · 新能源（与企业查询所属产业同口径）          │
├──────────────────────────────────────────────────────────────────────────┤
│ [产业链全景 需求追溯] [产业整体概况] [产业资讯] [产业发展历程] [深圳产业现状] │
├──────────────────────────────────────────────────────────────────────────┤
│ 当前 Tab Frame                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 当前 L0 产业 ID | string | 入口上下文 / 默认推荐配置 | 是 | `integrated-circuit` | — |
| 当前 L0 产业名称 | string | 产业目录（与企业所属产业同口径） | 是 | 集成电路 | — |
| 产业别名 | string[] | 产业目录 | 否 | 半导体、芯片 | — |
| 产业层级 | enum | 固定 | 是 | `L0` | — |
| 对比篮状态 | enum | 系统产业对比篮（`industry`） | 是 | `not_in_basket` | — |

### 2.3 交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 打开可检索下拉 | 仅列出产业层级 L0；按名称/别名匹配；加载态、无结果态；支持键盘上下选择与确认 | 不列出 L1 子链；不展示智能搜索、高级筛选或完整结果卡片 |
| 选择新 L0 产业 | 更新唯一 `industry_id`；保留当前 Tab；清除下钻栈、旧节点、关系、演进时间、详情 Tab 与筛选，右栏回空态 | 不混合两个 L0；不改写对比篮和已提交任务 |
| 切换 Tab | 只更换当前产业内容；各 Tab 不出现产业/子链选择器 | 不建立第二个对象上下文 |
| 权限 L0 点击加入对比篮 | 触发登录并保留 `return_url`、当前 `industry_id`、Tab 和页面上下文 | 不创建匿名篮；不先行改变按钮状态 |
| 权限 L1 及以上点击加入对比篮 | 加入当前 L0 `industry_id`，按钮变为“移出产业对比篮”，页面不跳转 | 不同时创建“关注”状态；不重置当前内容 |
| 点击移出对比篮 | 仅从篮中移除当前 L0 产业 | 不切换当前产业 |
| 需要查看全局对比篮 | 用户自行操作系统悬浮入口；总览不产生打开动作 | 不在总览重复提供打开按钮，不写入 `open_compare_basket`，不渲染本模块自建 Drawer |

### 2.4 状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 默认 | 当前 L0 有效、默认全景 Tab、按钮反映真实篮状态 | 浏览或切换 |
| 无入口对象 | 加载后台配置的默认推荐 L0 产业，并显示轻量说明 | 继续浏览或重新选择 |
| 对象失效 | 说明原对象不可用并回退默认 L0 | 重新选择 |
| 下拉加载 | 下拉内部 Skeleton；不遮挡当前页面 | 等待或关闭下拉 |
| 下拉无结果 | 保留输入和当前产业，展示“未找到产业” | 修改关键词 |
| 加入篮失败 | 按钮恢复原状态，Toast 说明失败并可重试 | 重试 |
| 未登录加入 | 触发登录；保留 return_url 和当前 industry_id | 登录后返回 |

## 3. F-CHAIN-OV-02～04：产业链全景（默认 L1）、对象详情与产业链演进

### 3.1 常驻双栏结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ {L0产业名称}产业链全景                                                  │
│ [面包屑：集成电路 › 晶圆制造]                         [返回上一级]       │
├───────────────────────────────────────────┬──────────────────────────────┤
│ 图谱区 60%                                │ 对象详情区 40%                │
│ [左上工具栏：放大/缩小/复位/全屏]         │                              │
│ 默认层级 = L1 子链：                      │ 未选择：                      │
│ 上游列          中游列          下游列    │   选择 L1 子链或关系           │
│ [半导体设备]─支撑→[晶圆制造]─交付→[封装] │   点击左侧节点或关系查看详情    │
│ [半导体材料]              [芯片设计]      │ 选中可下钻节点：               │
│                                           │   [下钻内部结构]               │
│ [左下图例：阶段/标注/关系/演进变化]       │                              │
└───────────────────────────────────────────┴──────────────────────────────┘
```

双栏在 1440、1680、1920 三档均固定为 60%/40%，不可拖拽、折叠或退回单栏。**默认图谱节点为产业层级 L1 子链**（不得默认铺开 L2+ 工艺叶子）。节点按上游/中游/下游三列布局，关系带方向与业务语义。下钻后图谱替换为该层 nodes/edges，面包屑可返回。图谱操作统一收纳在左上通用工具栏，图例固定在图谱左下角；全屏作用于完整双栏工作台并保持比例。

### 3.2 全景与演进字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 演进状态 ID | string | 图谱聚合服务 | 是 | `evolution-2026-07-31` | — |
| 演进有效时间 / 状态 | datetime + enum | 图谱聚合服务 | 是 | 2026-07-31 / current | — |
| 子链 / 节点 ID / 名称 | string | 产业链图谱 | 是 | 晶圆制造（默认层为 L1） | — |
| 产业层级 | enum | 产业链图谱 | 是 | `L1`（默认首屏）/ `L2`…（下钻层） | — |
| 阶段 | enum | 产业链图谱 | 是 | upstream / midstream / downstream | — |
| 关系类型 | enum | 产业链图谱 | 是 | supplies / depends_on / produces | — |
| 关系方向 | source→target | 产业链图谱 | 是 | 材料→晶圆制造 | — |
| 关键 / 瓶颈标注 | published tag | 专业分析已发布结果 | 否 | 关键环节 | —（仅标签，不在本页计算评分） |
| 标注证据 | source ref | 分析结果服务 | 标注存在时必填 | 分析版本、来源、更新时间 | — |
| 演进变化类型 | enum | 图谱演进服务 | 否 | node_added / node_exited / edge_changed / tech_replaced | — |
| 变化证据 | source ref | 图谱演进服务 | 变化存在时必填 | 事件或数据版本 | — |

### 3.3 右侧对象详情面板

```text
节点态：
┌──────────────────────────────────────┐
│ 晶圆制造 · 中游      [关键环节]      │
│ 简介 / 主要投入 / 主要产出           │
│ 市场规模：暂无正式数据源             │
│ [关联企业] [核心技术] [科研与服务机构]│
├──────────────────────────────────────┤
│ 当前详情 Tab 内容与来源、更新时间    │
└──────────────────────────────────────┘

关系态：
┌──────────────────────────────────────┐
│ 材料供给                             │
│ 来源节点 → 目标节点                  │
│ 业务语义 / 证据来源 / 更新时间       │
│ 当前产业链演进时间                   │
└──────────────────────────────────────┘
```

节点概览固定在面板顶部，不作为第四个 Tab。右栏独立滚动，左侧图谱视口保持稳定。关系态无 Tab；返回节点详情只能点击图谱节点，不提供返回、关闭、前后切换或第二节点选择器。

### 3.4 对象详情字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 环节简介 | text | 已发布产业链内容 / 图谱属性 | 是 | 晶圆制造负责…… | — |
| 主要投入 / 产出 | string[] | 图谱关系 | 否 | 硅片 / 晶圆 | — |
| 市场规模 | decimal | 指标服务 | 否；无源时显示不可用 | 暂无正式数据源 | `M_CHAIN_MARKET_SIZE` |
| 企业名称 / ID | string | 图谱主体清单 | 否 | 企业 A | — |
| 技术名称 / 路线 | string | 图谱技术清单 | 否 | 先进制程 | — |
| 机构名称 / 类型 | string | 图谱机构清单 | 否 | 科研机构 A | — |
| 业务数据来源 | source ref | 内容 / 图谱 / 指标服务 | 是 | 来源机构、更新时间、版本 | — |
| 关系名称 / 源节点 / 目标节点 | string | 产业链图谱 | 关系态必填 | 材料供给 / 材料 / 晶圆制造 | — |
| 关系语义 / 证据 / 更新时间 | source ref | 图谱演进服务 | 关系态必填 | 供给约束说明及证据 | — |
| 当前产业链演进时间 | datetime | 图谱演进服务 | 关系态必填 | 2026-07-31 | — |

### 3.5 全景交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 点击环节节点 | 强高亮节点和一跳上下游，弱高亮其他可达路径，无关对象降噪；右栏进入节点态并写入 `node_id` | 不取消同一节点选择；不把主体铺到主图 |
| 点击关系 | 右栏进入关系态，展示业务语义和证据 | 不弹 Drawer；不新增返回按钮 |
| 选择产业链演进时间 | 保持 `industry_id`，在原 60% 图谱呈现该状态并标记相对上一已发布状态的变化 | 不进入独立对比模式或工作区；下钻中禁用演进切换 |
| 点击变化对象 | 在右栏展示对象详情、变化类型、前后值、证据和版本 | 不只用颜色表达变化 |
| 点击关键 / 瓶颈标注 | 展示已发布标注说明和来源 | 不在总览即时运行关键/瓶颈模型 |
| 左上角通用工具栏操作 | 在画布内完成放大、缩小、复位和全屏 | 不在标题栏或右侧重复提供同类操作 |
| 通用工具栏点击“复位” | 恢复当前演进状态默认视口；已选对象保持选中 | 不切换对象、时间或清空页面筛选 |
| 通用工具栏点击“全屏” | 完整 60%/40% 双栏工作台进入全屏，比例不变 | 不只放大全景图谱 |
| 查看左下角图例 | 解释阶段、标注和关系的视觉编码 | 不遮挡主要节点；不把图例作为筛选器 |

### 3.6 全景状态

| 状态 | 表现 | 用户下一步 |
| --- | --- | --- |
| 默认 | 单链全景完整呈现；右栏显示“选择产业链环节”操作引导 | 选择节点、关系或演进时间 |
| 整体加载 | 固定图谱容器骨架，工具栏禁用 | 等待 |
| 无节点 | 明确当前链无已发布图谱，不生成示意节点 | 切换产业链 |
| 局部详情为空 | 右栏对应详情 Tab 独立空态，其他 Tab 可用 | 切换 Tab 或选择其他节点 |
| 关系失败 | 保留节点和阶段泳道，关系层错误提示与重试 | 重试 |
| 仅一个演进状态 | 显示当前状态且无变化标记；提示“暂无历史演进数据” | 继续浏览当前结构 |
| 演进切换后节点不存在 | 清除对象选择，右栏回操作引导并提示“原节点已不存在或不属于当前产业链” | 重新选择对象 |
| 无已发布标注 | 不显示关键/瓶颈 Tag，不以演示标签冒充 | 浏览结构 |

## 4. F-CHAIN-OV-05：产业资讯事件线

### 4.1 结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 产业资讯  [资讯类型 ▾] [时间范围 ▾]                                     │
├──────────────────────────────────────────────────────────────────────────┤
│ 2026-07-28 ● 事件标题                                                     │
│            事件摘要；来源机构；报道时间                                  │
│            [查看详情] [原始报道]                                         │
│ 2026-07-15 ● ……                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 事件 ID | string | 产业资讯聚合服务 | 是 | `event-001` | — |
| 标题 | string | 已整合确认资讯 | 是 | 关键项目投产 | — |
| 摘要 | text | 已整合确认资讯 | 是 | 项目完成…… | — |
| 事件发生时间 | datetime | 事件识别 / 人工确认 | 是 | 2026-07-28 | — |
| 报道时间 | datetime | 原始报道 | 是 | 2026-07-29 | — |
| 资讯类型 | enum | 资讯分类 | 是 | 政策 / 技术 / 企业 / 投融资 / 市场 | — |
| 来源机构 | string | 原始报道 | 是 | 来源机构 A | — |
| 原始报道链接 | URL | 原始报道 | 是；缺失须显式标记 | `https://…` | — |
| 内容版本 / 更新时间 | string / datetime | 内容发布服务 | 是 | v1 / 2026-07-30 | — |

### 4.3 交互与状态

| 触发 / 状态 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 默认 | 按事件发生时间倒序 | 不按抓取顺序替代事件时间 |
| 筛选类型 / 时间 | 只过滤当前 `industry_id` 事件线，保留筛选摘要 | 不改变当前产业 |
| 查看详情 | 打开事件详情 Drawer；关闭后保留时间位置和筛选 | 不跳到另一条产业链 |
| 打开原始报道 | 新窗口打开真实 URL，并保留返回上下文 | 不生成伪链接 |
| 无事件 | 显示当前筛选无事件，可清除筛选 | 不自动混入其他产业链资讯 |
| 原始链接缺失 | 明确“原始报道链接缺失” | 不隐藏缺口 |
| 加载失败 | 固定事件线容器并提供重试 | 不显示旧链缓存冒充当前数据 |

## 5. F-CHAIN-OV-06～07：产业整体概况与区域分布

### 5.1 结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 产业整体概况                                                             │
│ [产业介绍：整条产业链的基础说明____________________________________]     │
├───────────────────────────┬──────────────────────────────────────────────┤
│ 关联企业数                │ 关联机构数                                   │
│ 1,286                     │ 84                                           │
├───────────────────────────┴──────────────────────────────────────────────┤
│ 区域分布 [全球/全国/区域/深圳 可搜索级联] [地图视图|列表视图]          │
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ [左侧地图通用工具栏：放大/缩小/复位/全屏]                          │ │
│ │ 默认全国省级地图 / 与当前层级一致的地域聚合列表                    │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.2 整体概况字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 产业介绍 | text | 已发布产业概况内容 | 是 | 集成电路产业链包括…… | — |
| 关联企业数 | int | 指标服务 | 是 | 1,286 | `M_CHAIN_ENTERPRISE_COUNT` |
| 关联机构数 | int | 指标服务 | 是 | 84 | `M_CHAIN_INSTITUTION_COUNT` |
| 数据更新时间 | datetime | 指标 / 内容服务 | 是 | 2026-07-31 | — |
| 内容版本 | string | 内容发布服务 | 是 | v1.2 | — |

### 5.3 区域分布字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 地域路径 | string[] | 统一地域字典 | 是 | 全国 / 广东省 / 深圳市 / 南山区 | — |
| 地域名称 / 行政码 | string | 统一地域字典 | 是 | 南山区 / 440305 | — |
| 地域级别 | enum | 统一地域字典 | 是 | country / province / city / district | — |
| 地域关联企业数 | int | 当前地域过滤的指标服务 | 是 | 126 | `M_CHAIN_ENTERPRISE_COUNT` |
| 地域关联机构数 | int | 当前地域过滤的指标服务 | 是 | 18 | `M_CHAIN_INSTITUTION_COUNT` |
| 聚合快照时间 | datetime | 指标服务 | 是 | 2026-07-31 | — |
| 数据来源 / 版本 | source ref | 指标服务 | 是 | source_systems / version | — |

### 5.4 地域控件规则

- 单个可搜索级联组件，一级入口固定为全球、全国、区域、深圳。
- 全球数据对象固定为 G20 国家；不得将其他国家混入“全球”结果。
- 全国默认省级聚合，允许省→市→区县持续下钻。
- 区域沿用京津冀、长三角、粤港澳大湾区等统一区域字典。
- 深圳入口支持深圳市及各区。
- 搜索可命中任一可选节点并回显完整路径；无结果不改变当前路径。
- 复用企业分析统一地域控件的交互、搜索、键盘与路径状态；产业链只提供自己的数据口径。

### 5.5 地图 / 列表双视图交互

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 首次进入 | 默认“全国”，显示省级地图 | 不继承企业分析默认深圳 |
| 地图点击地域 | 在允许范围下钻并更新地图、列表数据源和路径 | 不改变顶部整链 KPI |
| 切换地图 / 列表 | 只替换区域分布主工作区；保留路径、范围和选中地域 | 不建立第二套列表层级状态 |
| 列表点击“在地图中查看” | 切回地图并定位、高亮对应地域 | 不通过点击普通数值列触发动作 |
| 左侧地图通用工具栏点击“复位” | 回到当前一级范围默认层级，并清除地图内临时选择 | 不在右侧或区域分布标题栏重复提供复位；不重置为另一一级范围或清空全局筛选 |
| 底图失败 | 保留列表可用，显示底图错误与重试 | 不让整个整体概况不可用 |

地图视图直接复用通用地图工具栏；复位是其左侧工具项之一，位置与行为服从 `UX-UE 通用交互组件规范.md` §9、§9.1，不作为右侧独立业务操作展示。切换为列表视图后不显示地图工具栏。

### 5.6 区域列表列定义

| 列 | 行为 |
| --- | --- |
| 地域 | 展示当前层级名称；普通单元格不跳转 |
| 关联企业数 | 展示当前链在该地域的聚合数量；不点击 |
| 关联机构数 | 展示当前链在该地域的聚合数量；不点击 |
| 数据更新时间 | 展示当前聚合快照时间 |
| 操作 | 仅提供“在地图中查看”；后续是否进入产业查询不在本模块自行扩展 |

## 6. F-CHAIN-OV-08：产业发展历程

### 6.1 结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 产业发展历程                                                             │
├──────────────────────────────────────────────────────────────────────────┤
│ [阶段一 2000—2008]──[阶段二 2009—2018]──[阶段三 2019—至今]              │
│ 阶段特征 / 代表性成果                                                    │
│  ● 里程碑时间 — 事件 — 产业影响 — [查看证据]                             │
│  ● ……                                                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 阶段 ID / 名称 | string | 已发布发展内容 | 是 | 规模化发展期 | — |
| 阶段起止时间 | date range | 已发布发展内容 | 是 | 2019—至今 | — |
| 阶段特征 | text | 已发布发展内容 | 是 | 产业进入规模化扩张…… | — |
| 代表性成果 | text[] | 已发布发展内容 | 是 | 形成完整制造体系 | — |
| 里程碑 ID / 时间 | string / datetime | 发展路线模型 + 人工确认 | 是 | 2024-05 | — |
| 里程碑事件 | text | 发展路线模型 + 人工确认 | 是 | 重大项目投产 | — |
| 产业影响 | text | 已发布分析内容 | 是 | 补齐某关键环节 | — |
| 专家观点 | text | 已发布内容 | 否 | 专家观点摘要 | — |
| 来源与版本 | source ref | 内容发布服务 | 是 | 原始资料、更新时间、版本 | — |

### 6.3 交互与状态

| 触发 / 状态 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 选择阶段 | 定位该阶段并显示其里程碑 | 不改变当前产业链 |
| 点击里程碑 | 打开详情与证据；关闭后保留时间轴位置 | 不把原始报道藏在评审模式中 |
| 阶段未发布 | 显示未发布空态，不用资讯自动拼阶段 | 不生成 AI 阶段文案冒充已确认内容 |
| 来源缺失 | 对应里程碑标明“来源缺失” | 不生成伪链接 |

## 7. F-CHAIN-OV-09：深圳产业现状

### 7.1 结构线框

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ 深圳产业现状                                                             │
│ [深圳企业数] [深圳机构数] [覆盖区县数]                                  │
├────────────────────────────────────────────┬─────────────────────────────┤
│ 深圳各区 [地图|列表] · 60%                 │ 区域特色研判 · 40%            │
│                                            │ [特色优势][集群效应][竞争地位] │
│ 当前链在深圳各区的主体分布                 │ 已发布内容 + 来源 + 更新时间   │
└────────────────────────────────────────────┴─────────────────────────────┘
```

主体内容区固定采用 **左 60% + 右 40%**：左侧用于深圳各区地图/列表，右侧用于区域特色研判。比例按内容区可用宽度计算，不包含两栏间距；`medium_1440_1920` 范围内保持该比例，不回退为 50% + 50%。

### 7.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 深圳产业链企业数 | int | 指标服务 | 是 | 326 | `M_CHAIN_SZ_ENTERPRISE_COUNT` |
| 深圳产业链机构数 | int | 指标服务 | 是 | 28 | `M_CHAIN_SZ_INSTITUTION_COUNT` |
| 深圳产业分布区域数 | int | 指标服务 | 是 | 9 | `M_CHAIN_SZ_REGION_COUNT` |
| 区域路径 / 区名称 | string | 统一地域字典 | 是 | 深圳 / 南山区 | — |
| 区域企业数 | int | 深圳地域过滤的指标服务 | 是 | 88 | `M_CHAIN_SZ_ENTERPRISE_COUNT` |
| 区域机构数 | int | 深圳地域过滤的指标服务 | 是 | 12 | `M_CHAIN_SZ_INSTITUTION_COUNT` |
| 特色优势 | rich text | 已发布深圳现状内容 | 是 | 技术创新资源集聚…… | — |
| 集群效应 | rich text | 已发布深圳现状内容 | 是 | 上下游协同…… | — |
| 竞争地位 | rich text | 已发布深圳现状内容 | 是 | 在全国处于…… | — |
| 来源 / 更新时间 / 内容版本 | source ref | 指标 / 内容发布服务 | 是 | 来源、2026-07-31、v1 | — |

### 7.3 交互与边界

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 地图 / 列表切换 | 保留深圳各区选择和视图上下文 | 不跳到全国或全球范围 |
| 点击区 | 更新当前区聚合与高亮 | 不修改顶部整链对象 |
| 切换特色研判分组 | 展示对应已发布内容和业务来源 | 不在页面即时生成建议 |
| 内容未发布 | 显示未发布空态 | 不从旧 Demo 或前端常量补文案 |
| 点击进入深圳决策（后续跨模块入口，如配置） | 只携带当前 `industry_id` 或打开系统对比篮选择对象 | 不在本页提交模型任务 |

## 8. F-CHAIN-OV-10：共享对比篮状态交接

### 8.1 结构线框

```text
[当前 L0 产业] ──点击加入/移出──> [系统共享篮：industry 对象域]
                                      │
                                      └─ 用户从系统悬浮入口自行打开全局浮层
```

> 本 Frame 只定义产业链总览与共享篮状态的对象交接。总览不提供打开浮层按钮、不发送打开信号，也不复制、不改写全局对比篮的内部线框。

### 8.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 对象类型 | enum | 总览交接上下文 | 是 | `industry` | — |
| 产业链 ID / 名称 | object ref | 当前产业链上下文 | 是 | `chain-integrated-circuit` / 集成电路产业链 | — |
| 加入来源 | route ref | 当前页面 | 是 | `/industry-center/overview` | — |
| 篮状态 | enum | 系统共享对比篮 | 是 | `in_basket` / `not_in_basket` | — |

### 8.3 交互与边界

| 触发 | 页面行为 | 不应发生的行为 |
| --- | --- | --- |
| 加入 / 移出当前 L0 产业 | 更新 `industry` 共享篮状态；保留当前总览 Tab、滚动、图谱和筛选状态 | 不打开全局浮层；不跳转独立篮页面 |
| 浮层内对象管理 | 用户从系统悬浮入口进入后，完全由全局对比篮合同处理并回写共享篮状态 | 总览不复制选择、清空或分析分发逻辑 |
| 全局篮状态变化 | 当前链加入/移出按钮跟随共享状态更新 | 不显示页面局部对象数，不建立页面局部篮状态 |
| 权限 L0 触发加入/移出对比篮 | 显示登录引导并保留当前 `industry_id`、Tab、滚动及图谱状态；登录成功后回到原触发点 | 不建立匿名篮、不静默失败 |
| L1 及以上加入/移出对比篮 | 使用全局对比篮的统一鉴权结果；总览只展示系统返回状态 | 不在总览重复实现权限或篮状态 |
| L1 尝试发起分析 | 全局对比篮按 L2 最低级别显示升级专业用户提示 | 总览不得绕过全局鉴权直接运行分析 |

## 9. 通用状态、响应式与视觉约束

### 9.1 通用状态优先级

1. 对象失效 / 权限失败。
2. Frame 整体错误。
3. Frame 加载。
4. 局部数据空 / 局部来源缺失。
5. 正常内容。

评审层加载失败不得覆盖业务状态；业务模式不得因为评审层关闭而改变字段、权限、布局或可操作能力。

### 9.2 屏幕与设计约束

- **screen_tier**：唯一声明 `medium_1440_1920`；科技专题服务系统不声明 `small_reflow`。
- **设计系统**：`agent-delivery/Design.md`；React + Vite + Arco；图谱内核 AntV G6，地图 Leaflet，图表 ECharts。
- **页面骨架**：Header 64px、Sidebar 200px（1440～1679 默认收起为 64px）、外壳 16px 间距；控件高度 32px。
- **图谱优先**：全景 Frame 常驻 60% 图谱 + 40% 对象详情；不使用 KPI 卡片替代图谱。
- **1440～1679**：左侧导航默认收起；双栏仍固定 60%/40%，图谱工具与图例可紧凑但不可删除；页面不得横向溢出。
- **1680～1920**：保留完整双栏工作台和工具栏；不扩张为 Track-L 大屏。
- **可访问性**：所有下拉、Tab、地图/图谱工具、列表操作和右侧对象详情可键盘到达；变化、标注和状态不得只依赖颜色。
- **可视化替代路径**：地图必须有同层列表；图谱关系失败时保留阶段化节点结构与文字错误说明；复杂图形提供文本摘要。

### 9.3 明确禁止

- 不得同时显示多条产业链的节点和关系。
- 不得在任一 Tab 内提供第二个产业链切换器。
- 不得把产业整体概况绑定到当前节点；它始终统计整条链。
- 不得把资讯事件线、发展阶段时间轴和产业链演进合并为一种时间组件。
- 不得为产业链演进新增独立“对比变化”按钮、对比模式或对比工作区。
- 不得把右侧对象详情改成 Drawer、可折叠/可拖拽面板，或在面板内增加第二节点选择器、返回/关闭、前后切换控件。
- 不得用无语义力导向彩点图替代阶段化产业链全景。
- 不得在总览运行趋势、区域、深圳决策模型或直接生成报告。
- 不得出现“关注产业链 / 已关注”。
- 不得让前端直连 Python、Nebula、ODS/DWD，或在前端硬编码评审说明、指标定义、数据来源。
- 不得在业务标题、业务副标题、卡片说明中混入需求编号、Mock、Pending 或内部评审文案。

## 10. 内部评审追溯合同

### 10.1 规则

- 每个 Frame 都显式登记 `review_mounts`；没有挂载时必须为空数组。本模块所有 Frame 均有对应挂载。
- 一个 `mount_id` 只对应一个 Frame 内的一个可见宿主，不得复用。
- 需求追溯触发器紧邻对应模块标题或交互宿主，浮层必须展示 Bid **完整原文**，不是编号列表或摘要替代。
- 每个统计指标使用独立的 `metric_spec` 挂载；禁止把多个 metric_id 合并进一个缩小字号浮层。
- 指标浮层中的每个元数据字段单独一行，统一使用正文级字号；不得通过逐层缩小字体容纳内容。
- `metric_spec`、`mock_badge`、`pending_badge`、`review_copy` 的语义和 payload 服从 `data-lineage-policy.md`；四件套只指定宿主和挂载清单。
- 评审模式 `present`；业务模式 `absent`，且业务字段、权限、布局和行为不因评审层开关而改变。
- 业务数据自己的来源、更新时间、版本和原始报道链接不属于内部评审层，在业务模式仍正常显示。

### 10.2 机器可读合同

```yaml
review_trace_contract:
  version: "1.0"
  business_mode_rule: review_layer_absent_without_business_behavior_change
  requirement_payload_rule: full_original_text_required
  metric_layout_rule: one_metric_per_mount_each_payload_field_own_row_uniform_body_font
  frames:
    - frame_id: F-CHAIN-OV-01
      review_mounts: [CHAIN-OV-F01-CONTEXT-REQ]
    - frame_id: F-CHAIN-OV-02
      review_mounts: [CHAIN-OV-F02-PANORAMA-REQ]
    - frame_id: F-CHAIN-OV-03
      review_mounts: [CHAIN-OV-F03-NODE-REQ, CHAIN-OV-F03-MARKET-METRIC, CHAIN-OV-F03-MARKET-PENDING, CHAIN-OV-F03-MARKET-MOCK]
    - frame_id: F-CHAIN-OV-04
      review_mounts: [CHAIN-OV-F04-EVOLUTION-REQ, CHAIN-OV-F04-EVOLUTION-PENDING]
    - frame_id: F-CHAIN-OV-05
      review_mounts: [CHAIN-OV-F05-NEWS-REQ]
    - frame_id: F-CHAIN-OV-06
      review_mounts: [CHAIN-OV-F06-PROFILE-REQ, CHAIN-OV-F06-ENT-METRIC, CHAIN-OV-F06-ENT-MOCK, CHAIN-OV-F06-ORG-METRIC, CHAIN-OV-F06-ORG-MOCK]
    - frame_id: F-CHAIN-OV-07
      review_mounts: [CHAIN-OV-F07-DIST-REQ, CHAIN-OV-F07-ENT-METRIC, CHAIN-OV-F07-ENT-MOCK, CHAIN-OV-F07-ORG-METRIC, CHAIN-OV-F07-ORG-MOCK, CHAIN-OV-F07-DIST-PENDING]
    - frame_id: F-CHAIN-OV-08
      review_mounts: [CHAIN-OV-F08-HISTORY-REQ, CHAIN-OV-F08-HISTORY-PENDING]
    - frame_id: F-CHAIN-OV-09
      review_mounts: [CHAIN-OV-F09-SZ-REQ, CHAIN-OV-F09-ENT-METRIC, CHAIN-OV-F09-ENT-MOCK, CHAIN-OV-F09-ORG-METRIC, CHAIN-OV-F09-ORG-MOCK, CHAIN-OV-F09-REGION-METRIC, CHAIN-OV-F09-REGION-MOCK, CHAIN-OV-F09-CONTENT-PENDING]
    - frame_id: F-CHAIN-OV-10
      review_mounts: [CHAIN-OV-F10-BASKET-REQ]
  mounts:
    - mount_id: CHAIN-OV-F01-CONTEXT-REQ
      frame_id: F-CHAIN-OV-01
      host_label: 当前产业链可检索下拉框与上下文操作组标题
      marker_type: requirement_trace
      source_relation: product_interpretation
      trace_refs: [PI-CHAIN-OV-01, PI-CHAIN-OV-02, PI-CHAIN-OV-03, PI-CHAIN-OV-12]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F02-PANORAMA-REQ
      frame_id: F-CHAIN-OV-02
      host_label: 顶部产业链全景 Tab
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-002, REQ-CHAIN-OV-005, PI-CHAIN-OV-04]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F03-NODE-REQ
      frame_id: F-CHAIN-OV-03
      host_label: 右侧对象详情面板标题（节点态与关系态共享宿主）
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-002, REQ-CHAIN-OV-005, PI-CHAIN-OV-05]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F03-MARKET-METRIC
      frame_id: F-CHAIN-OV-03
      host_label: 右侧节点概览中的市场规模字段标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_MARKET_SIZE]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F03-MARKET-PENDING
      frame_id: F-CHAIN-OV-03
      host_label: 右侧节点概览中的市场规模字段标签
      marker_type: pending_badge
      source_relation: open_question
      trace_refs: [Q056]
      required_payload: [pending_ref, summary, current_treatment, owner, deadline]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F03-MARKET-MOCK
      frame_id: F-CHAIN-OV-03
      host_label: 右侧节点概览中的市场规模字段值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_MARKET_SIZE]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F04-EVOLUTION-REQ
      frame_id: F-CHAIN-OV-04
      host_label: 产业链演进控件标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-005, PI-CHAIN-OV-06]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F04-EVOLUTION-PENDING
      frame_id: F-CHAIN-OV-04
      host_label: 演进时间状态与变化证据说明
      marker_type: pending_badge
      source_relation: open_question
      trace_refs: [Q062]
      required_payload: [pending_ref, summary, current_treatment, owner, deadline]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F05-NEWS-REQ
      frame_id: F-CHAIN-OV-05
      host_label: 产业资讯模块标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-003, PI-CHAIN-OV-07]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F06-PROFILE-REQ
      frame_id: F-CHAIN-OV-06
      host_label: 产业整体概况模块标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-004, PI-CHAIN-OV-08]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F06-ENT-METRIC
      frame_id: F-CHAIN-OV-06
      host_label: 关联企业数指标标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_ENTERPRISE_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F06-ENT-MOCK
      frame_id: F-CHAIN-OV-06
      host_label: 关联企业数指标值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_ENTERPRISE_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F06-ORG-METRIC
      frame_id: F-CHAIN-OV-06
      host_label: 关联机构数指标标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_INSTITUTION_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F06-ORG-MOCK
      frame_id: F-CHAIN-OV-06
      host_label: 关联机构数指标值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_INSTITUTION_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-DIST-REQ
      frame_id: F-CHAIN-OV-07
      host_label: 区域分布卡片标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-004, PI-CHAIN-OV-09]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-ENT-METRIC
      frame_id: F-CHAIN-OV-07
      host_label: 地图图例和列表中的关联企业数字段标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_ENTERPRISE_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-ENT-MOCK
      frame_id: F-CHAIN-OV-07
      host_label: 地图图例和列表中的关联企业数值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_ENTERPRISE_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-ORG-METRIC
      frame_id: F-CHAIN-OV-07
      host_label: 地图图例和列表中的关联机构数字段标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_INSTITUTION_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-ORG-MOCK
      frame_id: F-CHAIN-OV-07
      host_label: 地图图例和列表中的关联机构数值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_INSTITUTION_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F07-DIST-PENDING
      frame_id: F-CHAIN-OV-07
      host_label: 四级地域可搜索控件标签
      marker_type: pending_badge
      source_relation: open_question
      trace_refs: [Q060]
      required_payload: [pending_ref, summary, current_treatment, owner, deadline]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F08-HISTORY-REQ
      frame_id: F-CHAIN-OV-08
      host_label: 产业发展历程模块标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-001, PI-CHAIN-OV-10]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F08-HISTORY-PENDING
      frame_id: F-CHAIN-OV-08
      host_label: 发展阶段和里程碑内容标题
      marker_type: pending_badge
      source_relation: open_question
      trace_refs: [Q061]
      required_payload: [pending_ref, summary, current_treatment, owner, deadline]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-SZ-REQ
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业现状模块标题
      marker_type: requirement_trace
      source_relation: direct_requirement
      trace_refs: [REQ-CHAIN-OV-001, PI-CHAIN-OV-11]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-ENT-METRIC
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业链企业数指标标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_SZ_ENTERPRISE_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-ENT-MOCK
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业链企业数指标值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_SZ_ENTERPRISE_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-ORG-METRIC
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业链机构数指标标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_SZ_INSTITUTION_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-ORG-MOCK
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业链机构数指标值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_SZ_INSTITUTION_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-REGION-METRIC
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业分布区域数指标标签
      marker_type: metric_spec
      source_relation: metric_registry
      trace_refs: [M_CHAIN_SZ_REGION_COUNT]
      required_payload: [metric_id, metric_name_zh, definition, formula, source_tables, source_systems, update_freq, version]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-REGION-MOCK
      frame_id: F-CHAIN-OV-09
      host_label: 深圳产业分布区域数指标值
      marker_type: mock_badge
      source_relation: data_status
      trace_refs: [M_CHAIN_SZ_REGION_COUNT]
      required_payload: [metric_id, is_mock, source_systems, calc_batch_id]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F09-CONTENT-PENDING
      frame_id: F-CHAIN-OV-09
      host_label: 区域特色研判内容标题
      marker_type: pending_badge
      source_relation: open_question
      trace_refs: [Q061]
      required_payload: [pending_ref, summary, current_treatment, owner, deadline]
      review_mode: present
      business_mode: absent
    - mount_id: CHAIN-OV-F10-BASKET-REQ
      frame_id: F-CHAIN-OV-10
      host_label: 总览顶部加入或移出共享对比篮动作
      marker_type: requirement_trace
      source_relation: product_interpretation
      trace_refs: [PI-CHAIN-OV-12]
      required_payload: [source_location, source_original_text, current_placement, source_relation]
      review_mode: present
      business_mode: absent
```

### 10.3 禁止挂载位置

- 页面固定右上角、全局悬浮按钮或统一评审侧栏不得替代模块就地挂载。
- 页面主标题不得承载所有 Tab 的需求追溯；每个 Tab 必须挂在自己的模块标题。
- 指标卡片外部的统一“指标说明”不得替代每个指标标签旁的独立挂载。
- 需求编号、评审结论、Mock/Pending 文案不得写入业务标题、副标题、描述或空态。
- 右侧对象详情、事件详情、时间轴和地图/列表作为独立可见宿主时，不得复用其他 Frame 的 `mount_id`。

## 11. 本页 metric_id 清单

| metric_id | 展示位置 | 当前状态 | 条件处理 |
| --- | --- | --- | --- |
| `M_CHAIN_ENTERPRISE_COUNT` | F-06 整链企业数；F-07 地域过滤企业数 | D1 aligned / D2 partial（provisional）/ D3 full / D4 mock | 评审模式从 CHAIN readiness 矩阵只读显示 8 件套与 Mock；D2 待核验，正式数据接入前不宣称真实全量 |
| `M_CHAIN_INSTITUTION_COUNT` | F-06 整链机构数；F-07 地域过滤机构数 | D1 aligned / D2 partial（provisional）/ D3 full / D4 mock | 同上 |
| `M_CHAIN_MARKET_SIZE` | F-03 右侧节点概览 | D1 draft / D2 partial（provisional）/ D3 none / D4 mock；Q056 | 业务字段显示不可用；评审模式入口保留指标说明、Pending 与 Mock 三枚，D2 缺口在指标弹卡内展示，不得生成虚构数字 |
| `M_CHAIN_SZ_ENTERPRISE_COUNT` | F-09 深圳企业数及区级过滤 | D1 aligned / D2 partial（provisional）/ D3 full / D4 mock | 评审模式从 CHAIN readiness 矩阵只读显示 8 件套与 Mock；D2 待核验 |
| `M_CHAIN_SZ_INSTITUTION_COUNT` | F-09 深圳机构数及区级过滤 | D1 aligned / D2 partial（provisional）/ D3 full / D4 mock | 同上 |
| `M_CHAIN_SZ_REGION_COUNT` | F-09 深圳覆盖区县数 | D1 aligned / D2 partial（provisional）/ D3 full / D4 mock | 同上 |

## 12. Wireframe 自检

- [x] 10 个 Frame 均对应 IA 节点和 USM 主/异常路径。
- [x] 所有统计字段使用已登记的 `M_CHAIN_*`，没有自创指标或来源。
- [x] 默认、加载、空数据、局部缺失、错误、无来源、未发布和权限态均有定义。
- [x] 单链上下文、Tab 联动、固定 60%/40% 双栏、地图/列表共享状态和对比篮边界明确。
- [x] 每个 Frame 均有机器可读 `review_mounts`；所有 `mount_id` 唯一。
- [x] 需求追溯要求完整原文；指标一项一挂载、一字段一行、同一正文级字号。
- [x] 业务模式移除评审层，但保留业务数据自身的来源、时间、版本和原始报道链接。
- [x] 未引入产业查询、任务运行、报告生成、内容编辑或关注功能。
