# UX-SPEC-CHAIN-TOPIC-ANALYSIS｜专题侧产业链分析

> **2026-08-04 能力拆分通知**：全景图谱交互已迁移至 `../CHAIN-TOPIC-PANORAMA-产业链全景图谱/UX-SPEC-CHAIN-TOPIC-PANORAMA.md`。本文件的全景相关段落仅作历史追溯，禁止作为并行实施规格。  
> **2026-08-05 能力拆分通知**：区域产业评价交互已迁移至 `../CHAIN-TOPIC-REGIONAL-区域产业评价/UX-SPEC-CHAIN-TOPIC-REGIONAL.md`。本文件的 F-07/F-08 与区域相关旅程段落仅作历史追溯，禁止作为并行实施规格。  
> **2026-08-05 能力拆分通知（续）**：深圳产业决策交互已迁移至 `../CHAIN-TOPIC-SHENZHEN-深圳产业决策/UX-SPEC-CHAIN-TOPIC-SHENZHEN.md`。本文件的 F-09/F-10 与深圳相关旅程段落仅作历史追溯，禁止作为并行实施规格。  
> **2026-08-05 能力拆分通知**：产业运行诊断交互已迁移至 `../CHAIN-TOPIC-DIAGNOSIS-产业运行诊断/UX-SPEC-CHAIN-TOPIC-DIAGNOSIS.md`。本文件的 F-04/F-05/F-06 与诊断相关旅程段落仅作历史追溯，禁止作为并行实施规格。

> 版本：v0.6-ready-for-v1  
> 状态：ready_for_v1  
> 四件套版本：IA v0.9 / TRACE v0.7 / USM v0.7 / Wireframe v0.6  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> 阶段说明：交互规格已覆盖全部故事、Frame 和评审挂点；marker overflow 已由 `DEC-D9-DATA-HEALTH-GROUPING-20260803` 关闭，允许作为 V1 高保真首轮输入，但不代表 PDR/Gate、任务、提交、推送或部署状态。

## 1. 权威输入与边界

### 1.1 产品行为真源

| 工件 | 当前版本 | 本 UX-SPEC 的使用方式 |
| --- | --- | --- |
| `IA-CHAIN-TOPIC-ANALYSIS.md` | v0.9-core-package | 模块边界、入口、对象身份、路由、共享能力边界和跨页上下文 |
| `TRACE-CHAIN-TOPIC-ANALYSIS.yaml` | 0.7-core-package | 20 条故事、12 个 Frame、七类阶段注册、依赖、gap 和阶段状态 |
| `USM-CHAIN-TOPIC-ANALYSIS.md` | v0.7-core-package | 三类产品角色、主异常路径、验收场景和统一分析旅程 |
| `Wireframe-CHAIN-TOPIC-ANALYSIS.md` | v0.6-core-package | Frame 结构、字段、状态、禁止行为、21 个评审挂点和屏幕约束 |

### 1.2 适用规范

- `agent-delivery/产品定义评审规程.md`：Track-MS 的 UX、V1 首轮、PDR、联合修订冻结和 V2 边界。
- `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`：Arco 组件语义、上下文保持、反馈、键盘和无障碍合同。
- `agent-delivery/Design.md`：浅蓝白 PC 工作台、24 栅格、16px gutter、64px Header、200/64px Sidebar 和视觉 token。
- `agent-delivery/data-lineage-policy.md`：D1–D4、评审标识顺序、Popover payload 与业务模式隐去规则。
- `agent-delivery/metrics/metric-readiness-matrix-CHAIN.yaml`：仅为 `CHAIN-PORTAL-OVERVIEW` 真源，不得投射为本专题模块的指标状态。

### 1.3 不可越界项

- `product_scope_mutation: prohibited`：不新增角色、故事、字段、路由、权限、指标含义、任务状态或报告能力。
- `demo_code_mutation: prohibited`：本文只形成交互合同，不修改 Demo、任务注册、Gate、`delivery_tier` 或部署状态。
- 企业评估现有实现和用户截图仅作为交互证据；本模块只复用 Config / Processing / Result 页面壳层、状态反馈与动作顺序，不复用企业字段、指标、阶段文案、图表和结论。
- 系统对比篮为任意页面可打开的全局浮层；任何专题 Frame 都不得增加“打开对比篮”按钮。
- 门户产业总览、技术链分析、产业查询导出、结果/报告收藏、独立产业任务中心和执行管理均不进入本 UX-SPEC。

## 2. 四件套同步核对

### 2.1 故事覆盖

| 故事组 | Story ID | UX 落点 |
| --- | --- | --- |
| 对象准备 | `US-CHAIN-TOPIC-01` | F-01 查询、同类型选择、加入全局篮和摘要抽屉 |
| 全景认知 | `US-CHAIN-TOPIC-02/03` | F-02 完整图谱、F-03 节点详情、双快照与时间轴 |
| 周期分析 | `US-CHAIN-TOPIC-04/05` | F-04 配置、统一过程、不可变周期结果 |
| 关键环节 | `US-CHAIN-TOPIC-06/07` | F-05 固定因子确认、统一过程、关键环节结果 |
| 瓶颈堵点 | `US-CHAIN-TOPIC-08/09` | F-06 固定维度确认、统一过程、归因结果 |
| 区域指数 | `US-CHAIN-TOPIC-10/11` | F-07 对象/指标/权重/预览、统一过程、指数结果 |
| 区域竞争力 | `US-CHAIN-TOPIC-12/13` | F-08 三维权重、统一过程、排名与短板 |
| 深圳对比 | `US-CHAIN-TOPIC-14/15` | F-09 深圳与标杆配置、统一过程、对比结果 |
| 深圳发展 | `US-CHAIN-TOPIC-16/17` | F-10 来源结果与目标配置、统一过程、建议与路径 |
| 任务恢复与历史 | `US-CHAIN-TOPIC-18/19` | F-11 阶段 Steps、恢复、queued 撤回、历史复制 |
| 报告交接 | `US-CHAIN-TOPIC-20` | F-12 生成、任务反馈、只读阅读与同源 PDF |

覆盖结论：20/20 条故事均有 Frame、主路径、异常恢复和机器契约引用；未新增 Story ID。

### 2.2 Frame、路由与关键状态

| Frame | 路由 / 宿主 | 必需状态 | 核心禁止行为 |
| --- | --- | --- | --- |
| F-01 | `/industry-center/search?mode=smart\|industry\|advanced` | recommendation/default/loading/empty/error/permission/type_locked/partial_add | 混选对象、暗选跨页、直接发起分析、页内篮按钮、导出 |
| F-02 | `/industry-center/panorama` | default/loading/empty/error/permission/single/dual/timeline | 折叠正式环节、节点成为分析主对象、视口操作触发重算 |
| F-03 | F-02 右栏与演进区 | default/loading/empty/error/permission/incompatible_snapshot | 丢失画布上下文、伪造变化、技术分析假入口 |
| F-04 | `/industry-center/diagnosis?tab=cycle` | object_empty/draft/validating/processing/result/expired/error/permission | chain 对象提交、原位改结果、自动跳结果 |
| F-05 | `/industry-center/diagnosis?tab=key-link` | 同 F-04 | 编辑固定因子、无意义模板、直接发起企业分析 |
| F-06 | `/industry-center/diagnosis?tab=bottleneck` | 同 F-04 | 静默删维度、自定阈值、扩展执行管理 |
| F-07 | `/industry-center/regional?tab=index` | 同 F-04，另含 preview | 多产业×多区域、静默归一化、创建/删除指标、预览入历史 |
| F-08 | `/industry-center/regional?tab=competitiveness` | 同 F-04 | 改成两维模型、新增维度、混排不同版本 |
| F-09 | `/industry-center/shenzhen?tab=comparison` | 同 F-04 | 更换深圳主体、自动填标杆、静默删不利标杆 |
| F-10 | `/industry-center/shenzhen?tab=development` | 同 F-04 | PDF 作输入、自动继承最近结果、自动运行、补造路径 |
| F-11 | `/industry-center/tasks/:taskId`；各工作空间 `tab=records` | created/prechecking/queued/running/succeeded/failed/withdrawn/terminated/empty/error/permission | running 取消、原位重跑、复用 task_id、自动打开最近结果 |
| F-12 | `/industry-center/reports/:reportId` | not_generated/generating/ready/failed/expired/permission | 过期结果生成报告、报告重算结论、收藏/编辑、修订不一致 |

