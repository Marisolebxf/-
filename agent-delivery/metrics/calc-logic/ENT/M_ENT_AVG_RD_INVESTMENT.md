# 平均研发投入（M_ENT_AVG_RD_INVESTMENT）

> 口径真源：王惠底稿（选定产业、最近完整自然年、R&D 算术平均）→ 2026-08-31 回看：①② 分开；实现锁 **两张输入 + 查询半连接**。  
> 正名：`M_ENT_RD_INVEST_AVG` → 本条（不另建）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 口径定义

选定产业内全部法人，最近一个完整自然年度 R&D 经费内部支出的算术平均。

- 产业键 = 未来产业 `cluster_id`（`CL-FUT-01`～`05`）。Q068 仍 🟡。
- **多选 = 成员并集按 `org_id` 去重后再 AVG**（一企只进一次）。
- 未选产业：**不计算**（请求必须带产业键）。
- 只国内。国外无上链表，选产业时**不并**。
- `rd` 空或占位 0：**该企不进均**，不是整条无法计算。
- **禁止**上市 `dwd_org_stock_finance_info`（覆盖不到全部法人）。
- **禁止**各产业预聚合 `sum_rd/n` 加总冒充去重平均。
- **禁止**无过滤 `finance_history JOIN industry_chain`（一企多链会把 RD 算多次）。

## 两点分开（强制）

### ① DWD 能不能写

`enterprise_finance_history.rd_investment` + `enterprise_industry_chain` 在，公式就能写完。与 `RD_INVESTMENT_RATIO` 同 RD 列。

### ② ODS → DWD

国内年报 `arch_development_am` 空、DWD mock 填数、国外 RD 全 0：只记灌数 / 不升 D3 D4。**不写「当前无法执行」**。

## 实现：两张输入 + 查询半连接

| 角色 | 表 | 一行 | 现网 |
|------|-----|------|------|
| 输入 1 | 建议 `ads.ent_rd_latest`（`org_id, data_year, rd_investment`） | 每企最近完整年一条；空/占位 0 不进 | **缺口：无此表**；源是 `enterprise_finance_history` |
| 输入 2 | `enterprise_industry_chain` | `org_id + 产业键` | 表在 |
| 本条 | 查询半连接，**不预计算产业组合** | 当前所选键的一个 AVG | 无独立 AVG 结果表 |

```
成员 = DISTINCT org_id
       FROM enterprise_industry_chain
       WHERE 产业键 ∈ :selected

AVG(rd_investment)
FROM ads.ent_rd_latest
WHERE org_id ∈ 成员
```

去重只对**所选产业成员**，不是全国年报重跑。带 `org_id` / 产业键索引。

禁止：请求路径扫 `finance_history` 全历史再 JOIN 全量上链。

## 分场景 / 千万级（不进 8 件套）

- 场景 A · 单选一个未来产业：半连接成员后 AVG。
- 场景 B · 多选：同一条 SQL，`IN (:selected)`，`DISTINCT org_id` 一次。
- demo：成员少可现算。生产：先落企级快照，查询只碰两张输入。

**计算公式文件**：`M_ENT_AVG_RD_INVESTMENT.md`

## 源表字段

```
enterprise_finance_history <- ods: dwd_org_annual_financial_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

字段对照（细稿）：`rd_investment` ← `arch_development_am`；`data_year` ← `year`。计算 FROM 只用左端 DWD。

来源系统：国内机构要素库、产业链要素库。国外财务不进本条 `source_tables`。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- 国内年报 `arch_development_am`：样例行全 NULL（②）。
- 正式 DWD `enterprise_finance_history`：有 `rd_investment`，709 行 mock 填满，不当接通。
- 上市财务有非零 RD，不采用。
- `dwd_rd` 是临床试验项目表，不是企业 R&D 经费。

## 待建 / 缺口

- **缺口：无 `ads.ent_rd_latest`。**
- D3 / D4 本波不升。`is_mock: true`。Q068 🟡。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。与 `RD_INVESTMENT_RATIO` 同 RD 列、不同粒度（本条=选定产业 AVG，占比=按企）。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 曾误写成「无法计算」；2026-08-31 改为两张输入 + 半连接去重*
