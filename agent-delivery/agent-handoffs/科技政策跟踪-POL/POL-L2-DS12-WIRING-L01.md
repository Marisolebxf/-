# POL-L2-DS12-WIRING-L01 · 政策效果推演页接线 handoff

- 任务：`POL-L2-DS12-WIRING-L01`
- 日期：2026-11-06
- 认领/执行：`agent:frontend-agent`
- 监管：`human:淮政玮`
- 强度：ponytail full
- 仓：`repos/lumen-ui-science-pc`，分支 `dev`
- 本地提交：`de8bef7a8c9ad5122d424b46615c385841424b79`（未 push）
- ponytail：full（复用页内布局与 `request` 封装；只给当前可见且条件已齐的一种 kind 发请求）

`task-get` 未查到本任务。未改 `task-registry.yaml`，未把任务标 done。编排仓本文件不提交。

## 1. 范围

在已有政策效果推演页接线，不新开页面，不重做布局。唯一接口 `POST /display/v1/policy/simulation/jobs`，一次请求一个 `kind`。走 `src/utils/request.ts`（`optional: true`，`skipErrorToast`）。不新造 axios，不直连 Python，不直连 demo-*，不写死 Gateway。

HTTP 成功且 `data.records` 为空，或请求失败：区块空，不显示 501，不用 fixture 填这些区块。`USE_MOCK=true` 仍走原种子、公式和图表。`USE_MOCK=false` 这些区块不读种子填数。

页头四张统计卡、已有 ⓘ、`M_POLICY_LAYOUT_REC_COUNT` 未改。未改 D4，未把 mock 写成已上线，未删评审角标。`sharedCharts.ts` 未改，仍只服务 Mock 图表。

## 2. kind 与区块

条件闭集在 `src/views/policy/simulation/simulationLive.mjs`。行字段同时读 camel 与 snake。挂载时只请求当前可见且条件已齐的一种：效果预估默认子页签是多维评估（真轨打一次「多维评估」）；科技政策推演默认子页签是文本解析，政策编号为空，不发请求。切换子页签只重拉当前这一种。

| kind | 区块 | 条件 | 行字段 |
|---|---|---|---|
| 未出台仿真 | 效果预估 · 未出台政策仿真 | 政策类型 / 覆盖范围 / 支持力度 / 实施时间至少一项；四项都空不请求 | `econ_text`、`social_text`、`innovation_text`、`yearly_trend`、`explain_text` |
| 新出台预测 | 效果预估 · 新出台政策效果预测 | 必须 `policy_id` | `short_effect_text`、`long_effect_text`、`growth_text`、`industry_text`、`tech_effect_text`、`time_trend_text`、`space_feature_text`、`similar_basis_text` |
| 区域空间 | 效果预估 · 区域空间 | 必须 `region_name`；选了政策类型才带 `policy_type` | `gdp_text`、`industry_change_text`、`employment_text`、`spatial_items` |
| 多维评估 | 效果预估 · 多维评估 | 只传 `kind`，不传 `policy_id` | `dimension_name`、`score_value`、`score_text`；顺序跟服务端 |
| 利益攸关方 | 效果预估 · 利益攸关方 | 只传 `kind`，不传 `policy_id` | `actor_role`、`channel_name`、`opinion_text`、`opinion_at`。本页提交只留在浏览器，不写入接口 |
| 文本解析 | 科技政策推演 · 文本智能解析 | 必须 `policy_id` | `title`、`summary`、`auto_tags`、`structured_elements`。展示时去掉 `clauses` / `clause_meta` |
| 重点可视化 | 科技政策推演 · 政策重点可视化 | 必须 `policy_id` | `group_name`、`item_title`、`detail_text` |
| 影响范围 | 科技政策推演 · 影响范围分析 | 必须 `policy_id` | `impact_kind`、`impact_name`、`impact_text`、`time_change_text`、`region_text` |
| 路径预测 | 科技政策推演 · 实施路径预测 | 必须 `policy_id` | `stage_name`、`schedule_text`、`owner_name`、`stage_text` |
| 解读报告 | 科技政策推演 · 解读报告 | 必须 `policy_id` | 只展示 `section_name`、`body_text`。真轨不下载 PDF / Word / 文件 |
| 政策关联（240） | 科技政策推演 · 政策关联分析 | 不打 `simulation/jobs`；真轨 `GET /display/v1/policy/simulation/relation-graph?policy_id=`（须选政策后点「分析关联」） | 网络图 + 协同/体系说明。空图业务文案「暂无政策关联网络」。Mock 轨仍用原 ECharts force |
| 布局推荐 | 不接入 | — | 不拿来填推演区块 |

## 3. 改动文件

`lumen-ui-science-pc` @ `de8bef7`：

- 新增 `src/api/policySimulation.ts`
- 新增 `src/views/policy/simulation/simulationLive.mjs`
- 新增 `src/views/policy/simulation/simulationLive.test.mjs`
- 改 `src/views/policy/simulation/index.vue`（去掉挂载时的 dataset 占位请求）
- 改 `src/views/policy/simulation/estimate/EstimateWorkbench.vue`
- 改 `src/views/policy/simulation/interpret/InterpretWorkbench.vue`

未改 `sharedCharts.ts`、`package.json`、`vite.config`、`pnpm-workspace.yaml`。

## 4. 自检

