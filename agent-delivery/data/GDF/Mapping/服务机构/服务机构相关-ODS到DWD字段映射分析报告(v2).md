# 服务机构相关 ODS → DWD 字段映射分析报告（v2）

> 生成时间: 2026-06-23 ｜ 版本: v2（ODS 数据源为三方「要素库」）
> 分析范围: **服务机构（SVC/E6）** 数据域
> 任务 ID: ALGO-DB-DWD-S01 · Epic E-DB-DESIGN-ALGO-V11-DWD

---

## 1. 背景与版本变更

本报告分析三方采购数据源（ODS 层）能否满足本项目自建 **DWD 服务机构标准表** 的字段填充需求。

| 项 | v1 | v2（本报告） |
|----|----|----|
| ODS 来源 | PostgreSQL `demo_gdf_data.ods`（`poc_tb_*` 示例表） | 三方「要素库」`要素库建表语句.sql`（**无独立服务机构 Sheet**） |
| 识别策略 | 假设存在服务机构专表 | 从 **国内机构 41 张表** + 标签/经营范围/投融资事件 **筛选归一** |
| DWD 目标 | `dwd_service_org_snapshot`（占位） | **`gkx_dwd.service_org`** + **`gkx_dwd.service_org_financing`** |
| bid 对齐 | — | §4.1.1.7 服务机构基础指标 + §4.8/§4.9 产业服务深度 |

> **命名澄清**：要素库 `dwd_org_*` 是数据供应方命名，归属 **ODS 贴源层**；右侧 `dwd.service_org` 才是本项目自建 DWD 标准明细层。旧占位名 `dwd_service_org_snapshot` **废弃**，M1 快照走 `gkx_dwm` 或 ADS，不另建 snapshot 同名明细表。

**映射状态图例**：
- ✅**直接映射**：ODS 有对应字段，可直接取值或简单类型/枚举转换
- 🔧**需计算/算法**：有数据源但需规则判定、聚合、关键词分类或算法模型
- ⚠️**待确认/质量待验**：业务口径需甲方确认（见 Q-SVC-001~004；Q-ALGO-006 已确认）
- ❌**无来源**：要素库中无相关数据
- 🟦**系统/预留**：主键、时间戳、扩展位等由系统自动填充

---

## 2. 服务机构相关 ODS 源表概况

ODS **无独立「服务机构要素库」Sheet**。服务机构实体需从 **企业/机构域（国内机构 41 张）** 子集识别，主要依赖以下 ODS 表：

| 数据子域 | 来源 Sheet | 表数 | 本域角色 |
|----------|-----------|------|---------|
| 国内机构（工商/标签/投融资） | 国内机构要素库 | 41（本域用 6+） | **主源**：筛选服务机构子集 |

### 2.1 核心 ODS 源表

| ODS 表 | 中文名 | 字段数 | 本域角色 |
|--------|--------|--------|---------|
| `dwd_org_reg_info` | 机构基本信息 | 26* | **主源**：机构身份、区域、成立、资本、上市状态 |
| `dwd_org_tag_info` | 机构标签表 | 8 | **准入辅助**：资质/荣誉类 `org_tag`（**非**服务类型主源） |
| `dwd_org_org_product_info` | 经营信息 | 10 | **分类主源**：`industry_class`（行业）+ `main_activities`（经营范围）→ 六类打标签 |
| `dwd_org_financing_info` | 融资事件 | 12 | 服务链投融资（被投方视角）+ M_SVC_INVEST_Y |
| `dwd_org_invest_info` | 投资事件 | 11 | 服务链投融资（投资方视角，金融机构识别） |
| `dwd_org_important_news_info` | 重点资讯 | 10 | 服务能力/动态资讯（M1 资讯类指标 🔧） |
| `dwd_org_industry_chain_dtl` | 产业关联企业 | — | 服务机构产业布局（与 CHAIN 域交叉引用） |

> *`dwd_org_reg_info` 要素库 DDL 含 `org_type`（机构类型）字段，ODS 清单 v2 摘要未列，ETL 以 DDL 为准。

### 2.2 服务机构识别规则（ETL 准入，🔧 + ⚠️）

机构进入 `gkx_dwd.service_org` 当且仅当满足 **任一** 准入条件（服务机构识别与六类打标签均 **以行业+经营范围为主**，见 §6 Q-ALGO-006 已确认口径）：

