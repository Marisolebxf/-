# LUMEN-CHAIN-FE-TUNE-L01 · 产业链分析模块人工调整（Job / meta / 诚实空 / BIZ-UX 接线）

> 格式参考 `templates/handoff-template.md`；内容按本叶 as-built。  
> 本文件覆盖 **2026-09-07** 同单多批续修：①记录 Job；②`industry/meta`；③search 信封 / 深圳标杆 / cluster scope / 禁伪集群；④对接 Java `#U1–U17`（`API-CHAIN-BIZ-UX-CATALOG.md`，pipeline 6049 / 镜像 `f3bbc5d`）。任务仍为人工调优单，**不标 done**。  
> **不做**：扩到企业/服务/政策模块；直连 Python；市场规模 Q056 填 `12800`；`USE_MOCK=false` 时 fixture 填数；写死 Q016 对标城；用企业 `enterprise_code` / 企业 `filter-template` 冒充产业用户态。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | registry 已 `in_progress`；本叶为同单续修，不重新认领。执行 Agent：`agent:frontend-agent`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | Job 复用企业 `analysisTask*`；字典/用户态只走 `/chain`。未用 YAGNI 跳过 D8/D9/D10、诚实空、可观测。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 人测口径 + catalog / meta / BIZ-UX 实包精读，禁止 compress 代替。 |

## 问题清单

- 诊断/分析记录未带精确 `analysisType`；表格无分页；复制配置不回填；Job 取消/删除/下载未接。
- `industry/meta` 已返回字典，页面仍只用本地表；`benchmark.items=[]` 时仍可能冒充沪京苏。
- search 丢 `total` / `ignored_filters` / `honesty`；clusters 失败拼 `catalog-fallback:*`；`resolveIndustryClusterScope` 已封装未调。
- 对比篮 / 查询示例·场景·最近 / 高筛方案 / 区域模板仍 localStorage 或串企业表（Java `#U1–U17` 已发后须改接）。

## 修改内容

### A. 记录 Job + meta（前批，仍有效）

- `loadHistory` 精确 `analysisType` + 分页；复制配置切 Tab 回填；Cancel / Delete / #106。
- 周期默认增长率 12.8%、利润率 10.6%、成熟度 84；市场规模仍空（Q056）。
- `industryWorkspaceMeta` overlay 已注册 key；深圳 `items=[]` 级联空；查询高筛读 unsupported / level / attribute。

### B. FE 诚实空四项（本批）

1. **search 信封**：记下 `total` / `ignored_filters` / `honesty`；命中数无 refine 用接口 `total`；`a-alert` 展示未生效筛选与 honesty。
2. **深圳标杆**：`cascaderFromBenchmarkItems(meta.benchmark.items)`；有 items 画接口树，空则空；校验/标签用 flatten 选项。
3. **`attachResolvedClusterScope`**：`startOrReuseJob` create 前调 `resolveIndustryClusterScope`；`grain===empty` 或失败中止；成功写入 `cluster_id` / `industry_ids` / `cluster_grain`。Mock 可按 `industry_id` 反查集群。
4. **禁伪集群**：`useIndustryClusters` 失败只留 `error` + `clusters=[]` + 重试，删除 `catalog-fallback:*`。

### C. 对接 Java BIZ-UX `#U1–U17`（本批）

真源：`agent-delivery/agent-handoffs/产业链分析-CHAIN/API-CHAIN-BIZ-UX-CATALOG.md`；网关前缀一律 `/chain`。

| # | 能力 | FE 落点 |
|---|---|---|
| U1–U4 | 对比篮 | `api/industry/chainUx.ts` + `stores/compareBasket.ts`：`object_type`+`object_ids`；同步/增删/清空；禁止 `enterprise_code` |
| U5–U9 | 示例/场景/最近 | `IndustrySearchPage`：`search-biz/**`；去掉 `gkx-industry-search-recents:v1`；场景→热门场景+`query_tree` 应用 |
| U10–U12 | 高筛「我的方案」 | `useFilterTemplates('industry')` → `/chain/.../filter-template`；不再打企业接口、不用 `biz_type=industry` 混表 |
| U13–U17 | 区域指标/模板 | `IndustryRegionalPage`：`regional/metrics` + official/mine；去掉 `gkx-regional-index-templates` |
| U18 | analysis-dims | 已封装 `industryAnalysisDims`；页面继续用 `#C1` meta（文档允许并存） |

Mock：`src/mock/industry/chainUxApi.ts` + `register.ts`（仅 `USE_MOCK=true`）。

## 测试结果

