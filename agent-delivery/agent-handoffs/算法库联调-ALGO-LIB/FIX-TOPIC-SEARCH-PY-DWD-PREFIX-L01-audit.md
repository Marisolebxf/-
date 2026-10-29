# FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01 审计记录

> 日期：2026-08-03  
> 范围：`demo-svc-topic-py` / `gkx_search_service` / DWD 表名字段与 Mock 兜底路径  
> 执行：agent:data-agent  
> 监管：human:徐滕强

## 1. 审计结论

当前问题不是单纯的 `dwd_` 表名前缀错误，也不是单纯 Mock 开关问题，而是三类问题叠加：

1. **数据访问层未按“Model/Repository”方式落地**：代码里有少量 dataclass model，但 DWD 业务表主要仍在 view 中手写 SQL。
2. **连接池设计未真正生效**：`gkx_common/db.py` 写了 `dbutils.PooledDB`，但 `requirements.txt` 未声明 `dbutils`，运行时会降级为 pymysql 直连。
3. **设计文档、真实 MySQL、代码 SQL 三方漂移**：部分表只是 `dwd_` 前缀错；部分表字段也漂移；少数表在真实库缺失或语义不明，不能擅自映射。

本审计不修改业务代码，只给出差异分级。

## 2. 数据访问层现状

### 2.1 已有 Model 覆盖范围

代码文件：`${GKX_ROOT}/repos/demo-svc-topic-py/gkx_common/models.py`

已定义 dataclass：

- `CodeRegion` → `gkxlumenx_dim.code_region`
- `TagDict` → `gkxlumenx_dwd.tag_dict`
- `TechDomain` → `gkxlumenx_dim.tech_domain`
- `ChainInfo` → `gkxlumenx_dwd.chain`
- `ChainNode` → `gkxlumenx_dwd.chain_node`
- `SzCityBenchmark` → 审计时真实表为 `gkxlumenx_dwd.dwd_sz_city_benchmark`；human 决策后的目标表为 `gkxlumenx_dwd.sz_city_benchmark`
- `CodeNic` → `gkxlumenx_dim.code_nic`
- `RegionScope` → `gkxlumenx_dim.region_scope`

未定义 Model/Repository 的高风险表：

- `enterprise_patent_detail`
- `enterprise_patent_history`
- `enterprise_invest`
- `enterprise_region_summary`
- `enterprise_industry_distribution`
- `enterprise_growth_trend`
- `enterprise_industry_summary`
- `enterprise_stat_summary`
- `enterprise_type_scale_stats`
- `enterprise_risk_summary`
- `risk_*`
- `shenzhen_enterprise_summary`
- `enterprise_distribution`

### 2.2 查询层现状

`gkx_common/db.py` 提供了统一 `query()` / `query_one()`，但本质仍是“传 SQL 字符串”：

- 没有 ORM / Django model / SQLAlchemy model。
- 没有集中 schema 映射。
- 没有字段存在性校验。
- view 层仍直接拼写表名和字段。

### 2.3 连接池问题

初版审计曾记录“`requirements.txt` 未声明 DBUtils”，该结论经复核不准确，修正如下：

- 修改前 `requirements.txt` 已有 `DBUtils>=3.1.0`，原 PooledDB 具备安装条件。
- 但原实现仍只有 `query(sql, params)`，不具备 Model/Repository 能力。
- 2026-08-03 经 human:徐滕强确认，访问层技术选型定为 **SQLAlchemy 2.x ORM + QueuePool**。

当前已完成的阶段 1 基础：

- `requirements.txt`：`SQLAlchemy==2.0.51`
- `gkx_common/db.py`：进程级 Engine、QueuePool、只读 Session、遗留 SQL 共享同一连接池
- `gkx_common/orm_models.py`：按 2026-08-03 真实 MySQL 字段建立首批模型
- `gkx_common/repositories/base.py`：只读 Repository 基类
- 公网实测：`QueuePool(size=20)`；ORM 与遗留 SQL 均可通过同一池读取 MySQL

## 3. 手写 SQL 分布

