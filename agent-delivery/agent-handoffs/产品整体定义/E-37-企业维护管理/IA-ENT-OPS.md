# IA-ENT-OPS.md

> **模块**：企业发展内容管理 / ENT-OPS / E-37
> **阶段**：门 1 PDR 输入（核心产品包可评审，不代表门 1 已闭合）
> **体验 Owner**：human:高颖
> **交付轨道 / 屏幕**：Track-MS / 中屏（MEDIUM）
> **原始需求唯一来源**：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.5.6.3～§1.1.1.2.4.5.6.3.3`
> **根路由**：`/enterprise/content-management`

## 1. 模块边界

### 1.1 解决的问题

ENT-OPS 为企业发展门户内容提供统一的中屏内容工作台，使内容编辑、内容审核、发布管理员能够围绕企业画像、成长轨迹、重点企业图谱、能力榜单和代表企业介绍完成内容起草、复核、发布、下线、回滚与审计。

模块保留 E-37 为 **1 个 Bid 叶子**：

```yaml
module_id: ENT-OPS
acceptance_leaf: E-37
leaves_required: 1
leaves_mapped: 1
scope_enhancement: false
silent_leaf_deletion: false
delivery_track: Track-MS
screen_tier: MEDIUM
```

六类内容维护能力是同一叶子内部的信息归位和导航拆分，不构成新增、删除、合并或拆分 Bid 叶子。

### 1.2 承接的 Bid 直接能力

| 能力编号 | Bid 直接能力 | 精确锚点 | IA 落点 |
| --- | --- | --- | --- |
| IA-ENT-OPS-CAP-01 | 企业基础档案维护 | §1.1.1.2.4.5.6.3.1（1） | 内容类型 / 企业基础档案 |
| IA-ENT-OPS-CAP-02 | 企业成长轨迹内容维护 | §1.1.1.2.4.5.6.3.1（2） | 内容类型 / 成长轨迹事件 |
| IA-ENT-OPS-CAP-03 | 重点企业全景图内容维护 | §1.1.1.2.4.5.6.3.2（1） | 内容类型 / 重点企业全景 |
| IA-ENT-OPS-CAP-04 | 企业技术力与商业力榜单维护 | §1.1.1.2.4.5.6.3.2（2） | 内容类型 / 能力榜单 |
| IA-ENT-OPS-CAP-05 | 明星企业介绍内容维护 | §1.1.1.2.4.5.6.3.3（1） | 内容类型 / 明星企业介绍 |
| IA-ENT-OPS-CAP-06 | 深圳企业介绍内容维护 | §1.1.1.2.4.5.6.3.3（2） | 内容类型 / 深圳企业介绍 |

六项均有可达入口和内容治理链路，无静默删除；后续 TRACE 必须将六项归入同一 E-37 `direct_requirement` 叶子，不得把六项误计成六个验收叶子。

### 1.3 数据写入边界

- 企业工商、统一社会信用代码、成立时间、资质、专利、财务等企业主数据由外部主数据域提供，ENT-OPS 只读引用。
- CMS 仅写门户补充内容，包括叙事文本、展示标签、媒体、人工排序、事件说明、关系描述、评估依据与专家评述。
- 当只读主数据存在错误时，内容编辑可发起纠错请求；纠错不在 ENT-OPS 内直接覆盖数据真源。
- 门户只消费 `published` 版本，不读取草稿、审核意见、内部原因或权限规则。
- 能力榜单中的 Top30 是人工策展顺序；ENT-OPS 不计算技术力、商业力或竞争力算法分数，不自动生成排名。

以上主数据分治与人工策展口径属于 2026-07-22 经 human:高颖 批准的 `product_interpretation`，不是 Bid 原文。

### 1.4 明确不承接

- 企业工商、资质、专利、财务等主数据写入或主数据管理；
- 技术力、商业力、竞争力算法评分、自动排名或自动发布榜单；
- 企业搜索、分析、推荐、对比、导出等应用侧能力；
- 用户、角色、权限、数据源或知识图谱的系统级管理；
- LARGE 大屏或 SMALL 小屏维护入口；
- 物理删除已发布内容、版本历史或审计记录。

这些排除项用于明确模块责任，不删除 E-37 的任何直接能力，也不产生 `scope enhancement`。

## 2. 原始需求与批准解释分层

| 层级 | 内容 | 对 IA 的作用 | 不允许的作用 |
| --- | --- | --- | --- |
| `direct_requirement` | Bid §1.1.1.2.4.5.6.3～3.3 的一个叶子、三组内容与六类直接能力 | 决定能力必须存在并提供原始业务语义 | 不从实施、验收或设计文件补写 Bid 原文 |
| `product_interpretation` | 2026-07-22 human:高颖 批准的三角色分工、流程优先工作台、主数据分治、人工榜单、版本与风险治理 | 让六类能力可进入统一 CMS 流程并形成可用 IA | 不改写历史 Bid，不增加新的验收叶子 |
| 约束 / 索引 | 范围、验收、评审、数据治理、架构与权限政策 | 校验叶子、轨道、屏幕与边界 | 不创造业务页面、角色、字段或能力 |
| 衍生定义 | 当前 ENT-OPS 四件套 | 保持路由、故事、状态、Frame 与排除项一致 | 不充当原始需求来源 |

当前 IA 没有 `product_enhancement`。若后续出现超出六类内容维护与治理所需的业务能力，必须先登记并批准范围变更，不得借 IA 重组静默纳入。

## 3. 用户入口与产品角色

> 下列三角色及职责分离均为 **2026-07-22 human:高颖 批准的 `product_interpretation`**，不得表述为 Bid 原文。权限 persona 仅在后续实现中映射，不替代这里的产品角色。

| 产品角色 | 中屏入口 | 核心目标 | 可执行动作 | 禁止动作 |
| --- | --- | --- | --- | --- |
| 内容编辑 | 内容工作台 / 待我处理、全部内容、六类内容入口 | 创建和完善门户补充内容并提交审核 | 新建、编辑、保存草稿、预览、提交审核、发起主数据纠错 | 审核自己的提交、发布、覆盖企业主数据 |
| 内容审核 | 审核中心 | 核验内容、版本差异与来源说明 | 查看差异、填写意见、审核通过、退回 | 修改正文、直接发布、审核自己的提交 |
| 发布管理员 | 发布中心、版本与审计 | 控制上线时机、影响与可追溯性 | 立即/定时发布、退回、下线、回滚、查看审计 | 修改正文、绕过审核发布、删除历史 |

入口规则：

1. 根入口固定为 `/enterprise/content-management`，进入后按角色默认落到对应 `view`。
2. 内容编辑默认 `view=mine`；审核角色默认进入审核中心；发布管理员默认进入发布中心。
3. 无权限时保留节点说明并呈现可解释的无权限状态，不以“仅隐藏按钮”代替权限反馈。
4. 本模块仅提供 MEDIUM 中屏入口；LARGE 与 SMALL 均不展示 ENT-OPS 菜单、快捷入口或深链入口。

## 4. 信息架构

```text
企业发展内容管理（ENT-OPS / E-37）
├─ 内容工作台
│  ├─ 待我处理
│  └─ 全部内容
├─ 内容类型
│  ├─ 企业基础档案
│  ├─ 成长轨迹事件
│  ├─ 重点企业全景
│  ├─ 能力榜单
│  ├─ 明星企业介绍
│  └─ 深圳企业介绍
└─ 内容治理
   ├─ 审核中心
   ├─ 发布中心
   └─ 版本与审计
