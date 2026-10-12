# 高企数量（M_ENT_HIGH_TECH_COUNT）

> 口径真源：王惠底稿 → COVER-STAT；**2026-09-04 监管确认：口径已定、源不缺；中文 `org_tag` 由项目映射到内部 `high_tech`，不算无法执行**。  
> 判定只认 `enterprise_tag.tag_code='high_tech'`（不再 `tag_name` 模糊含）。  
> Q010 🟡 = 待甲方书面，不改本口径。  
> 维护：data-agent · 8 件套见 seed `0.3.2`。

## 元数据

- **指标ID**：`M_ENT_HIGH_TECH_COUNT`
- **指标名称**：高企数量
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：D1=`aligned`（8 件套齐）；Q010 仍待甲方书面
- **是否在数据库**：ODS `dwd_org_tech_tag` 有数；D4 仍 mock（灌数未升）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q010

## 口径定义

高新技术企业去重家数。`enterprise_tag.tag_code = 'high_tech'`，按 `org_id` 去重。

```
COUNT(DISTINCT org_id)
FROM enterprise_tag
JOIN enterprise_base
WHERE tag_code = 'high_tech'
```

- 只国内。无 `enterprise_forg_tag` / `dwd_forg_*tag*`，不造表。
- **不按产业过滤**。选产业是别的页（`TYPE_COUNT` / KEYPANO），不进本条 8 件套。
- 与 `TYPE_COUNT` 的高新格子同一判定码；本条是总览一个数，不是六类分布。
- 无认定起止日：**码在就算**。
- 计算键 `org_id`，JOIN `enterprise_base`，对不上 drop。
- **禁止** `tag_name` 模糊含。
- **禁止** `enterprise_type`。
- **禁止** `M_ENT_KEY_TOTAL` / 专利≥50 当高企。
- **禁止** 把六类 SUM 当本条。

## 中文 → 内部码（洗数，不算无法执行）

三方 `dwd_org_tech_tag.org_tag` 是中文名，不是 `high_tech`。项目自己对照落到内部码，**不写「当前无法执行」**。

| `org_tag`（live） | 内部 `tag_code` |
|---|---|
| 高新技术企业 | `high_tech` |
| 国家级高新技术企业 | `high_tech` |
| 曾获国家级高新技术企业 | `high_tech` |

对照可落 `tag_dict` / GDF Mapping，不进口径公式。禁止用 `tag_name LIKE '%高新%'` 在查询路径扫。

## 两点分开（强制）

### ① 能不能数

ODS 列不空、对照可做 → 公式完整，**可以算完**。中文未落到码 = 洗数未跑，仍不算无法执行。

### ② ODS → DWD（另一回事）

有没有灌进 `enterprise_tag`、D4 是否 mock，只记接入。没灌 **不写「当前无法执行」**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_tag` + `enterprise_base` | 设计表在 |
| 目标 | 建议 `ads.ent_high_tech_count`（全国一格 `high_tech_cnt`） | **缺口：无独立目标表**（落表工程，不是缺源） |

源 ≠ 目标。本波不改 GDF DDL。生产预聚合一格；禁止请求路径全表扫标签。

**计算公式文件**：`M_ENT_HIGH_TECH_COUNT.md`

## 源表字段

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
```

计算 FROM 只用左端 DWD。右端只作家谱。

来源系统（`source_systems`）：国内机构要素库。

## 分场景 / 千万级（不进 8 件套）

- 场景 A · 企业总览「高企数量」：全国一格 COUNT。
- 场景 B · 与类型分析高新格子对照：同一 `tag_code`，本条无产业维。
- demo：标签量小可 JOIN 现算。生产：按 `tag_code` 预聚合；禁止全表 `tag_name LIKE`。

## 现网探针（live `gkx`，2026-09-04；不进 8 件套）

- `dwd_org_tech_tag` `is_deleted=0`：202393 行 / 32297 企；空 `org_tag` = 0。
- 高新技术企业 27634；国家级高新技术企业 20937；曾获国家级高新技术企业 14012。
- 无国外标签表。
- 源不缺。三种中文 → `high_tech` 见上表。

## 待建 / 缺口

- **缺口：无独立目标表**（落表，不是缺源）。
- D3/D4 本波不升（D3 已 `full`；D4 仍 `mock`）。
- 认定起止日若甲方后补，再开「有效认定期」；当前码在就算。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。与 TYPE_COUNT / KEYPANO 高新码同一套。

---

*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 只国内、含曾获；2026-08-31 改 `tag_code=high_tech`；2026-09-04 D1 aligned + 中文对照不算无法执行*
