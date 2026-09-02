# LUMEN-POLICY-D-POL-01-L01 · 政策专题 D · 产业篮分发 + 三分析配置页对象栏

> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> 派单：[`LUMEN-POLICY-FE-D-总派单.md`](./LUMEN-POLICY-FE-D-总派单.md)  
> 细叶：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> 复刻：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> 前序：[`LUMEN-POLICY-D-SHELL-L01.md`](./LUMEN-POLICY-D-SHELL-L01.md) `f96f2a66` · [`LUMEN-POLICY-D-POL-01C-L01.md`](./LUMEN-POLICY-D-POL-01C-L01.md) `fbfe737`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权；lock 24h。未回滚产业链 `KEEP_ANALYSIS_QUERY` / `demo_state`。查询页仍不入篮。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 AnalysisPageHeader / WorkbenchTabs / IndustryClusterSelect / `@/review` / `analysisTaskCreate`；未贴 JSX；未 new 地图；未做过程壳/结果板/wait_view（POL-02/03/04 + WAITVIEW）；未做政策文档 Tab、未让查询页入篮。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 配置页只调 Java：读边 `policySearch` / `policyIndicators`；写边 `POST /topicAsync/topic/v1/analysis/tasks`（规范键 `policy_timeseries` / `policy_regional` / `policy_shenzhen`）。切条件不自动 create。工厂 ODS→GDF→DWD→ADS 拓扑未改。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 范围与实现

US-E7-POL-01 / 01b / 05，金路径 #2。SHELL 三项工作区由 `PolicyShellPlaceholder` 换成共用配置页 `PolicyAnalysisConfigPage`：

1. **对比篮产业 Tab 勾选 1 个产业** → 政策时序 `/policy/overview`、区域对比 `/policy/analysis`、深圳三维 `/policy/recommendation`。query：`source=compare-basket&analysis_type=…&object_type=industry&object_ids[]=&object_names[]=`。
2. **对象栏**：篮带入显示「来自对比篮 · 产业」；可直选产业 XOR 技术领域（Radio `setScopeKind` 清对方）。
3. **产业篮空 / 无有效 VID**：引导「去产业查询」；`canGenerate=false`，**禁止空跑提交**。VID 只用图上链码（`INB170101` → `chain:INB170101`；拒绝 `INB1303` / 中文名 / `CL-*`）。
4. **切条件不自动 create**；条件栏「开始分析」才 `POST analysisTaskCreate`（I2-12 指纹单飞 / 当天成功提示）。成功后留在配置页，不进过程壳。
5. **Java type**：URL 仍用 demo 别名 `policy_region_compare` / `policy_sz_3d`；提交 `javaType` = `policy_timeseries` / `policy_regional` / `policy_shenzhen`。

## 篮 → 配置页如何带对象

`IndustryCompareBasketPanel`（SHELL）勾选 1 产业 → `buildPolicyAnalysisUrl` 拼 query。配置页 `parsePolicyDispatchContext` + `applyDispatch` 填入 `IndustryClusterSelect`。技术领域不进篮，仅页内多选。

## XOR 如何实现

`scopeKind` Radio：`industry` 清空 `techFieldIds`；`tech_field` 清空产业。`buildCreateParams` 只带 `industry_vid` **或** `tech_fields`。Java 校验 `VALIDATION_OBJECT_XOR`。

## 是否禁止空跑

是。无 `chain:INB…` 且无技术领域 → 按钮 disabled + 文案「禁止空跑提交」。产业篮空仍走对比篮空态「去产业查询」。

## 偏离说明

- 本叶不做完整过程/结果/wait_view；记录 Tab 诚实空（WAITVIEW / POL-02 另叶）。
- 「开始分析」可 POST 创建任务，但不强制跑通 Job、不跳过程壳。
- 技术领域 / 深圳指标只读 Java `policyIndicators`，无数诚实空。
- 未改 vite / package.json / `.gitignore`。未回滚 `KEEP_ANALYSIS_QUERY`。

## 产物清单

- 代码：`lumen-ui-topic` `67628df0e3055e7bfa7bd58f4c205cdca1e896b6` → `origin/dev`
- 本文 handoff

## 菜单路径（本叶改）

| 侧栏 | path | 页 |
|------|------|----|
| 政策时序分析 | `/policy/overview` | `PolicyAnalysisConfigPage` |
| 区域政策对比 | `/policy/analysis` | 同上 |
| 深圳政策现状分析 | `/policy/recommendation` | 同上 |
| 门户 / 查询 / 维护 | 不变 | 查询仍 POL-01c；门户/维护仍壳 |

## Java 调用

| 动作 | 方法 | 路径 |
|------|------|------|
| 技术领域 / 深圳指标目录 | `policyIndicators` GET | `/policy/topic/v1/policy/indicators` |
| 关联政策条数 | `policySearch` GET | `/policy/topic/v1/policy/search`（`industry_vid`） |
| 开始分析 | `analysisTaskCreate` POST | `/topicAsync/topic/v1/analysis/tasks`（`analysisType` = 规范键） |
| I2-12 单飞 | `analysisTaskList` GET | 同上 list；指纹 `analysis_fp` |

