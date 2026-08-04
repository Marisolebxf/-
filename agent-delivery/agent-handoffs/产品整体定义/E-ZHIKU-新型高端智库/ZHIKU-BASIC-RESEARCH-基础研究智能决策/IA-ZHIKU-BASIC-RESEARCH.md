# IA-ZHIKU-BASIC-RESEARCH｜基础研究智能决策·信息架构

> **版本**：v1.0-rework-r2（AI 起草，待人确认）
> **同步件**：USM / Wireframe / UX-SPEC / TRACE 同版本

## 0. 源件清单

| 源件 | 路径 | 用途 |
| --- | --- | --- |
| 需求拆解表 §四 | `agent-delivery/bid-reference/高端智库/新型高端智库需求拆解.md` | 序号 82-87 唯一范围真源 |
| Epic 五件套（父包，已降级） | `../USM-E-ZHIKU-新型高端智库.md` 等 | 仅作历史对照，本叶子包为模块唯一真源 |
| S5 Wireframe v0.6 P67-P72 | `../Wireframe-E-ZHIKU-新型高端智库.md` | 字段表资产收编来源 |
| R1 叶子包 | `../ZHIKU-WRITING-报告智能写作/` | 跨叶子契约对手方 |
| 数据血缘规约 | `agent-delivery/data-lineage-policy.md` v1.3 §2.3 | 指标四维就绪度唯一真源 |

## 1. 模块目标

支撑"基础研究该投什么、投在深圳哪里、投后效果如何"的决策链：问题识别订阅 → 趋势监控 → 竞争研判 → 部署联动 → 资源配置 → 成果评估，并在研判/评估节点把结论导入 ZHIKU-WRITING 报告生产线。

## 2. 产品边界

**承接**：序号 82-87 全部 6 项；S5 P67-P72 页面资产收编重构。

**不承接**：

- 报告写作/编辑/发布本体 → ZHIKU-WRITING（本模块只负责创建预填任务并跳转）。
- 智能问数、技术路线图、人才地图等其他叶子域功能。
- 真实挖掘模型、竞争格局指数权重算法、成果四维量化算法（均为 🧪 演示态 + GAP 登记）。
- 部署清单/成果对象的后台维护（新增/编辑表单）。

## 3. 产品角色与权限

| 角色 | 问题清单 | 趋势监控 | 竞争格局 | 部署清单 | 组织实施 | 成果评估 |
| --- | --- | --- | --- | --- | --- | --- |
| `ROLE-BR-MANAGER` | 查询/订阅/识别/发布 | 查看+预警处理 | 查看 | 筛选/联动 | 查看+建议跟踪 | 查看 |
| `ROLE-BR-REVIEWER`（demo 合并代演） | — | — | 生成报告 | — | — | 生成报告 |

demo 单用户不做权限拦截，角色差异以界面动作语义呈现；正式权限模型挂 `Q-ZHIKU-01`。

## 4. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| 基础研究问题 `IssueItem` | `issue-*` / `issue-new-*`（新识别） | 识别中 → 已在线发布（可移除仅限未发布的新识别） | `zhiku-br-issues` |
| 订阅关系 | `issueId` 集合 | 订阅 ↔ 退订 | `zhiku-br-subscriptions` |
| 预警 `IssueAlert` | `ia-*` | 未处理 → 已处理 | `zhiku-br-alerts-handled` |
| 部署条目 `DeployItem` | `dep-*` | 静态种子（demo 不新增） | 筛选/选中态持久化 |
| 建议跟踪 | `rs-*` 集合 | 纳入 ↔ 移除 | `zhiku-br-suggestions` |
| 评估成果 `EvalResult` | `eval-*` | 静态种子 | 选择/视图态持久化 |
| 跨叶子产物：写作任务 | `TASK-*`（写作域） | 由 writing taskStore 管理 | `zhiku-wr:tasks`（对方域） |

## 5. 信息架构与导航

左侧手风琴菜单「基础研究智能决策」组（4 项，路由不变）：

| 菜单项 | 路由 | Frame | 序号 |
| --- | --- | --- | --- |
| 问题清单与趋势 | `/basic-research/issues` | F-BR-01/02/03（页内 Tab） | 82/83/84 |
| 深圳市部署清单 | `/basic-research/deploy` | F-BR-04 | 85 |
| 组织实施分析 | `/basic-research/org` | F-BR-05 | 86 |
| 成果评估 | `/basic-research/eval` | F-BR-06 | 87 |

URL 参数契约（刷新/分享可恢复）：

- `/basic-research/issues?tab=list|trend|competition&issue=<id>`：Tab 与当前问题下钻上下文。
- 其余页面的筛选/选中/视图态由 `zhiku-br-` 前缀 localStorage 恢复（非 URL 承载，见 UX-SPEC §3）。

跨叶子出口：

- F-BR-03 / F-BR-06「生成报告」→ `writing taskStore.createTask(预填)` → `/writing/create?step=outline&task=<id>`。
- F-BR-04 热点问题 → `/basic-research/issues?tab=trend&issue=<id>`（模块内回链）。

