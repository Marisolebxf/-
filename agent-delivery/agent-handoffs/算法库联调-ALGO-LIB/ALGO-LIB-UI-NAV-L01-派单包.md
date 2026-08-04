# 派单包：ALGO-LIB-UI-NAV-L01 — 算法库联调台左右菜单改造

- **任务 ID**：ALGO-LIB-UI-NAV-L01
- **派发角色**：coordinator-agent
- **承接角色**：frontend-agent
- **监管人**：human:淮政玮
- **仓**：`${GKX_ROOT}/repos/demo-ui-system-test`（push `origin/main`）
- **认领**：`claimed` · `coordinator_dispatch` · lock 至 `2026-08-04T16:00:00+08:00`
- **派发时间**：2026-08-04
- **effort / difficulty**：5 / M · est.tokens 250k

---

## 1. 背景

`demo-ui-system-test` 登录后首页为按钮卡片入口（「企业分析 Demo」等），企业页 `/entan` 用顶部 Tab 切换算法视图，【灌数据】在页头。调度者要求改为**左右菜单算法库导航**，命名与子页顺序对齐招标 `科技专题服务算法库.md`。

## 2. 范围（必做）

### 2.1 布局

- `layout`：顶栏保留 + **左侧菜单** + 右侧 `router-view`
- 登录后默认进入「框架联调」或首个可用算法库路由

### 2.2 一级菜单（顺序固定）

| 顺序 | 菜单文案 | 路由 | 状态 |
|------|----------|------|------|
| 1 | 框架联调 | `/home` | 可用（现联调页） |
| 2 | 产业链分析算法库 | `/chain` | 可用 |
| 3 | 企业分析算法库 | `/entan`（及子路由） | 可用 |
| 4 | 政策分析算法库 | `/policy` | 可用 |
| 5 | 产业服务算法库 | — | **灰显占位**（disabled + Tooltip「设计/算法待就绪」） |
| 6 | 产业综合分析算法库 | — | **灰显占位** |
| 7 | 创新监测 | `/innov` | 可用 |
| 8 | 科技新闻四要素复核 | `/tech-news` | 可用 |

禁止再在首页用大按钮堆入口（首页仅保留联调演示内容即可）。

### 2.3 企业分析算法库 · 子页

原 `el-tabs` **改为嵌套子路由**（如 `/entan/basic` …）。

**招标对齐组（顺序）**

1. 基础指标 — 【灌数据】按钮 + SeedHelpBadge **只放此页**
2. 竞争力水平分析（映射现「综合评分」等）
3. 发展历程（无实现则占位 Empty）
4. 痛难点识别（映射诊断类）
5. 供应链关系（映射链主/图谱相关可拆，主映射供应链语义）
6. 技术力评估
7. 商业力评估
8. 招引推荐（无则占位）
9. 培育推荐（无则占位）

**工程增强组（单独分组，不硬塞招标顺序）**

- 风险评分 / 重点资讯 / 企业图谱 / 企业评估（异步）等现有能力

政策 / 产业链：本任务至少完成**命名 + 左侧挂载**；Tab→子页可同范式或最小改动（handoff 注明 as-built）。

### 2.4 技术约束

- 本仓继续 **Element Plus + Vue3**（不强制 Arco / Design.md 新页栈）
- 前端只经网关调服务；不直连 Python / DB
- 可观测：沿用现有 request / observability 惯例
- commit 含 `[agent:frontend-agent]` + task-id；push `origin/main`

## 3. DoD

见 `task-registry.yaml#ALGO-LIB-UI-NAV-L01.definition_of_done`。

完工手递：`agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-UI-NAV-L01.md`（截图：左菜单全貌、企业子页、灌数据仅在基础指标、灰显占位；cost 四字段）。

## 4. /goal 话术（复制到新会话）

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue3 + Element Plus + TypeScript；组件化复用、只经网关调后端、不直连 Python/DB。
任务 ID：ALGO-LIB-UI-NAV-L01
监管人：human:淮政玮
仓库：${GKX_ROOT}/repos/demo-ui-system-test（push origin/main）
必读：
  - agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-UI-NAV-L01-派单包.md
  - agent-delivery/bid-reference/科技专题服务算法库.md（企业深度 §5 + 功能清单顺序）
  - agent-delivery/task-registry.yaml#ALGO-LIB-UI-NAV-L01
  - .cursor/rules/00-team-constitution.mdc
目标：
  1) layout 左右菜单；Demo 文案改为「××分析算法库」
  2) 一级菜单顺序与灰显占位见派单包 §2.2
  3) /entan Tab→子路由；灌数据仅在基础指标；招标组 + 工程增强组见派单包 §2.3
DoD：见 registry；完工 handoff；status→review；cost 回填。
明确开工后将 registry 本任务改为 in_progress。
不要问我，按派单包执行。
```
