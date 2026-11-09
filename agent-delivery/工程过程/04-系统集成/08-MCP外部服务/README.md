# MCP 外部服务 · 主文件

## 当前

| 项 | 内容 |
|---|---|
| 阶段 | 建档 |
| 项号 | 第 08 项（2026-11-09 增补，规约 §2 七项之外） |
| 对接方 | zmate 智能体客户端（对标 WorkBuddy）；供应商确认范围见步骤 1 |
| 智树角色 | 实现 + 对接：提供展示、专题系统的对外 MCP，配到 zmate 的 Skill 上 |
| 方案任务 ID | 未建 |
| 建档日 | 2026-11-09 |
| 最近更新 | 2026-11-09 |

**当前结论**：gkx-7chain 第一阶段 13 个工具已对 demo 网关调通（`CROSS-MCP-7CHAIN-L02` integration）。zmate 四批建设的第 1、2 步定在 2026-11-10，第一批验收 2026-12-05。两张评测方案单已建，暂不执行。近期紧急：11-11 技术标准（李瑞），11-12 评测标准草稿（淮政玮）、固态电池第一批范围与报告目录（闫德金），11-13 数据需求同步刘斌，11-20 一二三阶标注。明细见 [WBS](./WBS.md) 第〇节。

---

## 一、范围

把展示系统、专题系统的分析能力做成对外 MCP，由 zmate 的 Skill 调用，并按统一方案评测。

- 在本夹：gkx-7chain（专题五域查询与分析）、展示系统对外 MCP、zmate Skill 配置、Skill+MCP 评测
- 不在本夹：团队内部工具类 MCP（task-registry、metric-registry、ssh-executor、gitlab-ci-var、飞书 IM、headroom），它们只服务研发过程，不对外

## 二、做什么、不做什么

- 调用链：zmate / Skill → MCP → Java 网关 → Python `/internal/*`。MCP 不直连算法仓、Nebula，不调 `demo-*` 服务（正式对外前完成 M3 切 lumen 网关）
- MCP 只返回结构化数据，不渲染图。统计数字透传 `metric_id`，mock 状态原样返回，不冒充真数
- token 只放使用人本机环境，不进 git
- zmate 客户端本身不由智树开发

## 三、材料入口

| 材料 | 位置 |
|---|---|
| 盘点与总体方案 | [designs/7链分析四域功能点MCP工具化-盘点与方案.md](../../../designs/7链分析四域功能点MCP工具化-盘点与方案.md) |
| 使用与 WorkBuddy 接入说明 | [7chain-mcp-usage-guide.md](../../../7chain-mcp-usage-guide.md) |
| M1 实装 handoff | [CROSS-MCP-7CHAIN-L02.md](../../../agent-handoffs/CROSS-MCP-7CHAIN-L02.md) |
| 深圳活力示范 handoff | [CROSS-MCP-7CHAIN-L03.md](../../../agent-handoffs/CROSS-MCP-7CHAIN-L03.md) |
| 代码 | `scripts/7chain-mcp-server.mjs`、`scripts/7chain-mcp-selfcheck.mjs`；注册在 `.cursor/mcp.json` 的 `gkx-7chain` |
| zmate / MCP 产品要求（对端材料） | [对接文档/对端/](./对接文档/对端/) |
| 我方发出的材料 | [对接文档/我方/](./对接文档/我方/) |
| WBS | [WBS.md](./WBS.md) |
