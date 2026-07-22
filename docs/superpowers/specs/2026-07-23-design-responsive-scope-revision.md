# Design.md 中屏与小屏适配边界修订规格

> 日期：2026-07-23
>
> 评审对象：`agent-delivery/Design.md`
>
> 影响系统：科技信息展示系统、科技专题服务系统
>
> 决策 Owner：human:高颖

## 1. 修订目标

将现有 `Design.md` 从含混的“PC 宽屏 / 大屏 / 小屏”表述收敛为两档明确规范：

1. `1440px–1920px` 中屏工作台；
2. `<1440px` 小屏移动端重排。

科技信息展示系统的大屏可视化不在本规范内，由独立大屏规范处理。科技专题服务系统只支持中屏工作台，不提供小屏或移动端版本。

## 2. 已确认适用矩阵

| 视口宽度 | 科技专题服务系统 | 科技信息展示系统 | 本规范责任 |
| --- | --- | --- | --- |
| `>1920px` | 不定义 | 大屏可视化另行设计 | 明确排除，不提供拉伸规则 |
| `1440px–1920px` | 支持 | 支持 | 共同遵守中屏工作台规范 |
| `<1440px` | 不支持 | 支持移动端重排 | 只定义展示系统的小屏结构与触控规则 |

`1920px` 是中屏上限而不是大屏下限。任何大屏看板、拼接屏、超宽屏、驾驶舱或无导航全屏可视化均不得从本文件推导。

## 3. 中屏工作台规则

### 3.1 基准与栅格

- 基准画布为 `1920 × 1080`，支持宽度区间为 `1440px–1920px`。
- 页面保持 `24 columns`，`gutter` 固定为 `16px`。
- Header 高度固定为 `64px`。
- Sidebar 展开宽度为 `200px`，收起宽度为 `64px`。
- 主内容外边距使用 `16px`。
- 展开态基准为 `offset 200 / 24 columns / 56px column / 16px gutter`。
- 收起态基准为 `offset 64 / 24 columns / 62px column / 16px gutter`。

### 3.2 中屏断点行为

| 视口宽度 | 默认导航 | 工作区策略 |
| --- | --- | --- |
| `1680px–1920px` | 展开或保持用户选择 | 保留左控制、中央主视图、右分析三段式；优先保证中央主视图面积 |
| `1440px–1679px` | 默认收起至 `64px` | 仍保持 24 栅格；左控制区可压缩或折叠，右分析区取规范低宽度，但不得切换为移动端布局 |

科技专题服务系统在整个支持区间内保持中屏 PC 工作台，不使用移动端导航、底部抽屉或触控优先替代交互。

## 4. 展示系统小屏移动端重排

`<1440px` 时，科技信息展示系统不继续压缩中屏三栏，也不保持中屏 24 栅格。页面改为移动端任务顺序：

1. 顶部应用栏与上下文摘要；
2. 区域、时间、领域等筛选入口；
3. 地图、图谱或核心可视化主视图；
4. 底部分析抽屉承接趋势、排行、详情和下钻；
5. 左侧导航改为抽屉或明确的移动端导航入口。

小屏规则：

- 触控目标最小尺寸为 `44px × 44px`；
- 筛选默认折叠为摘要，不允许横向溢出；
- 分析抽屉支持半屏和全屏状态，并保留明确退出路径；
- 地图工具、图例和全屏退出控件不得因重排消失；
- loading、empty、error 和权限态保持主视图尺寸稳定；
- 不允许把中屏三栏等比例缩小后称为移动端适配；
- 不要求移动端沿用中屏 24 栅格，可采用适合触控的单列或局部分栏结构。

## 5. 本轮同步修订

除适配边界外，本轮一并处理已确认的规范与实现漂移：

