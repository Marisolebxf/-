# GKX 双系统 AI 原型设计规范

> 适用范围：科技信息展示系统、科技专题服务系统。
> 来源：Figma「科技信息展示系统」页面「风格稿-确定」，优先抽取范围为「P00_风格稿_基础框架_菜单展开」「P00_风格稿_基础框架_菜单收起」和「通用交互组件」。该 Figma 风格稿是两个系统共同遵守的工作台骨架、视觉与组件节奏依据，不代表本文只适用于科技信息展示系统。
> 用途：给两个系统的 AI 原型、页面生成、组件补全和多人协作时保持视觉与交互一致性。除非用户明确要求重做风格，否则所有新原型默认继承本文件；业务名称、菜单、指标、筛选字段和数据对象必须按当前系统及页面需求填写，不得默认沿用展示系统业务文案。

## 0. 给 AI 的执行指令

如果你是根据本文件生成页面或原型，必须把本文件当作强约束，而不是灵感参考。

适用边界：PC 工作台骨架、栅格、视觉 token、组件尺寸、交互状态和“控制 - 主视图 - 分析”关系是两个系统共同强约束；当前系统的业务名称、左侧菜单、页面标题、业务对象、指标和筛选字段由对应产品需求决定。

执行优先级：

1. 先复刻本文件定义的 PC 工作台骨架、尺寸、颜色、组件节奏。
2. 再填充业务内容、数据和图表。
3. 最后才考虑局部优化。

不得自行改成：

- 深色数据大屏
- 营销官网
- 通用后台模板
- 玻璃拟态炫光界面
- 大卡片仪表盘
- 自由发挥的渐变科技风

生成前必须先建立以下基础：

- 前端组件库：`@arco-design/web-react`
- 图标库：`@arco-design/web-react/icon`
- 主色：`#165DFF`
- 页面背景：`#D8E7FC`
- 正文字号：`14px`
- 控件高度：`32px`
- 控件圆角：`2px-4px`
- 页面基准：`1920 x 1080`

如果实现出来不像本规范，优先检查：是否用了错误组件库、是否用了错误 token、是否把 Header/Sidebar/控件做得过大、是否加入了深色或发光装饰。

## 1. 设计定位

这是一个面向科技信息展示与科技专题服务、态势感知、专题分析、地图/图谱探索和数据决策的 PC 工作台界面。

不要把它做成官网、营销页、BI 大屏或普通后台管理系统。它的核心体验是：

- 左侧稳定导航定位专题。
- 中央地图/图谱/主视图承担主要探索。
- 右侧分析面板承接结论、趋势、影响力、采类分析和要素比较。
- 顶部筛选条提供区域、时间、领域、关键词等上下文控制。
- 通用组件以 Arco Design 为前端实现基座，遵循 Arco 的企业级交互语义、组件状态和 token 命名；视觉在 Arco 默认浅色体系上更柔和、更偏蓝白科技工作台。

### 1.1 企业标识使用边界

科技专题服务系统不展示企业 Logo 或企业标识：不使用图片 Logo，也不以企业简称、首字或色块作为替代占位。企业卡片、列表、详情/画像、推荐和对比等触点仅以企业名称及业务字段识别对象；系统 Logo 与产品导航标识不受此规则影响。

## 2. 视觉气质

关键词：浅蓝白、轻科技、透明玻璃面板、地图工作台、低阴影、高留白、强结构、弱装饰。

视觉强度：

- 密度：中高密度。信息很多，但通过分区、描边和浅底来降低压迫感。
- 对比：中等对比。主操作和选中态使用蓝色，普通文本和边框保持克制。
- 装饰：低装饰。避免大面积渐变、发光、复杂背景纹理。
- 圆角：中等圆角。面板舒展，控件紧凑。
- 动效：功能性动效。用于展开收起、筛选反馈、地图工具状态，不做炫技动画。

生成新页面时，优先让界面像“科研情报分析工作台”，而不是“数据可视化展厅”。

## 3. 页面骨架

### 3.1 PC 基准画布

Figma 基准为 `1920 x 1080`。

固定结构和尺寸：

| 区域 | 尺寸 / 规则 |
| --- | --- |
| 页面画布 | `1920 x 1080`，全屏工作台，不是滚动长页 |
| 顶部 Header | 高度 `64px`，浅蓝半透明底，不超过 `72px` |
| 左侧导航展开 | 宽度 `200px`，从 Header 下方开始，满高；内容栅格 Offset 为 `200px` |
| 左侧导航收起 | 宽度 `64px`，仅显示图标和 Logo；内容栅格 Offset 为 `64px`，主内容横向扩展 |
| 主内容外边距 | 距离 Header、Sidebar 和窗口边缘均为 `16px` |
| 主内容容器 | 白色半透明，`border: 1px solid #FFFFFF`，圆角 `8-12px` |
| 筛选条 | 高度约 `88-104px`，位于主内容顶部 |
| 工作区 | 左侧图层面板 + 中央地图 + 右侧分析面板 |
| 左侧图层面板 | 宽度 `152-184px` |
| 中央地图区 | 自适应占满剩余空间，最小宽度不能低于右侧分析面板 |
| 右侧分析面板 | 宽度 `440-608px`，根据业务密度选择，不得删除 |

推荐 CSS Grid：

```css
.app-shell {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #d8e7fc;
  color: #1d2129;
  font-family: "PingFang SC", "Inter", system-ui, sans-serif;
}

.app-frame {
  display: grid;
  grid-template-columns: 200px minmax(0, 1fr);
  grid-template-rows: 64px minmax(0, 1fr);
  height: 100%;
}

.app-header {
  grid-column: 1 / -1;
  height: 64px;
  background: rgba(216, 231, 252, 0.88);
  border-bottom: 1px solid rgba(255, 255, 255, 0.72);
}

.app-sidebar {
  width: 200px;
  background: rgba(235, 244, 255, 0.82);
  border-right: 1px solid rgba(255, 255, 255, 0.72);
}

.content-shell {
  margin: 16px;
  min-width: 0;
  min-height: 0;
  border-radius: 10px;
  border: 1px solid #ffffff;
  background: rgba(255, 255, 255, 0.8);
  overflow: hidden;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 184px minmax(560px, 1fr) 520px;
  gap: 16px;
  height: 100%;
}
```

`.workspace-grid` 是 24 栅格之上的业务工作区分区示例，不替代页面级 24 栅格系统。

AI 生成时必须避免把 Header 做成 `84px+`、把左侧导航做成 `240px+`、把控件做成 `38px+`。这些都会偏离风格稿。

### 3.2 24 栅格系统

