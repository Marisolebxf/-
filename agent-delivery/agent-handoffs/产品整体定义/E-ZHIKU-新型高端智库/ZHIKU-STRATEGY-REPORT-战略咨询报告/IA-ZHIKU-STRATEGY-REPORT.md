# IA-ZHIKU-STRATEGY-REPORT｜战略咨询报告与成果 信息架构

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **上游**：USM-ZHIKU-STRATEGY-REPORT.md（同目录）
> **原始需求**：拆解表 §2.5（50-53）+ §2.6（54）

## 1. 来源与目标

| 项 | 内容 |
| --- | --- |
| 需求来源 | 新型高端智库需求拆解.md §2.5 战略咨询报告（4 项）+ §2.6 战略咨询成果（1 项） |
| 模块目标 | 研究资产沉淀（研报/洞察/热点）→ 战略报告生成 → 成果对外展示的价值转化链 |
| 承接批次 | R5（收编 S1 P09-P15 旧页资产；承接 R1 发布进成果契约） |

## 2. 覆盖与不覆盖

- **覆盖**：研究报告全生命周期（上传/编辑/版本/归档/删除/导出）、洞察月刊浏览订阅、三方向热点分析、战略报告生成向导（跨叶子出口）、成果四统计卡+ROI 筛选+详情、已发布报告承接区。
- **不覆盖**：真实 NLP 摘要/质检/脱敏/推荐算法（🧪 规则式）、真实推送通道、报告写作本体（ZHIKU-WRITING）、案例后台维护。

## 3. 产品角色与权限

| 角色 | 可见范围 | 关键动作 |
| --- | --- | --- |
| `ROLE-SP-RESEARCHER` | 研究报告 Tab | 上传/编辑/版本/归档/删除 |
| `ROLE-SP-READER` | 洞察/热点 Tab | 浏览/订阅/导出 |
| `ROLE-SP-CONSULTANT` | 生成/成果 | 勾底料生成、成果浏览 |

demo 单用户代演；角色确认挂 Q-ZHIKU-01。

## 4. 对象与稳定标识

| 对象 | id 规则 | 生命周期 | 持久化 |
| --- | --- | --- | --- |
| ResearchReport 研究报告 | `RR-<ts>`（种子 RR-001…） | parsing→ready→(archived)；删除有引用拦截 | `zhiku-sp-research` |
| ReportVersion 版本 | 内嵌 v1..n | 追加 | 随报告 |
| InsightIssue 洞察月刊 | `IR-*` | 只读种子 + 订阅态 | `zhiku-sp-insight-sub` / `zhiku-sp-insight-push` |
| Hotspot 热点 | `HS-*` | 只读种子 | — |
| GenerationRecord 生成记录 | `GEN-<ts>` | 追加；底料失效标注 | `zhiku-sp-generations` |
| StrategyCase 成果案例 | `CASE-*` | 只读种子（含投资/ROI/满意度扩展字段） | 过滤态 `zhiku-sp-ui` |
| 已发布报告 | 引用 writing taskStore.published | 由 WR 链路驱动 | 由 `zhiku-wr-` 承载 |

## 5. IA 结构与 Frame 职责

```
战略咨询报告 /strategy/report-mgmt         成果 /strategy/case-show
├─ Tab 研究报告        F-SP-01              F-SP-05 四统计卡 + ROI筛选
│   列表/上传/详情抽屉/版本/归档(研报库分组)  + 案例卡片 + 详情弹窗
├─ Tab 洞察月刊        F-SP-02              + 已发布报告承接区
│   期次卡 + 详情 + 订阅 + 推送记录 + 导出    （writing/cases 共享案例源）
├─ Tab 热点分析        F-SP-03
│   三方向切换 + 榜单 + 四源构成抽屉
└─ Tab 战略报告生成    F-SP-04
    底料三栏勾选 + 要点预览 + 生成历史
```

| Frame | 责任 | 关键状态 |
| --- | --- | --- |
| F-SP-01 | 研报全生命周期 | 解析中骨架/就绪/归档、删除引用拦截 |
| F-SP-02 | 月刊+订阅 | 订阅开关幂等、推送 Empty |
| F-SP-03 | 热点研判 | 指数红问号（D1 missing）、方向 Empty |
| F-SP-04 | 生成向导 | 底料未选禁用、失效底料标注 |
| F-SP-05 | 成果展示 | ROI 筛选态、发布承接 Empty |

## 6. 数据与服务边界

- 全 mock：领域 store `useStrategyReportStore`（研报/洞察/热点/生成）+ `useStrategyCaseStore`（案例，供两入口共享），reducer 式 action + `makePersist('zhiku-sp-')`。
- 已发布报告只读消费 `useWritingTaskStore.published`，不复制数据（单一真源）。
- 目标态 Java REST（gkxlumen-topic/metrics），前端不直连算法。

## 7. 指标（D9）

| metric_id | 中文名 | 位置 | 状态 |
| --- | --- | --- | --- |
| `ZHIKU-SP-RESEARCH-TOTAL` | 研究报告总数 | F-SP-01 | 新增 draft/mock |
| `ZHIKU-SP-INSIGHT-TOTAL` | 洞察报告库报告总数 | F-SP-02 | rename ← `ZHIKU-S1-INSIGHT-TOTAL` |
| `ZHIKU-SP-HOTSPOT-INDEX` | 热点热度指数（演示态） | F-SP-03 | 新增 **D1 missing**（四源指标体系算法未落地，GAP + Q-ZHIKU-04） |
| `ZHIKU-SP-CASE-TOTAL` | 成果案例总数 | F-SP-05 | rename ← `ZHIKU-S1-CASE-TOTAL` |
| `ZHIKU-SP-CASE-INVEST-TOTAL` | 成果案例·总投资额（演示态） | F-SP-05 | 新增 draft/mock（口径待甲方） |
| `ZHIKU-SP-CASE-ROI-AVG` | 成果案例·平均投资回报率（演示态） | F-SP-05 | 新增 draft/mock（口径待甲方） |
| `ZHIKU-SP-CASE-SATISFACTION` | 成果案例·客户满意度（演示态） | F-SP-05 | 新增 draft/mock（口径待甲方） |
| `ZHIKU-SP-ACHIEVEMENT-PUBLISHED` | 已发布报告成果数 | F-SP-05 / 案例广场 | 新增（承接 WR published 口径） |

## 8. 跨模块契约

| 契约 | 方向 | 载荷 | 说明 |
| --- | --- | --- | --- |
| CT-SP-01 生成战略咨询报告 | ZHIKU-STRATEGY-REPORT → ZHIKU-WRITING | `createTask`(type=strategy，大纲注入底料要点) | 生成历史留痕+任务回链 |
| 发布进成果（承接） | ZHIKU-WRITING → ZHIKU-STRATEGY-REPORT | taskStore.published 只读消费 | R1 契约，本包重构后复验不回归 |
| 热点↔月刊互通 | 模块内 | issueId 回链 | F-SP-03 → F-SP-02 |
