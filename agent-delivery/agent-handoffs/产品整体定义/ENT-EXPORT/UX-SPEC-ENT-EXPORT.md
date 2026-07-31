# UX-SPEC-ENT-EXPORT｜系统报告复用框架

> 版本：v0.4
> 状态：ready_for_v1
> 四件套版本：v0.5（2026-07-31）
> Track：Track-MS
> screen_tier：medium_1440_1920
> 下游目标：v1_hifi_round1（带阶段化缺口激活）

## 1. 权威输入与边界

### 1.1 产品权威

| 工件 | 版本 / 状态 | 本 UX-SPEC 使用方式 |
|---|---|---|
| `IA-ENT-EXPORT.md` | v0.5；产品契约基线已补齐，V1 首轮可实施，范围批准与技术冻结仍为后续缺口 | 模块边界、角色、对象、Frame、宿主、路由责任、状态和非目标 |
| `TRACE-ENT-EXPORT.yaml` | v0.5；`stage_activation: ready_for_v1_with_stage_scoped_gaps` | 故事、Frame、Owner、依赖、评审挂点、范围关系和阶段化 gap |
| `USM-ENT-EXPORT.md` | v0.5；跨模块故事可进入 V1 首轮验证，正式范围未激活 | 角色目标、验收条件、主流程、异常与业务规则 |
| `Wireframe-ENT-EXPORT.md` | v0.5；带阶段化缺口进入 V1 首轮 | 5 个 Frame、控件、字段可见性、状态矩阵、响应式和 7 个唯一评审挂点 |
| `REPORT-CONTRACT-ENT-EXPORT.md` | v0.1；产品定义层基线已确认 | 五个共用对象、七核心章节、字段所有权、业务/评审/PDF 可见性和消费者映射 |

### 1.2 适用治理

- `agent-delivery/产品定义评审规程.md`：Track-MS 按“核心产品包 → UX → UI/V1 首轮 → 门 1 完整闭合 → 联合冻结 → V2”推进；文档存在不等于 PDR、Gate 或开发激活。
- `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`：组件优先复用 Arco 语义，完整覆盖 pointer、keyboard、focus、ARIA、loading、empty、error、disabled 和权限态。
- `agent-delivery/Design.md`：使用详情/报告工作台原型与 `medium_1440_1920`；验收宽度为 1920 / 1680 / 1440；不引入移动端和 Track-L 大屏规则。
- `agent-delivery/data-lineage-policy.md`：ENT-EXPORT 不创建统计口径；消费者报告中的统计值继续携带来源模块登记的 `metric_id`、单位、时间/空间范围和版本。

### 1.3 边界声明

- 本文只把四件套已有行为转成可执行交互契约，不新增角色、字段、路由、能力、权限、业务规则、指标含义或验收范围。
- 产品范围变更与 Demo 代码变更均禁止；本文不改任务台账、`approved_scope_change`、包冻结、PDR 状态或 `delivery_tier`。
- Demo、截图和现有实现仅可作为后续实现证据，不是本 UX-SPEC 的需求权威。
- `F-EXPORT-03` 由 `SYS-ANALYSIS-JOBS` 承载，`F-EXPORT-05` 由个人资产中心承载；ENT-EXPORT 仅规定跨模块交接，不获得相邻模块页面所有权。
- V1 仅支持只读 HTML 与 PDF。DOCX、PPTX、XLSX、模板编辑、章节配置、全局报告中心和商业配额均不在范围内。

## 2. 四件套同步核对

### 2.1 故事与角色清单

| Story | 证据角色 | 目标 | Frame |
|---|---|---|---|
| `US-ENT-EXPORT-READ` | `ROLE-EXPORT-GOV` 政府科技管理与决策人员 | 在来源业务上下文阅读完整报告 | F-EXPORT-01 / 02 / 04 |
| `US-ENT-EXPORT-EVIDENCE` | `ROLE-EXPORT-RESEARCH` 高校科研与智库研究人员 | 核对范围、证据、来源、版本和局限性 | F-EXPORT-02 |
| `US-ENT-EXPORT-PDF` | `ROLE-EXPORT-GOV` | 下载与 HTML 同源的 A4 PDF | F-EXPORT-02 / 03 / 04 |
| `US-ENT-EXPORT-RESUME` | `ROLE-EXPORT-RESEARCH` | 从个人资产恢复同一报告修订 | F-EXPORT-05 / 02 / 04 |

角色仅使用上述两个产品证据角色，不增加管理员、运营人员、模板设计者或审批者。

