# TS-L2-M10-ENT-API · 维护管理 · 关键实体与关系 · 后台接口设计

- 任务：`TS-L2-M10-ENT-API`
- 日期：2026-11-07
- 状态：四角色会签完成（API 1+DATA 3+ARCH 4+ALGO 同意，条件全部回填），**待监管人签收**。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 41–47
- 上游：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（done，含 C1 裁定 A：display 代理）
- 会签输入：`会签/TS-L2-M10-ENT-SIGNOFF-API.md`（读端点 R1–R6/op 冻结 5 条/错误模型 3 项）

本分册只定 M10「关键实体与关系」的后台接口。**对外走 display 代理**（C1 裁定 A，监管人 2026-11-07）：`/display/v1/situation/maintain-ent/graph/**`（display ENT 门面 → Feign → topic 侧 `/topic/v1/tech/graph/**`）。op 枚举唯一上游=SCI-INT-A03（消费注记在册）。不写实现代码。

签收口径：写操作全走 changes 端点（ops[] 封闭枚举 7 个）；读操作 6 端点；乐观锁 409+差异列表；发布失败 projection_pending 可见。接口不返回内存 mock；105 未交付时空态+PendingBadge（不灌 mock 充数）。

## 0. 与 as-built 差异表（接线单输入）

| 项 | as-built（FE-TS-10A 演示态） | 本分册契约 | 接线单动作 |
|---|---|---|---|
| 数据源 | 页面内存纯函数 11 个 | 读端点 R1–R6 + changes 写链 | api 层新增 maintain-ent 模块 |
| 推荐列表 | 种子 5 条静态 | R1 服务端（keyword/sortBy 全参数） | 换数据源 |
| 添加全景图 | 本地 push + 自动建联观感 | hang_entities op（G2 首版不自动建联，SRS 42 缺口**待 PM 登记**——三分册会签 ARCH-A2 核实跟踪表暂无此条） | 去掉自动建联演示逻辑 |
| 关系新增 | `addPanoramaRelation` 纯函数 | **显式放弃**（A03/SRS 41–47 无此叶；demo 超需规，会签 API 备注 5） | 移除入口或留空态 |
| notice 文案 | 「（Mock）」遍布 | 真轨 mock 文案清除（随接线单，同分区1 先例） | 双轨感知 |
| 页级操作反馈 | 即时 notice | 提交回执（change_set 状态+failed_items） | 状态机化 |

## 1. 总则

对外前缀 `/display/v1/situation/maintain-ent/`（display ENT 门面：鉴权/校验/Feign；沿 LAYER 门面模式）。内部委托 topic 侧 `/topic/v1/tech/graph/**`（DN-07 模块落点实现单定；网关 dev 配置「前端禁止直连 topic」注释随实现补豁免说明——现前端不直连，冲突消）。

- 全同步 HTTP（发布为同步触发、异步投影：见 §6 错误模型）
- 幂等：`client_op_id` 每 op 必带（从 A03 add_node 扩展到全部 op，重试安全）
- 乐观锁：所有写请求带 `base_version`；不匹配 → 409 + 差异列表（§6）
- `ops[]` 单批上限 **50**（超限 400；A03 INT-A-X-221 gap 收口）；部分失败语义沿 A03：failed_items 清单+版本 stats 只计成功
- traceId 沿展示链贯穿 change_log

## 2. op 枚举与请求形状（会签 API-C1 更正后冻结）

本叶收 **7 op**（A03 十 op 中属 41–47 者；`add_node/add_edge/delete_edge` 属 34–40 不收）：

