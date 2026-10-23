# POLICY · Nebula（一张 G 挂接）

```yaml
---
doc_id: POLICY-STORE-NEBULA
element: POLICY
role: store-nebula
status: draft
version: "2026-08-21"
updated: 2026-10-23
engine: nebula
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> 拓扑真源：[`../01-data-flow.md`](../01-data-flow.md) §3（**approved** 施工范围）。本文件只落细表指针，**draft**。

## Space

| 项 | 值 |
|---|---|
| Demo | **仅** `demo_gkx_chain` |
| 正式 | `gkx_chain`（本管线禁写） |
| 废作目标 | `gkx_policy`（v1 §4 DDL 禁止照抄 CREATE SPACE） |
| vid | `FIXED_STRING(80)`（CHAIN）；政策点 `pol:{policy_id}` |

## 四类边语义（RE 抽取真源：`polan/graph/entity.py`）

四类边**方向一律以政策为起点**（`pol:{policy_id}` → 目标），不建反向边。语义与产出规则：

| 边 | 中文 | 起点 → 终点 | 源字段 | 权重 | props |
|---|---|---|---|---|---|
| `support` | **扶持**：政策把资源投向谁 | policy → industry | `policy_industry_rel`（`is_deleted=0`）。不读已弃用的 `related_entities.industry`，不用 `ext5` 兜底 | `0.8` | `{factor: factors}` |
| | | policy → enterprise | `related_entities.enterprise` | `0.5–0.9` 随机 | — |
| | | policy → talent | `related_entities.talent` | `0.7` | — |
| `apply_to` | **适用**：政策的效力覆盖谁 | policy → industry | 同 `industry` 源 | `0.6` | — |
| | | policy → service | `related_entities.service` | `0.5` | — |
| `regulate` | **监管 / 实施主体**：谁负责执行落地 | policy → org | `related_entities.org`（节点 `org_type=implement`） | `0.6` | — |
| `cite` | **引用谱系**：本政策的上位政策 | policy → policy | `pedigree` 中 `上位政策:{pid}`，且该 pid 在本批集合内 | `1.0` | `{relation: "上位"}` |

要点：

1. **`support` 与 `apply_to` 的区别**在于资源流向 vs 效力范围。产业会**同时**拿到两条边（`support` 0.8 + `apply_to` 0.6），代表"既扶持又适用"；企业/人才只有 `support`（是被扶持对象），服务机构只有 `apply_to`（是效力对象而非资金去向）。
2. `regulate` 与 `support` 不重叠：`org` 是实施机关，不作为被扶持对象。
3. `cite` 只在**批内**成环校验通过才落边——上位政策不在本批 `policy_id` 集合内则整条丢弃，不造悬挂边。
4. 边权之和即政策节点的加权度，是 `relation_degree`（关联度）指标的计算基础，见 `polan/eval/focus.py`。

**Nebula 实际落地少于上表**：ADS 镜像里六类关联主体齐全，但投影时 `industry` / `enterprise` / `org` / `service` 必须解析到既有 `chain:` / `segment:` / `ent:` / `inst:` 顶点才挂边，`talent` / `tech` 本波不上图（`OPEN-POLICY-GRAPH-01`）。首轮实测因此以政策点 + `cite` 边为主，跳过明细见 [`../etl/pipeline-to-nebula.md`](../etl/pipeline-to-nebula.md) §8。

## 本波 DDL（IF NOT EXISTS · B 叶执行）

```ngql
USE demo_gkx_chain;
CREATE TAG IF NOT EXISTS policy(name string, weight double, props string);
CREATE EDGE IF NOT EXISTS support(weight double, factor_type string, src_table string);
CREATE EDGE IF NOT EXISTS apply_to(weight double, src_table string);
CREATE EDGE IF NOT EXISTS regulate(weight double, src_table string);
CREATE EDGE IF NOT EXISTS cite(relation string, weight double);
```

> ⚠️ **上块 per-edge 列是设计意图，loader 未采纳**。`factor_type` / `src_table` / `relation` 对应上表 props 里的语义，但 as-built 把它们统一序列化进单列 `props`，四类边实际均为 `(weight double, props string)`。现网以 as-built 为准（[`../etl/pipeline-to-nebula.md`](../etl/pipeline-to-nebula.md) §4）；本块是否跟改属结构项，走 `OPEN-POLICY-GRAPH-03` 升级 `human:淮政玮`。

已有 Tag 只 hang：`chain` / `segment` / `enterprise` / `institution`。不新建 `org` / `industry` / `tech` / `talent`。

禁止：`DROP SPACE`；写 `gkx_chain`；`CREATE SPACE gkx_policy`。