粗略扫描 `gkx_search_service/views`，SQL/查询相关引用约 154 处，集中在：

| 文件 | 风险说明 |
|---|---|
| `enterprise_overview.py` | SQL 最集中；表名前缀错 + 多处字段名与真实库不一致 |
| `enterprise_key_enterprise.py` | `dwd_` 前缀错；字段大体可映射 |
| `enterprise_risk.py` | 18 类风险表名前缀错；字段与真实库存在较大漂移 |
| `enterprise_shenzhen.py` | 依赖 `shenzhen_enterprise_summary`，真实库缺表 |
| `enterprise_profile.py` | 专利明细表名前缀错；字段严重漂移 |
| `enterprise_detail_supply.py` | 对外投资表名前缀错；字段漂移 |
| `enterprise_detail_patent.py` | 专利趋势表名前缀错；字段漂移 |
| `enterprise_distribution.py` | 依赖 `enterprise_distribution` 语义表；设计和真实库均未找到 |
| `enterprise_star_enterprise.py` | `dwd_enterprise_stat_summary` 前缀错 |
| `meta.py` | 码表查询基本集中，但仍混有固定枚举 |

## 4. 真实库连接

本地公网连接：

- MySQL：`111.198.38.90:34306`
- 用户：`gkxlumenx`
- 库：`gkxlumenx_dwd`

K8s 内网配置仍为：

- MySQL：`10.50.11.76:3306`

ES 本地公网测试地址：

- HTTP：`http://111.198.38.90:34392/`
- Transport：`34393`
- 用户：`elastic`

## 5. 表级差异分级

### 5.1 可归类为“表名前缀错误”的表

这些表在设计文档和真实库中均存在无 `dwd_` 前缀版本，代码当前多写了 `dwd_`。

| 代码表名 | 真实库表名 | 涉及文件 | 风险级别 |
|---|---|---|---|
| `dwd_enterprise_invest` | `enterprise_invest` | `enterprise_detail_supply.py` | 表名可修，但字段需再确认 |
| `dwd_enterprise_patent_history` | `enterprise_patent_history` | `enterprise_detail_patent.py` | 表名可修，但字段需再确认 |
| `dwd_enterprise_patent_detail` | `enterprise_patent_detail` | `enterprise_profile.py` | 表名可修，字段严重不一致 |
| `dwd_enterprise_stat_summary` | `enterprise_stat_summary` | `enterprise_key_enterprise.py`, `enterprise_star_enterprise.py` | 表名可修 |
| `dwd_enterprise_type_scale_stats` | `enterprise_type_scale_stats` | `enterprise_key_enterprise.py` | 表名可修 |
| `dwd_enterprise_region_summary` | `enterprise_region_summary` | `enterprise_overview.py` | 表名可修，字段不一致 |
| `dwd_enterprise_industry_distribution` | `enterprise_industry_distribution` | `enterprise_overview.py` | 表名可修，字段不一致 |
| `dwd_enterprise_growth_trend` | `enterprise_growth_trend` | `enterprise_overview.py` | 表名可修，字段不一致 |
| `dwd_enterprise_industry_summary` | `enterprise_industry_summary` | `enterprise_overview.py` | 表名可修，字段不一致 |
| `dwd_enterprise_risk_summary` | `enterprise_risk_summary` | `enterprise_risk.py` | 表名可修 |
| `dwd_risk_*` | `risk_*` | `enterprise_risk.py` | 表名可修，字段不一致 |

### 5.2 表存在但字段与代码不一致

#### `enterprise_patent_detail`

真实库字段：

`id, org_id, patent_id, patent_name, patent_type, filing_date, publish_date, legal_status, ipc_code, create_time, update_time`

代码字段：

`patent_id, publication_number, title_zh, title_en, abstract_zh, patent_type, country, filing_date, filing_year, publication_date, publication_year, grant_date, grant_year, grant_number, ipc_main, cpc_main, inventor, applicant_name, assignee_name, legal_status, citation_count, cited_by_count`

设计文档字段：28 字段富模型，与代码接近，但与真实库不一致。

结论：不能只改表名。需要在“按真实库精简字段适配代码”与“按设计补齐 DWD 表字段”之间选一个方向。

