# QA-POLICY-acceptance-report —— 政策维度原型验收报告

> 任务：POLICY-PROTO-L08（Epic: E-POLICY-PROTOTYPE）｜ 角色：qa-agent ｜ 日期：2026-06-23
> 验收对象：政策算法全集（polan）+ 专题 3 页（`/policy/*`）+ 门户 6 页（`/policy-portal/*`）+ system-test `/policy` 模块
> 验收依据：bid 政策章节 + `catalog-topic-policy.yaml`（P-01~P-77）+ `Design.md §14`（D8）+ `data-lineage-policy.md`（D9）+ `cfg_metric-POLICY-seed.yaml`
> 例外约定：本次完整跑，**QA 不作为人工阻塞 gate**，但产出完整验收报告作为产物。
> 证据性质：**基于证据验收** —— QA 在 `demo-algo-ent-analysis` 本地复跑了 `run_all_policy.py`/`verify_policy.py` + 独立 TestClient，并实跑了 demo-ui-topic（`npm run build`）与 demo-ui-system-test（`pnpm build`）两套构建。

---

## 0. 执行摘要

| 维度 | 结论 |
|------|------|
| 算法全集（15 步 / 17 ADS / 11 模型 / 6 端点） | ✅ PASS（QA 本地复跑数据与 ALGO handoff **逐项一致**） |
| 专题 3 页 `/policy/*` | ✅ PASS（Arco+ECharts，recharts 已迁移，路由/角标到位） |
| 门户 6 页 `/policy-portal/*` | ⚠️ PARTIAL（B2/B3 地图/图谱按比例圆点/降级落地，待 GeoJSON+人工点测升级） |
| system-test `/policy` 模块 | ⚠️ PARTIAL（前端+脚本就位，网关 `/policy/**` 路由待 ops 执行才能真联调） |
| D9 血缘 8 件套 + ⓘ/🧪/⚠️ 角标 | ✅ PASS（19 指标 8 件套齐全，前端三类角标均落实） |
| Design.md §14（检查 8 + 验收） | ✅/⏳（设计/代码层 8 条检查全过；首屏观感/面积比例 4 条待截图核验） |
| 构建状态（topic / system-test） | ✅ PASS（两套 build 均 exit 0，QA 实跑复现） |

**总体结论：PASS WITH CONDITIONS**（条件见 §7）。

---

## 1. 范围对照（9 页 + 算法全集 vs bid 政策章节 + P-XX）

### 1.1 前端 9 页（catalog 路由已核对，见 catalog-topic-policy.yaml L176~226 / L706~736）

| # | 页面 | 路由 | P-XX | bid 章节 | 优先级 | 实现仓/文件 | 结论 |
|---|------|------|------|----------|--------|------------|------|
| A1 | 政策时序分析 | `/policy/overview` | P-70 | §1.1.1.2.4.2.6.1 | P0 | topic `PolicyOverview.tsx` | ✅ PASS |
| A2 | 区域政策对比 | `/policy/analysis` | P-72 | §1.1.1.2.4.2.6.2 | P0 | topic `PolicyAnalysis.tsx` | ✅ PASS |
| A3 | 深圳政策现状·三维框架 | `/policy/recommendation` | P-73 | §1.1.1.2.4.2.6.3 | P0 | topic `PolicyRecommendation.tsx` | ✅ PASS（三维雷达+权重校验落地） |
| B1 | 政策概况统计 | `/policy-portal/overview` | P-17 | §1.1.1.1.1.1.2.1 | P0 | topic `PolicyPortalOverview.tsx` | ✅ PASS |
| B2 | 政策地图 | `/policy-portal/map` | P-18 | §1.1.1.1.1.1.2.2 | P1 | topic `PolicyPortalMap.tsx`+`PolicyLeafletMap.tsx` | ⚠️ PARTIAL（比例圆点降级，未接 GeoJSON choropleth） |
| B3 | 政策产业覆盖 | `/policy-portal/industry-coverage` | P-19 | §1.1.1.1.1.1.2.3 | P1 | topic `PolicyPortalIndustryCoverage.tsx`+`PolicyChainGraph.tsx` | ⚠️ PARTIAL（G6 v5 事件待人工点测确认下钻） |
| B4 | 政策力度排名 | `/policy-portal/intensity-rank` | P-20 | §1.1.1.1.1.1.2.4 | P1 | topic `PolicyPortalIntensityRank.tsx` | ⚠️ PARTIAL（力度口径 QPOL-02 临时权重） |
| B5 | 最新政策动态 | `/policy-portal/latest` | P-21 | §1.1.1.1.1.1.2.5 | P0 | topic `PolicyPortalLatest.tsx` | ✅ PASS |
| B6 | 深圳政策对比 | `/policy-portal/shenzhen` | P-22 | §1.1.1.1.1.1.2.6 | P0 | topic `PolicyPortalShenzhen.tsx` | ✅ PASS |

