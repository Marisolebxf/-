# IA-ENT-OPS.md

> **模块**：企业发展内容管理 / ENT-OPS / E-37
> **版本 / 日期**：`1.0` / `2026-07-22`
> **状态 / 阶段**：`frozen_for_v1_hifi_round1` / `v1_hifi_round1`；本稿是 V1 高保真首轮执行基线，不代表门 1 PDR 已闭合
> **体验 Owner**：human:高颖
> **交付轨道 / 屏幕**：Track-MS / `medium_1440_1920`；科技专题服务系统仅承接 `1440px–1920px`
> **计划 Tier**：`planned_tier: null`
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
screen_tier: medium_1440_1920
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
- CMS 仅写门户补充内容，包括叙事文本、展示标签、媒体、人工排序、事件说明、关系描述、评估依据与评述。专家仅是业务材料来源，相关字段由 `content_editor` 引用真实 `source_material_ref` 录入或修订。
- 当只读主数据存在错误时，内容编辑可发起纠错请求；纠错不在 ENT-OPS 内直接覆盖数据真源。
- 门户只消费 `published` 版本，不读取草稿、审核意见、内部原因或权限规则。
- 能力榜单中的 Top30 是人工策展顺序；ENT-OPS 不计算技术力、商业力或竞争力算法分数，不自动生成排名。

以上主数据分治与人工策展口径属于 2026-07-22 经 human:高颖 批准的 `product_interpretation`，不是 Bid 原文。

### 1.4 六类内容边界矩阵

| `content_type` / 内容类型 | 适用对象 | 独占 payload 字段或内容 | 共享实体引用 / 媒体规则 | 跨类型禁止行为 |
| --- | --- | --- | --- | --- |
| `enterprise_profile` / 企业基础档案 | 单一企业的门户通用档案 | 短简介、通用展示标签、通用展示媒体及其排序 | 只读 `enterprise_ref` 指向企业主数据；媒体可引用共享媒体资产，但说明、排序、展示位与版本归本 payload | 不以本类型覆盖明星企业代表性叙事或深圳区域叙事；不反写主数据 |
| `growth_event` / 成长轨迹事件 | 单一企业的一条或一组关键发展事件 | 事件日期、标题、摘要、事件类型、来源说明、事件媒体 | 只读 `enterprise_ref`；每个事件及媒体绑定随本类型 payload 独立版本化 | 不从基础档案、新闻或其他类型自动生成、覆盖或同步事件 |
| `key_enterprise_panorama` / 重点企业全景 | 重点企业及企业间描述性关系 | 重点标识、专属档案、合作/供应链/竞争关系描述、全景展示媒体；专家材料只通过 `business_material_source + source_material_ref` 被引用 | 主体和关联方均使用只读企业引用；业务字段 `write_owner: content_editor` | 不计算图谱关系或风险；无专家角色、入口或直写 |
| `capability_ranking` / 能力榜单 | 某榜单类型与期次下的多家企业 | 技术力/商业力类型、期次、评估维度、Top30 人工顺序、评估依据、专家评述；材料只通过 `business_material_source + source_material_ref` 被引用 | 榜单项通过只读 `enterprise_ref` 关联企业；业务字段 `write_owner: content_editor` | 不从其他类型自动取值生成分数或排名；无专家角色、入口或直写 |
| `star_enterprise_intro` / 明星企业介绍 | 被人工选定为代表性对象的企业 | 代表性叙事、核心成果、代表产品、荣誉内容，以及成果/产品/荣誉媒体 | 只读 `enterprise_ref`；可复用媒体资产，但媒体语义、说明、排序和展示位归明星介绍版本 | 不把基础档案短简介或通用展示媒体自动覆盖为代表性叙事；不自动决定明星身份 |
| `shenzhen_enterprise_intro` / 深圳企业介绍 | 深圳本地企业的区域专题介绍 | 区域定位、区域优势、竞争力分析意见、区域叙事及媒体；专家材料只通过 `business_material_source + source_material_ref` 被引用 | 只读 `enterprise_ref`；业务字段 `write_owner: content_editor` | 不把明星介绍或基础档案自动同步为区域叙事；无专家角色、入口或直写 |

