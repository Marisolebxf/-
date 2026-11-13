# TS-L2-M10-GRAPH-L2-SIGNOFF-API · DATA / METRIC 二级分册会签（api-agent）

- 日期：2026-11-13
- 审稿身份：`agent:api-agent`
- 审稿对象（草稿 v1）：
  - `sdd/l2/TS-L2-M10-GRAPH-DATA.md`（下称 **DATA**）
  - `sdd/l2/TS-L2-M10-GRAPH-METRIC.md`（下称 **METRIC**）
- 基准：`sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（v2，2026-11-13 监管人 `human:刘剑锋` 签收，含 §11 末尾「拍板结果」）
- 参照（**只查跨稿一致性，不审**）：`sdd/l2/TS-L2-M10-GRAPH-API.md`（**API**，同身份起草）
- 代码证据简写：
  - **routes** = `repos/lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py`
  - **DDL** = `repos/lumen-algo-py/vendor/entan-py/scripts/mysql/tech_graph_maintain.sql`
  - **read** = `repos/lumen-algo-py/lumen_common/algorithms/tech_graph_read.py`
- 范围声明：本单只写本文件。未改被审稿、未改 API/ENT 册、未改 task-registry、未 git、未连库、未执行 DDL。
- 总判断：
  - **DATA：有条件可落，本签为「修改后同意会签」**。`API-DATA-C1～C9` 必修闭合后可会签；`C10～C19` 为建议。
  - **METRIC：有条件可签，本签为「修改后同意会签」**。`API-METRIC-C1～C4` 必修闭合后可会签；`C5～C9` 为建议。

---

## 一、`TS-L2-M10-GRAPH-DATA.md`

### 结论

表与列能覆盖 API 要返回的绝大多数字段：版本列表/详情（`graph_version` + `kind`/`snapshot_status`）、`results`（`publish_results`）、`node_id_map`（`change_log.after`）、`tech_edges`（`graph_tech_edge`）、`layout`（`layout_x/y`）、impact 的 `tech_edge_count`、`operator_display`（`kind`+`operator` 计算）均有落点；`panorama_hidden_relation_count` 为 Nebula 只读、不需列。**但存在 9 处会直接导致接口字段错、计数错或回滚失败的硬问题**，集中在 stats 键口径、`kind` 语义、`operator` 来源、幂等边界、回滚还原顺序/生成列、回滚求差口径、ENT 追记缺行、1062 映射二义。修完即同意。

### 条件表

| 编号 | 级别 | 稿内位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| API-DATA-C1 | **必修** | §5.2 末「stats 固定键」 | 写的是扁平键 `node_add/tech_edge_add/...`，与 API 冻结的分组键直接冲突；API 明言“替代 as-built 扁平”。seed 版本也用同一 `stats=计数`（§6.3） | 改为 API §3.4 结构：`{tech_nodes:{added,updated,removed}, tech_edges:{added,removed}, entity_links:{added,removed}, entity_edges:{added,updated,removed}, entity_attrs:{updated}}`；§6.3 seed 版本同结构；§8 增一条 `MODIFY graph_version.stats` 注释（旧注释仍是 `+node/-node`），历史行不改值 | DATA:338、DATA:427；API:193-205；DDL:59 |
| API-DATA-C2 | **必修** | §3.4 `kind` 列、§3.7 回填、§11-3 | `kind` 默认/注释为 `'ent'`，只说明“历史回填 ent”，未说**新保存（含 ENT 页经同一 publish）一律 `'save'`**，实现方可能按默认写 `ent`，版本列表「类型」和 `operator_display` 会错 | 在 §3.4 与 §11-3 各加一句：`kind` 是**动作类型**，`save/rollback/seed` 分别由保存/回滚/种子写死；`ent` **仅**用于历史版本回填（含 v0）；新 ENT 保存也是 `save` | DATA:175、DATA:211、DATA:579、DATA:662；API:232、API:314 |
| API-DATA-C3 | **必修** | §5.2 步骤 2/6、§5.3 步骤 6 | `INSERT graph_version (... operator ...)` 未写 `operator` 取值来源；API 要求保存取 `change_set.operator`、回滚取请求 operator（display 注入），且 `operator_display` 依赖它 | §5.2 步骤 2 的 SELECT 补 `operator`；步骤 6 写明 `operator = change_set.operator`；§5.3 步骤 6 写明 `operator = 请求 body.operator`（display 注入，Python 不再落 `'py'`） | DATA:316、DATA:320、DATA:346-347；API:308-318、API:404-405 |
| API-DATA-C4 | **必修** | §5.5 publish 幂等 | “`status='published'` 且批次匹配”在 publish **未带 `client_batch_id`** 时无法判定；API §3.3 说“已 published 幂等返回、不报 409”，§7 又说“批次不符→409” | 写死三种：① publish 带 batch 且 ≠ `change_set.client_batch_id` → 409/40901；② 不带 batch → 视为幂等重放，返回原回执（不报 409）；③ `status='rejected'` → 409，不返回旧回执 | DATA:386；API:167-171、API:416；DATA:316 |
| API-DATA-C5 | **必修** | §5.5 submit 幂等 | 按 `client_batch_id` 命中即返回旧回执，未区分 `rejected`；草稿被放弃后同批次重提会拿到 `status:'rejected'`（前端按 draft 解析会错），且同批次改 ops 会被静默丢弃 | 命中 `rejected` → 409/40901「批次已放弃，请重新生成 `client_batch_id`」；命中 `draft/published` 才幂等返回；同 batch 但 `ops` 不同 → 409（不得静默用旧回执） | DATA:385；API:153-157；DDL:24-34 |
| API-DATA-C6 | **必修** | §5.3 还原表方法（`technology_master` 行）、§4.1 列清单 | ① 先 INSERT missing、后 DELETE surplus：快照里 active 名 A 与当前 active 名 A 不同 `technology_id` 时会撞 `uk_name_cn_active` 1062；② “UPDATE 全列”若按表结构取列，会更新**生成列 `name_cn_active`**，MySQL 报 3105 | ① `technology_master` 改为与其它表一致的「先 `DELETE` 全表（或先删多余行）→ 再按快照 `INSERT` 显式 `technology_id`」，规避唯一键时序冲突；② 明确“全列 = §4.1 显式列清单”，**排除生成列 `name_cn_active`、排除 `updated_at`**，INSERT/UPDATE 列清单同源 | DATA:359、DATA:144-151、DATA:245、DATA:261；DDL:55-64 |
| API-DATA-C7 | **必修** | §5.3 步骤 4「逐表求差」 | 未定义“存在/修改”的比较键与字段：若把全部列（含 `version_id`、`updated_at`）纳入，会把“仅版本号变化”计成修改；软删行是否算“当前有”也未定，直接影响 preview 分组与 `total` | 写明：存在性按 `status='active'` 判（软删行不计“当前有”）；行键 `technology_id` / `edge_id`；比较字段排除 `version_id`、`updated_at`（及生成列）；`tech_edges` 若两端都 active 但 `strength_manual/time_from/time_to/rel_type` 有差异，记 `updated`（并在 API §3.4/§4.3 给 `tech_edges.updated` 补键，起草方同步）；`rollback:preview` 复用同一求差函数（只读、不取锁），preview 的 counts 与回滚新版本的 stats 同源 | DATA:343-350、DATA:359；API:199-204、API:274-285 |
| API-DATA-C8 | **必修** | §11 对 ENT-DATA 的追记 | 缺 5 类对 ENT 接口有可见影响的变化，ENT 原审稿无法据此追认：① 版本署名（`operator` 从 `'py'` 变真实用户名，历史行仍 `'py'`，`operator_display` 规则）；② `stats` 结构（新分组键 / 历史扁平键或 `{ops:N}`）；③ 名称唯一性放宽后“软删后可同名重建、改名撞 active 才 422”；④ `impact` 新增两字段，其中 panorama 计数引入 Nebula 只读依赖（超时 `null`）；⑤ 快照 payload 表/列清单新增 `graph_tech_edge`、`layout_x/y` 与 `schema_version` | §11 增 5 行（或并入现有行并注明），措辞=“ENT-DATA / ENT-API 原审稿追认项”；确认前不派 PY-IMPL（沿用 ARCH §10 / API-N5） | DATA:654-672；routes:844（现 operator 写死 `"py"`）、routes:404；API:189、API:308-318、API:354 |
| API-DATA-C9 | **必修** | §5.4 唯一键 1062 行 | “409 或 422”二义，且“或落 `failed_items`”与 API“发布成功、0 行才 failed_items”混用，客户端无法确定该刷新还是标红 | 写死：名称 1062（active 重名）→ 422/42201；`graph_tech_edge` 1062（active 同键）→ 409/40901 整笔回滚（validate 已挡常规重复，publish 命中即并发/脏数据）；删除“落 failed_items”分支 | DATA:379；API:416-417、API:188 |

### 建议项

| 编号 | 级别 | 稿内位置 | 问题 / 意见 | 证据 |
|---|---|---|---|---|
| API-DATA-C10 | 建议 | §2.1 `rel_code`、§12-1 | API 不返回 `rel_code`（`tech_edges[]` 只有 `rel_type`）；auto 行两列当前同值，属冗余。**api 身份表态：建议删 `rel_code`，只留 `rel_type`**（人工=中文枚举，种子=英文原码，唯一键不变）。若坚持保留，须写明“仅供内部原文快照、不出参、不被指标读取” | DATA:78、DATA:89、DATA:540；API:328-342 |
| API-DATA-C11 | 建议 | §2.1 `rel_type VARCHAR(32)`+§6.1 类型核查 | 种子码用 `35` 位以内尚可，但 §6.1 是“英文码 + 等”，未穷举。建议放宽到 `VARCHAR(64)`，或 seed `--dry-run` 对 >32 字符直接中止；同时补规则：**若 `tech_rel.relation_type` 恰为 `包含/依赖/促进`，seed 跳过并 warning**（否则与人工键同键，用户无法添加人工边） | DATA:77、DATA:408、DATA:539、DATA:681 |
| API-DATA-C12 | 建议 | §2.1、§12-2 | 出参类型写死：`src/dst` **保持 int/number，不做字符串化**（`technology_id` 为 MySQL AUTO_INCREMENT，实际远小于 2^53；`/current` 节点现已是 `"technology_id": int(...)`）；`strength_manual/strength_auto` 出参 number（沿 `_edge_dict` 的 `float()` 先例），`layout_x/y` number。前端直接按 number 关联 `nodes[].technology_id` | DATA:114、DATA:676；routes:333-341、routes:404 |
| API-DATA-C13 | 建议 | §2.3、API §2.2 | 因 UK 含 `rel_type`，种子英文码与人工中文枚举“天然不同键”，**人工 `add_edge` 不会复活已删种子边**；现文“复活时 `strength_auto`/`rel_code` 保留”“种子边原强度字段保留”属不可达路径。建议改写为“复活仅命中间键的人工行”，并声明同端点不同 `rel_type` 可并存（前端需渲染平行边、impact 按边计数） | DATA:104-112、DATA:89；API:106 |
| API-DATA-C14 | 建议 | §6.3 seed `time_to=NULL`、API §5.1 | 种子边可能只有 `time_from`；若 `/current` 复用 as-built `_edge_dict` 的 fallback（`from=to`），会把开放区间伪装成单年。建议明确输出 `{from:X}` 或 `{from:X,to:null}`，不复制 fallback | DATA:426、DATA:543-544；routes:333-338；API:330、API:340 |
| API-DATA-C15 | 建议 | §2.1 `strength_auto` | API `tech_edges[]` 不返回 `strength_auto`，种子边强度前端不可见。建议明确“不出参”；若产品要显示，API §5.1 增字段（由 API 起草方补），DATA 不动列 | DATA:79、DATA:541；API:328-342 |
| API-DATA-C16 | 建议 | §4/§11-4 “N=1”、§8-G 注释 | `N=1` 易被读成“只保留 1 行快照”；实际是“每版一份、按 `version_id` 全量保留”（`graph_snapshot` PK=version_id）。建议写清“每版一份、不裁剪”，并补一句存储增长估算/清理策略（当前无裁剪） | DATA:236、DATA:592-594、DATA:663；DDL:109-115 |
| API-DATA-C17 | 建议 | §5.3 步骤 11、API §4.4 | 回滚回执 `results` 的形状已定，但 DATA 未定义取值：建议 `succeeded = 实际应用差异条数`、`failed=0`、`failed_items=[]`；并声明与 preview `counts.total` 同源（同一事务内求差） | DATA:352；API:292-300 |
| API-DATA-C18 | 建议 | §5.2 步骤 10-12 | `delete_node` 级联软删多条 `graph_tech_edge` 时，`change_log` 只有一条 `node` 行，版本详情看不到被级联删的边（stats 里有数）。建议级联边各记一行 `object_type='tech_edge'`（`node_id_map` 重建须过滤 `op='add_node'`/`after` 含 `client_node_id`，避免扫到 `after=null` 的删除行）；若坚持不记，请在 §4.2/API 注明“级联删除只体现在 stats” | DATA:330-331、DATA:387；API:250-260 |
| API-DATA-C19 | 建议 | §3.1/§3.3、§4.1 列清单 | ① `layout_x/y` 主表与 ADS 节点双写，建议声明 master 为权威、发布时覆盖 ADS，并给修复路径，避免漂移；② 快照显式列清单必须含各表主键（`technology_id`/`edge_id`/复合键），否则“整表还原”会改主键、`change_log.object_id` 对不上 | DATA:133、DATA:164、DATA:261、DATA:323 |

---

## 二、`TS-L2-M10-GRAPH-METRIC.md`

### 结论

34–40 不挂 `metric_id`、六（七）类数字按 DN-A03-09“建议豁免”处理，方向成立；六类里 5 类可由接口产出（35-3 两项来自 `impact`、40-3 来自 `rollback:preview`、40-4 来自 `versions.stats`、publish 来自 `publish.results`），39-1 是前端会话计数、不依赖接口。**但有两处事实性错误必须改**：把“回滚预览 counts”说成与目标版本 `stats` 同源；漏了回滚回执 `results` 这类计数。另有 4 条表述需与 API 键矩阵/空值语义对齐。

### 条件表

| 编号 | 级别 | 稿内位置 | 问题 | 改成什么 | 证据 |
|---|---|---|---|---|---|
| API-METRIC-C1 | **必修** | §2.3-4、§7-5 | “40-3 与 40-4 同源……必须读同一份 `stats`”错误：40-4 展示的是**该版本自己**的 `stats`；40-3 的 `counts` 是**目标版本快照与当前工作集求差**的结果，两者不是同一份数据。按现文实现会拿目标版本 stats 冒充预览，数字必错 | 改为：“二者用**同一套分组键**，不是同一份数据；40-3 由快照 diff 得出；真正同源的是 40-3 `counts` 与**回滚产生的新版本** `stats`（同一求差函数），不是目标版本 stats”。§7-5 同步改写，并回答“需 API/DATA 在实现单写死求差函数” | METRIC:116、METRIC:224；API:274-285、API:199-204；DATA:343-350 |
| API-METRIC-C2 | **必修** | §2.2 六类表、§1.3、§3.1-5、§7-1 | 漏了**回滚回执 `results`**（`{succeeded,failed,failed_items}`）：接口确实返回，若前端显示“回滚成功 N 项”就是第 7 类操作回执计数。现文“六类”范围不完整 | 把 §2.2-6 扩为“publish / rollback 回执 `results`（同结构）”，或新增第 7 类；§1.3、§3.1-5、§7-1 的“六类”同步改“七类”；注明历史版本 `results:null` 时不显示逐条结果 | METRIC:96、METRIC:109、METRIC:129、METRIC:220；API:292-300、API:189 |
| API-METRIC-C3 | **必修** | §2.2-4 回滚分组计数 | “技术点 / 技术点间关系 / 实体挂接 / 实体关系 / 实体属性，**各拆增/删/改**”与 API 键矩阵不符：`tech_edges`、`entity_links` 只有增/删，`entity_attrs` 只有改；若 API 按 C7 给 `tech_edges` 补 `updated`，也仍非“各拆三键” | 改为逐组写：`tech_nodes` 增/改/删、`tech_edges` 增/删（+改，若 API 补）、`entity_links` 增/删、`entity_edges` 增/改/删、`entity_attrs` 改；或直接引用 API §3.4 键矩阵，不另立措辞 | METRIC:107；API:199-204 |
| API-METRIC-C4 | **必修** | §2.3-2 “其余计数取不到应按失败处理” | 与 API 冲突：40-3 在“无快照/超限”时**合法返回 200 + `counts:null`**，应显示不可回滚原因，不是失败/不渲染 | 加例外：“40-3 `counts:null` 属合法态：不显示分组计数，显示 `not_rollbackable_reason`（`no_snapshot`/`snapshot_oversize`）并置灰回滚；其余计数取不到才按失败处理” | METRIC:114；API:285-286、API:233-235 |

### 建议项

| 编号 | 级别 | 稿内位置 | 问题 / 意见 | 证据 |
|---|---|---|---|---|
| API-METRIC-C5 | 建议 | §3.2 字段清单 | `technology_master` 的 `x`/`y` 并非列名；DATA 实际加的是 `layout_x`/`layout_y`。改为 `layout_x/layout_y`（ADS `graph_entity_node` 同），避免实现单按 `x/y` 找列 | METRIC:141；DATA:133、DATA:164；API:79 |
| API-METRIC-C6 | 建议 | §2.2-5 版本 `stats` | 需补历史兼容：历史 ENT 版本的 `stats` 可能是旧扁平键或 `{ops:N}`（as-built 初始行），版本列表按可得键显示、缺键不补 0 | METRIC:108；API:205、API:237；routes:844 |
| API-METRIC-C7 | 建议 | §2.2-4 文案 | “将撤回该版本之后的全部改动共 X 项”里 `X=counts.total`，而 `total` 含 `added`（**将被恢复**）与 `removed`（**将被撤回**），不只是“撤回”。建议文案改为「将变更 X 项（恢复 A / 撤回 B）」，并说明 X 的口径 | METRIC:107；API:281-285 |
| API-METRIC-C8 | 建议 | §2.2-3 未保存改动 N | 明确 39-1 是**前端草稿净差 op 条数**（与后端 `OPS_LIMIT=50` 同口径），不依赖新接口；`changes:validate.op_count` 只用于预览，不是 39-1 的取数来源，避免实现单多接一个统计 | METRIC:106；API:162 |
| API-METRIC-C9 | 建议 | §2.2-6 `results` | 补一句“`results` 随版本行持久化（DATA `publish_results`），历史版本无值为 `null`；`failed_items` 是错误明细，不做聚合/不挂 ⓘ”，与 API §3.3/§4.4 对齐 | METRIC:109；API:188-189；DATA:177 |

---

## 三、跨稿一致性

1. **`stats` 键（冲突，必修）**：DATA 扁平键（`node_add…`）↔ API 分组键（`tech_nodes{added,…}`）↔ METRIC 中文分组。以 API §3.4 为唯一口径，DATA 改（API-DATA-C1），METRIC 键矩阵对齐（API-METRIC-C3）。历史 ENT 版本还可能 `{ops:N}`，三册都要承认“原样返回、缺键不补 0”。
2. **`layout` 列名（不一致，建议级）**：DATA `layout_x/layout_y`（正确，DDL 已这么写）↔ API §2.1 “`technology_master.x/y`”↔ METRIC §3.2 “`x/y`”。数据列不改名，**API/METRIC 措辞改 `layout_x/layout_y`**；出参键仍是 `layout:{x,y}`。
3. **`src/dst` BIGINT 出参（已闭合，补口径）**：`/current` 节点现有 `technology_id` 已是 int（routes:404），`graph_tech_edge.src/dst` 同为 `technology_id`，**出参保持 number，不做字符串化**；AUTO_INCREMENT 不会超 2^53。DATA §12-2 与 API §5.1 各补一句同口径即可（C12）。
4. **`rel_type` / `rel_code`（建议收敛）**：API 只出 `rel_type`，DATA 两列同值。api 身份建议删 `rel_code`（C10）；保留则声明不出参、不进指标。种子中文码若撞三枚举须 seed 跳过（C11）。
5. **`client_batch_id`（基本一致，边界待补）**：必填（changes）/选填（publish）/唯一（允许多 NULL）/历史 NULL 三册一致；缺 publish 缺省语义与 rejected 幂等两种边界要补（C4/C5）。ENT FE 必填属 API §9-E3 的追认项。
6. **`operator` / `operator_display`（可算，来源待补）**：规则可实现；DATA 需补 `operator` 取值来源（C3）。`kind='seed'` 时 DATA 写 `operator='seed'`，API 规则里写的是 `operator='system'`，因 `kind` 先命中不影响显示，但建议统一成一个词。新 ENT 保存署名从 `'py'` 变用户名，列入 ENT 追认（C8）。
7. **`tech_edges` 字段（齐全）**：`id/src/dst/rel_type/strength_manual/time_range/source/status` 均有列；`strength_auto` 不出参（C15）；开放时间区间不要复制 `_edge_dict` 的 from/to fallback（C14）；`status` 只回 active 一致。
8. **版本可回滚（可算）**：`graph_snapshot` PK=`version_id`、每版一行，历史 ENT 无行 → `rollbackable=false`、`reason=no_snapshot` 可实现；DATA “N=1”措辞要写清“每版保留、不裁剪”（C16）。
9. **回滚预览 vs 版本 stats（易错）**：preview counts = 目标快照 vs 当前求差；版本 stats = 该版本自身改动。二者同“键”不同“数据”，METRIC C1 已按此纠正；API §3.4 只需强调“同一套键”。
10. **错误码（基本一致）**：50301 退役、member 缺表静默、1213/1205→409、SQL→500 三册一致；1062 在 DATA 二义（C9），API §7 的 409/422 分法以 C9 为准。50303 只属 Java 层，DATA 不涉及。
11. **API 册自查项（不属本次审稿，交付协调方）**：API §5.1 补“`tech_edges.src/dst` 对应 `nodes[].technology_id`（现节点已带该字段）”；API §9 补 `impact` 新字段与 `operator` 注入两条 ENT-API 追记；API §3.4/§4.3 视 C7 决定是否给 `tech_edges` 增 `updated`；API §3.3 补 publish 缺省 batch 与 rejected 语义（与 C4/C5 同步）。

---

## 四、需监管人拍板

| # | 事项 | api 身份意见 | 来源 |
|---|---|---|---|
| 1 | 名称唯一键改造是否需数据平台 Owner 书面确认 | 改造本身**必须做**（active-only 是改名/新建查重的前提，否则 1062 会变 500）；流程上至少“监管人书面 + 执行前备份 + 变更窗口”，是否再要数据平台 Owner 由监管人定；因是 ENT/GRAPH 共用 demo 库，**建议要** | DATA:649-652、DATA:677 |
| 2 | `rel_code` 保留还是删除 | **建议删**；API 不返回，auto 行与 `rel_type` 同值，保留只增列和同步成本。若为将来统一类型口径留原文，可保留但必须声明内部字段 | DATA:675 |
| 3 | 快照阈值（2000 行/8 MB/单表 50000）与 `--all` 硬禁用 | 接受；请同时拍“每版保留一份、不裁剪”，并确认存储增长可接受（当前工作集 1 点/61 边，远低于阈值） | DATA:678、DATA:461-463 |
| 4 | 回滚整表还原语义（V 后新增消失、V 后删除复活） | 接受，与 API preview 语义一致；确认框文案按“将变更 X 项（恢复 A / 撤回 B）”更准确，建议 PRODUCT/FE 同步 | DATA:367、DATA:679；API:285 |
| 5 | DN-A03-09 豁免范围一次裁全 | 建议一次裁定；若按本单补回滚 `results`，范围为**七类**；未裁前维持“建议豁免”，界面不挂 ⓘ/MockBadge | METRIC:220；API-METRIC-C2 |
| 6 | 删点/删种子边后全景可见集合变小，是否知会 DS02 监管人 `human:淮政玮` | 建议知会（低成本、防已签收页面数字被质疑），不阻断本叶 | METRIC:221 |
| 7 | ENT 追认包 | 由 ENT-API / ENT-DATA 原审稿身份确认：`operator` 署名变化、`stats` 结构、`client_batch_id` 必填、`impact` 新字段、快照 payload 变化；确认前不派 PY-IMPL | DATA:656、API:478 |
| 8 | `tech_edges` 是否暴露 `strength_auto` | 默认不暴露（人工强度才是编辑值）；若产品要显示存量边权重，需 API 增字段、DATA 列不变 | API-DATA-C15 |

---

*会签：`agent:api-agent` · 2026-11-13 · 只读核对，未改任何其他文件、未 git、未连库*

## 复核（2026-11-13 api-agent）

> 对象：`TS-L2-M10-GRAPH-DATA.md` v2、`TS-L2-M10-GRAPH-METRIC.md` v2；口径基准：`会签/TS-L2-M10-GRAPH-L2-裁定.md`（A1–A8 / B1–B20）。只读复核，只追加本节。

### 一、DATA v2 逐条

| 条件 | 结论 | 说明 / 证据 |
|---|---|---|
| API-DATA-C1 stats 键 | **闭合** | §5.2 已改分组 JSON（DATA:353-367），seed 版本同结构（DATA:469），`stats` 列注释同步（DATA:671-677），历史行不回填（DATA:242）。 |
| API-DATA-C2 `kind` 语义 | **闭合** | `kind` 明确为动作类型，`ent` 仅历史回填，新保存（含 ENT 页）一律 `save`，且禁止依赖默认值（DATA:181、DATA:336、DATA:749）。 |
| API-DATA-C3 `operator` 来源 | **闭合** | §5.2 步骤 2 已 SELECT `operator`，步骤 6 取 `change_set.operator`；§5.3 回滚取 `body.operator`（DATA:334-336、DATA:377-378）。 |
| API-DATA-C4 publish 幂等三态 | **闭合** | 带 batch 不符→409；不带且已 published→原回执；rejected→409（DATA:423-425）。 |
| API-DATA-C5 submit rejected / ops 不同 | **闭合** | 命中 rejected→409；同 batch 但 ops 不同→409（DATA:417-420）。 |
| API-DATA-C6 回滚顺序 / 生成列 | **闭合** | `technology_master` 改先删全表再显式 `technology_id` 插入，排除 `name_cn_active`、`updated_at`；payload 显式列同步（DATA:388-389、DATA:273）。 |
| API-DATA-C7 求差口径 | **闭合** | active 判存在、`technology_id`/`edge_id` 行键、排除 `version_id`/`updated_at`/生成列；preview 与 rollback 同一函数；`tech_edges.updated` 已定义（DATA:365、DATA:374-376）。 |
| API-DATA-C8 ENT 追记 | **闭合** | §11 新增 13–17 行：operator 署名、stats 结构、名称唯一性放宽、impact 两字段+Nebula 只读、快照 payload/单测文档（DATA:751-765）。 |
| API-DATA-C9 1062 映射 | **闭合** | 名称 1062→422/42201；`graph_tech_edge` 1062→409/40901 整笔回滚；不再落 `failed_items`（DATA:405-409）。 |
| API-DATA-C10 删 `rel_code` | **闭合（按裁定撤回建议）** | 裁定 B4 保留用于已删存量边过滤；DATA 已写明“不参与唯一键/指标/接口出参”（DATA:74-86）。接口层无异议，撤回删除建议。 |
| API-DATA-C11 rel_type 长度 / 中文码 | **闭合** | 已放宽 `VARCHAR(64)`（DATA:74），种子对中文三枚举/非 ASCII 白名单外码跳过并计数（DATA:447）。 |
| API-DATA-C12 出参 number | **闭合** | `src/dst`、`strength_manual`、`layout_x/y` 均定为 JSON number，不做字符串化（DATA:117）。 |
| API-DATA-C13 复活范围 | **闭合** | 明确已删种子行不可达，复活仅同键人工行（DATA:109-111）。 |
| API-DATA-C14 开放时间端 | **闭合** | `time_to` 选填、种子不补 `to`（DATA:80-83、DATA:468）；API 同步允许 `{from,to:null}`。 |
| API-DATA-C15 `strength_auto` 不出参 | **闭合** | 列注释与 §2.5 均写明不出参、不进任何指标（DATA:79、DATA:88）。 |
| API-DATA-C16 N=1 措辞 | **闭合** | 已改“每版一份、按 `version_id` 保留、不裁剪”，附存储增长说明（DATA:59、DATA:276、DATA:671-673）。 |
| API-DATA-C17 rollback results | **闭合** | `succeeded=实际应用差异条数`、`failed=0`、与 preview `counts.total` 同源（DATA:381）。 |
| API-DATA-C18 级联删边 change_log | **未闭合（编辑性）** | 现文写“各写一行 ... `reason='cascade'` 的 change_log”（DATA:341），但 `graph_change_log` **没有 `reason` 列**（DDL:38-50）。改法：删去列引用，改为“`after` JSON 内含 `reason:"cascade"`（或 `before/after` 旁注）”；不新增列、不改 DDL。其余（`object_type='tech_edge'`、`op='delete_edge'`、`node_id_map` 只取 `add_node`）已闭合。 |
| API-DATA-C19 layout 权威 / payload 主键 | **闭合** | master 为权威、发布覆盖 ADS 并给重刷路径（DATA:141-143）；显式列清单含各表主键（DATA:273）。 |

**DATA v2 新引入问题**：除 C18 的 `reason` 列引用外，未发现新的接口/数据面问题。另建议（不阻塞）删除 §5.2 与 §12-1 的“若 API 最终不含 `updated` 则移除”条件句——API v2 §3.4 已正式含 `tech_edges.updated`，保留条件句会让实现方误删子键（DATA:365、DATA:766；API:218）。

**DATA 结论：同意会签。** C1–C9 全部闭合；唯一未闭合项 API-DATA-C18 属建议级编辑修正（`reason` 落 `after` JSON，不新增列），不作为会签前置。

### 二、METRIC v2 逐条

| 条件 | 结论 | 说明 / 证据 |
|---|---|---|
| API-METRIC-C1 同源误述 | **闭合** | 已改“同一套分组键 + 同一个快照求差函数，不是同一份数据”，并明确 40-4 是该版本自身 stats、40-3 是快照 diff（METRIC:124、METRIC:85-86）。 |
| API-METRIC-C2 漏 rollback results | **闭合** | 已扩为七类，新增 rollback `results`，§1.3/§3.1-5/§7-1 同步（METRIC:98、METRIC:117、METRIC:145、METRIC:246）。 |
| API-METRIC-C3 分组键矩阵 | **闭合** | 已逐组列键，不再“各拆增/删/改”，并给出 added/removed/updated 的双向语义与 total（METRIC:114）。 |
| API-METRIC-C4 `counts:null` | **闭合** | 明确为合法态：200、不显示分组计数、显示 `not_rollbackable_reason` 中文原因并置灰（METRIC:122）。 |
| API-METRIC-C5 列名 | **闭合** | §3.2 已改 `layout_x/layout_y`（METRIC:152、METRIC:259）。 |
| API-METRIC-C6 历史 stats | **闭合** | 四种旧形状原样显示、缺组不补 0（METRIC:126、METRIC:116）。 |
| API-METRIC-C7 total 文案 | **闭合** | 已改「将变更 X 项（恢复 A / 撤回 R / 还原 U）」，并说明 total 含三类（METRIC:114、METRIC:123）。 |
| API-METRIC-C8 39-1 前端本地 | **闭合** | 明确前端草稿净差 op 条数，`validate.op_count` 仅预览（METRIC:113）。 |
| API-METRIC-C9 results 持久化/null | **闭合** | 已写随 `publish_results` 持久化、历史 null 不显示逐条、failed_items 不聚合（METRIC:116-117）。 |

**METRIC v2 新引入问题（均为文字同步，不阻塞）**：
1. METRIC:148 仍写“现 `VARCHAR(32)`，API-DATA-C11 建议放宽至 64”，但 DATA v2 已是 `VARCHAR(64)`（DATA:74）。改法：改为“DATA v2 已为 `VARCHAR(64)`”，或直接删列宽括注。
2. METRIC:114、METRIC:248 仍把 `tech_edges.updated` 写成“若 API 补/是否补键”，但 API v2 §3.4 已正式包含该子键（API:218）。改法：`tech_edges{added,updated,removed}`，§7-3 改为“键已定，实现单写死函数落点”。

**METRIC 结论：同意会签。** C1–C4 全部闭合；两项为旧表述同步（列宽、updated 条件句），不构成会签前置。

### 三、跨稿一致性复核（补充）

- `stats`：DATA / API / METRIC 三稿现均为分组 JSON；DATA 与 METRIC 各留一处“若 API 不含 updated”的条件句，API v2 已含，建议同步删除（不影响闭合）。
- `layout_x/y`：DATA 与 API 已一致；METRIC 列名已改，仅列宽括注残留旧值。
- `client_batch_id`：DATA §3.5 已落 A7（可缺省、服务端生成、不享重试幂等），API v2 §1/§3.1/§9-E3 一致。
- `rel_code`：按 B4 保留、不出参；DATA 与 API 一致，接口无异议。
- `reason`：`change_log` 无该列，DATA 需按 C18 改法落 `after` JSON；API 版本详情不依赖独立 `reason` 列，无需联动改 API。

*复核：`agent:api-agent` · 2026-11-13 · 只读，仅追加本节*
