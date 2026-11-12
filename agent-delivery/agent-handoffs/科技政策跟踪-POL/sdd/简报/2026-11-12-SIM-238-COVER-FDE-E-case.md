# POL-L2-DS12-SIM-238-COVER-FDE · E 波次 · 用例 / 冒烟

- 总单：`POL-L2-DS12-SIM-238-COVER-FDE-L01`
- 日期：2026-11-12
- 依据：D 灌分 + FE 柱图接线

## 用例

| 文件 | 改动 |
|---|---|
| `合规演示用例/POL-L2-DS12-SIM-合规演示用例.md` | 238 期望补导图+柱形态；样例分 88/82/75/80；主路径第 3 步同；调度核对标可演 |

## 冒烟（§6.5）

| 项 | 结果 |
|---|---|
| 库 | `patch_gapfill_policy_sim_focus_238_scores.py --apply` after = 政策目标 88 / 支持领域 82 / 实施路径 75 / 资金安排 80 |
| jobs API | `POST http://10.50.69.111:30895/display/v1/policy/simulation/jobs` 无 token → 401（鉴权闸，非数据空）；数据面已 UPDATE |
| FE 自检 | `simulationLive.test.mjs` 绿；`pnpm type-check` 绿 |
| FE-POL-03A | 既有 `exportHtmlDoc` 断言红（与本 FDE 无关，未改 interpretExport） |

## 收口

A–E 齐；handoff + cost 回填后总单可进 integration。FE 待人工确认推送。
