# TS-L2-M10-GRAPH 二级分册会签 — 架构身份

| 项 | 内容 |
|---|---|
| 审稿身份 | `agent:arch-agent`（独立会话） |
| 日期 | 2026-11-13 |
| 会签级别 | 二级分册会签（v1 草稿） |
| 审稿对象 | `TS-L2-M10-GRAPH-API.md`（api-agent）<br>`TS-L2-M10-GRAPH-DATA.md`（data-agent）<br>`TS-L2-M10-GRAPH-METRIC.md`（algorithm-agent） |
| 架构基线 | `TS-L2-M10-GRAPH-ARCH.md`（2026-11-13 由 `human:刘剑锋` 签收；§11 四项拍板：关系类型三枚举可扩、删 ENT Nebula 投影走单事务、名称唯一键只约束 active、叠加失败非阻塞提示） |
| 参考 | 会签往返 `会签/TS-L2-M10-GRAPH-SIGNOFF-{API,DATA,ALGO,PRODUCT}.md`、`产品实现规程.md` §4.2.4、`.cursor/skills/gkx-fde-design-change/审稿硬清单.md`、`00-team-constitution.mdc`、`agent-delivery/architecture-baseline.md`、ENT 先例、as-built 代码 |
| 监管人 | `human:刘剑锋` |
| 范围 | **只读**：未改任何稿件/其他文件，未改 task-registry，未 git，未连库 |

## 0. 结论概览

| 稿件 | 结论 | 必修 | 建议 |
|---|---|---|---|
| `TS-L2-M10-GRAPH-API.md` | **有条件同意** | 4（C1–C4） | 2（C5–C6） |
| `TS-L2-M10-GRAPH-DATA.md` | **有条件同意** | 2（C1–C2） | 3（C3–C5） |
| `TS-L2-M10-GRAPH-METRIC.md` | **有条件同意** | 1（C1） | 2（C2–C3） |

三份对 ARCH 方向（单事务/删 Nebula 写/active-only 唯一键/整图回滚/叠加非阻塞）忠实，铁律无违反（详见 §6）。条件集中在：**跨稿字段冻结不一致**、**35-3 只读计数通道偏离已签条件**、**ENT 共用面追记漏单测**、**METRIC 黑名单漏 `strength_auto`**。均属可闭合项，无驳回。

---

## 1. `TS-L2-M10-GRAPH-API.md`（agent:api-agent）

**结论：有条件同意。** 接口契约对 ARCH §2/§3/§4/§7 与 §11 拍板忠实，错误码、版本端点、`/current` 增量、叠加字段均落到位。四处必修：坐标列名与 DATA 不一致、stats 形状与 publish 幂等措辞、35-3 Nebula 通道偏离已签 N2、ENT 单测未追记。

