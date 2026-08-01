# UX-SPEC-ENT-RECRUIT｜引育推荐

> 版本：v1.2 · 2026-07-31
> 状态：ready_for_v1
> 四件套版本：v1.9
> Track：Track-MS
> screen_tier：medium_1440_1920

## 1. 权威输入与边界

本规格只把当前四件套转译为可执行交互，不改变产品范围，不修改 Demo 代码。

- 产品输入：`IA-ENT-RECRUIT.md`、`TRACE-ENT-RECRUIT.yaml`、`USM-ENT-RECRUIT.md`、`Wireframe-ENT-RECRUIT.md`，版本均为 v1.9。
- 治理输入：`产品定义评审规程.md`、`UX-UE 通用交互组件规范.md`、`Design.md`、`data-lineage-policy.md`。
- 原始需求仍仅来自四件套登记的两份 `bid-reference`；本规格不新增角色、字段、路由、权限、指标或模型语义。
- 本次评审修订落实 `DEC-ENT-RECRUIT-IN-TAB-REVIEW-20260731` 及其入口隔离补充：指定对象复核必须在当前候选工作台 Tab 内完成，且条件筛选推荐 / 候选工作台分别拥有任务、过程和结果上下文。
- 本次报告修订落实 `DEC-ENT-RECRUIT-REPORT-CONSUMER-20260731`：招引 / 培育报告分别适配 ENT-EXPORT，共用 Reader 与同修订 PDF；推荐数据导出保持独立，不经过报告 Reader。
- `product_scope_mutation: prohibited`；`demo_code_mutation: prohibited`。

## 2. 四件套同步核对

| 核对项 | 四件套结论 | UX 投影 |
| --- | --- | --- |
| 路由与入口 | `/enterprise/recommendation`；招引 / 培育视图下各有条件筛选推荐 / 候选工作台 | 不预设 URL 参数；内部状态不改变入口 Tab |
| 指定对象复核 | `US-ENT-RECRUIT-L2`，当前候选集合内复核 | `candidate_list → review_config → review_process → review_result → candidate_list` |
| 参数配置 | `F-RECRUIT-REVIEW-CONFIG` | 当前候选工作台内嵌配置区；复用条件筛选推荐的统一判定模型布局，只渲染模型契约实际提供的参数 |
| 异步过程 | `F-RECRUIT-PROCESS`、`US-ENT-RECRUIT-R3` | 五阶段、稍后查看、系统任务层恢复 |
| 结果语义 | 招引 / 培育结果 Frame；指定集合排名 | 标题为“人工线索复核结果”，不得冒充全量排名 |
| 上下文保持 | 返回候选列表恢复原上下文 | 恢复视图、筛选、分页和未失效选择 |
| 入口状态隔离 | 条件筛选推荐 / 候选工作台的任务、过程和结果互不复用 | 状态键包含 `view + entry`；切换只挂载目标入口，切回恢复原任务进度或结果 |
| 报告消费者 | A3 / C3；两类不可变来源快照与七核心章节 | `attraction_recommendation_analysis_report / cultivation_recommendation_analysis_report` → ENT-EXPORT Reader → 同修订 PDF；返回恢复来源结果上下文 |
| 推荐数据导出 | A3 / C3；当前权限可见推荐结果 | 独立携带视图、筛选、排序、列、对象范围和数据版本；不生成报告章节或 `report_revision_id` |
| 状态 | initial、loading、success、empty、partial、error、permission 及候选特有状态 | 每个 Frame 明确进入、反馈和恢复动作 |
| 禁止行为 | 不编辑公式，不补造阈值 / 权重，不混用招引 / 培育，不自建任务中心 | 控件级 disabled、校验、焦点与恢复规则 |
| 屏幕层级 | `medium_1440_1920` | 覆盖 1920 / 1680 / 1440 |
| 评审挂点 | Wireframe 共 18 个唯一 mount | 全量投影；business mode 全部 absent |

差异结论：`F-RECRUIT-REVIEW-CONFIG` 与报告消费者映射已在 IA、TRACE、USM、Wireframe 中同步，无孤立 Frame、故事或状态。九个未决项均已分类为不阻断 V1，并具有显式安全的 V1 处理；它们继续阻断 PDR、V1-FINAL、V2 与生产闭合。

## 3. 用户旅程与任务流

### J-RECRUIT-01 条件筛选推荐

