# 利润率（M_ENT_PROFIT_MARGIN）

> 口径真源：王惠底稿「利润率」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。分子钉 **净利润**，不是利润总额。  
> **落表目标**（产出，禁止当源）：`enterprise_finance_history.profit_margin`（逐年）、`enterprise_base.profit_margin`（最新一年快照）。  
> **输入**：`enterprise_finance_history.net_profit`、`revenue`。国内 ODS `pure_profit` 与 `operating_revenue` 非全空，整条能算。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PROFIT_MARGIN`
- **指标名称**：利润率
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：年
- **对齐状态**：逐年净利润/营收；KPI 取最新能算出的一年；缺数该年不算，整条能算
- **是否在数据库**：ODS 有 `pure_profit` / `operating_revenue`；正式 DWD 财务年表有 `net_profit` / `revenue` / `profit_margin`（后者为产出列，现网 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E24

## 口径定义

`利润率 = net_profit / revenue * 100`。

- 分子：净利润。ODS `dwd_org_annual_financial_info.pure_profit` → DWD `net_profit`。
- 分母：营业收入。ODS `operating_revenue` → DWD `revenue`。年字段 ODS `year` → `data_year`。
- **禁止**用 `total_profit`（利润总额）顶替净利润。
- 缺 `net_profit`，或 `revenue` 空 / 0：**该年无法计算**。不是整条指标无法执行。
- 不挂产业。禁止对利润率做 SUM 当筛选合计。
- 国外：对等表 `enterprise_forg_finance_history` 正式库 0 行，暂不并。不造表。
- 禁止用上市财务 `dwd_org_stock_finance_info` 替代年报。
- **禁止读产出列**：`enterprise_finance_history.profit_margin`、`enterprise_base.profit_margin`。两表是本指标落表目标。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `enterprise_finance_history.profit_margin` | `org_id + data_year` | 该年 `net_profit/revenue*100`；算不出则 NULL |
| `enterprise_base.profit_margin` | `org_id` 一条 | 该企最新一个能算出的年份的利润率（KPI 快照） |

## 分场景 / 实现方案

### 场景 A · 逐年落表（计算真源）

对每个 `org_id + data_year`，用同行 `net_profit`、`revenue` 现算后写回财务年表。

### 场景 B · 画像 / 列表 KPI

取该企财务年表中**最新能算出利润率的一年**（或写完后的主档快照）。两边都缺：**该企无法计算**。

### 场景 C · 指定年

入参 `:year`：只算 / 只展示该年。

### demo（`demo_gkxlumenx_dwd`）

- 财务年表有 `revenue`、`total_profit`，**没有** `net_profit` / `profit_margin`（449 行）。
- 主档只有 `revenue_latest`，没有利润率列。
- **不能**用 `total_profit` 当净利润。demo 现算缺分子列 → 该库无法按本口径写出利润率；不改 GDF DDL（本波不建列）。
- 全表扫可以，但缺列不是扫全表能补的。

### 生产（`gkxlumenx_dwd`）

- 财务年表、主档 **已有** `net_profit` / `profit_margin`，但 `profit_margin` 现网是 mock（样例对不上 `net_profit/revenue`）。
- 灌实数后按 `org_id`、年取两列现算，禁止无过滤全表扫当生产方案。
- 算完写入两列；查询以本次计算为准，不要信任历史预存 `profit_margin`。

对应 seed `formula`：逐年 `net_profit/revenue*100`；KPI 取最新能算年；不加整条「当前无法执行」。

**计算公式文件**：`M_ENT_PROFIT_MARGIN.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
```

- 输入：`net_profit` ← `pure_profit`；`revenue` ← `operating_revenue`；`data_year` ← `year`
- 产出（不进 `source_tables`）：`profit_margin`（年表 + 主档快照）

来源系统（`source_systems`）：国内机构要素库。

## 现网探针（live `gkx` + 项目 DWD，2026-08-28；不进 8 件套）

- 国内 ODS：`pure_profit` 非空 376；与营收成对 **288 行 / 274 企**。
- 正式 DWD 财务年表：709 行，`net_profit` / `revenue` / `profit_margin` 全填（mock）。
- 正式 DWD 主档：`profit_margin` 120/120（mock 快照）。
- demo DWD 财务：449 行，仅 `total_profit` + `revenue`。
- 国外 ODS 成对很多；正式国外 DWD 财务 **0 行**，暂不并。

## 待建 / 缺口

- 多数企业年报无成对利润+营收：该年 / 该企无法计算，不是整条缺口。
- 国外 DWD 未灌。
- demo 无 `net_profit` 列：本口径在 demo 库现算缺分子；本波不改 DDL。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.4`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。王惠正文「利润总额」与公式 `pure_profit` 不一致，本波按净利润。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 COVER-STAT-L01 逐年落表 + KPI 最新年，分子=pure_profit，产出列禁止当源*