### 2.3 差异结论

- 四件套内部一致：`screen_tier=medium_1440_1920`、`delivery_stage=v1_hifi_round1`、12 个 Frame、20 条故事、21 个唯一挂点。
- 本模块仍没有专题侧正式 `M_CHAIN_*` 清单和 readiness matrix；现有 CHAIN 矩阵只覆盖门户。
- D1–D4 已采用批准的三组入口投影：D1 独立、D2+D3 合并为一个 `DataHealthBadge` 且 Popover 分两行、D4 独立；因此不存在入口超过三枚或静默隐藏维度的问题。

## 3. 用户旅程与任务流

### 3.1 J-CHAIN-GOV｜政府决策分析闭环

故事：`US-CHAIN-TOPIC-03/04/05/08/09/10/11/14/15/16/17/18/20`。

主路径：

1. 从专题导航或有效深链进入对应工作空间；通过系统全局篮原位选择兼容对象，配置页形成草稿。
2. 完成当前分析专属配置，点击“生成分析”；按钮进入 loading，服务端校验成功后创建唯一 `task_id`。
3. 进入 F-11 可视化过程：读取任务摘要、当前 `analysis_type` 的六段 Steps 与阶段说明；离页后任务继续。
4. `succeeded` 后页面保持完成态，用户点击“查看结果”进入对应 F-04～F-10 的只读结果。
5. 结果展示对象、配置、模型、数据和生成时间身份；有效且有权时点击“生成报告”进入 F-12。

异常恢复：配置校验失败保留草稿并聚焦首个错误；同 Tab 有任务时恢复原任务；queued 可二次确认撤回；running 无取消入口；失败只能复制配置新建；过期结果只读且禁新正式报告；报告能力未激活时保留结果阅读。

退出与恢复：离开 processing 不终止任务；从系统任务浮层或 `/tasks/:taskId` 恢复正确页面、Tab、对象和只读快照。关闭结果或报告后返回来源上下文，不覆盖未提交草稿。

### 3.2 J-CHAIN-PARK｜园区全景、环节与区域评价

故事：`US-CHAIN-TOPIC-01/02/03/06/07/12/13/18/19`。

主路径：

1. 在 F-01 初次进入、切换普通模式或清空条件时先看到带理由的确定性推荐产业；普通检索条件与推荐/结果之间显示当前模式的最近检索。点击“高级筛选”进入同路由独立高筛页，点击热门产业则携带对应父级产业条件进入该页，用户确认并应用后才执行查询。推荐态不显示复选框或批量工具栏，通过单卡查看摘要、进入全景图谱和加入对比篮操作；零命中保持空态；检索结果态由首个勾选锁定类型，并支持全选本页和批量加入对比篮。卡片与对象摘要抽屉跳转统一为「进入全景图谱」，不再提供去门户总览。
2. 进入 F-02 浏览完整链条，选择节点后 F-03 展示绑定快照的详情；必要时切双快照或时间轴。
3. 发起关键环节或区域竞争力分析时，完成只读因子/三维权重配置，经过统一过程后显式查看结果。
4. 从分析记录查看历史或复制配置创建新草稿；旧记录和原任务保持不可变。

异常恢复：混选类型时拒绝冲突项但保留已选项；详情失败只重试右栏；快照不兼容保留单点视图；固定因子/维度不可用时禁止提交；不同版本排名不得混排。

退出与恢复：查询、图谱视口、选中节点、Tab、筛选和历史列表位置分别保存；跨二级页面不得静默传递对象或配置。

### 3.3 J-CHAIN-ENTERPRISE｜企业战略只读认知

故事引用：`US-CHAIN-TOPIC-02/03`；有效结果或报告链接按 `US-CHAIN-TOPIC-05/07/09/11/13/15/17/20` 的既有只读合同消费，不改变这些故事的主角色和验收范围。

主路径：从产业或产业链入口浏览完整结构和演进；在已获授权的结果/报告链接中阅读上下游、技术路径、区域布局与合作位置；打开企业详情时使用共享抽屉并保持产业上下文。

异常恢复：对象或链接无权时失败关闭且不泄露摘要；企业敏感字段按服务端结果裁剪；技术路线只作产业链上下文，不出现技术对象入篮或技术分析入口。

退出与恢复：关闭共享企业抽屉后焦点回到触发卡片，节点、快照和图谱视口不变；报告返回来源结果，不改系统篮。

### 3.4 七项计算型分析统一任务流

```text
object_empty
  → draft
  → validating
  → created → prechecking → queued → running
  → succeeded → 用户点击查看结果 → result_readonly
  → 用户点击生成报告 → report_handoff
```

分支：`validating → draft`；`queued → withdrawn`；`created/prechecking/queued/running → failed|terminated`。终态不得原位重跑；复制配置必须重新校验并产生新 `task_id`。

## 4. Frame 与承载映射