| 命令 | 结果 |
|---|---|
| `node src/views/industry-center/industryReplicaFix.selfcheck.mjs` | ✅ |
| `node src/api/industry/chainUx.selfcheck.mjs` | ✅（路径 / object_ids / 禁企业串线 / 页接线） |
| `node src/composables/useIndustryClusters.catalogFallback.selfcheck.mjs` | ✅（禁止伪集群） |
| `node src/utils/industrySearchModel.selfcheck.mjs` | ✅（含 hitTotal / envelopeLines） |
| IDE lint（本叶 touched） | 0 |

浏览器端到端：无浏览器 MCP。人测建议本地 `pnpm dev`（网关 `http://111.198.38.90:50199`）：查询加篮、最近检索跨刷新、高筛方案、区域官方/个人模板、深圳标杆空清单。

## 遗留风险

- `#106` 在 `USE_MOCK=true` 无数据 mock，下载会失败（与企业一致）。
- Java `#103` `analysisType` 须精确白名单键；复制配置依赖 `targetParams`/`draft`。
- Java BIZ-UX 增量 SQL 须已上库；只发 topic-chain 不发 topic-enterprise 会 404 `/chain-ux/**`。
- 区域「我的模板」删除 UI 未接 `#U17`（保存/列表已接）；需要再补按钮。
- `pnpm-lock.yaml` 工作区有无关变动，**不要**随本叶提交。
- lumen-ui-topic 本叶代码 **未 commit / 未 push**；任务保持 `in_progress`。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commit：工作区未提交
- pipeline / K8s：本叶不跑；Java 侧 pipeline **6049**、镜像 `f3bbc5d`（topic-chain + topic-enterprise）
- dev 测试：本地 `pnpm dev`

## 可观测性（建议）

- 均走既有 `request.ts` / `defineApi`：`X-Trace-Id` / `traceparent`
- meta / search-biz / basket 失败 `console.error`，页面诚实空/重试，不造数
- 本叶无新埋点 ID

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 前端→Java | ✅ `/chain/topic/v1/industry/**` + `analysis/tasks*` |
| 3 Nebula | N/A |
| 4 可观测 | ✅ 复用既有 header |
| 5 CI/CD | ⚠ FE 未 push |
| 6 demo2 merge | ✅ |
| 7 只调 Java | ✅ |
| 8 数据策略 | ✅ `USE_MOCK=false` 不 fixture 填数 |
| 9 D8 | ✅ Arco；未另起 UI |
| 10 D9 | ✅ 不伪造口径；Q016 空清单 |
| 11 D10 | ✅ 删除确认；高筛/空态诚实 |
| 12 D12 | ✅ 未打 demo 服务 |

## 涉及文件

相对 `${GKX_ROOT}/repos/lumen-ui-topic/`：

- `src/api/industry/paths.ts` / `types.ts` / `index.ts` / `chainUx.ts` / `chainUx.selfcheck.mjs`
- `src/mock/industry/chainUxApi.ts` / `industryClusters.ts` / `register.ts`
- `src/stores/compareBasket.ts` / `industryWorkspaceMeta.ts`
- `src/composables/useFilterTemplates.ts` / `useIndustryAnalysisJob.ts` / `useIndustryClusters.ts`
- `src/config/industryWorkspace.ts` / `industrySearchConfig.ts`
- `src/utils/industryWorkspaceRuntime.js` / `industrySearchModel.ts`
- `src/views/industry-center/IndustrySearchPage.vue` / `IndustryRegionalPage.vue` / `IndustryShenzhenPage.vue` 等
- `src/views/industry-center/industryReplicaFix.selfcheck.mjs`
- `src/composables/useIndustryClusters.catalogFallback.selfcheck.mjs`

编排仓：

- `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-TUNE-L01.md`
- 对照：`…/API-CHAIN-BIZ-UX-CATALOG.md`、`LUMEN-CHAIN-JAVA-BIZ-UX-L01`

## 成本（本叶会话累计估）

| 字段 | 值 |
|------|-----|
| model_used | `claude-sonnet-4.5`（registry 枚举；会话实际为 Cursor Grok 4.5，无 Console 精确 in/out） |
| actual_tokens | 320000（Job/meta ~180000 + 诚实空 ~50000 + BIZ-UX 接线/handoff ~90000，估） |
| actual_cost | 2.11（frontend 70/30 × $3/$15 per MTok） |
| cost_warn | green |
| source | estimate |

## 下一步

- 人测：查询加篮与最近检索；高筛方案；区域模板；深圳空标杆；submit 前 scope。
- 需要上 K8s 时再 commit/push `lumen-ui-topic` `origin/dev`（勿带 `pnpm-lock.yaml`）并派 E0。
- Java 侧 `LUMEN-CHAIN-JAVA-BIZ-UX-L01` 已 `in_progress`（侯佳伟）；FE 已按 catalog 接线，联调确认后可 AV。
- 可选：区域模板删除按钮接 `#U17`；切 `#U18` analysis-dims（非必须）。
- coordinator 收 evidence；任务保持 `in_progress` 直至人测批注清完。