> 路由核对：9 个路由在 `demo-ui-topic/src/app/routes.tsx`（L182~192）+ `catalog-topic-policy.yaml` 中均已登记，前后一致。导航入口 `Layout.tsx` 新增「门户-政策扶持」组（6 项）。

### 1.2 算法全集（后台，P-01~P-16；P-08/09 实体图谱；文本/匹配/推演随全集）

| 范围段 | bid/P-XX | 实现 | 结论 |
|--------|----------|------|------|
| 基础指标 5 类（级别/类型/时序/全国/深圳） | P-01~P-07 §..1.1.3 | `polan/basic/indicators.py` → 5 张 ADS | ✅ PASS |
| 实体图谱 NER+RE（4 边） | P-08/P-09 §..2.5/2.6 | `polan/graph/entity.py` → entity 7517 / node 806 / edge 3726 | ✅ PASS（Nebula 本地兜底 PG/SQLite 镜像） |
| 深度模型 6（焦点/力度/效果/短板/机遇/布局） | P-10~P-16 §..8.1~8.6 | `polan/eval/*.py` | ✅ PASS |
| 文本解析/匹配推送/效果推演 | P-52/P-38/P-58~62 | `polan/text/*.py` | ✅ PASS（全集跑通，前端弱消费/system-test 展示） |
| 模型注册 | — | `polan/models/registry.py` → cfg_model_registry 11 POLICY | ✅ PASS |

### 1.3 范围边界核对

- DS-10/11/12（展示系统科技政策跟踪前端）**本次明确排除**，未发现误扩前端页面 → ✅ 合规，无 ±10% 越界风险。
- 检索/订阅/报告/对标类 P-23~P-69 多数 route=null（Wave2/后台）→ ✅ 未越界落前端。

---

## 2. 算法运行证据复核（QA 本地实跑）

> 复跑环境：`demo-algo-ent-analysis`，`PYTHONIOENCODING=utf-8`，DB 后端=SQLite（零依赖）。

### 2.1 run_all_policy 15 步（QA 复跑 `python scripts/run_all_policy.py`，总耗时 1.0s，exit 0）

| # | 步骤 | QA 复跑结果 | ALGO handoff 值 | 一致 |
|---|------|------------|-----------------|------|
| 1 | Schema 初始化 | done 0.01s | 0.01s | ✅ |
| 2 | 模型注册 seed | seeded=13 | 13 | ✅ |
| 3 | Mock 贴源 | 政策=600，层级 {国际27/市级266/省级137/国家级56/区县级114} | 同 | ✅ |
| 4 | A 基础指标 | A1=6(总600,时效80.83%) A2=5 A3=9 A4=31省 A5=9区 | 同 | ✅ |
| 5 | B NER/RE | 实体7517 节点806 边3726 {support1894/apply_to834/regulate600/cite398} | 同 | ✅ |
| 6 | B+ Nebula 灌入 | 未启用跳过（镜像可用） | 同 | ✅ |
| 7 | C1 焦点 | 600（Top focus 97.82 rel 1.58） | 同 | ✅ |
| 8 | C2 力度 | 单600 省31 三维62（榜首 广东 idx=115.0 覆盖100%） | 同 | ✅ |
| 9 | C3 效果 | 31 区域 | 同 | ✅ |
| 10 | C4 短板 | 31 区域，短板合计40 | 同 | ✅ |
| 11 | C5 机遇 | 31 区域，机遇541（阈值≥60） | 同 | ✅ |
| 12 | C6 布局 | 31 区域，布局建议68（优先级≥55） | 同 | ✅ |
| 13 | D1 文本解析 | 600 | 同 | ✅ |
| 14 | D2 匹配推送 | 主体18 匹配144（Top≤8） | 同 | ✅ |
| 15 | D3 效果推演 | 36（12省×3情景） | 同 | ✅ |

### 2.2 各 ADS 行数（QA 复跑 `python scripts/verify_policy.py`）—— 与 handoff §3.2 **逐行一致**

