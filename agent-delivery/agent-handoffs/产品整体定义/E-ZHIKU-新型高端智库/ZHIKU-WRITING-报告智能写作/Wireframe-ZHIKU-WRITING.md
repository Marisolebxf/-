# Wireframe-ZHIKU-WRITING｜战略咨询报告智能写作

> **版本**：v1.0-rework-r1
> **同步**：与 USM/IA/UX-SPEC/TRACE 同版本
> **视觉基线**：Design.md §4-§7（主色 `#165DFF`、正文 14px、控件 32px、容器 16px 内边距）；组件全部 Arco Design Vue

## 1. 页面骨架

```text
MainLayout（左侧手风琴导航，不改）
└── AI 智能报告创作
    ├── /writing/create            F-WR-01 创作首页
    │   ├── /writing/create?step=config&mode=template|nl   F-WR-03
    │   ├── /writing/create?step=outline&task={task_id}    F-WR-04
    │   └── /writing/create?step=editor&task={task_id}     F-WR-05
    ├── 模板库：F-WR-02（F-WR-01/03 内以全屏子视图 + 抽屉打开）
    ├── /writing/materials         F-WR-07 我的素材库
    └── /report-mgmt/my-tasks 菜单位（writing-tasks）F-WR-06 我的报告任务
```

- 步骤态用 URL query 承载（`step` + `task`），刷新可恢复；无效 `task` 回落首页并提示。

## 2. F-WR-01｜创作首页

### 2.1 结构草图

```text
┌ PageShell: 报告创作 ────────────────────────────────────────┐
│ [入口卡×2]  模板发起（研究/战略/洞察 三选） │ 自然语言发起      │
│ [指标行]   任务总数ⓘ🧪  待审核数ⓘ🧪  我的模板数ⓘ🧪            │
│ [最近任务] 最近 5 条任务卡（状态标签/进度/继续按钮）            │
│ [创作历史] 类型筛选 + 关键词搜索 + 历史列表（点击回溯打开）      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id |
| --- | --- | --- | --- | --- | --- |
| 入口卡 | 报告类型（研究/战略/洞察） | Card + RadioGroup | 常量 | 点击进入 F-WR-03(template) | — |
| 入口卡 | NL 发起 | Card | — | 点击进入 F-WR-03(nl) | — |
| 指标行 | 任务总数 | MetricCard | taskStore | ⓘ 弹 MetricSpecCard | `ZHIKU-WR-TASK-TOTAL` |
| 指标行 | 待审核数 | MetricCard | taskStore | 同上 | `ZHIKU-WR-TASK-PENDING-REVIEW` |
| 指标行 | 我的模板数 | MetricCard | templateStore | 同上 | `ZHIKU-WR-TEMPLATE-MINE-TOTAL` |
| 最近任务 | 标题/类型/状态/进度 | List + Tag + Progress | taskStore | 点击按状态路由（写作中→详情，草稿→编辑器） | — |
| 创作历史 | 类型筛选/关键词 | RadioGroup + InputSearch | taskStore | 过滤历史列表（序号 102） | — |
| 创作历史 | 历史条目 | List | taskStore | 点击打开任务 | — |

## 3. F-WR-02｜模板库与预览

### 3.1 结构草图

```text
┌ 模板库（全屏子视图，PageHeader 返回）───────────────────────┐
│ [筛选条] 类型 RadioGroup ｜ 行业标签 Select ｜ 清空筛选        │
│ [Tabs] 系统模板 ｜ 我的模板（含"来自分享"标注）               │
│   模板卡网格：名称/类型Tag/行业Tag/操作（预览·复制│编辑·分享·删除）│
│ [预览抽屉 640px]                                             │
│   ├ 章节框架树（Tree ≥2 层）                                  │
│   ├ 示例内容段落（缺失时局部说明）                             │
│   ├ 排版样式说明（字号/层级/图表位）                           │
│   └ 底部动作：用此模板创建 ｜ 复制为我的模板                    │
│ [同事视角 Modal] 只读预览 + 保存为我的模板                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 筛选条 | 类型/行业标签 | RadioGroup + Select | templateStore | 实时过滤，清空恢复 | 88 |
| 模板卡 | 名称/标签/来源 | Card + Tag | templateStore | 点击开预览抽屉 | 88 |
| 预览抽屉 | 框架树/示例/样式 | Tree + Typography | template.outline/sample | 三区块展示 | 88 |
| 预览抽屉 | 用此模板创建 | Button(primary) | → F-WR-03 | 携带 template_id | 88 |
| 预览抽屉 | 复制为我的模板 | Button | templateStore.copy | 生成"副本"进我的模板 | 96 |
| 我的模板卡 | 编辑 | Button → 编辑 Modal | templateStore.update | 名称/标签/章节结构可改 | 94 |
| 我的模板卡 | 分享 | Button → 分享 Modal | templateStore.share | 链接复制 + 同事视角入口 | 95 |
| 同事视角 | 保存为我的模板 | Button | templateStore.saveShared | 副本带"来自分享" | 95 |
| 我的模板卡 | 删除 | Button(danger) + 二次确认 | templateStore.remove | 确认文案含被引任务数 | 97 |

