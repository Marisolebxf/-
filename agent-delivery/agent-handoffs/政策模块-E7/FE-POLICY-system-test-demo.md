# FE-POLICY-system-test-demo —— 政策算法效果展示前端（系统级实验沙箱）

> 任务：POLICY-PROTO-L07（Epic: E-POLICY-PROTOTYPE）｜ 角色：frontend-agent ｜ 日期：2026-06-23
> 仓：`demo-ui-system-test`（Vue 3 + Vite + Element Plus + 静态 hash 路由）｜ 分支：`feat/policy-demo`（未直推 main/dev）
> 镜像模板：企业分析 `/entan` 范式（API 客户端 + el-tabs 壳 + ECharts + marked 报告）
> 上游真源：`demo-algo-ent-analysis/api/policy_routes.py` + handoff `ALGO-POLICY-fullset.md`

---

## 1. 范围与实现

新增 `/policy` 模块，**完全镜像 `/entan`**，前端经 `/api` → 网关 → Python 直连政策算法 `/v1/policy/**`，
展示上游 polan 算法子体跑通的政策算法效果。沿用现有 `request` 封装（envelope/鉴权/traceId）、
`observability.ts`；图表统一 ECharts（含力导向 graph）；政策解析报告用 `marked` 渲染。

---

## 2. 模块结构（新增文件）

```
src/api/policy/index.ts                         # 政策 API 客户端，BASE='/policy/v1'
src/views/policy/
├── index.vue                                   # el-tabs 壳（8 个 Tab）
└── components/
    ├── useGraceful.ts                          # 统一"优雅降级"加载器（捕获异常 + traceId）
    ├── ErrorBanner.vue                         # 错误横幅（带 traceId 截图可定位）
    ├── BasicIndicators.vue                     # 基础指标 A1-A5 + headline 卡片
    ├── GraphView.vue                           # 政策图谱（ECharts force graph，复用 entan 交互）
    ├── FocusAnalysis.vue                       # 焦点识别（focus 深度模型）
    ├── IntensityEval.vue                       # 力度评估（intensity 深度模型）
    ├── EffectEval.vue                          # 效果评估（effect 深度模型）
    ├── GapOpportunity.vue                      # 短板·机遇（gap + opportunity 深度模型）
    ├── LayoutRecommend.vue                     # 布局推荐（layout 深度模型）
    └── TextAnalysis.vue                        # 文本解析·匹配·推演（marked 渲染报告，内嵌 3 子 Tab）
```

改动文件：
- `src/router/index.ts`：layout.children 追加 `{ path: 'policy', name: 'policy', title: '政策分析' }`
- `src/views/home/index.vue`：hero 区新增「政策分析 Demo」按钮（el-icon Document，路由 `/policy`）

