# 段 D · 产业链前端（lumen-ui-topic）总派单 · 长任务

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（无人值守，见 [ABCD 总控](./DEMO-CHAIN-ABCD-长任务总控.md)）  
> **执行**：`frontend-agent`  
> **仓**：`${GKX_ROOT}/repos/lumen-ui-topic` · push **`origin/dev`**  
> **栈**：Vue 3 `<script setup>` + TS + **Arco Design Vue** + Pinia + Vite  
> **复刻源**：已评审 `repos/demo-ui-topic/src/app/pages/industry-center/**`（**语义/路由/状态 + 视觉壳 + 卡片布局**；**禁止**抄 React 进 Vue）  
> **强度**：ponytail **full**  
> **薄条**：[`DEMO-CHAIN-FE-D-派单条.md`](./DEMO-CHAIN-FE-D-派单条.md)  
> **视觉补单**：[`LUMEN-CHAIN-FE-SEARCH-SKIN-L01`](./LUMEN-CHAIN-FE-SEARCH-SKIN-L01-派单.md)（Hero/页底）· [`LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01`](./LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01-派单.md)（推荐卡竖排）  
> **复刻验收**：[`templates/fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)（手册 §9.0c）

本仓目前几乎无产业链页（仅对比篮跳转占位）。本段 **2 张长任务** 一次铺齐专题侧，禁止「先做一页再问要不要做八项」。

---

## 0. 铁律

1. **只调 Java REST**。禁止直连 Python / ES / MySQL / Nebula。  
2. **对齐已评审 Demo**：路由 `/industry-center/*`、侧栏文案、smart/industry/advanced、wait_view、全景秒开与改条件 Job。**视觉与本仓企业查询同皮肤**（页底 `#D8E7FC`、SearchHub Hero）。**推荐/结果卡内部布局**对照 Demo class 清单 + `RecommendationSection`（横排：左文右钮）。禁止另起灰白风，禁止叠互斥 layout class。验收：`templates/fe-replica-visual-dod.md` V1–V7。  
3. **复用本仓已有**：`SearchScaffold`（或 **同皮肤** 的 `SearchHub` + `enterprise-search-page` 页根 + `RecommendationSection`）、`compareBasket`、`analysisTask.ts`、`SystemTaskFloat`、`@/review`。不要第二套任务中心、不要第二套检索 Hero CSS。Hero 选择器不得只绑 `.enterprise-search-page` 而把产业查询排除在外。  
4. **D9**：每个统计数字 ⓘ；就绪度只读 catalog/镜像；评审关 DOM 零泄漏。`Design.md` §4 / §14 + D10 走查。  
5. **observability.ts** / `X-Trace-Id`。  
6. OPS「维护管理」只复刻 Demo **壳**（`CHAIN-OPS-PACK-DEMO-L01` 已定义），不在本段做写侧后端。  
7. 旧 `CHAIN-FE-L03`（CP1–CP6）废作施工。  
8. 介绍/历程无 CMS 则空态诚实，禁止用资讯冒充。

---

## 1. 长任务 A · `LUMEN-CHAIN-FE-ENTRY-L01`

**依赖**：`LUMEN-CHAIN-JAVA-FACADE-L01`  
**页**：侧栏「产业链分析」整组 + 查询 + 门户总览 + 对比篮产业/链。

| 路由 | Demo 真源 |
|---|---|
| `/industry-center/search` | `IndustrySearchPage.tsx` + `industrySearchModel.ts` |
| `/industry-center/overview` | `IndustryOverviewPage.tsx` |
| 篮 | `IndustryCompareBasketPanel` 语义；本仓已有 `IndustryCompareBasketPanel.vue` 扩实 |

侧栏条目对齐 Demo `Layout.tsx` 产业链分组（含诊断/区域/深圳菜单项，**本单可先挂路由到占位**，WORKSPACE 单填实；查询与总览必须可点可查）。

权限码：补 `menu:chain:*`（对齐 Demo `perms/matrix.ts`），接入现有 L0–L4 矩阵，不要破坏企业码。

### DoD

- 查询三模式 + 高筛独立页 + 入篮同类型锁 + 进入全景带 `object_type/object_id`。  
- 总览三 Tab（全景/资讯/概况）能从 Java 拉；无数空态。  
- **视觉**：页底 `#D8E7FC`；Hub Hero 同企业查询；**推荐卡横排**（Demo class = `search-content-card industry-search-recommendation-card`，**不要**叠 `industry-search-result-card`）；V1–V7。  
- 只调 Java；CI lint/type/build 绿。  
- 附录 D 扫描摘要进 handoff。  
- handoff `LUMEN-CHAIN-FE-ENTRY-L01.md`。

---

## 2. 长任务 B · `LUMEN-CHAIN-FE-WORKSPACE-L01`

**依赖**：`LUMEN-CHAIN-JAVA-JOB-L01` + `LUMEN-CHAIN-FE-ENTRY-L01`  
**页**：全景 / 诊断三键 / 区域两键 / 深圳两键 / 过程壳 / 显式看结果 / 报告阅读（只读）。

| 路由 | 键 |
|---|---|
| `/industry-center/panorama` | 默认 snapshot 秒开；脏条件 `chain:panorama:graph`；无报告入口 |
| `/industry-center/diagnosis` | cycle · key_link · bottleneck |
| `/industry-center/regional` | index · competitiveness |
| `/industry-center/shenzhen` | comparison · development（无对比结果禁止空跑发展） |
| 过程 | 复用/对齐 Demo `industryAnalysisShell` + 本仓评估过程壳 |

Create 走现有 `analysisTaskCreate`，`analysisType=chain:...`。wait_view 必须。G6/ECharts 按 Demo 能力复刻，token 走 Design/Arco。

B 其余 Job 后到：前端按 `analysis_key` 分发，**不要**为每个键再开 FE 单。

### DoD

- 八项 Bid 入口都在侧栏且能进工作区（维护管理壳可弱）。  
- key_link 主路径：配置→生成→过程→wait_view→结果。  
- 全景：默认无 task 出图；改条件出「开始分析」。  
- D9 数字旁 ⓘ；Q056 市场规模空文案。  
- 关闭评审零泄漏。附录 D 扫描。  
- handoff `LUMEN-CHAIN-FE-WORKSPACE-L01.md`。

---

## 2.5 视觉补单 · `LUMEN-CHAIN-FE-SEARCH-SKIN-L01`

**依赖**：`LUMEN-CHAIN-FE-ENTRY-L01` 联调闸门（`pending_test` 即可，不等 `done`）  
**厚包**：[`LUMEN-CHAIN-FE-SEARCH-SKIN-L01-派单.md`](./LUMEN-CHAIN-FE-SEARCH-SKIN-L01-派单.md)

ENTRY 把 SearchHub 裸放在 `industry-search-page` 上，Hero CSS 只挂在 `.enterprise-search-page`，截图像灰白后台。本单只修皮肤与推荐空态接线，不改三模式语义。

### DoD

- `/industry-center/search` 页底 `var(--sci-bg-page)`（`#D8E7FC`）。  
- Hub 与 `/enterprise/search` 同 Hero。  
- 推荐：catalog 有对象则出卡；无数诚实空。  
- 总览/诊断页根同样铺页底（不重做工作区）。  
- push `origin/dev`；handoff 本 ID。

---

## 2.6 布局补单 · `LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01`

**依赖**：SEARCH-SKIN 联调闸门  
**厚包**：[`LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01-派单.md`](./LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01-派单.md)

SKIN 让推荐卡露出后，人审截图：标题/摘要一字一换行、操作钮漂在空白区。根因：推荐 `article` 同时挂 `industry-search-recommendation-card`（flex）与 `industry-search-result-card`（`grid-template-columns: 24px 1fr auto`）。Demo 推荐卡 **只有** `search-content-card industry-search-recommendation-card`。

### DoD

- 推荐卡去掉 `industry-search-result-card`；宽屏左文右钮，正文横向。  
- 自检：推荐 `article` class 不含 `industry-search-result-card`。  
- V1–V7；push `origin/dev`；handoff 本 ID。

---

## 3. `/goal`

```text
/goal
你是经验丰富的前端工程师（frontend-agent）。
仓库：${GKX_ROOT}/repos/lumen-ui-topic · origin/dev
监管：human:淮政玮
强度：ponytail full。禁止用 YAGNI 跳过 D8/D9/D10、可观测、已评审 Demo 对齐。
上下文：headroom 推荐。Demo 页/Design/五件套禁止 compress 代替精读。
必读：DEMO-CHAIN-FE-D-总派单.md · Design.md §4/§14 · templates/fe-replica-visual-dod.md · 本仓 AGENTS.md · EnterpriseSearch.vue + search-workspace.css
禁止：直连 Python；另起一套更简/灰白 UI；手写就绪度改绿；问用户要不要做某 Bid 叶子。
复刻：语义+布局。禁止两套互斥 display 叠同一节点；只改页底/Hero 不算完成。推荐卡对照 Demo：search-content-card + industry-search-recommendation-card，不要叠 result-card。
```

认领：`claimed_by=agent:frontend-agent` · `supervised_by=human:淮政玮` · `lock_hours=24`
