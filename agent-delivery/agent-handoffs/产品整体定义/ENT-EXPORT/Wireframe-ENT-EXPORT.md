# Wireframe-ENT-EXPORT｜系统报告复用框架线框

> 版本：v0.5｜2026-07-31
> 目标：定义跨模块共用的报告入口契约、只读阅读器、同源 PDF 动作和异常状态
> `screen_tier: medium_1440_1920`，验收宽度 1920 / 1680 / 1440
> 下游 `delivery_stage: v1_hifi_round1`，当前以阶段化缺口进入 V1 首轮；不代表正式范围、PDR 或后续阶段已闭合
> 终端用户不可编辑正文或配置章节

## 1. Frame 清单

| Frame | 名称 | 页面归属 | 评审挂点 |
|---|---|---|---|
| F-EXPORT-01 | 来源模块报告入口 | 来源业务模块 | `ENT-EXPORT-F01-ENTRY-TITLE` |
| F-EXPORT-02 | 只读 HTML 报告阅读页 | ENT-EXPORT Reader，由来源路由挂载 | `ENT-EXPORT-F02-REPORT-TITLE`、`ENT-EXPORT-F02-SOURCE-TITLE`、`ENT-EXPORT-F02-LIMITATION-TITLE` |
| F-EXPORT-03 | 报告生成任务反馈 | SYS-ANALYSIS-JOBS | `ENT-EXPORT-F03-TASK-TITLE` |
| F-EXPORT-04 | 无权、过期、缺失与失败 | ENT-EXPORT Reader | `ENT-EXPORT-F04-STATE-TITLE` |
| F-EXPORT-05 | 个人资产恢复入口 | 个人资产中心 / 来源模块 | `ENT-EXPORT-F05-ASSET-TITLE` |

所有挂点仅在内部评审模式展示；业务模式完全不渲染追溯、Mock、Pending 或实现说明。

## 2. F-EXPORT-01｜来源模块报告入口

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ 业务结果标题                                             [按此配置新建分析] │
├──────────────────────────────────────────────────────────────────────────────┤
│ ……来源模块自己的业务结果……                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ 分析报告  [? ENT-EXPORT-F01-ENTRY-TITLE]                                  │
│ 查看基于当前任务结果生成的结构化分析报告。                                 │
│                                                      [生成报告 / 查看报告] │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 布局与动作

- 报告入口位于业务结果之后的独立区块，不挤入页面标题区。
- 区块标题左对齐，唯一主动作右对齐。
- `not_generated` 显示“生成报告”；`ready` 显示“查看报告”。
- `preparing / generating` 显示状态和“查看任务”，不重复提交。
- 入口由来源模块实现，共用层提供状态和动作协议。

### 2.2 评审挂点数组

```yaml
review_mounts:
  - id: ENT-EXPORT-F01-ENTRY-TITLE
    host: 分析报告标题
    content: [requirement_trace, capability_boundary, state_contract]
```

