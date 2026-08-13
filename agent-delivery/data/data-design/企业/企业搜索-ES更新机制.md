# DWD → Elasticsearch 数据同步文档

> **现行存储入口（S4）**：[`../storage/ENT/stores/elasticsearch/sync.md`](../storage/ENT/stores/elasticsearch/sync.md) · ETL [`../storage/ENT/etl/pipeline-dwd-to-es.md`](../storage/ENT/etl/pipeline-dwd-to-es.md)

> **版本**：v2.3（DWD 时间字段补齐，全部 DWD 模块按 update_time 增量，statistics 例外）
> **日期**：2026-08-13
> **范围**：MySQL `gkxlumenx_dwd` 层 → Elasticsearch 别名 `gkx_enterprise`（`gkx_enterprise_v1` 国内 + `gkx_enterprise_global_v1` 国外）
> **前置条件**：ODS → DWD 已完成，DWD 表有数据
> **ETL 项目**：`lumen-etl-es-py`（FastAPI 服务 + 模块化 ETL）

---

## 1. 整体架构

### 1.1 数据流

```
┌───────────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────────┐
│  MySQL gkxlumenx_dwd  │     │  lumen-etl-es-py                              │     │  Elasticsearch      │
│                       │     │                                                │     │  gkx_enterprise     │
│  enterprise_base      │────▶│  Module: reg_info                              │────▶│  (别名，搜索/读)     │
│  enterprise_extra     │     │  → 顶层工商字段 + upsert 创建文档              │     │  → gkx_enterprise_v1│
│                       │     │                                                │     │  (国内物理索引)      │
│  enterprise_tag       │────▶│  Module: tag_info → tags/tags_flat            │────▶│                     │
│  enterprise_industry_ │────▶│  Module: industry_chain → industry_chains     │────▶│  国内/国外各模块     │
│  chain                │     │                                                │     │  只写自己的字段      │
│  enterprise_executive │────▶│  Module: executive → executives               │────▶│  互不覆盖            │
│  enterprise_finance_  │────▶│  Module: finance → financials                 │────▶│                     │
│  history              │     │                                                │     │  Painless script     │
│  enterprise_financing │────▶│  Module: financing → financings               │────▶│  partial update      │
│  enterprise_bid       │────▶│  Module: bid → bids (nested)                  │────▶│                     │
│  enterprise_patent_   │────▶│  Module: patent → patents (nested)            │────▶│  refresh_interval    │
│  history              │     │                                                │     │  = 30s              │
│  enterprise_innovation│────▶│  Module: innovation_carrier                   │────▶│                     │
│  _carrier             │     │                                                │     │                     │
│  enterprise_invest    │────▶│  Module: invest → supply_chain_relations      │────▶│                     │
│  enterprise_news      │────▶│  Module: news → news                          │────▶│                     │
│  enterprise_supply_   │────▶│  Module: supply_chain                         │────▶│                     │
│  chain                │     │                                                │     │                     │
│  (多表聚合)            │────▶│  Module: statistics → statistics              │────▶│                     │
│                       │     │                                                │     │                     │
│  enterprise_forg_base │────▶│  Module: forg_reg_info                         │────▶│  → gkx_enterprise_  │
│  enterprise_forg_extra│     │  → name_cn/name_en/country_code + upsert       │     │    global_v1        │
│                       │     │                                                │     │  (国外物理索引)      │
│  enterprise_forg_     │────▶│  Module: forg_executive → executives          │────▶│                     │
│  executive            │     │                                                │     │                     │
│  enterprise_forg_     │────▶│  Module: forg_finance                          │────▶│                     │
│  finance_history      │     │  → financials + statistics 最新员工/研发        │     │                     │
│  enterprise_forg_     │────▶│  Module: forg_relations                        │────▶│                     │
│  invest +             │     │  → supply_chain_relations                      │     │                     │
│  enterprise_forg_     │     │                                                │     │                     │
│  parent_subsidiary    │     │                                                │     │                     │
└───────────────────────┘     └──────────────────────────────────────────────┘     └─────────────────────┘
```

### 1.2 核心设计

