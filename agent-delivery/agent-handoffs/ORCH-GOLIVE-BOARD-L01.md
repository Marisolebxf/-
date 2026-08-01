# ORCH-GOLIVE-BOARD-L01 — 「上线前必办」清单真源收敛 + 飞书第三张投影表

- **任务**：ORCH-GOLIVE-BOARD-L01（E-PLATFORM-ORCH / crosscut / P1）
- **执行**：agent:coordinator-agent · **监管**：human:淮政玮
- **日期**：2026-08-01
- **背景**：人类关注点全项目盘点（本会话）发现：散落各 handoff / baseline 的「上线前必须…」
  没有集中真源，属于真正的跟踪空白（区别于已投影的任务/指标/决策三板）。

## 1. 范围与实现

| 产物 | 说明 |
|------|------|
| `agent-delivery/golive-checklist.yaml` | **集中真源**：GL-01~GL-12 共 12 条，字段 = id/title/category(签核·口径闭合·数据·联调切换·核验走查)/gate(上线前·Wave1 前·联调前)/owner/depends/source/status/note |
| `agent-delivery/feishu-golive-board.yaml` | 投影配置：列字典 + status_map + 4 个视图建议；table_id 已回填 `tblnwK1V9aDlyJbb` |
| `scripts/sync-feishu-golive-board.mjs` | 出站同步：解析 YAML items → 自动建表/建列 → 按「事项ID」upsert；无凭据软失败 |
| cron 挂接 | `feishu-bitable-cron-sync.mjs#projectionBoards` 追加第三脚本（非致命）；15min tick 自动刷新 |
| CI | `.gitlab-ci.yml` 路径过滤 + smoke `node --check` 追加脚本与配置 |

**与决策清单的分工**：Q 项 = 甲方要拍板的**口径**；GL 项 = 上线放行前要**完成的动作**
（签核 2 / 口径闭合推动 3 / 数据 2 / 联调切换 2 / 核验走查 3），GL 的 depends 列引用 Q 集合不重复登记内容。

## 2. 首批 12 条来源摘要

GL-01 D10 补签（architecture-baseline）· GL-02 D9 v1.3 补会签 · GL-03 QPOL 口径升🟢（QA-POLICY）·
GL-04 政策执行数据采购（DEF-DATA-01）· GL-05 权限 Q020~030 升🟢（ARCH-权限评审）·
GL-06 企业 Q010~019 升🟢（QA-ENT-lineage §八）· GL-07 CHAIN gateway 切真实地址（FE-CHAIN-api-wiring）·
GL-08 ent_sz_status 落地（E-35 功能设计）· GL-09 久新 CMS 联调（Q050）·
GL-10 Wave1 四段链路核验+性能/视觉基线（QA-ENT-lineage §八 4/5）· GL-11 ⚠️/🧪 角标移除走查 ·
GL-12 D2 结构判定 初判→已核验（readiness-matrix 诚实性约束）

## 3. 验收证据

- 真跑：建表 `tblnwK1V9aDlyJbb` + 12 条新建；复跑 `新建 0 / 更新 12` 幂等 ✅
- `node --check` 全过；cron dry-run 因本地未提交改动在 git pull 步退出（预期，提交后自愈）
- 维护规约：任何 agent 在 handoff 写「上线前必须…」时**同步登记本表**（已写入 yaml 头注释）

## 4. 待办（监管人）

- 飞书 UI 手动配 4 个视图（`feishu-golive-board.yaml#view_hints`）：状态看板 / 门槛分组 / 口径闭合筛选
- GL 状态变更走 yaml 提交（飞书只读投影）

## 5. 架构合规自检

设计/编排类产出（cicd: skip_design_only）；不触碰调用链/图谱/算法边界；
commit 带 `[agent:coordinator-agent]`；push origin/main（编排主仓约定）。
