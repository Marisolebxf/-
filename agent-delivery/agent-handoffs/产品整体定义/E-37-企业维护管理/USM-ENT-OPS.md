# USM-ENT-OPS.md

> **模块**：企业发展内容管理 / ENT-OPS / E-37
> **状态**：核心产品包本地评审稿
> **体验 Owner**：`human:高颖`
> **交付轨道 / 阶段**：`Track-MS` / `delivery_stage: v1_hifi_round1`
> **屏幕层级**：`screen_tier: medium`
> **原始需求唯一来源**：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.5.6.3～§1.1.1.2.4.5.6.3.3`
> **评审边界**：本文只表示核心产品包可本地评审，不表示门 1 PDR 已闭合，不声明实际交付 Tier。

## 模块：企业发展内容管理 / E-37

ENT-OPS 以一个中屏统一内容工作台承接企业基础档案、成长轨迹事件、重点企业全景、能力榜单、明星企业介绍和深圳企业介绍六类内容的起草、复核、发布与版本治理。六类能力仍属于 E-37 一个 Bid 叶子；本模块不写入企业主数据，不计算技术力、商业力或竞争力分数，不执行自动排名。

## 来源分层与使用边界

| 层级 | 来源 | 本 USM 用法 | 禁止用法 |
| --- | --- | --- | --- |
| 原始需求 | Bid `§1.1.1.2.4.5.6.3～§1.1.1.2.4.5.6.3.3` | 决定 E-37 一个叶子及六类直接维护能力 | 不从其他文件补写或改写 Bid 原文 |
| 当前衍生定义 | `IA-ENT-OPS.md`、`TRACE-ENT-OPS.yaml` | 冻结当前角色、故事、路由、Frame、action、验收与挂载的一致性 | 不充当原始需求来源 |
| 批准决定 | `docs/superpowers/specs/2026-07-22-ent-ops-product-package-design.md` | 作为 `human:高颖` 批准的 `product_interpretation`，支撑三角色、流程、主数据分治、人工榜单、内容隔离与风险治理 | 不改写 Bid 历史原文，不新增叶子 |
| 补充约束 / 追溯 | SRS `## 6. 其他需求`、`## 7. 需求-验收追溯矩阵` | 前者只用于系统性约束，后者只用于 E-37 映射和遗漏检查 | 不产生业务能力、角色、页面、字段或交互 |

## 目标用户角色

> 三个产品角色的依据是 2026-07-22 由 `human:高颖` 批准的 `product_interpretation`，不是 Bid 原文。实现权限映射只作访问约束，不替代产品角色来源。发布管理员的稳定角色 ID 以当前已审定 TRACE 的 `publishing_admin` 为准；`release_administrator` 不是当前四件套契约。

| 角色 ID | 产品角色 | 角色依据 | 需要完成的业务任务 |
| --- | --- | --- | --- |
| `content_editor` | 内容编辑 | 批准的 `PI-ENT-OPS-01` | 新建、分型编辑和保存六类内容，预览后提交审核，对只读主数据发起纠错 |
| `content_reviewer` | 内容审核 | 批准的 `PI-ENT-OPS-01` | 核对当前草稿与对照版本差异、来源说明和审核意见，通过或退回非本人提交的内容 |
| `publishing_admin` | 发布管理员 | 批准的 `PI-ENT-OPS-01` | 核对发布范围和影响，执行立即/定时发布、发布退回、下线、回滚与审计查看 |

### 实现权限映射（仅作约束）

| 产品角色 | 实现权限层级 | 约束用途 |
| --- | --- | --- |
| 内容编辑 | `L4` 子角色 | 只开放编辑、草稿、预览、提交和纠错动作；禁止审核本人提交、发布或覆盖主数据 |
| 内容审核 | `L4` 子角色 | 只开放差异、来源、意见、通过和退回；禁止修改正文、直接发布或自审 |
| 发布管理员 | `L4` 子角色 | 只开放发布治理、下线、回滚和审计；禁止修改正文、绕过审核或删除历史 |

## 用户故事（As / Want / So that）

### US-ENT-OPS-01 统一待办