- **按源表独立模块 + 独立调度**：13 个国内 ETL 模块 + 4 个国外 ETL 模块，每个对应一组 DWD 表，各自独立调度、各自扫描增量、各自只更新自己的 ES 字段。不存在"一个脚本更新所有 ES 维度"的情况——大数据量下单脚本全量更新不现实，必须按表拆分独立跑
- **国外模块独立调度**：`forg_reg_info` 负责创建国外文档（upsert），`forg_executive` / `forg_finance` / `forg_relations` 做 partial update；`forg_relations` 合并 `enterprise_forg_invest` 与 `enterprise_forg_parent_subsidiary` 写 `supply_chain_relations`
- **写索引口径**：搜索/读走别名 `gkx_enterprise`；ETL 写物理索引 `gkx_enterprise_v1`（国内）/ `gkx_enterprise_global_v1`（国外）。别名指向多索引时不能用于写
- **Painless script 局部更新**：用 `ctx._source.xxx = params.xxx` 做字段级更新，不用全文档覆盖
- **各模块按 DWD 表的 `update_time` 独立调度**：每个模块有自己的水位线，按各自源表的数据更新频率独立调度（每日定时增量同步），互不依赖
- **国内 reg_info 首次必须先跑**：reg_info 模块负责 upsert 创建文档（含初始空 nested 数组），其余国内模块做 partial update。首次初始化时 reg_info 先跑一次，后续日常增量同步各模块独立跑
- **国内 statistics 定期跑**：统计模块聚合其他模块的明细数据，可低频调度（如每日最后一次）
- **水位线独立**：每个模块维护自己的水位线，单模块失败/重跑不影响其他模块

### 1.3 为什么不用全文档重写？

全文档 PUT 会覆盖其他模块写入的字段。script 局部更新是文档级锁定的，同一文档的并发 update 会排队串行执行，各模块只碰自己的字段，不会互相覆盖。

---

## 2. ETL 模块清单

### 2.1 模块注册表（13 个国内模块 + 4 个国外模块）

**国内模块（13 个）：**

| 序号 | 模块名 | DWD 源表 | script_id | 更新的 ES 字段 | 更新方式 |
|---|---|---|---|---|---|
| 1 | **reg_info** | `enterprise_base` + `enterprise_extra` | `gkx_reg_info` | name_cn/social_credit_code/province/city/district/region_id/address/... 等 40+ 顶层字段 | script 覆盖 + **upsert 创建文档** |
| 2 | tag_info | `enterprise_tag` | `gkx_tag_info` | tags (nested) / tags_flat | script 覆盖 |
| 3 | industry_chain | `enterprise_industry_chain` | `gkx_industry_chain` | industry_chains (nested) / industry_chains_flat / industry_chain_names_flat / industry_node_names_flat | script 覆盖 |
| 4 | executive | `enterprise_executive` | `gkx_executive` | executives (nested) | script 覆盖 |
| 5 | finance | `enterprise_finance_history` | `gkx_finance` | financials (nested) | script 覆盖 |
| 6 | financing | `enterprise_financing` | `gkx_financing` | financings (nested) | script 覆盖 |
| 7 | bid | `enterprise_bid` | `gkx_bid` | bids (nested) | script 覆盖 |
| 8 | patent | `enterprise_patent_history` | `gkx_patent` | patents (nested) | script 覆盖 |
| 9 | innovation_carrier | `enterprise_innovation_carrier` | `gkx_innovation_carrier` | innovation_carriers (nested) | script 覆盖 |
| 10 | invest | `enterprise_invest` | `gkx_invest` | supply_chain_relations (投资部分) | script 覆盖 |
| 11 | news | `enterprise_news` | `gkx_news` | news (nested) | script 覆盖 |
| 12 | supply_chain | `enterprise_supply_chain` | `gkx_supply_chain` | supply_chain_relations (供应链部分) | script 覆盖 |
| 13 | **statistics** | (多表聚合) | `gkx_statistics` | statistics (nested, 聚合统计) | script 覆盖 |

### 2.2 国外模块注册表（4 个模块）

| 序号 | 模块名 | DWD 源表 | script_id | 更新的 ES 字段 | 更新方式 |
|---|---|---|---|---|---|
| 1 | **forg_reg_info** | `enterprise_forg_base` + `enterprise_forg_extra` | `gkx_forg_reg_info` | name_cn/name_en/country_code/social_credit_code/... 等顶层字段 | script 覆盖 + **upsert 创建国外文档** |
| 2 | forg_executive | `enterprise_forg_executive` | `gkx_forg_executive` | executives (nested) | script 覆盖 |
| 3 | forg_finance | `enterprise_forg_finance_history` | `gkx_forg_finance` | financials (nested) + statistics 最新员工/研发 | script 覆盖 |
| 4 | forg_relations | `enterprise_forg_invest` + `enterprise_forg_parent_subsidiary` | `gkx_forg_relations` | supply_chain_relations（投资 + 母子公司关系） | script 覆盖 |

