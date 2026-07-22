# Wireframe-ENT-OPS.md

> **模块**：企业发展内容管理 / ENT-OPS / E-37
>
> **对应 IA**：`IA-ENT-OPS.md`
>
> **对应 USM / TRACE**：`USM-ENT-OPS.md` / `TRACE-ENT-OPS.yaml`
>
> **阶段**：Track-MS / `v1_hifi_round1`；本稿是产品定义与 V1 高保真首轮输入，不代表门 1 PDR 已闭合，也不声明实际交付 Tier
>
> **屏幕契约**：`screen_tier: medium`；`planned_tier: null`
>
> **根路由**：`/enterprise/content-management`
>
> **原始需求唯一来源**：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.5.6.3～§1.1.1.2.4.5.6.3.3`

## 1. Wireframe 边界与共同规则

本 Wireframe 只承接 E-37 一个 Bid 叶子内的六类企业发展内容维护，并按当前 IA、TRACE、USM 已审定的三角色、主数据分治、人工榜单、类型隔离和版本治理解释落位。页面不设置 KPI、数量卡或统计指标；所有业务明细字段的 `metric_id` 均为 `—（明细字段）`。

### 1.1 Frame 清单

| Frame | 触发入口 | 目的 | route-state | story_ids | acceptance_ids | source_relation | review_mounts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `F-OPS-01` 内容工作台 | 根入口及三角色默认入口 | 在同一列表态 Frame 中定位当前角色待办和六类内容 | `workbench / editor_workbench / review_center / publish_center` | `US-ENT-OPS-01` | `ENT-OPS-USM-01, ENT-OPS-USM-02, ENT-OPS-USM-14` | `direct_requirement + product_interpretation` | `[ENT-OPS-F01-WORKBENCH-TITLE]` |
| `F-OPS-02` 内容编辑器 | 工作台新建、编辑，或由历史版生成草稿后进入 | 只读核对主数据，分型维护 CMS payload，并同步预览门户效果 | `draft / readonly_lock / saving / save_failure / correction_submitted` | `US-ENT-OPS-02, US-ENT-OPS-07` | `ENT-OPS-USM-02, ENT-OPS-USM-03, ENT-OPS-USM-04, ENT-OPS-USM-05, ENT-OPS-USM-06, ENT-OPS-USM-10, ENT-OPS-USM-14` | `direct_requirement + product_interpretation` | `[ENT-OPS-F02-EDITOR-TITLE, ENT-OPS-F02-MASTER-DATA-BOUNDARY]` |
| `F-OPS-03` 审核详情 | 审核中心列表的待审核行 | 只读查看差异与来源，独立审核或退回 | `pending_review / review_rejected` | `US-ENT-OPS-03` | `ENT-OPS-USM-02, ENT-OPS-USM-06, ENT-OPS-USM-07, ENT-OPS-USM-14` | `product_interpretation` | `[ENT-OPS-F03-REVIEW-TITLE]` |
| `F-OPS-04` 发布确认 | 发布中心列表的待发布行 | 核对范围、时间和影响，立即发布、定时发布或退回 | `pending_publish / publishing / publish_failure` | `US-ENT-OPS-04` | `ENT-OPS-USM-02, ENT-OPS-USM-08, ENT-OPS-USM-09, ENT-OPS-USM-14` | `product_interpretation` | `[ENT-OPS-F04-PUBLISH-RISK]` |
| `F-OPS-05` 版本与审计 | 版本中心或内容详情的版本入口 | 按角色执行下线、回滚或从历史生成草稿，并查看不可变审计链 | `published / offline / create_draft_from_history` | `US-ENT-OPS-05` | `ENT-OPS-USM-02, ENT-OPS-USM-10, ENT-OPS-USM-11, ENT-OPS-USM-12, ENT-OPS-USM-14` | `product_interpretation` | `[ENT-OPS-F05-VERSION-AUDIT-TITLE]` |
| `F-OPS-06` 冲突处理 | 编辑保存检测到乐观版本冲突 | 保留本地输入，对比服务端版本并解决后重存 | `conflict_detected / compare_server_and_local / resaving / save_failure` | `US-ENT-OPS-06` | `ENT-OPS-USM-13, ENT-OPS-USM-14` | `product_interpretation` | `[ENT-OPS-F06-CONFLICT-TITLE]` |

### 1.2 返回上下文契约

- 规范列表上下文为 `view/type/status/page`。F-OPS-02～F-OPS-05 的进入路由必须透传这四项，完成、取消、返回及浏览器前进/后退均恢复原筛选和页码。
- F-OPS-06 继承 F-OPS-02 的完整编辑上下文，并附加 `state=conflict`；解决冲突后回到同一 `content_id` 编辑器，不新建对象、不清空输入。
- 新建在首次持久化前可使用 `/enterprise/content-management/content/new/edit?view&type&status&page`；取得真实 `content_id` 后以 replace 方式切换到规范对象路由。
- 返回目标失权或不存在时，显示可解释的无权限/对象不存在状态；不得静默落回无筛选第一页。

## 2. F-OPS-01 内容工作台

**路由**：`/enterprise/content-management`

**route variants**：

- `root_workbench`：`/enterprise/content-management`，列表态 `workbench`，仅作为根入口与有权角色的确定性分流容器。
- `editor_workbench`：`/enterprise/content-management?view=mine`，列表态 `editor_workbench`，角色 `content_editor`。
- `content_reviewer_center`：`/enterprise/content-management/review`，列表态 `review_center`，角色 `content_reviewer`。
- `publishing_admin_center`：`/enterprise/content-management/publish`，列表态 `publish_center`，角色 `publishing_admin`。

**story_ids**：`[US-ENT-OPS-01]`

**acceptance_ids**：`[ENT-OPS-USM-01, ENT-OPS-USM-02, ENT-OPS-USM-14]`

**source_relation**：`direct_requirement + product_interpretation`

**review_mounts**：`[ENT-OPS-F01-WORKBENCH-TITLE]`

### 2.1 独立线框

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header / 科技专题服务系统 / 当前角色 / 评审模式开关（非业务字段）              │
├──────────────┬───────────────────────────────────────────────────────────────┤
│ Sidebar      │ 面包屑  企业发展内容管理                                     │
│ 企业发展内容 │ 内容工作台 [review mount: F01 title]          [新建内容]       │
│              ├───────────────────────────────────────────────────────────────┤
│ 内容工作台   │ [待我处理|全部内容] [内容类型⌄] [状态⌄] [搜索] [重置]         │
│ 六类内容     ├───────────────────────────────────────────────────────────────┤
│ 审核中心     │ 内容标题 | 企业 | 内容类型 | 流程状态 | 更新时间 | 可执行操作 │
│ 发布中心     │ ------------------------------------------------------------- │
│ 版本与审计   │ ……Arco Table 列表行；操作随角色和状态授权……                  │
│              ├───────────────────────────────────────────────────────────────┤
│              │ 共用列表反馈区（loading / empty / error / no_permission）      │
│              │                                           Pagination  1 2 3  │
└──────────────┴───────────────────────────────────────────────────────────────┘
```

