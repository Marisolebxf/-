# REPORT-CONTRACT-ENT-EXPORT｜共用报告数据契约与消费者映射

> module_key：`ENT-EXPORT`
> 契约版本：v0.1
> 对应四件套：v0.4
> 更新日期：2026-07-31
> 状态：产品定义层基线已确认；技术接口、存储、授权、有效期与审计枚举仍待 `GAP-ENT-EXPORT-CONTRACT-01` 评审
> 适用消费者：`ENT-EVAL`（首消费者）、`ENT-RISK`（第二消费者）

## 1. 契约目的与结论边界

本契约冻结产品定义层允许进入适配器设计的最小对象、字段归属、章节语义、可见性和消费者映射，防止把企业评估的模式、权重、评分、排名、雷达图或评估模板误设为系统报告框架的共用必填字段。

本契约已经确认：

- 共用对象边界、字段语义和必填关系；
- 七个固定核心章节与扩展章节机制；
- 业务模式、内部评审模式和 PDF 的可见性边界；
- ENT-EVAL 九个现有章节到共用骨架的映射；
- ENT-RISK 两类报告到共用骨架的映射；
- 来源业务模块、ENT-EXPORT 与 `SYS-ANALYSIS-JOBS` 的字段所有权。

本契约没有确认：

- HTTP API、数据库表、消息事件或 TypeScript 最终命名；
- `report_fingerprint` 的哈希算法；
- 文件有效期、下载授权、审计留存和水印的最终枚举；
- 正式 `approved_scope_change`、PDR、Gate、V1 激活或实际交付 Tier；
- ENT-RISK 已完成代码适配、同源 HTML/PDF 或视觉验证。

## 2. 不可破坏的共用约束

1. `ReportDefinition / ReportSnapshotRef / ReportContentModel / ReportRevision / ReportArtifact` 是五个共用对象。
2. 来源模块拥有业务事实、指标语义、算法、结论、来源说明、局限性、权限上下文和安全回跳路由。
3. ENT-EXPORT 拥有内容结构校验、Reader、HTML/PDF 渲染、修订与产物元数据，不推导业务结论。
4. `SYS-ANALYSIS-JOBS` 拥有队列、进度、重试、跨登录恢复和个人资产投影。
5. HTML 与 PDF 必须绑定同一 `report_revision_id`；事实、数值、章节语义和证据关系一致。
6. 共用协议不得要求任何消费者伪造不属于自己的模式、模板、权重、评分、排名、雷达图或业务算法字段。
7. 业务统计值继续使用来源模块登记的 `metric_id`；共用框架不创建统计口径。
8. 业务模式不渲染内部评审挂点或原始内部 payload；PDF 不包含评审挂点、原始内部 ID、内部权限编码或实现说明。
9. 业务所需的数据来源、版本和局限性不能因“隐藏内部字段”而被删除；应使用业务可理解的标签呈现。
10. 缺少固定核心章节、来源快照、权限上下文或安全路由时，不生成残缺报告。

## 3. 共用对象字段基线

字段状态：

- `required`：所有消费者必须提供；缺失时阻断生成或读取。
- `conditional`：满足对应业务或产物条件时必填；不满足时不得伪造。
- `optional`：来源模块可提供，不影响通用结构有效性。

可见性：

- `business`：业务模式 HTML 与 PDF 均可使用业务化标签显示。
- `business_html`：仅业务模式 HTML 交互所需，不进入 PDF。
- `review`：仅内部评审挂点或评审面板显示。
- `audit`：仅服务端、任务或审计链路使用，前端业务正文不可直接显示。

### 3.1 `ReportDefinition`