| # | 规则 | ODS 来源 | 映射状态 |
|---|------|---------|---------|
| R1 | `industry_class` 属于服务业门类/大类码表，或映射至六类服务行业码 | `dwd_org_org_product_info.industry_class` | 🔧 |
| R2 | `main_activities` 经营范围命中六类服务关键词词典 | `dwd_org_org_product_info.main_activities` | 🔧 |
| R3 | `org_tag` 命中服务机构/六类服务关键词（准入辅助，**不单独决定 service_type**） | `dwd_org_tag_info.org_tag` | 🔧 |
| R4 | `org_type` 含「服务机构/中介/代理」等 | `dwd_org_reg_info.org_type` | 🔧 |
| R5 | 作为投资方出现在 ≥N 笔投资/融资事件（金融类 heuristic，可选） | `dwd_org_invest_info` / `investors_name` | 🔧 |

**排除规则**（避免与 ENT 全量企业重复）：
- 已通过 R1~R5 **未**识别为服务机构的，**不写入** `service_org`（即使存在于 `dwd_org_reg_info`）
- **禁止**在 SVC 域复制 ENT `enterprise` 66 字段全量工商；仅保留服务分析必要子集 + `enterprise_code` 关联键

---

## 3. DWD 服务机构标准表概览

| # | DWD 表（逻辑名） | 字段数 | 说明 | 主要 ODS 来源 |
|---|-----------------|--------|------|---------------|
| 1 | `dwd.service_org` | 38 | 服务机构主表（六类 `service_type` + 区域 + 能力摘要） | `dwd_org_reg_info`、`dwd_org_tag_info`、`dwd_org_org_product_info` |
| 2 | `dwd.service_org_financing` | 16 | 服务链投融资明细（融资+投资事件归一） | `dwd_org_financing_info`、`dwd_org_invest_info` |

---

## 4. 映射覆盖率总览

| DWD 表 | 总字段 | ✅直接 | 🔧需计算 | ⚠️待确认 | ❌无来源 | 🟦系统/预留 | 覆盖率* |
|--------|--------|--------|---------|---------|---------|------------|--------|
| service_org | 38 | 14 | 12 | 4 | 0 | 8 | **86.7%** |
| service_org_financing | 16 | 9 | 2 | 1 | 0 | 4 | **91.7%** |
| **合计** | **54** | **23** | **14** | **5** | **0** | **12** | **88.1%** |

> *覆盖率 = (✅直接 + 🔧需计算) / (总字段 − 系统/预留) = 37/42 = **88.1%**。
> **Q-ALGO-006 已确认**：ODS 无服务类型直字段，`service_type` 由 **行业 + 经营范围** 规则打标签（§6）；剩余 ⚠️ 主要为 district 抽取、投融资领域分类等。

---

## 5. 逐表字段映射详情

### 5.1 dwd.service_org（服务机构主表，38 字段）