### 2.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 内容标题 `title` | 文本，只读列表字段 | 当前内容版本 | 是 | 某企业成长轨迹 | `—（明细字段）` |
| 企业引用 `enterprise_ref` | 对象引用，只读 | 企业主数据域 | 是 | `ENT-000218` | `—（明细字段）` |
| 内容类型 `content_type` | Arco Select 筛选 / Tag 展示 | TRACE `content_types` | 是 | `growth_event` | `—（明细字段）` |
| 流程状态 `workflow_status` | Arco Select 筛选 / Tag 展示 | TRACE `workflow.states` | 是 | `pending_review` | `—（明细字段）` |
| 更新时间 `updated_at` | 日期时间，只读 | 内容版本审计 | 是 | `2026-07-22 14:30` | `—（明细字段）` |
| 列表视图 `view` | Tabs / 查询参数 | 当前用户显式选择 | 是 | `mine` | `—（明细字段）` |
| 页码 `page` | Pagination / 查询参数 | 当前列表上下文 | 是 | `2` | `—（明细字段）` |

### 2.3 交互表

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `—` / 首次进入根路由 | 多角色按“发布管理员 > 内容审核 > 内容编辑”选择默认 route variant；此后只恢复仍有权的上次显式入口 | 不随机落页；不把三个列表态拆成新增 Frame |
| `—` / 切换 `view/type/status/page` | 仅刷新列表区域，并把状态写入 URL | 不丢筛选，不整页闪烁，不用数量卡替代列表 |
| `—` / 打开列表行 | 按授权进入 F-OPS-02、03、04 或 05，并透传完整返回上下文 | 不用标题、企业名称或行号代替 `content_id` |
| `—` / 无权操作 | 保留节点语义并显示禁用原因或无权限反馈 | 不仅隐藏按钮造成不可解释状态 |

### 2.4 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `default/workbench` | 稳定标题、筛选条、表头与当前角色可访问列表 | 筛选或进入对象；URL 保留当前参数 |
| 编辑列表 `editor_workbench` | 仅显示编辑可继续处理的草稿、退回项及有权内容 | 新建、编辑或查看版本 |
| 审核列表 `review_center` | 仅显示审核角色可处理的 `pending_review` | 进入 F-OPS-03 |
| 发布列表 `publish_center` | 仅显示发布角色可处理的 `pending_publish` | 进入 F-OPS-04 |
| 加载 `loading` | 保留标题、筛选、表头和容器高度，表体显示 Skeleton | 等待或取消筛选请求 |
| 空 `empty` | 说明当前角色与筛选下暂无内容，不填充 Mock 行 | 编辑可新建；其他角色调整筛选 |
| 错误 `error` | 列表区展示真实错误与重试，保留筛选 | 原位重试，不跳首页 |
| 无权限 `no_permission` | 展示节点名称、缺少的访问权限及返回入口 | 返回上一个仍有权的列表上下文 |

## 3. F-OPS-02 内容编辑器

**路由**：`/enterprise/content-management/content/:content_id/edit?view&type&status&page`

**story_ids**：`[US-ENT-OPS-02, US-ENT-OPS-07]`

**acceptance_ids**：`[ENT-OPS-USM-02, ENT-OPS-USM-03, ENT-OPS-USM-04, ENT-OPS-USM-05, ENT-OPS-USM-06, ENT-OPS-USM-10, ENT-OPS-USM-14]`

**source_relation**：`direct_requirement + product_interpretation`

**review_mounts**：`[ENT-OPS-F02-EDITOR-TITLE, ENT-OPS-F02-MASTER-DATA-BOUNDARY]`

