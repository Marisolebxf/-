# 服务机构维度（SVC/E6）数据分析报告（v2 重写版）

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-SVC-ANALYSIS-L01 |
| 任务 ID | SVC-DATA-ANALYSIS-L01 |
| Epic | E-ALGO-LIB-DEMO |
| 版本 | **v2.2.0（实查修正）** — v2.1 按承诺文档修正，v2.2 按 ODS 库实查 DDL+数据修正（org_type 仅组织形式不可用、area 实为 district） |
| 状态 | Draft（待 architect-agent 会签 + 监管人 human:侯佳伟 审定） |
| 执行人 / 监管人 | human:侯佳伟 |
| 认领类型 | coordinator_dispatch · claimed_by=human:侯佳伟 |
| 创建日期 | 2026-08-05 |
| 仓 | agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`） |

> **v2.2 实查修正（最权威）**：监管人 human:侯佳伟 提供自有 ODS 库（`gkxlumenx_ods` @ 111.198.38.90:34306）连接，直接 `SHOW CREATE TABLE` + 字段值分布实查。实查推翻 v2.1 两处假设：
> 1. **org_type 不能用于服务机构准入**：org_type 非空率 100%（19993/20000），但内容是工商组织形式（"有限责任公司(自然人独资)""个人独资企业""事业单位""社会团体"等），**无任何服务机构语义关键词**（无"检测/知识产权/研发/技术转移"等），不能用来圈定服务机构池。v2.1 的 R1''（org_type 主准入）失效。
> 2. **area 字段不存在，实际是 district**：实查字段名是 `district`（区县 varchar(50)），不是 v2.1 写的 `area`。Q-SVC-004 仍可关闭（直字段可用），但字段名要正名为 district。
>
> **v2.1 修正原因**：监管人 human:侯佳伟 提供 `dwd_org_base_info` 实际建表 DDL，确认实际库**无 `industry` 字段**（承诺文档 xlsx 有但实际建表未落地），但实际有 `business_scope`（经营范围）和 `district`（区县直字段）。v2.0 误信承诺文档 xlsx 的 industry 字段，v2.1 按实际建表 DDL 修正：六类打标签主路径从 `industry` 改为 `business_scope`。
>
> **industry 字段来源说明**：v2.0 引用的 industry/industry_l1_name/industry_l1_code 等7个行业字段，来源是供应方承诺文档 `版权人才、企业机构、政策数据汇总表.xlsx`（国内机构要素库 Sheet，字段序号24-30）。但监管人提供的实际 `SHOW CREATE TABLE dwd_org_base_info` 结果显示：**实际建表无 industry 系列字段**，取而代之的是 `business_scope`（经营范围 text 字段）。承诺文档与实际建表存在偏差，需供应方核验（见 Q-SVC-009）。
>
> **v2 重写原因**：监管人 human:侯佳伟 指出，v1 报告基于的 `服务机构相关-ODS到DWD字段映射分析报告(v2).md` 使用了已作废的表名 `dwd_org_reg_info`。最新事实（GDF-ENT-WORKPACK-v1.2 命名词典 + Wave A 承诺表清单 + Mapping v3）：**国内机构主表是 `dwd_org_base_info`**，`dwd_org_reg_info` 已移出承诺表且 live 为 0 行空表。本 v2 基于 `dwd_org_base_info` 体系重新分析，**不照搬 v1**。

## 数据真源（v2 全部更新）

| 真源 | 路径 | 用途 |
|------|------|------|
| **命名词典 v1.2** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/01-命名与分层词典.md` | 表名归一（base_info vs reg_info） |
| **Wave A 承诺表清单** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml` | 40 张承诺表（含/不含判定） |
| **企业维 Mapping v3** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/09-企业维-ODS到DWD-Mapping说明-v3.md` | base_info 字段映射（SVC 复用） |
| **live 探测 08-04** | `data/third-party-source/gkx-mysql-raw/加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-04.md` | 实际行数 |
| **实际建表 DDL** | 监管人 human:侯佳伟 提供 `SHOW CREATE TABLE dwd_org_base_info`（2026-08-05） | **字段结构真源**（覆盖承诺文档 xlsx） |
| **ODS 库实查** | `gkxlumenx_ods.dwd_org_base_info` @ 111.198.38.90:34306（2026-08-05 human:侯佳伟 授权直连） | **字段值分布+非空率真源**（org_type/business_scope/district 实查） |
| **国内机构库分析** | `data/data-design/产业链/国内机构库-ODS到DWD字段映射分析报告.md` | reg_info=0 行确认 |
| bid §4.1.1.1.1.1.1.1.4 + §4.1.1.1.1.1.1.9 | `bid-reference/科技专题服务算法库.md` | 需规范围 |
| SVC-ALGO-DESIGN-L01 handoff | `agent-handoffs/算法库联调-ALGO-LIB/SVC-ALGO-DESIGN-L01.md` | 算法依赖交叉 |

---

## 目录

