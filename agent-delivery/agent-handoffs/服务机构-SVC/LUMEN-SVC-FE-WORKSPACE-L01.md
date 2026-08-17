# LUMEN-SVC-FE-WORKSPACE-L01 · 产业服务链 D — 分析/生态/招引工作区

> 日期：2026-08-17  
> Task：`LUMEN-SVC-FE-WORKSPACE-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

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
| 说明 | 复用 CHAIN `IndustryAnalysisProcessShell` + Java `analysisTask*`；仅扩 `svc:analysis:shortboard`；其余工作区诚实空壳 |

## 范围与实现

- **菜单/路由**（对齐 demo Layout `service-*`）：
  - `/service/institution-judgment`（领域/趋势/技术力）→ `ServiceOrgAnalysisPage` 壳
  - `/service/chain-analysis`（短板/图谱/深圳/记录）→ `ServiceChainAnalysisPage`（短板可跑 Job）
  - `/service/institution-decision`（引入/培育）→ `ServiceRecommendPage` 壳
  - `/service/maintenance` → `ServiceMaintenancePage` 壳
- **短板任务**：`analysisType=svc:analysis:shortboard` → Java `/topicAsync/topic/v1/analysis/tasks`（与企业/产业链共用 API，**非** demo-*）
- **wait_view**：`page_mode_hint=process_succeeded_wait_view`；须显式「查看分析结果」；结果读 `targetParams.result_payload`
- **权限**：`MENU_SVC_ORG_ANALYSIS` / `MENU_SVC_CHAIN` / `MENU_SVC_RECOMMEND` / `MENU_SVC_MAINTENANCE`（L2/L4）
- **D9**：结果 KPI + 壳位挂 `ReviewMetricBadges` + `Q-SVC-010`；禁止伪造 KPI
- **自检**：`node src/utils/svcAnalysisTask.selfcheck.mjs`；`npm run type-check` 绿

## 偏离说明

- Java 白名单仅 shortboard；图谱/深圳/机构分析/推荐页为诚实空壳（告警 + 空态 + 待核验角标），不伪跑 Job。
- Mock 层同步模拟 Java `applySvcSyncResult`（success + wait_view + result_payload）。

## 产物清单

| 产物 | 路径 |
|------|------|
| FE commit | `repos/lumen-ui-topic` `99f19becfeae859d6dc749ad2ebdac3d7908dc9f` |
| 页面 | `src/views/service-center/Service{ChainAnalysis,OrgAnalysis,Recommend,Maintenance}Page.vue` |
| Job 组合 | `useSvcAnalysisJob.ts` · `svcAnalysisTask.ts` · `svcWorkspace.ts` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-WORKSPACE-L01.md` |

## 验收证据

- [x] 侧栏 WORKSPACE 菜单与 demo 路径对齐
- [x] 短板 Create/wait_view/result 接线 Java analysisTask
- [x] type-check + selfcheck 通过
- [ ] K8s 已发布冒烟（段 E）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| D12 | 只调 Java `/topicAsync` + ENTRY `/svc`；禁 demo-* | ✅ |
| 调用链 | FE → Java async → topic-py → algo；FE 不直连 Python | ✅ |
| D8/D10 | Arco + 复用过程壳 | ✅ |
| D9 | metric_id + Q-SVC-010 诚实空；不造假 KPI | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~9 万 |
| actual_cost | 估 <$5 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：短板任务经 Java analysisTask 可创建并进入 wait_view/结果壳；其余 WORKSPACE 页诚实空态可分享路由。下一叶：段 E 发布/金路径。