### 2.2 Frame、宿主和状态清单

| Frame | 所有者 / 宿主 | 路由或承载 | 四件套状态 |
|---|---|---|---|
| `F-EXPORT-01` 来源模块报告入口 | 来源业务模块 | `source_module_defined_result_route` | `not_generated / preparing / generating / ready`；另覆盖不可生成、创建失败、无权限、产物过期 |
| `F-EXPORT-02` 只读 HTML 阅读页 | ENT-EXPORT Reader，由来源路由挂载 | `source_module_defined_report_route` | `ready`；首次加载使用骨架；异常转 F-EXPORT-04 |
| `F-EXPORT-03` 报告生成任务反馈 | `SYS-ANALYSIS-JOBS` | `system_task_layer` | `preparing / generating / ready / failed` |
| `F-EXPORT-04` 不可用状态 | ENT-EXPORT Reader / 来源路由 | `source_module_defined_report_route` | `forbidden / expired / source_invalid / artifact_missing / failed` |
| `F-EXPORT-05` 个人资产恢复入口 | 个人资产中心 + 来源模块 | `/personal/assets` → 安全回跳路由 | `ready / expired / forbidden`；另覆盖恢复中、空资产、回跳失败 |

### 2.3 固定内容与禁止行为

固定核心章节为：报告身份、决策摘要、对象与范围、核心发现、证据与分析、数据来源与生成说明、局限性与使用边界。扩展章节只能由系统按模式、对象范围、数据可用性和权限装配。

字段和消费者映射以 `REPORT-CONTRACT-ENT-EXPORT.md` v0.1 为准：

- ENT-EVAL 九个现有章节通过适配器映射到七核心章节与评估扩展章节；
- ENT-RISK 的供应链报告和痛难点建议报告分别注册 Definition，共享 Reader，不共享业务模板；
- 评估模式、指标权重、企业评分、排名、雷达图和终端用户评估模板配置不得成为共用必填字段；
- 业务模式与 PDF 隐藏内部 ID、权限编码、指纹和评审 payload，但保留业务化来源、版本、证据和局限性。

禁止行为：

- 不允许终端用户编辑正文、新增/删除/排序/隐藏/改名章节、保存模板或切换版式。
- 不允许 HTML 与 PDF 绑定不同 `report_revision_id`，也不允许打开旧报告时静默替换为最新数据。
- 不允许无数据或无证据时生成看似确定的结论，不允许框架自行推导业务结论。
- 不允许重复点击创建多个同指纹任务；复用规则由任务系统处理。
- 不允许通过历史生成成功绕过当前查看或下载权限复核。
- 不允许将评审标记、内部 payload 或实现说明写入业务模式 DOM 或 PDF。

### 2.4 同步结论

四件套在故事、Frame、宿主、状态、共用数据契约和 7 个评审挂点方面互相一致，主旅程、权限 fail-closed 与异常恢复均可形成安全且确定的 V1 方案。正式 `approved_scope_change`、技术接口、授权与审计枚举、验收目录和历史台账仍未冻结，但均已分类为不阻断 V1 的下游缺口，因此本文状态为 `ready_for_v1`；该结论不代表 PDR、V1-FINAL、V2 或生产条件闭合。

## 3. 用户旅程与任务流

### 3.1 J-EXPORT-READ｜来源上下文阅读

关联：`US-ENT-EXPORT-READ`；角色：政府科技管理与决策人员。

主路径：

1. 用户在来源结果页完成业务分析，报告区块呈现与报告状态一致的唯一主动作。
2. `not_generated` 时触发“生成报告”；来源模块先校验对象、权限与来源快照，再把结构化内容交给报告框架和任务系统。
3. `ready` 时触发“查看报告”，安全路由带入明确的 `report_revision_id`。
4. Reader 先稳定呈现页面骨架，再加载报告身份、元信息、目录和正文；焦点落到页面业务标题。
5. 用户用目录定位固定核心章节和已装配扩展章节；正文始终只读。
6. 用户通过“返回来源结果”回到来源模块安全路由，来源对象、任务和结果上下文保持。

异常与恢复：

- 来源内容不足：生成按钮禁用并在按钮旁说明不可生成原因，不创建任务。
- 结构缺少必需章节：拒绝生成并显示结构校验错误；返回来源模块修复，不渲染伪空报告。
- 加载失败、无权限或来源失效：转 F-EXPORT-04；不回显敏感摘要和文件信息。
- 返回失败：保留当前报告，不清空阅读位置，提供再次返回。

