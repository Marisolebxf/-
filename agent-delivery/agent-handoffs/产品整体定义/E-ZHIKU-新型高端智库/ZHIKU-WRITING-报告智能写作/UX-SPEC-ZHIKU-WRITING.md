# UX-SPEC-ZHIKU-WRITING｜战略咨询报告智能写作

> **版本**：v1.0-rework-r1
> **权威输入**：本目录 USM/IA/Wireframe/TRACE + `UX-UE 通用交互组件规范.md` + Design.md §4-§7、§14

## 1. 权威输入与边界

- 交互行为/状态覆盖/键盘可达以 `UX-UE 通用交互组件规范.md` 为准；视觉 token 以 Design.md 为准；两者分层互补。
- 本文只约束 ZHIKU-WRITING 七个 Frame 的交互合同，不重复通用规范条文。

## 2. 五件套同步核对

| 文档 | 版本 | 一致性 |
| --- | --- | --- |
| USM | v1.0-rework-r1 | 8 故事 42 AC，与本文任务流一一对应 |
| IA | v1.0-rework-r1 | Frame 职责表与本文 §4 映射一致 |
| Wireframe | v1.0-rework-r1 | 字段表控件与本文交互合同一致 |
| TRACE | v1.0-rework-r1 | routes 覆盖序号 88-110 |

## 3. 用户旅程与任务流

### WR-J01｜模板发起到后台写作

首页入口卡 → 创作配置（模板预选/可换）→ 大纲确认（编辑+思路）→ 确认提交 → toast"已进入后台写作" → 自由离开 → 任务列表观察进度 → 完成后进入编辑器。

### WR-J02｜自然语言发起

首页 NL 卡 → 输入诉求 → 意图确认卡（识别+追问）→ 确认 → 复用 J01 的大纲确认之后流程。取消确认可回改输入，已输入文本保留。

### WR-J03｜编辑与溯源核查

编辑器 → 点角标开来源抽屉 → 查提炼过程 → 查看原文预览 → 关闭回到角标位 → 框选文本 AI 改写 → 对照替换 → 版本历史新增 → 附录自动更新。

### WR-J04｜模板资产化与分享

大纲页"保存为我的模板" → 模板库我的分区出现 → 编辑模板 → 分享生成链接 → 同事视角只读预览 → 保存副本（带来源标注）。

### WR-J05｜素材化写作

素材库上传 → 解析中→已就绪 → 创作配置勾选素材 → 生成正文含"用户素材"类型引用 → 附录同格式列出。

### WR-J06｜导出与发布闭环

编辑器/列表导出 Word 或 PDF（真实下载）→ 提交审核 → 详情内模拟审核（显式标注）通过 → 已发布 → 战略咨询成果页出现条目。

## 4. Frame 与承载映射

| 旅程 | Frame 序列 | 关键状态位 |
| --- | --- | --- |
| WR-J01 | F-WR-01→03→04→06→05 | task.status: outline_confirm→writing→draft_done |
| WR-J02 | F-WR-01→03(nl)→04→… | 意图卡 confirmed 前无 task |
| WR-J03 | F-WR-05 | citation 抽屉、rewrite modal、versions |
| WR-J04 | F-WR-04→02 | template.origin: mine/shared |
| WR-J05 | F-WR-07→03→05 | material.parse_status: parsing→ready |
| WR-J06 | F-WR-05/06 → 成果页 | status: pending_review→published→achievement |

## 5. 交互与状态转换

### 5.1 任务状态机（唯一真源：taskStore）

```text
（创建）→ outline_confirm → writing → draft_done → pending_review → published
                                        ↑              │ 驳回（记意见）
                                        └──────────────┘
```

- 状态翻转只经 store action；UI 按钮按状态显隐（如待审核不出现"提交审核"）。
- `writing` 进度由定时器模拟推进（🧪），页面打开时可观察增长，完成自动翻转。

### 5.2 表单与拦截

- 必填空值：提交时 Message.error + 聚焦首个问题字段；不产生半成品任务。
- 大纲空/空标题：确认按钮禁用或定位标红节点。
- 导出空正文：拦截提示"正文为空"。
- 上传格式白名单前置校验，非法文件不进列表。

