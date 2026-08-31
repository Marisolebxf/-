# 专利总量（M_ENT_PATENT_TOTAL）

> 口径真源：指标名为 **专利总量**。2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01` 按总量落盘：不过滤法律状态、不挂产业。王惠底稿曾写「有效专利件数」，与总量冲突，本条跟总量。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PATENT_TOTAL`
- **指标名称**：专利总量
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：计算表已改挂项目 DWD；总量不过滤法律状态
- **是否在数据库**：ODS 专利有样例行；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E34

## 口径定义

企业作为专利权人（受让人映射到 `org_id`）的专利去重件数。授权 / 公开 / 审查中均计入，**不过滤** `legal_status`。

- 无独立国外专利表。同一套 ODS `dwd_patent*`，受让人名称映射到 `enterprise_base` 或 `enterprise_forg_base`，落到同一张 `enterprise_patent_detail`。不造 `enterprise_forg_patent`。
- 不按产业过滤。
- 港澳台 ≠ 国外。国外高校 / 科研表不是企业主档。

## 计算逻辑说明

```
COUNT(DISTINCT patent_id) FROM enterprise_patent_detail
```

`org_id` 由 ETL：`dwd_patent_assignees.name`（或专利表第一受让人）JOIN 国内 `enterprise_name` / 国外 `name_en`。对不上的权利人 drop，不进本条。

对应 seed `formula`：COUNT(DISTINCT patent_id) FROM enterprise_patent_detail。

**计算公式文件**：`M_ENT_PATENT_TOTAL.md`

## 源表字段

8 件套 `source_tables`：

```
enterprise_patent_detail <- ods: dwd_patent
enterprise_patent_detail.assignee_name <- ods: dwd_patent_assignees
```

计算 FROM 只用左端 DWD。`dwd_patent_legal` 本条不进 8 件套。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- `dwd_patent` 86028；`dwd_patent_assignees` 70000；`dwd_patent_legal` 53041（本条不用）。
- 无 `dwd_forg_patent`。项目 DWD 无 `enterprise_forg_patent`。
- 法律状态现网主值是「授权」不是「有效」；本条本来就不 WHERE。

## 待建 / 缺口

- 名称映射到 `org_id` 尚未 GDF 灌项目 DWD；`is_mock: true`。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 按总量不过滤法律状态*
