# IA-ZHIKU-STRATEGY-ROADMAP｜领域技术线路 信息架构

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **上游**：USM-ZHIKU-STRATEGY-ROADMAP.md（同目录）
> **原始需求**：拆解表 §2.4 序号 46-49

## 1. 来源与目标

| 项 | 内容 |
| --- | --- |
| 需求来源 | 新型高端智库需求拆解.md §2.4 领域技术线路（4 项） |
| 模块目标 | 德尔菲专家共识 + 技术路线图设计双工作线的一体化工作区，路线结论可直通报告创作 |
| 承接批次 | R5（收编 S3 P52-P53 旧页资产） |

## 2. 覆盖与不覆盖

- **覆盖**：概览速航、德尔菲问卷四态全流程、路线图项目管理、里程碑设计器、版本快照、开发精度总览、生成路线研判报告出口。
- **不覆盖**：问卷题目编辑器与专家名单管理（预置模板）、真实分发渠道（🧪 站内演示）、多人协同/审批流、甘特依赖线、报告写作本体（归 ZHIKU-WRITING）。

## 3. 产品角色与权限

| 角色 | 可见范围 | 关键动作 |
| --- | --- | --- |
| `ROLE-RM-PLANNER` | 全模块 | 新建/编辑路线、里程碑、快照、生成报告 |
| `ROLE-RM-SURVEYOR` | 全模块 | 新建/发放/催办/归档问卷 |

demo 单用户代演，不做真实权限闸；角色确认挂 Q-ZHIKU-01。

## 4. 对象与稳定标识

| 对象 | id 规则 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| DelphiSurvey 问卷 | `dp-<ts>` | draft→distributing→collecting→archived（单向） | `zhiku-rm-surveys` |
| SurveyActivity 问卷动态 | 内嵌于问卷 | 追加不可删 | 随问卷 |
| RoadmapProject 路线项目 | `rm-<ts>` | 创建→编辑→（无删除，demo 简化） | `zhiku-rm-projects` |
| Milestone 里程碑 | `ms-<ts>` | 增删改（至少保留 1 个） | 随项目 |
| RoadmapSnapshot 快照 | `snap-<ts>` | 追加；恢复前自动另存 | 随项目 |
| UI 偏好 | — | 标签页/筛选条件 | `zhiku-rm-ui` |

## 5. IA 结构与 Frame 职责

```
领域技术线路 /strategy/tech-roadmap
├─ Tab 概览               F-RM-01 统计卡×3 + 最近项目混排列表
├─ Tab 德尔菲问卷          F-RM-02 阶段筛选 + 问卷列表 + 新建/发放/催办/归档 + 结果分布
├─ Tab 技术发展路线        F-RM-03 宏观统计 + 筛选 + 项目列表 + 设计器(?project=)
│                                 设计器：时间轴 + 里程碑 CRUD + 快照 + 生成报告出口
└─ Tab 开发精度            F-RM-04 四模块完成度卡 + 子项明细抽屉
```

| Frame | 责任 | 关键状态 |
| --- | --- | --- |
| F-RM-01 | 总览与速航 | 空态（无项目）双入口 |
| F-RM-02 | 问卷全流程 | 四阶段态、催办幂等、归档只读 |
| F-RM-03 | 路线管理+设计器 | 列表态/设计器态（URL 承载）、快照回看只读态 |
| F-RM-04 | 完成度总览 | 演示口径 🧪 标注 |

## 6. 数据与服务边界

- 全 mock：领域 store `useTechRoadmapStore`（重构后），reducer 式 action + `makePersist('zhiku-rm-')`。
- 目标态：Java REST（gkxlumen-topic 聚合），本模块不直连 Python/nGQL。
- 回收进度模拟推进为前端定时器（🧪），页面卸载后由 store 恢复逻辑续跑。

## 7. 指标（D9）

| metric_id | 中文名 | 位置 | 状态 |
| --- | --- | --- | --- |
| `ZHIKU-RM-SURVEY-TOTAL` | 德尔菲问卷总数 | F-RM-01 | 新增，draft/mock |
| `ZHIKU-RM-DELPHI-COMPLETION` | 德尔菲问卷·平均完成率 | F-RM-01/02 | rename ← `ZHIKU-S3-DELPHI-COMPLETION` |
| `ZHIKU-RM-PROJECT-INPROGRESS` | 技术发展路线·在建项目数 | F-RM-01/03 | rename ← `ZHIKU-S3-ROADMAP-PROJECT-TOTAL` |

## 8. 跨模块契约

| 契约 | 方向 | 载荷 | 说明 |
| --- | --- | --- | --- |
| CT-RM-01 生成路线研判报告 | ZHIKU-STRATEGY-ROADMAP → ZHIKU-WRITING | `createTask`(type=research, 大纲注入项目名/里程碑统计/快照说明) | 跳转写作大纲确认页 |
| 概览互通 | ← 全局导航 | 路由 `strategy-tech-roadmap` | 菜单真源 menu.ts |