### 3.2 J-EXPORT-EVIDENCE｜证据与局限性核对

关联：`US-ENT-EXPORT-EVIDENCE`；角色：高校科研与智库研究人员。

主路径：

1. 用户进入同一 `report_revision_id` 的 Reader。
2. 元信息行展示对象范围、生成时间、模板版本、数据版本和算法版本；不存在的值明确显示“未提供”。
3. 用户从目录进入“证据与分析”“数据来源与生成说明”“局限性与使用边界”。
4. 结论与结构化证据保持可定位关系；来源模块统计值沿用其已登记 `metric_id` 及语义。
5. 用户完成核对后返回来源结果，或继续阅读同一修订。

异常与恢复：

- 缺少元信息：保留字段名并显示“未提供”，不猜测值；问题进入来源内容质量处理。
- 无数据、低可信度或来源不可用：对应章节显示明确降级说明；无证据结论不渲染。
- 模板已升级：旧报告继续使用旧 `template_version`，不静默重算。

### 3.3 J-EXPORT-PDF｜下载同源 PDF

关联：`US-ENT-EXPORT-PDF`；角色：政府科技管理与决策人员。

主路径：

1. 用户在 Reader 触发“下载 PDF”。
2. 按钮立即进入 loading 并禁止重复触发；系统复核当前权限和来源可见范围。
3. 已有且有效的同修订 PDF 可直接进入安全下载；需生成时转交 `SYS-ANALYSIS-JOBS` 并打开 F-EXPORT-03。
4. 用户可关闭任务反馈让任务后台继续，或进入“查看任务”。
5. 成功后提供明确完成位置；下载产物的 `report_revision_id` 与当前 Reader 一致。

异常与恢复：

- 权限失败：进入 `forbidden`，不暴露文件元数据。
- PDF 过期：进入 `expired`，在当前授权允许时提供“重新生成 PDF”。
- PDF 缺失但 HTML 有效：进入 `artifact_missing`，HTML 阅读不受影响，可重新生成目标格式。
- 生成失败：展示可理解原因和追踪编号；只有任务规则允许时才提供重试。

### 3.4 J-EXPORT-RESUME｜个人资产恢复

关联：`US-ENT-EXPORT-RESUME`；角色：高校科研与智库研究人员。

主路径：

1. 用户在 `/personal/assets` 找到报告资产。
2. “查看报告”使用资产中的来源模块、安全回跳路由和 `report_revision_id`。
3. 回跳后先复核当前权限，再恢复同一修订和来源上下文。
4. Reader 加载完成后，焦点进入报告标题；不因为来源模块出现新数据而替换修订。

异常与恢复：

- 权限失效：进入 `forbidden`，保留返回个人资产的安全路径。
- 文件过期但修订有效：允许按授权规则重建 PDF。
- 来源快照不可解析：进入 `source_invalid`，不自动切换最新数据。
- 回跳失败：个人资产记录保持不变，显示可重试反馈，不把用户留在空白页面。

## 4. Frame 与承载映射

| Frame | 入口 | 出口 | 核心控件 | 上下文保持与跨模块交接 |
|---|---|---|---|---|
| `F-EXPORT-01` | 来源模块业务结果完成后进入报告区块 | 生成→F-EXPORT-03；查看→F-EXPORT-02 | 状态文本、“生成报告 / 查看报告 / 查看任务”唯一主动作 | 来源模块保有对象、任务、筛选和权限上下文；提交 Definition、ContentModel、SnapshotRef、安全报告路由 |
| `F-EXPORT-02` | 来源结果页或个人资产安全路由 | 返回来源结果；下载→安全下载或 F-EXPORT-03；异常→F-EXPORT-04 | 返回按钮、报告标题、元信息、目录、只读正文、“下载 PDF” | 绑定 `report_id + report_revision_id`；目录位置只影响阅读，不改变内容；返回使用来源安全路由 |
| `F-EXPORT-03` | 创建/复用报告任务或异步 PDF 生成 | 关闭回原页面；查看任务→系统任务层；成功→Reader/资产 | Modal、阶段列表、状态说明、关闭、查看任务、规则允许的重试 | 交接 `report_id / report_revision_id / target_format / source_route / artifact_status`；任务队列与跨登录恢复归任务系统 |
| `F-EXPORT-04` | Reader 加载、权限复核、产物检查或任务失败 | 返回来源、重建 PDF、规则允许的重试 | Arco Result/Alert、状态图标、标题、说明、追踪编号、安全恢复动作 | 不泄露无权内容；不替换修订；恢复成功回到同一报告或来源上下文 |
| `F-EXPORT-05` | `/personal/assets` 报告资产列表 | 查看→来源报告安全路由；下载→权限复核/任务 | 资产标题、摘要元数据、查看报告、下载 | 资产中心保有列表位置；使用同一修订；本包只定义资产投影字段，不拥有列表页 |

