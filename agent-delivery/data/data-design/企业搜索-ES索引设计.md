# 企业搜索 Elasticsearch 索引设计

> **文档版本**：v3.5（新增高价值专利数/营收增长率/利润率/核心技术标签/供应链角色 5 个高级筛选字段）
> **日期**：2026-07-15
> **变更说明**：
> - v3.4（2026-07-13）：新增 region_id 国标行政区划码字段，支撑深圳企业介绍等按地市精确过滤场景
> - v3.5（2026-07-15）：statistics 新增 high_value_patent/revenue_growth_rate/profit_margin；顶层新增 supply_chain_role/core_tech_tags_flat/revenue_growth_rate/profit_margin/high_value_patent_count；enterprise_stat_summary 新增 patent_valid_count/high_value_patent_count 两种 stat_type；_FIELD_STRATEGY 同步追加 5 个高级筛选字段
> **范围**：科技专题服务系统 → 门户-企业发展（企业检索）+ 企业分析（9 模块）+ 企业详情画像（10 Tab）
> **数据源**：PostgreSQL DWD 层（`dwd.*` 表），通过 ETL 每日同步至 ES

---

## 1. 设计目标

### 1.2 设计原则

1. **以企业为文档单位**：一个 `org_id` 对应一个 ES 文档，`_id = org_id`
2. **宽表模式**：将 PG 中一对多关系（标签、产业链、高管、财务等）打平为 nested/数组字段
3. **搜索与详情合一**：一个索引同时支撑检索列表和企业详情页，避免双写
4. **冗余但自洽**：字段可冗余存储（如 `name_cn` 在多张表都有），以 ES 文档为准
5. **千万级数据量优化**：合理分片、控制单文档体积、热数据/冷数据分层

### 1.3 数据量预估

| 指标 | 值 | 说明 |
|------|-----|------|
| 文档总量 | ~1500 万 | 全国在营企业 |
| 单文档体积（平均） | ~10-20 KB | 中小企业：少量 nested |
| 单文档体积（大企业极端） | ~100-500 KB | bids/patents 各几万条；司法明细走 PG 不灌入 ES |
| 索引总大小 | ~60-120 GB | 含副本；大企业 nested 拉高平均值 |
| 日增变更量 | ~5-10 万 | 注册变更/标签更新/财务更新/招投标新增等 |
| nested_objects.limit | **100000** | 默认 10000 不够，大企业 bids+patents 可能 5万+ |

> **nested 体积说明**：大企业的 bids（招投标）和 patents（专利）可能分别到几万条。每条 nested 对象在 Lucene 底层是一个独立的隐藏文档，单文档 nested 总数受 `index.mapping.nested_objects.limit` 控制，已调高到 100000。列表页查询时通过 `_source` 过滤避免读取大 nested 字段，详情页按需指定 `_source.includes` 返回对应 Tab 数据。

> **司法数据不灌入 ES**：司法类数据（案件/失信/被执行/法院公告等 12 张表）大企业可能几万条，但只用于详情页展示、不作为搜索条件，全部走 PG 查询。ES 只存 `risk_flags`（3 个计数）+ `risk_level`（风险等级）用于搜索筛选。避免单文档体积膨胀到十几兆。

> **堆内存建议**：nested 隐藏文档会占用堆内存（parent bitset），按 1500 万文档 × 平均 50 条 nested/文档 = 7.5 亿隐藏文档，建议 ES 节点堆内存 ≥ 32GB，数据节点 ≥ 64GB RAM。

---

## 2. 索引规划

### 2.1 索引规划

基于原型给定模块（门户-企业发展 + 企业分析）的检索需求审视，**判断标准**：是否有独立检索页面，用户需要全局搜索该实体类型（而非从企业详情进入查看明细）。

| 索引名 | 文档单位 | 用途 | 预估文档量 |
|--------|---------|------|-----------|
| `gkx_enterprise` | 企业（按 org_id） | 门户-企业发展 → 企业检索 + 企业详情画像 + 企业分析模块聚合查询 | ~1500 万（千万级） |

### 2.2 `_id` 设计

```
_id = org_id   （32 位 MD5 企业唯一标识，如 1470d623589175f1fe06fb5466b77f55）
```

**为什么用 `org_id` 而不是 `social_credit_code`：**

| 对比项 | org_id | social_credit_code |
|--------|--------|-------------------|
| 覆盖率 | 100%（所有企业都有） | ~99.5%（港股/外资/红筹/个体户等可能缺失） |
| 格式统一 | 统一 32 位 MD5 | 有空值，需兜底 |
| ES 分片路由 | 均匀（MD5 特性） | 均匀 |
| 业务可读性 | 差 | 好（18 位工商代码） |
| 跨系统对接 | 需维护 social_credit_code → org_id 映射 | 直接用 |

**决策理由**：千万级数据中存在无统一社会信用代码的企业（港股上市的红筹架构企业如中国移动、中芯国际；外资企业；部分个体户等），`social_credit_code` 有空值不能作为唯一键。`org_id` 是系统内 100% 覆盖的唯一标识，格式统一，MD5 哈希特性保证 ES 分片路由均匀。

**`_id` 设计注意事项：**

1. **跨系统对接映射**：外部数据（工商/专利/税务）按 `social_credit_code` 关联，ETL 需先查 PG 的 `social_credit_code → org_id` 映射再定位 ES 文档
2. **ETL 去重**：PG 中可能存在同一家企业多条记录（如 stock_base 有 5845 条但只有 5518 个不同信用代码），ETL 需按 `org_id` 去重后写入
3. **不要用 ES 自动生成 `_id`**：增量更新时需要按 `_id` 定位文档做 upsert

### 2.3 千万级数据量的索引设计考量

| 设计点 | 方案 | 理由 |
|--------|------|------|
| **分片数** | 15 个主分片 | 每分片约 100 万文档 / 3-5GB，ES 推荐单分片不超过 50GB；15 分片兼顾并行度和单分片大小 |
| **副本数** | 1 副本 | 容错；搜索并发不高时 1 个够用，高峰可调到 2 |
| **索引别名** | `gkx_enterprise` → `gkx_enterprise_v1` | 重建时切别名零停机 |
| **mapping 控制** | 禁用 `_all`，不索引的字段不建索引 | 控制索引体积 |
| **nested 字段控制** | bids/patents 等大 nested 用 script 增量追加 + `_source` 过滤查询 | 防止 nested 爆炸影响性能 |
| **文档体积控制** | 司法明细等非搜索字段不放 ES，走 PG 查询 | 单文档控制在 100-500KB（大企业极端值） |
| **refresh_interval** | 增量同步时设为 30s（默认 1s） | 批量写入时降低 refresh 频率提性能；完成后调回 1s |
| **分段合并** | 全量重建后 force merge 到 1 段 | 减少段数，提升查询性能 |

### 2.4 字段分层策略（ES vs PG）

> **原则**：搜索/筛选/聚合用到的字段放 ES；只在企业详情页展示、不涉及搜索条件的明细走 PG 查询。

#### 放 ES 的字段（搜索条件 / 聚合 / 排序 / 详情核心信息）

| 字段块 | 类型 | 作为搜索条件 | 说明 |
|--------|------|------------|------|
| 基础工商信息 | 顶层 | ✅ 地区/行业/资本/上市/成立年份筛选 | 核心搜索字段 |
| tags | nested + flat | ✅ 标签筛选、标签聚合 | 数据量小（1-10条） |
| industry_chains | nested + flat | ✅ 产业链/环节筛选、聚合 | 数据量中（1-50条） |
| executives | nested | ❌ 仅详情展示 | 数据量小（5-30条），放 ES 无性能风险 |
| financials | nested | ✅ 营收范围筛选、趋势聚合 | 数据量小（5-15条） |
| financings | nested | ✅ 融资轮次/金额筛选 | 数据量中（1-30条） |
| innovation_carriers | nested + flat | ✅ 载体类型/级别筛选 | 数据量小（1-20条） |
| bids | nested | ✅ 招投标次数/中标筛选 | 数据量大（可能几万条），用 script 增量 + _source 过滤 |
| statistics | nested | ✅ 排序、KPI 卡片 | 预计算统计值（含专利总数/有效数/商标数/软著数/研发占比/合作机构数等，专利明细走PG） |
| risk_flags + risk_level | object + keyword | ✅ 风险等级筛选 | 只存计数，不存明细 |
| supply_chain_relations | nested | ❌ 仅详情展示 | 数据量中（10-500条），但暂保留在 ES |
| news | nested | ❌ 仅详情展示 | 数据量中（20-500条），暂保留在 ES |

#### 走 PG 查询的明细（只在详情页展示，不涉及搜索条件）

| 数据 | PG 源表 | 原型位置 | 不放 ES 的原因 |
|------|---------|---------|--------------|
| 司法案件明细 | gkx_dwd_org_opt_judicial_case | 详情页风险信息 Tab | 大企业可能几万条，且不需要作为搜索条件 |
| 失信明细 | gkx_dwd_org_risk_shixin | 详情页风险信息 Tab | ES 只存 count（risk_flags），明细查 PG |
| 被执行明细 | gkx_dwd_org_risk_zhixing | 详情页风险信息 Tab | ES 只存 count（risk_flags），明细查 PG |
| 经营异常明细 | gkx_dwd_org_company_abnormal | 详情页风险信息 Tab | ES 只存 count（risk_flags），明细查 PG |
| 行政处罚明细 | gkx_dwd_org_company_punish | 详情页风险信息 Tab | 不作为搜索条件 |
| 税务处罚明细 | gkx_dwd_org_risk_tax_punish | 详情页风险信息 Tab | 不作为搜索条件 |
| 法院公告 | gkx_dwd_org_risk_court_announcement + _list | 详情页风险信息 Tab | 不作为搜索条件 |
| 法院立案 | gkx_dwd_org_risk_court_filed_case + _litigant | 详情页风险信息 Tab | 不作为搜索条件 |
| 法院通知 | gkx_dwd_org_risk_court_notice + _list | 详情页风险信息 Tab | 不作为搜索条件 |
| 诉讼信息 | gkx_dwd_org_risk_lawsuit + _list | 详情页风险信息 Tab | 不作为搜索条件 |
| 破产案件 | gkx_dwd_org_bankruptcy_public_cases + _list | 详情页风险信息 Tab | 不作为搜索条件 |
| 司法拍卖 | gkx_dwd_org_tb_judicial_sale + _info_company | 详情页风险信息 Tab | 不作为搜索条件 |
| 企业司法概览 | gkx_dwd_org_company_justice | 详情页风险信息 Tab | 不作为搜索条件 |
| 专利明细 | dwd.enterprise_patent_detail | 详情页知识产权 Tab | 大企业可能几万条，走PG分页查询 |

> **司法数据策略**：ES 只存 `risk_flags`（abnormal_count / shixin_count / zhixing_count 三个计数）+ `risk_level`（风险等级），用于搜索筛选。司法明细（7 张 A 类表 + 5 张 C 类子表）全部走 PG 按 `social_credit_code` 分页查询。这样避免司法明细灌入 ES 导致大企业单文档体积到十几兆。

### 2.2 索引别名策略

```
gkx_enterprise       ← 别名（读写都走别名）
  └── gkx_enterprise_v1  ← 实际索引（重建时建 v2，切换别名实现零停机）
```

---

## 3. `gkx_enterprise` 索引设计

### 3.1 Mapping

