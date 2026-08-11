# ENT-MOD-RISK-SUPPLY-GRAPH-SYNC-LUMEN · lumen 同步供应链图谱重定中心/双视图 + 对比篮

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东`（会话执行 `agent:frontend-agent`） |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | demo-ui-topic@a29fda4 供应链 + 对比篮系统浮层设计态同步至 lumen-ui-topic |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致；未用 YAGNI 跳过 D8/D9/D10/可观测；图谱复用 demo 交互与 token，未另起一套 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 Cursor 未挂载 headroom；task-registry 用 `scripts/task-mcp-cli.mjs` 应急通道 |

---

## 1. 范围与实现（对照 DoD）

| DoD | 状态 | 证据 |
|-----|------|------|
| 重定中心下钻（面包屑回退，≤3 级）；点击供应商/客户/合作伙伴切 ego | ✅ | `riskInsightDemo.ts`：`SUPPLY_EGO_BY_CENTER` / `getActiveSupplyEgo` / `canDrillSupplyNode` / `buildSupplyDrillBreadcrumb`；`SupplyChainInsightPanel.vue` |
| G6 画布 + 边中文标注 + SharedMapChrome 缩放复位全屏 | ✅ | `@antv/g6`；`SupplyChainGraph.vue`；`SharedMapChrome.vue`；边 label 走 `getRelationTypeLabel` |
| 「图谱 \| 结构列表」双视图；列表分组并与选中态联动 | ✅ | `SupplyChainInsightPanel` Radio；`SupplyStructureList.vue` + `supply-chain-graph.css` |
| 文案：「企业供应链关系分析」「企业发展痛点分析」 | ✅ | `enterpriseRisk.ts` + `compareBasketDispatch.ts` |
| 关键节点/断链侧栏、只看关键/风险、D9 ⓘ/Mock、四态/历史/画像不回退 | ✅ | 侧栏与 `SupplyChainNodeList` / `RiskReportPanel` 保留；评审挂点未删 |
| 对照 demo a29fda4；type-check；handoff + lumen commit SHA | ✅ | `vue-tsc` 通过；本文件；`lumen-ui-topic@6601fca` |
| ponytail full；不直连 Python；不伪造就绪度改绿 | ✅ | 仅 lumen 前端；fixtures + MockBadge |

### 追加验收（note 同效）

| 项 | 状态 | 说明 |
|----|------|------|
| 对比篮 RISK 标题 + max=2 | ✅ | 文案对齐；供应链分发 `maxEnterpriseCount=2` 拦截保留 |
| 分发→风险 tab + 返回篮现场 | ✅ | `useCompareBasketDispatchContext` / `open_compare_basket=1` 恢复 |
| 系统浮层 / 对象 Tab / picker 缺口清单 | ✅ 见下表 | |

**系统浮层相对 demo 缺口清单**

| 能力 | 状态 |
|------|------|
| 可拖动系统对比篮浮层（DefaultLayout 挂载） | ✅ `SystemCompareBasketLayer.vue` |
| 对象类型 Tab：企业 / 产业 / 服务机构 / 区域 | ✅ 区域标「开发中」；产业/服务机构面板已挂 |
| picker 勾选回填（不发起任务） | ✅ `compareBasketPicker.ts` |
| 清空确认 Modal 挂 body + z-index token | ✅ `--sci-z-system-surface` / `--sci-z-modal` |
| 产业/服务机构「发起分析」全量 registry | 🟡 部分 `Message.info` 待接，不阻断企业维主路径 |
| 与任务状态浮层碰撞协调 | 🟡 未做专项碰撞算法；可后续 chore |
| Dropdown「⋯」恢复默认位置 z-index | 🟡 已接线；若仍被遮挡可再抬 popup z-index |

---

## 2. 修改内容

### A. 供应链

- fixture：ego 多中心图谱 + 下钻 helpers
- `SupplyChainGraph.vue`：G6 preset 布局；**mount + ResizeObserver 后再 render**（修复空白画布）
- `SupplyStructureList.vue` + `supply-chain-graph.css`：对齐 demo 结构列表双列卡片
- `SupplyChainInsightPanel.vue`：面包屑 / 双视图 / chrome / 图例
- `SharedMapChrome.vue`：缩放/复位/全屏壳

### B. 对比篮

- `SystemCompareBasketLayer.vue` + `system-compare-basket.css`；`DefaultLayout` 挂载
- `EnterpriseCompareBasketView.vue`：对象 Tab、TraceInfo、清空 Modal、picker
- `IndustryCompareBasketPanel.vue` / `ServiceOrgCompareBasketPanel.vue`
- `compareBasketPicker.ts`；`CompareBasketActionBar` 打开系统浮层
- 菜单页入口改为系统浮层优先（侧栏对比篮页注释保留说明）

### C. 依赖

- `package.json`：新增 `@antv/g6`

---

## 3. 测试结果

| 项 | 结果 |
|----|------|
| `npx vue-tsc --noEmit -p tsconfig.app.json` | ✅（供应链相关零报错） |
| 本机 `npm run dev` 供应链结果 | ✅ 图谱可渲染；结构列表样式对齐（human:孔东 确认后收口） |
| 调用链无 Python `/internal/*` | ✅ |
| 就绪度未前端改绿 | ✅ |

冒烟步骤：

1. 企业风险 → 供应链关系分析 → 见 G6 图谱与图例；工具栏缩放/复位可用。
2. 切换「结构」→ 供应商/客户/合作伙伴双列卡片 + 企业关系段。
3. 节点「以此为中心下钻」→ 面包屑回退，深度 ≤3。
4. 打开系统对比篮浮层 → 企业 Tab 分发供应链（≤2 家）；`open_compare_basket=1` 可回浮层。

---

## 4. 遗留风险

| 项 | 说明 |
|----|------|
| 产业/服务机构分析分发未全量 | 面板可展示；发起分析部分占位 |
| 浮层与全局 Popup 叠层 | Modal 已抬到 1400；个别 Dropdown 若仍被挡需补 `popup-container` |
| #106 真实 payload | 仍 fixtures 演示；与 V2-S2 开放项一致 |
| 本地 `.env.development` Mock 开关 | 未提交（本机联调） |

---

## 5. CI/CD（必填）

- 分支：`dev`（`lumen-ui-topic`）
- commit：`6601fcaf17558d86e99817d66e2c2bee0c7a0cb6`
- pipeline URL / ID：push 后 GitLab CI（`lumen-ui-topic` · `dev`）
- 部署 namespace / 镜像 tag：K8s dev（CI 触发）
- K8s rollout：待 CI
- dev 测试：本机 `npm run dev` 冒烟（见 §3）

编排仓：本 handoff + task-registry 状态/证据回填（本 commit）。

---

## 6. 可观测性

- 风险任务流仍走既有 `analysisTask` / `request.ts`（`X-Trace-Id`）
- 本单无新增越层调用；图谱为前端 fixtures 渲染

---

## 7. Design.md / 交互 / D9

| 检查 | 结果 |
|------|------|
| Design.md：主色/画布/Arco | ✅ 对齐 demo stage/token |
| D10：工具栏按钮 title/aria；结构列表 button 可键盘聚焦 | ✅ |
| D9：既有 ⓘ/MockBadge 评审挂点保留 | ✅ |

---

## 8. 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ N/A（前端 G6 展示） |
| 2 | 前端 → Java → Python | ✅ |
| 3 | Nebula | ✅ N/A |
| 4 | 可观测 | ✅ 既有 request 链 |
| 5 | CI/CD | ✅ push origin/dev |
| 6 | demo2 不 merge lumen | ✅ 仅对照移植 |
| 7 | 共享聚合核心 | ✅ |
| 8 | ADS/Mock | ✅ fixtures + Mock |
| 9 | Design.md / Arco | ✅ |
| 10 | D9 血缘 | ✅ 不伪造改绿 |
| 11 | D10 交互 | ✅ |

---

## 9. 涉及文件（`lumen-ui-topic`）

- `package.json` / `package-lock.json`（`@antv/g6`）
- `src/components/enterprise/risk/SupplyChainGraph.vue`
- `src/components/enterprise/risk/SupplyChainInsightPanel.vue`
- `src/components/enterprise/risk/SupplyChainNodeList.vue`
- `src/components/enterprise/risk/SupplyStructureList.vue`
- `src/components/map/SharedMapChrome.vue`
- `src/assets/enterprise/supply-chain-graph.css`
- `src/fixtures/enterprise/riskInsightDemo.ts` · `index.ts`
- `src/config/enterpriseRisk.ts` · `compareBasketDispatch.ts` · `compareBasketPicker.ts`
- `src/components/system/SystemCompareBasketLayer.vue`
- `src/assets/layout/system-compare-basket.css` · `design-tokens.css` · `main.css`
- `src/views/enterprise/EnterpriseCompareBasketView.vue` · `EnterpriseRisk.vue`
- `src/components/enterprise/compare/*` · `CompareBasketActionBar.vue`
- `src/layouts/DefaultLayout.vue` · `src/router/menu.ts`
- `src/composables/useCompareBasketDispatchContext.ts` 等

编排仓：本 handoff + `task-registry.yaml`（MCP/CLI）。
