# 展示窗口 · DS-10/11/12 科技政策跟踪

```yaml
---
doc_id: POLICY-WINDOW-DISPLAY-DS10-12
element: POLICY
role: source
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: null
task_id: DATA-POLICY-STORAGE-S3-L01
amendment: "展示系统窗口对照；不翻签 POLICY-STORAGE-FLOW 工厂拓扑"
---
```

> **窗口 ≠ 第二套库。** 科技政策跟踪与专题 E7 / 算法库 `polan` **共用** `policy_base_info` + `policy_*` ADS + 一张 G。  
> **禁止**：为展示再造 `display_policy_*` 平行 DWD；前端 fixture 当正式契约；浏览器直连 Nebula / Python。

## 1. 需规与原型真源

| 层 | 路径 |
|---|---|
| SRS 叶子 | `bid-reference/srs/02-科技信息展示系统/科技政策跟踪/`（全景 / 分析评价 / 效果推演） |
| 核增 | `bid-reference/科技信息展示系统(政策对比功能升级)核增需求.md` §4.2.4 |
| 产品包 | `agent-handoffs/产品整体定义/DS10-12-科技政策跟踪/` |
| Demo 原型 | `${GKX_ROOT}/repos/demo-ui-science/src/pages/policy-tracking/`（`PolicyPanorama` / `PolicyAnalysis` / `PolicySimulation` / `PolicyPcPages`） |
| 现网原型数据 | **fixture**：同目录 `policyData.js` / `policyPcData.js` 等。`USE_MOCK=false` 时禁止再用其填数 |

TRACE：展示 `/display/policy/*` **分轨**专题 `/policy/*` 与门户 `/policy-portal/*`。

## 2. 页面 → 存储（已有 ADS / DWD 能扛的）

| 原型 / Frame | SRS | 读 |
|---|---|---|
| 全景 KPI / 层级 / 类型 / 地图 / 时序 | 科创政策全景 · 多维检索+动向 | `policy_level_dist` `policy_type_dist` `policy_national_dist` `policy_sz_dist` `policy_timeseries`；列表筛 `policy_base_info` |
| 评价效能 / 焦点 / 短板 / 布局 | 政策分析评价 | `policy_effect` `policy_focus` `policy_metric_timeseries` |
| 推演预估 KPI | 政策效果推演 · 效果预估 | 同上 + **任务快照**（见 OPEN） |
| 推演关联图 | 政策关联分析 | 一张 G / `policy_graph_*`；前端只经 Java |
| PC01 治理 | 核增底座 | `M_POLICY_TOTAL_COUNT` / `VALIDITY_RATE` + `pipeline_status`（非业务 ADS） |
| PC02 拆解力度/关联 | 文本智能解析 | `policy_intensity` + 图 hang；条款树见 OPEN |
| PC03 对比 | 核增多维对比 | 已有力度/适配指标；对象集 = `policy_id[]`（上限 5，会话态） |
| PC04 研报 | 智能研报 | 指标结论 + MinIO 对象；溯源回 DWD `content`/`url` |

筛选维对齐贴源 DDL：国内 `type`（类别）`ministry`（部门）`province/city/district`（地区）`rank`（国家级/省级/市级/区县级）`status`（有效/失效文案）`keywords` `title`；不得另起类型表。行业 hang `industry_link_code`。海外读 `dwd_global_policy_base` 的 `category`/`country`/`region`/`organ`。`policy_support` JSON 给扶持/申报，不另造扶持宽表。

## 3. 原型有、工厂尚未落表（draft · 不自填绿）

| ID | 能力 | SRS / 原型 | 存储落点（候选） | 本波 |
|---|---|---|---|---|
| OPEN-POLICY-DISP-01 | 检索历史 / 收藏 | 全景 序号 201；Wireframe `search_history_id` | 账户/会话表，**不是** ADS 工厂 | 不进 `policy_*` |
| OPEN-POLICY-DISP-02 | 订阅推送 | 全景 序号 204；`policySubscription.js` | 同上 + 通知；条件 JSON | 不进工厂主链 |
| OPEN-POLICY-DISP-03 | 浏览量 / 智能排序权重 | 全景 序号 199 | DWD 扩展或行为日志 | 缺列则排序退化为时间/级别 |
| OPEN-POLICY-DISP-04 | 舆情正负中 / 话题热力 | 评价页 `TopicHeatmapWithSentiment` | **禁止**无源造 ADS；D3 none 则 Mock 角标 | 不伪闭合 |
| OPEN-POLICY-DISP-05 | 未出台仿真多轮对比 | 推演 序号 232；`EstimateWorkbench` | 分析任务 + 结果快照（I2-12）；Java 签发 | 不写回 ODS |
| OPEN-POLICY-DISP-06 | 拆解条款树 / 指标提取表 | PC02；推演解析 | `policy_parse_*` draft 另单 | 正文仍在 DWD |
| OPEN-POLICY-DISP-07 | 来源监控/抓取 | 全景 序号 203 | **ETL 入站**，不在展示仓爬 | 治理看板只读批次 |
| OPEN-POLICY-DISP-08 | 利益攸关方问卷 | 推演 序号 236 | 不进政策要素库 | Mock 至有产品表 |
| OPEN-POLICY-DISP-09 | 导出 Excel/PDF | 全景 202；研报 PDF | MinIO `policy/{task_id}/` | 元数据在任务表 |

## 4. 调用链（展示）

```text
目标态：demo-ui-science / lumen-ui-science-*  → 网关 → Java 只读 ADS（+ Feign /internal 要图/推演）
Demo 现网：policy-tracking 读本地 fixture（虚线 as-built）
禁止：展示前端直连 polan；与专题共用检索 storage key
```

## 5. 禁止

- 第二张 G / `gkx_policy` space  
- 展示专用平行 `policy_base_info`  
- 把 `policyData.js` 行数当 ADS 真值  
- 抓取互联网写入本树当「已接入」
