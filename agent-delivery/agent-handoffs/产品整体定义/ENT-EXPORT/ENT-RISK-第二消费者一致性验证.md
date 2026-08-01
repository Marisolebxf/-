# ENT-RISK 第二消费者一致性验证

> 验证对象：`ENT-EXPORT` 系统报告复用框架 × `ENT-RISK` 风险洞察
> 验证日期：2026-07-31
> 验证状态：`passed_definition_only`
> 结论边界：关闭 `GAP-ENT-EXPORT-CONSUMER-02` 的产品定义一致性验证；不声明代码适配、Demo 验证、V1 会签、PDR 或 Gate 完成

## 1. 权威输入

### 1.1 原始需求

- `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md`
  - §1.1.1.2.4.2.3.8 企业供应链关系分析；
  - §1.1.1.2.4.2.3.8.1 供应链图谱构建与多级下钻；
  - §1.1.1.2.4.2.3.8.2 关键节点与断链风险识别；
  - §1.1.1.2.4.2.3.9 企业发展痛难点分析；
  - §1.1.1.2.4.2.3.9.1 智能痛难点诊断模型；
  - §1.1.1.2.4.2.3.9.2 分析建议报告输出。
- `agent-delivery/bid-reference/科技专题服务算法库.md`
  - §1.1.1.1.1.1.1.5.3 企业发展痛难点识别模型；
  - §1.1.1.1.1.1.1.5.4 企业供应链关系分析模型。

### 1.2 当前派生定义

- `E-28_E-29-风险洞察/IA-ENT-RISK.md` v1.10；
- `E-28_E-29-风险洞察/TRACE-ENT-RISK.yaml` v1.10；
- `E-28_E-29-风险洞察/USM-ENT-RISK.md` v1.10；
- `E-28_E-29-风险洞察/Wireframe-ENT-RISK.md` v1.10；
- `ENT-EXPORT/IA-ENT-EXPORT.md` v0.4；
- `ENT-EXPORT/TRACE-ENT-EXPORT.yaml` v0.4；
- `ENT-EXPORT/USM-ENT-EXPORT.md` v0.4；
- `ENT-EXPORT/Wireframe-ENT-EXPORT.md` v0.4；
- `ENT-EXPORT/REPORT-CONTRACT-ENT-EXPORT.md` v0.1。

Demo、截图、交付覆盖和当前本地页面不作为本验证的产品权威。

## 2. 验证问题

本验证只回答以下问题：

1. ENT-RISK 的两类报告能否完整落入 ENT-EXPORT 的固定核心章节与扩展章节机制；
2. ENT-RISK 能否提供 ENT-EXPORT 要求的来源快照、权限上下文、业务内容和安全回跳路由；
3. 共用协议是否强制依赖 ENT-EVAL 专属的评估模式、指标权重、评分、排名、雷达图或评估模板字段；
4. 未闭合的 Q017 / Q018 应落在来源模块语义还是共用报告协议；
5. Frame、任务、资产和异常状态能否按既有跨模块边界交接。

不验证代码组件、接口可用性、HTML/PDF 实际同源性、视觉还原或浏览器交互。

## 3. ENT-RISK 报告资产清单

| 报告类型 | 原始需求关系 | 当前来源 Frame | 当前最小正文 |
|---|---|---|---|
| 供应链分析报告 | E-28；供应链模型支持结果输出与报告导出 | `F-RISK-02` 结果 + `F-RISK-06` 报告任务 | 对象与范围、关系结构、多级路径摘要、关键节点、断链风险、判断依据、数据来源/缺失/版本说明；适用风险项提示“建议提前制定备份方案” |
| 发展痛难点分析建议报告 | E-29；Bid 明确“分析建议报告输出” | `F-RISK-03` 结果 + `F-RISK-06` 报告任务 | 对象、四维诊断结论、问题、成因、行业最佳实践、解决方向、判断依据、数据来源/缺失/版本说明 |

两类报告都绑定当前不可变 `riskTaskId` 结果快照，通过不同报告定义保持业务边界，不合并为企业评估报告。

## 4. 通用对象适配

| ENT-EXPORT 对象 | ENT-RISK 已有输入 | 适配结论 |
|---|---|---|
| `ReportDefinition` | 两类明确报告类型、固定业务章节差异、报告模板版本参与指纹 | `pass`；供应链与痛难点分别注册定义；产品字段已由 v0.1 契约固定，最终技术 ID 和接口仍由 `GAP-ENT-EXPORT-CONTRACT-01` 闭合 |
| `ReportSnapshotRef` | `riskTaskId`、不可变对象快照、分析类型、数据/图谱或知识库/算法版本、权限范围 | `pass`；来源模块提供，不要求框架理解风险算法 |
| `ReportContentModel` | 两类报告的标题、对象范围、结论、结构化章节、判断依据、来源/缺失和局限性 | `pass`；业务内容由 ENT-RISK 生成，框架只校验结构 |
| `ReportRevision` | 当前任务报告、服务端报告指纹、模板版本和不可变任务快照 | `pass_with_contract_gap`；结构满足，最终指纹算法和字段归属仍由报告契约评审关闭 |
| `ReportArtifact` | 创建、生成中、完成、失败、权限、水印、有效期、下载与个人资产回查 | `pass_with_contract_gap`；状态语义满足，最终有效期/授权/审计枚举仍未冻结 |

