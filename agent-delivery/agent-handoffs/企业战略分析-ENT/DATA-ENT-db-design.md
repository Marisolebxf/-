# Data handoff：DATA-ENT-db-design

- 时间：2026-06-18
- 作者：data-agent（资深数据工程师 + 数据架构师）
- 支撑基线：`ENT-functional-design-v2.md`（v2.1.0，18 验收点 E-20~E-37）
- commit 标记建议：`[agent:data] ENT 企业域数据库设计 v1（DWD9+ADS13+cfg_metric49+Nebula6/8）`

## 产物清单

| 产物 | 绝对路径 | 行数 |
|------|---------|------|
| 主设计文档 | `e:\gkx_src\agent-delivery\data\企业域数据库设计(v1).md` | 约 690 |
| demo 对比报告 | `e:\gkx_src\agent-delivery\data\企业域-DB设计-vs-demo对比.md` | 约 200 |
| 总纲引用指针（追加） | `e:\gkx_src\agent-delivery\数据库设计.md` §2.2（+1 行，未删改） | —— |
| 本 handoff | `e:\gkx_src\agent-delivery\agent-handoffs\DATA-ENT-db-design.md` | 本文件 |
| cfg_metric 真源（已存在，复用） | `e:\gkx_src\agent-delivery\metrics\cfg_metric-ENT-seed.yaml` | 49 条 |

## 新增/变更表（22 张表 + 2 配置表 + 图谱）

**DWD（gkx_dwd，9 张）**：enterprise / enterprise_finance_history / enterprise_patent_history / enterprise_parent_subsidiary / enterprise_supply_chain / enterprise_industry / enterprise_cooperation / enterprise_business_tag / enterprise_news

**ADS（ads，13 张）**：ent_overview / ent_panorama / ent_star / ent_shenzhen / ent_map_layer / ent_type_dist / ent_domain_cover / ent_capability / ent_sz_status / ent_recommend / ent_supply_chain / ent_painpoint / ent_competitiveness

**cfg（gkx_cfg，2 张）**：cfg_metric / cfg_metric_lineage

**图谱（NebulaGraph space=gkx_enterprise）**：6 Tag（enterprise/industry/research/talent/service/region）+ 8 Edge（supply/parent_sub/invest/industry_belong/research_coop/talent_coop/service_provide/cooperate）；vid=`ent:{enterprise_code}`

## ODS 真源引用（企业域）

- 国内机构：`dwd_org_reg_info`（含经纬度/上市状态，归一键 external_id）、`dwd_org_annual_financial_info`、`dwd_org_stock_base`、`dwd_org_stock_finance_info`、`dwd_org_rd_achiev_info`、`dwd_org_tag_info`、`dwd_org_shareholder_info`、`dwd_org_invest_info`、`dwd_org_industry_chain_dtl`、`dwd_org_industry_chain_pat_dtl`、`dwd_org_important_news_info`、`dwd_org_financing_info`、`dwd_org_merger_acquisition_info`
- 工商通用（量子专题）：`dwd_company_base`（归一键 credit_code）、`dwd_company_nei_code`、`dwd_company_location_tags`、`dwd_company_honor_tags`、`dwd_company_industry_tags`、`dwd_company_basic_tags`、`dwd_company_diy_tags`、`dwd_company_shareholder`、`dwd_company_branch`
- 产业链：`dwd_industry_chain_info`、`dwd_industry_code`
- 专利：`dwd_patent`、`dwd_patent_legal`、`dwd_patent_cited`
- 外资（单独处理）：`dwd_forg_base_info`

## 字段映射覆盖率

- **DWD 字段层（129 字段，源映射报告 v2 §4）**：✅ 51.5% 直接 + 🔧 40.8% 需算法 + ⚠️ 4.9% 待甲方 + ❌ 2.9% 无来源；**综合覆盖率 92.2%**（剔除 🟦 系统列）
- **metric 层（49 个 M_ENT_*）**：✅ 14（28.6%）+ 🔧 30（61.2%）+ ⚠️ 4（8.2%）+ ❌ 1（2.0%）

## metric_id 注册数

