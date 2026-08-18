# LUMEN-CHAIN-FE-GAP-D01 · 产业链差距修复 D — D9、评审、地图与可观测

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 地图复用 UnifiedLeafletMap；评审信息自闸；未另造点击埋点。 |

## 范围与实现

- GAP-03 / 13：Q/QC/GAP/Demo-B 进入 `@/review` / `IndustryReviewOnly`；配置页 Q056 文案已迁入评审层。
- GAP-04 / 14：未登记 `M_CHAIN_REG_*` / `M_CHAIN_SZ_*` 保持 D1 missing 红问号；已登记数值走 ReviewMetricBadges。
- GAP-15：`IndustryRegionMap` 迁移到 `UnifiedLeafletMap`；Tooltip 只显示地名，选中详情用 Vue + D9 角标。
- GAP-16：错误态展示 traceId，并在配置了 Grafana 时给出 Tempo/Loki 深链；request 错误响应也会打 trace 链。
- GAP-23：专题全景保持三 Tab；补 `F-OV-01/02/03`；区域筛选只消费 Java `regionPoints`。

## 偏离说明

- GAP-12 CMS 无接口，维护写侧与 CMS 介绍仍诚实空。
- GAP-04 未登记指标真源仍是上游开放项，前端不伪造 8 件套。

## 测试结果

- selfcheck / type-check / build 通过。
- e2e 规格已扩展专题三 Tab 与深链诚实空；本机未跑 Playwright 对 K8s。

## 五维复刻检查

- R4 评审零泄漏：✅ Demo-B / Q 编码进入自闸层。
- R5 Mock-off：✅ 地图不补 Demo 区级企业数。
- W1–W3：✅ 地图与概况筛选基于 Java 点位。

## 附录 D

- D.1 页面差集：专题三 Tab 保留，无第四业务 Tab。
- D.2 KPI 接线：选中区域统计走已登记 metric_id。
- D.4 未登记 ID 不伪造 meta。
- D.5 地图、评审、trace 深链有 selfcheck / 静态扫描。

## CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：`5dcc8ed`（与 A/B/C 同提交）
- pipeline / K8s：push `origin/dev` 后由 GitLab CI 触发

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 可观测 | ✅ X-Trace-Id + Tempo/Loki 深链 |
| D9 | ✅ 未登记 missing，已登记有 ⓘ |
| D12 | ✅ |
| CI | ✅ 已 commit `5dcc8ed` 并 push `origin/dev` |

## 涉及文件

- `src/components/map/UnifiedLeafletMap.vue`
- `src/components/industry-center/IndustryRegionMap.vue`
- `src/components/industry-center/IndustryTraceLinks.vue`
- `src/components/industry-center/IndustryRegionalResultBoard.vue`
- `src/views/industry-center/IndustryOverviewPage.vue`
- `src/utils/request.ts`
- `e2e/chain-gold.spec.ts`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000（会话估计） |
| model_used | `gpt-5.6-sol` |
| actual_cost | 待账单核对 |
| cost_warn | `green` |
