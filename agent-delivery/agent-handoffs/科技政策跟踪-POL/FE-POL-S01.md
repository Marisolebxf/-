# FE-POL-S01 · 科技政策跟踪 — 前端模块基座

> 交付日期：2026-11-02 · 仓：`repos/lumen-ui-science-pc` · 状态：**停本地工作区，待孔东人工验收**（2026-10-20 闸门，不自动 commit/push）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（认领登记 commit `3e19dab3`，含 backlog→ready 放行：依赖链根节点 + 规划批 1 启动件） |
| 锁窗口 | 4h（至 2026-11-02 20:11） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单 `/goal` 默认 full。全量复用仓内先例（defineApi 双轨 / mock 注册 / PageTabFrame / FE-TS-08A 静态地图 / typeof import 类型），零新依赖。未跳过 D8（评审层集中 `src/review/` + 组件自闸）、D9（35 指标镜像 + QPOL ⚠️）、D10 语义（Arco 优先、Teleport 无新增弹层）、可观测（usePolicyTrack）、架构铁律（D12 无 demo 依赖、USE_MOCK=false 零 fixture） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞问题。2 个执行中判定已按规划真源落定，见「修改内容」⚠️ 标记。

## 修改内容

### 1. 菜单重建 3→7（`src/router/menu.ts`）
- policy 组 navItem +4：`policy-governance`（智能政策库构建）/ `policy-parse`（智能政策拆解）/ `policy-compare-upgrade`（多维政策对比）/ `policy-insight-report`（智能研报生成），permCode 机械推导 `menu:display:policy:governance|parse|compare|report`
- 7 项全部接 `views/policy/` 真实页壳组件（替换 DevelopingView 回落）
- ⚠️ **fullBleed 判定：不加**。同模块既有 3 项均不在 fullBleed 列表；demo 政策 7 页不走 `global-situation-page` 壳（核增 4 页为 `policy-pc-page` 普通卡壳），按「对齐既有同模块判定」执行

### 2. 门户权限清单同步（`docs/门户菜单权限注册清单.md`）
- §二 表格 +4 行（sort 40–70）；§六 机读 JSON +4 条（`tid_policy_governance/parse/compare/report`，命名对齐既有格式）；标题 35→39

### 3. Mock 种子冻结（`src/mock/modules/policy*Seed.ts`，6 文件）
| 文件 | demo 真源 | 行数 | 冻结校验 |
|---|---|---|---|
| `policySeed.ts` | policyData.js | 2502 | ✅ 锚点后主体逐行一致 |
| `policyPcSeed.ts` | policyPcData.js | 993 | ✅ |
| `policySubscriptionSeed.ts` | policySubscription.js | 97 | ✅ |
| `policyDetailContentSeed.ts` | policyDetailContent.js | 171 | ✅ |
| `policyGapSeed.ts` | policyPanoramaGapMock.js | 86 | ✅ |
| `policyMatchSeed.ts` | policyMatch.js | 130 | ✅（依赖闭包补齐：gapSeed 引用其纯函数） |

- 差异仅限：头注释（真源路径 + 同步任务 ID）+ import 切本仓（`CLUSTER_SEED` → `@/lib/industryCluster/seed` 同源冻结；`.js` 相对引用 → 本仓 seed 文件）
- ⚠️ **随机/时间函数定化判定**：`policyPcSeed.ts` L958 `Date.now()`（`inTimeWindow` 运行时时间窗筛选函数）——`publishDate` 均为固定日期字符串，属**查询行为非种子生成**，保留原语义不定化（自检断言 `Date.now() ≤ 1 处` 长期锁定）；其余 5 文件 0 随机 0 时间函数（自检断言锁定）
- demo `mocks/policy-metrics-catalog.json` **未照抄**（页面侧快照，改走 D9 镜像，见 §5）
- dataset 拼装层 `policy.ts`：7 个 create*Dataset 按 demo 各页消费形状分组（panorama 41 项 / analysis 44 项 / simulation 8 项 / 核增 4 页共享 pc 种子 / subscription 工具箱）