| 编号 | 级别 | 位置 | 问题 | 要求 | 依据 |
|---|---|---|---|---|---|
| ARCH-API-C1 | 必修 | §2.1 `add_node.layout` 行 | 写「落 `technology_master.x/y` 与 ADS `graph_entity_node.x/y`」，但 DATA 定列与 DDL 实为 `layout_x` / `layout_y`。按现文实施会写出不存在的列。 | 改为 `technology_master.layout_x/layout_y`、`graph_entity_node.layout_x/layout_y`；§5.1 `layout` 出参可保留 `{x,y}` 对象，但注明源列。 | API `:79`；DATA `:133-134`、`:164-165`、`:561-562`、`:574-575`、`§8 B1/C` |
| ARCH-API-C2 | 必修 | §3.4 `stats` 规范键（`:180-196`）、§3.3 publish（`:171`）、§7 409 行（`:416`） | ① `stats` 采用嵌套分组键（`tech_nodes{added,updated,removed}` 等），而 DATA §5.2 落成扁平键（`node_add/...`）且自述「交 API 定名」——两稿冲突，实现必分叉。② §3.3 写「变更集已 published 时幂等返回、不报 409」为无条件，§7 又写「published 但批次不符 → 409」，同稿自相矛盾；DATA §7.5 以「published 且批次匹配」为准。 | ① 冻结一套（建议采本册嵌套分组，语义更清），DATA §5.2 与 §8 注释同步；历史扁平键按 §3.4 保留原样不补 0（Q7 口径）。② §3.3 补限定：「同 `client_batch_id` 或未传 → 幂等返回；传入不同 batch → 409」，与 §7、DATA §7.5 对齐（ARCH §1-8 为「按批次幂等」，此限定不改变基线语义）。 | API `:180-196`、`:171`、`:416`；DATA `:338`、`:386`；ARCH `:82` |
| ARCH-API-C3 | 必修 | §5.2 `panorama_hidden_relation_count` 行 | 写「走 chainan 图谱只读通道，space 由 `chain_space()` 强制 `demo_gkx_chain`（`vendor/innov-py/chainan/...`）」。但 35-3 `impact` 运行在 **entan-py**，`chainan` 未 vendored 进 entan-py（`vendor/entan-py` 仅 `entan/innov/polan`），`chain_space()` 是 lumen-algo-py 全景读（`lumen_common/algorithms/tech_graph_read.py:14`）的路径，impact 端点不可达；且 API-C12/N2 已签「保留 entan Nebula 客户端，显式 `USE demo_gkx_chain`」。现文与已签条件及 ARCH §2 冲突。 | 改为：用 entan `entan.common.nebula` 的 `execute/rows`，会话内显式 `USE demo_gkx_chain`，双向 MATCH + `evidence_level IN [HIGH,MEDIUM]`，超时/失败 `null`；删除 chainan/`chain_space` 引用（或仅作「口径参照」注记，不作实现通道）。 | API `:354`；ARCH `:73`；`会签/…-SIGNOFF-API.md:151`、`:208`（N2/API-C12）；`vendor/entan-py/entan/common/nebula.py:31-34`；`lumen_common/algorithms/tech_graph_read.py:14` |
| ARCH-API-C4 | 必修 | §9「对 ENT-API 的追记」 | E1–E10 覆盖契约/前端，但**无单测追记行**。改发布签名（publish 加 body）、改 50301→50303、7 op 白名单放开，均会使现有 ENT 单测失败，签收后若不改会卡 CI。 | §9 增一行（或在 §10 注记）：「ENT 共用单测更新」：`SituationMaintainEntControllerTest:49`（50301 断言→50303）、`:70`（`publish("cs-1")` 签名）；`TechGraphMaintainControllerTest:72`（add_node/add_edge/delete_edge 由 400 改放行）、`:129/:137/:149`（50301 断言）、`:135`（publish 签名）；`PanoramaReadAssemblyTest` 补 `overlay` 与键集断言。**确认前不派 PY-IMPL** 的闸门应含单测。 | API `:480-493`；`repos/lumen-svc-platform/gkxlumen-display/src/test/java/.../SituationMaintainEntControllerTest.java:49`、`:70`；`gkxlumen-topic/src/test/java/.../TechGraphMaintainControllerTest.java:72`、`:129`、`:135`、`:137`、`:149` |
| ARCH-API-C5 | 建议 | §7 错误码表、§9-E10、§10-Q5 | 新增 `50303`（下游不可达）。ARCH §7 已冻结码位清单（`40001/40401/40901/42201/50001/50302`，50301 退役），未含 50303。虽合理，但属基线外新增码，需监管人确认（见 §5-1）。 | 保留本册提案，但 §7 标注「ARCH §7 增补，待监管人确认」；确认前不宣称「已冻结」。 | ARCH `:235`；API `:420`、`:491`、`:503` |
| ARCH-API-C6 | 建议 | §4/§6 路径参数 | 同一路径参数三处写法不一：`{version_id}`（`:241/263/289`）、`{versionId}`（`:387/388`）、`{id}`（`:402`）；`change_set` 亦然。 | 全文统一为 `{version_id}` / `{change_set_id}`（与 §4 标题、DATA/Java 侧一致），§6 表格同步。 | API `:241`、`:263`、`:289`、`:387-388`、`:402` |

---

## 2. `TS-L2-M10-GRAPH-DATA.md`（agent:data-agent）

