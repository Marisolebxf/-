# 城市平均技术力（M_ENT_CITY_AVG_TECH_POWER）

> 口径真源：王惠底稿「城市平均技术力」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT（ADS 特例，须先有 SCORE）**：本条只做城市均值，不算五维、不改权重。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（强制，先于本条）

必须先有 **`M_ENT_TECH_POWER_SCORE`（MODEL）** 跑完并写入 ADS `tech_power`：

```
ODS 原料 → 项目 DWD → M_ENT_TECH_POWER_SCORE → ADS tech_power.tech_power_index
                                                         ↓
                              本条 AVG → DWD sz_city_benchmark.avg_tech_power
```

| 顺序 | 指标 / 表 | 本条用它做什么 |
|------|-----------|----------------|
| 1 | `M_ENT_TECH_POWER_SCORE` | 出企业技术力分（Q014 权重在这一叶，本波不改） |
| 2 | ADS `tech_power` | 读 `org_id` + `tech_power_index`；无分不进均 |
| 3 | DWD `enterprise_base.region_id` | 市码 `LEFT(region_id,4)` 分组 |
| 4 | 本条 | AVG 后写入 `sz_city_benchmark.avg_tech_power` |

没有第 1 步出分、没有 `region_id`：标缺口，公式仍写 AVG。无分 = **该企不进均**（口径）。

禁止用 `enterprise_score`（创新/经营/成长）、专利量、`tech_power.headquarters_city` 中文名顶替。禁止抄 `sz_city_benchmark.avg_tech_power` 现成值（深圳 77.0 等对不上 ADS 均分，mock）。

## 元数据

- **指标ID**：`M_ENT_CITY_AVG_TECH_POWER`
- **指标名称**：城市平均技术力
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：多城市对标
- **更新频率**：周（随 SCORE 批次）
- **对齐状态**：FROM 锁 ADS `tech_power`；分组锁 `region_id`；缺口见下表
- **是否在数据库**：ADS 有 demo 分；主档无 `region_id`；结果表有 mock 均分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014（SCORE 权重）；Q016（对标城市集合）

## 口径定义

对已出技术力分的企业，按市求 `tech_power_index` 算术平均。

- 城市 = `LEFT(enterprise_base.region_id, 4)`（与区域企业数、深圳企业数同一套码）。
- 只国内。国外无对等 `tech_power` 表，暂不并。
- 无 `tech_power_index`：**该企不进均**。某市一个能进均的企业都没有：**该市无法计算**。
- 对标展示哪些市：Q016 🟡；未闭合前只用 `sz_city_benchmark` 已有 `city_code` 行，不新造城市。
- 选产业：用当前筛选 ∩ 已出分企业再均，不是另做一套 SCORE。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `sz_city_benchmark.avg_tech_power` | `city_code` 一条 | 该市 `AVG(tech_power_index)` |

**禁止读**现成 `avg_tech_power`。`avg_business_power` 不是本条。

## 分场景 / 实现方案

### 场景 A · 对标表（默认）

SCORE 批次就绪后：`tech_power` JOIN `enterprise_base` ON `org_id`，`GROUP BY LEFT(region_id,4)`，UPDATE 结果表对应 `city_code`。

### 场景 B · 单市 KPI（如深圳）

`region_id LIKE '4403%'` 的子集上 AVG，写入 `city_code=440300`。

### demo（`demo_gkxlumenx_*`）

- ADS `tech_power` 行数少，可全表 JOIN 再 GROUP BY。
- 主档同样无 `region_id`：**缺口：缺列**。不要用 ADS `headquarters_city` 凑。

### 生产（`gkxlumenx_*`）

- 按 `org_id` 关联后按市码聚合，禁止无过滤全表当常规方案。
- 现网结果表均分是 mock（深圳 77 vs ADS 中文城均分约 53.5），必须重算。

对应 seed `formula`：依赖 SCORE + AVG + 缺口（缺 `region_id` / SCORE 未出分）。

**计算公式文件**：`M_ENT_CITY_AVG_TECH_POWER.md`

## 源表字段

本波例外：二次 STAT 左端允许 ADS 结果表，右端写指标依赖。

```
tech_power <- metric: M_ENT_TECH_POWER_SCORE
enterprise_base <- ods: dwd_org_base_info
```

完整链（细稿）：ADS `tech_power` ← SCORE/MODEL ← DWD 原料 ← ODS。GDF：DWD **勿建** `enterprise_score`。

产出（不进 `source_tables`）：`sz_city_benchmark.avg_tech_power`。

来源系统：国内机构要素库（SCORE 原料侧）。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_ads.tech_power`：120 行，`tech_power_index` + 五维；`headquarters_city` 为中文名（不当键）。
- DWD `enterprise_base`：无 `region_id`、无 `tech_score`。
- `sz_city_benchmark.avg_tech_power`：8 市有值（深圳 77.0），mock。
- `enterprise_score`：不是技术力。

## 待建 / 缺口（必须标；不是无法执行）

| 类型 | 缺什么 | 现网 |
|------|--------|------|
| 缺列 | `enterprise_base.region_id` | 与 `SZ_COUNT` 同一缺口 |
| 缺上游 | `M_ENT_TECH_POWER_SCORE` 出分 | MODEL 本波未出；无分该企不进均 |
| 口径未闭合 | Q014 权重；Q016 对标集合 | 均 🟡 |
| 其它 | 结果列 `avg_tech_power` | 深圳 77.0 mock，禁止当源 |

D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.5`；STAT。COVER-STAT-L01 ADS 例外：`M_ENT_TECH_RANK`、本条。商业力均值未点头不准套。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 依赖 SCORE 再 AVG；2026-08-31 方案1 缺口标出*
