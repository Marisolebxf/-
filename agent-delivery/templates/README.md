# 交付文档模板

**格式**对齐 `5-实施和开发/详细设计/正式文件/`（章节、版式、Mermaid 写法）；**内容**按实际交付发挥。

| 模板 | 用途 |
|------|------|
| `handoff-template.md` | 子 agent handoff |
| `acceptance-test-report-template.md` | 接口/功能测试报告 |
| `acceptance-e2e-demo-template.md` | 端到端演示记录 |
| `usm-template.md` | 用户故事地图：产品角色、用户故事、主/异常路径与验收 |
| `ia-template.md` | 产品 IA：入口、层级、页面职责与模块边界 |
| `wireframe-template.md` | 页面线框：布局、控件、字段/指标、交互与状态 |
| `task-leaf-template.yaml` | task-registry 新建 leaf 片段（建单 / 拆单复制用） |
| `sys-capability-adapter-card-template.md` | 业务域接入 SYS-JOBS / COMPARE / EXPORT 的硬闸门登记卡（金样例场景） |
| `doc-vs-demo-scope-template.md` | 文档 vs Demo 三栏范围对照（防「写了没跑出来」） |

## docx

需要 Word 时：officecli 读 V6 的 **outline/styles**，克隆版式后写入 **自写正文**（见 `../officecli-doc-workflow.md` §5）。

## 可选字段

`format_ref`：标注对齐哪一章/哪份模板的**结构**，非强制逐条抄 V6。