**结论：有条件同意。** 数据落点写死完整：新表、软删占键/复活、active-only 名称唯一键、`kind/snapshot_status/publish_results`、N=1 快照与 INSERT 前预判、加锁单事务写序、种子与 `--all` 禁用、D12 demo 库口径均有据；§12 自列开放点多数已在册内给出默认。两处必修：stats 键与 API 冲突、ENT 单测追记缺失；另有三条建议。

| 编号 | 级别 | 位置 | 问题 | 要求 | 依据 |
|---|---|---|---|---|---|
| ARCH-DATA-C1 | 必修 | §5.2「stats 固定键」 | 定成扁平键 `node_add/node_del/node_upd`、`tech_edge_add/...`、`entity_link_add/...` 等，并注「交 API 定名」；与 API §3.4 嵌套分组键直接冲突，且 as-built 发布 `stats` 亦为扁平（`{+node,-node,+edge,-edge}`）。三处形状不一，落库/前端/回滚预览会分叉。 | 与 ARCH-API-C2 同一裁定：改用 API §3.4 嵌套分组键；§5.2 与 §8 DDL 注释同步；历史 ENT 版本保留旧键、原样返回不补 0。 | DATA `:338`；API `:180-196`；`tech_graph_maintain_routes.py:843-844` |
| ARCH-DATA-C2 | 必修 | §11「对 ENT-DATA 的追记」 | 12 行覆盖发布事务/删投影/加列/快照/名称键/批次键/双表/审计等，但**无单测/文档同步行**。发布签名、50301 退役、7 op 放行、`/current` 新键会破坏 ENT 单测与 README/契约文档；不追记则 ENT 面签收后无人认领。 | §11 增行：「ENT 共用单测与文档更新」——同 ARCH-API-C4 所列三处测试，加 `storage/ENT/stores/mysql/ads.md` + `CHANGELOG.md` 登记新表/新列、ENT-DATA 正文与 ENT 会签单追认。 | DATA `:654-671`；测试行号同 ARCH-API-C4 |
| ARCH-DATA-C3 | 建议 | §3.4 / §8 D `graph_version.kind` | `kind VARCHAR(16) NOT NULL DEFAULT 'ent'`：写入方若漏传 `kind`，新 save/rollback/seed 会被静默标成 `ent`，污染版本类型与 `operator_display`（「系统（历史）」误显）。 | 去掉 `DEFAULT 'ent'`（NOT NULL 无默认，强制显式写入），或保留默认但在 §5.1/§5.3 写死「所有 INSERT 必显式 `kind`」并加断言；历史回填仍走 §8-H 的 `UPDATE`。 | DATA `:175`、`:579`；API `:308-312`（operator 显示） |
| ARCH-DATA-C4 | 建议 | §12-1 `rel_code`、§2.1 | 同时保留 `rel_type`（参与唯一键）与 `rel_code`（auto 原文），drafter 请 API/ALGO 表态是否冗余。架构意见：**保留两列可接受**——`rel_type` 承担生效类型与唯一键，`rel_code` 保存种子原文，未来统一码表时不丢信息；当前同值不构成指标风险。 | 若无监管人要求精简，按保留落；在 §2.1 补一句「`rel_code` 仅供追溯，不参与唯一键/指标/读侧过滤」。 | DATA `:78`、`:89`、`:675` |
| ARCH-DATA-C5 | 建议 | §12-2 端点类型 | `src/dst` BIGINT（内部 `technology_id`），API `/current.tech_edges[]` 出参为 JSON number（`src:number`），与既有 `graph_entity_edge.src` VARCHAR 不同。属跨稿口径，非数据身份问题。 | 采纳 API 已冻结的 number 出参；DATA §12-2 改为「已确认：输出 JSON number，不做字符串化」并关闭。 | DATA `:676`；API `:469`、`:326-330` |

---

## 3. `TS-L2-M10-GRAPH-METRIC.md`（agent:algorithm-agent）

