# 路径步规则确认单 · KG-GRAPH-COVER-01 第 3 步（tech_path_step 缺口判定）

- 出具：human:白鑫凤（执行）/ 数据实测 2026-11-17
- 关联：[11-说明-技术点层四项缺口成因与解法-20261117](../11-说明-技术点层四项缺口成因与解法-20261117.md) §4.3；[派单-A](./派单-A-燕大-技术点层覆盖补齐.md) 第 3 步
- 源：久新 Doris `47.93.119.170:29030` / `gkx_technology_analysis_dev`.`ads_technology_evolution_path_step`（只读）
- 图：`10.50.75.136:9669` / `demo_gkx_chain`（只读计数）

---

## 一、结论（先说判定）

**缺口 12,891 条 = 每条路径的第一个节点，不是漏搬。** 属派单-A 第 3 步里的「③取数口径不同」：
源表按**节点行**记（一条路径有 N 个节点就 N 行），图 `tech_path_step` 是**边**（「上一步→这一步」，
N 个节点只有 N−1 条边）。第一条节点没有上一步，永远写不成边。

**裁定：采纳 11-说明 §4.3 选项 A——对账分母改为「跳数 35,018」，本项按 100% 关闭，不补数。**

## 二、五个总口径（2026-11-17 实测，可复算）

| 口径 | 实测 | 含义 |
|---|---:|---|
| 源表总行数 | 47,909 | 节点行总数 |
| `step_order=1` 行数 | 12,891 | 每条路径的第一节点 |
| `previous_technology_node_id IS NULL` 行数 | 12,891 | 与上行完全重合（第一步全部无前驱） |
| 路径条数（`COUNT(DISTINCT path_id)`） | 12,891 | 缺口 = 路径数，逐条对应 |
| `previous IS NOT NULL` 行数 | **35,018** | = 完整跳数 = 图中现有 `tech_path_step` 边数 |

验算：47,909 − 12,891 = **35,018** ✅；图中 `MATCH (:tech_point)-[e:tech_path_step]->(:tech_point) RETURN count(e)` = **35,018** ✅。

## 三、抽样 10 条路径留证（按 `path_id` 排序取前 10，未做任何筛选）

| path_id（前 20 位） | 节点行数 | step1 的 previous |
|---|---:|---|
| tep_0000471a77b3b33af… | 6 | NULL |
| tep_00035ea56419f43e… | 4 | NULL |
| tep_00065c1e012cd6e4… | 3 | NULL |
| tep_0008406bbacbe282… | 4 | NULL |
| tep_000d8867690c1c87… | 3 | NULL |
| tep_000d8d927d0d596a… | 6 | NULL |
| tep_0012b62e36515cf9… | 4 | NULL |
| tep_001ea24e0d6e0f3e… | 2 | NULL |
| tep_00234589c51b42cc… | 2 | NULL |
| tep_002574e3a62b3500… | 6 | NULL |

10/10 条路径的第一节点 `previous` 均为 NULL；行内第 2 行起 `previous` 均非空（链式指向上一节点）。
明细入仓：[KG-GRAPH-COVER-01-证据/path_sample_10.json](./KG-GRAPH-COVER-01-证据/path_sample_10.json)。

## 四、为什么不选 B（留档）

选项 B（为每条路径造 12,891 个虚拟起点节点 + 12,891 条边）会引入「造出来的实体」，
污染路径算法与对账口径，且 11-说明 §4.3 已明确不建议。**不做。**

## 五、对账口径变更（覆盖派单-A 对账表 tech_path_step 行）

| 项 | 源表应有（旧） | 源表应有（新） | 图中实有 | 跳过 | 跳过原因 |
|---|---:|---:|---:|---:|---|
| tech_path_step | 47,909 | **35,018（跳数）** | 35,018 | 12,891 | 每条路径首节点无前驱，结构性不可成边（非缺陷） |

覆盖率：35,018 / 35,018 = **100%**。

---

*复核方式：任取一条 path_id，`SELECT * FROM ads_technology_evolution_path_step` 按 `step_order` 排序，
看第 1 行 `previous_technology_node_id` 是否为 NULL；再对比图中该路径的边数（节点数 − 1）。*