```json
{
  "settings": {
    "number_of_shards": 15,
    "number_of_replicas": 1,
    "refresh_interval": "1s",
    "index.mapping.nested_fields.limit": 10,
    "index.mapping.nested_objects.limit": 100000,
    "analysis": {
      "analyzer": {
        "ik_smart_analyzer": {
          "type": "custom",
          "tokenizer": "ik_smart",
          "filter": ["lowercase"]
        },
        "ik_max_word_analyzer": {
          "type": "custom",
          "tokenizer": "ik_max_word",
          "filter": ["lowercase"]
        },
        "pinyin_analyzer": {
          "type": "custom",
          "tokenizer": "pinyin_tokenizer"
        },
        "edge_ngram_analyzer": {
          "type": "custom",
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        }
      },
      "tokenizer": {
        "pinyin_tokenizer": {
          "type": "pinyin",
          "keep_first_letter": true,
          "keep_full_pinyin": true,
          "keep_original": true,
          "lowercase": true
        },
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 20,
          "token_chars": ["letter", "digit"]
        }
      },
      "normalizer": {
        "lowercase": {
          "type": "custom",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "social_credit_code": {
        "type": "keyword"
      },
      "org_id": {
        "type": "keyword"
      },
      "name_cn": {
        "type": "text",
        "analyzer": "ik_max_word_analyzer",
        "search_analyzer": "ik_smart_analyzer",
        "fields": {
          "keyword": { "type": "keyword" },
          "pinyin": { "type": "text", "analyzer": "pinyin_analyzer" },
          "suggest": { "type": "completion", "analyzer": "ik_smart_analyzer" }
        }
      },
      "name_cn_sort": {
        "type": "keyword",
        "normalizer": "lowercase"
      },
      "former_names": {
        "type": "text",
        "analyzer": "ik_smart_analyzer",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "lerep": {
        "type": "text",
        "analyzer": "ik_max_word_analyzer",
        "search_analyzer": "ik_smart_analyzer",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "province": { "type": "keyword" },
      "city": { "type": "keyword" },
      "region_id": { "type": "keyword" },
      "address": {
        "type": "text",
        "analyzer": "ik_smart_analyzer"
      },
      "addr_lng": { "type": "double" },
      "addr_lat": { "type": "double" },
      "postal_code": { "type": "keyword" },
      "incorporation_year": { "type": "integer" },
      "incorporation_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "start_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "end_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "listing_status": { "type": "keyword" },
      "listing_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "registered_capital_value": { "type": "double" },
      "capital_currency_code": { "type": "keyword" },
      "registration_org": { "type": "keyword" },

      "stock_code": { "type": "keyword" },
      "stock_noun": { "type": "text", "analyzer": "ik_smart_analyzer" },
      "stock_type": { "type": "keyword" },
      "listed_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "listed_status": { "type": "keyword" },

      "industry_class": { "type": "keyword" },
      "industry_class_name": { "type": "keyword" },
      "main_activities": {
        "type": "text",
        "analyzer": "ik_max_word_analyzer"
      },
      "main_prod": {
        "type": "text",
        "analyzer": "ik_max_word_analyzer"
      },
      "description": {
        "type": "text",
        "analyzer": "ik_smart_analyzer"
      },

      "tags": {
        "type": "nested",
        "properties": {
          "tag_code": { "type": "keyword" },
          "tag_value": { "type": "keyword" }
        }
      },
      "tags_flat": {
        "type": "keyword"
      },

      "industry_chains": {
        "type": "nested",
        "properties": {
          "chain_code": { "type": "keyword" },
          "chain_name": { "type": "keyword" },
          "node_id": { "type": "keyword" },
          "node_name": { "type": "keyword" },
          "node_type": { "type": "integer" },
          "node_stage": { "type": "integer" },
          "node_stage_name": { "type": "keyword" },
          "chain_score": { "type": "float" },
          "level": { "type": "integer" }
        }
      },
      "industry_chains_flat": {
        "type": "keyword"
      },
      "industry_chain_names_flat": {
        "type": "keyword"
      },
      "industry_node_codes_flat": {
        "type": "keyword"
      },
      "industry_node_names_flat": {
        "type": "keyword"
      },

      "executives": {
        "type": "nested",
        "properties": {
          "name": { "type": "keyword" },
          "position": { "type": "keyword" }
        }
      },

      "financials": {
        "type": "nested",
        "properties": {
          "year": { "type": "integer" },
          "total_assets": { "type": "double" },
          "total_liabilities": { "type": "double" },
          "operating_revenue": { "type": "double" },
          "main_business_revenue": { "type": "double" },
          "total_profit": { "type": "double" },
          "pure_profit": { "type": "double" },
          "total_tax_paid": { "type": "double" },
          "total_fixed_assets": { "type": "double" }
        }
      },

      "financings": {
        "type": "nested",
        "properties": {
          "funding_round": { "type": "keyword" },
          "funding_amount": { "type": "double" },
          "funding_currency_code": { "type": "keyword" },
          "post_valuation": { "type": "double" },
          "completion_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
          "investors_name": { "type": "text", "analyzer": "ik_smart_analyzer" }
        }
      },

      "bids": {
        "type": "nested",
        "properties": {
          "id": { "type": "keyword" },
          "role": { "type": "keyword" },
          "announcement_title": { "type": "text", "analyzer": "ik_smart_analyzer" },
          "counterparty_name": { "type": "keyword" },
          "counterparty_code": { "type": "keyword" },
          "announcement_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" }
        }
      },

      "statistics": {
        "type": "nested",
        "dynamic": false,
        "properties": {
          "patent_total": { "type": "integer" },
          "patent_valid": { "type": "integer" },
          "patent_citation_total": { "type": "integer" },
          "financing_count": { "type": "integer" },
          "financing_total_amount": { "type": "double" },
          "bid_total": { "type": "integer" },
          "bid_win_count": { "type": "integer" },
          "executive_count": { "type": "integer" },
          "innovation_carrier_count": { "type": "integer" },
          "tag_count": { "type": "integer" },
          "industry_chain_count": { "type": "integer" },
          "news_count": { "type": "integer" },
          "invest_count": { "type": "integer" },
          "abnormal_count": { "type": "integer" },
          "shixin_count": { "type": "integer" },
          "zhixing_count": { "type": "integer" },
          "latest_revenue": { "type": "double" },
          "latest_revenue_year": { "type": "integer" },
          "latest_profit": { "type": "double" },
          "employees_number": { "type": "integer" },
          "research_development_amount": { "type": "double" },
          "trademark_total": { "type": "integer" },
          "software_copyright_total": { "type": "integer" },
          "rd_ratio": { "type": "float" },
          "high_value_patent": { "type": "integer" },
          "revenue_growth_rate": { "type": "float" },
          "profit_margin": { "type": "float" },
          "cooperation_count": { "type": "integer" },
          "last_updated": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" }
        }
      },

      "innovation_carriers": {
        "type": "nested",
        "properties": {
          "carrier_type": { "type": "keyword" },
          "carrier_name": { "type": "keyword" },
          "carrier_level": { "type": "keyword" },
          "create_year": { "type": "integer" }
        }
      },
      "innovation_carriers_flat": {
        "type": "keyword"
      },

      "risk_flags": {
        "type": "object",
        "properties": {
          "abnormal_count": { "type": "integer" },
          "shixin_count": { "type": "integer" },
          "zhixing_count": { "type": "integer" },
          "has_abnormal": { "type": "boolean" },
          "has_shixin": { "type": "boolean" },
          "has_zhixing": { "type": "boolean" },
          "punishment_count": { "type": "integer" },
          "has_punishment": { "type": "boolean" }
        }
      },

      "enterprise_scale": {
        "type": "keyword"
      },

      "operating_status": {
        "type": "keyword"
      },

      "competitiveness_score": {
        "type": "float"
      },

      "patent_valid_count": { "type": "integer" },
      "latest_revenue": { "type": "double" },

      "chain_position_text": {
        "type": "keyword"
      },

      "company_type": { "type": "keyword" },
      "paid_in_capital_value": { "type": "double" },
      "district": { "type": "keyword" },
      "logo_url": { "type": "keyword" },
      "tech_score": { "type": "float" },
      "business_score": { "type": "float" },
      "is_chain_leader": { "type": "boolean" },

      "supply_chain_role": { "type": "keyword" },
      "core_tech_tags_flat": { "type": "keyword" },
      "high_value_patent_count": { "type": "integer" },
      "revenue_growth_rate": { "type": "float" },
      "profit_margin": { "type": "float" },

      "risk_level": {
        "type": "keyword"
      },

      "website": {
        "type": "keyword"
      },
      "contact_phone": {
        "type": "keyword"
      },
      "contact_email": {
        "type": "keyword"
      },

      "business_scope": {
        "type": "text",
        "analyzer": "ik_smart_analyzer"
      },

      "supply_chain_relations": {
        "type": "nested",
        "properties": {
          "related_name": { "type": "keyword" },
          "relation_type": { "type": "keyword" },
          "related_code": { "type": "keyword" }
        }
      },

      "news": {
        "type": "nested",
        "properties": {
          "title": { "type": "text", "analyzer": "ik_smart_analyzer" },
          "source": { "type": "keyword" },
          "date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" }
        }
      },

      "data_source": { "type": "keyword" },
      "edw_data_date": { "type": "date", "format": "yyyy-MM-dd||epoch_millis" },
      "es_updated_at": {
        "type": "date",
        "format": "strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```

### 3.2 字段含义速查（备注）

> 以下表格按 mapping 顺序逐一标注每个字段的业务含义、数据类型和用途，方便快速查阅。

#### 基础工商信息

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `social_credit_code` | keyword | 统一社会信用代码（18位） | reg_info | 业务唯一标识，跨系统关联键；可能为空（港股/外资） |
| `org_id` | keyword | 企业内部唯一标识（32位MD5） | reg_info | **ES `_id` 主键**，100% 覆盖 |
| `name_cn` | text (+keyword/pinyin/suggest) | 企业中文名称 | reg_info | 搜索框全文检索 + 拼音搜索 + 自动补全建议 + 精确匹配/排序 |
| `name_cn_sort` | keyword (lowercase) | 企业名小写副本 | reg_info | 按名称字母序排序 |
| `former_names` | text (+keyword) | 企业曾用名列表 | reg_info/名称变更记录 | 分词检索曾用名匹配 + keyword 精确匹配 |
| `lerep` | text (+keyword) | 法定代表人姓名 | reg_info | 可按法人搜索/过滤 |
| `province` | keyword | 省份 | reg_info | 地区筛选、聚合统计 |
| `city` | keyword | 城市 | reg_info | 地区筛选、聚合统计 |
| `region_id` | keyword | 国标行政区划代码（如 440300=深圳市） | ETL 按 province+city 映射 | 按地市精确过滤（深圳企业介绍等场景） |
| `address` | text (ik_smart) | 注册地址 | reg_info | 地址全文搜索 |
| `addr_lng` | double | 经度 | reg_info | 地图定位 |
| `addr_lat` | double | 纬度 | reg_info | 地图定位 |
| `postal_code` | keyword | 邮编 | reg_info | 备用 |
| `incorporation_year` | integer | 成立年份 | reg_info | 按成立年份筛选/排序（如"近5年成立"） |
| `incorporation_date` | date | 成立日期 | reg_info | 精确日期筛选 |
| `start_date` | date | 经营起始日期 | reg_info | 备用 |
| `end_date` | date | 经营截止日期 | reg_info | 推导经营状态（在营/注销） |
| `listing_status` | keyword | 上市状态（已上市/未上市/拟上市） | reg_info | 上市企业筛选 |
| `listing_date` | date | 上市日期 | reg_info | 按上市时间筛选 |
| `registered_capital_value` | double | 注册资本（数值） | reg_info | 按资本规模筛选/排序、推导企业规模 |
| `capital_currency_code` | keyword | 注册资本币种 | reg_info | 币种标识 |
| `registration_org` | keyword | 登记机关 | reg_info | 备用 |
| `company_type` | keyword | 企业工商注册类型（有限责任公司/股份有限公司/外商投资等） | reg_info | 企业类型筛选、画像头部展示 |
| `paid_in_capital_value` | double | 实缴资本（数值） | reg_info | 实缴资本筛选 |
| `district` | keyword | 区县 | reg_info | 区县级筛选（省/市/区三级独立） |
| `logo_url` | keyword | 企业 LOGO 图片 URL | 工商 logo 服务 | 卡片和画像头部 LOGO 展示 |

