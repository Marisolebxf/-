# POL-L2-DS12-EST-234-COVER-L01

- task: `POL-L2-DS12-EST-234-COVER-L01`
- ponytail: full
- 日期：2026-11-12
- 来源：需规分句闭合简报；卡1–4 全锁 A；用户「按此计划开始」

## 范围

闭合 234 区域经济发展空间模拟：字典键对齐、live 闸门、用例形态、说明书裁定。不扩 232/233/235/236。

## 实现

| 层 | 改动 |
|---|---|
| 数据 | `simulation.py` + `seed_gapfill_policy_sim_forecast.py` 区域行 → 粤×人才政策、深×科创政策；`--check` 已覆写 `gapfill_policy_sim_forecast.sql` |
| FE | `EstimateWorkbench.vue`：`canLiveSpatialSim`=区域+类型；空态文案对齐 |
| 用例 | 合规 234 升可演 + 三维/热力形态；TEST-L01 区域键与 TC-06/07 |
| 说明书 | §234 补闸门、产业非契约、三维 G6、live 热力单列、可演键 |

## 验收证据

- `node .../simulationLive.test.mjs` 通过
- 仓内 SQL INSERT 已见 `人才政策`/`科创政策` 区域行
- **线上**：`python scripts/seed_gapfill_policy_sim_forecast.py --apply` **尚未执行**（等用户批准回灌）

## 架构合规

- D12/D16/D18：仍读 gapfill，不直连 demo，不接口写死 mock
- 不改 Nacos / 不 FORCE_REPUBLISH

## 待人

1. 批准线上 gapfill `--apply`（或等价回灌）后 ACCEPT-LOOP 回验 234
2. 前端仓改动待确认后再 push（`fe-manual-confirm-push`）
