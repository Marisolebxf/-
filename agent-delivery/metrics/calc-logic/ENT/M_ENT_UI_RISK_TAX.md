# 税收违法数（M_ENT_UI_RISK_TAX）

> **类型**：COUNT｜ **域**：企业分析／企业查询／企业画像｜ **UI 挂载**：科技专题服务系统 → 企业分析 → 企业查询 → 企业画像抽屉（风险信息 tab 计数卡）
> **数据支持度**：**完全转换支持**｜ **公式定义人**：仿王惠（UI 未给口径；推测定义=企业维度确定性计数）
> **四判定摘要**：直接结构 = 是（gkx 源表在，org_id 全覆盖）；直接数据 = 是；依赖结构 = 是（企业底册 org_id）；依赖数据 = 是
> **数据源口径**：开发库 live（gkxlumenx_*，仅风险表族 0 行披露）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin_warehouse（242 张 ads_* 探针留证）；**禁引 demo_\***。

## 〇、数据支持度与四判定口径

（四档定义：完全直接支持 / 完全转换支持 / 部分支持 / 完全不支持；判定一律点名库别，只写「开发库」视为未调研三方库与久新库。）

**完全转换支持**。gkx `dwd_org_risk_tax_punish` 有数（528 行）且 org_id **全覆盖（528/528，2026-11-04 复核探针更正早前「无 org_id 列」的误判）**——现在就能按企业确定性复算；久新无风险结果面（242 张 ads_* 探针留证）；live `risk_tax_punish` 表结构在、0 行，不参与本档判定（补数后可直查升「完全直接支持」）。

## 摘要

UI「企业画像抽屉·风险信息」展示「税收违法数」计数卡（enterpriseSearchConfig.ts `detailTabs` risk tab，`dataSource: 待源（司法/失信，Q020）`）。需求文档未给该卡定义方法，本件走推测定义（企业维度确定性计数）。本件判档：**完全转换支持**——gkx `dwd_org_risk_tax_punish` 实算可复算（528 行，org 关联 100%）。

## 一、需求定义概述

### 1.1 所属功能模块

科技专题服务系统 → 企业分析 → 企业查询 → 企业画像抽屉 → 风险信息（tab9）。

### 1.2 为什么需要本指标

企业画像风险面把一家企业的税务违法暴露压缩为单值计数卡，是尽调、招引前筛查与培育评估的风险眼。税收违法（重大税收违法失信主体）属高权重信用负面项，常与失信被执行并列展示。

### 1.3 需求文档是否给出定义方法

**需求文档没提及本卡的定义方法。** UI 配置源码即证据：`repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103` `{ key: 'risk', label: '风险信息', pending: true, dataSource: '待源（司法/失信，Q020）' }`——前端明示待源、无口径。

### 1.4 类似指标权威方法可行性分析概要

税收违法公布记录计数，权威口径 = 国家税务总局「重大税收违法失信主体」公布信息（登记记录计数方法族），无需建模假设。数据面为税务公布记录镜像计数。结论：方法可行；争议仅在**关联口径**（企业主体 vs 法定代表人），已在 §二披露。完整版见附录 C。

### 1.5 引用来源

- UI 源码：`repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103`（risk tab 定义）。
- 需求叶：`agent-delivery/bid-reference/科技专题服务算法库.md` §1.1.1.1.1.1.1.5.3–5.4（风险维旁证；**无本卡逐项叶子**——如实披露「三份需求说明书均未单列本卡」）。
- 探针证据：`metrics/repro/out/M_ENT_UI_RISK_BATCH_PROBE_out.json`（三源批量探针，2026-11-04）。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合）**：COUNT(*) WHERE org_id = :企业。

**升档触发器**：live `risk_tax_punish` 灌数后可直查升「完全直接支持」。

## 二、计算过程

### 2.1 口径与公式

$$\text{税收违法数} = \text{COUNT}(*) \quad \text{s.t.} \quad \text{org\_id} = :\text{企业}$$