#### 上市信息

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `stock_code` | keyword | 股票代码 | stock_base | 上市企业精确筛选 |
| `stock_noun` | text (ik_smart) | 股票简称 | stock_base | 股票名搜索 |
| `stock_type` | keyword | 上市板块（主板/创业板/科创板/北交所） | stock_base | 按板块筛选 |
| `listed_date` | date | 上市日期 | stock_base | 按上市时间筛选 |
| `listed_status` | keyword | 上市状态（已上市/退市） | stock_base | 过滤在市企业 |

#### 行业/产品信息

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `industry_class` | keyword | 行业分类代码 | org_product_info | 按行业代码筛选 |
| `industry_class_name` | keyword | 行业分类名称 | org_product_info | 按行业名称筛选/聚合 |
| `main_activities` | text (ik_max_word) | 主营业务范围 | org_product_info | 全文搜索主营业务 |
| `main_prod` | text (ik_max_word) | 主要产品 | org_product_info | 全文搜索产品关键词 |
| `description` | text (ik_smart) | 企业简介 | org_product_info | 全文搜索企业描述 |

#### 标签（一对多，nested + flat 双轨）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `tags` | nested | 企业标签列表（每项含标签编码+标签值） | enterprise_tag | "标签=高企 AND 值=国家级"联合查询 |
| `tags.tag_code` | keyword | 标签编码（如 `high_tech`/`little_giant`/`gazelle`） | enterprise_tag.tag_code | nested 内过滤（ES存编码，Java侧查tag_dict转中文） |
| `tags.tag_value` | keyword | 标签值/明细（如"国家级"、荣誉标签具体名称，可为空） | enterprise_tag.tag_value | nested 内联合过滤 |
| `tags_flat` | keyword (数组) | 标签编码扁平化数组 | enterprise_tag.tag_code | 只按标签编码快速过滤（无需联合值时更快） |

#### 产业链（一对多，nested + flat 双轨）

> **层级说明**：产业链（chain）= 集成电路/生物医药/智能制造…（几十条）；环节节点（node）= EDA/晶圆制造/集成电路设计…（几百条，5 个 level）。一家企业可挂多个产业链，每个产业链下可挂多个环节。

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `industry_chains` | nested | 企业参与的产业链及环节列表 | chain_dtl + chain_info | "产业链=集成电路 AND 环节=EDA"联合查询 |
| `industry_chains.chain_code` | keyword | 产业链代码 | chain_dtl | nested 内过滤 |
| `industry_chains.chain_name` | keyword | 产业链名称（集成电路/生物医药/智能制造…） | chain_dtl | nested 内展示/过滤 |
| `industry_chains.node_id` | keyword | 环节节点ID | chain_dtl | nested 内过滤 |
| `industry_chains.node_name` | keyword | 环节名称（EDA/晶圆制造/集成电路设计…） | chain_dtl | nested 内展示 |
| `industry_chains.node_type` | integer | 节点类型（1=大类节点/2=业务节点/3=展示节点） | chain_info.node_type | 节点分类过滤（业务节点才关联企业） |
| `industry_chains.node_stage` | integer | 上中下游环节（1=上游/2=中游/3=下游） | chain_info.node_stage | 上中下游筛选、链位分组 |
| `industry_chains.node_stage_name` | keyword | 上中下游文本（上游/中游/下游） | ETL 推导 | 可读展示 |
| `industry_chains.chain_score` | float | 企业在该产业链的匹配得分 | chain_dtl | 按匹配度排序 |
| `industry_chains.level` | integer | 环节层级深度（1-5） | chain_info | 备用 |
| `industry_chains_flat` | keyword (数组) | 产业链代码扁平化 | chain_dtl | 按产业链代码过滤/聚合 |
| `industry_chain_names_flat` | keyword (数组) | 产业链名称扁平化 | chain_dtl | **按产业链聚合企业数**（如"集成电路800家"） |
| `industry_node_codes_flat` | keyword (数组) | 环节节点代码扁平化 | chain_dtl | 按环节聚合企业数（钻取分析用） |
| `industry_node_names_flat` | keyword (数组) | 环节名称扁平化（如"EDA""晶圆制造"） | chain_dtl | 按环节名聚合企业数（钻取分析用） |

#### 高管信息（一对多，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `executives` | nested | 高管列表 | executive_info | 详情页展示、按高管名搜索 |
| `executives.name` | keyword | 高管姓名 | executive_info | 精确匹配 |
| `executives.position` | keyword | 职位 | executive_info | 精确匹配 |

#### 年报财务（全部年份，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `financials` | nested | 历年财务数据列表（全部年份） | annual_financial_info | 财务趋势分析、详情页财务概况 |
| `financials.year` | integer | 财务年份 | annual_financial_info | 年份筛选/排序 |
| `financials.total_assets` | double | 总资产 | annual_financial_info | 财务指标 |
| `financials.total_liabilities` | double | 总负债 | annual_financial_info | 财务指标 |
| `financials.operating_revenue` | double | 营业收入 | annual_financial_info | 财务指标、营收趋势 |
| `financials.main_business_revenue` | double | 主营业务收入 | annual_financial_info | 财务指标 |
| `financials.total_profit` | double | 利润总额 | annual_financial_info | 财务指标 |
| `financials.pure_profit` | double | 净利润 | annual_financial_info | 财务指标 |
| `financials.total_tax_paid` | double | 纳税总额 | annual_financial_info | 财务指标 |
| `financials.total_fixed_assets` | double | 固定资产 | annual_financial_info | 财务指标 |

> 查询时按 `financials.year` 倒序取第一条即为最新年，无需额外冗余 `financial_latest` 或 `stock_finance_latest` 字段。研发投入、员工数等上市财务指标如需展示，从 `financials` 最新年份取值即可。

#### 创新载体（一对多，nested + flat 双轨）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `innovation_carriers` | nested | 创新载体列表 | innovation_carrier | "载体类型=重点实验室 AND 级别=国家级"联合查询 |
| `innovation_carriers.carrier_type` | keyword | 载体类型（重点实验室/工程中心/技术中心等） | innovation_carrier | nested 内过滤 |
| `innovation_carriers.carrier_name` | keyword | 载体名称 | innovation_carrier | 展示 |
| `innovation_carriers.carrier_level` | keyword | 载体级别（国家级/省级/市级） | innovation_carrier | nested 内联合过滤 |
| `innovation_carriers.create_year` | integer | 认定年份 | innovation_carrier | 备用 |
| `innovation_carriers_flat` | keyword (数组) | 载体类型扁平化 | innovation_carrier | 快速按类型过滤 |

#### 融资事件（一对多，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `financings` | nested | 融资事件明细列表 | financing_info | 详情页融资历程、模块4商业力维度 |
| `financings.funding_round` | keyword | 融资轮次（天使轮/A轮/B轮/C轮/战略融资等） | financing_info | 按轮次筛选/聚合 |
| `financings.funding_amount` | double | 融资金额 | financing_info | 金额排序 |
| `financings.funding_currency_code` | keyword | 币种 | financing_info | 币种标识 |
| `financings.post_valuation` | double | 投后估值 | financing_info | 估值排序 |
| `financings.completion_date` | date | 完成日期 | financing_info | 按时间排序/筛选 |
| `financings.investors_name` | text (ik_smart) | 投资方名称 | financing_info | 投资方搜索 |

#### 招投标（一对多，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `bids` | nested | 招投标记录列表 | bid_info | 详情页招投标 Tab |
| `bids.role` | keyword | 企业角色（招标方/中标方） | ETL 推导 | 按角色筛选 |
| `bids.announcement_title` | text (ik_smart) | 公告标题 | bid_info | 标题搜索 |
| `bids.counterparty_name` | keyword | 对方企业名称 | bid_info | 关联方展示 |
| `bids.counterparty_code` | keyword | 对方信用代码 | bid_info | 关联标识 |
| `bids.announcement_date` | date | 公告日期 | bid_info | 按时间排序 |

#### 统计字段（nested，ETL 预计算汇总）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `statistics` | nested (dynamic:false) | 企业各维度统计汇总 | ETL 预计算 | 列表页排序、KPI 卡片、快速筛选 |
| `statistics.patent_total` | integer | 专利总数 | patent 表 count | 创新能力排序 |
| `statistics.patent_valid` | integer | 有效专利数 | patent 表 count(status=有效) | 创新能力筛选 |
| `statistics.patent_citation_total` | integer | 专利被引总次数 | patent 表 sum(cited_by_nums) | 技术影响力评估 |
| `statistics.financing_count` | integer | 融资次数 | financing_info count | 融资活跃度 |
| `statistics.financing_total_amount` | double | 累计融资金额 | financing_info sum | 融资规模 |
| `statistics.bid_total` | integer | 招投标参与总数 | bid_info count | 招投标活跃度 |
| `statistics.bid_win_count` | integer | 中标次数 | bid_info count(role=中标方) | 中标能力 |
| `statistics.executive_count` | integer | 高管人数 | executive_info count | 团队规模 |
| `statistics.innovation_carrier_count` | integer | 创新载体数 | innovation_carrier count | 创新平台数量 |
| `statistics.tag_count` | integer | 标签数 | tag_info count | 资质数量 |
| `statistics.industry_chain_count` | integer | 参与产业链数 | chain_dtl count | 产业链覆盖度 |
| `statistics.news_count` | integer | 新闻数 | important_news_info count | 舆情热度 |
| `statistics.invest_count` | integer | 对外投资数 | invest_info count | 投资活跃度 |
| `statistics.abnormal_count` | integer | 经营异常次数 | company_abnormal count | 风险评估 |
| `statistics.shixin_count` | integer | 失信次数 | risk_shixin count | 风险评估 |
| `statistics.zhixing_count` | integer | 被执行次数 | risk_zhixing count | 风险评估 |
| `statistics.latest_revenue` | double | 最新年营收 | financials 取最新年 | 营收排序 |
| `statistics.latest_revenue_year` | integer | 最新营收年份 | financials 取最新年 | 年份标识 |
| `statistics.latest_profit` | double | 最新年净利润 | financials 取最新年 | 利润排序 |
| `statistics.employees_number` | integer | 员工人数 | stock_finance_info | 规模参考 |
| `statistics.research_development_amount` | double | 研发投入 | stock_finance_info | 研发能力 |
| `statistics.trademark_total` | integer | 商标总数 | trademark 表聚合 | 知识产权筛选/统计 |
| `statistics.software_copyright_total` | integer | 软著总数 | software_copyright 表聚合 | 知识产权筛选/统计 |
| `statistics.rd_ratio` | float | 研发投入占比（研发投入/营收） | ETL 计算 | 研发投入占比筛选 |
| `statistics.high_value_patent` | integer | 高价值专利数 | ETL 从专利表计算（被引次数/同族数等规则） | 高价值专利筛选 |
| `statistics.revenue_growth_rate` | float | 营收增长率（%） | ETL 计算 (今年营收-去年)/去年 | 营收增长率筛选 |
| `statistics.profit_margin` | float | 利润率（%） | ETL 计算 pure_profit/operating_revenue | 利润率筛选 |
| `statistics.cooperation_count` | integer | 合作机构数 | cooperation 表聚合 | 供应链筛选 |
| `statistics.last_updated` | date | 统计最后更新日期 | ETL 写入 | 数据新鲜度 |

#### 风险标记

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `risk_flags` | object | 风险标记聚合 | abnormal + shixin + zhixing | 风险筛选 |
| `risk_flags.abnormal_count` | integer | 经营异常次数 | company_abnormal count | 风险评估 |
| `risk_flags.shixin_count` | integer | 失信记录次数 | risk_shixin count | 风险评估 |
| `risk_flags.zhixing_count` | integer | 被执行次数 | risk_zhixing count | 风险评估 |
| `risk_flags.has_abnormal` | boolean | 是否有经营异常 | ETL 计算 | 布尔筛选 |
| `risk_flags.has_shixin` | boolean | 是否失信 | ETL 计算 | 布尔筛选 |
| `risk_flags.has_zhixing` | boolean | 是否被执行 | ETL 计算 | 布尔筛选 |
| `risk_flags.punishment_count` | integer | 行政处罚次数 | punish 表聚合 | 风险筛选 |
| `risk_flags.has_punishment` | boolean | 是否有行政处罚 | punish 表 | 风险筛选（有无行政处罚） |

