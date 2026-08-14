# LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01 · 产业查询推荐卡去掉 result-card 网格

> 格式参考 `templates/handoff-template.md`；视觉对照 `templates/fe-replica-visual-dod.md`。  
> **不做**：重写 SearchScaffold / 三模式 / 入篮；改 Java/Python；给推荐卡再叠第三套 layout class；标 `done`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已 claimed + in_progress；长任务总控授权无人值守。本单为 bugfix 视觉补单，**不标 done**，evidence 交 coordinator 收。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。最短路径：推荐 `article` 去掉互斥 `industry-search-result-card`；lumen 无 `search-content-card`，边框 token 补在 `.industry-search-recommendation-card`。未重写 SearchScaffold。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 厚包 / Demo `IndustrySearchPage.tsx` ~956 / 本仓 CSS 精读，禁止 compress 代替。 |

## 问题清单

- 推荐 `article` 同时挂 `industry-search-recommendation-card`（flex 横排）与 `industry-search-result-card`（`grid-template-columns: 24px minmax(0,1fr) auto`）。
- 后者写在 CSS 后覆盖 flex；推荐卡仅 2 子节点 → 主文进 24px 第一列一字一换行，操作钮进第二列漂在空白。

## 修改内容

1. **推荐 `article`**：只保留 `industry-search-recommendation-card`。检索结果 `article` 仍用 `industry-search-result-card`（勾选列网格未动）。
2. **边框**：lumen 没有 Demo 的 `search-content-card`。在 `.industry-search-recommendation-card` 补 `border` / `border-radius: var(--sci-radius-card)` / `background: var(--sci-surface-solid)`；显式 `flex-direction: row`；`recommendation-main` 已是 `flex: 1; min-width: 0`；摘要 `white-space: normal`。**未**复制结果卡 grid。
3. **自检**：`industrySearchModel.selfcheck.mjs` 切片 `v-if="!searched"` 到 `v-else-if="matches.length === 0"`，断言含 `recommendation-card` 且不含 `result-card`。

## 复刻验收 V1–V7（`fe-replica-visual-dod.md`）

| # | 项 | 结果 |
|---|---|---|
| V1 | 页底 `var(--sci-bg-page)` / `#D8E7FC` | ✅ 本单未改页底；SEARCH-SKIN 已铺，仍在 |
| V2 | 检索 Hub Hero 与本仓企业查询同皮肤 | ✅ 本单未改 Hero；SEARCH-SKIN 选择器仍在 |
| V3 | 卡片内部：标题+摘要横向书写；操作在右侧 | ✅ 宽屏 flex-row：左 `recommendation-main`、右 `recommendation-actions`；摘要 `white-space: normal`，不再进 24px 列 |
| V4 | 一个节点一套 layout | ✅ 推荐 `article` 不再叠 `industry-search-result-card`；Demo 真源只有 `search-content-card` + `recommendation-card` |
| V5 | `min-width: 0` 只加在需截断的 flex 子项 | ✅ 在 `recommendation-main` / 标题按钮 / 摘要；内容列是 `flex:1` 不是 24px |
| V6 | 推荐空态诚实；有数则横卡 | ✅ `recommendations.length === 0` → `a-empty`「暂无推荐产业」；有数则 `article` 横排（`max-width: 1490px` 才变列，与 Demo 一致） |
| V7 | 推荐模板不得同时含 `result-card` | ✅ 自检切片 `!searched` 断言通过 |

## 测试结果

| 命令 | 结果 |
|---|---|
| `node src/utils/industrySearchModel.selfcheck.mjs` | ✅ `industrySearchModel.selfcheck ok` |
| `npx eslint` 本单 Vue + selfcheck | ✅ 0 error |
| `npm run type-check`（`vue-tsc --build`） | ✅ exit 0 |

## 遗留风险

- K8s 上仍是旧前端镜像，**需要 devops 再跑 E0 rollout** 后才能在 http://192.168.88.50:30892 看到横排推荐卡。
- 窄屏 `max-width: 1490px` 推荐卡改为 `flex-direction: column`（Demo 同断点），不是竖排字。

## 是否需要 devops 再跑 E0 rollout

**需要。** 本单已 push `lumen-ui-topic` `origin/dev`；集群要吃到推荐卡横排必须重建并滚动前端镜像。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`（禁止 main、禁止 force）
- commit：`1064c038eca1c13aa8a89da3b1510a95c8d793b1`
- 标题：`fix(chain): 推荐卡去掉 result-card 网格恢复横排 [agent:frontend-agent]`
- push：✅ `origin/dev`（`ee3ff6f..1064c03`）
- pipeline URL / ID：push 后 GitLab `frontend:build` 待跑；本机未取 pipeline ID
- 部署 namespace / 镜像 tag：待 E0
- K8s rollout：本单不跑；**需 E0**
- dev 测试 URL：http://192.168.88.50:30892 （rollout 后）

## 可观测性（建议）

- 请求头：沿用既有 `X-Trace-Id` / `traceparent`（本单未改 `request.ts`）
- 本单无新埋点（class/CSS/自检）

## 涉及文件

相对 `lumen-ui-topic/`：

- `src/views/industry-center/IndustrySearchPage.vue`
- `src/views/industry-center/industrySearch.css`
- `src/utils/industrySearchModel.selfcheck.mjs`

本 handoff：`agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-FE-SEARCH-LAYOUT-L01.md`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 调用链 | 只调 Java REST | ✅ 未改 API |
| Python | 禁止直连 | ✅ 未直连 Python / ES / MySQL / Nebula |
| D8 | token 边框/圆角 | ✅ `var(--sci-content-border)` / `--sci-radius-card` / `--sci-surface-solid`；未硬编码新色 |
| D12 | lumen 不打 demo-* | ✅ 未改 `VITE_*` / nginx |
| SearchScaffold | 禁止为布局重写 | ✅ 未套 Scaffold，未改三模式/入篮 |
| D9 | 本单无新统计数字 | ✅ 推荐卡不挂伪 metric_id |
| 复刻布局 | `fe-replica-visual-dod.md` | ✅ V1–V7 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.26 |
| cost_warn | green |

口径：frontend-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`48000×0.8×3/1e6 + 48000×0.2×15/1e6 = 0.26`。单任务 <$5。

## 联调确认

推荐卡 class 冲突已合入 `origin/dev`。视觉验收待 E0 镜像 rollout。本 agent **不**把任务标 `done`。