#### `enterprise_patent_history`

真实库字段：

`id, org_id, data_year, patent_apply_count, patent_grant_count, patent_valid_count, patent_citation_count, create_time, update_time`

代码字段额外需要：

`patent_invention_count, latest_patent_date, latest_grant_date`

结论：表名可修，但字段仍会报错。

#### `enterprise_invest`

真实库字段：

`id, org_id, inv_org_id, inv_org_name, invest_amount, invest_ratio, event_date, create_time, update_time`

代码字段：

`inv_org_id, inv_name, inv_external_id, investment_amount, investment_ratio, data_source`

结论：表名可修，但字段名和返回字段需确认映射。

#### `enterprise_region_summary`

真实库字段：

`id, region_code, region_name, stat_year, enterprise_total, new_count, active_count, output_value, stat_date, create_time, update_time`

代码字段：

`region_id, region_name, enterprise_total, new_enterprise_count, active_enterprise_count, total_revenue, region_type, parent_region_id`

设计文档字段：

`region_id, region_name, region_type, parent_region_id, stat_date, enterprise_total, new_enterprise_count, active_enterprise_count, total_revenue`

结论：真实库与设计/代码不一致，且缺 `region_type` / `parent_region_id`，区域热力查询无法按原设计执行。

#### `enterprise_industry_distribution`

真实库字段：

`id, region_code, chain_code, chain_name, enterprise_count, ratio, stat_date, create_time, update_time`

设计文档字段：

`id, region_id, chain_code, chain_name, enterprise_count, stat_date, create_time, update_time`

结论：真实库是设计表的变体，可用于产业分布饼图；不能替代 `enterprise_distribution` 四维地图热力表。

#### `enterprise_growth_trend`

真实库字段：

`id, region_code, stat_month, new_count, cumulative_count, stat_date, create_time, update_time`

代码字段：

`stat_year, stat_month, new_enterprise_count`

设计文档字段：

`region_id, stat_year, stat_month, stat_date, new_enterprise_count`

结论：真实库与设计/代码不一致，需确认 `stat_month` 是否为 `YYYY-MM` 或月份编码，以及是否用 `new_count` 映射 `new_enterprise_count`。

#### `enterprise_industry_summary`

真实库字段：

`id, chain_code, chain_name, stat_year, enterprise_count, high_tech_count, rd_staff_total, patent_total, revenue_total, stat_date, create_time, update_time`

代码字段：

`enterprise_count, research_staff_total, patent_total, high_tech_count`

结论：`research_staff_total` 与 `rd_staff_total` 字段名不一致。

#### `risk_*`

真实库样例：

- `risk_judicial_case`：`id, org_id, org_name, case_no, case_title, case_type, amount, court, event_date, status, create_time, update_time`
- `risk_lawsuit_party`：`id, case_id, org_id, party_name, party_role, create_time`

代码配置里使用富字段：

- `case_id, case_no, case_title, case_type_tag, case_cause, case_role, current_procedure, procedure_date, is_history`
- party 表还要求 `is_history`
- 多类表使用不同 `join_field`，如 `judgment_doc_id`、`case_unique_id`、`notice_id`

结论：风险表不是只改前缀即可。真实库是精简字段体系，代码按设计富字段体系写，需要统一口径。

### 5.3 表缺失或语义不明

#### `dwd_enterprise_distribution` / `enterprise_distribution`

代码用途：四维度地图热力图（global / national / regional / city）。

代码期待字段：

`dimension, region_type, parent_region_id, region_id, region_name, enterprise_count, new_enterprise_count`

设计文档：未找到 `enterprise_distribution` 对应表。

真实库：未找到 `enterprise_distribution` / `dwd_enterprise_distribution`。

相近表：`enterprise_industry_distribution`，但语义是“区域产业分布饼图”，不是四维地图热力。

结论：不能擅自映射。

#### `dwd_shenzhen_enterprise_summary` / `shenzhen_enterprise_summary`

设计文档：有 `shenzhen_enterprise_summary`，用于深圳企业介绍 KPI、产业分布、历年累计增长。

