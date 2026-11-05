# SVC-VIZ-DEMAND-MATCH-FIX-20261105 · 产业服务需求与匹配修复记录

- 日期：2026-11-05。
- 来源：用户直接要求修复产业服务可视化的需求分布、供需匹配空态，并要求按主仓 Cursor 规范提交代码。
- 执行：agent:codex；用户身份未确认，不代填监管人姓名。
- 标识：本文为本会话交付追踪标识，不宣称已在 task-registry 注册；本会话未挂载 task-registry MCP，不直接读写注册表。
- ponytail: full；复用现有 Arco/ECharts 及 Java 聚合层，无新增依赖。

## 范围与实现

对照 `bid-reference/科技信息展示系统和科技专题服务系统.md` 服务需求与匹配可视化：需求分布图按服务类型展示，支持行业、企业规模筛选；供需匹配用热力图展示。

- 前端真实模式恢复行业、规模筛选，需求分布按需求服务类型汇总。
- 需求分布和供需匹配使用面向客户的空态，不直接展示后端 reason。
- Java 两块的异常仍记日志，返回业务空态。
- 保持前端 → Java REST → Python `/internal/*` 调用链；未改路由、依赖、可观测配置、数据库或指标就绪度。

## 提交与文件

- `lumen-ui-topic`：`f517ccd`，已推送 `origin/dev`。
  - `src/views/viz/service/ServiceVizPage.vue`
  - `src/views/viz/service/serviceViz.selfcheck.mjs`
- `lumen-svc-platform`：`3e75227`，`git push origin dev` 返回 Everything up-to-date，远端已包含。
  - `gkxlumen-topic-svc/gkxlumen-topic-svc-biz/src/main/java/com/topcomm/gkxlumen/topic/svc/service/impl/ServiceVizServiceImpl.java`
  - 对应 `ServiceVizServiceImplTest.java`
- 上述历史提交带 `[agent:codex]`，未带本文追踪标识；已发布提交不改写，本记录补充映射。

## 验证

- 前端 `serviceViz.selfcheck.mjs`：通过。
- 前端 `npm run type-check`：通过。
- 前端 `npm run build-only`：通过。
- 两仓 `git diff --check`：通过。
- Java 已增加异常空态测试；本机无 Maven 和 Maven Wrapper，测试未执行，不宣称通过。

## 排查证据与遗留问题

- 前端请求 `/svc/topic/v1/service-portal/viz`；Java 映射 Python `/internal/gkx-svc/portal/demand`、`/match`，代码中的请求路径一致。
- Python 路由已存在，查询 `gkxlumenx_gapfill.svc_demand_match`；工作区未发现该表的 DDL 或装数脚本。这只能证明仓库缺少交付资产，不能证明线上数据库一定缺表。
- 截图的两句“数据服务暂不可用”对应 Java catch 分支，说明调用或响应处理发生异常；确切异常仍须从线上日志确认。
- Python demand/match 当前只处理 data_year，未应用顶部 industry 参数；不能据此前端修复宣称产业筛选端到端已闭环。
- 仍需核对线上 Python 版本、表结构与数据、查询权限及日志；未写入演示数据，未执行线上数据修复。

## CI/CD 与验收状态

- 两个业务仓的 `origin/dev` 代码提交已确认。
- 使用 GitLab API 按提交 SHA 查询流水线，两个项目均返回 HTTP 404，未取得 Pipeline ID/URL 或成功证据。
- K8s rollout、线上页面与接口冒烟：未验证，不标记完成。
- 当前交付范围为代码修复与提交；线上数据出数及 CI/部署闭环仍待验证。

## 规范与偏离

已核对主仓 `.cursor/rules/00-path-resolution.mdc`、`00-team-constitution.mdc`、`multi-session-protection.mdc`、`frontend.mdc`、`api.mdc`、`ponytail.mdc`。

代码保持现有 Vue/Arco 组件、蓝色图表和前端只调 Java 的架构。未更改第三方工作产物，未使用 force push。未新增独立指标或修改指标定义，不伪造 D9 就绪状态。未完成截图走查、D9 全量扫描或线上验收，故不宣称全部工程 DoD 已通过。

成本：本会话没有可核验的 token/费用计量，未虚填 actual_tokens / actual_cost；模型为 gpt-6.1-sol（本轮提交与规范核对）。

## 用户走查修正：筛选控件按需展示

用户指出无数据时新增两个空下拉框增加页面负担。重新核对需规：需求分布明确支持按行业、规模筛选，但未要求始终展示控件。

本次只调整显示条件：行业、规模分别在有效选项数量大于 1 时展示；两个维度都没有可筛选项时不渲染工具栏。无数据时保留需求分布、供需匹配两块业务空态，避免用户展开空下拉框。未增加接口、字段、依赖或新业务流程。

本次复验：前端自检、type-check、build-only、diff --check 均通过。
