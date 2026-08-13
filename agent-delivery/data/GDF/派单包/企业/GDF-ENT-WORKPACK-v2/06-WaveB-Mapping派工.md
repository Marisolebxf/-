# Wave B — Mapping / ETL 派工（v2.1）

> **DDL 真源**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)  
> **Mapping 真源**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)  
> **导读**：[09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md)  
> **禁止**：短版 v4 字段表当全文；WORKPACK-v1；PG/三方参考 9 表；自造 org_id

## 1. 触发条件

1. Wave A 中 **`mapping: wash` 且 priority=P0** 的表贴源验收通过（或本侧书面同意先纠偏 DDL）  
2. 可写 `gkxlumenx_dwd`（见 `03`）  
3. 现网结构已对照 `10/`（含 `enterprise_recruit`、`enterprise_forg_*`）  
4. ODS 关键列与 Mapping 明细可抽样对齐  

## 2. 数据流

```text
gkxlumenx_ods  ──Mapping 明细──►  gkxlumenx_dwd.enterprise_* / enterprise_forg_* / risk_* / …
                                      ▲
                                      └── DDL = 10/
```

## 3. 输入材料

| 材料 | 状态 |
|------|------|
| `02` Wave A | v2.1 |
| `10/` DDL | v2.1 刷新 |
| **Mapping 明细 `09-企业域-…`** | **正式施工** |
| 导读 `09-…-v4` | 仅导读 |
| `11` 作废对照 | 必读 |

## 4. 交付物

- DDL 差集处理说明  
- 字段 Mapping 追溯到明细章节号  
- ETL 依赖（导读 §2 / 明细总览）+ 可重跑  
- 元→万元、名称关联专利 org_id、tag↔tag_dict 等转换说明  
- 每表 ≥20 条抽样；§5 开放问题书面登记  

## 5. 本侧后续

lineage / gap catalog；不要求 GDF 改 Java/ES/前端；不写 demo_*。
