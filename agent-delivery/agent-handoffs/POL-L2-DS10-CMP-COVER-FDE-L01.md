# handoff · POL-L2-DS10-CMP-COVER-FDE-L01

- 任务：政策重点比对 · 需规分句闭合（卡1=A、卡2=B）
- 日期：2026-11-12
- 身份：`agent:fullstack-agent`（本会话串 A–E）
- 监管：`human:淮政玮`
- 强度：ponytail full
- ponytail: 中档 FDE；优缺点只读 gapfill；217 复用 trackingExport，无新 npm

## 范围与实现

| 分句 | 作为 |
|---|---|
| 213-3 | VersionCompareModal live 展示增/改/删 Tag 计数（`changeStatsOf`） |
| 214-5 | ComparisonModal live 差异柱图；无分轴空 |
| 214-6 | gapfill `pros_text`/`cons_text` → detail 贴列 → 每策优缺点 |
| 217-5 | BenchmarkCompareModal 导出 Word/PDF（trackingExport） |
| G3 | 合规用例形态期望已补 |

## 产物

- 简报 A/C/E：`sdd/简报/2026-11-12-CMP-COVER-FDE-*.md`
- 四单：`sdd/l2/POL-L2-DS10-CMP-{ARCH,DATA,API}.md`
- Java：`PolicyGapfillController` DETAIL_SQL；`PolicyPanoramaService.attachCompare`
- FE：`ComparisonModal` / `VersionCompareModal` / `BenchmarkCompareModal` / `compareLive.ts`
- 灌数：`seed_gapfill_policy_cmp.py` + `gapfill_policy_detail_compare_alter_pros_cons.sql`
- 线上 gapfill：已 ALTER + 演示对 18363390/18407696 优缺点已灌
- 用例：`POL-L2-DS10-CMP-合规演示用例.md`

## 验收证据

- `python scripts/seed_gapfill_policy_cmp.py --check` ok
- `node src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` 全绿
- MySQL `gkxlumenx_gapfill.gapfill_policy_detail_compare` 已有 `pros_text`/`cons_text`

## 架构合规

- D12 ✅ 未调 demo 服务
- D16 ✅ 只写 gapfill_
- D18 ✅ 优缺点读表，非接口写死 mock
- 无新 metric_id / 不改 D4
- 前端推送待人工确认（fe-manual-confirm-push）

## cost

- actual_tokens: 见会话用量
- model_used: Composer
- actual_cost: 估 <$10
- cost_warn: false