**结论：有条件同意。** 34–40 为人工编辑器、不挂 `metric_id` 的判断与 ARCH §9/ALGO-C5 一致；六类计数归 DN-A03-09 建议豁免、`strengthManual`/`timeRange`/`rel_type`/`source` 的 D9 护栏、S4/weighted_degree 身份不翻案、`--check` fixture 保护均到位。一处必修：字段黑名单漏 `strength_auto`。

| 编号 | 级别 | 位置 | 问题 | 要求 | 依据 |
|---|---|---|---|---|---|
| ARCH-METRIC-C1 | 必修 | §3.2 字段黑名单 | 现列 `strength_manual`、`time_from/time_to`、`rel_type`、`source`，**漏 `graph_tech_edge.strength_auto`**。DATA 明确新增该列并在 §12-6 请求「METRIC 确认不被任何指标消费」。漏项会使「auto 原强度快照」成为未设护栏的字段。 | §3.2 增一行：`graph_tech_edge.strength_auto`（auto 原强度快照）——任何指标/分数脚本不得读取；不映射 `weight`/`strength`/S4；人工强度只走 `strength_manual`。 | METRIC `:135-138`；DATA `:79`、`:680`；ARCH `:268` |
| ARCH-METRIC-C2 | 建议 | §3.3 计数表第 5 行、§3.5 第 4 条 | 两处称「`graph_version.stats` 固定键」但未钉形状；ARCH-DATA-C1/ARCH-API-C2 冻结后若不引用具体键，前端「+2 点 / -1 边」与回滚预览可能各读一套。 | 待 stats 形状冻结后，§3.3 第 5 行与 §3.5-4 改为「读 API §3.4 冻结的分组键」，并保留「预览与版本列表同源」要求。 | METRIC `:108`、`:116`；API `:180-196` |
| ARCH-METRIC-C3 | 建议 | §3.5 S4 种子守护（`:159`）、§7-4 | 对 `seed_technology_panorama_score.py` 的守护目前只有文档约束（只扫 Nebula、不读 `technology_master`/`graph_tech_edge`、不消费带 `overlay` 结果），无运行时断言。 | 本次可按文档约束签收；建议在实现单加轻量断言/白名单（拒绝工作集表名与 `overlay` 键），作为技术债登记，不阻塞本叶。 | METRIC `:159`、`:223`；ARCH `:172`；`会签/…-SIGNOFF-ALGO.md` S2 |

---

## 4. 跨稿一致性

| # | 项 | API | DATA | METRIC | 裁定 |
|---|---|---|---|---|---|
| 1 | `stats` 键形状 | 嵌套分组（`:180-196`） | 扁平 `node_add/...`（`:338`） | 语义描述、未钉键（`:108`） | **冲突 → 必修**（API-C2 / DATA-C1）；冻结嵌套，DATA/METRIC 同步 |
| 2 | 坐标列名 | `x/y`（`:79`） | `layout_x/layout_y`（`:133-134` 等） | — | **冲突 → 必修**（API-C1）；以 DATA DDL 为准 |
| 3 | 35-3 Nebula 读通道 | `chainan`/`chain_space()`（`:354`） | 35-3 只读、`null` 不挡删（`:146` 签收） | HIGH/MEDIUM 口径（`:105`） | **冲突 → 必修**（API-C3）；回到 entan 客户端 + 显式 `USE demo_gkx_chain` |
| 4 | `client_batch_id` | changes 必填、publish 选填（`:37`、`:171`） | 可空+唯一、历史 NULL（`:586`） | — | 一致；仅 API §3.3 幂等措辞需收紧（C2） |
| 5 | publish 幂等 | §3.3 无条件不报 409（`:171`） vs §7 批次不符 409（`:416`） | published 且批次匹配才幂等（`:386`） | — | 同稿矛盾 → 必修（C2）；以「同批次/未传才幂等」为准 |
| 6 | 边 id 命名 | 入参 `edge_id`（`:113/:118`），出参 `id`（`:469`） | 列 `edge_id`（`:537`） | — | 一致（出入参键名不同属 REST 常规）；API §5.1 补一句出参 `id` = `graph_tech_edge.edge_id` |
| 7 | `src/dst` 类型 | 出参 number（`:469`） | BIGINT，`graph_entity_edge.src` 为 VARCHAR（`:676`） | — | 采纳 number 出参，DATA §12-2 关闭（DATA-C5） |
| 8 | 快照阈值 | 未重述 | 8 MB / 2000 / 50000、`--all` 禁用（`:264-299`） | — | 与 ARCH 一致；阈值本身待监管人确认（§5-3） |
| 9 | `kind` 枚举 | save/rollback/seed/ent（`:308-312`） | 同（`:175`） | — | 一致；DATA 默认值风险见 DATA-C3 |
| 10 | 叠加字段 | `origin:"manual"`、`strengthManual`、`timeRange`、`tm:{id}`（`:366-373`） | 双表覆盖、快照含软删（`:109`） | `strengthManual` 不进公式（`:125`） | 一致，无冲突 |
| 11 | 50303 | 新增（`:420`） | 未涉及 | 未涉及 | 基线外新增码 → 待监管人确认（§5-1） |
| 12 | `strength_auto` | 未涉及 | 新增、请 METRIC 确认不消费（`:680`） | 黑名单漏（`:135-138`） | **漏 → 必修**（METRIC-C1） |

