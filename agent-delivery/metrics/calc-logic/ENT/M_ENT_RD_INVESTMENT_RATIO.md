# 研发投入占比（M_ENT_RD_INVESTMENT_RATIO）

> 口径真源：王惠底稿「R&D / 营业收入」→ 2026-08-31：`formula` 只写怎么算；有没有数是另一回事。  
> **粒度=企业**。不挂产业。不 reuse `M_ENT_AVG_RD_INVESTMENT`（那条是选定产业 AVG + 半连接）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 口径定义

**每个企业一条**：最近一个完整自然年度，研发投入占营业收入的比例（×100）。

```
rd_investment / revenue * 100
FROM enterprise_finance_history
WHERE data_year = 该 org 最近完整自然年
```

- 分子：`rd_investment` ← ODS `arch_development_am`（血缘，不是 FROM）。
- 分母：同表 `revenue` ← `operating_revenue`。
- 营收空或 0、分子空：**该企业无法计算**（除零）。不是整条指标算不了。
- 不挂产业。不是筛选范围加总，也不是 AVG_RD。
- 国外暂不并。不造表。
- **禁止**上市财务。
- **禁止**读 `rd_investment_ratio` / 主档 `enterprise_base.rd_investment_ratio`（产出，不当输入）。

## 两点分开（强制）

### ① formula

DWD 有 `rd_investment`、`revenue` 就能写完。与 AVG_RD 同 RD 列。

### ② 有没有数

ODS `arch_development_am` 空、DWD mock 填数、国外财务 0 行：只记灌数 / 不升 D3 D4。**不写「当前无法执行」**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_finance_history` | 表在，有列 |
| 目标 | 建议 `ads.ent_rd_ratio_latest`（`org_id + data_year + ratio`） | **缺口：无此表** |

源 ≠ 目标。禁止把产出列当已接通。

**计算公式文件**：`M_ENT_RD_INVESTMENT_RATIO.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
```

来源系统：国内机构要素库。

## 分场景（不进 8 件套）

- 场景 A · 单企画像：按 `org_id` 取最新完整年一行。
- 场景 B · 列表：批量按企，禁止全集加总当「产业占比」。
- 生产按 `org_id` 查快照；禁止请求路径全表扫年报。

## 现网探针（2026-08-27；不进 8 件套）

- DWD `enterprise_finance_history`：709 行，`rd_investment`/`revenue` 有值（mock，不当接通）。
- ODS `arch_development_am`：全 NULL（②）。
- 正式 `enterprise_forg_finance_history`：0 行。

## 待建 / 缺口

- **缺口：无独立目标表。**
- D3 / D4 本波不升。`is_mock: true`。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 误把 ODS 空写入无法执行；2026-08-31 方案1：formula 与有数分开*