真实库：缺失 `shenzhen_enterprise_summary`。

真实库相近表：`shenzhen_policy_compare` / `shenzhen_policy_distribution` / `shenzhen_policy_status`，语义是政策分析，不是深圳企业统计。

结论：不能擅自映射。

## 6. Mock 与降级问题

当前代码里仍存在大量 Mock 分支：

- `if should_use_mock(): return _mock_*`
- AI 分析 Mock 下直接内存生成结果，不发 Java callback
- 部分代码有“ES 不可用则返回 Mock”的死代码/历史逻辑

同时，`conf/settings.yaml` 和 K8s 当前写的是 `GKX_MOCK_ENABLED=0`，但 `gkx_common/config.py` 在配置缺失时默认 `True`，Dockerfile 中 AI/worker 仍有 `GKX_MOCK_ENABLED=1` 的风险。

结论：要实现“绝不 Mock”，不仅要设置环境变量，还要：

- 默认值改为 false
- 删除/禁用业务 Mock 分支
- 删除静默降级 Mock
- 数据源异常直接抛错

## 7. 建议修复策略

### 阶段 1：先做访问层基建

1. 明确采用轻量 Repository，而不是继续在 view 写 SQL。
2. 引入真正生效的连接池依赖（如 `dbutils`），或选定 SQLAlchemy Core / SQLModel。
3. 增加 `gkx_common/repositories/`：
   - `enterprise_patent_repository.py`
   - `enterprise_risk_repository.py`
   - `enterprise_overview_repository.py`
   - `enterprise_key_repository.py`
   - `enterprise_shenzhen_repository.py`
4. Repository 层集中维护：
   - 表名
   - 字段名
   - 真实库字段到接口字段的映射
   - 缺表/缺字段的 fail-closed 错误

### 阶段 2：按分级修复

可直接修：

- 只改 `dwd_` 前缀且字段能对齐的查询。

需确认后修：

- 专利明细、专利趋势、对外投资、overview 聚合、风险明细字段映射。

需补表或另定真源：

- 四维地图 `enterprise_distribution`
- 深圳企业统计 `shenzhen_enterprise_summary`

### 阶段 3：Mock 清退

1. `config.py` 默认 Mock 改 false。
2. Dockerfile 的 `GKX_MOCK_ENABLED=1` 改 false/移除。
3. search service 中 Mock 分支改为显式测试入口或删除。
4. AI service Mock 分支不再直接标 success；未接通算法时直接 fail 或返回 503。

## 8. 当前不确定项（需 human 决策）

1. `enterprise_patent_detail`：按真实库 11 字段适配，还是要求 DWD 补齐设计的 28 字段？
2. `risk_*`：按真实库精简字段适配，还是要求 DWD 补齐设计富字段？
3. `enterprise_region_summary` 等 overview 表：按真实库字段适配，还是要求 DWD 表结构回归设计？
4. `enterprise_distribution`：是否需要新建四维地图分布表？
5. `shenzhen_enterprise_summary`：是否要求补建该设计表？
6. ~~访问层技术选型~~：已由 human:徐滕强确认采用 SQLAlchemy 2.x ORM + QueuePool。

## 9. 建议结论

不要继续在 view 中逐个修 SQL。当前最稳路径是：

1. 先建立 Repository/Model 访问层。
2. 把真实库字段映射集中到一处。
3. 对缺表/缺字段明确 fail-closed。
4. 对需要 human 决策的表不做猜测映射。

这样既能解决当前 500，也能避免后续 DWD 字段调整时每个接口再次散点爆雷。

## 10. 第二轮审计补充（2026-08-03）

### 10.1 数据本身的 Mock 占比

即使代码关闭 Mock，当前 ES / DWD 数据源本身仍包含大量 Mock/样例数据：

