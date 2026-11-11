# POL-L2-DS12-EST-236-COVER-FDE · C/D/E 收口（本窗口连跑）

- 总单：`POL-L2-DS12-EST-236-COVER-FDE-L01`
- 日期：2026-11-12
- 裁定：卡1=B · 卡2=A · 补政策选择
- 监管人授权：本窗口按推荐连跑（非分会话对抗会签；C 以说明书/四单回写代替多身份对抗）

## C · 会签产物（本窗代写）

- 说明书 #### 236：功能点表 236-0…8 + 状态表；差表改「按政策出识别+意见」
- EST-ARCH §5.5 / 调用链 §7；EST-API §7；SIM-DATA §8：`policy_id` + `评估识别` 列
- 明确：纳入模型 G6 不做

## D · 实现

| 仓 | 改动 |
|---|---|
| lumen-algo-py | seed/SQL 意见表扩列；4 条识别 + 3 条意见挂 `18363390`；`simulation.py` `_stake_rows`；迁移 `gapfill_policy_sim_stakeholder_236_alter.sql` |
| lumen-svc-platform | display `POLICY_KINDS` 含利益攸关方；element 按 `policy_id` 读两种 row_kind；单测同步 |
| lumen-ui-science-pc | 条件栏政策选择；live 绑识别四卡；`simulationJobBody` 必带政策；去「演示」placeholder；页头 KPI 用样例政策计参与意见条数 |

自检：`seed --check` 绿；`simulationLive.test.mjs` 绿；`FE-POL-03A` 至利益攸关断言绿（文件后段 exportHtmlDoc 为既有 242 漂移，非本叶）。

## E · 用例

`POL-L2-DS12-EST-合规演示用例.md` 236 行：政策 `18363390` + 四卡原文 + 三意见 + 形态（政策选择 / 无纳入开关）。

## 线上待办（部署后）

1. 对 `gkxlumenx_gapfill` 执行 `gapfill_policy_sim_stakeholder_236_alter.sql`（列已存在则跳过）
2. 再跑推演按钮 / seed `--apply` 灌 7 行（3 意见 + 4 识别）
3. Java/FE CI rollout 后按用例冒烟

## ponytail

`ponytail: full` · 同表扩列最短路径；未新建第二张表；纳入模型不实现。
