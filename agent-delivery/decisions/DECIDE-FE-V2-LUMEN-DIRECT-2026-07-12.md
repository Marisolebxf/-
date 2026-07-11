# DECIDE-FE-V2-LUMEN-DIRECT · Track-MS 前端直落 lumen 交付

> **日期**：2026-07-12  
> **状态**：✅ 已采纳（调度者落实）  
> **提议**：孔东（前端 Lead）  
> **拍板**：淮政玮（团队内部交付方案）  
> **关联规程**：`产品定义评审规程.md` v2.1

---

## 1. 背景

门 1 已通过的企业三模块（搜索 / 对比篮 / 企业详情）进入 V1 高保真后，原流程为：

```text
V1 → V2 在 demo-ui-topic（React）对齐 → 门 2 → 门 3 → frontend-agent 复刻 lumen（Vue）
```

存在问题：

| 问题 | 说明 |
|------|------|
| 技术栈断层 | 高颖线框/demo 为 **React**；正式交付为 **Vue + @arco-design/web-vue**（`lumen-ui-science-topic`） |
| 重复工程 | V2 demo 与 lumen 复刻两次实现同一页面，前端工作量大（孔东、曹丽影） |
| 准生产滞后 | 后台 API 对接完成的真实能力无法在同一工程内渐进呈现 |

备选方案曾讨论：新建独立前端 git 工程 — **不采纳**（增加重复与同步成本）。

---

## 2. 决议

### 2.1 Track-MS（中/小屏）新流程

```text
wireframe（高颖）
  → V1 高保真会签（ui-agent · demo-ui-topic 仅作视觉参照/UX 沙箱）
  → V2 lumen 准生产实现（孔东团队 · lumen-ui-science-topic dev 分支）
  → 门 2 体验+语义会签
  → 门 3 DG
  → ready（后续为 API 接线 / 联调 / 硬化，无「复刻」步骤）
```

### 2.2 仓边界

| 仓 | 角色 | 技术栈 | 维护人 |
|----|------|--------|--------|
| `demo-ui-topic` | **UX/线框演示沙箱**；保留高颖迭代线框与 V1 高保真参照 | React + Arco（D8 试点） | 高颖 + ui-agent |
| `lumen-ui-science-topic` | **专题系统正式前端**；V2 起按生产标准直接开发 | Vue 3 + Vite + @arco-design/web-vue | 孔东（Lead）+ 曹丽影 + 团队工程师 |
| `lumen-ui-science-pc` | 展示系统正式前端；**框架真源**（observability、request、布局） | 同上 | 展示系统前端 |

**框架策略**：`lumen-ui-science-topic` 复用 `lumen-ui-science-pc` 已验证的工程骨架（孔东确认专题仓当前为空壳，直接 fork 框架后按模块开发）。

**分支策略**：企业维度 Track-MS 页面开发统一在 **`lumen-ui-science-topic` 的 `dev` 分支**（与 CI/K8s dev 对齐）。

### 2.3 内部评审模式

- lumen dev 环境即**准生产评审面**：随后台对接进度逐渐完整，Mock 与真实 API 可并存。
- 须保留 **「内部评审」模式**（环境开关或路由级标识），用于门 2 walkthrough 与甲方演示前彩排；不得与生产灰度混淆。
- 会签单记录 **lumen commit SHA** + K8s dev URL（非 demo-ui-topic SHA）。

### 2.4 明确取消

- ❌ Track-MS 下 **取消 `frontend-agent`「demo → lumen 复刻」派单链**
- ❌ 不在 demo React 与 lumen Vue 之间再建第三套前端工程
- ✅ `demo2 禁止 merge 进 lumen` 铁律不变（本决议为 **直接在 lumen 开发**，非 merge demo 代码）

---

## 3. 任务与看板变更

| 原 Task | 变更 |
|---------|------|
| `ENT-MOD-*-V2-DEMO` | **保留 ID**；`repo` → `ui_topic.lumen`；标题改为「V2 lumen 准生产实现会签」 |
| 门 3 后工程 leaf | 定义为 API 接线 / 联调 / 权限硬化，非复刻 |

---

## 4. 验收签字

| 角色 | 姓名 | 日期 |
|------|------|------|
| 前端 Lead | 孔东 | 2026-07-12（提议） |
| 体验 Owner | 高颖 | 待 V1 会签时知会 |
| 调度/coordinator | — | 2026-07-12 规程与 registry 已回填 |
