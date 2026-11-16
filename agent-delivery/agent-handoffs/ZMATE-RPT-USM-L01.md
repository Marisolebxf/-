# ZMATE-RPT-USM-L01 · 定义：USM 完整用户故事地图（战略报告创作）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | FDE 波次 A1；门 1 前唯一开工叶 |

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
| diagram_id | N/A（本叶仅 USM；协作拓扑引用建设方案 §6.2，IA/WF 后续叶出图） |
| 图 diff | 无 |
| 会签态 | draft |
| 说明 | TRACE/IA/Wireframe 见后续 A2–A4 |

## 问题清单

- OPEN-ZMATE-ROLE-01 / 02：源文无岗位，待业务确认是否另建写作/模板岗  
- OPEN-ZMATE-HANG-01：父包挂靠（推荐高端智库生成 + 专题切片交叉引用）  
- OPEN-ZMATE-V1-01 / DEMO-01 / EXPORT-01：见 USM 开放项表  

## 修改内容

- 新增完整 USM：`agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/USM-ZMATE-战略报告创作.md`  
- 角色回指 `§1.1.1.2.4.2` 四类服务对象；高端智库 SRS 无岗位处标待确认  
- 故事覆盖创作壳、人在回路禁 autoRun、Graph 协作可见、卷宗≠切片、指标四态、装配溯源、合规 Judge、评审模式页特有差异  
- 边界：`demo-ui-topic` 纯前端样机；非目标与不挡 V1 真后端已写清  

## 测试结果

- 结构对照范例 `USM-E7-政策分析.md`：角色表 / As-Want-So that / 主异 walkthrough / 可测验收 / 差异与开放项 — 齐  
- 未改代码、未手改 task-registry.yaml  

## 遗留风险

- 体验 Owner 未指定；门 1 前需补  
- 旧 FE Graph 脚手架与本 USM 可能冲突，待会签按废稿默认处理  

## CI/CD（必填）

- 分支：`dev`  
- commit：（本 handoff 提交后回填）  
- pipeline URL / ID：编排仓无业务 CI  
- 部署 namespace / 镜像 tag：N/A  
- K8s rollout：N/A  
- dev 测试 URL / 命令与结果：N/A（定义文档）  

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A  
- traceId：N/A  
- Tempo / Loki：无  

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/USM-ZMATE-战略报告创作.md`  
- `agent-delivery/agent-handoffs/ZMATE-RPT-USM-L01.md`  

## 架构合规自检（摘要）

| 铁律 | 结论 |
|------|------|
| 角色可回指 bid-reference | ✅ §1.1.1.2.4.2；SRS 无岗 → 待确认 |
| 禁止从页面反推岗位 | ✅ |
| D12 Demo 边界 | ✅ 写清 demo-ui-topic / 不写 lumen |
| 调用链 / 算法 | ✅ 非目标声明；Demo Mock |
| handoff | ✅ 本文件 |