#### 顶层排序/筛选字段（ETL 预计算）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `enterprise_scale` | keyword | 企业规模（大型/中型/小型/微型/规上） | ETL 按注册资本判定 | 规模筛选 |
| `operating_status` | keyword | 经营状态（在营/注销/迁出/吊销） | 从 end_date 推导 | 默认只看在营企业 |
| `competitiveness_score` | float | 综合竞争力评分 | ai-service 计算 | 默认排序字段（评分降序） |
| `tech_score` | float | 技术力评分 | algorithm | 技术力评分筛选/排序 |
| `business_score` | float | 商业力评分 | algorithm | 商业力评分筛选/排序 |
| `patent_valid_count` | integer | 有效专利数（顶层冗余，ETL从statistics提取） | statistics | 排序专用（避免nested sort） |
| `latest_revenue` | double | 最新营收（顶层冗余，ETL从statistics提取） | statistics | 排序专用（避免nested sort） |
| `chain_position_text` | keyword | 产业链位置文本（如"设计层 · 上游EDA"） | ETL 拼装 | 企业卡片展示 |
| `is_chain_leader` | boolean | 是否产业链链主 | chain_dtl | 链主企业筛选 |
| `supply_chain_role` | keyword | 供应链角色（上游供应商/核心制造/下游客户） | ETL 从 industry_chains.node_stage 映射 | 供应链角色筛选 |
| `core_tech_tags_flat` | keyword (数组) | 核心技术标签扁平化（集成电路/AI芯片/工业软件/生物医药/储能/智能终端） | ETL 从产业标签映射 | 核心技术标签筛选 |
| `high_value_patent_count` | integer | 高价值专利数（顶层冗余，ETL从statistics提取） | statistics | 排序专用（避免nested sort） |
| `revenue_growth_rate` | float | 营收增长率（顶层冗余，ETL从statistics提取） | statistics | 排序/筛选专用 |
| `profit_margin` | float | 利润率（顶层冗余，ETL从statistics提取） | statistics | 排序/筛选专用 |
| `risk_level` | keyword | 风险等级（无风险/低风险/中风险/高风险） | ETL 从风险标记推导 | 风险等级筛选 |

> 营收/利润/专利数/员工数等明细排序字段统一收入 `statistics` nested 字段；其中有效专利数（`patent_valid_count`）和最新营收（`latest_revenue`）在顶层额外冗余一份，专供列表页排序使用，避免 nested sort 性能开销。技术力分（`tech_score`）、商业力分（`business_score`）为算法侧独立产出的评分模型，直接放顶层。

#### 联系方式

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `website` | keyword | 企业官网 | reg_info / ETL 补充 | 详情页工商概况 |
| `contact_phone` | keyword | 联系电话 | ETL 补充 | 详情页（敏感信息，需权限） |
| `contact_email` | keyword | 联系邮箱 | ETL 补充 | 详情页（敏感信息，需权限） |
| `business_scope` | text (ik_smart) | 经营范围 | org_product_info | 全文搜索经营范围 |

#### 供应链关系（一对多，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `supply_chain_relations` | nested | 供应链关系列表 | invest_info + bid_info 推导 | 详情页供应链 Tab |
| `supply_chain_relations.related_name` | keyword | 关联方企业名 | 推导 | 展示 |
| `supply_chain_relations.relation_type` | keyword | 关系类型（投资方/被投资方/招标方/中标方） | 推导 | 关系类型筛选 |
| `supply_chain_relations.related_code` | keyword | 关联方信用代码 | 推导 | 关联标识 |

#### 舆情新闻（一对多，nested）

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `news` | nested | 重要新闻列表（最多20条） | important_news_info | 详情页舆情动态 Tab |
| `news.title` | text (ik_smart) | 新闻标题 | important_news_info | 新闻全文搜索 |
| `news.source` | keyword | 新闻来源 | important_news_info | 按来源筛选 |
| `news.date` | date | 发布日期 | important_news_info | 按时间排序 |

#### 元数据

| 字段 | ES 类型 | 业务含义 | 来源 | 用途 |
|------|---------|---------|------|------|
| `data_source` | keyword | 数据来源标识 | ETL 写入 | 数据溯源 |
| `edw_data_date` | date | 数据仓库日期 | ETL 写入 | 数据新鲜度标识 |
| `es_updated_at` | date | ES 文档最后更新时间 | ETL 写入 | 同步时间戳、增量监控 |

### 3.3 字段来源映射（PG → ES）

> **说明**：本表对齐 DWD 层表结构（v3.2）。DWD 表名以 `enterprise_*` / `dwd_org_*` 为准，`enterprise_extra` 为工商扩展字段表（v3.2 新增 12 字段），`enterprise_score` 为评分表（v3.2 新增 tech_score/business_score），`enterprise_finance_history` 为财务历史表（v3.2 新增 3 字段），`enterprise_history_name` 为曾用名表（v3.2 新建），`enterprise_industry_chain` 为产业链表（v3.2 新增 is_chain_leader）。
>
> **图例**：✅ 有明确 DWD 数据源 | ❌ 无数据源（ODS 也无） | 🧪 MockBadge 置空 | ⚠️ 单位/口径风险 | 🟡 待业务确认

#### 基础工商信息（顶层字段）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `social_credit_code` | enterprise_base | social_credit_code | 业务唯一标识（可能为空，港股/外资） |
| `org_id` | enterprise_base | org_id | **ES 文档主键 `_id`**，100% 覆盖 |
| `name_cn` | enterprise_base | name_cn | IK 分词 + 拼音 + completion suggest |
| `name_cn_sort` | enterprise_base | name_cn | ETL 小写化副本，按名称字母序排序 |
| `former_names` | enterprise_history_name | history_name | 🆕 新建表，ETL 聚合为数组（WHERE org_id=X） |
| `lerep` | enterprise_base | lerep | 法人代表 |
| `province` / `city` / `address` | enterprise_base | 同名 | 地区筛选、地址全文搜索 |
| `region_id` | enterprise_base | ETL 按 province+city 映射国标码 | 按地市精确过滤（深圳企业介绍等） |
| `addr_lng` / `addr_lat` | enterprise_base | 同名 | 地图定位 |
| `postal_code` | enterprise_extra | postal_code | 🆕 邮编 |
| `incorporation_year` / `incorporation_date` | enterprise_base | 同名 | 成立年份/日期筛选 |
| `start_date` | enterprise_extra | start_date | 🆕 经营起始日期 |
| `end_date` | enterprise_extra | end_date | 🆕 经营截止日期，推导经营状态（在营/注销） |
| `listing_status` | enterprise_base | listing_status | 上市状态筛选 |
| `listing_date` | enterprise_base | listing_date | 上市日期筛选 |
| `registered_capital_value` | enterprise_base | registered_capital | ⚠️ 单位注意：DWD 存储单位为万元，ES 统一用元，ETL 需 ×10000 |
| `capital_currency_code` | enterprise_extra | capital_currency_code | 🆕 注册资本币种 |
| `registration_org` | enterprise_extra | registration_org | 🆕 登记机关 |
| `company_type` | enterprise_base | enterprise_type | 🆕 企业工商注册类型（有限责任公司/股份有限公司/外商投资等） |
| `paid_in_capital_value` | enterprise_extra | paid_in_capital | ⚠️ 单位注意：DWD 存储单位为万元，ES 统一用元，ETL 需 ×10000 |
| `district` | enterprise_base | district | 区县（省/市/区三级独立） |
| `logo_url` | ❌ 无数据源 | — | ODS 也无数据，需接外部服务或置空 + 🧪 MockBadge |

#### 上市信息

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `stock_code` | enterprise_base | stock_code | 上市企业精确筛选 |
| `stock_noun` | enterprise_extra | stock_noun | 🆕 股票简称，股票名搜索 |
| `stock_type` | enterprise_base | stock_type | 上市板块（主板/创业板/科创板/北交所） |
| `listed_date` | enterprise_base | listed_date | 上市日期 |
| `listed_status` | enterprise_extra | listed_status | 🆕 上市状态（已上市/退市） |

#### 行业/产品信息

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `industry_class` / `industry_class_name` | enterprise_base | 同名 | 行业分类代码/名称 |
| `main_activities` | enterprise_extra | main_activities | 🆕 主营业务范围，全文搜索 |
| `main_prod` | enterprise_extra | main_prod | 🆕 主要产品，全文搜索产品关键词 |
| `description` | enterprise_extra | description | 🆕 企业简介，全文搜索 |
| `business_scope` | enterprise_extra | business_scope | 经营范围，全文搜索 |

#### 联系方式

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `website` | ❌ 无数据源 | — | ODS 无 website 字段，需爬取或置空 + 🧪 |
| `contact_phone` | enterprise_extra | contact_phone | 🆕 联系电话（敏感信息，需权限控制） |
| `contact_email` | enterprise_extra | contact_email | 🆕 联系邮箱（敏感信息，需权限控制） |

#### 标签（nested + flat 双轨）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `tags` (nested) | enterprise_tag | tag_code + tag_value | 一企业多标签 |
| `tags_flat` | enterprise_tag | tag_code 扁平化 | 用于快速过滤（非 nested 查询） |

#### 产业链（nested + flat 双轨）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `industry_chains` (nested) | enterprise_industry_chain + industry_chain_info | JOIN 后拼装 | 一企业多产业链多环节 |
| `industry_chains_flat` | enterprise_industry_chain | chain_code 扁平化 | 按产业链代码过滤/聚合 |
| `industry_chain_names_flat` | enterprise_industry_chain | chain_name 扁平化 | 按产业链名过滤/聚合企业数 |
| `industry_node_codes_flat` | enterprise_industry_chain | node_id 扁平化 | 按节点代码聚合企业数（企业级去重） |
| `industry_node_names_flat` | enterprise_industry_chain | node_name 扁平化 | 按节点名聚合企业数（企业级去重） |
| `is_chain_leader` | enterprise_industry_chain | is_chain_leader | 🆕 是否产业链链主（🟡 待业务确认规则） |

#### 高管信息（nested）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `executives` (nested) | enterprise_executive | executive_name + position | 高管信息 |

#### 年报财务（nested，全部年份）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `financials` (nested) | enterprise_finance_history | 全部年份财务数据 | 查询时倒序取最新年 |
| `financials.year` | enterprise_finance_history | year | 财务年份 |
| `financials.total_assets` | enterprise_finance_history | total_assets | 总资产 |
| `financials.total_liabilities` | enterprise_finance_history | total_liabilities | 总负债 |
| `financials.operating_revenue` | enterprise_finance_history | operating_revenue | 营业收入 |
| `financials.main_business_revenue` | enterprise_finance_history | main_business_revenue | 🆕 主营业务收入 |
| `financials.total_profit` | enterprise_finance_history | total_profit | 🆕 利润总额 |
| `financials.pure_profit` | enterprise_finance_history | pure_profit | 净利润 |
| `financials.total_tax_paid` | enterprise_finance_history | total_tax_paid | 纳税总额 |
| `financials.total_fixed_assets` | enterprise_finance_history | total_fixed_assets | 🆕 固定资产 |

#### 融资事件（nested）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `financings` (nested) | enterprise_financing | funding_round/amount/valuation/date/investors | 全部融资事件明细 |

#### 招投标（nested）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `bids` (nested) | enterprise_bid | 推导 role + counterparty + title + date | 全部招投标记录 |