六类内容遵循以下统一隔离契约：

1. 同一企业可以同时存在不同 `content_type` 的内容对象；是否存在某一类型不自动决定其他类型的存在。
2. `enterprise_ref` 是各类型共享的只读实体引用，不是共享 payload；共享只限身份引用，不代表字段所有权共享。
3. 每个 `content_type` 的 payload 以自己的 `content_id + content_type + version` 独立版本化、审核、发布、下线和回滚。
4. 同一物理媒体资产允许以 `media_ref` 被多个类型引用，但媒体说明、裁切/展示位、排序、替代文本和使用语境属于各自 payload 版本。
5. 禁止跨 `content_type` 覆盖字段、联动保存或自动同步；需要复用内容时必须由有权限的内容编辑显式确认并在目标类型生成独立草稿。
6. 专家仅是已登记业务材料的来源语义；相关字段必须同时记录 `business_material_source`、真实 `source_material_ref` 与 `write_owner: content_editor`，ENT-OPS 不定义专家产品角色、默认入口或直写权限。

上述内容边界是对六类 Bid 能力可共存、可治理所作的 `product_interpretation`，不新增 Bid 叶子。

### 1.5 明确不承接

- 企业工商、资质、专利、财务等主数据写入或主数据管理；
- 技术力、商业力、竞争力算法评分、自动排名或自动发布榜单；
- 企业搜索、分析、推荐、对比、导出等应用侧能力；
- 用户、角色、权限、数据源或知识图谱的系统级管理；
- `1440px–1920px` 之外的维护入口或重排交付；
- 物理删除已发布内容、版本历史或审计记录。

这些排除项用于明确模块责任，不删除 E-37 的任何直接能力，也不产生 `scope enhancement`。

## 2. 原始需求与批准解释分层

| 层级 | 内容 | 对 IA 的作用 | 不允许的作用 |
| --- | --- | --- | --- |
| `direct_requirement` | Bid §1.1.1.2.4.5.6.3～3.3 的一个叶子、三组内容与六类直接能力 | 决定能力必须存在并提供原始业务语义 | 不从实施、验收或设计文件补写 Bid 原文 |
| `product_interpretation` | 2026-07-22 human:高颖 批准的三角色分工、流程优先工作台、主数据分治、人工榜单、类型隔离、确定性角色入口、下线及版本风险治理 | 让六类能力可进入统一 CMS 流程并形成可用 IA | 不改写历史 Bid，不增加新的验收叶子 |
| 约束 / 索引 | 范围、验收、评审、数据治理、架构与权限政策 | 校验叶子、轨道、屏幕与边界 | 不创造业务页面、角色、字段或能力 |
| 衍生定义 | 当前 ENT-OPS 四件套 | 保持路由、故事、状态、Frame 与排除项一致 | 不充当原始需求来源 |

当前 IA 没有 `product_enhancement`。若后续出现超出六类内容维护与治理所需的业务能力，必须先登记并批准范围变更，不得借 IA 重组静默纳入。

## 3. 用户入口与产品角色

> 下列三角色及职责分离均为 **2026-07-22 human:高颖 批准的 `product_interpretation`**，不得表述为 Bid 原文。权限 persona 仅在后续实现中映射，不替代这里的产品角色。

| 产品角色 | 中屏入口 | 核心目标 | 可执行动作 | 禁止动作 |
| --- | --- | --- | --- | --- |
| 内容编辑 | `/enterprise/content-management?view=mine` | 创建和完善门户补充内容并提交审核 | 新建、编辑、保存草稿、预览、提交审核、发起主数据纠错 | 审核自己的提交、发布、覆盖企业主数据 |
| 内容审核 | `/enterprise/content-management/review` | 核验内容、版本差异与来源说明 | 查看差异、填写意见、审核通过、退回 | 修改正文、直接发布、审核自己的提交 |
| 发布管理员 | `/enterprise/content-management/publish` | 控制上线时机、影响与可追溯性 | 立即/定时发布、退回、下线、回滚、查看审计 | 修改正文、绕过审核发布、删除历史 |