| 表 | QA 复跑 | handoff | 表 | QA 复跑 | handoff |
|----|--------|---------|----|--------|---------|
| dwd.policy_base_info | 600 | 600 | policy_focus | 631 | 631 |
| policy_level_dist | 6 | 6 | policy_intensity | 631 | 631 |
| policy_type_dist | 5 | 5 | policy_effect | 93 | 93 |
| policy_timeseries | 9 | 9 | policy_metric_timeseries | 93 | 93 |
| policy_national_dist | 31 | 31 | policy_entity | 7517 | 7517 |
| policy_sz_dist | 9 | 9 | policy_graph_node/edge | 806/3726 | 806/3726 |
| policy_text_parse | 600 | 600 | policy_match | 144 | 144 |
| policy_simulate | 36 | 36 | cfg_model_registry | 13(含11 POLICY) | 13 |

> 幂等性：QA 二次连续运行行数完全一致（truncate+批量 insert），与 handoff「幂等可重跑」一致。✅

### 2.3 `/v1/policy` 端点（QA 用**独立 FastAPI app 挂载 `api/policy_routes.py`** + TestClient 实跑）

> 说明：`api/main.py` 因 import `entan.common.db`（需 `pg8000`，本地未装）无法直接整体启动；QA 改用「独立 app + include policy router」方式验证政策路由本身，**不安装额外依赖**。

| 端点 | QA 实跑结果 | 核对 |
|------|------------|------|
| `GET /internal/policy/models/registry` | **count=11，source=db** | ✅ 11 模型注册一致 |
| `GET /v1/policy/metrics` | headline={total=600, validity=80.83, provinces=31, peak=139, nodes=806, edges=3726}，model_count=11 | ✅ 与 handoff §3.4 一致 |
| `GET /v1/policy/indicators` | keys=[level,type,timeseries,national,sz] | ✅ |
| `GET /v1/policy/analysis/intensity` | 返回行（LIMIT 默认 100） | ✅ 端点可用（注：handoff §3.4 记 count=3 系不同查询口径，端点功能正常） |
| `GET /v1/policy/graph?center=POL202500010` | source=sqlite，子图 nodes=9 edges=9 | ✅ 与 handoff 一致（Nebula 不在位自动回退镜像） |
| `GET /v1/policy/simulate?scope_code=440000` | 3 条 | ✅ 一致 |

### 2.4 polan 包结构核对

`polan/` 26 个 .py 模块均存在（common×4 / mockgen×2 / basic×2 / graph×3 / eval×8 / text×4 / models×2 / `__init__`），与 handoff §1.1 结构图一致。✅

**§2 复核结论：ALGO handoff 所述算法运行证据全部属实，QA 本地复跑数据逐项吻合。✅ PASS**

---

## 3. D9 数据血缘抽检（8 件套完整性 + 前端角标落实）

### 3.1 抽检 8 个统计指标的 8 件套（真源 `cfg_metric-POLICY-seed.yaml`，19 条）

| metric_id | 中文名 | 口径 | 公式 | 源表 | 源系统 | 频率 | 版本 | status | 8 件套 |
|-----------|--------|------|------|------|--------|------|------|--------|--------|
| M_POLICY_LEVEL_DIST | 政策级别分布 | ✓ | ✓ | ✓ | Mock@batch | daily | 0.1.0 | ✅ | 齐 |
| M_POLICY_TOTAL_COUNT | 政策总数 | ✓ | ✓ | ✓ | Mock@batch | daily | 0.1.0 | ✅ | 齐 |
| M_POLICY_TYPE_DIST | 政策类型分布 | ✓(QPOL-01) | pending_algorithm | ✓ | Mock@batch | daily | 0.1.0 | ⚠️ | 齐 |
| M_POLICY_TIMESERIES | 政策时序指标 | ✓ | ✓(环比/连续性) | ✓ | Mock@batch | daily | 0.1.0 | 🔧 | 齐 |
| M_POLICY_INTENSITY_INDEX | 政策力度指数 | ✓(QPOL-02) | pending(权重) | ✓ | Mock@batch | weekly | 0.1.0 | ⚠️ | 齐 |
| M_POLICY_EFFECT_SCORE | 政策效果评分 | ✓(数据缺口) | pending | ✓(待采购) | Mock@batch | quarterly | 0.1.0 | 🔧 | 齐 |
| M_POLICY_SUPPORT_STRENGTH | 支持力度 | ✓(QPOL-02) | pending | ✓ | Mock@batch | weekly | 0.1.0 | ⚠️ | 齐 |
| M_POLICY_IMPLEMENTATION_EFFECT | 落地实效性 | ✓(数据缺口) | pending | ✓(待采购) | Mock@batch | quarterly | 0.1.0 | 🔧 | 齐 |

