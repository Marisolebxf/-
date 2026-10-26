# POLICY-DDL-GAP-L10

- 任务：补 CHECK 列出的表注释和三列注释，并按 `dwd.md` 建空的 DWD `policy_text_parse`
- 状态：改库完成（本叶不改 registry）
- 执行：agent:data-agent
- 监管人：human:淮政玮
- 日期：2026-10-26
- ponytail: full
- 依据：`POLICY-DDL-CHECK-L04` 的不一致清单；`ads.md` / `dwd.md` 的 CREATE

口令未写入本文件。未改 `policy_base_info`。未 DROP。未从 ADS 拷行。

联调通过。

## 改了什么

表注释，只改 `COMMENT`，不动列和索引。demo 与产线 ADS 各 15 张，注释与 `ads.md` 的 CREATE 相同。

`policy_industry_rel` 的 `id`、`create_time`、`update_time` 补上列注释。四个库都改：`demo_gkxlumenx_dwd`、`gkxlumenx_dwd`、`demo_gkxlumenx_ads`、`gkxlumenx_ads`。类型仍是 `bigint NOT NULL AUTO_INCREMENT` 和 `datetime DEFAULT CURRENT_TIMESTAMP`，没有 `ON UPDATE`。

`policy_text_parse` 按 `dwd.md` 的 CREATE 在两个 DWD 库建空表。0 行。算法仍写 ADS 同名表。

`dwd.md` 两句过时正文已改：关联表不再写 `policy_id` 仍是 `utf8mb4_general_ci`；文本解析不再写 DWD 没有这张表。

## 改后快照

2026-10-26。行数是 `COUNT(*)`。`information_schema.TABLES.TABLE_ROWS` 是估计，不采用。

| 对象 | 结果 |
| --- | --- |
| ADS 15 张 × 2 库 | 表注释与 `ads.md` 一致，排序规则 `utf8mb4_0900_ai_ci` |
| `policy_industry_rel` × 4 库 | 三列注释为「自增主键」「写入时间」「最近一次同步时间」 |
| `demo_gkxlumenx_dwd.policy_industry_rel` | 322 行 |
| `demo_gkxlumenx_ads.policy_industry_rel` | 322 行 |
| 两个产线 `policy_industry_rel` | 0 行 |
| `demo_gkxlumenx_ads.policy_text_parse` | 20000 行，只补了表注释 |
| `gkxlumenx_ads.policy_text_parse` | 0 行 |
| 两个 DWD `policy_text_parse` | 11 列，空注释 0，表注释与 CREATE 一致，0 行 |

## 架构合规

- D1–D4：未改算法、未改调用链、未改 Nebula。✅
- D12：demo 与产线分库执行同一份结构，没有把 ADS 行写入 DWD。✅
- 未写 ODS 或供应库 `gkx`，未改 `policy_base_info`，未 DROP。✅
- D8 / D9 / D10 / D14：未改页面、未改口径、未改对象存储。✅
- 口令未写入本文件。✅

## cost

- actual_tokens: 未单列
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green
