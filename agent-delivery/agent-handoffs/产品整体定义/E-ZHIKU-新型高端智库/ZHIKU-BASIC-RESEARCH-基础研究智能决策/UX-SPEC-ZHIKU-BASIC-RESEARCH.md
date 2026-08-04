# UX-SPEC-ZHIKU-BASIC-RESEARCH｜基础研究智能决策·体验规格

> **版本**：v1.0-rework-r2（AI 起草，待人确认）
> **一致性**：与 USM v1.0-rework-r2 / IA / Wireframe / TRACE 同步；交互底线遵循《UX-UE 通用交互组件规范》，视觉 token 遵循 Design.md。

## 1. 与五件套一致性检查

- 故事 7 条（US-ZHIKU-BR-01…07）↔ Frame 6 个（F-BR-01…06）↔ 页面 4 个（issues/deploy/org/eval）映射闭合，无孤儿 Frame。
- 指标 6 枚全部有 metric_id 与就绪度呈现方案；两项 D1 missing（竞争格局指数/成果评估得分）不出伪 8 件套。

## 2. 用户旅程

| 旅程 | 路径 | 关键体验点 |
| --- | --- | --- |
| BR-J01 问题订阅 | issues(list) 筛选→订阅→刷新验证 | 筛选叠加即时反馈；订阅双处同步；持久化 |
| BR-J02 识别入库 | 识别🧪→loading→新问题置顶→在线发布→总数+1 | loading 禁用防并发；池尽空态；发布状态流转 |
| BR-J03 趋势研判 | list→查看趋势→URL 下钻→预警处理→推荐跳转 | 上下文可分享可刷新；预警分组处理 |
| BR-J04 竞争研判出报告 | competition→层次切换→图型切换→生成报告→写作大纲页 | 跨叶子无缝；预填大纲含统计思路 |
| BR-J05 部署联动 | deploy 筛选→表↔图互点→热点回链 issues | 双向选中同一 id；筛选空态可恢复 |
| BR-J06 配置跟踪 | org 看短板→建议纳入跟踪→刷新验证 | 幂等；跟踪清单计数 |
| BR-J07 评估出报告 | eval 切成果→切子视图→生成评估报告 | 状态恢复；跨叶子出口同 J04 |

## 3. 状态持久化与上下文恢复

| 状态 | 载体 | key（前缀 `zhiku-br-`） |
| --- | --- | --- |
| issues Tab 与当前问题 | **URL query**（tab/issue，可分享） | — |
| 问题清单本体（含新识别） | localStorage | `zhiku-br-issues` |
| 订阅集合 | localStorage | `zhiku-br-subscriptions` |
| 已处理预警 | localStorage | `zhiku-br-alerts-handled` |
| 识别候选池游标 | localStorage | `zhiku-br-identify-cursor` |
| 筛选条件（issues/deploy） | localStorage | `zhiku-br-filters` |
| 竞争层次 / 部署选中 / 评估成果 / 评估子视图 | localStorage | `zhiku-br-ui` |
| 建议跟踪集合 | localStorage | `zhiku-br-suggestions` |

规则：URL 承载"可分享的下钻上下文"，localStorage 承载"个人偏好与业务状态"；两者冲突时 URL 优先（issues 页）。所有写入经 store reducer action，视图不得直改 state。

## 4. 交互与状态机

- **问题状态机**：`identifying →(在线发布)→ published`；`新识别 ∧ identifying` 允许"移除"；published 不可移除（demo 无归档）。
- **识别流程**：按钮 click → `loading=true`（禁用）→ 900ms 模拟 → 候选池出栈 1 条置顶入库 → success Message；池空 → info Message"演示数据池已用尽"，提供「恢复演示数据」入口（Modal 确认后 resetToSeed）。
- **预警**：未处理组（按级别红/橙/灰 Tag）→「标记已处理」→ 已处理组（灰、时间戳保留）；无未处理时显示"当前问题暂无预警"。
- **生成报告（跨叶子）**：click → Modal（标题、将创建的任务名、"将创建新的写作任务"提示）→ 确认 → `writingTaskStore.createTask` → `router.push('/writing/create?step=outline&task=')` → 由 ZHIKU-WRITING UX-SPEC 接管；取消 → 无副作用。
- **地图联动**：表格行 click → `setSelectedDeploy(id)` → 地图 flyTo 点位 + 高亮描边；地图 `select-point` → 同一 reducer → 表格行 class 高亮 + 详情侧条刷新；筛选变化时若选中项被过滤掉则清空选中。
- **评估子视图**：radio 切换 `compare|trend`，切换即持久化；单成果对比时显示样本提示。

