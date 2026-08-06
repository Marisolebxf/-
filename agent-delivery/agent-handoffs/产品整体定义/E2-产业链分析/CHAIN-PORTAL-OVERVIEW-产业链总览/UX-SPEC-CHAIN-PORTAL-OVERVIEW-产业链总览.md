# UX-SPEC-CHAIN-PORTAL-OVERVIEW-产业链总览

> **模块**：CHAIN-PORTAL-OVERVIEW / 产业链总览  
> **文档版本**：v1.5-portal-panorama-scope  
> **四件套版本**：v1.5-portal-panorama-scope  
> **日期**：2026-08-06  
> **交付阶段**：v1_hifi_round1  
> **屏幕档位**：medium_1440_1920  
> **UX 结论**：ready_for_v1  
> **边界**：本文件只把已确认产品定义转译为可实现、可验证的交互规则，不修改产品范围，不代表 PDR、V1-FINAL、V2 或 Gate 通过。  
> **决策真源**：`DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806.md`；`DEC-CHAIN-PORTAL-OVERVIEW-PANORAMA-SCOPE-20260806.md`

## 1. 权威输入与边界

> **v1.5 门户全景范围**：全景 Tab 仅承接门户 Bid §1.1.1.1.1.1.1.1（结构图 + 简介/企业列表）；不提供演进、核心技术、科研与服务机构、市场规模。顶部选 L0；默认 L1 并可结构下钻；对比篮 `industry`。

### 1.1 权威输入

| 类型 | 文件 | 本文用途 |
| --- | --- | --- |
| DEC | `DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806.md` | L0 选择器与 L1 默认下钻决策 |
| IA | `IA-CHAIN-PORTAL-OVERVIEW-产业链总览.md` | 路由、对象上下文、五个 Tab 与页面边界 |
| TRACE | `TRACE-CHAIN-PORTAL-OVERVIEW-产业链总览.yaml` | 原始需求、产品解释、指标、缺口与阶段约束 |
| USM | `USM-CHAIN-PORTAL-OVERVIEW-产业链总览.md` | 三类角色、故事、主异常路径与验收结果 |
| Wireframe | `Wireframe-CHAIN-PORTAL-OVERVIEW-产业链总览.md` | Frame、承载位置、布局及评审挂载 |
| 评审规程 | `agent-delivery/产品定义评审规程.md` | Track-MS 阶段、PDR 与交付等级边界 |
| 通用交互 | `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md` | Tabs、图谱、地图、双栏工作台、键盘与状态反馈 |
| 视觉规范 | `agent-delivery/Design.md` | medium 端工作台、Arco 组件、尺寸与响应式约束 |
| 数据血缘 | `agent-delivery/data-lineage-policy.md` | 指标 8 件套、Mock、Pending 与评审模式规则 |

### 1.2 不可变产品边界

- 页面只描述一个当前 **L0 产业**；顶部可检索产业下拉框是五个 Tab 的唯一对象切换入口，选项仅 L0；Tab 内不得再次提供产业或子链切换。
- 路由固定为 `/industry-center/overview`；主参 `industry_id`；默认 Tab 为 `panorama`，其余为 `profile`、`news`、`history`、`shenzhen`。
- 全景默认展示当前 L0 下的 **L1 子链**（如半导体设备、晶圆制造），不得默认铺开 L2+ 工艺叶子；更细分结构经详情区「下钻内部结构」逐级进入，面包屑返回。
- 页面只承载门户浏览与加入系统产业对比篮，不在本页直接执行趋势诊断、区域评价或深圳决策。
- 不设置“关注产业”能力；不新增建议生成、方案推荐、任务提交、报告生成或企业分析业务语义。
- 页面只把当前 L0 产业加入或移出 `industry` 共享篮，不提供打开全局对比篮按钮或打开信号；用户从系统悬浮入口自行打开浮层，页面不得自建篮 Drawer。
- 全景常驻固定 60% 图谱 + 40% 对象详情面板；产业链演进只在原图谱展示时间状态与变化，不新增独立对比按钮、模式或工作区。
- 不存在专项权限例外：权限 L0 只读浏览总览（含 L1 默认结构），权限 L1 可查看主体明细并加入/移出对比篮，权限 L2 在全局篮选择并发起分析，权限 L3 承载敏感明细与高级配置；前端降级不能替代统一权限服务的服务端鉴权。
- 内部评审层只在评审模式出现；业务模式 DOM 中不存在评审标识、需求原文、指标说明、Mock 或 Pending 文案，且业务行为不因评审层开关而变化。

## 2. 四件套同步核对

### 2.1 故事清单

| story_id | 产品角色 | 目标 | Frame |
| --- | --- | --- | --- |
| US-CHAIN-OV-01 | 政府产业管理与决策人员 | 确定并切换当前 L0 产业 | F-CHAIN-OV-01 |
| US-CHAIN-OV-02 | 政府产业管理与决策人员 | 看清 L1 子链结构 | F-CHAIN-OV-02 |
| US-CHAIN-OV-03 | 企业战略与产业合作人员 | 查看简介与企业列表 | F-CHAIN-OV-03 |
| US-CHAIN-OV-04 | — | （废止）动态演进归专题 | — |
| US-CHAIN-OV-05 | 投资机构产业研究人员 | 沿事件线追踪资讯 | F-CHAIN-OV-05 |
| US-CHAIN-OV-06 | 政府产业管理与决策人员 | 查看整链概况 | F-CHAIN-OV-06 |
| US-CHAIN-OV-07 | 政府产业管理与决策人员 | 查看产业空间布局 | F-CHAIN-OV-07 |
| US-CHAIN-OV-08 | 投资机构产业研究人员 | 理解产业发展阶段 | F-CHAIN-OV-08 |
| US-CHAIN-OV-09 | 政府产业管理与决策人员 | 查看深圳产业现状 | F-CHAIN-OV-09 |
| US-CHAIN-OV-10 | 准备开展专业分析的用户 | 加入后续分析对象集合 | F-CHAIN-OV-01、F-CHAIN-OV-10 |
| US-CHAIN-OV-11 | 政府产业管理与决策人员 | 从 L1 逐级下钻更细分结构 | F-CHAIN-OV-02、F-CHAIN-OV-03 |

