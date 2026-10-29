# LUMEN-CHAIN-FE-SEARCH-SKIN-L01 · 产业查询套回 Lumen 搜索 Hero 与页底

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：重写 SearchScaffold / 三模式 / 入篮；改 Java/Python；另起第二套 Hero 色值；标 `done`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已 claimed + in_progress；lock 24h。本单为 bugfix 视觉补单，**不标 done**，evidence 交 coordinator 收。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过 D8 页底/Hero。最短路径：页根双 class + Hero 选择器并列 + catalog 推荐回退；未套 SearchScaffold。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 厚包 / D 总派单铁律 2/3 / EnterpriseSearch / search-workspace.css 精读，禁止 compress 代替。 |

## 问题清单

- 产业查询页根只有 `industry-search-page`，Hero CSS 只绑 `.enterprise-search-page` → 灰白裸页。
- 推荐用 fixture `recordId` 对 catalog，对不上则「暂无推荐产业」。

## 修改内容

1. **页根皮肤**：`IndustrySearchPage` 同时带 `enterprise-search-page` + `industry-search-page`，`background: var(--sci-bg-page)`（`#D8E7FC`）、`min-height: 100%`。
2. **Hero**：`search-workspace.css` 把 `.search-hub-card` / `.enterprise-search-hero` 选择器扩到 `.industry-search-page`，色值/底图仍只写一份（`enterprise-search-bg.png` + 蓝渐变 + 橙钮 `#ff7d00`）。
3. **推荐**：`resolveIndustrySearchRecommendations` — fixture `recordId` 命中优先；全未命中且 catalog 非空则取前 N 条（N=fixture 长度，空 seed 则 6）；catalog 空数组 → 诚实空，文案仍为「暂无推荐产业」。`RecommendationSection` 绑企业 `ElementRecord`，未套；保留现卡，内容区包 `search-translucent-container`（`--sci-surface-main`）。
4. **其它产业链页根**铺 `var(--sci-bg-page)`：总览 / 诊断 / 全景 / 区域 / 深圳 / 维护。不重做 G6/工作区。
5. **自检**：`industrySearchModel.selfcheck.mjs` 扩推荐回退断言 + CSS/页根选择器字符串。

## 测试结果

| 命令 | 结果 |
|---|---|
| `node src/utils/industrySearchModel.selfcheck.mjs` | ✅ `industrySearchModel.selfcheck ok` |
| `npm run type-check`（`vue-tsc --build`） | ✅ exit 0 |
| `npx eslint` 本单 8 个 Vue/TS 文件 | ✅ 0 error |
| 全量 `npm run build`（含 vite 打包） | 未再跑；type-check 已是 `build` 脚本的编译闸门 |

## 遗留风险

- K8s 上仍是旧前端镜像，**需要 devops 再跑 E0 rollout** 后才能在 http://10.50.69.111:30892 看到新皮肤。
- catalog API 真 0 行时推荐区诚实空（不造假卡）。
- 未改三模式/入篮语义。

## 是否需要 devops 再跑 E0 rollout

**需要。** 本单已 push `lumen-ui-topic` `origin/dev`；集群要吃到新 Hero/页底必须重建并滚动前端镜像。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commit：`ee3ff6f7d26e0e25a6b11aaa08374960611c2551`
- 标题：`fix(chain): 产业查询套回 Lumen 搜索 Hero 与页底 [agent:frontend-agent]`
- push：✅ `origin/dev`（`b0032e1..ee3ff6f`）
- pipeline URL / ID：push 后 GitLab `frontend:build` 待跑；本机未取 pipeline ID
- 部署 namespace / 镜像 tag：待 E0
- K8s rollout：本单不跑；**需 E0**
- dev 测试 URL：http://10.50.69.111:30892 （rollout 后）

## 可观测性（建议）

- 请求头：沿用既有 `X-Trace-Id` / `traceparent`（本单未改 `request.ts`）
- 本单无新埋点（皮肤/推荐接线，无新 API）

## 涉及文件

相对 `lumen-ui-topic/`：

- `src/views/industry-center/IndustrySearchPage.vue`
- `src/assets/search-workspace.css`
- `src/utils/industrySearchModel.ts`
- `src/utils/industrySearchModel.selfcheck.mjs`
- `src/views/industry-center/industrySearch.css`
- `src/views/industry-center/industryOverview.css`
- `src/views/industry-center/IndustryOverviewPage.vue`
- `src/views/industry-center/IndustryDiagnosisPage.vue`
- `src/views/industry-center/IndustryPanoramaPage.vue`
- `src/views/industry-center/IndustryRegionalPage.vue`
- `src/views/industry-center/IndustryShenzhenPage.vue`
- `src/views/industry-center/IndustryMaintenancePage.vue`

本 handoff：`agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-SEARCH-SKIN-L01.md`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 调用链 | 只调 Java REST | ✅ 未改 API；仍走 `/chain/topic/v1/industry/**` |
| Python | 禁止直连 | ✅ 未直连 Python / ES / MySQL / Nebula |
| D8 | 页底 `#D8E7FC` / Hero 与企业查询同皮肤 | ✅ `var(--sci-bg-page)`；Hero 选择器扩产业页，未复制第二套色值 |
| D12 | lumen 不打 demo-* | ✅ 未改 `VITE_*` / nginx；不调 `demo-*` |
| SearchScaffold | 禁止为皮肤重写 | ✅ 未套 Scaffold，未改三模式/入篮 |
| D9 | 本单无新统计数字 | ✅ 推荐卡不挂伪 metric_id |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.49 |
| cost_warn | green |

口径：frontend-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`90000×0.8×3/1e6 + 90000×0.2×15/1e6 = 0.49`。单任务 <$5。

## 联调确认

皮肤与推荐接线已合入 `origin/dev`。视觉验收待 E0 镜像 rollout。本 agent **不**把任务标 `done`。
