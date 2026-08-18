# LUMEN-CHAIN-FE-GAP-A01 · 产业链差距修复 A — Mock-off 查询与对比篮

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
| 说明 | 复用 Java catalog、系统对比篮与现有查询状态，不新增依赖或平行状态；未跳过 D8/D9/D10、可观测及诚实空约束。 |

## 范围与实现

- GAP-01：生产查询页及配置层不再静态引用 `@/mock/**` / `industrySearchFixture`；推荐、热词、父级及领域选项统一从 Java catalog 派生，空 catalog 保持空。
- GAP-08：移除查询页平行对比抽屉，复用系统对比篮及 `open_compare_basket=1` 查询协议；补齐批量入篮失败反馈。
- GAP-17：补可执行 catalog 派生与查询状态纯函数自检，并收紧模板事件接线扫描。
- GAP-21：补 `data-frame-id`、`data-search-state`、权限及键盘语义；错误、加载、推荐、空、权限和结果状态互斥。

## 偏离说明

- Java catalog 缺少推荐、父级或领域数据时不使用本地 fixture 补数，界面按真实响应显示空态。
- 本单不新增接口、不修改视觉体系、不触碰用户本地 `.env.development`。

## 测试结果

- `node src/views/industry-center/industryReplicaFix.selfcheck.mjs`：通过。
- `node src/utils/industrySearchModel.selfcheck.mjs`：通过。
- `npm run type-check`：通过。
- `npm run build`：通过；仅有既存 VueUse 注释与大 chunk 警告。
- 独立任务复审：规范 `PASS`，质量 `APPROVED`，无 Critical / Important / Minor。

## 五维复刻检查

- V1 查询首屏：✅ 保留 SearchHub、推荐与结果布局。
- V2 查询交互：✅ 示例、筛选、搜索与系统对比篮链路完整。
- V3 查询状态：✅ loading/error/recommendation/empty/permission/result 互斥。
- V4 查询样式：✅ 未另起 UI 或修改既有 token。
- V5 评审层：✅ 未绕过 `@/review`。
- V6 Mock 开关：✅ Mock-off 无 fixture 回填。
- V7 可访问性：✅ frame/search-state、键盘和权限语义齐。
- R1–R5：N/A，本单未修改分析结果工作区；既有结果布局、交互、样式、评审与 Mock 门控保持不变。

## 附录 D 防漏扫描摘要

- D.1 页面差集：查询页生产路径已扫描，未发现 `@/mock` / fixture 静态引用。
- D.2 本地 KPI 接线：本单未新增统计数字。
- D.3 镜像 vs 矩阵：本单未修改 metric readiness 镜像。
- D.4 错挂/正名：本单未新增 metric_id。
- D.5 契约防漏：catalog 空响应、系统对比篮事件、查询状态与 A11y 均有 selfcheck。

## CI/CD

- 分支：`lumen-ui-topic` `dev`
- commit：`f8048a2`（`fix(chain): close FE GAP Pack A–D for industry center [agent:frontend-agent]`；与 B/C/D 同提交）
- pipeline URL / ID：push `origin/dev` 后由 GitLab CI 触发（本 handoff 落盘时待跑）
- K8s rollout：随 CI 自动部署（待 pipeline）
- 本地证据：`industryReplicaFix` / `industrySearchModel` selfcheck、type-check、build 均通过

## 可观测性

- 沿用请求层 `X-Trace-Id` 与既有 Java catalog 调用；本单未新增直连或观测旁路。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 前端未实现算法 |
| FE → Java 调用链 | ✅ 仅消费现有 Java catalog |
| Nebula | ✅ 前端不直连 |
| 可观测性 | ✅ 沿用现有 trace 注入 |
| CI/CD | ✅ 已 commit `f8048a2` 并 push `origin/dev`；pipeline/K8s 由 CI 接管 |
| demo/lumen 隔离 | ✅ 未 merge demo，未调用 demo 服务 |
| D8 / D9 / D10 | ✅ 未改视觉体系；未新增指标；状态与键盘语义已补齐 |
| D12 | ✅ 无 demo 服务地址 |

## 涉及文件

- `src/config/industrySearchCatalog.js`
- `src/config/industrySearchConfig.ts`
- `src/utils/industrySearchModel.selfcheck.mjs`
- `src/views/industry-center/IndustrySearchPage.vue`
- `src/views/industry-center/industryReplicaFix.selfcheck.mjs`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000（会话估计，含实现、两轮修正与独立复审） |
| model_used | `gpt-5.6-sol` |
| actual_cost | 待账单核对（估算低于 $5） |
| cost_warn | `green` |

## 遗留风险

- catalog 数据质量不足时推荐与筛选项会为空；这是 Mock-off 诚实行为，需要 Java 数据侧补齐，而非前端 fixture 兜底。