### 2.2 Frame、路由与状态清单

| Frame | 承载位置 | 关键状态 | 明确禁止 |
| --- | --- | --- | --- |
| F-CHAIN-OV-01 | 页面顶部对象上下文与 Tab Shell | `industry_id`（L0）、`active_tab`、篮内状态 | Tab 内第二选择器、L1 选项、关注状态 |
| F-CHAIN-OV-02 | `panorama` 左 60% 主图谱 | 演进时间、缩放、平移、选中对象、`drill_stack` | 多产业混显、默认铺开 L2+、无依据连线、单栏退化 |
| F-CHAIN-OV-03 | `panorama` 右 40% 对象详情 | 空态、节点态（简介+企业列表）、关系摘要、下钻动作 | 核心技术/科研机构/市场规模 Tab、演进证据、Drawer |
| F-CHAIN-OV-04 | ~~演进控件~~（废止） | — | 门户全景不得出现演进控件 |
| F-CHAIN-OV-05 | `news` 事件线与事件详情 | 类型、时间、事件详情 | 伪造原始报道链接 |
| F-CHAIN-OV-06 | `profile` 整链概况 | 整链指标、介绍 | 随图谱节点选择改变整链指标 |
| F-CHAIN-OV-07 | `profile` 区域分布 | 地域路径、层级、地图/列表 | 地图与列表范围不一致、右侧独立复位 |
| F-CHAIN-OV-08 | `history` 阶段时间轴 | 阶段、里程碑、证据 | 与资讯或产业链演进职责混合 |
| F-CHAIN-OV-09 | `shenzhen` 深圳现状 | 深圳指标、区级地图/列表、研判内容 | 决策建议、任务提交、改变 60%/40% |
| F-CHAIN-OV-10 | 页面顶部共享篮状态交接 | `industry` 域、当前 L0 篮内状态 | 页面打开浮层、自建浮层、直接运行分析 |

同步结论：11/11 故事、10/10 Frame、6/6 指标、30/30 评审挂载均有交互落点；四项已知缺口均有确定的 V1 处理，不阻断 `v1_hifi_round1`。Q063 已按全系统权限基线闭合，TRACE 当前其他治理状态不由本文件改写。

## 3. 用户旅程与任务流

### 3.1 J-CHAIN-OV-GOV｜政府产业管理与决策人员

- **关联故事**：US-CHAIN-OV-01、02、06、07、09、10、11。
- **主路径**：进入路由 → 加载有效 `industry_id`（L0）或默认推荐产业 → 在全景确认 L1 子链上下游结构 → 可逐级下钻更细子链 → 切换整体概况 → 使用四级地域控件查看全国至区县或 G20 → 在地图/列表间保持同层切换 → 查看深圳现状 → 加入产业对比篮 → 需要时从系统悬浮入口自行打开全局篮。
- **异常路径**：入口对象无效时说明原因并回退默认 L0；地图失败时保留地域路径并切列表；未登录加入时进入登录并保留返回上下文；全局篮浮层异常由系统入口原位反馈，不在总览增加恢复按钮。
- **完成出口**：继续在五个 Tab 浏览，或从全局对比篮发起后续分析；本页不代替后续分析页。

### 3.2 J-CHAIN-OV-INVEST｜投资机构产业研究人员

- **关联故事**：US-CHAIN-OV-01、04、05、08。
- **主路径**：确定当前 L0 → 在“产业链演进”选择同产业历史状态 → 在原图谱查看新增、退出、技术替代与关系变化 → 在右栏查看变化对象和证据 → 切换资讯与发展历程继续研究。
- **异常路径**：仅一个演进状态时显示“暂无历史演进数据”；证据失败时保留当前图谱并提供重试；原始报道缺失时显示明确缺失状态；内容未发布时显示未发布空态。
- **完成出口**：返回当前全景、切换其他门户 Tab，或把当前 L0 产业交给全局对比篮。

### 3.3 J-CHAIN-OV-COLLAB｜企业战略与产业合作人员

- **关联故事**：US-CHAIN-OV-01、02、03、11。
- **主路径**：确定当前 L0 → 在全景识别 L1 子链与关系方向 → 键盘或指针选择节点 → 右侧面板查看固定概览及关联企业、核心技术、科研与服务机构 → 对可下钻节点进入内部结构 → 点击关系查看语义和证据 → 点击节点回到节点详情。
- **异常路径**：部分详情缺失时只在对应详情 Tab 显示局部空态；关系服务失败时保留节点和阶段分区；市场规模无正式来源时显示“暂无正式数据源”。
- **完成出口**：继续选择其他节点/关系、返回上级子链，或切换其他 Tab；右栏独立滚动，图谱视口和演进状态保持。

