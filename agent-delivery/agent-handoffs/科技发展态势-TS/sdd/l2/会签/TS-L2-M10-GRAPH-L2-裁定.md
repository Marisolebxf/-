# TS-L2-M10-GRAPH 二级分册 · 会签裁定单

- 日期：2026-11-13
- 适用：`TS-L2-M10-GRAPH-API.md` / `TS-L2-M10-GRAPH-DATA.md` / `TS-L2-M10-GRAPH-METRIC.md` v1 → v2
- 会签单：`会签/TS-L2-M10-GRAPH-L2-SIGNOFF-{ARCH,API,DATA,ALGO,PRODUCT}.md`（五个身份，均为有条件同意、无驳回）
- 本单分两部分：A 是监管人拍板，B 是协调方（arch / coordinator）对跨稿冲突的统一口径。三稿 v2 必须与本单一致；对本单有异议的，在稿内「会签回应」里写明理由，交监管人

## A. 监管人拍板（`human:刘剑锋`，2026-11-13）

| # | 事项 | 结论 |
|---|---|---|
| A1 | 名称唯一键改造（DROP `uk_name_cn` → 生成列 `name_cn_active` + 唯一索引）是否需数据平台 Owner 书面确认 | **不需要**。监管人定；DDL 由监管人执行前备份 |
| A2 | SEED-L01 种子切片 | **候选 #2「人工智能 / 大模型」**：按加权度取前 50，作演示默认；#1（ENT 现有点一跳）只做回归，#3 只做压测；执行前 dry-run 报点数、边数、distinct relation_type、丢弃数 |
| A3 | 34 / 38 的「技术分类」 | **维表下拉，空则手填**：选项来自 `dim_tech_domain`，维表为空时允许手填；后端只校验非空和长度 ≤64，不做外键；存中文名。演示分类清单由 DATA 在 SEED-L01 里给一版（分类体系选型仍是甲方待定项 OI-C02-02） |
| A4 | 快照阈值 | 8 MB / 主表 active 2000 / 总行 50000；种子禁用 `--all`；每版快照都保留，不裁剪 |
| A5 | 错误码 50303 | 新增，表示下游不可达，仅 Java 层（display / topic `relayStatus`）使用；作为 ARCH §7 的增补 |
| A6 | 36-3 时间范围 | **改为选填**（需规原文是「可设置」） |
| A7 | `client_batch_id` | `changes` 可缺省，缺省时服务端生成，不享受重试幂等；ENT 前端 FE-TS-10C 不强制改，建议后续补上 |
| A8 | DN-A03-09 豁免范围扩到七类计数 | 这是 PM / 数据 Lead 的口径，协调方写请示单由监管人转交；回执前，METRIC 册写「按 DN-A03-09 建议范围，待 PM / 数据 Lead 确认」，不阻塞会签 |

## B. 跨稿统一口径（协调方裁定）