## 3. F-EXPORT-02｜只读 HTML 报告阅读页

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← 返回来源结果    报告标题 [? ENT-EXPORT-F02-REPORT-TITLE]   [下载 PDF ▾] │
│ 对象范围 · 生成时间 · 模板版本 · 数据版本 · 算法版本                       │
├────────────────┬─────────────────────────────────────────────────────────────┤
│ 报告目录       │ 报告正文                                                    │
│                │ ┌─────────────────────────────────────────────────────────┐ │
│ 01 决策摘要    │ │ 封面与报告身份                                           │ │
│ 02 对象与范围  │ └─────────────────────────────────────────────────────────┘ │
│ 03 核心发现    │ ┌─────────────────────────────────────────────────────────┐ │
│ 04 证据与分析  │ │ 决策摘要                                                 │ │
│ 05 来源说明    │ └─────────────────────────────────────────────────────────┘ │
│ 06 局限性      │ ┌─────────────────────────────────────────────────────────┐ │
│                │ │ 对象与范围                                               │ │
│                │ └─────────────────────────────────────────────────────────┘ │
│                │ ……固定核心章节 + 系统装配的扩展章节……                     │
│                │ ┌─────────────────────────────────────────────────────────┐ │
│                │ │ 数据来源与生成说明 [? ENT-EXPORT-F02-SOURCE-TITLE]      │ │
│                │ └─────────────────────────────────────────────────────────┘ │
│                │ ┌─────────────────────────────────────────────────────────┐ │
│                │ │ 局限性与使用边界 [? ENT-EXPORT-F02-LIMITATION-TITLE]    │ │
│                │ └─────────────────────────────────────────────────────────┘ │
└────────────────┴─────────────────────────────────────────────────────────────┘
```

### 3.1 信息层级

- 顶部栏：安全返回、报告标题、PDF 下载。
- 元信息行：对象范围、生成时间、模板/数据/算法版本；缺失时显示“未提供”。
- 左侧目录：固定核心章节和已装配扩展章节，支持键盘定位。
- 主内容：连续流式阅读；长表格与图表保持可读，不复制 PDF 分页空白。
- 不出现编辑、配置、排序、隐藏、保存模板或切换版式动作。

### 3.2 响应式

- 1920：内容最大宽度约 1440，目录 240，正文自适应。
- 1680：保持双栏，正文缩减外围留白。
- 1440：目录 216，正文最小有效宽度 920；图表允许区块内横向滚动。
- 本轮不定义小屏折叠目录或移动端阅读。

### 3.3 下载动作

- V1 单一格式时使用按钮“下载 PDF”；若未来存在多个已批准格式，再升级为 Dropdown。
- 点击后先做权限复核；需异步生成时进入 F-EXPORT-03。
- 生成成功后下载的 `report_revision_id` 必须与当前页面一致。

### 3.4 评审挂点数组

```yaml
review_mounts:
  - id: ENT-EXPORT-F02-REPORT-TITLE
    host: 报告标题
    content: [bid_trace, report_revision_id, template_version]
  - id: ENT-EXPORT-F02-SOURCE-TITLE
    host: 数据来源与生成说明标题
    content: [source_snapshot, data_version, algorithm_version, metric_semantics]
  - id: ENT-EXPORT-F02-LIMITATION-TITLE
    host: 局限性与使用边界标题
    content: [missing_data_policy, evidence_boundary, permission_boundary]
```

## 4. F-EXPORT-03｜报告生成任务反馈

```text
┌────────────────────────────────────────────────────────────┐
│ 报告生成任务 [? ENT-EXPORT-F03-TASK-TITLE]           [×] │
├────────────────────────────────────────────────────────────┤
│ ● 准备来源快照                                            │
│ ◐ 生成 HTML 与 PDF                                        │
│ ○ 写入个人资产                                            │
│                                                            │
│ 当前状态：正在生成报告                                    │
│ 报告生成可在后台继续，完成后可从个人资产进入。             │
│                                      [关闭] [查看任务]     │
└────────────────────────────────────────────────────────────┘
```

### 4.1 所有权

- Modal、任务阶段、队列、重试和跨登录恢复由 `SYS-ANALYSIS-JOBS` 定义与实现。
- 本框架只交付 `report_id`、`report_revision_id`、目标格式、来源路由和产物状态。
- 不在本 Frame 复制业务报告预览。

### 4.2 评审挂点数组

```yaml
review_mounts:
  - id: ENT-EXPORT-F03-TASK-TITLE
    host: 报告生成任务标题
    content: [handoff_contract, report_fingerprint, artifact_formats]
```

## 5. F-EXPORT-04｜异常和不可用状态

```text
┌──────────────────────────────────────────────────────────────────────┐
│ 报告暂不可用 [? ENT-EXPORT-F04-STATE-TITLE]                         │
│                                                                      │
│ [状态图标]  当前用户无权查看此报告                                  │
│             权限可能已变更，请返回来源页面确认可见范围。             │
│                                             [返回来源页面]           │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.1 状态变体