### 3.1 独立线框

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ ← 返回原 view/type/status/page   内容编辑器 [review mount: F02 editor title]          │
│ 企业 / content_id / content_type / 草稿状态                    [预览] [保存] [提交审核]│
├───────────────────┬────────────────────────────────────┬────────────────────────────┤
│ 企业主数据（只读）│ CMS 分型表单                      │ 门户预览                   │
│ [review mount:    │ 内容类型：企业基础/成长轨迹/……    │ 当前草稿预览               │
│  master boundary] │ ┌ 当前类型 payload only ───────┐ │ 桌面门户内容结构           │
│ 企业名称           │ │ 字段、媒体、排序、来源说明   │ │ 只反映 CMS + 只读主数据    │
│ 成立时间           │ │ 六类 field_id 严格隔离      │ │ 不显示审核原因/内部字段     │
│ 行业 / 规模        │ └──────────────────────────────┘ │                            │
│ [发起纠错]         │ 榜单：Top30 人工策展，无算法分    │                            │
├───────────────────┴────────────────────────────────────┴────────────────────────────┤
│ 校验/保存反馈；已发布与草稿并存提示                         [取消] [保存草稿] [提交审核]│
└─────────────────────────────────────────────────────────────────────────────────────┘
```

三栏为业务结构，不是可选装饰：左栏企业主数据只读，中栏只编辑当前 `content_type` 的 CMS payload，右栏展示门户消费效果。`<1280px` 时右栏改为 Arco Drawer，由“门户预览”打开；抽屉关闭不丢中栏输入。

### 3.2 公共字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 内容对象 `content_id` | 稳定标识，只读 | CMS 持久化结果 | 已保存对象是 | `CNT-OPS-1024` | `—（明细字段）` |
| 企业引用 `enterprise_ref` | 对象引用，只读 | 企业主数据域 | 是 | `ENT-000218` | `—（明细字段）` |
| 企业名称 / 成立时间 / 行业 / 规模 | Descriptions，只读 | 企业主数据域 | 按主数据返回 | 深圳某科技公司 / 2016 / 新材料 / 中型 | `—（明细字段）` |
| 内容类型 `content_type` | Arco Select，新建选定后锁定 | TRACE `content_types` | 是 | `capability_ranking` | `—（明细字段）` |
| 来源版本 `source_version_id` | 版本引用，只读 | `create_draft_from_version` 输入 | 从历史生成时是 | `VER-0098` | `—（明细字段）` |
| 当前版本 `version` | 乐观锁版本，只读 | CMS 版本 | 是 | `12` | `—（明细字段）` |
| 纠错字段 `correction_fields` | 多选 | 企业主数据只读字段 | 发起纠错时是 | `[industry]` | `—（明细字段）` |
| 纠错原因 `correction_reason` | TextArea | 内容编辑人工输入 | 发起纠错时是 | 行业归类与登记材料不一致 | `—（明细字段）` |
| 纠错请求号 `correction_request_id` | 结果文本，只读 | 纠错队列真实返回 | 成功时是 | `CORR-20260722-0091` | `—（明细字段）` |
| 纠错交接目标 `target` | 结果文本，只读 | TRACE 固定逻辑目标 | 成功时是 | `enterprise_master_data_correction_queue` | `—（明细字段）` |
| 纠错状态 `status` | 结果状态，只读 | 纠错队列真实返回 | 成功时是 | `submitted` | `—（明细字段）` |
| 提交时间 `submitted_at` | 日期时间，只读 | 纠错队列真实返回 | 成功时是 | `2026-07-22T14:30:00+08:00` | `—（明细字段）` |

### 3.3 六类 payload 字段隔离表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| `enterprise_profile_payload.display_name` | Input | 内容编辑 | 是 | 某科技企业 | `—（明细字段）` |
| `enterprise_profile_payload.short_introduction` | TextArea | 内容编辑 | 是 | 专注新材料研发与产业化 | `—（明细字段）` |
| `enterprise_profile_payload.display_tags` | Select 多选 | 内容编辑 | 否 | `[新材料, 专精特新]` | `—（明细字段）` |
| `enterprise_profile_payload.display_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-101` | `—（明细字段）` |
| `growth_event_payload.event_date` | DatePicker | 内容编辑 | 是 | `2025-09-18` | `—（明细字段）` |
| `growth_event_payload.event_title` | Input | 内容编辑 | 是 | 完成 B 轮融资 | `—（明细字段）` |
| `growth_event_payload.event_summary` | TextArea | 内容编辑 | 是 | 融资用于扩建中试线 | `—（明细字段）` |
| `growth_event_payload.event_type` | Select | 内容编辑 | 是 | 融资 | `—（明细字段）` |
| `growth_event_payload.source_note` | TextArea | 内容编辑 | 是 | 企业公告，2025-09-18 | `—（明细字段）` |
| `growth_event_payload.event_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-202` | `—（明细字段）` |
| `key_enterprise_panorama_payload.key_enterprise_flag` | Checkbox | 内容编辑 | 是 | `true` | `—（明细字段）` |
| `key_enterprise_panorama_payload.exclusive_profile` | TextArea | 内容编辑 | 是 | 重点企业专属档案说明 | `—（明细字段）` |
| `key_enterprise_panorama_payload.descriptive_relationships` | 可编辑表格 / 批量编辑 | 专家建议 + 内容编辑人工描述 | 否 | 与某企业存在供应链协作 | `—（明细字段）` |
| `key_enterprise_panorama_payload.panorama_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-303` | `—（明细字段）` |
| `capability_ranking_payload.ranking_type` | Radio Group | 内容编辑 | 是 | 技术力 | `—（明细字段）` |
| `capability_ranking_payload.ranking_period` | Input | 内容编辑 | 是 | 2026 年度 | `—（明细字段）` |
| `capability_ranking_payload.evaluation_dimensions` | 可编辑列表 | 专家定义 + 内容编辑 | 是 | 技术成果、研发能力 | `—（明细字段）` |
| `capability_ranking_payload.curated_top30_order` | 拖拽排序表 | 内容编辑人工策展 | 是 | 1. 企业甲；2. 企业乙 | `—（明细字段）` |
| `capability_ranking_payload.evaluation_basis` | TextArea | 专家内容 + 内容编辑 | 是 | 依据公开材料与专家研判 | `—（明细字段）` |
| `capability_ranking_payload.expert_commentary` | TextArea | 专家内容 + 内容编辑 | 否 | 研发组织能力突出 | `—（明细字段）` |
| `capability_ranking_payload.ranking_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-404` | `—（明细字段）` |
| `star_enterprise_intro_payload.representative_narrative` | Rich Text | 内容编辑 | 是 | 代表性企业发展介绍 | `—（明细字段）` |
| `star_enterprise_intro_payload.core_achievements` | 可编辑列表 | 内容编辑 | 是 | 核心材料实现量产 | `—（明细字段）` |
| `star_enterprise_intro_payload.representative_products` | 可编辑列表 | 内容编辑 | 否 | 高性能复合材料 | `—（明细字段）` |
| `star_enterprise_intro_payload.honor_content` | 可编辑列表 | 内容编辑 | 否 | 国家级专精特新 | `—（明细字段）` |
| `star_enterprise_intro_payload.achievement_product_honor_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-505` | `—（明细字段）` |
| `shenzhen_enterprise_intro_payload.regional_positioning` | TextArea | 专家内容 + 内容编辑 | 是 | 深圳新材料链关键企业 | `—（明细字段）` |
| `shenzhen_enterprise_intro_payload.regional_advantages` | TextArea | 专家内容 + 内容编辑 | 是 | 研发与供应链协同优势 | `—（明细字段）` |
| `shenzhen_enterprise_intro_payload.competitiveness_opinion` | TextArea | 专家内容 + 内容编辑 | 否 | 在细分领域具备差异化能力 | `—（明细字段）` |
| `shenzhen_enterprise_intro_payload.regional_narrative` | Rich Text | 内容编辑 | 是 | 立足深圳产业集群持续成长 | `—（明细字段）` |
| `shenzhen_enterprise_intro_payload.regional_media` | Upload + 排序 | 媒体资产引用 + 内容编辑 | 否 | `MEDIA-606` | `—（明细字段）` |

六类 payload 只共享只读 `enterprise_ref` 与可复用 `media_ref`，字段所有权、说明、排序、展示位和版本彼此隔离；切换类型不得复制、覆盖、联动保存或自动同步另一类型 payload。能力榜单的 Top30 只表示人工策展顺序，界面不得展示或暗示算法分、模型得分或自动排名。

### 3.4 交互表

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `save_draft` / 保存草稿 | 仅保存当前 `content_type` payload；成功更新真实 `version`，失败保留全部输入 | 不跨类型保存；不在失败时显示成功或清空输入 |
| `create_draft_from_version` / 从已发布或已下线历史版进入编辑 | 必须携带真实 `source_version_id`，生成独立新草稿；线上 published 指针与历史不变 | 不原位覆盖已发布版；不把 offline 直接改为 published |
| `batch_relation_change` / 批量变更关系描述 | 仅对 `key_enterprise_panorama_payload.descriptive_relationships` 开放；先填原因，再展示前后差异并二次确认，成功写完整审计 | 不生成算法关系、图谱边、关系推断或风险；不对其他类型开放 |
| `submit_for_review` / 提交审核 | 内容完整且无冲突时从 `draft` 进入 `pending_review`；返回 F-OPS-01 原上下文 | 不越过审核进入发布；不在冲突未解决时提交 |
| `submit_master_data_correction` / 发起纠错 | 只提交选定字段与原因；成功必须显示真实 `correction_request_id`、`target: enterprise_master_data_correction_queue`、`status: submitted`、真实 `submitted_at` | 不虚构 API、请求号、时间或成功；不覆盖企业主数据，不把纠错请求混入 CMS payload |
| `—` / 打开门户预览 | 宽屏刷新右栏；`<1280px` 打开预览 Drawer，内容只由当前输入与只读主数据组成 | 不向门户预览暴露审核意见、内部原因、权限或追溯标识 |
| `—` / 返回或取消 | 有未保存输入时先确认；确认后恢复原 `view/type/status/page` | 不静默丢输入，不返回无筛选首页 |

### 3.5 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `default/draft` | 三栏稳定展示；保存与提交按完整性授权 | 编辑当前类型 payload |
| 加载 `loading` | 三栏列宽和标题稳定，局部 Skeleton；底部动作暂时 disabled | 等待或返回原列表 |
| 空 `empty` | 新草稿显示真实空表单与必填引导；主数据缺失单独报错 | 输入内容或发起纠错，不用 Mock 填空 |
| 错误 `error` | 对象加载失败，保留返回入口与错误详情 | 原位重试或回原上下文 |
| 无权限 `no_permission` | 只读说明缺少编辑权限；不渲染可提交动作 | 返回原列表 |
| 只读锁定 `readonly_lock` | 企业主数据控件不可编辑，明确“主数据域提供” | 选择字段并发起纠错 |
| 保存中 `saving` | 保存按钮 loading、防重复提交；输入保持可见但提交审核 disabled | 等待真实结果 |
| 保存成功 `save_success` | 显示真实版本号和保存时间，不清空表单 | 继续编辑或提交审核 |
| 保存失败 `save_failure` | 保持 `draft`、版本和全部本地输入；定位校验/服务错误 | 修正或重试 `save_draft` |
| 已发布与草稿并存 `draft_with_published_version` | 明示线上版本继续服务，当前为独立草稿 | 编辑草稿或打开版本对照 |
| 纠错提交中 `correction_submitting` | 纠错动作 loading，字段和原因保持可见 | 等待真实队列结果 |
| 纠错成功 `correction_submitted` | 展示四个真实结果字段，可按请求号追踪；主数据仍只读且未被自动改正 | 继续编辑 CMS 内容或返回 |
| 纠错失败 `correction_failure` | 不生成请求号，不显示 submitted；保留字段选择和原因 | 重试或保留输入后离开 |

## 4. F-OPS-03 审核详情

**路由**：`/enterprise/content-management/content/:content_id/review?view&type&status&page`

**story_ids**：`[US-ENT-OPS-03]`

**acceptance_ids**：`[ENT-OPS-USM-02, ENT-OPS-USM-06, ENT-OPS-USM-07, ENT-OPS-USM-14]`

**source_relation**：`product_interpretation`

**review_mounts**：`[ENT-OPS-F03-REVIEW-TITLE]`

### 4.1 独立线框

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← 返回审核中心原 type/status/page   审核详情 [review mount: F03 title]       │
│ content_id / content_type / submitter / submitted_at / pending_review        │
├──────────────────────────────┬───────────────────────────────────────────────┤
│ 当前草稿（只读）             │ 对照版本（只读）                              │
│ 字段级差异高亮               │ 来源说明 / 上一发布版或提交基线               │
│ 媒体、排序、文本差异         │ 不允许审核人编辑正文                          │
├──────────────────────────────┴───────────────────────────────────────────────┤
│ 审核意见 [TextArea]                                                        │
│ 自审校验 / 完整性与来源提示                              [退回] [审核通过] │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 内容对象 `content_id` | 文本，只读 | CMS | 是 | `CNT-OPS-1024` | `—（明细字段）` |
| 提交人 `submitter_id` | 用户引用，只读 | 提交审计 | 是 | `USER-EDITOR-08` | `—（明细字段）` |
| 审核人 `reviewer_id` | 用户引用，只读 | 当前登录与授权 | 是 | `USER-REVIEW-03` | `—（明细字段）` |
| 当前草稿 `reviewed_version` | 版本引用，只读 | CMS 版本 | 是 | `VER-0012` | `—（明细字段）` |
| 对照版本 `baseline_version` | 版本引用，只读 | CMS 版本历史 | 否 | `VER-0009` | `—（明细字段）` |
| 字段差异 `field_diff` | Diff，只读 | 当前草稿与对照版本 | 是 | `short_introduction: 修改` | `—（明细字段）` |
| 来源说明 `source_note` | 文本，只读 | 当前类型 payload / 审计 | 按内容类型 | 企业公告 | `—（明细字段）` |
| 审核意见 `review_opinion` | TextArea | 内容审核人工输入 | 退回时是 | 请补充事件来源 | `—（明细字段）` |

### 4.3 交互表

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `approve_review` / 审核通过 | 校验 `reviewer_id != submitter_id`，正文不可变；成功从 `pending_review` 进入 `pending_publish`，记录审计并返回原审核列表 | 不允许自审；不让审核人改正文；不审核后直接发布 |
| `return_from_review` / 退回 | 原因必填，完整审计后回到 `draft`，草稿内容不清空；返回原审核列表 | 不无原因退回，不物理删除提交版本 |
| `—` / 返回 | 恢复进入时的 `view/type/status/page` | 不回无筛选首页 |

### 4.4 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `default/pending_review` | 差异、来源、提交人与审核意见完整，只读正文 | 通过或填写原因退回 |
| 加载 `loading` | 保留双栏标题与底部动作位，差异区 Skeleton | 等待或返回原审核列表 |
| 空 `empty` | 对照版本不存在时明确“首次提交，无历史对照”，仍展示当前草稿 | 继续审核，不用 Mock 版本 |
| 错误 `error` | 差异/对象加载失败，不允许提交审核动作 | 重试或返回原审核列表 |
| 无权限 `no_permission` | 说明缺少审核权限，审核动作不渲染 | 返回仍有权入口 |
| 审核拒绝 `review_rejected` | 自审、状态已变化或服务端拒绝时展示真实原因；不改变正文和原状态 | 刷新状态或返回列表 |

## 5. F-OPS-04 发布确认

**路由**：`/enterprise/content-management/content/:content_id/publish?view&type&status&page`

**story_ids**：`[US-ENT-OPS-04]`

**acceptance_ids**：`[ENT-OPS-USM-02, ENT-OPS-USM-08, ENT-OPS-USM-09, ENT-OPS-USM-14]`

**source_relation**：`product_interpretation`

**review_mounts**：`[ENT-OPS-F04-PUBLISH-RISK]`

### 5.1 独立线框

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← 返回发布中心原 type/status/page    发布确认 / pending_publish              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 发布风险说明 [review mount: F04 publish risk]                                │
│ 内容对象 / 类型 / 已审核版本 / 发布范围 / 门户影响摘要（正文只读）            │
├──────────────────────────────────────────────────────────────────────────────┤
│ 生效方式  (立即发布) (定时发布)     scheduled_effective_at [DatePicker]       │
│ 发布/退回原因 [TextArea]                                                     │
│ □ 我已核对发布范围、生效时间与影响摘要（二次确认）                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ 定时状态说明：计划写入后仍为 pending_publish，system event 激活才 published  │
│                                      [取消] [退回草稿] [确认发布/保存计划]    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 内容对象 `content_id` | 文本，只读 | CMS | 是 | `CNT-OPS-1024` | `—（明细字段）` |
| 待发布版本 `source_version` | 版本引用，只读 | 审核通过结果 | 是 | `VER-0012` | `—（明细字段）` |
| 发布范围 `publish_scope` | Descriptions，只读 | 内容类型与门户映射 | 是 | 企业发展门户 / 明星企业介绍 | `—（明细字段）` |
| 影响摘要 `impact_summary` | 文本，只读 | 当前发布前后差异 | 是 | 替换当前门户介绍文本与 2 张媒体 | `—（明细字段）` |
| 生效方式 `publish_mode` | Radio Group | 发布管理员 | 是 | `scheduled` | `—（明细字段）` |
| 生效时间 `scheduled_effective_at` | DatePicker | 发布管理员 | 定时发布时是 | `2026-07-23 09:00` | `—（明细字段）` |
| 原因 `reason` | TextArea | 发布管理员 | 是 | 配合专题内容更新 | `—（明细字段）` |
| 二次确认 `second_confirmation` | Checkbox | 发布管理员 | 发布动作是 | `true` | `—（明细字段）` |

### 5.3 交互表

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `immediate_publish` / 确认立即发布 | 原因和二次确认必填；真实成功后生成新 published 版本、更新门户指针并完整审计 | 不绕过审核；不提前显示 published；发布管理员不改正文 |
| `schedule_publish` / 保存定时计划 | 写入真实 `scheduled_effective_at` 与审计，状态保持 `pending_publish` | 不把“计划已保存”表达为“已发布” |
| `scheduled_publish_activate` / 到时系统事件 | 仅系统事件且到达计划时间、计划未取消时执行；真实成功后转 `published` 并审计 | 不提供人工按钮冒充 system event；失败不伪造 published |
| `return_from_publish` / 退回草稿 | 原因必填，完整审计后回 `draft`，保留内容；返回原发布列表 | 不无原因退回，不清空草稿 |
| `—` / 取消或返回 | 恢复原 `view/type/status/page`，保留未提交原因和时间需先确认 | 不静默丢输入 |

### 5.4 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `default/pending_publish` | 显示范围、时间、影响、原因与二次确认，正文只读 | 立即、定时或退回 |
| 加载 `loading` | 保留风险区和表单结构，内容 Skeleton，动作 disabled | 等待或返回原发布列表 |
| 空 `empty` | 无可发布版本时说明状态已变化，不填充版本 | 刷新或返回原发布列表 |
| 错误 `error` | 对象/影响摘要加载失败，发布动作 disabled | 原位重试 |
| 无权限 `no_permission` | 显示缺少发布管理权限；不渲染发布动作 | 返回仍有权入口 |
| 发布中 `publishing` | 目标按钮 loading、防重复提交；原因、时间仍可见 | 等待真实结果 |
| 发布失败 `publish_failure` | 保持原 `pending_publish`、原因、时间和输入；不显示成功审计 | 修正后重试或退回 |
| 定时待激活 `pending_publish` | 显示已保存计划与计划时间；仍明确“待发布” | 等待 `scheduled_publish_activate` 或按权限调整 |
| 定时激活失败 | 保持 `pending_publish`，显示真实激活错误与计划时间 | 查看审计并重试/调整计划，不补写成功 |

## 6. F-OPS-05 版本与审计

**路由**：`/enterprise/content-management/content/:content_id/versions?view&type&status&page`

**story_ids**：`[US-ENT-OPS-05]`

**acceptance_ids**：`[ENT-OPS-USM-02, ENT-OPS-USM-10, ENT-OPS-USM-11, ENT-OPS-USM-12, ENT-OPS-USM-14]`

**source_relation**：`product_interpretation`

**review_mounts**：`[ENT-OPS-F05-VERSION-AUDIT-TITLE]`

### 6.1 独立线框

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← 返回原 view/type/status/page   版本与审计 [review mount: F05 title]         │
│ content_id / content_type / 当前线上版本 / 当前流程状态                       │
├────────────────────────────┬─────────────────────────────────────────────────┤
│ 版本时间线                 │ 选中版本详情与前后差异                          │
│ ● v12 published 当前线上   │ 操作人 / 操作时间 / action_id / 原因            │
│ │ v11 pending_publish      │ 审计 payload / 来源版本 / 新版本                │
│ ● v10 offline              │ 发布影响 / 下线影响 / 回滚前后差异              │
│ │ v09 published            │                                                 │
├────────────────────────────┴─────────────────────────────────────────────────┤
│ 角色动作区：publishing_admin [下线] [回滚为新发布版]                          │
│             content_editor  [从此版本生成草稿]                               │
│ 禁止交叉授权；历史与审计不可物理删除                                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 版本标识 `version_id` | 文本，只读 | CMS 版本历史 | 是 | `VER-0012` | `—（明细字段）` |
| 版本状态 `version_state` | Tag，只读 | 工作流历史 | 是 | `published` | `—（明细字段）` |
| 来源版本 `source_version_id` | 版本引用，只读/动作输入 | CMS 版本历史 | 从历史动作时是 | `VER-0009` | `—（明细字段）` |
| 操作标识 `action_id` | 文本，只读 | 审计链 | 是 | `rollback_as_new_published_version` | `—（明细字段）` |
| 操作人 `operator_id` | 用户引用，只读 | 审计链 | 是 | `USER-PUBLISH-02` | `—（明细字段）` |
| 操作时间 `operated_at` | 日期时间，只读 | 审计链 | 是 | `2026-07-22 16:20` | `—（明细字段）` |
| 原因 `reason` | TextArea / 审计只读字段 | 当前操作者 / 历史审计 | 高风险动作是 | 更正门户错误内容 | `—（明细字段）` |
| 前后差异 `before_after_diff` | Diff，只读 | 目标历史版与当前线上版 | 回滚时是 | 简介与媒体排序变化 | `—（明细字段）` |
| 影响摘要 `impact_summary` | 文本，只读 | 当前线上与目标动作 | 下线时是 | 门户停止展示该内容 | `—（明细字段）` |
| 二次确认 `second_confirmation` | Checkbox | 当前操作者 | 下线/回滚时是 | `true` | `—（明细字段）` |

### 6.3 action_actor_map 与交互表

```yaml
action_actor_map:
  publishing_admin: [take_offline, rollback_as_new_published_version]
  content_editor: [create_draft_from_version]