国外模块统一写物理索引 `gkx_enterprise_global_v1`；`forg_reg_info` 首次创建文档，其余国外模块做 partial update。

### 2.3 调度策略（国内模块）

**日常增量同步：各模块独立调度，互不依赖**

每个模块对应一个独立的 K8s CronJob，按各自源表的数据更新频率设定调度时间。模块之间不需要串行等待——每个模块用 Painless script partial update 只写自己的字段，并发执行不会互相覆盖。

| 模块 | DWD 源表 | 时间字段 | 建议调度时间 | 说明 |
|---|---|---|---|---|
| reg_info | enterprise_base + enterprise_extra | base.update_time 或 extra.update_time | 02:00 | 工商基础信息 |
| tag_info | enterprise_tag | update_time | 02:10 | 资质标签，变更较少 |
| industry_chain | enterprise_industry_chain | update_time | 02:15 | 产业链关联 |
| executive | enterprise_executive | update_time | 02:20 | 高管信息 |
| finance | enterprise_finance_history | update_time | 02:25 | 财务历史 |
| financing | enterprise_financing | update_time | 02:30 | 融资信息 |
| bid | enterprise_bid | update_time | 02:35 | 招投标，数据量可能较大 |
| patent | enterprise_patent_history | update_time | 02:40 | 专利历史，数据量可能较大 |
| innovation_carrier | enterprise_innovation_carrier | update_time | 02:45 | 创新载体 |
| invest | enterprise_invest | update_time | 02:50 | 对外投资 |
| news | enterprise_news | update_time | 02:55 | 新闻动态 |
| supply_chain | enterprise_supply_chain | update_time | 03:00 | 供应链关系 |
| statistics | (多表聚合) | 无（派生聚合，org_id 游标） | 03:30 | 最后跑，聚合统计 |

> 调度时间错开 5 分钟，避免所有模块同时打满 MySQL 连接池和 ES 写入队列。
> DWD 正式表已全部补充 `update_time`，日常调度按时间分片做真正增量；
> `statistics` 是多表派生聚合，仍按 `org_id` keyset 游标全量补齐。

**首次初始化：reg_info 先跑，其余模块可并行**

首次灌数据时 reg_info 必须先跑一次（创建 ES 文档），其余 12 个模块可并行跑（各自 partial update 自己的字段）。statistics 最后跑。

```
首次：reg_info → (并行: tag_info / industry_chain / ... / supply_chain) → statistics
日常：各模块独立 CronJob 定时增量同步，互不依赖
```

### 2.4 国外模块调度

国外模块与国内模块独立调度，建议在国内外 DWD 均就绪后错峰执行：

| 模块 | DWD 源表 | 时间字段 | 建议调度时间 | 说明 |
|---|---|---|---|---|
| forg_reg_info | enterprise_forg_base + enterprise_forg_extra | base.update_time 或 extra.update_time | 03:10 | 国外工商基础信息，upsert 创建国外文档 |
| forg_executive | enterprise_forg_executive | update_time | 03:20 | 国外高管 |
| forg_finance | enterprise_forg_finance_history | update_time | 03:25 | 国外财务 |
| forg_relations | enterprise_forg_invest + enterprise_forg_parent_subsidiary | update_time | 03:30 | 国外投资 + 母子公司关系合并写 supply_chain_relations |

> 现网 `enterprise_forg_extra` 已有 `update_time`，无 `data_source`；
> `forg_reg_info` 增量按 base 或 extra 任一更新时间变化驱动。

**首次初始化：forg_reg_info 先跑，其余国外模块可并行**

```
国外首次：forg_reg_info → (并行: forg_executive / forg_finance / forg_relations)
日常：国外模块独立 CronJob 定时增量同步，写 gkx_enterprise_global_v1
```

### 2.5 模块基类（SyncModule）

每个模块继承 `SyncModule` 基类，实现 3 个方法：

| 方法 | 说明 |
|---|---|
| `extract(watermark, time_end)` | 从 DWD 查询一个**有界时间片**；禁止 `extract(None)` 一次拉全表 |
| `build_params(row)` | 将一行 DWD 数据转为 `(org_id, script_params)` |
| `build_script()` | 返回 Painless 脚本文本 |

基类的 `sync(full=)` 方法统一执行：读水位线 → 生成有界分片/游标 → extract → 批量 build_params → bulk update → 更新水位线。

全量策略：
- 有 `update_time`：从 `MIN(update_time)` 到当前时间按 `full_slice_days`（默认 1 天）切片。
- 无 `update_time`（当前仅 `statistics` 派生聚合）：按 `org_id` keyset 游标分批，每批 `batch_size` 个企业。
- 聚合表在时间片内再按 `org_id` 分批回查完整明细，避免加载全量明细后 OOM。

