# 企业域 DB 设计（v1）vs 现有 demo 实现 · 差异对比报告

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-ENT-DB-vs-demo-v1 |
| 版本 | v1.0.0 |
| 作者 | data-agent |
| 创建日期 | 2026-06-18 |
| 本设计 | `企业域数据库设计(v1).md`（MySQL 8 + NebulaGraph，支撑 FDS v2.1 18 验收点） |
| 对比对象 A | `E:\gkx_src\ent-analysis-demo\`（E1 企业分析算法 POC：PostgreSQL + NebulaGraph `entan`） |
| 对比对象 B | `E:\gkx_src\topic_demo\src\app\pages\enterprise\*.tsx`（前端展示原型，内联 Mock） |
| 结论摘要 | demo 是「算法 POC（A）+ 展示原型（B）」两套独立实现，均未对接真实 ODS、均无 cfg_metric 注册；本设计是首个「ODS 真源对齐 + ADS 契约 + D9 血缘」的正式库设计 |

---

## 0. 对比对象定位

| 对象 | 角色 | 引擎 | 数据来源 | 与正式仓关系 |
|------|------|------|---------|-------------|
| **A. ent-analysis-demo** | 企业分析**算法 POC** | PostgreSQL + NebulaGraph(`entan`) | DWD 自造 Mock（Python） | 算法可迁移，schema 需重构 |
| **B. topic_demo/enterprise** | 企业页面**展示原型** | 无 DB（内联 TS Mock） | 前端硬编码 camelCase | UI 可参考，数据层全部重做 |
| **C. 本设计 (v1)** | 正式库设计 | MySQL 8 + NebulaGraph(`gkx_enterprise`) | ODS 要素库 186 表 → DWD → ADS | 目标态 |

---

## 1. 表/字段层面对比

### 1.1 DWD 层

| DWD 表（本设计） | demo A 对应 | 差异 | 迁移动作 |
|------------------|-------------|------|---------|
| `dwd.enterprise`（66字段，双源归一） | `dwd.enterprise`（demo，少量字段 + `tech_transaction_amount` patch） | 🔴 字段差异大：demo 字段少、无双源归一、无经纬度/上市/资质标志位完整集 | 扩字段 + 改主键 + 接 ODS |
| `dwd.enterprise_finance_history`（13字段，逐年） | ❌ 无（demo 财务直接挂主表） | 🟢 新增历史表 | 新建 |
| `dwd.enterprise_patent_history`（逐年） | ❌ 无 | 🟢 新增 | 新建 |
| `dwd.enterprise_parent_subsidiary` | ❌ 无独立表（仅图谱边） | 🟢 新增 RDBMS 表 | 新建 |
| `dwd.enterprise_supply_chain` | ⚠️ 仅在图谱 `graph_edge` | 🟡 RDBMS 落地 + 图谱双写 | 新建 RDBMS 表 |
| `dwd.enterprise_industry` | ⚠️ 部分在 `ads.graph_membership` | 🟡 重构为标准 DWD | 新建 |
| `dwd.enterprise_cooperation` | ⚠️ 仅图谱边（research/talent/service_coop） | 🟡 RDBMS 落地 | 新建 |
| `dwd.enterprise_business_tag` | ⚠️ demo 主表 tags 字段内嵌 | 🟡 拆为标准标签表 | 新建 |
| `dwd.enterprise_news`（16字段） | ✅ `dwd.enterprise_news`（patch 已建） | 🟢 基本一致，字段名对齐 ODS | 微调字段名 |

> demo A 的 DWD 仅 1~2 张表 + 图谱边承载关系；本设计拆为 9 张标准 DWD，字段名全部沿用 ODS（demo 为自造英文短名）。

### 1.2 ADS 层

| 本设计 ADS（13张） | demo A 对应 ADS | 差异 |
|---------------------|------------------|------|
| `ads_ent_overview` | `enterprise_news_stat` / `new_enterprise_stat`（拆散） | 🟡 demo 按统计项分表，本设计按页面读模型聚合 |
| `ads_ent_type_dist` | `enterprise_type_dist` | 🟡 本设计加区域维 + 集聚指数 |
| `ads_ent_domain_cover` | `enterprise_domain_dist` | 🟡 本设计加广度/深度/多元化 |
| `ads_ent_capability` | `tech_power` + `biz_power`（两表） | 🔴 demo 技术力/商业力分两表，本设计合并逐企业读模型 |
| `ads_ent_supply_chain` | `graph_node` / `graph_edge` / `graph_membership` | 🔴 demo 用通用图三表，本设计用页面读模型 + Nebula 回写 |
| `ads_ent_recommend` | `key_enterprise`（部分） | 🟡 本设计独立招引/培育指数 |
| `ads_ent_competitiveness` | `eval_weight`（仅权重配置） | 🔴 demo 无成品竞争力表，仅存权重 |
| `ads_ent_panorama/star/shenzhen/map_layer/sz_status/painpoint` | ❌ 无 | 🟢 全新增（demo 无 A 层门户/深圳/痛难点） |
| —— | `entity_recognition`（demo 有） | 本设计并入 cooperation/图谱构建中间态，不单列 ADS |

> demo A 共 12 张 ADS 表（`eval_weight / key_enterprise / enterprise_type_dist / enterprise_domain_dist / enterprise_news_stat / new_enterprise_stat / entity_recognition / graph_node / graph_edge / graph_membership / tech_power / biz_power`），偏「算法中间结果」；本设计 13 张偏「页面读模型契约」。

### 1.3 字段命名差异（核心问题）

| 维度 | demo A (PG) | demo B (前端 Mock) | 本设计 | 结论 |
|------|-------------|---------------------|--------|------|
| 命名风格 | 自造英文短名（snake_case） | camelCase 中文义（`patentCount/rdInvestment/score`） | **严格沿用 ODS**（`patent_grant_count/rd_investment/revenue_latest`） | 🔴 三方各异，需统一到 ODS |
| JSON 列 | `text` 存 JSON 字符串 | TS 对象 | 原生 `JSON` 类型 | 🟡 PG text→MySQL JSON |
| 主键类型 | `bigserial` | 无（前端） | `BIGINT AUTO_INCREMENT` + `enterprise_code` UNIQUE | 🟡 自增策略不同 |

---

## 2. 主键与实体归一对比

| 维度 | demo A | demo B | 本设计 |
|------|--------|--------|--------|
| 物理主键 | `id bigserial` | 无（`id` 临时字符串/序号） | `id BIGINT AUTO_INCREMENT` |
| 业务键 | ❌ 无统一信用代码 | ❌ 无 | ✅ `enterprise_code`（统一社会信用代码）UNIQUE |
| 关联键 | `enterprise_id`（内部自增） | 前端对象引用 | `enterprise_id`(FK) + `enterprise_code`(冗余) |
| 实体归一 | ❌ 无双源归一 | ❌ 无 | ✅ `dwd_org_reg_info.external_id` ∪ `dwd_company_base.credit_code` |
| 图谱 vid | `ent:{id}`（内部自增，**跨批次漂移**） | —— | `ent:{enterprise_code}`（**稳定，跨批次/跨库一致**） |

> 🔴 **最关键迁移点**：demo 用内部自增 id 作图谱 vid，重灌数据后 vid 漂移、RDBMS↔图谱关联断裂；本设计改用统一社会信用代码，从根上解决稳定关联。

---

## 3. 图谱对比（NebulaGraph）

| 维度 | demo A `entan` | 本设计 `gkx_enterprise` | 差异 |
|------|----------------|--------------------------|------|
| space 名 | `entan` | `gkx_enterprise` | 🟡 重命名（总纲约定） |
| vid_type | FIXED_STRING(64) | FIXED_STRING(80) | 🟡 扩长 |
| vid 规则 | `ent:{id}` 内部自增 | `ent:{enterprise_code}` 信用代码 | 🔴 见 §2 |
| Tag | enterprise / industry / research / talent / service（5） | + region（6） | 🟢 加区域节点(支撑P1区域聚合) |
| Edge | supply / cooperate / membership 类（~5） | supply / parent_sub / invest / industry_belong / research_coop / talent_coop / service_provide / cooperate（8） | 🟢 细化母子/投资/产学研边 |
| 灌数 | `nebula_loader.py`（PG→Nebula） | 复用同模式（MySQL→Nebula） | 🟢 脚本可复用，改连接 |
| 中心性回写 | 图内算 | 回写 `ads_ent_supply_chain` 供 Java 只读 | 🟢 符合 Java 禁直连 nGQL |

> demo 图谱模型与算法（`entity.py`/`nebula_loader.py`/中心性）**可直接迁移复用**，仅需改 vid 规则 + space 名 + 数据源连接。

---

## 4. metric_id 注册对比（D9）

| 维度 | demo A | demo B | 本设计 |
|------|--------|--------|--------|
| cfg_metric 8 件套 | ❌ 无（仅 `cfg_model_registry.yaml` 算法侧 model 注册） | ❌ 无 | ✅ 49 条 `M_ENT_*` 全注册 |
| metric↔model 映射 | ✅ `metric_index`（yaml，algorithm-agent 已建） | ❌ | ✅ cfg_metric_lineage + 回链 model_id |
| metric 命名 | `M_E1_*`（旧别名） | 无 metric 概念 | `M_ENT_*`（Q009 已会签为正式码） |
| UI 数据说明卡 ⓘ | ❌ | ❌ | ✅ 经 cfg_metric→catalog API 支撑 |

> demo A 的 `cfg_model_registry.yaml` 已注册 12 个 model 覆盖 30 条 🔧 指标，**与本设计 cfg_metric 互补**（一个管口径/血缘，一个管算法实现），迁移时对齐 `M_E1_*→M_ENT_*` 即可。

---

## 5. Mock vs 真实 ODS 对比

| 维度 | demo A | demo B | 本设计 |
|------|--------|--------|--------|
| Mock 位置 | Python 写 PG dwd（合规方向对） | 前端 TS 内联（❌ 违总纲，前端造假） | Python 写 ADS，前缀 `mock_` |
| 字段对齐 ODS | ❌ 自造短名 | ❌ camelCase | ✅ 沿用 ODS（dwd_org_reg_info 等） |
| 切真实成本 | 高（字段不对齐需大改） | 极高（前端硬编码） | 低（Wave 1 换数据源零改字段） |
| 批次可追溯 | 部分 | ❌ | ✅ calc_batch_id |

---

## 6. demo → 正式仓迁移改造清单（按优先级）

| 优先级 | 改造项 | 来源 demo | 目标 | 工作量 |
|--------|--------|----------|------|--------|
| 🔴 P0 | **图谱 vid 改造**：`ent:{id}` → `ent:{enterprise_code}` | A `nebula_loader.py` | 稳定关联 | 中 |
| 🔴 P0 | **字段名对齐 ODS**：demo 自造短名/前端 camelCase → ODS 命名 | A schema + B Mock | 字段映射 | 大 |
| 🔴 P0 | **引擎迁移**：PostgreSQL → MySQL 8（bigserial→AUTO_INCREMENT，text→JSON） | A `schema_*.sql` | 总纲合规 | 中 |
| 🔴 P0 | **实体归一**：建双源归一 ETL（external_id ∪ credit_code） | 新增 | 主键统一 | 大 |
| 🟠 P1 | **cfg_metric 注册**：落 49 条 8 件套 + `M_E1_*→M_ENT_*` 改名 | A yaml | D9 合规 | 中（种子已备） |
| 🟠 P1 | **ADS 重构为页面读模型**：算法中间表 → ads_ent_* 契约表 | A 12 表 | Java 只读契约 | 大 |
| 🟠 P1 | **前端 Mock 下线**：B 内联数据 → 调 Java 读 ADS | B `*.tsx` | 调用链合规 | 大 |
| 🟡 P2 | **算法迁移复用**：ENT_WEIGHTED_SCORE/中心性等 model 接新 DWD/ADS | A `entan/` | 复用 | 中 |
| 🟡 P2 | **补 A 层门户表**：panorama/star/shenzhen/map_layer/painpoint | 新增 | 支撑 E-31~35 | 中 |
| 🟢 P3 | **DQ 入 CI**：15 条规则 | 新增 | 质量门禁 | 小 |
| 🟢 P3 | **映射登记补登**：data-source-mapping-registry 扩 DWD9+ADS13 | 扩充 | 血缘完整 | 小 |

---

## 7. 关键结论（3-5 条）

1. **demo 是两套独立 POC（算法 A + 展示 B），均未对接真实 ODS、均无 cfg_metric 注册**；本设计是首个端到端正式库设计（ODS→DWD→ADS→图谱 + D9 血缘）。
2. **最高优先迁移点是图谱 vid 与字段命名**：demo 用内部自增 id 作 vid（跨批次漂移）+ 自造/前端 camelCase 字段，本设计统一到「统一社会信用代码 + ODS 字段名」，从根上保证稳定可追溯。
3. **算法与图谱可大量复用**：demo A 的 12 个 model（`cfg_model_registry.yaml`）+ 图谱构建脚本可迁移，仅需对齐 `M_E1_*→M_ENT_*`、改 vid/space/数据源连接。
4. **ADS 定位需翻转**：demo ADS 是「算法中间结果」，本设计 ADS 是「页面读模型契约（Java 只读）」，需按 13 个页面读模型重构。
5. **前端 Mock 必须下线**：demo B 前端内联造假违反总纲（前端禁造假/调用链越层），改为 Python 写 ADS + Java 只读。

---

## 附录 · demo 文件索引

| demo | 关键文件 |
|------|---------|
| A schema | `ent-analysis-demo/scripts/schema_ads.sql`、`schema_dwd_patch.sql` |
| A 图谱/算法 | `ent-analysis-demo/entan/graph/{entity.py,nebula_loader.py}`、`entan/metrics/registry.py` |
| A 算法注册 | `ent-analysis-demo/conf/cfg_model_registry.yaml` |
| A 详设 | `ent-analysis-demo/docs/企业算法demo详细设计文档.md` |
| B 前端 | `topic_demo/src/app/pages/enterprise/{EnterpriseOverview,SupplyChainAnalysis,...}.tsx` |
