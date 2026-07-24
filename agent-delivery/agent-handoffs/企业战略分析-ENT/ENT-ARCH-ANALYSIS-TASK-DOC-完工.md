# ENT-ARCH-ANALYSIS-TASK-DOC 完工交接

## 1. 认领信息

- task-id：`ENT-ARCH-ANALYSIS-TASK-DOC`
- 执行：`agent:architect-agent`
- 监管：`human:徐滕强`
- 认领类型：`pull`
- 日期：2026-07-24

## 2. 范围与实现

依据用户提供的企业评估、风险洞察、招引推荐、培育推荐完整结果页截图，修订：

- `ARCH-ANALYSIS-TASK-设计方案.md` **v3.0**（含通读自检与数据库统一修订）
- 补齐招引 `attraction` 与培育 `cultivation` 两套结果契约
- 明确两类推荐均支持：
  - `selectionMode=filter`：按条件形成候选集合
  - `selectionMode=candidate_workbench`：从对比篮加入候选后显式指定 `enterpriseCodes[]`
- 明确两种来源仍共用 `analysisType=talent_recommend` 与 `/internal/gkx-ai/recommend/tasks`
- 补齐推荐排名、企业评价详情、证据状态、关键指标和风险信用字段
- 补齐 Java 本地 `recommend_report` 六节点异步报告任务
- 同步 §7.6 TypeScript 类型、C-8/C-9、D-18/D-19，并关闭 Q-1

### 2.1 通读自检发现并已修正的问题（v2.4）

| # | 问题 | 修正 |
|---|---|---|
| 1 | 架构图仍写「直接回调 Java / 不走 Python」，与正文矛盾 | 图例与算法侧文案改为「算法→Python→Java」；§2.4 标题同步 |
| 2 | 报告任务未接入框架：DDL 无 `parent_task_id`、前缀/小窗/创建接口/状态修正未覆盖 `*_report` | 补 §3.2 报告 6 节点、§12.1 框架规则、并发与 reconciler 分支 |
| 3 | 前端 SSE 示例仍查 `pending`；DDL 注释写 UUID；重启说明写 running/pending | 统一为无 pending；taskId=`EVAL|RISK|REC|REP-YYYYMMDD-NNN` |
| 4 | 关键指标误写「最近融资」；截图为「最近年度营收」 | 改为 `latestAnnualRevenueYiYuan` |
| 5 | F-3「全局任务列表页」与 C-4 冲突；架构图「策略路由」与「无策略模式」冲突 | F-3 改为模块内最近 Tab；图改为 if-else 路由 |
| 6 | §7.2 未列报告类型与 `selectionMode` | 创建任务表补齐 |
| 7 | 对比篮边界未写清 | 新增 §12.2：候选池 CRUD 属对比篮模块 |
| 8 | 导出推荐数据 / 图谱展开是否二次任务未决 | 登记 Q-6 / Q-7 |

### 2.2 v2.5 确认决策

| 项 | 结论 |
|---|---|
| 供应链图谱 | **方案 A**：分析任务一次算满最多 3 级写入快照；前端按需展开；不新建分析任务 |
| 创建报告 | Java 本地异步 `*_report`（`REP-`），PDF |
| 导出推荐数据 | Java 本地异步 `recommend_export`（`EXP-`），Excel/CSV；**与报告分离** |
| Q-6 / Q-7 | 已关闭 |

### 2.3 v3.0 数据库统一决策

- Java 编排任务库：MySQL
- entan / science 算法任务状态与结果库：MySQL
- 大结果、报告、导出文件：MinIO；MySQL 存指针
- 数据库统一不代表跨层直连：Java 与算法侧分库/分 schema，通过 API/回调交互
- 全文运行时 PostgreSQL/PG 引用已清除

## 3. 偏离说明

- 未拆分四套任务接口。招引/培育是 `subType`，条件筛选/候选工作台是 `selectionMode`，避免编排接口重复。
- 报告任务不重新调用 Python/算法；Java 读取父任务决策快照生成报告。
- 本任务仅修改设计文档与任务登记，不包含 Python、Java、前端实现。

## 4. 产物

- `agent-delivery/agent-handoffs/企业战略分析-ENT/ARCH-ANALYSIS-TASK-设计方案.md`
- `agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-ARCH-ANALYSIS-TASK-DOC-完工.md`
- `agent-delivery/task-registry.yaml`

## 5. 验收证据

- Markdown 代码围栏数量为偶数，结构闭合。
- §11.1～§11.7、§12.1～§12.2、报告节点 `read_snapshot`、C-9/D-19 均已落文档。
- 已检索确认无「直接回调 Java / 不走 Python」「running,pending」「业务任务ID(UUID」「latestFinancingAmount」残留。
- `git diff --check` 通过。
- 设计类任务：`cicd: skip_design_only`，不触发构建与部署。

## 6. 架构合规自检

1. ✅ 算法仅在 Python；文档未引入 Java 算法。
2. ✅ 分析调用链保持前端 → Java → Python `/internal/*` → 算法。
3. ✅ 未引入 Neo4j；图谱约束不变。
4. ✅ 未删除 Java/Python/前端既有可观测性要求。
5. ✅ 设计类任务按 `cicd: skip_design_only`。
6. ✅ 未操作 lumen 正式仓或合并 demo 代码。
7. ✅ Java 只编排、鉴权、存快照和生成报告，不写推荐算法。
8. ✅ 保持 ADS/Mock 先行策略。
9. ✅ 未修改前端视觉规范；后续实现仍须遵守 `Design.md`。
10. ✅ 结果字段保留证据可用性；统计指标实现时须补 D9 八件套与 MetricSpecCard。

## 7. 成本

- actual_tokens：约 60,000
- model_used：`gpt-5.6-sol`
- actual_cost：`0.00`（Cursor 席位未提供单任务计费）
- cost_warn：`green`
