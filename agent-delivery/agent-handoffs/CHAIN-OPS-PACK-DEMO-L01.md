# CHAIN-OPS-PACK-DEMO-L01 · handoff

> **任务**：产业链维护管理 — 产品定义五件套补齐 + demo-ui-topic 菜单壳落地  
> **执行**：agent:product-agent（协作 frontend）  
> **监管**：human:高颖  
> **日期**：2026-08-06

## 1. 范围与实现

对照：

- Bid `§1.1.1.2.4.5.6.1` 产业全景内容管理 + catalog `IC-42`/`IC-43`
- IA 写侧补齐通知（`IA-CHAIN-TOPIC-ANALYSIS` 2026-08-05）与 `DEC-CHAIN-OPS-REUSE-ENT-OPS-20260805`
- `SPEC-CMS-CHAIN-PORTAL-CONTENT` 五块落位

交付：

1. **定义包** `agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-OPS-维护管理/`  
   - 能力全清单 / IA / TRACE / USM / Wireframe / UX-SPEC（`ready_for_v1`）
2. **Demo** `demo-ui-topic`  
   - 菜单「维护管理」、路由 `/industry-center/maintenance`  
   - 权限 `menu:chain:maintenance`（L4 子角色）  
   - 15 项导航壳；A1 门户内容可演示状态机；其余占位

## 2. 偏离说明

- A2–C6 为占位可评（与 ENT-OPS 同期策略一致），未做深度联调。
- 未改 lumen 正式仓；admin 正式 content_type 存储仍属开放项（GAP-CHAIN-OPS-CMS-STORE）。
- 不增加八项分析 Bid 叶子计数。

## 3. 产物清单

| 仓 | 路径 |
| --- | --- |
| gkx-orchestration | `agent-delivery/agent-handoffs/产品整体定义/E2-产业链分析/CHAIN-OPS-维护管理/*` |
| gkx-orchestration | `SPEC-CMS-CHAIN-PORTAL-CONTENT.md` CMS-OV-03 回填 |
| demo-ui-topic | `src/app/pages/industry-center/IndustryMaintenancePage.tsx` |
| demo-ui-topic | `src/app/pages/industry-center/industryMaintenanceDefinition.ts` |
| demo-ui-topic | `Layout.tsx` / `routes.tsx` / `IndustryCenterPage.tsx` / `perms/matrix.ts` |

## 4. 验收证据

- 切换 L4「内容运营」等子角色 → 左侧「产业链分析 → 维护管理」可见  
- 打开 `/industry-center/maintenance?tab=portal` → 五块类型 + 草稿/审核/发布可点通  
- 左栏 15 项齐全；非 portal 为占位页  

## 5. 架构合规自检

| # | 铁律 | 结果 |
| --- | --- | --- |
| 1 | 算法只在 Python | ✅ 无算法 |
| 2 | 前端 → Java → Python | ✅ Demo 本地状态，未越层调算法 |
| 3 | NebulaGraph | ✅ 未引入 Neo4j |
| 4 | 可观测性 | ✅ 评审挂载 / MockBadge（既有组件） |
| 5 | CI/CD | ✅ push 触发既有流水线 |
| 6 | demo 不 merge lumen | ✅ 仅 demo-ui-topic + 编排文档 |
| 7 | 共享聚合核心 | ✅ 未破坏 |
| 8 | ADS/Mock | ✅ CMS 不背数；MockBadge |
| 9 | Design.md / Arco | ✅ Arco + 既有 token |
| 10 | 数据血缘 | ✅ 本页以内容运营为主；禁止假指标录入已写 Alert |
| 11 | D10 交互规范 | ✅ UX-SPEC 含锁态/键盘/走查 |

## 6. Cost（回填）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~95k（估） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~$3.5（估） |
| cost_warn | false |