| 状态 | 标题 | 说明 | 主动作 |
|---|---|---|---|
| `forbidden` | 无权查看此报告 | 当前权限无法访问，不显示敏感元数据 | 返回来源页面 |
| `expired` | PDF 文件已过期 | 报告修订仍有效时可重建产物 | 重新生成 PDF |
| `source_invalid` | 报告来源已失效 | 不自动切换到最新数据 | 返回来源页面 |
| `artifact_missing` | PDF 暂不可用 | HTML 可继续阅读 | 重新生成 PDF |
| `failed` | 报告生成失败 | 展示可理解错误和追踪编号 | 按任务规则重试 |

### 5.2 评审挂点数组

```yaml
review_mounts:
  - id: ENT-EXPORT-F04-STATE-TITLE
    host: 状态标题
    content: [state_code, permission_policy, recovery_action, audit_ref]
```

## 6. F-EXPORT-05｜个人资产恢复入口

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ 企业评估报告 [? ENT-EXPORT-F05-ASSET-TITLE]                  2026-07-31     │
│ 企业 A 等 6 家 · 综合竞争力评估 · PDF 已生成                                │
│ 来源：企业评估   模板 v1.2   报告修订 R-001             [查看报告] [下载] │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.1 恢复规则

- “查看报告”使用来源模块提供的安全路由，恢复相同 `report_revision_id`。
- “下载”仍需当前权限复核，不直接复用长期公开链接。
- 资产中心由相邻模块拥有；本包只定义报告资产所需字段。

### 6.2 评审挂点数组

```yaml
review_mounts:
  - id: ENT-EXPORT-F05-ASSET-TITLE
    host: 报告资产标题
    content: [report_id, report_revision_id, source_module, return_route]
```

## 7. 报告章节组件

| 组件 | 必需 | 数据责任 | 缺失处理 |
|---|---|---|---|
| `ReportIdentity` | 是 | 来源模块 + 框架 | 阻断生成 |
| `ExecutiveSummary` | 是 | 来源模块 | 无可信结论时显示不可形成摘要的原因 |
| `SubjectScope` | 是 | 来源模块 | 阻断生成 |
| `KeyFindings` | 是 | 来源模块 | 允许明确“暂无可确认发现” |
| `EvidenceSection` | 是 | 来源模块 | 无证据不得输出对应结论 |
| `SourceAndGeneration` | 是 | 双方 | 缺失字段标“未提供”并登记问题 |
| `Limitations` | 是 | 来源模块 + 框架 | 不可隐藏 |
| `ExtensionSection` | 否 | 来源模块 | 按系统规则隐藏或显示不可用说明 |

### 7.1 字段与 metric_id 处理

| 对象 | 字段 | 类型 | 业务来源 | 必填 | metric_id |
|---|---|---|---|---|---|
| `ReportDefinition` | `template_id / template_version / core_sections / extension_slots` | 标识与配置引用 | 报告框架 | 是 | N/A（协议字段，不是统计指标） |
| `ReportSnapshotRef` | `source_task_id / source_snapshot_id / subject_scope` | 来源引用 | 来源模块 | 是 | N/A（关联字段） |
| `ReportContentModel` | `title / executive_summary / sections / evidence_refs / limitations` | 结构化内容 | 来源模块 | 是 | N/A（内容字段） |
| `ReportRevision` | `report_id / report_revision_id / report_fingerprint / created_at` | 修订与审计 | 报告框架 | 是 | N/A（审计字段） |
| `ReportArtifact` | `artifact_id / format / status / expires_at / audit_ref` | 产物元数据 | 报告框架与任务系统 | 是 | N/A（产物字段） |

本框架不产生新的统计值。业务章节出现统计值时，必须携带来源模块已经登记的 `metric_id`、单位、时间范围、空间粒度和版本；本框架不得生成替代 metric_id。

完整字段状态、所有权、业务/评审/PDF 可见性和消费者映射见 `REPORT-CONTRACT-ENT-EXPORT.md` v0.1。Reader 和适配器必须满足以下展示边界：

| 信息类型 | 业务 HTML | PDF | 内部评审 |
|---|---:|---:|---:|
| 报告身份、对象、业务结论、业务化来源和版本说明 | 显示 | 显示 | 显示 |
| 缺失、可信度、权限影响和使用边界 | 显示 | 显示 | 显示 |
| 原始证据 ID、快照 ID、内部版本 ref、指纹 | 不显示 | 不显示 | 显示 |
| 内部权限编码、审计 ref、评审 payload | 不显示 | 不显示 | 显示 |
| 返回、下载、目录定位等交互控件 | 显示 | 不显示 | 显示 |