1. [DWD 表设计方案（基于 base_info 重做）](#1-dwd-表设计方案基于-base_info-重做)
2. [服务机构指标（重对齐）](#2-服务机构指标重对齐)
3. [第三方数据缺口（重矩阵）](#3-第三方数据缺口重矩阵)
4. [问题或待决策项（重登记）](#4-问题或待决策项重登记)
5. [架构合规自检](#5-架构合规自检)
6. [依赖与风险](#6-依赖与风险)
7. [附录：v1→v2 变更对照](#7-附录v1v2-变更对照)

---

## 1. DWD 表设计方案（基于 base_info 重做）

### 1.1 关键事实修正（v1 vs v2.2 实查）

| 项 | v1（作废） | v2.2（实查本版） | 依据 |
|----|-----------|-----------|------|
| 主表名 | `dwd_org_reg_info` | **`dwd_org_base_info`** | 命名词典 §2 + Wave A 清单 line 56 |
| 主表 live 行数 | 未探测（假设有） | **20,000**（reg_info=0 行空表） | LIVE-08-04 + ODS 实查 COUNT(*) |
| tag_info | 准入辅助 R3 来源 | **不在承诺40表** | Wave A 清单 removed_vs_v1_1 line 128 |
| financing_info | M_SVC_INVEST_Y 来源 | **不在承诺40表**（旁路949行） | Wave A 清单 removed line 129 |
| invest_info | M_SVC_INVEST_Y 来源 | **不在承诺40表** | Wave A 清单 removed line 130 |
| Mapping 真源 | Mapping v2（作废） | **Mapping v3** | 09-企业维 v3 §0 明确作废 v2 |
| **industry 字段** | — | **❌ 实际不存在** | ODS 实查 SHOW CREATE TABLE |
| **org_type 字段** | 准入辅助 | **❌ 仅工商组织形式，无服务机构语义** | ODS 实查值分布（TOP值全为"有限责任公司"等） |
| **district 字段** | address 解析 | **✅ 直字段（varchar(50) 区县）** | ODS 实查（v2.1 误记为 area，v2.2 正名为 district） |
| **六类打标签来源** | product_info（空）→ 退化 org_type+tag | **仅 business_scope（自由文本，质量参差）** | v2.0 误信 industry；v2.1 误用 org_type；v2.2 实查后仅剩 business_scope |

### 1.2 DWD 表清单（承接 v1 结构，来源更新）

| # | DWD 表 | 字段数 | 角色 | 承诺 ODS 主源 | live 行数 |
|---|--------|--------|------|--------------|-----------|
| 1 | `gkx_dwd.service_org` | 38 | 服务机构主表 | `dwd_org_base_info` + `dwd_org_org_product_info` | 20,000 / 0(空) |
| 2 | `gkx_dwd.service_org_financing` | 16 | 服务链投融资明细 | **无承诺表**（financing_info/invest_info 均移出） | — |

> **v1 结构（service_org 38字段 / service_org_financing 16字段）可承接**，但字段映射全部要按 base_info 重做（见 §1.3）。

### 1.3 字段映射重做（service_org 主表，基于 Mapping v3 §2）

| # | DWD 字段 | v2 映射 | 承诺 ODS | 状态 | v1 偏差说明 |
|---|----------|---------|----------|------|-------------|
| 1 | id | 🟦 自增 | — | ✅ | — |
| 2 | service_org_code | ✅ org_id | base_info.org_id | ✅ | v1 用 reg_info.external_id（表名错+字段不存在）；v2.2 实查无 external_id，改用 org_id |
| 3 | org_id | ✅ org_id | base_info.org_id | ✅ | v1 用 reg_info.org_id |
| 4 | enterprise_code | ✅ social_credit_code | base_info.social_credit_code | ✅ | v2.2 实查无 external_id，企业标识改用统一社会信用代码 |
| 5 | name_cn | ✅ name_cn | base_info.name_cn | ✅ | 同上 |
| 6 | **service_type** | 🔧 base_info.business_scope（经营范围）关键词打标签 | base_info | 🔧 | **v1 依赖 product_info（空）；v2.0 误用 industry（实际无）；v2.1 用 org_type（实查仅组织形式不可用）；v2.2 仅剩 business_scope** |
| 7 | service_type_source | 🔧 命中来源 | — | 🔧 | — |
| 8 | service_type_tags | 🔧 JSON 数组 | — | 🔧 | — |
| 9 | org_type | ✅ org_type | base_info.org_type | ⚠️ | **v2.2 实查：非空率100%但内容仅工商组织形式（有限责任公司/个人独资企业等），无服务机构语义，仅作信息字段保留，不用于准入判断** |
| 10 | province | ✅ province | base_info.province | ✅ | — |
| 11 | city | ✅ city | base_info.city | ✅ | — |
| 12 | district | ✅ **district** | base_info.district | ✅ | **v1 用 address 解析；v2.1 误记为 area；v2.2 实查正名为 district（varchar(50) 区县直字段）** |
| 13 | address | ✅ address | base_info.address | ✅ | — |
| 14 | addr_lng | 🔧 lng_lat 拆分 | base_info.lng_lat | 🔧 | **v2.2 实查：无 addr_lng/addr_lat 分字段，只有 lng_lat 合并字段，需拆分** |
| 15 | addr_lat | 🔧 lng_lat 拆分 | base_info.lng_lat | 🔧 | 同上 |
| 16 | incorporation_date | ✅ incorporation_date | base_info.incorporation_date | ✅ | — |
| 17 | incorporation_year | 🔧 incorporation_date 取年 | base_info.incorporation_date | 🔧 | **v2.2 实查：无 incorporation_year 直字段，需从 incorporation_date(varchar) 解析年份** |
| 18 | org_size | ❌ **无源** | — | ❌ | **v1 以为有；v2.2 实查确认 base_info 无 org_size** |
| 19 | registered_capital_value | ✅ registered_capital_value | base_info.registered_capital_value | ✅ | **v2.2 实查：字段已是 float 量纲-万，无需单位换算（v1/v2.0 误以为要换算）** |
| 20 | listing_status | ✅ listed_status | base_info.listed_status | ✅ | v2.2 实查字段名为 listed_status |
| 21 | industry_class | 🔧 business_scope 关键词推断 | base_info.business_scope | 🔧 | **v1 用 product_info.industry_class（空）；v2.0 误用 industry（实际无）；v2.1 改用 business_scope 关键词推断行业大类** |
| 22 | main_activities | ✅ main_activities | **product_info**（空） | ⚠️ | product_info 空时缺失；base_info 无此字段 |
| 23 | main_prod | ✅ main_prod | product_info（空） | ⚠️ | 同上 |
| 24 | service_tag_raw | ❌ **无源** | — | ❌ | **v1 用 tag_info.org_tag；tag_info 不在承诺表** |
| 25 | is_shenzhen | 🔧 city/province 规则 | base_info | 🔧 | — |
| 26 | financing_count | ❌ **无承诺源** | — | ❌ | **v1 用 financing_info COUNT；该表移出承诺** |
| 27 | invest_count | ❌ **无承诺源** | — | ❌ | **v1 用 invest_info COUNT；该表移出承诺** |
| 28 | latest_financing_amount | ❌ **无承诺源** | — | ❌ | 同上 |
| 29 | latest_financing_date | ❌ **无承诺源** | — | ❌ | 同上 |
| 30 | tech_score | 🔧算法 | M3 模型输出 | 🔧 | — |
| 31-38 | 其余系统/扩展列 | 🟦/✅ | — | ✅ | — |

### 1.4 service_org_financing 表（无承诺源）

`dwd_org_financing_info` 和 `dwd_org_invest_info` **均不在 Wave A 承诺40表**（Wave A 清单 removed_vs_v1_1 line 129-130）。live 探测 financing_info 旁路有 949 行，但非承诺表。

**处置**：
- service_org_financing 表结构保留，但当前**无承诺数据源**
- M_SVC_INVEST_Y 指标暂标 ❌ 无承诺源
- 若后续纳入 Wave B 或供应方确认旁路表可用，再激活

### 1.5 六类打标签路径修正（v2.2 实查定论）

> **⚠️ 本节为 v2.2 核心修正点。v2.0 误信承诺文档 industry 字段；v2.1 按建表 DDL 改用 business_scope+org_type 但未验证 org_type 内容；v2.2 经 ODS 库实查（字段值分布）推翻 v2.1 的 org_type 主准入假设。**

#### 1.5.1 industry 字段来源与实际差异（溯源说明）

| 项 | 内容 |
|----|------|
| **industry 字段的"来源依据"** | 供应方承诺文档 `版权人才、企业机构、政策数据汇总表.xlsx` →「国内机构要素库」Sheet，字段序号 24–30 列出了 industry / industry_l1_name / industry_l1_code 等 7 个行业分类字段。v2.0 报告据此认为 base_info 自带结构化行业码。 |
| **实际状况（建表 DDL）** | 监管人 human:侯佳伟 提供的 `SHOW CREATE TABLE dwd_org_base_info` 实际建表 DDL 中，**不存在 industry 系列任何字段**。承诺文档 xlsx 与实际建表存在偏差。 |
| **实际替代字段** | 实际建表有 `business_scope`（经营范围，text 类型），但**不是结构化行业分类码**，是企业自填的自由文本经营范围。 |
| **结论** | industry 字段在当前 live 库**不可用**（根本不存在）。承诺文档与实际建表的偏差需供应方核验（登记为 Q-SVC-009）。 |

#### 1.5.2 org_type 字段实查结论（v2.2 新增，推翻 v2.1 主准入假设）

v2.1 假设 org_type 可作"主准入"（含"服务/中介/代理/检测/知识产权"等关键词 → 圈定服务机构池）。**v2.2 实查 org_type 值分布后推翻此假设**：

| 实查维度 | 结果 |
|----------|------|
| 非空率 | 100%（19993/20000） |
| TOP 值（占绝对多数） | 「有限责任公司(自然人独资)」8145 行、「有限责任公司(自然人投资或控股)」4395 行、「有限责任公司」3366 行、「个人独资企业」1006 行 |
| 是否含服务机构语义 | **❌ 否**。全部值均为工商登记的**组织形式**分类（有限责任公司/有限合伙/分公司/基层工会/事业单位/社会团体/民办非企业单位等），**无任何"检测/知识产权/研发/技术转移/科技金融/综合科技服务"等六类服务机构关键词** |
| 结论 | org_type **不能用于服务机构准入判断**，更不能区分六类。v2.1 的 R1''（org_type 主准入）**作废**。org_type 仅作为信息字段保留在 service_org 表中。 |

#### 1.5.3 business_scope 实际内容质量评估（v2.2 实查）

ODS 库实查 business_scope：非空率 99.1%（19817/20000），内容为企业自填经营范围自由文本。质量问题：

| 质量维度 | 评估 | 影响 |
|----------|------|------|
| 结构化程度 | ❌ 自由文本，无行业码 | 无法直接码表匹配六类 |
| 表述口径一致性 | ❌ 参差不齐（有写产品销售、有写服务、有写很长一段含多个业务） | 关键词匹配召回率不稳定 |
| 与六类语义对齐度 | ❌ 多数记录与「研发/技术转移/检验检测/知识产权/科技金融/综合科技服务」六类无直接对应 | 需人工标定关键词词典，且准确率有限 |
| 非空率 | ✅ 99.1%（19817/20000） | 数据量充足，但质量不等于可用性 |

**抽样示例**（实查前 10 条非空）：
1. 「一般经营项目：非居住房地产租赁；物业管理；商业综合体管理服务；企业管理咨询；会议及展览服务…」
2. 「市场投资；市场经营管理；批发业、零售业…」
3. 「幻灯及投影设备销售;礼仪服务;保健食品销售;…企业总部管理」
4. 「销售：纸制品包装材料、电子制品、五金、塑胶制品」
5. 「软件开发；以自有资金从事投资活动；融资咨询服务；企业总部管理；企业管理；…」

**结论**：business_scope **不能作为六类精确分类的可靠主路径**，是当前唯一可用的文本信号，但准确率有上限。

#### 1.5.4 v2.2 打标签路径（实查定论后）

| 优先级 | 来源 | 字段 | 状态 | 角色 | 说明 |
|--------|------|------|------|------|------|
| ~~1~~ | ~~base_info~~ | ~~org_type~~ | ~~✅ 有数~~ | ~~主准入~~ | **❌ v2.2 作废**：实查内容仅工商组织形式，无服务机构语义 |
| 1 | base_info | business_scope | ⚠️ 自由文本、质量参差 | **唯一可用信号** | 关键词命中六类词典 → 标注候选分类（需人工复核，UI 带「待核验」角标） |
| 2 | product_info | main_activities | ❌ 空（连续空） | 待回灌 | product_info 回灌后与 business_scope 合并判别 |
| 3 | — | industry（结构化行业码） | ❌ **实际不存在** | **待供方补** | 见 Q-SVC-009，若供方补建 industry 字段则升级为主路径 |

**v2.2 打标签规则**（替代 v2.1 的 R1''/R2''/R3''/R4''）：
- ~~**R1''（org_type 主准入）**~~：**v2.2 作废**，org_type 实查仅工商组织形式，无服务机构语义
- **R1'''（唯一可用，⚠️ 待供方确认）**：`base_info.business_scope` 关键词命中六类词典 → 标注候选 service_type，**UI 须带「待核验」角标**，不作为权威分类。准确率有上限，需向甲方明示。
- **R2'''（待激活）**：`product_info.main_activities` 回灌后，与 business_scope 合并判别
- **R3'''（待供方补）**：若供方补建 industry 结构化字段（Q-SVC-009），则升级为主路径，替换 R1'''
- ~~R1'（base_info.industry 码表匹配）~~：**作废**，industry 字段实际不存在
- ~~R3（tag_info.org_tag）~~：**作废**，tag_info 不在承诺表
- ~~R5（invest_info 投资方 heuristic）~~：**作废**，invest_info 不在承诺表

**结论（v2.2，实查定论）**：
1. **服务机构准入本身无可靠主路径**：industry 不存在、org_type 仅组织形式、business_scope 是自由文本——当前 live 数据**既无法可靠圈定"哪些机构是服务机构"，更无法精确区分六类**。
2. 短期唯一可落地的是 **R1'''**（business_scope 关键词候选标注 + 人工复核），但这是"尽力而为"方案，准确率有上限，UI 须带「待核验」角标，评审时须向甲方明示数据局限。
3. **精确服务机构准入 + 六类分类依赖 Q-SVC-009 的供方答复**：若供方补建 industry 字段 → 主路径可用；若不补 → 长期只能靠 business_scope + 人工复核，需在评审时向甲方明示数据局限，并考虑是否调整功能范围（见 Q-SVC-010）。

---

## 2. 服务机构指标（重对齐）

### 2.1 M1 基础指标（bid §4.1.1.1.1.1.1.1.4，6项）

| # | bid 指标 | metric_id | v2 数据来源 | v1 偏差 | 状态 |
|---|----------|-----------|------------|---------|------|
| 1 | 全球服务机构产业布局 | M_SVC_INDUSTRY_LAYOUT | ⚠️ **base_info 无 industry；business_scope 自由文本质量不足** | v1 用 product_info（空）；v2.0 误用 industry；v2.1 实事求是 | ⚠️ **六类维度不可靠**（见 §1.5），待 Q-SVC-009 |
| 2 | 全球服务机构分布 | M_SVC_ORG_CNT | base_info.province/city | v1 用 reg_info | 🔧 可算（无 country，全球维度待补） |
| 3 | 投融资动态资讯 | M_SVC_INVEST_Y | **无承诺源** | v1 用 financing_info（移出承诺） | ❌ **无源** |
| 4 | 新增服务机构动态 | M_SVC_NEW_CNT | base_info.incorporation_date（取年） | v1 用 reg_info.incorporation_year | 🔧 可算（**v2.2 实查无 incorporation_year，需从 date 解析年份**） |
| 5 | 深圳服务机构规模 | M_SVC_SZ_SCALE | base_info.is_shenzhen(推导) + tech_score | v1 用 reg_info.city | 🔧 可算（服务能力待M3） |
| 6 | 深圳服务机构分布 | M_SVC_SZ_DISTRICT | **base_info.district** | v1 用 address 解析（无直字段） | ✅ **可算**（v2.2 实查 district 是直字段 varchar(50) 区县） |

**v2.2 修正**：指标 #6（深圳分布）从 v1 的"⚠️ 缺口"升级为"✅ 可算"（base_info 有 **district** 直字段，v2.1 误记为 area，v2.2 实查正名）。指标 #1（产业布局）**仍是 ⚠️**——industry 实际不存在、org_type 仅组织形式不可用、business_scope 质量不足，六类维度分类不可靠，待 Q-SVC-009 供方答复。指标 #4（新增动态）从 ✅ 降为 🔧（incorporation_year 实际不存在，需从 date 解析）。

### 2.2 M3 深度模型（bid §4.1.1.1.1.1.1.9，10项）

> 同 v1：依赖 SVC-ALGO-DESIGN-L01 产出物（仓内查无，D-1）；权重阈值 Q060~Q063 pending_client。model_id 列表不变。

| # | bid 模型 | model_id | v2 数据依赖变化 | 状态 |
|---|----------|----------|----------------|------|
| 1 | 服务链短板 | SVC_SERVICE_CHAIN_GAP | 服务质量数据仍无源 | 🔧⚠️ Q061 |
| 2 | 服务关系链 | SVC_SERVICE_RELATION_CHAIN | Nebula gkx_service | 🔧⚠️ Q062 |
| 3-8 | 六类技术力 | SVC_{FINANCE/IP/HR/MKT/CONSULT/INNOV}_TECH_POWER | base_info.industry 可分六类；但质量/案例数据无源 | 🔧⚠️ Q060 |
| 9 | 引入推荐 | SVC_ATTRACTION_RECOMMEND | 深圳连接度数据无源 | 🔧⚠️ Q063 |
| 10 | 培育推荐 | SVC_CULTIVATION_RECOMMEND | 潜力数据无源 | 🔧⚠️ Q063 |

### 2.3 八件套骨架（D9，更新 2 例）

#### M_SVC_ORG_CNT — 服务机构数量（v2）

| 字段 | 值 |
|------|-----|
| metric_id | M_SVC_ORG_CNT |
| definition | 满足准入规则且在营的服务机构去重数量；可按 service_type / region / incorporation_year 切片 |
| formula | COUNT(DISTINCT service_org_code) WHERE is_deleted=0 |
| source_tables | `["gkx_dwd.service_org"]` |
| source_systems | `["ods.dwd_org_base_info","ods.dwd_org_org_product_info"]` |
| update_freq | monthly |
| version | **v2.0.0**（来源改为 base_info） |

#### M_SVC_SZ_DISTRICT — 深圳服务机构分布（v2 新增可算）

| 字段 | 值 |
|------|-----|
| metric_id | M_SVC_SZ_DISTRICT |
| definition | 深圳各区服务机构去重数量及环比增长率 |
| formula | COUNT(DISTINCT service_org_code) WHERE is_shenzhen=1 GROUP BY district |
| source_tables | `["gkx_dwd.service_org"]` |
| source_systems | `["ods.dwd_org_base_info"]`（district 字段） |
| update_freq | monthly |
| version | v2.0.0 |

---

## 3. 第三方数据缺口（重矩阵）

### 3.1 承诺表 live 状态（08-04，基于 Wave A 40表）

| 承诺表 | SVC 角色 | 优先级 | live 行数 | 缺口判定 |
|--------|----------|--------|-----------|----------|
| `dwd_org_base_info` | **主源**（身份/区域/成立/资本/经营范围） | P0 | 20,000（实查确认） | ⚠️ 量级样例（口头711万，Q-SVC-005）；**无 industry 字段（Q-SVC-009）**；**org_type 仅组织形式不可用于准入** |
| `dwd_org_org_product_info` | 经营范围（六类补判） | P0 | **0（连续空）** | 🔴 **阻断**（base_info 无 industry，product_info 是唯一经营范围来源且为空；见 §1.5） |
| `dwd_org_shareholder_info` | 股东（关系链辅助） | P0 | 19,024 | ✅ |
| `dwd_org_executive_info` | 高管（关系链辅助） | P0 | 20,000 | ✅ |
| `dwd_org_annual_financial_info` | 财务（技术力辅助） | P0 | 5,352 | ✅ |
| `dwd_org_important_news_info` | 资讯（服务能力代理） | P0 | 913 | ⚠️ 量级小 |
| `dwd_org_stock_base` | 上市信息 | P0 | 5,845 | ✅ |
| `dwd_org_heis_info` | 高校机构 | P0 | 20,000 | ✅ |
| `dwd_research_institute_base_info` | 科研机构 | P0 | 2,075 | ✅ |
| `dwd_org_industry_tags` | 产业链关联企业 | P0 | **0（连续空）** | 🔴 产业布局指标受阻 |
| `dwd_org_industry_product_tags` | 产业链关联产品 | P0 | **0（连续空）** | 🔴 产品维度受阻 |
| `dwd_industry_chain_info` | 产业链图谱 | P0 | 180 | ⚠️ 量级小 |
| `dwd_org_recruit_info` | 招聘（HR技术力辅助） | P1 | 2,000 | ✅ |

### 3.2 非承诺表（v1 误用，v2 标注移出）

| 表 | v1 用途 | v2 处置 | 依据 |
|----|---------|---------|------|
| `dwd_org_reg_info` | 主源 | **作废**（0行空表，移出承诺） | 命名词典 §2 + Wave A removed line 126 |
| `dwd_org_tag_info` | 准入辅助 R3 | **作废**（移出承诺） | Wave A removed line 128 |
| `dwd_org_financing_info` | M_SVC_INVEST_Y 来源 | **移出承诺**（旁路949行，非承诺） | Wave A removed line 129 |
| `dwd_org_invest_info` | M_SVC_INVEST_Y 来源 | **移出承诺** | Wave A removed line 130 |

### 3.3 缺口矩阵（v2 重做）

| # | 缺口项 | 有表 | 有行 | 影响 | v1→v2 变化 | 处置 |
|---|--------|------|------|------|-----------|------|
| G1' | product_info 空 | ✅ | ❌(0) | main_activities 缺失，六类补判不可用 | **v1=阻断 → v2.0=非阻断（误判，以为 industry 可替）→ v2.1=🔴 阻断**（industry 实际不存在，product_info 是经营范围唯一来源且空） | 见 §1.5；Q-SVC-009 待供方核验 industry 是否补建 |
| G2' | industry_tags 空 | ✅ | ❌(0) | 产业链关联企业维度缺 | 同 v1 | 暂置灰 |
| G3' | industry_product_tags 空 | ✅ | ❌(0) | 产品维度缺 | 同 v1 | 暂置灰 |
| G4' | financing_info 移出承诺 | ❌(非承诺) | 949(旁路) | M_SVC_INVEST_Y 无承诺源 | **v1=⚠️ → v2=❌ 无源** | 等供应方确认是否纳入 Wave B 或旁路表可用 |
| G5' | invest_info 移出承诺 | ❌(非承诺) | — | INVEST 事件无源 | 同 v1 | 同上 |
| G6' | reg_info/tag_info 移出承诺 | ❌(非承诺) | 0/— | v1 的 R3/R5 规则失效 | **v2 新增** | 打标签规则改为 R1'/R2'/R3'（§1.5） |
| G7' | base_info 量级样例 | ✅ | 20,000 | M_SVC_ORG_CNT 量级失真 | 同 v1 | 标 ⚠️ 样例；Q-SVC-005 |
| G8' | org_size 无字段 | — | — | 企业规模维度缺 | **v2 新增**（v1 误以为有） | 暂空，二期补 |
| G9' | service_tag_raw 无源 | — | — | 原始标签串缺 | **v2 新增**（tag_info 移出） | 暂空 |
| G10' | 投融资预聚合字段无源 | — | — | financing_count/invest_count/latest_* 缺 | **v2 新增** | 相关字段暂空，等 Wave B |
| G11' | 服务质量/案例数据无源 | ❌ | — | M3 模型 1/3~7/9~10 受阻 | 同 v1 | Q-SVC-007 |
| G12' | country 无字段 | — | — | 全球分布指标不可算 | 同 v1 | ext.country 预留 |
| G13' | **base_info 无 industry 字段** | — | — | 六类精确分类无结构化主路径 | **v2.1 新增**（v2.0 误信承诺文档） | Q-SVC-009；降级 R1'''，UI 带「待核验」 |
| G14' | **org_type 仅工商组织形式，无服务机构语义** | ✅ | 20,000 | 服务机构准入无可靠主路径（org_type 不能圈定服务机构池） | **v2.2 新增**（v2.1 误用 org_type 主准入） | 见 §1.5.2；准入只能靠 business_scope 尽力而为 + 人工复核；Q-SVC-010 |

### 3.4 缺口分级（v2.2）

| 级别 | 缺口 | 变化 |
|------|------|-----------|
| ❌ 无源 | G4'/G5'（投融资移出承诺）、G10'（预聚合无源）、G11'（质量/案例）、G8'/G9'（字段/标签无源） | v2 新增多个 ❌ |
| 🔴 阻断 | G2'/G3'（industry_tags/product_tags 空）、**G1'（product_info 空，无 industry 替代）**、**G13'（base_info 无 industry 字段）**、**G14'（org_type 无服务机构语义，准入无主路径）** | **v2.2：G14' 新增（准入本身阻断）** |
| ⚠️ 样例 | G7'（base_info 2万） | 同 v1 |

---

## 4. 问题或待决策项（重登记）

### 4.1 v1 已确认项（维持）

| 编号 | 事项 | 状态 |
|------|------|------|
| Q-ALGO-006 | 六类服务类型枚举与打标签口径 | ✅ 已确认（口径不变） | **v2.2 修正**：industry 不存在、org_type 仅组织形式，打标签仅剩 business_scope 关键词（见 §1.5） |

### 4.2 v2 待决策项

| 编号 | 事项 | 状态 | v1→v2 变化 | 临时默认 |
|------|------|------|-----------|----------|
| Q-SVC-001 | 服务机构 vs 一般企业边界 | 🔴 | **v2.2 升级为 🔴**（org_type 主准入失效，边界判定无可靠主路径） | **v2.2：仅靠 business_scope 尽力而为 + 人工复核，UI 带「待核验」** |
| Q-SVC-002 | M_SVC_ORG_CNT 计数口径 | 🟡 | 维持 | DISTINCT service_org_code |
| Q-SVC-003 | 投融资领域分类来源 | 🟡 | 维持 | 暂 NULL |
| Q-SVC-004 | district 抽取规则 | 🟢→**可关闭** | **v2.2 实查修正：字段名是 district（不是 area），是直字段，无需地址解析** | 直接用 district 字段 |
| Q-SVC-005 | base_info 量级口径（2万 vs 711万） | 🟡 | 维持（表名 reg_info→base_info） | 标 ⚠️ 样例 |
| Q-SVC-006 | financing_info/invest_info 纳入 Wave B | 🟡 | **v2 扩展**（v1 只问 invest，v2 加 financing） | 旁路表暂不用 |
| Q-SVC-007 | 服务质量/案例三方源 | 🟡 | 维持 | 无源时 M3 相关模型置灰 |
| **Q-SVC-008**（v2新增，v2.2修正） | ~~industry 码表~~ → ~~org_type 主准入+business_scope 辅助~~ → **business_scope 关键词词典（唯一可用信号）** | 🟡 | **v2.0=industry（误）；v2.1=org_type+business_scope（org_type 实查不可用）；v2.2=仅 business_scope** | 算法侧维护 business_scope→六类关键词词典；UI 标「待核验」；准确率有上限 |
| **Q-SVC-009**（v2.1新增，v2.2 实查确认） | **承诺文档 xlsx 的 industry 字段与实际建表不符**：xlsx 列 industry/industry_l1_name 等7字段，实际 `dwd_org_base_info` 建表无任何 industry 字段（v2.2 ODS 库实查确认）。请供方核验：(1) industry 是否后续补建？(2) 还是长期以 business_scope 替代？ | 🟡 | **v2.2 ODS 实查确认**（v2.1 基于建表 DDL，v2.2 基于直连库 SHOW CREATE + 字段分布） | 临时按 business_scope + 人工复核；精确六类分类待此答复 |
| **Q-SVC-010**（v2.2新增） | **服务机构准入本身无可靠主路径**：industry 不存在、org_type 仅工商组织形式（实查 TOP 值全为"有限责任公司"等，无服务机构语义）、business_scope 自由文本质量不足。当前数据**既无法可靠圈定"哪些机构是服务机构"，更无法精确区分六类**。是否：(1) 接受 business_scope 尽力而为 + 人工复核方案（准确率有限，UI 带「待核验」）？(2) 调整功能范围（如六类分类降级为"服务机构总览不分六类"）？(3) 等待供方补 industry 后再实现六类？ | 🔴 | **v2.2 新增**（v2.1 误以为 org_type 可准入） | 临时按 business_scope 尽力而为；**此为阻断级，须甲方+供方共同决策** |
| Q060~Q063 | M3 权重/阈值/口径/数据源 | 🟡 | 维持 | pending_client |

> **Q-SVC-004 可关闭**：v1 以为 district 要从 address 解析（待定），v2.2 实查 base_info 自带 **district** 直字段（v2.1 误记为 area），直接取值即可。

---

## 5. 架构合规自检

| # | 铁律 | v2 合规 | 说明 |
|---|------|---------|------|
| 1 | 算法只在 Python | ✅ | 数据设计文档 |
| 2 | Java 只读 ADS | ✅ | SVC 指标经 gkxlumen-metrics |
| 3 | 图谱 NebulaGraph | ✅ | gkx_service |
| 4 | 数据血缘 D9 | ✅ | 八件套骨架，缺口标 ❌/⚠️，未伪闭合 |
| 5 | 不替甲方拍板 | ✅ | 歧义登记决策清单 |
| 6 | cicd: skip_design_only | ✅ | — |
| 7 | cost 四字段 | ✅ | — |
| 8 | **数据真源以承诺表为准** | ✅ | v2 严格按 Wave A 40表，不照搬 live 旧名 |

---

## 6. 依赖与风险

### 6.1 依赖

| 编号 | 依赖项 | 状态 | v1→v2 变化 |
|------|--------|------|-----------|
| D-1 | SVC-ALGO-DESIGN 产出物落盘 | 🔴 仓内查无 | 同 v1 |
| D-2 | product_info 回灌 | 🔴 连续空 | **v1=阻断 → v2.0=非阻断（误判）→ v2.1=🔴 阻断**（industry 不存在，product_info 是经营范围唯一结构化来源） |
| D-3 | financing/invest 纳入 Wave B | 🟡 均移出承诺 | **v2 扩展**（v1 只问 invest） |
| D-4 | Q060~Q063 甲方确认 | 🟡 pending | 同 v1 |
| D-5 | base_info 量级澄清 | 🟡 2万 vs 711万 | 同 v1（表名更新） |

### 6.2 v2.2 风险变化

| 风险 | v1 | v2.2 |
|------|----|----|
| **服务机构准入阻断** | 🔴 高（product_info 空） | **🔴 极高**（v2.2 实查：industry 不存在 + org_type 仅组织形式 + business_scope 质量不足 → 准入本身无可靠主路径） |
| 六类打标签阻断 | 🔴 高（product_info 空） | **🔴 高**（同上，且六类细分比准入更难） |
| 投融资指标无源 | ⚠️ 中（invest 未承诺） | 🔴 高（financing+invest 均移出承诺，M_SVC_INVEST_Y 完全无源） |
| M3 模型数据缺 | 🔴 高 | 🔴 高（不变） |

---

## 7. 附录：v1→v2.0→v2.1→v2.2 变更对照

| 维度 | v1（作废） | v2.0（误判） | v2.1（修正） | **v2.2（实查定论，本版）** |
|------|-----------|-----------|-----------|-----------|
| 主表 | dwd_org_reg_info（0行空表） | dwd_org_base_info（20,000行） | 同 v2.0 ✅ | 同 v2.0 ✅（ODS 实查确认 20000 行） |
| Mapping 真源 | Mapping v2（作废） | Mapping v3 + Wave A 清单 v1.2 | 同 v2.0 ✅ | 同 v2.0 ✅ |
| **industry 字段** | — | ~~以为有（信 xlsx）~~ | 实际不存在（Q-SVC-009） | **ODS 实查确认不存在** ✅ |
| **org_type 字段** | 准入辅助 | 准入辅助 | 主准入（R1''） | **❌ 仅工商组织形式，无服务机构语义，准入失效**（G14'） |
| **六类打标签主路径** | product_info.industry_class（空） | ~~base_info.industry（误判）~~ | org_type 主准入 + business_scope 辅助 | **仅剩 business_scope 尽力而为 + 人工复核**（R1'''） |
| **district 字段** | address 解析（待定） | base_info.area 直字段 | 同 v2.0 | **正名为 district（v2.1 误记 area），ODS 实查确认** |
| tag_info | 准入辅助 R3 | 移出承诺，R3 作废 | 同 v2.0 ✅ | 同 v2.0 ✅ |
| financing_info | M_SVC_INVEST_Y 来源 | 移出承诺，无源 | 同 v2.0 ✅ | 同 v2.0 ✅ |
| invest_info | M_SVC_INVEST_Y 来源 | 移出承诺 | 同 v2.0 ✅ | 同 v2.0 ✅ |
| org_size | 以为有 | 确认无（G8'） | 同 v2.0 ✅ | 同 v2.0 ✅ |
| **M1 #1 产业布局** | ⚠️ 缺口 | ~~🔧 可算（误判）~~ | ⚠️ 六类维度不可靠 | **⚠️ 仍不可靠**（待 Q-SVC-009/010） |
| **M1 #4 新增动态** | ✅ 可算 | ✅ 可算 | ✅ 可算 | **🔧 需从 incorporation_date 解析年份**（无 incorporation_year） |
| M1 #6 深圳分布 | ⚠️ 缺口 | ✅ 可算（误记 area） | ✅ 可算（误记 area） | **✅ 可算（正名 district）** |
| M1 #3 投融资 | 🔧 可算（半边） | ❌ 无承诺源 | 同 v2.0 ✅ | 同 v2.0 ✅ |
| **缺口总数** | 12项（3阻断） | 12项（2阻断+4无源） | 13项（3阻断+4无源） | **14项（4阻断+4无源，G14' 新增：准入阻断）** |
| 新增决策项 | Q-SVC-005/006/007 | + Q-SVC-008 | + Q-SVC-009 | Q-SVC-008 改仅 business_scope + **Q-SVC-010（准入阻断，🔴）** |

---

*v2.2 文档版本（ODS 实查定论：industry❌ + org_type 不可用 + district 正名） · human:侯佳伟 · SVC-DATA-ANALYSIS-L01 · 2026-08-05*