---

## 5. 需监管人拍板

| # | 事项 | 现状/默认 | 需拍板点 | 涉及 |
|---|---|---|---|---|
| 1 | 新增错误码 `50303` | API 提案：下游不可达由 50301 改 50303；ARCH §7 码位清单未含 | 是否批准作为 ARCH §7 增补（或另选码位）；批准前不得称「已冻结」 | API `:420`、`:503`；ARCH `:235` |
| 2 | 名称唯一键改造的 Owner 确认 | DATA：生成列 `name_cn_active` + 唯一索引替换 `uk_name_cn`，非纯增量；建议数据平台 Owner 书面确认，demo 库可免 | demo 共享库是否免 Owner、按「监管人书面确认+备份+窗口」执行即可 | DATA `:646-651`、`:677` |
| 3 | 快照阈值与 `--all` 硬禁用 | 沿用 ARCH 草案 8 MB / 2000 行 / 50000 行；种子 `--all` 脚本层禁用 | 阈值是否足够、`--all` 硬禁用是否接受（种子全量约 1.9 万点/58.7 万边） | DATA `:264-299`、`:678` |
| 4 | `rel_code` 独立列保留与否 | DATA 落两列并请表态；架构意见倾向保留（DATA-C4） | 若监管人要求最小列，可合并为 `rel_type` 单列，需同步改唯一键与种子 | DATA `:78`、`:675` |
| 5 | DN-A03-09 豁免范围一次裁全 | METRIC 列六类计数按「建议豁免」表述，未裁前不挂 ⓘ/MockBadge | 属 PM/数据 Lead 裁定（非架构身份）；请一次裁全并在 ENT/METRIC 统一口径 | METRIC `:92-98`、`:220` |

> 说明：ARCH §11 四项拍板（三枚举可扩、删除 ENT Nebula 投影、active-only 名称键、叠加失败非阻塞）已覆盖本叶主要架构分歧，三稿均未发现需要推翻或新增架构决策的「隐变」；上表第 1–4 项为落地边界确认，第 5 项为 D9 政策裁定，不在架构身份权限内。

---

## 6. 附：铁律与 ARCH 基线符合性核对