业务模式隐藏内部编码不等于删除“数据来源与生成说明”。来源模块必须提供业务可读标签；缺失时明确“未提供”或不可用原因，不得伪造版本。

## 8. HTML / PDF 同源规则

| 内容 | HTML | PDF | 一致性要求 |
|---|---|---|---|
| 报告修订 | 连续阅读 | A4 分页 | ID 完全一致 |
| 章节与事实 | 全量 | 全量 | 语义完全一致 |
| 目录 | 可点击 | 书签/页码 | 章节集合一致 |
| 图表 | 交互只读或静态 | 静态高分辨率 | 数据完全一致 |
| 页面动作 | 返回、下载 | 不包含 | 可不同 |
| 页眉页脚 | 可无 | 报告身份、页码、生成时间 | 仅打印适配差异 |

## 9. 可访问性与视觉约束

- 使用 Arco 标准 Button、Alert、Modal、Spin、Empty、Result 等组件语义。
- 主动作唯一，破坏性或高风险动作不使用主蓝。
- 文字与状态满足对比度要求；状态不可只靠颜色。
- 目录、下载、返回、重试和关闭均支持键盘。
- 内部评审挂点不遮挡业务标题，不进入 PDF 正文。

## 10. Frame 状态覆盖矩阵

| Frame | 默认 | 加载/生成 | 空数据 | 错误 | 无权限 | 过期/失效 |
|---|---|---|---|---|---|---|
| F-EXPORT-01 | `not_generated / ready` 显示唯一主动作 | `preparing / generating` 显示状态和“查看任务” | 来源模块无可报告内容时禁用生成并说明原因 | 创建任务失败时显示可重试反馈 | 不展示生成或查看动作，沿用来源模块权限反馈 | 已有产物过期时进入重新生成 |
| F-EXPORT-02 | `ready` 连续阅读并提供目录 | 首次取修订时保持页面骨架与元信息占位 | 固定核心章节缺失视为 `source_invalid`，不渲染伪空报告 | 加载失败进入 F-EXPORT-04 | 进入 `forbidden`，不回显敏感元数据 | 产物过期不影响仍有效的 HTML 修订 |
| F-EXPORT-03 | 展示任务摘要 | 准备、生成、写入资产阶段稳定呈现 | N/A（任务 Frame） | 展示错误原因、追踪编号和规则允许的重试 | 不回显无权任务摘要 | N/A |
| F-EXPORT-04 | 按异常类型显示 Result | 重试时保持原容器 | `artifact_missing` 作为目标格式缺失态 | `failed / source_invalid` | `forbidden` | `expired` |
| F-EXPORT-05 | 展示报告资产及安全动作 | 恢复中保持资产卡尺寸 | 无报告资产时使用个人中心统一空态 | 回跳失败保留资产记录并提示 | 禁止查看或下载，不泄露文件地址 | 允许按授权规则重新生成产物 |

状态文本必须同时具备图标或可访问名称，不得只以颜色区分。

## 11. 机器可读评审追溯契约