| 数据源 | 实测 |
|---|---|
| ES alias `gkx_enterprise` → `gkx_enterprise_v1` | 10,000 个企业根文档 |
| ES `org_id` 前缀 `MOCKENT` | 9,880 个（98.8%） |
| ES 非 `MOCKENT` | 120 个，编号为 `ORG00000001` 等样例式 ID |
| DWD `enterprise_base` | 10,000 行；`MOCKENT` 9,880 行，`ORG*` 120 行 |
| DWD `enterprise_invest` | 9,863 行；`MOCKENT` 9,835 行，`ORG*` 28 行 |
| DWD `enterprise_patent_detail` | 460 行；全部挂在 `ORG*` 样例 ID |

结论：需要区分两件事：

1. **代码 Mock**：`should_use_mock()`、内存生成、静默回退。
2. **数据源 Mock**：代码真实读取 ES/MySQL，但 ES/MySQL 中装的是样例数据。

仅关闭代码 Mock 不能满足“全部真实数据”目标；ES/DWD 还需要真实数据重建或替换。

### 10.2 代码引用表行数

| 表 | 行数 | 备注 |
|---|---:|---|
| `enterprise_base` | 10,000 | 98.8% `MOCKENT` |
| `enterprise_patent_detail` | 460 | 字段为 11 字段精简版 |
| `enterprise_patent_history` | 50,096 | 代码额外要求 3 个不存在字段 |
| `enterprise_invest` | 9,863 | 字段名与代码不一致 |
| `enterprise_region_summary` | 10 | 字段/粒度与设计不一致 |
| `enterprise_industry_distribution` | 25 | 可用于产业分布饼图，不能替代四维地图 |
| `enterprise_growth_trend` | 12 | 字段/时间粒度与代码不一致 |
| `enterprise_industry_summary` | 12 | `rd_staff_total` vs 代码 `research_staff_total` |
| `enterprise_stat_summary` | 11 | 真实字段为 `metric_value`，代码部分查询使用 `stat_value` |
| `enterprise_type_scale_stats` | 27 | 真实字段 `region`，代码使用 `region_code/region_name` |
| `enterprise_risk_summary` | 360 | 汇总表可用 |
| 18 类 `risk_*` 主表及 6 张 party 表 | 全部 0 行 | 表存在，但字段体系与代码配置不一致 |
| `dwd_sz_city_benchmark` | 8 | Python 确实使用；代码已改查 `sz_city_benchmark`，待 DBA 重命名/迁移 |
| `shenzhen_enterprise_summary` | 缺表 | 设计有、真实库无 |
| `enterprise_distribution` | 缺表 | 代码用途为四维地图；设计/真实库均无 |

### 10.3 风险表整体结论

18 类风险代码配置按设计文档富字段编写；真实库则采用统一精简字段体系：

- 多数主表实际字段接近 `case_no/case_title/amount/court/event_date/status`
- 代码要求各业务类型专属字段，如 `procedure_date/judgment_doc_id/notice_id/...`
- 6 类 party 表的实际关联字段多为 `case_id`，代码则分别使用 `judgment_doc_id/case_unique_id/notice_id/case_no`
- 代码要求 party 表 `is_history`，真实 party 表普遍没有
- 当前全部风险明细表均为 0 行

因此风险明细不能通过机械改字段名解决，需先确定：

1. 真实库精简模型是否为正式新规范；
2. 还是应按 DWD 设计文档恢复富字段；
3. party 主外键统一使用 `case_id` 还是保留各源业务 ID。

### 10.4 当前执行边界

human:徐滕强要求本轮先完成全量表结构审计，再统一决定“改代码还是改表”。因此：

- 已完成：SQLAlchemy 访问层基础、已确认目标表的 `dwd_` 前缀清理。
- 暂停：所有有争议字段的接口映射。
- 暂停：缺表替代映射。
- 下一步：继续完成 ES mapping 与代码字段三方对账，然后提交统一决策清单。

### 10.5 ES mapping 与字段覆盖率

ES alias：`gkx_enterprise` → `gkx_enterprise_v1`

mapping 与代码使用的主要检索字段在“字段定义”层面能够对上：

- `org_id/region_id/province/city/district`
- `tags_flat`
- `industry_chains_flat/industry_chain_names_flat/industry_node_names_flat`
- `company_type/enterprise_scale/operating_status/listing_status/risk_level`
- `incorporation_date`

