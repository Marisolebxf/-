# Design.md 通用交互组件与 24 栅格体系轻量评审单

> **任务 ID**：E-PROD-UXUE-COMP-L03  
> **上游任务**：E-PROD-UXUE-COMP-L02  
> **评审对象**：`agent-delivery/Design.md`  
> **评审方式**：轻量评审，不做 UI/UE 和 QA 审核  
> **评审角色**：Frontend / coordinator  
> **状态**：pending

## 1. 评审范围

本评审只确认 `Design.md` 中以下新增/调整内容是否可执行、可验收、编排一致：

- 通用交互组件：顶部导航、左侧导航、一级 Tab、二级圆角 Tab、按钮组。
- 地图基础图例 / 热力强度图例。
- Arco 外围 + 图表 / 地图 / 图谱可视化内核边界。
- 24 栅格体系：展开态 `offset 200 / 24 columns / 56px column / 16px gutter`，收起态 `offset 64 / 24 columns / 62px column / 16px gutter`。
- 栅格复用层级：页面级、卡片级、表单级、浮层级。
- 间距 token：`4 / 8 / 12 / 16 / 24 / 32`，筛选区默认 `16px`，宽松场景 `24px`，不使用 `20px` 字段 gap。
- 断点策略和 `Design.md §14` 检查 / 验收清单。

## 2. 不审范围

- 不做 UI/UE 审核。
- 不做 QA 审核。
- 不重新评审 Figma 视觉稿。
- 不改业务代码。
- 不评审具体业务页面的信息架构、权限逻辑或数据口径。
- 不新增独立 `UI-通用交互组件视觉规范.md`。

## 3. Frontend 审核项

| 检查项 | 结论 | 备注 |
| --- | --- | --- |
| 24 栅格、`16px gutter`、展开/收起态 offset 可用 CSS 实现 | 待审核 |  |
| 断点策略可落到工程，不会破坏主视图优先原则 | 待审核 |  |
| 顶部/左侧导航作为 Figma 定制组件 + Arco 语义可实现 | 待审核 |  |
| 一级 Tab、二级圆角 Tab、按钮组边界清楚，可封装复用 | 待审核 |  |
| 图表 / 地图 / 图谱由专业内核承载，Arco 只做外围的边界可执行 | 待审核 |  |
| `20px` 字段 gap 收敛为 `16px / 24px` 可落地 | 待审核 |  |

## 4. Coordinator 审核项

| 检查项 | 结论 | 备注 |
| --- | --- | --- |
| `task-registry.yaml` 中 L02 已指向 `evidence: Design.md` | 待审核 |  |
| L03 轻量评审任务依赖 L02，范围不包含 UI/UE | 待审核 |  |
| 派单话术与任务登记口径一致：直接完善 `Design.md`，不另起 handoff | 待审核 |  |
| 本轮提交记录可追踪 | 待审核 |  |

## 5. 评审结论

| 角色 | 结论 | 审核人 / 记录 | 日期 |
| --- | --- | --- | --- |
| Frontend | 待审核 |  |  |
| Coordinator | 待审核 |  |  |

## 6. 问题与处理建议

| 编号 | 问题 | 严重级别 | 处理建议 | 状态 |
| --- | --- | --- | --- | --- |
| R1 |  |  |  | open |

## 7. 关闭条件

- Frontend 和 coordinator 均给出通过或有条件通过结论。
- 如有阻塞问题，需回到 `Design.md` 修订后再复核。
- 关闭时将 `task-registry.yaml` 中 `E-PROD-UXUE-COMP-L03` 更新为 `done`，并记录最终提交 hash。