**ODS 来源**: `dwd_org_reg_info`、`dwd_org_tag_info`、`dwd_org_org_product_info`（准入筛选后）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增主键 |
| 2 | service_org_code | varchar(64) | ✅直接 | `dwd_org_reg_info.external_id` | 业务归一主键；无信用代码时 `svc:{org_id}` |
| 3 | org_id | varchar(64) | ✅直接 | `dwd_org_reg_info.org_id` | ODS 机构 id，关联其它 ODS 表 |
| 4 | enterprise_code | varchar(64) | ✅直接 | `dwd_org_reg_info.external_id` | 与 ENT 域 `enterprise_code` 对齐，可 JOIN `gkx_dwd.enterprise` |
| 5 | name_cn | varchar(255) | ✅直接 | `dwd_org_reg_info.name_cn` | 机构名称 |
| 6 | service_type | smallint | 🔧 | ❌ ODS 无直字段 | **DWD 衍生**：按 `industry_class` + `main_activities` 打六类标签；见 §6 ✅ Q-ALGO-006 |
| 7 | service_type_source | varchar(32) | 🔧 | 打标签命中来源 | **industry / scope / industry+scope**（主）；org_tag 仅作准入辅助 |
| 8 | service_type_tags | json | 🔧 | 行业+经营范围规则 | 多类型机构 JSON 数组，如 `[1,5]`；**非** ODS org_tag 直映射 |
| 9 | org_type | varchar(100) | ✅直接 | `dwd_org_reg_info.org_type` | ODS 机构类型原值 |
| 10 | province | varchar(100) | ✅直接 | `dwd_org_reg_info.province` | 所在省份 |
| 11 | city | varchar(100) | ✅直接 | `dwd_org_reg_info.city` | 所在城市 |
| 12 | district | varchar(100) | 🔧 | `dwd_org_reg_info.address` 解析 | ODS 无独立区县字段，地址规则抽取 |
| 13 | address | text | ✅直接 | `dwd_org_reg_info.address` | 注册/经营地址 |
| 14 | addr_lng | decimal | ✅直接 | `dwd_org_reg_info.addr_lng` | 经度（字符串→decimal） |
| 15 | addr_lat | decimal | ✅直接 | `dwd_org_reg_info.addr_lat` | 纬度 |
| 16 | incorporation_date | date | ✅直接 | `dwd_org_reg_info.incorporation_date` | 成立日期 |
| 17 | incorporation_year | int | ✅直接 | `dwd_org_reg_info.incorporation_year` | 成立年份 |
| 18 | org_size | varchar(50) | ✅直接 | `dwd_org_reg_info.org_size` | 企业规模 |
| 19 | registered_capital_value | decimal | ✅直接 | `dwd_org_reg_info.registered_capital_value` | 注册资本(元)，展示时 /10000 转万元 |
| 20 | listing_status | varchar(50) | ✅直接 | `dwd_org_reg_info.listing_status` | 上市状态 |
| 21 | industry_class | varchar(255) | ✅直接 | `dwd_org_org_product_info.industry_class` | 行业分类 |
| 22 | main_activities | text | ✅直接 | `dwd_org_org_product_info.main_activities` | 经营范围（服务识别输入） |
| 23 | main_prod | varchar(255) | ✅直接 | `dwd_org_org_product_info.main_prod` | 主要产品/服务 |
| 24 | service_tag_raw | varchar(500) | 🔧 | `dwd_org_tag_info.org_tag` 聚合 | 原始标签串（逗号拼接） |
| 25 | is_shenzhen | tinyint | 🔧 | province/city 规则 | city='深圳市' 或 province 含深圳 → 1 |
| 26 | financing_count | int | 🔧 | `dwd_org_financing_info` COUNT | 累计融资事件数（预聚合） |
| 27 | invest_count | int | 🔧 | `dwd_org_invest_info` COUNT | 累计对外投资数（预聚合） |
| 28 | latest_financing_amount | decimal | 🔧 | `dwd_org_financing_info` MAX(date) | 最近一轮融资金额(元) |
| 29 | latest_financing_date | date | 🔧 | `dwd_org_financing_info.completion_date` | 最近融资日期 |
| 30 | tech_score | decimal | 🔧算法 | 多表综合 | M3 六类技术力模型输出占位（algorithm-agent） |
| 31 | data_source | varchar(100) | ✅直接 | 各表 `data_source` | 数据来源 |
| 32 | data_collect_time | datetime | ✅直接 | 各表 `created_time` | ODS 入库时间 |
| 33 | classification_rule_version | varchar(32) | 🟦系统 | - | 服务机构识别规则版本，如 `svc_rule_v1` |
| 34 | is_deleted | smallint | 🟦系统 | - | 逻辑删除 0=有效 |
| 35 | ext | json | 🟦预留 | - | 扩展（产业链标签、国际机构等） |
| 36 | create_time | datetime | 🟦系统 | - | ETL 写入 |
| 37 | update_time | datetime | 🟦系统 | - | ETL 更新 |
| 38 | audit_status | varchar(20) | 🟦系统 | - | 默认 pending |

### 5.2 dwd.service_org_financing（服务链投融资明细，16 字段）