| 字段 | 状态 | 所有者 | 可见性 | 说明 |
|---|---|---|---|---|
| `definition_id` | required | ENT-EXPORT | review / audit | 稳定报告定义标识，不等同于用户模板 |
| `definition_version` | required | ENT-EXPORT | business / review / audit | 用业务化“报告模板版本”展示 |
| `source_module` | required | 来源模块 | business / review / audit | 如 `ENT-EVAL`、`ENT-RISK` |
| `report_type` | required | 来源模块 | business / review / audit | 来源模块拥有的报告类型 |
| `core_sections` | required | ENT-EXPORT | business / review | 固定为七个核心章节，消费者不得删除或改名 |
| `extension_slots` | required | ENT-EXPORT | review / audit | 定义允许装配的扩展槽位 |
| `supported_formats` | required | ENT-EXPORT | business / review | V1 仅 `HTML / PDF` |

### 3.2 `ReportSnapshotRef`

| 字段 | 状态 | 所有者 | 可见性 | 说明 |
|---|---|---|---|---|
| `source_task_id` | required | 来源模块 | business / review / audit | 当前不可变来源任务 |
| `source_snapshot_id` | required | 来源模块 / 任务系统 | review / audit | 不可变结果快照引用；业务正文不显示原始内部 ID |
| `subject_scope` | required | 来源模块 | business / review / audit | 对象类型、对象摘要和数量；对象明细受权限控制 |
| `version_refs[]` | required | 来源模块 | business / review / audit | 数据、算法、图谱、知识库或指标目录版本引用 |
| `permission_context_ref` | required | 来源模块 | review / audit | 生成和读取时复核；业务模式只显示权限结果，不显示内部编码 |
| `desensitization_policy_ref` | conditional | 来源模块 | review / audit | 存在字段脱敏时必填 |
| `source_result_route` | required | 来源模块 | business_html / review | 安全返回来源结果页 |
| `source_report_route` | required | 来源模块 | business_html / review | 安全阅读当前修订 |

`version_refs[]` 的产品层最小结构：

| 子字段 | 状态 | 可见性 | 说明 |
|---|---|---|---|
| `kind` | required | review / audit | `data / algorithm / graph / knowledge_base / metric_catalog / other` |
| `display_label` | required | business | 如“数据版本 2026-07”“供应链图谱版本 3” |
| `internal_ref` | conditional | review / audit | 内部编码存在时提供；不得直接进入业务 PDF |
| `status` | required | business / review | `available / unavailable / not_applicable`；不可用时给出原因 |

### 3.3 `ReportContentModel`

| 字段 | 状态 | 所有者 | 可见性 | 说明 |
|---|---|---|---|---|
| `title` | required | 来源模块 | business / review | 报告业务标题 |
| `executive_summary` | required | 来源模块 | business / review | 仅压缩已有结构化事实 |
| `subject_scope_summary` | required | 来源模块 | business / review | 对象、范围与当前权限可见边界 |
| `sections[]` | required | 来源模块 + ENT-EXPORT | business / review | 七个核心章节加允许的扩展章节 |
| `evidence_refs[]` | required | 来源模块 | business / review / audit | 结论到结构化证据的关系 |
| `data_source_notes[]` | required | 来源模块 | business / review | 业务可理解的数据来源说明 |
| `generation_notes[]` | required | 双方 | business / review | 生成时间、模板版本和可复现性说明 |
| `limitations[]` | required | 来源模块 + ENT-EXPORT | business / review | 缺失、低可信、权限、临时口径和使用边界 |

`sections[]` 的产品层最小结构：

| 子字段 | 状态 | 说明 |
|---|---|---|
| `section_id` | required | 当前修订内稳定且唯一 |
| `section_kind` | required | `core / extension` |
| `core_key` | conditional | 核心章节必须提供；取七个固定 key |
| `extension_key` | conditional | 扩展章节必须提供；必须在 Definition 中登记 |
| `title` | required | 业务标题；核心章节不得改义 |
| `order` | required | 由系统定义；终端用户不可调整 |
| `blocks[]` | required | 结构化文本、表格、图表、指标或证据块 |
| `availability` | required | `available / unavailable / hidden_by_rule` |
| `unavailable_reason` | conditional | 不可用时必填，不得补造空结论 |

`evidence_refs[]` 必须同时支持：

