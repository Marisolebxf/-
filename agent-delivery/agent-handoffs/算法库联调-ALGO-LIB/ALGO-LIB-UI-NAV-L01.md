# Handoff：ALGO-LIB-UI-NAV-L01 — 算法库联调台左右菜单改造

- **任务 ID**：ALGO-LIB-UI-NAV-L01
- **执行 Agent**：agent:frontend-agent
- **监管人**：human:淮政玮
- **仓**：`${GKX_ROOT}/repos/demo-ui-system-test`（push `origin/dev`）
- **关联仓**：`demo-algo-science`（产业链 A2–A9 API）、`demo-svc-platform`（Java 透传）
- **状态**：待 review（registry MCP 不可用，需 coordinator 手动更新）
- **完成时间**：2026-08-04

---

## 1. 范围与实现

| 派单包要求 | 实现 | 状态 |
|-----------|------|------|
| layout 顶栏 + 左侧菜单 + 右侧 router-view | `layout/index.vue` + `LayoutMenuNodes.vue` + `menuConfig.ts` | ✅ |
| 一级菜单顺序 §2.2 | 链路追踪Demo → 三库 → 产业服务/综合 → 展示系统分组 | ✅ |
| 产业服务/产业综合分析 | 由灰显改为可展开子菜单 + 占位子页 | ✅ |
| 顶栏标题 GKX 系统和算法 | `VITE_GLOBAL_TITLE` / index.html / layout | ✅ |
| 首页移除大按钮堆入口 | `home/index.vue` 仅联调 Demo | ✅ |
| `/entan` Tab→嵌套子路由 | 13 子路由；灌数据仅基础指标 | ✅ |
| 产业链/政策 Tab→嵌套子路由 | 子路由 + 左侧子菜单；内容区 router-view | ✅ |
| 创新监测 | 展示系统分组下三级子菜单 | ✅ |
| 基础指标对齐招标 §4.1 | `bidBasicIndicators.ts` + 各库 BasicIndicators 查缺补漏 | ✅ |

---

## 2. 一级菜单（as-built）

1. 链路追踪Demo `/home`
2. 产业链分析算法库 `/chain`（8 子页）
3. 企业分析算法库 `/entan`（13 子页）
4. 政策分析算法库 `/policy`（8 子页）
5. 产业服务算法库 `/industry-service`（9 子页占位）
6. 产业综合分析算法库 `/industry-comp`（4 子页；基础指标=上游七维依赖表）
7. 展示系统 → 创新监测（7 子页）、科技新闻四要素复核

---

## 3. 基础指标招标对齐（§4.1）

| 维度 | 招标项 | UI 覆盖 |
|------|--------|---------|
| 产业链 | A1–A9 | 折叠面板 + API（A2–A9 后端已补） |
| 企业 | A1–A5 | 基础指标页含 A4 资讯统计 |
| 政策 | A1–A5 | 完整图表 + 合规横幅 |
| 服务机构 | A1–A6 | 六项折叠占位 |
| 产业综合 | 无独立子模型 | 七维上游依赖表 + 说明 |

真源：`src/views/shared/bidBasicIndicators.ts`

---

## 4. 偏离说明

1. **技术链/人才/科研机构**：招标七类基础指标中的三项未纳入联调台一级菜单（派单包范围外）；已在 `bidBasicIndicators.ts` 标注 `planned`。
2. **registry / MCP**：本机未加载 task-registry MCP，状态与 cost 四字段需 coordinator 补录。
3. **构建**：本机 shell 无 node/pnpm，未本地 `pnpm build`；依赖 CI。

---

## 5. 产物清单（主要）

- `src/layout/` — 多级侧栏
- `src/router/index.ts` — 全模块嵌套子路由
- `src/views/{chain,entan,policy,industry-service,industry-comp,innov}/` — 子菜单配置与子页
- `src/views/shared/bidBasicIndicators.ts` — 招标基础指标清单
- `demo-algo-science/api/main.py` — chain A2–A9 REST
- `demo-svc-platform/gkx-innov/.../chain/*` — Java 透传

---

## 6. 架构合规自检

| 铁律 | 结果 |
|------|------|
| D1 算法只在 Python | ✅ 前端/Java 仅透传 |
| D2 调用链 前端→Java→Python | ✅ `/innov/v1/industry/**` |
| D8 Design token | ✅ gkx-design-tokens 主色 #165DFF |
| commit `[agent:frontend-agent]` | ✅ |

---

## 7. cost（待回填 registry）

| 字段 | 值 |
|------|-----|
| actual_tokens | （待估） |
| model_used | composer |
| actual_cost | （待估） |
| cost_warn | false |
