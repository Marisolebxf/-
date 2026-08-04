# UX-SPEC-ZHIKU-SMART-QUERY｜智能问数 交互规格

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **交互基线**：UX-UE 通用交互组件规范.md（D10）；视觉 token 以 Design.md 为准

## 1. 用户旅程与任务流

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| J1 接入 | 新增数据源 → 测试连接 → 保存 → 查看语义映射/质检 | F-SQ-01 |
| J2 问数 | 新建会话 → 多轮追问 → 图表切换 → 收藏/导出 | F-SQ-02 |
| J3 看板 | 新建看板 → 页管理 → 拖拽组件 → 保存 → 手动刷新 | F-SQ-03 |
| J4 报告 | 勾收藏 → 占位符预览 → 数据校验 → 写作大纲确认 | F-SQ-04→WRITING |

## 2. 状态机

**数据源**：`(新建·测试中) → 正常 ⇄ 停用`；测试失败停留表单态可重试。
**问数轮次**：`asking(识别→SQL→图表 三阶段) → hit | miss`；miss 为终态但可一键重试生成新轮。
**看板**：集合 CRUD；页 append/remove（≥1 拦截）。
**生成校验**：`pass | warning(双选项) `；warning 选择"仍然生成"后照常走 CT-SQ-01。

## 3. 表单与校验

| 表单 | 规则 | 反馈 |
| --- | --- | --- |
| 新增数据源 | 类型必选、名称/连接串非空、测试通过才可保存 | 逐项标红；失败原因面板 |
| 提问 | 非空 | 输入框标红 |
| 新建/重命名看板、会话重命名 | 名称非空 | 标红拦截 |

## 4. 反馈与恢复

- 识别中三阶段文案顺次呈现（识别意图→生成 SQL→生成图表），约 1s，禁止跳过导致闪烁。
- 未命中样例：`a-alert(info)` + 可试问题 tag 一键填入，明确"正式环境由智谱大模型解析"，不返回伪造数据。
- 停用数据源联动：问数轮内 warning + "去启用"跳转；一键报告校验清单中呈现为警告项。
- 删除会话/看板均 `Modal.confirm`；最后一页删除拦截 `Message.warning`。
- 手动刷新：按钮 loading + 时间戳更新 + `Message.success('已刷新（🧪 演示数据重采样）')`。

## 5. 键盘与无障碍

- 提问输入框 Enter 提交；SQL 折叠面板可 Tab/Enter 展开。
- 会话列表项/看板卡为可聚焦元素，Enter 进入。
- 归属声明 Alert 使用 `role=alert` 语义，可折叠不可永久移除（会话级重现）。

## 6. ReviewMode 与 D9

- 三枚统计指标 MetricCard ⓘ + 🧪；无算法得分类指标（NL2SQL 质量不设伪指标）。
- 🧪 常驻：测试连接、语义映射、质检清单、SQL 样例、占位符替换、数据校验、定时刷新说明、看板演示数据。

## 7. 机器可读交付契约

```yaml
frames: [F-SQ-01, F-SQ-02, F-SQ-03, F-SQ-04]
route: { name: strategy-smart-query, query: { tab: source|query|dashboard|report, session: QS-id, dashboard: DB-id } }
stores:
  - id: useSmartQueryStore
    persist_prefix: zhiku-sq-
    keys: [sources, sessions, favorites, dashboards, generations, ui]
    actions: [addSource, testConnection, toggleSource, createSession, renameSession, removeSession, ask, setTurnChartType, toggleFavorite, exportTurnCsv, createDashboard, renameDashboard, removeDashboard, refreshDashboard, createGeneration, resetToSeed]
  - id: useDashboardBuilderStore
    note: S3 收编（页/组件拖拽层），存储 key zhiku-dashboard-pages-v1 保留
cross_contracts:
  - { id: CT-SQ-01, to: useWritingTaskStore.createTask, prefill: [title, templateName, outline(idea=各收藏结果问题+结论摘要)] }
ownership_banner: { text: "55/56/58 智谱、57 智树承建；本页为集成边界演示", persistent: session-level }
acceptance_source: USM-ZHIKU-SMART-QUERY.md#4
```
