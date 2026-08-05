# 服务机构维度（SVC/E6）数据分析报告（v2 重写版）

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-SVC-ANALYSIS-L01 |
| 任务 ID | SVC-DATA-ANALYSIS-L01 |
| Epic | E-ALGO-LIB-DEMO |
| 版本 | **v2.0.0（重写）** — v1 基于已作废的 Mapping v2 / `dwd_org_reg_info`，作废 |
| 状态 | Draft（待 architect-agent 会签 + 监管人 human:侯佳伟 审定） |
| 执行人 / 监管人 | human:侯佳伟 |
| 认领类型 | coordinator_dispatch · claimed_by=human:侯佳伟 |
| 创建日期 | 2026-08-05 |
| 仓 | agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`） |

> **v2 重写原因**：监管人 human:侯佳伟 指出，v1 报告基于的 `服务机构相关-ODS到DWD字段映射分析报告(v2).md` 使用了已作废的表名 `dwd_org_reg_info`。最新事实（GDF-ENT-WORKPACK-v1.2 命名词典 + Wave A 承诺表清单 + Mapping v3）：**国内机构主表是 `dwd_org_base_info`**，`dwd_org_reg_info` 已移出承诺表且 live 为 0 行空表。本 v2 基于 `dwd_org_base_info` 体系重新分析，**不照搬 v1**。

## 数据真源（v2 全部更新）

| 真源 | 路径 | 用途 |
|------|------|------|
| **命名词典 v1.2** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/01-命名与分层词典.md` | 表名归一（base_info vs reg_info） |
| **Wave A 承诺表清单** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml` | 40 张承诺表（含/不含判定） |
| **企业维 Mapping v3** | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/09-企业维-ODS到DWD-Mapping说明-v3.md` | base_info 字段映射（SVC 复用） |
| **live 探测 08-04** | `data/third-party-source/gkx-mysql-raw/加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-04.md` | 实际行数 |
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

### 1.1 关键事实修正（v1 vs v2）

| 项 | v1（作废） | v2（本版） | 依据 |
|----|-----------|-----------|------|
| 主表名 | `dwd_org_reg_info` | **`dwd_org_base_info`** | 命名词典 §2 + Wave A 清单 line 56 |
| 主表 live 行数 | 未探测（假设有） | **20,000**（reg_info=0 行空表） | LIVE-08-04 + 国内机构库报告 |
| tag_info | 准入辅助 R3 来源 | **不在承诺40表** | Wave A 清单 removed_vs_v1_1 line 128 |
| financing_info | M_SVC_INVEST_Y 来源 | **不在承诺40表**（旁路949行） | Wave A 清单 removed line 129 |
| invest_info | M_SVC_INVEST_Y 来源 | **不在承诺40表** | Wave A 清单 removed line 130 |
| Mapping 真源 | Mapping v2（作废） | **Mapping v3** | 09-企业维 v3 §0 明确作废 v2 |
| 六类打标签来源 | product_info（空）→ 退化 org_type+tag | **base_info.industry 字段可直接用** + product_info（空时降级） | Mapping v3 §2 line 68-69 |

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
| 2 | service_org_code | ✅ external_id | base_info.external_id | ✅ | v1 用 reg_info.external_id（表名错） |
| 3 | org_id | ✅ org_id | base_info.org_id | ✅ | v1 用 reg_info.org_id |
| 4 | enterprise_code | ✅ external_id | base_info.external_id | ✅ | 同上 |
| 5 | name_cn | ✅ name_cn | base_info.name_cn | ✅ | 同上 |
| 6 | **service_type** | 🔧 base_info.industry / industry_l1_name 打标签 | base_info | 🔧 | **v1 依赖 product_info（空）；v2 改用 base_info.industry** |
| 7 | service_type_source | 🔧 命中来源 | — | 🔧 | — |
| 8 | service_type_tags | 🔧 JSON 数组 | — | 🔧 | — |
| 9 | org_type | ✅ org_type | base_info.org_type | ✅ | v1 用 reg_info.org_type |
| 10 | province | ✅ province | base_info.province | ✅ | — |
| 11 | city | ✅ city | base_info.city | ✅ | — |
| 12 | district | ✅ **area** | base_info.area | ✅ | **v1 用 address 解析；v2 承诺字段名=area，有直字段** |
| 13 | address | ✅ address | base_info.address | ✅ | — |
| 14 | addr_lng | ✅ addr_lng | base_info.addr_lng | ✅ | — |
| 15 | addr_lat | ✅ addr_lat | base_info.addr_lat | ✅ | — |
| 16 | incorporation_date | ✅ incorporation_date | base_info.incorporation_date | ✅ | — |
| 17 | incorporation_year | ✅ incorporation_year | base_info.incorporation_year | ✅ | — |
| 18 | org_size | ❌ **无源** | — | ❌ | **v1 以为有；Mapping v3 §2 line 75 确认 base_info 无 org_size** |
| 19 | registered_capital_value | 🔧 元→万元 | base_info.registered_capital_value | 🔧 | v1 直取（未做单位换算） |
| 20 | listing_status | ✅ listing_status | base_info.listing_status | ✅ | — |
| 21 | industry_class | ✅ industry / industry_l1_name | base_info（优先最深 industry，空则 l1_name） | ✅ | **v1 用 product_info.industry_class（空）；v2 用 base_info 自带 industry** |
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