跨模块交接失败时，触发方保持原容器、焦点和上下文；不得用空白跳转或无说明关闭代替错误反馈。

## 5. 交互与状态转换

### 5.1 状态机与动作

| 当前状态 | 触发 | 结果状态 / Frame | 可逆与防重复 |
|---|---|---|---|
| `not_generated` | 生成报告 | `preparing` / F-EXPORT-03 | 点击后 loading + disabled；重复点击交给指纹复用 |
| `preparing` | 查看任务 | F-EXPORT-03 | 不创建新任务，可关闭 Modal 回原页 |
| `generating` | 查看任务 | F-EXPORT-03 | 不创建新任务，可后台继续 |
| `ready` | 查看报告 | F-EXPORT-02 | 返回来源保持上下文 |
| `ready` | 下载 PDF | 权限复核→下载或 F-EXPORT-03 | loading 防重复；失败保持 Reader |
| `failed` | 任务规则允许的重试 | `preparing` | 原追踪编号保留；不可重试时只提供返回 |
| `expired` | 重新生成 PDF | `preparing` / F-EXPORT-03 | 旧公开链接不可用；HTML 修订可继续读 |
| `forbidden` | 返回来源页面 | 来源安全路由 | 不提供查看/下载，不回显敏感元数据 |
| `source_invalid` | 返回来源页面 | 来源安全路由 | 不切换最新数据 |
| `artifact_missing` | 重新生成 PDF | `preparing` / F-EXPORT-03 | HTML 阅读与目录位置保持 |

### 5.2 Reader 目录

- pointer 点击目录项、键盘 `Enter/Space` 或方向键选择均定位同一章节。
- 当前章节使用选中态、`aria-current="location"` 和可见文本共同表达，不只依赖颜色。
- 定位后把焦点移到对应章节标题，或在不打断连续阅读时更新可访问状态提示；不得把焦点留在不可见位置。
- 长目录独立滚动，正文滚动不导致顶部安全返回和下载动作消失到不可恢复位置。

### 5.3 下载与任务反馈

- V1 只有 PDF 时使用单一 Button，不展示 Dropdown 箭头和未批准格式。
- 下载前权限复核期间按钮显示“校验权限中”；生成期间由任务层显示“准备来源快照 / 生成 HTML 与 PDF / 写入个人资产”。
- Modal 关闭只关闭反馈层，不取消后台任务；若未来支持取消任务，须先回到任务系统产品定义，本文不推断取消能力。
- Notification 只用于后台任务完成入口；页面级失败使用 Result/Alert，不依赖瞬时 Message 承载关键信息。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 | 上下文规则 |
|---|---|---|---|
| Reader 首次加载 | 保留标题栏、元信息和目录轮廓，正文 Skeleton；动态状态可被辅助技术感知 | 自动完成或进入加载失败 | 不闪回来源页，不清空安全路由参数 |
| 无可报告内容 | F-EXPORT-01 保持区块，生成按钮 disabled，并说明原因 | 回来源业务内容处理 | 不创建任务 |
| 必需章节缺失 | 结构校验错误，列出缺失的产品章节名称 | 返回来源模块修复 | 不渲染伪空报告 |
| 页面加载失败 | F-EXPORT-04 页面级错误 + 重试 | 重试同一修订或返回来源 | 保留 `report_revision_id`，不显示旧缓存冒充成功 |
| `forbidden` | “无权查看此报告”，隐藏敏感元数据 | 返回来源页面 | 不提供文件地址、对象摘要和下载 |
| `expired` | “PDF 文件已过期” | 当前授权允许时重新生成 | HTML 修订有效时继续可读 |
| `source_invalid` | “报告来源已失效” | 返回来源页面 / 联系管理员 | 不自动用最新数据替代 |
| `artifact_missing` | “PDF 暂不可用” | 重新生成 PDF | HTML 阅读和目录位置保持 |
| `failed` | 可理解原因、追踪编号、是否可重试 | 按任务规则重试或返回 | 不无限重试，不丢任务身份 |
| 资产回跳失败 | 资产卡局部错误，记录仍在 | 再次查看报告 | 保持个人资产列表位置 |

