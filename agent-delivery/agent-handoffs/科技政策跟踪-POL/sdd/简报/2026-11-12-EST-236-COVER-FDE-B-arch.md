# POL-L2-DS12-EST-236-COVER-FDE · B 波次 · arch

- 总单：`POL-L2-DS12-EST-236-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：arch（本会话代写；监管人授权本窗口连跑）
- 定档：**中档** · 卡1=B · 卡2=A · 补政策选择

## 定档结论

| 项 | 裁定 |
|---|---|
| 表 | 仍用 `gkxlumenx_gapfill.gapfill_policy_sim_stakeholder`，**不**新建第二张表 |
| `policy_id` | 参与意见与评估识别行均必填；样例键 `18363390` |
| `row_kind` | 闭集扩为 `参与意见` \| `评估识别` |
| 识别列 | 新增可空列 `audit_item` / `audit_result` / `audit_text`；参与意见行留空 |
| 意见列 | `actor_role` / `channel_name` / `opinion_text` / `opinion_at` 改为可空（识别行留空） |
| jobs | `kind=利益攸关方` **必带** `policy_id`；无政策不查表；一次返回该政策下两种 `row_kind` |
| 纳入模型 | **不做**（G6） |
| metric | 不新注册；行上 `metric_id` 仍 NULL；D4 mock |

## 停机

未触新建正式库表 / Neo4j / 越层；ALTER 仅限 gapfill 意见表，按 D16/D18 缺项扩列允许。本波不另问监管人。