#### 统计字段（nested，ETL 预计算汇总）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `statistics` (nested) | ETL 预计算 | 各维度 count/sum/最新值汇总 | 排序、KPI、快速筛选（专利明细走 PG 查 enterprise_patent_detail） |
| `statistics.patent_total` | enterprise_patent_history | SUM(patent_apply_count) | ETL 聚合全部年份专利申请数 |
| `statistics.patent_valid` | enterprise_patent_history | SUM(patent_valid_count) | ETL 聚合全部年份有效专利数 |
| `statistics.trademark_total` | ❌ 无数据源 | — | ODS 也无商标数据，需采购或置空 + 🧪 |
| `statistics.software_copyright_total` | ETL 从 ODS 聚合 | dwd_org_rd_achiev_info.soft_copyright_num | DWD 暂不建表，ETL 直接从 ODS 聚合 |
| `statistics.rd_ratio` | ETL 计算 | enterprise_finance_history.rd_investment / revenue | 取最新年份计算研发投入占比 |
| `statistics.cooperation_count` | ❌ 无数据源 | — | 依赖 NER 推导，延后实现 |
| `statistics.last_updated` | ETL 写入 | 当前时间 | 统计最后更新日期 |

> 以上仅列出 v3.2 新增/变更/无数据源的统计字段，其余统计字段（patent_citation_total/financing_count/bid_total 等）来源保持 v3.1 不变，详见 §3.2 字段含义速查表。

#### 创新载体（nested + flat 双轨）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `innovation_carriers` (nested) | enterprise_innovation_carrier | carrier_type/name/level | DWD 已建表 |
| `innovation_carriers_flat` | enterprise_innovation_carrier | carrier_type 扁平化 | 快速按类型过滤 |

#### 风险标记

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `risk_flags` | company_abnormal + risk_shixin + risk_zhixing + company_punish | count 聚合 | 含行政处罚计数 |
| `risk_flags.has_*` | ETL 计算 | count > 0 | 布尔标记（has_abnormal/has_shixin/has_zhixing/has_punishment） |

#### 顶层排序/筛选字段（ETL 预计算）

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `enterprise_scale` | enterprise_score | ETL 按注册资本判定 | 大型/中型/小型/微型/规上 |
| `operating_status` | enterprise_base | 从 end_date 推导 | 在营/注销/迁出/吊销 |
| `competitiveness_score` | enterprise_score | 综合竞争力评分（算法产出） | 排序字段 |
| `tech_score` | enterprise_score | tech_score | 🆕 技术力评分（算法产出） |
| `business_score` | enterprise_score | business_score | 🆕 商业力评分（算法产出） |
| `patent_valid_count` | ETL 从 statistics.patent_valid 提取 | patent_valid | 顶层冗余，排序专用（避免 nested sort） |
| `latest_revenue` (顶层) | ETL 从 statistics.latest_revenue 提取 | latest_revenue | 顶层冗余，排序专用（避免 nested sort） |
| `chain_position_text` | enterprise_score | 如"设计层 · 上游EDA" | 企业卡片展示用 |
| `is_chain_leader` | enterprise_industry_chain | is_chain_leader | 🆕 是否产业链链主（🟡 待业务确认规则） |
| `risk_level` | enterprise_score | 从 shixin/zhixing/abnormal 推导 | 无风险/低风险/中风险/高风险 |

#### 其他

| ES 字段 | 来源 DWD 表 | 来源字段 | 说明 |
|---------|------------|---------|------|
| `supply_chain_relations` (nested) | enterprise_invest | 推导后拼装 | 详情页供应链关系 Tab |
| `news` (nested) | important_news_info | title/source/date | 详情页舆情动态 Tab |
| `data_source` | ETL 写入 | 固定值 | 数据溯源 |
| `edw_data_date` | ETL 写入 | 当前日期 | 数据新鲜度标识 |
| `es_updated_at` | ETL 写入 | 当前时间 | 同步时间戳、增量监控 |

#### 无数据源字段汇总

> 以下字段在 DWD 层和 ODS 层均无对应数据源，需后续接外部服务、采购数据或置空 + 🧪 MockBadge。

| ES 字段 | 状态 | 说明 |
|---------|------|------|
| `logo_url` | ❌ 无数据源 | ODS 也无数据，需接外部 logo 服务或置空 + 🧪 MockBadge |
| `statistics.trademark_total` | ❌ 无数据源 | ODS 也无商标数据，需采购或置空 + 🧪 |
| `statistics.cooperation_count` | ❌ 无数据源 | 依赖 NER 推导合作机构，延后实现 |
| `website` | ❌ 无数据源 | ODS 无 website 字段，需爬取或置空 + 🧪 |

### 3.4 ETL 计算字段说明

> 以下字段无法直接从 DWD 表单字段映射，需要 ETL 在同步阶段做**聚合、计算或冗余复制**。ETL 作业需按本表实现对应逻辑，保证 ES 文档字段值与 DWD 源数据一致。

| ES 字段 | 计算方式 | 来源 DWD 表 | 说明 |
|---------|---------|-----------|------|
| `former_names` | 聚合为数组 | enterprise_history_name.history_name WHERE org_id=X | 🆕 曾用名列表，按 start_date 排序聚合 |
| `statistics.patent_total` | SUM 全部年份 | enterprise_patent_history.patent_apply_count | 专利申请总数 |
| `statistics.patent_valid` | SUM 全部年份 | enterprise_patent_history.patent_valid_count | 有效专利总数 |
| `statistics.rd_ratio` | 计算 rd_investment / revenue | enterprise_finance_history（取最新年） | 研发投入占比，取最新年份财务数据计算 |
| `patent_valid_count`（顶层） | 复制 statistics.patent_valid | ETL 内部 | 顶层冗余，排序专用（避免 nested sort） |
| `latest_revenue`（顶层） | 复制 statistics.latest_revenue | ETL 内部 | 顶层冗余，排序专用（避免 nested sort） |
| `risk_flags.has_*` | 计算 count > 0 | enterprise_risk_summary | 布尔标记（has_abnormal/has_shixin/has_zhixing/has_punishment） |
| `tags_flat` | 聚合为数组 | enterprise_tag.tag_code | 标签编码扁平化数组 |
| `industry_chain_names_flat` | 聚合为数组 | enterprise_industry_chain.chain_name | 产业链名称扁平化数组，用于聚合企业数 |
| `registered_capital_value` | ×10000 单位换算 | enterprise_base.registered_capital | ⚠️ DWD 存万元，ES 存元 |
| `paid_in_capital_value` | ×10000 单位换算 | enterprise_extra.paid_in_capital | ⚠️ DWD 存万元，ES 存元 |
| `operating_status` | 从 end_date 推导 | enterprise_base.end_date | 在营/注销/迁出/吊销 |
| `enterprise_scale` | 按注册资本判定 | enterprise_base.registered_capital | 大型/中型/小型/微型/规上 |
| `risk_level` | 从风险计数推导 | enterprise_risk_summary | 无风险/低风险/中风险/高风险 |
| `supply_chain_role` | 从 industry_chains.node_stage 映射 | enterprise_industry_chain | 1→上游供应商，2→核心制造，3→下游客户（取企业主要产业链环节） |
| `core_tech_tags_flat` | 从产业标签映射 | enterprise_industry_chain | 枚举：集成电路/AI芯片/工业软件/生物医药/储能/智能终端，一企业可多标签 |
| `statistics.high_value_patent` | ETL 计算高价值专利 | enterprise_patent_detail | 按被引次数≥10 或 同族数≥3 等规则判定 |
| `statistics.revenue_growth_rate` | 计算 (今年营收-去年营收)/去年营收 | enterprise_finance_history | 取最近两年财务数据计算，百分比 |
| `statistics.profit_margin` | 计算 pure_profit / operating_revenue | enterprise_finance_history | 取最新年份，百分比 |
| `high_value_patent_count`（顶层） | 复制 statistics.high_value_patent | ETL 内部 | 顶层冗余，排序专用 |
| `revenue_growth_rate`（顶层） | 复制 statistics.revenue_growth_rate | ETL 内部 | 顶层冗余，排序/筛选专用 |
| `profit_margin`（顶层） | 复制 statistics.profit_margin | ETL 内部 | 顶层冗余，排序/筛选专用 |

> **ETL 作业注意事项**：
> 1. **单位换算**：`registered_capital_value` 和 `paid_in_capital_value` 在 DWD 层以"万元"存储，ES 统一用"元"，ETL 需 ×10000。若漏做换算会导致筛选/排序数值偏差 4 个数量级。
> 2. **顶层冗余一致性**：`patent_valid_count`（顶层）与 `statistics.patent_valid`（nested）、`latest_revenue`（顶层）与 `statistics.latest_revenue`（nested）必须由同一次 ETL 保证一致，避免排序与展示不一致。
> 3. **聚合顺序**：`former_names` 按 `start_date` 升序聚合，保证曾用名时间顺序正确。
> 4. **无数据源字段**：`logo_url`/`trademark_total`/`cooperation_count`/`website` 在 ETL 阶段置空 + 🧪 MockBadge 标记，待数据源接入后补齐。

### 3.5 分词器说明

| 分词器 | 用途 | 示例 |
|--------|------|------|
| `ik_max_word_analyzer` | 索引时分词，最细粒度 | "深圳芯微集成电路" → 深圳/芯微/集成电路 |
| `ik_smart_analyzer` | 搜索时分词，智能切分 | "深圳芯微" → 深圳/芯微 |
| `pinyin_analyzer` | 拼音搜索 | "shenzhen" / "szxw" |
| `edge_ngram_analyzer` | 前缀搜索（备用） | "深圳" → 深/深圳 |

### 3.6 nested vs flat 双轨设计

对于一对多字段（tags、industry_chains、innovation_carriers），同时存 nested 和 flat 两个版本：

| 类型 | 用途 | 查询示例 |
|------|------|---------|
| `tags` (nested) | 需要"标签=高企 AND 值=国家级"联合查询 | `nested: tags.tag_code=high_tech AND tags.tag_value=国家级` |
| `tags_flat` (keyword array) | 只按标签编码过滤，更快 | `terms: tags_flat=["high_tech","little_giant"]` |

---

## 4. 搜索场景 → ES 查询映射

### 4.1 智能检索（搜索框）

用户在搜索框输入关键词，系统在多个字段中全文检索：

```json
{
  "query": {
    "multi_match": {
      "query": "深圳 集成电路",
      "fields": [
        "name_cn^5",
        "name_cn.pinyin^3",
        "main_activities^2",
        "main_prod^2",
        "description",
        "lerep",
        "stock_noun"
      ],
      "type": "best_fields",
      "operator": "or"
    }
  }
}
```

### 4.2 高级筛选

```json
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "province": "广东省" } },
        { "term": { "listing_status": "已上市" } },
        { "range": { "registered_capital_value": { "gte": 50000000 } } },
        { "range": { "incorporation_year": { "gte": 2010, "lte": 2025 } } },
        { "terms": { "tags_flat": ["high_tech", "little_giant"] } },
        { "terms": { "industry_chain_names_flat": ["集成电路"] } },
        { "term": { "enterprise_scale": "大型" } },
        { "term": { "industry_class": "I6519" } }
      ]
    }
  }
}
```