| # | 冲突 | 裁定 | 来源条件 |
|---|---|---|---|
| B1 | `stats` 形状 | **以 API §3.4 的分组 JSON 为唯一口径**，分组键：`tech_nodes` / `tech_edges` / `entity_links` / `entity_edges` / `entity_attrs`，每组内按 API 键矩阵列键。DATA §5.2 的扁平键（`node_add` 等）作废；种子版本、回滚版本同结构；`stats` 列注释同步改。历史版本**不回填**；前端兼容四种旧形状：`{"ops":N}`、旧扁平键、`{}`、NULL | ARCH-API-C2、ARCH-DATA-C1、DATA-API-C2、API-DATA-C1、ALGO-API-C3、ALGO-DATA-C3、PROD-API-C5/C6、PROD-DATA-C3 |
| B2 | 坐标列名 | `technology_master.layout_x / layout_y`、`graph_entity_node.layout_x / layout_y`（DATA DDL 为准）；API、METRIC 措辞同步 | ARCH-API-C1、DATA-API-C1 |
| B3 | 35-3 的 Nebula 计数通道 | entan-py 自有 Nebula 只读会话，显式 `USE demo_gkx_chain`，只做 MATCH / 计数；不走 chainan（`chain_space()` 未打进 entan 镜像） | ARCH-API-C3、ALGO-API-C2 |
| B4 | `rel_code` | **保留**（存种子边原关系码），用于全景过滤已删存量边：过滤用 `rel_code`，为空时回退 `rel_type`。API 不返回它 | ARCH 拍板④、ALGO-DATA-C5、API-DATA-C10（不采纳删除） |
| B5 | 种子关系码 | 种子不写中文三枚举：`relation_type` 若为「包含 / 依赖 / 促进」之一，跳过并记数；同时丢弃自环、已删端点、缺端点的边 | ALGO-DATA-C1、C4 |
| B6 | 人工边的 `evidenceLevel` | 人工边**不带** `evidenceLevel`（否则 Java `lowEvidence` 会误删，也等于伪造证据等级） | ALGO-API-C1 |
| B7 | src / dst 出参类型 | 出参保持 number（int），与 `/current` 现有 `technology_id` 一致，不做字符串化；全景叠加里的 id 仍按 ARCH §4.2 映射成字符串 | ARCH 跨稿、API-DATA-C12 |
| B8 | 同一对点上的 auto 边与 manual 边 | 允许并存（两者类型集合不相交，不会同键）；界面分别标「存量」「人工」 | ALGO 拍板① |
| B9 | `strength_auto` | 不出参；METRIC §3.2 黑名单补 `graph_tech_edge.strength_auto`，不得照抄 `graph_entity_edge`「指标只取此列」的注释 | ARCH-METRIC-C1、DATA-METRIC-C1、API-DATA-C15 |
| B10 | 唯一键冲突 1062 | 名称冲突 → 422 / 42201；`graph_tech_edge` 冲突 → 409 / 40901，整笔回滚 | API-DATA-C9 |
| B11 | publish 的批次判定 | 带 `client_batch_id` 且与变更集不符 → 409；不带 → 若已 published，返回原回执；变更集已 rejected → 409。submit 按批次命中 rejected → 409；同一批次、ops 不同 → 409 | ARCH-API-C2、API-DATA-C4/C5 |
| B12 | 40-3 与 40-4 的「同源」 | 改为：**同一套分组键 + 同一个快照求差函数**。回滚预览的计数 = 回滚生成的新版本的 stats；它不等于目标版本自己的 stats | DATA-METRIC-C4、API-METRIC-C1、PROD-METRIC-C3 |
| B13 | 回滚还原 `technology_master` | 先整表删除，再按快照插入（带显式 `technology_id`）；排除生成列 `name_cn_active` 与 `updated_at`；求差按 active 判断存在，按 `technology_id` / `edge_id` 比对，排除 `version_id`、`updated_at`；回滚预览与回滚用同一个求差函数 | API-DATA-C6/C7、ALGO-DATA-C2 |
| B14 | 种子边 `time_range` | 允许开放端 `{from, to: null}`，或整体省略；不补 `to` | DATA-API-C3、API-DATA-C14 |
| B15 | `tech_edge_count` | 只数 `status='active'`，两个方向都算 | DATA-METRIC-C3 |
| B16 | `kind` | `ent` 只用于历史回填；新保存（含 ENT 页）一律 `save`；`rollback` / `seed` 各写各值 | API-DATA-C2 |
| B17 | `graph_version.operator` | 保存取 `change_set.operator`；回滚取 display 注入的 operator | API-DATA-C3 |
| B18 | ENT 追记 | API 与 DATA 两册的「对 ENT 的追记」必须包括：display / topic 单测里的 50301 断言、publish 签名、7 op 白名单；operator 署名由 `py` 改为用户名；stats 结构；名称唯一性放宽；impact 两字段与 Nebula 只读依赖；快照 payload 新增表与列 | ARCH-API-C4、ARCH-DATA-C2、API-DATA-C8 |
| B19 | 用户可见文案 | 所有英文码（kind、`not_rollbackable_reason`、stats 分组、`snapshot_status`）在接口层给中文显示值或在 API 册给中文对照表；版本详情 `changes[]` 给中文摘要；回滚确认框写清双向语义（目标版本之后新增的会消失、之后删除的会恢复、修改的会还原），`added=恢复`、`removed=移除` 不能译反 | PROD-API-C1/C2/C4、PROD-DATA-C1/C2 |
| B20 | 「人工」标识 | 36-3 弹窗字段标「关系强度（人工）」；画布悬浮和详情标「人工」；不挂 ⓘ | PROD-API-C7、PROD-METRIC-C1 |

其余条件（单稿内部的必修与建议）由各起草方逐条回应。