- `display_label`：业务可读的依据或来源名称，可进入 HTML/PDF；
- `metric_id`：统计值适用时引用来源模块登记的指标；
- `internal_ref`：原始证据 ID，仅 `review / audit`；
- `source_kind`：业务模式转换成“评估结果、数据质量结果、供应链图谱、知识库”等可理解标签。

### 3.4 `ReportRevision`

| 字段 | 状态 | 所有者 | 可见性 | 说明 |
|---|---|---|---|---|
| `report_id` | required | ENT-EXPORT | business / review / audit | 报告资产身份 |
| `report_revision_id` | required | ENT-EXPORT | business / review / audit | HTML/PDF 一致性边界 |
| `report_fingerprint` | required | ENT-EXPORT | review / audit | 服务端创建或复用依据 |
| `definition_ref` | required | ENT-EXPORT | review / audit | 指向 Definition 版本 |
| `snapshot_ref` | required | ENT-EXPORT | review / audit | 指向不可变来源快照 |
| `content_digest` | required | ENT-EXPORT | review / audit | 证明同修订内容未被静默替换 |
| `created_at` | required | ENT-EXPORT | business / review / audit | 报告修订生成时间 |

### 3.5 `ReportArtifact`

| 字段 | 状态 | 所有者 | 可见性 | 说明 |
|---|---|---|---|---|
| `artifact_id` | required | ENT-EXPORT / 任务系统 | review / audit | 具体格式产物身份 |
| `report_revision_id` | required | ENT-EXPORT | business / review / audit | 必须与阅读页一致 |
| `format` | required | ENT-EXPORT | business / review | V1 为 `HTML / PDF` |
| `status` | required | 任务系统 | business / review / audit | 使用 ENT-EXPORT 状态协议 |
| `file_ref` | conditional | 任务系统 | audit | PDF 完成时提供；不得作为长期公开地址 |
| `expires_at` | conditional | 任务系统 / 合规 | business / review / audit | 仅在有效期规则适用时提供 |
| `download_policy_ref` | required | 来源模块 / 合规 | review / audit | 下载前重新校验 |
| `audit_ref` | required | 任务系统 / 合规 | review / audit | 操作者、时间、结果等审计链路 |

## 4. 七个固定核心章节

| core_key | 业务标题 | 必须承载 | 允许扩展但不得替代 |
|---|---|---|---|
| `report_identity` | 封面与报告身份 | 报告、修订、来源任务、对象、生成时间、报告类型/模板版本 | 来源模块品牌或业务副标题 |
| `executive_summary` | 决策摘要 | 范围、主要结论、关键发现、风险或限制提示 | 模式摘要、共性摘要 |
| `subject_and_scope` | 对象与范围 | 对象范围、任务范围、权限可见边界 | 评估方法、关系范围、诊断维度 |
| `key_findings` | 核心发现 | 来源模块确认的主要发现 | 得分排名、风险线索、问题成因 |
| `evidence_and_analysis` | 证据与分析 | 结论依据、结构化分析、统计值的 `metric_id` 引用 | 图表、排名、路径、最佳实践 |
| `sources_and_generation_notes` | 数据来源与生成说明 | 数据来源、业务化版本说明、生成时间、模板版本和缺失说明 | 图谱/知识库/算法版本说明 |
| `limitations` | 局限性与使用边界 | 缺失、低可信、临时口径、权限和禁止外推边界 | 来源模块未闭合 Q/GAP 的业务化说明 |

## 5. ENT-EVAL 首消费者映射

来源基线：ENT-EVAL v1.12。该映射保留企业评估九个现有阅读章节，但只通过适配器提交共用对象；不把评估专属字段提升为共用必填项。

