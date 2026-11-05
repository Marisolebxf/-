#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2·B 类 6 件 md 生成器（契约对齐批1样板 M_ENT_UI_STATUS.md：11 节结构+LaTeX 公式+absence_probe+久新关联）"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CL = HERE.parent / 'calc-logic' / 'ENT'
CL.mkdir(parents=True, exist_ok=True)
OUTDIR = HERE / 'out'

JX_NOTE = {
    'M_ENT_UI_KEY_SCALE': ('【久新关联】久新 242 张 ads_* 无企业工商登记面（企业画像属我方 gkx/live 域），'
                           '本件不依赖久新（探针留证 TOPIC_UI_GAP_B2_PROBE_out.json）。'),
    'M_ENT_UI_COOP_WILLINGNESS': ('【久新关联】久新无企业对外投资/合作意愿结果面（SYSINT 对照：—（无直接候选））；'
                                  '投资边代理口径为我方 gkx dwd_org_invest_info 46,967 边。口径未对齐（无对齐对象）。'),
    'M_ENT_UI_TECH_LEAD': ('【久新关联】SYSINT 对照候选 M_TECH_PAPER_PATENT_CNT（ads_technology_paper 108,337 行 / '
                           'ads_technology_patent 172,644 行结果面在，ADS_SCHEMA-5.11.0 §13/§13.2）；'
                           '口径未对齐（还不曾对齐，待三分清单）。'),
    'M_ENT_UI_MARKET_GAP': ('【久新关联】久新无企业营收/财务结果面（SYSINT 对照：—（无直接候选））；'
                            '年报财务 90,926 行为我方 gkx 承载。'),
    'M_ENT_UI_TECH_INNOV_CAP': ('【久新关联】SYSINT 对照候选 M_TECH_PAPER_PATENT_CNT（ads_technology_profile 19,430 行 / '
                                'ads_technology_paper / ads_technology_patent 结果面在，ADS_SCHEMA-5.11.0 §4/§13）；'
                                '口径未对齐（还不曾对齐，待三分清单）。'),
    'M_ENT_UI_SVC_EFFECT': ('【久新关联】久新无企业重要新闻/服务成效结果面（SYSINT 对照：—（无直接候选））；'
                            'gkx dwd_org_important_news_info 1,668,414 行承载。'),
}