- 角色：政府招商与产业管理人员、园区运营与企业服务人员、投资机构 / 投资平台产业研究人员；培育还包括行业协会产业服务人员。
- Story：`US-ENT-RECRUIT-A1/A2/A3`、`US-ENT-RECRUIT-C1/C2/C3`、`US-ENT-RECRUIT-R1/R2/R3`。
- 主路径：选择招引或培育 → 进入条件筛选推荐 → 设置当前视图条件 → 显式执行分析 → 五阶段过程 → 完整结果 → 详情 / 风险复核 → 报告或导出。
- 异常恢复：空结果保留条件；失败保留输入并重试；无权限不泄露数量和详情；版本不一致保留上一版可追溯结果。

### J-RECRUIT-02 当前 Tab 指定对象复核

- 角色：四类已登记产品角色。
- Story：`US-ENT-RECRUIT-L1/L2`、`US-ENT-RECRUIT-R3`。
- 主路径：候选工作台选择对象 → 点击“执行指定对象复核” → 当前 Tab 内将候选列表切换为内嵌参数配置区 → 校验并提交 → 当前 Tab 内五阶段过程 → 当前 Tab 内人工线索复核结果 → 返回候选列表。
- 上下文：进入配置前保存 `view`、候选筛选、页码、每页数量和选择集合；返回时恢复仍有效的上下文。
- 异常恢复：超过数量上限时不打开配置；参数契约不可用时主按钮 disabled；字段校验失败不创建任务；任务失败保留配置快照并提供原配置重试。
- 严禁：点击执行后切换到条件筛选推荐 Tab，或使用条件筛选表单作为复核配置页。
- 隔离：候选复核处于排队、运行、成功或失败时，切换到条件筛选推荐不得显示该复核的五阶段过程或结果列表；切回候选工作台后恢复。

### J-RECRUIT-03 对比篮研判闭环

- 角色：四类已登记产品角色。
- Story：`US-ENT-RECRUIT-L3`、`US-ENT-RECRUIT-R2`。
- 主路径：从结果或候选工作台选择企业 → 加入对比篮 → 发起企业评估 / 风险洞察 → 使用 `return_context_id` 返回原候选工作台 → 查看证据 → 人工确认 / 待定 / 排除。
- 异常恢复：容量不足整批阻断；返回上下文失效时保留候选记录并允许手工关联。

### J-RECRUIT-04 异步任务恢复

- 角色：四类已登记产品角色。
- Story：`US-ENT-RECRUIT-R3`。
- 主路径：提交分析 → 查看当前阶段 → 稍后查看 → 从系统任务浮层或个人中心恢复 → 回到原招引 / 培育语境和对应结果。
- 异常恢复：恢复时校验用户、任务类型、输入指纹和结果版本；不匹配时阻止挂载并说明原因。

### J-RECRUIT-05 报告阅读与推荐数据导出

- 角色：四类已登记产品角色；招引报告不包含行业协会专属培育语境。
- Story：`US-ENT-RECRUIT-A3`、`US-ENT-RECRUIT-C3`。
- 报告主路径：当前结果 → 生成分析报告 → 冻结来源任务与结果快照 → preparing / generating → ready → ENT-EXPORT 只读 Reader → 下载同 `report_revision_id` PDF或返回来源结果。
- 数据导出主路径：当前结果 → 导出数据 → 固定视图、筛选、排序、列、对象范围、数据版本与权限上下文 → 直接生成或后台生成 → 当前页 / Notification 反馈去向。
- 异常恢复：报告来源失效时重新执行分析；报告失败按原快照重试；无权限不显示正文或下载地址；数据过大提示缩小范围或后台生成；两类任务失败互不覆盖。
- 严禁：从当前 DOM 拼装报告、让用户编辑正文 / 章节、把 HTML / PDF 当作推荐数据导出格式、把评审 payload 写入业务 HTML 或 PDF。

## 4. Frame 与承载映射