### 1.5 六类打标签的新路径（v2 关键改进）

v1 的六类打标签完全依赖 `product_info`（空表），只能退化到 org_type 粗筛。v2 发现 **`base_info` 自带 `industry` / `industry_l1_name` / `industry_l1_code` 字段**（Mapping v3 §2 line 68-69），打标签有了新路径：

| 优先级 | 来源 | 字段 | 状态 | 说明 |
|--------|------|------|------|------|
| 1 | base_info | industry / industry_l1_name | ✅ 有数（20,000行） | 行业码表匹配六类（主路径） |
| 2 | product_info | main_activities | ⚠️ 空（连续空） | 经营范围关键词补判（product_info 回灌后激活） |
| 3 | base_info | org_type | ✅ 有数 | 机构类型含"服务/中介/代理"→准入辅助 |

**v2 打标签规则**（替代 v1 的 R1~R5）：
- R1'：`base_info.industry` / `industry_l1_name` 命中六类服务行业码/关键词 → 打标签
- R2'：`product_info.main_activities` 命中六类关键词 → 补判（product_info 空时跳过）
- R3'：`base_info.org_type` 含"服务机构/中介/代理" → 准入辅助（不单独决定 service_type）
- ~~R3（tag_info.org_tag）~~：**作废**，tag_info 不在承诺表
- ~~R5（invest_info 投资方 heuristic）~~：**作废**，invest_info 不在承诺表

**结论**：product_info 空时，**base_info.industry 仍可支撑六类打标签**（主路径不依赖 product_info）。v1 的"退化方案"在 v2 下不再需要——直接用 base_info.industry 做主路径即可。

---

## 2. 服务机构指标（重对齐）

### 2.1 M1 基础指标（bid §4.1.1.1.1.1.1.1.4，6项）

| # | bid 指标 | metric_id | v2 数据来源 | v1 偏差 | 状态 |
|---|----------|-----------|------------|---------|------|
| 1 | 全球服务机构产业布局 | M_SVC_INDUSTRY_LAYOUT | base_info.industry | v1 用 product_info（空） | 🔧 **可算**（industry 有数） |
| 2 | 全球服务机构分布 | M_SVC_ORG_CNT | base_info.province/city | v1 用 reg_info | 🔧 可算（无 country，全球维度待补） |
| 3 | 投融资动态资讯 | M_SVC_INVEST_Y | **无承诺源** | v1 用 financing_info（移出承诺） | ❌ **无源** |
| 4 | 新增服务机构动态 | M_SVC_NEW_CNT | base_info.incorporation_year | v1 用 reg_info | ✅ 可算 |
| 5 | 深圳服务机构规模 | M_SVC_SZ_SCALE | base_info.is_shenzhen(推导) + tech_score | v1 用 reg_info.city | 🔧 可算（服务能力待M3） |
| 6 | 深圳服务机构分布 | M_SVC_SZ_DISTRICT | **base_info.area** | v1 用 address 解析（无直字段） | ✅ **可算**（area 是直字段） |

**v2 改善**：指标 #1 和 #6 从 v1 的"⚠️ 缺口"升级为"🔧 可算"——因为 base_info 自带 industry 和 area 字段。

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
| source_systems | `["ods.dwd_org_base_info"]`（area 字段） |
| update_freq | monthly |
| version | v2.0.0 |

---

## 3. 第三方数据缺口（重矩阵）

### 3.1 承诺表 live 状态（08-04，基于 Wave A 40表）

| 承诺表 | SVC 角色 | 优先级 | live 行数 | 缺口判定 |
|--------|----------|--------|-----------|----------|
| `dwd_org_base_info` | **主源**（身份/区域/行业/成立/资本） | P0 | 20,000 | ⚠️ 量级样例（口头711万，Q-SVC-005） |
| `dwd_org_org_product_info` | 经营范围（六类补判） | P0 | **0（连续空）** | 🟡 非阻断（base_info.industry 可替代主路径） |
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
| G1' | product_info 空 | ✅ | ❌(0) | main_activities 缺失，六类补判不可用 | **v1=阻断 → v2=非阻断**（base_info.industry 可替代） | product_info 回灌后激活补判；当前主路径用 base_info.industry |
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

### 3.4 缺口分级（v2）

