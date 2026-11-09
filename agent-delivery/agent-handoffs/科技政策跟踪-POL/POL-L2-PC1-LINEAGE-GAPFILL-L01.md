# POL-L2-PC1-LINEAGE-GAPFILL-L01 · 溯源索引缺项表灌数

- 任务：`POL-L2-PC1-LINEAGE-GAPFILL-L01`
- 日期：2026-11-08
- 执行：`agent:data-agent` · 监管：`human:淮政玮`
- ponytail: full
- 上游：`sdd/l2/POL-L2-PC1-LINEAGE-ARCH.md` / `LINEAGE-DATA.md`

## 1. 范围与实现

| 项 | 内容 |
|---|---|
| 库 | `gkxlumenx_gapfill`（`10.50.11.76:3306`） |
| 表 | `gapfill_policy_lineage_index` |
| 脚本 | `lumen-algo-py/scripts/seed_gapfill_policy_lineage_index.py` |
| SQL | `lumen-algo-py/scripts/mysql/gapfill_policy_lineage_index.sql` |

行两类：

| link_kind | 行数 | is_mock | 说明 |
|---|---|---|---|
| 原文条款 | 5 | 0 | 冻结自 `demo_gkxlumenx_ads.policy_text_parse` 真实条款（policy_id `18319069`/`18319394`/`18318861`） |
| 条款结论 | 5 | 1 | 假想结论挂真实条款；`fill_method=manual` |

未写 ODS/DWD/ADS/供应方库。未读 `gapfill_policy_report_trace`。`metric_id` 全 NULL。

## 2. 命令与证据

```text
python scripts/seed_gapfill_policy_lineage_index.py --check
# → {"mode":"check","ok":true,"rows":{"原文条款":5,"条款结论":5}}

$env:LUMEN_ALGO_MYSQL_PASSWORD = "<secret>"
python scripts/seed_gapfill_policy_lineage_index.py --apply
# → {"mode":"apply","connected":true,"db":"gkxlumenx_gapfill","rows":{"total":10,"原文条款":5,"条款结论":5}}
```

## 3. 架构合规

| 铁律 | 结果 |
|---|---|
| D16/D18 gapfill 只写缺项库 | ✅ |
| 不伪闭合：真条款不编造 | ✅ ADS 快照 |
| 结论端 mock + MockBadge 字段 | ✅ is_mock=1 |
| 不新造 metric_id | ✅ |

## 4. cost（占位）

`actual_tokens` / `model_used` / `actual_cost` / `cost_warn` 完工总控回填。