| Frame | 宿主与入口 | 退出与上下文 |
| --- | --- | --- |
| `F-RECRUIT-A-CONFIG` | 招引推荐 → 条件筛选推荐 | 执行后进入过程；切视图时保留未提交招引条件 |
| `F-RECRUIT-A-RESULT` | 招引条件分析或招引指定对象复核成功 | 调整条件返回招引配置；指定对象结果返回候选列表 |
| `F-RECRUIT-C-CONFIG` | 培育推荐 → 条件筛选推荐 | 执行后进入过程；切视图时保留未提交培育条件 |
| `F-RECRUIT-C-RESULT` | 培育条件分析或培育指定对象复核成功 | 调整条件返回培育配置；指定对象结果返回候选列表 |
| `F-RECRUIT-CANDIDATES` | 当前招引 / 培育视图 → 候选工作台 | 保存筛选、分页、选择和当前候选状态 |
| `F-RECRUIT-REVIEW-CONFIG` | 候选工作台内嵌配置区 | 返回候选列表；提交后当前 Tab 进入过程 |
| `F-RECRUIT-PROCESS` | 当前业务宿主内的过程区或系统任务恢复入口 | 完成进入对应结果；稍后查看只关闭当前可视面 |
| `F-RECRUIT-SERVICE-CONTRACT` | 仅评审模式的非业务页面契约摘要 | 业务模式无入口、无占位 |

报告生成后的 `F-EXPORT-02 / F-EXPORT-03 / F-EXPORT-04` 由 ENT-EXPORT 拥有，不计入引育推荐本地 Frame 数。来源结果 Frame 必须通过 `source_result_route / source_report_route` 与 Reader 双向恢复，不能复制一份消费者私有 Reader。

## 5. 交互与状态转换

### 5.1 指定对象复核状态机

| 触发 | 前置 | 转换与反馈 | 可逆操作 | 禁止行为 |
| --- | --- | --- | --- | --- |
| 点击执行指定对象复核 | 当前为候选工作台，已选择合法对象且不超上限 | `candidate_list → review_config`；候选列表切换为内嵌配置区，焦点进入标题 | 返回候选列表 | 改变当前 Tab或打开 Modal |
| 加载参数契约 | 内嵌配置区已进入 | 显示 Skeleton；成功后渲染契约字段 | 返回候选列表 | 复用条件筛选字段凑配置 |
| 参数契约失败 | 契约不可用 | Alert 说明原因，主按钮 disabled | 关闭或重试加载 | 创建任务或补默认值 |
| 参数校验失败 | 用户确认提交 | 保留输入，显示字段错误并聚焦首个错误 | 修改后重试 | 清空配置或提交无效任务 |
| 参数校验成功 | 契约与权限有效 | 创建一次任务，`review_config → review_process` | 稍后查看 | 重复提交 |
| 任务成功 | 五阶段完成 | `review_process → review_result`，标题固定“人工线索复核结果” | 返回候选列表 | 跳到条件筛选结果入口 |
| 返回候选列表 | 当前为复核结果 | `review_result → candidate_list`，恢复保存的上下文 | 可再次选择并复核 | 清空筛选、分页或仍有效选择 |

### 5.2 参数配置规则

- 内嵌配置区标题为“指定对象模型参数配置”，副标题显示当前招引 / 培育视图和已选数量；布局、权重控件、平均分配和合计校验与条件筛选推荐的统一判定模型保持一致。
- 对象集合、业务视图、模型版本、数据版本、参数版本为只读快照。
- 可编辑字段只能来自模型契约返回的 schema；字段类型、必填、范围、枚举和默认值均来自该 schema。
- Q015 或其他未闭合参数显示 pending / disabled 及原因；不得把 Demo 值或前端常量作为正式默认。
- 返回候选列表不改变候选状态，不清空选择，不切换 Tab。
- 提交中主按钮进入 loading 并防重复点击；关闭能力按任务创建是否完成分别处理。

### 5.3 列表、结果与批量操作

- 表头全选只选当前页；“全选当前筛选结果 Y 家”明确跨页范围。
- 局部筛选不重跑模型，不改变结果版本，不重编号原始排名。
- 超出对比篮容量或指定对象上限时整批阻断，不静默截断。
- 招引 / 培育、条件筛选 / 指定对象任务分别保存输入快照与结果引用。
- 每个 `view + entry` 独立保存 `analysis_state`、`task_id`、输入 / 参数快照、五阶段过程、结果引用、局部筛选、分页和选择集合；入口切换不得覆盖另一份状态。

### 5.4 报告与推荐数据导出状态机

