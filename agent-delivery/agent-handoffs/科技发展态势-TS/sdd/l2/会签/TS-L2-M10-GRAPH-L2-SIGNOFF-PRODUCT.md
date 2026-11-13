# TS-L2-M10-GRAPH-L2-SIGNOFF-PRODUCT · 产品会签（API / DATA / METRIC 三份二级分册）

- 角色：`agent:product-agent`
- 日期：2026-11-13
- 会签对象：
  - `sdd/l2/TS-L2-M10-GRAPH-API.md`（草稿 v1）
  - `sdd/l2/TS-L2-M10-GRAPH-DATA.md`（草稿 v1）
  - `sdd/l2/TS-L2-M10-GRAPH-METRIC.md`（草稿 v1）
- 基准：`sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（v2，2026-11-13 监管人 `human:刘剑锋` 签收）§6 功能点表、§7 状态与错误、§11 末尾「拍板结果」
- 监管：`human:刘剑锋`
- 边界：只读审稿；只写本文件；不改被审稿、其他文件、`task-registry`；不 git、不连库
- 方法：以 SRS 34–40 原文与 ARCH §6「界面必见」为验收面，逐项核对三份分册；对起草方留给产品的 5 个点直接给结论；对英文码、错误提示、历史数据兼容、影响清单做产品侧补齐。证据中的 `API:` / `DATA:` / `METRIC:` / `ARCH:` 均指本目录同名分册行号。

## 0. 结论

| 分册 | 结论 | 必修 | 建议 |
|---|---|---|---|
| API | **有条件同意** | 8 | 5 |
| DATA | **有条件同意** | 4 | 4 |
| METRIC | **有条件同意** | 3 | 4 |

一句话：三份分册已把 34–40 的接口、数据、指标边界写到可实现粒度，ARCH §6 的 27 个功能点与 2 个横切均有落点；但「界面必见」的中文化、错误/状态提示、历史版本兼容、回滚确认文案仍有产品缺口。下列必修项闭合后可签收，建议项不阻断派单但应写入实现单。

### 0.1 对 ARCH §11「拍板结果」的落实核对

| 拍板项 | 分册落实 | 判定 |
|---|---|---|
| P2 人工关系只给 包含 / 依赖 / 促进，枚举可扩展；前端删「转化 / 关联」 | API §2.2 三枚举、§8.1 删两项 | ✓；「可扩展」的实现方式见 PROD-API-C8 附注 |
| 停机确认①：删 Nebula 投影，发布 / 回滚改加锁单事务 | API §3.3、§9-E9/E10；DATA §5.1、§5.2、§11-1/2 | ✓ |
| 停机确认②：名称唯一键只约束 active；DDL 备份；Owner 确认在 DATA 标出 | API §2.4；DATA §3.2、§10、§12-3 | ✓；Owner 书面确认仍待闭环（见 §6） |
| P4：全景页非阻塞提示「人工维护的改动暂未显示，请稍后刷新」；知会 DS02 监管人 | API §5.3；DATA §7.2 | ✓；知会回执仍待闭环（见 §6） |

## 1. 「界面必见」覆盖核对

图例：✓ 已给出；△ 有落点但需补产品规则（见条件编号）；— 不涉及。

| 功能点 | ARCH §6 界面必见要点 | API | DATA | METRIC | 产品判定 |
|---|---|---|---|---|---|
| 34-1 右键创建 | 右键「添加节点」 | `add_node` | 主表 / ADS node | N/A | ✓ |
| 34-2 工具栏按钮 | 按钮「添加节点」 | 同 34-3 | — | N/A | ✓ |
| 34-3 弹窗字段 | 名称、技术分类、描述、重要性 | §2.1 四字段；category 自由文本 | 主表列 | N/A | △ PROD-API-C9 |
| 34-4 指定位置 | 点击处落点、刷新不变 | `layout{x,y}` | `layout_x/y` | N/A | ✓ |
| 34-5 唯一标识符 | 节点详情显示编号 | `node_id_map`；`/current.nodes[].technology_id`（routes:404） | `technology_id` | N/A | ✓ |
| 35-1 单选 / 框选 | 单选 + 框选 | — | — | N/A | ✓ FE 复用 |
| 35-2 右键 / Delete | 右键「删除节点」+ Delete | `delete_node` | 软删 | N/A | ✓ |
| 35-3 确认框提示关系 | 工作集 N 条 + 全景隐藏 M 条 | §5.2 两计数 | §7.4 | §2.2 #1-2 | △ PROD-API-C11 |
| 35-4 节点与关系移除 | 节点与连线消失 | 级联软删 | §2.3 | N/A | ✓ |
| 36-1 Ctrl 选两点 | 依次选中两点 | `src`/`dst` | §2.4 方向 | N/A | ✓ |
| 36-2 右键「添加关系」 | 选中两点才出现 | `add_edge` | — | N/A | ✓ |
| 36-3 类型 / 强度 / 时间 | 类型下拉、强度、起止年 | §2.2 三枚举 + 0–10 + 年份 | §2.1 | §3.1 人工边界 | △ PROD-API-C7/C8、PROD-METRIC-C1 |
| 36-4 显示连线 | 有向箭头 + 类型标签 | `rel_type`/`strength_manual` | — | N/A | ✓ |
| 37-1 点击高亮 | 选中态 | — | — | N/A | ✓ FE 复用 |
| 37-2 右键 / Delete | 右键「删除关系」+ Delete | `delete_edge` | 软删 | N/A | ✓ |
| 37-3 确认后移除 | 确认框「两端节点保留」 | §2.3 | §2.3 | N/A | ✓；存量边提示见 PROD-API-C7 |
| 38-1 双击 / 右键编辑 | 双击 + 右键「编辑属性」 | `update_node` | — | N/A | ✓ |
| 38-2 四字段 | 名称 / 分类 / 描述 / 重要性 | §2.4 patch | 主表列 | N/A | △ PROD-API-C9 |
| 38-3 点保存更新 | 画布新值 +「已加入待保存改动」 | 进草稿 | — | N/A | ✓ |
| 39-1 自动记录修改 | 「未保存改动 N 项（本批上限 50）」 | §1 OPS_LIMIT=50 | — | §2.2 #3 | △ PROD-API-C3（50 提示缺） |
| 39-2 撤销 / 重做 | 两按钮 + 可用态 | — | — | N/A | ✓ FE 草稿栈 |
| 39-3 Ctrl+Z / Ctrl+Y | 快捷键 | — | — | N/A | ✓ FE |
| 39-4 可追溯 | 刷新恢复提示；版本详情逐条 | §4.2 change_log | change_log | N/A | △ PROD-API-C2/C6 |
| 40-1 保存 | 「保存图谱」→ 成功提示 | §3.3 publish/results | `publish_results` | §2.2 #6 | △ PROD-API-C4、PROD-METRIC-C2 |
| 40-2 创建新版本 | 版本说明输入 + 列表新增 | `label`/`kind` | `graph_version.kind` | N/A | △ PROD-API-C1/C10 |
| 40-3 回滚 | 确认框 + 分组计数 + 可再回滚提示 | §4.3/§4.4 | §5.3 | §2.2 #4 | △ PROD-DATA-C1 |
| 40-4 修改记录与操作人 | 列表（操作人/时间/类型/计数）+ 详情 | §4.1/§4.2 | §3.4 | §2.2 #5 | △ PROD-API-C1/C2/C6、PROD-METRIC-C3 |
| 横切 real 轨不显示种子 | 只显示服务端数据；空态 | §5.1 `tech_edges[]`/`layout` | 两张边表 | N/A | ✓ |
| 横切 未登录只读 | 写控件禁用 + 顶部提示 | §6.3 `relayWrite` | — | N/A | △ PROD-API-C3（401 提示缺） |

## 2. API 分册会签

### 2.1 结论

**有条件同意。** 10 op、版本四端点、`impact` 两计数、`/current` 增量、单事务发布、operator 注入、50301 退役 / 50303 新增均与 ARCH 一致；`node_id_map`、`kind`、`rollbackable`、`operator_display` 能支撑 34-5、40-2/40-3/40-4。主要缺口不在接口能力，而在「接口字段到用户文案」这一段：英文码直出、版本详情仍是裸 JSON、错误/状态提示不完整、历史版本兼容未定、`stats` 与 DATA 形状冲突。

### 2.2 条件

#### PROD-API-C1 · 必修 · 版本 / 回滚英文码显示映射

- 改哪里：API §3.4 `stats`、§4.1 版本列表字段表、§4.3 回滚预览、§7 前端配合。
- 改成什么：
  1. `kind` 显示：`save`→「保存」、`rollback`→「回滚」、`seed`→「种子」、`ent`→「历史版本」。界面不得出现原始码。
  2. `not_rollbackable_reason`：`no_snapshot`→「该版本无快照，不能回滚」；`snapshot_oversize`→「该版本数据量超出快照上限，不能回滚」；`null` 不显示。
  3. `snapshot_status` 不在界面直接显示，只用于派生 `rollbackable` 与原因。
  4. 分组中文名：`tech_nodes`→技术点、`tech_edges`→技术点间关系、`entity_links`→实体挂接、`entity_edges`→实体关系、`entity_attrs`→实体属性。
  5. **同一组键、两种时态、两套文案**：版本统计用「新增 / 修改 / 删除」；回滚预览用「恢复 / 还原 / 移除」。不得把回滚预览的 `added` 译成「新增」（它在回滚语境是「恢复」）。
  6. 界面不得出现 `stats` / `counts` / `rollbackable` / `snapshot_status` / `not_rollbackable_reason` 字段名。
- 证据：API:193-206、:229-237、:274-286、:433-436；ARCH:218-219。

#### PROD-API-C2 · 必修 · 版本详情 `changes[]` 中文化

- 改哪里：API §4.2。
- 改成什么：
  1. 每条 change 增加或派生中文摘要：新增技术点「X」、编辑技术点「X」（描述）、删除技术点「X」、新增关系「A→B（依赖）」、删除关系「A→B（依赖）」、挂接实体「X」、实体关系变更等；不得只显示 `add_node` 等 op 码。
  2. `object_type` 中文：`node`→技术点、`tech_edge`→技术点间关系、`entity`→实体、`edge`→实体关系；`op` 按动作词映射。
  3. `before` / `after` 用中文字段标签 + 值展示；标签至少覆盖 `name_cn`（名称）、`category`（分类）、`description`（描述）、`importance_level`（重要性）、`layout`（位置）、`rel_type`（关系类型）、`strength_manual`（强度）、`time_range`（时间范围）、`status`（状态）、`source`（来源）；隐藏 `client_op_id`、`client_node_id`、`trace_id`、`base_version`、`op` 等内部字段。
  4. `tech_edge` 变更必须显示两端节点名，不能只显示 `src`/`dst` 数字；`before`/`after` 需带 `src_name`/`dst_name`，或由 API 保证前端可解析。
  5. 历史版本 `before=null` →「修改前未记录」；历史 `after` 是提交的 op 请求而非发布后行，显示「历史记录：仅保留操作请求」，按动作白名单展示，不把内部字段当业务字段。
- 证据：API:245-261；`routes:771-776`（as-built `before` 不写、`after`=op）；ARCH:219。

#### PROD-API-C3 · 必修 · 错误 / 状态用户提示补齐

- 改哪里：API §7「前端配合」表。
- 改成什么（新增或修正以下行）：
  - 401 / `40101`：写控件禁用 + 顶部提示「登录后可使用编辑功能」；草稿本地保留。
  - 503 / `50303`：下游不可达 →「服务暂不可用，请稍后重试」；草稿保留；不得显示 50303。
  - 503 / `50302`：工作集表 / 列缺失 →「维护功能暂不可用，请联系管理员」；**不要写「可重试」**，重试不会修复缺表。
  - 500 / `50001`：保留「保存失败，改动未丢失，可重试」。
  - 404 / `40401`（change_set 不存在）：「本次改动已失效，请刷新后重试」。
  - 409 / `40901`（死锁 1213 / 锁等待 1205）：同「他人正在保存，请稍后重试」，草稿保留。
  - 409（change_set 状态 rejected 再发布）：「本次改动已失效，请刷新后重试」。
  - 单批 50 条：`N=50` 时提示「本批已满，请保存图谱后继续」+「保存后继续」按钮；N 与 39-1 同口径（op 条数，一个 `delete_node` 带多个点仍算 1 条）。
  - 422 逐条：直接显示 API `errors[].msg` 的中文；名称重复补「名称已存在（不区分大小写），请换一个」；自环、端点不存在、时间越界给字段级中文。
- 证据：API:407-436；ARCH:239-254；`routes:42`（OPS_LIMIT=50）。

#### PROD-API-C4 · 必修 · 保存回执与「未生效项」

- 改哪里：API §3.3 `results`、§7 前端配合。
- 改成什么：
  1. 40-1 成功提示若展示计数，用「保存成功：N 项已生效，M 项未生效」；不得出现 `results` / `failed_items` / `succeeded` 字段名。
  2. `M>0` 时必须可展开查看未生效项，每项中文原因，并提供「查看未生效项」入口；是否支持「重新加入草稿」由 FE 决定，但不能让用户无从修复。
  3. `failed_items[].reason` 必须是用户可读中文，或 API 给稳定 code + FE 字典；不得直出英文异常。
  4. 历史版本 `results:null`（API §3.3 :189）不显示计数，显示「该版本未记录逐条结果」；不得当作 0 项。
- 证据：API:183-189、:430；METRIC:109；`routes:866-884`。

#### PROD-API-C5 · 必修 · `stats` 形状 API 与 DATA 必须统一

- 改哪里：API §3.4 与 DATA §5.2 同一处。
- 现状：API 定义嵌套分组 `{tech_nodes:{added,updated,removed}, ...}`；DATA §5.2 写死扁平键 `node_add/node_del/...`。两份分册不能各说一套。
- 改成什么：二选一，写入 API / DATA / DDL / 实现单；40-3 的 `counts` 与 40-4 的版本 `stats` 必须同一结构（METRIC §7-5）。产品不指定技术形状，但必须唯一。
- 证据：API:195-206；DATA:338；METRIC:116、:224。

#### PROD-API-C6 · 必修 · 历史版本 `stats` / `before` 显示规则

- 改哪里：API §3.4 :205、§4.1、§4.2。
- 改成什么：
  1. 历史 `stats` 至少四种形状：`{"ops":N}`（发布中断 / 未走到统计更新时）、`{"+node","-node","+edge","-edge"}`（投影流程走完，含 pending）、`{}`、`NULL`。列表显示：`ops`→「N 项改动」；扁平→「技术点 +a/−b · 关系 +c/−d」；空 / `NULL` / 无法识别→「—」+ tooltip「历史版本未记录分组计数」。缺组不补 0。
  2. 详情旧记录 `before=null` →「修改前未记录」；旧 `after`=操作请求 →「历史记录仅保留操作请求」；不展示内部字段。
  3. 新版本用规范 `stats`；历史版本可不回填，但显示规则固定。
- 证据：API:205、:260；`routes:844`（先写 `{"ops":len(ops)}`）、`:852-858`（投影成功后改扁平四键）；ARCH:219。

#### PROD-API-C7 · 必修 · 36-3 人工强度标识与字段名

- 改哪里：API §5.1 `tech_edges[]`、§5.3 人工边字段；与 METRIC §3.1-2 对齐。
- 改成什么：
  1. 36-3 弹窗强度字段显示「关系强度（人工）」；关系标签 / 详情显示灰色「人工」标签；种子边显示「存量」，不得标「人工」。
  2. 不挂任何 auto 口径 ⓘ；如需说明，用文字「人工编辑值，不参与自动指标」，不用 ⓘ 图标（避免打开空指标卡）。
  3. 界面不得出现 `strength_manual` / `strengthManual` / `strength_auto` 字段名；种子边若显示强度，标「存量强度（只读）」并说明来源。
- 证据：API:339、:370；METRIC:126、:222；ARCH:269。

#### PROD-API-C8 · 建议 · 强度 / 时间 UX 与必填性

- 改哪里：API §2.2 :103-104。
- 改成什么：强度 UI 0–10、步长 0.1（后端可收 0.01），helper「数值越大关系越强」；时间范围建议与 ENT 46 对齐为**选填**（`time_range` 可省略；若填则 from/to 均需 1900–2100 且 from≤to），文案「时间范围（选填）」；错误「起始年不能晚于结束年」「年份需在 1900–2100」。若坚持必填，需在验收说明理由。
- 证据：API:103-104；`routes:681-692`（ENT 46 `time_range` 为可选）。
- 附注（P2「枚举可扩展」）：三项枚举应集中在单一常量 / 配置位，未来加第四项不改多处硬编码；本次 UI 仍固定三项。

#### PROD-API-C9 · 建议 · `category` 与 `importance_level` 表单契约

- 改哪里：API §2.1 :76-78、§2.4。
- 改成什么：`category` 为下拉单选，选项来自 `dim_tech_domain`；显示并提交中文 `domain_name`（详见 §5.2）；维表为空 / 不可用时降级为文本输入（allow-create）；历史自由文本作为当前值显示；种子点 `NULL` 显示「未分类」，编辑时提示选择。`importance_level` 空显示「未设置」，不得默认「中」。
- 证据：API:76-78；DDL:7、:117-122；ARCH:195。

#### PROD-API-C10 · 建议 · 版本列表 / 回滚入口可用性

- 改哪里：API §4.1、§4.3。
- 改成什么：列表标「当前版本」；当前版本行不提供回滚（或按钮禁用，tooltip「已是当前版本」）；回滚确认标题用 `label`+`v{n}`，不用裸 id；`operator` 原值放详情 / 悬浮提示，列表只显示 `operator_display`；版本说明输入上限 128，默认「保存 yyyy-MM-dd HH:mm」。
- 证据：API:212-239、:291；DDL:55-64（`label VARCHAR(128)`）。

#### PROD-API-C11 · 必修 · 35-3 确认框关系口径

- 改哪里：API §5.2；ARCH:200 的确认框文案。
- 改成什么：确认框除 `tech_edge_count`、`panorama_hidden_relation_count` 外，还应把 `edge_count`（实体关系）与 `entity_link_count`（人工挂接实体）按用户语言列出，否则「全部关系」不成立；文案注明「工作集内」与「全景图中」是不同视图、可能重叠；`M=null` 显示「无法统计」。
- 证据：API:349-355；ARCH:200。

#### PROD-API-C12 · 建议 · 版本详情 `changes[]` 分页 / 分组

- 改哪里：API §4.2。
- 改成什么：单版本变更可能因 `delete_node` 级联产生大量行；详情需分页或按对象分组 / 虚拟滚动，至少给出总数与分组计数，避免一次渲染数百条。
- 证据：API:241-261；DATA:111（级联）。

#### PROD-API-C13 · 建议 · 空态 / 加载态补齐

- 改哪里：API §7 前端配合。
- 改成什么：`N=0` 时「保存图谱」禁用，tooltip「没有待保存的改动」；版本列表空态「暂无版本记录」；工作集空态「暂无技术点，右键或点击『添加节点』开始」；加载中骨架屏 / 保存中禁用编辑（ARCH §7 已有，API 表未列全，由 FE-TS-10D 承接）。
- 证据：API:434-436；ARCH:239-254。

## 3. DATA 分册会签

### 3.1 结论

**有条件同意。** 新表 `graph_tech_edge`、坐标列、`name_cn_active` 生成列、`kind`/`snapshot_status`/`publish_results`、批次幂等键、快照 N=1 含软删行、加锁单事务、1213/1205→409、种子 `--all` 禁用均成立，且对 ARCH 停机确认①/② 有明确落点。主要缺口是：回滚整表还原的用户语义、不可回滚原因与历史版本显示、`stats` 形状与 API 的冲突、分类维表就绪。

### 3.2 条件

#### PROD-DATA-C1 · 必修 · 回滚确认框「整表还原」双向语义

- 改哪里：DATA §5.3 :367、§12-5 :679；API §4.3 回滚预览文案。
- 改成什么：确认框必须同时说明「之后新增的会消失、之后删除的会恢复、之后修改的会还原」，不能只写「将撤回 X 项」。完整文案见 §5.4。`counts` 的 `added` / `removed` / `updated` 在回滚语境分别译「恢复 / 移除 / 还原」，不是「新增 / 删除 / 修改」。
- 证据：DATA:367、:679；API:274-286；ARCH:218。

#### PROD-DATA-C2 · 必修 · 不可回滚原因与历史版本显示

- 改哪里：DATA §3.4 :175-181、§3.7 :213-223。
- 改成什么：`snapshot_status='none'`（历史 ENT 版本）→ 列表标「历史版本」/「无快照」；`skipped_oversize`→「快照超限」；`rollbackable=false` 时按钮置灰 + 原因；不得显示 `none` / `skipped_oversize` / `no_snapshot` 原文；历史版本仍可查看详情。
- 证据：DATA:175-181、:213-223；API:233-235。

#### PROD-DATA-C3 · 必修 · `stats` 形状与 API 统一

- 改哪里：DATA §5.2 :338。
- 改成什么：与 PROD-API-C5 同一决定；`graph_version.stats` 持久化形状必须能被 API 直接返回并被 40-3 / 40-4 共用，不能 DATA 写扁平、API 读嵌套。
- 证据：DATA:338；API:195-206；METRIC:116、:224。

#### PROD-DATA-C4 · 必修 · 分类下拉数据源就绪

- 改哪里：DATA §6.3 / §6.7 与执行前检查。
- 改成什么：确认 demo 库 `dim_tech_domain` 至少覆盖演示所需分类（算法 / 算力 / 数据 / 应用等）；现有 DDL 只带三行演示值（DDL:117-122），不足时由 DATA / SEED 补种子行，不改表结构。若维表不可用，FE 降级文本输入，但 34-3 不能因下拉为空而无法提交。
- 证据：API:76；DDL:7、:117-122。

#### PROD-DATA-C5 · 建议 · SEED-L01 演示切片

- 改哪里：DATA §6.2。
- 改成什么：演示默认切片建议选 #2「人工智能 / 大模型」（可读性好、关系密度足够覆盖增删边与回滚）；#1 用于与现有 ENT 1 点 / 61 实体边的回归；#3 只做压测。执行前 `--dry-run` 输出点数、边数、`distinct relation_type`，确认 ≤50 点且快照阈值内，结果附在 SEED-L01 执行记录。
- 证据：DATA:410-418、:418。

#### PROD-DATA-C6 · 建议 · 快照超限的再回滚提示

- 改哪里：DATA §4.2 :291-292。
- 改成什么：目标版本 `rollbackable=false` 时按钮置灰 + 原因；目标可回滚但担心新快照超限时，确认框加「若数据量超出快照上限，本次回滚生成的新版本将不能再次回滚」。不要承诺「一定可再回滚」。
- 证据：DATA:291-292；API:305。

#### PROD-DATA-C7 · 建议 · `tech_edge` 变更记录的可展示数据

- 改哪里：DATA §5.2 :326、:330、§5.5 :389。
- 改成什么：`add_edge` / `delete_edge` 的 `change_log.before/after` 要带足够信息让 40-4 显示「A→B（依赖 / 存量码）」：至少 `src`/`dst` 对应节点名、中文 `rel_type`（auto 行带 `rel_code`）；`object_id` 的 `edge_id` 只作内部号，不在界面直出。
- 证据：DATA:326、:330、:389；API:245-261。

#### PROD-DATA-C8 · 建议 · 种子边强度的只读展示

- 改哪里：DATA §2.1 :79、§6.3 :426；API §5.1 `tech_edges[]`。
- 改成什么：`strength_auto` 保留在表中是对的；但 `/current.tech_edges[]` 目前不返回它。若维护页要显示种子边强度，增加只读字段并标「存量强度（只读）」；若不显示，关系详情写「存量关系，强度见全景」。种子边任何情况下不标「人工」。
- 证据：DATA:79、:426；API:339。

## 4. METRIC 分册会签

### 4.1 结论

**有条件同意。** 「34–40 不挂 `metric_id`、六类操作回执计数按 DN-A03-09 建议豁免、不挂 ⓘ / MockBadge、人工强度不进任何 `M_TECH_*` / S4、新建点无度无分显示空」的判定与 ARCH §9 完全一致，证据链（读图、S4 种子、Java 回填、DDL 默认值）扎实。主要缺口是产品侧落点：36-3「人工」标签位置、40-1 回执文案、40-3/40-4 的两种时态文案、0/null 规则的界面表达。

### 4.2 条件

#### PROD-METRIC-C1 · 必修 · 36-3「人工」标签落点

- 改哪里：METRIC §3.1-2 :126、§7-3 :222。
- 改成什么：把「由 FE 实现单定」改为固定规则：弹窗字段「关系强度（人工）」；画布关系标签常驻只显示类型，强度与「人工」标签放悬浮提示 / 关系详情（「强度 7.5 · 人工」）；种子边标「存量」；不挂 ⓘ，如需说明用文字「人工编辑值，不参与自动指标」。
- 证据：METRIC:126、:222；ARCH:269；API:339、:370。

#### PROD-METRIC-C2 · 必修 · 40-1 保存回执文案与未生效项

- 改哪里：METRIC §2.2-6 :109。
- 改成什么：文案定为「保存成功：N 项已生效，M 项未生效」；`M>0` 可展开中文原因；不出现 `results` / `failed_items` / `succeeded` 字段名；与 PROD-API-C4 同一口径。
- 证据：METRIC:109；API:183-189、:430。

#### PROD-METRIC-C3 · 必修 · 40-3 / 40-4 同源与两套时态

- 改哪里：METRIC §2.3-4 :116、§2.2 #4-#5 :107-108。
- 改成什么：回滚预览「将撤回 / 恢复 / 还原」与版本列表 `stats` 必须读同一份结构；分组中文名固定；版本统计用「新增 / 修改 / 删除」，回滚预览用「恢复 / 还原 / 移除」；不显示键名。§2.2 #4「各拆增 / 删 / 改」改为实际分组（`tech_edges` 只有增 / 删，`entity_attrs` 只有改）。
- 证据：METRIC:107-108、:116、:224；API:195-206。

#### PROD-METRIC-C4 · 建议 · 0 / null / 取不到规则（确认项）

- 改哪里：METRIC §2.3 :113-117。
- 改成什么：产品确认并写入实现单：35-3 的 `panorama_hidden_relation_count=null` →「无法统计」；其余计数取不到不渲染、不显示 0；39-1 的 N 与后端 50 同为 op 条数；40-3 的 `total` 为差异处数；40-4 缺组显示「—」而非 0。
- 证据：METRIC:113-117；API:354、:434-436。

#### PROD-METRIC-C5 · 建议 · §1.2 事实修正

- 改哪里：METRIC §1.2 40-1 行 :77。
- 改成什么：「界面必见无；回执有」不准确。ARCH 40-1 的界面必见是「保存图谱 → 成功提示 → 刷新后仍在」；应写「成功提示（无固定数字；若展示回执计数见 §2.2-6）」。
- 证据：METRIC:77；ARCH:216。

#### PROD-METRIC-C6 · 建议 · 指标边界转成验收断言

- 改哪里：METRIC §3.2 / §3.3 / §3.4。
- 改成什么：把「字段不得被指标读取」「公式不得引入人工层」「种子脚本只扫 Nebula」转成 PY-IMPL / JAVA-IMPL 的可执行验收断言（单测或脚本检查），而不只是文档约束；至少覆盖 `strength_manual` 不进 `weight` / `strength` / S4、`tm:` 点无分数、`--check` fixture-only。
- 证据：METRIC:131-162、:223。

#### PROD-METRIC-C7 · 建议 · 页卡 YAML 同步纳入影响清单

- 改哪里：METRIC §5 :188-207。
- 改成什么：9 处 diff 全部纳入影响清单；`updated` 改 2026-11-13；`maintain_ruling` 补「草稿栈 → 保存即发布 → 版本列表 / 详情 / 回滚」；六类计数按 DN-A03-09 建议豁免，不挂 ⓘ / MockBadge；不改 `srs02_boundary`、`leaf_count`、`seq`、`metric_id: null`、D4。
- 证据：METRIC:188-207；ARCH:287（指标页卡影响行）。

## 5. 产品结论（起草方待定点）

> 以下五点为起草方明确留给产品的判断，直接给结论；实现时以本节文案为准，技术形状仍由 API / DATA 定。

### 5.1 `operator_display` 显示「系统（历史）」「系统（种子）」的规则

**结论：接受两条主规则，但必须补 `unknown` 分支与优先级；真实用户名不得被 `kind` 掩盖。**

规则（优先级从高到低）：

1. `kind='seed'` 或 `operator` ∈ {`seed`, `system`} → 「系统（种子）」。
2. `kind='ent'` 或 `operator='py'` → 「系统（历史）」。
3. `operator` ∈ {空串, `unknown`, `null`}（不区分大小写）→ 「未知」。
4. 其余 → 原样用户名。

说明：

- `unknown` 是 as-built 的默认值（`routes:755`），必须归「未知」，不能直出英文；`py` 是 as-built 发布写死值（`routes:844`），归「系统（历史）」。API §4.5 目前只处理空串，漏了字面量 `unknown`，必须补。
- 若 `kind='ent'` 但 `operator` 是真实用户名，优先显示用户名（历史数据未见此情况，但规则不应掩盖真人）；可在名字后加「（历史）」。
- 列表 / 详情只显示 `operator_display`；`operator` 原值放详情「审计信息」或悬浮提示，供追溯。
- 版本类型列与操作人列分工：类型列负责「是什么」（保存 / 回滚 / 种子 / 历史版本），操作人列负责「谁」（用户名 / 系统（种子）/ 系统（历史）/ 未知），避免两列都说「历史」。
- 历史版本若 `operator` 缺失，详情加注「历史版本未记录操作人」，不推测姓名。
- 证据：API:312-318；`routes:755`、`:844`；ARCH:219。

### 5.2 `category` 用自由文本还是维表下拉

**结论：表单用下拉单选，显示并提交中文分类名；维表不可用时降级文本输入。**

- 选项来源：`dim_tech_domain`（DDL:117-122，现有 `domain_code` + `domain_name` 两列，演示三行）。下拉显示 `domain_name`，提交并把**中文分类名**写入 `technology_master.category`，使 `/current`、版本详情、全景叠加无需再查字典即可显示中文。`category` 现为 `VARCHAR(64)`；若 `domain_name` 超长，DATA 需评估加宽或改存 `domain_code` 并由 API 返回 `category_name`。
- 不存英文 `domain_code`，避免英文码漏到界面。若 DATA 坚持存 `domain_code`，则 API `/current` 与版本详情必须同时返回 `category_name`（join 维表），否则产品不接受。
- 维表为空 / 接口失败：降级为文本输入（allow-create），不阻塞 34-3；历史自由文本作为当前选项显示；不做维表外键存在性校验。
- 种子点 `category` 为 `NULL`：列表 / 详情显示「未分类」；编辑弹窗分类为空并提示「请选择技术分类」；不得用空串或英文码占位。
- 数据就绪：demo 库 `dim_tech_domain` 至少覆盖演示所需分类（算法 / 算力 / 数据 / 应用等）；不足由 DATA / SEED 补种子行，不改表结构（PROD-DATA-C4）。
- 证据：API:76；DDL:7、:117-122；ARCH:195。

### 5.3 历史 ENT 版本是旧扁平 `stats`，版本列表上怎么显示

**结论：兼容四种历史形状，列表只显示中文摘要，缺组不补 0；详情以逐条记录为准。**

先纠正事实：as-built 历史 `stats` 不只有扁平四键。发布事务先写 `{"ops":N}`（`routes:844`），投影流程走完后写成扁平四键（成功或 pending 都会写，除非中途异常，`routes:852-858`）；发布中断 / 未走到该更新时保留 `{"ops":N}`。因此至少四种形状：`{"ops":N}`、扁平四键、`{}`、`NULL`。

列表显示规则：

| 形状 | 显示 |
|---|---|
| 新嵌套 `stats` | 按组显示非零项，如「技术点 新增2 / 删除1 / 修改3 · 关系 新增4 / 删除1」；全零组省略 |
| `{"ops":N}` | 「N 项改动」 |
| 扁平四键 | 「技术点 +a / −b · 关系 +c / −d」 |
| `{}` / `NULL` / 无法识别 | 「—」+ tooltip「历史版本未记录分组计数」 |

- 任何情况下缺组不补 0；不显示 `+node` 等键名。
- 详情顶部显示 stats 摘要（同上）；`changes[]` 为权威明细。
- 历史记录 `before=null` →「修改前未记录」；历史 `after` 是提交的 op 请求（`routes:771-776`），不是发布后行，显示「历史记录：仅保留操作请求」，按动作白名单展示（如「删除技术点 X（请求）」），不展示 `client_op_id` / `trace_id` 等内部字段。
- 若 `changes[]` 为空，显示「该版本未记录逐条改动」，不伪造。
- 不回填历史 stats；显示层兼容即可（若 DATA 选择回填，需单独迁移单，不在本波）。
- 证据：`routes:844`、`:852-858`、`:771-776`；API:205、:260；DATA:213-223。

### 5.4 回滚「整表按快照还原」的确认框文案

**结论：确认框必须同时说「新增的消失、删除的恢复、修改的还原」，不能只写「撤回 X 项」。** 文案可按版式微调，语义不可少：

- 标题：「回滚到「{label}」（v{n}）？」
- 第一段：「将把当前图谱恢复到 {created_at} 由 {operator_display} 保存的 v{n} 状态。」
- 第二段：「目标版本之后新增的 {removed_total} 项将被移除；之后删除的 {added_total} 项将恢复；之后修改的 {updated_total} 项将还原为当时的值。」
- 分组明细（只显示非零组）：
  - 技术点：恢复 {a} / 移除 {r} / 还原 {u}
  - 技术点间关系：恢复 {a} / 移除 {r}
  - 实体挂接：恢复 {a} / 移除 {r}
  - 实体关系：恢复 {a} / 移除 {r} / 还原 {u}
  - 实体属性：还原 {u}
- 变量口径：`{a}`=`added`（目标有、当前无，将被恢复）；`{r}`=`removed`（当前有、目标无，将被移除）；`{u}`=`updated`（两边都有但值不同，将被还原）。
- 合计：「共 {total} 处差异。」
- 尾部：「回滚会生成一个新版本，可再回滚恢复。」
- `rollbackable=false`：按钮置灰 + 原因「该版本无快照 / 快照超限，不能回滚」；若担心新快照超限，加「若数据量超出快照上限，本次回滚生成的新版本将不能再次回滚」。
- 按钮：「确认回滚」/「取消」。
- 禁止：只写「将撤回 X 项」而不说「删除的会恢复」；显示 `added` / `removed` / `rollbackable` / `counts` 等字段名；把回滚语境的 `added` 一律译成「新增」。
- 证据：DATA:367、:679；API:274-286；ARCH:218。

### 5.5 36-3 的强度 ⓘ 和「人工」标签放在哪里

**结论：弹窗标「关系强度（人工）」；画布常驻标签不塞强度，强度与「人工」放在悬浮提示 / 关系详情；不挂 ⓘ。**

- 关系弹窗：字段标签「关系强度（人工）」，helper「0–10，数值越大关系越强；人工编辑值，不参与自动指标」。
- 画布关系标签：常驻只显示类型（如「依赖」）；强度与「人工」标签放悬浮提示 / 关系详情抽屉，如「强度 7.5 · 人工」。
- 关系详情：显示「强度 7.5（人工）」+「时间范围 2022–2024」；种子边显示「存量关系」，强度若显示标「存量强度（只读）」。
- ⓘ：不在强度字段挂任何 ⓘ，不用 ⓘ 打开指标卡。若设计坚持要信息入口，用文字链接「什么是人工强度？」弹出一段说明，不接 `MetricSpecCard`。
- 术语：界面只用「人工」「存量」「未设置」，不出现 `strength_manual` / `strengthManual` / `strength_auto` / `weighted_degree`。
- 证据：METRIC:126、:222；ARCH:269；API:339、:370。

## 6. 需监管人拍板

| # | 事项 | 产品建议 | 需谁 |
|---|---|---|---|
| P-L2-1 | DN-A03-09 六类操作回执计数（35-3 两项、39-1、40-3、40-4、publish results）是否一次裁定豁免 | 建议全部按「操作回执类计数」豁免，不注册 `metric_id`、不挂 ⓘ / MockBadge；未裁前文档写「建议豁免」 | PM / 数据 Lead / 监管人 |
| P-L2-2 | 名称唯一键改 DDL 是否需数据平台 Owner 书面确认（ARCH 停机确认②） | 技术不表态；上线前必须闭环，至少监管人书面确认 + 备份 + 变更窗口 | 监管人 / 数据平台 Owner |
| P-L2-3 | `dim_tech_domain` 分类数据就绪与演示分类清单 | 建议 DATA / SEED 补足算法 / 算力 / 数据 / 应用等演示分类；监管人确认范围 | 监管人 / DATA |
| P-L2-4 | SEED-L01 演示切片选择 | 产品建议默认 #2「人工智能 / 大模型」；#1 做 ENT 回归；#3 仅压测；以 dry-run 结果为准 | 监管人 / DATA / 算法 |
| P-L2-5 | 36-3 时间范围是否改为选填 | 产品建议选填（与 ENT 46 对齐）；强度保持必填；若监管人坚持时间必填，API 不改 | 监管人 |
| P-L2-6 | DS02 监管人 `human:淮政玮` 知会：`overlay` 字段、可见集合变小（少点 / 少边 / 少路径）、P4 提示文案 | 按 ARCH §4.5 / METRIC §7-2 发知会单，拿到回执再派全景读图实现 | 监管人 / 淮政玮 |
| P-L2-7 | 50303 新码跨仓契约（display / topic / FE） | 产品无异议；需 API / 前端在实现单确认，避免与退役 50301 混用 | API / 前端 |

## 7. 影响清单增补（相对 ARCH §10）

| 资产 | 增补内容 | 归谁 |
|---|---|---|
| `storage/ENT/stores/mysql/ads.md` + `CHANGELOG.md` | 登记 `graph_tech_edge`、坐标列、`graph_version` 三列、`graph_change_set.client_batch_id`、快照 N=1；`storage/README.md` §6 改表纪律 | data-agent |
| `TS-L2-M10-ENT-API.md` §9 / `TS-L2-M10-ENT-DATA.md` §11 | 把 GRAPH-API §9、GRAPH-DATA §11 的追记落到 ENT 两册；ENT 会签单追加原审稿身份确认；确认前不派 PY-IMPL | api-agent / data-agent |
| `TechGraphMaintainControllerTest.java:69-78` | 把「add_node / add_edge / delete_edge → 400」改为正向透传；补 versions / rollback / 50 上限 / 50303 用例 | api-agent |
| `tests/test_tech_graph_read.py`、`SituationPanoramaService` 单测 | overlay 透传、人工边端点并入 nodes、200 截断、新点选中、子域过滤灰字 | algorithm-agent / java-agent |
| `FE-TS-10D`（新） | 承载本会签 §5 全部文案与规则：版本列表 / 详情、回滚确认、operator_display、kind / stats 中文化、历史版本兼容、36-3 人工标签、category 下拉、50 上限、401 / 50303 / 50302 / 404 change_set 提示 | frontend-agent |
| `FE-TS-10C` | 两处必改：`changes` 补 `client_batch_id`（必填）；删 50301 分支、`publish` 支持空 body | frontend-agent |
| `FE-TS-02A` | 全景页 `overlay.status=unavailable` 非阻塞提示「人工维护的改动暂未显示，请稍后刷新」；学科筛选灰字「维护中新建的技术点不参与学科筛选」 | frontend-agent |
| `DS-02-MAINTAIN-GRAPH.yaml` | METRIC §5 九处 diff（`updated`、头部注释、`maintain_ruling`、三条 `demands`、`metric_open_note`、`items` 口径、可选 `metric_guardrails`）；不改 `srs02_boundary` / `leaf_count` / `seq` / `metric_id: null` / D4 | metric-agent / data-agent |
| `metrics/registry/metric-readiness-matrix-TECH.yaml`、`metric-srs-map.yaml` | 确认 34–40 无新增行、无 D4 变更；在本波记录「no-change」备注，防误登记 | data-agent / metric-agent |
| `dim_tech_domain` demo 数据 | 补演示分类行；确认 `domain_name` 中文名可用（PROD-DATA-C4） | data-agent / seed |
| `TS-L2-M10-GRAPH-SEED-L01`（新） | 新增种子任务 / 文档：≤50 点诱导子图 + `tech_rel`，写主表 / ADS node / `graph_tech_edge`，产 `kind=seed` 版本 + 快照，禁用 `--all` | data-agent / algorithm-agent |
| `TS-L2-M10-合规演示用例.md` 34–40 七行 + `科学技术全景-索引.md` | 按新流程重写：草稿栈、保存即发布、版本 / 回滚、全景回显、子域筛选不显示新点、叠加降级 | qa-agent / product-agent |
| 模块说明书 34–40 叶 | 按 ARCH §6 + 本会签 §5 写功能点与界面必见；落点仍待 doc-agent 确认 | product-agent / doc-agent |
| 41–47 用例 | 回滚连带实体改动、技术点列表多出种子点、删除种子点后重跑不复活 | qa-agent |
| DDL 执行 | `demo_gkxlumenx_dwd/ads` 执行前备份；名称唯一键 Owner 确认；变更窗口 | 监管人 `human:刘剑锋` |
| `TS-L2-M10-GRAPH-SIGNOFF-{API,DATA,ALGO,PRODUCT}.md` | 追加本 L2 会签结果与条件闭合记录 | coordinator |

## 8. 签收边界

- 本会签只对 API / DATA / METRIC 三份分册的产品可见行为负责；接口形状、表结构、指标注册由对应审稿身份继续会签。
- 必修项闭合后，产品侧同意三份分册进入实现派单；建议项不阻断派单，但应进入 `FE-TS-10D` / `PY-IMPL` / `JAVA-IMPL` 的实现单验收。
- 本文件不改被审稿、不改 ARCH、不改 ENT 两册、不改 `task-registry`、不 git。ENT 共用路径的最终确认仍以 ENT 原审稿身份的追认为准。

---

*起草：`agent:product-agent` · 2026-11-13 · 只读审稿 · 未改被审稿 / 其他文件 / registry · 未 git、未连库*

## 复核（2026-11-13 product-agent）

- 复核对象：`TS-L2-M10-GRAPH-API.md` / `TS-L2-M10-GRAPH-DATA.md` / `TS-L2-M10-GRAPH-METRIC.md` 的 v2 稿（均含文末「会签回应」）。
- 裁定依据：`会签/TS-L2-M10-GRAPH-L2-裁定.md`（A2/A3/A5/A6/A8；B1/B4/B5/B9/B12/B13/B16/B17/B19/B20）。
- 方法：逐条核对原条件，并读 v2 实际改动段落，不只看「会签回应」表；另扫用户可见文案是否漏出英文码或字段名。
- 标记：**闭合**；**未闭合（原因 + 改法）**。证据行号均指本目录三份 v2 分册。

### 1. API 分册（PROD-API-C1～C13）

| 编号 | 级别 | 判定 | 依据 / 说明 |
|---|---|---|---|
| PROD-API-C1 | 必修 | **闭合** | API:260-269 给出 `kind` / `not_rollbackable_reason` / 五个分组 / 两种时态的中文映射；API:255 明确 `snapshot_status` 不在界面直接显示；API:327、:488-494 固定版本统计「新增/修改/删除」与回滚「恢复/移除/还原」。界面字段名禁令见 API:494。 |
| PROD-API-C2 | 必修 | **闭合** | API:281-299 增 `summary` 中文摘要、`object_type` 中文、`src_name`/`dst_name`；隐藏 `client_op_id` 等内部字段；历史 `before=null`→「修改前未记录」、历史 `after`→「历史记录：仅保留操作请求」；字段中文标签由 FE-TS-10D 承接。 |
| PROD-API-C3 | 必修 | **闭合** | API:475-493 补齐 401、50303、50302（不写「可重试」）、50001、404 change_set、409 死锁/rejected、50 条上限、422 逐条中文；API:471-473 明确 50303 仅 Java 层、50301 退役。 |
| PROD-API-C4 | 必修 | **闭合** | API:207、:488 固定「保存成功：N 项已生效，M 项未生效」；未生效项可展开；`results:null`→「该版本未记录逐条结果」，不当 0 项；禁止显示 `results`/`failed_items`/`succeeded` 字段名。 |
| PROD-API-C5 | 必修 | **闭合** | API:213-228 将嵌套分组定为 `stats` 与 `counts` 的唯一持久化形状；DATA:345-361 同步为同一结构，扁平键废止；历史不回填。 |
| PROD-API-C6 | 必修 | **闭合** | API:225、:298、:489 覆盖 `{"ops":N}`、旧扁平四键、`{}`、`NULL` 四种历史形状；缺组不补 0；`before=null` 与历史 `after` 均有显示规则。 |
| PROD-API-C7 | 必修 | **闭合** | API:392-394、:494 固定 36-3 弹窗「关系强度（人工）」、悬浮/详情「人工」、种子边「存量」；不挂 ⓘ；界面不出现 `strength_manual`/`strength_auto` 字段名。 |
| PROD-API-C8 | 建议 | **闭合** | API:106、:118 强度 UI 0–10/步长 0.1、后端 0.01；`time_range` 改为选填（裁定 A6）；三项枚举本次固定，集中常量的实现细节归 FE-TS-10D。 |
| PROD-API-C9 | 建议 | **闭合** | API:76-80、:137-142 分类为维表下拉、空则手填、显示并提交中文 `domain_name`、不做外键；`importance_level` 空显示「未设置」，不默认「中」。 |
| PROD-API-C10 | 建议 | **闭合** | API:364、:553 已做到列表/详情只显示 `operator_display`，`operator` 原值仅放详情「审计信息」或悬浮提示，符合原条件。但审计区原值仍有 `py`/`unknown` 英文码风险，见 N2；建议实现时一并收口。 |
| PROD-API-C11 | 必修 | **未闭合（部分）** | API:407、:492 已把确认框扩到四项，但只列字段名，未给 `edge_count` / `entity_link_count` 的用户语言标签；同时 API:226、:406 与 METRIC:23、:68、:96、:219、:246 仍写「35-3 两项」，与本条「四项」自相矛盾；METRIC:107-117 只给两项文案。改法：API §5.2/§7 用中文写全四项（如「工作集内技术点间关系 N 条」「全景图中将隐藏存量关系 M 条（上限）」「实体关系 N 条」「挂接实体 N 个」），并把 §3.4/§5.2 的豁免表述改为「35-3 四项」；METRIC 同步 §1.2、§2.2、§7。`edge_count` / `entity_link_count` 是否并入 DN-A03-09，需与已签收的 ENT 口径对齐后一次写清。 |
| PROD-API-C12 | 建议 | **闭合** | API:290 增 `changes_total` 与 `page`/`size`（默认 100、上限 500），可支撑大量级联变更的分页。 |
| PROD-API-C13 | 建议 | **闭合** | API:493 补齐 `N=0` 禁用与 tooltip、版本列表空态、工作集空态、保存中禁用编辑、骨架屏。 |

### 2. DATA 分册（PROD-DATA-C1～C8）

| 编号 | 级别 | 判定 | 依据 / 说明 |
|---|---|---|---|
| PROD-DATA-C1 | 必修 | **闭合** | DATA:396 明确「之后新增的会消失、之后删除的会恢复、之后修改的会还原」；DATA:345-361 固定 `added=恢复`、`removed=移除`、`updated=还原`，并禁止只写「撤回 X 项」；DATA:372-374 的「该版本无快照，不可回滚」与 API 双向语义一致。 |
| PROD-DATA-C2 | 必修 | **闭合** | DATA:186-193 给出 `kind`、`snapshot_status`、`no_snapshot`、`snapshot_oversize` 的中文显示与「英文码不得直出界面」；DATA:213-223 历史版本回填 `ent`/`none`；历史版本仍可查详情。 |
| PROD-DATA-C3 | 必修 | **闭合** | DATA:345-361 与 API §3.4 同为嵌套分组；DATA:365 的「若 API 最终键矩阵不含 `updated`」是旧条件句，API 最终稿已含 `tech_edges.updated`，建议删掉该句以免实现误删子键（清理项，不影响闭合）。 |
| PROD-DATA-C4 | 必修 | **闭合** | DATA:540-562 给出 `dim_tech_domain` 演示分类清单与「维表为空降级文本输入、34-3 不因下拉为空无法提交」；`category` 存中文 `domain_name`，VARCHAR(64)、无外键。 |
| PROD-DATA-C5 | 建议 | **闭合** | DATA:452-460 默认切片 #2「人工智能 / 大模型」；#1 回归、#3 压测；执行前 `--dry-run` 输出点数、边数、distinct relation_type、丢弃计数。 |
| PROD-DATA-C6 | 建议 | **闭合** | DATA:301-303 固定提示「若数据量超出快照上限，本次回滚生成的新版本将不能再次回滚」，不承诺一定可再回滚；DATA:289-291 置灰与原因规则齐全。 |
| PROD-DATA-C7 | 建议 | **闭合** | DATA:355-358、:383 要求 `tech_edge` 的 `before/after` 带两端节点名、中文 `rel_type`（auto 行带 `rel_code`），`edge_id` 只作内部号；API:296 同步要求界面不得只显示 `src`/`dst` 数字。 |
| PROD-DATA-C8 | 建议 | **闭合** | DATA:474 明确 `strength_auto` 不出参；若维护页展示种子边强度，标「存量强度（只读）」，不标「人工」；API:392 同步。 |

### 3. METRIC 分册（PROD-METRIC-C1～C7）

| 编号 | 级别 | 判定 | 依据 / 说明 |
|---|---|---|---|
| PROD-METRIC-C1 | 必修 | **闭合** | METRIC:136 固定 36-3 弹窗「关系强度（人工）」、画布只显示类型、强度与「人工」放悬浮/详情（「强度 7.5 · 人工」）、种子边「存量」、不挂 ⓘ；METRIC:138 同步新点无度无分。 |
| PROD-METRIC-C2 | 必修 | **闭合** | METRIC:77 已把 40-1 改为「成功提示（无固定数字；若展示回执计数见 §2.2-6）」；METRIC:116 固定「保存成功：N 项已生效，M 项未生效」、`M>0` 展开、历史 `results:null` 不显示逐条结果。 |
| PROD-METRIC-C3 | 必修 | **未闭合** | 两处需改：① METRIC:114 仍写 `tech_edges{added,removed}`（若 API 补 `updated` 则加），但 API:213-228、:302-328 已把 `tech_edges.updated` 定为正式键，METRIC 应直接写 `{added,updated,removed}`，否则 40-3 分组会漏「修改关系」；② METRIC:114 与 :283 用「撤回 R」，而 METRIC:125 与 API:327、§7 已定 `removed` 回滚语境译「移除」，同一册内自相矛盾；METRIC:86「确认框撤回计数」应改「变更计数」。改法：§2.2-4 改为「恢复 A / 移除 R / 还原 U」，并同步 `tech_edges` 三键；§1.2 40-3 与 §2.2-4 的「撤回」全部改「移除/变更」。 |
| PROD-METRIC-C4 | 建议 | **闭合** | METRIC:122 区分 0、取不到、合法 null：35-3 的 M 取不到→「无法统计」；40-3 `counts:null` 为合法态并显示不可回滚原因；其余取不到不渲染、不显示 0。 |
| PROD-METRIC-C5 | 建议 | **闭合** | METRIC:77 的 40-1 行已改为「成功提示（无固定数字；若展示回执计数见 §2.2-6）」，与 ARCH:216 一致。 |
| PROD-METRIC-C6 | 建议 | **闭合** | METRIC:178-188 已转成六条可执行验收断言（字段不进公式、源表登记、`tm:` 点无分、S4 fail-closed、七类不挂 ⓘ、历史 stats 兼容）。 |
| PROD-METRIC-C7 | 建议 | **闭合** | METRIC:213-231 的 9 处 DS-02 YAML diff 全量保留，`updated` 改 2026-11-13，`maintain_ruling` 补流程，七类计数口径写入，且明确不改 `srs02_boundary`/`leaf_count`/`seq`/`metric_id`/D4。 |

### 4. v2 新引入问题 / 跨册一致性

| # | 位置 | 问题 | 改法 |
|---|---|---|---|
| N1 | API:407、:492；API:226、:406；METRIC:23、:68、:96、:219、:246 | 35-3 确认框在 API §5.2/§7 已扩为四项，但 API §3.4/§5.2 的豁免表述与 METRIC 全册仍写「两项」，且四项只给字段名、未给 `edge_count`/`entity_link_count` 的中文标签。ARCH:200 也仍写「确认框显示两项」。 | 按 PROD-API-C11 改法统一为「四项」并补中文标签；ARCH §6 该行需协调方做追补（或监管人明确维持两项并说明实体关系/挂接不在「全部关系」内），二者只能留一个口径。 |
| N2 | API:364、:553 | `operator` 原值可进详情「审计信息」/悬浮提示，历史 `py`/`unknown` 可能直出英文系统码。 | 审计区也只显示 `operator_display`；真实用户名才显示原值；`py`/`unknown` 分别显示「系统（历史）」/「未知」。 |
| N3 | METRIC:114、:283、:86 | 「撤回」与「移除」混用，且 `tech_edges` 仍带「若 API 补 updated」旧条件句。 | 按 PROD-METRIC-C3 统一。 |
| N4 | DATA:365 | 「若 API 最终键矩阵不含 `updated`」为旧条件句；API 最终稿已含该键。 | 删除该条件句，直接写 `tech_edges.updated` 的计数条件。 |
| N5 | DATA:190；API:255 | DATA 给 `snapshot_status` 的显示映射（「无快照」/「快照超限」），API 说该字段不在界面直接显示，只派生原因；DATA:396「会消失」与 API:492「将移除」也不完全同词。 | 统一为：列表不显示 `snapshot_status` 原值，只显示「不可回滚 + 原因」；确认框统一用「移除」。 |

除上述外，未发现 v2 在「界面必见」文案中新增英文码或字段名直出；API:494、DATA:193、METRIC:125 均有明确的字段名禁令。

### 5. 三份结论

| 分册 | 结论 | 未闭合项 |
|---|---|---|
| `TS-L2-M10-GRAPH-API.md` | **仍有条件** | PROD-API-C11（必修，部分未闭合：四项计数的用户语言与「两项/七类」口径统一、ARCH/METRIC 同步）；另见 N2（建议级风险：审计区 `operator` 原值可能露出 `py`/`unknown`）。C1-C10、C12、C13 闭合。 |
| `TS-L2-M10-GRAPH-DATA.md` | **同意会签** | 无必修/建议未闭合。附两项清理：DATA:365 删除 `tech_edges.updated` 旧条件句；DATA:190 与 API:255 统一 `snapshot_status` 显示口径。 |
| `TS-L2-M10-GRAPH-METRIC.md` | **仍有条件** | PROD-METRIC-C3（必修：`tech_edges` 补 `updated`；「撤回」统一为「移除」）；另需随 PROD-API-C11 把 35-3 从「两项」同步为「四项」。C1、C2、C4-C7 闭合。 |

> 产品侧对 API / METRIC 的未闭合项均为文案与口径收口，不改接口能力或数据方案；改完上述各行即可转「同意会签」。DATA 的清理项可与 API / METRIC 同批改，不单独阻断。

*复核：`agent:product-agent` · 2026-11-13 · 只读复核 · 只追加本节 · 未改被审稿 / 其他文件 / registry · 未 git、未连库*

## 最终确认（2026-11-13 product-agent）

复核范围仅限协调方列出的 v2.1 改动，不重开其余条款。

| 项 | 核对结果 | 证据 |
|---|---|---|
| PROD-API-C11 | **闭合**。35-3 确认框已改为四项中文文案：「技术点关系 N 条、实体关系 E 条、实体挂接 L 条；全景图中将隐藏存量关系 M 条」，并给出 `tech_edge_count` / `edge_count` / `entity_link_count` / `panorama_hidden_relation_count` 字段对照；API §5.2/§7、METRIC §1.2/§2.2、ARCH §6 均已按四项表述。 | API:411、:496；METRIC:68、:111-114；ARCH:200 |
| N2（operator 原值） | **闭合**。列表、详情、审计区、悬浮提示一律显示 `operator_display`，不直出 `operator` 原值；`py` / `unknown` 由后端映射中文。 | API:368、:557 |
| PROD-METRIC-C3 | **闭合**。`tech_edges{added,updated,removed}` 已去掉「若 API 补」条件句；「撤回」已全部统一为「移除」；回滚文案为「恢复 A / 移除 R / 还原 U」；35-3 四项与九类计数一致。 | METRIC:23、:96、:116、:285、:298 |
| DATA:190 / API:255 | **闭合**。`snapshot_status` 统一为「不在界面直接显示，只派生 `rollbackable` 与原因」，原码不直出；回滚语境的 `removed` 统一译「移除」。 | DATA:190；API:255、:491 |

**残留口径清理（不阻断会签）**：API:230、:410、:688 仍写「七类」，但同句已列「35-3 四项」，按数字计应为「九类」（METRIC 已统一写九类）；ARCH:272 仍写「35-3 impact 两项」。建议在向 PM / 数据 Lead 报送 DN-A03-09 豁免范围前，把这两处数字文案同步为「四项 / 九类」，避免豁免清单口径不一致。该问题不影响界面文案与接口能力。

### 最终结论

| 分册 | 最终结论 |
|---|---|
| `TS-L2-M10-GRAPH-API.md` | **同意会签**。PROD-API-C11 与 N2 均已闭合；仅附上述「七类→九类」数字口径清理，不阻断。 |
| `TS-L2-M10-GRAPH-METRIC.md` | **同意会签**。PROD-METRIC-C3 已闭合；四项 / 九类口径一致。 |

*最终确认：`agent:product-agent` · 2026-11-13 · 只核指定改动 · 只追加本节 · 未改被审稿 / 其他文件 / registry · 未 git、未连库*
