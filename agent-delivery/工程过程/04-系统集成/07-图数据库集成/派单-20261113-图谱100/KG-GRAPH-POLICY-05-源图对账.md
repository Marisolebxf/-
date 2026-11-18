# KG-GRAPH-POLICY-05 · 源图对账（只读，非补数执行记录）

日期：2026-11-17。结论和责任见 [政策线与空态裁定](KG-GRAPH-POLICY-05-政策线与空态裁定.md)。本轮写入=0，删除=0，未修改任何数据库数据。下表“排除”是补数计划前的原料排除，不冒充执行器运行后的“跳过”。

## 0. 徐滕强确认与旧快照溯源

2026-11-18，徐滕强确认 M12/M13/M14/M16 本期 C 档、`MISSING_STABLE_ID`；稳定 ID 补齐后重开补边。M19/M20 分别由 M01/M02 承载，不重灌。徐同意将 16 条原因码对照交 API-04 接入；不代表 API 或页面联调完成。

任务卡内旧值 `policy_entity=59,904 / policy_graph_edge=21,792 / policy_graph_node=19,677` 的可追溯位置是 `KG-GRAPH-POLICY-05` 任务卡 note，2026-11-17 补建时录入（MCP 查询显示当日约 16:29 更新）。**仓库内未找到载有这组三项旧值的独立快照文档，也未找到原查询语句、SQL 执行时间或数据源信息。** 因此旧快照的 SQL 不能被可靠转述。徐滕强协助核对环境说明时，可从这张任务卡 note 着手；不要把下方的本轮 SQL 误认作旧快照 SQL。

本轮同口径可复跑的 ADS 精确计数为：

```sql
SELECT COUNT(*) FROM gkxlumenx_ads.policy_entity;
SELECT COUNT(*) FROM gkxlumenx_ads.policy_graph_edge;
SELECT COUNT(*) FROM gkxlumenx_ads.policy_graph_node;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_entity;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_graph_edge;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_graph_node;
```

对应有库前缀、时间戳和结果行的完整查询归档为 [`02-schema-count-queries.json`](KG-GRAPH-POLICY-05/02-schema-count-queries.json) 与 [`02-schema-count-results.json`](KG-GRAPH-POLICY-05/02-schema-count-results.json)。

## 1. 应有与实有

本任务的“应有”须指有可靠源证据、满足关系语义、两端 Tag 存在的可入图集合，不能直接拿 ADS 全表行数当分母。

| 范围 | 源侧物理量/候选 | 本轮确认可直接入图 | 图中有效实有 | 对账结论 |
|---|---:|---:|---:|---|
| 政策点 | demo DWD 20,000 active、20,000 distinct ID | 本轮未重做全量点映射；不补点 | 20,000 | 数量相等不代表逐 VID 全量相等，也不证明全部是真实政策 |
| M12 政策→企业 | related_entities.enterprise 非空=0 | 0 | 0 | 缺稳定企业 ID/适用证据，无可补候选 |
| M13 政策→人才 | related_entities.talent 非空=0 | 0 | 0 | 缺稳定人才 ID/适用证据，无可补候选 |
| M14 政策→科研机构 | related_entities 无 research key；org 名称=19,989 | 0 | 0 | 发文名称不等于科研机构适用关系 |
| M16 政策→政策 cite | pedigree 非空=2、约定 ID token=0；非 demo ADS cite=401 | 0 | 0 | 2 行只有标题文本；401 条为 mock/seed，全部排除 |
| M11 政策↔政策 policy_relate | 两套 ADS 无该边型，缺已确认关联对 | 0 | 0 | 不能用 cite 替代无向关联 |
| regulate 政策侧 | 非 demo ADS 600 条 pol→org | 0 | 0 | mock 批，org 为名称；无合规关系证据 |
| M10 科研机构→政策 publish | 发文名称非空=19,989，稳定科研机构 ID 列不存在 | 0 | 0 | 不能反转 regulate 或按名称推断发布者 |
| 历史政策→chain/segment apply_to | 本轮未重建原始源分母 | 不补 | 1,678+9,279=10,957 | 非 M；只读 apply_to，不双读 support、不使用常数 weight 作强度 |

