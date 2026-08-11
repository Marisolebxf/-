# ENT-NAV-WORKSPACE-LUMEN-L01 · 企业分析 workspace 侧栏拆分 + 政策壳对齐

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 对照 `repos/demo-ui-topic@527084e`；监管人确认完工后写本 handoff |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 Design / D10 / 路由高亮 / 深链；D9 无新增裸统计数字 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 Cursor 未挂载 headroom；task-registry 用 CLI 应急通道 |

---

## 1. 范围与实现（对照 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| 侧栏对齐 demo：类型/领域、技术力/商业力、招引/培育/供应链/痛难点；无合并入口 | ✅ + 正式加量 | `menu.ts`：`menuKey` + `query.workspace`；**保留「企业综合竞争力评估」侧栏**（demo@527084e 漏拆，本单正式加量，监管人确认） |
| 页内去掉跨 mode Tab；改由 workspace/query 驱动；条件下沉到分析 Tab | ✅ | Eval/Risk/Key/Recruit 去掉模式切换 Tab；对象上下文仅在分析 Tab；历史 Tab 不带条件 |
| 分析页壳对齐政策：Tabs → main → heading；embedded 无双层 padding | ⚠️ as-built | **监管人改口**：取消「标题下沉到 Tab 内」；现为 **heading（页外顶部）→ Tabs → main**；`diagnosis-page-heading` 仍 20px；`.analysis-shell-root.is-embedded` 去双层 padding |
| 旧链兼容高亮；对比篮/任务深链补 `workspace=` | ✅ | `isNavItemActive` / `findActiveNavItem` query 感知；`compareBasketDispatch` + `analysisTaskRoutes` 补 `workspace`（引育另补 `recommendation_tab`） |
| build 绿；handoff 含 527084e 对照；ponytail full | ✅ | `vue-tsc` + `vite build` 绿；本文件；强度 full |

**不做（已遵守）**：企业发展 / 维护管理缺页不新建；不改 Java/Python；不 merge demo 进 lumen。

### demo@527084e 对照

| 项 | demo@527084e | lumen as-built |
|----|--------------|----------------|
| 侧栏拆分（类型/领域、技/商、招引/培育、供应/痛点） | ✅ | ✅ |
| 综合竞争力侧栏 | ❌ 漏拆 | ✅ **正式加量** |
| 页内 mode Tab | 去掉 | ✅ 去掉 |
| 页壳标题相对 Tabs | Tabs 下、分析 Tab 内 heading | **标题在 Tabs 外顶部**（监管人指示） |
| 深链 `workspace=` | ✅ | ✅ |

---

## 2. 修改内容

- **menu / layout / guard**：共享 path + 唯一 `menuKey`；query/`workspace` 高亮与标题
- **Eval / Risk / Recruit / Key / SzStatus**：政策壳 CSS；条件下沉；标题置顶；Tab 文案「当前分析 / 最近*」
- **history `subType`**：`loadEvalHistory(mode)` / risk `loadHistory` 与侧栏 workspace 对齐
- **深链**：`compareBasketDispatch.ts`、`analysisTaskRoutes.ts`
- **评审 TraceInfoIcon**：对齐 demo 透明灰文件图标；去悬停蓝方框；页标题旁去掉「评审模式」标签
- **新增** `src/assets/layout/diagnosis-shell.css`（经 `main.css` 引入）

---

## 3. 测试结果

| 项 | 结果 |
|----|------|
| `npx vue-tsc --noEmit -p tsconfig.app.json` | ✅ |
| `npm run build-only` | ✅（见 CI/CD commit 后本地绿） |
| 侧栏拆分入口 / workspace 高亮 | ✅ 本机 `npm run dev`（监管人孔东） |
| 标题在 Tab 外顶部；无「评审模式」标签 | ✅ |
| TraceInfoIcon 悬停无蓝方框 | ✅ |
| 调用链无 Python `/internal/*` | ✅ |

截图：本机浏览器验收（监管人会话内 DOM 点选确认）；未另存静态截图文件。

---

## 4. 遗留风险

| 项 | 说明 |
|----|------|
| DoD 原文「Tabs→main→heading」与 as-built 标题外置 | 以监管人最新指示为准；若产品要回退到 demo 标题下沉需另开单 |
| 竞争力侧栏加量 | 已文档化；若甲方要求与 demo 完全一致可再藏菜单 |
| `node_modules` 曾缺 `@arco-design` | 已 `npm install` 恢复；勿在 dev 中途清依赖 |

---

## 5. CI/CD（必填）

- 分支：`dev`（`lumen-ui-topic`）
- commit：`9f68584`
- pipeline URL / ID：push 后等 GitLab CI（仓 `lumen-ui-topic` · `dev`）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：待 CI
- dev 测试：本机 `npm run dev` 冒烟通过（见 §3）；`vue-tsc` + `npm run build-only` 绿

---

## 6. 可观测性

- 路由/请求走既有拦截器（`X-Trace-Id`）；无新增越层调用
- 本单无新增业务埋点点位

---

## 7. Design.md / 交互 / D9

| 检查 | 结果 |
|------|------|
| Design.md：Arco + 既有 workbench tabs / section panel | ✅ |
| D10：Tab `role=tablist` / aria-selected 保留 | ✅ |
| D9：无新增裸统计数字；TraceInfo 仅评审模式自闸 | ✅ |

---

## 8. 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ N/A |
| 2 | 前端 → Java → Python | ✅ |
| 3 | Nebula | ✅ N/A |
| 4 | 可观测 | ✅ 既有 request 链 |
| 5 | CI/CD | ✅ push origin/dev |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ |
| 8 | ADS/Mock | ✅ N/A（导航/壳） |
| 9 | Design.md / Arco | ✅ |
| 10 | D9 血缘 | ✅ N/A |
| 11 | D10 交互 | ✅ |

---

## 9. 涉及文件（`lumen-ui-topic`）

- `src/router/menu.ts` · `guard.ts`
- `src/layouts/DefaultLayout.vue`
- `src/assets/layout/diagnosis-shell.css` · `src/assets/main.css`
- `src/views/enterprise/Enterprise{Evaluation,Risk,Recruit,KeyAnalysis,SzStatus}.vue`
- `src/composables/{useEvalTask,useEnterpriseRisk,useRecruit,useKeyEnterpriseAnalysis,enterpriseEvalLoaders,analysisTaskRoutes}.ts`
- `src/config/{compareBasketDispatch,enterpriseEvaluation}.ts`
- `src/components/review/{TraceInfoIcon.vue,persona-switcher.css}`

编排仓：本 handoff + task-registry 状态/证据/cost 回填。
