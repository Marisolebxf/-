# 全球企业科研人数（M_ENT_RESEARCHER_COUNT）

> 口径真源：T0-X / Q-E32-01 → 2026-08-31 方案1：`formula` 只写怎么算；有没有数是另一回事。  
> 禁止从业人数、禁止研发投入金额冒充。Q-E32-01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 口径定义

全球合计：每企取最新一个有年报的自然年，把科研人员数加总。

```
国内：该企 MAX(data_year) 行的 development_employee
国外：该企 MAX(data_year) 行的 rd_staff
本条 = SUM(国内有效值) + SUM(国外有效值)
```

- 无值 / NULL / 占位 0：**该企不进合计**，不补 0。
- 选未来产业：成员表半连接收 `org_id` 后再 SUM（跟 AVG_RD 同一成员表，本条是 SUM 不是 AVG）。
- 国外无上链：选产业过滤不含国外。未选产业时国外仍并入全球合计。
- **禁止** `employees_number`（从业人数）。
- **禁止** RD 金额。
- **禁止**上市财务子集冒充全部法人。

## 两点分开（强制）

### ① formula

列名已钉。DWD 有 `development_employee` / `rd_staff` 就能写 SUM。国内财务表现网无该列 = **补列缺口**，不把公式改成无法执行。

### ② 有没有数

ODS 空置率、mock、未灌：只记探针 / 不升 D3 D4。**不写「当前无法执行」**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_finance_history.development_employee` / `enterprise_forg_finance_history.rd_staff` | 国内财务表待补列 |
| 目标 | 建议 `enterprise_researcher_year_sum`（`stat_year + researcher_cnt`） | **缺口：无此表** |

源 ≠ 目标。本波不改 GDF DDL。

## 分场景 / 千万级（不进 8 件套）

- 未选产业：全球 SUM（国内 ∪ 国外）。
- 选产业：`DISTINCT org_id` 自 `enterprise_industry_chain` 半连接后再 SUM。
- 生产：按企取最新年再汇总；禁止请求路径扫年报全历史。

**计算公式文件**：`M_ENT_RESEARCHER_COUNT.md`

## 源表字段

```
enterprise_finance_history.development_employee <- ods: dwd_org_annual_financial_info
enterprise_forg_finance_history.rd_staff <- ods: dwd_foreign_org_annual_financial_info
```

空置率不进 `source_systems`。来源系统：国内机构要素库、国外机构要素库。

## 现网探针（live `gkx`，2026-08-31；不进 8 件套）

| 表.列 | 行数 | NULL | 有效 >0 | 空置率 |
|--------|------|------|---------|--------|
| `dwd_org_annual_financial_info.development_employee` | 517,597 | 517,597 | 0 | 100% |
| `dwd_foreign_org_annual_financial_info.rd_staff` | 18,193 | 18,193 | 0 | 100% |
| `dwd_org_stock_finance_info` | — | — | — | 无研发人员列，不采用 |

## 待建 / 缺口

1. 国内 `enterprise_finance_history` 补研发人员列。
2. **无独立目标表。**
3. D3 / D4 本波不升。`is_mock: true`。Q-E32-01 🟡。

---
*2026-08-31 COVER-STAT-L01：SUM 最新年研发人员；方案1 与有数分开*
