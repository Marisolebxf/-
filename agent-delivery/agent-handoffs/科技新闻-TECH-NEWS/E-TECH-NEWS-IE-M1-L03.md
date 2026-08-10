# Frontend handoff：E-TECH-NEWS-IE-M1-L03

- 时间：2026-07-27
- 仓库：`lumen-ui-science-pc`
- 分支：`feat/E-TECH-NEWS-IE-M1-L03`（基于 `origin/dev` worktree）
- 监管人：`human:孙英哲`
- 执行：`agent:frontend-agent`
- PR / push：已合入 `origin/dev`（merge `63478c4`；功能分支 tip `321130b`）
- CI：本地 `vue-tsc --build` 通过、`vite build` 通过；合入后等 Pipeline
- 路由：侧栏「科技服务全景」→「科技新闻四要素复核」→ `/service/tech-news-review`
- 关单：监管人指示 Phase C 收尾（`human:孙英哲`）；内网网关 UI 截图为已知残留

## 范围与实现

对照 `formal-migration-plan.md` Phase C + `java-integration.md`：

| 项 | 说明 |
|----|------|
| 页面 | `src/views/tech-news/index.vue`（Arco Vue，对齐 Design 主色 / 14px / 控件高） |
| API | `src/api/tech-news/index.ts` → **仅** `/innov/v1/tech-news/**`（经 `/api` 网关），禁止 Python `/internal/*` |
| 展示 | 公司名称 / 完成时间 / 完成事项 / 作用与影响 + 证据 Collapse + flags Tag |
| D9 | `MockBadge`（mode=mock）；`MetricSpecHint`（metric_id=`TNIE.event_count`，⚠️ 待甲方确认） |
| 可观测 | 复用 `request.ts` + `observability.ts`（页面显式引用 Tempo 工具） |

## 产物清单

- `src/types/tech-news.ts`
- `src/api/tech-news/index.ts`
- `src/views/tech-news/index.vue`
- `src/components/lineage/MockBadge.vue`
- `src/components/lineage/MetricSpecHint.vue`
- `src/router/menu.ts`（菜单 + resolveNavComponent）

## 验收证据

- `vue-tsc --build` exit 0
- `vite build` exit 0（约 15s）
- 截图：待监管人本地 `pnpm dev` 打开 `/service/tech-news-review` 后补（依赖网关 + innov Java + Python `:8000`）

## Design.md §14 / UX §19 对照（摘要）

| 检查 | 结果 |
|------|------|
| Arco 新页（Vue 仓用 `@arco-design/web-vue`） | ✅ |
| 主色 `#165DFF` / 页面白卡片 + 外层壳 `#D8E7FC` | ✅（沿用 layout token） |
| 禁止直连 Python | ✅ |
| 状态：loading / empty / error | ✅（spin / empty / alert + request Message） |
| 键盘：原生表单控件 + Collapse | ✅ 基本可达；未做完整 §3.4 自动化用例 |
| MockBadge | ✅ Wave0 |

## 架构合规自检

1. 算法只在 Python ✅（前端不写抽取）
2. 调用链 前端 → Java REST → Python ✅（URL 设计）
3. 图谱 Nebula N/A
4. 可观测性 ✅（现有 request + observability）
5. CI/CD：本地绿；远程待 push
6. demo2 merge 铁律 N/A（本任务正式仓）
7. 共享聚合 N/A
8. 数据策略 Wave0 Mock ✅
9. Design/D8 ✅（Arco Vue 为本仓权威栈）
10. D9 血缘 ✅（MockBadge + ⓘ）
11. D10 交互：部分对照，完整走查待 UE

## 开放项（已逐条关闭）

| # | 原开放项 | 结论 | 证据 |
|---|----------|------|------|
| 1 | 网关登记 `/innov/v1/tech-news/**` | **已覆盖**：Helm `Path=/innov/**` + StripPrefix=1；已补 as-built 注释 | `evidence/E-TECH-NEWS-IE-M1-L03/01-gateway-route.md`；gateway-dev.yml（lumen/demo） |
| 2 | 真 Spring 联调与截图 | **部分完成**：Python mock + Java HttpClient 契约烟测通过；本机网关/Spring 进程不可达，以 JSON 证据替代截图 | `evidence/.../02-smoke.md` + `02-smoke-evidence.json` |
| 3 | MetricSpec 8 件套进指标库 | **已完成**：`M_TNIE_EVENT_COUNT` 种子 + 说明卡；UI metric-id 对齐 | `metrics/cfg_metric-TNIE-seed.yaml`；`evidence/.../metric-M_TNIE_EVENT_COUNT.md` |
| 4 | registry L03 推远程 | **已完成**：`origin/dev` `18f7ba1` | GitLab `gkx-orchestration` |

残留（非阻塞）：dev 网关恢复后补 UI 登录截图；完整 Spring Boot 进程级联调。

## 偏离说明

- Design.md 文本以 Arco **React** 为例；本仓为 Vue 3 + Arco Vue，按仓内既有 innov 页范式实现（不引入 React）。