M12/M13/M14 共用一个物理边型，但统计按终点 Tag 分三条；M16 与 M06 共用 cite，按 policy/paper Tag 分开。

## 2. ADS 分母不能跨库混加

| 库前缀 | entity | graph_edge | graph_node | 边批次构成 |
|---|---:|---:|---:|---|
| gkxlumenx_ads | 7,517 | 3,738 | 818 | mock_20260623=3,726；seed-240-relation-20261112=12 |
| demo_gkxlumenx_ads | 0 | 12 | 20,007 | 全部 seed-240-relation-20261112 |

非 demo 的 3,738 条边可按端点组合求和复核：600 support→industry + 600 apply_to→industry + 1,226 support→enterprise + 600 regulate→org + 401 cite→pol + 68 support→talent + 234 apply_to→service + 3 support→tech + 3 support→segment + 3 apply_to→segment。

不能把 1,226 条 `support→enterprise:名称` 改名充作 M12；不能把 68 条 `support→talent:名称` 改名充作 M13；不能把 600 条 `regulate→org:名称` 改名充作 M14。

### 2.1 三对 seed 引用的端点检查

| 源 policy_id | 目标 policy_id | 源/目标在 DWD | 源/目标在 policy Tag | 原文引用证据 | 处置 |
|---|---|---|---|---|---|
| 18318861 | 18318862 | 两端存在 | 两端存在 | pedigree 均空，ADS props={} | seed，不入合规补边计划 |
| 18363390 | 18363391 | 两端存在 | 两端存在 | pedigree 均空，ADS props={} | seed，不入合规补边计划 |
| 18407696 | 18407697 | 仅源存在 | 仅源存在 | 源 pedigree 空，ADS props={} | seed 且缺目标，不入计划 |

398 条 mock cite 与 3 条 seed cite 是同一非 demo ADS 全量 401 条的划分；demo 的 3 条 seed 是另一库中的同名批次，不再加成 404 个真实候选。

## 3. 实测语句与审计文件

- 表/字段：`01-discovery-queries.json`、`02-schema-count-queries.json`。
- 精确源/图计数：`02-schema-count-results.json`。
- 批次/端点/字段内容：`03-source-profile-queries.json` 与 `03-source-profile-results.json`。
- ID、原料 provenance：`04-source-id-*`、`05-seed-validation-*`。
- 16 条逐项：`06-empty16-queries.json`、`06-empty16-results.json`。
- org 槽全量长度：`07-org-validation-*`，19,989 行恰好 1 个字符串，11 行为空数组。

以上文件均在 [证据目录](KG-GRAPH-POLICY-05/)。每条 query 有 SQL/nGQL 和时间。关键查询示例：

```sql
SELECT COUNT(*) AS row_count FROM demo_gkxlumenx_dwd.policy_base_info WHERE is_deleted=0;
SELECT calc_batch_id,COUNT(*) AS cnt FROM gkxlumenx_ads.policy_graph_edge
WHERE relation_type='cite' GROUP BY calc_batch_id;
```

```text
MATCH (p:policy)-[e:policy_apply_to]->(t:enterprise) RETURN count(e) AS cnt
MATCH (p:policy)-[e:cite]->(t:policy) RETURN count(e) AS cnt
```

本轮未执行写入，不出具“补数成功”对账。未来真实补数须另开 `KG-GRAPH-POLICY-05-补数对账.md`，逐批记录应写、实际写、已存在、缺端点/证据不合格的跳过及回读，不覆盖本次只读基线。

## 4. 限制与复核事项

- 当前精确源计数未复现任务卡旧快照；需原快照执行人/徐滕强对齐环境和 SQL，不能推断删数。
- SHOW STATS 的 apply_to/support 各 10,964，锚定有效 policy 端点聚合各 10,957。缓存/物理计数与有效端点计数分列，差 7 不擅自归因。
- 一个查询别名使用 `tags` 导致 SyntaxError，已改 `endpoint_tags` 重跑成功；没有高水位错误，没有失败后继续灌数。
- 未发起图统计重算、全图聚合、模型调用、DDL 或 DML。所有只读会话已关闭。