| op | 叶 | 请求要点（A03 卡出处） |
|---|---|---|
| `hang_entities` | 42 | `[base_version, technology_id, entities[(entity_type, entity_id)], client_op_id]`；回执 edges_created[].strength 复用 105 快照边权（ALGO 边界 1） |
| `unhang_entities` | 43 | `[base_version, technology_ids[], entity_ids[], cascade, client_op_id]`（A03:883 原文 technology_id 单数，分册扩复数批量——三分册会签注记）；cascade 语义含 SRS-43「所有关系」（会签 API 备注 3） |
| `delete_node` | 43（技术点本体） | `[base_version, technology_ids[], cascade, client_op_id]`；前置 impact 预检（R3）（**2026-11-10 监管人 human:刘剑锋 裁定**：需规 41 推荐仅人/机构/论文/专利、43「保留在推荐列表以便重新添加」，技术点删除原文归需规 35 维护技术图谱——本页前端**不发** delete_node，技术点行不可勾选；后端 op 与 impact 保留待 34–40） |
| `update_node` | 45（技术点） | `[base_version, technology_id, patch(name_cn, category, description, importance_level), client_op_id]` |
| `update_entity_overlay` | 45（三方实体） | `[base_version, entity_type, entity_id, patch(display_name, type, description, importance_level), client_op_id]`——与 update_node 形状不同，**不得混用**（API-C1） |
| `delete_entity_edge` | 44 | `[base_version, edge_key, client_op_id]`；edge_key=(src,dst,rel_type,rank)（A03 INT-A-TECH-204）；回执带 edge_source(auto\|manual) |
| `update_entity_edge` | 46 | `[base_version, edge_key, patch(rel_type, strength_manual, time_range), client_op_id]`；time_range 年粒度（A03 granularity）；G1 强度/时间在此（A03 草案已含） |

`technology_id` 类型冻 **INT64**（自建主表先行档即可定，会签建议）；`entity_id` 对齐 C01/C03/C02 主数据（在册，分册注记不锁）。

## 3. 读端点（R1–R6，会签核对三）

| # | 端点 | 语义 | 备注 |
|---|---|---|---|
| R1 | `GET …/nodes/{technology_id}/recommend-entities` | 推荐 Top 实体（叶 41）：keyword 筛选 + sortBy=strength\|time\|name（A03 卡 **213** L711；路径资源段与三值系三分册会签 ARCH-A1/API-条件1 补正） | 强度展示数字挂 `M_TECH_GRAPH_105_1`（METRIC 册）；105 未交付→空态+PendingBadge |
| R2 | `GET …/graph/current` | **全景现状读**（会签必答题 1）：当前 published 图（技术点+挂接实体+边），含 projection_status | A03 无卡、ARCH 提出无路径——本分册新定；差异列表/版本信息挂此 |
| R3 | `GET …/nodes/{technology_id}/impact` | 删除影响预检：edge_count/entity_link_count/snapshot_refs | 计数豁免归 DN-A03-09（METRIC 册裁定） |
| R4 | `POST …/changes:validate` | 预览（dry_run）：返回 diff+影响面+计数 | A03 两形态（:validate/dry_run）归一本形态（DATA 会签 §6 同裁） |
| R5 | `POST …/changes/{change_set_id}/publish` | **发布动作落点**（会签必答题 2）：独立端点触发发布 | A03 挂 versions 端点与 ARCH 暗示 changes 自带两说不一——本分册裁定独立发布端点（语义清晰、可重试、审计独立）；「提交即发布」捷径不做 |
| R6 | `GET …/conflicts` | 冲突队列读（reserved 首版空实现） | DN-A03-03 在册；端点占位防后续破坏性变更 |

写端点两个：`POST …/changes`（提交 ops[] → change_set status=draft）、`GET …/changes/{id}`（回执/状态查询）。

## 4. DTO 概要

- RecommendEntity：entity_id/entity_type/display_name/strength(**105 边权**)/year/description（description 沿 demo 在用形状，会签 API 备注 2）
- GraphCurrent：technology_id/name_cn/category/importance_level/entities[](overlay 已套用)/edges[](edge_key,rel_type,strength_auto,strength_manual,source,time_range)/base_version/projection_status
- ChangeSetReceipt：change_set_id/status/failed_items[]/version_stats{succeeded}
- ImpactResult/ValidatePreview/DiffList：字段沿 A03 202/221/204

**边强度双字段**（ALGO 保护条款落 DTO）：`strength_auto` / `strength_manual` / `source` 三列贯穿读写——UI 可显人工值但须**标注「人工」**（METRIC §3.2），读面指标口径只取 auto。

