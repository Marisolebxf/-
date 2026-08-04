# UX-SPEC-ZHIKU-STRATEGY-ROADMAP｜领域技术线路 交互规格

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **交互基线**：UX-UE 通用交互组件规范.md（D10）；视觉 token 以 Design.md 为准

## 1. 用户旅程与任务流

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| J1 专家共识 | 概览 → 新建问卷 → 发放 → 跟踪回收/催办 → 归档 → 结果研判 | F-RM-01→02 |
| J2 路线设计 | 概览/列表 → 新建路线 → 设计器编辑里程碑 → 保存快照 → 生成报告 | F-RM-01→03→WRITING |
| J3 进展同步 | 开发精度总览 → 子项明细 | F-RM-04 |

## 2. 状态机

**问卷**：`draft → distributing → collecting → archived`（单向；collecting 满员自动 archived 或手动归档）。
**路线项目进度**：派生态 = done 里程碑数 / 总数，无独立状态机。
**快照**：append-only；`restore(snapId)` 前置动作 = `saveSnapshot(auto)`。

## 3. 表单与校验

| 表单 | 规则 | 反馈 |
| --- | --- | --- |
| 新建问卷 | 标题非空；专家数 ≥1；截止 ≥ 今天 | 逐项标红，弹窗不关闭 |
| 新建路线 | 名称非空；start ≤ end | 同上 |
| 里程碑 | 名称非空；日期在项目周期内，否则双选项（扩展周期/改日期） | Modal.confirm 双按钮 |

## 4. 反馈与恢复

- 所有破坏性动作（删除里程碑、恢复快照、生成报告跳转）走 `Modal.confirm`；恢复快照附带"当前态已自动另存"success 提示。
- 催办幂等窗口 5 分钟：重复触发 `Message.info('刚刚已催办')`，不追加记录。
- 局部 Empty 一律带恢复动作按钮（清空筛选/查看全部/双入口）。
- 模拟推进（问卷回收）由 store 定时器驱动，页面重进时 `resumeTimers()` 续跑，不出现"卡死进度"。

## 5. 键盘与无障碍

- 弹窗表单 Enter 提交、Esc 关闭（Arco 默认语义保留）。
- 时间轴节点为 button 语义，可 Tab 聚焦、Enter 打开编辑。
- 状态色不作为唯一信息载体：阶段/状态均带文字 Tag。

## 6. ReviewMode 与 D9

- 所有统计数字 MetricCard 自带 ⓘ + 🧪（mock），弹卡含 8 件套与就绪度四行。
- 演示态能力常驻标注：问卷分发/答复推进、开发精度口径。

## 7. 机器可读交付契约

```yaml
frames: [F-RM-01, F-RM-02, F-RM-03, F-RM-04]
route: { name: strategy-tech-roadmap, query: { tab: overview|delphi|roadmap|precision, project: rm-id } }
stores:
  - id: useTechRoadmapStore
    persist_prefix: zhiku-rm-
    keys: [surveys, projects, ui]
    actions: [createSurvey, advanceStage, remindSurvey, archiveSurvey, createProject, upsertMilestone, removeMilestone, saveSnapshot, restoreSnapshot, setFilters, resetToSeed]
cross_contracts:
  - id: CT-RM-01
    to: useWritingTaskStore.createTask
    prefill: [title, templateName, outline(idea 注入里程碑统计/快照说明)]
acceptance_source: USM-ZHIKU-STRATEGY-ROADMAP.md#4
```