页面采用 Figma 24 栅格系统。栅格从当前左侧导航右边界开始计算，而不是从整个画布 `x=0` 开始计算。PC 端所有断点下 `gutter` 固定为 `16px`，不得压缩或放大；`columns` 固定为 `24`；响应式变化只调整 `column width` 和左侧导航状态。

| 菜单状态 | 左侧导航宽度 / Offset | Columns | Gutter | 1920 基准 Column width | 1920 基准内容栅格宽 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 展开态 | `200px` | `24` | `16px` | `56px` | `1712px` |
| 收起态 | `64px` | `24` | `16px` | `62px` | `1856px` |

计算规则：

- `contentGridWidth = 24 * columnWidth + 23 * 16`
- `columnWidth = (contentGridWidth - 23 * 16) / 24`
- 展开态基准：`24 * 56 + 23 * 16 = 1712`，从 `x=200` 开始，右侧约 `8px` 安全余量。
- 收起态基准：`24 * 62 + 23 * 16 = 1856`，从 `x=64` 开始，覆盖剩余内容区。
- 菜单展开 / 收起会改变内容区栅格列宽，但保持 `24 columns` 和 `16px gutter` 不变。
- 页面主内容、筛选区、地图 / 图谱主视图、右侧分析面板、卡片和浮层均应优先按 24 栅格对齐。
- 不要在内容区内部另起一套不兼容的 12 栅格或自由像素布局；如局部组件需要内部布局，可在组件内部使用本文件定义的间距 token，但外边界仍需贴合页面 24 栅格。

### 3.3 栅格复用层级

| 层级 | 对齐规则 | 适用对象 |
| --- | --- | --- |
| 页面级 | 使用 24 栅格，`gutter=16px` 固定；页面主内容、大区块、地图区、右侧分析面板外边界必须贴合列线 | `content-shell`、筛选区、`workspace-grid`、地图/图谱主视图、右侧分析面板 |
| 卡片级 | 卡片外边界贴合页面 24 栅格；卡片内部可使用 `2/3/4/6/8/12` 等分栏，不再强制套 24 栅格 | 数据卡片、图表卡片、指标组、排行模块 |
| 表单级 | 表单容器贴合页面或卡片栅格；字段内部按 `label + control` 节奏排布，输入宽度优先使用固定规格或局部分栏 | 筛选条、查询表单、Drawer 表单、Modal 表单 |
| 浮层级 | 抽屉、弹窗、地图浮层外宽按列跨度或固定宽度取值；内部使用间距 token，不另起页面级栅格 | Drawer、Modal、Popover、地图图例 |

### 3.4 间距 token

间距采用 `4px` 基础单位，常用阶梯为 `4 / 8 / 12 / 16 / 24 / 32`。`16px` 同时是页面 24 栅格的固定 gutter。

| Token | 值 | 用途 |
| --- | ---: | --- |
| `--sci-space-1` | `4px` | 图标与文字、紧凑元素内部间距 |
| `--sci-space-2` | `8px` | 表单 label 与控件、按钮内图标间距、Tag 内部间距 |
| `--sci-space-3` | `12px` | 卡片内小组间距、列表行内间距 |
| `--sci-space-4` | `16px` | 页面 gutter、字段默认间距、区块默认间距、卡片 padding 基准 |
| `--sci-space-6` | `24px` | 宽松字段间距、大区块上下间距、复杂表单段落间距 |
| `--sci-space-8` | `32px` | 页面级分组间距、复杂模块之间的大间距 |

规则：

- 表单与筛选区默认字段 gap 使用 `16px`，与页面 24 栅格 gutter 对齐。
- 当字段组信息密度较高、需要更强分组感时，可使用 `24px`。
- 不使用 `20px` 作为字段 gap，避免形成脱离 `4/8/12/16/24/32` 阶梯的中间值。
- 卡片 padding 默认 `16px`，高密度卡片可用 `12px`，复杂内容卡片可用 `16px / 24px`。
- 页面大区块之间优先使用 `16px` 或 `24px`，不要自由写 `17px / 19px / 21px`。

### 3.5 主内容三段关系

默认主工作区采用三段式：

1. 左侧控制 / 图层面板：承载当前页面的要素、维度或视图控制；地图场景可控制专家学者、会议、科研机构、企业、论文、期刊、专利等图层。
2. 中央主视图区：承载地图、图谱、列表矩阵或其他当前页面主视图；地图场景包含热力、点位、图例、视图切换和工具栏。
3. 右侧分析面板：承载当前页面的结论、趋势、对比、明细或操作闭环，不预设具体业务 Tab 名称。

AI 生成时不得只生成一张地图或一组卡片。必须保留“控制 - 主视图 - 分析”的任务闭环。

### 3.6 菜单展开与收起

展开态：

- 左侧导航显示系统名称、图标、一级菜单、二级菜单和展开箭头。
- 当前一级、二级菜单名称取当前系统与页面上下文，不默认写死为展示系统的「科技发展态势 / 科技全域态势」。
- 选中项使用浅蓝底和蓝色文字。

收起态：

- 左侧只保留 Logo、折叠按钮和纵向图标。
- 主内容区域横向扩展，内容栅格从 `x=64` 重新计算；顶部 Header 和整体背景不改变。
- 收起态不是移动端样式，不要出现汉堡抽屉式遮罩。

## 4. 色彩系统

### 4.1 基础色

从 Figma 样式与画面抽取的核心色：

| 语义 | 色值 | 用途 |
| --- | --- | --- |
| 页面底色 | `#D8E7FC` | 整页浅蓝背景 |
| 主面板白 | `#FFFFFFCC` | 内容主容器、右侧分析面板，允许半透明 |
| 纯白 | `#FFFFFF` | 输入框、地图浮层、按钮文字、卡片内容区 |
| 填充浅灰 | `#F7F8FA` | 次级背景、表格浅底、轻量容器 |
| 填充灰 | `#F2F3F5` | hover、禁用浅底、分隔背景 |
| 边框浅灰 | `#E5E6EB` | 输入框、分页、表格、组件描边 |
| 边框中灰 | `#C9CDD4` | 禁用边框、次级分割 |
| 主文字 | `#1D2129` | 正文、菜单、字段值 |
| 次文字 | `#4E5969` | 标签、辅助字段、说明 |
| 弱文字 | `#86909C` | 占位、禁用、次级图例 |
| 品牌主蓝 | `#165DFF` | 主按钮、选中态、链接、激活 tab |
| 品牌浅蓝 | `#E8F3FF` | 选中底、浅色蓝标签、focus 背景 |
| 品牌中蓝 | `#4080FF` | hover、图表主序列 |