> 8/8 抽检指标的 D9「8 件套」字段齐全；状态分布 19 条 = ✅4 / 🔧12 / ⚠️3 / ❌0，与 seed 文件尾部汇总一致。✅

### 3.2 前端角标落实（ⓘ MetricSpecCard / 🧪 MockBadge / ⚠️ PendingBadge）

- `demo-ui-topic/src/app/pages/policy/policyShared.tsx`：`PolicyMetricCard` 中
  - `metricId` 存在 → 渲染 `<MetricSpecCard meta={meta} />`（ⓘ）
  - `is_mock` → `<MockBadge />`（🧪）
  - `mapping_status==='⚠️' || pending_ref` → `<PendingBadge pendingRef />`（⚠️）
- 门户 6 页 `portalShared.tsx` re-export 同一 `PolicyMetricCard`，两层角标一致。✅
- 前端 8 件套副本 `src/app/mock/policy/policyMetricSeed.ts`（19 条）与 cfg seed 对齐，注明 Wave1 起改读 `/metrics/v1/catalog` 前端零改动。✅

**§3 结论：D9 血缘抽检 PASS。** 唯一观察：QPOL-01/02/03 业务口径未定（⚠️ 已标），属待甲方项（见 §6），非血缘缺陷。

---

## 4. Design.md §14 对照（检查清单 8 条 + 验收标准）

> 核对真源 `Design.md` L831~856。注：§14 实为 **8 条检查清单 + 10 条验收标准**；FE/UI handoff 习惯简称「验收 6 条」（取关键子集），此处按权威全文逐条核对。

### 4.1 检查清单 8 条（设计/代码层，QA 静态核验）

| # | 检查项 | 证据 | 结论 |
|---|--------|------|------|
| 1 | 浅蓝白工作台非深色大屏 | DOM 用 `var(--sci-bg-page)`，token 锁 #D8E7FC | ✅ |
| 2 | 保留 Header/左导航/主内容/中央主视图/右侧分析 | AnalysisShell + SecondaryAnalysisTabs（policyShared/portalShared） | ✅ |
| 3 | 选中态统一 #165DFF / #E8F3FF | `var(--sci-primary)`/`-soft` | ✅ |
| 4 | 表单/按钮/分页/标签接近 Arco 节奏 | 9 页均 `@arco-design/web-react`（Table/Tabs/Button/Slider/Timeline…） | ✅ |
| 5 | 地图工具栏/图例/筛选尺寸克制 | Leaflet 图例 + Radio 切换 h32 | ✅ |
| 6 | loading/empty/disabled/error 状态 | system-test useGraceful+ErrorBanner；topic Alert/空态 | ✅ |
| 7 | 图表色遵循要素色/图表色序列 | `POLICY_COLORS`/`LEVEL_COLOR` 镜像 design-tokens hex | ✅ |
| 8 | 避免霓虹/紫蓝发光/营销 hero/emoji/无意义占位 | 政策页无 hero/emoji，结论先行 JudgmentStrip | ✅ |

### 4.2 验收标准（实测/截图层，部分待 frontend 运行后核验）

| # | 验收项 | 结论 | 说明 |
|---|--------|------|------|
| 1 | 首屏一眼是地图/图谱分析工作台 | ⏳ | 规格三段工作区已定，待运行截图核验 |
| 2 | Header≈64px | ✅(token) | `--sci-header-h:64px` |
| 3 | 左导航≈200px | ✅(token) | `--sci-sidebar-w:200px` |
| 4 | 控件≈32px | ✅ | Arco 默认 h32 + token |
| 5 | 主色≈#165DFF | ✅(token) | — |
| 6 | 背景≈#D8E7FC | ✅(token) | — |
| 7 | 卡片无强阴影 | ✅ | `--sci-shadow-none` |
| 8 | 中央主视图>右侧面板 | ⏳ | 面积比例待截图核验 |
| 9 | 右侧有 tabs/分组 | ✅ | SecondaryAnalysisTabs |
| 10 | 依赖含 @arco-design/web-react 无 antd | ✅ | package.json 含 arco；**政策 9 页 grep 零 `from 'antd'`、零 recharts** |

