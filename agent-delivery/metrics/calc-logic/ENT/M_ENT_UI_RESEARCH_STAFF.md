# 科研人数（M_ENT_UI_RESEARCH_STAFF）

> **类型**：METRIC（企业属性指标）｜ **域**：企业分析／企业档案（基础信息）｜ **UI 挂载**：科技专题服务系统 → 企业分析 → 企业详情 → 基本信息区「科研人数」
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（UI 字段名直读，公式未给）｜ **批属**：1104 盘点·批2组1（TOPIC-UI-GAP-L01）
> **复现脚本**：`metrics/repro/M_ENT_UI_RESEARCH_STAFF.py`｜ **产物**：`metrics/repro/out/M_ENT_UI_RESEARCH_STAFF_out.json`
> **四判定摘要**：直接结构 = 是（live 列直读）；直接数据 = **无（0 行非空，B4 情形②）**；依赖结构 = 是（久新 ads_talent_* 人才粒度原料）；依赖数据 = 部分（127.8 万行人才记录在、机构映射未建）
> **数据源口径**：开发库 live + 三方库 gkx + 久新 jiuxin_warehouse（Doris，`ads_talent_yearly_metrics` 1,278,048 行实测）；**禁引 demo_\***。
> **铁律**：所有数字由复现脚本落 `_out.json` 产出。

## 〇、数据支持度与四判定口径

**本件判定：部分支持。** live `enterprise_base.rd_staff_count` 列**结构在**（直读即可复现页面语义），但 400 行底册**实测 0 行非空**——这是典型 B4 情形②（表/列存在但 0 数据），如实降档；久新 `ads_talent_yearly_metrics` 人才粒度原料 **1,278,048 行**在（`current_institution` 等列实测可算人才维），但久新机构 → 我方 org 映射未建立，企业维当前不可算。**升档触发器**：live 列灌数，或久新机构映射落地。

## 摘要

UI 企业详情基本信息区的「科研人数」字段。本件三源探针实测：live 直读列 0 行非空（B4 情形②）；久新人才年表 1,278,048 行在但为人才粒度（企业归集需机构映射）；gkx 无 rd_staff 类列。判档部分支持，不虚构数字。

## 一、需求定义概述

### 1.1 所属功能模块

科技专题服务系统 → 企业分析 → 企业详情 → 基本信息区「科研人数」。

### 1.2 为什么需要本指标

科研人数是科技型企业画像的核心字段（高企认定、专精特新评审均要求研发人员占比），页面在基本信息区直接展示。

### 1.3 需求文档是否给出定义方法

**需求文档没提及**本字段的统计口径（是否含兼职、是否按年末时点等）。

### 1.4 类似指标权威方法可行性分析概要

研发人员数通行口径族：①高企认定口径（认定年度科技人员数占比 ≥10% 的员工数）；②统计口径（R&D 人员折合全时当量，科技部统计）；③工商年报口径（从业人数中的技术人员）。本件 live 列的口径以甲方灌数时为准；久新路径的口径见附录 C。

### 1.5 引用来源

- UI 证据：live 30892 企业分析>企业详情>基本信息「科研人数」（20261104 盘点实拍）；缺口清单 seq33。
- 需求叶：`agent-delivery/bid-reference/科技专题服务算法库.md`（企业画像字段族，无本字段逐项口径）。
- 探针证据：`metrics/repro/out/M_ENT_UI_PAIN_BATCH_PROBE_out.json` + `M_ENT_UI_RESEARCH_STAFF_out.json`。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合）**：科研人数 = 该企业研发/科技活动人员数量（人）。**升档触发器**：①live `rd_staff_count` 灌数（列直读，零改造）；②或久新 `ads_talent_yearly_metrics.current_institution` → 我方 org 映射建立后按人才粒度聚合。

## 二、计算过程

### 2.1 live 直读面（当前不可出数）

```sql
SELECT enterprise_name, rd_staff_count FROM enterprise_base
WHERE rd_staff_count > 0 ORDER BY rd_staff_count DESC LIMIT 5;
-- 实测：rd>0 rows = 0，rd sum = None（400 行底册全空）
```

### 2.2 久新人才面（原料在、映射未建）

`ads_talent_yearly_metrics` **1,278,048** 行人才年度记录；`current_institution`（现机构）列实测在，人才维可算；企业归集卡在机构映射（见四）。

### 2.3 派生比（落产物）

| 派生键 | 数值 | 分子/分母 |
|---|---:|---|
| `rd_pos_row_share_pct` | 0.0 | 0 / 400（rd_staff_count > 0 行占比） |
| `rd_nonnull_row_share_pct` | 0.0 | 0 / 400（rd_staff_count 非空行占比） |

### 2.4 确定性声明

全 SQL 计数，重跑逐位一致（B5）；0 就是 0，不虚构。

### 2.5 复现代码结果展示

- 代码：`metrics/repro/M_ENT_UI_RESEARCH_STAFF.py`（退出码 0）；关键数字：400 / 0 / 1,278,048。
- 需求符合性评审：live 列语义直读成立；数据缺 → 部分支持。

## 三、数据支撑情况

| 依赖 | 库·表 | 行数 | 结论 |
|---|---|---:|---|
| 直读列 | live.enterprise_base.rd_staff_count | 400 底册 / **0 非空** | **B4 情形②：结构在、数据缺** |
| 人才粒度原料 | 久新 ads_talent_yearly_metrics | 1,278,048 | 在（current_institution 实测；企业维待映射） |

## 四、数据缺失情况

- live 直读列 0 行非空（B4 情形②）→ 当前页面该字段即使接上也是空。
- 久新机构 → 我方 org 映射未建立 → 人才粒度无法归集到企业维。
- gkx 无 rd_staff 类承载（批探针零命中）。

## 参考文献

不适用（UI 字段直读口径；通行口径族见 1.4，无单篇文献承载本件口径）。

# 附件

## 附录 A 原始需求原文摘录

需求文档仅有「科研人数」字段名（企业画像字段族），无统计口径原文（如实披露）。

## 附录 B 历史库表探测证据

`M_ENT_UI_PAIN_BATCH_PROBE_out.json`：久新 ads_talent_* 族表清单与行数；`M_ENT_UI_RESEARCH_STAFF_out.json`：live 0 行非空实测（rd>0 rows = 0）。

## 附录 C 可行性报告完整版

口径族对照：①高企认定口径 ②R&D 全时当量 ③工商年报技术人员。路径对照：live 直读（零改造，等灌数）vs 久新聚合（原料 127.8 万行在，卡机构映射）。两路任一落地即升档。
