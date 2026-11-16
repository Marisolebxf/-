# ZMATE-RPT-WF-L01 · 定义：Wireframe + 状态清单（HITL/协作分屏）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:ux-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | IA integration 后解锁 A4 Wireframe |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义任务；不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机定义文档任务，未挂载 headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `ZMATE-RPT-WF-SPLIT`（统一分屏壳 + 各 Frame ASCII；对齐 IA 树） |
| 图 diff | 新增 HITL/Graph 分屏线框与六态；辩论∥切片并行入口；禁止单页全链 |
| 会签态 | draft |
| 说明 | 线框级构图；非仓内运行图；高保真另叶 |

## 问题清单

- OPEN-ZMATE-ROLE-01/02、HANG-01、V1-01、DEMO-01、EXPORT-01：继承 USM/IA，本叶未新开业务口径  
- 体验 Owner 仍待门 1 前指定  
- V1 最短跳过辩论与 Demo 完整可点验并存，实现须同时保留两条路径入口  

## 修改内容

- 新增 Wireframe：`agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/Wireframe-ZMATE-战略报告创作.md`  
- Frame 覆盖：创作壳、Hub、澄清人闸、Planner、辩论∥切片、Seeker、Writer、Judge、旧链重定向  
- 全局六态：`empty` / `locked` / `awaiting_gate` / `running` / `failed` / `compliance_fail`  
- 术语合同与内部评审模式页特有差异；D10 §19 走查对照  
- 未改前端代码；未手改 task-registry.yaml；未碰他人未跟踪 feishu.json  

## 测试结果

- 结构对照范例 `Wireframe-E7-政策分析.md`：Frame 清单 / 线框 / 状态 / review mounts / 走查 — 齐  
- 对照 IA §3 路由与 USM 主路径 A/B/C、异常表 — 一致  
- DoD：线框覆盖主路径与空/锁定/人闸/失败态；内部评审模式页说明；对照 D10 §19；handoff — ✅  

## 遗留风险

- 旧 FE Graph 脚手架与本 WF 路由可能并存，会签默认废稿后按 Frame 重做  
- 正式导出与 ENT-EXPORT 对齐时机未定（OPEN-ZMATE-EXPORT-01）  

## CI/CD（必填）

- 分支：`dev`  
- commit：（push 后回填）  
- pipeline URL / ID：编排仓无业务 CI  
- 部署 namespace / 镜像 tag：N/A  
- K8s rollout：N/A  
- dev 测试 URL / 命令与结果：N/A（定义文档）  

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A  
- traceId：N/A  
- Tempo / Loki：无  

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/Wireframe-ZMATE-战略报告创作.md`  
- `agent-delivery/agent-handoffs/ZMATE-RPT-WF-L01.md`  

## 架构合规自检（摘要）

| 铁律 | 结论 |
|------|------|
| 角色与 USM / bid 一致 | ✅ 不新增岗位；沿用四类服务对象 |
| Agent 协作分屏可见 | ✅ Hub + 分站 Frame；禁单页全链 |
| 卷宗 ≠ 切片；Judge ≠ 胜负 | ✅ §0 / §7 / §8 / §11 |
| D8 Design 线框引用 | ✅ 32px / `#165DFF` / `#D8E7FC` |
| D10 §19 | ✅ §14 对照表 |
| D12 Demo 边界 | ✅ 不写前端 / 不连 lumen |
| handoff | ✅ 本文件 |