但真实文档字段覆盖率暴露了另一个问题：

| 字段 | 10,000 企业文档覆盖 |
|---|---:|
| `org_id/region_id/province/city/district` | 100% |
| `tags_flat/industry_chains_flat/industry_chain_names_flat` | 100% |
| `company_type/enterprise_scale/operating_status/listing_status` | 100% |
| `risk_level` | 99.7% |
| `competitiveness_score` | 0% |
| `tech_score/business_score` | 0% |
| `supply_chain_role/core_tech_tags_flat` | 0% |
| `statistics.*` 任一已抽查指标 | 0% |
| `risk_flags.*` | 0% |
| `financials/executives/financings/bids` | 0% |
| `supply_chain_relations/innovation_carriers` | 0% |
| `tags/industry_chains` nested 明细 | 0% |

结论：

1. ES mapping 预先定义了 162 个字段路径，但实际文档只填充了搜索/筛选用的一部分扁平字段。
2. 大量企业详情、评分、财务、风险、供应链接口即使真实查询 ES，也会返回空值或 0。
3. mapping 存在不等于数据已接入；后续必须把“字段存在性”与“字段覆盖率”都作为验收条件。
4. 当前 ES 数据与 DWD `enterprise_base` 的 9,880 `MOCKENT` + 120 `ORG*` 样例结构一致，属于样例索引，不是正式企业数据索引。

### 10.6 当前 DWD 数据与精简字段的来源线索

在 `lumen-etl-es-py` 找到两类明确的 Mock 灌数脚本：

1. `scripts/seed_enterprise_relational_mock.py`
   - `MOCK_PREFIX = "MOCKENT"`
   - 生成 `enterprise_base` 与投资、供应链、合作、招投标等关系数据
   - 当前库 9,880 个 `MOCKENT` 与该脚本语义一致
2. `scripts/seed_dwd_mock.py`
   - 文件说明为“往 DWD 空表灌 mock 数据”
   - 直接灌入 `enterprise_risk_summary/enterprise_stat_summary/enterprise_growth_trend/enterprise_region_summary/enterprise_industry_distribution/enterprise_industry_summary/enterprise_type_scale_stats`
   - 插入字段与当前真实库精简结构完全对应，例如：
     - `enterprise_stat_summary.enterprise_count/metric_value`
     - `enterprise_region_summary.region_code/new_count/active_count/output_value`
     - `enterprise_growth_trend.region_code/stat_month/new_count/cumulative_count`

因此可以确认：

- 当前这些表内的数据来自或至少符合 Mock 灌数脚本。
- 暂不能确认这些表最初由谁创建：ETL 仓未找到核心表的正式 CREATE TABLE DDL。
- 不应把当前精简 Mock 表结构直接认定为新的正式业务规范。

附带风险：

- `seed_dwd_mock.py` 存在硬编码公网数据库连接与明文密码，应另行安全整改；本任务不擅自修改 ETL 仓。

### 10.7 三方对账后的总体关系

| 对象 | 代码 SQL vs 设计文档 | 真实库 vs 设计文档 |
|---|---|---|
| `enterprise_patent_detail` | 基本一致（代码按 28 字段设计） | 真实库仅 11 字段 |
| `enterprise_patent_history` | 一致（代码需要设计中的 12 字段） | 缺 3 个业务字段 |
| `enterprise_invest` | 一致（代码使用 `inv_name/investment_amount/...`） | 使用另一套 `inv_org_name/invest_amount/...` |
| `enterprise_region_summary` | 一致 | 使用精简字段且缺 region_type/parent_region_id |
| `enterprise_industry_distribution` | 代码仅表名前缀需改，字段基本按设计 | `region_code` 替代 `region_id`，多 `ratio` |
| `enterprise_growth_trend` | 一致 | 使用 `YYYY-MM` 字符串 + cumulative 精简模型 |
| `enterprise_industry_summary` | 一致 | `rd_staff_total` 替代 `research_staff_total`，多 `revenue_total` |
| `enterprise_stat_summary` | 一致（代码使用 `stat_value`） | 使用 `enterprise_count/metric_value` |
| `enterprise_type_scale_stats` | 一致（代码使用 region_code/name） | 合并为单列 `region` |
| `risk_*` | 基本按设计富字段 | 统一精简字段，party 关联键也不同 |
| `shenzhen_enterprise_summary` | 与设计一致 | 缺表 |
| `enterprise_distribution` | 代码有、设计无 | 缺表 |

