# 匹配企业总数（M_ENT_TYPE_MATCH_COUNT）

> 计算口径 2026-09-04 钉死：产业 ∩ 类型、未选不计算、多选并集再交、中文对照不算无法执行。  
> 类型只认 `enterprise_tag.tag_code`，六类码同 `TYPE_COUNT`。  
> Q010 🟡 = 待甲方书面，不改本口径。  
> 维护：data-agent · seed `0.3.2`。

## 元数据

- **指标ID**：`M_ENT_TYPE_MATCH_COUNT`
- **指标名称**：匹配企业总数
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：日
- **对齐状态**：D1=`aligned`（计算口径齐）；Q010 仍待甲方书面
- **关联Q编号**：Q010（类型判定）；Q072（专题类型字典，不提前收窄本条）

## 计算口径（已定）

所选产业 ∩ 所选类型的国内企业去重数。

```
未选产业 OR 未选类型 → 不计算

COUNT(DISTINCT org_id)
FROM enterprise_base
JOIN enterprise_industry_chain   -- 命中所选产业并集
JOIN enterprise_tag
WHERE tag_code IN (:types)       -- 所选类型并集；六类码同 TYPE_COUNT
```

- **未选产业或未选类型：不计算。**
- **多选**：产业并集、类型并集，再求交。
- 类型码：`foreign` / `high_tech` / `sme` / `listed` / `little_giant` / `little_giant_pro`。禁止 `enterprise_type`、`is_listed`、`org_size`、`sme_tech`。
- 只国内。无国外上链 / 国外标签表，不造表，不并国外。
- 选产业 / 选类型是 API，不进口径枚举。
- 计算键 `org_id`，JOIN `enterprise_base`，对不上 drop。

## 中文 → 内部码（洗数，不算无法执行）

与 `HIGH_TECH_COUNT` / `TYPE_COUNT` 同一套：三方中文 `org_tag` 由项目对照落到六码。外资 / 上市可以不在 `dwd_org_tech_tag`，从主档类型 / 股基灌进 `enterprise_tag` 同一列。**不写「当前无法执行」。**

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_base` + `enterprise_industry_chain` + `enterprise_tag` | 设计表在 |
| 目标 | 建议 `ads.ent_type_match_count` | **缺口：无独立目标表**（落表，不是口径） |

## 源表字段

```
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
enterprise_tag <- ods: dwd_org_tech_tag
```

计算 FROM 只用左端 DWD。`industry_tags` 当选产业源（已定）；正式 INB 链位未到只记灌数。

来源系统：国内机构要素库、产业链要素库。

## 分场景 / 千万级（不进 8 件套）

- 场景 A · 类型分析页「匹配企业总数」：当前筛选下 COUNT。
- 场景 B · 与 `TYPE_COUNT` 对照：同一六码；本条必须同时有产业条件。
- demo：可 JOIN 现算。生产：按 `chain_code × tag_code` 预聚合；禁止 `tag_name LIKE`。

## 现网探针（live `gkx`，2026-09-04；不进 8 件套）

- `dwd_org_industry_tags` `is_deleted=0`：19029 行；`credit_code` / `industry_link_code` / `industry_code` 空列 0。
- `dwd_org_tech_tag` 高新 / 专精特新 / 小巨人有数；`org_tag` 含「上市」「外资/外商」为 0（走别源灌 `listed` / `foreign`）。
- 无国外标签表、无国外上链表。

## 待建 / 缺口（不是口径）

- 无独立目标表。
- D3 `pending_ods` / D4 `mock` 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.1`；STAT。

---

*2026-08-27 只国内；2026-08-30 改挂 tag_code；2026-09-04 计算口径钉死（未选不计算 / 并集再交 / 中文对照不算无法执行）*