入口规则：

1. 根入口固定为 `/enterprise/content-management`；内容编辑默认进入 `/enterprise/content-management?view=mine`，内容审核默认进入 `/enterprise/content-management/review`，发布管理员默认进入 `/enterprise/content-management/publish`。
2. 多角色账号首次进入时按 `发布管理员 > 内容审核 > 内容编辑` 选择默认入口。
3. 用户显式切换到自己有权访问的入口后，系统可记忆其上次显式选择；后续优先恢复该入口。记忆入口已失权或不存在时，重新按角色优先级选择。
4. `view` 只描述内容工作台的列表视图，不用于表达审核中心或发布中心角色入口。
5. 无权限时保留节点说明并呈现可解释的无权限状态，不以“仅隐藏按钮”代替权限反馈。
6. 本模块唯一屏幕契约是 `medium_1440_1920`；科技专题服务系统仅在 `1440px–1920px` 展示 ENT-OPS 菜单、快捷入口和深链入口。

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
| 内容工作台 | 汇总角色待办、状态计数与统一内容列表；承载搜索、新建、类型/状态筛选 | F-OPS-01 五个固定 `route_variant_id` | 六类能力的统一流程入口；工作台组织方式为 `product_interpretation` |
| 待我处理 | 只显示内容编辑可继续处理的草稿与退回项 | `editor_workbench` 派生 `view=mine` | 流程入口，不新增 Bid 能力 |
| 全部内容 | 查看权限范围内全部六类内容及其当前流程状态 | `all_content` 派生 `view=all` | 六类直接能力总览 |
| 企业基础档案 | 维护门户展示名称、短简介、通用展示标签和通用展示媒体；并列展示只读企业主数据 | `type=enterprise_profile` | IA-ENT-OPS-CAP-01；主数据只读为批准解释 |
| 成长轨迹事件 | 录入事件日期、标题、摘要、类型、媒体和来源说明，形成结构化时间节点 | `type=growth_event` | IA-ENT-OPS-CAP-02 |
| 重点企业全景 | 维护重点标识、专属档案及合作、供应链、竞争关系的描述性内容 | `type=key_enterprise_panorama` | IA-ENT-OPS-CAP-03；不计算图谱关系或风险 |
| 能力榜单 | 维护技术力/商业力榜单期次、评估维度、Top30 顺序、评估依据与专家评述 | `type=capability_ranking` | IA-ENT-OPS-CAP-04；人工顺序，不计算分数 |
| 明星企业介绍 | 维护代表性叙事、核心成果、代表产品、荣誉内容及成果/产品/荣誉媒体 | `type=star_enterprise_intro` | IA-ENT-OPS-CAP-05；荣誉内容不反写主数据，payload 与基础档案隔离 |
| 深圳企业介绍 | 维护区域定位、优势、竞争力分析意见、区域叙事及区域叙事媒体 | `type=shenzhen_enterprise_intro` | IA-ENT-OPS-CAP-06；payload 与明星介绍隔离，不生成区域统计或竞争力分数 |
| 内容编辑器 | 在同一 `content_id` 下展示企业主数据只读区、分型 CMS 表单、门户预览与完整性检查 | `/content/:content_id/edit` | 六类直接能力的写入落点；三栏结构由 Wireframe 细化 |
| 审核中心 | 汇总待审核内容；审核详情展示版本差异、来源说明和审核意见 | `/enterprise/content-management/review`、`/content/:content_id/review` | 审核职责为批准解释 |
| 发布中心 | 汇总待发布内容；发布详情展示范围、生效时间、影响摘要、原因与二次确认 | `/enterprise/content-management/publish`、`/content/:content_id/publish` | 发布职责和高风险控制为批准解释 |
| 版本与审计 | 展示版本时间线、操作人、时间、原因和差异，支持受控下线与回滚 | `/enterprise/content-management/versions`、`/content/:content_id/versions` | 版本治理为批准解释；历史不可物理删除 |

