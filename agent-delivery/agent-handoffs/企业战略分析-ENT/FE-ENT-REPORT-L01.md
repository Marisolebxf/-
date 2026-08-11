# FE-ENT-REPORT-L01 · 企业报告 HTML/PDF + 付费导出闸门 + 菜单权限

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 对照 demo `d23700b` / `5f3dced` / `e0049aa`；监管人确认完工后写本 handoff |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 Design / D10 / 付费闸门 / 菜单权限 / handoff；报告壳复用 demo 契约语义 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 headroom；task-registry 走 MCP |

---

## 1. 范围与实现（对照 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| P0 共享壳 SystemReportReader + HTML/同源 PDF 入口分离 | ✅ | `src/components/report/*`、`system-report-reader.css` |
| P0 评估/风险/招引「查看 HTML 报告」+ `view=report` | ✅ | Eval/Risk/Recruit 结果区与历史 CTA |
| P0 付费闸门 paid + ReportExportButton + Persona | ✅ | `src/perms/*`、`PersonaLevelSwitcher`、`review` store |
| P1 Key / 深圳现状报告 + 任务浮层跳转 | ✅ | Key/SzStatus `demo_state=report`；`SystemTaskFloat` / `analysisTaskRoutes` |
| P2 菜单 permCode + 侧栏裁剪 + guard | ✅ | `menu.ts`、`DefaultLayout`、`guard.ts` |
| precheck 覆盖率面板（关 mock 走接口；开 mock 走注册层+fixture） | ✅ | `EvalQualityPanel` + `mockEntEvalPrecheck` |
| 对比篮回填 precheck 不误触发 / 不双打 | ✅ | `useEvalTask` 字符串 watch + hydrate 同 id 跳过 |
| vue-tsc / 自检绿；ponytail full | ✅ | `reportExport.selfcheck.mjs` ok；本机验收 |

**不做（已遵守）**：不 merge demo 进 lumen；不改 Java/Python；完成弹层不直接下 PDF。

---

## 2. 修改内容

- **报告壳**：契约、Reader、同源 PDF、企业域报告模型、导航
- **付费/权限**：`paid`、导出闸门、菜单 `permCode`、Persona 双角标
- **三叶 + Key/SzStatus**：结果态 HTML 报告 CTA 与 `view=report` / `demo_state=report`
- **评估预检**：`per_enterprise` 类型与质量面板统一读 precheck；mock 由 fixture 填契约
- **对比篮**：打开选择器不打 precheck；确认改对象后单次预检

---

## 3. 测试结果

| 项 | 结果 |
|----|------|
| `node src/components/report/reportExport.selfcheck.mjs` | ✅ ok |
| 报告 CTA / 付费锁态 / 菜单裁剪 | ✅ 本机 `npm run dev`（监管人孔东 DOM 点选） |
| mock 关：质量面板读 precheck.per_enterprise | ✅ |
| 打开对比篮不预检；确认后单次 precheck | ✅ |
| 调用链无 Python `/internal/*` | ✅ |

---

## 4. 遗留风险

| 项 | 说明 |
|----|------|
| 真 PDF 服务端排版 | 当前同源打印/导出；正式版式待后端联调 |
| 菜单无权限强开 URL | guard 拦截；升级占位文案可再打磨 |
| 历史招引列表 | 招引无独立历史表；结果区 CTA 已覆盖 |

---

## 5. CI/CD（必填）

- 分支：`dev`
- commit：`3d89955`（`repos/lumen-ui-topic`）
- pipeline URL / ID：push `origin/dev` 后由 GitLab CI 触发（待 CI 面板确认）
- 部署 namespace / 镜像 tag：K8s topic-ui dev（CI 惯例）
- K8s rollout：待 CI
- dev 测试 URL / 命令：本机 `npm run dev`；`reportExport.selfcheck.mjs` 绿

---

## 6. 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 topic-ui 既有前端埋点
- 本单未新增独立 trace 字段；报告打开走现有页面路由

---

## 7. 涉及文件

- `src/components/report/**`
- `src/perms/**`
- `src/assets/layout/system-report-reader.css`
- `src/components/enterprise/evaluation|risk|recruit/**`
- `src/views/enterprise/Enterprise{Evaluation,Risk,KeyAnalysis,SzStatus}.vue`
- `src/composables/useEvalTask.ts`、`analysisTaskRoutes.ts`
- `src/mock/enterprise/evaluation.ts`、`src/api/enterprise/types/evaluation.ts`
- `src/router/menu.ts`、`guard.ts`、`layouts/DefaultLayout.vue`
- `src/stores/review.ts`、`src/components/review/PersonaLevelSwitcher.vue`

---

## 8. 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未越层 |
| 前端 → Java REST | ✅ |
| Nebula 禁 Neo4j | ✅ N/A |
| 可观测 | ✅ 沿用壳 |
| CI/CD push → Pipeline | ✅ push `origin/dev` |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / ADS | ✅ N/A 本单 UI |
| D8 Design / Arco Vue | ✅ |
| D9 指标血缘 | ✅ 无新增裸 KPI；评审 MockBadge 保留 |
| D10 交互 | ✅ 报告阅读/导出分入口 |

---

## 9. Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 380000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 3.8 |
| cost_warn | green |
