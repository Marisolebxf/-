# 股权出质数（M_ENT_UI_RISK_EQUITY_PLEDGE）

> **类型**：COUNT｜ **域**：企业分析／企业查询／企业画像｜ **UI 挂载**：科技专题服务系统 → 企业分析 → 企业查询 → 企业画像抽屉（风险信息 tab 计数卡）
> **数据支持度**：**完全不支持**｜ **公式定义人**：仿王惠（UI 未给口径；推测定义=企业维度确定性计数）
> **四判定摘要**：直接结构 = 无（三源无承载表）；直接数据 = 无；依赖结构 = 是（企业底册 org_id）；依赖数据 = 无
> **数据源口径**：开发库 live（gkxlumenx_*，仅风险表族 0 行披露）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin_warehouse（242 张 ads_* 探针留证）；**禁引 demo_\***。

## 〇、数据支持度与四判定口径

（四档定义：完全直接支持 / 完全转换支持 / 部分支持 / 完全不支持；判定一律点名库别，只写「开发库」视为未调研三方库与久新库。）

**完全不支持**。三源探针：① gkx 280 张全表名扫描（auction/paimai/拍卖、freeze/dongjie/冻结、pledge/chuzhi/出质、mortgage/diya/抵押 关键词）零命中；② 久新 242 张 ads_* 风险类 7 张均为技术/人才/机构要素面；③ live gkxlumenx_dwd 对应 risk_* 表（risk_judicial_sale / risk_equity_freeze / risk_equity_pledge / risk_chattel_mortgage）**表存在但 0 行**（B4 四分法：②表存在 0 行 ≠ 无表 ≠ 无数据；修复动作 = 向 live 表族补数据同步，结构已就绪）。absence_probe 三件套（查了什么/条件/命中几行）落 `metrics/repro/out/M_ENT_UI_RISK_BATCH_PROBE_out.json`。

## 摘要

UI「企业画像抽屉·风险信息」展示「股权出质数」计数卡（enterpriseSearchConfig.ts `detailTabs` risk/overview tab，`dataSource: 待源（司法/失信，Q020）`）。需求文档未给该卡定义方法，本件走推测定义（企业维度确定性计数）。批1（TOPIC-UI-GAP-L01）: 18 风险计数 + 经营范围/经营状态。本件判档：**完全不支持**——三源均无承载，absence_probe 三件套留证。

## 一、需求定义概述

### 1.1 所属功能模块

科技专题服务系统 → 企业分析 → 企业查询 → 企业画像抽屉 → 风险信息（tab9）。

### 1.2 为什么需要本指标

企业画像风险面把一家企业的司法/执行/处罚/经营暴露压缩为单值计数卡，是尽调、招引前筛查与培育评估的风险眼。live risk_equity_pledge 结构在 0 行；gkx 无登记类出质明细.

### 1.3 需求文档是否给出定义方法

**需求文档没提及本卡的定义方法。** UI 配置源码即证据：`repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103` `{ key: 'risk', label: '风险信息', pending: true, dataSource: '待源（司法/失信，Q020）' }`——前端明示待源、无口径。

### 1.4 类似指标权威方法可行性分析概要

风险计数卡属企业信用/司法风险登记计数，国内权威口径体系（国家企业信用信息公示系统登记事项、司法公开四平台：中国裁判文书网/中国执行信息公开网/人民法院公告网/全国法院破产审判网）即「登记记录计数」方法族，无需建模假设；数据面为登记/公开记录镜像计数。结论：方法可行，争议仅在**关联口径**（企业主体 vs 法定代表人/历史移出记录），已在 §二 与 §四 披露。完整版见附录 C。

### 1.5 引用来源

- UI 源码：`repos/demo-ui-topic/src/app/components/search/configs/enterpriseSearchConfig.ts:103`（risk tab 定义）。
- 需求叶：`agent-delivery/bid-reference/科技专题服务算法库.md` §1.1.1.1.1.1.1.5.3–5.4（企业发展痛难点/供应链关系模型，风险维旁证；**无本卡逐项叶子**——如实披露「三份需求说明书均未单列本卡」）。
- 探针证据：`metrics/repro/out/M_ENT_UI_RISK_BATCH_PROBE_out.json`（三源批量探针，2026-11-04）。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合）**：从缺

