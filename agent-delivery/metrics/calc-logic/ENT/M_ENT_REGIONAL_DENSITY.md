# 区域企业密度（M_ENT_REGIONAL_DENSITY）

> 口径真源：算法 2026-09（分母=面积，全国不算，area 空或≤0 该区空，与 CITY_DENSITY 同一套）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：分子 ← `M_ENT_REGIONAL_COUNT` 国内省/市/县；分母 = `gkxlumenx_dim.code_region.area`（有表有列，不是缺表）。GDP 不进。国外不算。Q012 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（强制）

| 顺序 | 指标 / 表 | 本条用它做什么 |
|------|-----------|----------------|
| 1 | `M_ENT_REGIONAL_COUNT` | 国内省 2 / 市 4 / 县 6 去重企业数（`region_id` 缺列留在那一叶） |
| 2 | `enterprise_region_summary` | 读区划键 + 家数 |
| 3 | `gkxlumenx_dim.code_region.area` | 分母；项目 dim，不是三方 ODS |
| 4 | 本条 | 相除。目标建议 `ads.ent_regional_density`，**当前无此表** |

不重扫 `enterprise_base`。禁止 `headquarters_city`。禁止 GDP / 人口顶面积。COUNT 的国外国家行 **不除面积**。

## 元数据

- 指标ID：`M_ENT_REGIONAL_DENSITY`
- 名称：区域企业密度
- 更新频率：日
- 关联Q：Q012
- 对齐：D1 aligned（算法 2026-09）

## 口径定义

国内省 / 市 / 县：该区 `REGIONAL_COUNT` / 该区 `code_region.area`。单位 **家 / km²**（列注释只写「面积」，单位待核，⚠️）。

- 键对齐：`RPAD(区划前缀, 6, '0') = code_region.code`。省 `44`→`440000`；市 `4403`→`440300`；县 `440305`。
- `area` 空或 ≤0：**该区空**（不写 0）。不除零，不拿上级面积顶。
- **全国行不算**。
- **国外不算**：`city` / `code_country` 无面积列；COUNT 按国家合并的行不进本条。
- 产业不是分组维。选产业跟 COUNT 过滤，本条不 JOIN chain。

## 两点分开

### ① 口径

三级家数 / area。维表有 `area` 就能写除法。

### ② 有没有数

有表有列，不是缺表。灌数空该区空。`region_id` 缺列在 COUNT 叶。无独立目标表。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_region_summary` + `code_region.area` | COUNT 落表可能 0 行；area 可能仍空 |
| 目标 | 建议 `ads.ent_regional_density`（区划键+粒度+密度） | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。禁止把对标表 `enterprise_density` 当本条（那是市密度）。

## 分场景 / 实现方案

### 场景 A · 跑批

COUNT 国内三级就绪后，按粒度 JOIN `code_region` 除面积。`area` 空该行不写。生产按区划点查，禁止请求路径扫全库主档。

### 场景 B · 换粒度

省 / 市 / 县换键重算，禁止拿市密度冒充县。

### demo

行少可全表 JOIN。area 空则该区空，不用 mock 顶。

## 源表字段

```
enterprise_region_summary <- metric: M_ENT_REGIONAL_COUNT
code_region.area
```

分母进 8 件套，不写 `<- ods:`。来源系统：国内机构要素库。

## 现网探针（2026-08-27；不进 8 件套）

- `gkxlumenx_dim.code_region`：约 3349 行，有 `area` 列。当时全 NULL。无独立面积表。
- 国外维无面积列。
- 分子见 `M_ENT_REGIONAL_COUNT.md`。

## 待建 / 缺口

1. `area` 灌数（有列不是缺表）。
2. **无独立目标表**。
3. `region_id` 在 COUNT 叶。
4. D3/D4 本波不升。`is_mock: true`。

---
*2026-09-07 COVER-STAT-L01：0.3.1 挂 REGIONAL_COUNT 省市县 + dim.area；国外/全国不算；D1 aligned*