错误文案必须回答“发生了什么、当前内容是否安全、用户下一步能做什么”。状态同时使用文本与图标/可访问名称，不只用颜色。

## 7. 组件、键盘与无障碍

| 交互对象 | Arco / 语义映射 | Pointer | Keyboard / Focus | ARIA、disabled、loading |
|---|---|---|---|---|
| 返回来源 | `Button` 或语义链接 | 点击返回 | `Tab` 聚焦，`Enter` 激活；返回后焦点回来源报告区块或来源标题 | 可访问名称含“返回来源结果”；无安全路由时 disabled 并说明 |
| 生成/查看/下载 | `Button` | 单击触发 | `Tab` + `Enter/Space`；任务开始后焦点保持按钮或进入 Modal 标题 | loading 时 `aria-busy`; disabled 阻止重复提交并提供原因 |
| 报告目录 | `nav` + 可访问目录项，视觉可用定制组件 | 点击定位 | 方向键移动，`Home/End` 首尾，`Enter/Space` 定位 | `aria-label="报告目录"`；当前项 `aria-current` |
| 报告正文 | `main/article/section` | 连续阅读与区块内横滚 | 章节标题可程序化聚焦；跳转后焦点可见 | 标题层级连续；图表提供摘要或等价表格 |
| 元信息 | `Descriptions` 或语义定义列表 | 文本查看 | 按阅读顺序到达 | 缺失值显示“未提供”，字段名不省略 |
| 任务反馈 | `Modal` + `Steps/Progress/Alert` | 关闭、查看任务 | 打开后焦点进入标题或首个操作；`Esc` 关闭；关闭回触发按钮 | `role="dialog"`、可访问标题；状态更新使用 live region |
| 异常结果 | `Result` + `Alert` + `Button` | 执行恢复动作 | 标题先获程序化焦点，动作按主次顺序 | 错误/权限状态有文本；敏感内容不进入 DOM |
| 评审挂点 | `Button/Popover`，仅评审模式 | 点击打开 payload | `Tab`、`Enter/Space` 打开，`Esc` 关闭，焦点返回宿主 | 可访问名称包含宿主；业务模式完全 absent |

通用要求：

- 所有自定义控件保留清晰 `focus-visible`，对比度满足 WCAG AA 基线。
- reading、目录、返回、下载、重试、关闭和查看任务均有键盘等价路径。
- 异步状态、权限复核结果和任务完成可被辅助技术感知；状态变化不强抢用户正在阅读的焦点。
- PDF 是静态产物，不包含按钮、Tooltip、Popover、评审挂点或业务模式之外的内部信息。
- 状态不可只靠色彩表达；图标按钮均有可访问名称。

## 8. 响应式行为

本模块只覆盖 `medium_1440_1920`。三档均保持详情/报告工作台，不切换移动端，不采用 Track-L 大屏驾驶舱。

| 宽度 | Shell 与导航 | F-EXPORT-02 Reader | F-EXPORT-01 / 03 / 04 / 05 |
|---:|---|---|---|
| 1920 | 默认可展开左侧导航；24 栅格、16px gutter；报告内容外壳最大宽约 1440 | 目录 240px；正文自适应；元信息单行优先；顶部返回、标题、下载保持明确层级 | 来源区块主动作右对齐；Modal 使用适合任务的中等宽度；Result 居中但不变成大屏海报；资产卡动作完整显示 |
| 1680 | 保持用户导航选择，优先缩减外围留白 | 保持双栏；目录 240px 或按空间收缩至 216px；元信息可在语义组间换行 | 主动作不与标题重叠；Modal、Result 与资产卡保持相同操作顺序 |
| 1440 | 默认导航收起到 64px；仍使用 24 栅格和 16px gutter | 目录 216px；正文最小有效宽度 920px；长表格/图表只在内容区横向滚动；标题和下载空间不足时分行但下载仍可见 | 来源区块说明先换行、主动作不缩成纯图标；Modal 不超出视口；资产卡元信息分行，操作区不遮挡内容 |

共同规则：

- 固定核心章节、动作可用性、权限结果和评审 payload 不因宽度改变。
- 长标题允许两行并保留完整可访问名称；不通过省略关键报告身份换取单行。
- 目录和正文各自滚动时必须保留清晰边界；图表横滚不能带动整页横向溢出。
- 本轮不定义 `<1440px` 折叠目录、底部抽屉、触控优先手势或移动端导航。

## 9. 内部评审投影

