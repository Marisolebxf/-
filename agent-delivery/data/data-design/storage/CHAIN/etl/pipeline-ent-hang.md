# CHAIN · 企业上链（ENT hang → INB node）

> **任务**：`ENT-CHAIN-HANG-MOCK-L01` · Owner `agent:algorithm-agent` · 监管 `human:淮政玮`  
> **不是**行业分析抽边，**不是**图边 LLM。不造整棵链。  
> **消费**：已存在的 DWD `industry_chain` / `industry_chain_node`（由 [`pipeline-demo-sim-process.md`](./pipeline-demo-sim-process.md) 灌树）。  
> **流图**：[`../01-data-flow.md`](../01-data-flow.md) **已会签，本叶不翻签**。

```yaml
---
doc_id: CHAIN-ETL-ENT-HANG
element: CHAIN
role: etl
status: as-built
version: "2026-08-16"
updated: "2026-08-16"
task: ENT-CHAIN-HANG-MOCK-L01
engine: mysql
---
```

## 0. 意图

把 Demo **企业**挂到 **产业链节点（INB）**。企业归一键 = `org_id`（ENT `enterprise_base`）；链/节点 = DWD v5 Q053 `chain_id` / `node_id`。ODS 侧常见 `credit_code`，必须经 `credit_code ↔ org_id` 对照；对不上 **drop + honesty**，禁止编 `org_id`，禁止用亿集内部 vid。

两表都写（同 Demo 实例 `demo_gkxlumenx_dwd`）：

| 域 | 表 | 语义 |
|---|---|---|
| ENT DWD | `enterprise_industry_chain` | 企业侧挂链：`org_id` + `chain_code`/`chain_name` + `node_id`/`node_name` |
| CHAIN DWD | `industry_chain_entity_rel` | 链侧挂实体：`chain_id`/`node_id`/`entity_type=enterprise`/`entity_id=org_id`/`relation_type=belongs_to` |

2026-10-24 demo 实查：两表对得上多少企业、能不能按产业节点检索，见 [产业检索企业条数](../../../../../qa/test-cases/SDWJSF-KJZTFWSFK/enterprise-企业分析/产业检索企业条数-20261024.md)。政策、服务机构同口径见 [产业检索政策条数](../../../../../qa/test-cases/SDWJSF-KJZTFWSFK/policy-政策分析/产业检索政策条数-20261024.md)、[产业检索服务机构条数](../../../../../qa/test-cases/SDWJSF-KJZTFWSFK/svc-产业服务分析/产业检索服务机构条数-20261024.md)。

## 1. 过程步骤

```text
读 ENT enterprise_base（org_id, enterprise_code=credit, name, industry）
  → credit_code ↔ org_id 对照（对不上 drop）
  → 读已有 industry_chain_node（仅 INB；拒绝 Paper 点）
  → 名称/行业弱对齐或 SEED-08 确定性种子选节点
  → 写 enterprise_industry_chain + industry_chain_entity_rel
  → 可选 Nebula 投影（本叶只给指针，fail-soft；不强制投影）
```

| 步 | 输入 | 输出 | 失败 |
|---|---|---|---|
| 1 读企业 | `enterprise_base` | 候选行 | 缺表 → `--apply` 空集；`--self-check` 不连库 |
| 2 对齐 | `enterprise_code` ↔ `org_id` | 有 `org_id` 的行 | 无 org_id 且 credit 对不上 → **drop**，不编键 |
| 3 选节点 | `industry_chain_node` INB | 一企一节点 | 无 INB 节点 → **不写**，OPEN-ENT-HANG-01 |
| 4 写 ENT 表 | 对齐后的挂点 | `enterprise_industry_chain` | 缺列 `insert` 过滤；覆盖该 `org_id` 旧行（含 ENT `map_industry_chain` 的 `node_id=NULL` 占位） |
| 5 写 CHAIN 表 | 同上 | `industry_chain_entity_rel` | `etl_batch_id=ent-hang-mock`；产品行不碰 |
| 6 Nebula | 上两表 | 不在本叶强制写图 | 见 [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) |

脚本：`${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/run_ent_chain_hang.py`（`--self-check` / `--apply`）。门禁 `entan.common.db.assert_demo_mysql_targets()`。

