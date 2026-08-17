# LUMEN-SVC-FE-ENTRY-L01 · 产业服务链 D — 入口壳 + 门户/查询

> 日期：2026-08-17  
> Task：`LUMEN-SVC-FE-ENTRY-L01`  
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
| 说明 | 对齐 CHAIN ENTRY；只调 `/svc/topic/v1/**`；门户五 Tab 路由就位 |

## 范围与实现

- API：`src/api/svc/{paths,types,index}.ts` → gateway `/svc/topic/v1/service**` + `service-portal/**`
- 门户：`ServicePortalShell` + overview / industry-distribution / region-map / capability-rank / shenzhen
- 查询：`ServiceOrgSearchPage`（mode + 画像抽屉）
- 菜单/权限/图标：`menu.ts` · `MENU_SVC_PORTAL`/`SEARCH` L0 · `IconSafe`
- Mock：`src/mock/svc/svcApi.ts` + register；自检 `serviceOrgSearchModel.selfcheck.mjs`
- **非范围**：WORKSPACE 分析工作区（下一叶）

## 偏离说明

- Java 今日仅 overview+ranking；其余门户 Tab 读 overview 字段或诚实空态，不伪造 KPI。
- 查询页用轻量表单+表格（未整页搬 SearchHub），语义对齐 demo mode/shareable URL。

## 产物清单

| 产物 | 路径 |
|------|------|
| FE | `repos/lumen-ui-topic/src/api/svc/**` · `views/service-portal/**` · `views/service-center/**` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ENTRY-L01.md` |

## 验收证据

- [x] 路由与 Java 路径接线
- [x] 自检脚本通过
- [ ] K8s 已发布冒烟（段 E）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| D12 | 只调 Java `/svc/**`，禁 demo-* | ✅ |
| D8/D10 | Arco + 壳布局 | ✅ ENTRY 轻量 |
| D9 | KPI 有 metric_id 时挂 ReviewMetricBadges；空诚实 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~5 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：门户/查询经 Java 门面路径可分享；空态诚实。下一叶：`LUMEN-SVC-FE-WORKSPACE-L01`（依赖 JAVA-JOB + 本叶）。