## 6. Frame 责任

| Frame | 责任 | 主要区块 |
| --- | --- | --- |
| F-BR-01 问题清单 | 查询/筛选/订阅/识别/发布 | 统计卡（总数+订阅数）、来源目录、清单表格、我的订阅、识别入口 |
| F-BR-02 问题发展趋势 | 单问题研判 | 来源回溯条、轨迹图、三得分卡、预警（未/已处理）、智能推荐、文献摘要抽屉 |
| F-BR-03 竞争格局报告 | 三层次对比+报告出口 | 层次 Tab、四统计卡、区域对比（柱/雷达）、趋势追踪、生成报告按钮 |
| F-BR-04 部署清单 | 筛选+地图联动+回链 | 统计卡、三维筛选条、地图（选中联动）、清单表格（行选中）、详情侧条、趋势图、热点问题 |
| F-BR-05 组织实施 | 能力分析+建议跟踪 | 综合得分+五维卡、雷达、资源清单表、需求预测图、四类建议、我的跟踪清单 |
| F-BR-06 成果评估 | 四维评估+视图切换+报告出口 | 告警条、成果选择器、五统计卡、四维雷达、评估报告文本、对比/趋势子视图、生成报告按钮 |

## 7. 数据与服务边界

- demo 全量 mock：领域 store `src/mock/basicResearch.ts`（reducer 化 action + `zhiku-br-` 前缀 localStorage）。
- 正式态最小服务面（Java REST，只读 ADS；算法经 Python `/internal/*`）：
  - `GET /basic-research/v1/issues`（含订阅态）/ `POST .../issues/{id}/subscribe|publish`
  - `POST /basic-research/v1/issues/identify`（转发 Python 挖掘服务）
  - `GET /basic-research/v1/issues/{id}/trend|alerts|recommendations`
  - `GET /basic-research/v1/competition?tier=`、`GET /basic-research/v1/deploy-list`、`GET /basic-research/v1/org-analysis`、`GET /basic-research/v1/eval-results`
  - 指标 8 件套+就绪度：`GET /metrics/v1/catalog`（gkxlumen-metrics）
- 前端禁止直连 Python/nGQL；图表全部 ECharts，地图 Leaflet+天地图（复用 TalentMapView）。

## 8. 指标（D9）

| metric_id（正名后） | 原 id（S5） | D1 def | 呈现 |
| --- | --- | --- | --- |
| `ZHIKU-BR-ISSUE-TOTAL` | ZHIKU-S5-ISSUE-TOTAL | draft | ⓘ+🧪 |
| `ZHIKU-BR-ISSUE-HEAT-SCORE` | ZHIKU-S5-ISSUE-HEAT-SCORE | draft | ⓘ+🧪（演示态打分） |
| `ZHIKU-BR-COMPETITION-INDEX` | ZHIKU-S5-COMPETITION-INDEX | **missing** | 红问号 → GAP 引用 |
| `ZHIKU-BR-DEPLOY-TOTAL` | ZHIKU-S5-DEPLOY-TOTAL | draft | ⓘ+🧪 |
| `ZHIKU-BR-ORG-CAPABILITY-SCORE` | ZHIKU-S5-ORG-CAPABILITY-SCORE | draft | ⓘ+🧪（等权重演示） |
| `ZHIKU-BR-EVAL-SCORE` | ZHIKU-S5-EVAL-SCORE | **missing** | 红问号 → GAP 引用 |

rename 规则：页面引用、metricSeed、readinessSeed 一次性切换，不留双 id；GAP 引用同步正名（`GAP-ZHIKU-BR-COMPETITION-INDEX-权重算法定义卡未落地`、`GAP-ZHIKU-BR-EVAL-SCORE-算法定义卡未落地`）；TRACE §metrics 登记映射。

## 9. 跨模块交接

| 方向 | 契约 | 载体 |
| --- | --- | --- |
| 出 → ZHIKU-WRITING | 竞争格局/成果评估"生成报告"创建预填任务：`createTask({type:'strategy'|'research', title, templateName, outline(含 idea 注入统计数值), materialIds:[]})`，随后路由 `/writing/create?step=outline&task=<id>` | writing taskStore（Pinia，`zhiku-wr:tasks` 持久化） |
| 入 ← 无 | 本模块无上游预填入口 | — |
| 内部回链 | 部署清单热点问题 → issues 页 trend Tab | URL query |

## 10. 自检

- [x] 菜单/路由与现有 4 页保持一致，无新增路由，仅页内信息架构升级。
- [x] 每个统计数字均有 metric_id 挂接方案，两项 missing 指标不出伪 8 件套。
- [x] 跨叶子契约只经 writing taskStore 公开 action，不直改对方 store 内部状态。
- [x] URL 可恢复上下文限定在 issues 页（下钻语义），其余页用持久化恢复，与 UX-SPEC §3 一致。