## 4. F-WR-03｜创作配置（模板式 / NL 式）

### 4.1 结构草图

```text
┌ PageHeader: 新建{类型}报告 ← 返回首页 ─────────────────────┐
│ [模板式] 标题Input* ｜ 模板Select(+去模板库) ｜ 素材关联Select │
│ [NL式]  大输入框（示例句提示）→ 提交解析                      │
│   [意图确认卡] 主题/类型/时间范围 识别结果 + 模糊项追问选项      │
│              [确认生成任务] [返回修改]                        │
│ [底部] 下一步：确认大纲 ｜ 取消                                │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 模板式 | 报告标题 | Input（必填） | 表单 | 空值拦截 | 89 |
| 模板式 | 模板 | Select + 链接"去模板库" | templateStore | 预选自 F-WR-02 带入 | 88 |
| 模板式 | 关联素材 | Select multiple | materialStore（仅 ready） | Empty 态给"去上传" | 108/109 |
| NL 式 | 需求输入 | Textarea + 示例句 | — | 提交触发解析 🧪 | 98 |
| 意图卡 | 主题/类型/时间范围 | Descriptions + Tag | NL 解析 mock | 识别结果可改 | 99 |
| 意图卡 | 追问项 | RadioGroup 选项 | NL 解析 mock | 至少一个模糊维度追问 | 99 |
| 意图卡 | 确认生成 | Button(primary) | taskStore.createTask | 未确认不建任务 | 99 |

## 5. F-WR-04｜大纲确认工作区

### 5.1 结构草图

```text
┌ PageHeader: 大纲确认·{任务标题} ← 返回 ────────────────────┐
│ ┌ 左 60%：章节树 ────────────┐ ┌ 右 40%：章节详情 ────────┐ │
│ │ 章节行：拖手柄/Input/上移/下移/删除│ │ 选中章节名              │ │
│ │ [+ 新增章节]                 │ │ 分析思路 Textarea（自动存）│ │
│ │ [常用分析章节] 面板：宏观环境· │ │ 提示：AI 将按思路生成 🧪  │ │
│ │  竞争格局·政策法规·核心建议…  │ └─────────────────────────┘ │
│ └─────────────────────────────┘                              │
│ [底部动作] 保存为我的模板 ｜ 确认大纲，开始 AI 写作(primary)     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 章节树 | 章节标题 | Input 行内 | task.outline | 增/删/改/移，空标题标红 | 89 |
| 章节树 | 常用章节面板 | Tag 列表（≥6 项） | 常量 | 点选插入选中位后 | 89 |
| 章节详情 | 分析思路 | Textarea | outline_node.idea | 按节点独立保存 | 90 |
| 底部 | 保存为我的模板 | Button | templateStore.saveFromOutline | 命名 Modal，重名自动加序号 | 93 |
| 底部 | 确认大纲 | Button(primary) | taskStore.confirmOutline | 空大纲禁用 | 89/91 |

## 6. F-WR-05｜报告编辑器

### 6.1 结构草图