仅投影 Wireframe §11 的 7 个唯一挂点，不创建额外挂点。

| mount_id | Frame / 精确宿主 | 状态 | payload | 模式 |
|---|---|---|---|---|
| `ENT-EXPORT-F01-ENTRY-TITLE` | F-EXPORT-01 / “分析报告”标题 | not_generated / preparing / generating / ready | source_location, source_summary, current_placement, source_relation | review present；business absent |
| `ENT-EXPORT-F02-REPORT-TITLE` | F-EXPORT-02 / 报告标题 | ready | source_location, source_summary, current_placement, source_relation | review present；business absent |
| `ENT-EXPORT-F02-SOURCE-TITLE` | F-EXPORT-02 / “数据来源与生成说明”标题 | ready | source_task_id, source_snapshot_id, report_revision_id, template_version, data_version, algorithm_version | review present；business absent |
| `ENT-EXPORT-F02-LIMITATION-TITLE` | F-EXPORT-02 / “局限性与使用边界”标题 | ready | evidence_boundary, missing_data_policy, permission_boundary | review present；business absent |
| `ENT-EXPORT-F03-TASK-TITLE` | F-EXPORT-03 / “报告生成任务”标题 | preparing / generating / ready / failed | report_fingerprint, artifact_formats, task_owner, source_route | review present；business absent |
| `ENT-EXPORT-F04-STATE-TITLE` | F-EXPORT-04 / 报告不可用状态标题 | forbidden / expired / source_invalid / artifact_missing / failed | state_code, permission_policy_ref, recovery_action, audit_ref | review present；business absent |
| `ENT-EXPORT-F05-ASSET-TITLE` | F-EXPORT-05 / 报告资产标题 | ready / expired / forbidden | report_id, report_revision_id, source_module, return_route | review present；business absent |

投影规则：

- 每个挂点使用独立 `mount_id`；不得用页级横幅、统一问号或图标簇替代。
- 打开后完整呈现 `required_payload`；字段缺失显示字段名与“未提供”，不静默省略。
- 业务模式下 7 个挂点均不得出现在 DOM；切换评审模式不得改变内容、修订、权限、章节和动作。
- 所有评审标记与 payload 均不得进入 PDF。
- 本模块不创建 `metric_spec / mock_badge / pending_badge` 挂点；消费者指标继续由来源模块定义。

## 10. Demo 实施交接

### 10.1 页面包与边界

| 交付单元 | 所有者 | 交接重点 |
|---|---|---|
| 来源报告入口适配 | 首个消费者 ENT-EVAL；第二消费者 ENT-RISK | 状态协议、唯一主动作、内容/快照/权限/安全路由提交 |
| ENT-EXPORT Reader | ENT-EXPORT | 只读目录与正文、同修订身份、元信息、下载和异常态 |
| 报告任务反馈 | SYS-ANALYSIS-JOBS | 任务阶段、队列、重试、后台完成、跨登录恢复 |
| 个人资产投影 | SYS-ANALYSIS-JOBS / 个人中心 | 报告身份、同修订恢复、安全查看与下载 |

共享组件候选：`ReportReaderShell`、`ReportTableOfContents`、`ReportMetadata`、`ReportSection`、`ReportUnavailableResult`、`ReportDownloadAction`、评审模式既有挂点组件。候选名称不构成代码 API 或新增产品能力。

适配器输入必须符合 `REPORT-CONTRACT-ENT-EXPORT.md` v0.1。不得直接把 ENT-EVAL 专用模型作为共用接口；ENT-EVAL 和 ENT-RISK 分别完成来源字段到五个共用对象的转换。

### 10.2 状态模型与测试关注点

- 覆盖 `not_generated / preparing / generating / ready / failed / forbidden / expired / source_invalid / artifact_missing`。
- 覆盖单企、双企、多企内容，固定核心章节完整，扩展章节按系统规则装配。
- 验证 HTML/PDF 同一 `report_revision_id`，旧模板修订不被新模板静默替换。
- 验证权限降级、文件过期、PDF 缺失但 HTML 有效、来源快照失效、重复提交和跨登录恢复。
- 验证 1920 / 1680 / 1440，长标题、长目录、长表格、图表横滚、键盘与焦点。
- 验证评审模式 7 个挂点完整、业务模式 0 个挂点、PDF 0 个内部标记。
- 验证业务 HTML/PDF 保留业务化来源、版本和局限性，不因隐藏内部编码而删除核心内容。
- 验证 ENT-RISK 两类报告均不需要提交评估模式、权重、评分、排名、雷达图或评估模板配置。

