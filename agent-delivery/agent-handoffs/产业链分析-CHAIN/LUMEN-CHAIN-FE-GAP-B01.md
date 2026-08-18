# LUMEN-CHAIN-FE-GAP-B01 · 产业链差距修复 B — 路由、对象上下文与权重合并

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
| 说明 | 复用 compareBasketPicker、任务路由构造器和本地权重元数据；未虚构权重 API；未跳过 D8/D9/D10 与诚实空。 |

## 范围与实现

- GAP-02：诊断 / 区域 / 深圳复用 `readCompareBasketPickerSelection` 读取 `object_ids[]`。
- GAP-09：`mergeIndustryWorkspaceWeights` 只覆盖已登记 key；非法权重回退本地默认。
- GAP-10 / 11：补 `/industry-center`、`results/:resultId`、`reports/:reportId`；legacy view 归一化；深链先过 overview 路由权限，再按工作区 perm 校验，不预取结果资产。
- GAP-18 / 19：错误与 traceId 持久展示；记录页查看结果 / 复制配置 / 查看报告。复制仅在清洗后仍有业务参数时启用。
- GAP-24：周期无效数值保持 `null`。
- 产业链报告入口：成功结果可经 SystemReportReader 阅读；企业非 chain 结果不会仅因有资产就被当成报告。

## 偏离说明

- 本轮无真实权重 API，默认使用本地 metadata。
- 深链路经权限使用 `MENU_CHAIN_OVERVIEW`，落地工作区再校验 diagnosis / regional / shenzhen / panorama。

## 测试结果

- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs`：通过。
- `node src/utils/industryChainTask.selfcheck.mjs`：通过。
- `npm run type-check`：通过。
- `npm run build`：通过。

## 五维复刻检查

- V1–V7：查询页本单未回退 Pack A 契约。
- R1 工作区布局：✅ 诊断/区域/深圳对象上下文恢复。
- R2 工作区交互：✅ 记录三操作与深链。
- R3 工作区样式：✅ 未另起视觉。
- R4 评审：✅ 未绕过 `@/review`。
- R5 Mock 开关：✅ 无 fixture 填数。
- W1–W3：✅ 过程错误可追溯；结果/报告视图语义分离。

## 附录 D

- 本单未新增伪造指标 8 件套；未登记指标仍走 D1 missing。
- 契约：多值 object_ids、权重合并、view 归一化、报告判定、资产 5xx 不吞，均有可执行 selfcheck。

## CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：`f8048a2`（与 A/C/D 同提交）
- pipeline / K8s：push `origin/dev` 后由 GitLab CI 触发

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| FE → Java | ✅ |
| D12 | ✅ |
| D8 / D9 / D10 | ✅ |
| 可观测 | ✅ 错误保留 message + traceId |
| CI | ✅ 已 commit `f8048a2` 并 push `origin/dev` |

## 涉及文件

- `src/config/compareBasketPicker.ts`
- `src/config/industryWorkspace.ts`
- `src/utils/industryWorkspaceRuntime.js`
- `src/router/menu.ts`
- `src/composables/analysisTaskRoutes.ts`
- `src/composables/useIndustryAnalysisJob.ts`
- `src/views/industry-center/IndustryTaskDeepLink.vue`
- `src/views/industry-center/IndustryDiagnosisPage.vue`
- `src/views/industry-center/IndustryRegionalPage.vue`
- `src/views/industry-center/IndustryShenzhenPage.vue`
- `src/utils/industryChainTask.ts`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 160000（会话估计，含审查修正） |
| model_used | `gpt-5.6-sol` |
| actual_cost | 待账单核对（估算低于 $10） |
| cost_warn | `green` |
