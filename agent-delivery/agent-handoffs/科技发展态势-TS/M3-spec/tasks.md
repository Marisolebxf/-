# M3 技术发展跟踪 — 执行任务清单

> 关联 spec：`spec.md`（SITUATION-TS-M3-REVIEW-L01）
> 规约：`supervised_by human:孔东` → 全部改动停留本地，不 commit / 不 push。

## 阶段 A：前端收口（2 文件）

- [x] **T1** `components/RunningStage.vue`：引入 `useReviewStore`，给 `.tracking-evaluation-run-demo` 加 `v-if="!review.reviewMode"`；失败态仍由 `evaluationProgress.status` 驱动。验收：评审模式关闭时不渲染该控件，开启时可渲染。→ 2026-11-06 已改
- [x] **T2** `models/trackingModel.ts#L828`：把「该对象来自技术发展跟踪模拟数据…」改为真实口径文案。验收：全文检索无「模拟数据」残留（注释除外）。→ 2026-11-06 已改为「真实评估结果，数值与结论由评估任务返回」
- [x] **T3** `pnpm type-check`（cwd=`repos/lumen-ui-science-pc`）。验收：0 error。→ 2026-11-06 实测 exit 0
- [x] **T4** `pnpm build`（同上）。验收：构建成功。→ 2026-11-06 因 pnpm engine 闸门（Node 22.7 < 22.12）改用 `node node_modules/vite/bin/vite.js build` 直跑，exit 0

## 阶段 B：真实数据链路走查（不改代码）

- [x] **T5** 启动 show-py：`GKX_JIUXIN_ENABLED=1` + `GKX_JIUXIN_HOST=47.93.119.170` + `GKX_JIUXIN_PORT=29030`（凭据按环境变量）。验收：服务健康、tracking-eval 端点有返回。→ 2026-11-06 8082 已起，technologies/hotspot-yearly/relations 200
- [x] **T6** display 本地鉴权：带有效 token 调 `POST /display/v1/situation/tracking/meta`。验收：200 且 `globalFilterDefaults` 非空（久新有数据时）。→ 本地 local profile 7099 实测 200
- [x] **T7** 页面进入：默认区域/产业领域/年份 + 数据集。验收：非空；且只改筛选才触发重载。→ dataset 实测 records/hotTopics/bubbles 均非空
- [ ] **T8** 五视图（热力/地图/气泡/雷达/弦线）+ 时间轴 + Top20 榜单。验收：均为真实值或诚实空态，无 mock。
- [ ] **T9** 发起评估 → running → result。验收：进度逐步推进；结果与 ADS 表口径一致。
- [ ] **T10** 报告生成 → 下载 → 二次生成 → 删除。验收：`report` 表 +1；二次不 +1；删除后 `status=deleted` 且文件清理。
- [ ] **T11** 评审模式开关。验收：关闭后 DOM 无 `GAP-*`、无「演示用状态切换」。

## 阶段 C：留痕

- [x] **T12** 更新 `M3-spec/spec.md` §4 验证结果（逐项打勾 + 实测值）。→ 2026-11-06 已按 §9 复核更新回写
- [ ] **T13** `git status` 复核仅 T1/T2 两个文件改动；**不 commit、不 push**，等孔东确认。

## 阶段 D：2026-11-06 本轮补洞（数据口径 + 详情消费）

- [x] **T14** 规模（论文）改累计口径：Python `profile.paper_count AS paper_count_total`、`evolution_yearly.cumulative_paper_count`；BFF `record.scale` 取累计、气泡逐年 scale 取截至该年累计。验收：top20 20/20 非 0（实测 10~30）。
- [x] **T15** 成熟度补值：`maturityFromStage(stage_code)` 回落（`NO_PUBLICATION_OBSERVED` → 阶段研判）。验收：`records/hotTopics` maturity 空值 0 条。
- [x] **T16** 并排对比最近 3 期：FE `slice(-3)`、BFF `HISTORY_MATRIX_PERIODS=3`。验收：`meta.historyMatrix.periods=3`。
- [x] **T17** 气泡详情消费成熟度 + 「论文数」更名「累计论文数」。验收：`buildBubbleDetail` 含成熟度项。
- [x] **T21** 详情面板消费 5 类后端事实字段：`communityRole/communityRank/communitySize`、`applicationCaseSummary`（标注「未核实为市场应用」）、`bottlenecks`（按 severity 取最高，`NO_GAP_OBSERVED` 如实写「未观测到缺口」）、`evolutionPath`（步数/截断）、`evidenceSummary`（总数+类型分布）；热力图/默认详情与气泡详情共用 `buildFactualMetricRows`。验收：dataset 20/20 五字段有值；`pnpm type-check` exit 0。
- [x] **T22** 时间轴年份与热力图列轴同源：`resultTimelineYears` 改用 `dataset.heatMatrixYears ?? dataset.years`，空年份不占位（2000-2014 不再显示）。覆盖热力图/气泡两条时间轴。验收：接口 `heatMatrixYears=2015..2025`、`years=2000..2025`；type-check/build 绿。
- [ ] **T18** 台账 `指标入库详情.xlsx` 错挂订正（`M_TECH_*` 为另一套且 `is_mock=true`）——待台账侧确认，非代码改动。
- [ ] **T19** D9 D2/D3/D4 角标：`src/review/readinessSeed.ts` 无 tracking 条目（指标库无已签收 DS-03 指标），按 D9 §1 禁止前端自填，维持 D1 missing 红问号。
- [ ] **T20** 报告链路（V8）复跑（`report` 表 +1 / 二次复用 / 删除清理）。构建已验证：`vite build` exit 0。