必须在新项目里落地为 CSS 变量：

```css
:root {
  --sci-bg-page: #d8e7fc;
  --sci-surface-main: rgba(255, 255, 255, 0.8);
  --sci-surface-solid: #ffffff;
  --sci-surface-soft: #f7f8fa;
  --sci-surface-hover: #f2f3f5;
  --sci-border: #e5e6eb;
  --sci-border-strong: #c9cdd4;
  --sci-text-1: #1d2129;
  --sci-text-2: #4e5969;
  --sci-text-3: #86909c;
  --sci-primary: #165dff;
  --sci-primary-hover: #4080ff;
  --sci-primary-soft: #e8f3ff;
  --sci-map-border: #dce9ff;
  --sci-space-1: 4px;
  --sci-space-2: 8px;
  --sci-space-3: 12px;
  --sci-space-4: 16px;
  --sci-space-6: 24px;
  --sci-space-8: 32px;
  --sci-focus-ring: rgba(22, 93, 255, 0.18);
  --sci-control-active-bg: #ffffff;
  --sci-control-track-bg: #f2f3f5;
  --sci-legend-bg: rgba(255, 255, 255, 0.92);
  --sci-legend-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}
```

禁止把主色替换成 `#2F6DF6`、`#1677FF`、紫蓝渐变或其他“看起来也差不多”的蓝色。这个系统的主色固定是 `#165DFF`。

### 4.2 状态色

沿用 Arco Design 语义，不重新发明状态色。

| 语义 | 主色 | 浅底 |
| --- | --- | --- |
| 成功 | `#00B42A` | `#E8FFEA` |
| 警示 | `#FF7D00` | `#FFF7E8` |
| 错误 | `#F53F3F` | `#FFECE8` |
| 链接 | `#165DFF` | `#E8F3FF` |

### 4.3 业务语义用色

业务语义色用于表达业务含义，不等同于系统状态色。尤其是趋势、增减、涨跌、排名变化等业务指标，必须遵循国内业务阅读习惯：

| 业务语义 | 主色 | 浅底 | 用途 |
| --- | --- | --- | --- |
| 上升 / 增长 / 涨 / 环比为正 | `#F53F3F` | `#FFECE8` | 趋势箭头、增长率、涨幅、排名上升、正向增量 |
| 下降 / 减少 / 跌 / 环比为负 | `#00B42A` | `#E8FFEA` | 趋势箭头、下降率、跌幅、排名下降、负向增量 |

实现建议落地为 CSS 变量：

```css
:root {
  --sci-trend-up: #f53f3f;
  --sci-trend-up-soft: #ffece8;
  --sci-trend-down: #00b42a;
  --sci-trend-down-soft: #e8ffea;
}
```

注意区分：

- `成功 / 警示 / 错误` 仍沿用 Arco 状态色语义；不要因为“成功”是绿色就把业务上升也做绿色。
- 趋势类图表、指标卡、排行升降、同比/环比变化统一使用“上升红、下降绿”。
- 如果业务含义不是涨跌增减，而是风险高低、状态成功失败、任务是否完成，应使用状态色或专门的风险色说明，不套用趋势色。

### 4.4 科技要素与图表色

地图点位、图例、要素分类和图表序列使用以下业务色。它们用于区分类别，不用于基础按钮或页面装饰。

| 要素 | 色值 |
| --- | --- |
| 专家学者 | `#4180FD` |
| 企业 | `#16C7C7` |
| 科研机构 | `#4DD164` |
| 会议 | `#F6BA21` |
| 论文 | `#A872E2` |
| 专利 | `#58A8F9` |
| 服务机构 | `#F779B6` |
| 项目 | `#83DDD3` |
| 课题 | `#78D986` |
| 期刊 | `#FBD08A` |

图表序列优先顺序：

`#4180FD`, `#58A8F9`, `#8DB6F2`, `#96C9ED`, `#16C7C7`, `#83DDD3`, `#4DD164`, `#78D986`, `#FD7E03`, `#F6BA21`, `#FBD08A`, `#A872E2`, `#BA8DE5`, `#F779B6`。

不要在同一张图里使用过多高饱和色。连续量优先使用同一色系渐变，离散分类才使用多色序列。

## 5. 字体与排版

### 5.1 字体

中文界面主字体：

- `PingFang SC`，用于菜单、表单、标签、正文、图例。

英文和数字辅助字体：

- `Inter`，用于框架标题、趋势图、数字、英文标签。
- 如果实现环境无 `Inter`，可降级为 `system-ui`，但不要换成风格强烈的展示字体。

### 5.2 字号层级

| 层级 | 字号 / 行高 | 字重 | 用途 |
| --- | --- | --- | --- |
| 页面/模块大标题 | `18px / 24px` | 600 | 分析面板标题、模块标题 |
| 次级标题 | `16px / 22-24px` | 500-600 | 分组标题、卡片标题 |
| 正文 | `14px / 22px` | 400 | 菜单、字段、表单、列表 |
| 正文强调 | `14px / 22px` | 500 | 选中项、表头、标签强调 |
| 辅助文字 | `12px / 16-20px` | 400 | 图例、占位、注释、分页说明 |
| 小图表刻度 | `10px / 12-15px` | 400 | 坐标轴、小型图表标签 |
| 关键数值 | `24-34px / 35-44px` | 600 | 数据概览、排名、指标值 |

排版规则：

- 中文正文默认 `14px`，不要把业务界面做成大字号展示页。
- 表单标签与菜单保持 `14px`。
- 图表刻度可用 `10px` 或 `12px`，但必须清晰。
- 数字指标可以放大，但要服务分析，不要做成海报式巨字。
- 字距保持 `0`，不要使用负字距。

## 6. 圆角、描边与阴影

### 6.1 圆角

Figma 抽取的常见圆角：`2px`, `4px`, `6px`, `8px`, `10px`, `12px`, `999px`。

推荐规则：

| 对象 | 圆角 |
| --- | --- |
| 页面主内容外壳 | `12-16px` |
| 一级面板 / 大卡片 | `8-12px` |
| 表单输入框 | `2-4px` |
| 按钮 | `2-4px` |
| 标签 / 胶囊 / 用户入口 | `999px` 或 `12px` |
| 地图浮层 | `6-8px` |

不要把所有卡片都做成超大圆角。这个系统是工作台，不是消费级 App。

### 6.2 描边

默认使用 `1px` 描边。

- 常规边框：`#E5E6EB`
- 主容器白色描边：`#FFFFFF`
- 地图/分析区浅蓝边框：`#DCE9FF`
- 分隔线：`#E5E6EB` 或 `#F2F3F5`

