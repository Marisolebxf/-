# 营收（M_ENT_REVENUE_LATEST）

> 口径真源：王惠底稿「最新年度营业收入」→ 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。**粒度=企业**。国内 ODS `operating_revenue` 非全空（286/20000 有值），**可以按企算**，不套研发投入占比的「当前无法执行」。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_REVENUE_LATEST`
- **指标名称**：营收
- **一级模块**：企业分析
- **二级模块**：企业查询
- **三级模块**：企业画像
- **更新频率**：年
- **对齐状态**：按企取最新年营收；无值该企不算，整条能算
- **是否在数据库**：ODS 有 `operating_revenue`；DWD `enterprise_finance_history.revenue` 有列
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E23

## 口径定义

**每个企业一条**：最近一个年度的营业收入。

- 取值：`enterprise_finance_history.revenue`，该 `org_id` 的 `MAX(data_year)` 那一行。
- ODS：`dwd_org_annual_financial_info.operating_revenue`，年字段是 `year`（不是 `yearTime`）。
- 无财务行或 `revenue` 空：**该企业无法计算**。不是整条指标无法执行。
- 不挂产业。禁止筛选范围加总。
- 国外：对等表 `enterprise_forg_finance_history.operating_revenue` 正式库 0 行，暂不并。不造表。
- **禁止**抄 `enterprise_base.revenue_latest`。
- **禁止**套用 `M_ENT_RD_INVESTMENT_RATIO` 的整条「当前无法执行」（那边 ODS RD 全空；这边营收不是全空）。

## 计算逻辑说明

```
SELECT org_id, revenue
FROM enterprise_finance_history t
WHERE t.data_year = (
  SELECT MAX(data_year) FROM enterprise_finance_history x
  WHERE x.org_id = t.org_id
)
```

无行或 `revenue` IS NULL → 该企无法计算。

对应 seed `formula`：按企最新年 `revenue`；可执行，不加「当前无法执行」。

**计算公式文件**：`M_ENT_REVENUE_LATEST.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
```

- `revenue` ← `operating_revenue`
- `data_year` ← `year`

来源系统（`source_systems`）：国内机构要素库。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- 国内年报 `operating_revenue`：20000 行，非空 286（可算，稀疏）。
- 正式 DWD `enterprise_finance_history.revenue`：709/709 非空（mock 填满，对不上 ODS 覆盖，故 `is_mock=true`，不升 D4）。
- 国外 ODS `operating_revenue` 非零 12312；正式 DWD 国外财务 0 行，暂不并。

## 待建 / 缺口

- 多数企业年报无营收：按口径该企无法计算，不是整条缺口。
- 国外 DWD 未灌。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 按企最新年营收，可算*
