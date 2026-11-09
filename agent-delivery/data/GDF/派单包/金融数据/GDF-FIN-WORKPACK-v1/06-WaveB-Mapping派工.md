# Wave B — Mapping / ETL 派工（FIN v1.0）

> **DDL**：`10-DWD-MySQL-DDL/fin-dwd-draft.md`（草稿，未签收）  
> **Mapping**：`09-金融域-ETL-Mapping明细-源表到DWD.md`  
> **禁止**：洗 P2 / 0 行表；洗企业包三张重叠表；自造 `org_id`；把 `--` 写成 0；读写 demo 库

## 1. 触发条件

1. Wave A 中 `mapping: wash` 且 `owner: FIN` 的表（19 张）贴源验收通过（行数对账、`SHOW CREATE TABLE` 差异已登记）
2. 可写 `gkxlumenx_dwd`，`fin_*` 已建（建表草稿见 `10`；OPEN-FIN-01 未关前由 GDF 按草稿建，建后回报）
3. **不依赖** `enterprise_base`。企业包未就绪不阻塞本包任何作业

## 2. 作业拆分

作业之间互不依赖，可并行；大表单独调度，不要拖住小表。

| 作业 | 输入 | 输出 | 分期 | 备注 |
|---|---|---|---|---|
| `FIN-B1-CORP` | `dwd_corp_basic_info` | `fin_corp_basic` | P0 | |
| `FIN-B2-SEC` | `dwd_sec_basic_info` | `fin_security` | P0 | 124 万行，按 `updated_time` 增量 |
| `FIN-B3-FUND` | 产业基金 5 张 | `fin_industrial_fund` / `_gp` / `_lp` / `_strategy` / `_inv_summary` | P0 | 5 张目标表可拆 5 个子作业 |
| `FIN-B4-BOND` | 科创债 + 高新债 | `fin_bond` | P0 | UNION ALL |
| `FIN-B5-INDCLASS` | 行业分类 4 张 | `fin_industry_class_his` | P1 | UNION ALL |
| `FIN-B6-MAINBIZ` | 主营构成 3 张 | `fin_main_biz_composition` | P1 | UNION ALL；约 137 万行 |
| `FIN-B7-VAL` | 估值 3 张 | `fin_valuation_daily` | P1 | UNION ALL；A 股 322 万行，按 `dt` 增量 |

没有 `FIN-B*-P2`：P2 / 0 行表本期不洗。

## 3. 作业状态

| 作业 | 状态 | 阻塞边界 |
|---|---|---|
| `FIN-B1` ~ `FIN-B7` | 可配置 | 仅受各自 Wave A 与 `fin_*` 建表影响，互不阻塞 |
| P2 / 0 行表洗数 | **不配置** | v1 不出明细（OPEN-FIN-07） |
| 重叠三表 | **不在本包** | 归 ENT-v4 |

## 4. 交付物

- 目标表建改说明（对照 `10` 草稿）
- 字段可追溯到 09 §3.4 ~ §3.14
- `reg_capital_wan` 解析成功数 / 失败数 / 外币数（09 §3.3）
- 每张目标表 ≥20 条抽样，附 `src_dwd_id` 回查
- 行数对账（09 §7）
- 自然键重复数（OPEN-FIN-02）
- 增量、删除与重跑策略回签；**未回签不得宣称 CDC 闭环**
- OPEN-FIN-* 书面登记

## 5. 本侧后续

② 后加工（`12`）读 `fin_*` 写 `ads_fin_*`，不要求 GDF 写 Java 或前端。
