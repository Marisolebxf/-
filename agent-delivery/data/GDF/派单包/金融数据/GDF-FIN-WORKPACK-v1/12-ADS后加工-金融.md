# 12 — ADS 后加工：金融（FIN-ADS）

> **读者**：GDF 数据中台产线。  
> **版本**：v1.0（2026-11-09）。**草稿口径，未会签，未在库上执行**：下面的 SQL 只做语法与口径说明，GDF 配作业前由架构师 / data-agent 复核。  
> **一句话**：Wave B 的 `fin_*` 当日成功后，写 4 张 `ads_fin_*`；Java **只读** ADS；本环节不写 ES / 图谱 / 向量库。

---

## 0. 位置

```text
gkxlumenx_ods ──Wave B──► gkxlumenx_dwd.fin_*
                              │ 对应 DWD 当日 success
                              ▼
                  ② 本文（FIN-ADS-1 ~ 4）
                              │
                              ▼
                  gkxlumenx_ads.ads_fin_*  ──► Java 只读
```

两阶段铁律：无 ①（Wave B 回传）不算开工跑通；无 ② 不算业务可消费。本包 ② 只写口径，**不宣称已跑通**。

---

## 1. 与指标的关系（先读）

| 项 | 说明 |
|---|---|
| 候选消费方 | `ads_fin_industrial_fund_summary` 的 `reg_capital_wan_sum`、`cum_inv_amount_sum` 与已有指标调研点名的产业基金数据同源（`M_INNOV_PG_FUND` 用 `reg_capital`；`M_TECH_INVEST_AMOUNT` 的 D7 基金项目只有基金级）。**仅是候选**，口径是否沿用由算法 / 指标负责人另行会签 |
| `metric_id` | 本包 ADS **不带** `metric_id` 列，也不改任何指标 seed / 矩阵 |
| D1–D4 | 本包不改。ADS 有行 ≠ D4 `live`；D4 按 `data-lineage-policy.md` 实况另判 |
| 缺口不补 | `M_INNOV_PG_FUND` 调研已确认补贴资助整类无表、`dwd_fund_basic_info` 0 行。本包**不**用项目资助额或 mock 填。基金级汇总**不冒充**项目级 |
| 其他 ADS | 行情、期权、外汇、公募基金：v1 无 DWD，无 ADS |
| 候选未做 | 融资 / 投资事件按机构×年汇总：依赖 ENT-v4 的 `enterprise_financing` / `enterprise_invest`，企业包回传后另议，**本包不建** |

---

## 2. 四张 ADS 口径

通用：

- 每批 `stat_date = CURDATE()`。同一事务内 `DELETE ... WHERE stat_date = :stat_date` 再 `INSERT`，可重跑。
- `calc_batch_id` 由作业填，建议 `fin_YYYYMMDD`。本包不写任何 mock 行。
- 值取不到写 `NULL`，不写 0。
- 去重只在 ADS 层、只取 `src_dwd_id` 最大的一行（DWD 不去重，OPEN-FIN-02）。`ponytail:` 天花板——若 `industrial_fund_id` / `bond_code` 重复数很高，说明源数据有口径问题，应回供应方，不能靠这一条长期兜底。

### 2.1 FIN-ADS-1 `ads_fin_industrial_fund_summary`

粒度：`reg_region_l1 × fund_type × est_year`。读：`fin_industrial_fund`、`_gp`、`_lp`、`_inv_summary`。

```sql
-- 草稿，未执行
INSERT INTO gkxlumenx_ads.ads_fin_industrial_fund_summary
 (stat_date, reg_region_l1, fund_type, est_year, fund_cnt, state_owned_fund_cnt,
  reg_capital_wan_sum, reg_capital_parsed_cnt, reg_capital_parse_rate,
  gp_rel_cnt, lp_rel_cnt, lp_sub_capital_sum, cum_inv_amount_sum, calc_batch_id)
WITH f AS (
  SELECT industrial_fund_id,
         NULLIF(SUBSTRING_INDEX(reg_region,'-',1),'') AS reg_region_l1,
         fund_type, YEAR(est_date) AS est_year, state_owned, reg_capital_wan,
         ROW_NUMBER() OVER (PARTITION BY industrial_fund_id ORDER BY src_dwd_id DESC) AS rn
  FROM gkxlumenx_dwd.fin_industrial_fund),
f1 AS (SELECT * FROM f WHERE rn = 1),
gp AS (SELECT industrial_fund_id, COUNT(*) AS c
       FROM gkxlumenx_dwd.fin_industrial_fund_gp GROUP BY industrial_fund_id),
lp AS (SELECT industrial_fund_id, COUNT(*) AS c, SUM(sub_capital) AS s
       FROM gkxlumenx_dwd.fin_industrial_fund_lp GROUP BY industrial_fund_id),
sm AS (SELECT industrial_fund_id, SUM(cum_inv_amount) AS a
       FROM gkxlumenx_dwd.fin_industrial_fund_inv_summary GROUP BY industrial_fund_id)
SELECT CURDATE(), f1.reg_region_l1, f1.fund_type, f1.est_year,
       COUNT(*), SUM(f1.state_owned = '是'),
       SUM(f1.reg_capital_wan), SUM(f1.reg_capital_wan IS NOT NULL),
       SUM(f1.reg_capital_wan IS NOT NULL) / COUNT(*),
       SUM(COALESCE(gp.c, 0)), SUM(COALESCE(lp.c, 0)), SUM(lp.s), SUM(sm.a), :calc_batch_id
FROM f1
LEFT JOIN gp ON gp.industrial_fund_id = f1.industrial_fund_id
LEFT JOIN lp ON lp.industrial_fund_id = f1.industrial_fund_id
LEFT JOIN sm ON sm.industrial_fund_id = f1.industrial_fund_id
GROUP BY f1.reg_region_l1, f1.fund_type, f1.est_year;
```

