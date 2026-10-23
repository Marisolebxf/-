# Wave B — Mapping / ETL 派工（POLICY v1.0）

> **DDL**：本包 `10/`  
> **Mapping**：`09-政策域-ETL-Mapping明细-源表到DWD.md`  
> **禁止**：Demo 映射当全文；第二张政策主表；写 ES/ADS/图谱；旧 37 列贴源；加 `gbl:` 改键（MAP-01 已关：永远分 UK）

## 1. 触发条件

1. Wave A 两张 P0 表贴源验收通过（行数对账 + `is_deleted`/`is_history` 过滤一致）  
2. 可写 `gkxlumenx_dwd`  
3. 现网/目标结构已对照 `10` 快照（缺列先 ALTER，禁止按 Demo as-built 灌假列）

## 2. 数据流

```text
POLICY-B1-DOMESTIC
gkxlumenx_ods.dwd_policy_base
        → policy_base_info  (source_plane=domestic)

POLICY-B2-GLOBAL
gkxlumenx_ods.dwd_global_policy_base
        → policy_base_info  (source_plane=global)
```

顺序见 09 §4。两作业写同一张表，UK `(source_plane, policy_id)`。

## 3. 作业状态

| 作业 | 状态 | 阻塞边界 |
|---|---|---|
| `POLICY-B1-DOMESTIC` | 可配置 | 无；国内洗入 |
| `POLICY-B2-GLOBAL` | 可配置 | 无；国际洗入同一张表 |
| 写 ES / Nebula | **不执行** | 不在本包 |
| `POLICY-C1-INDUSTRY` / `POLICY-C2-CLAUSE` | B 成功后另排 | 见 `12`。不要配进本 Mapping 作业 |

B1/B2 可并行配置，但必须共用同一 UK；碰撞行按 09 §1.2 **隔离计数**，禁止改键。

## 4. 交付物

- DDL 差集说明（仅 `policy_base_info`）  
- 字段可追溯到 09 §3.1–3.2  
- 每平面 ≥20 条抽样（含 `content` 未截断抽检）  
- drop / 冲突计数（空 `id`、UK 冲突）  
- OPEN-POLICY-MAP-* 书面登记  
- 增量、删除与重跑策略回签；未回签不得宣称 CDC 闭环

## 5. 本侧后续

指标 STAT / 图谱 / 检索不在本包。B 成功后的抽取产业与条款结构化见 `12`（不进本派工的字段配置）。正式 DAG 名仍挂 `OPEN-POLICY-FLOW-01`，由产线回写。