```

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `take_offline` / 发布管理员下线当前 published | 原因、影响摘要和二次确认必填；成功转 `offline`，门户停止消费指针，历史与审计保留 | 内容编辑不可执行；不物理删除版本；不由 offline 直接恢复 published |
| `rollback_as_new_published_version` / 发布管理员选择历史发布版回滚 | 展示前后差异，原因和二次确认必填；成功生成新的 published 版本并完整审计 | 内容编辑不可执行；不倒写、覆盖或删除历史 |
| `create_draft_from_version` / 内容编辑从 published 或 offline 历史版生成草稿 | 必须传 `source_version_id`；生成独立 draft 后进入 F-OPS-02，并透传列表上下文 | 发布管理员不可执行；不让 offline 直接上线；不覆盖来源版本 |
| `—` / 查看版本或审计 | 选择时间线节点只刷新右侧详情，保留滚动和选中项 | 不提供物理删除入口，不修改审计记录 |
| `—` / 返回 | 恢复原 `view/type/status/page` | 不回无筛选首页 |

### 6.4 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `default/published` | 当前线上版、历史时间线、审计详情和角色动作清晰 | 按角色查看或执行治理动作 |
| 加载 `loading` | 保留时间线与详情列宽，局部 Skeleton，动作 disabled | 等待或返回原列表 |
| 空 `empty` | 无历史版本时显示真实空态；不伪造发布时间线 | 返回或从有权入口创建内容 |
| 错误 `error` | 历史/审计加载失败，不允许高风险动作 | 原位重试 |
| 无权限 `no_permission` | 可解释缺少版本/治理权限；不渲染越权动作 | 返回仍有权入口 |
| 已下线 `offline` | 明示门户已停止消费，保留历史版；只允许编辑从版本生成草稿 | 按新草稿重新走审核发布链 |
| 从历史生成草稿 `create_draft_from_history` | 显示来源版本与新草稿真实标识，随后进入 F-OPS-02 | 编辑新草稿；不可直接上线 |
| 下线/回滚失败 | 保持原 published 状态与用户填写原因，不写成功审计 | 重试或取消 |

## 7. F-OPS-06 冲突处理

**路由**：`/enterprise/content-management/content/:content_id/edit?view&type&status&page&state=conflict`

**story_ids**：`[US-ENT-OPS-06]`

**acceptance_ids**：`[ENT-OPS-USM-13, ENT-OPS-USM-14]`

**source_relation**：`product_interpretation`

**review_mounts**：`[ENT-OPS-F06-CONFLICT-TITLE]`

### 7.1 独立线框

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ 冲突处理 [review mount: F06 title]   content_id / 本地 version / 服务端 version│
├──────────────────────────────┬───────────────────────────────────────────────┤
│ 本地未保存输入（完整保留）   │ 服务端新版本（只读）                          │
│ 字段、媒体、排序             │ 字段、媒体、排序                              │
│ 本地变更标记                 │ 他人变更标记 / 操作时间                       │
├──────────────────────────────┴───────────────────────────────────────────────┤
│ 字段级解决选择：保留本地 / 采用服务端 / 手动编辑                             │
│ 当前差异未全部解决时“重新保存”disabled                                      │
│                               [返回编辑器且保留输入] [刷新比较] [重新保存]    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 内容对象 `content_id` | 文本，只读 | CMS | 是 | `CNT-OPS-1024` | `—（明细字段）` |
| 本地版本 `local_version` | 版本号，只读 | 编辑器当前上下文 | 是 | `12` | `—（明细字段）` |
| 服务端版本 `server_version` | 版本号，只读 | 冲突响应 | 是 | `13` | `—（明细字段）` |
| 本地 payload `local_payload` | Diff 左栏，可编辑解决 | F-OPS-02 未保存输入 | 是 | `short_introduction: 本地文本` | `—（明细字段）` |
| 服务端 payload `server_payload` | Diff 右栏，只读 | CMS 最新版本 | 是 | `short_introduction: 他人文本` | `—（明细字段）` |
| 冲突字段 `conflict_fields` | 字段列表 | 本地/服务端差异计算 | 是 | `[short_introduction]` | `—（明细字段）` |
| 解决策略 `resolution` | Radio / 手动编辑 | 内容编辑 | 每个冲突字段是 | `keep_local` | `—（明细字段）` |

### 7.3 交互表

| action_id / 触发 | 结果 | 禁止 |
| --- | --- | --- |
| `save_draft` / 解决全部差异后重新保存 | 使用最新服务端版本作乐观锁基线，仅保存当前类型已解决 payload；成功回 F-OPS-02 同一对象 | 不强制覆盖；不跨类型保存；不在差异未解决时提交 |
| `—` / 刷新比较 | 获取真实服务端最新版本并重新计算差异，本地输入继续完整保留 | 不用刷新清空本地输入，不自动选用任一侧 |
| `—` / 返回编辑器 | 回到 F-OPS-02 同一 `content_id` 与完整 `view/type/status/page`，保留当前输入和冲突提示 | 不创建新对象，不跳到列表首页 |

### 7.4 状态表

| 状态 | 表现 | 用户下一步 / 返回上下文 |
| --- | --- | --- |
| 默认 `conflict_detected` | 明确冲突原因、两个版本号，本地输入完整可见 | 刷新比较 |
| 加载 `loading` | 双栏尺寸稳定，服务端栏 Skeleton，本地栏保持可见 | 等待真实服务端版本 |
| 空 `empty` | 若刷新后无差异，明确“冲突已消失”，仍保留本地输入 | 返回编辑器再次保存 |
| 错误 `error` | 服务端版本加载失败，本地输入可见且不可提交 | 重试或返回编辑器 |
| 无权限 `no_permission` | 权限在冲突期间失效时保留输入快照并说明不可保存 | 返回有权入口；不得假成功 |
| 对比 `compare_server_and_local` | 字段级显示本地/服务端差异与解决选择 | 逐项解决 |
| 重存 `resaving` | 按钮 loading、防重复提交；双栏不消失 | 等待真实保存结果 |
| 保存失败 `save_failure` | 保留解决结果与本地输入，显示真实失败原因 | 重试 `save_draft` |

## 8. 13 个 TRACE action 落位

| action_id | actor | Frame | 关键状态结果 | 禁止边界 |
| --- | --- | --- | --- | --- |
| `save_draft` | `content_editor` | F-OPS-02；冲突重存落 F-OPS-06 | `draft → draft` | 失败不清空，冲突不强制覆盖 |
| `create_draft_from_version` | `content_editor` | F-OPS-05 发起，F-OPS-02 承接编辑 | `published/offline → draft` | 发布管理员不可执行；不覆盖来源版本 |
| `submit_for_review` | `content_editor` | F-OPS-02 | `draft → pending_review` | 内容不完整或冲突未解决不得提交 |
| `approve_review` | `content_reviewer` | F-OPS-03 | `pending_review → pending_publish` | 不自审、不改正文 |
| `return_from_review` | `content_reviewer` | F-OPS-03 | `pending_review → draft` | 原因必填，内容不清空 |
| `immediate_publish` | `publishing_admin` | F-OPS-04 | `pending_publish → published` | 不提前展示成功 |
| `schedule_publish` | `publishing_admin` | F-OPS-04 | `pending_publish → pending_publish`，写计划时间 | 计划写入不等于发布 |
| `scheduled_publish_activate` | `system_event` | F-OPS-04 | 到时真实成功才 `pending_publish → published` | 无人工入口，不伪造 system event |
| `return_from_publish` | `publishing_admin` | F-OPS-04 | `pending_publish → draft` | 原因必填，不改正文 |
| `take_offline` | `publishing_admin` | F-OPS-05 | `published → offline` | 不物理删除，不由内容编辑执行 |
| `rollback_as_new_published_version` | `publishing_admin` | F-OPS-05 | `published → 新 published 版本` | 不倒写或覆盖历史 |
| `batch_relation_change` | `content_editor` | F-OPS-02 | `draft → draft` | 仅人工 `descriptive_relationships`，非算法图谱 |
| `submit_master_data_correction` | `content_editor` | F-OPS-02 | `draft → draft`，逻辑交接纠错队列 | 不改主数据，不虚构 API 或结果 |

## 9. review_trace_contract

评审挂载只用于内部需求追溯。业务模式的挂载数量为 0；切换评审/业务模式不得改变业务字段、值、权限、流程、按钮可用性或持久化 payload。挂载标记不得放在 input label、按钮、表格单元格、状态 Tag 或 Modal 主按钮上；也不得作为焦点目标替代业务宿主。允许宿主仅为本契约登记的稳定页面/区块标题，Popover/注解 payload 必须完整来自追溯数据。

```yaml
review_trace_contract:
  - mount_id: ENT-OPS-F01-WORKBENCH-TITLE
    frame_id: F-OPS-01
    host_label: 内容工作台标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-37]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: workbench
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F02-EDITOR-TITLE
    frame_id: F-OPS-02
    host_label: 内容编辑器标题
    marker_type: requirement_trace
    source_relation: direct_requirement
    trace_refs: [E-37, IA-ENT-OPS-CAP-01, IA-ENT-OPS-CAP-02, IA-ENT-OPS-CAP-03, IA-ENT-OPS-CAP-04, IA-ENT-OPS-CAP-05, IA-ENT-OPS-CAP-06]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: draft
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F02-MASTER-DATA-BOUNDARY
    frame_id: F-OPS-02
    host_label: 企业主数据只读区标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [PI-ENT-OPS-02, PI-ENT-OPS-06]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: readonly_lock
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F03-REVIEW-TITLE
    frame_id: F-OPS-03
    host_label: 审核详情标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [PI-ENT-OPS-01]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: pending_review
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F04-PUBLISH-RISK
    frame_id: F-OPS-04
    host_label: 发布风险说明区标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [PI-ENT-OPS-01, PI-ENT-OPS-05]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: pending_publish
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F05-VERSION-AUDIT-TITLE
    frame_id: F-OPS-05
    host_label: 版本与审计标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [PI-ENT-OPS-05]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: published
    review_mode: present
    business_mode: absent
  - mount_id: ENT-OPS-F06-CONFLICT-TITLE
    frame_id: F-OPS-06
    host_label: 冲突处理标题
    marker_type: review_copy
    source_relation: product_interpretation
    trace_refs: [PI-ENT-OPS-05]
    required_payload: [source_location, source_summary, current_placement, source_relation]
    route_state: conflict_detected
    review_mode: present
    business_mode: absent