提示：`gp_rel_cnt` / `lp_rel_cnt` 是**关系条数**，不是去重机构数。`lp_sub_capital_sum`、`cum_inv_amount_sum` 单位未确认（OPEN-FIN-03），展示前不得标「亿元」或「万元」。

### 2.2 FIN-ADS-2 `ads_fin_bond_issue_summary`

粒度：`issue_year × bond_class × issuer_type`。读：`fin_bond`。

```sql
-- 草稿，未执行
INSERT INTO gkxlumenx_ads.ads_fin_bond_issue_summary
 (stat_date, issue_year, bond_class, issuer_type, bond_cnt, issuer_cnt,
  issue_amount_yi_sum, coupon_rate_avg, calc_batch_id)
WITH b AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY bond_class, bond_code ORDER BY src_dwd_id DESC) AS rn
  FROM gkxlumenx_dwd.fin_bond)
SELECT CURDATE(), YEAR(issue_date), bond_class, issuer_type,
       COUNT(*), COUNT(DISTINCT issuer), SUM(issue_amount_yi), AVG(current_coupon_rate), :calc_batch_id
FROM b WHERE rn = 1
GROUP BY YEAR(issue_date), bond_class, issuer_type;
```

### 2.3 FIN-ADS-3 `ads_fin_listed_company_snapshot`（v1 仅 A 股）

粒度：一个 `org_id` 一行。读：`fin_security`、`fin_valuation_daily`（`market='CN'`）、`fin_corp_basic`、`fin_industry_class_his`。

取数规则：

1. **代表证券**：该机构下 `is_listing = 1 AND is_delisted = 0` 且在 CN 估值表里有数据的证券，取 `sec_code` 升序第一只。`ponytail:` 天花板——同一机构有 A 股与其他证券时，这条规则是简单默认，不是业务口径；换规则不改表结构（OPEN-FIN-09）。
2. **最新估值**：该证券 `dt` 最大的一行。
3. **一级行业**：申万 / 证监会 / 中信各取 `industry_level = 1 AND is_latest = 1`、`inclusion_date` 最大的一行。**`industry_level` 在不同体系里的含义没有核对过**（源样例里申万有 3、证监会有 2，未必 1 就是一级），先按 1 写，实测后校正（OPEN-FIN-11）。
4. 港股、美股：v1 不出快照。

```sql
-- 草稿，未执行
INSERT INTO gkxlumenx_ads.ads_fin_listed_company_snapshot
 (stat_date, org_id, org_name_cn, reg_region, sec_id, sec_code, td_mkt, valuation_dt,
  pe_ttm_ed, pb_mrq, ps_ttm_ed, pcf_ttm_ed, tmv_rmb,
  sw_l1_code, sw_l1_name, crsc_l1_code, crsc_l1_name, citic_l1_code, citic_l1_name, calc_batch_id)
WITH v AS (
  SELECT sec_id, dt, pe_ttm_ed, pb_mrq, ps_ttm_ed, pcf_ttm_ed, tmv_rmb,
         ROW_NUMBER() OVER (PARTITION BY sec_id ORDER BY dt DESC, src_dwd_id DESC) AS rn
  FROM gkxlumenx_dwd.fin_valuation_daily WHERE market = 'CN'),
vl AS (SELECT * FROM v WHERE rn = 1),
p AS (
  SELECT s.org_id, s.sec_id, s.sec_code, s.td_mkt, s.issuer_name,
         ROW_NUMBER() OVER (PARTITION BY s.org_id ORDER BY s.sec_code, s.src_dwd_id) AS rn
  FROM gkxlumenx_dwd.fin_security s
  JOIN vl ON vl.sec_id = s.sec_id
  WHERE s.is_listing = 1 AND s.is_delisted = 0 AND s.org_id IS NOT NULL),
pp AS (SELECT * FROM p WHERE rn = 1),
ind AS (
  SELECT org_id, class_system, industry_code, industry_name,
         ROW_NUMBER() OVER (PARTITION BY org_id, class_system ORDER BY inclusion_date DESC, src_dwd_id DESC) AS rn
  FROM gkxlumenx_dwd.fin_industry_class_his
  WHERE class_system IN ('SW_CN','CRSC_CN','CITIC_CN') AND industry_level = 1 AND is_latest = 1)
SELECT CURDATE(), pp.org_id, COALESCE(c.org_name_cn, pp.issuer_name), c.reg_region,
       pp.sec_id, pp.sec_code, pp.td_mkt, vl.dt,
       vl.pe_ttm_ed, vl.pb_mrq, vl.ps_ttm_ed, vl.pcf_ttm_ed, vl.tmv_rmb,
       sw.industry_code, sw.industry_name, cs.industry_code, cs.industry_name, ci.industry_code, ci.industry_name,
       :calc_batch_id
FROM pp
JOIN vl ON vl.sec_id = pp.sec_id
LEFT JOIN gkxlumenx_dwd.fin_corp_basic c ON c.org_id = pp.org_id
LEFT JOIN ind sw ON sw.org_id = pp.org_id AND sw.class_system = 'SW_CN'   AND sw.rn = 1
LEFT JOIN ind cs ON cs.org_id = pp.org_id AND cs.class_system = 'CRSC_CN' AND cs.rn = 1
LEFT JOIN ind ci ON ci.org_id = pp.org_id AND ci.class_system = 'CITIC_CN' AND ci.rn = 1;
```

