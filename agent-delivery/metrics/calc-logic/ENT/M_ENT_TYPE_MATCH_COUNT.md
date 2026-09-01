# 匹配企业总数（M_ENT_TYPE_MATCH_COUNT）

> 口径真源：王惠底稿 → 2026-08-27 COVER-STAT-L01；**2026-08-30 类型条件改挂 `enterprise_tag.tag_code`**，不再走主档 `enterprise_type` / `is_listed` / `org_size`。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TYPE_MATCH_COUNT`
- **指标名称**：匹配企业总数
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：日
- **对齐状态**：类型条件走 `enterprise_tag.tag_code`；六类码已冻
- **是否在数据库**：live ODS 主档/标签/产业 tags 有样例行；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q010（类型判定）；Q072（专题类型字典，不提前收窄本条）

## 口径定义

所选产业 ∩ 所选类型的国内企业去重数。

- 产业过滤是本条口径本身，走 `enterprise_industry_chain`。
- 类型条件走 `enterprise_tag.tag_code`。六类码与 `M_ENT_TYPE_COUNT` 相同（`foreign` / `high_tech` / `sme` / `listed` / `little_giant` / `little_giant_pro`）。禁止 `enterprise_type`、`is_listed`、`org_size`、`sme_tech`。
- 只国内。无 `enterprise_forg_industry_chain` / `enterprise_forg_tag`，不造表。选产业后国外不并入。
- 港澳台 ≠ 国外。计算键 `org_id`，JOIN `enterprise_base`，对不上 drop。

## 计算逻辑说明

```
COUNT(DISTINCT org_id)
FROM enterprise_base
JOIN enterprise_industry_chain  -- chain_code / chain_name 命中 :industry
JOIN enterprise_tag
WHERE tag_code = :type          -- 六类码同 TYPE_COUNT
```

类型：`enterprise_tag.tag_code = :type`（六类见 TYPE_COUNT）。  
① DWD 标签关系在就能数。② ODS→DWD 灌数另写，不进「无法执行」。

现网 ODS 无 `dwd_org_industry_chain_dtl`；`enterprise_industry_chain` 不能用 tags 冒充正式链位。

对应 seed `formula`：COUNT(DISTINCT org_id) FROM enterprise_base JOIN enterprise_industry_chain WHERE chain 命中 :industry AND 类型条件 :type。

**计算公式文件**：`M_ENT_TYPE_MATCH_COUNT.md`

## 源表字段

```
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
enterprise_tag <- ods: dwd_org_tech_tag
```

计算 FROM 只用左端 DWD。

来源系统（`source_systems`）：国内机构要素库、产业链要素库。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- `dwd_org_base_info` 40000 行。`org_type` 非空 39985，含「外商」132。`org_size` 有微型/小型/中型/大型/未知；一半 NULL。`listing_status` 非空 11，值像股票代码，不是「上市」文案。
- `dwd_org_tech_tag` 20000 行。`dwd_org_industry_tags` 20000 行。
- `dwd_org_stock_base` 6925 行（备选，未进 8 件套）。
- 无 `dwd_forg_*tag*`、无国外上链表、无 `dwd_org_industry_chain_dtl`。

## 待建 / 缺口

- 六类码已冻（随 TYPE_COUNT）。ODS 没灌齐记在 ②，不改 ①。
- D3 维持 pending_ods；D4 维持 mock。本波不升。
- 正式链位表未到；tags 非正式链。

## 备注

bid `§1.1.1.2.4.2.3.1`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*2026-08-27 只国内；2026-08-30 类型条件改挂 tag_code*