---

## 3. reg_info 模块详解（核心模块）

### 3.1 数据源

合并两张 DWD 表：

| 表 | 字段数 | 说明 |
|---|---|---|
| `enterprise_base` | 50+ | 工商注册信息、财务汇总、资质标签、规模、行业 |
| `enterprise_extra` | 19 | 经营范围、上市信息、联系方式、简介、经纬度 |

```sql
SELECT base.org_id, base.enterprise_code, base.enterprise_name, ...
       extra.business_scope, extra.listed_market, extra.listed_code, ...
FROM gkxlumenx_dwd.enterprise_base base
LEFT JOIN gkxlumenx_dwd.enterprise_extra extra ON base.org_id = extra.org_id
WHERE base.update_time > %s OR extra.update_time > %s  -- 增量条件；base/extra 任一变化都同步
ORDER BY base.org_id
```

### 3.2 ETL 派生逻辑

reg_info 模块不只是字段映射，还做以下派生计算：

| 派生字段 | 来源 | 逻辑 |
|---|---|---|
| `operating_status` | `business_status` | 含"注销"→注销 / "迁出"→迁出 / "吊销"→吊销 / 其他→在营 |
| `enterprise_scale` | `org_size` 或 `registered_capital` | 优先用 DWD org_size；为空时按注册资本兜底（≥1亿→大型 / ≥5000万→中型 / ≥1000万→小型 / 否则→微型） |
| `listing_status` | `is_listed` | Q059：上市/未上市/退市 |
| `is_above_scale` | `revenue_latest` | Q058：营收万元 ≥ 2000 → true |
| `registered_capital_value` | `registered_capital` | 单位换算：DWD 万元 → ES 元（×10000） |
| `incorporation_year` | `registration_date` | 截取前 4 位 |
| `addr_lng/addr_lat` | `headquarters_lng/lat` 或 `lng/lat` | 优先 headquarters，兜底 extra |

### 3.3 upsert 初始文档

reg_info 首次创建文档时，写入初始空结构（供后续模块 partial update）：

```python
params["_upsert"] = {
    "org_id": org_id,
    "social_credit_code": row.get("enterprise_code"),
    "name_cn": row.get("enterprise_name"),
    "tags": [],
    "tags_flat": [],
    "industry_chains": [],
    "executives": [],
    "financials": [],
    "financings": [],
    "bids": [],
    "innovation_carriers": [],
    "supply_chain_relations": [],
    "news": [],
    "statistics": [{}],
    "risk_flags": {},
}
```

---

## 4. 水位线机制

### 4.1 水位线表（增强版，含调度状态追踪）

```sql
-- 位于 gkxlumenx_cfg 库
CREATE TABLE IF NOT EXISTS gkxlumenx_cfg.es_sync_watermark (
    module_name       VARCHAR(64) PRIMARY KEY COMMENT '模块名（reg_info/tag_info/...）',
    source_table      VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'DWD 源表名',
    target_index      VARCHAR(64) NOT NULL DEFAULT 'gkx_enterprise_v1' COMMENT 'ES 目标物理索引（写）',
    time_field        VARCHAR(32) NOT NULL DEFAULT 'update_time' COMMENT '增量水位字段名',
    last_sync_time    DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '上次同步水位（增量 WHERE > 此值）',
    last_sync_count   INT NOT NULL DEFAULT 0 COMMENT '上次同步处理的行数',
    last_sync_cost_s  DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '上次同步耗时（秒）',
    sync_status       VARCHAR(16) NOT NULL DEFAULT 'idle' COMMENT '运行状态：idle/running/success/failed',
    update_mode       VARCHAR(16) NOT NULL DEFAULT 'incremental' COMMENT '上次同步模式：full/incremental',
    error_msg         TEXT COMMENT '失败时的错误信息（成功时清空）',
    begin_time        DATETIME DEFAULT NULL COMMENT '本次同步开始时间',
    end_time          DATETIME DEFAULT NULL COMMENT '本次同步结束时间',
    retry_count       INT NOT NULL DEFAULT 0 COMMENT '连续失败重试次数',
    is_active         TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用 0/1（禁用后不被调度）',
    updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ES 同步水位线 + 调度状态表';
```

相比基础水位线表，新增了以下调度状态字段：

