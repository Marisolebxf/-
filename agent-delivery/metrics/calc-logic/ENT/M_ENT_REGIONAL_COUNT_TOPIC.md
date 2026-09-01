# 区域企业数量规模占比（M_ENT_REGIONAL_COUNT_TOPIC）

> 口径真源：专题 OPEN seq 41 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **Q073 / Q-MO-ENT-02 走 C**（架构确认）：规模 = 数量，只出家数 + 占比。不挂营收、不挂从业人数。Q073 仍 🟡，不升 🟢。  
> 不 reuse 展示 `M_ENT_REGIONAL_COUNT`（无年、无产业过滤、无占比）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_REGIONAL_COUNT_TOPIC`
- 名称：区域企业数量规模占比
- 模块：专题企业 / TOPIC-ENT-05
- 更新频率：年
- 关联Q：Q-MO-ENT-02 / Q073（走 C，仍 🟡）；Q012；Q056🟢

## 口径定义

自然年 × 区域键：国内名录去重家数，以及该格占当期集合占比。

```
COUNT(DISTINCT b.org_id)
FROM enterprise_base b
GROUP BY stat_year, region_key
```

占比：

```
region_cnt / set_cnt
```

`set_cnt` = 同一自然年、同一产业过滤后的国内名录去重家数。分母 0 → 占比空。

区域键：`nation:CN` + 省 `LEFT(region_id,2)` + 市 `LEFT(region_id,4)` + 县 `region_id` 6 位 + 复合 `scope:gba|yrd|jjj`（`region_scope_member`）。热门城市并入市，不另开 `scope:shenzhen`。嵌套格子不可加。

- 统计主体 = `enterprise_base`。禁止 FROM `enterprise_finance_history`。禁止抄 `enterprise_base.revenue_latest`。
- **选产业是 API**：名录先经 `enterprise_industry_chain`；ETL 全量年×区域（及需要的链键）。禁止把「当前所选产业」写进 GROUP BY。
- 只国内。无国外上链，不 UNION。
- 三级地图可视化不进本核。
- 禁止 reuse 展示 `M_ENT_REGIONAL_COUNT`。

8 件套只留这条 COUNT + 占比。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

主档 `region_id` 在就能 GROUP BY 年×区域键 COUNT，再除当期集合。公式完整。规模面不另开。

### ② 灌数 / 绑码（另一回事）

`region_id` 待 ETL 绑维；上链灌 INB。Q012 / Q073 未甲方确认。不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_base` / `enterprise_industry_chain` | 表在 |
| 目标 | `enterprise_region_year_dist`（建议：`stat_year + region_key + org_cnt + share`） | **缺口：无此表** |

源 ≠ 目标。维表 `code_region` / `region_scope_member` 不进 `source_systems`。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 每年全量年×区域键 COUNT 写入目标表；`share = org_cnt / set_cnt`（`set_cnt` 按链键预存）。 |
| API | 按年 / `region_key` / 链键过滤；禁止请求路径全表现算。 |
| 前端 | 选产业 / 选区 = 带键查行。全国→省→市下钻只读已落格。 |

**计算公式文件**：`M_ENT_REGIONAL_COUNT_TOPIC.md`

## 源表字段

```
enterprise_base.region_id <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端主档。上链表只做产业过滤。维表写细稿。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-27 覆盖展示 REGIONAL_COUNT 叶；不进 8 件套）

- ODS `dwd_org_base_info`：`province/city` 全满，无 adcode。
- `region_id` 待 ETL 绑 `gkxlumenx_dim.code_region`。
- `enterprise_region_summary` 0 行，不是本条目的表。

## 待建 / 缺口（不是口径算不全）

1. `region_id` 绑码；Q012 / Q073 🟡。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `TOPIC-ENT-05`；STAT。Q073 选项 A（营收合计）/ B（从业人数）不作本条口径。

---
*2026-08-31 COVER-STAT-L01：年×区域键 COUNT + 占比；规模=数量；选产业是 API*
