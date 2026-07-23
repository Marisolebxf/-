# ENT-OPS 维护管理 UI 规范整改设计

## 1. 目标

将 `/enterprise-center/maintenance` 从快速演示实现整改为 GKX 标准的搜索/列表工作台，同时保持 ENT-OPS 四件套已经冻结的业务语义、六个 Frame、七个评审挂载与三角色工作流不变。

本轮只整改维护管理页面及其最小入口接线，不修改企业分析其他页面，不处理当前工作区中的无关未提交改动。

## 2. 页面归类与边界

- 系统：科技专题服务系统。
- 屏幕契约：`medium_1440_1920`。
- 页面一致性：`standard`。
- 页面原型：搜索/列表工作台。
- 标准任务闭环：工作台筛选与列表 → 页面级业务详情 Frame → 完成动作 → 返回原列表上下文。
- 不新增自定义例外，不引入第二套设计系统。

## 3. 组件整改

### 3.1 工作台 F-OPS-01

- 五个列表 variant 使用 Arco `Tabs`，受控值继续使用 `route_variant_id`。
- 内容类型和流程状态使用 Arco `Select`。
- 关键词使用 Arco `Input.Search`。
- 内容列表使用 Arco `Table`，由 `columns` 描述列，不再渲染原生 `<table>`、`<thead>`、`<tbody>` 或私有 hover/边框样式。
- 分页使用 Arco `Table` 的 pagination 配置，包含总数文案；不再维护独立私有分页区。
- 加载、空、错误状态使用 Arco `Spin/Skeleton`、`Empty`、`Alert/Result` 的标准反馈语义。

### 3.2 内容编辑 F-OPS-02 与冲突处理 F-OPS-06

- 内容编辑器不再使用 `92vw` Drawer。
- 进入编辑态后，在当前 Shell 的内容区渲染页面级详情 Frame，并提供明确返回入口。
- 按四件套固定为 24 栅格三栏：主数据 4 列、编辑区 12 列、门户预览 8 列，`16px` gutter。
- 主数据只读区继续使用 Arco `Descriptions`；纠错使用标准 `Modal + Form`。
- 编辑字段使用 Arco `Form.Item`、`Input`、`Input.TextArea`、`Select`，不使用原生 `<label>`。
- 冲突处理使用局部页面状态或标准 `Modal`，失败时保留本地脏输入与原业务状态。

### 3.3 审核、发布与版本治理 F-OPS-03～05

- 审核、发布、版本审计使用当前 Shell 内的页面级详情 Frame；次级确认可使用标准 `Modal`。
- `return_from_publish` 仍是唯一发布退回动作；存在定时计划时，文案和状态必须表达“取消计划并转草稿”的原子语义。
- 从历史版本创建草稿不得覆盖历史版本。
- 通用动作统一使用 Arco `Button` 和 Arco Icon。

## 4. 视觉与交互

- 页面背景、主色、文字、边框和间距继续使用 `--sci-*` Token，不新增近似硬编码色。
- 控件默认高度 `32px`；正文 `14px`；页面与列 gutter `16px`。
- 主容器使用现有蓝白工作台表面，不新增营销卡片、重渐变或装饰性玻璃。
- 1440～1920px 内保持 PC 工作台；不生成移动端重排。
- 当前页面不出现用户姓名或其他真实个人姓名；演示维护人统一使用“内容编辑 A/B/C”等虚构角色标识。

## 5. 评审模式

保留并逐项匹配以下七个 mount：

1. `ENT-OPS-F01-WORKBENCH-TITLE`
2. `ENT-OPS-F02-EDITOR-TITLE`
3. `ENT-OPS-F02-MASTER-DATA-BOUNDARY`
4. `ENT-OPS-F03-REVIEW-TITLE`
5. `ENT-OPS-F04-PUBLISH-RISK`
6. `ENT-OPS-F05-VERSION-AUDIT-TITLE`
7. `ENT-OPS-F06-CONFLICT-TITLE`

继续复用 `TraceInfoIcon` 的自门控能力。评审模式只增加证据入口，不改变业务值、权限、动作或状态；业务模式下渲染 mount 数量必须为 0。

## 6. 数据与状态

- 保留当前确定性演示内容，不声明真实 CMS、主数据、审核、发布或审计服务接入。
- `route_variant_id` 仍是返回上下文唯一规范键。
- 操作状态保留 `idle / submitting / succeeded / failed`。
- 保存、审核、发布、纠错等失败态保留用户输入和原业务状态。

## 7. 验证

完成后执行：

- `gkx-ui-design-standards/scripts/check-composite-labels.mjs`。
- `git diff --check`。
- 维护管理源文件静态扫描：无原生 table、无真实个人姓名、七个 mount 集合一致。
- 项目现有设计合同检查。
- 生产构建。
- 评审/业务双模式 DOM、真实指针交互和 1440/1680/1920 页面截图。

若用户继续要求“暂不测试”，则只执行不属于项目测试的源文件审计，并把状态保留为 `implemented/manual_review`，不得登记 `verified`。
