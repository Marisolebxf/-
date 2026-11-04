# FIX-POL-ANALYSIS-APPLY-L01 · 政策分析评价·报告可视化修复（点应用双请求 + 数据不刷新）

- **仓**：`lumen-ui-science-pc` · 一轮 **`c75762c`**（2026-11-04 用户放行推送）、二轮 **`93414e3`**（同日线上复测仍空图后对齐 as-built，均推 `origin/dev`）
- **类型 / 状态**：bugfix · in_progress（验收通过 push → CI 部署后转 pending_test）
- **强度**：ponytail full

## 走查问题（用户 2026-11-04 截图反馈）

政策分析评价 → 政策分析报告可视化呈现，Tab1。修改条件后点【应用】：

1. **请求了两次接口**（Network 面板两个 `jobs`）；
2. **返回有数据的响应没有刷新界面**，图表仍空；
3. 界面提示「已按所选维度刷新分析图表（**Mock**）」——真轨读表后该文案不诚实。

## 根因（3 个，均已定位到行）

| # | 根因 | 证据 |
|---|---|---|
| 1 | **契约键位错位**：前端读 `result?.items` + 蛇形行字段（`axis_kind/axis_position/metric_name/compare_value`）；真实链路 `PolicyEvaluationService.trend()` / element `records()` 返回**信封键 `records`**，行字段经 `ElementDao#camel` 转为**驼峰**（`axisKind/dimValue/metricName/pointValue`、`objectKind/objectName/compareCount`）→ 行全部被丢弃，图恒空 | `gkxlumen-display/.../PolicyEvaluationService.java#trend`（`out.put("records", points)`）、`gkxlumen-element/.../ElementDao.java#camel`（注释明示「行记录 snake_case 列名统一转 camelCase，与前端契约一致」）、handoff `POL-L2-DS11-BE-L01`（「无行则 `records` 空」） |
| 2 | **watch 引用比较双触发**：`index.vue` 里 `:switch-dims` 是内联模板表达式，每次渲染生成**新数组引用**；改条件（v-model 更新 `dimensions` 触发父重渲）一次 + 点【应用】（`appliedDimensions` 更新）一次 = 两次 POST `/jobs` | `index.vue` 原 L678 内联 `Object.keys(...).filter(...)`；`TrendMetricsChart.vue` `watch([props.switchDims, props.metrics])` |
| 3 | 提示语写死「（Mock）」字样 | `index.vue#applyDimensions` |

## 修复内容（只动前端 5 文件）

| 文件 | 改动 |
|---|---|
| `src/api/policyEvaluationViz.ts` | 三个 Result 信封键 `items`→`records`；行接口改 **camel 主字段 + 蛇形可选兜底**；新增统一解包纯函数 `policyEvalRowsOf()`（`records ?? items ?? []`，undefined/null 不炸） |
| `src/mock/modules/policyEvalViz.ts` | mock 轨返回同形行（`{ records }` + camel 字段，蛇形键保留兜底）——双轨单一读法，种子派生逻辑零改动 |
| `src/views/policy/analysis/index.vue` | `:switch-dims` 内联表达式提为页级 `computed trendSwitchDims`（子组件拿到稳定引用，改条件不触发、点【应用】只触发一次）；提示语按 `USE_MOCK` 双轨区分；补 `USE_MOCK` import |
| `src/views/policy/analysis/TrendMetricsChart.vue` | 读行改 `policyEvalRowsOf`；camel 消费 + 蛇形兜底；watch 加 `deep: true`（防父侧未来整组替换引用时漏触发）；注释补请求时机契约 |
| `src/views/policy/analysis/RegionGroupCompare.vue` | 同上（分区行 camel 消费） |
| `src/views/policy/analysis/ReportTemplateExport.vue` | 模板选用行同改（`templateName/reportPeriod` + 兜底） |

> 请求时机语义（修复后）：趋势 = 首屏 + 点【应用】各一次；分区 = 首屏 + 切子 Tab/资源投向 + 点【应用】（投向是受控 prop，属「应用后」值，语义不变）；条件变更（未点应用）零请求。

## 偏离说明

