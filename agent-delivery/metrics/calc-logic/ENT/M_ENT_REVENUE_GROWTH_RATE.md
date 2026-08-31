# 营收增长率（M_ENT_REVENUE_GROWTH_RATE）

> 口径真源：王惠底稿「营业收入增长率」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **落表目标**（产出，禁止当源）：`enterprise_finance_history.revenue_growth_rate`（逐年）、`enterprise_base.revenue_growth_rate`（最新一年快照）。  
> **输入**：只读 `enterprise_finance_history.revenue`。国内 ODS `operating_revenue` 非全空，整条能算。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_REVENUE_GROWTH_RATE`
- **指标名称**：营收增长率
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：年
- **对齐状态**：逐年相邻年同比；KPI 取最新能算出的一年；无相邻年该年不算，整条能算
- **是否在数据库**：ODS 有 `operating_revenue`；正式 DWD 财务年表有 `revenue` / `revenue_growth_rate`（后者为产出列，现网 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E23

## 口径定义

相邻年营收同比：`(本年 revenue − 上年 revenue) / 上年 revenue * 100`。

- 本年 = 该行 `data_year`；上年必须是 `data_year - 1`，且上年 `revenue` 非空、非 0。
- **禁止**隔年硬凑（如 2016 vs 2018）。
- 缺上年或除零：**该年无法计算**（该年不写增长率）。不是整条指标无法执行。
- 不挂产业。禁止对增长率做 SUM 当筛选合计。
- 国外：对等表 `enterprise_forg_finance_history` 正式库 0 行，暂不并。不造表。
- 禁止用上市财务 `dwd_org_stock_finance_info` 替代年报。
- **禁止读产出列**：`enterprise_finance_history.revenue_growth_rate`、`enterprise_base.revenue_growth_rate`。两表是本指标落表目标。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `enterprise_finance_history.revenue_growth_rate` | `org_id + data_year` | 该年相对上年的同比；算不出则 NULL |
| `enterprise_base.revenue_growth_rate` | `org_id` 一条 | 该企最新一个能算出的年份的增长率（KPI 快照） |

## 分场景 / 实现方案

### 场景 A · 逐年落表（计算真源）

对每个 `org_id + data_year`，join 同年企业的 `data_year-1` 行，用 `revenue` 现算后写回财务年表。

### 场景 B · 画像 / 列表 KPI

读该企财务年表中**最新能算出增长率的一年**（或写完后的主档快照）。无相邻年：**该企无法计算**。

### 场景 C · 指定年

入参 `:year`：只算 / 只展示该年相对 `:year-1`。

### 场景 D · 营收趋势图

趋势用 **营收序列**（`M_ENT_REVENUE_LATEST` 的逐年 `revenue`），不把增长率 SUM 成趋势。无连续年度营收则不画，不造数。

### demo（`demo_gkxlumenx_dwd`）

- `enterprise_finance_history` 现网 **没有** `revenue_growth_rate` 列，只有 `revenue`（449 行）。
- 全表自连即可：`cur.data_year = prev.data_year + 1`。
- 主档 demo 只有 `revenue_latest`，没有增长率列 → KPI 查询时现算，不改 GDF DDL（本波不建列）。

### 生产（`gkxlumenx_dwd`）

- 财务年表、主档 **已有** 增长率列，但现网值是 mock（与相邻年 `revenue` 对不上）。
- 灌实数后按 `org_id` 取相邻两年再算，禁止无过滤全表自连。
- 算完写入两列；查询仍以本次计算为准，不要信任历史预存值。

对应 seed `formula`：逐年 `(rev_t - rev_{t-1}) / rev_{t-1} * 100`；KPI 取最新能算年；不加整条「当前无法执行」。

**计算公式文件**：`M_ENT_REVENUE_GROWTH_RATE.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
```

- 输入：`revenue` ← `operating_revenue`；`data_year` ← `year`
- 产出（不进 `source_tables`）：`revenue_growth_rate`（年表 + 主档快照）

来源系统（`source_systems`）：国内机构要素库。

## 现网探针（live `gkx` + 项目 DWD，2026-08-28；不进 8 件套）

- 国内 ODS `operating_revenue`：20178 行，非空 300；相邻年成对 **11 对 / 2 企**（另 2 企隔年，不算）。
- 正式 DWD 财务年表：709 行 / 120 企，`revenue` 与 `revenue_growth_rate` 全填（mock）；相邻年 589 对 / 114 企。
- demo DWD 财务年表：449 行，**无**增长率列。
- 国外 ODS 相邻年很多（2093 企）；正式国外 DWD 财务 **0 行**，暂不并。
- ADS **无**企业营收增长率表/列。`enterprise_growth_trend` 是区域新增企业数，不是本指标。

## 待建 / 缺口

- 多数企业无相邻年营收：该年 / 该企无法计算，不是整条缺口。
- 国外 DWD 未灌。
- demo 主档/财务缺增长率列：现算，本波不改 DDL。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 COVER-STAT-L01 逐年落表 + KPI 最新年，产出列禁止当源*