## 4. Frame 与承载映射

| Frame | 入口与宿主 | 核心控件 | 退出与上下文保持 |
| --- | --- | --- | --- |
| F-CHAIN-OV-01 | `/industry-center/overview` 页面头部 | L0 可检索 Select、加入/移出按钮、Tabs | 切 Tab 保留 `industry_id`；切 L0 保留 Tab、清除下钻栈与旧局部状态 |
| F-CHAIN-OV-02 | `active_tab=panorama` | 专业有向图谱（默认 L1）、面包屑、左上工具栏、左下图例 | 离开 Tab 保存当前产业内视口；切 L0 后恢复默认 L1 视口 |
| F-CHAIN-OV-03 | F-02 节点/关系点击或键盘激活 | 右侧固定对象详情；节点概览 +「下钻内部结构」+ 三 Tab；关系单页 | 选择其他对象直接替换内容；下钻替换图谱层级但不改 `industry_id` |
| F-CHAIN-OV-04 | F-02 产业链演进区 | 时间状态选择、变化标记、证据入口 | 切换状态不改变产业与视口 |
| F-CHAIN-OV-05 | `active_tab=news` | 类型/时间筛选、事件线、详情 | 关闭详情回原事件；切 Tab 保留当前产业 |
| F-CHAIN-OV-06 | `active_tab=profile` 上部 | 整链介绍、企业数、机构数 | 不受 F-02 节点选中影响 |
| F-CHAIN-OV-07 | `active_tab=profile` 主区 | 四级可搜索地域控件、地图/列表切换、地图左上工具栏 | 地图/列表共享地域路径、层级、筛选；返回上级显式操作 |
| F-CHAIN-OV-08 | `active_tab=history` | 阶段导航、里程碑、影响、证据 | 返回阶段列表时保持当前产业 |
| F-CHAIN-OV-09 | `active_tab=shenzhen` | 深圳指标、左 60% 地图/列表、右 40% 特色研判 | 两视图共享深圳区级选择；切 Tab 保持当前产业 |
| F-CHAIN-OV-10 | 页面顶部加入/移出动作 | 共享对比篮、`industry` 域 | 状态更新后停留当前总览上下文；浮层从系统入口另行打开 |

所有 Frame 的加载、成功、空、局部空、错误、受限或未发布状态都在原宿主内替换内容，不通过页面跳转规避状态。

## 5. 交互与状态转换

### 5.1 全局对象与 Tab

1. 首次进入：若入口 `industry_id`（L0）有效，直接加载；否则显示轻量说明后使用后台配置的默认推荐 L0 产业；旧 `chain_id` 只读兼容解析。
2. 展开产业下拉：仅列 L0；支持名称和别名检索、键盘上下选择与 Enter 确认；无结果时保留输入和当前产业。
3. 确认切换 L0：先提交新 `industry_id`，保留 `active_tab`，清除下钻栈、节点、关系、演进时间、详情 Tab、资讯筛选、地域路径和深圳区级选择，右栏回到操作引导空态，再进入新产业加载态；请求失败则回滚旧产业并给出重试。
4. 切换 Tab：只改变 `active_tab`；不得产生第二个对象选择器。返回全景时恢复同产业最后视口，切换过 L0 后不恢复旧产业状态。
   - `CHAIN-OV-F02-PANORAMA-REQ` 固定挂在顶部“产业链全景”Tab 文案右侧；全景内容区标题使用“`{L0产业名称}产业链全景`”，例如“集成电路产业链全景”。
5. 权限分级：权限 L0 可浏览总览（含默认 L1 结构）；权限 L0 触发主体明细下钻或加入/移出对比篮时进入登录并保留上下文；权限 L1 可查看主体明细、加入/移出对比篮；权限 L2 可在全局篮选择并发起分析；权限 L3 承载敏感明细和高级配置。
6. 加入/移出篮：权限 L1 及以上成功后只改变当前 L0 的篮内状态（`industry` 域），不跳转；重复加入保持幂等，不创建匿名本地篮。
7. 查看全局篮：总览不提供打开按钮、不写入打开信号；用户操作系统悬浮入口，系统浮层读取共享篮状态并自行处理打开、关闭和异常反馈。

### 5.2 专业全景、对象详情、L1 默认与逐级下钻、产业链演进

- 图谱首屏默认同时可辨上游、中游、下游的 **L1 子链**、关系方向及关系业务语义；只展示当前一个 L0 产业下的结构，不把企业、技术、机构全部铺成首层节点，也不默认铺开 L2+ 工艺叶子。
- 全景内容区标题随 `industry_id` 更新为“`{L0产业名称}产业链全景`”；需求追溯入口不在该标题中重复出现，而是挂在顶部“产业链全景”Tab 旁。
- 全景常驻固定 60% 图谱 + 40% 对象详情，三档 medium 宽度均不拖拽、不折叠、不回退单栏；右栏独立滚动。未选择对象时显示标题“选择产业链环节”和点击节点/关系的操作引导。
- 图谱左上通用工具栏依次提供放大、缩小、复位、全屏；复位恢复当前演进状态默认视口并保留对象选择，全屏作用于完整双栏工作台且比例不变。图例固定在图谱左下角。
- 节点支持单击与 Enter/Space 激活；选中节点和一跳上下游强高亮，其他可达路径弱高亮，无关对象降噪。再次激活同一节点不取消选择，`node_id` 写入 URL。
- 节点态展示基础信息、简介与企业列表；若节点具备子结构，提供「下钻内部结构」。不提供核心技术、科研与服务机构、市场规模 Tab。
- 下钻：图谱替换为该层 nodes/edges；面包屑展示 `L0产业 › L1 › …`；可点任一级或「返回上一级」；下钻不改变顶部 `industry_id`，也不写入对比篮；切换 L0 清空下钻栈。
- 关系激活后右栏切换为无 Tab 的关系单页，展示名称、源/目标节点、语义解释、证据来源、更新时间和当前演进时间；点击图谱节点返回节点态，不提供返回、关闭、前后切换或面板内第二选择器。
- 门户全景**不提供**「产业链演进」控件；动态演进归专题全景。

