# 深圳企业数（M_ENT_SZ_COUNT）

> 口径真源：王惠底稿「深圳企业数」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。深圳键 = `region_id` 市前缀 `4403`，不是中文城市名。  
> **落表目标**（产出，禁止当源）：`shenzhen_enterprise_summary`（`stat_type=enterprise_total`，`dim_code=440300`）。  
> **过滤源**：`enterprise_base`。缺 `region_id` 标缺口，不写无法执行。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_SZ_COUNT`
- **指标名称**：深圳企业数
- **一级模块**：企业分析
- **二级模块**：企业总览 / 深圳企业现状
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：计算键已钉 `region_id LIKE '4403%'`；缺列见缺口表
- **是否在数据库**：结果表有壳；主档无 `region_id`；ODS `city='深圳市'` 有样例行
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E25（区域码规则同 Q012 三级前缀，本条城市已钉死深圳）

## 口径定义

国内主档中，行政区划落在深圳市的企业去重数。

- 深圳 = `enterprise_base.region_id LIKE '4403%'`（市码 4403，含各区；完整市码 `440300`）。
- 计算键 `org_id`。只国内。国外不并（深圳不是外国城市）。
- **禁止** `headquarters_city` / `city` 中文名（「深圳」「深圳市」）当计算键。
- 未选产业：全市。选产业：国内 `enterprise_industry_chain` 按 `chain_code` / `chain_name` 过滤后再数（同 `M_ENT_TOTAL_COUNT`）。
## 两点分开（强制）

### ① formula

主档有 `region_id` 就能 `LIKE '4403%'` 去重 COUNT。

### ② 有没有数 / 缺列

正式 / demo 主档都没有 `region_id`：**缺口：缺列**。ODS `city='深圳市'` 有 17562 行，只说明源有市名，不是已绑码。**不写「当前无法执行」**。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `shenzhen_enterprise_summary` | 全市一条 KPI | `stat_type='enterprise_total'`，`dim_code='440300'`，`dim_name='深圳市'`，`stat_value`=去重企业数 |

同表其它 `stat_type`（重点企业、分年、分产业分布）不是本条 KPI，本波不写。

**禁止读**现成 `stat_value`（现网 12860，mock）。

不要写入：`sz_city_benchmark.sz_count`（对标城市表，列全空）、ADS `chain_sz_advantage.sz_enterprise_count`（产业链）、`enterprise_region_summary`（正式库 0 行）。

## 分场景 / 实现方案

### 场景 A · 全市 KPI（默认）

`COUNT(DISTINCT org_id) FROM enterprise_base WHERE region_id LIKE '4403%'` → 写入结果表 `enterprise_total`。

### 场景 B · 选产业

先 JOIN `enterprise_industry_chain` 过滤，再按同一 `region_id` 条件计数。国外无上链表，不并。

### demo（`demo_gkxlumenx_dwd`）

- 主档无 `region_id`。有 `shenzhen_enterprise_summary` 壳的话仍禁止读 mock。
- 全表扫补不出缺列。本波不改 GDF 加列。

### 生产（`gkxlumenx_dwd`）

- 主档 120 行 mock，`headquarters_city='深圳'` 仅 15 条，且无 `region_id`。
- 结果表已有 `enterprise_total=12860`，**不可信**。
- `region_id` 绑上后按 `org_id` 过滤计数再写回；禁止用中文城市名凑数。

对应 seed `formula`：COUNT + ①能写 + 缺口：无 `region_id`。

**计算公式文件**：`M_ENT_SZ_COUNT.md`

## 源表字段

```
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

- 输入：`region_id`（待绑码；ODS 现有 `city`）
- 产出（不进 `source_tables`）：`shenzhen_enterprise_summary.stat_value`

来源系统：国内机构要素库、产业链要素库。

## 现网探针（live `gkx` + 项目 DWD，2026-08-28；不进 8 件套）

- ODS `dwd_org_base_info.city='深圳市'`：17562 / 40020。无 `region_id`。
- 正式 / demo DWD `enterprise_base`：**无 `region_id` 列**。
- `shenzhen_enterprise_summary`：22 行；KPI `enterprise_total` / `440300` = 12860（mock）。
- `enterprise_region_summary`：0 行。
- `sz_city_benchmark.sz_count`：全 NULL。

## 待建 / 缺口（必须标；不是无法执行）

| 类型 | 缺什么 | 现网 |
|------|--------|------|
| 缺列 | `enterprise_base.region_id` | 正式/demo 主档都无此列 |
| 未绑码 | ODS `city` → `region_id` | `city='深圳市'` 17562 行，未进 DWD 码 |
| 其它 | 结果表 `stat_value` | 12860 mock，禁止当源 |

D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.5`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 深圳=4403；2026-08-31 方案1 缺列标缺口*