## 5. 错误码汇总

| 码 | 场景 |
|---|---|
| `400 PARAM_INVALID` | op 枚举外/缺 base_version/ops>50/edge_key 形状错/technology_id 非法 |
| `404 NOT_FOUND` | change_set/technology_id 不存在 |
| `409 VERSION_CONFLICT` | base_version 不匹配——data 带 diff 列表（双方 ops 对照）；另 `409 CHANGE_SET_STATE`（published/rejected 态再发布——draft/approved 可发布，三分册会签 ARCH-A3 更正原「非 draft」措辞） |
| `422 UNPROCESSABLE` | validate 发现的图结构违规（悬挂边/类型不匹配；含 edge_key/entity_id 不存在的图结构类归此）。平台先例：Python 内部已用 422、Java 门面已消费（SvcAnalysisAdapterImpl/IndustryFacadeServiceImpl）——display 门面须透传（三分册会签 API 备注） |
| `503 PROJECTION_PENDING` | 发布投影中——**读 R2 仍可用**（返回上一版+projection_status=pending），写可继续提交（base_version 不变） |

空态=200 空列表（R1 无推荐/R6 无冲突），不是 501 不是 404。无 mock 兜底端点。

## 6. 状态机与发布语义

`draft →（可选 approve，DN-A03-02）→ published`（ARCH 图已按 DATA 会签改为 approve 可选）。发布单事务语义+失败补偿沿 ARCH §1（**发布序列三分册会签 ARCH-A4 锁定：MySQL 先提交 → Nebula 投影 → ADS 投影最后**——ADS 与 Nebula 同段失败同补偿，R2 恒读上一已发布版，无需 pending 版过滤；DATA 册 §4 已同步）；projection_status 枚举（ok/pending/failed）经 R2 暴露。pending 期间提交照常受理（新 change_set 基于 MySQL 已提交版本）。

## 7. 不做

- 不写实现代码；不做 G2 现算（无 105 边对强度空，产品口径在册）；不收 34–40 的 3 op
- 不做审核流引擎（DN-A03-02 未决，status 字段留位）
- 不做合并/拆分 redirect（首版查重命中只提示「仍新建」，DATA 册同步裁定）
- 不做 conflicts 实际逻辑（reserved）
- 不新造 metric_id（叶 41 沿 M_TECH_GRAPH_105_1，METRIC 册）

## 增量 2026-11-11（TS-L2-M10-DEMO-FULL-L01，以实现为准）

真源：`agent-handoffs/科技发展态势-TS/TS-L2-M10-DEMO-FULL-L01-方案.md` §2.1。要点：

- R1 `recommend-entities` 新增 `entityType`（含中文别名）、`yearFrom` / `yearTo`、`page` / `size`（默认 20，最大 100）；`keyword` 改为服务端过滤，不区分大小写。返回 `{items,total,page,size}`，排除该技术点的成员实体。
- 挂接状态改由 ADS `graph_entity_member` 表达（含挂接时 `snapshot_strength` / `snapshot_time_to`），与边解耦：
  - `delete_entity_edge` 只删边，两端实体保留。
  - `unhang_entities` 删成员与人工边，按快照回写候选边。
  - 成员表缺失时回退旧语义。
- R2 节点增加 `description`；实体 `entity_type` 为生效类型（overlay `type` 覆盖）。
- `update_entity_overlay.patch.type` 生效（person / institution / paper / patent）；`update_entity_edge.strength_manual` 限 0–10，`time_range.from ≤ to`。
- `changes:validate` 改为结构与存在性校验：违例返回 422 / 42201 + `errors[]`；通过时返回 `summary` 与中文 `preview[].desc`。`POST /changes` 提交前跑同一套校验。
- `publish` 返回 `results{succeeded,failed,failed_items}`；`impact` 对不存在的技术点返回 404 / 40401。
- display 写入口（changes / validate / publish）要求登录：开关 `gkxlumen.maintain.write-require-login` 默认 true，未登录返回 401 / 40101。
