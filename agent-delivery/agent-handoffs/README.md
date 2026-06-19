# Agent handoffs

各子 agent 完成任务后在此目录提交结构化报告。已按**业务/功能**汉字子目录归集，方便人工浏览。

- **格式参考**：`../templates/handoff-template.md`、`../formal-docs-registry.yaml`（章节/版式）
- **内容**：按 task 实测填写；读 V6 **样式** 用 officecli（见 `../officecli-doc-workflow.md`）

## 子目录索引

| 子目录 | 业务/Epic | 包含 | 说明 |
|--------|-----------|------|------|
| [`软科学成果展示-DS25/`](./软科学成果展示-DS25/) | DS-25 软科学成果展示（INTEG 试点） | UX/UI trial + PILOT 协同包 + Arco 截图 8 张 | 多智能体编排第二次试点，全链路 PM/UX/UI/UE/客户备选话术 |
| [`科技人才态势-DS15/`](./科技人才态势-DS15/) | DS-15 科技人才态势（首次试点） | UX/UI trial + D8 改造决策 | 多智能体编排首次试点 + 后续 D8 规范的 DS-15 retrofit |
| [`企业战略分析-ENT/`](./企业战略分析-ENT/) | 企业专题（ENT）战略分析 | ALGO/API/ARCH/DATA/QA/UI/UX 全角色 | 企业战略分析模块的算法、API、数据、架构、质量、UI/UX 协同 |
| [`平台基建-PLATFORM/`](./平台基建-PLATFORM/) | 平台基建（INNOV/PLATFORM/ORCH 类任务） | 仓库 clone、流水线、聚合核心、orchestration 等基础设施任务 | 跨 Epic 的平台级一次性基础工作 |
| [`政策模块-E7/`](./政策模块-E7/) | 政策模块（E7-POLICY） | 政策指标、图谱、模型、API、专题 UI、展示绑定 | E7 政策专题 epic 全链条 handoff |
| [`运维事件/`](./运维事件/) | 运维与事件（INCIDENT） | 事件复盘记录 | 生产/UAT/Dev 环境事件的诊断与处置记录 |

## 命名规范

新增 handoff 时遵循：

1. **文件名**：`{角色}-{Epic-ID}-{描述}.md`（已有惯例，保持不变）
   - 角色：`UX` / `UI` / `ALGO` / `API` / `ARCH` / `DATA` / `QA` / `PILOT` / `D8` / `INCIDENT` 等
   - Epic-ID：`DS-25` / `DS-15` / `ENT` / `INNOV-M1-L01` 等
   - 描述：尽量短、英文连字符（如 `trial`、`dispatch`、`metric-seed`）

2. **归集子目录**（按文件名前缀自动归位，coordinator 派单时必须按此约定写 evidence 路径）：

   | 文件名前缀 | 归集目录 |
   |------------|----------|
   | `*-DS-25-*` / `PILOT-DS-25-*` | `软科学成果展示-DS25/` |
   | `*-DS-15-*` / `D8-DS-15-*` | `科技人才态势-DS15/` |
   | `*-ENT-*` | `企业战略分析-ENT/` |
   | `E-INNOV-*` / `E-PLATFORM-*` / `E-PLATFORM-ORCH-*` | `平台基建-PLATFORM/` |
   | `E-E7-POLICY-*` | `政策模块-E7/` |
   | `INCIDENT-*` | `运维事件/` |
   | 新业务 epic 启动 | coordinator 新建对应汉字子目录并更新本表 |

3. **本目录根**只保留 `README.md`，不放具体 handoff 文件
4. **空目录用 `.gitkeep` 占位**（已为 `平台基建-PLATFORM/` / `政策模块-E7/` / `运维事件/` 加占位，确保子目录结构入库可见）
