# ZMATE-RPT-IA-L01 · 定义：IA 信息架构（含 Agent 协作站点）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | FDE 波次 A3；USM integration 后解锁 |

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
| diagram_id | `ZMATE-RPT-IA-TREE`（IA 文档 §3 文本树 + Graph 主序；非仓内运行图） |
| 图 diff | 新增创作壳→Hub→澄清→Planner→辩论∥切片→Seeker→Writer→Judge 导航树；路由对齐建设方案 §9.2 |
| 会签态 | draft |
| 说明 | Wireframe 叶再出线框级构图；本叶交付 IA 树与路由语义 |

## 问题清单

- OPEN-ZMATE-ROLE-01/02、HANG-01、V1-01、DEMO-01、EXPORT-01：继承 USM，IA 未新开业务口径  
- 体验 Owner 仍待门 1 前指定  

## 修改内容

- 新增 IA：`agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/IA-ZMATE-战略报告创作.md`  
- 模块边界 / 角色入口与 USM 一致；Agent 协作分站入 IA 树  
- 术语合同：辩论知识卷宗 ≠ 专题切片/研判卡；合规 Judge ≠ 胜负裁判  
- 内部评审模式仅页特有差异；Design.md 仅 token/布局引用，未画高保真  
- 未改前端代码；未手改 task-registry.yaml  

## 测试结果

- 结构对照范例 `IA-E7-政策分析.md`：边界 / 角色入口 / IA 树 / 页面清单 / 主路径 / 跨模块 / 差异 / 自检 — 齐  
- 对照建设方案 §9.2 路由与 harness 阶段序一致  
- DoD：导航、页面清单、Agent 协作在 IA 中的位置、角色表与 USM 一致 — ✅  

## 遗留风险

- 旧 FE Graph 脚手架与本 IA 路由可能并存，会签默认废稿后按 WF 重做  
- V1 最短跳过辩论与 Demo「可点验完整协作」并存，Wireframe 须显式画清两条路径  

## CI/CD（必填）

- 分支：`dev`  
- commit：`5eab809a8`  
- pipeline URL / ID：编排仓无业务 CI  
- 部署 namespace / 镜像 tag：N/A  
- K8s rollout：N/A  
- dev 测试 URL / 命令与结果：N/A（定义文档）  

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A  
- traceId：N/A  
- Tempo / Loki：无  

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/IA-ZMATE-战略报告创作.md`  
- `agent-delivery/agent-handoffs/ZMATE-RPT-IA-L01.md`  

## 架构合规自检（摘要）

| 铁律 | 结论 |
|------|------|
| 角色与 USM / bid 一致 | ✅ §1.1.1.2.4.2 四类；无岗位不反推 |
| Agent 协作在 IA 中有位置 | ✅ Hub + 分站路由语义 |
| 卷宗 ≠ 切片；Judge ≠ 胜负 | ✅ §3.1 / §8 |
| D12 Demo 边界 | ✅ demo-ui-topic；不写 lumen |
| 禁止单页跑完全链 | ✅ §3.2 / §5 |
| handoff | ✅ 本文件 |