| 字段 | 作用 |
|---|---|
| `source_table` | DWD 源表名，方便排查 |
| `target_index` | ES 目标物理索引（写） |
| `time_field` | 水位字段名（有 update_time 的表用 update_time；无则游标全量） |
| `sync_status` | 运行状态：idle/running/success/failed |
| `update_mode` | 全量/增量模式记录 |
| `error_msg` | 失败原因，成功时清空 |
| `begin_time` / `end_time` | 本次同步开始/结束时间 |
| `retry_count` | 连续失败次数，成功时重置为 0 |
| `is_active` | 禁用模块不参与调度 |

### 4.2 工作流程

```
1. 标记 sync_status = running，记录 begin_time
2. 读取本模块水位线 last_sync_time
3. 增量：把 [last_sync_time, now()] 切成 10 分钟一片；全量/首次：从 MIN(update_time) 起按 full_slice_days 切片，statistics 改用 org_id 游标
4. 逐片处理：
   a. WHERE update_time > slice_start AND update_time <= slice_end 查该片数据
   b. 按 org_id 聚合（一对多表）或逐行（一对一表）
   c. 批量 bulk update 写 ES（refresh=False）
   d. 推进水位线到 slice_end（sync_status 保持 running）
5. 全部片处理完后：
   - 统一 es.indices.refresh() 刷新一次
   - 更新水位线 = now()，sync_status = success，retry_count = 0
6. 失败：sync_status = failed，error_msg = 错误信息，retry_count += 1，水位线不推进
```

**时间分片设计**：增量同步不一次性查 24 小时数据，而是按 10 分钟一片逐片查询写入。每片处理完立即推进水位线，挂了重跑从上次水位线继续，不丢数据也不重复写。50 万行增量分成 144 片（24h / 10min），每片约 3500 行，内存可控。

**全量分片设计**：全量也禁止一次 `extract(None)`。有 `update_time` 的表从 `MIN(update_time)` 起按 `full_slice_days`（默认 1 天）切片，聚合模块在片内再按 `org_id` 分批回查；当前仅 `statistics` 无 DWD 时间字段，按 `org_id > last` 游标分页。索引不做删除重建，只创建/校验，异常由人工介入。

**refresh=False**：同步期间不逐批 refresh ES segment，全部写完后统一 refresh 一次。避免产生大量小 segment 导致 merge 压力。

每个模块独立读写自己的水位线，单模块失败不影响其他模块。`retry_count` 在成功时重置为 0，连续失败超过阈值可触发告警。

### 4.3 聚合模式 vs 一对一模式

基类 `SyncModule` 支持两种数据处理模式：

| 模式 | `is_aggregate` | 适用表 | 子类实现 | 基类处理 |
|---|---|---|---|---|
| 聚合模式 | `True`（默认） | 一对多表（bid/patent/finance/tag_info 等） | `build_aggregated_params(org_id, rows)` | 按 org_id 分组后调子类构建参数 |
| 一对一模式 | `False` | 一对一表（reg_info/statistics） | `build_params(row)` | 逐行调子类构建参数 |

子类不需要重写 `sync()`——基类统一管时间分片、状态追踪、批量写入、错误处理。

---

## 5. Painless Script 局部更新

### 5.1 更新方式

所有模块统一用 Painless stored script 做 partial update：

```python
# 1. 服务启动时预编译脚本
es.put_script(id="gkx_reg_info", body={
    "script": {"lang": "painless", "source": REG_INFO_SCRIPT}
})

# 2. 同步时 bulk update
helpers.bulk(es, [
    {
        "_op_type": "update",
        "_index": "gkx_enterprise_v1",  # 国内模块；国外模块写 gkx_enterprise_global_v1
        "_id": org_id,
        "script": {"id": "gkx_reg_info", "params": params},
        "upsert": params.get("_upsert", {}),  # reg_info 专用
    },
    ...
], raise_on_error=False, refresh=True)
```

### 5.2 脚本设计原则

| 场景 | 脚本写法 | 示例 |
|---|---|---|
| 顶层字段 | `ctx._source.field = params.field` | `ctx._source.name_cn = params.name_cn` |
| nested 数组 | `ctx._source.field = params.field`（整体替换） | `ctx._source.tags = params.tags` |
| 条件写入 | `if (params.containsKey('field'))` | 避免空值覆盖已有值 |

### 5.3 脚本清单