### 4.3 智能检索 + 高级筛选组合

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "芯微",
            "fields": ["name_cn^5", "name_cn.pinyin^3", "main_prod^2"],
            "type": "best_fields"
          }
        }
      ],
      "filter": [
        { "term": { "province": "广东省" } },
        { "terms": { "industry_chain_names_flat": ["集成电路"] } },
        { "nested": {
            "path": "tags",
            "query": {
              "bool": {
                "must": [
                  { "term": { "tags.tag_code": "high_tech" } },
                  { "term": { "tags.tag_value": "国家级" } }
                ]
              }
            }
        }}
      ]
    }
  }
}
```

### 4.4 聚合统计（faceting）

搜索结果页侧边栏的统计计数，一次查询返回：

```json
{
  "size": 0,
  "aggs": {
    "by_province": { "terms": { "field": "province", "size": 35 } },
    "by_listing_status": { "terms": { "field": "listing_status" } },
    "by_scale": { "terms": { "field": "enterprise_scale" } },
    "by_tags": { "terms": { "field": "tags_flat", "size": 20 } },
    "by_industry_chain": { "terms": { "field": "industry_chain_names_flat", "size": 20 } },
    "by_industry_node": { "terms": { "field": "industry_node_names_flat", "size": 100 } },
    "capital_range": {
      "range": {
        "field": "registered_capital_value",
        "ranges": [
          { "to": 1000000, "key": "100万以下" },
          { "from": 1000000, "to": 10000000, "key": "100万-1000万" },
          { "from": 10000000, "to": 50000000, "key": "1000万-5000万" },
          { "from": 50000000, "to": 100000000, "key": "5000万-1亿" },
          { "from": 100000000, "key": "1亿以上" }
        ]
      }
    },
    "by_year": {
      "date_histogram": {
        "field": "incorporation_date",
        "calendar_interval": "year",
        "format": "yyyy"
      }
    }
  }
}
```

### 4.5 产业链聚合统计

#### 数据层级说明

先明确数据库里产业链的层级关系（`gkx_dwd_industry_chain_info` 表）：

| 层级 | 字段 | 示例 | 数量级 |
|------|------|------|--------|
| **产业链**（chain） | `chain_name` | 集成电路、低空经济、生物医药、智能制造… | 几十条 |
| **环节节点**（node） | `node_name` | EDA软件、晶圆制造、集成电路设计… | 几百条（5 个 level） |

一家企业可挂多个产业链，每个产业链下可挂多个环节节点。

#### 场景 1：统计各产业链上的企业数量（核心需求）

> "集成电路有多少家企业""生物医药有多少家"——这是最常见的企业分析模块需求。

用 `industry_chain_names_flat`（keyword 数组），企业级自然去重：

```json
GET /gkx_enterprise/_search
{
  "size": 0,
  "aggs": {
    "by_chain": {
      "terms": { "field": "industry_chain_names_flat", "size": 50 }
    }
  }
}
```

**返回**：
```json
{
  "aggregations": {
    "by_chain": {
      "buckets": [
        { "key": "集成电路", "doc_count": 800 },
        { "key": "低空经济", "doc_count": 300 },
        { "key": "生物医药", "doc_count": 1200 },
        { "key": "智能制造", "doc_count": 950 }
      ]
    }
  }
}
```

> `doc_count` 是**企业数**。一家企业同时挂"集成电路"和"低空经济"，在各自桶里各计 1，符合业务预期。

#### 场景 2：统计某产业链下各环节节点的企业数量（钻取分析）

> "集成电路产业链下，EDA有多少家、晶圆制造有多少家"

用 `industry_node_names_flat`（keyword 数组），同样是企业级去重。通常配合 `industry_chain_names_flat` 过滤使用：

```json
GET /gkx_enterprise/_search
{
  "size": 0,
  "query": {
    "term": { "industry_chain_names_flat": "集成电路" }
  },
  "aggs": {
    "by_node": {
      "terms": { "field": "industry_node_names_flat", "size": 200 }
    }
  }
}
```

**返回**：
```json
{
  "aggregations": {
    "by_node": {
      "buckets": [
        { "key": "集成电路设计", "doc_count": 150 },
        { "key": "EDA软件(电子设计自动化)", "doc_count": 80 },
        { "key": "晶圆制造", "doc_count": 90 }
      ]
    }
  }
}
```

> ⚠️ 这里有个精度问题：`industry_node_names_flat` 是所有产业链的节点混在一起的，过滤 `industry_chain_names_flat=集成电路` 只是先筛出集成电路产业链的企业，但这些企业可能同时挂了其他产业链的节点，`by_node` 桶里会把其他产业链的节点也算进去。
> 如果需要严格"集成电路产业链下的环节"，必须用 **nested 聚合**（见场景 3）。

#### 场景 3：产业链 → 环节 层级钻取（需要精确归属关系）

> "集成电路产业链下各环节企业数，且严格只算集成电路的环节"

用 `industry_chains`（nested）做层级聚合，能保证 chain 和 node 的归属关系正确：

```json
GET /gkx_enterprise/_search
{
  "size": 0,
  "aggs": {
    "chains": {
      "nested": { "path": "industry_chains" },
      "aggs": {
        "by_chain": {
          "terms": { "field": "industry_chains.chain_name", "size": 50 },
          "aggs": {
            "by_node": {
              "terms": { "field": "industry_chains.node_name", "size": 100 },
              "aggs": {
                "by_node_stage": { "terms": { "field": "industry_chains.node_stage_name" } }
              }
            }
          }
        }
      }
    }
  }
}
```

> ⚠️ nested 聚合的 `doc_count` 是 **nested 文档数**，不是企业数。一家企业在集成电路下挂 3 个环节，`by_chain` 的"集成电路"桶里计 3。
> 如果需要企业级去重，要加 `reverse_nested` + `cardinality(org_id)`，语法复杂且千万级数据下性能较差。

#### 三种场景总结

| 场景 | 用哪个字段 | 聚合方式 | 统计单位 | 精度 | 性能 |
|------|-----------|---------|---------|------|------|
| 各产业链企业数 | `industry_chain_names_flat` | terms 聚合 | **企业数**（去重） | 精确 | 快 ✅ |
| 某产业链下各环节企业数（粗略） | `industry_node_names_flat` + 过滤 | terms 聚合 | **企业数**（去重） | 粗略（跨产业链节点混入） | 快 |
| 产业链→环节 层级钻取（精确归属） | `industry_chains`（nested） | nested 聚合 | nested 文档数（需 reverse_nested 才去重） | 精确 | 慢 |

**推荐策略**：
- 日常"各产业链企业数"统计 → **场景 1**（`industry_chain_names_flat`）
- "某产业链下环节分布"概览 → **场景 2**（`industry_node_names_flat`），精度够用
- 严格层级钻取报表 → **场景 3**（nested），离线或低频调用

### 4.6 企业详情页

直接按 `org_id` GET 文档，`_source` 即为完整详情数据，无需 JOIN：

```
GET /gkx_enterprise/_doc/{org_id}
```

> 千万级数据量下，按 `_id` GET 是 O(1) 路由到具体分片，性能不受数据量影响，稳定 <10ms。
> 前端传入 `social_credit_code` 时，Java 服务先查 PG `reg_info` 获取 `org_id`，再查 ES。

### 4.7 搜索建议（completion suggest）

```json
{
  "suggest": {
    "enterprise-suggest": {
      "prefix": "深圳芯",
      "completion": {
        "field": "name_cn.suggest",
        "size": 10
      }
    }
  }
}
```

---

## 5. 完整筛选条件清单（原型确认）

### 5.1 全局筛选器（顶部，三仓共享）

| 筛选维度 | 原型选项 | ES 字段 | 查询类型 |
|----------|---------|---------|---------|
| 产业（单选） | 生物医药/新能源/新材料/智能制造/电子信息/数字经济/合成生物/光载信息/量子信息/脑科学与脑机工程/深地深海/智能机器人/前沿新材料/未来网络与通信 | `industry_chain_names_flat` | term |
| 时间窗口（单选） | 2020-2026 / 2021-2026 / ... / 近3年（默认）/ 近5年 | `incorporation_year` | range |
| 起始年份（单选） | 年份 | `incorporation_year` | gte |
| 结束年份（单选） | 年份 | `incorporation_year` | lte |
| 区域（级联树多选） | 全球/全国/区域 → 全国热门科创城市/深圳/北京/广州/上海/杭州/苏州/南京/武汉/成都/全部 → 南山区/福田区/罗湖区/宝安区/龙岗区/龙华区/光明区/坪山区/盐田区/大鹏新区 | `province` + `city` | terms |

### 5.2 三种检索模式

#### 模式一：关键字检索（默认 Tab）

搜索框 placeholder："输入企业名称 / 简称 / 领域关键词"

热门词：专精特新、国高企、独角兽、集成电路、南山区

```json
{
  "query": {
    "multi_match": {
      "query": "集成电路",
      "fields": [
        "name_cn^5",
        "name_cn.pinyin^3",
        "main_activities^2",
        "main_prod^2",
        "description",
        "tags_flat^2",
        "industry_chain_names_flat^2"
      ],
      "type": "best_fields",
      "operator": "or"
    }
  }
}
```

#### 模式二：智能检索

placeholder："试试：南山区 专精特新 集成电路 专利大于100"

自然语言 → ai-service 解析为结构化条件 → ES bool 查询：

```json
// ai-service 解析 "南山区 专精特新 集成电路 专利大于100" 后生成：
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "city": "南山区" } },
        { "terms": { "tags_flat": ["little_giant", "sme_sme"] } },
        { "terms": { "industry_chain_names_flat": ["集成电路"] } },
        { "range": { "patent_valid_count": { "gt": 100 } } }
      ]
    }
  }
}
```

#### 模式三：高级筛选（字段库抽屉）

6 大类 14 字段，支持 AND/OR 条件组合：

| 分类 | 字段 | 原型选项 | ES 字段 | 查询类型 |
|------|------|---------|---------|---------|
| 基础信息 | 企业名称 | 文本输入 | `name_cn` | match |
| 基础信息 | 经营状态 | 在营/注销/迁出/吊销 | `operating_status` | terms |
| 基础信息 | 注册区县 | 南山区/福田区/... | `city` | terms |
| 基础信息 | 注册资本 | 范围 | `registered_capital_value` | range |
| 组织信息 | 法定代表人 | 文本输入 | `lerep` | match |
| 组织信息 | 企业类型 | 下拉 | `listing_status` + `tags_flat` | terms |
| 组织信息 | 所属产业 | 下拉 | `industry_chain_names_flat` | terms |
| 企业规模 | 企业规模 | 规上/大型/中型/小微 | `enterprise_scale` | terms |
| 企业规模 | 最新营收 | 范围 | `latest_revenue` | range |
| 经营/资质 | 资质荣誉 | 多选 | `tags_flat` | terms |
| 经营/资质 | 是否上市 | 是/否 | `listing_status` | term |
| 经营/资质 | 是否高企 | 是/否 | `tags_flat` | term（含"高新技术企业"） |
| 经营/资质 | 综合竞争力分 | 范围 | `competitiveness_score` | range |
| 经营/资质 | 核心技术标签 | 多选 | `core_tech_tags_flat` | terms |
| 知识产权 | 有效专利数 | 范围 | `patent_valid_count` | range |
| 知识产权 | 高价值专利数 | 范围 | `high_value_patent_count` | range |
| 经营/财务 | 营收增长率 | 范围 | `revenue_growth_rate` | range |
| 经营/财务 | 利润率 | 范围 | `profit_margin` | range |
| 供应链 | 供应链角色 | 上游供应商/核心制造/下游客户 | `supply_chain_role` | terms |
| 风控信息 | 失信级别 | 无/低/中/高 | `risk_level` | terms |

### 5.3 快捷筛选下拉框（结果区上方）

| 筛选框 | 原型选项 | ES 字段 |
|--------|---------|---------|
| 经营状态（多选） | 在营/注销/迁出/吊销 | `operating_status` |
| 企业规模（多选） | 规上/大型/中型/小微 | `enterprise_scale` |
| 注册区县（多选） | 南山区/福田区/宝安区/龙岗区/龙华区/罗湖区/坪山区/光明区 | `city` |
| 资质荣誉（多选） | 上市/专精特新/国高企/独角兽/瞪羚 | `tags_flat` + `listing_status` |

### 5.4 排序字段

| 排序选项 | ES 字段 | 类型 | 说明 |
|----------|---------|------|------|
| 综合竞争力分 | `competitiveness_score` | float | 降序默认，ai-service 预计算 |
| 有效专利数 | `patent_valid_count` | integer | 顶层冗余，ETL从statistics提取，避免nested sort |
| 最新营收 | `latest_revenue` | double | 顶层冗余，ETL从statistics提取，避免nested sort |
| 技术力分 | `tech_score` | float | 算法模型产出 |
| 商业力分 | `business_score` | float | 算法模型产出 |
| 近期新增 | `es_updated_at` | date | 按ES入库时间倒序（新增企业） |
| 成立时间 | `incorporation_date` | date | 按成立日期排序 |
| 注册资本 | `registered_capital_value` | double | 按注册资本规模排序 |

支持升序/降序切换。

### 5.5 搜索结果卡片字段

| 卡片字段 | ES 字段 | 说明 |
|----------|---------|------|
| 企业名称 | `name_cn` | 可点击 |
| 状态标签 | `operating_status` | 如"在营" |
| 资质标签 | `tags_flat` | 上市/专精特新/国高企/独角兽/小巨人/规上 |
| 规模标签 | `enterprise_scale` | 大型/中型/小微/规上 |
| 综合竞争力分 | `competitiveness_score` | 数值 + ⓘ |
| 领域关键词 | `main_prod` / `main_activities` | 如"集成电路设计/EDA/第三代半导体" |
| 法定代表人 | `lerep` | |
| 成立时间 | `incorporation_date` | |
| 注册资本(万) | `registered_capital_value` | 除以 10000 展示 |
| 区县 | `city` | |
| 链位 | `chain_position_text` | 如"设计层 · 上游EDA" |

### 5.6 企业详情画像（10 Tab）→ ES 字段映射

| Tab | 内容 | ES 字段 |
|-----|------|---------|
| 1. 工商概况 | 经营范围/注册地址/官网/联系方式 | `business_scope` / `address` / `website` / `contact_phone` / `contact_email` |
| 2. 主要团队 | 姓名/职务表格 | `executives` (nested) |
| 3. 资质荣誉 | 资质/认定机构/时间表格 | `tags` (nested) + `innovation_carriers` (nested) |
| 4. 知识产权 | 专利名称/类型/日期/状态 | `statistics.patent_total` + `statistics.patent_valid`（总数在ES，明细走PG查 `enterprise_patent_detail`） |
| 5. 经营财务 | 总资产/净利润/研发投入/营收趋势 | `financials` (nested，取最新年份) |
| 6. 供应链关系 | 关联方/关系类型表格 | `supply_chain_relations` (nested) |
| 7. 关系图谱 | 企业关系图谱（G6） | `supply_chain_relations` + 图谱服务 |
| 8. 舆情动态 | 新闻列表 | `news` (nested) |
| 9. 风险信息 | 待接入（Q020） | `risk_flags` + `risk_level` |
| 10. 招投标 | 待接入 | 暂无（需 ETL 接入 bid_info 明细） |

---

## 6. 原型发现与设计补充

### 6.1 智能检索的 NL→结构化解析

原型智能检索支持自然语言输入（如"南山区 专精特新 集成电路 专利大于100"），需要 `gkx-ai-service` 提供 NL 解析能力：

```
用户输入 → ai-service NL 解析 → 结构化 ES bool 查询 → ES 检索 → 结果
```

ai-service 需要识别的实体类型：

| 实体类型 | 示例 | 映射到 ES 字段 |
|----------|------|---------------|
| 区域 | 南山区/深圳/北京 | `city` / `province` |
| 资质标签 | 专精特新/国高企/独角兽 | `tags_flat` |
| 产业领域 | 集成电路/新能源 | `industry_chain_names_flat` |
| 数值比较 | 专利大于100/营收>1亿 | `patent_valid_count` / `latest_revenue` |
| 企业规模 | 大型/中小微 | `enterprise_scale` |
| 上市状态 | 上市/非上市 | `listing_status` |

### 6.2 排序字段需要顶层平铺

原型支持按"综合竞争力分/有效专利数/最新营收/成立时间/技术力分/商业力分/注册资本"等排序。ES 排序要求字段在顶层（不能排序 object/nested 内的字段），因此：

- `competitiveness_score`：顶层 float（ai-service 预计算）
- `patent_valid_count`：顶层 integer（ETL 从 `statistics.patent_valid` 提取到顶层，避免 nested sort）
- `latest_revenue`：顶层 double（ETL 从 `statistics.latest_revenue` 提取到顶层，避免 nested sort）
- `tech_score`：顶层 float（算法模型产出）
- `business_score`：顶层 float（算法模型产出）
- `incorporation_date`：已有顶层 date 字段
- `es_updated_at`：已有顶层 date 字段（近期新增排序）
- `registered_capital_value`：已有顶层 double 字段（注册资本排序）

> `patent_valid_count` 与 `latest_revenue` 在 `statistics` nested 内有同名字段（`patent_valid` / `latest_revenue`），顶层冗余版本专供排序使用，两者由 ETL 保证一致。

### 6.3 权限分级可见性

原型有 L0-L4 五级权限，联系方式标"敏感信息"。ES 层不做权限过滤（性能差），由 Java 网关层根据用户权限级别决定：
- L0/L1：返回 ES 文档时剔除 `contact_phone` / `contact_email`
- L2+：返回完整文档

### 6.4 详情页 Tab 9/10 数据待接入

- Tab 9 风险信息：当前 ES 有 `risk_flags`（异常/失信/被执行计数），明细需走 PG 查询或后续 ETL 接入
- Tab 10 招投标：`bid_info` 表有结构，后续 ETL 灌入 ES 的 `supply_chain_relations` 或独立 Tab

### 6.5 产业选项与数据库产业链的映射

原型全局产业下拉有 13 项（生物医药/新能源/新材料/智能制造/电子信息/数字经济/合成生物/光载信息/量子信息/脑科学与脑机工程/深地深海/智能机器人/前沿新材料/未来网络与通信），但数据库 `industry_chain_info` 当前只有 2 条产业链（集成电路/低空经济）。需要建立产业选项 → 产业链的映射关系，或 ETL 补充更多产业链数据。

---

## 8. 样例数据

> 以下是一条真实的 ES 文档样例，基于 PostgreSQL 测试库中的真实企业数据组装。
> 主体数据来自「软通动力信息技术(集团)股份有限公司」（`org_id = 2f077675ff176e0e6e1fbc5d28a28821`），包含基础工商、上市、财务、高管、对外投资、产品信息等真实字段。
> 产业链数据来自「深圳市翔农创新科技有限公司」（低空经济产业链，4 个环节节点），用于展示 nested + flat 双轨结构的效果。
> 标签、创新载体、风险标志、竞争力评分等字段在测试库中缺失，用合理的 mock 值填充并标注 `// mock`。
> 这条文档可以直接 PUT 到 ES 中验证 mapping、查询和聚合效果。