### 10.3 明确排除

不实现正文/章节/模板编辑，DOCX/PPTX/XLSX，占位格式菜单，独立全局报告中心，任务队列和个人资产页面的重复实现，业务指标/算法/结论生成，以及未经批准的取消任务能力。

本节授权按上述边界进入 V1 首轮 Demo：仅形成高保真验证证据，必须显式登记下游缺口及对应处理，不得宣称正式范围、接口、PDR、V1-FINAL、V2 或生产交付已经闭合。

## 11. 缺口与阻断项

| ID | 摘要 | `blocks_v1` | `blocks_stages` | V1 处理 | Owner / deadline | return_to |
|---|---|---:|---|---|---|---|
| `GAP-ENT-EXPORT-SCOPE-01` | 跨模块系统报告复用框架缺少正式 `approved_scope_change` | false | PDR / V1-FINAL / V2 / production | `review_only_gap`：只形成未激活范围的 V1 高保真证据，不登记活动叶子 | 郭万迎 / 项目负责人；before_pdr | approval / TRACE |
| `GAP-ENT-EXPORT-CONTRACT-01` | 产品字段和消费者映射已固定，但技术接口、指纹算法、有效期、下载授权、审计枚举和接口归属未闭合 | false | PDR / V1-FINAL / V2 / production | `deterministic_demo_contract`：使用产品契约 v0.1、固定 fixture 和 fail-closed 权限，不承诺最终接口或枚举 | 侯佳伟；before_pdr | TRACE；涉及字段/状态时回 Wireframe |
| `GAP-ENT-EXPORT-CATALOG-01` | 门户报告管理 Bid 锚点未进入当前验收目录与 scope baseline 可计数条目 | false | PDR / V1-FINAL / V2 / production | `review_only_gap`：保留 Bid 上下文和零计数结论，不新增、迁移或虚增验收叶子 | 郭万迎；before_pdr | TRACE / approval |
| `GAP-ENT-EXPORT-HISTORY-01` | 现有 PDR-G1 的 blocked 状态与历史“已通过”表述冲突 | false | PDR / V1-FINAL / V2 / production | `manual_review`：V1 不继承历史通过结论，不改变任务台账或 Gate 状态 | 郭万迎；before_pdr_or_task_registration | task / approval |

已关闭记录：`GAP-ENT-EXPORT-CONSUMER-02` 已通过 `ENT-RISK-第二消费者一致性验证.md` 完成产品定义层验证；未声明代码适配、同源产物或 V1 视觉验证。

