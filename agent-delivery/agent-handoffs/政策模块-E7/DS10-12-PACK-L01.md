# DS10-12-PACK-L01 · 展示系统科技政策跟踪核心产品包

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:ux-agent` |
| supervised_by | `human:高颖` |
| claim_type | `pull` |
| claimed_at | 2026-08-05（MCP task-claim） |
| lock | 认领后 +4h |

## 范围与实现（对照 bid-reference）

| 锚点 | 落点 |
| --- | --- |
| `§1.1.1.1.4.2.1` 科创政策全景 | DS-10 · `/display/policy/panorama`（含四 Tab） |
| `§1.1.1.1.4.2.2` 政策分析评价 | DS-11 · `/display/policy/evaluation` |
| `§1.1.1.1.4.2.3` 政策效果推演 | DS-12 · `/display/policy/simulation` |
| `§1.1.1.1.4.2.4.1~4` 核增四叶子 | DS-PC-01~04 · governance/parse/compare/insight-report |
| 三屏双轨 | TRACE `screen_tier` large/medium/small；Track-L Owner 王亚东 |

**与专题分轨**：USM/IA/Wireframe 均显式声明展示 `/display/policy/*` ≠ 专题 `/policy/*`（E7）≠ 门户 `/policy-portal/*`。

## 产物清单

| 文件 | 路径 |
| --- | --- |
| USM | `agent-delivery/agent-handoffs/产品整体定义/DS10-12-科技政策跟踪/USM-DS10-12-科技政策跟踪.md` |
| TRACE | `…/TRACE-DS10-12-科技政策跟踪.yaml` |
| IA | `…/IA-DS10-12-科技政策跟踪.md` |
| Wireframe | `…/Wireframe-DS10-12-科技政策跟踪.md` |
| 本 handoff | `agent-delivery/agent-handoffs/DS10-12-PACK-L01.md` |

## DoD 对照

- [x] USM：角色来自 bid §1.1.1.1.4.2 / 系统概述四场景 + §4.2.1.3 施政者/受众；含三屏说明
- [x] TRACE：leaves = DS-10/11/12 + DS-PC-01~04；`source_inventory_complete: true`
- [x] IA：全模块信息架构与跨系统边界
- [x] Wireframe：字段表含 metric_id（D9）
- [x] 与专题 `/policy/*` 差异说明已写

## 偏离与开放项

| 项 | 说明 |
| --- | --- |
| GAP-DS-PC-CATALOG | `catalog-display-7modules.yaml` 尚未登记 DS-PC-01~04；本包按 scope-baseline 核增四叶子编号，待 catalog 补条 |
| GAP-DS-ROUTE | catalog DS-10/11/12 `route=null`；本包给出候选 route，待门1后回写 |
| Q030 / QPOL-* | 权限屏幕口径与政策指标口径仍 🟡；Wireframe 已标 ⚠️ |
| 未改代码 | 定义任务；无 CI/K8s |

## 验收证据

- 四件套路径见上；结构自检清单已在各文档勾选
- 下游：`POLICY-UX-L01`（依赖本单）、`POLICY-METRIC-OPEN-L01`

## 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未写算法代码 |
| 2 | 调用链 前端→Java→Python | ✅ Wireframe 禁止直连 Nebula/Python |
| 3 | 图谱 Nebula | ✅ 仅展示消费声明 |
| 4 | 可观测性 | N/A（定义包） |
| 5 | CI/CD | N/A（无代码 push） |
| 6 | demo2 不 merge lumen | ✅ 未改业务仓 |
| 7 | 共享聚合 | ✅ 展示消费 /topic 经 Java（联调任务另单） |
| 8 | ADS/Mock | ✅ Wave0 MockBadge 写入 |
| 9 | Design.md / 三屏双轨 | ✅ Track-MS vs Track-L 分离 |
| 10 | D9 血缘 | ✅ metric_id 列 |
| 11 | D10 交互 | ⏳ 交 `POLICY-UX-L01` |

## 成本回填（预算）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~95000（估） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~2.5 USD（估） |
| cost_warn | false |

## 建议下一状态

definition 任务：handoff 已交 → 请 coordinator 走 AV / 会签；下游 UX 可认领 `POLICY-UX-L01`。