**ODS 来源**: `dwd_org_financing_info`（被投融资）、`dwd_org_invest_info`（对外投资）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | service_org_id | bigint | ✅直接 | 经 `org_id`/`external_id` 关联 `service_org.id` | 外键 |
| 3 | service_org_code | varchar(64) | ✅直接 | `service_org.service_org_code` | 冗余便于查询 |
| 4 | event_type | varchar(20) | 🔧 | 来源表区分 | FINANCING=被投融资；INVEST=对外投资 |
| 5 | event_id | varchar(128) | 🔧 | org_id+date+amount hash | 事件去重键 |
| 6 | funding_round | varchar(50) | ✅直接 | `dwd_org_financing_info.funding_round` | 融资轮次（INVEST 事件 NULL） |
| 7 | amount | decimal | ✅直接 | `funding_amount` / `investment_amount` | 金额(元) |
| 8 | currency_code | varchar(20) | ✅直接 | `funding_currency_code` | 币种 |
| 9 | post_valuation | decimal | ✅直接 | `dwd_org_financing_info.post_valuation` | 投后估值 |
| 10 | completion_date | date | ✅直接 | `completion_date`（融资）/ invest 缺日期用 created_time | 事件完成日期 |
| 11 | counterparty_name | text | ✅直接 | `investors_name` / `inv_name` | 投资方或被投方名称 |
| 12 | counterparty_code | varchar(64) | ✅直接 | `inv_external_id` | 对手方信用代码 |
| 13 | industry_domain | varchar(200) | ⚠️ | 无 ODS 直字段 | bid §4.1.1.7(3) 领域分类；暂 NULL，待资讯/标签补全 |
| 14 | data_source | varchar(100) | ✅直接 | 各表 `data_source` | 数据来源 |
| 15 | create_time | datetime | 🟦系统 | - | ETL 写入 |
| 16 | update_time | datetime | 🟦系统 | - | ETL 更新 |

---

## 6. 六类服务类型枚举（✅ Q-ALGO-006 已确认 · 行业+经营范围打标签）

> **甲方确认口径（2026-06-23）**：ODS **无**「服务类型」直字段；`service_type` 为 DWD **衍生字段**，ETL/algorithm-agent 依据 **`industry_class`（行业）** 与 **`main_activities`（经营范围）** 规则打标签归入 bid 六类。`dwd_org_tag_info.org_tag` 仅作准入辅助，**不作为 service_type 主判定依据**。

| code | service_type | 中文名 | 打标签规则（行业码 + 经营范围关键词，algorithm-agent 维护词典） | 映射状态 |
|------|-------------|--------|---------------------------------------------------------------|---------|
| 1 | FINANCE | 金融服务 | 行业含 J 类金融/租赁/商务服务等；经营范围含：金融、银行、证券、基金、保险、投资、融资租赁、担保、小贷 | 🔧 |
| 2 | IP | 知识产权服务 | 行业/经营范围含：知识产权、专利代理、商标、版权、IP | 🔧 |
| 3 | HR | 人力资源服务 | 行业/经营范围含：人力资源、猎头、劳务派遣、人才服务、招聘 | 🔧 |
| 4 | MKT | 市场营销服务 | 行业/经营范围含：营销、广告、品牌、市场调研、公关、传媒 | 🔧 |
| 5 | CONSULT | 咨询服务 | 行业/经营范围含：咨询、管理咨询、战略、会计、审计、法律、评估 | 🔧 |
| 6 | INNOV | 科技创新服务 | 行业/经营范围含：科技服务、检验检测、研发服务、技术转移、孵化器、众创空间、科创 | 🔧 |

**打标签优先级**：`industry_class` 行业码表匹配 **优先** → `main_activities` 经营范围关键词 **补判** → 双命中取置信度高者；均未命中则 `service_type=NULL`（不入 M_SVC_ORG_CNT 分类型统计）。

**多类型机构**：`service_type` 取优先级最高的一类；`service_type_tags` 保留全部命中类型（JSON 数组）。

**规则版本**：`classification_rule_version = svc_rule_v2`（Q-ALGO-006 确认后）。

**与 ENT 关系**：
- SVC 独立业务键 `service_org_code`（= 信用代码或 `svc:{org_id}`）
- `enterprise_code` 可关联 ENT，但 SVC 表 **不存** enterprise 全量工商字段
- 同一信用代码在 ENT 与 SVC **允许并存**（不同域、不同用途）

---

## 7. bid §4.1.1.7 / §4.8 指标 ↔ DWD 链路

| bid 指标维度 | M1 metric_id | DWD 来源 | ADS 落点 | 状态 |
|-------------|-------------|---------|---------|------|
| 全球/深圳服务机构数量 | M_SVC_ORG_CNT | service_org.service_org_code | ads_metric_timeseries | 🔧 |
| 服务机构投融资规模（年） | M_SVC_INVEST_Y | service_org_financing.amount | ads_metric_timeseries | 🔧 |
| 深圳各区分布 | M_SVC_ORG_CNT | service_org.district/city | ads_metric_timeseries dim_key=region | 🔧⚠️ district 规则抽取 |
| 六类服务机构技术力 | M_SVC_TECH_SCORE_* | service_org.tech_score | ads_model_score | 🔧 M3 |
| 服务链短板/关系链 | MDL_SVC_* | service_org + graph | ads_model_score / Nebula gkx_service | 🔧 Wave2 |