| Frame | 入口与宿主 | 主要控件 / 触发 | 出口 | 反馈与恢复 | 上下文保持 |
| --- | --- | --- | --- | --- | --- |
| F-01 | 导航进入产业查询；普通页点击高级筛选或热门产业进入同路由下级高筛页 | 普通页模式 Tabs、关键词、搜索框下方可关闭 SmartChip、热门产业与结果上方最近检索；独立高筛页字段库、条件编辑、AND/OR、方案与应用；推荐/结果卡：查看摘要、进入全景图谱、加入对比篮；结果态 Checkbox、全选本页、批量加入对比篮；摘要抽屉：关闭、加入对比篮、进入全景图谱 | 返回产业查询、F-02（统一全景出口）、系统篮 | SmartChip 移除后按剩余关键词重算；最近检索点击恢复并重跑、清除回空态；热门产业只预置条件并等待应用；初始推荐；卡片 Skeleton；已执行查询空态建议调整或清空条件；部分加入逐项反馈；不可用/权限受限禁用进入全景图谱 | `source/sourceSearch` 保留返回地址；`preset` 保留热门条件；最近检索本地 30 天、按标题去重、最多 10 条并按当前模式过滤；保留输入文本、当前 SmartChip、模式、分页、滚动和选中项；抽屉关闭回触发卡；全景跳转携带 `object_type`/`object_id` 与查询返回上下文 |
| F-02 | 导航、产业/产业链对象深链 | 单点/双快照/时间轴、节点、缩放/适配/复位 | F-03 详情；返回来源 | 画布固定尺寸；无结构与快照错误分开；节点详情失败不清画布 | 对象、快照、视口、节点选择独立保存 |
| F-03 | F-02 节点点击或演进模式 | 详情 Tabs、企业卡、共享企业抽屉、快照选择、播放/暂停 | 关闭详情、回单点、共享企业抽屉 | 右栏 Skeleton/Empty/Error；不兼容快照保持原视图 | `node_id+chain_id+snapshot_id` 三重绑定；关闭回触发点 |
| F-04 | 诊断 `tab=cycle` | 参数表单、预测窗口、生成分析、查看配置、查看结果、生成报告 | F-11、周期结果、F-12 | 表单内联校验；过程恢复；过期 Alert | 草稿与结果身份隔离；结果不可变 |
| F-05 | 诊断 `tab=key-link` | 固定因子只读区、生成分析、环节选择、企业抽屉 | F-11、关键环节结果、F-12 | 模型不可用禁用生成；无关键环节为业务空态 | 保留完整链条与当前环节；企业抽屉不改结果 |
| F-06 | 诊断 `tab=bottleneck` | 固定维度确认、生成分析、健康图/矩阵选择、生成报告 | F-11、瓶颈结果、F-12 | 必需维度缺失阻止提交；部分证据显示局限 | 结果与模型/数据版本绑定 |
| F-07 | 区域 `tab=index` | 产业/区域选择、指标勾选、权重输入、一键均分、轻量预览、生成分析 | F-11、指数结果、F-12 | 组合/权重错误定位；预览独立 loading；自定义指标 gap 可见 | Tab 间不共享区域/权重/模板；预览不入任务历史 |
| F-08 | 区域 `tab=competitiveness` | 对象组合、固定三维、一级权重、一键均分、生成分析 | F-11、竞争力结果、F-12 | 三维缺失禁用；版本不一致拒绝混排 | 对象可兼容共享，权重与结果焦点隔离 |
| F-09 | 深圳 `tab=comparison` | 固定深圳、产业、标杆多选、四维只读、就绪矩阵、生成分析 | F-11、对比结果、F-12、F-10 来源选择 | 无有效标杆禁用；不可用标杆保留原因 | 深圳固定；标杆、模型和结果快照绑定 |
| F-10 | 深圳 `tab=development` | 来源结果 Select、目标确认、生成分析、路径切换、证据展开 | F-11、发展结果、F-12 | PDF/过期/跨产业/无权结果不可选；不足两路径标不完整 | 来源结果显式选择；不继承最近结果 |
| F-11 | 任务深链或各工作空间记录 Tab | Steps、当前阶段 Alert、撤回 Popconfirm、查看结果、复制配置、历史筛选 | 来源 Tab、结果、复制草稿 | 后台 Notification；失败/终止/撤回可复制；空历史 Empty | 服务端 `task_id` 为真源；恢复所属页面/Tab/快照 |
| F-12 | 有效结果的生成报告动作或报告深链 | 生成报告、查看任务、查看报告、下载 PDF、返回来源 | 来源结果、报告任务、只读阅读器 | 生成中 Notification；失败可重试；过期/无权失败关闭 | `source_task_id+source_result_id+report_revision_id` 固定 |

F-01 可见页头：“产业查询”标题和说明整体仅评审态显示；业务态折叠该行并直接进入查询主区。该已确认例外只改变评审说明占位，不得改变查询字段、操作、结果或权限。

F-01 高筛导航：高级筛选 Tab 使用真实导航进入 `mode=advanced` 独立页面；热门产业按钮使用同一导航并附加稳定 `preset`，落页后将对应父级产业条件显示为可编辑条件。高筛直接复用企业查询的 `FilterPanel` 页面结构与交互：左侧内置字段库按产业分组展示“对象类型、父级产业、所属领域、对象来源、可用状态”，右侧为条件编辑区，并保留字段搜索、推荐字段标识、展开/收起、AND/OR、保存/使用查询方案、清空、应用和结果态编辑；仅 schema 与文案替换为产业语义。焦点进入高筛标题或首个条件；面包屑“产业查询”返回 `source/sourceSearch`。预置成功只显示条件和“已带入热门产业条件”反馈，不自动应用、不显示伪检索结果，也不得把条件编辑器嵌入蓝色查询主视觉。

F-01 智能匹配反馈：复用企业查询 SmartChip 的位置、Tag 关闭按钮、`aria-live` 和降级反馈语义。提交后在搜索输入框与示例查询之间显示“已匹配关键词：字段：值”；关闭按钮的可访问名称由 Arco 提供，pointer/Enter/Space 均可激活。关闭一个 Tag 后保留输入文本和其他 Tag，立即更新结果数量与卡片集合；结果卡只呈现对象业务字段和产业标签，不再呈现匹配关键词、匹配字段或匹配说明。未命中词典时同一区域显示多字段关键词降级说明。

F-01 最近检索：复用企业查询的半透明容器、历史 Tag 和清除动作，固定在普通检索条件与推荐/结果之间。智能检索和查产业仅在有效执行后记录；同标题覆盖旧记录并置顶，最多 10 条、本地保留 30 天，按当前模式过滤展示。点击历史 Tag 立即恢复关键词、SmartChip/模式和 URL 并重跑；“清除”移除全部产业查询最近记录并回到空态。示例查询只预填输入，热门产业只进入高筛并预置条件，两者在未执行或未应用前均不写入。

F-01 权限锁态：对象级权限结果与数据可用性是两条独立轴。`permission_locked` 卡片使用 Arco `IconLock`、锁态 Token 和可聚焦的原因 Tooltip；保留允许公开的名称、对象类型、父级产业、所属领域、更新时间与来源，敏感摘要替换为权限原因。查看摘要、进入全景图谱、Checkbox 和单卡加入对比篮均保持可识别的锁定语义，不能只做无说明的 disabled；`unavailable` 卡片仅显示目录、数据或服务原因，不出现锁图标。正式权限矩阵关闭前，界面不得显示或推断具体最低 L 级，切换 review mode 或 Mock persona 也不得改变同一业务权限结果。

F-01 全景出口：推荐卡、检索结果卡与对象摘要抽屉的跳转统一为「进入全景图谱」，目标路由 `/industry-center/panorama`，携带 `object_type`、`object_id` 与返回查询上下文。`industry` 入口沿用全景既有行为先展开所含产业链；`industry_chain` 直接进入该链工作区。页面不得再出现「去门户总览」或「打开专题全景」。对象摘要“可进入的页面”说明产业入口展开子链，并声明返回时保留查询条件。

### 4.1 F-01 共享组件与领域插槽合同

