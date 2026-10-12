# 城市企业密度（M_ENT_CITY_DENSITY）

> 口径真源：算法 2026-09（分母=面积，全国不算，area 空或≤0 该市空，与 REGIONAL_DENSITY 同一套）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：分子 ← `M_ENT_REGIONAL_COUNT` 市层；分母 = `gkxlumenx_dim.code_region.area`（有表有列，不是缺表）。GDP 不进公式。Q016 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（强制，先于本条）

必须先有 **`M_ENT_REGIONAL_COUNT`** 按默认市（`LEFT(region_id, 4)`）出数，写入 `enterprise_region_summary`：

```
ODS → enterprise_base.region_id → M_ENT_REGIONAL_COUNT（市层）
        → enterprise_region_summary.enterprise_total
                         ↓
              本条 / code_region.area
                         ↓
              sz_city_benchmark.enterprise_density
```

| 顺序 | 指标 / 表 | 本条用它做什么 |
|------|-----------|----------------|
| 1 | `M_ENT_REGIONAL_COUNT` | 出市层去重企业数（`region_id` 缺列缺口留在这一叶，本条不重写） |
| 2 | `enterprise_region_summary` | 读 `region_code` + `enterprise_total` |
| 3 | `gkxlumenx_dim.code_region.area` | 分母；项目 dim，不是三方 ODS |
| 4 | 本条 | 相除后写入 `sz_city_benchmark.enterprise_density` |

不挂 `M_ENT_SZ_COUNT`（深圳全市一条，对标要多城）。不重扫 `enterprise_base`。禁止抄 `sz_city_benchmark.enterprise_density`（现网深圳 41.0 等 mock）。禁止 `headquarters_city` / `city` 中文名。

## 元数据

- **指标ID**：`M_ENT_CITY_DENSITY`
- **指标名称**：企业密度（对标城市）
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：多城市对标
- **更新频率**：周（对标表；分子日更后本条可随批重算）
- **对齐状态**：D1 aligned（算法 2026-09）；分母锁 dim.`area`；Q016 集合未甲方确认
- **是否在数据库**：`gkxlumenx_dim.code_region` 有 `area` 列（不是缺表）；现网灌数可能仍空；COUNT 落表 0 行；结果列有 mock 密度
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q016（对标城市集合）；面积单位 / 区划精度见 Q012（本波不拍，细稿记载）

## 口径定义

对标城市：该市 `M_ENT_REGIONAL_COUNT`（默认市） / 该市 `code_region.area`。展示单位 **家 / km²**（列注释只写「面积」，单位待核，⚠️；王惠底稿「百 km²」本波不改单位，与区域密度对齐）。

- 市键对齐：COUNT 的 `LEFT(region_id,4)`（例 `4403`）与 dim / 对标表 6 位码用 `RPAD(..., 6, '0')`（例 `440300`）。
- `area` 空或 ≤0：**该市空**（不写 0）。不除零，不拿上级面积顶。列存在，不是缺表。
- `city_code='NATIONAL'`：**不算**（不是行政区划面积键）。
- 只国内。国外区域数本条不用（国外无面积列，与区域密度相同）。
- 对标哪些市：Q016 🟡。未闭合前只更新 `sz_city_benchmark` 已有民政部 6 位 `city_code` 行，不新造城市。现网：深 / 北 / 上 / 苏 / 广 / 杭 / 成。
- 产业不是分组维。页面传入产业：分子随 COUNT 的 MATCH 过滤结果，本条不 JOIN chain。
- GDP 本波不进公式。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `sz_city_benchmark.enterprise_density` | `city_code` 一条 | 该市企业数 / area |

**禁止读**现成 `enterprise_density`。`sz_count` / `avg_tech_power` 不是本条。

## 分场景 / 实现方案

### 场景 A · 对标表（默认）

COUNT 市层就绪后：

```
JOIN enterprise_region_summary
  ON RPAD(region_code, 6, '0') = sz_city_benchmark.city_code   -- 若 COUNT 已落 6 位则直接等值
JOIN code_region ON code_region.code = city_code
SET enterprise_density = enterprise_total / area
WHERE city_code 为 6 位民政部码
  AND area > 0
```

`area` 空：该行不写密度（该市空，不当 0）。`NATIONAL` 跳过。

### 场景 B · 单市 KPI（如深圳）

取 `city_code=440300` 一行，同一除法。分子等于 `REGIONAL_COUNT` 的 `4403` / `440300`，不是另跑 `M_ENT_SZ_COUNT`。

### demo（`demo_gkxlumenx_*`）

- 对标表行数少，可全表 JOIN。
- `code_region.area` 若仍全空 → 该市空；不要用 mock 41.0 顶。不是缺表。
- 不要扫主档凑分子。

### 生产（`gkxlumenx_*`）

- 只更新对标表已有 `city_code`，禁止无过滤扫全部 `code_region`。
- COUNT 落表按 `region_code` 点查后除面积。

对应 seed `formula`：依赖 COUNT + /area + 该市空（area 空）+ 全国行不算。**不写**「无 region_id 整条无法执行」（缺列在 COUNT 叶）。**不写缺维表**。

**计算公式文件**：`M_ENT_CITY_DENSITY.md`

## 源表字段

本波例外：二次 STAT 左端允许 COUNT 落表，右端写指标依赖。

```
enterprise_region_summary <- metric: M_ENT_REGIONAL_COUNT
code_region.area
```

分母 JOIN `gkxlumenx_dim.code_region.area`（项目 dim，有表有列，进 8 件套；不是 ODS，不写 `<- ods:`）。

产出（不进 `source_tables`）：`sz_city_benchmark.enterprise_density`。

来源系统：国内机构要素库（COUNT 国内侧）。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_dim.code_region`：3349 行，**有 `area` 列**（注释「面积」）。无独立「城市面积表」，分母就是这一列。2026-08-28 探针 `area` 全 NULL（含对标 7 城）；灌数空该市空，**不是缺表**。
- `gkxlumenx_dwd.enterprise_region_summary`：`region_code` + `enterprise_total`；正式库 0 行（COUNT 尚未落数）。
- `sz_city_benchmark.enterprise_density`：8 行有值（深圳 41.0 … 全国 8.0），mock。
- 分子缺列见 `M_ENT_REGIONAL_COUNT.md` / `M_ENT_SZ_COUNT.md`（主档无 `region_id`）。

## 待建 / 缺口

- Q016 对标城市集合：🟡，本波不拍；只用已有行。
- Q012：面积单位待核；本条粒度已钉市。
- 维表有 `area`，不是缺表。灌数空则该市空（不当 0）。
- COUNT 的 `region_id` ETL：缺口留在 COUNT 叶。
- D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.5`；STAT。COVER-STAT-L01 二次 STAT 例外：本条挂 COUNT。禁止 GDP / 人口列顶面积。禁止把 `gkx.dwd_*` 写入 `source_tables`。

---
*2026-09-07 COVER-STAT-L01：0.3.1 分母挂 dim.`code_region.area`；全国不算；该市空；D1 aligned*