| script_id | 模块 | 说明 |
|---|---|---|
| `gkx_reg_info` | reg_info | 覆盖 40+ 顶层工商字段 + upsert |
| `gkx_tag_info` | tag_info | 覆盖 tags + tags_flat |
| `gkx_industry_chain` | industry_chain | 覆盖 industry_chains + 3 个 flat 字段 |
| `gkx_executive` | executive | 覆盖 executives |
| `gkx_finance` | finance | 覆盖 financials |
| `gkx_financing` | financing | 覆盖 financings |
| `gkx_bid` | bid | 覆盖 bids |
| `gkx_patent` | patent | 覆盖 patents |
| `gkx_innovation_carrier` | innovation_carrier | 覆盖 innovation_carriers |
| `gkx_invest` | invest | 覆盖 supply_chain_relations (投资) |
| `gkx_news` | news | 覆盖 news |
| `gkx_supply_chain` | supply_chain | 覆盖 supply_chain_relations (供应链) |
| `gkx_statistics` | statistics | 覆盖 statistics 聚合统计 |

---

## 6. 全量同步与索引维护

### 6.1 触发方式

- 手动调用 `POST /internal/etl/modules/sync-all?full=true`
- 或逐模块调用 `POST /internal/etl/modules/{module_name}/sync?full=true`

### 6.2 全量同步流程

全量同步按物理索引执行，共用别名只服务搜索/读。每个模块用 script upsert + partial update；有 `update_time` 的表按天切片，`statistics` 按 `org_id` 游标分页，绝不 `extract(None)` 一次拉全表。对于已存在的文档，script 会覆盖该模块的字段；对于新文档，upsert 创建初始文档。

```
1. POST /internal/etl/init              ← 建国内/国外物理索引 + 建水位表 + 注册 scripts
2. POST /internal/etl/modules/reg_info/sync?full=true&sync=true   ← 先跑国内 reg_info 创建文档
3. POST /internal/etl/modules/forg_reg_info/sync?full=true&sync=true ← 先跑国外 forg_reg_info 创建文档
4. POST /internal/etl/modules/sync-all?full=true&sync=true        ← 跑其余国内/国外模块
```

### 6.3 索引维护原则（mapping 变更时）

**索引只创建，不删除**。现有索引存在时 `POST /internal/etl/indexes/enterprise` / `enterprise-global` 只补别名/校验，不会删除索引；传 `recreate=true` 会返回错误，需要人工介入处理。

当确实需要变更 mapping 时，按以下人工流程处理：

1. 人工确认新索引名/新 mapping，创建新物理索引并绑定共用别名。
2. 新索引注册 scripts + 水位表。
3. 逐模块全量灌入新索引。
4. 数据校验通过后由人工调整别名，再下线旧索引。

`recreate` 参数仅保留为兼容旧调用，传入 `true` 会直接报错，不会发生删除。

别名 `gkx_enterprise` 同时指向 `gkx_enterprise_v1` 与 `gkx_enterprise_global_v1`，只用于搜索/读；ETL 写物理索引。重建单个物理索引时，可先将其移出共用别名，重建后再加回，避免共用别名整体不可用。多索引别名不能作为写目标。

---

## 7. API 接口

### 7.1 管理接口

| 接口 | 方法 | 说明 |
|---|---|---|
| `/healthz` | GET | 探活 + ES 状态 |
| `/internal/etl/status` | GET | ETL 任务状态（running/last_result/error） |
| `/internal/etl/jobs` | GET | 列出可用 ETL 任务 |
| `/internal/etl/modules` | GET | 列出 13 个国内模块 + 4 个国外模块 + 执行顺序 |
| `/internal/etl/watermarks` | GET | 查看所有模块水位线 |

### 7.2 执行接口

| 接口 | 方法 | 参数 | 说明 |
|---|---|---|---|
| `/internal/etl/init` | POST | `recreate=bool` | 建索引（create-only）+ 建水位表 + 注册 scripts |
| `/internal/etl/indexes/enterprise` | POST | `recreate=bool` | 创建/校验国内 ES 物理索引 `gkx_enterprise_v1`，不删除 |
| `/internal/etl/indexes/enterprise` | GET | - | 查看国内 ES 物理索引信息 |
| `/internal/etl/indexes/enterprise-global` | POST | `recreate=bool` | 创建/校验国外 ES 物理索引 `gkx_enterprise_global_v1`，不删除 |
| `/internal/etl/indexes/enterprise-global` | GET | - | 查看国外 ES 物理索引信息 |
| `/internal/etl/scripts/put` | POST | - | 注册所有 Painless scripts |
| `/internal/etl/modules/{name}/sync` | POST | `full=bool, sync=bool` | 触发单模块同步 |
| `/internal/etl/modules/sync-all` | POST | `full=bool, sync=bool` | 按顺序同步所有国内/国外模块 |
| `/internal/etl/enterprise` | POST | `full_refresh=bool, sync=bool` | 旧版全量入口（reg_info 独立） |
| `/internal/etl/listing-scale` | POST | `mode=ods|dwd|both, write_es=bool` | Q059 上市状态 + Q058 规上 派生同步 |