```

## 10. 响应式、组件与视觉约束

- **屏幕层级**：仅 `medium`。Track-MS 中屏实现，不把 viewport 宽度解释为 LARGE 或 SMALL 交付物；LARGE / SMALL 均无菜单、快捷入口或深链入口。
- **Shell**：使用 `Layout + Header + Sidebar + Content`；顶部与左侧导航是定制结构并保留 Arco 菜单语义。`<1440px` 时 Sidebar 从 `200px` 折叠到 `64px`，内容区重排但不产生 SMALL 维护入口。
- **F-OPS-02**：`>=1280px` 保持“主数据只读 / CMS 分型表单 / 门户预览”三栏；`<1280px` 仅把预览改为 Arco Drawer，中栏输入和返回上下文不变。
- **视觉 token**：页面背景 `#D8E7FC`，主色 `#165DFF`，中文正文和表单标签 `14px`，按钮/输入/筛选/分页常用高度 `32px`；使用浅色蓝白工作台，不使用暗色、霓虹、紫蓝渐变或发光效果。
- **组件**：Button、Input、Select、DatePicker、Tag、Drawer、Modal、Table、Pagination、Tooltip、Popover、Skeleton、Empty、Alert 优先用 `@arco-design/web-react`；不引入 `antd`，不使用 native select，不用 emoji 充当业务图标。
- **复合 label 安全**：不得用原生 `<label>` 包裹 Arco Select、Cascader、DatePicker、TreeSelect 或 AutoComplete。使用 `Form.Item`，或将可见标签与控件作为兄弟节点并用 `aria-labelledby` 关联，避免双激活使弹层立即关闭。
- **稳定状态**：selected、hover、focus-visible、disabled、loading、error 沿用 Arco 语义；focus-visible 保留主蓝焦点环；disabled 保留布局并说明原因；loading 局部呈现且不重置筛选、输入、分页或容器尺寸。
- **危险动作**：原因、影响/差异和二次确认必须在提交前可见；Modal 主按钮只承载业务确认，不承载评审追溯挂载。

