# IA-ZHIKU-RESEARCH-NEED｜研究需求分析 · 信息架构

> **版本**：v1.0-rework-r4（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **真源**：拆解表 §2.1（序号 1-7）；USM-ZHIKU-RESEARCH-NEED.md

## 1. 模块目标与边界

- **目标**：为战略研究提供"研究对象发现"入口——科技实体底盘、颠覆/前沿技术识别、趋势速览、媒体舆情联动。
- **包含**：实体清单与画像、颠覆性/前沿技术、趋势卡片、媒体聚焦（含预警与报告出口）。
- **不包含**：技术体系结构化管理（ZHIKU-TECH-SYSTEM）、聚类/共性网络/预警深挖（ZHIKU-TECH-TREND）、报告写作本体（ZHIKU-WRITING）、真实挖掘/推荐/舆情算法（🧪 演示态）。

## 2. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| 科技实体 TechEntity | `ent-*` / `ent-import-*` | 种子 + 批量导入新增 | `zhiku-rn-entities` |
| 颠覆性技术 DisruptiveTech | `dt-*` | 静态种子 | — |
| 前沿技术 FrontierTech | `ft-*` | 静态种子；关注集持久化 | `zhiku-rn-frontier-follows` |
| 趋势卡 TrendCard | `tc-*` | 静态种子 | — |
| 媒体舆情 MediaFocusItem | `mf-*` | 静态种子；处理态持久化 | `zhiku-rn-media-handled` |
| UI 态（筛选/视图/标签） | — | 会话间保留 | `zhiku-rn-filters` / `zhiku-rn-ui` |

## 3. IA 结构（路由与 Frame）

```
/strategy/research-need（研究需求分析 · 单路由多标签，?tab= 同步）
├─ tab=entity    F-RN-01 科技实体清单（?entity= 详情抽屉 → F-RN-02）
├─ tab=frontier  F-RN-03 颠覆性技术 / 前沿技术
├─ tab=trend     F-RN-04 技术趋势卡片
└─ tab=media     F-RN-05 媒体聚焦
```

| Frame | 职责 | 主要数据 | 指标 |
| --- | --- | --- | --- |
| F-RN-01 | 检索/筛选/视图切换/批量导入 | entities + filters | `ZHIKU-RN-ENTITY-TOTAL` |
| F-RN-02 | 实体画像抽屉（URL 可分享） | entity + heatTrend + 相似推荐 | — |
| F-RN-03 | 颠覆卡 + 前沿清单 + 关注集 | disruptive/frontier + follows | — |
| F-RN-04 | 趋势卡片 + 标签过滤 + 摘要抽屉 | trendCards + tagFilter | `ZHIKU-RN-TREND-TECH-TOTAL` |
| F-RN-05 | 舆情层次研判 + 预警处理 + 报告出口 | mediaItems + handled | `ZHIKU-RN-MEDIA-WARNING-PENDING` |

## 4. 数据与服务边界

- 全部数据来自 `src/mock/researchNeed.ts` 领域 store（reducer 化 action + localStorage `zhiku-rn-` 前缀）；目标态替换为 Java REST（gkxlumen-topic 聚合层），前端不感知算法实现。
- 相似推荐/批量导入校验/自动挖掘/图谱联动为 🧪 演示态；算法定义卡登记 Q-ZHIKU-04，图谱联动登记 `GAP-ZHIKU-RN-KG-LINK`。

## 5. 跨模块契约

| 契约 | 方向 | 说明 |
| --- | --- | --- |
| CT-RN-01 | RN → WRITING | 媒体聚焦"生成舆情研判报告"：调 `useWritingTaskStore.createTask` 预填大纲（层次过滤+预警统计），跳 `/writing/create?step=outline&task=` |
| CT-RN-02 | RN → TECH-TREND | 趋势摘要抽屉"去技术趋势分析深挖"跳 `/strategy/tech-trend?tab=hotspot` |