## 验收证据

- `node src/router/menu.selfcheck.mjs`：`svc-shell ok` + `policy-shell ok`
- `node src/views/policy/policyConfig.selfcheck.mjs`：`policyConfig.selfcheck ok`（Java type / VID / 篮 query / XOR 空跑）
- `npx vue-tsc --noEmit`：通过
- USE_MOCK=true：任务走既有 `analysisTaskStore`（政策 type 跳过企业 subType）；indicators/search 诚实空
- USE_MOCK=false：页内无 `MOCK_`、无 `@/mock/**` 填数

### 复刻五维 R1–R5

| # | 结果 |
|---|------|
| R1 布局 | ✅ 三路由共用配置页：页头 + 对象栏 + 条件栏 + 开始分析；一节点一套 layout |
| R2 交互 | ✅ 篮带入 / 页内直选 / XOR 切换 / 空对象引导 / 切条件不 create / 开始分析才 POST |
| R3 样式 | ✅ `--sci-bg-page` / `#D8E7FC`；复用 `industry-diagnosis` 配置区皮肤 |
| R4 评审 | ✅ 只从 `@/review`：`E7-POL-F01/F02/F03-PAGE-TITLE-TRACE` + CONFIG/SCOPE/INDUSTRY/TECH Trace；`IndustryReviewOnly` |
| R5 Mock | ✅ 开：`registerApiMock`；关：Java 实包，无数诚实空 |

### 检索皮肤 V1–V7

本叶 **无检索页**（查询已由 POL-01c 交付）。下列 **N/A**：

| # | 结果 |
|---|------|
| V1 | N/A 本叶无检索 Hub；配置页底仍用 `--sci-bg-page` / `#d8e7fc` |
| V2 | N/A 无检索 Hero |
| V3 | N/A 无结果卡 |
| V4 | N/A 未叠检索卡 class |
| V5 | N/A 无检索内容列 |
| V6 | N/A 检索空态属 POL-01c |
| V7 | N/A 无 `industry-search-result-card` |

### 工作区 W1–W4（本叶配置区；过程/结果另叶）

| # | 结果 |
|---|------|
| W1 | ✅ **配置区有**（`diagnosis-config-panel` 分析配置 + 对象/条件/开始分析）。过程壳 / 结果板留给 POL-02/03/04；记录 Tab 诚实空留给 WAITVIEW |
| W2 | N/A 本叶无关系图 |
| W3 | N/A 本叶无报告阅读器 |
| W4 | ✅ 切条件不自动 create；条件栏「开始分析」；同指纹 inflight 不重复创建；当天成功提示不跳转（过程打开留给工作区叶） |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端无 NLP |
| 前端→Java→Python `/internal/*` | ✅ 只调 `/policy/topic/v1/policy/**` 与 `/topicAsync` |
| 图谱 Nebula | ✅ 本叶不 new 地图、不直连 nGQL；VID 只用图上链码 |
| 可观测 | ✅ 复用 `request.ts` `X-Trace-Id` |
| CI/CD | ✅ 推 `origin/dev`；禁止 force |
| demo2 不 merge lumen | ✅ Vue 重写，未贴 JSX |
| D8 / D10 | ✅ token + Arco；交互对照企业/产业配置区 |
| D9 8 件套 | ✅ 深圳三维指标旁 MetricSpecCard / PendingBadge；未自造 ⓘ |
| D12 lumen 不调 demo **服务** | ✅ 无 `demo-*` URL；数仓共用 `demo_gkxlumenx_*` 是总控 §0 #6 |

## 测试结果

- 菜单自检、policyConfig 自检、vue-tsc 通过。
- 本机未起 K8s 现网页点；联调确认：配置页只打 Java 契约路径，create 用规范键。

## 遗留风险

- POL-02/03/04 需消费本叶已创建任务的过程壳 / 结果板。
- WAITVIEW 需把记录 Tab 接到 SystemTaskLayer。
- 技术领域目录依赖 Java indicators 带 `kind=tech_field`；现网无数则诚实空、不可空跑。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`67628df0e3055e7bfa7bd58f4c205cdca1e896b6`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev
- 部署：随仓既有 CI；本叶不改 helm
- dev URL：`http://192.168.88.50:30892`（发布后：产业篮勾 1 产业 → 政策三项；或直开 `/policy/overview`）

## 可观测性

- 复用前端 `request.ts` `X-Trace-Id` / `traceparent`
- Tempo / Loki：随平台；本叶未抽样

## 修改内容

| 路径 | 动作 |
|------|------|
| `src/views/policy/PolicyAnalysisConfigPage.vue` | 新增三路由共用配置页 |
| `src/config/policyAnalysisRegistry.ts` | 分发解析 / VID / 指纹 / javaType |
| `src/router/menu.ts` | 三分析路由改挂配置页 |
| `src/router/menu.selfcheck.mjs` | 配置页断言 |
| `src/views/policy/policyConfig.selfcheck.mjs` | XOR / VID / type 自检 |
| `src/mock/enterprise/analysisTaskStore.ts` | 政策 type 跳过企业 subType 校验 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 185000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 1.28 |
| cost_warn | green |