## 6. 路由与状态保留

### 6.1 路由契约

| 场景 | 路由 |
| --- | --- |
| 根入口 / 内容工作台 | `/enterprise/content-management` |
| F-OPS-01 五个列表态 | `editor_workbench=/enterprise/content-management?view=mine`；`all_content=/enterprise/content-management?view=all`；`review_center=/enterprise/content-management/review`；`publish_center=/enterprise/content-management/publish`；`versions_center=/enterprise/content-management/versions` |
| 内容编辑 | `/enterprise/content-management/content/:content_id/edit?route_variant_id&type&status&page` |
| 审核详情 | `/enterprise/content-management/content/:content_id/review?route_variant_id&type&status&page` |
| 发布详情 | `/enterprise/content-management/content/:content_id/publish?route_variant_id&type&status&page` |
| 版本详情 | `/enterprise/content-management/content/:content_id/versions?route_variant_id&type&status&page` |
| 冲突处理 | `/enterprise/content-management/content/:content_id/edit?route_variant_id&type&status&page&state=conflict` |

`route_variant_id` 是所有详情返回上下文的唯一必填键，枚举固定为 `editor_workbench / all_content / review_center / publish_center / versions_center`；`type/status/page` 均可选。pathname 与工作台 `view` 只能由上表的固定 variant path 派生，调用方不得传 `view`、pathname 或 `return_path`。原 variant 失权、缺失或未知时，按当前仍有效权限的“发布管理员 > 内容审核 > 内容编辑”选择默认入口；全部失权时显示可解释的无权限状态。

新建内容在持久化前可使用 `/enterprise/content-management/content/new/edit`，并携带同一 `route_variant_id/type/status/page` 合同；首次保存成功并取得 `content_id` 后必须替换为规范对象路由。详情不使用标题、企业名称或列表序号充当对象标识。

### 6.2 工作流状态

```text
草稿 --提交--> 待审核 --通过--> 待发布 --发布--> 已发布
  ^               |退回          |退回
  └---------------┴--------------┘

已发布 --下线（原因 + 二次确认）--> 已下线
已下线 --基于历史版本重新编辑--> 新草稿 --提交--> 待审核 --通过--> 待发布 --发布--> 新已发布版本
```

- 审核退回或发布退回必须填写原因，内容回到草稿。
- 已发布版本再次编辑时创建新草稿；线上 `published` 版本继续服务门户。
- 发布可立即生效或设置生效时间。
- 发布、下线、回滚及批量关系变更必须填写原因、二次确认并写入审计链。
- 已发布内容下线后进入“已下线”，门户停止消费该内容的 `published` 指针；历史发布版本、下线原因、操作人和时间完整保留。
- 已下线内容重新上线时，必须从选定历史版本生成新草稿，重新走提交、审核、发布；禁止把“已下线”直接切回“已发布”。
- 回滚以历史发布版本生成新的已发布版本，不倒写、不覆盖、不删除历史。
- 并发冲突保留当前输入，进入差异比较与重新保存流程。
- 保存或发布失败不得提前改变前端流程状态，也不得清空用户输入。
- 全部 13 个变更 action 统一引用 TRACE `ui_operation_state_contract` 与 Wireframe `operation_state_contract`：局部操作仅使用 `idle / submitting / succeeded / failed`，`submitting` 禁止重复提交，`failed` 保留 dirty input 和原 business state，不伪造成功或提前跳转。

### 6.3 页面状态