### 4. api 双轨（`src/api/policy.ts`）
- 8 端点 `defineApi`（polPanorama/polAnalysis/polSimulation/polGovernance/polParse/polCompare/polInsightReport Dataset），`request.ts`/`http.ts` 复用，api 不感知 mock
- ⚠️ **real 路径占位方式**：契约未冻结（BE-POL-CONTRACT-01 进行中），real 用 `contractPending()` 显式 reject（诚实失败优于伪数据）——比 DR 先例的假 fetch 更严格，冻结时统一替换
- `mock/register.ts` 挂 7 个注册；USE_MOCK=false 零 fixture（D12）

### 5. D9 只读镜像（`src/views/policy/policyMetricsMirror.gen.ts`，脚本生成）
- **真源**：`metrics/registry/metric-readiness-matrix-POLICY.yaml` + `cfg_metric-POLICY-seed.yaml`（查询走 metric-registry MCP，fields=full 导出）+ `产品整体定义/POLICY-data-gap-catalog.yaml`（pending_hint）
- 35 指标全量：D1=aligned 35 / D4=mock 35；8 件套（definition/formula/源表/源系统/频率/版本）+ D1–D4 四维 + `d2Assessed=provisional` 待核验标记
- QPOL 🟡 引用 13 条（QPOL-01×1 / QPOL-02×9 / QPOL-03×2 / QPOL-07×1；QPOL-05 在 gap catalog open_questions 无指标直挂），pendingHint 长文案逐条从 gap catalog 搬运，前端零硬编码
- 生成脚本入库：`scripts/gen-policy-metrics-mirror.ps1`（矩阵更新后重跑；UTF-8 显式编码防 GBK 乱码）

### 6. 地图注册（`src/views/policy/mapRegistry.ts`）
- FE-TS-08A 先例：静态 import + 同步 `registerMap`，无网络竞态，禁运行时外网拉取（demo 的 fetch `/data/*.json` 机制按此升级替换）
- china：复用仓内 `assets/china.geo.json`；shenzhen：新增 `assets/shenzhen.geo.json`（69 KB，冻结自 demo `public/data/shenzhen.json`）+ `toShenzhenDistrictName` 区名映射冻结
- `config/echarts.ts` 核对：Map/Lines/Geo/Heatmap 已注册，**不重复注册**

### 7. 共享样式（`src/views/policy/styles/`）
- `demo-policy-panorama.css`(1549) / `demo-policy-analysis.css`(1259) / `demo-policy-pc-pages.css`(185) / `demo-policy-simulation.css`(556) 整块抽取（含头注释标真源）
- 主色核对：demo 原文已全 `#165dff`（54 处命中零替换，符合 Design.md token）；antd 类名内选择器（`.ant-card-body` 等）由整页复刻时 Arco 对应覆写（各整页单落点）

### 8. 模块组件立项（`src/views/policy/components/`）
- `PolicyStatCard.vue` + 自含 css：左 标题+ⓘ/大数字，右 Mock+QPOL 纵向左对齐（demo 语义等价，Arco a-card 重写）
- `PolicyMetricSpecTrigger.vue`：ⓘ 弹卡 = 8 件套 + **就绪度四行区块**（状态点 Icon 满足绿/部分橙/缺失红/待定蓝/不适用灰）+ QPOL ⚠️ 长文案；数据读模块镜像（非 demo catalog）
- `PendingBadge.vue`：QPOL ⚠️ 角标（评审模式门控）

### 9. 评审层集中（`src/review/useReviewStore.ts`，新建）
- 仓内首个集中评审层（组织方式对齐 lumen-ui-topic `src/review/`，AGENTS.md D8 要求）
- 总开关：`?review=1` 或 localStorage；组件**自闸**（PendingBadge/MetricSpecTrigger 各自读 store，不依赖父级包裹）；关闭后 DOM 零泄漏（metric_id/QPOL/GAP-* 不出现）

### 10. 页壳骨架 ×7（`views/policy/{panorama,analysis,simulation,governance,parse,compare,insight-report}/index.vue`）
- PageTabFrame 页签结构对齐 demo（全景 5 Tab / 分析 3 Tab / 推演 2 Tab）；首屏同步初值防白屏；观测埋点挂载
- **深链（规划 D4）**：全景壳解析 `?tab=match` → 动向 Tab + 匹配弹窗意图（demo `initialOpenMatch` 语义；弹窗本体 FE-POL-01B 实装）；不建菜单项
- 对比壳注明**展示侧会话槽分轨**语义（禁写专题对比篮，R7）
- 推演壳注明 D2：不复刻 demo L2 权限锁，按钮常可用