1. 将 `Design.md` 中的“PC 宽屏”“大屏策略”等表述统一为“中屏工作台”，并更新生成检查清单。
2. 修正最小页面模板中原生 `<label>` 与 Arco `Select`、`DatePicker` 的复合控件嵌套，使用 `Form.Item` 或等价的标签关联结构。
3. 将 `E-PROD-UXUE-COMP-L03` 从互相矛盾的 `ready + completed_at` 收敛为与评审单一致的 `done`。
4. 将专题系统 Demo 壳层从 `224px / 68px` 收敛到 `200px / 64px`，保留现有业务交互和无障碍状态。
5. 更新 `design-tokens.css` 中“不引入 Arco”的过时说明，使其与实际依赖和 `Design.md` 一致。
6. 修订趋势语义检查器，使其验证仍存在的趋势渲染宿主，不强迫已不展示 KPI 趋势文本的页面保留无意义字符串。
7. 同步更新 `gkx-ui-design-standards`、`gkx-product-definition-package`、`gkx-definition-to-demo` 三个复用技能，防止后续产品定义和 Demo 交付重新推导出旧屏幕边界。

## 6. 文件边界

计划修改：

- `gkx-orchestration/agent-delivery/Design.md`
- `gkx-orchestration/agent-delivery/task-registry.yaml`
- `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/Design-通用交互组件栅格体系-轻量评审单.md`
- `repos/demo-ui-topic/src/styles/theme.css`
- `repos/demo-ui-topic/src/styles/design-tokens.css`
- `repos/demo-ui-topic/scripts/check-design-contract.mjs`
- `repos/demo-ui-topic/scripts/check-trend-semantics.mjs`
- `~/.codex/skills/gkx-ui-design-standards/SKILL.md`
- `~/.codex/skills/gkx-ui-design-standards/references/source-map.md`
- `~/.codex/skills/gkx-ui-design-standards/scripts/check-responsive-scope.mjs`
- `~/.codex/skills/gkx-product-definition-package/SKILL.md`
- `~/.codex/skills/gkx-definition-to-demo/SKILL.md`

不修改业务四件套、数据血缘语义、交付 Tier、评审挂载清单和具体业务页面信息架构。

## 7. 验收设计

### 7.1 文档契约

- 适用矩阵明确包含三段宽度边界及两个系统的支持状态；
- `>1920px` 被明确排除；
- 专题系统 `<1440px` 明确不支持；
- 展示系统 `<1440px` 明确采用移动端重排；
- 中屏上限、下限、Header、Sidebar、栅格和 gutter 数值一致；
- 最小页面模板不存在原生 `<label>` 包裹 Arco 复合控件。

### 7.2 工程契约

- `npm run design:check` 通过；
- 趋势语义专项检查通过；
- 复合控件标签审计通过；
- `npm run build` 通过；
- 在 `1920px`、`1680px`、`1440px` 三个视口验证 Header、Sidebar 和主内容边界；
- 修改不引入 `antd`、Emoji 图标、第二套设计系统或业务逻辑变化。

### 7.3 技能契约

- `gkx-ui-design-standards` 明确中屏、小屏和大屏三段边界及系统适用矩阵；
- `gkx-product-definition-package` 使用 `medium_1440_1920`、`small_reflow`、`large_screen_track_l` 三个 `screen_tier` 值，并阻止专题系统声明小屏；
- `gkx-definition-to-demo` 按 `screen_tier` 分流 Design 约束，Track-L 不继承中屏壳层；
- 三个技能分别通过 `quick_validate.py`；
- 响应式范围契约脚本通过，并能在缺失任一关键边界时失败；
- `agents/openai.yaml` 与更新后的技能触发范围仍一致，无需变更时保持原样。

### 7.4 状态一致性

- 评审单和任务登记对 `E-PROD-UXUE-COMP-L03` 均显示 `done`；
- R2 在壳层尺寸和中屏断点验证完成后关闭；
- 既有无关工作区改动不被纳入本轮提交。

## 8. 非目标

- 设计或实现科技信息展示系统的大屏可视化；
- 为科技专题服务系统新增移动端；
- 在本轮完整实现科技信息展示系统全部移动端页面；
- 修改业务模块 IA、指标、权限、数据或评审追溯规则；
- 将中屏规范扩展到超宽屏、拼接屏或驾驶舱。