## 11. 全局状态与失败保真

| 状态类别 | 全局契约 |
| --- | --- |
| 默认 | 只展示真实授权、真实流程状态和真实业务字段；业务模式无任何评审挂载 |
| 加载 | 保留标题、筛选、表头、表单列宽、底部动作和容器尺寸；局部 Skeleton/Spin |
| 空 | 说明真实空因和下一步，不用 Mock 数据、假版本、假请求号或占位业务行填充 |
| 错误 | 显示真实失败范围与重试入口；对象、列表、差异、预览失败彼此隔离 |
| 无权限 | 保留节点与原因说明；不只隐藏按钮，不因前端隐藏替代服务端授权 |
| 保存失败 | 保持草稿、版本基线与全部输入，不显示成功，不提前切换状态 |
| 发布失败 | 保持 `pending_publish`、原因、生效时间与全部输入，不生成 published 或成功审计 |
| 审核退回 | 原因必填并完整审计，返回 `draft`，内容不清空 |
| 定时未激活 | 保持 `pending_publish` 和计划时间；只有真实 system event 成功才转 published |
| 冲突 | 完整保留本地输入，真实比较服务端新版本，解决后再保存，不强制覆盖 |
| 纠错失败 | 保留字段与原因，不生成 `correction_request_id`、submitted 状态或虚假时间 |