| 触发 | 前置 | 转换与反馈 | 恢复 | 禁止行为 |
| --- | --- | --- | --- | --- |
| 生成分析报告 | 当前结果成功、来源快照与权限上下文有效 | `not_generated → preparing → generating`；按钮 loading，持续任务使用 Notification / 系统任务入口 | 继续浏览当前结果 | 重复创建、清空结果、用旧报告替代当前版本 |
| 报告生成成功 | 七核心章节、证据、安全路由与权限校验通过 | `generating → ready`；主动作变为“查看分析报告” | 进入 Reader，返回恢复来源结果 | 允许正文编辑、章节配置或混用招引 / 培育报告类型 |
| 下载 PDF | Reader ready 且下载权限通过 | 下载与 HTML 同一 `report_revision_id` 的 PDF | 下载失败仍可阅读 HTML 并重试 | 静默切换修订、在 PDF 写入评审标识或内部 ID |
| 报告失败 / 来源失效 | 生成失败或快照不可复现 | `failed / source_invalid`；局部 Alert，不影响推荐结果 | 原快照重试或重新执行分析 | 表现为空结果、生成残缺报告 |
| 导出推荐数据 | 当前结果存在可见数据 | 独立 `preparing → generating → success`；记录当前导出上下文 | 即时下载或后台完成通知 | 创建报告章节、产生 `report_revision_id`、复用 Reader |
| 导出数据过大 | 超过暂定阈值 | `too_large`；提示缩小范围或转后台生成 | 保留筛选、分页和选择 | 静默截断或默认导出前若干家 |

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| 无候选选择 | 按钮 disabled；辅助文本说明需先选择对象 | 选择合法候选 |
| 培育范围不符 | 行级显示范围不符，批量提交前列出不可提交数量 | 移除或显式转为招引线索 |
| 参数契约加载中 | 内嵌配置区显示 Skeleton，返回可用，提交不可用 | 等待或返回候选列表 |
| 参数契约不可用 | Alert 展示不可提交原因，不展示伪字段 | 重试加载或关闭 |
| 参数校验失败 | 字段级错误 + 顶部错误摘要 | 聚焦首个错误并修改 |
| 任务排队 / 运行 | 五阶段、当前阶段、稍后查看 | 系统任务层恢复 |
| 任务失败 | 保留任务引用和参数快照，明确失败不等于空结果 | 以原配置重试 |
| 空复核结果 | 显示“分析成功但当前指定对象无可用结果” | 返回候选列表调整对象 |
| 部分字段缺失 | 字段显示“暂无数据”，指标保留 pending / GAP | 查看可用结果 |
| 无权限 | 隐藏数量、参数详情、结果与导出 | 返回或申请授权 |
| 恢复上下文失效 | 保留任务结果入口，说明无法恢复旧筛选 | 回候选列表建立新上下文 |
| 报告准备 / 生成中 | 结果页保持可读，报告按钮 loading，持续反馈可进入任务层 | 继续浏览或稍后进入 Reader |
| 报告来源失效 | 局部 Alert 说明不可复现，不显示残缺 Reader | 重新执行分析后再生成 |
| 报告无权限 | 不显示正文、内部元数据或下载地址 | 返回来源结果或申请授权 |
| 推荐数据导出失败 / 过大 | 保留导出上下文，说明失败原因或后台生成选项 | 原上下文重试、缩小范围或等待通知 |

## 7. 组件、键盘与无障碍

| 场景 | Arco / 共享组件 | Pointer 与键盘 | 焦点 / ARIA |
| --- | --- | --- | --- |
| 双层 Tab | `Tabs` | 点击或方向键切换；只有用户操作才切换 | `role=tablist/tab/tabpanel`，当前项 `aria-selected=true` |
| 候选表格 | `Table` + `Checkbox` + `Pagination` | 行选择、Space 切换复选框、分页按钮可键盘触达 | 表头全选和行选择有明确 accessible name |
| 参数配置 | `SectionPanel` + `Form` | Enter 仅在表单有效且焦点不在多行输入时提交；返回按钮恢复候选列表 | 进入后焦点到标题；返回列表后焦点回“执行指定对象复核”按钮 |
| 参数字段 | `Form.Item`、`Select`、`InputNumber` 等契约映射控件 | Tab 顺序按视觉顺序；错误字段可直接聚焦 | `aria-invalid`、`aria-describedby` 关联错误说明 |
| 五阶段过程 | `Steps` + `Alert` | 稍后查看按钮可键盘触达 | 当前阶段使用 `aria-current=step`，状态变化用非打断式 live region |
| 结果与详情 | `Table` + `Drawer` | Enter 打开详情，Esc 关闭 Drawer | Drawer 标题含企业名，关闭后回原触发行 |
| 报告与数据导出 | `Button` + `Notification`；Reader 由 ENT-EXPORT 提供 | Enter 触发；生成中防重复；Reader 目录、返回和下载均可键盘触达 | 状态变化使用 live region；返回后焦点回“查看 / 生成分析报告”；两个导出动作具有不同 accessible name |
| 评审标记 | `RequirementTrace`、`MetricSpecCard`、`PendingBadge` | 只在评审模式可触达 | business mode 不渲染节点，不改变业务 accessible name |