| 铁律/基线 | 核对结果 | 依据 |
|---|---|---|
| Java 零 nGQL、只读 ADS | 成立。Java display/topic 只做 Feign 透传，版本读写与 Nebula 计数都在 Python | API `:205`、`:225`；DATA `:69`；ARCH `:69` |
| 单写者（entan-py） | 成立。所有写走 entan-py；algo-py 只读工作集（只读、带超时） | ARCH `:69`；DATA `§13` |
| 层级链不新开 | 成立。版本端点挂既有 `/topic/v1/tech/graph/**`，网关不路由；全景叠加在 algo-py 读路径 | ARCH `:34`、`:225`；API `§6.1-6.2` |
| D9 数据血缘 | 成立。34–40 不挂 metric_id；人工值/计数按 DN-A03-09 建议豁免；叠加人工值标「人工」 | METRIC `§2-§3`；ARCH `:272` |
| D12 demo/lumen 隔离 | 成立。DDL 落 `demo_gkxlumenx_*`，正式化到 `gkxlumenx_*` 另走 Owner；差异已记档 | DATA `§7`、`:646-651`；ARCH `§11` |
| D15 display 单入口 | 成立。对外 `/display/v1/situation/maintain-ent/graph/**`，topic 内部轨 | API `§6`；`RemoteTechGraphMaintainClient` |
| D18 不硬编码 mock | 成立。种子从 Nebula `demo_gkx_chain` 取数；S4 不消费工作集 | DATA `§6`；METRIC `:159`；ARCH `§2` |
| ARCH 拍板忠实度 | 成立。未见悄悄改架构/扩范围/漏拍板；唯一偏离为 API-C3 的 35-3 通道（与已签 N2 冲突，需回改） | 全文 |

---

*本文件为架构身份独立审稿意见，只读产出；未修改三份草稿、ARCH、ENT 册、task-registry，未 git，未连库。*
*审稿：`agent:arch-agent` · 2026-11-13 · 二级分册会签 v1*

---

## 复核（2026-11-13 arch-agent）

复核依据：三稿 v2 + `会签/TS-L2-M10-GRAPH-L2-裁定.md`（A1–A8 监管人拍板、B1–B20 统一口径）。逐条核对本单原条件与跨稿项：**原条件全部闭合；对裁定单无架构异议**；另列 2 条 v2 新引入的非阻塞问题。

### 一、原条件逐条

| 编号 | 结论 | v2 落点 / 证据 |
|---|---|---|
| ARCH-API-C1 | **闭合** | §2.1 改 `technology_master.layout_x/layout_y`、ADS 镜像；§5.1 `layout` 由 ADS 列组装、种子 `null`（API `:81`、`:392`） |
| ARCH-API-C2 | **闭合** | §3.4 冻结唯一嵌套形状并含 `tech_edges.updated`；§3.3 三态幂等（带不同 batch→409、未带/相同→原回执）；§7 409 行同步；DATA §5.5 一致（API `:185-187`、`:213-225`、`:468`；DATA `§5.5`） |
| ARCH-API-C3 | **闭合** | §5.2 改「entan 自有 Nebula 只读会话 + 显式 `USE demo_gkx_chain`」，明写「不得引用 chainan / `chain_space()`」（API `:402`） |
| ARCH-API-C4 | **闭合** | §9 增 E11「ENT 共用单测更新」，列 display/topic 具体测试行号、`PanoramaReadAssemblyTest`，闸门含单测（API `:551`） |
| ARCH-API-C5 | **闭合** | 50303 标注「ARCH §7 增补」并按裁定 A5 记已拍板、仅 Java 层（API `:461`、`:472`、`:567`） |
| ARCH-API-C6 | **闭合** | 路径参数统一 `{version_id}` / `{change_set_id}`（API `:433-440`、`:454`） |
| ARCH-DATA-C1 | **闭合** | §5.2 改 API §3.4 分组 JSON；§8-H `stats` MODIFY 注释同步；历史四种旧形状不回填、缺组不补 0（DATA `:353-367`、`:676-687`） |
| ARCH-DATA-C2 | **闭合** | §11 增第 17 行「ENT 共用单测 / 文档更新」，含三处测试、`stores/mysql/ads.md`+`CHANGELOG`、ENT 追认（DATA `:762`） |
| ARCH-DATA-C3 | **闭合** | 保留 `DEFAULT 'ent'` 仅为加列平滑 + 代码显式写 `kind` + 启动/单测断言新版本 `kind ∈ {save,rollback,seed}`（DATA `:181`、`:687`） |
| ARCH-DATA-C4 | **闭合** | 保留 `rel_code`，用途按 B4 扩为「已删存量边过滤」，不参与唯一键/指标/出参（DATA `:86`） |
| ARCH-DATA-C5 | **闭合** | 端点 number 出参，原 §12-2 关闭（DATA `§2.4`、`:769`） |
| ARCH-METRIC-C1 | **闭合** | §3.2 增 `strength_auto` 黑名单（禁止照抄实体边注释）；§3.1/§3.5/§3.4 全链路禁读、种子仅作快照（METRIC `:135`、`:146`、`:174`、`:182`） |

