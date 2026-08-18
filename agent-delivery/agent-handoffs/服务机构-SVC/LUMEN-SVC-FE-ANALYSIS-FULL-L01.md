# LUMEN-SVC-FE-ANALYSIS-FULL-L01 · SVC Gate-1：分析/生态/招引有数（非空壳）

> 日期：2026-08-18  
> Task：`LUMEN-SVC-FE-ANALYSIS-FULL-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md` / Gate-1（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 `useSvcAnalysisJob` + `IndustryAnalysisProcessShell`；扩八叶子白名单接线；不新增依赖；Q-SVC-010 诚实空 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本会话未挂载 headroom MCP |

## 范围与实现

### Before → After

| 工作区 | Before | After |
|--------|--------|-------|
| 机构三视图 | stub Message「未入白名单」 | Create `org_coverage` / `org_trend` / `tech_power` → 过程壳 → 显式结果 |
| 生态 | 仅 shortboard 可跑；graph/shenzhen stub | `shortboard` / `graph` / `shenzhen` 均可 Create |
| 招引/培育 | 本地空壳「生成」 | `attract` / `cultivate` Create + 名单回填或诚实空 |

### analysisType 对齐 Java（8）

| analysisType | analysis_key | 页面 |
|--------------|--------------|------|
| `svc:analysis:org_coverage` | `svcan.org_coverage.v0` | `/service/institution-judgment?workspace=field` |
| `svc:analysis:org_trend` | `svcan.org_trend.v0` | `workspace=trend` |
| `svc:analysis:tech_power` | `svcan.tech_power.v0` | `workspace=capability` |
| `svc:analysis:shortboard` | `svcan.shortboard.v0` | `/service/chain-analysis?workspace=chain` |
| `svc:analysis:graph` | `svcan.graph.v0` | `workspace=graph` |
| `svc:analysis:shenzhen` | `svcan.shenzhen.v0` | `workspace=shenzhen` |
| `svc:analysis:attract` | `svcan.attract.v0` | `/service/institution-decision?workspace=attract` |
| `svc:analysis:cultivate` | `svcan.cultivate.v0` | `workspace=cultivate` |

- API：只调 Java `analysisTaskCreate/Detail/Result/List/Stream`（`/topicAsync/topic/v1/**`）；门户查询仍 `/svc/topic/v1/**`（D12，禁 demo-*）
- wait_view：`page_mode_hint=process_succeeded_wait_view`；须点「查看分析结果」
- 结果：读 `targetParams.result_payload`；空/mock/Q-SVC-010 诚实提示，不伪 KPI
- 系统任务浮层：`buildAnalysisTaskRoute` 按类型跳回对应 workspace

## 偏离说明

- 图谱 ADS 无快照时结果诚实空（algo 已约定）；UI 展示 note，不画假边
- 技术力雷达仅为骨架；正式分在排名表
- 与并行叶 `LUMEN-SVC-FE-PORTAL-FULL-L01` 同仓；本叶未改 portal 文件

## 产物清单

| 产物 | 路径 |
|------|------|
| FE commit | `repos/lumen-ui-topic` `d5dab10`（push 后以 `git log -1` 为准） |
| 类型白名单 | `src/api/enterprise/types/analysisTask.ts` · `src/config/svcWorkspace.ts` |
| Job 组合 | `useSvcAnalysisJob.ts` · `svcAnalysisTask.ts` · `analysisTaskRoutes.ts` |
| 页面 | `ServiceOrgAnalysisPage` / `ServiceChainAnalysisPage` / `ServiceRecommendPage` |
| 自检 | `svcAnalysisTask.selfcheck.mjs` · `svcWorkspaceVisual.selfcheck.mjs` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ANALYSIS-FULL-L01.md` |

## 验收证据

- [x] 八叶子 FE 类型与 Java 白名单一致
- [x] 三视图 / 生态三页 / 招引培育可配置并 Submit Job
- [x] wait_view + 结果或诚实 Job/空态
- [x] `node src/utils/svcAnalysisTask.selfcheck.mjs` 绿
- [x] `node src/utils/svcWorkspaceVisual.selfcheck.mjs` 绿
- [x] `npm run type-check` 绿
- [ ] K8s 已发布冒烟（外网 http://111.198.38.90:50892/ · 待 ui-topic deploy）

## Smoke 笔记（本机/已发布）

1. 打开机构领域分析 → 对比篮选机构 →「开始分析」→ 应进过程页（或 success wait_view）→「查看分析结果」→ 表或诚实空 + Q-SVC-010
2. 短板 / 图谱 / 深圳：各自 workspace「开始分析」同路径
3. 招引/培育：「生成名单」→ 过程 → 结果名单或诚实空
4. 非法/失败：过程壳展示 failed/cancelled，不伪造终态 KPI
5. D12：Network 仅 gateway Java，无 demo-* NodePort

## CI/CD

- 分支：`dev`
- commit：`d5dab10`（push 后确认）
- pipeline：push `origin/dev` 触发；若 ui-topic deploy 为 manual，需人工点
- 外网：http://111.198.38.90:50892/

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python；不直连算法 | ✅ |
| D8 | Design/Arco 既有壳复用 | ✅ |
| D9 | 指标角标 + Q-SVC-010 | ✅ |
| D10 | 过程/结果状态机 wait_view | ✅ |
| D12 | 禁 demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~8 万 |
| actual_cost | 估 <$5 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：FE 八叶子 Create 键与 Java/Python 对齐；结果诚实消费。待部署后外网冒烟。下一叶：`LUMEN-SVC-E-FULL-SMOKE-L01`。