| ENT-EVAL 现有章节 | 共用落点 | 类型 | 专属字段处理 |
|---|---|---|---|
| `identity` 封面与报告身份 | `report_identity` | core | `mode` 作为业务标签，不进入共用必填字段 |
| `executive-summary` 决策摘要 | `executive_summary` | core | 得分、排名和改进方向作为来源内容 |
| `scope-method` 评估范围与方法 | `subject_and_scope` + `sources_and_generation_notes` | core content | 指标、权重、模板属于 ENT-EVAL 内容 |
| `overall-results` 综合结果 | `key_findings` | core content | `score / rank / confidence` 由 ENT-EVAL 拥有 |
| `mode-analysis` 模式分析 | `evidence_and_analysis` | extension：`evaluation_mode_analysis` | 仅装配当前评估模式 |
| `strengths-gaps` 优势、短板与差距 | `key_findings` + `evidence_and_analysis` | extension：`evaluation_strengths_gaps` | 必须引用结构化证据 |
| `recommendations` 改进方向 | `executive_summary` + `key_findings` | extension：`evaluation_recommendations` | 不生成无证据策略外推 |
| `quality-limitations` 数据质量与局限 | `limitations` | core | 缺失、可信度、权限和临时口径 |
| `appendix` 附录与证据追溯 | `sources_and_generation_notes` + `evidence_and_analysis` | extension：`evaluation_evidence_appendix` | 业务模式显示业务化来源；原始 ID 仅评审/审计 |

ENT-EVAL 专属且禁止进入共用必填字段：

- `evaluation_mode`
- `indicator_weights`
- `enterprise_score`
- `enterprise_ranking`
- `radar_chart`
- `evaluation_template_configuration`
- 单企/双企/多企评估专属版式

## 6. ENT-RISK 第二消费者映射

来源基线：ENT-RISK v1.10。供应链报告与痛难点建议报告分别注册 `ReportDefinition`，共享共用对象和 Reader，不合并业务模板。

### 6.1 供应链分析报告

| 共用核心章节 | ENT-RISK 内容 | 扩展章节 |
|---|---|---|
| `report_identity` | 报告标题、`riskTaskId`、对象、生成时间、模板/数据/图谱/算法版本 | — |
| `executive_summary` | 供应链结构摘要、关键节点和主要断链风险线索 | — |
| `subject_and_scope` | 1–2 家中心企业、关系类型、展开范围、权限范围 | `relation_structure` |
| `key_findings` | 关键节点、单点依赖、节点异常、路径脆弱风险 | `key_nodes`、`chain_break_risks` |
| `evidence_and_analysis` | 关系结构、多级路径摘要、判断依据、来源指标引用 | `multi_level_path_summary` |
| `sources_and_generation_notes` | 来源快照、数据/图谱/算法版本、缺失和生成说明 | — |
| `limitations` | Q017、数据缺失、权限边界；不生成替代供应商或备份方案 | — |

### 6.2 发展痛难点分析建议报告

| 共用核心章节 | ENT-RISK 内容 | 扩展章节 |
|---|---|---|
| `report_identity` | 报告标题、`riskTaskId`、对象、生成时间、模板/数据/知识库/算法版本 | — |
| `executive_summary` | 单企结论或集合共性诊断摘要 | — |
| `subject_and_scope` | 单企业或最多 50 家不可变对象快照、四个诊断维度、权限范围 | `four_dimension_diagnosis` |
| `key_findings` | 问题、影响范围和主要成因 | `issues_and_causes` |
| `evidence_and_analysis` | 判断依据、成因、行业最佳实践和解决方向 | `industry_best_practices`、`solution_directions`、`affected_enterprises_summary` |
| `sources_and_generation_notes` | 来源快照、数据/知识库/算法版本、缺失和生成说明 | — |
| `limitations` | Q018、低可信或数据不足；不生成企业评分/排名或第二份单企报告 | — |

## 7. 可见性与模式隔离

| 信息 | 业务 HTML | PDF | 内部评审 | 审计 |
|---|---:|---:|---:|---:|
| 报告标题、对象、生成时间、业务结论 | 是 | 是 | 是 | 是 |
| 业务化模板/数据/算法/图谱/知识库版本标签 | 是 | 是 | 是 | 是 |
| 数据来源、缺失、可信度与使用边界 | 是 | 是 | 是 | 是 |
| 业务可读证据名称和来源标签 | 是 | 是 | 是 | 是 |
| 原始证据 ID、`metric_id` 内部编码 | 否；指标说明交互按来源模块定义 | 否 | 是 | 是 |
| `source_snapshot_id`、内部版本 ref、指纹、内容摘要 | 否 | 否 | 是 | 是 |
| 内部权限级别、角色编码、审计 ref | 否 | 否 | 是 | 是 |
| 评审挂点、Popover、Mock/Pending/实现说明 | 否 | 否 | 是 | 按审计规则 |
| 安全返回与下载控件 | 是 | 否 | 是 | 否 |