### 11. 观测（`src/views/policy/usePolicyTrack.ts`）
- `trackPolicyInteraction` CustomEvent + createTraceId（对齐 useDataResourcesTrack 先例）；pageview 沿用仓内 guard 机制（路由级自动覆盖）

### 12. 最小自检（`src/views/policy/policy.test.mjs`）
- 10 组断言：文件存在性 / 6 对种子冻结逐行一致 / 禁 Math.random+Date.now 限额 / 菜单 3→7 + 组件解析 / mock 注册 + api 双轨 + 契约占位 / D9 镜像 35+QPOL13 / 地图静态注册禁 fetch / 页壳 7 + 深链 + 禁互斥 display / 权限清单同步 / 评审层自闸
- 运行：`node src/views/policy/policy.test.mjs`

## 测试结果（交付三绿）

| 门 | 结果 |
|---|---|
| 自检 | ✅ 全绿（含 6 对种子与 demo 真源逐行冻结校验） |
| `pnpm type-check` | ✅ 0 错（vue-tsc --build） |
| `pnpm build` | ✅ built in 25.26s（policy chunk 97.55 kB / gzip 32.20 kB；echarts/geojson chunk 复用既有） |

## 遗留风险

1. **css minify 存量警告**：`Unexpected "/" [css-syntax-error]` 经 stash 基线验证为**存量问题**（本次改动前即存在），非本单引入，未处理——建议另立 chore 单排查
2. **契约冻结后动作**：BE-POL-CONTRACT-01 定稿后需统一替换 `api/policy.ts` 8 处 `contractPending` 占位 + dataset 类型对齐真 DTO
3. **D9 镜像同步义务**：readiness-matrix-POLICY.yaml 更新后须重跑 `scripts/gen-policy-metrics-mirror.ps1`（依赖 metric-registry MCP 导出 full JSON 作输入；脚本已入库可复跑）
4. **antd 类名覆写债**：4 个抽取 css 内 `.ant-*` 选择器在整页复刻（01A~07A）时逐页 Arco 化（避坑清单 §5.3 同款坑：`arco-tabs-pane` 非 `arco-tabs-tabpane`）
5. **QPOL 口径返工面**（R3）：QPOL-01/02/03/07 甲方拍板后只改镜像重生成 + 角标翻转，页组件经 `findPolicyMetric` 读镜像不受影响

## CI/CD（必填）

- 分支：本地 `dev`（基于 origin/dev 同步基线）
- commit：**无**（2026-10-20 人工验收闸门：改动停本地工作区，等孔东走查通过后再 commit/push）
- pipeline / K8s：未触发（同上）
- dev 验证命令：`node src/views/policy/policy.test.mjs && pnpm type-check && pnpm build`

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用仓内（pageview 走 guard `trackPageview`；交互走 `pol-policy-track` CustomEvent）
- traceId：`usePolicyTrack` 每事件 createTraceId
- Tempo / Loki：待 K8s dev 部署后抽样（联调期）

## 涉及文件

**新增（19）**
- `src/views/policy/`：`panorama|analysis|simulation|governance|parse|compare|insight-report/index.vue`、`policyMetricsMirror.gen.ts`、`mapRegistry.ts`、`usePolicyTrack.ts`、`policy.test.mjs`、`components/{PolicyStatCard.vue, PolicyStatCard.css, PolicyMetricSpecTrigger.vue, PendingBadge.vue}`、`styles/demo-policy-{panorama,analysis,pc-pages,simulation}.css`
- `src/mock/modules/`：`policy.ts` + 6 个 `policy*Seed.ts`
- `src/api/policy.ts`、`src/types/policy.ts`、`src/assets/shenzhen.geo.json`、`src/review/useReviewStore.ts`、`scripts/gen-policy-metrics-mirror.ps1`

**修改（3）**
- `src/router/menu.ts`（policy 组 +4 / 组件解析 +7）
- `src/mock/register.ts`（+7 注册）
- `docs/门户菜单权限注册清单.md`（+4 行 +4 JSON 条，35→39）