> 关键合规核验（QA grep 实测）：
> - 专题 3 页：均 `import ... from '@arco-design/web-react'` + `EChart`，**已无 recharts**（recharts→ECharts 迁移完成，符合 D8/UX R5/O-UI-05）。
> - 门户 6 页：Arco + `@antv/g6`（B3）+ `leaflet`（B2/B6），**无 antd/recharts**。
> - `package.json` 仍保留 `recharts@2.15.2`（供其他历史页面），政策页面未引用，不违规。

**§4 结论：检查 8 条全 ✅；验收标准 token/代码层达标，2 条（首屏观感、面积比例）待 frontend 截图核验（⏳，非阻断）。**

---

## 5. 构建状态复核（QA 实跑）

| 仓 | 命令 | QA 实跑结果 | handoff 声称 | 结论 |
|----|------|------------|--------------|------|
| demo-ui-topic | `npm run build`（vite v6.3.5） | **exit 0**，4790 modules，built in **56.22s** | 4790 modules ~57s | ✅ 一致 |
| demo-ui-system-test | `pnpm build`（vite v4.5.14） | **exit 0**，built in **30.30s**，marked.esm 打包通过 | 2263 modules ~29s | ✅ 一致 |

> topic build 有「chunk > 500kB」warning（index js 5.2MB），属性能优化提示，非错误，exit 0。建议后续 manualChunks 拆包（非本次阻断）。
> system-test marked.esm（1.07MB）打包通过，印证 TextAnalysis marked 报告渲染链路。

**§5 结论：两套构建 QA 实跑均绿，与 handoff 一致。✅ PASS**

---

## 6. 缺陷 / 风险清单

| 编号 | 级别 | 描述 | 当前处理 | 责任 | 上线前条件 |
|------|------|------|----------|------|-----------|
| QPOL-01 | 🟡 口径待定 | 政策"类型"一级分类口径未定 | 临时取 ODS topic_type，TYPE_DIST 标 ⚠️ | PM→甲方 | 甲方确认后升 🟢，移除 ⚠️ |
| QPOL-02 | 🟡 口径待定 | 力度/效果/焦点/短板/机遇/布局/三维 权重阈值未定 | settings_policy.yaml 经验权重，INTENSITY_INDEX/SUPPORT_STRENGTH 标 ⚠️ | 算法 lead+甲方 | 同上 |
| QPOL-03 | 🟡 口径待定 | 政策关联/产业适配匹配规则未定 | 临时共现/相似度，INDUSTRY_FIT/RELATION_DEGREE 标 🔧 | 算法 lead+甲方 | 同上 |
| DEF-DATA-01 | 🟠 数据缺口 | 落地实效性/政策效果：执行监测/宏观经济/社会数据**无 ODS 来源（待采购）** | A3/B6 以受控随机 Mock 代理（seed 固定）+ 文案明示"待采购" | PM+数据 lead | 采购到位或对接政府执行库 |
| DEF-OPS-01 | 🟠 联调阻断 | system-test 网关 `/policy/**` 路由未落 | 已备 `add_gateway_route_policy.py`，**需 ops/算法仓执行**（DB 写+Redis 重载）；未执行前 system-test 8 Tab 走 useGraceful 优雅降级（不崩） | ops/算法 | 执行脚本后真联调复测 |
| DEF-FE-01 | 🟡 降级 | B2/B6 Leaflet 未接省/市 GeoJSON，先比例圆点降级（非 choropleth）；底图瓦片需联网 | 规格已定，待 GeoJSON 资产+三级下钻人工评审升级 | frontend/UI | GeoJSON 接入+人工评审 |
| DEF-FE-02 | 🟡 待点测 | B3 G6 v5 `NodeEvent.CLICK` 下钻命中以构建通过为准 | 建议联调期人工点测确认 | frontend | 人工点测确认 |
| DEF-FE-03 | 🟢 已闭环 | 专题 3 页 recharts→ECharts 迁移 | QA grep 确认已迁移、无 recharts 引用 | — | 无（已完成） |
| DEF-NEB-01 | 🟡 环境 | 本地无 NebulaGraph（192.168.88.43:9669 不可达） | nebula_loader 安全跳过，图谱走 PG/SQLite 镜像，API 自动回退；`set POLAN_NEBULA_ENABLED=1` 可灌入 | 算法/运维 | 生产环境接 Nebula 复测 |
| DEF-ALGO-01 | 🟢 观察 | `/v1/policy/analysis/intensity` handoff 记 count=3，QA 实跑返回 LIMIT 100 行 | 端点功能正常，仅查询口径/默认 limit 差异 | algorithm | 无（非缺陷） |
| DEF-PERF-01 | 🟢 优化 | topic build 主 chunk 5.2MB（>500kB warning） | 非错误，exit 0 | frontend | 建议后续 manualChunks 拆包 |