各节点按适用性覆盖默认、加载、空数据、错误、无权限、只读锁定、保存中、保存成功、保存失败、审核退回、发布失败、已下线、从历史生成新草稿、草稿与线上版本并存、并发冲突。空状态不得使用 Mock 内容伪装真实业务数据。

## 7. 跨模块边界

| 来源或去向 | 可携带内容 | ENT-OPS 可执行 | 不可携带 / 不可承担 |
| --- | --- | --- | --- |
| 企业主数据域 | 稳定企业引用、名称、工商、资质等事实字段 | 只读展示、引用、发起纠错 | 覆盖主数据、改变主数据真源、虚构物理主键 |
| 门户企业发展展示 | `content_id`、内容类型、当前 `published` 指针、展示载荷、生效时间 | 发布时更新指针；下线时停止该指针消费；回滚时生成并指向新已发布版本 | 向门户暴露草稿、已下线内容、审核意见、操作原因或内部权限 |
| 企业分析 / 对比能力 | 可引用同一企业对象和已发布说明 | 维护人工叙事与评述 | 执行分析、推荐、对比、评分、自动排名或导出 |
| 企业搜索 | 已发布内容可被下游依法索引 | 提供已发布内容 | 承担搜索结果页、检索策略或搜索权限管理 |
| 身份与权限平台 | 角色映射与授权结果 | 消费授权结果并呈现无权限状态 | 创建用户、管理角色、配置系统级权限 |
| 数据 / 算法平台 | 若后续有只读计算事实，可分源展示 | 保持计算事实与 CMS 内容分开标识 | 计算或修改技术力、商业力、竞争力分数 |
| 契约屏幕范围外 | 无 ENT-OPS 维护入口 | 无 | 将 `medium_1440_1920` 工作台缩放、复制或重排到其他屏幕轨道 |

跨模块跳转只能携带稳定对象引用、来源摘要和已授权的返回上下文；不得借跨模块跳转把排除能力反向嵌入 ENT-OPS。

## 8. 与 Bid 差异说明

| Bid 原始功能 / 文字 | IA 归位或差异 | 分类 | 追溯动作 |
| --- | --- | --- | --- |
| 企业发展内容管理包含三组、六类维护能力 | 统一归入一个流程优先工作台，六类作为稳定导航和筛选维度 | `product_interpretation`（组织方式） | 六类均映射 E-37，保持 `leaves_required = leaves_mapped = 1` |
| 六类能力可围绕同一企业维护不同内容 | 共享只读 `enterprise_ref` 与可复用媒体资产引用，但各 `content_type` payload 独立版本化，禁止跨类型覆盖或自动同步 | `product_interpretation`（内容边界） | TRACE / USM / Wireframe 保持类型所有权、版本和禁止行为一致 |
| 可手动维护企业名称、成立时间、行业、规模等基础属性 | 企业主数据字段只读；CMS 仅维护门户展示补充内容，错误通过纠错流程处理 | `product_interpretation`（2026-07-22 human:高颖 批准的主数据分治） | TRACE 须保留 Bid 原句与差异说明，不得把批准解释改写为 Bid 原文 |
| 可录入关键发展历程事件 | 归位为“成长轨迹事件”内容类型，并进入草稿—审核—发布治理 | `direct_requirement` + 流程 `product_interpretation` | 落点 IA-ENT-OPS-CAP-02 |
| 基于专家建议筛选重点企业并维护关系描述 | 归位为“重点企业全景”；专家仅作为 `business_material_source`，由 `content_editor` 引用 `source_material_ref` 维护描述性内容 | `direct_requirement` + 边界解释 | 落点 IA-ENT-OPS-CAP-03；无专家角色、入口或直写 |
| 定义技术力、商业力评估维度并手动维护 Top30 | 归位为“能力榜单”；明确人工排序，不产生算法分数或自动排名 | `direct_requirement`；人工策展边界为 `product_interpretation` | 落点 IA-ENT-OPS-CAP-04；无统计 `metric_id` |
| 维护明星企业与深圳企业介绍 | 分别保留独立内容类型；竞争力仅记录由 `content_editor` 根据已登记专家材料录入的分析意见 | `direct_requirement` | 落点 IA-ENT-OPS-CAP-05 / 06；材料引用可追溯 |
| Bid 未规定编辑、审核、发布三角色、默认入口与版本治理 | 增加职责分离、确定性入口、下线后重审重发、发布风险控制和版本审计，作为 CMS 可用性解释 | `product_interpretation`（2026-07-22 human:高颖 批准） | TRACE / USM / Wireframe 必须保持角色、入口、状态、动作与禁止项一致 |

