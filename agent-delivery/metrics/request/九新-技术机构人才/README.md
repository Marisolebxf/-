# JIUXIN-TECH-ORG-TALENT-L01 · 北京九新交付形态清单

> **日期**：2026-08-24  
> **任务**：`JIUXIN-TECH-ORG-TALENT-L01`（spike）  
> **执行**：`agent:product-agent` · **监管**：`human:淮政玮`  
> **对九新开会**：仍待 `human:郭万迎` 持本表谈；`human:李伟` 辅助抽清单（本叶已按 A2 yaml 抽完）  
> **铁律**：未与九新开会 **不得** 把「九新确认」写成「确认」或「九新已交」。本批 **待确认 = 51**。

## 给人主数字（对人主表 51 行）

| 交付形态 | 条数 | 沟通起点（非最终） |
|----------|------|--------------------|
| **SQL** | **3** | `STAT`：seq 96 技术基础指标 / 99 科研机构基础指标 / 98 人才基础指标 |
| **Python** | **6** | `GRAPH`：seq 104–105 / 114–115 / 110–111（Nebula，禁止 Neo4j） |
| **API** | **42** | 28 条深度库叶 + 1 条无专叶（TOPIC-RORG-012）+ 13 条展示 third_party |
| **待确认** | **51** | 确认 = 0 · 九新不提供 = 0 |

拆开：库叶 37 + 无专叶 1 + 展示 third_party 13 = **51**。

xlsx「计数」sheet 用公式跟对人主表 H/I 列，改确认状态后数字会跟着变。

## 文件

| 文件 | 读者 |
|------|------|
| `JIUXIN-TECH-ORG-TALENT-L01.xlsx` | 郭万迎对九新；淮政玮抽检 |
| `JIUXIN-TECH-ORG-TALENT-L01.yaml` | 机器真源，与 xlsx 对人主表同行 |
| `JIUXIN-TECH-ORG-TALENT-L01-minutes.md` | 会前清单 / 会后改确认列的唯一入口 |
| 本 README | 计数 |

xlsx sheets：`对人主表` · `专题回溯` · `展示人才mapped` · `不进本包` · `计数`。

## `algorithm.type`

A1（`ALGO-LIB-METRIC-DEPS-L01`）已签收，三维 `coverage_status` 多为 `third_party`（**不伪展开公式**）。  
本叶 **交付形态仍按 SRS 层** 问九新（基础→SQL、图谱→Python、深度/实现类→API），**不**因为 A1 标了 third_party 就把 51 条全改成 API。  
`algorithm.type` 列 = SRS 层暂标；唐绍祖会签后的 seed `algorithm_type` 不在本叶回写。

## 禁止

- 前端直连九新；调用链仍 前端 → Java REST → Python `/internal/*`
- 改 `cfg_metric-*-seed.yaml`、写业务代码、挡 A1、复活废作四叶
- 把 `ENT-SEARCH-009`（企业份额 Q019）或 `DS-CHAIN-OV-009/010`（投融资 QC07）写进对人主表
- 把 DS-16 六条 A2 `missing` 写成「九新已承诺 API」