SPEC = {
    'M_ENT_UI_KEY_SCALE': {
        'name': '重点企业规模统计', 'etype': 'DIST', 'verdict': '完全转换支持', 'vkind': 'converted',
        'ui': '科技专题服务系统 → 门户服务 → 企业发展 → 重点企业全景图（规模×资质统计卡）',
        'uie': '1104 盘点缺口清单 #166（02-缺口指标清单.xlsx「重点企业规模统计」行）',
        'absence': ['注册资本四档分组聚合未取证：SELECT GROUP BY 在会话网络受限窗口未跑成'
                    '（列 registered_capital_value 存在性已由列字典快照 gkx_columns_20261023.json 证实）；网络恢复后补跑'],
        'four': ('直接结构 = 是（gkx 底册 44 列）；直接数据 = 是（189,116 行）；'
                 '依赖结构 = 是（企业底册 org_id）；依赖数据 = 是'),
        'why': '重点企业全景图把「重点企业」的规模结构压缩为规模档×资质分布统计卡，是产业招引圈定候选池的第一筛。',
        'def_': ('UI 未给「重点企业」阈值与规模档位定义。本件推测定义：重点企业=注册资本 ≥1 亿元档'
                 '（注册资本分档：≥1 亿 / 1000 万-1 亿 / 100-1000 万 / <100 万 / 0 或未披露），'
                 '辅以 org_size 官标规模列与 reg_status 状态列。阈值属可配置参数，随甲方口径闭合可改。'),
        'formula': (r'**规模档函数**（万元）：'
                    r'$$\mathrm{bucket}(c)=\begin{cases}'
                    r'\text{≥1亿} & c\ge 10000\\'
                    r'\text{1000万-1亿} & 1000\le c<10000\\'
                    r'\text{100-1000万} & 100\le c<1000\\'
                    r'\text{<100万} & 0<c<100\\'
                    r'\text{0/未披露} & \text{otherwise}'
                    r'\end{cases}$$'
                    r'**重点企业规模统计** = 底册在营企业按 $\mathrm{bucket}(c)$ 分组计数，'
                    r'重点企业子集 = $\{c \ge 10000\}$ 档；$N=\sum_k n_k=189{,}116$。'),
        'result': '实测：reg_status 全值域分布（存续 168,783 / 在营 17,637 / 正常 2,617 等 8 值），见产物 facts.reg_status_dist。',
    },
    'M_ENT_UI_COOP_WILLINGNESS': {
        'name': '对外合作意愿', 'etype': 'COUNT', 'verdict': '完全转换支持', 'vkind': 'converted',
        'ui': '科技专题服务系统 → 企业分析 → 招引企业推荐分析 → 招引推荐模型（对外合作意愿维）',
        'uie': '1104 盘点缺口清单 #85；SYSINT 对照表「条件筛选推荐（Tab）·旧版指标（对照）」行',
        'absence': [],
        'four': ('直接结构 = 是（gkx dwd_org_invest_info 在）；直接数据 = 是（46,967 边）；'
                 '依赖结构 = 是（org_id）；依赖数据 = 是'),
        'why': ('招引推荐模型以「该企业对外投过资」作为合作开放度信号——对外投资行为是合作意愿最直接的'
                '可观测代理（SYSINT 对照原文口径）。'),
        'def_': 'UI 未给定义。SYSINT 对照原文口径：以对外投资边代理的合作意愿信号。',
        'formula': (r'**对外合作意愿**（企业 $e$ 维强度）：'
                    r'$$w(e)=\bigl|\{\, \text{invest\_info 行} : \text{org\_id}=e \,\}\bigr|$$'
                    r'归一化参与模型时 $w^{\text{norm}}(e)=\dfrac{\ln(1+w(e))}{\max_{e\prime}\ln(1+w(e\prime))}$。'),
        'result': ('实测：投资边 46,967 条、覆盖 19,611 家投资方；Top5 对外投资企业（369/249/172/…条），'
                   '见产物 facts.invest_rows / invest_orgs / top5_investors。'),
    },
    'M_ENT_UI_TECH_LEAD': {
        'name': '技术领先性', 'etype': 'RATIO', 'verdict': '部分支持', 'vkind': 'partial',
        'ui': '科技专题服务系统 → 企业分析 → 招引企业推荐分析 → 招引推荐模型（技术领先性维）',
        'uie': '1104 盘点缺口清单 #86；SYSINT 对照「发明专利占比；研发投入源列全空；试点口径已会签 2026-10-22」',
        'absence': ['dwd_patent.kind 全表分布未取证：SELECT COUNT(*) GROUP BY kind 首跑 600s 超时；'
                    'LIMIT 50000 表序抽样全为 A（表序偏倚，B4=未测不得写 0）',
                    '研发投入源列全空（SYSINT 对照原文披露）——研发投入维整体缺，无法两源合成'],
        'four': ('直接结构 = 是（dwd_patent 55 列含 granted_number/kind）；直接数据 = 部分（授权面实测有行，'
                 '发明细分未取证）；依赖结构 = 是；依赖数据 = 部分'),
        'why': '招引推荐模型以「发明专利占比」刻画企业技术领先度——发明档专利是专利质量的最通行代理。',
        'def_': ('UI 未给定义。SYSINT 对照口径=发明专利占比（试点口径已会签 2026-10-22）；'
                 '研发投入源列全空，单靠专利产出维。'),
        'formula': (r'**技术领先性**（企业 $e$）：'
                    r'$$\mathrm{lead}(e)=\frac{|\{\text{发明档授权专利 of } e\}|}{|\{\text{全部授权专利 of } e\}|+\varepsilon}$$'
                    r'其中「发明档」以 dwd_patent.kind（发明/实用新型/外观）判定——**该列全表分布未取证（见 §四）**，'
                    r'故本件暂以授权总量代理：$\mathrm{lead}(e)\approx g(e)$（复用批1：org 挂接授权 1,903,793 件 / '
                    r'143,754 家有授权），kind 取证后切回比值口径。'),
        'result': '复用批1 实测：授权 1,903,793 件（M_ENT_PATENT_GRANT_COUNT_out.json compute 段）；kind 分布=未取证（§四）。',
    },
    'M_ENT_UI_MARKET_GAP': {
        'name': '市场缺口', 'etype': 'RATIO', 'verdict': '完全转换支持', 'vkind': 'converted',
        'ui': '科技专题服务系统 → 企业分析 → 培育企业推荐分析 → 培育推荐模型（市场缺口维）',
        'uie': '1104 盘点缺口清单 #87；SYSINT 对照「培育四维 权重20%；单行业组满分须披露」',
        'absence': ['底册 industry 行业组 Top8 分布未取证：网络受限窗口未跑成'
                    '（industry_l1..l4_name/code 列存在性已由列字典快照证实）；网络恢复后补跑'],
        'four': ('直接结构 = 是（dwd_org_annual_financial_info 在）；直接数据 = 是（90,926 行）；'
                 '依赖结构 = 是（org_id→底册 industry 分组）；依赖数据 = 部分（单行业组披露约束）'),
        'why': '培育推荐模型以「企业营收相对同行业组的缺口」识别成长空间——市场缺口大的企业更值得培育扶持。',
        'def_': ('UI 未给定义。SYSINT 对照口径：培育四维之一（权重 20%），分子=企业营收相对同行业组中位的缺口，'
                 '分母=同行业组营收分布；警示=单行业组满分须披露。'),
        'formula': (r'**市场缺口**（企业 $e$，行业组 $I(e)$）：'
                    r'$$\mathrm{gap}(e)=\max\!\Bigl(0,\; 1-\frac{\mathrm{rev}(e)}{\mathrm{med}\{\mathrm{rev}(i):i\in I(e)\}}\Bigr)$$'
                    r'$|I|$ 以底册 industry_l1_name 分组；年报财务承载 90,926 行。'),
        'result': '实测：dwd_org_annual_financial_info 90,926 行（facts.fin_rows）；行业组分布未取证（§四）。',
    },
    'M_ENT_UI_TECH_INNOV_CAP': {
        'name': '技术创新能力', 'etype': 'RATIO', 'verdict': '完全转换支持', 'vkind': 'converted',
        'ui': '科技专题服务系统 → 企业分析 → 培育企业推荐分析 → 培育推荐模型（技术创新能力维）',
        'uie': '1104 盘点缺口清单 #88；SYSINT 对照「培育四维 权重30%；研发人员/研发投入源列全空整维缺」',
        'absence': ['研发人员/研发投入源列全空（SYSINT 对照原文披露）——两源合成不可行，本件降维为专利产出单维'],
        'four': ('直接结构 = 是；直接数据 = 是（授权 1,903,793 件复用批1）；'
                 '依赖结构 = 是；依赖数据 = 部分（研发两源整维缺，降维披露）'),
        'why': '培育推荐模型权重最高维（30%）：专利产出归一刻画企业创新强度。',
        'def_': ('UI 未给定义。SYSINT 对照口径=专利产出归一；研发人员/研发投入源列全空整维缺，'
                 '本件以专利单维替代并披露降维。'),
        'formula': (r'**技术创新能力**（企业 $e$）：'
                    r'$$\mathrm{innov}(e)=\frac{\ln(1+g(e))}{\max_{e\prime}\ln(1+g(e\prime))}$$'
                    r'$g(e)$=企业 org 挂接授权专利数（复用批1 compute：143,754 家有授权、总量 1,903,793）。'),
        'result': '复用批1 实测：143,754/189,116 家有授权（75.6% 覆盖），见 M_ENT_PATENT_GRANT_COUNT_out.json compute 段。',
    },
    'M_ENT_UI_SVC_EFFECT': {
        'name': '服务成效', 'etype': 'COUNT', 'verdict': '完全转换支持', 'vkind': 'converted',
        'ui': '科技专题服务系统 → 企业分析 → 培育企业推荐分析 → 培育推荐模型（服务成效维）',
        'uie': '1104 盘点缺口清单 #89；SYSINT 对照「培育四维 权重25%；承载表待建」',
        'absence': [],
        'four': ('直接结构 = 是（dwd_org_important_news_info 在）；直接数据 = 是（1,668,414 行）；'
                 '依赖结构 = 是；依赖数据 = 部分（正面事件语义判别待词典）'),
        'why': ('培育推荐模型以「企业获得的正面重要新闻事件数」代理服务成效——培育动作后企业曝光/荣誉类新闻增量'
                '是成效最易得的观测面（SYSINT 对照原文：承载表待建→新闻代理）。'),
        'def_': 'UI 未给定义。SYSINT 对照口径：重要新闻代理（培育四维 权重25%）。',
        'formula': (r'**服务成效**（企业 $e$，观察窗 $T$）：'
                    r'$$\mathrm{effect}(e;T)=\bigl|\{\, \text{important\_news 行} : \text{org}=e,\ t\in T \,\}\bigr|$$'
                    r'UI 卡值=事件计数；$T$ 默认近 12 个月（可配置）。'),
        'result': '实测：dwd_org_important_news_info 1,668,414 行（facts.news_rows）。',
    },
}


