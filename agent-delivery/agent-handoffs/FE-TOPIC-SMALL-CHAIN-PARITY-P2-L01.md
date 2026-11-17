# Handoff · FE-TOPIC-SMALL-CHAIN-PARITY-P2-L01

- **任务**：专题小屏·产业分析差单 P2（查询分页 / trace 深链 / 记录分页 / Overview 地图 / 评审层裁定）
- **仓库**：`repos/lumen-ui-topic-mobile`（origin/dev）
- **监管**：human:孔东 · **执行**：agent:frontend-agent
- **状态**：implementation 完成，自检三绿
- **ponytail:** full —— observability 深链函数从 PC 对齐移植（~60 行）；van-list 复用 vant 原生组件；零新依赖

## 范围与实现（对照 DoD 六项）

### ① 产业查询分页
- `IndustrySearchView.vue`：结果区改 `van-list` on-load 懒加载（每批 10 条本地分页——`industrySearch` API 无 offset 参数，PC 亦为全量+前端分页，语义一致）；total 提示保留（「共 N 个对象」）

### ② 失败态 trace 深链
- `src/utils/observability.ts`：补 `buildTempoExploreUrl` / `buildLokiExploreUrl`（对齐 PC 实现；`VITE_GRAFANA_BASE_URL`/`VITE_GRAFANA_TEMPO_DS`/`VITE_GRAFANA_LOKI_DS` 未配置返回 null 优雅降级）
- `ChainTraceLinks.vue`（新，~40 行）：traceId 文本 + Tempo/Loki 外链，未配置时只显文本
- `ChainAnalysisShell.vue`：失败不再静默弹回 config——running 态留存失败区块（错误信息 + ChainTraceLinks + 「返回条件重试」）；`taskTraceIdOf` 从任务实体/targetParams 提取 traceId（对齐 PC taskTraceId）

### ③ 记录分页
- 诊断/区域/深圳三页记录区：`size=20` 一次性拉取 → `van-list` 加载更多（`recordsPage` 递增调 `analysisTaskList`，`rows < 20` 判 finished）；tab 切换重置页码

### ④ Overview 区域分布地图形态
- `IndustryOverviewView.vue`：区域分布加 map/list `van-tag` 切换；地图复用 P1 `RegionalCompareMap`（点 = regionPoints 经 `resolveRegionalGeo` 定位，score 取企业数/机构数；无可定位点时地图入口置灰）

### ⑤ 评审层裁定（书面结论）
**裁定：mobile 小屏不引入 `IndustryReviewMount` / `IndustryReviewOnly` 组件树，维持现有轻量 review 层（`review/config.ts` + `MetricMarker.vue` + `readiness.generated.ts`）。**

理由：
1. **D9 核心链路已全覆盖**：mobile `MetricMarker` 弹卡完整承载 8 件套 + 就绪度四行（D1-D4）+ SchemaGap/Pending/Mock/Ingesting 全家族角标，语义与 PC `MetricSpecCard`+`ReviewMetricBadges` 等价，且 `reviewMode` 门控一致（`VITE_REVIEW_MODE !== 'false'`）
2. **IndustryReviewMount 的 kind/refs 挂载是 PC 评审现场的需求追溯 UI**（约 15 处 requirement_trace/pending_badge 引用），属 PC 端评审工作台产物；小屏复刻规划（系统-06 §4）明确小屏裁剪评审工作台交互
3. **组件自闸已满足**：mobile 角标组件自身判断可见性（StatCard 内 `v-if="reviewMode"`），关闭评审模式 DOM 零泄漏的验收口径不受影响
4. 上线清理随 `src/review/` 既有清单一并执行

**本裁定需 human:孔东 认可；若需补齐 PC 全量挂载，另开差单。**

### ⑥ 工程自检
- `pnpm type-check` ✅ · `pnpm test` 72/72 ✅ · `pnpm build` ✅（13.96s）

## 防漏扫描摘要（附录 D）

- **D.1 页面差集**：本单 5 子项全落 DoD；P1 遗留热力图条款已在 P1 handoff 声明不适用（PC 同名组件亦无热力层）
- **D.2 本地 KPI 接线**：本单未新增统计位；Overview 地图 score 复用 regionPoints 既有数据（企业数/机构数），非新指标
- **D.3 镜像 vs 矩阵**：无新 metric 镜像
- **D.4 错挂/正名**：无
- **D.5 契约防漏**：observability 深链纯前端构建（读 VITE_ 环境变量），无后端契约变更；记录分页沿用既有 `analysisTaskList` page/size 参数

## 产物

- commit：`[agent:frontend-agent] FE-TOPIC-SMALL-CHAIN-PARITY-P2-L01 …`（lumen-ui-topic-mobile origin/dev）
- CI：push 后自动触发

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 可观测铁律（公约 §2.4） | ✅ 失败态 trace 深链闭合（本单主目标） |
| D9 指标入口 | ✅ 未破坏既有 MetricMarker 链路 |
| D12 | ✅ 只读对照 PC 重写 |
| I2-12 | ✅ Shell 闸门未动，仅失败展示增强 |