## 12. 明确排除项

- 企业工商、统一社会信用代码、成立时间、资质、专利、财务等主数据写入或主数据管理。
- 技术力、商业力、竞争力算法评分、算法关系、图谱推断、风险计算、自动榜单或自动发布。
- KPI、数量卡、统计指标及其趋势表达。
- 企业搜索、分析、推荐、对比、导出等应用侧能力。
- 用户、角色、权限、数据源或知识图谱的系统级管理。
- LARGE 大屏或 SMALL 小屏维护入口。
- 物理删除已发布内容、版本历史或审计记录。
- 向门户暴露草稿、已下线内容、审核意见、内部原因、权限规则或评审挂载。
- 假成功、失败时丢输入、用 Mock 内容填空、虚构接口或纠错结果。

## 13. 指标、开放项与阻断缺口

```yaml
metrics:
  applicability: N/A
  reason: CMS内容与人工策展顺序均为业务明细，不是统计指标
  required: 0
  mapped: 0
  metric_ids: []
open_questions: []
blocking_gaps: []
```

## 14. Typed handoff source inventories

```yaml
original_requirement_sources:
  - file: agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
    sections:
      - "1.1.1.2.4.5.6.3 企业发展内容管理"
      - "1.1.1.2.4.5.6.3.1 企业基础与成长内容维护"
      - "1.1.1.2.4.5.6.3.2 重点企业与竞争力榜单维护"
      - "1.1.1.2.4.5.6.3.3 明星企业与深圳企业介绍维护"
    authority: original_requirement
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
    status: current
supplemental_constraint_sources:
  - file: agent-delivery/Design.md
    role: medium shell、Arco 组件与视觉约束，不创造业务需求
  - file: agent-delivery/data-lineage-policy.md
    role: review trace 挂载治理，不创造业务需求
  - file: agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md
    role: 交互状态、上下文保留与可访问性约束，不创造业务需求
```