> `fin_corp_basic` 若出现同一 `org_id` 多行（OPEN-FIN-02），上面的 `LEFT JOIN` 会把快照行放大，违反 `uk_stat_org`。配作业前先登记 `fin_corp_basic` 的 `org_id` 重复数；有重复时在 `c` 处先按 `src_dwd_id` 最大去重。

### 2.4 FIN-ADS-4 `ads_fin_main_biz_latest`

粒度：`org_id × dim_type × dim_name`（取每个机构每个维度的最新报告期）。读：`fin_main_biz_composition`。

```sql
-- 草稿，未执行
INSERT INTO gkxlumenx_ads.ads_fin_main_biz_latest
 (stat_date, org_id, dim_type, dim_name, occur_period, core_biz_income,
  core_biz_income_prop, core_biz_cost, gross_margin, calc_batch_id)
SELECT CURDATE(), org_id, dim_type, dim_name, occur_period, core_biz_income,
       core_biz_income_prop, core_biz_cost, gross_margin, :calc_batch_id
FROM (
  SELECT m.*, DENSE_RANK() OVER (PARTITION BY org_id, dim_type ORDER BY occur_period DESC) AS r
  FROM gkxlumenx_dwd.fin_main_biz_composition m) t
WHERE r = 1;
```

提示：`occur_period` 当 `YYYYMM` 字符串按字典序取最大。若实测出现其他格式（OPEN-FIN-04），先回供应方，再改这一条。

---

## 3. 触发与顺序

| 作业 | 触发条件 |
|---|---|
| FIN-ADS-1 | `FIN-B3-FUND` 的 5 张目标表当日都 `success` |
| FIN-ADS-2 | `FIN-B4-BOND` 当日 `success` |
| FIN-ADS-3 | `FIN-B2-SEC`、`FIN-B5-INDCLASS`、`FIN-B7-VAL`、`FIN-B1-CORP` 当日都 `success` |
| FIN-ADS-4 | `FIN-B6-MAINBIZ` 当日 `success` |

- 任一前置未成功：对应 ADS 不跑，不回滚已成功的 B。
- ADS 失败：只记该作业，不回滚 B，不连带其他 ADS。
- 四个 ADS 互不依赖，不要合成一个大作业。

---

## 4. 谁写谁读

| 角色 | 做 | 不做 |
|---|---|---|
| GDF | 配 4 个作业，按 §3 触发，回执带行数与 `calc_batch_id` | 写 ES / 图谱 / 向量库；写 mock；改 DWD |
| 本包 SQL | 只读 `gkxlumenx_dwd.fin_*`，只写 `gkxlumenx_ads.ads_fin_*` | 读供应方 `gkx.dwd_*`、读 `gkxlumenx_ods`、读 demo 库 |
| Java | 只读 ADS | 直连 DWD / ODS；算法 |

执行形态（SQL 作业还是 Python 节点）待 GDF 回复（OPEN-FIN-06）。若需 Python，另派，不在本包写算法。

---

## 5. 验收

1. 4 张表建好后，每张 ≥20 条抽样，回查到 `fin_*` 源行。
2. `ads_fin_industrial_fund_summary`：`SUM(fund_cnt)` 等于 `fin_industrial_fund` 按 `industrial_fund_id` 去重后的行数；`reg_capital_parse_rate` 与 Wave B 验收登记的解析成功率一致。
3. `ads_fin_listed_company_snapshot`：`(stat_date, org_id)` 无重复；登记 `sw_l1_code IS NULL` 占比。
4. 重跑同一 `stat_date` 行数不变。
5. 没有任何 `mock_` 行、没有 0 代替缺失。

---

## 6. 本期不做

- 行情 / 期权 / 外汇 ADS；公募基金 ADS。
- 事件类（融资 / 投资 / 并购）ADS。
- 港股 / 美股快照。
- 实时指标；T+1 以外的调度。
- Java 接口、前端展示、指标 8 件套登记。
