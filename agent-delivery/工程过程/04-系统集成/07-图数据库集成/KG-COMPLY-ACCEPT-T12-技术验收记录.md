# T12 技术验收记录 · 后台接口契约与压测建议（2026-11-12 18:40）

- 任务：`KG-COMPLY-LOAD-T12`（后台接口契约与压测建议，两案通用）
- 执行：`human:李周`（`agent:api-agent`）｜验收：唐绍祖
- 验收对象：`0dfd38628` → [T12 送审稿](对接文档/燕大/T12/KG-COMPLY-LOAD-T12-接口契约与压测建议-送审稿.md)
- 上游：[T09-S1 技术验收记录](KG-COMPLY-ACCEPT-T09-S1-技术验收记录.md)（18:20 签收）
- 前序评审：[初稿六条](KG-COMPLY-答复-李周-T12初稿评审-20261112.md) · [二稿三条](KG-COMPLY-答复-李周-T07送审与T12二稿评审-20261112.md) · [收尾三处](KG-COMPLY-答复-李周-加权度口径确认与S1签收-20261112.md)
- 结论：**技术验收通过，置 `done`**

---

## 一、三处收尾逐条核验

| # | 要求 | 改法（原文摘录） | 判定 |
|---|---|---|---|
| ① | 加权度口径改「入射边（入 + 出）」 | §4.1 `weighted_degree_recomputed`：「对**入射边（入边 + 出边）**的 `relation_confidence_score/100` 求和…榜首 2,347 条入边与 567 条出边的权重合计为 1,478.04514324」；`degreeBasis=weight_sum_incident`；handoff 同步改写 | ✅ |
| ② | 428 放开 Top20 上限、整榜分页 | §3 表 428 行：「读取 T09-S1 `degree-full.json`…**全量 19,430 点可分页**」；§4.1：「`topN` 为**每页条数**，默认 20，接受**正整数**；请求超过剩余行数时返回剩余记录；游标绑定条目与快照，续页可遍历全部 19,430 点，末页 `nextCursor=null`」；`meta.scope` = `full_graph`；原「越界返回 400」「仅前 20 内有效」已删 | ✅ |
| ③ | 432 与中台 1 撤销 deferred 空态 | §3 表 432 行改「读取 `composite-recomputed.json`，返回 1,500 点等权综合榜、原始分项、归一化分项与权重」、空态仅「无已发布榜单或无匹配结果」；中台 1 行改「读取 `weighted-degree-full.json`…19,430 点…`degreeBasis=weight_sum_incident`」；§4.1 末改为「两项均按成功结构返回可用榜单，查询无匹配时用普通空态」；`UPSTREAM_DEGREE_PENDING` / `UPSTREAM_WEIGHTED_DEGREE_PENDING` 全文已无 | ✅ |

`availability=deferred` 枚举按约定保留在 §1 定义中（`missing` / `deferred` / `unreachable`），本次只是这两条不再走它 ✅

## 二、契约与归档数据的对齐核验（我按 `T09-S1` 四份 JSON 实测）

| 契约声明 | 归档实测 | 判定 |
|---|---|---|
| 428 覆盖 19,430 点、榜首 2,914 | `degree-full.json` 19,430 行，榜首 2,914 | ✅ |
| 428 前 20 顺序与已签收一致 | 与 T09 `recomputed_degree_top20` id/顺序/分值全一致 | ✅ |
| 432 覆盖 1,500 点、四项各 0.25 | `composite-recomputed.json` 1,500 行、`rank` 1..1500 连续、`score` 单调降 | ✅ |
| `meta.scope` = `t09_composite_1500` | 文件 `scope.population_count` = **1,500**，与 428/中台 1 的 19,430 区分正确 | ✅ |
| `populationSize` 取 `scope.population_count` | 428 / 中台 1 = 19,430；432 = 1,500，三个值都能对上 | ✅ |
| `meta.metric_source` 透传归档同名对象 | 三份文件均含 `metric_source`（space / 快照起止 / nodes_sha256 / edges_sha256 / method / formula） | ✅ |
| `items[{nodeId,rank,score,raw,normalized}]` | composite 行字段恰为 `rank/id/name/score/raw{degree,pagerank,closeness,betweenness}/normalized{...}` | ✅ |
| 数据相对路径 `../T09-S1/*.json` | 由 `对接文档/燕大/T12/` 解析为 `对接文档/燕大/T09-S1/`，正确 | ✅ |

## 三、23 项与两案结构（未改动部分抽查）

- 436 / M22 仍为唯一的两个 501（`MULTI_SNAPSHOT_REQUIRED` / `GRAPH_SHAPE_UNSUPPORTED`），426 选企业合作网复用 M22 的 501 且带 `requestedItem=426` ✅
- 16 条空态 M 关系（M03/M05/M06/M07/M10–M14/M16/M18–M21/M23/M24）编号与理由齐，M12–M14 为「缺稳定 ID」、M06 为「无符合论文引用语义的数据源」✅
- 三态（`status` + `reason.code` + `availability` / `unsupported.code`）可机器区分 ✅
- 案 1 / 案 2 前缀与压测分段已分开表述，§5 增加「428 整榜续页」负载档 ✅

## 四、三条不阻塞的小建议（下次顺带）

1. **§1 成功示例的 `meta.metric_source` 只写了 `{formula}`**，与 §4.1「透传归档同名对象」不一致。示例是截断展示、也加了说明，但建议写成 `{ ...完整对象..., "formula": ... }` 或加省略号，免得实现方只填 formula。
2. **`data.weights` 四项各 0.25 是契约常量**，归档文件里并无 `weights` 字段。建议 §4.1 明写「`weights` 由契约固定为 0.25，不取自归档文件」，避免实现方去 JSON 里找。
3. **`method` 命名**：§1 示例用 `T09-S1_recomputed`，§3 表 428 未写 `method` 取值。建议在 §3 或 §4.1 统一给一张 `method` 取值表（`T09-S1_degree_full` / `T09-S1_composite` / `T09-S1_weighted`），前端日志才好归因。

## 五、结论与状态

三处收尾全部闭合、契约与归档数据逐项对得上、23 项与三态结构完整。
**`KG-COMPLY-LOAD-T12` 技术验收通过，`review` → `done`。**

本契约是 428/432/中台加权度三项对外能力的唯一依据，实现方（案 1 Java + Python、案 2 燕大服务）按此取数即可；
压测阈值仍按 §5 由集成方按环境确认，不属本任务验收范围。
