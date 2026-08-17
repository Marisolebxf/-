# 前端复刻 · 视觉/布局验收（派单必贴）

> **读者**：coordinator 写 `/goal`、frontend-agent 收单。  
> **触发**：任何「对照已评审 Demo / 本仓兄弟页」的 lumen 前端单（含 demo→lumen、专题直落对照 `demo-ui-topic`）。  
> **挂钩**：手册 **§9.0c** · `.cursor/rules/frontend.mdc` 铁律 11 · 长任务 D 段。  
> **2026-08-17**：复刻范围扩为五维。拆单粒度由总控/`/goal` 范围清单决定，**不**强制一页或一 `workspace` 一叶。**不**把人审截图当作下一叶解锁条件。

## 一句话

**复刻 = 布局 + 交互 + 样式 + 评审模式 + Mock 开关数据**（外加语义 / 路由 / 状态机）。  
只对齐路由/三模式/Hero 色，**不算**复刻完成。禁止用「禁止抄 React」当借口另起一套灰白/挤爆的 DOM。

## 拆单（粒度自选，完成标准看范围清单 + 五维）

- **不强制**一叶一路由或一 `workspace`/`tab` 键。按页、按键、按能力横切（如对比篮分发、Mock 门控、GIS）、或多页一叶均可。coordinator **不得**因「不是一页一叶」拒派。
- `/goal` **必须**写清本叶范围（路由 / 键 / 能力 / 区块清单）。收单按该清单勾五维；清单外的缺口开补单，不假装本叶已铺齐模块。
- **仍拒**：范围只写「入口壳 / 工作区铺齐」且无区块清单；占位路由当完成；只改 Hero；本叶唯一产物是「抽齐组件 / API 封装」且没有可点页（本模块 `src/api/{module}` 尚不存在时，允许一张契约薄单）。
- 组件抽离发生在**第一张用到它的叶**；后叶复用，禁止再抄一份。
- 同仓仍一次一张 frontend 单。下一叶解锁走长任务**联调闸门**（handoff + 本清单勾齐），**不等**人审截图、不等签收 `done`。

## `/goal` 必贴（frontend 复刻单，缺则拒派）

```text
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：{本叶路由/workspace键/能力横切/多页，列出区块}。占位与只改 Hero 不算完成。
禁止：贴 JSX；页内 MOCK；自造 ⓘ；再 new 地图；两套互斥 display。
禁止：USE_MOCK=false 时硬 mock、引用 @/mock/** 或 Demo fixture 填数。
对照：Demo 区块清单 + 本仓兄弟页 + Java 实包字段。handoff 须 V1–V7 + R1–R5（工作区另加 W1–W3）。
```

## 验收清单（handoff 逐条 ✅/❌，缺条 `needs-revision`）

### 检索皮肤（V1–V7，查询/Hub 页必过）

| # | 项 | 不过的典型样子 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | 灰白整页 |
| V2 | 检索 Hub Hero 与本仓企业查询同皮肤 | 白卡片搜框、无底图/橙钮 |
| V3 | **卡片/列表内部**：标题+摘要横向书写；操作在右侧或下行，不断开漂 | 一字一换行（容器被挤到 ~24px） |
| V4 | **一个节点一套 layout**：Demo 用 `recommendation-card` 就不要再叠 `result-card`（后者 `grid-template-columns: 24px 1fr auto` 是给「勾选列」的） | 推荐卡变成三列网格，主文进 24px 列 |
| V5 | `min-width: 0` 只加在 **flex/grid 子项需要截断** 时，不要让唯一内容列宽度塌成 0 | 标题 `ellipsis` 只剩 1～2 字 |
| V6 | 推荐/结果空态：无数诚实空；有数则卡结构与 Demo/`RecommendationSection` 同行（`xl:flex-row`） | 有数据却 `a-empty`，或有卡但结构错 |
| V7 | 自检：推荐 `article` class **不得**同时含 `industry-search-result-card`（除非子节点数=网格列数，且第一列真是 checkbox） | 本清单 V3 复现 |

### 复刻五维（每叶必过）

| # | 项 | 不过的典型样子 |
|---|---|---|
| R1 布局 | Demo 本页区块都有结构；一节点一套 layout | 只有路由/Tab 标题 |
| R2 交互 | 空 / 加载 / 失败 / wait_view / 有结果 / 条件脏，Demo 有则有 | 静态壳 |
| R3 样式 | `--sci-*`、页底、与本仓兄弟页同皮肤 | 灰白后台、只改 Hero |
| R4 评审 | 只从 `@/review` 挂点；handoff 列本页 mount-id；关评审 DOM 零泄漏 | 页内自造 ⓘ / Trace |
| R5 Mock | 开：只走 `USE_MOCK` + `src/mock/register.ts` 的 `registerApiMock`，形状=Java 实包。**关（`USE_MOCK=false` 或未开全局 Mock）**：禁止硬 mock，禁止引用 `@/mock/**` 或 Demo fixture 填数；只渲染 Java 实包，无字段=可见空态 | 页内 `const MOCK_`、关开关仍用 fixture 撑满 |

### 工作区页另加（诊断 / 区域 / 深圳 / 全景 / 服务机构分析等）

| # | 项 | 不过的典型样子 |
|---|---|---|
| W1 | 配置区 / 过程壳 / 结果板 / 记录 Tab，Demo 有则有 | 标题 + 空 `a-empty` |
| W2 | 关系图用本仓 G6（全景/样板键/瓶颈等），不用 ECharts 冒充 | 柱状图代替关系图 |
| W3 | 报告入口挂已有 `SystemReportReader`，不新造阅读器 | 再做一套报告页 |

### 拆单闸

| # | 项 |
|---|-----|
| S1 | `/goal` 无范围清单（路由/键/能力/区块）→ 拒派；有清单则不论按页还是横切都可派 |
| S2 | 标题含「API 封装 / 组件抽离」且本叶没有可点页 → 本叶无效（除非本模块 `src/api` 尚不存在的契约薄单） |

## 工程约束（写进 `/goal` 即可，不必每条再造编号）

- 语法：Vue 3 `<script setup>` + TS；禁止把 Demo `.tsx` / JSX / React props（如 `content`、`className`）贴进 `.vue`。
- 地图：复用 `UnifiedLeafletMap` 或已有天地图封装；禁止页面再 `new L.map`；禁止高德/Google；禁止用 Demo 区级假点位填地图。
- 类型真源：Java 实包字段，不是 Demo 的 TypeScript interface。
- 复用白名单：`@/review`、`SearchScaffold`/`SearchHub`、`compareBasket`、`analysisTask`、`SystemTaskFloat`、`SystemReportReader`、已有 `components/{module}/*`。禁止第二套检索 Hero、任务中心、地图栈。

## 施工顺序（防 ponytail 偷工）

1. 打开 Demo 真源，按 `/goal` 范围列出**本叶区块清单**（不要凭记忆叠 class）。  
2. 只补本叶缺的 Java types + `registerApiMock`（已有 `src/api/{module}` 则不要另开封装单）。  
3. 能复用的组件复用；本叶新块才抽到 `components/{module}/`。  
4. 范围内组装：布局 / 交互 / 样式 / 评审挂点一次做完。  
5. `USE_MOCK=false` 走一遍：必须诚实空或实包，不得回落到 fixture。  
6. handoff 写 V1–V7（查询页）+ R1–R5 + 工作区 W1–W3；缺条 `needs-revision`。

金路径 / `e2e:chain-gold` 绿 **≠** 复刻完成。