- 所有 disabled 控件必须同时提供邻近原因，不能只靠颜色。
- loading 状态保留控件尺寸，避免布局跳动。
- 焦点可见性、文本 / 背景对比度和状态色使用遵循 `Design.md`。

## 8. 响应式行为

| 宽度 | 布局与优先级 | 指定对象复核 |
| --- | --- | --- |
| 1920 | 名单与详情双栏；筛选、结果摘要和批量栏完整展开 | 内嵌配置三列展示统一判定模型，与条件筛选推荐一致 |
| 1680 | 保留双栏，收紧非关键留白；表格中间字段可横向滚动 | 内嵌配置三列保持，非关键留白收紧，对象摘要单行优先 |
| 1440 | 名单为主，详情使用右侧 Drawer；固定首列与操作列，批量主操作始终可见 | 内嵌配置随工作区宽度响应，不使用 Modal、不切换 Tab；提交操作始终可见 |

- 三档均保持双层 Tab 可见，指定对象复核的内部状态不改变选中 Tab。
- 页面只声明 `medium_1440_1920`；不产生 `<1440px` 产品交付承诺。
- 表格横向滚动不得隐藏企业名称、选择列和当前候选状态。
- 三档结果页均保持“生成 / 查看分析报告”与“导出数据”为两个独立动作；Reader 自身按 ENT-EXPORT 的 1920 / 1680 / 1440 规则响应，本模块不得复制或改写其布局。

## 9. 内部评审投影

下列 mount 均投影到 Wireframe 指定 host；`review_mode: present`，`business_mode: absent`：

- `SYS-JOBS-F03-PROCESS-TITLE`
- `ENT-RECRUIT-F01-CONFIG-TITLE`
- `ENT-RECRUIT-F02-RESULT-TITLE`
- `ENT-RECRUIT-F02-MANUAL-RESULT-TITLE`
- `ENT-RECRUIT-F02-METRIC-DETAIL`
- `ENT-RECRUIT-F02-MODEL-STATUS`
- `ENT-RECRUIT-F02-LARGE-RESULT`
- `ENT-RECRUIT-F02-RISK-CREDIT`
- `ENT-RECRUIT-F03-CONFIG-TITLE`
- `ENT-RECRUIT-F04-RESULT-TITLE`
- `ENT-RECRUIT-F04-MANUAL-RESULT-TITLE`
- `ENT-RECRUIT-F04-METRIC-DETAIL`
- `ENT-RECRUIT-F04-MODEL-STATUS`
- `ENT-RECRUIT-F04-LARGE-RESULT`
- `ENT-RECRUIT-F04-RISK-CREDIT`
- `ENT-RECRUIT-F05-CANDIDATE-TITLE`
- `ENT-RECRUIT-F07-REVIEW-CONFIG-TITLE`
- `ENT-RECRUIT-F06-SERVICE-CONTRACT`

不得在参数字段标签、企业名称、候选状态或提交按钮上新增评审标记。配置标题挂点只说明产品解释来源，不改变参数 schema 或业务权限。

报告 Reader 使用 ENT-EXPORT 已声明的 `ENT-EXPORT-F02-*` 等挂点；引育结果页不复制这些 mount。两侧业务模式均完全移除评审节点，报告内容、章节、权限和动作保持不变，PDF 永不包含评审标识。

## 10. Demo 实施交接