本 IA 不包含 `product_enhancement`，不以 ±10% 规则作为范围变更授权，也未删除、合并或拆分 E-37 叶子。

## 9. 来源清单

### 9.1 original_requirement_sources

仅列 Bid 精确章节：

```yaml
original_requirement_sources:
  - file: agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
    authority: original_requirement
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
    effect: 三角色、流程优先 IA、主数据分治、人工榜单、版本与高风险操作治理、五 route variant 返回合同、统一操作态与专家材料来源边界
```

### 9.3 derived_definition_sources

仅列当前四件套；除本文件外其余为同包待生成文件：

```yaml
derived_definition_sources:
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md
    artifact: IA
    status: current
    freeze_scope: frozen_for_v1_hifi_round1
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml
    artifact: TRACE
    status: current
    freeze_scope: frozen_for_v1_hifi_round1
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md
    artifact: USM
    status: current
    freeze_scope: frozen_for_v1_hifi_round1
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md
    artifact: Wireframe
    status: current
    freeze_scope: frozen_for_v1_hifi_round1
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
- [x] 六类内容边界矩阵明确适用对象、独占字段、共享实体/媒体规则；同一企业可存在多类型内容，各 payload 独立版本化且禁止跨类型覆盖或自动同步。
- [x] 信息树完整包含内容工作台、待我处理、全部内容、六类内容、审核中心、发布中心、版本与审计。
- [x] 根路由固定为 `/enterprise/content-management`。
- [x] F-OPS-01 仅有五个固定 route variant；详情以必填 `route_variant_id` 和可选 `type/status/page` 恢复上下文，工作台 `view` 只由 variant path 派生。
- [x] 内容编辑、内容审核、发布管理员明确标为 2026-07-22 human:高颖 批准的 `product_interpretation`，未伪称 Bid 原文。
- [x] 企业主数据只读、CMS 仅写门户补充内容；Top30 为人工策展，不计算算法分数或自动排名。
- [x] 三角色默认入口已确定；多角色首次按“发布管理员 > 内容审核 > 内容编辑”，后续仅恢复仍有权限的上次显式选择入口。
- [x] 状态机覆盖“已发布 → 已下线 → 新草稿 → 重新审核/发布”；下线停止门户 `published` 指针消费并保留历史，回滚仍生成新已发布版本。
- [x] 交付轨道为 Track-MS，唯一屏幕契约为 `screen_tier: medium_1440_1920`；科技专题服务系统仅承接 `1440px–1920px`。
- [x] 主数据写入、算法评分、自动排名、分析、推荐、对比、导出及用户角色管理均明确排除。
- [x] 页面职责互不替代，跨模块对象、内容与禁止能力边界清晰。
- [x] 与 Bid 的差异逐项记录；无 `product_enhancement`，未使用范围阈值替代批准流程。
- [x] `original_requirement_sources`、`approved_decision_sources`、`derived_definition_sources` 分层列出，设计规格未混入原始需求或衍生四件套。
- [x] IA 已为后续 TRACE、USM、Wireframe 提供一致的能力编号、角色、路由、状态、排除项与来源分类基线。

**IA 结论**：本 IA 已作为 V1 高保真首轮执行基线与同版四件套冻结；该结论不代表门 1 PDR 已闭合，不声明实际交付 Tier，也不解锁工程任务。
