# IA-ZHIKU-TECH-SYSTEM｜技术体系分析 · 信息架构

> **版本**：v1.0-rework-r4（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **真源**：拆解表 §2.2（序号 8-28）；USM-ZHIKU-TECH-SYSTEM.md

## 1. 模块目标与边界

- **目标**：技术体系"结构资产 + 四类证据"一站式研判：体系建管/树编辑/专家会审 + 论文/专利/项目/网络证据分析。
- **包含**：序号 8-28 全部 21 项。
- **不包含**：聚类/共性网络/趋势预警（ZHIKU-TECH-TREND）、报告写作本体（ZHIKU-WRITING）、真实检索/图算法/调度（🧪 演示态 + 能力说明卡）。

## 2. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| 技术体系 TechSystem | `sys-*` | 种子 + 新建/删除 | `zhiku-ts-systems` |
| 树节点 TechSystemNode | `<sys>-*` | 随体系编辑 | 同上（内嵌） |
| 专家意见 ExpertOpinion | `op-*` | 种子；回复/确认演进 | `zhiku-ts-opinions` |
| 论文任务 PaperTask | `pt-*` | 种子 + 新建/合并/重跑 | `zhiku-ts-paper-tasks` |
| 专利任务 PatentTask | `pat-*` | 种子 + 启停/删除 | `zhiku-ts-patent-tasks` |
| 项目任务 ProjectTask | `ptk-*` | 种子 + 新建/合并 | `zhiku-ts-project-tasks` |
| 网络任务 NetworkTask | `net-*` | 种子 + 上传生成 | `zhiku-ts-network-tasks` |
| 维护节点 NetworkNodeMaintain | `n*` / `nm-*` | 种子 + 增删改 | `zhiku-ts-maintain-nodes` |
| UI 态（筛选/选中/展开） | — | 会话间保留 | `zhiku-ts-ui` / `zhiku-ts-filters` |

## 3. IA 结构（路由与 Frame）

```
/strategy/tech-system（技术体系分析 · 单路由多标签，?tab= 同步）
├─ tab=system   F-TS-01 技术体系管理（新建/筛选/删除）
│                F-TS-02 在线编辑器（?system= 可分享）
├─ tab=expert   F-TS-03 专家交互
├─ tab=paper    F-TS-04 论文分析（总览/交叉/任务）
├─ tab=patent   F-TS-05 专利分析（总览/任务/案例/深度+报告出口）
├─ tab=project  F-TS-06 科研项目分析（检索/仪表盘/任务）
└─ tab=network  F-TS-07 社会网络分析（可视化/结果/任务/上传/维护）
```

| Frame | 职责 | 指标 |
| --- | --- | --- |
| F-TS-01/02 | 体系建管 + 树编辑（URL ?system=） | `ZHIKU-TS-SYSTEM-TOTAL` |
| F-TS-03 | 专家意见会审 | — |
| F-TS-04 | 论文证据 | `ZHIKU-TS-PAPER-TOTAL` |
| F-TS-05 | 专利证据 + 报告出口 | — |
| F-TS-06 | 项目证据 | `ZHIKU-TS-PROJECT-TOTAL` |
| F-TS-07 | 网络关系 | `ZHIKU-TS-NETWORK-NODE-TOTAL` |

## 4. 数据与服务边界

- 数据来自 `src/mock/techSystem.ts`（体系+专家）、`paperAnalysis.ts`、`patentAnalysis.ts`、`researchProject.ts`、`socialNetwork.ts` 五个领域 store（reducer 化 + localStorage `zhiku-ts-` 前缀）；目标态换 Java REST，Java 不做图算法（架构铁律，图算法归 Python /internal/*）。
- 序号 19/20 算法层能力以说明卡呈现目标态（🧪），实现登记 Q-ZHIKU-04。

## 5. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-TS-01 | TS → WRITING | 专利深度分析"生成专利分析报告"：`createTask` 预填大纲（当前维度+高相关格数），跳 `/writing/create?step=outline&task=` |
| CT-TS-02 | TS ← RN | RN 实体画像与 TS 网络节点共享机构名词表（演示层面一致性，无硬链接） |
