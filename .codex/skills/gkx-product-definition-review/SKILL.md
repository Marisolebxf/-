---
name: gkx-product-definition-review
description: Use when defining, reviewing, or revising a GKX module before PDR, preparing its USM/TRACE/IA/Wireframe package, running V1 high-fidelity signoff, handing off Track-MS V2 lumen work, or validating parent-module and leaf-module product-definition artifacts.
---

# GKX 产品定义评审流程

以 `agent-delivery/产品定义评审规程.md` 为唯一规程真源。此 Skill 将规程转为可执行工作流；不修改规程、不伪造会签或其他 Owner 的确认。

## 开始前

1. 对正式项目交付，先使用 `gkx-task-claim-supervision` 完成认领；纯本地 Skill 维护不适用。
2. **先锁定原始需求真源，再写角色、USM 或 TRACE。** GKX 科技专题服务系统的原始需求只取 `agent-delivery/bid-reference/` 下的两份实施方案 Markdown：`科技信息展示系统和科技专题服务系统.md` 与 `科技专题服务算法库.md`。其中，产品模块、服务对象和业务任务以系统方案对应章节为准；算法、指标和模型能力以算法库对应章节为准。`.docx` 仅作归档，不作为定义依据。
3. **角色取值必须可逐条回指源章节。** 先定位模块原文，再原样采用其明确的服务对象 / 用户角色；若源章节没有岗位或权限 persona，只能写“待业务确认”。不得从页面功能推导岗位角色，也不得从 Demo、SRS、FDS、User Flow、权限模型或常识推导。不得使用 SRS、会议纪要或评审意见替代或改写源需求角色；它们只能作为“差异 / 本轮决策”记录。
4. 在 USM 首段和 IA 角色表中记录源文件名、章节号与原文依据；TRACE 的 `role` 必须与 USM 一致。角色来源无法定位时，停止角色定义并形成开放项，而不是猜测。
5. 读取验收目录和规程 §2、§3、§5–§7；确定父模块、当前叶子、`screen_tier` 与交付轨道。
6. 以验收父节点命名产品包。叶子不是平铺的第二套产品包。

### 源需求与角色检查（强制）

- 企业分析示例：在 `科技信息展示系统和科技专题服务系统.md` 的 `§1.1.1.2.4.2.3 企业分析` 中，源文是“面向政府、园区与投资机构”；可记录为源需求服务对象，不得擅自替换成“业务分析师”“招商 / 育商专员”等岗位。
- 每一项产品角色都必须同时能回答：**来自哪份源文件、哪个章节、原文是什么**。三者任一缺失，即不是正式角色。
- 若评审产生与源需求不同的裁剪或新增，保留“源需求 / 本轮决策 / 待确认”的差异分层；不要把本轮决策倒灌为源需求。

## 产品定义包

对父模块 `{PARENT-ID}-{父模块名}` 创建或修订：

```text
agent-handoffs/产品整体定义/
└── {PARENT-ID}-{父模块名}/
    ├── USM-{PARENT-ID}-{父模块名}.md
    ├── TRACE-{PARENT-ID}-{父模块名}.yaml
    ├── IA-{PARENT-ID}-{父模块名}.md
    └── Wireframe-{PARENT-ID}-{父模块名}.md
```

- **USM**：完整产品定义，至少含角色、故事、主/异常路径、可测试验收与原始需求差异。
- **TRACE**：与 USM、IA、Wireframe 一起置于父模块目录；父矩阵中用 `leaves` 与 `compliance_refs.leaf_id` 追溯当前叶子，不另建 `TRACE-{叶子}.yaml`。
- **IA / Wireframe**：置于同一父模块目录；父文档说明全模块信息架构与成熟度，当前跑通叶子作为完整样例章节。
- **指标与开放项**：有统计数字时补 metric-spec 或 `cfg_metric` 种子；有 🟡 项时由 PM 同步 Q0xx。未确认数据必须显性标为 Mock、待接入或开放项。

命名与组织的完整示例见 [references/e31-e32-runthrough.md](references/e31-e32-runthrough.md)。

## 内部评审模式

每个模块的产品定义和 Demo 都必须交付评审层内容：来源/验收解释、Mock/待接入/开放项标识及页面特有评审说明。

- 入口只有一个：右上角**用户 / 角色切换**下拉面板中的全局“内部评审模式”开关。
- `SYS` 只是角色之一，不是入口名称；页面内不重复造开关。
- 关闭时仅隐藏评审层，保留正式视角、业务数据与业务权限。
- 每个 Wireframe 说明开关开启后本页显示什么；仅记录页面特有差异，不复制通用规则。

## 门禁顺序

1. **门 1 PDR**：五件套齐备，按规程 §5.2 的 PDR-01～PDR-14 逐项核对；🟡 项必须有开放项记录。
2. **Track-MS V1**：门 1 后完成高保真会签与版本冻结；按意见修订 V1 Demo，并记录修订证据。
3. **Track-MS V2**：在 `lumen-ui-science-topic` 的 `dev` 分支做准生产实现；V1 demo 只作 UX 参照。V2 通过前不得进入门 2。
4. **门 2**：体验与语义会签，核对 walkthrough、异常态、TRACE/指标、评审模式及范围卫生。
5. **门 3 DG**：仅在门 1、视觉门和门 2 满足后，由项目负责人拍板并解锁正式工程任务。
6. **门 3 之后**：工程拆单、联调、Sprint 关闭以 `agent-delivery/产品实现规程.md` 为真源（门 I1/I2/I3）；本 Skill 不替代该规程。

Track-L 走 V-L 大屏会签，与 Track-MS 并行；不要把大屏交付塞进 lumen 轨道。

## 验证

先运行结构检查，再按当前阶段运行相应 demo / lumen 验证。示例：

```bash
node .codex/skills/gkx-product-definition-review/scripts/check-product-definition-package.mjs \
  --module-id E-31 --module-name 企业发展 \
  --leaf-id E-32 --leaf-name 企业整体概况
```

结构通过不等于会签已通过。状态、签字、数据语义和远端交付证据必须如实记录。