描边用于建立结构，不要使用重边框或深色线框。

### 6.3 阴影

阴影轻量、少用。

- 普通浮层：`0 4px 10px rgba(0, 0, 0, 0.05)`
- 下拉/弹层：`0 4px 10px rgba(0, 0, 0, 0.10)`
- 大面板可使用柔和蓝色阴影：`0 8px 18px rgba(107, 143, 235, 0.08)`

禁止霓虹外发光、强投影、黑色重阴影。

默认不要给普通卡片加大阴影。只有下拉、浮层、地图工具面板可以有轻阴影。

```css
:root {
  --sci-shadow-popover: 0 4px 10px rgba(0, 0, 0, 0.10);
  --sci-shadow-soft: 0 8px 18px rgba(107, 143, 235, 0.08);
}

.sci-card {
  border: 1px solid var(--sci-border);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: none;
}
```

## 7. 通用组件规范

### 7.1 按钮

主按钮：

- 背景 `#165DFF`
- 文字 `#FFFFFF`
- 高度常用 `32px`
- 圆角 `2-4px`
- 用于导出、确认、查询、保存等页面级动作。

次级按钮：

- 白底或浅底，边框 `#E5E6EB`
- 文字 `#1D2129` 或 `#4E5969`
- hover 使用浅蓝底或蓝色描边。

小按钮：

- 高度 `24px`
- 适合地图模式切换、弹层选项、标签操作。

按钮不要使用渐变、发光、3D、图标堆叠。图标按钮应使用 Arco Icon 或同等线性图标语义，如导出、放大、缩小、复位、全屏、框选。

Arco Button 覆盖建议：

```css
.arco-btn {
  height: 32px;
  border-radius: 3px;
  font-size: 14px;
}

.arco-btn-primary {
  background: #165dff;
  border-color: #165dff;
}

.arco-btn-primary:hover {
  background: #4080ff;
  border-color: #4080ff;
}
```

### 7.2 输入与筛选

筛选组件统一结构：

- label 在上方，字号 `14px`，颜色 `#1D2129` 或 `#4E5969`。
- 输入框高度 `32px` 或 `34px`。
- 输入框白底，边框 `#E5E6EB`，圆角 `2-4px`。
- placeholder 使用 `#86909C`。
- focus 使用 `#165DFF` 描边或浅蓝背景，不要出现厚重外发光。

常见筛选：

- 关键词搜索：右侧搜索图标。
- 区域层级选择：下拉或 Cascader。
- 年份范围选择：`2020 - 2026` 类型范围选择器。
- 领域筛选：多选标签，超出部分显示 `+1 more`。
- 单选/分段：用于地图视图、列表视图、短范围切换。

Arco 表单控件覆盖建议：

```css
.arco-input,
.arco-select-view,
.arco-picker {
  height: 32px;
  border-radius: 3px;
  border-color: #e5e6eb;
  background: #ffffff;
  font-size: 14px;
}

.filter-row {
  display: grid;
  grid-template-columns: 304px 244px 304px minmax(0, 1fr) auto;
  gap: 16px;
  align-items: end;
}

.filter-row--relaxed {
  gap: 24px;
}

.filter-item label {
  display: block;
  margin-bottom: 8px;
  color: #4e5969;
  font-size: 14px;
  line-height: 22px;
}
```

#### 7.2.1 ContextBar 与局部 FilterBar

筛选视觉必须分层。共用基础 ContextBar，不共用全部筛选条件。

| 层级 | 位置 | 视觉规则 |
| --- | --- | --- |
| 基础 ContextBar | 页内一级 Tab 上方，主内容容器顶部 | 使用筛选条样式；字段数量克制；控件高 `32px`；字段间距默认 `16px`；必要时可换行但不得横向溢出。 |
| 页面 / Tab 局部 FilterBar | 当前 Tab 内容区顶部、图表工具条或表格工具条 | 视觉权重低于 ContextBar；可使用紧凑行、工具条或局部表单；只影响当前区域。 |
| 二级分段控件 | 当前 Tab 内容区内 | 使用二级圆角 Tab、按钮组或 Segmented；高度 `28-32px`；不伪装成一级 Tab 或 ContextBar。 |

ContextBar 与页内一级 Tab 之间保留 `8-12px` 间距，并用背景、分隔线或留白区分“分析口径”和“视角切换”。

不要把所有筛选都塞进 ContextBar。企业类型、规模、资质、风险等级、评分维度、名单策略等专业筛选应放入局部 FilterBar 或图表 / 表格工具条。

跨页带入筛选上下文时，使用可关闭 `Alert` / `Notification` / `Message` 提示，例如“已沿用上一页口径：区域=深圳，时间=近三年”。提示应提供“调整口径 / 清除条件”入口，不遮挡主任务。

### 7.3 导航、Tabs 与按钮组

顶部导航、左侧导航、一级 Tab、二级圆角 Tab 和按钮组的层级必须分清。顶部导航和左侧导航是 Figma 定制组件，不直接等同 Arco `Menu` / `Tabs`；实现时可以自定义 DOM 和样式，但必须保留菜单或页签的语义、键盘路径、焦点态、选中态和禁用态。

| 组件 | 用途 | 视觉规则 | Arco 边界 |
| --- | --- | --- | --- |
| 顶部导航 / 用户区 | 系统标题、角色入口、全局操作 | 高度跟随 Header `64px`；右侧用户入口可用 `24-32px` 胶囊；hover 使用浅蓝或浅灰底；focus-visible 使用主蓝焦点环 | 定制组件 + `Dropdown` / `Button` / `Tooltip` 语义，不直接写成普通 Tabs |
| 左侧导航 | 系统级模块切换和二级菜单 | 展开宽 `200px`，收起宽 `64px`；当前项使用 `#E8F3FF` 浅蓝底 + `#165DFF` 文字；图标 `16px`；菜单项高度约 `40px` | 定制组件 + `Menu` 语义；保留 `selectedKey`、`openKeys`、disabled 和键盘上下移动 |
| 一级 Tab | 页面或模块内同级内容切换 | 文本 `14px`；激活项 `#165DFF`，底部 `2px` 主蓝指示条；非激活项 `#4E5969`；hover 使用浅蓝底或主蓝文字 | 可用定制页签 + `Tabs` 语义；不要把主导航写成一级 Tab |
| 二级圆角 Tab | 卡片、面板、抽屉内局部视角切换 | 外层浅底，选中项圆角浅蓝底 + 主蓝文字；高度 `28-32px`；圆角 `999px` 或 `6-8px` | 可用 `Radio.Group`、`Segmented` 或自定义 Tab 组；只刷新所在局部容器 |
| 按钮组 | 模式、粒度、排序、指标口径等互斥选择 | 外层 `#F2F3F5`，选中项白底浮层 + 主蓝文字；高度 `28-32px`；组内只允许一个选中项 | 优先 `Radio.Group type="button"` 或 `Segmented`；不承载页面跳转 |

