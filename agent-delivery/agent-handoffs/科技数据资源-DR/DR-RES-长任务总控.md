# 长任务总控 · 科技数据资源四视窗后台接口

| 字段 | 内容 |
|---|---|
| 授权人 | `human:淮政玮` |
| 日期 | 2026-11-03 |
| 目标 | 展示系统四页在 `USE_MOCK=false` 时能读到四个 Dataset，数从久新或 `gapfill_dr_*` 表来，接口不内嵌 mock |
| 升级人 | 结构歧义 `human:李伟` |
| 锁 | `lock_hours=24` |
| 授权句 | **后续认领不必再问** |

授权来自 2026-11-03 主会话：「编排相关的任务，自动多个子智能体进行领取并执行」。监管人即授权人。

方案真源：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/方案-科技数据资源-后台接口.md`。  
WBS：`WBS-05-04` 子表 `4.1a2`。不代替 `SYSINT-05-04-L01` 的页面交付。

## 已拍板

- 调用链：页面 `request()` → 网关 `/display/v1/data-ops/{overview|access|theme|application}/dataset` → `gkxlumen-display` → Java 只读。
- 信封：`{ code: 0, msg, data }`，`data` 键名等于 `lumen-ui-science-pc/src/types/dataResources.ts`。
- 库：只写验收库 `demo_gkxlumenx_ads`。表名以 `gapfill_` 开头。不写正式 `gkxlumenx_ads`、ODS、DWD、久新、`gkxlumenx_gapfill`。
- 久新实体存量只进 `entityStock`。`SHOW COLUMNS` 只进 `columnCatalog`。不写入「资源总量」和 `tableSchemas`。
- 分支：各仓 `origin/dev`。禁止 force push。
- 强度：A0 与契约 `ponytail off`。DDL、灌数、Java、前端接线 `ponytail full`。
- 同仓：`lumen-svc-platform` 同时只派一张编码单。编排仓允许 A0 与契约并行，两叶不得改同一文件。
- 前端仓 `lumen-ui-science-pc`：接线改完停在本地，不自动 commit、不 push。
- Java 叶到达 `integration` 即可解锁下一叶，不等淮政玮签收。Agent 不得把任务标 `done`。

## 叶表

| 顺序 | 任务 | 仓 | 依赖门 | 谁做 |
|---|---|---|---|---|
| 1 | `DR-RES-A0-L01` | `gkx-orchestration` | `SYSINT-05-04-01-L01` 已 done | data-agent |
| 1 | `BE-DR-CONTRACT-01` | `gkx-orchestration` | 无。与 A0 并行 | api-agent |
| 2 | `DR-RES-MOCK-DDL-L01` | `gkx-orchestration` | A0 handoff 已落盘，且状态 ≥ `ready_to_sign` | data-agent |
| 3 | `DR-RES-MOCK-LOAD-L01` | `gkx-orchestration` | DDL handoff 已落盘，且状态 ≥ `ready_to_sign` | data-agent |
| 4 | `DR-RES-C1-L01` | `lumen-svc-platform` | 契约 ≥ `ready_to_sign`，灌数 ≥ `ready_to_sign` | api-agent |
| 5 | `DR-RES-C2-L01` | `lumen-svc-platform` | C1 ≥ `integration` | api-agent |
| 6 | `DR-RES-C3-L01` | `lumen-svc-platform` | C2 ≥ `integration` | api-agent |
| 7 | `DR-RES-C4-L01` | `lumen-svc-platform` | C3 ≥ `integration` | api-agent |
| 8 | `DR-RES-D1-L01` | `lumen-ui-science-pc` | C1–C4 均 ≥ `integration` | frontend-agent |

## 废作

- 不实现 `/display/v1/data-ops/sources`、`/themes`、`/usage` 等资源路径。
- 不新建 `DR-RES-CONTRACT-L01`。
- 不把 mock JSON 写进接口代码。
