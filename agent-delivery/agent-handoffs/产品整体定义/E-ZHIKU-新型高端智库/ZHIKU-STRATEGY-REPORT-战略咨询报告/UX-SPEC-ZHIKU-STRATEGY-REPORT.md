# UX-SPEC-ZHIKU-STRATEGY-REPORT｜战略咨询报告与成果 交互规格

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **交互基线**：UX-UE 通用交互组件规范.md（D10）；视觉 token 以 Design.md 为准

## 1. 用户旅程与任务流

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| J1 资产沉淀 | 上传研报 → 🧪 解析加工 → 编辑/版本/归档 | F-SP-01 |
| J2 洞察消费 | 月刊浏览 → 订阅 → 推送记录 → 导出 | F-SP-02 |
| J3 热点研判 | 三方向切换 → 榜单 → 四源构成下钻 → 回链月刊 | F-SP-03→02 |
| J4 战略生成 | 勾底料 → 要点预览 → 生成 → 写作大纲确认 → 发布 → 成果区 | F-SP-04→WRITING→F-SP-05 |
| J5 成果展示 | 四统计卡 → ROI 筛选 → 案例详情 | F-SP-05 |

## 2. 状态机

**研究报告**：`parsing → ready →（archived）`；删除为终止态，被生成记录引用时删除被拦截。
**版本**：append-only（v1..n），编辑元信息不升版本，重传升版本。
**订阅**：布尔开关幂等；退订即停推送（已有推送记录保留）。
**生成记录**：append-only；底料删除后记录标 `invalid_source`。

## 3. 表单与校验

| 表单 | 规则 | 反馈 |
| --- | --- | --- |
| 上传报告 | 文件已选（演示）、标题非空、行业已选 | 逐项标红，弹窗不关闭 |
| 编辑元信息 | 标题非空 | 同上 |
| 生成报告 | 至少 1 份底料 | 按钮禁用 + tooltip |

## 4. 反馈与恢复

- 删除报告：`Modal.confirm`；被引用时改为 `Modal.warning` 列出引用记录，不提供强删。
- 解析中条目：行内 loading 标签 + 详情骨架屏；解析完成 `Message.success`。
- ROI 筛选：统计卡选中态描边 + 案例区 Banner"当前仅显示 ROI 高于均值案例 [查看全部]"。
- 所有 Empty 带恢复/引导动作按钮。

## 5. 键盘与无障碍

- 详情抽屉/弹窗 Esc 关闭；表格行操作按钮可 Tab 聚焦。
- 热度指数红问号为 button 语义，Enter 打开治理引用说明。
- 状态色均伴随文字 Tag，不以颜色为唯一载体。

## 6. ReviewMode 与 D9

- 全部统计数字 MetricCard ⓘ + 🧪；`ZHIKU-SP-HOTSPOT-INDEX` 为 D1 missing 红问号，点开只显 GAP 治理引用，不显伪 8 件套。
- 🧪 常驻标注：自动摘要/关键词/标签/质检、洞察专题、推送、四源构成、脱敏、推荐、投资/ROI/满意度口径。

## 7. 机器可读交付契约

```yaml
frames: [F-SP-01, F-SP-02, F-SP-03, F-SP-04, F-SP-05]
routes:
  - { name: strategy-report-mgmt, query: { tab: research|insight|hotspot|generate } }
  - { name: strategy-case-show }
  - { name: writing-cases, note: 案例区共享数据源 }
stores:
  - id: useStrategyReportStore
    persist_prefix: zhiku-sp-
    keys: [research, generations, insightSub, insightPush, ui]
    actions: [uploadReport, editReport, addVersion, archiveReport, removeReport, exportReport, toggleSubscription, exportIssue, createGeneration, setFilters, resetToSeed]
  - id: useStrategyCaseStore
    persist_prefix: zhiku-sp-
    keys: [caseUi]
    actions: [setIndustryFilter, toggleRoiSpotlight]
cross_contracts:
  - { id: CT-SP-01, to: useWritingTaskStore.createTask, prefill: [title, templateName, outline(idea=底料要点)] }
  - { id: CT-WR-承接, from: useWritingTaskStore.published, mode: readonly }
acceptance_source: USM-ZHIKU-STRATEGY-REPORT.md#4
```