### 5.3 整体概况与区域分布

- 整链介绍、企业数和机构数是 `industry_id` 级内容，不随图谱节点点选变化。
- 四级地域控件固定提供“全球 / 全国 / 区域 / 深圳”一级入口并支持搜索；默认全国省级。全球对象限 G20；全国可按省 → 市 → 区县下钻。
- 地图和列表是同一查询状态的两种表达，共享范围、层级、地域路径、筛选、排序基线与选中对象。列表“在地图中查看”切回地图并定位同一地域。
- 地图左上通用工具栏包含放大、缩小、复位、全屏；复位不在右侧重复出现。底图失败时自动保留列表入口；无数据不回退到其他地域。

### 5.4 资讯、历程与深圳现状

- 资讯筛选只影响资讯 Tab；事件详情至少呈现事件时间、报道时间、来源机构，以及原始报道链接或明确缺失状态。
- 发展历程按阶段组织里程碑、产业影响与证据，不复刻资讯事件线，也不承担产业链演进变化。
- 深圳现状先呈现三项指标，再以 60% 地图/列表 + 40% 区域特色研判固定分栏；研判只呈现特色优势、集群效应、竞争地位及来源/更新时间。
- 内容未发布时显示发布状态空态；前端不得编写替代研判、来源或报道链接。

## 6. 反馈与异常恢复

| 场景 | 即时反馈 | 恢复动作 | 保留内容 |
| --- | --- | --- | --- |
| 首次页加载 | 页面骨架；头部与 Tab 位置稳定 | 自动完成或重试 | 路由与入口参数 |
| 切链加载 | 顶部 Select 显示目标链，内容区骨架 | 失败回滚旧链并重试 | 原 `active_tab` |
| 检索无结果 | 下拉内空态，不清空当前对象 | 修改关键词或关闭下拉 | 当前链与页面状态 |
| 图谱整体失败 | 图谱宿主错误态与“重试” | 重试图谱 | Tabs、工具栏、当前链 |
| 关系服务失败 | 节点保留，关系层错误提示 | 重试关系层 | 阶段分区、视口、节点 |
| 对象详情局部缺失 | 对应详情 Tab 局部空态及更新时间 | 切详情 Tab 或选择其他对象 | 其他已成功详情 |
| 仅一个演进状态 | 说明“暂无历史演进数据”，不显示变化标记 | 继续浏览 | 当前状态 |
| 演进切换后节点失效 | 清除无效 `node_id`，右栏回操作引导并提示原节点已不存在 | 重新选择对象 | 当前链、演进时间和图谱视口 |
| 市场规模无来源 | 显示“暂无正式数据源” | 浏览其他字段 | 右栏其他内容 |
| 地图底图失败 | 地图错误态、列表仍可用 | 切列表或重试底图 | 地域路径与层级 |
| 当前地域无数据 | 地图与列表同范围空态 | 返回上级或换地域 | 当前选择路径 |
| 原始报道缺失 | 明确“原始报道链接缺失” | 返回事件线 | 事件详情其余内容 |
| 历程/研判未发布 | 未发布空态 | 切换其他 Tab | 当前链 |
| 未登录加入篮 | 登录提示并进入登录 | 登录后返回并重试 | `industry_id`、Tab、滚动位置 |
| 全局篮打开失败 | 非阻断消息与重试 | 再次触发 Shell 接口 | 页面全部业务状态 |
| 评审数据失败 | 对应评审浮层内失败与重试 | 只重试评审数据 | 业务内容和交互不变 |

加载按钮进入 loading 后禁用重复提交；可取消的请求在切换 L0 或卸载 Frame 时取消，过期响应不得覆盖新 `industry_id`。

## 7. 组件、键盘与无障碍

### 7.1 组件约束

| 场景 | 优先组件/模式 | 约束 |
| --- | --- | --- |
| L0 产业选择 | Arco 可检索 `Select` | 仅 L0；与企业查询所属产业同口径；名称/别名检索；无结果不改变当前值 |
| 五个页签 | Arco `Tabs` | 共享顶部对象上下文；Tab 内无对象切换 |
| 全景双栏 | CSS Grid / Flex + 固定比例 | 左图谱 60%、右对象详情 40%；不可拖拽、折叠；右栏独立滚动 |
| 下钻路径 | Arco `Breadcrumb` +「返回上一级」 | 展示 L0 › L1 › …；切换 L0 清空 |
| 节点详情 | 固定概览 +「下钻内部结构」+ Arco `Tabs` | 仅三个 Tab：关联企业、核心技术、科研与服务机构 |
| 关系详情 | 右侧单页详情容器 | 无 Tab、返回、关闭、前后切换和第二选择器 |
| 产业链演进 | Arco 可选择时间状态控件 | 可见命名统一；无独立对比按钮、模式或工作区 |
| 地域选择 | 企业分析同源四级可搜索级联控件 | 全球/全国/区域/深圳四入口；路径可读 |
| 地图/列表 | `Segmented` 或等价单选切换 | 同一数据状态、同层对象 |
| 图谱/地图工具 | 图标按钮组 | 必须有 Tooltip 与可访问名称 |
| 事件/阶段 | Timeline + 详情容器 | 当前项、时间与证据关系明确 |
| 全局篮 | 应用 Shell 既有浮层 | 总览只负责交接信号，不复制组件 |