### 7.3 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `full` | false | true=全量（忽略水位线）；false=增量 |
| `sync` | false | true=同步执行（阻塞等待结果）；false=异步后台任务 |
| `recreate` | false | 已禁用删除；传 true 会返回错误，要求人工介入 |
| `full_refresh` | true | 旧版参数，已不再清空索引/文档，全量改为 script upsert 覆盖 |

---

## 8. 配置

### 8.1 settings.yaml

```yaml
mysql:
  host: 192.168.88.43
  port: 3306
  user: gkxlumenx
  password: GKX@Lumen2026
  dwd_db: gkxlumenx_dwd
  ods_db: gkxlumenx_ods

elasticsearch:
  hosts:
    - http://192.168.88.43:9200
  username: elastic
  password: htrfadmin
  verify_certs: false
  request_timeout: 60

etl:
  batch_size: 500
  full_slice_days: 1           # 全量时间片宽度（天），禁止一次拉全表
  enterprise_index: gkx_enterprise                # 别名（只用于搜索/读）
  enterprise_index_physical: gkx_enterprise_v1    # 国内实体索引（ETL 写）
  enterprise_index_global_physical: gkx_enterprise_global_v1  # 国外实体索引（ETL 写）
  number_of_shards: 1
  number_of_replicas: 0
  full_refresh: false          # 旧版参数已不再清空索引/文档
  watermark_db: gkxlumenx_cfg
  watermark_table: es_sync_watermark
```

### 8.2 环境变量覆盖

| 环境变量 | 说明 |
|---|---|
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` | MySQL 连接 |
| `MYSQL_DWD_DB` / `MYSQL_ODS_DB` | DWD/ODS 库名 |
| `ES_HOSTS` | ES 地址（逗号分隔） |
| `ES_USERNAME` / `ES_PASSWORD` | ES 认证 |
| `ETL_BATCH_SIZE` | 批量大小 |
| `ETL_FULL_SLICE_DAYS` | 全量时间片宽度（天） |
| `ETL_ENTERPRISE_INDEX` | ES 索引别名（搜索/读） |
| `ETL_ENTERPRISE_INDEX_PHYSICAL` | 国内 ES 实体索引名（ETL 写） |
| `ETL_ENTERPRISE_INDEX_GLOBAL_PHYSICAL` | 国外 ES 实体索引名（ETL 写） |

---

## 9. 部署

### 9.1 K8s 部署

```yaml
# k8s/dev-etl-es-py.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: etl-es-py
  namespace: dev
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: etl-es-py
          image: harbor.htmisoft.net/gkx-lumen/etl-es-py:latest
          ports:
            - containerPort: 8090
          env:
            - name: MYSQL_HOST
              value: "192.168.88.43"
            - name: ES_HOSTS
              value: "http://192.168.88.43:9200"
```

### 9.2 启动

```bash
# 本地开发
uvicorn app.main:app --host 0.0.0.0 --port 8090

# Docker
docker build -t etl-es-py .
docker run -p 8090:8090 etl-es-py
```

---

## 10. 首次初始化操作步骤

```bash
# 1. 确认 DWD 表有数据
mysql -h 192.168.88.43 -u gkxlumenx -p -e "SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base;"

# 2. 启动 ETL 服务
uvicorn app.main:app --host 0.0.0.0 --port 8090

# 3. 初始化（建国内/国外物理索引 + 水位表 + scripts）
curl -X POST http://localhost:8090/internal/etl/init

# 4. 国内首次全量：先跑 reg_info 创建文档
curl -X POST "http://localhost:8090/internal/etl/modules/reg_info/sync?full=true&sync=true"

# 5. 国内其余模块全量同步（可并行触发，各自只更新自己的字段）
curl -X POST "http://localhost:8090/internal/etl/modules/tag_info/sync?full=true&sync=true"
curl -X POST "http://localhost:8090/internal/etl/modules/industry_chain/sync?full=true&sync=true"
# ... 其余模块同理

# 6. 国内最后跑 statistics 聚合统计
curl -X POST "http://localhost:8090/internal/etl/modules/statistics/sync?full=true&sync=true"