当前没有 `blocks_v1: true` 的缺口，故本文可为 `ready_for_v1`。上述缺口仍阻断其列明的后续阶段；若产品字段、路由、权限或状态因后续评审变化，必须先回写对应四件套，再重新生成受影响 UX-SPEC 段落并使既有 V1 证据失效。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: ENT-EXPORT
  version: "0.4"
  status: ready_for_v1
  source_four_pack:
    - IA-ENT-EXPORT.md
    - TRACE-ENT-EXPORT.yaml
    - USM-ENT-EXPORT.md
    - Wireframe-ENT-EXPORT.md
  source_four_pack_version: "0.5"
  product_contract:
    path: REPORT-CONTRACT-ENT-EXPORT.md
    version: "0.1"
    status: product_definition_baseline_confirmed
    technical_interface_freeze: pending
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-EXPORT-READ
      role: ROLE-EXPORT-GOV
      story_refs: [US-ENT-EXPORT-READ]
      primary_flow: [enter_from_source_result, generate_or_open_report, read_same_revision, return_to_source]
      abnormal_flows: [content_incomplete, load_failed, forbidden, source_invalid, return_failed]
    - journey_id: J-EXPORT-EVIDENCE
      role: ROLE-EXPORT-RESEARCH
      story_refs: [US-ENT-EXPORT-EVIDENCE]
      primary_flow: [open_reader, inspect_scope_and_versions, inspect_evidence_and_sources, inspect_limitations]
      abnormal_flows: [metadata_missing, evidence_missing, low_confidence, source_unavailable, old_template_revision]
    - journey_id: J-EXPORT-PDF
      role: ROLE-EXPORT-GOV
      story_refs: [US-ENT-EXPORT-PDF]
      primary_flow: [request_pdf, recheck_permission, reuse_or_generate_artifact, download_same_revision]
      abnormal_flows: [forbidden, expired, artifact_missing, generation_failed]
    - journey_id: J-EXPORT-RESUME
      role: ROLE-EXPORT-RESEARCH
      story_refs: [US-ENT-EXPORT-RESUME]
      primary_flow: [open_personal_asset, follow_safe_return_route, recheck_permission, restore_same_revision]
      abnormal_flows: [forbidden, expired, source_invalid, return_route_failed]
  frame_specs:
    - frame_id: F-EXPORT-01
      route_or_host: source_module_defined_result_route
      owner: source_business_module
      source_refs: [US-ENT-EXPORT-READ]
      states: [not_generated, preparing, generating, ready, disabled_no_content, error, forbidden, expired]
      interactions: [generate_report, view_report, view_task]
    - frame_id: F-EXPORT-02
      route_or_host: source_module_defined_report_route
      owner: ENT-EXPORT
      source_refs: [US-ENT-EXPORT-READ, US-ENT-EXPORT-EVIDENCE, US-ENT-EXPORT-PDF, US-ENT-EXPORT-RESUME]
      states: [loading, ready, source_invalid, error, forbidden]
      interactions: [return_to_source, navigate_toc, read_sections, download_pdf]
    - frame_id: F-EXPORT-03
      route_or_host: system_task_layer
      owner: SYS-ANALYSIS-JOBS
      source_refs: [US-ENT-EXPORT-PDF]
      states: [preparing, generating, ready, failed, forbidden]
      interactions: [close_feedback, view_task, retry_when_allowed]
    - frame_id: F-EXPORT-04
      route_or_host: source_module_defined_report_route
      owner: ENT-EXPORT
      source_refs: [US-ENT-EXPORT-READ, US-ENT-EXPORT-PDF, US-ENT-EXPORT-RESUME]
      states: [forbidden, expired, source_invalid, artifact_missing, failed, retrying]
      interactions: [return_to_source, regenerate_pdf, retry_when_allowed]
    - frame_id: F-EXPORT-05
      route_or_host: /personal/assets
      owner: SYS-ANALYSIS-JOBS
      source_refs: [US-ENT-EXPORT-RESUME]
      states: [loading, ready, empty, error, expired, forbidden]
      interactions: [view_same_revision, request_download, retry_return_route]
  feedback_rules:
    - trigger: first_reader_load
      response: stable_shell_with_metadata_and_content_skeleton
      recovery: load_same_revision_or_show_F_EXPORT_04
    - trigger: report_generation_or_pdf_generation
      response: task_progress_in_system_task_layer
      recovery: background_continue_view_task_or_rule_based_retry
    - trigger: permission_recheck_failed
      response: forbidden_without_sensitive_metadata
      recovery: return_to_source
    - trigger: artifact_expired_or_missing
      response: keep_valid_html_and_explain_pdf_state
      recovery: regenerate_pdf_when_authorized
    - trigger: source_snapshot_invalid
      response: source_invalid_without_silent_latest_data_substitution
      recovery: return_to_source_or_contact_administrator
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, live_region, non_color_status, document_structure]
  review_mounts:
    - ENT-EXPORT-F01-ENTRY-TITLE
    - ENT-EXPORT-F02-REPORT-TITLE
    - ENT-EXPORT-F02-SOURCE-TITLE
    - ENT-EXPORT-F02-LIMITATION-TITLE
    - ENT-EXPORT-F03-TASK-TITLE
    - ENT-EXPORT-F04-STATE-TITLE
    - ENT-EXPORT-F05-ASSET-TITLE
  gaps:
    - id: GAP-ENT-EXPORT-SCOPE-01
      summary: formal_approved_scope_change_missing
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: review_only_gap
      owner: human:郭万迎
      deadline: before_pdr
      return_to: approval_and_TRACE
    - id: GAP-ENT-EXPORT-CONTRACT-01
      summary: report_contract_and_ownership_not_closed
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:侯佳伟
      deadline: before_pdr
      return_to: TRACE_and_Wireframe
    - id: GAP-ENT-EXPORT-CATALOG-01
      summary: bid_anchor_not_countable_in_current_catalog_and_scope_baseline
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: review_only_gap
      owner: human:郭万迎
      deadline: before_pdr
      return_to: TRACE_and_approval
    - id: GAP-ENT-EXPORT-HISTORY-01
      summary: historical_pdr_status_conflict
      blocks_v1: false
      blocks_stages: [pdr, v1_final, v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: manual_review
      owner: human:郭万迎
      deadline: before_pdr_or_task_registration
      return_to: task_and_approval
```
