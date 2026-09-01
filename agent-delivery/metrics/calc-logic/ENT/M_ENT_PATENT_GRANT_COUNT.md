# 专利授权量（M_ENT_PATENT_GRANT_COUNT）

> 口径真源：王惠底稿「第一专利权人 + 授权」→ 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。**粒度=企业**（每 org 一条），不是筛选范围加总。累计授权件数，不按报告期。查询键是 `org_id`，第一专利权人须名称匹配落 `first_assignee_org_id`。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PATENT_GRANT_COUNT`
- **指标名称**：专利授权量
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：日
- **对齐状态**：口径已锁第一专利权人；缺两列标缺口，不写无法执行
- **是否在数据库**：ODS 有第一受让人名称与 `status=授权`；项目 DWD 明细无第一人字段
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：无（王惠底稿曾标 24，不进 8 件套）

## 口径定义

**每个企业一条**：该企业作为**第一专利权人**的授权专利去重件数（累计）。发明 / 实用新型 / 外观设计都计。不是「选定企业授权量合计」。

- 第一专利权人 ≠ 第一申请人。ODS 键 = `dwd_patent.first_current_assignee_name`（与 `dwd_patent_assignees.sequence=1` 一致；子表行数不全，以主表字段为准）。
- 应用层按 `org_id` 查，不能直接用名称。ETL 用第一受让人名称匹配 `enterprise_base.enterprise_name` / `enterprise_forg_base.name_en`，写入 `first_assignee_org_id`。匹配不上：**不计入**该企业。
- 法律状态 = ODS `dwd_patent_legal.status` **授权**。禁止把 DWD 现网「有效」当成授权。
- 不按产业过滤。不按报告期（正式现网明细无授权日列可用；本条不做本年授权量）。
- 无独立国外专利表。同一套 ODS，名称映射到国内或国外主档。不造 `enterprise_forg_patent`。
- 与 `M_ENT_PATENT_TOTAL`：总量用现有 `org_id`（权利人映射，不过滤法律状态）；本条用 `first_assignee_org_id` + 授权。两列不要混用。

## 计算逻辑说明

```
SELECT first_assignee_org_id,
       COUNT(DISTINCT patent_id) AS grant_count
FROM enterprise_patent_detail
WHERE legal_status = '授权'
  AND first_assignee_org_id IS NOT NULL
GROUP BY first_assignee_org_id
```

单企读取：`WHERE first_assignee_org_id = :org_id`（仍是该企业自己的 COUNT，不是全集）。禁止无 `GROUP BY` 的全集 `COUNT`。

## 两点分开（强制）

### ① formula

明细有 `first_assignee_org_id` + `legal_status='授权'` 就能按企 COUNT。

### ② 缺列

正式 DWD 无 `first_current_assignee_name` / `first_assignee_org_id`：**缺口：缺列**（要补到专利明细，不另建表）。**不写「无法按第一人计算」当整条无法执行。**

**计算公式文件**：`M_ENT_PATENT_GRANT_COUNT.md`

## 源表字段

```
enterprise_patent_detail <- ods: dwd_patent
enterprise_patent_detail.legal_status <- ods: dwd_patent_legal
enterprise_patent_detail.first_current_assignee_name <- ods: dwd_patent
```

`first_assignee_org_id` 是 DWD 内名称匹配产物，不进 ODS 右端。主档 JOIN 不进 8 件套 `source_tables`。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库。

## DWD 字段变更（COVER-STAT-L01）

正式 `gkxlumenx_dwd.enterprise_patent_detail` 现网无这两列，**要补到专利明细**（不是另建表）。GDF workpack 暂缓对外，变更先记本条。

| 列 | 类型（建议） | 来源 | 用途 |
|---|---|---|---|
| `first_current_assignee_name` | varchar(255) | `dwd_patent.first_current_assignee_name` | 第一专利权人**名称**（匹配原料） |
| `first_assignee_org_id` | varchar(64) | 上列名称 JOIN `enterprise_base.enterprise_name` ∪ `enterprise_forg_base.name_en` | 查询键；与现有 `org_id` 分立 |

建议索引：`KEY idx_patent_first_org (first_assignee_org_id, legal_status)`。

不要用 `assignee_name` 顶第一人（那是当前权利人全集）。不要用 `first_applicant_name`。demo 有 `assignee_name` 但全空，且没有 `first_*` 两列。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- `dwd_patent` 86028；`first_current_assignee_name` 非空 85894。
- `dwd_patent_assignees.sequence=1` 与第一受让人名称对上的 61442 条全部一致；子表仅 70000 行，不能当唯一真源。
- 第一申请人 ≠ 第一专利权人：1867 条不同。
- `dwd_patent_legal.status` 授权 27939。
- 正式 DWD 明细 467 行、`legal_status` 仅「审中/有效」、无第一人列。

## 待建 / 缺口（必须标；不是无法执行）

| 类型 | 缺什么 | 现网 |
|------|--------|------|
| 缺列 | `enterprise_patent_detail.first_current_assignee_name` | 正式明细无此列；ODS 主表有名称 |
| 缺列 | `enterprise_patent_detail.first_assignee_org_id` | 未建；名称匹配产物 |
| 未灌 | `legal_status='授权'` | DWD 现网只有审中/有效 |
| 其它 | 名称匹配规则（繁简/曾用名/英文） | GDF 未定；匹配失败 drop |

D3 / D4 本波不升。`is_mock: true`。本波不改 GDF DDL。

## 备注

bid `§1.1.1.2.4.2.3.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止抄 `patent_history.patent_grant_count` 代替本条。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 第一专利权人=名称匹配；2026-08-31 方案1 缺列标缺口*
