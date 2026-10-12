# 区域企业数量（M_ENT_REGIONAL_COUNT）

> 计算口径 2026-09-04 钉死：国内省/市/县都出；国外按国家合并进同一条。Q012 🟡 仅甲方书面。
> 维护：data-agent · seed `0.3.2`。

## 元数据

- **指标ID**：`M_ENT_REGIONAL_COUNT`
- **指标名称**：区域企业数量
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析 / 企业总览（同 metric_id）
- **三级模块**：类型与区域分析
- **更新频率**：日
- **对齐状态**：计算键已改挂 `region_id`；Q012 默认到市未甲方确认
- **是否在数据库**：live ODS 主档有样例；`region_id` 需 ETL 绑码；国外主档 0 行（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q012；Q-E32-02（全球层）

## 口径定义

按区域对企业 `org_id` 去重。国内∪国外。产业不是本条分组维。

- 国内：6 位民政部 `region_id`，**省 2 / 市 4 / 县 6 都出**（三套 GROUP BY 都写，不默认只出市）。
- 国外：只按 `country_code` 国家合并进本条。**不按国外城市拆**，**禁止写入 `region_id`**。
- 不按城市中文名分组。经纬度只打点，不当分组键。
- 港澳台 ≠ 国外。计算键 `org_id`。

## 计算逻辑说明

```
国内（三级都出）:
  COUNT(DISTINCT org_id) FROM enterprise_base
  省: GROUP BY LEFT(region_id, 2)   例 44
  市: GROUP BY LEFT(region_id, 4)   例 4403
  县: GROUP BY region_id            例 440305
  过滤深圳: region_id LIKE '4403%'（查询）

国外国家层:
  COUNT(DISTINCT org_id) FROM enterprise_forg_base
  GROUP BY country_code

国外城市层:
  GROUP BY city_code   -- 绑 gkxlumenx_dim.city，不进 region_id
```

页面若传入产业：按 MATCH 同规则过滤；国外无上链则该过滤不含国外。本条不 JOIN chain。

对应 seed `formula`：国内 LEFT(region_id,:level) 默认 4；国外 GROUP BY country_code。

**计算公式文件**：`M_ENT_REGIONAL_COUNT.md`

## 源表字段

```
enterprise_base.region_id <- ods: dwd_org_base_info
enterprise_forg_base.country_code <- ods: dwd_forg_base_info
```

计算 FROM 只用左端 DWD。`region_id` 由 `province/city/area` 绑 `gkxlumenx_dim.code_region`（不进 8 件套）。国外城市码维表 `gkxlumenx_dim.city`（不在 dwd）。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库。

## 现网探针（live，2026-08-27；不进 8 件套）

- ODS `dwd_org_base_info`：`province/city` 全满，`area` 约 1.7/4 万；无 adcode。
- ODS `dwd_forg_base_info`：有 `country_code` / `city` 名；**0 行**。无 `city_code` 列。
- `gkxlumenx_dim.code_region` 3315；`city` 73（含 `JPTYO` 与旧 `JP-TYO`）；`code_country` 19。
- `gkxlumenx_dwd` 无国外城市字典；`enterprise_region_summary` 0 行。

## 待建 / 缺口

- Q012 未确认默认市 vs 区县。
- 国内 `region_id`、国外 `city_code` 均待 ETL 绑维表。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.1`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止把 alpha-3 / UN/LOCODE 写入 `region_id`。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 region_id 三级前缀 + 国外分码*
