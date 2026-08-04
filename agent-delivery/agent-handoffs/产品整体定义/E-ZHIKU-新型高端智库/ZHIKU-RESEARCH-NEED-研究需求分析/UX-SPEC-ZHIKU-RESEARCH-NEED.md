# UX-SPEC-ZHIKU-RESEARCH-NEED｜研究需求分析 · 交互规格

> **版本**：v1.0-rework-r4；交互基线遵循《UX-UE 通用交互组件规范》（D10）与 Design.md（D8）

## 1. 任务流与 Frame 映射

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| 发现研究对象 | 筛选实体 → 下钻画像 → 相似扩展 | F-RN-01 → F-RN-02 |
| 技术观察 | 颠覆卡 → 前沿详情 → 关注 | F-RN-03 |
| 趋势速览 | 标签过滤 → 摘要 → 深挖跳转 | F-RN-04 → CT-RN-02 |
| 舆情研判 | 层次过滤 → 预警处理 → 生成报告 | F-RN-05 → CT-RN-01 |

## 2. 状态与转移

- **Tab 态**：`?tab=entity|frontier|trend|media`，切换 replace 路由；非法值回落 entity。
- **详情态**：`?entity=<id>` 打开 F-RN-02 抽屉；非法 id → Message.warning + 清参回落。
- **导入流**：idle → 选择文件（演示）→ 确认（loading ≥600ms）→ 摘要 Message + 新实体置顶（isImported 标记）→ 幂等：重复项跳过。
- **预警处理**：未处理 → 已处理（单向，demo 不提供撤销；已处理分组可折叠查看）。
- **关注/取关**：toggle 幂等；关注区实时同步。

## 3. 反馈与错误恢复

| 场景 | 反馈 |
| --- | --- |
| 筛选/标签/层次无结果 | 局部 EmptyState + 一键恢复按钮（清空筛选/清空标签/查看全部层次） |
| 导入未选文件 | Message.warning，弹窗不关闭 |
| 非法 URL 参数 | Message.warning + 回落默认态 |
| 生成报告 | Modal.confirm 说明将创建预填任务 → 成功 Message + 路由跳转 |
| 恢复演示数据 | Modal.confirm 后重置 `zhiku-rn-` 全部 key |

## 4. 组件与可达性

- 组件全用 Arco：a-tabs/a-input-search/a-select/a-radio-group/a-card/a-table/a-drawer/a-modal/a-tag(checkable)/a-collapse。
- 键盘：抽屉/弹窗 Esc 关闭；表格行操作用 a-link 可聚焦；标签过滤可 Tab 聚焦 + Enter 切换。
- 状态角标遵循 D9：统计数字 → ⓘ MetricSpecCard（8 件套+就绪度四行）→ 🧪 MockBadge；演示能力（导入校验/相似推荐/自动挖掘/图谱联动）行内 🧪 文案标注。

## 5. 机器可读交付契约

```yaml
frames:
  - { id: F-RN-01, route: /strategy/research-need, query: { tab: entity } }
  - { id: F-RN-02, route: /strategy/research-need, query: { tab: entity, entity: "<id>" } }
  - { id: F-RN-03, route: /strategy/research-need, query: { tab: frontier } }
  - { id: F-RN-04, route: /strategy/research-need, query: { tab: trend } }
  - { id: F-RN-05, route: /strategy/research-need, query: { tab: media } }
stores:
  - id: useResearchNeedStore
    file: src/mock/researchNeed.ts
    persistence_prefix: zhiku-rn-
    keys: [entities, import-cursor, filters, ui, frontier-follows, media-handled]
cross_leaf:
  - { id: CT-RN-01, target: useWritingTaskStore.createTask, route: /writing/create }
  - { id: CT-RN-02, target: route, route: /strategy/tech-trend?tab=hotspot }
acceptance_source: USM-ZHIKU-RESEARCH-NEED.md#4
```