```

架构原则：

- 流程优先：工作台、审核、发布、版本分别回答“我现在处理什么”“是否可通过”“是否可上线”“发生过什么”。
- 类型稳定：六类 Bid 直接能力同时作为稳定导航和 `type` 筛选维度。
- 一对象一标识：同一内容对象在编辑、审核、发布、版本详情中复用 `content_id`。
- 线上与草稿分离：已发布内容再次编辑时生成新草稿，不覆盖线上版本。

## 5. 页面 / 节点职责

| 节点 | 页面职责 | 主要路由 / 状态 | 来源关系与落点 |
| --- | --- | --- | --- |
| 内容工作台 | 汇总角色待办、状态计数与统一内容列表；承载搜索、新建、类型/状态筛选 | 根路由；`view=mine\|all` | 六类能力的统一流程入口；工作台组织方式为 `product_interpretation` |
| 待我处理 | 只显示当前角色可继续处理的草稿、退回、待审或待发布项 | `view=mine&type&status&page` | 流程入口，不新增 Bid 能力 |
| 全部内容 | 查看权限范围内全部六类内容及其当前流程状态 | `view=all&type&status&page` | 六类直接能力总览 |
| 企业基础档案 | 维护门户展示名称、简介、展示标签和媒体；并列展示只读企业主数据 | `type=enterprise_profile` | IA-ENT-OPS-CAP-01；主数据只读为批准解释 |
| 成长轨迹事件 | 录入事件日期、标题、摘要、类型、媒体和来源说明，形成结构化时间节点 | `type=growth_event` | IA-ENT-OPS-CAP-02 |
| 重点企业全景 | 维护重点标识、专属档案及合作、供应链、竞争关系的描述性内容 | `type=key_enterprise_panorama` | IA-ENT-OPS-CAP-03；不计算图谱关系或风险 |
| 能力榜单 | 维护技术力/商业力榜单期次、评估维度、Top30 顺序、评估依据与专家评述 | `type=capability_ranking` | IA-ENT-OPS-CAP-04；人工顺序，不计算分数 |
| 明星企业介绍 | 维护详细介绍、核心成果、代表产品、荣誉资质与媒体 | `type=star_enterprise_intro` | IA-ENT-OPS-CAP-05；荣誉资质正文不反写主数据 |
| 深圳企业介绍 | 维护深圳企业详细介绍、区域定位、优势及竞争力分析意见 | `type=shenzhen_enterprise_intro` | IA-ENT-OPS-CAP-06；不生成区域统计或竞争力分数 |
| 内容编辑器 | 在同一 `content_id` 下展示企业主数据只读区、分型 CMS 表单、门户预览与完整性检查 | `/content/:content_id/edit` | 六类直接能力的写入落点；三栏结构由 Wireframe 细化 |
| 审核中心 | 汇总待审核内容；审核详情展示版本差异、来源说明和审核意见 | `/review`、`/content/:content_id/review` | 审核职责为批准解释 |
| 发布中心 | 汇总待发布内容；发布详情展示范围、生效时间、影响摘要、原因与二次确认 | `/publish`、`/content/:content_id/publish` | 发布职责和高风险控制为批准解释 |
| 版本与审计 | 展示版本时间线、操作人、时间、原因和差异，支持受控下线与回滚 | `/versions`、`/content/:content_id/versions` | 版本治理为批准解释；历史不可物理删除 |

## 6. 路由与状态保留

### 6.1 路由契约

| 场景 | 路由 |
| --- | --- |
| 根入口 / 内容工作台 | `/enterprise/content-management` |
| 待我处理 / 全部内容 / 类型列表 | `/enterprise/content-management?view={mine|all}&type={content_type}&status={workflow_status}&page={n}` |
| 内容编辑 | `/enterprise/content-management/content/:content_id/edit?view&type&status&page` |
| 审核详情 | `/enterprise/content-management/content/:content_id/review?view&type&status&page` |
| 发布详情 | `/enterprise/content-management/content/:content_id/publish?view&type&status&page` |
| 版本详情 | `/enterprise/content-management/content/:content_id/versions?view&type&status&page` |

`view`、`type`、`status`、`page` 是列表上下文的规范查询参数。子路由必须透传这些参数；用户完成、取消或使用返回操作后，恢复原 `view/type/status/page`，不得回到无筛选的第一页。浏览器前进/后退也遵循同一规则。

新建内容在持久化前可使用 `/content/new/edit`；首次保存成功并取得 `content_id` 后必须替换为规范的 `content/:content_id/edit` 子路由。四类详情不使用标题、企业名称或列表序号充当对象标识。

### 6.2 工作流状态

```text
草稿 --提交--> 待审核 --通过--> 待发布 --发布--> 已发布
  ^               |退回          |退回
  └---------------┴--------------┘