### 8.1 单条文档样例（PUT `gkx_enterprise/_doc/2f077675ff176e0e6e1fbc5d28a28821`）

```json
{
  "social_credit_code": "91110108781703664R",
  "org_id": "2f077675ff176e0e6e1fbc5d28a28821",
  "name_cn": "软通动力信息技术(集团)股份有限公司",
  "name_cn_sort": "软通动力信息技术(集团)股份有限公司",
  "lerep": "刘天文",
  "province": "北京市",
  "city": "北京市",
  "address": "北京市海淀区西北旺东路10号院东区16号楼5层502",
  "addr_lng": 116.285175,
  "addr_lat": 40.044846,
  "postal_code": "100000",
  "incorporation_year": 2005,
  "incorporation_date": "2005-11-04",
  "start_date": "2005-11-04",
  "end_date": null,
  "listing_status": "已上市",
  "listing_date": "2022-03-15",
  "registered_capital_value": 952941177,
  "capital_currency_code": "CNY",
  "registration_org": "北京市海淀区市场监督管理局",
  "company_type": "股份有限公司",
  "paid_in_capital_value": 45000000.0,
  "district": "南山区",
  "logo_url": "",
  "tech_score": 78.5,
  "business_score": 82.0,
  "is_chain_leader": false,

  "stock_code": "301236.SZ",
  "stock_noun": "软通动力",
  "stock_type": "中国_深市A股_创业板",
  "listed_date": "2022-03-15",
  "listed_status": "已上市",

  "industry_class": "I6531",
  "industry_class_name": "软件开发",
  "main_activities": "一般项目:技术服务、技术开发、技术咨询、技术交流、技术转让、技术推广;软件开发;信息系统运行维护服务;信息技术咨询服务;大数据服务;计算机软硬件及辅助设备零售;计算机软硬件及辅助设备批发;计算机软硬件及外围设备制造;计算机系统服务;会议及展览服务;旅游开发项目策划咨询;安全技术防范系统设计施工服务;货物进出口;技术进出口;进出口代理;非居住房地产租赁",
  "main_prod": "软件与数字技术服务,数字能源与智算服务,计算产品与数字基础设施",
  "description": "软通动力信息技术(集团)股份有限公司成立于2005年11月4日,董事长为刘天文,公司于2022年3月15日在深交所上市,股票代码为301236.SZ。软通动力是一家全栈智能化产品与服务提供商,业务涵盖软件与数字技术服务、计算产品与智能电子、数字能源与智算服务以及国际化服务等领域。",

  "tags": [
    { "tag_code": "high_tech", "tag_value": "国家级" },
    { "tag_code": "software_top100", "tag_value": "省级" },
    { "tag_code": "little_giant", "tag_value": "国家级" }
  ],
  "tags_flat": ["high_tech", "software_top100", "little_giant"],

  "industry_chains": [
    {
      "chain_code": "IC9901",
      "chain_name": "低空经济",
      "node_id": "IC9901090",
      "node_name": "民用无人机",
      "node_type": 2,
      "node_stage": 2,
      "node_stage_name": "中游",
      "chain_score": 98.23,
      "level": 2
    },
    {
      "chain_code": "IC9901",
      "chain_name": "低空经济",
      "node_id": "IC9901036",
      "node_name": "无人机系统",
      "node_type": 2,
      "node_stage": 1,
      "node_stage_name": "上游",
      "chain_score": 98.23,
      "level": 2
    },
    {
      "chain_code": "IC9901",
      "chain_name": "低空经济",
      "node_id": "IC9901104",
      "node_name": "植保无人机",
      "node_type": 2,
      "node_stage": 3,
      "node_stage_name": "下游",
      "chain_score": 98.23,
      "level": 2
    },
    {
      "chain_code": "IC9901",
      "chain_name": "低空经济",
      "node_id": "IC9901106",
      "node_name": "遥感测绘无人机",
      "node_type": 2,
      "node_stage": 3,
      "node_stage_name": "下游",
      "chain_score": 98.23,
      "level": 2
    }
  ],
  "industry_chains_flat": ["IC9901"],
  "industry_chain_names_flat": ["低空经济"],
  "industry_node_codes_flat": ["IC9901090", "IC9901036", "IC9901104", "IC9901106"],
  "industry_node_names_flat": ["民用无人机", "无人机系统", "植保无人机", "遥感测绘无人机"],

  "executives": [
    { "name": "刘天文", "position": "董事长" },
    { "name": "李宏", "position": "董事" },
    { "name": "车俊河", "position": "董事" },
    { "name": "陈柏汀", "position": "监事" },
    { "name": "张鹥茜", "position": "监事" },
    { "name": "唐琳", "position": "监事会主席" }
  ],

  "financials": [
    {
      "year": 2025,
      "total_assets": 27413795768,
      "total_liabilities": 16730511472,
      "operating_revenue": 35089898381,
      "main_business_revenue": 70179796761,
      "total_profit": 5586777.97,
      "pure_profit": 177356807.8,
      "total_tax_paid": 1179630866,
      "total_fixed_assets": null
    },
    {
      "year": 2024,
      "total_assets": 23856000000,
      "total_liabilities": 14280000000,
      "operating_revenue": 31159000000,
      "main_business_revenue": 62318000000,
      "total_profit": 4800000.00,
      "pure_profit": 156000000.0,
      "total_tax_paid": 1050000000,
      "total_fixed_assets": null
    },
    {
      "year": 2023,
      "total_assets": 20500000000,
      "total_liabilities": 12100000000,
      "operating_revenue": 28500000000,
      "main_business_revenue": 57000000000,
      "total_profit": 3200000.00,
      "pure_profit": 132000000.0,
      "total_tax_paid": 980000000,
      "total_fixed_assets": null
    }
  ],

  "financings": [
    {
      "funding_round": "战略融资",
      "funding_amount": 500000000,
      "funding_currency_code": "CNY",
      "post_valuation": 5000000000,
      "completion_date": "2024-11-20",
      "investors_name": "红杉资本中国,经纬中国,高瓴资本"
    },
    {
      "funding_round": "C轮",
      "funding_amount": 600000000,
      "funding_currency_code": "CNY",
      "post_valuation": 3500000000,
      "completion_date": "2023-06-15",
      "investors_name": "腾讯投资,阿里创投"
    },
    {
      "funding_round": "B轮",
      "funding_amount": 400000000,
      "funding_currency_code": "CNY",
      "post_valuation": 1800000000,
      "completion_date": "2021-09-08",
      "investors_name": "深创投,松禾资本"
    }
  ],

  "bids": [
    {
      "id": "bid_2026_00001",
      "role": "中标方",
      "announcement_title": "某大型银行核心系统数字化转型项目中标公告",
      "counterparty_name": "中国工商银行股份有限公司",
      "counterparty_code": "911000002000013474",
      "announcement_date": "2026-05-20"
    },
    {
      "id": "bid_2026_00002",
      "role": "中标方",
      "announcement_title": "深圳市政务服务云平台运维项目",
      "counterparty_name": "深圳市政务服务数据管理局",
      "counterparty_code": "11440300MB2C93686L",
      "announcement_date": "2026-03-10"
    },
    {
      "id": "bid_2026_00003",
      "role": "招标方",
      "announcement_title": "软通动力2026年度IT基础设施采购招标公告",
      "counterparty_name": "华为技术有限公司",
      "counterparty_code": "914403001922038216",
      "announcement_date": "2026-01-15"
    }
  ],

  "statistics": [
    {
      "patent_total": 1523,
      "patent_valid": 892,
      "patent_citation_total": 3856,
      "financing_count": 3,
      "financing_total_amount": 1500000000,
      "bid_total": 28,
      "bid_win_count": 22,
      "executive_count": 6,
      "innovation_carrier_count": 2,
      "tag_count": 3,
      "industry_chain_count": 1,
      "news_count": 3,
      "invest_count": 5,
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "latest_revenue": 35089898381,
      "latest_revenue_year": 2025,
      "latest_profit": 177356807.8,
      "employees_number": 95000,
      "research_development_amount": 2105393903,
      "trademark_total": 45,
      "software_copyright_total": 23,
      "rd_ratio": 0.085,
      "high_value_patent": 156,
      "revenue_growth_rate": 12.6,
      "profit_margin": 0.51,
      "cooperation_count": 12,
      "last_updated": "2026-07-02"
    }
  ],

  "innovation_carriers": [
    {
      "carrier_type": "企业技术中心",
      "carrier_name": "软通动力企业技术中心",
      "carrier_level": "国家级",
      "create_year": 2018
    },
    {
      "carrier_type": "工程技术研究中心",
      "carrier_name": "北京市软件工程技术研究中心",
      "carrier_level": "省级",
      "create_year": 2020
    }
  ],
  "innovation_carriers_flat": ["企业技术中心", "工程技术研究中心"],

  "risk_flags": {
    "abnormal_count": 0,
    "shixin_count": 0,
    "zhixing_count": 0,
    "has_abnormal": false,
    "has_shixin": false,
    "has_zhixing": false,
    "punishment_count": 0,
    "has_punishment": false
  },

  "enterprise_scale": "大型",
  "operating_status": "在营",

  "competitiveness_score": 87.5,
  "patent_valid_count": 892,
  "high_value_patent_count": 156,
  "latest_revenue": 35089898381,
  "revenue_growth_rate": 12.6,
  "profit_margin": 0.51,
  "supply_chain_role": "核心制造",
  "core_tech_tags_flat": ["集成电路", "工业软件"],
  "chain_position_text": "产业链核心企业",
  "risk_level": "低",

  "website": "www.isoftstone.com",
  "contact_phone": "010-82825588",
  "contact_email": "contact@isoftstone.com",

  "business_scope": "一般项目:技术服务、技术开发、技术咨询、技术交流、技术转让、技术推广;软件开发;信息系统运行维护服务;信息技术咨询服务;大数据服务;计算机软硬件及辅助设备零售;计算机软硬件及辅助设备批发;计算机软硬件及外围设备制造;计算机系统服务;货物进出口;技术进出口;进出口代理",

  "supply_chain_relations": [
    { "related_name": "深圳软通动力信息技术有限公司", "relation_type": "子公司", "related_code": "91440300MA5DJWNF8W" },
    { "related_name": "宁夏软通动力科技有限公司", "relation_type": "子公司", "related_code": "91640100MAEB7T3B92" },
    { "related_name": "无锡软通能源科技发展有限公司", "relation_type": "控股子公司", "related_code": "91320214MAK05NJ12F" }
  ],

  "news": [
    { "title": "软通动力发布2025年年度报告：营收同比增长12.6%", "source": "证券时报", "date": "2026-03-28" },
    { "title": "软通动力中标某大型银行数字化转型项目", "source": "中国招标投标公共服务平台", "date": "2026-02-15" },
    { "title": "软通动力入选2025中国软件百强企业榜单", "source": "中国软件行业协会", "date": "2025-12-10" }
  ],

  "data_source": "GKX",
  "edw_data_date": "2026-06-17",
  "es_updated_at": "2026-07-02T16:20:00+08:00"
}
```

