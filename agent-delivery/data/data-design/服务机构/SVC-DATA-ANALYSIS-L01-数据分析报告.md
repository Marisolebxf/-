# 服务机构维度（SVC/E6）数据分析报告

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-SVC-ANALYSIS-L01 |
| 任务 ID | SVC-DATA-ANALYSIS-L01 |
| Epic | E-ALGO-LIB-DEMO |
| 版本 | v1.0.0 |
| 状态 | Draft（待 architect-agent 会签 + 监管人 human:侯佳伟 审定） |
| 执行人 / 监管人 | human:侯佳伟 |
| 认领类型 | coordinator_dispatch · claimed_by=human:侯佳伟 |
| 创建日期 | 2026-08-05 |
| 仓 | agent-delivery（仅文档/数据设计资产；`cicd: skip_design_only`） |
| 数据真源 | `服务机构域数据库设计(v1).md`、`服务机构相关-ODS到DWD字段映射分析报告(v2).md`、`bid-reference/科技专题服务算法库.md` §4.1.1.1.1.1.1.1.4 + §4.1.1.1.1.1.1.9、`gkx-mysql-raw/加工/LIVE-DWD-ENTERPRISE-READINESS-2026-08-04.md` |

> **本报告定位**：在进入 SVC 实现波次之前，对 DWD 表设计做一次复核、对指标做一次清单化、对三方数据缺口做一次矩阵化、对开放项做一次登记。**不写 Java/前端、不强制 ETL 灌数**。所有业务口径歧义一律登记客户决策清单，**不替甲方拍板**（铁律 §3.8）。

---

## 目录