| 级别 | 缺口 | v1→v2 变化 |
|------|------|-----------|
| ❌ 无源 | G4'/G5'（投融资移出承诺）、G10'（预聚合无源）、G11'（质量/案例）、G8'/G9'（字段/标签无源） | **v2 新增多个 ❌**（因 tag/financing/invest 移出承诺） |
| 🔴 阻断 | G2'/G3'（industry_tags/product_tags 空） | 同 v1 |
| ⚠️ 样例 | G7'（base_info 2万） | 同 v1 |
| 🟡 非阻断 | G1'（product_info 空，但有 base_info.industry 替代） | **v1=阻断 → v2=非阻断** |

---

## 4. 问题或待决策项（重登记）

### 4.1 v1 已确认项（维持）

| 编号 | 事项 | 状态 |
|------|------|------|
| Q-ALGO-006 | 六类服务类型枚举与打标签口径 | ✅ 已确认（打标签来源改为 base_info.industry，口径不变） |

### 4.2 v2 待决策项

| 编号 | 事项 | 状态 | v1→v2 变化 | 临时默认 |
|------|------|------|-----------|----------|
| Q-SVC-001 | 服务机构 vs 一般企业边界 | 🟡 | 维持（规则改为 R1'/R2'/R3'） | 命中即纳入 |
| Q-SVC-002 | M_SVC_ORG_CNT 计数口径 | 🟡 | 维持 | DISTINCT service_org_code |
| Q-SVC-003 | 投融资领域分类来源 | 🟡 | 维持 | 暂 NULL |
| Q-SVC-004 | district 抽取规则 | 🟢→**可关闭** | **v2: base_info.area 是直字段，无需地址解析** | 直接用 area 字段 |
| Q-SVC-005 | base_info 量级口径（2万 vs 711万） | 🟡 | 维持（表名 reg_info→base_info） | 标 ⚠️ 样例 |
| Q-SVC-006 | financing_info/invest_info 纳入 Wave B | 🟡 | **v2 扩展**（v1 只问 invest，v2 加 financing） | 旁路表暂不用 |
| Q-SVC-007 | 服务质量/案例三方源 | 🟡 | 维持 | 无源时 M3 相关模型置灰 |
| **Q-SVC-008**（v2新增） | base_info.industry 字段做六类打标签的码表对齐规则 | 🟡 | **v2 新增** | 算法侧维护 industry→六类映射词典 |
| Q060~Q063 | M3 权重/阈值/口径/数据源 | 🟡 | 维持 | pending_client |

> **Q-SVC-004 可关闭**：v1 以为 district 要从 address 解析（待定），v2 发现 base_info 自带 area 直字段，直接取值即可。

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
| D-2 | product_info 回灌 | 🟡 连续空 | **v1=阻断 → v2=非阻断**（base_info.industry 替代） |
| D-3 | financing/invest 纳入 Wave B | 🟡 均移出承诺 | **v2 扩展**（v1 只问 invest） |
| D-4 | Q060~Q063 甲方确认 | 🟡 pending | 同 v1 |
| D-5 | base_info 量级澄清 | 🟡 2万 vs 711万 | 同 v1（表名更新） |

### 6.2 v2 风险变化

| 风险 | v1 | v2 |
|------|----|----|
| 六类打标签阻断 | 🔴 高（product_info 空） | 🟡 中（base_info.industry 可用，product_info 补判缺） |
| 投融资指标无源 | ⚠️ 中（invest 未承诺） | 🔴 高（financing+invest 均移出承诺，M_SVC_INVEST_Y 完全无源） |
| M3 模型数据缺 | 🔴 高 | 🔴 高（不变） |

---

## 7. 附录：v1→v2 变更对照

| 维度 | v1（作废） | v2（本版） |
|------|-----------|-----------|
| 主表 | dwd_org_reg_info（0行空表） | dwd_org_base_info（20,000行） |
| Mapping 真源 | Mapping v2（作废） | Mapping v3 + Wave A 清单 v1.2 |
| 六类打标签主路径 | product_info.industry_class（空） | base_info.industry（有数） |
| district | address 解析（待定 Q-SVC-004） | base_info.area 直字段（Q-SVC-004 可关闭） |
| tag_info | 准入辅助 R3 | 移出承诺，R3 作废 |
| financing_info | M_SVC_INVEST_Y 来源 | 移出承诺，M_SVC_INVEST_Y 无源 |
| invest_info | M_SVC_INVEST_Y 来源 | 移出承诺 |
| org_size | 以为有 | 确认无（G8'） |
| M1 #1 产业布局 | ⚠️ 缺口 | 🔧 可算 |
| M1 #6 深圳分布 | ⚠️ 缺口 | ✅ 可算 |
| M1 #3 投融资 | 🔧 可算（半边） | ❌ 无承诺源 |
| 缺口总数 | 12项（3阻断） | 12项（2阻断+4无源） |
| 新增决策项 | Q-SVC-005/006/007 | + Q-SVC-008（industry 码表对齐） |

---

*v2 文档版本 · human:侯佳伟 · SVC-DATA-ANALYSIS-L01 · 2026-08-05*