作为内容编辑、内容审核或发布管理员，我想从统一工作台进入与当前角色相符的待办视图并保留列表上下文，以便快速找到自己可继续处理的 E-37 内容。

- `role_ids`: `[content_editor, content_reviewer, publishing_admin]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management`
- `route_variant_ids`: `[editor_workbench, content_reviewer_center, publishing_admin_center]`
- `frame_ids`: `[F-OPS-01]`；`state`: `default`
- `action_ids`: `[]`
- `acceptance_ids`: `[ENT-OPS-USM-01, ENT-OPS-USM-02, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F01-WORKBENCH-TITLE]`

### US-ENT-OPS-02 编辑六类内容

作为内容编辑，我想按内容类型独立编辑、保存、预览和提交企业内容，以便六类 Bid 直接能力都能在不覆盖主数据或其他类型 payload 的前提下持续更新。

- `role_ids`: `[content_editor]`
- `source_relation`: `direct_requirement`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/edit?view&type&status&page`
- `frame_ids`: `[F-OPS-02]`；`state`: `draft`
- `action_ids`: `[save_draft, create_draft_from_version, batch_relation_change, submit_for_review]`
- `acceptance_ids`: `[ENT-OPS-USM-02, ENT-OPS-USM-03, ENT-OPS-USM-04, ENT-OPS-USM-05, ENT-OPS-USM-06, ENT-OPS-USM-10, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F02-EDITOR-TITLE, ENT-OPS-F02-MASTER-DATA-BOUNDARY]`

### US-ENT-OPS-03 审核差异

作为内容审核，我想查看当前草稿与对照版本的差异及来源说明，以便在不修改正文、不审核自己提交的前提下决定通过或退回。

- `role_ids`: `[content_reviewer]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/review?view&type&status&page`
- `frame_ids`: `[F-OPS-03]`；`state`: `pending_review`
- `action_ids`: `[approve_review, return_from_review]`
- `acceptance_ids`: `[ENT-OPS-USM-06, ENT-OPS-USM-07, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F03-REVIEW-TITLE]`

### US-ENT-OPS-04 发布与退回

作为发布管理员，我想在核对发布范围、生效时间和影响摘要后立即发布、定时发布或退回，以便上线变更受控、可追溯且失败时不会被误报为已发布。

- `role_ids`: `[publishing_admin]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/publish?view&type&status&page`
- `frame_ids`: `[F-OPS-04]`；`state`: `pending_publish`
- `action_ids`: `[immediate_publish, schedule_publish, scheduled_publish_activate, return_from_publish]`
- `acceptance_ids`: `[ENT-OPS-USM-08, ENT-OPS-USM-09, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F04-PUBLISH-RISK]`

### US-ENT-OPS-05 下线与回滚

作为发布管理员或内容编辑，我想受控地下线、从历史生成新草稿或以历史发布版生成新已发布版，以便停止错误内容服务或恢复经验证内容时仍保留完整历史。

- `role_ids`: `[publishing_admin, content_editor]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/versions?view&type&status&page`
- `frame_ids`: `[F-OPS-05]`；`state`: `published`
- `action_ids`: `[take_offline, create_draft_from_version, rollback_as_new_published_version]`
- `acceptance_ids`: `[ENT-OPS-USM-10, ENT-OPS-USM-11, ENT-OPS-USM-12, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F05-VERSION-AUDIT-TITLE]`

### US-ENT-OPS-06 并发冲突

作为内容编辑，我想在保存时比对服务端新版本与本地输入，以便解决并发冲突后重新保存，而不丢失或强制覆盖当前编辑内容。

- `role_ids`: `[content_editor]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/edit?view&type&status&page&state=conflict`
- `frame_ids`: `[F-OPS-06]`；`state`: `conflict_detected`
- `action_ids`: `[save_draft]`
- `acceptance_ids`: `[ENT-OPS-USM-13, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F06-CONFLICT-TITLE]`

### US-ENT-OPS-07 主数据纠错

作为内容编辑，我想对编辑器中只读主数据的错误发起带原因的纠错请求，以便数据真源的责任方可处理问题，同时 CMS 不直接覆盖主数据。

- `role_ids`: `[content_editor]`
- `source_relation`: `product_interpretation`；`parent_requirement`: `E-37`
- `route`: `/enterprise/content-management/content/:content_id/edit?view&type&status&page`
- `frame_ids`: `[F-OPS-02]`；`state`: `readonly_lock`
- `action_ids`: `[submit_master_data_correction]`
- `acceptance_ids`: `[ENT-OPS-USM-04, ENT-OPS-USM-14]`
- `review_mounts`: `[ENT-OPS-F02-MASTER-DATA-BOUNDARY]`

## 场景 walkthrough（主路径）

### 主路径 A：编辑六类内容并提交

1. `content_editor` 默认进入 `/enterprise/content-management?view=mine`，从待我处理选择新建或现有内容；`view/type/status/page` 作为返回上下文传入 F-OPS-02。
2. 新内容可在 `/content/new/edit` 开始，首次持久化成功后替换为带 `content_id` 的规范路由；已发布或已下线内容不直接编辑原版，必须选择 `source_version_id` 执行 `create_draft_from_version` 生成独立新草稿。
3. 编辑器展示只读 `enterprise_ref` 主数据区、当前 `content_type` 专属 CMS payload 和门户预览。六类 payload 独立版本化，不跨类型覆盖、联动保存或自动同步。
4. 编辑执行 `save_draft`。若为重点企业全景的批量关系变更，`batch_relation_change` 只允许更新 `key_enterprise_panorama_payload.descriptive_relationships`，且必须填写原因、二次确认并写入完整审计；它不计算算法关系、图谱边、关系推断或风险。
5. 能力榜单编辑保留评估维度、Top30 人工顺序、评估依据和专家评述，显式披露为人工策展，不声称算法排名。
6. 完整性校验通过且无未解决冲突后，编辑执行 `submit_for_review`，状态从 `draft` 进入 `pending_review`，并恢复原列表上下文。

### 主路径 B：审核差异

1. `content_reviewer` 默认进入 `/enterprise/content-management/review`，选择 `pending_review` 内容进入 F-OPS-03。
2. 系统展示当前提交版、对照版、字段级差异、来源说明与提交人；审核人只可填写审核意见，不可修改正文。
3. 执行 `approve_review` 前必须验证 `reviewer_id != submitter_id`；满足后状态从 `pending_review` 进入 `pending_publish`。
4. 如不通过，审核人必须填写原因后执行 `return_from_review`，系统写入完整审计并将内容返回 `draft`，编辑的已有内容保留。

### 主路径 C：发布或发布退回

1. `publishing_admin` 默认进入 `/enterprise/content-management/publish`，选择 `pending_publish` 内容进入 F-OPS-04，仅查看已审核内容、发布范围、生效时间和影响摘要，不可修改正文。
2. 立即发布时，管理员填写原因并二次确认后执行 `immediate_publish`，系统写入完整审计并生成新 `published` 版本。
3. 定时发布时，管理员填写原因、`scheduled_effective_at` 并二次确认后执行 `schedule_publish`；此时只记录计划且状态仍为 `pending_publish`。到时由 system event 执行 `scheduled_publish_activate`，才转为 `published` 并记录系统事件审计。
4. 若不应发布，管理员填写原因后执行 `return_from_publish`，系统写入完整审计并返回 `draft`，不得绕过编辑和审核链。

### 主路径 D：下线、重新上线与回滚

1. 发布管理员在 F-OPS-05 选择当前 `published` 版本，填写原因、核对影响摘要并二次确认后执行 `take_offline`；门户停止消费该 `published` 指针，状态转为 `offline`，历史与审计保留。
2. 重新上线时，内容编辑从选定历史版本执行 `create_draft_from_version`，传入 `source_version_id` 生成新草稿，再完整执行 `submit_for_review` → `approve_review` → `immediate_publish` 或 `schedule_publish` / `scheduled_publish_activate`；禁止 `offline` 直接切回 `published`。
3. 回滚时，发布管理员选择历史发布版，填写原因、查看前后差异并二次确认后执行 `rollback_as_new_published_version`；系统生成新 `published` 版本，不倒写、覆盖或删除历史。

### 主路径 E：主数据纠错

1. 内容编辑在 F-OPS-02 的企业主数据只读区发现错误，选择待纠错字段并填写纠错原因。
2. 编辑执行 `submit_master_data_correction`，系统保持主数据只读，写入 `enterprise_ref`、纠错字段、原因和操作审计。
3. 提交成功后显示真实 `correction_request_id`；纠错请求不进入 CMS payload，不作为发布内容。

## 异常与降级路径

| 场景 | 页面行为 | 用户下一步 / 系统保护 |
| --- | --- | --- |
| 空列表 | F-OPS-01 显示与当前角色、`view/type/status` 匹配的空态，不用 Mock 内容伪装业务数据 | 有新建权限的编辑可新建；其他角色可调整筛选或返回 |
| 列表或详情加载失败 | 保留路由和列表上下文，显示可重试错误，不把失败显示为空数据 | 重试或回到原 `view/type/status/page` |
| 无权限 | 显示可解释的 `no_permission` 状态，不只隐藏按钮，不泄露未授权草稿 | 返回有权入口或按组织流程申请权限 |
| 保存失败 | F-OPS-02 维持 `draft` 和全部本地输入，不显示保存成功，不提前改变版本 | 修正校验问题或重试 `save_draft` |
| 审核退回 | F-OPS-03 要求原因并记录完整审计，内容回到 `draft`，不清空已编辑内容 | 编辑根据原因修订后重新提交 |
| 发布失败 | F-OPS-04 保留原流程状态、发布原因、生效时间与用户输入，明确显示 `publish_failure`，不得显示或切换为 `published` | 重试或退回，禁止假成功 |
| 并发冲突 | F-OPS-06 保留本地输入，展示服务端新版本与本地差异，不强制覆盖 | 用户刷新比较、解决差异后重新 `save_draft` |
| 纠错失败 | F-OPS-02 显示 `correction_failure`，保留选定字段和纠错原因，不生成虚假请求号，不将主数据显示为已修正 | 重试 `submit_master_data_correction` 或保留内容后离开 |
| 定时发布到时未生效 | 保持 `pending_publish`，展示计划时间和未激活错误，不得补写虚假 `published` 或伪造 system event 审计 | 发布管理员查看审计并重试/调整计划；只有真实 `scheduled_publish_activate` 成功才转 `published` |

## 验收场景（逐条可测试）

| 编号 | 给定 / 当 / 则 | `action_ids` | 故事 / Frame / 评审挂载 |
| --- | --- | --- | --- |
| `ENT-OPS-USM-01` | 给定分别拥有编辑、审核、发布角色的用户，当首次进入 ENT-OPS，则内容编辑进入 `/enterprise/content-management?view=mine`，内容审核进入 `/enterprise/content-management/review`，发布管理员进入 `/enterprise/content-management/publish`；三者均落在 F-OPS-01 的不同 `route_variant`。多角色首次按“发布管理员 > 内容审核 > 内容编辑”选择，之后只恢复仍有权的上次显式选择。 | `[]` | US-ENT-OPS-01 / F-OPS-01 / `ENT-OPS-F01-WORKBENCH-TITLE` |
| `ENT-OPS-USM-02` | 给定用户已设置 `view/type/status/page`，当进入编辑、审核、发布或版本子路由并完成、取消或返回，则原筛选和页码完整恢复，浏览器前进/后退也不回到无筛选首页。 | `[]` | US-ENT-OPS-01、US-ENT-OPS-02 / F-OPS-01、F-OPS-02 / `ENT-OPS-F01-WORKBENCH-TITLE`、`ENT-OPS-F02-EDITOR-TITLE` |
| `ENT-OPS-USM-03` | 给定六类 `content_type` 各自的草稿，当内容编辑执行 `save_draft`，则只保存当前类型 payload。当对重点企业全景执行 `batch_relation_change`，则只更新 `key_enterprise_panorama_payload.descriptive_relationships` 人工描述，且执行前必须填写原因、二次确认并生成完整审计；不产生算法关系、图谱边、关系推断或风险计算。 | `[save_draft, batch_relation_change]` | US-ENT-OPS-02 / F-OPS-02 / `ENT-OPS-F02-EDITOR-TITLE` |
| `ENT-OPS-USM-04` | 给定 F-OPS-02 展示企业主数据，当内容编辑尝试编辑主数据或发现错误，则主数据字段保持只读；编辑只能填写纠错字段与原因后执行 `submit_master_data_correction`，且 CMS 不覆盖数据真源。 | `[submit_master_data_correction]` | US-ENT-OPS-02、US-ENT-OPS-07 / F-OPS-02 / `ENT-OPS-F02-MASTER-DATA-BOUNDARY` |
| `ENT-OPS-USM-05` | 给定内容类型为 `capability_ranking`，当编辑查看或 `save_draft`，则页面明确披露 Top30 为人工策展顺序，并保留评估维度、评估依据和专家评述，不声称算法排名或生成算法分数。 | `[save_draft]` | US-ENT-OPS-02 / F-OPS-02 / `ENT-OPS-F02-EDITOR-TITLE` |
| `ENT-OPS-USM-06` | 给定内容完整且无未解决冲突的 `draft`，当内容编辑执行 `submit_for_review`，则状态进入 `pending_review`。当内容审核执行 `approve_review`，则必须满足 `reviewer_id != submitter_id`，审核者不可修改正文，通过后进入 `pending_publish`；自审必须被拒绝。 | `[submit_for_review, approve_review]` | US-ENT-OPS-02、US-ENT-OPS-03 / F-OPS-02、F-OPS-03 / `ENT-OPS-F02-EDITOR-TITLE`、`ENT-OPS-F03-REVIEW-TITLE` |
| `ENT-OPS-USM-07` | 给定待审内容，当审核者查看时，则可见当前草稿与对照版本的差异和来源说明；当执行 `return_from_review`，则必须填写原因、记录完整审计并返回 `draft`，不清空草稿内容。 | `[approve_review, return_from_review]` | US-ENT-OPS-03 / F-OPS-03 / `ENT-OPS-F03-REVIEW-TITLE` |
| `ENT-OPS-USM-08` | 给定 `pending_publish` 内容，当发布管理员执行 `immediate_publish` 或 `schedule_publish`，则执行前均展示发布范围、生效时间和影响摘要，要求原因、二次确认并记录完整审计。`schedule_publish` 只写入 `scheduled_effective_at` 且保持 `pending_publish`，到时只有 system event `scheduled_publish_activate` 成功才转为 `published` 并记录审计；发布管理员也可填写原因执行 `return_from_publish`，完整审计后返回 `draft`。 | `[immediate_publish, schedule_publish, scheduled_publish_activate, return_from_publish]` | US-ENT-OPS-04 / F-OPS-04 / `ENT-OPS-F04-PUBLISH-RISK` |
| `ENT-OPS-USM-09` | 给定立即发布、定时计划写入或定时激活失败，当系统返回失败，则 F-OPS-04 不显示或提前切换为 `published`，保留原流程状态、原因、生效时间及其他用户输入，不伪造成功审计。 | `[immediate_publish, schedule_publish, scheduled_publish_activate]` | US-ENT-OPS-04 / F-OPS-04 / `ENT-OPS-F04-PUBLISH-RISK` |
| `ENT-OPS-USM-10` | 给定内容已为 `published`，当内容编辑要再次编辑，则必须传入 `source_version_id` 执行 `create_draft_from_version` 生成独立新草稿，再用 `save_draft` 保存草稿内修改；线上 `published` 版本及历史不被覆盖，并继续服务门户。 | `[create_draft_from_version, save_draft]` | US-ENT-OPS-02、US-ENT-OPS-05 / F-OPS-02、F-OPS-05 / `ENT-OPS-F02-EDITOR-TITLE`、`ENT-OPS-F05-VERSION-AUDIT-TITLE` |
| `ENT-OPS-USM-11` | 给定 `published` 内容，当发布管理员执行 `take_offline`，则必须填写原因、二次确认并记录完整审计。当 `offline` 内容要再上线，则必须传入 `source_version_id` 执行 `create_draft_from_version`，再执行 `submit_for_review`、`approve_review` 以及 `immediate_publish` 或 `schedule_publish` / `scheduled_publish_activate`；任何 `offline` 直接切回 `published` 的尝试必须被拒绝。 | `[take_offline, create_draft_from_version, submit_for_review, approve_review, immediate_publish, schedule_publish, scheduled_publish_activate]` | US-ENT-OPS-05 / F-OPS-05 / `ENT-OPS-F05-VERSION-AUDIT-TITLE` |
| `ENT-OPS-USM-12` | 给定发布管理员在 F-OPS-05 选择历史发布版，当执行 `rollback_as_new_published_version`，则执行前必须填写原因、查看前后差异并二次确认，系统写入完整审计并生成新 `published` 版本，不覆盖或删除历史。 | `[rollback_as_new_published_version]` | US-ENT-OPS-05 / F-OPS-05 / `ENT-OPS-F05-VERSION-AUDIT-TITLE` |
| `ENT-OPS-USM-13` | 给定 `save_draft` 发现乐观版本不匹配，当进入 F-OPS-06，则系统保留当前全部输入，展示服务端新版本与本地差异；只有用户刷新比较、处理差异后才可重新保存，禁止清空输入或强制覆盖。 | `[save_draft]` | US-ENT-OPS-06 / F-OPS-06 / `ENT-OPS-F06-CONFLICT-TITLE` |
| `ENT-OPS-USM-14` | 给定以评审模式分别打开 F-OPS-01～F-OPS-06，则 7 个唯一挂载 `ENT-OPS-F01-WORKBENCH-TITLE`、`ENT-OPS-F02-EDITOR-TITLE`、`ENT-OPS-F02-MASTER-DATA-BOUNDARY`、`ENT-OPS-F03-REVIEW-TITLE`、`ENT-OPS-F04-PUBLISH-RISK`、`ENT-OPS-F05-VERSION-AUDIT-TITLE`、`ENT-OPS-F06-CONFLICT-TITLE` 均出现在 TRACE 指定宿主；给定业务模式再打开同一组 Frame，则上述挂载全部不渲染（`business_mode: absent`），且切换模式不改变业务字段、权限或流程。 | `[]` | US-ENT-OPS-01～US-ENT-OPS-07 / F-OPS-01～F-OPS-06 / 全部 7 个挂载 |

## 与 bid-reference 差异说明

| Bid 原始功能 / 章节 | 当前 IA / 故事归位 | 分类 | 是否影响范围 / TRACE 动作 |
| --- | --- | --- | --- |
| `§1.1.1.2.4.5.6.3～3.3` 的三组、六类维护能力 | 在 F-OPS-01 统一工作台中以六类稳定导航/筛选归位，在 F-OPS-02 分型编辑 | 直接能力 + 组织方式 `product_interpretation` | 否；E-37 仍为单一叶子，`leaves_required = leaves_mapped = 1` |
| 六类内容可围绕企业维护 | 公共层只共享只读 `enterprise_ref` 和可复用 `media_ref`；六类 payload、语义、排序、展示位与版本独立，禁止跨类型覆盖、联动保存或自动同步 | `product_interpretation` | 否；落于 PI-ENT-OPS-06、US-ENT-OPS-02 |
| Bid 允许手动维护企业基本属性 | 企业主数据只读，CMS 只写门户补充内容，错误通过纠错请求处理 | `product_interpretation` | 否；落于 PI-ENT-OPS-02、US-ENT-OPS-07，不把批准解释伪装为 Bid 原文 |
| Bid 要求手动维护技术力和商业力 Top30 | 能力榜单保留评估维度、企业顺序、评估依据与专家评述，明确为人工策展，不计分、不自动排名 | `product_interpretation` | 否；落于 PI-ENT-OPS-03、ENT-OPS-USM-05 |
| Bid 未规定三角色、确定性入口与治理状态 | 内容编辑、内容审核、发布管理员分工；使用流程优先工作台、草稿—审核—发布状态与角色默认入口 | `product_interpretation` | 否；落于 PI-ENT-OPS-01、PI-ENT-OPS-04 与 US-ENT-OPS-01、03、04 |
| Bid 未规定已发布再编辑、下线、回滚和批量关系变更的风险控制 | 已发布/已下线版本通过 `create_draft_from_version` 生成新草稿；高风险操作要求原因、二次确认和完整审计 | `product_interpretation` | 否；落于 PI-ENT-OPS-05、US-ENT-OPS-02、05、06 |

**差异结论**：三角色、流程优先归位、主数据分治、人工榜单、六类内容隔离、确定性入口与治理状态均为已批准 `product_interpretation`；当前无 `product_enhancement`，无叶子新增、删除、合并或拆分。

## 指标、开放项与阻断缺口

```yaml
metrics:
  applicability: N/A
  reason: CMS内容与人工顺序无统计指标
  required: 0
  mapped: 0
  metric_ids: []
