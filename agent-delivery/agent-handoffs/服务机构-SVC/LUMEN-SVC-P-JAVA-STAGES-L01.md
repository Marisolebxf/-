# LUMEN-SVC-P-JAVA-STAGES-L01 · svc 异步分析 8 叶阶段节点生命周期

> 日期：2026-10-21 · 执行：`agent:api-agent` · 监管：`human:侯佳伟` · 签收：`human:淮政玮`
> 任务：`LUMEN-SVC-P-JAVA-STAGES-L01`（E7-产业服务链分析 · feature · P0）
> 替代废单：`LUMEN-SVC-JAVA-JOB-L01`（2026-08-18 范围3停机废作，勿复用）
> 强度：ponytail full

## 1. 背景与范围

用户走查发现：产业服务链全部异步分析叶子（机构领域覆盖 / 新增趋势 / 技术力评估 / 服务链短板 / 图谱 / 深圳现状 / 引育推荐）在过程页**没有阶段节点**，与企业分析（ChainAnalysis）行为不一致，不符合 demo-ui-topic 原型 `/service/institution-judgment` 的 Steps 设计。

根因：`AnalysisTaskServiceImpl.createTaskInternal` 的 `svcJob` 分支**没有预插入 `analysis_task_node` 节点**（Chain/Policy 分支均有），前端过程页拿不到节点数据，只能显示无节点态。

## 2. 实现与偏离

| 文件 | 改动 |
|---|---|
| `SvcAnalysisTypes.java` | 新增八叶子标准阶段词表 `STAGES` / `stagesOf(leaf)` / `stageTotal(analysisType)`；`org_coverage`/`org_trend`/`tech_power`/`shortboard`/`graph`/`shenzhen` = 4 阶段，`attract`/`cultivate` = 5 阶段 |
| `AnalysisTaskServiceImpl.java` | `svcJob` 分支接入 `seedSvcNodes`（创建时预插全部节点：首节点 `started`，其余 `pending`）与 `finalizeSvcNodes`（同步/异步落地：成功→全 `completed`；失败→当前节点 `failed`，其余保持 `pending`） |
| `AnalysisTaskServiceImplSvcJobTest.java` | 重写单测覆盖词表一致性与节点流转（16 用例） |

偏离说明：无。词表与 demo-ui-topic 原型一致；节点状态机复用既有 `analysis_task_node` 通道，未新增表或接口。

## 3. 验证证据

- 离线单测（内网 Nexus 不可达，java -cp + JDK 21 JUnit Platform Launcher 直跑）：
  **17 tests found / 17 successful / 0 failed**（2026-10-21 代码审查后）
- 覆盖：8 叶词表阶段数与文案、seed 后节点数与首节点状态、成功流转全 `completed`、失败流转当前 `failed` 余 `pending`、**下游异常路径 finalize**、非 svc 类型不受影响。

## 3.1 代码审查记录（2026-10-21，用户质询后补做）

逐 diff 审查（词表 / 主逻辑 / 单测）发现并修复 **1 个真实缺陷**：

- ❌ **异常路径漏推进节点**：`createDownstream` 抛异常（如 Feign 超时）时 catch 块只置任务 `failed`，未调 `finalizeSvcNodes`，节点会永挂 `started`，前端过程页出现永不结束的步骤。
- ✅ 修复：catch 块补 `finalizeSvcNodes(entity, true)`（根因单点修复，覆盖所有异常入口）。
- ✅ 新增回归用例 `downstreamExceptionAlsoFinalizesNodesToFailed`（17th 用例）。
- 审查同时排除：`applySvcSyncResult` 为 success/failed 二元落态，无中间态误置 completed 风险。

工程备注（离线编译坑，供后续复现）：`target/` 内 class 曾被 IDE/ECJ 重编译为坏产物（"Flexible Constructor Bodies" source level 25 错误）；本机 javac 离线编译须用 **lombok ≥1.18.42**（1.18.12 在 JDK 21 注解处理崩溃），`--release 21 -proc:full`，产物写入 `target/svcfix-cls/`（workspace 内，sandbox 可写）。

- `git status`：3 文件改动，均在 dev 工作区，**未 commit（受人工验收闸门约束）**。

## 4. 架构合规自检

| 铁律 | 合规 |
|---|---|
| D1 调用链（前端→Java→Python /internal） | ✅ 未触碰调用链，仅 Java 内任务节点生命周期 |
| D9 指标血缘 | ✅ 不涉及统计口径；节点为过程态非指标 |
| demo2 只读 merge | ✅ 词表对齐原型语义，未 merge demo 仓代码 |
| D12 demo/lumen 隔离 | ✅ 仅改 lumen-svc-platform |
| 人工验收闸门（2026-10-20 裁定） | ✅ 改动停留本地，push 前待监管人走查确认 |

## 5. 下一步

1. 监管人（侯佳伟）走查本地代码 → 确认后 commit + push `origin/dev` → CI → K8s dev
2. 发布后验证：svc 分析工作区过程页出现阶段节点并正确流转
3. 前端联调单 `LUMEN-SVC-P-FE-STAGES-L01`（frontend-agent）走查 8 叶全叶子过程页
4. cost 回填 + coordinator AV-0/AV-1

## cost

- actual_tokens: 110000
- model_used: glm-5.3-Flash（本段）+ claude-sonnet-4.5（编码段）
- actual_cost: 0.9
- cost_warn: green