| 层级 | 共享组件职责 | 企业查询注入 | 产业查询注入 | 一致性验收 |
| --- | --- | --- | --- | --- |
| 工作台 | `ElementSearchWorkbench` 组织普通查询的固定区块和状态顺序 | 企业 config、推荐/结果渲染和动作 | 产业 config、推荐/结果渲染和动作 | 两页 DOM 区块顺序一致，均不复制共享容器 |
| 检索区 | `SearchHub` 提供模式、Arco 搜索框、反馈宿主、示例和热门入口；标签和 test-id 支持 namespace 配置 | `keyword` 显示“查企业”，企业 SmartChip 与热门场景 | `industry` 显示“查产业”，产业 SmartChip 与热门产业 | 结构、焦点和键盘行为一致；领域文案和数据隔离 |
| 最近检索 | `RecentSearchPanel` 处理过滤、恢复、清除、空态和可访问标签 | 企业 storage key 与 snapshot | 产业 storage key 与 snapshot | 相同行为与表面；存储互不污染 |
| 结果宿主 | 工作台提供标题、说明、工具栏和稳定状态容器，卡片通过 render slot 注入 | 企业推荐卡、企业列表与企业动作 | 产业推荐卡、产业/产业链横向卡和同类型入篮 | loading/empty/error/permission 位置一致；领域动作不串线 |
| 高筛 | `FilterPanel` 页面结构和交互 | 企业 field library | 产业 field library | 只共享组件，不共享 schema |

迁移期间企业查询的业务逻辑、路由、存储数据和动作结果必须保持不变。共享组件新增 props 必须有企业默认值，先以现有企业查询行为作为回归基线，再接入产业配置。不得通过修改全局样式让产业页面偶然接近企业页面，也不得让共享组件读取领域数据文件。

## 5. 交互与状态转换

### 5.1 配置、生成、过程、结果、报告

| 控件 / 事件 | 前置 | 交互与即时反馈 | 成功状态 | 失败与恢复 |
| --- | --- | --- | --- | --- |
| “生成分析” | 对象、配置、权限和同 Tab 互斥的客户端可判项通过 | 主按钮 loading，阻止重复点击；提交服务端最终校验 | 创建 `task_id` 并导航 F-11 | 停留草稿；字段错误内联；权限/并发用 Alert，聚焦首个可修正项 |
| Steps 阶段更新 | 存在有效任务 | 已完成/进行中/等待/失败使用文字与图标，不显示百分比 | current stage 更新；页面和系统浮层同步 | 断线保留最后服务端状态并提供重试，不前端推演阶段 |
| queued“撤回” | 当前用户为发起人且状态 queued | `Popconfirm` 说明撤回后无结果并释放互斥 | `withdrawn`，提供返回配置/复制入口 | 失败保持 queued，Message 说明原因并刷新真源 |
| running | 状态 running | 只展示已用时间、当前阶段和后台继续说明 | 进入 succeeded 或失败终态 | 普通用户不显示取消；直接调用取消由服务端拒绝 |
| “查看结果” | 状态 succeeded 且返回有效 `result_id` | 主按钮；保留任务页，打开绑定结果 | `result_readonly` | 结果身份失效时留在任务页并可刷新任务真源 |
| “生成报告” | 结果 succeeded、未过期且有权 | 按钮 loading；创建或复用报告任务 | generating/ready；提供查看任务或报告 | 来源无权/过期/共享能力未激活时失败关闭，结果仍可读 |

### 5.2 七类阶段注册

| `analysis_type` | 六段阶段文案 |
| --- | --- |
| `cycle` | （执行权威见 DIAGNOSIS）任务提交与参数冻结 → 整合产业参数与联网检索的历史与市场数据 → 大语言模型推理与周期阶段判断（诊断）→ 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点 → 结果可信性校验与分析报告组装 |
| `key_link` | （执行权威见 DIAGNOSIS）任务提交与产业链对象冻结 → 全链路环节结构化拆解（研发/设计/制造/销售/服务）→ 基于附加值率、技术壁垒、市场集中度计算高端化指数 → 关键环节智能标注与竞争格局/代表企业/技术趋势归纳 → 结果可信性校验与分析报告组装 |
| `bottleneck` | 任务提交与产业链对象冻结 → 整合各环节技术/人才/资本/政策等时序数据 → 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度 → 瓶颈智能识别与卡脖子环节归因/改进建议生成 → 结果可信性校验与靶向方案/报告组装（权威在 CHAIN-TOPIC-DIAGNOSIS） |
| `regional_index` | 任务提交 → 权限与配置校验 → 产业与区域数据准备 → 区域产业指数计算 → 可比性与可信性校验 → 结果图表与结论组装 |
| `regional_competitiveness` | 任务提交 → 权限与配置校验 → 产业与区域数据准备 → 区域竞争力计算 → 可比性与可信性校验 → 排名图表与结论组装 |
| `shenzhen_comparison` | 任务提交 → 权限与配置校验 → 深圳与标杆数据准备 → 产业对标分析 → 可比性与可信性校验 → 对比图表与结论组装 |
| `shenzhen_development` | 任务提交 → 权限与来源结果校验 → 对比结果与目标准备 → 发展建议与路径生成 → 依据与完整性校验 → 建议路径与结论组装 |

阶段数量和文案由正式任务合同返回；V1 只可按上述当前四件套注册表演示，不得从企业评估复制领域阶段，不得使用计时器伪造推进。

### 5.3 对象、Tab 与结果隔离

- 诊断页只在兼容 Tab 间共享 `industry_id`；关键环节/瓶颈可共享兼容 `chain_id`，周期不消费 `chain_id`。
- 区域页只共享兼容产业对象；区域、指标、权重、模板和预览分别维护。
- 深圳页只共享兼容产业对象；发展分析必须显式选择来源结构化结果。
- 切换二级页面时优先恢复目标页自己的未提交草稿或非终态任务；两者皆无才显示对象空态。
- 进入结果、记录或报告不得覆盖草稿；返回时恢复触发元素、Tab、滚动和筛选位置。

## 6. 反馈与异常恢复

| 场景 | 反馈载体 | 文案语义 | 恢复动作 |
| --- | --- | --- | --- |
| 首次加载页面/卡片 | `Skeleton` | 保持标题、工具和容器尺寸 | 自动完成或局部重试 |
| 局部刷新/预览 | 控件 loading + 局部 `Spin` | 说明正在更新受控区域 | 保留旧上下文，不阻塞其他卡片 |
| 查询/图谱/结果空态 | `Empty` | 说明无对象、无结构、无结果或无已确认变化的具体原因 | 调整查询、选择节点/快照或返回配置 |
| 表单校验失败 | `Form.Item` error + 页面摘要 | 指明字段、规则和修复动作 | 聚焦首个错误；保留全部合法输入 |
| 服务或图层失败 | 局部 `Result` / `Alert` | 区分查询、详情、快照、图层、结果身份失败 | 仅重试失败区域；不清对象/视口/草稿 |
| permission | 对象级 `IconLock` + 锁态 Tag/Tooltip；页面级 `Result` / `Alert` | 保留允许公开的对象元数据，隐藏无权摘要、结果或报告；与普通 unavailable 明确分离，不显示推断的最低 L 级 | 返回、关闭、选择其他对象或按正式权限合同申请 |
| queued | `Tag` + Steps + Alert | 显示队列位置、后台继续和可撤回边界 | 离页、等待或二次确认撤回 |
| running | `Tag` + Steps + Alert | 显示当前阶段和已用时间，不显示百分比 | 离页后台继续；从浮层恢复 |
| succeeded | success `Alert` | 结果已固化，需用户主动查看 | 点击“查看结果” |
| failed/terminated | error `Alert` | 说明失败原因；原任务不可重跑 | 复制配置形成新草稿 |
| withdrawn | neutral `Result` | 已撤回、无结果、互斥已释放 | 返回配置或复制新建 |
| result expired | warning `Alert` | 旧结果仍可读，不可新建正式报告 | 复制配置重做 |
| 报告生成 | `Notification` | 后台任务状态和完成入口 | 查看任务/报告；失败时重试 |
| 网络中断 | 页面级非阻断 Alert | 显示最后一次服务端状态，禁止前端猜状态 | 重连后按 `task_id` 刷新 |