- `node src/views/policy/simulation/simulationLive.test.mjs`：通过
- `node src/views/policy/simulation/FE-POL-03A.test.mjs`：41 项通过（页上现成的 policyWorkbench 结构自检）
- `vue-tsc --build`：通过（exit 0）
- 直接 `pnpm type-check` 被仓内已有 `pnpm-workspace.yaml`（只有 `allowBuilds`，没有 `packages`）拦住，报 `packages field missing`，脚本没启动。同一脚本用 `pnpm run --ignore-workspace type-check` 跑通。未改该文件。
- 未在浏览器点真轨。真轨要 `USE_MOCK=false` 且 Gateway 上有该接口；本机未起页面。

## 5. Git

- 只提交上述 6 个文件。message 含 `[agent:frontend-agent]`。
- 工作区在提交后干净。分支 `dev` 相对 `origin/dev` 为 ahead 1（另有提交前已存在的 behind，未 pull、未 push）。
- 执行会话当时没有 `git push`。

## 总控推送

2026-11-06 三仓都落地后推 `lumen-ui-science-pc` `origin/dev`。提交 `de8bef7a8c9ad5122d424b46615c385841424b79` 已在远端。真轨浏览器未点。gapfill 表未灌库，接口空列表会显示空态。

## 6. 真轨浏览器核对（2026-11-06，frontend-agent）

监管 `human:淮政玮`。未新建任务，未改 `task-registry.yaml`，未把任务标 done。未 push。编排仓本文件不提交。

本地页：`http://127.0.0.1:3000/policy/policy-effect-simulation`。`.env.development` 已是 `VITE_APP_USE_MOCK=false`（另在启动进程里设了同名环境变量）。未改 `package.json`、`vite.config`、`pnpm-workspace.yaml`。启动命令 `pnpm run --ignore-workspace dev`。

### 代码

只改了一处违反「真轨不读 fixture」的点：`InterpretWorkbench.vue` 政策重点的节点说明。`USE_MOCK=false` 时初值不再取 `policyFocusMindData`，点击节点也不再回退种子 `focusDetails`。Mock 轨仍用种子。

本地提交：`ffc80d550496a7290c6d388e3800aa44592dd987`（`dev`，未 push）。其余接线仍是 `de8bef7`。`node src/views/policy/simulation/simulationLive.test.mjs` 在这次改动前通过；这次只动 Vue 初值，未改条件闭集。

页头四张统计卡仍是原写死数字（86.5 / 78 / 7 节点 / 3 条），不走 `simulation/jobs`，也没有拿布局推荐去填下面的推演区块。未改页头。

### 浏览器请求

网关对当前 mock 登录回了 HTTP 401（`访问令牌不存在`）。页面收成空态，正文没有「501」，也没有「利益低关方」。区域页没有出现「全国」。

刷新后、还没点任何子页签：`simulation/jobs` 只有 1 次，画面停在「多维度效果评估 / 没有多维评估行」。这一次的请求体没挂上页内拦截（文档起始脚本没进页面世界）。随后点回该子页签，抓到的是 `POST {"kind":"多维评估"}`。

| 操作 | jobs |
|---|---|
| 未出台，四参都空 | 不请求。文案「四类参数都空，未发起仿真」 |
| 未出台，只填政策类型「研发补助」 | `{"kind":"未出台仿真","policy_type":"研发补助"}` |
| 新出台，政策编号空 | 不请求 |
| 新出台，编号 `18363390` | `{"kind":"新出台预测","policy_id":"18363390"}` |
| 区域，区域名为空 | 不请求 |
| 区域，只填「广东省」 | `{"kind":"区域空间","region_name":"广东省"}`，无 `policy_type` |
| 区域，再填政策类型「人才引进」 | 同上并带 `policy_type` |
| 多维评估 | `{"kind":"多维评估"}` |
| 利益攸关方 | `{"kind":"利益攸关方"}` |
| 提交一条意见 | 没有任何 `/api/` 请求。提示「意见留在本页，未写入接口」 |
| 切到科技政策推演，编号空 | 不请求。文案「未选择政策文本，不可解析」 |
| 填编号后：文本解析 / 重点可视化 / 影响范围 / 路径预测 / 解读报告 | 各 1 次，body 只有 `kind` + `policy_id` |
| 政策关联 | 须 `policy_id`；请求 `GET .../simulation/relation-graph`。空图文案「暂无政策关联网络」。不见 `simulation/jobs`、不见浏览器直打 `/topic` |
| 解读报告 | 无「下载」 |

`?review=1` 再开一次：页上 3 个「查看指标」按钮（含 `M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_LAYOUT_REC_COUNT`），5 处「演示数据」角标，jobs 仍是挂载 1 次。角标组件还在，只是默认评审关时不进 DOM。

### 未能在浏览器里核对

- 没有 HTTP 200 且 `records: []` 的响应。看到的是 401 被收成空态，不是成功空列表。
- 没有解析行，所以页面上没能看到去掉 `clauses` / `clause_meta` 后整行还在。这条只由 `simulationLive.test.mjs` 的 `elementEntries` 断言覆盖。
- 没有重点行，所以改过的节点说明在有数据时是否只显示接口 `detail`，浏览器没点到。
- 利益攸关反馈这张页头卡没有 metric_id，评审态也没有 ⓘ。这是原卡片，本次没加也没删。
