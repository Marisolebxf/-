# ZMATE-RPT-TRACE-L01 · 定义：TRACE 父矩阵 + 功能点编号

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | FDE 波次 A2；依赖 USM `ZMATE-RPT-USM-L01`（integration） |

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
| diagram_id | N/A（本叶 TRACE；协作拓扑仍引用建设方案 §6.2，IA/WF 后续叶出图） |
| 图 diff | 无 |
| 会签态 | draft |
| 说明 | provisional_route 占位；正式 route/frame 由 IA/WF 回填 |

## 问题清单

- OPEN-ZMATE-HANG-01 / ROLE-01/02 / V1-01 / EXPORT-01 / DEMO-01：沿用 USM，已写入 TRACE `open_questions` + gaps  
- GAP-ZMATE-RPT-01：IA/WF 未交付，route 为 provisional  
- GAP-ZMATE-RPT-02：体验 Owner 未指定  

## 修改内容

- 新增 TRACE：`agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/TRACE-ZMATE-战略报告创作.yaml`  
  - `module` / `source_requirement` / `product_artifacts` / `leaves`（RPT-01…12）  
  - 12 条 `stories` 对齐 `US-ZMATE-RPT-01…12`，每条含 `compliance_refs`  
  - 可测功能点子点 **46** 个（`RPT-xx-n`）  
  - 排除：研究报告管理/洞察发布/热点分析、门户推荐、专题八域工作区  
- USM 头注「对应 TRACE」改为指向本 TRACE 文件  

## 测试结果

- 结构对照范例 `TRACE-E7-政策分析.yaml`：源需求 / 产物指针 / leaves / stories+compliance_refs / exclusions / gaps — 齐  
- 对照规程 §3.3：stories + compliance_refs + coverage_summary — 齐  
- 未改业务代码；未手改 `task-registry.yaml`；未提交他人未跟踪 `*.feishu.json`  

## 遗留风险

- provisional_route 在 IA/WF 前可能漂移，须 A3/A4 回填  
- 父包挂靠与体验 Owner 仍为 draft，门 1 前需监管人确认  

## CI/CD（必填）

- 分支：`dev`  
- commit：`1360bb79f`（docs TRACE 父矩阵）  
- pipeline URL / ID：编排仓无业务 CI  
- 部署 namespace / 镜像 tag：N/A  
- K8s rollout：N/A  
- dev 测试 URL / 命令与结果：N/A（定义文档）  

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A  
- traceId：N/A  
- Tempo / Loki：无  

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/TRACE-ZMATE-战略报告创作.yaml`  
- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/USM-ZMATE-战略报告创作.md`（TRACE 指针）  
- `agent-delivery/agent-handoffs/ZMATE-RPT-TRACE-L01.md`  

## 架构合规自检（摘要）

| 铁律 | 结论 |
|------|------|
| 角色可回指 bid-reference | ✅ §1.1.1.2.4.2 |
| USM 故事全映射 | ✅ 12/12 → RPT-01…12 |
| 功能点可测编号 | ✅ RPT-xx-n 共 46 |
| D12 Demo 边界 | ✅ module_exclusions + DEC |
| 调用链 / 算法 | ✅ 非目标；Demo Mock |
| handoff | ✅ 本文件 |