（UI 卡值 = 单企业维度计数；批内无权重、无派生比，纯 COUNT 面件。）

### 2.2 复现代码结果展示

- 代码：`metrics/repro/M_ENT_UI_RISK_TAX.py`（退出码 0，产物 `metrics/repro/out/M_ENT_UI_RISK_TAX_out.json`）。
- 实测：源表 528 行、org 关联 528/528（100%）、按企业计数 Top10（首名「深圳市科上美电子有限公司」6 次）、计数分布，见产物 `facts` 段。

## 三、数据支撑情况

| 依赖维 | 库别 | 表 | 行数/覆盖 | 结论 |
|---|---|---|---|---|
| 源面 | gkx | dwd_org_risk_tax_punish | 528 行 | 有数 |
| 企业关联 | gkx | dwd_org_risk_tax_punish | org_id 全覆盖（528/528） | 全量可关联 |
| 兜底面 | live | gkxlumenx_dwd risk_tax_punish | 结构齐全、**0 行** | 待补数据同步（不作结果面） |
| 第三源 | 久新 | 242 张 ads_* | 风险类 7 张均非本卡语义 | 无承载（探针留证） |

久新 gkx_technology_analysis_dev 242 张 ads_* 风险类命中 7 张（ads_research_outcome_trend_case 22,881 / ads_technology_application_case 181,735 等），均为技术/人才/机构要素面，**无税务违法结果面**——三源探针留证（out/M_ENT_UI_RISK_BATCH_PROBE_out.json）。

## 四、数据缺失情况

- 表内含 `case_type`/`report_period`/`publish_date` 等可下钻维；528 行规模小（重大违法公布面本来就窄），语义与 UI 卡「税收违法数」相符。
- live gkxlumenx_dwd risk_* 表族（18 张+字典）结构齐全但 0 行——若按「先灌数后直查」路径走，本卡族可整体升档；该灌数属共享库写入，须用户授权另单执行。

## 参考文献

不适用（推测定义 + 登记计数方法族，无单行可引公式文献；方法族说明见 §1.4 与附录 C）。

# 附件

## 附录 A 原始需求原文摘录

- 三份需求说明书（`agent-delivery/bid-reference/科技专题服务算法库.md`、`科技信息展示系统和科技专题服务系统.md`、`科技信息展示系统(政策对比功能升级)核增需求.md`）均**未单列「税收违法数」逐项叶子**；同域旁证段落 = 科技专题服务算法库 §1.1.1.1.1.1.1.5.3–5.4（痛难点识别「风险防控」/供应链关系模型）。无无关长文。

## 附录 B 历史库表探测证据

- 批量探针：`metrics/repro/M_ENT_UI_RISK_BATCH_PROBE.py` → `out/M_ENT_UI_RISK_BATCH_PROBE_out.json`（2026-11-04，三源）。
- live 表族行数补探：`metrics/repro/out/_live_risk_tables_probe.json`（18 表+enterprise_bid 全 0 行实证）。

## 附录 C 可行性报告完整版

**方法族对照**

| 方法族 | 来源 | 贴合度 | 采用 |
|---|---|---|---|
| 登记记录计数 | 国家企业信用信息公示系统/税务总局重大税收违法公布口径 | 高（中国官方口径） | 是 |
| 信用评分模型 | 境外商业征信（D&B 等） | 低（超出 UI 卡语义） | 否 |

**数据矩阵**：见 §三；**方案**：企业维度确定性计数（无建模假设）；**风险**：无（org 直连，无代理误配）；**总判**：完全转换支持。

## 附录 D 实测脚本与结果摘要

- `metrics/repro/M_ENT_UI_RISK_TAX.py`（退出码 0）→ `metrics/repro/out/M_ENT_UI_RISK_TAX_out.json`：facts（源表行数/org 覆盖/Top10）+ support_judgment + base_years_used（截面件 []）。
