# 企业域 ODS→项目 DWD Mapping 基线（表级对照 / 辅助）

> **正式字段级施工请用**：[09-企业域-ETL-Mapping明细-源表到DWD.md](09-企业域-ETL-Mapping明细-源表到DWD.md)  
> 导读：[09-企业维-ODS到DWD-Mapping说明-v4.md](09-企业维-ODS到DWD-Mapping说明-v4.md)  
> 本文仅表级备忘；**与明细冲突时以明细为准**。  
> **DWD 建表**：[10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/)

---

## 1. 总览指针（勿再抄旧短表）

直接 / 关联 / 指标 / 暂不映射 / 国外：见明细 **§2.1–§2.5**。  
字段：见明细 **§3**；指标聚合：**§4**；开放问题：**§5**。

## 2. 相对历史口径（保留）

| 项 | 旧口径 | 现行 |
|----|--------|------|
| 表名真源 | live 推断 | doc 承诺 + Mapping 明细 |
| 企业主表 | `reg_info` / 宽表 `enterprise` | `dwd_org_base_info` → `enterprise_base` |
| 标签 | tech_tag / 缺口 | `dwd_org_tag_info` → `enterprise_tag` |
| 专利 | 另波不做 | `dwd_patent` 名称关联 |
| 招投标洗数 | 四表全洗 | **仅** win_candidate + base_out |