ENT `llm_ods.gdf_sim.map_industry_chain` **已写**本表（字段名复用 v3.1：`chain_code`/`chain_name`/`node_id`/`node_name`，**无第二套列名**），但 Demo 占位 `node_id` 常空、`chain_code` 为 `IC-*` 非 INB。本叶 `--apply` 对能对齐的 `org_id` **覆盖为 INB 挂点**，供 `yiji_sim.facts.iter_located_in` 直接出事实边（**不改** `facts.py` / `infer.py`）。

## 2. 字段对照

| 目标 | 来源 | 规则 |
|---|---|---|
| `org_id` | `enterprise_base.org_id`；或 `enterprise_code` lookup | 对不上 drop |
| `enterprise_code` | `enterprise_base.enterprise_code`（= ODS `credit_code`） | 可空；只作对照 |
| ENT `chain_code` / `chain_name` | L0 `industry_chain`（`node_id` 前缀匹配 `INB1303` 等） | 无 L0 则退回 node.`chain_id` |
| ENT `node_id` / `node_name` | `industry_chain_node` | **必须** `INB*`；禁 Paper |
| ENT `node_stage` | node.`stage_code` | 可空 |
| `entity_type` | 常量 `enterprise` | 产品仍走 GDF `p:{credit}:…` |
| `entity_id` | **org_id** | 禁止亿集 vid；禁止把未对齐 credit 当成 org_id |
| `relation_type` | `belongs_to` | — |
| CHAIN `chain_id` | node.`chain_id`（现网 L1，如 `INB130302`） | 与 `industry_chain_node` 可 join |
| `ext.honesty` | `org_id_aligned` / drop 清单 | 不对齐不入库 |

选点（确定性，弱对齐）：

1. SEED-08 credit → L0（云启/格物/星辰/磐石 → `INB1303`；深极智机 → `INB1401`）
2. 名称含 华为 / 中芯 / 微电子 / 半导体 / 集成电路 → `INB1303`；智机 / 机器人 → `INB1401`
3. `industry_category` 关键词
4. 在候选 INB 节点中按 `md5(org_id)` 取模（优先更长 `node_id` = L2）

库内真实 `node_id` 为准；fixture 里华为/中芯应对 `INB1303*`。写不出（无节点）→ OPEN，不编节点。

## 3. 失败 / 对不齐语义

| 情况 | 行为 |
|---|---|
| `org_id` 空且 credit 不在 `enterprise_base` | **drop**；`honesty=drop_unresolved_org_id` |
| 无 INB 节点（或只有 Paper） | **drop**；`--apply` 打印 `OPEN-ENT-HANG-01`，不造树 |
| 目标非 `demo_*` | `RuntimeError refusing` |
| GDF `map_entity_rel` lookup 失败 | **skip 该企业行** + log；产品行仍写 `p:{credit}:…` |
| GDF 读不到 `enterprise_base` | `org_by_credit=None`，企业行 **暂留 credit_code** + `ext.honesty=credit_code_pending_org`（不假装已是 org_id） |

## 4. 与 `pipeline-demo-sim-process.md` 的接口

| 本叶 | 模拟过程叶（`DEMO-CHAIN-SIM-PROCESS-L01`） |
|---|---|
| **消费** 已灌的 `industry_chain` / `industry_chain_node` | **负责** ODS 四表 → 模拟 GDF 造树与缺口空表 |
| **独占** `gdf_sim.map_entity_rel` 的企业 `entity_id`（改为 org_id） | **禁止**改 `gdf_sim.py`（该叶已声明只读） |
| 不重做灌数按钮 / `generate.py` 主路径 | 入口 `run_all.py --chain` 仍归该叶 |
| 不改行业分析六表 / documents | 同禁 |

上链可在模拟 GDF **之后**单独 `--apply`；不把 hang 塞进 `generate.py`。`gdf_sim_gaps.apply_gaps` 仍后置，本叶不 hook。

## 5. Nebula 指针（本叶不强制投影）

关系真源已在 MySQL 两表。图投影任务 `DEMO-CHAIN-PY-GRAPH-L01`（pending_test）。本叶若将来投影：只写 `demo_*` space，失败不阻断，禁 Neo4j。见 [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) · [`../stores/nebula/graph-chain.md`](../stores/nebula/graph-chain.md)。

## 6. 禁止

- APPLY 正式 `gkxlumenx_*`；Neo4j；翻签 `01-data-flow.md`
- 用产业链资讯表冒充行业分析 `documents`
- 改 `entan/yiji_sim/infer.py` / `infer_llm.py` / `pipeline.py` / `prompts/**`
- 乱编 `org_id` 或把亿集 vid 当企业键