状态矩阵：

| 状态 | 顶部/左侧导航 | 一级 Tab | 二级圆角 Tab / 按钮组 |
| --- | --- | --- | --- |
| default | 主文字或次文字，透明或浅底 | `#4E5969` 文本 | 透明或浅灰底，次文字 |
| hover | 浅蓝底或浅灰底，图标和文字加深 | 主蓝文字或浅蓝底 | 浅蓝底，边界不跳动 |
| active | 保持当前尺寸，仅颜色加深 | 短暂加深文字或指示条 | 选中块轻微加深 |
| selected | 浅蓝底 + 主蓝文字，左侧可有主蓝指示 | 主蓝文字 + 底部 `2px` 指示条 | 白底或浅蓝底 + 主蓝文字 |
| disabled | `#86909C`，不可点击，保留布局 | 弱文字，说明不可用原因 | 弱文字，保留位置，不自动改选 |
| loading | 不让整条导航闪烁，目标区域局部 loading | 内容区 loading，不重置筛选 | 受控区域局部 loading |
| focus-visible | `0 0 0 2px var(--sci-focus-ring)` | 同左 | 同左 |

一级 Tab 与二级圆角 Tab 同屏出现时，一级 Tab 控制模块级内容，二级圆角 Tab 只控制所在卡片、面板或抽屉。按钮组只表达互斥模式，不表达层级导航。

标题、面包屑与 Tab 的去重规则：

- 左侧导航 active 态或面包屑已表达当前位置时，不重复展示路径型页面标题。
- 面包屑用于超过 2 级的下钻、对象详情或回溯路径；显示面包屑后，不再额外显示同一条路径的标题。
- 当前一级 Tab 只由 Tab 选中态表达，不拼进页面标题，不在右上角重复 Tag。
- 只有业务对象名、结果主题、报告名等真实内容标题才应作为可见标题展示。

### 7.4 标签

Tag 用于领域筛选、地图图例、状态提示。

- 默认高度 `20-24px`。
- 浅色底，低饱和边框。
- 文本 `12px` 或 `14px`。
- 业务分类标签使用要素色，但底色要淡，不要满屏高饱和。

#### 7.4.1 数据血缘角标组件（D9 规约业务扩展层）

统计数字旁的角标体系，按 `mapping_status` 状态决定显示哪种。四组件**互斥优先级**：⏳ OdsPendingBadge > ⚠️ PendingBadge > 🧪 MockBadge > ⓘ MetricSpecCard。

| 组件 | 触发 `mapping_status` | 触发条件 | 视觉 | Arco 映射 |
|------|----------------------|----------|------|-----------|
| **⏳ OdsPendingBadge** | `⏳ pending_ods` | 8/20 前 ODS 未稳定，`source_tables` 指向项目自研 DWD | 浅蓝底 `#E8F3FF` + 深蓝字 `#165DFF` + ⏳ 图标；tooltip："当前数据源（甲方 ODS）预计 2026-08-20 稳定，映射待 GDF 完成" | `Tag` + `Tooltip` |
| **⚠️ PendingBadge** | `🟡` 或 `❌` | 口径待甲方确认 / ODS 缺口已确认 | 浅橙底 `#FFF7E8` + 橙字 `#FF7D00` + ⚠️ 图标；`pending_hint` ≤80 字用 Tooltip，>80 字用 Popover | `Tag` + `Tooltip` / `Popover` |
| **🧪 MockBadge** | `is_mock=true` | Mock 占位数据 | 浅灰底 `#F2F3F5` + 灰字 `#86909C` + 🧪 图标；tooltip："当前为 Mock 数据，预计 {mock_until} 切换为真实数据" | `Tag` + `Tooltip` |
| **ⓘ MetricSpecCard** | `✅ mapped` | 数据完整可追溯 | 无角标，数字旁 ⓘ 图标，hover/点击弹出 8 件套说明卡 | `Card` + `Popover` |

> **与 MockBadge 的关系**：Mock 数据 + ODS 未供应 → 同时显示 🧪 + ⏳（两者语义不同：🧪=数据是假的，⏳=源还没定）；真实数据但 ODS 未稳定 → 仅 ⏳；口径有歧义 → 仅 ⚠️。
>
> **详见**：`data-lineage-policy.md` §2.2 状态机、§5.1 UI 落地规范。

### 7.5 单选、复选和开关

复选框：

- 方形 `16-20px`。
- 包含未选中、选中、半选、禁用、悬浮状态。
- 文本和控件间距 `4-8px`。

单选框：

- 圆形 `16px`。
- 适合领域、模式、单值选择。
- 禁用态文字使用 `#86909C`。

开关：

- 常用尺寸 `40 x 24px`。
- 打开态使用 `#165DFF`。
- 关闭态使用 `#C9CDD4` 或更浅灰。
- 用于地图图层开关，不能替代普通复选筛选。

### 7.6 分页

分页遵循 Arco Design 风格：

- 高度 `32px`。
- 页码按钮白底，边框浅灰。
- 当前页蓝色高亮。
- 总数文案使用 `共计 150 条` 这类格式。
- 页大小选择放在分页右侧。

### 7.7 Transfer / 穿梭框

用于左右列表选择：

- 左右列表等宽，工具按钮居中。
- 列表头、搜索框、列表项、底部信息完整保留。
- 搜索框高度 `32px`。
- 列表项高度约 `32px-40px`。

不要把复杂批量选择改成一组散乱 checkbox。

### 7.8 Drawer / 抽屉

详情、配置、要素信息可以使用抽屉：

- 从右侧滑出。
- 宽度按内容 `480-720px`。
- 标题、关闭、底部操作区完整。
- 背景白色，边框和阴影克制。

### 7.9 Arco 外围与定制组件边界

通用组件落地时优先使用 Arco 的语义和状态，但不要把所有视觉都误认为 Arco 原生能力。