1. [DWD 表设计方案（复核）](#1-dwd-表设计方案复核)
2. [服务机构指标（清单 + 八件套骨架）](#2-服务机构指标清单--八件套骨架)
3. [第三方数据缺口（矩阵）](#3-第三方数据缺口矩阵)
4. [问题或待决策项（回填决策清单）](#4-问题或待决策项回填决策清单)
5. [架构合规自检](#5-架构合规自检)
6. [依赖与风险](#6-依赖与风险)
7. [附录：指标 ↔ bid 章节 ↔ DWD 字段对照全表](#7-附录指标--bid-章节--dwd-字段对照全表)

---

## 1. DWD 表设计方案（复核）

### 1.1 复核结论

以 `服务机构域数据库设计(v1).md` v1.0.0 + Mapping v2 为起点复核，**结论：v1 设计可承接，无颠覆性修订，仅做 3 处补强**。

| # | 复核项 | v1 现状 | 复核结论 | 偏离/as-built |
|---|--------|---------|----------|---------------|
| 1 | 表清单 | `gkx_dwd.service_org`（38 字段）+ `service_org_financing`（16 字段） | ✅ 维持 | 无 |
| 2 | 业务键 | `service_org_code` = `external_id`，缺失用 `svc:{org_id}` | ✅ 维持 | 无 |
| 3 | 分层 | ODS(`dwd_org_*`) → DWD(`gkx_dwd.service_org*`) → DWM(预留) → ADS(`ads_metric_timeseries`/`ads_model_score`) → Nebula `gkx_service` | ✅ 维持 | 无 |
| 4 | 与 ENT 边界 | SVC 仅存 38 字段子集 + `enterprise_code` 关联键，**禁止**复制 ENT 66 字段全量工商 | ✅ 维持 | 无 |
| 5 | service_type | DWD 衍生：`industry_class` + `main_activities` 打六类标签（Q-ALGO-006 ✅ 已确认） | ✅ 维持 | 无 |
| 6 | 覆盖率 | service_org 86.7% / financing 91.7% / 合计 88.1% | ✅ 维持 | 无 |
| 7 | DDL 物理表名 | 旧占位 `dwd_service_org_snapshot` 已废弃 → `gkx_dwd.service_org` | ✅ 维持 | 无 |

**3 处补强（非偏离，细化执行约束）**：

- **补强 A — `dwd_org_org_product_info` 空表兜底**：截至 2026-08-04 live 探测，该表（六类打标签的**分类主源**）连续空。ETL Phase 1 准入须支持「无 product_info 时退化为仅用 `dwd_org_reg_info.org_type` + `dwd_org_tag_info.org_tag` 做准入判定」，并打 `classification_rule_version=svc_rule_v1_degraded`；product_info 回灌后重跑升级 `svc_rule_v2`。
- **补强 B — `dwd_org_invest_info` 未在承诺 40 表**：`service_org_financing` 的 INVEST 事件来源 `dwd_org_invest_info` 不在 Wave A 承诺表清单（承诺清单见 `02-WaveA-贴源表清单.yaml`）。ETL Phase 2 灌 `service_org_financing` 时，INVEST 事件应标 `data_source='pending_wave_b'` 并允许暂空；FINANCING 事件（`dwd_org_financing_info` live=949 行）可先行。
- **补强 C — 旁路命名归一**：live 库存在 `dwd_org_change_record_info`（1,676）与承诺名 `dwd_org_changerecord_info`（10,901）双轨。SVC 域不直接消费变更记录，但若后续 ADS 需要"机构变更次数"辅助指标，须以承诺名 `dwd_org_changerecord_info` 为准（与 Q055 关联，待供应方澄清）。

### 1.2 表清单（承接 v1，不重复 DDL）

| # | DWD 表 | 字段数 | 角色 | 主源 ODS | 覆盖率 |
|---|--------|--------|------|----------|--------|
| 1 | `gkx_dwd.service_org` | 38 | 服务机构主表（六类 + 区域 + 能力摘要） | `dwd_org_reg_info` / `dwd_org_tag_info` / `dwd_org_org_product_info` | 86.7% |
| 2 | `gkx_dwd.service_org_financing` | 16 | 服务链投融资明细（FINANCING+INVEST 归一） | `dwd_org_financing_info` / `dwd_org_invest_info` | 91.7% |

> 完整逐字段映射见 Mapping v2 §5.1 / §5.2；完整 DDL 见 `database-design/科技专题服务算法库/ddl/gkx_dwd_svc_v1.sql`。本报告不复制 DDL，只做复核签注。

### 1.3 主键与交叉关联

| 键 | 类型 | 角色 | 说明 |
|----|------|------|------|
| `id` | BIGINT AUTO_INCREMENT | 物理主键/外键 | `service_org_financing.service_org_id` 引用 |
| `service_org_code` | VARCHAR(64) | **SVC 业务归一主键** | = `external_id`；缺失时 `svc:{org_id}` |
| `org_id` | VARCHAR(64) | ODS 关联键 | 对齐 `dwd_org_reg_info.org_id` |
| `enterprise_code` | VARCHAR(64) | ENT 交叉关联键 | = `external_id`，可 JOIN `gkx_dwd.enterprise` |
| Nebula vid | — | 图谱节点 | `svc:{service_org_code}`（与 RDBMS 对齐） |

**与 ENT/ORG 边界铁律**：
- SVC 独立业务键，**不**复用 ENT `enterprise_code` 作主键
- SVC 表**不存** enterprise 全量工商字段（专利/财务/供应链等需要时 ADS 层 JOIN 或 algorithm 聚合）
- 同一信用代码在 ENT 与 SVC **允许并存**（不同域、不同用途）

---

## 2. 服务机构指标（清单 + 八件套骨架）

### 2.1 指标分层

SVC 指标分两层，对齐 bid §4.1.1.1.1.1.1.1.4（基础指标模型，6 项）与 §4.1.1.1.1.1.1.9（产业服务深度分析模型，10 项）：

| 层 | bid 章节 | 模型数 | 落点 | 数据依赖 | 状态 |
|----|----------|--------|------|----------|------|
| M1 基础指标 | §4.1.1.1.1.1.1.1.4 | 6 | `ads_metric_timeseries` | `gkx_dwd.service_org` + `service_org_financing` | 🔧 可算（待 product_info 回灌） |
| M3 深度模型 | §4.1.1.1.1.1.1.9 | 10 | `ads_model_score` + Nebula `gkx_service` | service_org + 多源 + 图谱 | 🔧 Wave2（待 Q060~Q063） |

### 2.2 M1 基础指标清单（6 项，对齐 bid §4.1.1.1.1.1.1.1.4）

| # | bid 指标 | metric_id（草案） | 口径要点 | DWD 来源 | ODS 真源 | 状态 |
|---|----------|-------------------|----------|----------|----------|------|
| 1 | 全球服务机构产业布局 | M_SVC_INDUSTRY_LAYOUT | 按产业领域统计服务机构服务规模 + 环比增长率 | service_org.industry_class / main_activities | dwd_org_org_product_info | 🔧⚠️ product_info 空 |
| 2 | 全球服务机构分布 | M_SVC_ORG_CNT | 按国家/地区 COUNT(DISTINCT service_org_code) | service_org.province/city + ext.country | dwd_org_reg_info | 🔧 全球维度需补 country 抽取 |
| 3 | 投融资动态资讯 | M_SVC_INVEST_Y | 年度投融资事件金额合计 + 领域分类 | service_org_financing.amount / completion_date / industry_domain | dwd_org_financing_info / dwd_org_invest_info | 🔧⚠️ industry_domain 无源 |
| 4 | 新增服务机构动态 | M_SVC_NEW_CNT | 历年新增机构数（按 incorporation_year） | service_org.incorporation_year | dwd_org_reg_info | ✅ 可算 |
| 5 | 深圳服务机构规模 | M_SVC_SZ_SCALE | 深圳机构数量 + 服务能力（is_shenzhen=1） | service_org.is_shenzhen + tech_score | dwd_org_reg_info.city | 🔧 服务能力待 M3 |
| 6 | 深圳服务机构分布 | M_SVC_SZ_DISTRICT | 深圳各区机构数量 + 增长率 | service_org.district | dwd_org_reg_info.address 解析 | 🔧⚠️ district 规则待定（Q-SVC-004） |

### 2.3 M3 深度模型清单（10 项，对齐 bid §4.1.1.1.1.1.1.9）

> ⚠️ 本节指标口径依赖 `SVC-ALGO-DESIGN-L01` 产出的 `docs/产业服务算法设计说明.md`。**截至本报告日，该文档在 `demo-algo-ent-analysis` 仓内查无实体文件**（见 §6 依赖缺口 D-1）。下表口径要点来自 bid 原文 + handoff 声称的 10 模型 ID，权重/阈值均 `pending_client`（Q060~Q063）。

| # | bid 模型 | model_id（SVC-ALGO-DESIGN 声称） | 口径要点（bid 摘要） | 数据依赖 | 状态 |
|---|----------|-------------------------------|----------------------|----------|------|
| 1 | 服务链短板分析 | SVC_SERVICE_CHAIN_GAP | 服务质量/经营效益/服务类型三维指标 + 阈值定位短板成因 | service_org + 服务质量数据（无源） | 🔧⚠️ Q061 |
| 2 | 服务关系链 | SVC_SERVICE_RELATION_CHAIN | 关系强度(4:4:2)/层次(1/N-hop)/密度 + Nebula 图算法 | Nebula gkx_service + 关系数据 | 🔧⚠️ Q062 |
| 3 | 金融服务机构技术力 | SVC_FINANCE_TECH_POWER | 资金规模/融资成本/资金风险/服务质量四维加权 | service_org(type=1) + 财务数据 | 🔧⚠️ Q060 |
| 4 | 知识产权服务机构技术力 | SVC_IP_TECH_POWER | 专业能力/业务范围/成功案例/合作伙伴四维 | service_org(type=2) + 案例数据（无源） | 🔧⚠️ Q060 |
| 5 | 人力资源服务机构技术力 | SVC_HR_TECH_POWER | 人才资源/服务标准化/客户满意度三维 | service_org(type=3) + 招聘/反馈数据 | 🔧⚠️ Q060 |
| 6 | 市场营销服务机构技术力 | SVC_MKT_TECH_POWER | 调研能力/策划能力/成功项目案例三维 | service_org(type=4) + 项目案例（无源） | 🔧⚠️ Q060 |
| 7 | 咨询服务机构技术力 | SVC_CONSULT_TECH_POWER | 人才密度/行业经验/成功案例/行业声誉四维 | service_org(type=5) + 声誉数据（无源） | 🔧⚠️ Q060 |
| 8 | 科技创新服务机构技术力 | SVC_INNOV_TECH_POWER | 合作科研机构数/合作企业数/创新成果/转化成果四维 | service_org(type=6) + 科研合作数据 | 🔧⚠️ Q060 |
| 9 | 服务机构引入推荐 | SVC_ATTRACTION_RECOMMEND | 竞争力/产业相关度/政策匹配度/深圳连接度四维 | service_org + 政策匹配 + 深圳连接度 | 🔧⚠️ Q063 |
| 10 | 服务机构培育推荐 | SVC_CULTIVATION_RECOMMEND | 竞争力/产业相关度/政策匹配度/发展潜力四维 | service_org + 潜力数据 | 🔧⚠️ Q063 |

### 2.4 八件套骨架（D9 血缘，示例 2 项）

> 完整 `cfg_metric_lineage` 注册待实现波次；本报告先给骨架，缺口径标 🟡。规范真源：`data-lineage-policy.md` v1.3。

#### M_SVC_ORG_CNT — 服务机构数量

| 字段 | 值 |
|------|-----|
| metric_id | M_SVC_ORG_CNT |
| metric_name_zh | 服务机构数量 |
| definition | 满足 R1~R5 准入且在营的服务机构去重数量；可按 service_type / region / incorporation_year 切片 |
| formula | COUNT(DISTINCT service_org_code) WHERE is_deleted=0 |
| source_tables | `["gkx_dwd.service_org"]` |
| source_systems | `["ods.dwd_org_reg_info","ods.dwd_org_tag_info","ods.dwd_org_org_product_info"]` |
| update_freq | monthly |
| version | v1.0.0 |

#### M_SVC_INVEST_Y — 服务机构年度投融资总额

| 字段 | 值 |
|------|-----|
| metric_id | M_SVC_INVEST_Y |
| metric_name_zh | 服务机构年度投融资总额 |
| definition | 服务机构在指定自然年的投融资事件金额合计（元）；含被投融资与对外投资 |
| formula | SUM(amount) WHERE YEAR(completion_date)=:year AND event_type IN ('FINANCING','INVEST') |
| source_tables | `["gkx_dwd.service_org_financing","gkx_dwd.service_org"]` |
| source_systems | `["ods.dwd_org_financing_info","ods.dwd_org_invest_info"]` |
| update_freq | monthly |
| version | v1.0.0 |

> ⚠️ `industry_domain`（投融资领域分类）无 ODS 直字段，M_SVC_INVEST_Y 按领域切片暂不可算，待 Q-SVC-003 闭合。

---

## 3. 第三方数据缺口（矩阵）

### 3.1 数据源现状（2026-08-04 live 探测）

对照 `LIVE-DWD-ENTERPRISE-READINESS-2026-08-04.md`，SVC 域依赖的 ODS 表 live 状态：

| ODS 表 | SVC 角色 | 承诺优先级 | live 行数 | 缺口判定 |
|--------|----------|-----------|-----------|----------|
| `dwd_org_reg_info` | 主源（身份/区域/成立/资本） | P0 | 20,000 | ⚠️ 量级样例级（口头 711 万待澄清，Q055） |
| `dwd_org_tag_info` | 准入辅助（资质/荣誉标签） | P0 | 未单列（应在 base_info 体系内） | 🟡 待核 |
| `dwd_org_org_product_info` | **分类主源**（行业+经营范围→六类） | P0 | **0（连续空）** | 🔴 **阻断六类打标签** |
| `dwd_org_industry_tags` | 行业标签 | P0 | **0（连续空）** | 🔴 阻断产业布局指标 |
| `dwd_org_industry_product_tags` | 产品标签 | P0 | **0（连续空）** | 🔴 阻断产品维度 |
| `dwd_org_financing_info` | 投融资（被投方） | P1（旁路有数） | 949 | ⚠️ 量级小 |
| `dwd_org_invest_info` | 投融资（投资方） | **未在承诺 40 表** | 未探测 | 🔴 INVEST 事件无源 |
| `dwd_org_important_news_info` | 服务能力/动态资讯 | P0 | 913 | ⚠️ 量级小 |
| `dwd_org_industry_chain_dtl` | 产业布局（与 CHAIN 交叉） | — | 未在 40 表 | 🟡 待 Wave B |
| `dwd_org_industry_chain_news_info` | 产业链资讯 | — | 1 | 🔴 几乎空 |

### 3.2 缺口矩阵（按"有无表/有无行/关键字段缺失"）

| # | 缺口项 | 有表 | 有行 | 关键字段缺失 | 影响 | 临时默认 / 兜底 |
|---|--------|------|------|-------------|------|-----------------|
| G1 | product_info 空表 | ✅ | ❌(0) | industry_class / main_activities 全缺 | 六类 service_type 无法打标签；M1 #1/#2/#6 受阻 | 退化规则 R4(org_type)+R3(org_tag) 准入；标 `svc_rule_v1_degraded` |
| G2 | industry_tags 空表 | ✅ | ❌(0) | 行业标签全缺 | M_SVC_INDUSTRY_LAYOUT 不可算 | 暂置灰，标 🧪 Mock |
| G3 | industry_product_tags 空表 | ✅ | ❌(0) | 产品标签全缺 | 产品维度指标不可算 | 暂置灰 |
| G4 | invest_info 未承诺 | ❌(未在40表) | — | INVEST 事件全缺 | M_SVC_INVEST_Y 仅 FINANCING 半边；service_org_financing INVEST 行暂空 | INVEST 标 `pending_wave_b`，金额不计入 |
| G5 | financing_info 量级小 | ✅ | 949 | — | M_SVC_INVEST_Y 样例级 | 可算但标 ⚠️ 样例 |
| G6 | reg_info 量级样例 | ✅ | 20,000 | — | M_SVC_ORG_CNT 远低于口头口径 | 标 ⚠️ 样例；待 Q055 供应方澄清 711 万口径 |
| G7 | industry_domain 无直字段 | — | — | service_org_financing.industry_domain | M_SVC_INVEST_Y 按领域切片不可算 | 暂 NULL；Q-SVC-003 |
| G8 | district 无直字段 | — | — | service_org.district 需地址解析 | M_SVC_SZ_DISTRICT 精度依赖解析规则 | 地址关键词 + dim_region；Q-SVC-004 |
| G9 | country 无直字段 | — | — | service_org 无 country 字段 | M_SVC_ORG_CNT 全球分布不可算 | ext.country 预留；待 Wave B |
| G10 | 服务质量数据无源 | ❌ | — | 服务质量评价/客户满意度全缺 | M3 模型 1/3/4/5/6/7 受阻 | 待 Q060/Q061 + 三方补充 |
| G11 | 成功案例/合作伙伴无源 | ❌ | — | M3 模型 4/6/7 案例维度全缺 | 技术力评估缺关键输入 | 待三方补充或置灰 |
| G12 | 政策匹配度数据无源 | ❌ | — | M3 模型 9/10 政策匹配维度 | 推荐模型缺输入 | 政策匹配子模型待 POL 域联动 |

### 3.3 缺口分级

| 级别 | 缺口 | 处置建议 |
|------|------|----------|
| 🔴 阻断 | G1/G2/G3（product/tags 空）、G4（invest 未承诺）、G10/G11（服务质量/案例无源） | G1~G3：等供应方回灌 + 退化规则兜底；G4：上 Wave B；G10/G11：登记三方补充需求，M3 相关模型标 Wave2 |
| ⚠️ 样例 | G5/G6（量级小） | 可算但 UI 标 ⚠️ 样例；不阻塞 Mapping 试点 |
| 🟡 待定 | G7/G8/G9（字段缺失）、G12（政策匹配） | G7/G8 待 Q-SVC-003/004；G9 待 Wave B；G12 待 POL 域联动 |

---

## 4. 问题或待决策项（回填决策清单）

### 4.1 已确认项（不重复登记）

| 编号 | 事项 | 确认状态 | 说明 |
|------|------|----------|------|
| Q-ALGO-006 | 六类服务类型枚举与打标签口径 | ✅ 已确认（2026-06-23） | ODS 无直字段；industry_class + main_activities 打标签；六类枚举见 v1 §4.2 |

### 4.2 待甲方确认项（本报告复核/新增）

> 下列项已登记或需登记 `客户决策清单跟踪表.md`。**禁止替甲方拍板**（铁律 §3.8）。下表"本报告动作"列说明是否新增/更新/维持。

| 编号 | 事项 | 状态 | 影响字段/模型 | 临时默认 | 本报告动作 |
|------|------|------|--------------|----------|-----------|
| Q-SVC-001 | 服务机构 vs 一般企业边界（R1~R5 阈值） | 🟡 待确认 | ETL 准入规则 | 命中任一 R 即纳入 | 维持（v1 已登） |
| Q-SVC-002 | M_SVC_ORG_CNT 计数口径（org vs org×type） | 🟡 待确认 | M_SVC_ORG_CNT 分组 | DISTINCT service_org_code | 维持（v1 已登） |
| Q-SVC-003 | 投融资领域分类来源（industry_domain） | 🟡 待确认 | service_org_financing.industry_domain / M_SVC_INVEST_Y 切片 | 暂 NULL | 维持（v1 已登） |
| Q-SVC-004 | district 抽取规则（深圳各区） | 🟡 待确认 | service_org.district / M_SVC_SZ_DISTRICT | 地址关键词 + dim_region | 维持（v1 已登） |
| Q060 | 六类技术力指标权重与阈值 | 🟡 pending_client | M3 模型 3~8 / M_SVC_TECH_POWER_* | 等权草案 | 维持（SVC-ALGO-DESIGN 已登） |
| Q061 | 服务链短板判定阈值与成因词典 | 🟡 pending_client | M3 模型 1 / M_SVC_CHAIN_GAP_* | <45 短板、≥70 优势 | 维持（SVC-ALGO-DESIGN 已登） |
| Q062 | 服务关系强度/层次/密度口径 | 🟡 pending_client | M3 模型 2 / M_SVC_RELATION_* | 4:4:2 强度 | 维持（SVC-ALGO-DESIGN 已登） |
| Q063 | 机构潜力、深圳连接度数据源 | 🟡 pending_client | M3 模型 9~10 / M_SVC_ATTRACTION_*/CULTIVATION_* | 融资/关系边代理 | 维持（SVC-ALGO-DESIGN 已登） |
| **Q-SVC-005**（新增） | reg_info 量级口径（20,000 vs 口头 711 万） | 🟡 待供应方澄清 | M_SVC_ORG_CNT 量级可信度 | 标 ⚠️ 样例 | **新增**（关联 Q055） |
| **Q-SVC-006**（新增） | invest_info 是否纳入 Wave B 承诺 | 🟡 待供应方确认 | M_SVC_INVEST_Y INVEST 半边 | INVEST 标 pending_wave_b | **新增** |
| **Q-SVC-007**（新增） | 服务质量/成功案例/合作伙伴三方源是否供应 | 🟡 待甲方/供应方确认 | M3 模型 1/3~7/9~10 关键输入 | 无三方源时相关模型标 Wave2 置灰 | **新增** |

> Q-SVC-005~007 为本报告复核新增，将在 §4.3 回填到决策清单跟踪表。Q055（国内机构库主体表空）已存在，Q-SVC-005 与之关联但聚焦 SVC 量级口径，单列避免与机构库全域问题混淆。

### 4.3 决策清单回填动作

本报告完成后，将向 `客户决策清单跟踪表.md` 追加 Q-SVC-005 / Q-SVC-006 / Q-SVC-007 三条 🟡 记录（见 handoff §3）。Q-SVC-001~004、Q060~Q063 已存在，**不重复登记**，仅在本报告交叉引用。

---

## 5. 架构合规自检

| # | 铁律（公约 §2） | 本报告合规 | 说明 |
|---|----------------|-----------|------|
| 1 | 算法只在 Python | ✅ | 本报告为数据设计文档，未涉及 Java 算法；M3 模型规划在 Python |
| 2 | 调用链 前端→Java REST→Python /internal | ✅ | SVC 指标 Java 只读 ADS，不越层 |
| 3 | 图谱 NebulaGraph | ✅ | SVC 关系链用 `gkx_service`，未引入 Neo4j |
| 4 | 可观测性 | 🟦 | 本阶段不涉及（设计文档） |
| 5 | CI/CD | ✅ | `cicd: skip_design_only` |
| 6 | demo2 只读 merge | ✅ | 本任务只在 agent-delivery，不动 demo 仓 |
| 7 | 共享聚合核心 | ✅ | SVC 指标经 gkxlumen-metrics，前端只调 Java |
| 8 | 数据策略 ADS 先行 + Mock | ✅ | M1 可算路径用真数，缺口路径标 🧪 Mock / ⚠️ 样例 |
| 9 | 前端规范唯一来源 D8 | 🟦 | 本任务无前端产物 |
| 10 | 数据血缘 D9 | ✅ | §2.4 给八件套骨架；缺口径标 🟡，未伪闭合 |
| 11 | 交互规范 D10 | 🟦 | 本任务无交互产物 |
| — | §3.8 业务口径不替甲方拍板 | ✅ | 所有歧义登记决策清单，临时默认标 🟡 |

---

## 6. 依赖与风险

### 6.1 依赖

| 编号 | 依赖项 | 依赖对象 | 状态 | 风险 |
|------|--------|----------|------|------|
| D-1 | `docs/产业服务算法设计说明.md`（SVC 10 模型分册） | SVC-ALGO-DESIGN-L01 handoff 声称已产出 | 🔴 **仓内查无实体文件** | M3 模型口径/权重/阈值无权威来源；本报告 §2.3 口径要点来自 bid 原文 + handoff 声称的 model_id，需 algorithm-agent 落盘确认 |
| D-2 | `dwd_org_org_product_info` 回灌 | 供应方 | 🟡 连续空 | 六类打标签阻断；已给退化规则兜底 |
| D-3 | `dwd_org_invest_info` 纳入 Wave B | 供应方 | 🟡 未承诺 | M_SVC_INVEST_Y INVEST 半边缺 |
| D-4 | Q060~Q063 甲方确认 | PM / 甲方 | 🟡 pending_client | M3 十模型权重/阈值无法定稿 |
| D-5 | Q055 机构库量级澄清 | 供应方 | 🟡 待确认 | M_SVC_ORG_CNT 量级可信度 |

### 6.2 风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| SVC-ALGO-DESIGN 产出物未落盘导致 M3 口径悬空 | 🔴 高 | 已在 §2.3 / D-1 标注；建议 coordinator 跟进 algorithm-agent 补落盘 |
| product_info 长期空导致六类打标签不可用 | 🔴 高 | 退化规则 R4+R3 + `svc_rule_v1_degraded`；回灌后升级 v2 |
| M3 模型大量依赖无三方源的服务质量/案例数据 | 🔴 高 | 相关模型标 Wave2 置灰；登记 Q-SVC-007 待三方补充 |
| 量级样例导致 UI 指标失真 | 🟡 中 | UI 标 ⚠️ 样例角标；不伪闭合 |

---

## 7. 附录：指标 ↔ bid 章节 ↔ DWD 字段对照全表

### 7.1 M1 基础指标（bid §4.1.1.1.1.1.1.1.4）

| bid 指标 | bid 子章节 | metric_id | DWD 表.字段 | ODS 真源 | 缺口 |
|----------|-----------|-----------|-------------|----------|------|
| 全球服务机构产业布局 | (1) | M_SVC_INDUSTRY_LAYOUT | service_org.industry_class / main_activities | dwd_org_org_product_info | G1/G2 |
| 全球服务机构分布 | (2) | M_SVC_ORG_CNT | service_org.province/city + ext.country | dwd_org_reg_info | G9 |
| 投融资动态资讯 | (3) | M_SVC_INVEST_Y | service_org_financing.amount/completion_date/industry_domain | dwd_org_financing_info / dwd_org_invest_info | G4/G5/G7 |
| 新增服务机构动态 | (4) | M_SVC_NEW_CNT | service_org.incorporation_year | dwd_org_reg_info | — |
| 深圳服务机构规模 | (5) | M_SVC_SZ_SCALE | service_org.is_shenzhen + tech_score | dwd_org_reg_info.city | G10(M3) |
| 深圳服务机构分布 | (6) | M_SVC_SZ_DISTRICT | service_org.district | dwd_org_reg_info.address | G8 |

### 7.2 M3 深度模型（bid §4.1.1.1.1.1.1.9）

| bid 模型 | bid 子章节 | model_id | 数据依赖 | 缺口 |
|----------|-----------|----------|----------|------|
| 服务链短板分析 | §9.1 | SVC_SERVICE_CHAIN_GAP | service_org + 服务质量数据 | G10/G11；Q061 |
| 服务关系链 | §9.2 | SVC_SERVICE_RELATION_CHAIN | Nebula gkx_service + 关系数据 | Q062 |
| 金融服务机构技术力 | §9.3 | SVC_FINANCE_TECH_POWER | service_org(type=1) + 财务 | G10；Q060 |
| 知识产权服务机构技术力 | §9.4 | SVC_IP_TECH_POWER | service_org(type=2) + 案例 | G11；Q060 |
| 人力资源服务机构技术力 | §9.5 | SVC_HR_TECH_POWER | service_org(type=3) + 招聘/反馈 | G10；Q060 |
| 市场营销服务机构技术力 | §9.6 | SVC_MKT_TECH_POWER | service_org(type=4) + 项目案例 | G11；Q060 |
| 咨询服务机构技术力 | §9.7 | SVC_CONSULT_TECH_POWER | service_org(type=5) + 声誉 | G10/G11；Q060 |
| 科技创新服务机构技术力 | §9.8 | SVC_INNOV_TECH_POWER | service_org(type=6) + 科研合作 | G11；Q060 |
| 服务机构引入推荐 | §9.9 | SVC_ATTRACTION_RECOMMEND | service_org + 政策匹配 + 深圳连接度 | G12；Q063 |
| 服务机构培育推荐 | §9.10 | SVC_CULTIVATION_RECOMMEND | service_org + 潜力 | G12；Q063 |

---

*文档版本 v1.0.0 · human:侯佳伟 · SVC-DATA-ANALYSIS-L01 · 2026-08-05*