- **49 个**（全部 `M_ENT_*`，8 件套已在 `cfg_metric-ENT-seed.yaml`；本设计提供 cfg_metric/cfg_metric_lineage DDL + seed→INSERT 转换脚本约定 + 4 类样例 INSERT）
- 命名：Q009 已会签 `ENT` 为企业要素正式助记码，`M_E1_*` 降为废弃别名

## 用户态自建 DWD 表

- 本期不涉及（企业域无用户态评论/收藏；如需在用户中心域单独设计）

## Mock 数据规模建议（Python 写 ADS，前缀 mock_，seed=20260618）

- dwd.enterprise ≥1500、finance_history ≥7500、patent_history ≥7500、industry ≥2000、supply_chain ≥3000、parent_subsidiary ≥1000、cooperation ≥2500、business_tag ≥4000、news ≥2000；ADS 由 DWD 聚合派生，🔧 字段由 algorithm-agent 产出

## 字段映射登记

- 待补登 `data-source-mapping-registry.yaml`：DWD 9 张 + ADS 13 张（当前仅登记 ENT 5 条），见对比报告 §6 P3

## DQ 规则

- **15 条**（DQ-01~15）：唯一性(credit_code)、非空、参照完整、值域(经纬度/比率/枚举)、逐年唯一、cfg_metric 8 件套完整性、Mock 前缀、图谱 vid 对齐；阻断级 6 条入 CI

## 待甲方确认的开放项（12 条）

Q010 企业类型判定 / Q011 创新型企业口径 / Q012 区划精度+密度分母 / Q013 领域广深口径 / Q014 技术力商业力权重 / Q015 引育指数阈值 / Q016 对标城市集 / Q017 供应链核心阈值+断链评级 / Q018 痛难点维度 / Q019 科研人数口径 / Q020 明星企业入选规则 / K-O7 市场份额数据采购（❌ 无来源）

> 已在主设计文档 §12 登记；请 PM 整理进 `客户决策清单跟踪表.md`，UI 加 ⚠️ 角标。

## 影响下游

- **algorithm-agent**：30 个 🔧 指标需实现/对齐（demo `cfg_model_registry.yaml` 12 model 可复用，改 `M_E1_*→M_ENT_*` + 接新 DWD/ADS + 图谱中心性回写 ent_supply_chain）
- **api-agent**：13 张 ent_* 为 Java 只读契约面；cfg_metric→catalog/lineage API 支撑 ⓘ 数据说明卡；Java 禁直连 nGQL
- **ui-agent / qa-agent**：前端 Mock（topic_demo 内联）须下线，改调 Java 读 ADS；每统计数旁挂 metric_id 的 ⓘ
- **architect-agent**：schema 变更需三方会签（铁律 7）

## 架构合规自检（公约 §2）

✅ 算法只在 Python（🔧 全标 algorithm-agent）｜✅ 调用链不越层（Java 只读 ADS）｜✅ NebulaGraph 禁 Neo4j｜✅ ADS 先行+Mock 写 ADS｜✅ D9 cfg_metric 8 件套全注册可回链｜✅ 字段名沿用 ODS｜✅ 不替甲方决策（12 开放项登记）

## 给 doc-agent 的接力要点（编写《数据库设计说明书》）

- **输入产物**：① 主设计 `企业域数据库设计(v1).md`（DDL/三段映射/DQ/ER）② 对比报告（现状 vs 目标）③ `cfg_metric-ENT-seed.yaml`（指标真源）④ 映射报告 v2（逐字段血缘）⑤ 总纲 `数据库设计.md`（平台层规约）
- **章节建议**：1 概述与分层 → 2 库/Schema 规划 → 3 实体归一与主键 → 4 DWD 明细（9 表逐表）→ 5 ADS 读模型（13 表逐表，标消费页面）→ 6 cfg_metric 指标注册（D9 8 件套 + 49 清单）→ 7 NebulaGraph 图谱 → 8 ODS→DWD→ADS 三段映射与覆盖率 → 9 DQ 规则 → 10 Mock 策略 → 11 开放项 → 附录 ER 图/DDL 全量
- **注意**：DWD 9 表/ADS 13 表的完整逐字段表可由本设计 §4/§5/§13 的 DDL COMMENT 直接转表格（COMMENT 已含「映射状态 + ODS 来源」）；49 metric 清单从 seed yaml 取。
