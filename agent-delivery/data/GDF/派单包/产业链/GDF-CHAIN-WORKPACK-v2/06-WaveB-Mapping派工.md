# Wave B — Mapping / ETL 派工（CHAIN v2.0 · 基线 10-19；规则继承 v1.0）

> **DDL**：v5（见 `10/`）  
> **Mapping**：`09-产业链域-ETL-Mapping明细-源表到DWD.md`  
> **禁止**：Demo 模拟映射当全文；资讯洗进 `news_event`；自造 org_id；**CHAIN-B2-INDANA**

## 1. 触发条件

1. Wave A 中 `mapping: wash` 且 P0 的表贴源验收通过  
2. 可写 `gkxlumenx_dwd`  
3. 现网/目标结构已对照链树四表  
4. **`enterprise_base` 已有可 JOIN 的 `org_id`/`enterprise_code`**（企业包 Wave B）。未就绪只阻塞 B3，B1 继续

## 2. 数据流

```text
CHAIN-B1-TREE
gkxlumenx_ods.dwd_industry_chain_info
        → industry_chain → node → node_rel

CHAIN-B3-ENTITY-REL
gkxlumenx_ods.dwd_org_industry_tags
        + gkxlumenx_dwd.enterprise_base
        → industry_chain_entity_rel
```

**CHAIN-B2-INDANA**：本期不配置、禁止写入 `industry_analysis_*`。

顺序见 09 §4。

## 3. 作业状态

| 作业 | 状态 | 阻塞边界 |
|---|---|---|
| `CHAIN-B1-TREE` | 可配置 | 无；按 INB 原文生成链树 |
| `CHAIN-B2-INDANA` | **不执行** | 李伟：六表不同构入项目 DWD |
| `CHAIN-B3-ENTITY-REL` | 条件可配置 | 仅受 `enterprise_base` JOIN 就绪影响 |

## 4. 交付物

- DDL 差集说明（四张链表）  
- 字段可追溯到 09 §3.1–3.4  
- JSON 拆行、INB 校验、credit→org_id drop 规则  
- B1/B3 每表 ≥20 条抽样  
- drop 计数（无 org_id / 非 INB）  
- OPEN-CHAIN-MAP-* 书面登记  
- 增量、删除与重跑策略回签；未回签不得宣称 CDC 闭环

## 5. 本侧后续

指标 STAT 只读 DWD/ADS；不要求 GDF 写 ADS/Java/前端。