- 页面包：引育推荐页面壳层、候选工作台、指定对象内嵌参数配置区、五阶段过程、招引 / 培育结果。
- 共享组件候选：系统任务过程、任务恢复、参数 schema 表单渲染器、候选上下文快照；报告 Reader 与 HTML / PDF 渲染直接复用 ENT-EXPORT，不创建引育私有副本。
- 状态模型：以 `view + entry` 为上下文键，分别保存 `analysis_state`、`task_id`、输入 / 参数快照、五阶段过程、结果引用、局部筛选、分页和选择集合；候选入口另含 `candidate_stage`。
- 测试关注：点击执行不改变当前 Tab且不打开 Modal；内嵌配置返回后恢复焦点；校验失败不创建任务；成功后结果仍属候选工作台；条件筛选 / 候选工作台的过程与结果隔离且切回恢复；招引 / 培育任务隔离；两类报告类型、七核心章节、来源快照、安全返回、同修订 HTML/PDF、模式隔离；报告与推荐数据导出任务互不覆盖；1920 / 1680 / 1440。
- 明确排除：Demo 代码修改、模型公式编辑、前端默认阈值 / 权重、条件筛选 Tab 跳转、自建任务中心、任务状态或 Gate 状态变更。

本规格为 `ready_for_v1`，授权 `v1_hifi_round1` Demo 实施；不代表 PDR 或下游 Gate 关闭。

## 11. 缺口与阻断项

| ID | 阻断摘要 | Owner | return_to / 关闭条件 |
| --- | --- | --- | --- |
| Q015 | 推荐指数、维度阈值与权重语义未闭合 | PM / 何老师 / data-agent / algorithm-agent | TRACE / Wireframe；完成语义会签 |
| GAP-RECRUIT-UX-01 | 产品角色到权限角色映射未闭合 | PM / architect-agent | TRACE；形成权限矩阵 |
| GAP-RECRUIT-EXPORT-01 | 推荐数据导出格式、字段范围与生产阈值未闭合 | PM / backend-agent / data-agent | Wireframe；形成独立数据导出契约 |
| GAP-RECRUIT-REPORT-ADAPTER-01 | 引育报告适配器技术接口、字段映射、指纹、授权、审计与资产投影未闭合 | architect-agent / backend-agent / compliance-owner | TRACE；形成生产适配器契约 |
| GAP-RECRUIT-DATA-01 | 数据来源、标准化和覆盖契约未闭合 | data-agent / 辜少彬 / architect-agent | TRACE；形成数据契约 |
| GAP-RECRUIT-MODEL-01 | 模型训练、版本和动态更新触发规则未闭合 | algorithm-agent / data-agent / 何老师 | TRACE；形成模型契约 |
| GAP-RECRUIT-API-01 | RESTful API 与 SDK 精确契约未闭合 | backend-agent / algorithm-agent / architect-agent | TRACE；形成接口契约 |
| GAP-RECRUIT-BATCH-01 | 复核与导出性能阈值未验证 | PM / frontend-agent / backend-agent / algorithm-agent | TRACE；完成性能验证 |
| GAP-RECRUIT-RISK-CREDIT-01 | 风险数据范围、来源、去重和状态语义未闭合 | PM / data-agent / 辜少彬 / compliance-owner | Wireframe；完成数据与合规评审 |

