# DEC-E7-PORTAL-RANK-PRESENTATION · 力度榜呈现（P-20）

| 字段 | 值 |
|---|---|
| id | `DEC-E7-PORTAL-RANK-PRESENTATION-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认） |
| approval_status | `approved` |
| source_relation | product_interpretation |
| 上级 | `DEC-E7-PORTAL-TAB-MERGE-A-20260807` · `DEC-E7-PORTAL-STATS-INDUSTRY-COMPARE-20260807` |
| Bid | P-20（§1.1.1.1.1.1.2.4） |

## 决策（已确认）

门户概览 `view=rank`（政策力度排名）呈现合同：

1. **不绑产业 / 对照 / geo**：力度另轴；本地仅「省级排名 | 城市排名」切换（与 STATS-INDUSTRY-COMPARE 一致）。
2. **招标「对政策的关键指标进行提取」**：上游加工能力，产出区域力度指数；门户可见结果为榜单，**不**另开「指标提取」交互页。
3. **榜体单呈现**：需求未要求多图；**去掉**与排名表趋同的条形榜；**去掉**摘要 KPI 卡条。
4. **Top3 领奖台**：效果图样式——银（左）/ 金（中抬高）/ 铜（右）；缎带名次 + 奖杯；底栏三指标（力度指数 / 政策量 / 覆盖率）。
5. **全量榜**：一张排名表（排名 / 省或市 / 力度指数 / 政策量 / 产业覆盖率）；分页默认 15。
6. **口径（仅评审模式）**：挂「力度指数口径」+ `MetricSpecCard` ⓘ + `MockBadge` 🧪 + `PendingBadge` ⚠️（QPOL-02）；业务态不展示榜首摘要句与口径文案；禁止正文裸 emoji。

## scope_effect

不增删 Bid 叶子；收紧 P-20 Demo/文档呈现，避免双榜/KPI 冗余。