业务模式隐藏的是内部编码和实现载荷，不是删除业务所需的来源、版本、证据和局限性。

## 8. 适配器提交与校验顺序

```text
来源任务与不可变快照
  → 来源模块 Adapter
  → Definition + SnapshotRef + ContentModel
  → ENT-EXPORT 结构、权限与安全路由校验
  → ReportRevision
  → HTML Reader / A4 PDF
  → ReportArtifact
  → SYS-ANALYSIS-JOBS 状态与个人资产投影
```

阻断校验：

- `definition_id / definition_version / source_module / report_type` 缺失；
- `source_task_id / source_snapshot_id / permission_context_ref` 缺失；
- 七个核心章节任一缺失或被扩展章节替代；
- 结论没有可定位证据，或统计值缺来源模块 `metric_id`；
- 内部原始 ID、权限编码或评审 payload 被写入业务 PDF；
- HTML 与 PDF 的 `report_revision_id` 不一致；
- 安全返回路由或报告路由缺失；
- 来源版本不可解析且没有明确 `unavailable` 说明。

## 9. 机器可读产品契约

```yaml
report_contract_baseline:
  module_key: ENT-EXPORT
  contract_version: "0.1"
  four_pack_version: "0.4"
  status: product_definition_baseline_confirmed
  formal_scope_activation: blocked
  technical_interface_freeze: pending
  core_objects:
    - ReportDefinition
    - ReportSnapshotRef
    - ReportContentModel
    - ReportRevision
    - ReportArtifact
  core_sections:
    - report_identity
    - executive_summary
    - subject_and_scope
    - key_findings
    - evidence_and_analysis
    - sources_and_generation_notes
    - limitations
  invariants:
    html_pdf_same_revision: true
    source_snapshot_required: true
    permission_context_required: true
    safe_routes_required: true
    business_mode_review_mounts: 0
    pdf_internal_markers: 0
    source_module_owns_business_semantics: true
    framework_creates_metrics: false
  forbidden_shared_requirements:
    - evaluation_mode
    - indicator_weights
    - enterprise_score
    - enterprise_ranking
    - radar_chart
    - end_user_report_template_configuration
  consumers:
    ENT-EVAL:
      role: reference_consumer
      source_definition_version: "1.12"
      adapter_implementation_status: existing_consumer_specific_not_shared_adapter
    ENT-RISK:
      role: anti_coupling_validation_consumer
      source_definition_version: "1.10"
      definition_validation_status: passed_definition_only
      adapter_implementation_status: not_claimed
      report_types:
        - supply_chain_analysis_report
        - pain_point_analysis_advice_report
  remaining_blockers:
    - GAP-ENT-EXPORT-SCOPE-01
    - GAP-ENT-EXPORT-CONTRACT-01
    - GAP-ENT-EXPORT-CATALOG-01
    - GAP-ENT-EXPORT-HISTORY-01
```

## 10. 后续评审与实现准入

进入适配器代码实现前必须完成：

1. 架构、后端、合规 Owner 对字段归属、接口边界、指纹输入、授权和审计枚举形成书面意见；
2. 正式 `approved_scope_change` 激活 ENT-EXPORT 产品增强；如仅做本地受限验证，必须维持 `not_claimed / blocked` 状态；
3. ENT-EVAL Adapter 证明现有业务报告无回归；
4. ENT-RISK 两类 Adapter 证明不依赖 ENT-EVAL 专属字段；
5. 共用测试覆盖同修订、七核心章节、模式隔离、异常状态和安全路由；
6. 1920 / 1680 / 1440 完成 V1 视觉与交互验证。