### 二、跨稿一致性项

| # | 项 | 结论 | 说明 |
|---|---|---|---|
| 1 | `stats` 键形状 | **闭合** | 以 API §3.4 分组为唯一口径（B1）；DATA/METRIC 同步 |
| 2 | 坐标列名 | **闭合** | `layout_x/layout_y`（B2），三稿一致 |
| 3 | 35-3 Nebula 通道 | **闭合** | entan 自有会话 + 显式 `USE demo_gkx_chain`（B3） |
| 4 | `client_batch_id` | **闭合** | changes 可缺省、服务端生成、不享重试幂等（A7） |
| 5 | publish 幂等 | **闭合** | 同 ^C2；API §3.3/§7 与 DATA §5.5 一致（B11） |
| 6 | 边 id 命名 | **闭合** | 入参 `edge_id`、出参 `id`，语义为同一 `graph_tech_edge.edge_id`（B7） |
| 7 | `src/dst` 类型 | **闭合** | 出参 number、不做字符串化；全景叠加 id 仍字符串映射（B7） |
| 8 | 快照阈值 | **闭合** | 8 MB / 2000 / 50000、每版保留不裁剪、`--all` 禁用（A4） |
| 9 | `kind` 枚举 | **闭合** | 新保存（含 ENT）一律 `save`，`ent` 仅历史回填（B16） |
| 10 | 叠加字段 | **一致** | `origin`/`strengthManual`/`timeRange`/`tm:{id}`/禁 `evidenceLevel`（B6） |
| 11 | `50303` | **闭合** | 作为 ARCH §7 增补，监管人 A5 已批 |
| 12 | `strength_auto` | **闭合** | 不出参、进指标黑名单（B9） |

### 三、v2 新引入问题（非阻塞，建议随实现单处理）

| 编号 | 位置 | 问题 | 改法 |
|---|---|---|---|
| ARCH-REV-N1 | API §5.2「启动断言 space 前缀 `demo_gkx_`，非该 space 直接拒」 | 措辞有歧义：entan `conf().space` 默认是 `entan`（`vendor/entan-py/entan/common/nebula.py:31-34`），若按**配置 space** 断言前缀会拒绝启动；`session(use_space=True)` 会自动 `USE` 配置 space（同文件 `:71-80`）。 | 明确断言对象是**查询目标字面量 `demo_gkx_chain`**（或 `GKX_CHAIN_NEBULA_SPACE`），不是 `settings.nebula.space`；并写明用 `session(use_space=False)` + 显式 `USE demo_gkx_chain`。证据：API `:402`。 |
| ARCH-REV-N2 | METRIC §2.2-4、DATA §5.2 注 | `tech_edges.updated` 已在 API §3.4 冻结为固定子键，两稿仍留条件句（METRIC「若 API 补 `updated` 则加」、DATA「若 API 最终不含则移除」），易使前端按 METRIC 漏取该组。 | 两处去掉条件句，直接列 `tech_edges{added,updated,removed}`。证据：API `:218`；METRIC `:114`；DATA `:365`。 |

### 四、复核结论

| 稿件 | 结论 |
|---|---|
| `TS-L2-M10-GRAPH-API.md` v2 | **同意会签**（ARCH-API-C1～C6 全闭合） |
| `TS-L2-M10-GRAPH-DATA.md` v2 | **同意会签**（ARCH-DATA-C1～C5 全闭合） |
| `TS-L2-M10-GRAPH-METRIC.md` v2 | **同意会签**（ARCH-METRIC-C1 闭合；ARCH-METRIC-C3 已按更严口径升级为必修并落 §3.4） |

对裁定单 A1–A8 / B1–B20：**无架构异议**。ARCH-REV-N1 / N2 为非阻塞实现注记，不构成返稿条件。

*复核：`agent:arch-agent` · 2026-11-13 · 只追加本节，未改其他文件*