```text
┌ PageHeader: 编辑·{任务标题} ← 返回列表  [状态Tag][导出▾][提交审核] ┐
│ [写作中态] Progress + 骨架段落（只读）                             │
│ ┌ 正文区 70% ──────────────────────┐ ┌ 右栏 30% ─────────────┐ │
│ │ 段落文本（引用句尾脚注角标[1][2]…）  │ │ Tabs: 大纲｜版本历史     │ │
│ │ 思路段落头部 🧪"依据您的分析思路生成" │ │ 版本 Timeline（改写/保存）│ │
│ │ [图表卡] 标题+ECharts+样式切换⚙+🧪  │ └───────────────────────┘ │
│ │ 框选文本 → 浮条 [AI 改写]           │                           │
│ └───────────────────────────────────┘                           │
│ [溯源附录区] 引用来源列表（系统+用户素材同格式）自动生成            │
│ [来源抽屉 520px] 标题/类型Tag/摘要/提炼过程/[查看原文]             │
│ [原文预览 Modal] demo 内置原文页 🧪                               │
│ [AI 改写 Modal] 需求输入 → 原文/改写稿并排 → 替换｜放弃            │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 正文 | 段落 + 脚注角标 | 富文本区（分段渲染） | task.sections/citations | 点角标开来源抽屉 | 103/104 |
| 图表卡 | 图表 + 样式切换 | ECharts + RadioGroup(柱/折/饼) | chart_block | 切换持久化 | 100/101 |
| 来源抽屉 | 标题/类型/摘要/提炼过程 | Drawer + Descriptions | citation | 四要素齐备 | 104 |
| 来源抽屉 | 查看原文 | Button | citation.sourceDoc | 无原文置灰说明 | 105 |
| AI 改写 | 需求输入/并排对照 | Modal + 双栏 | rewrite mock 🧪 | 替换记版本 | 106 |
| 附录 | 溯源附录 | 列表（自动） | citations 派生 | 随引用增删同步 | 107/110 |
| 顶部 | 导出 | Dropdown(Word/PDF) | 前端生成文件 | 空正文拦截 | 92 |
| 顶部 | 提交审核 | Button | taskStore.submitPublish | 状态翻转 | 91→92 |
| 右栏 | 版本历史 | Timeline | task.versions | 改写/保存均记录 | 102/106 |

## 7. F-WR-06｜我的报告任务

### 7.1 结构草图

```text
┌ PageShell: 我的报告任务 ────────────────────────────────────┐
│ [指标行] 任务总数ⓘ🧪 ｜ 待审核数ⓘ🧪                            │
│ [筛选] 状态 RadioGroup（全部/配置中/大纲/写作中/草稿/待审/已发布）│
│ [表格] 标题｜类型｜状态Tag｜进度｜更新时间｜操作                  │
│        操作：进入编辑器/查看详情｜导出｜提交审核｜模拟审核(标注)    │
│ [任务详情 Drawer] 大纲摘要/素材清单/版本 Timeline/审核动作区       │
│   审核动作区：模拟角色标注 + [通过并发布][驳回(意见)]              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 表格 | 状态/进度 | Tag + Progress | taskStore | 写作中进度模拟推进 🧪 | 91 |
| 操作 | 导出 | Dropdown | 同 F-WR-05 | 真实文件下载 | 92 |
| 详情 | 素材清单 | List | task.materialIds → materialStore | 点击看素材摘要 | 109 |
| 详情 | 审核区 | Alert(模拟角色) + Button×2 | taskStore.approve/reject | 驳回回退草稿+意见 | 92 链路 |
| 详情 | 发布出口 | — | achievementStore.addFromTask | 发布写入成果 store | 跨叶子 |

## 8. F-WR-07｜我的素材库

### 8.1 结构草图

```text
┌ PageShell: 我的素材库 ─────────────────────────────────────┐
│ [指标行] 已就绪素材数ⓘ🧪 ｜ [上传素材] Button(primary)          │
│ [Upload 区] 拖拽/点击上传（仅 .doc/.docx/.pdf，前置校验）        │
│ [表格] 文件名｜大小｜解析状态Tag（解析中⟳/已就绪/失败+重试）      │
│        ｜摘要预览｜被引任务数｜操作（预览/重试/删除）             │
│ [摘要 Drawer] 文件信息 + 解析摘要段落 🧪                        │
│ [删除确认] 被 N 个任务引用提示                                  │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 字段表

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 上传 | 文件 | Upload（格式白名单） | materialStore.upload | 非法格式拦截 | 108 |
| 表格 | 解析状态 | Tag + 定时翻转 🧪 | material.parse_status | 解析中→已就绪模拟 | 108 |
| 表格 | 被引任务数 | Link | taskStore 反查 | 点击列出任务 | 109 |
| 操作 | 删除 | 确认弹窗 | materialStore.remove | 被引提示 + 任务侧降级占位 | 108 |

## 9. 服务响应最小字段（目标态预留）

```text
report_task: task_id/type/title/template_id/status/progress/outline[]/sections[]/citations[]/versions[]/material_ids[]/updated_at
template:    template_id/origin/name/type/industry_tags[]/outline[]/sample_html/style_notes
material:    material_id/file_name/size/parse_status/summary/updated_at
citation:    citation_id/marker/source_type/source_title/excerpt/derivation/source_doc?
achievement: achievement_id/task_id/title/type/published_at/source_label
```

## 10. ReviewMode 挂点

- MetricSpecCard（全部 ⓘ）、MockBadge 🧪、`Q-ZHIKU-01` ⚠️ 角标走评审层门控（`src/review`），关闭评审模式 DOM 零泄漏；
- 模拟角色标注（审核区/同事视角）属于业务演示语义，不随评审层隐藏，但文案必须显式"模拟"。

## 11. 本页 metric_id 清单

`ZHIKU-WR-TASK-TOTAL` / `ZHIKU-WR-TASK-PENDING-REVIEW` / `ZHIKU-WR-TEMPLATE-MINE-TOTAL` / `ZHIKU-WR-MATERIAL-READY-TOTAL` / `ZHIKU-WR-CITATION-TOTAL`（旧 `ZHIKU-S1-*` 正名迁移，不留双 id）

## 12. Wireframe 自检

- [x] 每个 Frame 有结构草图 + 字段表，字段表含控件/数据源/交互。
- [x] 序号 88-110 在字段表"序号"列全部出现至少一次。
- [x] 每个统计数字有 metric_id 列挂接；mock 位置标注 🧪。
- [x] 异常/空态在 USM 异常表定义，本文以控件级约束呼应（拦截/置灰/Empty）。
- [x] 视觉 token 遵循 Design.md，不引入新配色或新组件体系。