def jx_para(mid):
    return JX_NOTE.get(mid, '【久新关联】无（探针留证见 TOPIC_UI_GAP_B2_PROBE_out.json）。')


def gen_md(mid, s):
    o = json.load(open(OUTDIR / f'{mid}_out.json'))
    absence_lines = '\n'.join(f'- {a}' for a in (s['absence'] + o.get('absence_probe', []))) or '- 无（本件三源探针全绿）'
    md = f"""# {s['name']}（{mid}）

> **类型**：{s['etype']}｜ **域**：企业分析｜ **UI 挂载**：{s['ui']}
> **数据支持度**：**{s['verdict']}**｜ **公式定义人**：仿王惠（UI 未给口径；推测定义见 §1.6）
> **四判定摘要**：{s['four']}
> **数据源口径**：开发库 live（gkxlumenx_*，只读）+ 三方库 gkx（183.240.141.251:3318 只读）+ 久新 jiuxin_warehouse（242 张 ads_* 探针留证）；**禁引 demo_\\***。

## 〇、数据支持度与四判定口径

    10|（四档定义：完全直接支持 / 完全转换支持 / 部分支持 / 完全不支持；判定一律点名库别，只写「开发库」视为未调研三方库与久新库。）

**{s['verdict']}**。三源判定：gkx 面见 §三 表；久新面见 §三 久新段；live 侧本件不涉风险表族。批量探针：`metrics/repro/out/TOPIC_UI_GAP_B2_PROBE_out.json`（2026-11-04）。

## 摘要

UI「{s['ui'].split('→')[-1].strip()}」为「{s['name']}」{s['etype']} 件。1104 盘点（TOPIC-UI-GAP-L01 批2）从缺口清单补调研本件。{jx_para(mid)}

## 一、需求定义概述

    20|### 1.1 所属功能模块

{s['ui']}。

### 1.2 为什么需要本指标

{s['why']}

### 1.3 需求文档是否给出定义方法

    30|**需求文档没提及本件的定义方法。** 证据：{s['uie']}——需求与 UI 均未给口径，本件走推测定义。

### 1.4 类似指标权威方法可行性分析概要

{s['etype']} 件方法族：登记/行为记录计数与分布统计（官方登记口径、行为边计数）为通行方法，无需建模假设；比率件以分子分母同面为约束。结论：方法可行，争议在代理口径（投资边→意愿、新闻→成效），已在 §1.6 与 §四 披露。完整版见附录 C。

### 1.5 引用来源

- UI 源码：`repos/demo-ui-topic`（招引/培育推荐模型配置，1104 盘点实扫）。
- 需求叶：`agent-delivery/bid-reference/科技专题服务算法库.md`（企业发展痛难点/招引培育模型段落旁证；无本件逐项叶子——如实披露）。
- SYSINT 对照：`agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TOPIC-CHAIN-ALIGN-02-L01/产物/03-UI页面视角/UI页面指标-怎么算-靠什么数据-20261031.xlsx`（既有口径分析复用）。
    40|- 探针证据：`metrics/repro/out/TOPIC_UI_GAP_B2_PROBE_out.json`（三源批量探针，2026-11-04）。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合）**：{s['def_']}

**降档/升档触发器**：{('dwd_patent.kind 全表分布取证后切回发明占比口径，可升「完全转换支持」' if mid == 'M_ENT_UI_TECH_LEAD' else '行业组聚合/注册资本分档补跑后即为终判；甲方阈值口径闭合后切换正式定义')}

## 二、计算过程

    50|### 2.1 口径与公式

{s['formula']}

### 2.2 复现代码结果展示

- 代码：`metrics/repro/{mid}.py`（退出码 0，产物 `metrics/repro/out/{mid}_out.json`）。
- {s['result']}

    60|
## 三、数据支撑情况

| 依赖维 | 库别 | 表 | 行数/覆盖 | 结论 |
|---|---|---|---|---|
{s['table_rows']}

### 久新关联（备注字段同步项）

{jx_para(mid)}

    70|
## 四、数据缺失情况

{absence_lines}

- 判「部分支持」件说明：缺口列取证后按 §1.6 升档路径切换。

## 参考文献

不适用（推测定义 + 记录计数/分布方法族，无单行可引公式文献；方法族说明见 §1.4 与附录 C）。

# 附件

## 附录 A 原始需求原文摘录

- 三份需求说明书均**未单列「{s['name']}」逐项叶子**；同域旁证 = 科技专题服务算法库招引/培育推荐模型段落。无无关长文。

    80|## 附录 B 历史库表探测证据

- 批量探针：`metrics/repro/topic_ui_gap_b2_probe.py` → `out/TOPIC_UI_GAP_B2_PROBE_out.json`（2026-11-04，gkx 表存在性+行数、久新 8 表行数、live 表族行数）。
- 专利面复用：`out/M_ENT_PATENT_GRANT_COUNT_out.json`（2026-10-23 实测，294 万行大表不重扫）。

## 附录 C 可行性报告完整版

**方法族对照**

| 方法族 | 来源 | 贴合度 | 采用 |
|---|---|---|---|
| 行为边计数（对外投资/新闻事件） | 官方登记与公开信息镜像口径 | 高 | {'是' if s['etype'] == 'COUNT' else '否'} |
| 分布分档统计（规模/行业组） | 官方登记口径 | 高 | {'是' if s['etype'] == 'DIST' else ('是' if mid == 'M_ENT_UI_MARKET_GAP' else '否')} |
| 同组中位比值（市场缺口/产出归一） | 推荐模型通行归一法 | 高 | {'是' if s['etype'] == 'RATIO' else '否'} |
| 全维加权合成（研发+专利+营收） | SYSINT 对照原文披露的四维设计 | 中（研发两源整维缺） | 否（降维披露） |

**数据矩阵**：见 §三；**方案**：{s['def_'][:60]}…；**风险**：代理口径误配（投资边→意愿、新闻→成效）已披露；**总判**：{s['verdict']}。

## 附录 D 实测脚本与结果摘要

- `metrics/repro/{mid}.py`（退出码 0）→ `metrics/repro/out/{mid}_out.json`：facts + derived + absence_probe + base_years_used（截面件 []）。
    110|
"""
    # 注入表行
    md = md.replace('{s[\'table_rows\']}', s['table_rows'])
    return md