## 5. 固定核心章节映射

### 5.1 供应链分析报告

| ENT-EXPORT 固定核心章节 | ENT-RISK 内容落点 | 结果 |
|---|---|---|
| 报告身份 | 供应链分析报告标题、`riskTaskId`、对象、生成时间、模板/数据/图谱/算法版本 | covered |
| 决策摘要 | 供应链结构摘要、关键节点与主要断链风险线索 | covered |
| 对象与范围 | 1–2 家中心企业、关系范围、当前任务与权限范围 | covered |
| 核心发现 | 关键节点、单点依赖、节点异常、路径脆弱风险 | covered |
| 证据与分析 | 关系结构、多级路径摘要、判断依据、来源模块已有 `metric_id` 引用 | covered |
| 数据来源与生成说明 | 来源快照、数据/图谱/算法版本、缺失说明、生成信息 | covered |
| 局限性与使用边界 | Q017 未闭合语义、数据缺失、权限边界；不生成替代供应商或备份方案 | covered |

来源模块扩展章节可使用：关系结构、多级路径、关键节点、断链风险。它们不覆盖或删除固定核心章节。

### 5.2 发展痛难点分析建议报告

| ENT-EXPORT 固定核心章节 | ENT-RISK 内容落点 | 结果 |
|---|---|---|
| 报告身份 | 痛难点分析建议报告标题、`riskTaskId`、对象、生成时间、模板/数据/知识库/算法版本 | covered |
| 决策摘要 | 单企诊断结论或集合共性诊断摘要 | covered |
| 对象与范围 | 单企业或最多 50 家的不可变对象快照、四个页面诊断维度、权限范围 | covered |
| 核心发现 | 问题或共性问题、影响范围、主要成因 | covered |
| 证据与分析 | 判断依据、成因、行业最佳实践、来源模块已有 `metric_id` 引用 | covered |
| 数据来源与生成说明 | 来源快照、数据/知识库/算法版本、缺失说明、生成信息 | covered |
| 局限性与使用边界 | Q018 未闭合语义、低可信或数据不足说明；不转成企业评分/排名，不逐家生成第二份完整报告 | covered |

来源模块扩展章节可使用：四维诊断、问题与成因、行业最佳实践、解决方向、集合共性问题和受影响企业摘要。它们不改变固定核心章节语义。

## 6. ENT-EVAL 专属耦合检查

| 候选专属内容 | ENT-EXPORT 是否强制 | ENT-RISK 是否需要 | 结论 |
|---|---|---|---|
| 技术力/商业力/综合竞争力评估模式 | 否 | 否；ENT-RISK 使用供应链/痛难点分析类型 | 无耦合 |
| 指标选择与权重配置 | 否 | 否；风险指标和诊断维度由来源任务决定 | 无耦合 |
| 企业综合得分与排名 | 否 | 明确禁止 | 无耦合 |
| 雷达图或评估对比矩阵 | 否 | 否 | 无耦合 |
| 评估系统模板/个人模板 | 否；只要求来源模块提供 `ReportDefinition` | 否；ENT-RISK 明确没有用户模板能力 | 无耦合 |
| 评估结论生成规则 | 否；业务结论归来源模块 | 否 | 无耦合 |
| 单企/双企/多企固定评估版式 | 否；内容协议支持来源范围 | 供应链 1–2 家、痛难点 1–50 家均可由 `subject_scope` 和扩展章节表达 | 无耦合 |
| 共用对象、快照、修订、产物、权限和审计字段 | 是 | 是 | 通用契约 |

结论：当前 ENT-EXPORT 共用对象没有 ENT-EVAL 专属必填字段；ENT-RISK 不需要伪造评估模式、权重、评分、排名或雷达图即可形成完整报告。

### 6.1 v0.1 产品数据契约复核

`REPORT-CONTRACT-ENT-EXPORT.md` v0.1 已把此前的结构性判断落实为字段、所有权和可见性基线。复核结果：

- `ReportDefinition` 只要求来源模块、报告类型、核心章节、扩展槽位和格式，不要求评估模板配置；
- `ReportSnapshotRef` 使用通用任务、快照、对象、版本、权限和安全路由，不要求评估模式或权重；
- `ReportContentModel` 使用通用摘要、章节、证据、来源和局限，ENT-RISK 可提交自身业务内容；
- 原始内部 ID、权限编码和评审 payload 不进入业务 PDF，但业务化数据/图谱/知识库/算法版本说明仍保留；
- ENT-RISK 两类报告的七核心章节和扩展章节均已逐项映射；
- 技术接口和枚举仍未冻结，因此 `implementation_adapter_status` 维持 `not_claimed`。