0. **【二轮 2026-11-04】一轮修复后线上仍空图（trace `bc1e546caeb2acd5ca176e73ec6cdab`，用户：「几乎是全部的条件了，应该有数据才对」）**。排查（Tempo 两平面无此 trace；Loki element 近 30 分钟唯一业务错误行 `gapfill 读表失败，返回空列表: Unknown column 'topic_or_metric' in 'field list'` —— 属壳表另一缺口）+ 灌数单 as-built 对照定位**三个新根因**（灌数行在库：trend 44 / partition 41，但链路三套词表/字段对不上）：
   1. **指标名词表漂移**：前端发种子名「支持力度/惠及面/执行率」，表内 `metric_name` DISTINCT = 科技政策连续出台数 / 研发投入强度 / 企业受惠覆盖率 / 政策兑现满意度 → element `metric_name IN (...)` 零命中。
   2. **行字段名漂移**：表列 as-built = `switch_dim/dim_value/point_value/is_key_point/is_fluctuation`（camel 后 `dimValue/pointValue`），一轮读的 `axisPosition/compareValue` 在真实响应里不存在 → 即使命中也取不到值。分区同理（`compare_value`→`compareValue`，非 `compareCount`）。
   3. **投向外发词表漂移**：前端发「资金支持/平台载体/税收优惠」，表内 `resource_direction` = 财政资金/人才引进/创新平台/税费减免。另发现从上线起的原生 bug：`loadTrend` 把 seed key（`supportStrength`）直接当 metric 外发，连 mock 轨中文词表都对不上。
   - **二轮修复**（commit `93414e3`）：新增 `trendVocab.ts`（表内闭集单文件真源）；请求前种子 key → 表内名映射（mock 轨保持种子词表，两轨互不覆盖）；行字段消费改 `dimValue/pointValue`（蛇形兜底）；分区投向外发真轨用表内闭集；接上 `isKeyPoint/isFluctuation` markPoint；分区行字段 `compareValue`。
   - **契约口径裁定**：API 分册「只收表内已有名称」本义即表内闭集 → 前端对齐 as-built 为正解；灌数单 handoff「列与 DATA 逐列一致」与 DATA 分册 `axis_kind/axis_position/compare_value` 不符，属灌数单偏离未登记（Data 侧待办，不动已评审灌数数据）。
1. **行接口 camel 为主 + 蛇形可选兜底**，而非只留 camel：`policyEvalRowsOf` 已兼容历史 `items` 信封，兜底成本一行（`r.dimValue ?? r.axis_position`），换双轨（mock 轨同形行）零风险过渡。真实链路 element DAO 只出 camel，兜底分支不生效。
2. **`watch` 加 `deep: true`**：稳定引用修复双触发后，若未来父侧整组替换 `appliedDimensions` 内层数组，浅比较会漏触发；`deep` 保证「点应用必有恰好一次请求」。实测无额外请求（computed 引用稳定时 deep 不产生多余触发）。
3. 本地**未跑 `pnpm build`**：按 2026-11-04 用户指令（本机编译验证禁止，走 GitLab 流水线）；type-check（`vue-tsc --build`）已本地跑绿。

## 验收证据（本地三件套）

- **类型门**：`pnpm type-check` → exit 0 ✓
- **契约自检**：`POL-L2-DS11-VIZ-WIRING.test.mjs` → **29 项全绿** ✓（含 §1b 响应形状、§5 修复防回归 7 组断言：表内闭集词表、as-built 字段消费、单次请求、双轨文案）
- **行为自检**：`FIX-POL-ANALYSIS-APPLY-L01.test.mjs`（新增）→ **7 项全绿** ✓（as-built 场景：真实 records/camel 响应 → 趋势/分区序列非空；重点/波动 markPoint；闭集外行丢弃；诚实空态；蛇形兜底；空信封不炸）
- **页面回归**：`FE-POL-02A.test.mjs` → 28 组全绿 ✓
- **待复测**：二轮 `93414e3` CI 部署后，同条件复测（勾指标→应用：趋势出时间维 4 条序列 2021–2026；分区出对象柱/热力；应用仅 1 次 `jobs`）
## 架构合规自检

| 条 | 结论 |
|---|---|
| 调用链：前端只打 `/display/v1/policy/**`，不越层直连 Python/库 | ✅ 零新增端点，仅修正响应消费 |
| D9：不伪闭合，无行诚实空态 | ✅ `records` 空仍渲染 a-empty，不造假曲线；`policyEvalRowsOf` 不补行 |
| D10/评审门控：MockBadge、评审闸门零改动 | ✅ 仅动数据接线与请求时机 |
| 双轨：USE_MOCK=true 种子轨视觉不回归 | ✅ mock 轨种子派生逻辑零改动，仅输出形状对齐；FE-POL-02A 28 组断言回归绿 |
| 禁改配置文件 / .gitignore / package.json | ✅ 未触碰 |
| commit 标注 `[agent:frontend-agent]`；业务仓不自动 push | ✅ 已按 2026-11-04 用户放行推送（`c75762c`） |

## 后续（CI 部署后）

1. CI 绿 + K8s dev 发布 → 走查复测三件（改条件→应用仅 1 次 `jobs` / 趋势分区出数 / 文案无「（Mock）」）；
2. 复测过 → 任务转 `pending_test` → QA 集成测试。

ponytail: 修复为最小 diff（5 文件），未加兼容抽象层——`policyEvalRowsOf` 一个纯函数覆盖三叶解包；蛇形兜底为双轨过渡的一行成本，可随 mock 轨下线一并删除。
