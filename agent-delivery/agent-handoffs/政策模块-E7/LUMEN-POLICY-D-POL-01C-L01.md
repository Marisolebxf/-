# LUMEN-POLICY-D-POL-01C-L01 · 政策专题 D · US-E7-POL-01c /policy/search 查询页

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-SHELL-L01.md`](./LUMEN-POLICY-D-SHELL-L01.md) `f96f2a66`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。未回滚产业链 `KEEP_ANALYSIS_QUERY` / `demo_state`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 SearchHub / ElementSearchWorkbench / FilterPanel / RecentSearchPanel / `@/review` TraceInfoIcon；未贴 JSX；未 new 地图；未入篮、未 create 分析任务；卡片操作仅「查看详情」。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 前端走图上已有读边：`lumen-ui-topic` → gateway `/policy/topic/v1/policy/search` · `/docs/{id}` → `gkxlumen-topic-policy`。工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

`/policy/search` 由 SHELL 空壳补齐为查询完成页（US-E7-POL-01c）：

1. **智能检索**：本地 `parsePolicyQuery` 抽出 level / policy_type / region chips，余词作 `keyword`/`q`，GET Java `policySearch`。
2. **查政策**：`keyword`/`q` 打 Java search。
3. **高级筛选**：本仓 `FilterPanel` page 变体；条件映射 Java `keyword` / `level` / `policy_type` / `region` / `ministry` / `publish_code`。热门标签预置 DSL 后切高级筛选。
4. **结果卡**：标题+摘要横向书写（`line-clamp-2`）；级别/类型 Tag；元信息；右侧「查看详情」。**无**「加入对比篮」「深度分析」。class=`policy-search-result`，未叠 `industry-search-result-card`。
5. **详情**：点卡 `policyDocs(id)`；loading / 失败可重试 / `item=null` 诚实空。
6. **空态**：仅已执行查询且无命中才 `data-search-state="empty"`；未搜为 recommendation（Java 最近 6 条，无数诚实空，非 5xx）。
7. 查询不入篮、不发起分析（DEC-E7）。未改 DefaultLayout `KEEP_ANALYSIS_QUERY`。

## 偏离说明

- 智能解析在前端做词典/正则（对标服务机构查询 / demo Wave0），不另调 Python NL；条件仍只打 Java search。
- Java/Python search 单值透传：多选 level/type/region 取首项。
- 字段库只含 Java 能吃的字段；未做 Demo 的 supportStrength / fund 等无参筛选项（避免假筛）。
- 列表不造支持强度数字（无 KPI 不造假）。
- 现网 `30899` search 本机探测 404（topic-policy Deployment 可能未起，SHELL 已记）；编码联调按 C-SEARCH 契约：路径、空态、不 5xx 填数。

## 产物清单

- 代码：`lumen-ui-topic` `fbfe73724bb7eb7498bb6edb7329a112c1651402` → `origin/dev`
- 本文 handoff

## Java 调用

| 动作 | 方法 | 路径 | 参数 |
|------|------|------|------|
| 智能/关键字/高筛 | `policySearch` GET | `/policy/topic/v1/policy/search` | `keyword`/`q`、`level`、`policy_type`、`region`、`ministry`、`publish_code`、`limit`/`offset` |
| 详情 | `policyDocs` GET | `/policy/topic/v1/policy/docs/{id}` | path id |
| Mock 开 | `registerApiMock` | 诚实空 `items=[]` / `item=null` `fabricated=false` | 页内无 `MOCK_` |

## 验收证据

- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`（含无 `>加入对比篮<` / `>深度分析<`、有 `policyDocs`/`FilterPanel`/`parsePolicyQuery`、KEEP_ANALYSIS_QUERY 仍在 DefaultLayout）
- `node src/views/policy/policySearchModel.selfcheck.mjs`：`policySearchModel.selfcheck ok`
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=true：仍走 `src/mock/policy/policyApi.ts` 诚实空包
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数；只渲染 Java 实包

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ Demo 本页区块：标题/Hub 三模式/示例与热门/最近检索/高级筛选字段库/结果网格/详情抽屉；一节点一套 layout |
| R2 交互 | ✅ 未搜推荐 / 加载 / 失败可重试 / 无命中空态 / 有结果 / 高筛条件脏后需再应用；详情空/失败诚实 |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；SearchHub 经 ElementSearchWorkbench 与企业查询同皮肤 |
| R4 评审 | ✅ 只从 `@/review`：`POLICY-SEARCH-POL-01C-TRACE` / `POLICY-SEARCH-ADVANCED-TRACE`；关评审 TraceInfoIcon 自闸 |
| R5 Mock | ✅ 开：`registerApiMock` 诚实空；关：Java 实包，无数诚实空 |

### 检索皮肤 V1–V7

| # | 结果 |
|---|------|
| V1 | ✅ 页底 `var(--sci-bg-page)` / `#D8E7FC` |
| V2 | ✅ SearchHub `enterprise-search-hero` 挂在 ElementSearchWorkbench 下，与企业查询同皮肤 |
| V3 | ✅ 卡内标题+摘要横向书写；操作在右侧「查看详情」 |
| V4 | ✅ 未叠 `industry-search-result-card`；一节点 `policy-search-result` flex |
| V5 | ✅ 主列 `min-width: 0` + `flex: 1`；标题不 `ellipsis` 塌成 1 字 |
| V6 | ✅ 无数：推荐空或检索空 `a-empty`；有数才出卡，`xl` 两列网格 |
| V7 | ✅ 结果 `article` 不含 `industry-search-result-card` |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP 服务调用；词典解析只为组 Java 查询参数 |
| 前端→Java→Python `/internal/*` | ✅ 只调 `policySearch` / `policyDocs` |
| 图谱 Nebula | ✅ 本叶不 new 地图、不直连 nGQL |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；交互对标本仓服务机构查询 + demo `/policy/search` |
| D9 8 件套 | ✅ 本页无统计 KPI 数字，未自造 ⓘ；评审只 TraceInfoIcon |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL；数仓共用 `demo_gkxlumenx_*` 是总控 §0 #6 |

## 测试结果

- 菜单自检 + 映射自检 + vue-tsc 通过。
- 金路径 #1：智能检索或高级筛选走 Java 能出卡（有数）或无命中空态；卡上无禁钮。
- 联调通过：前端查询/详情路径与 C-SEARCH 对外 REST 对齐；空/失败诚实，不 5xx 填数。

## 遗留风险

- K8s `gkxlumen-topic-policy` 若未发布，现网 search 404；前端仍诚实失败/空，不回落 fixture。
- 多选筛选因 Java 单值透传只送首项。
- 三项工作区 / 产业篮分发仍待 POL-01 / 工作区叶。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`fbfe73724bb7eb7498bb6edb7329a112c1651402`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://192.168.88.50:30892/policy/search`（发布后）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/views/policy/PolicySearchPage.vue` | SHELL 空壳 → 查询完成页 |
| `src/views/policy/policySearchModel.ts` | 字段库 / 智能解析 / Java 参数映射 |
| `src/views/policy/policySearchModel.selfcheck.mjs` | 映射自检 |
| `src/config/policySearchConfig.ts` | 转 re-export 完成配置 |
| `src/router/menu.selfcheck.mjs` | POL-01c 禁钮/详情/高筛断言 |

未改 `DefaultLayout.vue`（KEEP_ANALYSIS_QUERY 保留）。未改 vite / package.json / `.gitignore`。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 195000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.28 |
| cost_warn | green |