### 5.3 抽屉与弹窗

- 来源抽屉、摘要抽屉：Esc/遮罩可关，关闭后焦点回触发元素。
- AI 改写 Modal：对照双栏，替换为 primary、放弃为普通按钮；放弃不产生任何变更。
- 删除类确认：danger 按钮 + 后果说明（被引数量），不可一键误删。

### 5.4 图表卡

- 样式切换 RadioGroup 即点即换，300ms 内完成重绘；选择持久化到 chart_block。
- 数据空时渲染局部 Empty，不出现空坐标轴假图。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复路径 |
| --- | --- | --- |
| 提交任务成功 | Message.success + 跳大纲页 | — |
| NL 解析不足 | 意图卡"需要更多信息"+示例句 | 补充重试 |
| 解析失败素材 | 状态 Tag 红 + 重试按钮 | 重试/删除 |
| 审核驳回 | 状态回退 + 驳回意见展示于详情 | 修改后重新提交 |
| 无效 task URL | 回落首页 + Message.warning | 从列表重进 |
| 刷新/重开 | 全部 store 从 localStorage 恢复 | 无感 |

## 7. 组件、键盘与无障碍

- 全部使用 Arco 组件；状态图标用 Arco Icon，禁 emoji 表状态（🧪 MockBadge 为 D9 规约组件例外）。
- 章节树行内操作提供键盘可达（Tab 聚焦、Enter 确认重命名）；上移/下移为显式按钮不依赖拖拽。
- 角标为 button 语义，可 Tab 聚焦、Enter 打开来源抽屉。
- 颜色不作为唯一状态区分：状态 Tag 均带文字。

## 8. 响应式行为

- 基线 1920×1080；≥1440 双栏（编辑器 70/30，大纲 60/40）；<1440 右栏折叠为 Tabs 置底。
- 表格横向滚动兜底，不隐藏操作列。

## 9. 内部评审投影

- ⓘ MetricSpecCard、🧪 MockBadge、⚠️ Q-ZHIKU-01 角标走 `src/review` 门控；BusinessMode 下 DOM 零泄漏。
- 覆盖序号徽标（PageShell covered-ids）仅评审模式可见。

## 10. Demo 实施交接

- store：`src/mock/writing/`（taskStore/templateStore 沿用重构 + materialStore 迁移 + achievement 出口），全部 localStorage 持久化（前缀 `zhiku-wr-`）。
- 导出：前端 Blob 生成 `.doc`（HTML 兼容格式）与 `.pdf`（打印流或 jsPDF 任一，允许简版排版），内容必须含标题/正文/附录。
- NL 解析与 AI 改写：规则式 mock（关键词抽取 + 模板句转写），产物带 🧪。
- 进度模拟：`setInterval` 驱动 store action，组件卸载不中断（挂 store 层）。

## 11. 缺口与阻断项

| 缺口 | 处理 |
| --- | --- |
| 语音输入（序号 98 局部） | demo 仅文字；开放项记 TRACE，UI 不出现假麦克风按钮 |
| 外链真实研报页（105） | demo 内置原文预览 🧪；正式态换外链 |
| 真实排版引擎（92） | 简版导出 + 不承诺版式还原 |
| 产品角色正式口径 | 挂 Q-ZHIKU-01，评审层 ⚠️ 角标 |

## 12. 机器可读交付契约

```yaml
frames: [F-WR-01, F-WR-02, F-WR-03, F-WR-04, F-WR-05, F-WR-06, F-WR-07]
routes:
  - { path: /writing/create, frames: [F-WR-01, F-WR-02, F-WR-03, F-WR-04, F-WR-05] }
  - { path: /writing/materials, frames: [F-WR-07] }
  - { path: writing-tasks(menu report-mgmt), frames: [F-WR-06] }
stores: [zhiku-wr-tasks, zhiku-wr-templates, zhiku-wr-materials, zhiku-wr-achievements]
persistence: localStorage
acceptance_source: USM-ZHIKU-WRITING.md#AC-US-ZHIKU-WR-*
```