```yaml
review_trace_contract:
  - mount_id: ENT-EXPORT-F01-ENTRY-TITLE
    frame_id: F-EXPORT-01
    host_label: 分析报告标题
    marker_type: requirement_trace
    source_relation: product_enhancement
    trace_refs: [BID-PORTAL-REPORT-MANAGEMENT-01, US-ENT-EXPORT-READ]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route: source_module_defined_result_route
    states: [not_generated, preparing, generating, ready]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F02-REPORT-TITLE
    frame_id: F-EXPORT-02
    host_label: 报告标题
    marker_type: requirement_trace
    source_relation: product_enhancement
    trace_refs: [BID-PORTAL-REPORT-MANAGEMENT-01, US-ENT-EXPORT-READ, US-ENT-EXPORT-PDF]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route: source_module_defined_report_route
    states: [ready]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F02-SOURCE-TITLE
    frame_id: F-EXPORT-02
    host_label: 数据来源与生成说明标题
    marker_type: review_copy
    source_relation: product_enhancement
    trace_refs: [US-ENT-EXPORT-EVIDENCE]
    required_payload: [source_task_id, source_snapshot_id, report_revision_id, template_version, data_version, algorithm_version]
    route: source_module_defined_report_route
    states: [ready]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F02-LIMITATION-TITLE
    frame_id: F-EXPORT-02
    host_label: 局限性与使用边界标题
    marker_type: review_copy
    source_relation: product_enhancement
    trace_refs: [US-ENT-EXPORT-EVIDENCE]
    required_payload: [evidence_boundary, missing_data_policy, permission_boundary]
    route: source_module_defined_report_route
    states: [ready]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F03-TASK-TITLE
    frame_id: F-EXPORT-03
    host_label: 报告生成任务标题
    marker_type: review_copy
    source_relation: product_enhancement
    trace_refs: [US-ENT-EXPORT-PDF]
    required_payload: [report_fingerprint, artifact_formats, task_owner, source_route]
    route: system_task_layer
    states: [preparing, generating, ready, failed]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F04-STATE-TITLE
    frame_id: F-EXPORT-04
    host_label: 报告不可用状态标题
    marker_type: review_copy
    source_relation: product_enhancement
    trace_refs: [US-ENT-EXPORT-READ, US-ENT-EXPORT-PDF, US-ENT-EXPORT-RESUME]
    required_payload: [state_code, permission_policy_ref, recovery_action, audit_ref]
    route: source_module_defined_report_route
    states: [forbidden, expired, source_invalid, artifact_missing, failed]
    review_mode: present
    business_mode: absent

  - mount_id: ENT-EXPORT-F05-ASSET-TITLE
    frame_id: F-EXPORT-05
    host_label: 报告资产标题
    marker_type: review_copy
    source_relation: product_enhancement
    trace_refs: [US-ENT-EXPORT-RESUME]
    required_payload: [report_id, report_revision_id, source_module, return_route]
    route: /personal/assets
    states: [ready, expired, forbidden]
    review_mode: present
    business_mode: absent
```

契约不声明 `metric_spec / mock_badge / pending_badge`，因为共用框架本身不产生统计值或样例数据；消费者报告中的指标挂点继续由来源模块四件套定义。

## 12. 挂点禁止位置与载荷行为

- 不得用一个页级横幅、统一问号或图标簇代替 7 个宿主挂点。
- 不得把挂点放在不可见 wrapper、页面根节点、导航菜单或来源模块无关标题上。
- 不得把 `review_copy` 的原始字段名、内部路由、版本或权限策略作为业务文案常驻展示。
- 不得把任何评审标识、Popover、Tooltip 或内部 payload 写入 PDF。
- 同一共享组件在不同 Frame 或宿主出现时必须使用各自 `mount_id`，不得复用 DOM 标识。
- 每个交互式挂点打开后必须完整呈现对应 `required_payload`；字段缺失时显示“未提供”并保留字段名，不得静默省略。
- 业务模式下 7 个 `mount_id` 均不得出现在 DOM；切换模式不得改变报告内容、权限、章节集合和动作。

## 13. 验证清单

- [ ] 1920 / 1680 / 1440 三档阅读页；
- [ ] 固定核心章节完整；
- [ ] 单企、双企、多企报告内容适配；
- [ ] HTML 与 PDF 同一修订；
- [ ] 加载、生成中、成功、失败、无权限、过期、来源失效、产物缺失；
- [ ] 长标题、长目录、长表格、图表分页；
- [ ] 键盘导航与可访问名称；
- [ ] 业务模式无内部评审标记；
- [ ] 企业评估首消费者；
- [x] 风险洞察第二消费者产品定义映射（`ENT-RISK-第二消费者一致性验证.md`；不代表代码或视觉验证）；
- [x] 共用字段、章节、可见性及 ENT-EVAL / ENT-RISK 映射已形成 `REPORT-CONTRACT-ENT-EXPORT.md` v0.1；
- [ ] 无正文编辑和章节配置入口。
