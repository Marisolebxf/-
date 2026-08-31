# 区域企业密度（M_ENT_REGIONAL_DENSITY）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。分母锁 `code_region.area`；国外不算。Q012 仍 🟡。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_REGIONAL_DENSITY`
- **指标名称**：区域企业密度
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析 / 企业总览（同 metric_id）
- **三级模块**：类型与区域分析
- **更新频率**：日
- **对齐状态**：分母已锁面积（非 GDP）；Q012 默认到市未甲方确认；面积单位未在列注释标明
- **是否在数据库**：dim 有 `code_region.area` 列，现网全空；分子随 COUNT（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q012（精度 + 分母；本波团队默认面积）

## 口径定义

国内某行政区域：`M_ENT_REGIONAL_COUNT` / 该区面积。展示单位 **家 / km²**（列注释只写「面积」，单位待核，标 ⚠️）。

- 区划键与 `M_ENT_REGIONAL_COUNT` 国内相同：6 位民政部 `region_id`，省 2 / 市 4 / 县 6 前缀。Q012 临时默认 **市（4 位）**。
- 分母：`gkxlumenx_dim.code_region.area`。`code` 全 6 位，与前缀对齐用 `RPAD(LEFT(region_id, :level), 6, '0') = code`。例：市 `4403` → `440300`。
- `area` 空或 ≤0：**该区无法计算**。不除零，不拿上级面积顶。
- **国外无法计算**：`city` / `code_country` 无面积列，本波不算。
- GDP 本波不进公式。
- 产业不是分组维。页面若传入产业：分子按 MATCH 同规则过滤；本条不 JOIN chain。
- 港澳台 ≠ 国外。计算键 `org_id`。

## 计算逻辑说明

```
国内（默认市）:
  分子: COUNT(DISTINCT org_id) FROM enterprise_base
        GROUP BY LEFT(region_id, 4)
  分母: code_region.area
        JOIN ON RPAD(LEFT(region_id, 4), 6, '0') = code_region.code
  密度 = 分子 / 分母   -- area 空或 ≤0 则该区无法计算

  省: LEFT(region_id, 2)  JOIN RPAD(..., 6, '0')   例 44 → 440000
  市: LEFT(region_id, 4)  JOIN RPAD(..., 6, '0')   例 4403 → 440300
  县: region_id                                    例 440305

国外: 无法计算（无面积列，本波不算）
```

对应 seed `formula`：国内 COUNT / code_region.area 默认 level=4；area 空该区无法计算；国外无法计算。

**计算公式文件**：`M_ENT_REGIONAL_DENSITY.md`

## 源表字段

```
enterprise_base.region_id <- ods: dwd_org_base_info
```

计算 FROM 只用左端 DWD。分母 JOIN `gkxlumenx_dim.code_region.area`（项目 dim，不是三方 ODS，不进 8 件套 `source_tables`）。

来源系统（`source_systems`）：国内机构要素库。

## 现网探针（live，2026-08-27；不进 8 件套）

- `gkxlumenx_dim.code_region`：约 3349 行；`area` / `people` **全 NULL**（有值 0 行）。无独立面积表。
- `city` / `code_country` / `admin_division`：**无面积列**。dim 无 GDP 列。
- `code_region.level`：1 省 32 / 2 市 342 / 3 县 2975；`code` 一律 6 位。
- 分子探针见 `M_ENT_REGIONAL_COUNT.md`。

## 待建 / 缺口

- Q012 未确认：默认市 vs 区县；面积单位；上线前是否改 GDP。
- `code_region.area` 待灌数；灌入前密度数值无法产出。
- 国内 `region_id` 待 ETL 绑维表。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.1`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止把国外码写入 `region_id`。禁止用 GDP 或人口列顶面积。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 锁面积分母，国外不算*