异步动态更新使用 `aria-live=polite`；阻断性提交错误使用 `role=alert`。Message 只承载短反馈，不作为任务完成的唯一入口。

## 7. 组件、键盘与无障碍

### 7.1 组件映射

| 交互区域 | Arco / 组合组件 | 必需语义 |
| --- | --- | --- |
| 主导航与业务 Tab | 定制导航/Tab + `Menu`/`Tabs` 语义 | 当前项、展开态、方向键、禁用原因，不重复页面路径标题 |
| 查询与配置 | `Form`、`Input.Search`、`Select`、`Cascader`、`Checkbox`、`Radio.Group`、`DatePicker` | label、帮助文本、错误定位、加载/空选项、清除规则 |
| 权重 | `InputNumber` + 表格/表单 + `Button` | 百分比可访问名称、总和状态、一键均分不静默触发 |
| 图表 | `Card`、`Skeleton`、`Empty`、`Alert`、`Tooltip` + 可视化内核 | 图例、文本摘要、等价表格、点选反馈 |
| 图谱 | `Card`、搜索、筛选、`Drawer` + 图谱内核 | 节点列表替代路径、重置视图、防迷失、当前节点 |
| 详情 | `Drawer`、`Descriptions`、`Tabs`、`Timeline`、`Table` | header/body/footer 稳定，关闭回焦点，未保存内容确认 |
| 任务过程 | `Descriptions`、`Tag`、`Steps`、`Alert`、`Popconfirm`、`Notification` | 当前阶段文本、后台继续、撤回确认、完成入口 |
| 报告 | `Button`、`Notification`、共享只读 Reader | 状态、来源修订、下载去向、失败重试 |
| 评审挂点 | `Tooltip` / `Popover` + Arco Icon | 仅 review mode 出现；可键盘激活；不改变业务布局和权限 |

### 7.2 Pointer 与键盘合同

- `Tab/Shift+Tab`：按导航 → ContextBar → 当前 Tab → 主内容 → 主动作的视觉顺序移动。
- `Enter/Space`：激活按钮、链接、复选、Tab、图例、节点替代列表、Steps 辅助入口和评审标识。
- `ArrowLeft/Right`：Tab、分段控件、时间轴和 Steps 辅助导航；`ArrowUp/Down`：下拉、列表、表格和节点替代列表。
- `Esc`：关闭 Dropdown、Tooltip、Popover、Drawer、Modal；有未保存配置时先确认；关闭后回到触发元素。
- 图谱/图表的鼠标 hover、节点/点位点击、拖拽或时间轴操作必须提供可聚焦列表、摘要、筛选或表格等价路径。
- “生成分析”“撤回”“查看结果”“生成报告”均可键盘触发；loading 时设置 `aria-busy=true` 且阻止重复提交。

### 7.3 ARIA、焦点与可读性

- Tabs 使用 tablist/tab/tabpanel；当前导航使用 `aria-current`；展开组使用 `aria-expanded`。
- 表单错误用 `aria-describedby` 关联帮助/错误文本；禁用动作同时提供可读原因，不只降低透明度。
- Steps 暴露当前阶段和状态文本；状态不只依赖蓝/绿/红颜色。
- Drawer/Modal 打开后焦点进入标题或首个控件并限制在浮层内；关闭后恢复触发点。
- 图标按钮、评审标识、图谱工具和报告下载均有可访问名称；图表提供摘要或等价表格。
- 正文、控件、状态文字满足 WCAG AA；自定义 focus-visible 不得被视觉还原移除。

## 8. 响应式行为

本模块只支持 `medium_1440_1920`。三个宽度始终保持 24 列和 16px gutter，不产生移动端或 `<1440px` 交付物。

| Viewport | 导航与容器 | 配置 / 过程 | 图谱 / 结果 | 固定与滚动 |
| ---: | --- | --- | --- | --- |
| 1920 | Sidebar 默认 200px；内容区完整 24 栅格 | 配置字段可 3～4 列；任务摘要 4 列；六段 Steps 单行 | F-02 主画布 + F-03 480～640px 右栏；结果图表可双列 | Header/Sidebar 稳定；主内容纵向滚动；结果主动作保持可见 |
| 1680 | Sidebar 保持用户状态；内容动态列宽 | 配置字段 2～3 列；任务摘要 2～4 列；Steps 保持单行，长文案截断并提供完整可读名称 | 右栏取低宽度；结果双列优先保留主结论，次级区可纵向排列 | 不横向溢出；表格区域可内部滚动，操作列固定 |
| 1440 | Sidebar 默认收起 64px | 配置字段 2 列，长字段整行；任务摘要 2 列；Steps 容器允许水平滚动并提供阶段列表键盘替代，不折叠阶段 | 图谱详情转右侧 Drawer；结果卡由双列转单列；不得删除字段、状态或评审宿主 | 主动作区可粘底但不得遮挡内容；页面仅纵向滚动，宽表内部滚动 |

共同规则：筛选项可换行但不横向溢出；标题、操作和状态位置稳定；除 F-01 可见评审页头按已确认口径在业务态折叠外，评审模式与业务模式拥有相同布局容量；图表/图谱在尺寸变化后重绘但不得丢失选中、图例、视口、草稿或任务身份。

## 9. 内部评审投影

### 9.1 显隐与交互合同

- `review_trace_applicability: applicable`；21 个挂点只在 review mode 呈现，business mode 全部 absent。
- 挂点不得改变字段、权限、动作、结果快照、布局容量或报告修订；禁止放入业务按钮、表单 label、图例、数据值字符串和下载正文。
- requirement trace Popover payload：`source_location/source_summary/current_placement/source_relation`。
- missing metric entry Popover payload：`gap_ref/host_fields/metric_owner/expected_matrix`；只说明未登记事实，不显示虚构数值或 D1–D4 状态。
- Pointer：click 打开、再次 click 或点击外部关闭；Keyboard：Tab 聚焦、Enter/Space 打开、Esc 关闭并回焦点。

### 9.2 21 个挂点清单