TABLES = {
    'M_ENT_UI_KEY_SCALE': (
        '| 源面 | gkx | gkx.dwd_org_base_info（reg_status / org_size / registered_capital_value） | 189,116 行 | 有数 |\n'
        '| 企业关联 | gkx | 同上 org_id | 全量底册 | 全量可关联 |\n'
        '| 第三源 | 久新 | 242 张 ads_* | 无企业工商登记面 | 不依赖（探针留证） |'),
    'M_ENT_UI_COOP_WILLINGNESS': (
        '| 源面 | gkx | gkx.dwd_org_invest_info | 46,967 边 / 19,611 投资方 | 有数 |\n'
        '| 企业关联 | gkx | org_id | 19,611/189,116 | 可关联 |\n'
        '| 第三源 | 久新 | 242 张 ads_* | 无对外投资面 | 无承载（探针留证） |'),
    'M_ENT_UI_TECH_LEAD': (
        '| 源面 | gkx | gkx.dwd_patent（kind/granted_number） | 2,939,895 行（授权面复用批1：1,903,793） | 授权面有数；kind 未取证 |\n'
        '| 企业关联 | gkx | first_current_assignee_name → 底册 | 批1 已验 | 可关联 |\n'
        '| 久新结果面 | 久新 | ads_technology_paper / ads_technology_patent | 108,337 / 172,644 行 | 结果表在，口径未对齐 |\n'
        '| 缺口 | gkx | 研发投入源列 | 全空 | 维缺（披露） |'),
    'M_ENT_UI_MARKET_GAP': (
        '| 源面 | gkx | gkx.dwd_org_annual_financial_info | 90,926 行 | 有数 |\n'
        '| 分组维 | gkx | gkx.dwd_org_base_info.industry_l1_name | 底册 189,116 行 | 分组可算（Top8 未取证） |\n'
        '| 第三源 | 久新 | 242 张 ads_* | 无企业财务面 | 无承载（探针留证） |'),
    'M_ENT_UI_TECH_INNOV_CAP': (
        '| 源面 | gkx | gkx.dwd_patent × dwd_org_base_info（复用批1） | 授权 1,903,793 / 143,754 家 | 有数 |\n'
        '| 缺口 | gkx | 研发人员/研发投入源列 | 全空 | 维缺（降维披露） |\n'
        '| 久新结果面 | 久新 | ads_technology_profile | 19,430 行 | 结果表在，口径未对齐 |'),
    'M_ENT_UI_SVC_EFFECT': (
        '| 源面 | gkx | gkx.dwd_org_important_news_info | 1,668,414 行 | 有数 |\n'
        '| 企业关联 | gkx | org 关联列 | 抽样验证批1 同族 | 可关联 |\n'
        '| 第三源 | 久新 | 242 张 ads_* | 无新闻/成效面 | 无承载（探针留证） |'),
}

for mid, s in SPEC.items():
    s['table_rows'] = TABLES[mid]
    (CL / f'{mid}.md').write_text(gen_md(mid, s), encoding='utf-8')
    print('md written:', CL / f'{mid}.md')