open_questions: []
blocking_gaps: []
```

## 明确排除项

- 企业工商、统一社会信用代码、成立时间、资质、专利、财务等主数据写入或主数据管理。
- 技术力、商业力或竞争力算法评分，自动生成排名或自动发布榜单。
- 企业搜索、分析、推荐、对比或导出等应用侧能力。
- 用户、角色、权限、数据源或知识图谱的系统级管理。
- LARGE 大屏或 SMALL 小屏维护入口。
- 物理删除已发布内容、版本历史或审计记录。
- 向门户暴露草稿、已下线内容、审核意见、内部原因或权限规则。

## Typed handoff source inventories

```yaml
original_requirement_sources:
  - file: agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
    sections:
      - "1.1.1.2.4.5.6.3 企业发展内容管理"
      - "1.1.1.2.4.5.6.3.1 企业基础与成长内容维护"
      - "1.1.1.2.4.5.6.3.2 重点企业与竞争力榜单维护"
      - "1.1.1.2.4.5.6.3.3 明星企业与深圳企业介绍维护"
    authority: original_requirement
approved_decision_sources:
  - file: docs/superpowers/specs/2026-07-22-ent-ops-product-package-design.md
    approved_by: human:高颖
    approved_at: "2026-07-22"
    classification: product_interpretation