本次“当前 Tab 复核闭环”和“ENT-EXPORT 第三消费者产品映射”已闭合。上述未决项均 `blocks_v1: false`；报告适配器按确定性 V1 契约演示，数据导出在生产契约不可用时禁用并说明原因，不得声称正式接口、范围或语义已闭合。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: ENT-RECRUIT
  version: "1.2"
  status: ready_for_v1
  source_four_pack:
    - IA-ENT-RECRUIT.md
    - TRACE-ENT-RECRUIT.yaml
    - USM-ENT-RECRUIT.md
    - Wireframe-ENT-RECRUIT.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-RECRUIT-01
      role: 政府招商与产业管理人员
      story_refs: [US-ENT-RECRUIT-A1, US-ENT-RECRUIT-A2, US-ENT-RECRUIT-C1, US-ENT-RECRUIT-C2]
      primary_flow: [选择业务视图, 设置条件, 执行分析, 查看结果]
      abnormal_flows: [空结果保留条件, 失败按原输入重试, 无权限不泄露数据]
    - journey_id: J-RECRUIT-02
      role: 四类已登记产品角色
      story_refs: [US-ENT-RECRUIT-L1, US-ENT-RECRUIT-L2, US-ENT-RECRUIT-R3]
      primary_flow: [候选列表选择对象, 当前Tab配置参数, 当前Tab查看过程, 当前Tab查看复核结果, 返回候选列表]
      abnormal_flows: [参数契约不可用, 参数校验失败, 任务失败, 上下文失效]
    - journey_id: J-RECRUIT-03
      role: 四类已登记产品角色
      story_refs: [US-ENT-RECRUIT-L3, US-ENT-RECRUIT-R2]
      primary_flow: [加入对比篮, 发起专业研判, 返回候选工作台, 人工确认]
      abnormal_flows: [对比篮容量不足, 返回上下文失效]
    - journey_id: J-RECRUIT-04
      role: 四类已登记产品角色
      story_refs: [US-ENT-RECRUIT-R3]
      primary_flow: [提交任务, 稍后查看, 系统任务层恢复, 返回对应结果]
      abnormal_flows: [任务类型不匹配, 输入指纹不匹配, 结果版本错误]
    - journey_id: J-RECRUIT-05
      role: 四类已登记产品角色
      story_refs: [US-ENT-RECRUIT-A3, US-ENT-RECRUIT-C3]
      primary_flow: [冻结来源快照, 生成分析报告, 进入共享Reader, 下载同修订PDF或返回, 独立导出推荐数据]
      abnormal_flows: [报告来源失效, 报告失败, 报告无权限, 数据导出失败, 数据过大转后台]
  frame_specs:
    - frame_id: F-RECRUIT-A-CONFIG
      route_or_host: /enterprise/recommendation 的招引条件筛选推荐
      source_refs: [US-ENT-RECRUIT-A1]
      states: [initial, loading, error, permission]
      interactions: [设置条件, 执行招引分析]
    - frame_id: F-RECRUIT-A-RESULT
      route_or_host: /enterprise/recommendation 的招引结果宿主
      source_refs: [US-ENT-RECRUIT-A2, US-ENT-RECRUIT-A3, US-ENT-RECRUIT-L2]
      states: [success, empty, partial, error, permission, report_preparing, report_generating, report_ready, report_failed, report_source_invalid]
      interactions: [筛选分页, 查看详情, 返回候选列表, 生成或查看招引报告, 下载同修订PDF, 独立导出推荐数据]
    - frame_id: F-RECRUIT-C-CONFIG
      route_or_host: /enterprise/recommendation 的培育条件筛选推荐
      source_refs: [US-ENT-RECRUIT-C1]
      states: [initial, loading, error, permission]
      interactions: [设置条件, 执行培育分析]
    - frame_id: F-RECRUIT-C-RESULT
      route_or_host: /enterprise/recommendation 的培育结果宿主
      source_refs: [US-ENT-RECRUIT-C2, US-ENT-RECRUIT-C3, US-ENT-RECRUIT-L2]
      states: [success, empty, partial, error, permission, report_preparing, report_generating, report_ready, report_failed, report_source_invalid]
      interactions: [筛选分页, 查看行业分布, 查看详情, 返回候选列表, 生成或查看培育报告, 下载同修订PDF, 独立导出推荐数据]
    - frame_id: F-RECRUIT-CANDIDATES
      route_or_host: /enterprise/recommendation 的候选工作台
      source_refs: [US-ENT-RECRUIT-L1, US-ENT-RECRUIT-L2, US-ENT-RECRUIT-L3]
      states: [initial, loading, empty, error, permission]
      interactions: [筛选候选, 选择对象, 发起指定对象复核, 人工确认]
    - frame_id: F-RECRUIT-REVIEW-CONFIG
      route_or_host: 候选工作台当前Tab内嵌配置区
      source_refs: [US-ENT-RECRUIT-L2, DEC-ENT-RECRUIT-IN-TAB-REVIEW-20260731]
      states: [loading, ready, validation_error, contract_error, permission]
      interactions: [核对对象, 配置契约参数, 取消返回, 确认提交]
    - frame_id: F-RECRUIT-PROCESS
      route_or_host: 当前业务宿主与系统任务恢复入口
      source_refs: [US-ENT-RECRUIT-R3]
      states: [queued, running, succeeded, failed]
      interactions: [查看当前阶段, 稍后查看, 恢复任务]
    - frame_id: F-RECRUIT-SERVICE-CONTRACT
      route_or_host: 仅评审模式的非业务页面契约摘要
      source_refs: [DR-ENT-RECRUIT-A-09, DR-ENT-RECRUIT-C-09]
      states: [review_present, business_absent]
      interactions: [查看服务契约追溯]
  feedback_rules:
    - trigger: 参数契约加载失败
      response: 保持当前候选工作台Tab并禁用提交
      recovery: 重试加载或关闭返回
    - trigger: 参数校验失败
      response: 保留输入并聚焦首个错误项
      recovery: 修正后重新提交
    - trigger: 指定对象任务失败
      response: 保留参数快照和候选上下文
      recovery: 以原配置重试
    - trigger: 返回候选列表
      response: 恢复视图筛选分页和未失效选择
      recovery: 无需重新建立上下文
    - trigger: 报告来源失效
      response: 保持推荐结果可读并阻止生成残缺报告
      recovery: 重新执行分析后生成
    - trigger: 报告生成成功
      response: 提供共享Reader入口和同修订PDF下载
      recovery: Reader返回时恢复来源结果上下文
    - trigger: 推荐数据导出过大
      response: 保留导出上下文并提供缩小范围或后台生成
      recovery: 当前页或Notification反馈完成位置
  report_consumer:
    framework_module: ENT-EXPORT
    contract_version: "0.1"
    definition_mapping_status: defined_for_v1
    implementation_status: not_claimed
    formal_scope_activation: not_claimed
    report_types: [attraction_recommendation_analysis_report, cultivation_recommendation_analysis_report]
    core_sections: [report_identity, executive_summary, subject_and_scope, key_findings, evidence_and_analysis, sources_and_generation_notes, limitations]
    source_snapshot_required: true
    html_pdf_same_revision: true
    source_module_owns_business_semantics: true
    end_user_body_editing: prohibited
    end_user_section_configuration: prohibited
    business_mode_review_mounts: 0
    pdf_internal_markers: 0
    data_export_reader_reuse: prohibited
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast]
  review_mounts:
    - SYS-JOBS-F03-PROCESS-TITLE
    - ENT-RECRUIT-F01-CONFIG-TITLE
    - ENT-RECRUIT-F02-RESULT-TITLE
    - ENT-RECRUIT-F02-MANUAL-RESULT-TITLE
    - ENT-RECRUIT-F02-METRIC-DETAIL
    - ENT-RECRUIT-F02-MODEL-STATUS
    - ENT-RECRUIT-F02-LARGE-RESULT
    - ENT-RECRUIT-F02-RISK-CREDIT
    - ENT-RECRUIT-F03-CONFIG-TITLE
    - ENT-RECRUIT-F04-RESULT-TITLE
    - ENT-RECRUIT-F04-MANUAL-RESULT-TITLE
    - ENT-RECRUIT-F04-METRIC-DETAIL
    - ENT-RECRUIT-F04-MODEL-STATUS
    - ENT-RECRUIT-F04-LARGE-RESULT
    - ENT-RECRUIT-F04-RISK-CREDIT
    - ENT-RECRUIT-F05-CANDIDATE-TITLE
    - ENT-RECRUIT-F07-REVIEW-CONFIG-TITLE
    - ENT-RECRUIT-F06-SERVICE-CONTRACT
  gaps:
    - {id: Q015, summary: 推荐指数维度阈值和权重语义未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_demo_contract, owner: PM和数据算法负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-UX-01, summary: 权限映射未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: fail_closed, v1_treatment: fail_closed_permission, owner: PM和架构负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-EXPORT-01, summary: 推荐数据导出格式字段范围与生产阈值未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: feature_disabled_with_reason, owner: PM和后端数据负责人, deadline: before_pdr, return_to: Wireframe-ENT-RECRUIT.md}
    - {id: GAP-RECRUIT-REPORT-ADAPTER-01, summary: 引育报告适配器技术接口授权审计与资产投影未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_demo_contract, owner: 架构后端和合规负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-DATA-01, summary: 数据来源标准化和覆盖契约未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: demo_provenance_visible, v1_treatment: simulated_or_local_fixture, owner: 数据与架构负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-MODEL-01, summary: 模型训练版本和更新契约未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_demo_contract, owner: 算法与数据负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-API-01, summary: 接口与SDK精确契约未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: demo_provenance_visible, v1_treatment: simulated_or_local_fixture, owner: 后端算法和架构负责人, deadline: before_pdr, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-BATCH-01, summary: 批量复核与导出阈值未验证, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: deterministic_demo_contract, owner: 产品前后端和算法负责人, deadline: before_v1_review, return_to: TRACE-ENT-RECRUIT.yaml}
    - {id: GAP-RECRUIT-RISK-CREDIT-01, summary: 风险数据与合规语义未闭合, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: demo_provenance_visible, v1_treatment: simulated_or_local_fixture, owner: 产品数据和合规负责人, deadline: before_v1_review, return_to: Wireframe-ENT-RECRUIT.md}
```