```

- 审核退回或发布退回必须填写原因，内容回到草稿。
- 已发布版本再次编辑时创建新草稿；线上 `published` 版本继续服务门户。
- 发布可立即生效或设置生效时间。
- 发布、下线、回滚及批量关系变更必须填写原因、二次确认并写入审计链。
- 回滚以历史发布版本生成新的已发布版本，不倒写、不覆盖、不删除历史。
- 并发冲突保留当前输入，进入差异比较与重新保存流程。
- 保存或发布失败不得提前改变前端流程状态，也不得清空用户输入。

### 6.3 页面状态

各节点按适用性覆盖默认、加载、空数据、错误、无权限、只读锁定、保存中、保存成功、保存失败、审核退回、发布失败、草稿与线上版本并存、并发冲突。空状态不得使用 Mock 内容伪装真实业务数据。

## 7. 跨模块边界

| 来源或去向 | 可携带内容 | ENT-OPS 可执行 | 不可携带 / 不可承担 |
| --- | --- | --- | --- |
| 企业主数据域 | 稳定企业引用、名称、工商、资质等事实字段 | 只读展示、引用、发起纠错 | 覆盖主数据、改变主数据真源、虚构物理主键 |
| 门户企业发展展示 | `content_id`、内容类型、已发布版本、展示载荷、生效时间 | 发布、下线、回滚门户补充内容 | 向门户暴露草稿、审核意见、操作原因或内部权限 |
| 企业分析 / 对比能力 | 可引用同一企业对象和已发布说明 | 维护人工叙事与评述 | 执行分析、推荐、对比、评分、自动排名或导出 |
| 企业搜索 | 已发布内容可被下游依法索引 | 提供已发布内容 | 承担搜索结果页、检索策略或搜索权限管理 |
| 身份与权限平台 | 角色映射与授权结果 | 消费授权结果并呈现无权限状态 | 创建用户、管理角色、配置系统级权限 |
| 数据 / 算法平台 | 若后续有只读计算事实，可分源展示 | 保持计算事实与 CMS 内容分开标识 | 计算或修改技术力、商业力、竞争力分数 |
| LARGE / SMALL 展示轨道 | 无 ENT-OPS 维护入口 | 无 | 将中屏工作台缩放或复制到大屏、小屏 |

跨模块跳转只能携带稳定对象引用、来源摘要和已授权的返回上下文；不得借跨模块跳转把排除能力反向嵌入 ENT-OPS。

## 8. 与 Bid 差异说明

| Bid 原始功能 / 文字 | IA 归位或差异 | 分类 | 追溯动作 |
| --- | --- | --- | --- |
| 企业发展内容管理包含三组、六类维护能力 | 统一归入一个流程优先工作台，六类作为稳定导航和筛选维度 | `product_interpretation`（组织方式） | 六类均映射 E-37，保持 `leaves_required = leaves_mapped = 1` |
| 可手动维护企业名称、成立时间、行业、规模等基础属性 | 企业主数据字段只读；CMS 仅维护门户展示补充内容，错误通过纠错流程处理 | `product_interpretation`（2026-07-22 human:高颖 批准的主数据分治） | TRACE 须保留 Bid 原句与差异说明，不得把批准解释改写为 Bid 原文 |
| 可录入关键发展历程事件 | 归位为“成长轨迹事件”内容类型，并进入草稿—审核—发布治理 | `direct_requirement` + 流程 `product_interpretation` | 落点 IA-ENT-OPS-CAP-02 |
| 基于专家建议筛选重点企业并维护关系描述 | 归位为“重点企业全景”；只维护描述性内容，不计算关系或风险 | `direct_requirement` + 边界解释 | 落点 IA-ENT-OPS-CAP-03 |
| 定义技术力、商业力评估维度并手动维护 Top30 | 归位为“能力榜单”；明确人工排序，不产生算法分数或自动排名 | `direct_requirement`；人工策展边界为 `product_interpretation` | 落点 IA-ENT-OPS-CAP-04；无统计 `metric_id` |
| 维护明星企业与深圳企业介绍 | 分别保留独立内容类型；竞争力仅记录专家分析意见 | `direct_requirement` | 落点 IA-ENT-OPS-CAP-05 / 06 |
| Bid 未规定编辑、审核、发布三角色与版本治理 | 增加职责分离、发布风险控制和版本审计，作为 CMS 可用性解释 | `product_interpretation`（2026-07-22 human:高颖 批准） | TRACE / USM / Wireframe 必须保持角色、动作与禁止项一致 |

本 IA 不包含 `product_enhancement`，不以 ±10% 规则作为范围变更授权，也未删除、合并或拆分 E-37 叶子。

## 9. 来源清单

### 9.1 original_requirement_sources

仅列 Bid 精确章节：

```yaml
original_requirement_sources:
  - file: agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
    sections:
      - "1.1.1.2.4.5.6.3 企业发展内容管理"
      - "1.1.1.2.4.5.6.3.1 企业基础与成长内容维护"
      - "1.1.1.2.4.5.6.3.2 重点企业与竞争力榜单维护"
      - "1.1.1.2.4.5.6.3.3 明星企业与深圳企业介绍维护"
