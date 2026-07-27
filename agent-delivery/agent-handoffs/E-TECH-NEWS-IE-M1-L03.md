# Frontend handoff：E-TECH-NEWS-IE-M1-L03

- 时间：2026-07-27
- 仓库：`lumen-ui-science-pc`
- 分支：`feat/E-TECH-NEWS-IE-M1-L03`（基于 `origin/dev` worktree）
- 监管人：`human:孙英哲`
- 执行：`agent:frontend-agent`
- PR / push：待监管人确认后推 `origin/dev`（或合入）
- CI：本地 `vue-tsc --build` ✅、`vite build` ✅（未触发远程 Pipeline）
- 路由：侧栏「科技服务全景」→「科技新闻四要素复核」→ `/service/tech-news-review`

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

## 开放项

1. 网关是否已登记 `/innov/v1/tech-news/**`（L02 handoff 开放项）——未通时页面会 upstream 报错
2. 真 Spring 联调与截图待补
3. `MetricSpecCard` 完整 8 件套元数据台账尚未进正式指标库（当前为页面内联 Wave0 卡）
4. orchestration `task-registry` L03 条目待随 handoff 推远程

## 偏离说明

- Design.md 文本以 Arco **React** 为例；本仓为 Vue 3 + Arco Vue，按仓内既有 innov 页范式实现（不引入 React）。
