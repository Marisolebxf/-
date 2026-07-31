# Wave B — Mapping / ETL 派工（v1.3）

> **本波已纳入企业维派单。** 与 Wave A 同包投递；**开工前提**是 Wave A P0 贴源验收通过。  
> **正式 Mapping 真源**：[09-企业维-ODS到DWD-Mapping说明-v3.md](09-企业维-ODS到DWD-Mapping说明-v3.md)  
> **禁止**：按历史 Mapping **v2** 或旧表名（`reg_info` / `org_bid_info` / `company_base` 等）直接施工。

## 1. 触发条件（全部满足）

1. Wave A 企业 **P0（17 张）** 验收回签完成  
2. 目标侧可写 `gkxlumenx_dwd`（连接见 `03`；密钥线下）  
3. 贴源后抽样确认 `dwd_org_base_info` 等关键列与 `09` 一致（差异回写本侧后微调）

> 源结构大面积不可用时暂停 Wave B，登记供应方；不阻塞 Wave A 余表。

## 2. 数据流（项目视角）

```text
gkxlumenx_ods.dwd_*  ──GDF Mapping/ETL──►  gkxlumenx_dwd.enterprise_* / risk_* / ...
```

- **不是**供应方内部 `ods_*` → `dwd_*`。  
- 项目 DWD **不与**供应方 `dwd_*` 一一同名。

## 3. 输入材料（本包已齐）

| 材料 | 状态 |
|------|------|
| Wave A 表清单 `02` | 投递 |
| **Mapping 说明 v3 `09`** | **正式施工输入** |
| 表级对照 `08` | 辅助；细节以 `09` 为准 |
| Mapping v2 | **仅参考，勿施工**（`GDF/Mapping/企业/…(v2).md`） |
| DWD 设计 | `data/data-design/企业/DWD表结构设计-企业模块.md` |
| 承诺字段 CSV | `third-party-source/doc/md-extract/_csv/` |

## 4. GDF 交付物

- 字段级 Mapping 配置（可追溯到源表.字段 / `09` 行号）  
- ETL 作业 + 调度依赖（`09` §0）+ 失败重跑  
- 关键转换：元→万元、枚举、org_id / 信用代码归一  
- 抽样对账：每张目标表 ≥20 条  
- 与本侧 lineage：`mapping_status` ⏳→✅/❌  

## 5. 本侧后续

- lineage / data-agent 验证映射完整性  
- 缺口进 `data-gap-catalog` + 客户决策清单（🟡）  
- **不**要求 GDF 改 Java/ES/前端  

## 6. 时间盒

| 阶段 | 时间感 |
|------|--------|
| Wave A | 立即；P0 为第一里程碑 |
| Wave B | P0 关单后按 `09` 开工；Mapping 材料已随 v1.3 投递 |