### 7.2 键盘与焦点

- Tab 顺序遵循：当前 L0 产业 → 加入/移出 → 全局篮 → 五个 Tab → 当前内容区主控件 → 内容项。
- Select/级联控件支持方向键浏览、Enter 确认、Esc 关闭；关闭未确认检索时回到原值。
- Tabs 支持左右方向键切换，焦点可见；TabPanel 与 Tab 通过 `aria-controls` / `aria-labelledby` 关联。
- 图谱节点和关系均可键盘访问；Enter/Space 选择对象并更新右栏。图谱必须提供可聚焦的结构化文本/列表替代表达。
- 右栏不是模态层，不实行焦点锁定；对象激活后以 `aria-live=polite` 宣告详情已更新，Tab 顺序可从图谱继续进入右栏内容。
- 工具栏按钮、地图区域、列表行、事件与里程碑均有可见焦点；全屏退出后焦点返回全屏按钮。
- 浮层关闭后焦点返回其触发器；错误消息使用 `aria-live=polite`，阻断错误使用 `role=alert`。

### 7.3 ARIA、禁用与对比度

- 图标按钮均设置描述动作的 `aria-label`，不得只读图标名称；Tooltip 文案与动作一致。
- 加载区域设置 `aria-busy=true`；骨架不进入 Tab 序列。禁用按钮同时给出可见原因与 `aria-disabled`。
- 地图视觉信息必须可通过同层列表获取；颜色不是新增、退出、关系变化、上中下游的唯一编码。
- 文本、控件边界、焦点环和状态色遵守 `Design.md` 的对比度与语义色要求；评审标记不得覆盖业务控件命中区。

## 8. 响应式行为

| 画布宽度 | Shell 与网格 | 核心内容行为 |
| --- | --- | --- |
| 1920 | 侧栏 200px；Header 64px；主区 24 列、16px gutter | F-02/03 全景工作台及 F-09 均严格 60%/40% |
| 1680 | 侧栏保持展开或遵循用户已保存偏好；间距保持 16px | 顶部上下文控件可收缩；两处双栏仍为 60%/40% |
| 1440 | 侧栏折叠为 64px；业务主区不得横向溢出 | 全景仍固定 60%/40%；工具栏左上、图例左下；F-09 仍为 60%/40% |

- 本模块不启用 `small_reflow`，不定义移动端重排。
- 五个 Tab 名称、当前产业链、全局篮入口和主要操作在三档宽度均不得被隐藏。
- 图谱与地图可以内部缩放/平移，但页面本身不得因画布产生横向滚动。
- 全景全屏时完整双栏工作台进入全屏并保持 60%/40%；右栏滚动不得带动图谱区。

## 9. 内部评审投影

### 9.1 投影规则

- 严格复用 Wireframe 的 30 个 `mount_id`，不得新增、合并、迁移到统一右上角或全局评审侧栏。
- `requirement_trace` 紧邻对应模块标题或交互宿主，展开后显示每个 `trace_ref` 对应的来源位置、**完整需求原文**、当前落点和来源关系；编号或摘要不能替代原文。
- `metric_spec` 一次只展示一个指标，8 个字段各自独立成行并统一使用正文级字号：`metric_id`、`metric_name_zh`、`definition`、`formula`、`source_tables`、`source_systems`、`update_freq`、`version`。
- `mock_badge` 与 `pending_badge` 就地挂在各自业务宿主，不能写进业务标题、副标题或空态。评审模式关闭后，对应触发器、浮层和评审文案从 DOM 移除。

### 9.2 完整挂载清单

| Frame | requirement_trace | metric_spec | mock_badge | pending_badge |
| --- | --- | --- | --- | --- |
| F-CHAIN-OV-01 | CHAIN-OV-F01-CONTEXT-REQ | — | — | — |
| F-CHAIN-OV-02 | CHAIN-OV-F02-PANORAMA-REQ | — | — | — |
| F-CHAIN-OV-03 | CHAIN-OV-F03-NODE-REQ | CHAIN-OV-F03-MARKET-METRIC | CHAIN-OV-F03-MARKET-MOCK | CHAIN-OV-F03-MARKET-PENDING |
| F-CHAIN-OV-04 | CHAIN-OV-F04-EVOLUTION-REQ | — | — | CHAIN-OV-F04-EVOLUTION-PENDING |
| F-CHAIN-OV-05 | CHAIN-OV-F05-NEWS-REQ | — | — | — |
| F-CHAIN-OV-06 | CHAIN-OV-F06-PROFILE-REQ | CHAIN-OV-F06-ENT-METRIC；CHAIN-OV-F06-ORG-METRIC | CHAIN-OV-F06-ENT-MOCK；CHAIN-OV-F06-ORG-MOCK | — |
| F-CHAIN-OV-07 | CHAIN-OV-F07-DIST-REQ | CHAIN-OV-F07-ENT-METRIC；CHAIN-OV-F07-ORG-METRIC | CHAIN-OV-F07-ENT-MOCK；CHAIN-OV-F07-ORG-MOCK | CHAIN-OV-F07-DIST-PENDING |
| F-CHAIN-OV-08 | CHAIN-OV-F08-HISTORY-REQ | — | — | CHAIN-OV-F08-HISTORY-PENDING |
| F-CHAIN-OV-09 | CHAIN-OV-F09-SZ-REQ | CHAIN-OV-F09-ENT-METRIC；CHAIN-OV-F09-ORG-METRIC；CHAIN-OV-F09-REGION-METRIC | CHAIN-OV-F09-ENT-MOCK；CHAIN-OV-F09-ORG-MOCK；CHAIN-OV-F09-REGION-MOCK | CHAIN-OV-F09-CONTENT-PENDING |
| F-CHAIN-OV-10 | CHAIN-OV-F10-BASKET-REQ | — | — | — |

