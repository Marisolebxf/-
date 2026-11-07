# POL-L2-DS10-TREND-INGEST-FIX01 · 最新入库政策只读真实政策

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 一行 SQL 条件，未加新代码路径 |

## 问题清单

- 科创政策全景「政策来源监控与更新 → 最新入库政策」列出【调试构造】行。
- 查实：`demo_gkxlumenx_dwd.policy_base_info` 有 540 行 `source_plane='debug'`、`etl_batch_id='debug_one_map_20261107_v1'`，创建于 2026-11-07 18:39，按 `created_time DESC` 排在最前。真实政策为 `domestic` 20007 行、`global` 1 行。

## 修改内容

- `gkxlumen-element` `PolicyGapfillController.INGEST_SQL` 增加 `AND source_plane IN ('domestic', 'global')`。只影响 203 入库列表（`/v1/element/policy/ingest`）。
- 用白名单而不是排除 `debug`：以后再出现其他调试来源也不会进列表。新增真实来源时需在此补值。

## 测试结果

- 只读库验证：同条件 `ORDER BY created_time DESC, id DESC LIMIT 5` 返回日本经济产业省、山东省工信厅、珠海市政府等真实政策。
- 本机无 JDK，未编译；依赖 CI。

## 遗留风险

- 调试行仍在 DWD，可能出现在其他读 `policy_base_info` 的页面（检索、一张图）。未删除，那批数据属于一张图调试会话。

## CI/CD（必填)

- 分支：`origin/dev`
- commit：lumen-svc-platform `5a64e08`（合并 `099242e`）
- 部署：`deploy:element` 自动发布 zhipu-tts，待核对

## 架构合规自检

- ✅ 展示 → element 只读 DWD，不发起抓取，不调 demo-* 服务
- ✅ 未改写库数据

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 8000 |
| model_used | claude-opus |
| actual_cost | 0.04 |
| cost_warn | green |