| 类型 | 使用方式 | 不允许 |
| --- | --- | --- |
| Arco 原生优先 | `Button`、`Input`、`Select`、`DatePicker`、`Tag`、`Drawer`、`Modal`、`Table`、`Pagination`、`Tooltip`、`Popover`、`Skeleton`、`Empty`、`Alert` | 页面私有按钮、私有下拉、私有弹窗替代 Arco 基础组件 |
| 定制组件 + Arco 语义 | 顶部导航、左侧导航、一级 Tab、二级圆角 Tab、按钮组 | 直接套 Arco 默认外观导致与 Figma 组件层级不一致；丢失键盘与无障碍语义 |
| 可视化外围 | 图表、地图、图谱的标题、工具栏、筛选、图例、loading、empty、error、Drawer | 用 Arco 组件硬画折线、地图点位、热力层或图谱关系 |
| 可视化内核 | ECharts / GIS / 图谱库负责坐标轴、图形渲染、地图平移缩放、节点布局、hover/click 命中 | 让内核承担全局 loading、权限占位、导出反馈、抽屉等通用 UI |

## 8. 地图与分析工作区

### 8.1 地图主视图

地图是主舞台：

- 必须占据页面最大视觉区域。
- 可以叠加热力、点位、边界、网格、图例。
- 地图工具栏固定在地图左上角或右上角。
- 基础图例固定在地图容器右下角，跟随地图容器显示；全屏时图例必须保留。
- 地图不要做深色科幻大屏风格，保持浅色底图和清晰信息层。

地图工具栏：

- 使用 `32px` 高工具条。
- 图标尺寸 `16px`。
- 工具包括放大、缩小、复位、全屏、框选区域。
- 图标之间间距约 `16px` 或工具项宽度 `32px`。
- 工具按钮必须有 tooltip 或可访问名称；达到最大/最小级别后禁用对应按钮。

地图显示模式：

- 使用 `地图视图 / 列表视图` 切换。
- 展开弹层可包含「区域 / 城市 / 国家」等模式按钮。
- 弹层使用白底、轻阴影和 `16px` 内边距。

图例与热力：

- 基础图例展示对象类型或区域分级，使用 `12px` 文本、`6-8px` 色点/线段，容器白底半透明，圆角 `6-8px`，轻阴影。
- 热力开关开启时，地图叠加热力覆盖层，同时展示基础图例和热力强度分级图例。
- 热力开关关闭时，隐藏热力覆盖层和热力强度分级图例，保留基础图例和点位/区域对象。
- 热力强度分级只表达密度或强度趋势，不用于精确读取单点数值；必须标注低/高或最小/最大语义。
- 图例不得遮挡核心地图对象；小视口下优先压缩图例宽度，不得移除。

```css
.map-legend {
  position: absolute;
  right: 16px;
  bottom: 16px;
  max-width: 260px;
  padding: 10px 12px;
  border: 1px solid var(--sci-border);
  border-radius: 8px;
  background: var(--sci-legend-bg);
  box-shadow: var(--sci-legend-shadow);
  font-size: 12px;
  color: var(--sci-text-2);
}

.heatmap-legend {
  margin-top: 8px;
}
```

### 8.2 左侧要素图层面板

结构：

- 标题「科创要素」或「基础设置」。
- 每一行包含色点、图标、名称、开关。
- 行高约 `24px`，行间距约 `16px`。
- 图层分类包括专家学者、会议、科研机构、企业、服务机构、课题、项目、论文、期刊、专利。

规则：

- 色点必须使用对应业务色。
- 图标使用线性图标，不使用填充插画。
- 开关靠右对齐。
- 禁用项使用灰色开关和弱文字。

### 8.3 右侧分析面板

右侧面板是结论收口区，默认不可删除。

常用内容：

- 数据概览
- 影响力
- 采类分析
- 要素比较
- 发展趋势
- 领域分布
- 指标说明或占位输入

布局规则：

- 标题左侧可使用 `3px x 16px` 蓝色竖条。
- 分组标题 `14-16px`，正文 `14px`。
- 输入/说明块使用白底浅边框。
- 图表区使用浅网格线、细线、点线组合。
- 右侧面板内部滚动，不影响左侧导航和顶部区域。

## 9. 图表规范

趋势图：

- 网格线使用浅灰蓝，不要使用深色坐标轴。
- 折线使用业务色，线宽 `2px` 左右。
- 点位 `6px` 左右。
- X/Y 轴标签使用 `10-12px`，弱文字色。
- 图例居底或居中，不遮挡图形。

饼图/环图：

- 使用要素色序列。
- 图例右侧或下方列表展示。
- 文本保持 `12px`，数字右对齐。

热力色阶：

- 使用单条连续渐变。
- 标注 `低` / `高` 或 `Low` / `High`。
- 不要混用离散色做连续强度。
- 热力图例只在热力层开启时出现；关闭热力层后必须隐藏热力强度图例，但保留基础对象图例。

排名：

- 金银铜可使用：
  - 金 `#F59E0B`
  - 银 `#94A3B8`
  - 铜 `#B7791F`
- 排名只是辅助，不要让奖牌色超过主蓝权重。

图表 / 地图 / 图谱边界：

| 对象 | Arco 外围负责 | 可视化内核负责 |
| --- | --- | --- |
| 图表 | 容器、标题、图例区、指标切换、下载入口、loading、empty、error、tooltip 外观约束 | 折线、柱状、排行、桑基、坐标轴、数据点 hover/click、brush、zoom |
| 地图 | 容器、工具栏、热力开关、基础图例、热力强度图例、详情抽屉入口、状态反馈 | 底图、点位、区域边界、热力层、平移缩放、框选、聚合计算 |
| 图谱 | 容器、搜索框、类型筛选、图例、重置入口、详情抽屉、状态反馈 | 节点、边、布局算法、拖拽、邻居展开、路径高亮 |

可视化状态必须稳定：

- loading 时保留标题、工具栏、图例和容器尺寸，不让图形区塌陷。
- empty 时说明当前筛选无结果，提供调整筛选或查看列表的路径。
- error 时显示错误原因和重试入口，不只在图形内部画红字。
- selected / hover 由内核高亮图形元素，外围同步标题、详情、表格或 Drawer。
- fullscreen 时外围工具栏、图例和退出入口必须保留，内核响应尺寸变化重新渲染。

## 10. 交互状态

必须覆盖：

- 默认
- hover
- active / selected
- disabled
- loading
- empty
- error
- partial selected / 半选

状态规则：

- 选中：蓝色文字或蓝色底。
- hover：浅蓝底或浅灰底。
- disabled：文字 `#86909C`，边框 `#E5E6EB`，背景 `#F7F8FA`。
- loading：优先骨架屏或局部加载，不要整页转圈。
- empty：保留模块外壳，提供占位说明，不要让面板塌陷。
- error：内联提示或 Alert，不要只用红色边框。
- focus-visible：所有自定义导航、Tab、按钮组、图例项和地图工具按钮必须补回可见焦点环，不能因视觉还原移除键盘可达性。

