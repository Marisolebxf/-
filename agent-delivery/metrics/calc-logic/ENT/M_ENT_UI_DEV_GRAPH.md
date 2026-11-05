# 产业生态图谱（M_ENT_UI_DEV_GRAPH）

> **类型**：UI-ENTRY-STRUCTURE（页面图谱入口，底座=产业链树+企业挂接面）｜ **域**：企业分析／企业发展｜ **UI 挂载**：科技专题服务系统 → 企业分析 → 企业发展 → DevelopmentOverviewPanel 图谱卡
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（图谱口径 UI 未给）｜ **批属**：1104 盘点·批2组2（TOPIC-UI-GAP-L01）
> **复现脚本**：`metrics/repro/M_ENT_UI_DEV_GRAPH.py`｜ **产物**：`metrics/repro/out/M_ENT_UI_DEV_GRAPH_out.json`｜ 批探针：`metrics/repro/out/M_ENT_UI_DEVCLUSTER_BATCH_PROBE_out.json`
> **四判定摘要**：直接结构 = 无（无现成图谱结果面）；直接数据 = 无；依赖结构 = 是（链树 1,273 节点 + 企业行业四级列）；依赖数据 = 部分（链树 node_company_count 全 0，企业挂接数未灌）
> **数据源口径**：开发库 live + 三方库 gkx + 久新 jiuxin_warehouse（ads_technology_graph_node/edge 表名探针留证，行数待账号解锁补测）；**禁引 demo_\***。
> **铁律**：本文档所有数字由复现脚本落 `_out.json` 产出；`demo_gkxlumenx_*` 已废弃禁引。

## 〇、数据支持度与四判定口径

**本件判定：部分支持。** 图谱数据底座**现在**可搭：gkx `dwd_industry_chain_info` 链树 **1,273** 节点（`parent_code` 齐备）+ 企业底册 L1-L4 行业列（L1 覆盖 **186,809/189,116** 家，98.7801%）。但两处缺口：①链树 `node_company_count` 实测**全 0**（企业挂接数未灌，图谱节点热度无法渲染）；②页面「图谱」语义（节点热度规则/边关系/图例）UI 未给口径 → 部分支持。**升档触发器**：`node_company_count` 灌数或甲方图谱口径闭合。

## 摘要

UI 企业发展页的产业生态图谱卡。本件复现其数据底座：链树 1,273 节点 + 企业挂接面（98.78% 可挂）实测；企业挂接数与图谱规则两处缺口如实披露。判档部分支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技专题服务系统 → 企业分析 → 企业发展 → 产业生态图谱（DevelopmentOverviewPanel 图谱入口卡）。

### 1.2 为什么需要本指标

图谱是企业发展页的核心可视化入口：以产业链节点为骨架、企业挂接为肉，支撑「看生态—选节点—查企业」的下钻动线。

### 1.3 需求文档是否给出定义方法

**需求文档没提及**图谱的节点热度、边类型、图例分级等口径；仅页面证据（图谱卡入口）。

### 1.4 类似指标权威方法可行性分析概要

产业图谱通行方法族：①产业链树 + 企业归属映射（本件采用，两块结构均实测在）；②企业-企业关系图（投资/供应链边，见 `M_ENT_UI_SUPPLY_PREFLIGHT` 承载）；③知识图谱（实体抽取，久新 `ads_technology_graph_node/edge` 为技术知识图方向）。完整版见附录 C。

### 1.5 引用来源

- UI 证据：live 30892 企业分析>企业发展>DevelopmentOverviewPanel 图谱卡（20261104 盘点实拍）；缺口清单 seq34（1104 盘点任务产出，出处登记见主表「挂载来源」列）。
- 需求叶：`agent-delivery/bid-reference/科技专题服务算法库.md`（产业链图谱相关模型叶）。
- 探针证据：`metrics/repro/out/M_ENT_UI_DEVCLUSTER_BATCH_PROBE_out.json`（链树/集群/底册三源扫描）。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合）**：产业生态图谱 = 产业链树节点为骨架、按企业行业归属挂接企业的生态可视化底座。**升档触发器**：①`node_company_count` 灌数（节点企业数可渲染）；②甲方给出图谱规则（热度/边/图例）。

## 二、计算过程

### 2.1 链树结构面

gkx `dwd_industry_chain_info` **1,273** 行、distinct `industry_code` **1,273**（一码一节点）；`parent_code` 全部非空（1,273/1,273）；`level` 实测全部为 0（单层清单式存储，树形由 `parent_code` 递归构成）；`node_company_count` **全 0**（企业挂接数未灌）。表列含 `industry_code/industry_name/industry_link_code/industry_link_name/level/parent_code/parent_name/node_company_count`。

### 2.2 企业挂接面

gkx `dwd_org_base_info` 底册 **189,116** 家；`industry_l1_code` 非空 **186,809** 家（**98.7801%**，derived 落产物）；`industry_l4_code` 细粒度列同样在（L1→L4 四级行业码可挂图谱对应层级节点）。

### 2.3 派生比（落产物）

| 派生键 | 数值 | 分子/分母 |
|---|---:|---|
| `chain_node_org_coverage_pct` | 98.7801 | 186,809 / 189,116（底册 L1 行业码非空占比，企业可挂图谱节点的比例） |

### 2.4 确定性声明

全 SQL 计数，无随机无采样，重跑逐位一致（B5）。

### 2.5 复现代码结果展示

- 代码：`metrics/repro/M_ENT_UI_DEV_GRAPH.py`（退出码 0）；关键数字：1,273 / 186,809 / 98.7801%。
- 需求符合性评审：底座成立；挂接数与图谱规则两处缺口如实披露。

## 三、数据支撑情况

| 依赖 | 库·表 | 行数 | 结论 |
|---|---|---:|---|
| 产业链树 | gkx.dwd_industry_chain_info | 1,273 | 在（parent_code 齐；node_company_count 全 0） |
| 企业底册·行业四级列 | gkx.dwd_org_base_info | 189,116（L1 非空 186,809） | 在（98.78% 可挂接） |

## 四、数据缺失情况

- `node_company_count` 全 0（企业挂接数未灌）→ 节点热度渲染缺数。
- 图谱口径（热度/边/图例）UI 未给（甲方缺口）。
- 久新 `ads_technology_graph_node/edge` 补测完成（2026-11-04 解锁后）：**node 19,430 行 / edge 587,252 行**，节点含 `community_id/weighted_degree`、边含 `relation_type/relation_confidence_score`——为技术知识图谱（技术节点粒度），非企业挂接面，可作图谱「技术关系层」参考数据源。

## 参考文献

不适用（UI 入口结构件、推测定义；方法族为产业链树+归属映射，无单篇文献承载本件口径）。

# 附件

## 附录 A 原始需求原文摘录

需求文档无图谱专项口径原文；页面证据为 DevelopmentOverviewPanel 图谱卡入口（如实披露）。

## 附录 B 历史库表探测证据

`metrics/repro/out/M_ENT_UI_DEVCLUSTER_BATCH_PROBE_out.json`：gkx 链树/集群/企业底册/供应链面全扫描；久新 245 表 eco/graph/chain/enterprise 类命中表清单（含 `ads_technology_graph_node/edge`）。

## 附录 C 可行性报告完整版

方法族对照：①产业链树+归属映射（本件采用，结构实测在）②企业关系图（投资边 46,967 行在，见预检件）③知识图谱（久新技术图方向，行数待补测）。缺口两项（挂接数灌数、图谱口径闭合）任一落地即升档。