| Frame | mount_id | 精确宿主 | 类型 | trace refs |
| --- | --- | --- | --- | --- |
| F-01 | `CHAIN-TOPIC-F01-SEARCH-TITLE` | 产业查询评审页头（标题和说明） | requirement_trace | `US-CHAIN-TOPIC-01` |
| F-02 | `CHAIN-TOPIC-F02-PANORAMA-TITLE` | 产业链全景图谱标题 | requirement_trace | `REQ-CHAIN-TOPIC-01`、`US-CHAIN-TOPIC-02` |
| F-03 | `CHAIN-TOPIC-F03-EVOLUTION-TITLE` | 动态演进区标题 | requirement_trace | `REQ-CHAIN-TOPIC-01`、`US-CHAIN-TOPIC-03` |
| F-03 | `CHAIN-TOPIC-F03-STATS-HOST` | 节点详情统计字段组 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-04 | `CHAIN-TOPIC-F04-CYCLE-TITLE` | 周期分析结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-02`、`US-CHAIN-TOPIC-04/05` |
| F-04 | `CHAIN-TOPIC-F04-CYCLE-METRICS` | 周期判断与预测统计区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-05 | `CHAIN-TOPIC-F05-KEYLINK-TITLE` | 关键环节结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-04`、`US-CHAIN-TOPIC-06/07` |
| F-05 | `CHAIN-TOPIC-F05-KEYLINK-METRICS` | 固定因子与关键环节指标区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-06 | `CHAIN-TOPIC-F06-BOTTLENECK-TITLE` | 瓶颈堵点结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-05`、`US-CHAIN-TOPIC-08/09` |
| F-06 | `CHAIN-TOPIC-F06-BOTTLENECK-METRICS` | 健康度与归因指标区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-07 | `CHAIN-TOPIC-F07-INDEX-TITLE` | 区域产业指数结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-03`、`US-CHAIN-TOPIC-10/11` |
| F-07 | `CHAIN-TOPIC-F07-INDEX-METRICS` | 指标配置与指数结果区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS`、`GAP-CHAIN-TOPIC-CUSTOM-METRIC` |
| F-08 | `CHAIN-TOPIC-F08-COMPETITIVENESS-TITLE` | 区域竞争力结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-08`、`US-CHAIN-TOPIC-12/13` |
| F-08 | `CHAIN-TOPIC-F08-COMPETITIVENESS-METRICS` | 三维权重与排名指标区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-09 | `CHAIN-TOPIC-F09-SZ-COMPARE-TITLE` | 深圳产业对比结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-06`、`US-CHAIN-TOPIC-14/15` |
| F-09 | `CHAIN-TOPIC-F09-SZ-COMPARE-METRICS` | 四维对比与阶段指标区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-10 | `CHAIN-TOPIC-F10-DEVELOPMENT-TITLE` | 深圳产业发展结果标题 | requirement_trace | `REQ-CHAIN-TOPIC-07`、`US-CHAIN-TOPIC-16/17` |
| F-10 | `CHAIN-TOPIC-F10-DEVELOPMENT-EVIDENCE` | 建议与路径依据区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |
| F-11 | `CHAIN-TOPIC-F11-TASK-TITLE` | 统一可视化分析过程与分析记录标题 | requirement_trace | `US-CHAIN-TOPIC-18/19` |
| F-12 | `CHAIN-TOPIC-F12-REPORT-TITLE` | 产业分析报告标题 | requirement_trace | `US-CHAIN-TOPIC-20`、`GAP-CHAIN-TOPIC-REPORT-ACTIVATION` |
| F-12 | `CHAIN-TOPIC-F12-REPORT-METRICS` | 报告统计与图表区 | missing_metric_entry | `GAP-CHAIN-TOPIC-METRICS` |

### 9.3 Metric readiness 投影边界

本专题没有已登记的 `M_CHAIN_*` 指标，也没有 `CHAIN-TOPIC-ANALYSIS` readiness matrix；现有矩阵属于门户总览。因此当前不能合法生成带 `metric_id/matrix_ref` 的 `metric_readiness_projection`，机器契约保持空数组，并以 `GAP-CHAIN-TOPIC-METRICS` 阻断下游指标投影。

指标真源建立后，每个统计宿主必须逐指标声明：`def_status/schema_status/source_mapping_status/ingestion_status` 四维引用，维度顺序 `definition/structure/source_mapping/ingestion`，入口组 `definition/data_health/ingestion`，`data_health_dimensions: [schema_status, source_mapping_status]`，`data_health_component: DataHealthBadge`，`data_health_popover_rows: [structure, source_mapping]`，`max_markers: 3`，`spacing_px: 4`，pointer 与 keyboard 激活，以及 Tooltip/Popover payload。D4 `ingesting` 只能显示 `ods_synced/dwd_loaded/es_indexed/graph_loaded/verified` 五阶段清单，不显示百分比；D3 `pending_ods` 作为 DataHealthBadge「源映射」行的时钟态，不实现独立 OdsPendingBadge。

禁止把 D2、D3 重新展开为同宿主的两枚兄弟入口标识；组合只发生在入口层，Popover 和 `aria-label` 必须保留两维独立语义、状态和证据。

## 10. Demo 实施交接

### 10.1 页面包与共享候选

| 交接项 | 实施合同 |
| --- | --- |
| 页面包 | search、panorama、diagnosis、regional、shenzhen、task deep link、result deep link、report deep link |
| 分析壳层 | `ConfigView`、`ProcessingView`、`ResultView` 作为页面模式；共享 task summary、StageSteps、CurrentStageAlert 和 result action |
| 领域注册 | 七个 `analysis_type` 分别提供 object/config summary、stage definitions、result route、result slot、report type |
| 状态模型 | 服务端任务真源；草稿、任务、结果、报告四种身份分开；不通过 URL 猜对象或结果 |
| 可视化边界 | Arco 外围负责容器/状态/工具/Drawer；图表、图谱内核只负责图形和命中 |
| 评审模式 | 21 个挂点按清单投射；业务模式完全 absent；不得因评审模式改变布局或动作 |

### 10.2 测试关注点

- 七种配置都只能在最终校验成功后创建唯一任务，重复点击不会产生重复 `task_id`。
- 七种过程都使用同一壳层但显示自己的阶段；没有企业阶段文案、单一 Spinner、虚构百分比或自动跳结果。
- queued 撤回、running 不可取消、离页继续、深链恢复、失败复制配置和 succeeded 显式查看结果可逐项验证。
- F-01～F-12 的 default/loading/empty/error/permission 与特殊状态均可进入；返回后上下文和焦点正确。
- F-01 权限受限对象显示锁图标、原因和锁定动作，敏感摘要不可见；普通不可用对象不显示锁图标；切换 L0～L4 Mock persona 或 review mode 不得让静态权限结果自行解锁。
- 1920/1680/1440 无页面级横向溢出，1440 不删除业务字段、状态、挂点或动作。
- 业务模式 21 个评审挂点全部不存在；review mode payload、键盘、焦点和关闭行为一致。

### 10.3 明确排除

`ready_for_v1` 允许下游按 `gkx-definition-to-demo` 进入 V1 高保真首轮；本次文档回写没有执行代码修改、任务创建/认领、Gate 推进、指标命名、数据源推断、报告框架激活、旧路由迁移、移动端或 Track-L 实现。

## 11. 缺口与阻断项

| gap | blocks_v1 | 阻断阶段 | V1 处理 | Owner / deadline | return_to |
| --- | --- | --- | --- | --- | --- |
| `GAP-CHAIN-TOPIC-APPROVAL` | false | pdr、v1_final、v2_lumen、production | gap_visible；允许交互验证，范围变化和正式冻结不生效 | 郭万迎 / before_pdr_or_scope_activation | TRACE |
| `GAP-CHAIN-TOPIC-CUSTOM-METRIC` | false | pdr、v1_final、v2_lumen、production | gap_visible；仅预设指标，明确自定义指标未纳入本轮 | 淮政玮 / before_pdr | compliance |
| `GAP-CHAIN-TOPIC-METRICS` | false | pdr、v1_final、v2_lumen、production | gap_visible；使用明确 Mock/空态与 missing metric entry，不发明指标或状态 | 何老师 / before_pdr | TRACE |
| `GAP-CHAIN-TOPIC-PERMISSIONS` | false | pdr、v1_final、v2_lumen、production | fail_closed；提交、结果、报告和敏感摘要均以服务端拒绝优先；对象级拒绝显示锁态并保留非敏感元数据，与普通不可用态分离，不推断最低 L 级 | 郭万迎 / before_pdr | USM |
| `GAP-CHAIN-TOPIC-COMPARE-BASKET` | false | v1_final、v2_lumen、production | gap_visible；只模拟已定义的原位选择和分发，不复制共享篮内部能力 | 高颖 / before_v1_final | architecture |
| `GAP-CHAIN-TOPIC-REPORT-ACTIVATION` | false | v1_final、v2_lumen、production | gap_visible；验证报告入口/反馈/只读壳，未激活时正式生成与下载失败关闭 | 淮政玮 / before_v1_final | compliance |
| `GAP-CHAIN-TOPIC-ROUTE-MIGRATION` | false | v2_lumen、production | deterministic_demo_contract；V1 仅写规范路由，旧路由只作迁移审计 | 徐滕强 / before_v2_lumen | architecture |
| `GAP-CHAIN-TOPIC-TEMPLATE-CONTRACT` | false | shared_template_maintenance | no_impact；本 UX-SPEC 已包含完整合同，不修改共享模板 | 郭万迎 / none | TRACE |

当前不存在 `blocks_v1: true` 的 gap；其余缺口均有显式 V1 处理并继续阻断各自下游阶段。本文可作为 V1 高保真首轮交互输入，不代表 PDR、V1-FINAL、V2 或 production 已关闭。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-ANALYSIS
  version: "0.4-ready-for-v1"
  status: ready_for_v1
  source_four_pack:
    - IA-CHAIN-TOPIC-ANALYSIS.md
    - TRACE-CHAIN-TOPIC-ANALYSIS.yaml
    - USM-CHAIN-TOPIC-ANALYSIS.md
    - Wireframe-CHAIN-TOPIC-ANALYSIS.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-CHAIN-GOV
      role: ROLE-CHAIN-GOV
      story_refs: [US-CHAIN-TOPIC-03, US-CHAIN-TOPIC-04, US-CHAIN-TOPIC-05, US-CHAIN-TOPIC-08, US-CHAIN-TOPIC-09, US-CHAIN-TOPIC-10, US-CHAIN-TOPIC-11, US-CHAIN-TOPIC-14, US-CHAIN-TOPIC-15, US-CHAIN-TOPIC-16, US-CHAIN-TOPIC-17, US-CHAIN-TOPIC-18, US-CHAIN-TOPIC-20]
      primary_flow: [选择对象并完成配置, 生成分析, 查看可视化过程, 显式查看结果, 从有效结果生成报告]
      abnormal_flows: [配置失败保留草稿, queued可撤回, running不可取消且离页继续, 失败复制配置新建, 过期结果禁新报告]
    - journey_id: J-CHAIN-PARK
      role: ROLE-CHAIN-PARK
      story_refs: [US-CHAIN-TOPIC-01, US-CHAIN-TOPIC-02, US-CHAIN-TOPIC-03, US-CHAIN-TOPIC-06, US-CHAIN-TOPIC-07, US-CHAIN-TOPIC-12, US-CHAIN-TOPIC-13, US-CHAIN-TOPIC-18, US-CHAIN-TOPIC-19]
      primary_flow: [发现同类型对象并加入系统篮, 浏览完整链条与节点, 完成关键环节或区域竞争力分析, 查看历史并复制配置]
      abnormal_flows: [混选对象被拒绝且保留已选, 节点详情独立重试, 固定因子或维度不可用时禁止生成, 不同版本结果禁止混排]
    - journey_id: J-CHAIN-ENTERPRISE
      role: ROLE-CHAIN-ENTERPRISE
      story_refs: [US-CHAIN-TOPIC-02, US-CHAIN-TOPIC-03, US-CHAIN-TOPIC-20]
      primary_flow: [浏览产业链结构, 查看动态演进, 阅读获授权结果或报告, 打开共享企业抽屉后返回原上下文]
      abnormal_flows: [无权对象或链接失败关闭, 敏感字段按服务端裁剪, 技术路线不形成技术分析入口]
  frame_specs:
    - frame_id: F-CHAIN-01
      route_or_host: /industry-center/search?mode=smart|industry|advanced
      source_refs: [US-CHAIN-TOPIC-01]
      states: [recommendation, default, loading, empty, error, permission, type_locked, partial_add]
      interactions: [切换检索模式, 推荐态单卡查看摘要与进入全景图谱与加入对比篮, 执行查询与清空条件, 检索结果态同类型勾选, 检索结果态全选本页与批量加入对比篮, 打开对象摘要, 抽屉进入全景图谱]
    - frame_id: F-CHAIN-02
      route_or_host: /industry-center/panorama
      source_refs: [US-CHAIN-TOPIC-02, US-CHAIN-TOPIC-03]
      states: [default, loading, empty, error, permission, single, dual, timeline]
      interactions: [选择节点, 切换快照模式, 缩放适配复位, 打开绑定详情]
    - frame_id: F-CHAIN-03
      route_or_host: /industry-center/panorama#node-detail-evolution
      source_refs: [US-CHAIN-TOPIC-02, US-CHAIN-TOPIC-03]
      states: [default, loading, empty, error, permission, incompatible_snapshot]
      interactions: [切换详情, 打开共享企业抽屉, 选择双快照, 播放暂停时间轴]
    - frame_id: F-CHAIN-04
      route_or_host: /industry-center/diagnosis?tab=cycle
      source_refs: [US-CHAIN-TOPIC-04, US-CHAIN-TOPIC-05]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [配置周期参数, 生成分析, 查看过程, 查看结果, 生成报告]
    - frame_id: F-CHAIN-05
      route_or_host: /industry-center/diagnosis?tab=key-link
      source_refs: [US-CHAIN-TOPIC-06, US-CHAIN-TOPIC-07]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [确认固定因子, 生成分析, 查看过程, 选择关键环节, 打开企业抽屉]
    - frame_id: F-CHAIN-06
      route_or_host: /industry-center/diagnosis?tab=bottleneck
      source_refs: [US-CHAIN-TOPIC-08, US-CHAIN-TOPIC-09]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [确认固定维度, 生成分析, 查看过程, 查看归因, 生成报告]
    - frame_id: F-CHAIN-07
      route_or_host: /industry-center/regional?tab=index
      source_refs: [US-CHAIN-TOPIC-10, US-CHAIN-TOPIC-11]
      states: [object_empty, draft, preview, validating, processing, result, expired, error, permission]
      interactions: [配置对象组合, 勾选预设指标, 调整权重, 轻量预览, 生成分析, 查看结果]
    - frame_id: F-CHAIN-08
      route_or_host: /industry-center/regional?tab=competitiveness
      source_refs: [US-CHAIN-TOPIC-12, US-CHAIN-TOPIC-13]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [配置对象组合, 调整三维权重, 生成分析, 查看过程, 查看排名与短板]
    - frame_id: F-CHAIN-09
      route_or_host: /industry-center/shenzhen?tab=comparison
      source_refs: [US-CHAIN-TOPIC-14, US-CHAIN-TOPIC-15]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [选择产业与标杆, 核对四维模型, 生成分析, 查看过程, 查看对比结果]
    - frame_id: F-CHAIN-10
      route_or_host: /industry-center/shenzhen?tab=development
      source_refs: [US-CHAIN-TOPIC-16, US-CHAIN-TOPIC-17]
      states: [object_empty, draft, validating, processing, result, expired, error, permission]
      interactions: [选择结构化来源结果, 确认三类目标, 生成分析, 查看过程, 比较发展路径]
    - frame_id: F-CHAIN-11
      route_or_host: /industry-center/tasks/:taskId|workspace?tab=records
      source_refs: [US-CHAIN-TOPIC-18, US-CHAIN-TOPIC-19]
      states: [created, prechecking, queued, running, succeeded, failed, withdrawn, terminated, empty, error, permission]
      interactions: [查看阶段Steps, queued二次确认撤回, 显式查看结果, 复制配置新建, 筛选分析记录]
    - frame_id: F-CHAIN-12
      route_or_host: /industry-center/reports/:reportId
      source_refs: [US-CHAIN-TOPIC-20]
      states: [not_generated, generating, ready, failed, expired, permission]
      interactions: [生成报告, 查看报告任务, 打开只读报告, 下载同修订PDF, 返回来源结果]
  feedback_rules:
    - trigger: 配置校验失败
      response: 字段内联错误并聚焦首个错误
      recovery: 保留草稿并允许修正重试
    - trigger: 任务进入queued或running
      response: Steps与当前阶段Alert同步服务端状态
      recovery: 离页后台继续并由系统浮层或深链恢复
    - trigger: queued撤回
      response: Popconfirm后二次提交服务端撤回
      recovery: 成功进入withdrawn或失败保持原状态
    - trigger: 任务succeeded
      response: success反馈并启用查看结果
      recovery: 用户显式打开绑定结果
    - trigger: 结果expired
      response: 结果只读并禁用新正式报告
      recovery: 复制配置创建新分析
    - trigger: 报告生成失败或未激活
      response: 保留来源结果并说明失败原因
      recovery: 重试或等待共享能力激活
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, text_alternative, live_region]
  readiness_entry_projection:
    entry_marker_groups: [definition, data_health, ingestion]
    data_health_dimensions: [schema_status, source_mapping_status]
    data_health_component: DataHealthBadge
    data_health_popover_rows: [structure, source_mapping]
    max_markers: 3
    spacing_px: 4
  metric_readiness_projection: []
  review_mounts:
    - {mount_id: CHAIN-TOPIC-F01-SEARCH-TITLE, frame_id: F-CHAIN-01, host_label: 产业查询评审页头（标题和说明）, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F02-PANORAMA-TITLE, frame_id: F-CHAIN-02, host_label: 产业链全景图谱标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F03-EVOLUTION-TITLE, frame_id: F-CHAIN-03, host_label: 动态演进区标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F03-STATS-HOST, frame_id: F-CHAIN-03, host_label: 节点详情统计字段组, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F04-CYCLE-TITLE, frame_id: F-CHAIN-04, host_label: 周期分析结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F04-CYCLE-METRICS, frame_id: F-CHAIN-04, host_label: 周期判断与预测统计区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F05-KEYLINK-TITLE, frame_id: F-CHAIN-05, host_label: 关键环节结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F05-KEYLINK-METRICS, frame_id: F-CHAIN-05, host_label: 固定因子与关键环节指标区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F06-BOTTLENECK-TITLE, frame_id: F-CHAIN-06, host_label: 瓶颈堵点结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F06-BOTTLENECK-METRICS, frame_id: F-CHAIN-06, host_label: 健康度与归因指标区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F07-INDEX-TITLE, frame_id: F-CHAIN-07, host_label: 区域产业指数结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F07-INDEX-METRICS, frame_id: F-CHAIN-07, host_label: 指标配置与指数结果区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F08-COMPETITIVENESS-TITLE, frame_id: F-CHAIN-08, host_label: 区域竞争力结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F08-COMPETITIVENESS-METRICS, frame_id: F-CHAIN-08, host_label: 三维权重与排名指标区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F09-SZ-COMPARE-TITLE, frame_id: F-CHAIN-09, host_label: 深圳产业对比结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F09-SZ-COMPARE-METRICS, frame_id: F-CHAIN-09, host_label: 四维对比与阶段指标区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F10-DEVELOPMENT-TITLE, frame_id: F-CHAIN-10, host_label: 深圳产业发展结果标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F10-DEVELOPMENT-EVIDENCE, frame_id: F-CHAIN-10, host_label: 建议与路径依据区, marker_type: missing_metric_entry}
    - {mount_id: CHAIN-TOPIC-F11-TASK-TITLE, frame_id: F-CHAIN-11, host_label: 统一可视化分析过程与分析记录标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F12-REPORT-TITLE, frame_id: F-CHAIN-12, host_label: 产业分析报告标题, marker_type: requirement_trace}
    - {mount_id: CHAIN-TOPIC-F12-REPORT-METRICS, frame_id: F-CHAIN-12, host_label: 报告统计与图表区, marker_type: missing_metric_entry}
  gaps:
    - id: GAP-CHAIN-TOPIC-APPROVAL
      summary: 产品解释与撤回规则的结构化审批证据不完整
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 允许交互验证但不激活范围变化或正式冻结
      owner: human:郭万迎
      deadline: before_pdr_or_scope_activation
      return_to: TRACE
    - id: GAP-CHAIN-TOPIC-CUSTOM-METRIC
      summary: 区域产业指数的自定义指标能力未纳入本轮
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 仅展示预设指标并明确差异
      owner: human:淮政玮
      deadline: before_pdr
      return_to: compliance
    - id: GAP-CHAIN-TOPIC-METRICS
      summary: 专题指标与D1-D4矩阵未建立
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 使用明确Mock或空态与缺失指标挂点且不发明语义
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE
    - id: GAP-CHAIN-TOPIC-PERMISSIONS
      summary: 产品角色与L0-L4权限映射没有正式真源
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: fail_closed
      v1_treatment: 关键动作按服务端拒绝优先且不暴露敏感摘要
      owner: human:郭万迎
      deadline: before_pdr
      return_to: USM
    - id: GAP-CHAIN-TOPIC-COMPARE-BASKET
      summary: 系统对比篮正式共享产品包尚未建立
      blocks_v1: false
      blocks_stages: [v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 只验证既定领域接入而不复制共享篮内部能力
      owner: human:高颖
      deadline: before_v1_final
      return_to: architecture
    - id: GAP-CHAIN-TOPIC-REPORT-ACTIVATION
      summary: 共享报告框架尚未激活
      blocks_v1: false
      blocks_stages: [v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: 验证入口反馈与只读壳且正式生成下载失败关闭
      owner: human:淮政玮
      deadline: before_v1_final
      return_to: compliance
    - id: GAP-CHAIN-TOPIC-ROUTE-MIGRATION
      summary: 旧chainId路由迁移合同未建立
      blocks_v1: false
      blocks_stages: [v2_lumen, production]
      v1_disposition: deterministic_demo_contract
      v1_treatment: 仅写规范新路由且旧路由只作审计输入
      owner: human:徐滕强
      deadline: before_v2_lumen
      return_to: architecture
    - id: GAP-CHAIN-TOPIC-TEMPLATE-CONTRACT
      summary: 共享模板未完整包含新版阶段合同
      blocks_v1: false
      blocks_stages: [shared_template_maintenance]
      v1_disposition: no_impact
      v1_treatment: 本文已补齐合同且不修改共享模板
      owner: human:郭万迎
      deadline: none
      return_to: TRACE
```
