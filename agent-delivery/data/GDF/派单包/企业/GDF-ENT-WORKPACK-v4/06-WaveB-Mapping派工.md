# Wave B — Mapping / ETL 派工（v4.0 · 基线 10-19）

> **DDL 真源**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)（v4.0 已重同步 data-design 最新版：含 `enterprise_base` 主键=id+`uk_enterprise_base_org_id(org_id)` 拍板、executive/extra/finance/financing 唯一键）  
> **现网差集（先读）**：[13-现网DDL差集-GDF开工必读.md](13-现网DDL差集-GDF开工必读.md)  
> **Mapping 真源**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)（v4.0：§3.21 国外母子换源；§3.15.7 已废止）  
> **导读**：[09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md)  
> **禁止**：短版 v4 字段表当全文；WORKPACK-v1/v2/v3 历史包；PG/三方参考 9 表；自造 org_id；按已废止 §3.15.7 施工

## 1. 触发条件

1. Wave A 中本批 **`mapping: wash`（P0/P1）** 的表贴源验收通过（或本侧书面同意先纠偏 DDL）  
2. 可写 **`gkxlumenx_dwd`**（见 `03`）。不写 `demo_gkxlumenx_*`。  
3. 现网结构已对照 `10/` **正式库**（含 `enterprise_base.region_id` / 可空 `enterprise_code` / 主键=id 拍板反转、`enterprise_patent_org_rel`、`enterprise_recruit`、`enterprise_forg_*` 及四表唯一键）  
4. ODS 关键列与 Mapping 明细可抽样对齐  

## 2. 数据流

```text
gkxlumenx_ods  ──Mapping 明细──►  gkxlumenx_dwd.enterprise_* / enterprise_forg_* / risk_* / …
                                      ▲
                                      └── DDL = 10/（v4.0 重同步版）
```

## 3. 输入材料

| 材料 | 状态 |
|------|------|
| `02` Wave A | **v4.0 · 62 张**（P0=15/P1=33/P2=14；stock_base 已移出、agg_subsidiary 换源、专利侧表+5） |
| `10/` DDL | **v4.0 重同步**（主键/唯一键 10-12 回写 + 10-20 拍板） |
| **Mapping 明细 `09-企业域-…`** | **正式施工**（v4.0） |
| 导读 `09-…-v4` | 仅导读 |
| `11` 作废对照 | 必读（含 v3→v4 变更对照表） |

## 4. 交付物

- DDL 差集处理说明  
- 字段 Mapping 追溯到明细章节号  
- ETL 依赖（导读 §2 / 明细总览）+ 可重跑  
- 元→万元、专利完整角色名称精确关联、tag↔tag_dict 等转换说明  
- 每表 ≥20 条抽样；未命中 / 外部 OPEN 书面登记  
- **v4.0 新增**：国外母子（`dwd_agg_subsidiary_info`）eid 未匹配治理清单及命中率统计；`dwd_org_stock_base` 移出后上市字段改源说明（09 §3.1.2）随交付  

## 5. 本侧后续

lineage / gap catalog；不要求 GDF 写 ES 或改检索 Java/前端；ES 边界见 [12-DWD到ES.md](12-DWD到ES.md)；贴源/洗数都不写 `demo_gkxlumenx_*`。