## 15. Wireframe 自检

- [x] 恰有 F-OPS-01～F-OPS-06 共 6 个唯一 Frame，每个都有独立 ASCII 线框、六列字段表、交互表、状态表和显式 `review_mounts`。
- [x] F-OPS-01 在一个 Frame 内定义 root、editor、review、publish 四个 route variant 列表态；F-OPS-02 为三栏且在 `<1280px` 只把预览重排为 Drawer。
- [x] 7 个 `mount_id` 唯一，逐一落在稳定标题宿主；F-OPS-02 恰有两个挂载，其余 Frame 各一个；评审模式 `present`、业务模式 `absent`，业务影响为 0。
- [x] `save_draft`、`create_draft_from_version`、`submit_for_review`、`approve_review`、`return_from_review`、`immediate_publish`、`schedule_publish`、`scheduled_publish_activate`、`return_from_publish`、`take_offline`、`rollback_as_new_published_version`、`batch_relation_change`、`submit_master_data_correction` 共 13 个 TRACE action 均落在正确 Frame 与角色。
- [x] `ENT-OPS-USM-01`～`ENT-OPS-USM-14` 共 14 条验收均被 Frame 引用；`US-ENT-OPS-01`～`US-ENT-OPS-07` 共 7 个故事均有落点。
- [x] 企业主数据只读；纠错只显示真实队列结果；六类 payload 的 `field_id` 严格隔离；人工榜单无算法分；批量关系变更只维护描述性文本且需原因、二次确认和完整审计。
- [x] 立即发布、定时发布、系统激活与发布退回边界清晰；定时计划写入后保持 `pending_publish`，只有真实 system event 激活才进入 `published`。
- [x] F-OPS-05 明确 `action_actor_map`：发布管理员下线/回滚，内容编辑从历史生成草稿；任何交叉授权均被禁止。
- [x] 所有业务字段均为 `—（明细字段）`；`metrics: N/A`、`required: 0`、`mapped: 0`，无 KPI 或数量卡。
- [x] 默认、加载、空、错误、无权限、保存失败、发布失败、审核退回、定时未激活、纠错失败、下线/回滚失败与并发冲突均保留真实状态和用户输入。
- [x] 返回上下文统一使用 `view/type/status/page`；未引入主数据写入、算法评分、自动榜单、分析推荐导出、角色管理、物理删除历史、假成功、丢输入或 Mock 填空。
- [x] `open_questions: []`、`blocking_gaps: []`；本文不宣告 PDR 闭合，不声明实际交付 Tier。
