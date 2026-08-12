# Wave B — Mapping / ETL 派工（v2.0）

> **本波已纳入企业维派单。** 与 Wave A 同包投递；**开工前提**是 Wave A P0 贴源验收通过（DDL 纠偏可并行）。  
> **DDL 真源**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)  
> **正式 Mapping 真源**：[09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md)  
> **禁止**：按 WORKPACK-v1、旧 PG 稿、三方参考 9 表清单、Mapping **v2/v3** 单独施工。

## 1. 触发条件（全部满足）

1. Wave A 企业 **P0（17 张）** 验收回签完成（或本侧书面同意先纠偏 DDL）  
2. 目标侧可写 `gkxlumenx_dwd`（连接见 `03`；密钥线下）  
3. **现网表结构已对照 `10/`**（差集 ALTER/重建完成或书面例外）  
4. 贴源后抽样确认 `dwd_org_base_info` 等关键列与 `09` v4 一致（差异回写本侧后微调）

> 源结构大面积不可用时暂停洗数，登记供应方；不阻塞 Wave A 余表与 DDL 纠偏。

## 2. 数据流（项目视角）

```text
gkxlumenx_ods.dwd_*  ──GDF Mapping/ETL──►  gkxlumenx_dwd.enterprise_* / risk_* / ...
                         ▲
                         └── 表结构只认 10-DWD-MySQL-DDL/
```

- **不是**供应方内部 `ods_*` → `dwd_*`。  
- 项目 DWD **不与**供应方 `dwd_*` 一一同名。  
- **不是** PG `demo_gdf_data.dwd.enterprise` 宽表。

## 3. 输入材料（本包已齐）

| 材料 | 状态 |
|------|------|
| Wave A 表清单 `02` | 投递（同 v1.3） |
| **DWD MySQL DDL `10/`** | **建表 / ALTER 唯一真源** |
| **Mapping 说明 v4 `09`** | **正式施工输入** |
| 表级对照 `08` | 辅助；细节以 `09` 为准 |
| 作废对照 `11` | 旧表名 / 误源 → 新表 |
| Mapping v2 / v3 / WORKPACK-v1 | **仅参考，勿施工** |

## 4. GDF 交付物

- 对照 `10/` 的建表 / ALTER / 废弃旧表说明  
- 字段级 Mapping 配置（可追溯到源表.字段 / `09` v4 行号）  
- ETL 作业 + 调度依赖（`09` §0）+ 失败重跑  
- 关键转换：元→万元、枚举、org_id / 信用代码归一（**禁止自造 org_id**）  
- 抽样对账：每张目标表 ≥20 条  
- 与本侧 lineage：`mapping_status` ⏳→✅/❌  

## 5. 本侧后续

- lineage / data-agent 验证映射完整性  
- 缺口进 `data-gap-catalog` + 客户决策清单（🟡）  
- **不**要求 GDF 改 Java/ES/前端；**不**要求写 `demo_gkxlumenx_*`  

## 6. 时间盒

| 阶段 | 时间感 |
|------|--------|
| Wave A | 立即；P0 为第一里程碑 |
| DDL 纠偏 | **优先于洗数**；发现旧宽表/PG 结构立即停建并按 `10/` 改 |
| Wave B Mapping | P0 关单且 DDL 对齐后按 `09` v4 开工 |