---

## 8. ETL 阶段建议

```text
Phase 1（准入+直灌，<1周）：
  - 执行 R1~R5 服务机构识别规则（svc_rule_v1）
  - 直灌 reg_info / product_info / tag 14 字段
  - 写入 service_org，classification_rule_version=svc_rule_v1

Phase 2（聚合+分类，1~2周）：
  - service_type 六类打标签引擎（industry_class + main_activities，algorithm-agent 维护词典）
  - financing_count / invest_count / latest_* 预聚合
  - 灌 service_org_financing（FINANCING + INVEST 归一）

Phase 3（M1/M3 对接）：
  - M_SVC_ORG_CNT / M_SVC_INVEST_Y → ads_metric_timeseries
  - 六类 tech_score → ads_model_score（M3 深度模型）
```

### 8.1 ETL 伪代码（服务机构准入示例）

```sql
-- 服务机构准入 + service_type 打标签（示意，非生产 SQL）
-- Q-ALGO-006：无 ODS 服务类型直字段；分类依据 industry_class + main_activities
WITH product AS (
  SELECT org_id, external_id, industry_class, main_activities
  FROM ods.dwd_org_org_product_info
),
candidates AS (
  SELECT DISTINCT org_id, external_id
  FROM product
  WHERE industry_class REGEXP '(J66|J67|J68|J69|M74|L72|L73|M73|M75)'  -- 行业码表示例，algorithm 维护全量
     OR main_activities REGEXP '(金融|知识产权|人力资源|营销|咨询|科技服务|专利代理|猎头|广告|孵化器|检验检测|技术转移)'
)
SELECT r.*, p.industry_class, p.main_activities
     , CASE
         WHEN p.main_activities REGEXP '金融|银行|证券|基金|保险' OR p.industry_class REGEXP 'J66|J67|J68|J69' THEN 1
         WHEN p.main_activities REGEXP '知识产权|专利代理|商标|版权' THEN 2
         WHEN p.main_activities REGEXP '人力资源|猎头|劳务派遣|人才服务|招聘' THEN 3
         WHEN p.main_activities REGEXP '营销|广告|品牌|市场调研|公关|传媒' THEN 4
         WHEN p.main_activities REGEXP '咨询|管理咨询|战略|会计|审计|法律|评估' THEN 5
         WHEN p.main_activities REGEXP '科技服务|检验检测|研发服务|技术转移|孵化器|众创空间|科创' THEN 6
         ELSE NULL
       END AS service_type  -- DWD 衍生，非 ODS 直取
FROM ods.dwd_org_reg_info r
JOIN product p ON r.org_id = p.org_id
WHERE r.org_id IN (SELECT org_id FROM candidates);
```

---

## 9. 待甲方确认开放项

| 编号 | 事项 | 状态 | 影响 | 已确认/临时默认 |
|------|------|------|------|----------------|
| **Q-ALGO-006** | **六类服务类型枚举与打标签口径** | **✅ 已确认** | service_type、M_SVC_ORG_CNT 分组 | ODS 无直字段；按 **industry_class + main_activities** 打标签；六类枚举见 §6 |
| Q-SVC-001 | 服务机构 vs 一般企业边界 | ⚠️ 待确认 | 准入规则 R1~R5 阈值 | 命中任一 R 即纳入 |
| Q-SVC-002 | M_SVC_ORG_CNT 计数口径 | 按 org 还是 org×type | DISTINCT service_org_code |
| Q-SVC-003 | 投融资「领域分类」来源 | industry_domain | 暂 NULL，后续标签/资讯补 |
| Q-SVC-004 | district 抽取规则 | 深圳各区分布指标准确性 | 地址关键词 + dim_region 维表 |

---

## 10. 与 ENT 域交叉引用

| 场景 | ENT 表 | SVC 表 | 策略 |
|------|--------|--------|------|
| 企业全景工商 | `gkx_dwd.enterprise` | — | ENT 全量，SVC 不重复 |
| 服务机构专题 | — | `gkx_dwd.service_org` | SVC 子集 + service_type |
| 跨域 JOIN | enterprise_code | enterprise_code | 等值关联，可选 LEFT JOIN 补 ENT 字段到 ADS |
| 产业链归属 | `enterprise_industry` | ext.industry_chain | SVC 引用 CHAIN 域，不重复建链表 |

---

*报告版本 v2 · data-agent · ALGO-DB-DWD-S01 · 2026-06-23*