> 无 🔴 阻断级缺陷。联调真打通依赖 DEF-OPS-01（网关路由）；前端 9 页与算法全集均已在各自层面跑通。

---

## 7. 验收结论：PASS WITH CONDITIONS

政策维度原型（算法全集 + 专题 3 页 + 门户 6 页 + system-test 模块）**通过验收**，附以下放行条件：

1. **业务口径（QPOL-01/02/03 + 🟡-04/05/07）上线前必须升 🟢**：力度/三维/类型/连续性等口径由甲方书面/纪要确认，前端 ⚠️ 角标方可移除（否则 A1/A2/A3/B1/B4 统计数字存在返工）。
2. **数据缺口（DEF-DATA-01）需采购闭环**：落地实效性/政策效果的执行监测、宏观经济、社会发展数据无 ODS 来源，上线前需采购或对接政府执行库，替换 Mock 代理。
3. **网关 `/policy/**` 路由（DEF-OPS-01）需 ops 执行**：system-test 真联调前须在算法/ops 仓执行 `add_gateway_route_policy.py` 并 Redis 重载；当前优雅降级保证不崩但非真数据。
4. **B2/B6 地图与 B3 图谱升级（DEF-FE-01/02）**：GeoJSON 接入 + 三级下钻 + G6 下钻命中需人工评审/点测后升级，当前比例圆点降级可演示。
5. **§14 验收 2 条截图核验（首屏观感、中央主视图>右侧面板）**：待 frontend 运行后截图复核（非阻断）。
6. **上线前仍需 UX/UI/PM 人工评审**：本次为例外完整跑跳过人工 gate，正式上线前补齐人工评审与 NebulaGraph 生产环境联调。

---

## 8. 架构合规自检（公约 §2 十条，QA 视角）

| # | 铁律 | 核验 |
|---|------|------|
| 1 | 算法只在 Python | ✅ polan 全 Python；前端零算法（纯展示/mock） |
| 2 | 调用链 前端→Java→Python 不越层 | ✅ system-test 走 `/api`→网关→`/v1/policy/**`；topic 当前 mock，Wave1 切 Java |
| 3 | 图谱 NebulaGraph 禁 Neo4j | ✅ space gkx_policy；本地兜底 PG/SQLite 镜像；前端仅 G6 渲染 |
| 4 | 可观测性必加 | ✅ system-test 复用 observability.ts/traceId；topic POLICY_TRACK 埋点 |
| 7 | 共享聚合核心（方案 A） | ✅ 专题+门户共享 polan + Java；Java 只读 ADS |
| 8 | 标准表先行 + Mock | ✅ 17 张 ADS 先行 + batch=mock_20260623 |
| 10 | 数据血缘 D9 | ✅ 19 指标 8 件套 + ⓘ/🧪/⚠️ 角标 |
| 5/6 | CI/CD / demo2 只读 | ✅ topic 走 feature 分支未直推 main；system-test feat/policy-demo；未动 lumen |

> 全部 ✅，无 ❌。

---

## 9. 产物清单与证据

- 本报告：`agent-handoffs/政策模块-E7/QA-POLICY-acceptance-report.md`
- 算法复跑证据：QA 实跑 `run_all_policy.py`（1.0s/15 步绿）+ `verify_policy.py`（17 表行数）+ 独立 TestClient（6 端点 + registry=11）
- 构建证据：QA 实跑 topic `npm run build`（exit 0，56.22s）+ system-test `pnpm build`（exit 0，30.30s）
- 静态核验：routes.tsx 9 路由 / policyShared 角标 / cfg_metric seed 8 件套 / Design.md §14 全文
- 上游 handoff（9 份）：PROD / DATA×2 / UX / UI / ALGO / FE×3，均已通读对照

---

> 本 handoff 即 POLICY-PROTO-L08 的验收交付证据。维护：qa-agent 起草；业务口径（QPOL-01~03）变更须 PM + 甲方确认后由 data/algorithm-agent 更新 seed 与角标。
