# 政策分析走查清单 · E7

> **用途**：开工 / Demo 联调 / 门 2 前自检  
> **配套**：`SYS-CAPABILITY-ADAPTER-E7-POLICY.md` · `DOC-vs-DEMO-SCOPE-E7-POLICY.md` · `POLICY-TASK-TYPE-CONTRACT.md`  
> **金样例**：企业评估任务浮层 + 产业链 `chain:{module}:{analysisKey}` 互斥/恢复  
> **日期**：2026-08-07

## A. 前置（文档闸门）

| # | 项 | ☐ |
|---|---|---|
| A1 | 接入卡 §1–§5 已填；task_type 与 Registry 对照表一致 | |
| A2 | DOC-vs-DEMO 三栏无「文档写全、Demo 无入口又无占位」 | |
| A3 | 维护管理：门户样例=`demo_must`，其余=`placeholder` 话术一致 | |
| A4 | 未改 ENT-COMPARE / SYS-JOBS / ENT-EXPORT 壳层故事 | |

## B. 对比篮（产业 Tab 发起政策三项 · 回归）

| # | 步骤 | 期望 | ☐ |
|---|---|---|---|
| B1 | 产业查询加入 1 个产业 | 按钮「已加入」；Shell 角标同步；停留原页 | |
| B2 | 打开系统篮 → **产业** Tab | 可见产业对象；**无「政策」Tab** | |
| B3 | 勾选 1 产业 → 发起分析 →「政策分析」→ 时序 | 跳转 `/policy/overview?source=compare-basket&analysis_type=policy_timeseries&object_type=industry&object_ids[]=…` | |
| B4 | 区域对比 / 深圳现状 | 分别到 `/policy/analysis`、`/policy/recommendation`，同分发契约 | |
| B5 | 政策查询/门户 | **无**「加入对比篮」写政策文档 | |
| B6 | 未选 / 多选产业发起政策三项 | 阻断并提示（需恰好 1 个产业） | |

## C. 任务浮层（2026-08-07 Demo 已接线 · 需人工点验）

> as-built：`PolicyAnalysisWorkspace` + `policyTaskType.ts` 已挂 Gate；契约测试覆盖 task_type。下表 ☐ 仍须人工在浏览器点验。

| # | 场景 | 期望 | 对接 task_type | ☐ |
|---|---|---|---|---|
| C1 | 时序页提交分析后离页 | 浮层可见非终态任务 | `policy:overview:policy_timeseries` | |
| C2 | 同分析再进配置 | 恢复原任务，不并行第二条 | 同上 | |
| C3 | 时序任务在途时再开区域对比 | 可并行（不同 task_type） | `policy:analysis:policy_region_compare` | |
| C4 | 完成后 | 停进度页；手动「查看分析结果」 | 对齐产业链纠偏 | |
| C5 | 失败重试 | 新 task_id；可带 retry_from | | |
| C6 | 打开任务浮层时对比篮展开 | 篮自动收起（互斥） | | |
| C7 | storage | 无企业 task/key 串读 | | |
| C8 | 勿使用 | `policy_analysis_batch`（旧 policy-center） | 废弃 | |

## D. 报告（ENT-EXPORT · 触发已接线 · 需人工点验）

> as-built：三结果页已带 `data-report-task-type=policy:report:{template}` + fingerprint；已去掉纯 Mock Toast。完整 Reader/PDF 链路仍依赖系统壳。

| # | 步骤 | 期望 | ☐ |
|---|---|---|---|
| D1 | 结果页点导出 | 走系统报告任务弹层，非仅 Toast | |
| D2 | 同 fingerprint 再点 | 复用任务/产物，不重复空跑 | |
| D3 | 阅读 | HTML Reader → 再 PDF；不跳过 HTML | |
| D4 | data-* | `data-system-report-trigger` + task-type/fingerprint/template | |

## E. 三项分析页（业务）

| # | 页 | 检查 | ☐ |
|---|---|---|---|
| E1 | `/policy/overview` | 分发上下文有效；无上下文空态 CTA（去查询/开篮） | |
| E2 | `/policy/analysis` | 同上；区域对比字段不进篮对象 | |
| E3 | `/policy/recommendation` | 同上；权重属配置快照 | |
| E4 | Design.md §14 | 主色/控件高/字号/间距 | |
| E5 | UX-UE §19 | 状态/键盘/抽屉 | |
| E6 | 对照企业过程页 | 操作栏/进度/返回不另造交互语言 | |

## F. 维护管理（防写了没跑出来）

| # | 项 | 期望 | ☐ |
|---|---|---|---|
| F1 | `/policy/maintenance` 门户内容样例 | 草稿→审→发可点通 | |
| F2 | 其余 ENT-OPS 对齐菜单 | 可达 + 占位说明；不删项 | |
| F3 | 评审话术 | 不把 F2 说成已交付 | |

## G. 结论栏

| 结论 | 条件 |
|---|---|
| ☐ 可进视觉走查 | B 全过；C 接线计划已排期 |
| ☐ 可称「系统能力复用完成」 | B+C+D 全过 |
| ☐ 可进门 2 准备 | A–F 全过或软项书面结转 |

**阻塞项（当前已知）**

1. ~~专题三分析页未接 SYS-JOBS~~ → 已接线；C 段待人工点验勾选。  
2. ~~报告导出纯 Toast~~ → 触发属性已齐；D1–D3 待人工点验。  
3. 旧 `policy_analysis_batch` 勿当模板。