当前最强证据表明：**代码字段与设计文档整体更接近；真实库核心企业表是另一套用于 Mock 演示的精简结构。**

因此下一阶段不应把代码全面适配到当前 Mock 精简表，否则会固化偏离。应先由 human 决定：

1. 《DWD表结构设计-企业模块.md》是否继续作为目标结构真源；
2. 若是，先产出 MySQL 正式 DDL + 迁移/重建方案，再把 SQLAlchemy Model 改为目标结构；
3. 若不是，需要先正式修订设计文档，不能仅以当前 Mock 表倒推新规范。

### 10.8 Human 决策：API 契约与 ES 执行边界

2026-08-03 human:徐滕强确认：

1. 暂不改已提供给 Java 的 API 结构：
   - 路径不变
   - 请求字段不变
   - 响应字段、字段含义、层级不变
2. 后续表字段变化由 Python Model/Repository 兼容层处理，不把数据库字段漂移传递给 Java。
3. 无法可靠兼容的字段应显式暴露错误，不允许伪造或静默 Mock。
4. ES 更新脚本等待 DWD 表结构稳定后再处理，本轮不修改 `lumen-etl-es-py` 的 ES 同步逻辑。

实施含义：

- View/API 层保持稳定。
- Repository 层集中维护“数据库字段 → 稳定 API 字段”映射。
- SQLAlchemy Model 可随数据库版本调整，但 DTO/API 契约不随之改变。
- 当前发现的 ES Mock 数据与字段覆盖缺口保留为阻塞证据，不在本轮擅自重建索引。

### 10.9 ODS 可用性抽查

为判断“修表后能否立即以真数据重建”，只读抽查 `gkxlumenx_ods`：

- `dwd_company/dwd_company_base/dwd_company_*`：当前均 0 行
- `dwd_patent/dwd_patent_title/dwd_patent_abstract/dwd_patent_legal`：当前均 0 行
- `dwd_org_invest_info`：0 行
- 司法/风险相关 `dwd_org_risk_*`、`dwd_org_company_*`：当前均 0 行
- `dwd_forg_investment`：约 12,077 行
- `invest`：约 25 行
- `company_history_name`：约 10 行

结论：

- ODS 是否已有数据不决定接口成功与否：目标 DWD 表结构存在但为空时，接口应返回 200 空结果。
- 只有 DWD 缺表、缺字段或数据库连接故障才返回 503；不得把“ODS 未入站”当作接口失败条件。
- ODS 数据量只影响返回内容是否为空和后续 DWD 重建，不阻塞 Python 的查询契约。
- ES 更新按 human 决策延期到 DWD 结构稳定之后。

### 10.10 运行时 Mock 清退进度

已完成：

- `AppConfig` 默认且强制 `mock_enabled=False`
- 任意 `GKX_MOCK_ENABLED=1/true/yes` 直接拒绝启动
- Docker search/ai/worker/analytics/graph 镜像全部默认 `GKX_MOCK_ENABLED=0`
- search client 调 Java 失败直接抛错，不再回退内存企业
- entan/science 提交失败直接抛错，不再伪造 `running`
- entan 同步评估 Mock 后门改为显式报错，强制走异步算法接口
- fail-closed + SQLAlchemy 契约测试共 16 条通过

测试现状：

- 旧全量测试中 216 条是“Mock 模式接口测试”，关闭运行时 Mock 后按预期失败。
- 不能为恢复测试绿而重新开放生产 Mock。
- 后续测试应改为依赖注入 fake/contract test，fake 只存在测试进程，不进入运行时代码路径。

### 10.11 逐表复核工作簿

human:徐滕强无法一次性指定“现库/设计”哪个整体为准，要求逐表补充后重新形成正式 DWD 设计。