禁止位置：页面主标题、固定右上角、统一指标说明浮层、统一评审按钮或与宿主无关的悬浮侧栏。业务数据自身的来源、更新时间、版本和原始报道链接不是评审层，业务模式仍应显示。

## 10. Demo 实施交接

### 10.1 实现分层

- 页面域只维护 `industry_id`（L0）、`active_tab`、`drill_stack`、各 Tab 局部状态及全局篮交接；切换 L0 是清理局部状态的唯一全局对象变更。
- 图谱、地图、地域控件、固定双栏、Tabs、时间状态控件、MetricSpecCard、MockBadge、PendingBadge 与 ReviewTrace 优先复用系统共享机制，但产业节点、关系、指标和内容契约必须来自本模块四件套。
- 总览只向 `industry` 对象域写入加入/移出状态，不发送浮层打开信号；全局篮的视图、入口、权限与分析逻辑全部由系统组件负责。
- 评审挂载以 `mount_id` 为唯一键，并由同一登记表驱动渲染与自动化断言；不得将说明文本硬编码进业务组件。

### 10.2 V1 数据处理

- M_CHAIN_MARKET_SIZE 显示“暂无正式数据源”，不生成数字或排名。
- 地域使用固定可回放地域树与 Mock ADS 快照；全球严格限制为 G20，全国可下钻至区县。
- 资讯、历程和深圳特色仅消费固定已发布演示内容快照，并保留 `source_url`、`source_name`、`published_at`、`content_version`。
- 全景默认 L1 子链 Mock；至少「半导体设备」「晶圆制造」具备可下钻子结构样例。
- 产业链演进使用两个固定已发布状态和确定性变化标记，不宣称实时，不实现独立对比工作区。
- 权限直接继承全系统基线：权限 L0 浏览，权限 L1 主体明细与对比篮，权限 L2 选择并发起分析，权限 L3 敏感明细与高级配置；未登录操作受限能力时进入登录并返回原上下文。

### 10.3 实施验收焦点

- 10 个 Frame 均具有加载、成功及适用的空/错/受限状态；切换 L0 不会出现旧产业响应覆盖，且下钻栈被清空。
- 默认图谱为 L1；可下钻节点进入更深层级后面包屑可返回。
- 三档宽度无页面横向溢出；全景与深圳区块均固定 60%/40%；图谱工具栏左上、图例左下；全景全屏覆盖完整双栏。
- 评审挂载逐一在正确宿主出现，业务模式逐一不存在；需求完整原文、单指标 8 件套与 D1–D4 readiness 状态均可读。
- 指针、键盘、焦点回归、ARIA、地图列表等价表达均通过验证。

本文 `ready_for_v1` 只表示 UX-SPEC 已具备进入 V1 高保真实现交接的结构条件；是否启动 Demo 仍需按 `gkx-definition-to-demo` 和任务治理流程另行执行，不由本文件自动激活。

## 11. 缺口与阻断项