运维脚本（算法/ops 仓）：
- `demo-algo-ent-analysis/scripts/add_gateway_route_policy.py`：仿 `add_gateway_route.py`，
  新增网关路由 `gkx-policy` Path=/policy/**（需在算法/ops 仓提交并执行）

---

## 3. Tab 与算法端点映射表

| # | Tab | 组件 | 算法端点（前端 url，BASE=/policy/v1） | 后端真实路径 | 主要产出 |
|---|-----|------|----------------------------------------|--------------|----------|
| 1 | 基础指标 | BasicIndicators | `/policy/indicators?kind=all` + `/policy/metrics` | `/v1/policy/indicators`、`/v1/policy/metrics` | 级别/类型/时序/全国/深圳 + headline（总数/时效/省数/峰值/图节点边） |
| 2 | 政策图谱 | GraphView | `/policy/graph?center=&steps=&limit=` | `/v1/policy/graph` | 政策关联子图（Nebula 优先，PG/SQLite 镜像兜底），点击节点重定心 |
| 3 | 焦点识别 | FocusAnalysis | `/policy/analysis/focus` | `/v1/policy/analysis/focus` | 政策焦点指数 focus_score + 关联度 relation_degree |
| 4 | 力度评估 | IntensityEval | `/policy/analysis/intensity` | `/v1/policy/analysis/intensity` | 力度指数 intensity_index + 产业覆盖 industry_coverage |
| 5 | 效果评估 | EffectEval | `/policy/analysis/effect` | `/v1/policy/analysis/effect` | 区域 effect_score + 落地实效 impl_effect |
| 6 | 短板·机遇 | GapOpportunity | `/policy/analysis/gap` + `/policy/analysis/opportunity` | `/v1/policy/analysis/gap`、`.../opportunity` | 区域短板数 shortboard_cnt + 机遇数 opportunity_cnt |
| 7 | 布局推荐 | LayoutRecommend | `/policy/analysis/layout` | `/v1/policy/analysis/layout` | 区域布局建议数 layout_rec_cnt + ext 明细 |
| 8 | 文本解析·匹配·推演 | TextAnalysis | `/policy/text/parse` + `/policy/match` + `/policy/simulate` | `/v1/policy/text/parse`、`.../match`、`.../simulate` | 结构化解析(marked 报告) / 主体匹配推送 / 效果推演曲线 |
| — | 模型注册（API 已封装，备用） | api/policy `fetchModelsRegistry` | `/policy/internal/policy/models/registry` | `/internal/policy/models/registry` | element=POLICY 11 模型注册表 |

> 响应统一 `{code, msg, data}`，业务取 `res.data`；与企业 `/v1/**` 完全一致。

---

## 4. 路由 / 入口

- 路由：hash 路由 `#/policy`（layout 子路由，isAuth=true）。
- 入口：首页 hero 区「政策分析 Demo」按钮（与「企业分析 Demo」「创新监测 Demo」并列）。

---

## 5. 网关路由说明（关键）

政策算法 `polan` 已 `include_router` 进**与企业分析同一个** FastAPI 应用
（`ent-analysis-demo`，见 `api/main.py` L31-36），政策端点 `/v1/policy/**` 与
`/internal/policy/**` 与企业 `/v1/**` 同进程同服务。

**链路（与 entan 同范式，全局 StripPrefix=1）：**
```
前端 /api/policy/v1/policy/indicators
  → nginx 去 /api → 网关 Path=/policy/** 命中 → StripPrefix 去 /policy → /v1/policy/indicators
前端 /api/policy/internal/policy/models/registry
  → 网关 Path=/policy/** → StripPrefix 去 /policy → /internal/policy/models/registry
```

**两种落地方式（任选其一）：**
1. **新增专用路由（推荐，已备脚本）**：在算法/ops 仓执行
   `python scripts/add_gateway_route_policy.py`，插入 `gkx-policy` 路由
   `Path=/policy/** → http://demo-platform-entan-py:8000`（与 entan 同 Service，因同进程）。
2. **若暂不能改网关**：因政策端点与 entan 同服务，可临时复用 entan 路由——
   把 `src/api/policy/index.ts` 的 `BASE` 由 `'/policy/v1'` 改为 `'/entan/v1'`、
   并把 registry 调用前缀由 `/policy/internal/...` 改为 `/entan/internal/...`，
   即走已存在的 `/entan/**` 路由（`/entan/v1/policy/**` → strip → `/v1/policy/**`）。
   > 当前默认按方式 1（专用 `/policy/**` 路由）实现，语义更清晰、与"政策维度独立模块"一致。

---

## 6. 联调 / 降级说明

- **正常联调**：网关 `/policy/**` 路由就位 + Python 服务（含 polan 路由）起 + ADS 已跑
  （`python scripts/run_all_policy.py`）→ 8 个 Tab 直出真实算法效果。
- **优雅降级（Python 未起 / 网关未配 / 业务错）**：每个组件用 `useGraceful` 包裹加载，
  捕获异常后顶部显示 `<ErrorBanner>`（"政策算法服务暂不可用…（traceId: xxxxxxxx…）"），
  `request.ts` 拦截器同时弹 ElMessage（含 traceId 8 位短码）。**页面不崩**，可继续切 Tab。
- **traceId**：沿用 `observability.ts` 的 `extractTraceId`，跨 Java/Python 单一 traceId 串联，
  截图即可在企业 Grafana Tempo/Loki 排障。

---

## 7. 自检：构建结果

- `pnpm install --node-linker=hoisted` ✅（Windows 默认 symlink 受限，用 hoisted 规避）
- `pnpm build` ✅ —— `vite v4.5.14`，2263 modules transformed，built in ~29s，exit 0，无 TS/编译错误。
- `ReadLints`（policy api + views）✅ 无 lint 错误。
- marked / echarts 均为仓内既有依赖，无新增依赖、无改动配置文件（合规 §4.3）。

---

## 8. 架构合规自检（公约 §2）

| # | 铁律 | 自检 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 前端零算法，纯展示 polan 产出 |
| 2 | 调用链不可越层 | ✅ 前端 → /api → 网关 → Python `/v1/policy/**`；不直连裸端口 |
| 4 | 可观测性必加 | ✅ 复用 `request.ts` + `observability.ts`，traceId 透传/展示 |
| 6 | demo2 只读 merge | ✅ 本仓为 system-test，未触碰 lumen 正式仓 |
| git §4.2 | demo-ui-* 走分支 | ✅ 新建 `feat/policy-demo`，未推 main/dev；commit 带 `[agent:frontend]` |
| §4.3 | 不改配置文件 | ✅ 未动 package.json / vite.config / .gitignore（仅 add_gateway_route_policy.py 为新增脚本） |

---

## 9. 阻塞与风险

| 项 | 描述 | 当前处理 | 责任 |
|----|------|----------|------|
| 网关路由需人工执行 | `/policy/**` 路由需在算法/ops 仓跑 `add_gateway_route_policy.py`（含 DB 写 + Redis 重载） | 已备脚本 + 文档；前端不具网关权限 | ops/算法 |
| 字段结构弱约定 | `ext`/`structured_elements`/`match_reasons`/`curve` 等 JSON 结构由算法侧解析，前端做了"数组/对象/字符串"多形态兜底渲染（如 LayoutRecommend ext、TextAnalysis curve） | 通用渲染，结构稳定后可精修列名 | frontend + 算法 |
| 政策图谱无 search/path/编辑端点 | 政策侧仅 `/v1/policy/graph`（无 candidates/path/mock-enterprise），故图谱 Tab 不含 entan 的"待加入/路径发现/增量增删"交互 | 改为"输入中心 + 点击节点重定心 + 全局概览"，对齐政策端点能力 | — |
| 业务口径 pending（QPOL-01/02/03） | 类型口径/权重阈值/匹配规则待甲方（见 ALGO handoff §6） | 前端如实展示算法当前产出；口径角标由数据/算法侧标注，前端不替甲方拍板 | PM→甲方 |
| 未起 Python 时无 mock 数据 | 本任务采用"优雅降级提示"而非前端造 mock（避免与真实联调目标冲突） | ErrorBanner + traceId 提示，页面不崩 | — |

---

## 10. 一句话总结

`/policy` 政策分析模块已按企业 `/entan` 范式落地（`src/api/policy/index.ts` + 8-Tab 壳 + 8 组件 + 路由 + 首页入口 + 网关脚本），
直连政策算法 `/v1/policy/{indicators,metrics,graph,analysis/{focus,intensity,effect,gap,opportunity,layout},text/parse,match,simulate}` 与
`/internal/policy/models/registry`，统一 `{code,msg,data}` 取数、ECharts 出图、marked 渲染解析报告，
Python 未起时按组件级 `useGraceful` + `ErrorBanner`（带 traceId）优雅降级不崩；`pnpm build` 已绿（2263 modules，无报错）。
```
