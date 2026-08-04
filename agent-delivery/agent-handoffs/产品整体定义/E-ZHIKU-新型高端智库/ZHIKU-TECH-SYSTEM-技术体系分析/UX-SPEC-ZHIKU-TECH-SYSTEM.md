# UX-SPEC-ZHIKU-TECH-SYSTEM｜技术体系分析 · 交互规格

> **版本**：v1.0-rework-r4；交互基线遵循《UX-UE 通用交互组件规范》（D10）与 Design.md（D8）

## 1. 任务流与 Frame 映射

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| 体系建管 | 新建 → 树编辑/评估 → 专家会审 | F-TS-01 → F-TS-02 → F-TS-03 |
| 证据分析 | 论文 → 专利 → 项目 → 网络 | F-TS-04…F-TS-07 |
| 报告出口 | 专利深度分析 → 生成报告 | F-TS-05 → CT-TS-01 |

## 2. 状态与转移

- **Tab 态**：`?tab=system|expert|paper|patent|project|network`，非法回落 system。
- **体系编辑**：`?system=<id>` 同步选中体系；删除当前体系后回落到第一个体系并清参。
- **任务状态机**：
  - 论文：`queued → analyzing(进度模拟) → done | failed`；`failed → analyzing`（重新解析）；合并 = 勾选任务归档 + 新任务入列。
  - 专利：`monitoring ↔ paused`；`删除` 需确认。
  - 网络：`created → running(模拟) → done`（由上传生成）。
- **树编辑**：属性修改即时保存（无显式保存按钮，D10 即时反馈范式）；删除节点 Modal.confirm 级联提示。
- **专家意见**：`pending → confirmed`（单向幂等）；回复无限追加。

## 3. 反馈与错误恢复

| 场景 | 反馈 |
| --- | --- |
| 新建体系名空/重名 | 表单 error 提示，不关弹窗 |
| 合并勾选 <2 | 按钮 disabled + Tooltip 说明 |
| 删除体系/节点/任务/关键网络节点 | Modal.confirm / a-popconfirm，含级联影响文案 |
| 导出空矩阵/空网络 | 导出按钮 disabled |
| 上传未选模板 | 生成按钮 disabled + 提示 |
| 各表格/清单无结果 | 局部 EmptyState + 一键恢复 |
| 恢复演示数据 | Modal.confirm 后重置 `zhiku-ts-` 全部 key |

## 4. 组件与可达性

- Arco 组件：a-tabs/a-tree/a-slider/a-comment/a-progress/a-switch/a-upload/a-popconfirm/a-drawer/a-modal/a-table/a-alert。
- 键盘：树节点方向键导航（a-tree 原生）；弹窗 Esc 关闭；表格操作 a-link/a-button 可聚焦。
- D9 角标：4 枚统计卡全部 ⓘ+🧪；序号 19/20 能力说明卡与社群分组、进度模拟等演示能力行内 🧪 标注。

## 5. 机器可读交付契约

```yaml
frames:
  - { id: F-TS-01, route: /strategy/tech-system, query: { tab: system } }
  - { id: F-TS-02, route: /strategy/tech-system, query: { tab: system, system: "<id>" } }
  - { id: F-TS-03, route: /strategy/tech-system, query: { tab: expert } }
  - { id: F-TS-04, route: /strategy/tech-system, query: { tab: paper } }
  - { id: F-TS-05, route: /strategy/tech-system, query: { tab: patent } }
  - { id: F-TS-06, route: /strategy/tech-system, query: { tab: project } }
  - { id: F-TS-07, route: /strategy/tech-system, query: { tab: network } }
stores:
  - { id: useTechSystemStore, file: src/mock/techSystem.ts, persistence_prefix: zhiku-ts-, keys: [systems, opinions, ui] }
  - { id: usePaperTaskStore, file: src/mock/paperAnalysis.ts, persistence_prefix: zhiku-ts-, keys: [paper-tasks] }
  - { id: usePatentTaskStore, file: src/mock/patentAnalysis.ts, persistence_prefix: zhiku-ts-, keys: [patent-tasks] }
  - { id: useProjectTaskStore, file: src/mock/researchProject.ts, persistence_prefix: zhiku-ts-, keys: [project-tasks, project-filters] }
  - { id: useSocialNetworkStore, file: src/mock/socialNetwork.ts, persistence_prefix: zhiku-ts-, keys: [network-tasks, maintain-nodes, network-ui] }
cross_leaf:
  - { id: CT-TS-01, target: useWritingTaskStore.createTask, route: /writing/create }
acceptance_source: USM-ZHIKU-TECH-SYSTEM.md#4
```