开发/验收态提示：

- IA 解释、旧路由兼容说明、实现阶段说明不作为正式 UI 顶部内容。
- Mock、Pending、待维护、待确认和更新时间优先使用 `Tag` / `Badge` / `Tooltip` / 局部 `Alert` 表达，放在指标、图表、表格或字段旁。
- 不使用大面积蓝底说明条常驻页面顶部承载 IA 来源或开发说明。
- 如果演示环境必须展示验收提示，应可关闭，并与正式业务内容视觉区分。

## 11. 响应式与适配

当前设计优先 PC 宽屏。**科技专题服务系统全系统仅支持 PC 工作台，不提供移动端、小屏裁剪、响应式重排或小屏替代交互；小屏访问不纳入本期设计、开发与验收范围。**科技信息展示系统如有移动端范围，再按下述移动端规则单独适配。两者在 PC 工作台骨架、24 栅格和组件节奏上遵守同一规范。

PC 规则：

- PC 端保持 `24 columns` 和 `16px gutter` 不变；断点变化只调整 `column width`、左侧导航状态和工作区面板策略。
- `1440px` 以下优先收起左侧导航。
- 右侧分析面板可缩小，但不要完全移除；空间不足时转 Drawer / overlay。
- 地图主舞台必须保持最大可用区域。
- 筛选项不足时可换行，不能横向溢出。

断点策略：

| Viewport | 默认导航状态 | Columns | Gutter | Column width 规则 | 工作区策略 |
| ---: | --- | ---: | ---: | --- | --- |
| `>=1920px` | 展开 `200px` | `24` | `16px` | 展开态基准 `56px`，收起态基准 `62px` | 三段式完整显示：左图层 + 中央主视图 + 右分析 |
| `1680-1919px` | 展开或按用户状态 | `24` | `16px` | 按内容区动态计算，允许小数列宽 | 右分析面板优先收缩，中央主视图优先保证面积 |
| `1440-1679px` | 默认收起 `64px` | `24` | `16px` | 按内容区动态计算，允许小数列宽 | 左图层面板可压缩或折叠，右分析面板取低宽度 |
| `<1440px` | 收起 `64px` | `24` | `16px` | 仍保持 24 栅格，但组件需跨更多列 | 科技专题服务系统不作为支持目标；科技信息展示系统如继续适配，再按右分析转 Drawer / overlay、主视图优先执行 |

移动端规则（仅在科技信息展示系统已单列移动端范围时适用；不适用于科技专题服务系统）：

- 如果需要移动端，不能直接压缩 PC 三栏，也不强制沿用 PC 24 栅格。
- 移动端应转为：顶部筛选摘要 + 地图主视图 + 底部抽屉分析。
- 左侧导航改为抽屉或底部入口。
- 所有触控目标不小于 `44px`。

## 12. AI 生成规则

### 12.1 必须生成

生成两个系统的 PC 工作台页面时，默认包含：

- 顶部 Header。
- 左侧专题导航，支持展开/收起。
- 主内容白色半透明容器。
- 页头筛选条：区域、时间、领域、关键词至少保留三类。
- 左侧要素图层控制。
- 中央地图/图谱/主视图。
- 地图工具栏和图例。
- 右侧分析 tabs。
- 至少一个趋势/分布/排名类分析模块。

### 12.2 允许变化

可以根据业务变化替换：

- 地图为图谱、关系网络、列表矩阵。
- 要素类型为政策、人才、成果、项目、企业、机构等。
- 右侧分析 tabs 名称。
- 图表类型。
- 筛选字段。

变化时仍需保留“筛选 - 主视图 - 分析 - 下钻”的结构关系。

### 12.3 禁止事项

不要生成以下内容：

- 深色大屏风格。
- 霓虹蓝、紫色发光、赛博网格背景。
- 纯营销 hero。
- 三个等宽营销卡片作为主体。
- 大面积玻璃拟态模糊遮罩导致文字不清晰。
- 过多渐变文字。
- 复杂插画作为主视觉。
- 无右侧分析面板的单地图页面。
- 无筛选上下文的静态图表页面。
- 把图例、工具栏、筛选项放得过大。
- 使用 emoji 表达状态或菜单。
- 使用随机英文假数据替代科技业务对象。

### 12.4 高还原生成流程

AI 生成新项目时按以下顺序执行：

1. 创建 Arco React 项目，安装 `@arco-design/web-react` 和 `@arco-design/web-react/icon`。
2. 引入 Arco 基础样式，但立刻用本文件的 token 覆盖默认视觉。
3. 先搭建 `app-shell / app-frame / app-header / app-sidebar / content-shell / workspace-grid` 六个骨架容器。
4. 再实现 Header、Sidebar、筛选条、图层面板、地图区、右侧分析面板。
5. 最后填充图表、地图、业务数据和状态。

不要先生成一堆业务卡片再尝试套样式。这个风格的核心不是卡片，而是工作台骨架和组件尺寸。

### 12.5 最小页面结构模板

```jsx
import {
  Button,
  Checkbox,
  DatePicker,
  Input,
  Select,
  Switch,
  Tabs,
  Tag,
} from '@arco-design/web-react';
import {
  IconSearch,
  IconDownload,
  IconFullscreen,
  IconRefresh,
  IconZoomIn,
  IconZoomOut,
} from '@arco-design/web-react/icon';

export default function GkxWorkbench() {
  const systemName = '按当前系统填写';
  const currentModuleName = '按当前系统和页面填写';

  return (
    <div className="app-shell">
      <div className="app-frame">
        <header className="app-header">
          <div className="brand">{systemName}</div>
          <div className="header-actions">普通用户</div>
        </header>

        <aside className="app-sidebar">
          <nav className="sidebar-menu">{currentModuleName}</nav>
        </aside>

        <main className="content-shell">
          <section className="filter-row">
            <div className="filter-item">
              <label>地域范围</label>
              <Select placeholder="全球" />
            </div>
            <div className="filter-item">
              <label>时间选择</label>
              <DatePicker.RangePicker picker="year" />
            </div>
            <div className="filter-item">
              <label>领域筛选</label>
              <Select mode="multiple" placeholder="请选择领域" />
            </div>
            <Button type="primary" icon={<IconDownload />}>导出</Button>
          </section>

          <section className="workspace-grid">
            <aside className="layer-panel">科创要素图层</aside>
            <section className="map-stage">地图主视图</section>
            <aside className="analysis-panel">
              <Tabs defaultActiveTab="overview">
                <Tabs.TabPane key="overview" title="数据概览" />
                <Tabs.TabPane key="impact" title="影响力" />
                <Tabs.TabPane key="compare" title="要素比较" />
              </Tabs>
            </aside>
          </section>
        </main>
      </div>
    </div>
  );
}
```