### 8.2 样例数据说明

| 数据块 | 来源 | 说明 |
|--------|------|------|
| 基础工商信息 | `gkx_dwd_org_reg_info` | 真实数据，org_id/name_cn/lerep/address/经纬度/注册资本等 |
| 上市信息 | `gkx_dwd_org_stock_base` | 真实数据，股票代码 301236.SZ，创业板 |
| 行业/产品信息 | `gkx_dwd_org_org_product_info` | 真实数据，行业代码 I6531，主营业务/主要产品/企业简介 |
| 高管信息 | `gkx_dwd_org_executive_info` | 真实数据，6 位高管（董事长+董事+监事） |
| 财务信息 | `gkx_dwd_org_annual_financial_info` | 真实数据，2025 年总资产 274 亿、营收 350 亿 |
| 对外投资 | `gkx_dwd_org_invest_info` | 真实数据，5 家被投企业（取前 3 展示在 supply_chain_relations） |
| 产业链信息 | `gkx_dwd_org_industry_chain_dtl`（翔农创新） | 真实数据，低空经济产业链 4 个环节节点（软通动力本身无产业链数据，借用展示） |
| 上市财务快照 | ~~`stock_finance_latest`~~ | 已移除，从 `financials` 最新年份取值即可 |
| 标签 | `tags` | mock，测试库中软通动力无标签数据 |
| 创新载体 | `innovation_carriers` | mock，测试库中软通动力无创新载体数据 |
| 专利统计 | `statistics.patent_total` 等 | mock，测试库中专利表无 social_credit_code 关联 |
| 专利明细 | 走 PG 查 `enterprise_patent_detail` | 不灌入 ES |
| 风险标志 | `risk_flags` | mock，测试库中无异常/失信数据 |
| 竞争力评分 | `competitiveness_score` | mock，由 ai-service 算法模型计算 |
| 新闻 | `news` | mock，测试库中软通动力无新闻数据 |
| 企业规模/经营状态 | `enterprise_scale`/`operating_status` | mock，根据注册资本推导为"大型"，状态为"在营" |

### 8.3 用这条样例可以验证的查询场景

<details>
<summary>① 智能搜索：输入"软通"匹配企业名</summary>

```json
GET gkx_enterprise/_search
{
  "query": {
    "multi_match": {
      "query": "软通",
      "fields": ["name_cn^3", "name_cn.pinyin^2", "stock_noun^2", "main_prod", "description"],
      "type": "best_fields"
    }
  },
  "size": 10
}
```
</details>

<details>
<summary>② 拼音搜索：输入"ruantong"匹配企业名</summary>

```json
GET gkx_enterprise/_search
{
  "query": {
    "match": {
      "name_cn.pinyin": "ruantong"
    }
  }
}
```
</details>

<details>
<summary>③ 高级筛选：北京+已上市+软件行业+注册资本>1亿</summary>

```json
GET gkx_enterprise/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "province": "北京市" } },
        { "term": { "listed_status": "已上市" } },
        { "term": { "industry_class_name": "软件开发" } },
        { "range": { "registered_capital_value": { "gte": 100000000 } } }
      ]
    }
  }
}
```
</details>

<details>
<summary>④ 产业链节点聚合：统计各环节节点上的企业数量</summary>

```json
GET gkx_enterprise/_search
{
  "size": 0,
  "aggs": {
    "by_node": {
      "terms": {
        "field": "industry_node_names_flat",
        "size": 20
      }
    }
  }
}
```
预期返回：
```json
{
  "aggregations": {
    "by_node": {
      "buckets": [
        { "key": "民用无人机", "doc_count": 1 },
        { "key": "无人机系统", "doc_count": 1 },
        { "key": "植保无人机", "doc_count": 1 },
        { "key": "遥感测绘无人机", "doc_count": 1 }
      ]
    }
  }
}
```
</details>

<details>
<summary>⑤ 产业链级别聚合：统计各产业链上的企业数量</summary>

```json
GET gkx_enterprise/_search
{
  "size": 0,
  "aggs": {
    "by_chain": {
      "terms": {
        "field": "industry_chain_names_flat",
        "size": 20
      }
    }
  }
}
```
预期返回：
```json
{
  "aggregations": {
    "by_chain": {
      "buckets": [
        { "key": "低空经济", "doc_count": 1 }
      ]
    }
  }
}
```
</details>

<details>
<summary>⑥ 搜索建议（completion suggest）</summary>

```json
GET gkx_enterprise/_search
{
  "suggest": {
    "org-suggest": {
      "prefix": "软通",
      "completion": {
        "field": "name_cn.suggest",
        "size": 5
      }
    }
  }
}
```
预期返回：`软通动力信息技术(集团)股份有限公司`
</details>

<details>
<summary>⑦ 企业详情页：按 org_id 获取全量字段</summary>

```json
GET gkx_enterprise/_doc/2f077675ff176e0e6e1fbc5d28a28821
```
</details>

<details>
<summary>⑧ 标签筛选+聚合：国家级标签的企业分布</summary>

```json
GET gkx_enterprise/_search
{
  "size": 0,
  "query": {
    "nested": {
      "path": "tags",
      "query": { "term": { "tags.tag_value": "国家级" } }
    }
  },
  "aggs": {
    "tag_names": {
      "nested": { "path": "tags" },
      "aggs": {
        "by_tag": {
          "terms": { "field": "tags.tag_code", "size": 20 }
        }
      }
    }
  }
}
```
</details>

---

## 9. 待补充

- [ ] ES 集群部署配置（分片/副本/内存/磁盘）
- [ ] IK 分词器 + 拼音插件安装清单
- [ ] 产业选项（13 项）→ 产业链数据的映射方案

---

*本文档为 v3.2，PG→ES 映射表对齐 DWD 表结构变更（enterprise_extra/enterprise_score/enterprise_finance_history/enterprise_history_name/enterprise_industry_chain）。聚焦门户-企业发展 + 企业分析两个模块，只设计 1 个 ES 索引 `gkx_enterprise`。`_id = org_id`（32 位 MD5），15 分片支撑千万级数据。*