# 7. 国外首次全量：forg_reg_info 先创建国外文档，其余国外模块可并行
curl -X POST "http://localhost:8090/internal/etl/modules/forg_reg_info/sync?full=true&sync=true"
curl -X POST "http://localhost:8090/internal/etl/modules/forg_executive/sync?full=true&sync=true"
curl -X POST "http://localhost:8090/internal/etl/modules/forg_finance/sync?full=true&sync=true"
curl -X POST "http://localhost:8090/internal/etl/modules/forg_relations/sync?full=true&sync=true"

# 8. 验证 ES 文档数（物理索引分别核对，别名确认 fan-out）
curl http://192.168.88.43:9200/gkx_enterprise_v1/_count
curl http://192.168.88.43:9200/gkx_enterprise_global_v1/_count
curl http://192.168.88.43:9200/gkx_enterprise/_count
```

## 10.1 日常增量调度（K8s CronJob）

每个国内/国外模块一个独立 CronJob，错开时间调用各自的增量同步 API：

```yaml
# reg_info 每日 02:00 增量同步
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etl-reg-info
  namespace: dev
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: trigger
              image: curlimages/curl
              command:
                - curl
                - -X
                - POST
                - "http://demo-platform-etl-es-py:8000/internal/etl/modules/reg_info/sync?full=false&sync=false"
          restartPolicy: OnFailure
---
# bid 每日 02:35 增量同步（数据量大的模块延后）
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etl-bid
  namespace: dev
spec:
  schedule: "35 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: trigger
              image: curlimages/curl
              command:
                - curl
                - -X
                - POST
                - "http://demo-platform-etl-es-py:8000/internal/etl/modules/bid/sync?full=false&sync=false"
          restartPolicy: OnFailure
---
# forg_reg_info 每日 03:10 增量同步（国外索引）
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etl-forg-reg-info
  namespace: dev
spec:
  schedule: "10 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: trigger
              image: curlimages/curl
              command:
                - curl
                - -X
                - POST
                - "http://demo-platform-etl-es-py:8000/internal/etl/modules/forg_reg_info/sync?full=false&sync=false"
          restartPolicy: OnFailure
---
# forg_relations 每日 03:30 增量同步（国外供应链/母子公司关系）
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etl-forg-relations
  namespace: dev
spec:
  schedule: "30 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: trigger
              image: curlimages/curl
              command:
                - curl
                - -X
                - POST
                - "http://demo-platform-etl-es-py:8000/internal/etl/modules/forg_relations/sync?full=false&sync=false"
          restartPolicy: OnFailure
```

国外模块写物理索引 `gkx_enterprise_global_v1`；国内模块写 `gkx_enterprise_v1`。共用别名 `gkx_enterprise` 仅用于搜索/读。

每个 CronJob 只做一件事：调用对应模块的增量同步 API。模块内部自己读水位线、查增量、写 ES、更新水位线。单模块失败不影响其他模块的 CronJob。

---

## 11. 与旧文档（v1.0）的主要变化

| 项 | v1.0（旧） | v2.1（新） |
|---|---|---|
| 数据源 | PostgreSQL ODS 层 | MySQL `gkxlumenx_dwd` 层 |
| 源表前缀 | `gkx_dwd_org_*` | `enterprise_*`（DWD 表名简化） |
| 模块数 | 17 个 | 13 个国内 + 4 个国外（新增 forg_reg_info/forg_executive/forg_finance/forg_relations） |
| 索引 | 1 个实体索引 | `gkx_enterprise_v1`（国内）+ `gkx_enterprise_global_v1`（国外）共用别名 `gkx_enterprise` |
| 写目标 | 别名/实体索引混用 | ETL 写物理索引；共用别名只用于搜索/读 |
| 专利表 | `gkx_ods_patent` | `enterprise_patent_history`（DWD 内） |
| 水位线存储 | PostgreSQL `ads.es_sync_watermark` | MySQL `gkxlumenx_cfg.es_sync_watermark` |
| 全量同步 | 别名切换 + Bulk index 全文档 | 有界时间分片（statistics 例外游标）+ script upsert；索引只创建不删除 |
| 调度 | APScheduler / K8s CronJob | FastAPI 异步任务 + API 手动触发 |
| ES 认证 | 无 | elastic / htrfadmin（xpack.security=true） |
| 并发控制 | asyncio.Semaphore(5) | 按顺序执行（sync-all）或手动并行（单模块触发） |

---

*v2.2：基于 lumen-etl-es-py 实际代码重写并补充国外模块。13 个国内模块 + 4 个国外模块从 MySQL DWD 同步到 ES，搜索读别名 `gkx_enterprise`，ETL 写物理索引，Painless script 局部更新，水位线独立管理。全量同步有界分批，索引 create-only。*