## 7. Frame 与跨模块交接

| ENT-RISK | ENT-EXPORT | 交接 |
|---|---|---|
| F-RISK-02 / F-RISK-03 独立报告区块 | F-EXPORT-01 来源模块报告入口 | 来源结果页承载状态与唯一主动作 |
| 风险报告安全阅读路由 | F-EXPORT-02 Reader | 来源适配器提供 `report_revision_id`、安全返回路由和权限上下文 |
| F-RISK-06 报告任务 | F-EXPORT-03 + `SYS-ANALYSIS-JOBS` | 报告框架交付修订/产物元数据；任务系统负责队列、进度和重试 |
| 风险报告无权、过期、缺失或失败 | F-EXPORT-04 | Reader 使用共用异常语义，不泄露敏感元数据 |
| `/personal/assets` 风险报告资产 | F-EXPORT-05 | 通过同一修订和安全回跳路由恢复，不复制第二套状态 |

ENT-RISK 的三类直接产品角色和权限仍归来源模块；ENT-EXPORT 不新增或授权角色，只消费来源模块提供的 `permission_context_ref` 并在查看/下载时复核。

## 8. 数据、指标与未闭合语义

- ENT-EXPORT 不创建风险统计指标，也不重定义 `M_ENT_*`。
- 供应链报告沿用 ENT-RISK 已登记的供应商数量、核心供应商数量、节点中心性、供应链风险和关系强度等语义引用。
- 痛难点报告沿用问题数量与严重度等已有语义引用；`M_ENT_PAINPOINT_GAP` 当前不可见，不得因报告框架而启用。
- Q017 与 Q018 继续阻塞 ENT-RISK 正式语义和 PDR；在报告中只能表现为明确的局限性、数据缺失或待确认说明，不能由框架猜测阈值。
- 上述语义缺口属于来源模块内容质量，不构成 ENT-EVAL 专属字段耦合，因此不阻塞本次结构一致性验证。

## 9. 验证结论与非声明

验证结果：`passed_definition_only`。

本次已证明：

- ENT-RISK 两类报告完整覆盖 ENT-EXPORT 七个固定核心章节；
- 两类业务差异可由来源模块内容和扩展章节承载；
- 共用协议不强制 ENT-EVAL 专属字段；
- Frame、任务、异常和个人资产交接边界一致；
- 风险指标与未闭合口径继续由 ENT-RISK 拥有。

本次未证明：

- ENT-RISK 代码已经接入共用 Reader 或渲染器；
- HTML 与 PDF 实际绑定同一修订；
- 下载权限、有效期、水印和审计接口已经闭合；
- 1920 / 1680 / 1440 视觉 QA 或 V1 首轮会签完成；
- ENT-EXPORT 已获得正式范围批准、PDR-ready、Gate 通过或实际交付 Tier。

## 10. 机器可读验证记录

```yaml
second_consumer_validation:
  validation_id: ENT-EXPORT-ENT-RISK-DEFINITION-COMPAT-20260731
  framework_module: ENT-EXPORT
  consumer_module: ENT-RISK
  consumer_definition_version: "1.10"
  framework_source_version: "0.4"
  product_contract_version: "0.1"
  product_contract_evidence: agent-delivery/agent-handoffs/产品整体定义/ENT-EXPORT/REPORT-CONTRACT-ENT-EXPORT.md
  validation_status: passed_definition_only
  closes_gap: GAP-ENT-EXPORT-CONSUMER-02
  implementation_adapter_status: not_claimed
  demo_validation_status: not_claimed
  pdr_or_gate_status_change: prohibited
  report_types:
    - source_leaf: E-28
      source_story: US-ENT-RISK-REPORT
      source_frames: [F-RISK-02, F-RISK-06]
      fixed_core_sections_covered: 7
      source_extension_sections: [relation_structure, multi_level_path_summary, key_nodes, chain_break_risks]
    - source_leaf: E-29
      source_story: US-ENT-RISK-REPORT
      source_frames: [F-RISK-03, F-RISK-06]
      fixed_core_sections_covered: 7
      source_extension_sections: [four_dimension_diagnosis, issues_and_causes, industry_best_practices, solution_directions]
  shared_objects:
    - ReportDefinition
    - ReportSnapshotRef
    - ReportContentModel
    - ReportRevision
    - ReportArtifact
  forbidden_consumer_assumptions:
    - evaluation_mode_required
    - indicator_weights_required
    - enterprise_score_required
    - enterprise_ranking_required
    - radar_chart_required
    - end_user_report_template_configuration
  retained_consumer_gaps: [Q017, Q018]
  remaining_framework_blockers:
    - GAP-ENT-EXPORT-SCOPE-01
    - GAP-ENT-EXPORT-CONTRACT-01
    - GAP-ENT-EXPORT-CATALOG-01
    - GAP-ENT-EXPORT-HISTORY-01
```