这个模板只表达结构。生成真实页面时必须替换占位内容，但不得改变骨架关系。

## 13. 推荐实现映射

基础组件优先映射到 Arco Design：

- 页面骨架：`Layout`, `Grid`, `Space`, `ResizeBox`
- 导航：定制导航组件 + `Menu` 语义、`Dropdown`, `Breadcrumb`
- 筛选：`Form`, `Input`, `Select`, `Cascader`, `DatePicker`, `Radio`, `Checkbox`, `Switch`
- 操作：`Button`, `Segmented`, `Tooltip`, `Popover`, `Trigger`
- 展示：`Tabs`, `Table`, `Tag`, `Badge`, `Statistic`, `Descriptions`, `Pagination`
- 数据血缘角标（D9 业务扩展）：`Tag` + `Tooltip` / `Popover`（⏳ OdsPendingBadge / ⚠️ PendingBadge / 🧪 MockBadge）+ `Card` + `Popover`（ⓘ MetricSpecCard），详见 §7.4.1
- 反馈：`Skeleton`, `Empty`, `Alert`, `Result`, `Message`, `Notification`, `Spin`
- 下钻：`Drawer`, `Modal`
- 图表地图图谱：业务自定义可视化内核 + Arco 外围容器、工具栏、图例和状态反馈

主题 token 建议：

```ts
const arcoThemeTokens = {
  'primary-6': '#165DFF',
  'success-6': '#00B42A',
  'warning-6': '#FF7D00',
  'danger-6': '#F53F3F',
  'link-6': '#165DFF',
  'color-text-1': '#1D2129',
  'color-text-2': '#4E5969',
  'color-text-3': '#86909C',
  'color-border-2': '#E5E6EB',
  'color-fill-1': '#F7F8FA',
  'color-fill-2': '#F2F3F5',
  'color-bg-1': '#FFFFFF',
  'border-radius-small': '2px',
  'border-radius-medium': '4px',
};
```

React 侧优先使用 `@arco-design/web-react` 组件和 `@arco-design/web-react/icon` 图标；业务样式通过项目级 CSS 变量或主题 token 统一覆盖，不要在单个页面里散落硬编码主色。

Arco 入口建议：

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigProvider } from '@arco-design/web-react';
import '@arco-design/web-react/dist/css/arco.css';
import App from './App';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ConfigProvider>
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
```

不要引入 `antd`、`antd/dist/reset.css` 或 Ant Design 的 `ConfigProvider`。如果项目里出现 `vendor-antd`、`.ant-` class 或 `colorPrimary` 风格 token，说明没有按本规范执行。

业务 token 建议：

```ts
const scienceTokens = {
  surfaceShell: 'rgba(255, 255, 255, 0.8)',
  surfaceSoft: '#F7F8FA',
  surfaceSelected: '#E8F3FF',
  borderSoft: '#E5E6EB',
  mapBorder: '#DCE9FF',
  factorExpert: '#4180FD',
  factorCompany: '#16C7C7',
  factorResearch: '#4DD164',
  factorMeeting: '#F6BA21',
  factorPaper: '#A872E2',
  factorPatent: '#58A8F9',
  factorService: '#F779B6',
  factorProject: '#83DDD3',
  factorTopic: '#78D986',
  factorJournal: '#FBD08A',
};
```

## 14. 生成检查清单

交付 AI 原型前检查：

- 是否仍是浅蓝白科技工作台，而不是深色大屏？
- 是否保留 Header、左侧导航、主内容容器、中央主视图、右侧分析？
- 选中态是否统一使用 `#165DFF` 或 `#E8F3FF`？
- 表单、按钮、分页、标签是否接近 Arco Design 节奏？
- 地图工具栏、图例、筛选项是否尺寸克制？
- 页面主内容、筛选区、地图/图谱主视图、右侧分析面板和卡片外边界是否按 24 栅格对齐？
- 展开态是否使用 `offset 200 / 24 columns / 56px column / 16px gutter`？
- 收起态是否使用 `offset 64 / 24 columns / 62px column / 16px gutter`，且主内容横向扩展？
- PC 断点下是否始终保持 `24 columns` 和 `16px gutter`，只调整 column width、导航状态和面板策略？
- 科技专题服务系统是否仍限定为 PC 工作台，未新增小屏裁剪、移动端重排或替代交互？
- 表单、筛选区和卡片间距是否使用 `4 / 8 / 12 / 16 / 24 / 32` 阶梯，并避免 `20px` gap？
- 顶部导航和左侧导航是否按 Figma 定制组件处理，而不是误写成 Arco 默认 Menu/Tabs 外观？
- 一级 Tab、二级圆角 Tab、按钮组是否层级清楚，并覆盖 selected / disabled / loading / focus-visible？
- 地图基础图例是否固定右下角，热力图例是否只随热力开关开启出现，且全屏仍保留？
- 图表、地图、图谱是否区分 Arco 外围与可视化内核，没有把复杂图形误写成 Arco 组件能力？
- 是否有 loading、empty、disabled、error 状态？
- 图表颜色是否遵循要素色/图表色序列？
- 是否避免了霓虹、紫蓝发光、营销 hero、emoji 和无业务意义的占位？

验收标准：

- 首屏一眼能看出是“地图/图谱分析工作台”，不是卡片仪表盘。
- Header 高度接近 `64px`，不是 `84px` 或更高。
- 左侧展开导航接近 `200px`，不是 `256px`。
- 页面主内容在展开态和收起态均能贴合 24 栅格列线，菜单收起时内容区应横向扩展。
- 表单、按钮、分页、工具栏高度接近 `32px`。
- 筛选区字段默认 gap 为 `16px`，宽松场景为 `24px`，不得出现 `20px` 字段间距。
- 主色在截图取样中接近 `#165DFF`。
- 页面背景接近 `#D8E7FC`，不得出现大面积深蓝、紫色、黑色。
- 普通卡片没有强阴影，浮层阴影也很轻。
- 中央主视图面积必须大于右侧分析面板面积。
- 右侧分析面板必须存在 tabs 或分组分析内容。
- 图表、地图、图谱必须由专业可视化内核承载，Arco 只负责外围容器、工具栏、图例、状态反馈和弹层。
- 新项目依赖里必须有 `@arco-design/web-react`，不得只依赖 `antd`。