derived_definition_sources:
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md
    artifact: IA
    status: current
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml
    artifact: TRACE
    status: current
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md
    artifact: USM
    status: current
  - file: agent-delivery/agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md
    artifact: Wireframe
    status: planned
supplemental_constraint_sources:
  - file: agent-delivery/验收文档/企业要素需求规格说明书SRS(v1).md
    section: "## 6. 其他需求"
    allowed_use: 仅用于系统性约束与合规预留，不产生业务能力、角色、页面或交互
  - file: agent-delivery/验收文档/企业要素需求规格说明书SRS(v1).md
    section: "## 7. 需求-验收追溯矩阵"
    allowed_use: 仅用于 E-37 验收映射与遗漏检查，不扩大 Bid 范围
```

## USM 自检

- [x] 共 7 个唯一故事 ID，每个故事均为 As / Want / So that，并与 TRACE 的角色、路由、Frame、`action_ids`、`acceptance_ids` 和 `review_mounts` 一致。
- [x] 共 14 个唯一验收 ID，逐条可测试，并与 TRACE statement 和 action 语义一致。
- [x] F-OPS-01～F-OPS-06 全部 6 个 Frame 均被故事或验收引用。
- [x] 7 个唯一评审挂载均被引用，业务模式均为 `absent`，不改变业务字段、权限或流程。
- [x] TRACE 的 `save_draft`、`create_draft_from_version`、`submit_for_review`、`approve_review`、`return_from_review`、`immediate_publish`、`schedule_publish`、`scheduled_publish_activate`、`return_from_publish`、`take_offline`、`rollback_as_new_published_version`、`batch_relation_change`、`submit_master_data_correction` 均有故事和验收语义。
- [x] 空列表、加载失败、无权限、保存失败、审核退回、发布失败、并发冲突、纠错失败和定时发布未生效均有稳定处理；失败不清空输入，不伪造成功状态。
- [x] E-37 保持一个 Bid 叶子，无 `product_enhancement`，`metrics: N/A`、`open_questions: []`、`blocking_gaps: []`。

**USM 结论**：本地核心产品包评审稿已建立完整故事与验收映射；该结论不代表门 1 PDR 已闭合，不声明实际交付 Tier。