**降档/升档触发器**：任一源（live 表族灌数 / gkx 新表）出现可关联承载即重判。

## 二、计算过程

### 2.1 计算过程

**从缺**（三源均无承载，见 §四 与 absence_probe；禁止伪公式）。

### 2.3 absence_probe（负证据三件套）

- 查了什么：gkx SHOW TABLES 280 张全表名 + 久新 SHOW TABLES 242 张 ads_* + live gkxlumenx_dwd risk_* 表族。
- 条件：拍卖/冻结/出质/抵押 关键词（英/拼/中）+ 风险类语义。
- 命中几行：gkx 零命中；久新 7 张均为技术/人才/机构面；live 对应表 0 行（risk_type_dict 18 行字典除外）。

## 三、数据支撑情况

| 依赖维 | 库别 | 表 | 行数/覆盖 | 结论 |
|---|---|---|---|---|
| 源面 | gkx | （三源均无承载表） | — | 无承载 |
| 企业关联 | — | — | — | 无 |
| 兜底面 | live | gkxlumenx_dwd risk_* 表族 | 结构齐全、**0 行** | 待补数据同步（不作结果面） |
| 第三源 | 久新 | 242 张 ads_* | 风险类 7 张均非本卡语义 | 无承载（探针留证） |

久新 gkx_technology_analysis_dev 242 张 ads_* 风险类命中 7 张（ads_research_outcome_trend_case 22,881 / ads_technology_application_case 181,735 等），均为技术/人才/机构要素面，**无司法/执行/处罚风险结果面**——三源探针留证（out/M_ENT_UI_RISK_BATCH_PROBE_out.json）。

## 四、数据缺失情况

- live risk_equity_pledge 结构在 0 行；gkx 无登记类出质明细.
- live gkxlumenx_dwd risk_* 表族（18 张+字典）结构齐全但 0 行——若按「先灌数后直查」路径走，本卡族可整体升档；该灌数属共享库写入，须用户授权另单执行。
- 判完全不支持件：三源均无承载，若甲方坚持该卡出数，需接入外部登记源（国家企业信用信息公示系统/司法公开四平台镜像），另立数据接入单。

## 参考文献

不适用（推测定义 + 登记计数方法族，无单行可引公式文献；方法族说明见 §1.4 与附录 C）。

# 附件

## 附录 A 原始需求原文摘录

- 三份需求说明书（`agent-delivery/bid-reference/科技专题服务算法库.md`、`科技信息展示系统和科技专题服务系统.md`、`科技信息展示系统(政策对比功能升级)核增需求.md`）均**未单列「股权出质数」逐项叶子**；同域旁证段落 = 科技专题服务算法库 §1.1.1.1.1.1.1.5.3–5.4（痛难点识别「风险防控」/供应链关系模型）。无无关长文。

## 附录 B 历史库表探测证据

- 批量探针：`metrics/repro/M_ENT_UI_RISK_BATCH_PROBE.py` → `out/M_ENT_UI_RISK_BATCH_PROBE_out.json`（2026-11-04，三源）。
- live 表族行数补探：`metrics/repro/out/_live_risk_tables_probe.json`（18 表+enterprise_bid 全 0 行实证）。

## 附录 C 可行性报告完整版

**方法族对照**

| 方法族 | 来源 | 贴合度 | 采用 |
|---|---|---|---|
| 登记记录计数 | 国家企业信用信息公示系统登记事项口径 | 高（中国官方口径） | 是 |
| 司法公开四平台记录镜像计数 | 裁判文书网/执行信息公开网/公告网/破产审判网 | 高 | 是（有表件） |
| 信用评分模型 | 境外商业征信（D&B 等） | 低（超出 UI 卡语义） | 否 |

**数据矩阵**：见 §三；**方案**：企业维度确定性计数（无建模假设）；**风险**：关联代理件的误配（taxpayer_name/respondent_info/公告标题包含匹配），已披露；**总判**：完全不支持。

## 附录 D 实测脚本与结果摘要

- `metrics/repro/M_ENT_UI_RISK_EQUITY_PLEDGE.py`（退出码 0）→ `metrics/repro/out/M_ENT_UI_RISK_EQUITY_PLEDGE_out.json`：facts（源表行数/关联覆盖/Top10/样例）+ support_judgment + absence_probe（ZERO 件）+ base_years_used（截面件 []）。
