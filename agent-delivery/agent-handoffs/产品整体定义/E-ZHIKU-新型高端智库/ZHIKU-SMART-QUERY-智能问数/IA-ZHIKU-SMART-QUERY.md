# IA-ZHIKU-SMART-QUERY｜智能问数 信息架构

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **上游**：USM-ZHIKU-SMART-QUERY.md（同目录）
> **原始需求**：拆解表 §2.7 序号 55-58（55/56/58 智谱、57 智树承建；本叶子=集成边界演示）

## 1. 来源与目标

| 项 | 内容 |
| --- | --- |
| 需求来源 | 新型高端智库需求拆解.md §2.7 智能问数（4 项） |
| 模块目标 | "大白话拿数据结论"的端到端演示：接入→问数→看板→一键报告 |
| 承接批次 | R5（收编 S1 smart-query 页 + S3 dashboardBuilder 拖拽编辑器） |

## 2. 覆盖与不覆盖

- **覆盖**：数据源接入管理（四类连接器/模拟测试/停启用/语义映射/质检状态）、多轮问数会话（持久化/收藏/CSV 导出/图表切换/诚实边界）、看板集合管理（标签/搜索/CRUD）+ 多页拖拽编辑、一键报告（占位符预览/数据校验/写作预填）。
- **不覆盖**：真实数据库连接、NL2SQL/大模型解析、模板解析引擎、定时刷新调度、语音输入（以上均为智谱/智树承建能力，🧪 代演）。

## 3. 产品角色与权限

| 角色 | 可见范围 | 关键动作 |
| --- | --- | --- |
| `ROLE-SQ-ADMIN` | 数据接入 | 新增/测试/停启用数据源 |
| `ROLE-SQ-ANALYST` | 问数/一键报告 | 会话问答、收藏、导出、生成报告 |
| `ROLE-SQ-DESIGNER` | 数据看板 | 看板 CRUD、拖拽编辑 |

demo 单用户代演；角色确认挂 Q-ZHIKU-01。

## 4. 对象与稳定标识

| 对象 | id 规则 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| DataSource 数据源 | `DS-<ts>`（种子 DS-01…） | 新建(测试通过)→正常⇄停用 | `zhiku-sq-sources` |
| QuerySession 会话 | `QS-<ts>` | 新建→追加轮次→删除（确认） | `zhiku-sq-sessions` |
| QueryTurn 轮次 | 内嵌 | 追加；命中/未命中两态 | 随会话 |
| FavoriteResult 收藏 | 引用 sessionId+turnId | 收藏⇄取消（幂等） | `zhiku-sq-favorites` |
| DashboardMeta 看板 | `DB-<ts>`（种子 DB-01…） | CRUD+标签 | `zhiku-sq-dashboards` |
| DashboardPage/Widget | 沿用 dashboardBuilder | 页/组件 CRUD | `zhiku-dashboard-pages-v1`（S3 遗留 key，收编保留，TRACE 登记） |
| SqGeneration 生成记录 | `SQGEN-<ts>` | 追加 | `zhiku-sq-generations` |

## 5. IA 结构与 Frame 职责

```
智能问数 /strategy/smart-query（常驻承建归属 Alert）
├─ Tab 数据接入   F-SQ-01 统计卡 + 数据源卡片 + 新增(测试连接) + 详情抽屉(语义映射/质检)
├─ Tab 智能问数   F-SQ-02 会话列表 | 多轮问答流(SQL/图表/表格) + 收藏 + 导出 CSV
├─ Tab 数据看板   F-SQ-03 看板集合(搜索/标签/CRUD) → 编辑器(多页+组件库拖拽，DashboardCanvas)
└─ Tab 一键报告   F-SQ-04 收藏勾选 + 占位符预览 + 数据校验清单 + 生成历史
```

| Frame | 责任 | 关键状态 |
| --- | --- | --- |
| F-SQ-01 | 接入管理 | 测试中/失败重试、停用态 |
| F-SQ-02 | 问数会话 | 识别中三阶段、未命中诚实态、停用源联动提示 |
| F-SQ-03 | 看板管理+编辑 | 集合空态、最后一页拦截 |
| F-SQ-04 | 一键报告 | 无收藏 Empty、校验警告双选项 |

## 6. 数据与服务边界

- 全 mock：领域 store `useSmartQueryStore`（sources/sessions/favorites/dashboards meta/generations），reducer 式 action + `makePersist('zhiku-sq-')`；页内拖拽复用 `useDashboardBuilderStore`（S3 遗留存储 key 保留）。
- 目标态：智谱问数服务 + 智树看板服务经 Java REST 聚合接入；本前端不直连。
- NL2SQL 命中逻辑 = 预置样例匹配；未命中一律诚实提示，禁止伪造结果。

## 7. 指标（D9）

| metric_id | 中文名 | 位置 | 状态 |
| --- | --- | --- | --- |
| `ZHIKU-SQ-SOURCE-CONNECTED` | 接入数据源数（正常态） | F-SQ-01 | 新增 draft/mock |
| `ZHIKU-SQ-SESSION-TOTAL` | 问数会话总数 | F-SQ-02 | 新增 draft/mock |
| `ZHIKU-SQ-DASHBOARD-TOTAL` | 数据看板总数 | F-SQ-03 | 新增 draft/mock |

## 8. 跨模块契约

| 契约 | 方向 | 载荷 | 说明 |
| --- | --- | --- | --- |
| CT-SQ-01 一键生成数据报告 | ZHIKU-SMART-QUERY → ZHIKU-WRITING | `createTask`(type=research，大纲注入结果问题+结论摘要) | 生成历史留痕+任务回链 |
| 承建归属声明 | UI 常驻 | 55/56/58 智谱、57 智树 | 四 Tab Alert，不可永久关闭 |