已生成：

- `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-SCHEMA-REVIEW.md`

内容包括：

1. 12 张非风险差异/缺失/表名调整表；
2. 18 类风险主表及 6 张 party 表逐项字段差异；
3. 从现有代码和设计恢复的 `shenzhen_enterprise_summary` 候选 MySQL DDL；
4. 从 `/stats/distribution` SQL/API 契约恢复的 `enterprise_distribution` 候选 MySQL DDL；
5. `dwd_sz_city_benchmark` 使用核实与去前缀处理结论。

该工作簿已由 human:徐滕强逐表填写并完成二次冲突确认。

### 10.12 DWD v3.0 正式候选

已生成：

- `agent-delivery/data/data-design/企业/DWD表结构设计-企业模块-MySQL-v3.0.md`

范围严格限定已复核的 36 张表：

- 12 张非风险表；
- 18 张风险主表；
- 6 张风险 Party 表。

文档包含 36 份完整 MySQL 8 DDL、复合唯一键、DWD→稳定 API 映射、显式 `null` 字段规则和 DBA 迁移动作。结构自检结果：36 张表、0 重复表名、0 重复字段。

### 10.13 Python v3.0 兼容实现

已完成：

1. `gkx_common/orm_models.py`
   - 12 张非风险表 Model 全部对齐 v3.0；
   - 不再以旧精简样例库字段作为目标契约。
2. `enterprise_risk.py`
   - 18 类查询改用 DWD v3.0 物理列并通过 SQL alias 保持 Java API 字段不变；
   - 6 类拆分案件统一 `t.case_id = p.case_id`；
   - Party 的 `is_history` 直接返回为稳定字段名；
   - 约定不入 DWD 的 7 个字段用 `NULL AS` 显式返回；
   - 删除本模块 Mock 生成器、Mock 路由分支和 ES→Mock 静默回退；
   - `/risk/all` 计数改为数据库真实 total，不再受分页 size 截断。
3. 非风险查询
   - `enterprise_type_scale_stats.region_id AS region_code`，保持 API 不变；
   - `enterprise_distribution` 固定读取同一筛选条件下最新 `stat_date` 批次。
4. 测试
   - 新增 `tests/test_dwd_v3_compatibility.py`；
   - 聚焦回归：47 passed；
   - 全量旧测试：138 passed / 216 failed，失败集仍主要依赖旧 Mock 模式或本地不可达真实数据源，禁止通过重新开放运行时 Mock 修复。

### 10.14 真实库 v3.0 迁移

2026-08-03 经 human:徐滕强明确授权，直接迁移公网 MySQL `gkxlumenx_dwd`，不再等待 DBA：

1. 备份
   - 34 张迁移前现存目标/旧名表已完成结构快照；
   - 10 张有数据表已完成结构+数据完整备份，共 60,524 行。
2. 有数据差异表
   - 9 张表采用目标暂存表迁移；
   - 区域名称通过 `gkxlumenx_dim.code_region` 严格匹配到 level=2 编码；
   - `YYYY-MM` 趋势月份拆为 `stat_year`、`stat_month`；
   - `enterprise_stat_summary.metric_value` 与 `enterprise_count` 全量一致后迁入 `stat_value`；
   - 迁移前后逐表行数一致，共 60,516 行。
3. 风险表
   - 24 张风险主表/party 表迁移前均为 0 行；
   - 已按 v3.0 DDL 建立并切换目标结构。
4. 缺表与改名
   - 已创建 `shenzhen_enterprise_summary`、`enterprise_distribution`；
   - 已将 `dwd_sz_city_benchmark` 重命名为 `sz_city_benchmark`，保留 8 行。
5. 切换与验证
   - 33 组新旧表通过单条 `RENAME TABLE` 原子切换；
   - 36/36 张目标表存在，`__v3` 暂存表为 0；
   - 33 张旧结构表保留为 `__pre_v3`，等待观察期后由 human 决定是否清理；
   - 风险 alias、party `case_id` JOIN 和非风险查询 SQL smoke test 均成功；空风险表正常返回空结果。