```

### 9.2 approved_decision_sources

批准决定单列，不混入原始需求或衍生定义：

```yaml
approved_decision_sources:
  - file: docs/superpowers/specs/2026-07-22-ent-ops-product-package-design.md
    approved_by: human:高颖
    approved_at: 2026-07-22
    classification: product_interpretation
    effect: 三角色、流程优先 IA、主数据分治、人工榜单、版本与高风险操作治理
```

### 9.3 derived_definition_sources

仅列当前四件套；除本文件外其余为同包待生成文件：

```yaml
derived_definition_sources:
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md
    status: current
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml
    status: planned
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md
    status: planned
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md
    status: planned
```

### 9.4 constraint_and_review_sources

以下文件只约束范围、评审、验收或治理，不是业务需求来源，也不进入前述两类 inventory：

- `agent-delivery/scope-baseline.yaml`
- `agent-delivery/acceptance-compliance-policy.md`
- `agent-delivery/产品定义评审规程.md`
- `agent-delivery/data-lineage-policy.md`
- `agent-delivery/acceptance-catalog/catalog-topic-enterprise.yaml`

## 10. IA 自检

- [x] E-37 保持 1 个 Bid 叶子，`leaves_required = leaves_mapped = 1`。
- [x] 六类 Bid 直接能力均有独立、可达 IA 落点，无静默删除。
- [x] 信息树完整包含内容工作台、待我处理、全部内容、六类内容、审核中心、发布中心、版本与审计。
- [x] 根路由固定为 `/enterprise/content-management`。
- [x] 列表上下文统一使用 `view/type/status/page`，编辑、审核、发布、版本详情复用 `content_id` 子路由并恢复返回上下文。
- [x] 内容编辑、内容审核、发布管理员明确标为 2026-07-22 human:高颖 批准的 `product_interpretation`，未伪称 Bid 原文。
- [x] 企业主数据只读、CMS 仅写门户补充内容；Top30 为人工策展，不计算算法分数或自动排名。
- [x] 交付轨道为 Track-MS 且仅有 MEDIUM 中屏入口；LARGE / SMALL 无入口。
- [x] 主数据写入、算法评分、自动排名、分析、推荐、对比、导出及用户角色管理均明确排除。
- [x] 页面职责互不替代，跨模块对象、内容与禁止能力边界清晰。
- [x] 与 Bid 的差异逐项记录；无 `product_enhancement`，未使用范围阈值替代批准流程。
- [x] `original_requirement_sources`、`approved_decision_sources`、`derived_definition_sources` 分层列出，设计规格未混入原始需求或衍生四件套。
- [x] IA 已为后续 TRACE、USM、Wireframe 提供一致的能力编号、角色、路由、状态、排除项与来源分类基线。

**IA 结论**：核心 IA 可进入四件套内部一致性评审；该结论不代表门 1 PDR 已闭合，不声明实际交付 Tier，也不解锁工程任务。