## 5. 反馈与错误恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| 筛选无结果 | 局部 EmptyState（非整页） | 「清空筛选」按钮 |
| 新识别问题无趋势 | 轨迹图 EmptyState + 统计卡"—" | 引导回清单 |
| URL issue 无效 | 回退默认问题 + warning Message | 重新选择 |
| 候选池耗尽 | info Message + 恢复演示数据入口 | resetToSeed |
| 地图底图失败 | 容器占位 + 刷新按钮（表格不受影响） | 手动重试 |
| 生成报告取消 | 无任何副作用 | — |

所有 Message 持续 3s；破坏性动作（移除问题、恢复演示数据）必须 Modal 二次确认。

## 6. 组件与可达性

- 组件全部 Arco Design Vue：a-tabs/a-table/a-select/a-drawer/a-alert/a-radio-group/a-descriptions/a-list/a-tag；图表 VChart（ECharts）；地图 TalentMapView（Leaflet）。
- 状态图标全部 Arco Icon（禁 emoji 表状态；🧪 仅出现在 MockBadge 语义内）。
- 键盘：表格行操作按钮可 Tab 聚焦；抽屉/Modal ESC 关闭；Tab 切换支持左右键（Arco 默认）。
- 地图点位带 `role=button` 与 aria-label（组件已内置）。

## 7. 内部评审投影（ReviewMode）

- 开：6 枚指标全带 ⓘ/红问号 + 🧪 MockBadge + 就绪度四行区块；missing 两枚点开仅 GAP 治理引用。
- 关：DOM 零泄漏（无 `metric_id`/`GAP-*`/`Q-ZHIKU-*` 字样）；诚实性文案中面向用户的"演示态"说明保留（属产品诚实性而非评审泄漏）。

## 8. demo 实现交接

- store：`src/mock/basicResearch.ts` 重构为领域 store——静态种子 + `state`（issues/subscriptions/alertsHandled/filters/ui/suggestions/identifyCursor）+ reducer 化 actions + `persist()` 统一落盘（`zhiku-br-` 前缀）+ `resetToSeed()`。
- 跨叶子只调 `useWritingTaskStore().createTask(...)` 公开 action；预填大纲 idea 注入当前统计数值（模板化字符串）。
- 页面：4 页 + 3 panel 重构，异常态按 §5 全落地；vue-tsc 0 错、vite build 通过为门禁。

## 9. 缺口与阻塞

| 项 | 状态 | 去向 |
| --- | --- | --- |
| 竞争格局指数权重算法 | def_status=missing | `GAP-ZHIKU-BR-COMPETITION-INDEX-权重算法定义卡未落地`；Q-ZHIKU-04 |
| 成果评估四维算法 | def_status=missing | `GAP-ZHIKU-BR-EVAL-SCORE-算法定义卡未落地`；Q-ZHIKU-04 |
| 产品角色正式确认 | 待甲方 | Q-ZHIKU-01（客户决策清单跟踪表） |
| 真实挖掘模型/预警规则/推送通道 | 不在 demo 范围 | 正式版算法侧任务 |

## 10. 机器可读交付契约

```yaml
module: ZHIKU-BASIC-RESEARCH
frames: [F-BR-01, F-BR-02, F-BR-03, F-BR-04, F-BR-05, F-BR-06]
routes:
  - path: /basic-research/issues
    query: { tab: [list, trend, competition], issue: issueId }
  - path: /basic-research/deploy
  - path: /basic-research/org
  - path: /basic-research/eval
persistence:
  prefix: zhiku-br-
  keys: [issues, subscriptions, alerts-handled, identify-cursor, filters, ui, suggestions]
cross_leaf:
  - from: F-BR-03
    action: writingTaskStore.createTask
    then: /writing/create?step=outline&task=<id>
  - from: F-BR-06
    action: writingTaskStore.createTask
    then: /writing/create?step=outline&task=<id>
metrics:
  - { id: ZHIKU-BR-ISSUE-TOTAL, def: draft }
  - { id: ZHIKU-BR-ISSUE-HEAT-SCORE, def: draft }
  - { id: ZHIKU-BR-COMPETITION-INDEX, def: missing }
  - { id: ZHIKU-BR-DEPLOY-TOTAL, def: draft }
  - { id: ZHIKU-BR-ORG-CAPABILITY-SCORE, def: draft }
  - { id: ZHIKU-BR-EVAL-SCORE, def: missing }
```