| 缺口 | 阻断阶段 | V1 处理 | Owner / 回流 |
| --- | --- | --- | --- |
| GAP-CHAIN-OV-MARKET-SOURCE / Q056 | pdr、v1_final、v2_lumen、production | 显示“暂无正式数据源”；评审挂 Pending，不生成排名 | human:何老师 / TRACE / before_pdr |
| GAP-CHAIN-OV-REGION-DATA / Q060 | pdr、v1_final、v2_lumen、production | 固定地域树 + Mock ADS；不宣称真实全量 | human:徐滕强 / architecture / before_pdr |
| GAP-CHAIN-OV-CONTENT-CONTRACT / Q061 | pdr、v1_final、v2_lumen、production | 固定已发布快照并保留来源元数据；不硬编码伪来源 | human:侯佳伟 / backend / before_pdr |
| GAP-CHAIN-OV-EVOLUTION-EVIDENCE / Q062 | pdr、v1_final、v2_lumen、production | 两个固定已发布状态 + 确定性变化标记；不宣称实时、不建独立对比工作区 | human:唐绍祖 / architecture / before_pdr |
V1 阻断项：无。以上四项均 `blocks_v1: false`，但在进入 PDR、V1-FINAL、V2 或生产前必须回流至指定权威层闭合；Q063 已按全系统权限基线闭合，不再构成产业链专项缺口。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-PORTAL-OVERVIEW-产业链总览
  version: v1.5-portal-panorama-scope
  status: ready_for_v1
  delivery_stage: v1_hifi_round1
  screen_tier: medium_1440_1920
  route: /industry-center/overview
  primary_param: industry_id
  industry_level_default: L0
  panorama_default_level: L1
  compare_basket_object: industry
  decision_ref: DEC-CHAIN-PORTAL-OVERVIEW-L0-L1-20260806
  product_scope_mutation: prohibited
  source_four_pack:
    - IA-CHAIN-PORTAL-OVERVIEW-产业链总览.md
    - TRACE-CHAIN-PORTAL-OVERVIEW-产业链总览.yaml
    - USM-CHAIN-PORTAL-OVERVIEW-产业链总览.md
    - Wireframe-CHAIN-PORTAL-OVERVIEW-产业链总览.md
  journeys:
    - journey_id: J-CHAIN-OV-GOV
      role: 政府产业管理与决策人员
      story_refs: [US-CHAIN-OV-01, US-CHAIN-OV-02, US-CHAIN-OV-06, US-CHAIN-OV-07, US-CHAIN-OV-09, US-CHAIN-OV-10, US-CHAIN-OV-11]
      primary_flow: [确定当前L0, 浏览默认L1全景, 逐级下钻, 查看整链概况, 检索地域并切换地图列表, 查看深圳现状, 加入共享产业对比篮, 按需从系统入口打开全局篮]
      abnormal_flows: [无效对象回退默认L0, 地图失败切列表, 未登录先登录后返回, 系统篮异常由系统入口反馈]
    - journey_id: J-CHAIN-OV-INVEST
      role: 投资机构产业研究人员
      story_refs: [US-CHAIN-OV-01, US-CHAIN-OV-04, US-CHAIN-OV-05, US-CHAIN-OV-08]
      primary_flow: [确定当前L0, 选择产业链演进时间, 在原图谱查看变化, 在右栏查看证据, 筛选资讯, 打开原始报道, 按阶段查看发展历程]
      abnormal_flows: [单一演进状态显示无历史数据, 证据失败保留图谱, 原始报道缺失明确标记, 内容未发布显示空态]
    - journey_id: J-CHAIN-OV-COLLAB
      role: 企业战略与产业合作人员
      story_refs: [US-CHAIN-OV-01, US-CHAIN-OV-02, US-CHAIN-OV-03, US-CHAIN-OV-11]
      primary_flow: [确定当前L0, 识别L1子链关系, 激活节点, 浏览固定概览和三类详情, 下钻内部结构, 激活关系查看语义证据]
      abnormal_flows: [局部详情缺失不影响其他详情, 关系失败保留节点, 市场规模无来源显示不可用]
  frame_specs:
    - frame_id: F-CHAIN-OV-01
      route_or_host: /industry-center/overview#context-and-tabs
      source_refs: [US-CHAIN-OV-01, US-CHAIN-OV-10]
      states: [initial, loading, ready, search_empty, switch_error, auth_required]
      interactions: [search_l0_industry, switch_l0_industry, switch_tab, add_or_remove_basket]
    - frame_id: F-CHAIN-OV-02
      route_or_host: /industry-center/overview?tab=panorama#graph
      source_refs: [US-CHAIN-OV-02, US-CHAIN-OV-11]
      states: [loading, ready, empty, graph_error, relation_error, drilled]
      interactions: [zoom_in, zoom_out, reset_view, toggle_fullscreen, select_node, focus_relation, drill_down, breadcrumb_return]
    - frame_id: F-CHAIN-OV-03
      route_or_host: F-CHAIN-OV-02#object-detail-panel
      source_refs: [US-CHAIN-OV-03, US-CHAIN-OV-11]
      states: [guidance_empty, node_loading, node_ready, relation_loading, relation_ready, partial_empty, error]
      interactions: [select_node, select_relation, switch_detail_tab, drill_internal_structure, retry_detail]
    - frame_id: F-CHAIN-OV-04
      route_or_host: /industry-center/overview?tab=panorama#evolution
      source_refs: [US-CHAIN-OV-04]
      states: [loading, current_only, comparable, evidence_error]
      interactions: [select_evolution_time, inspect_change, open_evidence]
    - frame_id: F-CHAIN-OV-05
      route_or_host: /industry-center/overview?tab=news
      source_refs: [US-CHAIN-OV-05]
      states: [loading, ready, empty, detail_open, source_missing, error]
      interactions: [filter_type, filter_time, open_event, open_source, close_event]
    - frame_id: F-CHAIN-OV-06
      route_or_host: /industry-center/overview?tab=profile#summary
      source_refs: [US-CHAIN-OV-06]
      states: [loading, ready, partial_empty, error]
      interactions: [inspect_summary, inspect_enterprise_metric, inspect_institution_metric]
    - frame_id: F-CHAIN-OV-07
      route_or_host: /industry-center/overview?tab=profile#region-distribution
      source_refs: [US-CHAIN-OV-07]
      states: [loading, map_ready, list_ready, empty, basemap_error, data_error]
      interactions: [search_region, drill_region, return_parent, switch_map_list, locate_on_map, reset_map, toggle_fullscreen]
    - frame_id: F-CHAIN-OV-08
      route_or_host: /industry-center/overview?tab=history
      source_refs: [US-CHAIN-OV-08]
      states: [loading, ready, unpublished, evidence_error]
      interactions: [select_stage, select_milestone, open_evidence, return_stage_list]
    - frame_id: F-CHAIN-OV-09
      route_or_host: /industry-center/overview?tab=shenzhen
      source_refs: [US-CHAIN-OV-09]
      states: [loading, ready, map_ready, list_ready, partial_empty, unpublished, error]
      interactions: [inspect_metrics, switch_map_list, select_district, inspect_findings, open_source]
    - frame_id: F-CHAIN-OV-10
      route_or_host: /industry-center/overview#compare-basket-action
      source_refs: [US-CHAIN-OV-10]
      states: [not_in_basket, in_basket, auth_required, update_error]
      interactions: [add_current_industry, remove_current_industry, preserve_page_context]
  feedback_rules:
    - loading_keeps_layout_stable
    - industry_switch_error_rolls_back_previous_industry
    - stale_response_cannot_overwrite_current_industry
    - industry_switch_clears_drill_stack
    - local_failure_does_not_clear_sibling_content
    - unavailable_source_is_explicit_and_never_fabricated
    - map_failure_preserves_equivalent_list
    - review_failure_never_blocks_business_content
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, map_list_equivalence, color_independence]
  permission_contract:
    exception_policy: none
    L0_GUEST: [view_overview]
    L1_REGISTERED: [view_overview, drill_node_detail, add_or_remove_compare_basket]
    L2_PRO: [L1_capabilities, select_analysis_type, start_analysis]
    L3_INTERNAL: [L2_capabilities, view_sensitive_detail, advanced_configuration]
    unauthorized_behavior: fail_closed_with_login_or_upgrade_guidance_and_context_preservation
  metric_readiness_projection:
    - metric_id: M_CHAIN_MARKET_SIZE
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-03
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness, pending_ref, v1_behavior]
    - metric_id: M_CHAIN_ENTERPRISE_COUNT
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-06
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness]
    - metric_id: M_CHAIN_INSTITUTION_COUNT
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-06
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness]
    - metric_id: M_CHAIN_SZ_ENTERPRISE_COUNT
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-09
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness]
    - metric_id: M_CHAIN_SZ_INSTITUTION_COUNT
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-09
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness]
    - metric_id: M_CHAIN_SZ_REGION_COUNT
      matrix_ref: agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml
      frame_id: F-CHAIN-OV-09
      dimensions: [def_status, schema_status, source_mapping_status, ingestion_status]
      marker_order: [definition, structure, source_mapping, ingestion]
      entry_marker_groups: [definition, data_health, ingestion]
      data_health_dimensions: [schema_status, source_mapping_status]
      data_health_component: DataHealthBadge
      data_health_popover_rows: [structure, source_mapping]
      max_markers: 3
      spacing_px: 4
      activation: [pointer, keyboard]
      required_payload: [metric_id, readiness]
  review_mounts:
    - CHAIN-OV-F01-CONTEXT-REQ
    - CHAIN-OV-F02-PANORAMA-REQ
    - CHAIN-OV-F03-NODE-REQ
    - CHAIN-OV-F03-MARKET-METRIC
    - CHAIN-OV-F03-MARKET-PENDING
    - CHAIN-OV-F03-MARKET-MOCK
    - CHAIN-OV-F04-EVOLUTION-REQ
    - CHAIN-OV-F04-EVOLUTION-PENDING
    - CHAIN-OV-F05-NEWS-REQ
    - CHAIN-OV-F06-PROFILE-REQ
    - CHAIN-OV-F06-ENT-METRIC
    - CHAIN-OV-F06-ENT-MOCK
    - CHAIN-OV-F06-ORG-METRIC
    - CHAIN-OV-F06-ORG-MOCK
    - CHAIN-OV-F07-DIST-REQ
    - CHAIN-OV-F07-ENT-METRIC
    - CHAIN-OV-F07-ENT-MOCK
    - CHAIN-OV-F07-ORG-METRIC
    - CHAIN-OV-F07-ORG-MOCK
    - CHAIN-OV-F07-DIST-PENDING
    - CHAIN-OV-F08-HISTORY-REQ
    - CHAIN-OV-F08-HISTORY-PENDING
    - CHAIN-OV-F09-SZ-REQ
    - CHAIN-OV-F09-ENT-METRIC
    - CHAIN-OV-F09-ENT-MOCK
    - CHAIN-OV-F09-ORG-METRIC
    - CHAIN-OV-F09-ORG-MOCK
    - CHAIN-OV-F09-REGION-METRIC
    - CHAIN-OV-F09-REGION-MOCK
    - CHAIN-OV-F09-CONTENT-PENDING
    - CHAIN-OV-F10-BASKET-REQ
  gaps:
    - id: GAP-CHAIN-OV-MARKET-SOURCE
      summary: M_CHAIN_MARKET_SIZE 无正式来源且口径未定
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 显示暂无正式数据源并挂载 Pending Q056，不生成数字或排名
    - id: GAP-CHAIN-OV-REGION-DATA
      summary: G20 和全国省市区县地域与聚合数据契约未闭合
      owner: human:徐滕强
      deadline: before_pdr
      return_to: architecture
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 使用固定可回放地域树和 Mock ADS 快照，不宣称真实全量
    - id: GAP-CHAIN-OV-CONTENT-CONTRACT
      summary: 资讯历程与深圳特色内容发布和来源契约未闭合
      owner: human:侯佳伟
      deadline: before_pdr
      return_to: backend
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 仅消费固定已发布内容快照并保留来源元数据，不硬编码伪来源
    - id: GAP-CHAIN-OV-EVOLUTION-EVIDENCE
      summary: 产业链演进状态、变化枚举与证据指针契约未闭合
      owner: human:唐绍祖
      deadline: before_pdr
      return_to: architecture
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 使用两个固定已发布状态和确定性变化标记并挂载 Pending Q062，不宣称实时，不实现独立对比工作区
```
