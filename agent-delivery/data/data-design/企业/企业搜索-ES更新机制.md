# 企业搜索 ES 更新机制设计

> **文档版本**：v1.0（重构增量更新机制：改为按源表独立模块并行同步 + Painless script 局部更新，各模块只碰自己的字段，互不覆盖）
> **日期**：2026-07-02
> **范围**：PostgreSQL ODS 层 → Elasticsearch `gkx_enterprise` 索引的数据同步机制
> **前置文档**：[企业搜索-ES索引设计.md](./企业搜索-ES索引设计.md)
> **原型页面**：`https://skxdemo.unicomcn.tech:30999/development/search`

---

## 0. 核心设计原则

### 0.1 为什么不用"收集 org_id → 重新查全部表 → 全文档写入"？

旧方案（v0.8 及之前）的增量逻辑是：
1. 扫描所有源表的增量，收集受影响的 `org_id` 集合
2. 对每个变更企业，按 `org_id` 重新查询全部 17 张源表，组装完整 ES 文档
3. Bulk `index`（全文档 PUT）写入 ES

**问题**：
- **一个字段变更导致全文档重写**：招投标表新增 100 条记录涉及 50 个企业 → 这 50 个企业的全部 17 张表数据被重新查询、重新组装、全文档覆盖写入。实际只有 `bids` 字段变了，其他 16 张表的数据完全没变。
- **大 nested 全文档重写更离谱**：企业有 3 万条 bids，新增 1 条 → GET 全文档（含 3 万条 bids）→ 改 bids → PUT 全文档。这正是 script 方案要解决的问题，但旧方案主流程还是全文档重写。
- **串行瓶颈**：所有源表变更检测 → 收集 org_id → 逐个组装 → 写入，是一个串行流水线，17 张表数据混在一起，任何一个慢了整体就慢。

### 0.2 新方案：按源表独立模块并行同步 + script 局部更新

**核心思想**：每个源表对应一个独立的同步模块（Sync Module），各自扫描自己源表的昨日增量数据，各自只更新 ES 文档中属于自己的字段，多模块并行跑。

```
┌──────────────────────────────────────────────────────────────────┐
│                     每日凌晨 02:00 触发                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ reg_info     │  │ tag_info     │  │ stock_base   │  ...      │
│  │ Sync Module  │  │ Sync Module  │  │ Sync Module  │  17个模块 │
│  │              │  │              │  │              │           │
│  │ 扫描昨日增量 │  │ 扫描昨日增量 │  │ 扫描昨日增量 │           │
│  │ 查自己的字段 │  │ 查自己的字段 │  │ 查自己的字段 │           │
│  │ script 更新  │  │ script 更新  │  │ script 更新  │           │
│  │ ES 的 reg_*  │  │ ES 的 tags   │  │ ES 的 stock  │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         └────────────────┬┴────────────────┘                    │
│                          ▼                                       │
│              ES gkx_enterprise 索引                              │
│         (各模块只写自己的字段，互不覆盖)                          │
│         refresh_interval = 30s (保持不变)                        │
└──────────────────────────────────────────────────────────────────┘
```

### 0.3 并发写同一文档会不会互相覆盖？

**不会**，前提是：**所有模块都用 Painless script 的 `ctx._source.xxx = params.xxx` 局部更新，而不是全文档 `index`（PUT）**。

- ES 的 `_update` with script 是**文档级锁定**的：同一文档的并发 update 请求会排队串行执行，不会交叉。
- 每个 script 只碰自己的字段（`ctx._source.bids`、`ctx._source.tags`、`ctx._source.name_cn`...），不碰其他字段，所以即使排队串行执行，也不会覆盖其他模块写入的字段。
- 如果两个模块同时更新同一个文档产生版本冲突（`version_conflict_engine_exception`），通过 `retry_on_conflict` 自动重试即可。

**为什么不能用全文档 `index`（PUT）？**
全文档 PUT 会用传入的 `_source` 完整覆盖文档。如果 reg_info 模块和 tag_info 模块同时 PUT 同一个企业，后写的会覆盖先写的，导致先写的字段丢失。**必须用 script 局部更新。**

### 0.4 refresh_interval 保持 30s 有没有问题？

**没有问题**，反而建议保持。

- `refresh_interval=30s` 意味着 ES 每 30 秒生成一个新的 Lucene segment，使新写入的数据可被搜索。
- 17 个模块并行写入，每个模块的写入量分散在 30 秒内，ES 的 indexing pressure 可控。
- 30s 的刷新间隔相比默认的 1s，**减少了 segment 生成频率**，降低 merge 压力，对批量写入更友好。
- 业务场景是 T+1 同步（凌晨跑完，白天查询），30s 的搜索可见延迟完全可接受。
- **不需要在同步期间临时调大 refresh_interval**（旧方案的 30s→1s 切换是多余的），直接保持 30s 即可。

---

## 1. 同步架构总览

### 1.1 整体数据流

```
┌─────────────┐                                               ┌──────────────────┐
│ PostgreSQL  │  ┌─ Module: reg_info ──────────────────────┐  │  Elasticsearch   │
│ ODS 层      │  │  扫描 reg_info 昨日增量 → script 更新    │  │  gkx_enterprise  │
│ ods.* 表    │  │  name_cn/province/... 等 reg_* 字段     │  │  索引             │
│             │  └─────────────────────────────────────────┘  │                  │
│ 每张表有    │  ┌─ Module: tag_info ──────────────────────┐  │  各模块只写      │
│ 自己的      │  │  扫描 tag_info 昨日增量 → script 更新    │  │  自己的字段      │
│ updated_time│  │  tags + statistics.tag_count            │  │  互不覆盖        │
│ 或          │  └─────────────────────────────────────────┘  │                  │
│ edw_data_   │  ┌─ Module: bid_info ──────────────────────┐  │  refresh_interval│
│ date        │  │  扫描 bid_info 昨日增量 → script 追加    │  │  = 30s (不变)    │
│             │  │  bids nested + statistics.bid_*         │  │                  │
│             │  └─────────────────────────────────────────┘  │                  │
│             │  ... (共 17 个独立模块，并行执行)             │                  │
└─────────────┘                                               └──────────────────┘
```

### 1.2 同步策略

| 策略 | 触发方式 | 适用场景 | 本期采用 |
|------|---------|---------|---------|
| **增量更新（按源表独立模块）** | 每日凌晨定时 | 日常数据同步，各源表各自增量 | ✅ Phase 1 主策略 |
| **全量重建** | 每周/手动 | mapping 变更、数据修复 | ✅ Phase 1 |
| **实时同步** | PG WAL → ES | 秒级延迟要求 | ⏳ Phase 2（可选） |
| **手动触发** | API 调用 | 紧急修复/数据回刷 | ✅ Phase 1 |

**Phase 1 主策略：每日凌晨 17 个独立模块并行增量更新 + 每周全量重建**

---

## 2. 增量更新机制（按源表独立模块）

### 2.1 同步模块清单

每个源表一个独立的 Sync Module，各自维护自己的水位线，各自只更新自己的 ES 字段：

| # | 模块名 | 源表 | 时间字段 | 更新的 ES 字段 | 更新方式 |
|---|--------|------|---------|---------------|---------|
| 1 | reg_info | gkx_dwd_org_reg_info | updated_time | name_cn, lerep, province, city, address, ... operating_status | script 覆盖 |
| 2 | tag_info | gkx_dwd_org_tag_info | updated_time | tags (nested), tags_flat | script 覆盖 + statistics.tag_count |
| 3 | stock_base | gkx_dwd_org_stock_base | updated_time | stock_code, stock_noun, listing_status, ... | script 覆盖 |
| 4 | stock_finance | gkx_dwd_org_stock_finance_info | updated_time | stock_finance_latest | script 覆盖 + statistics.employees_number, research_development_amount |
| 5 | annual_financial | gkx_dwd_org_annual_financial_info | updated_time | financials (nested, 全部年份) | script 覆盖 + statistics.latest_revenue, latest_profit |
| 6 | product_info | gkx_dwd_org_org_product_info | updated_time | industry_class, main_activities, main_prod, description | script 覆盖 |
| 7 | executive_info | gkx_dwd_org_executive_info | updated_time | executives (nested) | script 覆盖 + statistics.executive_count |
| 8 | innovation_carrier | gkx_dwd_org_innovation_carrier | edw_data_date | innovation_carriers (nested) | script 覆盖 + statistics.innovation_carrier_count |
| 9 | industry_chain | gkx_dwd_org_industry_chain_dtl | updated_time | industry_chains (nested), *_flat, chain_position_text | script 覆盖 + statistics.industry_chain_count |
| 10 | company_abnormal | gkx_dwd_org_company_abnormal | edw_data_date | risk_flags.abnormal_count, risk_level | script 覆盖 |
| 11 | risk_shixin | gkx_dwd_org_risk_shixin | edw_data_date | risk_flags.shixin_count, risk_level | script 覆盖 |
| 12 | risk_zhixing | gkx_dwd_org_risk_zhixing | edw_data_date | risk_flags.zhixing_count, risk_level | script 覆盖 |
| 13 | invest_info | gkx_dwd_org_invest_info | updated_time | supply_chain_relations (投资部分) | script 覆盖 + statistics.invest_count |
| 14 | bid_info | gkx_dwd_org_bid_info | updated_time | bids (nested, 追加) + supply_chain_relations | **script 追加** + statistics.bid_total, bid_win_count |
| 15 | financing_info | gkx_dwd_org_financing_info | updated_time | financings (nested) | script 覆盖 + statistics.financing_count, financing_total_amount |
| 16 | important_news | gkx_dwd_org_important_news_info | updated_time | news (nested) | script 覆盖 + statistics.news_count |
| 17 | patent | gkx_ods_patent | publication_date | patents (nested, 追加) | **script 追加** + statistics.patent_total, patent_valid, patent_citation_total |

> **注**：ai-service 评分结果（competitiveness_score）作为第 18 个模块，由 ai-service 自行推送，不在 ETL 调度内。

### 2.2 水位线机制（每模块独立）

每个模块维护自己的水位线，互不干扰：

```sql
-- 水位线存储表
CREATE TABLE ads.es_sync_watermark (
    module_name     VARCHAR(50) PRIMARY KEY,   -- 'reg_info', 'bid_info', ...
    source_table    VARCHAR(100),
    time_field      VARCHAR(50),                -- 'updated_time' 或 'edw_data_date'
    last_sync_time  TIMESTAMP,
    last_sync_count INTEGER,
    sync_status     VARCHAR(20),                -- running/success/failed
    updated_at      TIMESTAMP DEFAULT now()
);
```

```python
# 每个模块各自读写自己的水位线
class SyncModule:
    def __init__(self, name: str, source_table: str, time_field: str):
        self.name = name  # 'reg_info', 'bid_info', ...
        self.source_table = source_table
        self.time_field = time_field

    def get_watermark(self) -> datetime:
        """读取本模块的水位线"""
        return query_watermark(self.name)

    def update_watermark(self, sync_time: datetime, count: int):
        """更新本模块的水位线"""
        upsert_watermark(self.name, sync_time, count)
```

### 2.3 单个模块的执行流程

每个模块的执行逻辑完全独立、完全相同：

```
┌─ Module: {module_name} ──────────────────────────────────────┐
│                                                              │
│  1. 读取本模块水位线 last_sync_time                           │
│     ↓                                                        │
│  2. 扫描源表增量数据                                          │
│     SELECT ... FROM {source_table}                           │
│     WHERE {time_field} > :last_sync                          │
│       AND {time_field} <= :now                               │
│     ↓                                                        │
│  3. 按 org_id 分组（无 org_id 的表 JOIN reg_info 映射）       │
│     {org_id: [record1, record2, ...], ...}                  │
│     ↓                                                        │
│  4. 对每个 org_id，组装本模块负责的 ES 字段值                 │
│     （只组装自己的字段，不碰其他字段）                         │
│     ↓                                                        │
│  5. 调用预编译的 Painless script，局部更新 ES 文档            │
│     POST gkx_enterprise/_update/{org_id}?retry_on_conflict=3 │
│     { "script": {"id": "{module_name}_script", "params":...}}│
│     ↓                                                        │
│  6. 更新本模块水位线 = now                                    │
│     ↓                                                        │
│  7. 记录本模块同步日志（成功/失败数、耗时）                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 2.4 调度执行方式

17 个模块**并行执行**，可用 Python `asyncio` 或 K8s CronJob 并行 Pod：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 17 个模块定义
MODULES = [
    SyncModule("reg_info",          "gkx_dwd_org_reg_info",            "updated_time"),
    SyncModule("tag_info",          "gkx_dwd_org_tag_info",            "updated_time"),
    SyncModule("stock_base",        "gkx_dwd_org_stock_base",          "updated_time"),
    SyncModule("stock_finance",     "gkx_dwd_org_stock_finance_info",  "updated_time"),
    SyncModule("annual_financial",  "gkx_dwd_org_annual_financial_info","updated_time"),
    SyncModule("product_info",      "gkx_dwd_org_org_product_info",    "updated_time"),
    SyncModule("executive_info",    "gkx_dwd_org_executive_info",      "updated_time"),
    SyncModule("innovation_carrier","gkx_dwd_org_innovation_carrier",  "edw_data_date"),
    SyncModule("industry_chain",    "gkx_dwd_org_industry_chain_dtl",  "updated_time"),
    SyncModule("company_abnormal",  "gkx_dwd_org_company_abnormal",    "edw_data_date"),
    SyncModule("risk_shixin",       "gkx_dwd_org_risk_shixin",         "edw_data_date"),
    SyncModule("risk_zhixing",      "gkx_dwd_org_risk_zhixing",        "edw_data_date"),
    SyncModule("invest_info",       "gkx_dwd_org_invest_info",         "updated_time"),
    SyncModule("bid_info",          "gkx_dwd_org_bid_info",            "updated_time"),
    SyncModule("financing_info",    "gkx_dwd_org_financing_info",      "updated_time"),
    SyncModule("important_news",    "gkx_dwd_org_important_news_info", "updated_time"),
    SyncModule("patent",            "gkx_ods_patent",                  "publication_date"),
]

async def run_all_modules():
    """凌晨 02:00 触发，17 个模块并行执行"""
    # 控制并发数，避免 PG 连接数和 ES 写入压力过大
    semaphore = asyncio.Semaphore(5)  # 最多 5 个模块同时跑

    async def run_one(module: SyncModule):
        async with semaphore:
            try:
                await module.run()  # 执行该模块的完整流程
                logger.info(f"Module {module.name} done")
            except Exception as e:
                logger.error(f"Module {module.name} failed: {e}")
                # 单模块失败不影响其他模块

    await asyncio.gather(*[run_one(m) for m in MODULES])
    logger.info("All modules finished")
```

**为什么并发数控制在 5 而不是 17 全开？**
- PG 连接池限制：每个模块需要查 PG，17 个全开会打满连接池
- ES indexing pressure：虽然各模块写不同字段，但同时大量 update 会增加 ES 写入队列压力
- 5 并发已经能保证大部分模块并行，整体耗时由最慢的模块（通常是 bid_info/patent）决定

### 2.5 并发冲突处理

多个模块同时更新同一个 ES 文档时，ES 会排队串行执行（文档级锁），可能产生版本冲突：

```python
# 每个模块的 ES 更新都带 retry_on_conflict
es_client.update(
    index="gkx_enterprise",
    id=org_id,
    body={
        "script": {
            "id": f"{module_name}_script",  # 预编译脚本 ID
            "params": module_params
        }
    },
    retry_on_conflict=5  # 冲突自动重试 5 次
)
```

- `retry_on_conflict=5`：ES 检测到版本冲突后，自动重新读取文档最新版本，重新执行 script，最多重试 5 次。
- 因为每个 script 只碰自己的字段，重试不会导致数据错误。
- 正常情况下冲突率很低（只有当两个模块恰好同时更新同一个企业时才冲突），5 次重试足够。

---

## 3. Painless Script 局部更新（各模块）

### 3.1 更新方式分类

| 类型 | 模块 | 更新方式 | 理由 |
|------|------|---------|------|
| **顶层字段覆盖** | reg_info, stock_base, stock_finance, product_info | script: `ctx._source.xxx = params.xxx` | 字段少，直接覆盖 |
| **小 nested 覆盖** | tag_info, executive_info, innovation_carrier, industry_chain, financings, news, invest_info | script: `ctx._source.xxx = params.xxx`（整个数组覆盖） | 单文档 nested 总数 < 500，全量覆盖开销可控 |
| **大 nested 追加** | bid_info, patent | script: 按 id 去重追加 | 可能几万条，只追加新增项 |
| **statistics 联动** | 所有模块 | script 内同步更新本模块负责的 statistics 字段 | 保持 statistics 与明细一致 |

### 3.2 顶层字段覆盖示例（reg_info 模块）

```json
POST gkx_enterprise/_update/<org_id>?retry_on_conflict=5
{
  "script": {
    "id": "reg_info_script",
    "params": {
      "name_cn": "深圳市腾讯计算机系统有限公司",
      "lerep": "马化腾",
      "province": "广东省",
      "city": "深圳市",
      "address": "深圳市南山区科技中一路腾讯大厦",
      "operating_status": "在营",
      "updated_time": "2026-07-01T10:00:00Z"
    }
  }
}
```

预编译脚本：

```python
es_client.put_script(id="reg_info_script", body={
    "script": {
        "lang": "painless",
        "source": """
            ctx._source.name_cn = params.name_cn;
            ctx._source.lerep = params.lerep;
            ctx._source.province = params.province;
            ctx._source.city = params.city;
            ctx._source.address = params.address;
            ctx._source.operating_status = params.operating_status;
            if (ctx._source.statistics != null && ctx._source.statistics.size() > 0) {
                ctx._source.statistics[0].last_updated = params.updated_time;
            }
        """
    }
})
```

### 3.3 小 nested 覆盖示例（tag_info 模块）

整个 tags 数组覆盖写入，同时更新 statistics.tag_count：

```python
es_client.put_script(id="tag_info_script", body={
    "script": {
        "lang": "painless",
        "source": """
            ctx._source.tags = params.tags;
            ctx._source.tags_flat = params.tags_flat;
            if (ctx._source.statistics == null) { ctx._source.statistics = [new HashMap()]; }
            if (ctx._source.statistics.size() == 0) { ctx._source.statistics.add(new HashMap()); }
            ctx._source.statistics[0].tag_count = params.tags.size();
        """
    }
})
```

调用：

```python
# 从 PG 查出该企业的所有标签
tags_data = [
    {"org_tag": "高新技术企业", "tag_level": "国家级"},
    {"org_tag": "专精特新", "tag_level": "省级"},
]
tags_flat = [t["org_tag"] for t in tags_data]

es_client.update(
    index="gkx_enterprise", id=org_id,
    body={"script": {"id": "tag_info_script", "params": {
        "tags": tags_data,
        "tags_flat": tags_flat
    }}},
    retry_on_conflict=5
)
```

### 3.4 大 nested 追加示例（bid_info 模块）

按 `id` 去重追加新增的招投标记录，同时更新 statistics：

```python
es_client.put_script(id="bid_info_script", body={
    "script": {
        "lang": "painless",
        "source": """
            if (ctx._source.bids == null) { ctx._source.bids = []; }
            def existingIds = new HashSet();
            for (def b : ctx._source.bids) { if (b.id != null) existingIds.add(b.id); }
            for (def newBid : params.newBids) {
                if (newBid.id != null && !existingIds.contains(newBid.id)) {
                    ctx._source.bids.add(newBid);
                    existingIds.add(newBid.id);
                }
            }
            if (ctx._source.statistics == null) { ctx._source.statistics = [new HashMap()]; }
            if (ctx._source.statistics.size() == 0) { ctx._source.statistics.add(new HashMap()); }
            def stat = ctx._source.statistics[0];
            stat.bid_total = ctx._source.bids.size();
            stat.bid_win_count = 0;
            for (def b : ctx._source.bids) { if (b.role == '中标方') stat.bid_win_count++; }
        """
    }
})
```

调用（扫描昨日 bid_info 增量，按 org_id 分组后追加）：

```python
# 1. 扫描昨日增量
new_bids = query("""
    SELECT
        CASE
            WHEN b.winner_social_credit_code = r.social_credit_code THEN r.org_id
            WHEN b.tender_social_credit_code = r.social_credit_code THEN r.org_id
        END AS org_id,
        b.id,
        CASE
            WHEN b.winner_social_credit_code = r.social_credit_code THEN '中标方'
            WHEN b.tender_social_credit_code = r.social_credit_code THEN '招标方'
        END AS role,
        b.announcement_title,
        b.created_time AS announcement_date
    FROM ods.gkx_dwd_org_bid_info b
    JOIN ods.gkx_dwd_org_reg_info r
      ON r.social_credit_code IN (b.winner_social_credit_code, b.tender_social_credit_code)
    WHERE b.updated_time > :last_sync AND b.updated_time <= :now
""")

# 2. 按 org_id 分组
bids_by_org = group_by(new_bids, key="org_id")

# 3. 每个 org_id 调用 script 追加
for org_id, bids in bids_by_org.items():
    es_client.update(
        index="gkx_enterprise", id=org_id,
        body={"script": {"id": "bid_info_script", "params": {"newBids": bids}}},
        retry_on_conflict=5
    )
```

### 3.5 大 nested 追加示例（patent 模块）

与 bid_info 同理，按 `id`（publication_number）去重追加：

```python
es_client.put_script(id="patent_script", body={
    "script": {
        "lang": "painless",
        "source": """
            if (ctx._source.patents == null) { ctx._source.patents = []; }
            def existingIds = new HashSet();
            for (def p : ctx._source.patents) { if (p.id != null) existingIds.add(p.id); }
            for (def newPat : params.newPatents) {
                if (newPat.id != null && !existingIds.contains(newPat.id)) {
                    ctx._source.patents.add(newPat);
                    existingIds.add(newPat.id);
                }
            }
            if (ctx._source.statistics == null) { ctx._source.statistics = [new HashMap()]; }
            if (ctx._source.statistics.size() == 0) { ctx._source.statistics.add(new HashMap()); }
            def stat = ctx._source.statistics[0];
            stat.patent_total = ctx._source.patents.size();
            stat.patent_valid = 0;
            stat.patent_citation_total = 0;
            for (def p : ctx._source.patents) {
                if (p.status == '有效') stat.patent_valid++;
                if (p.cited_by_nums != null) stat.patent_citation_total += p.cited_by_nums;
            }
        """
    }
})
```

### 3.6 风险模块联动更新（abnormal + shixin + zhixing → risk_level）

风险等级（risk_level）依赖 3 个风险模块的计数。处理方式：**每个风险模块更新自己的计数后，重新计算 risk_level**：

```python
es_client.put_script(id="risk_abnormal_script", body={
    "script": {
        "lang": "painless",
        "source": """
            if (ctx._source.risk_flags == null) { ctx._source.risk_flags = new HashMap(); }
            ctx._source.risk_flags.abnormal_count = params.abnormal_count;
            def shixin = ctx._source.risk_flags.containsKey('shixin_count') ? ctx._source.risk_flags.shixin_count : 0;
            def zhixing = ctx._source.risk_flags.containsKey('zhixing_count') ? ctx._source.risk_flags.zhixing_count : 0;
            def abnormal = params.abnormal_count;
            if (shixin > 0 || zhixing > 5) {
                ctx._source.risk_level = '高风险';
            } else if (zhixing > 0) {
                ctx._source.risk_level = '中风险';
            } else if (abnormal > 0) {
                ctx._source.risk_level = '低风险';
            } else {
                ctx._source.risk_level = '无风险';
            }
        """
    }
})
```

> shixin_script 和 zhixing_script 同理，各自更新自己的计数后重新计算 risk_level。因为 script 是文档级锁串行执行，所以读取到的其他风险计数一定是最新值。

### 3.7 脚本预编译清单

所有脚本在服务启动时预编译，避免每次请求都编译：

| 脚本 ID | 模块 | 说明 |
|---------|------|------|
| reg_info_script | reg_info | 覆盖基础信息 |
| tag_info_script | tag_info | 覆盖 tags + statistics.tag_count |
| stock_base_script | stock_base | 覆盖上市信息 |
| stock_finance_script | stock_finance | 覆盖 stock_finance_latest + statistics.employees_number |
| annual_financial_script | annual_financial | 覆盖 financials + statistics.latest_revenue/profit |
| product_info_script | product_info | 覆盖行业/产品信息 |
| executive_info_script | executive_info | 覆盖 executives + statistics.executive_count |
| innovation_carrier_script | innovation_carrier | 覆盖 innovation_carriers + statistics |
| industry_chain_script | industry_chain | 覆盖 industry_chains + flat + statistics |
| risk_abnormal_script | company_abnormal | 更新 abnormal_count + 重算 risk_level |
| risk_shixin_script | risk_shixin | 更新 shixin_count + 重算 risk_level |
| risk_zhixing_script | risk_zhixing | 更新 zhixing_count + 重算 risk_level |
| invest_info_script | invest_info | 覆盖 supply_chain_relations(投资) + statistics.invest_count |
| bid_info_script | bid_info | **追加** bids + statistics.bid_total/win_count |
| financing_info_script | financing_info | 覆盖 financings + statistics.financing_count/total |
| important_news_script | important_news | 覆盖 news + statistics.news_count |
| patent_script | patent | **追加** patents + statistics.patent_total/valid/citation |

---

## 4. 全量重建机制

### 4.1 触发时机

- 每周日凌晨 03:00 定时触发
- ES mapping 变更后手动触发
- 数据修复后手动触发

### 4.2 零停机重建流程

利用别名机制实现零停机：

```
1. 当前状态：
   gkx_enterprise (别名) → gkx_enterprise_v1 (索引)

2. 创建新索引：
   PUT gkx_enterprise_v2  ← 使用最新 mapping

3. 全量灌数据（按模块顺序组装完整文档）：
   遍历所有企业 org_id → 按 §5 完整组装 SQL 查全部 17 张表
   → 组装完整 ES 文档 → Bulk 写入 gkx_enterprise_v2
   （全量重建时用 Bulk index 全文档写入，不用 script）

4. 切换别名：
   POST _aliases
   { "actions": [
     { "remove": { "index": "gkx_enterprise_v1", "alias": "gkx_enterprise" }},
     { "add":    { "index": "gkx_enterprise_v2", "alias": "gkx_enterprise" }}
   ]}

5. 删除旧索引：
   DELETE gkx_enterprise_v1
```

> **注意**：全量重建用 Bulk `index`（全文档 PUT），因为是新索引不存在并发覆盖问题。增量更新用 script 局部更新，因为有并发。两种方式适用场景不同。

### 4.3 全量灌数据策略

千万级数据需并行灌入，按 `org_id` 哈希分批：

```python
BATCH_SIZE = 1000
PARALLEL_WORKERS = 3

def full_rebuild():
    all_org_ids = query_all_org_ids_cursor()  # PG 游标

    batch = []
    for org_id in all_org_ids:
        doc = build_es_document(org_id)  # 按 §5 完整组装
        batch.append({"_index": "gkx_enterprise_v2", "_id": org_id, "_source": doc})
        if len(batch) >= BATCH_SIZE:
            helpers.bulk(es_client, batch, chunk_size=500, max_retries=3)
            batch = []
    if batch:
        helpers.bulk(es_client, batch, chunk_size=500, max_retries=3)

    es_client.indices.forcemerge(index="gkx_enterprise_v2", max_num_segments=1)
```

---

## 5. 各模块源表查询 SQL

> **与旧方案的区别**：旧方案是"单企业完整文档组装 SQL"（17 个子查询拼一个完整文档）。新方案下，每个模块有自己的查询 SQL，只查自己需要的字段。

### 5.1 reg_info 模块

```sql
SELECT org_id, social_credit_code, name_cn, lerep,
       province, city, address, addr_lng, addr_lat,
       postal_code, incorporation_year, incorporation_date,
       start_date, end_date, listing_status, listing_date,
       registered_capital_value, capital_currency_code, registration_org,
       updated_time
FROM ods.gkx_dwd_org_reg_info
WHERE updated_time > :last_sync AND updated_time <= :now;
-- ETL 推导 operating_status: end_date 为空/未来=在营, 否则=注销
```

### 5.2 tag_info 模块

```sql
SELECT t.social_credit_code, r.org_id, t.org_tag, t.tag_level
FROM ods.gkx_dwd_org_tag_info t
JOIN ods.gkx_dwd_org_reg_info r ON t.social_credit_code = r.social_credit_code
WHERE t.updated_time > :last_sync AND t.updated_time <= :now;
-- ETL 按 org_id 分组，组装 tags 数组 + tags_flat
```

### 5.3 bid_info 模块（大 nested 追加）

```sql
SELECT
    r.org_id,
    b.id,
    CASE
        WHEN b.winner_social_credit_code = r.social_credit_code THEN '中标方'
        WHEN b.tender_social_credit_code = r.social_credit_code THEN '招标方'
    END AS role,
    b.announcement_title,
    CASE
        WHEN b.winner_social_credit_code = r.social_credit_code THEN b.tender_name_cn
        WHEN b.tender_social_credit_code = r.social_credit_code THEN b.winner_name_cn
    END AS counterparty_name,
    b.created_time AS announcement_date
FROM ods.gkx_dwd_org_bid_info b
JOIN ods.gkx_dwd_org_reg_info r
  ON r.social_credit_code IN (b.winner_social_credit_code, b.tender_social_credit_code)
WHERE b.updated_time > :last_sync AND b.updated_time <= :now;
-- ETL 按 org_id 分组，调用 bid_info_script 追加
```

### 5.4 patent 模块（大 nested 追加）

```sql
-- ⚠️ 专利表 current_assignee 是文本，需先通过"机构名→统一社会信用代码"映射表关联
SELECT
    r.org_id,
    p.publication_number AS id,
    p.title_localized AS title,
    p.abstract_localized AS abstract,
    p.kind_code AS patent_type,
    p.status, p.legal_status,
    p.filing_date, p.publication_date, p.grant_date,
    p.filing_year, p.grant_year,
    p.citation_nums, p.cited_by_nums,
    p.ipc, p.cpc, p.inventor
FROM ods.gkx_ods_patent p
JOIN ods.gkx_dwd_org_reg_info r ON p.current_assignee = r.name_cn
WHERE p.publication_date > :last_sync AND p.publication_date <= :now;
-- ETL 按 org_id 分组，调用 patent_script 追加
```

### 5.5 annual_financial 模块

```sql
SELECT f.social_credit_code, r.org_id,
       f.year, f.total_assets, f.total_liabilities, f.operating_revenue,
       f.main_business_revenue, f.total_profit, f.pure_profit,
       f.total_tax_paid, f.total_fixed_assets
FROM ods.gkx_dwd_org_annual_financial_info f
JOIN ods.gkx_dwd_org_reg_info r ON f.social_credit_code = r.social_credit_code
WHERE f.updated_time > :last_sync AND f.updated_time <= :now
ORDER BY f.year DESC;
-- ETL 按 org_id 分组，组装 financials 数组（全部年份）
-- 同时预计算 statistics.latest_revenue = financials[0].operating_revenue
```

### 5.6 financing_info 模块

```sql
SELECT fi.social_credit_code, r.org_id,
       fi.funding_round, fi.funding_amount, fi.funding_currency_code,
       fi.post_valuation, fi.completion_date, fi.investors_name
FROM ods.gkx_dwd_org_financing_info fi
JOIN ods.gkx_dwd_org_reg_info r ON fi.social_credit_code = r.social_credit_code
WHERE fi.updated_time > :last_sync AND fi.updated_time <= :now
ORDER BY fi.completion_date DESC;
```

### 5.7 风险模块（abnormal / shixin / zhixing）

```sql
-- abnormal 模块：扫描增量，全量重查该企业的异常计数
SELECT r.org_id,
       (SELECT count(*) FROM ods.gkx_dwd_org_company_abnormal a
        WHERE a.social_credit_code = r.social_credit_code) AS abnormal_count
FROM ods.gkx_dwd_org_company_abnormal a
JOIN ods.gkx_dwd_org_reg_info r ON a.social_credit_code = r.social_credit_code
WHERE a.edw_data_date > :last_sync AND a.edw_data_date <= :now
GROUP BY r.org_id;
-- shixin / zhixing 同理，用全量重查计数确保 statistics 准确
```

### 5.8 其他模块

其余模块（stock_base, stock_finance, product_info, executive_info, innovation_carrier, industry_chain, invest_info, important_news）查询模式相同：扫描自己源表的昨日增量，JOIN reg_info 拿到 org_id，按 org_id 分组后组装自己的 ES 字段。

### 5.9 全量重建时的完整文档组装

全量重建时需要组装完整文档（17 个子查询拼一个文档），核心区别在于：**全量重建用 Bulk index 全文档写入新索引，增量更新用 script 局部更新现有索引**。

---

## 6. 调度与监控

### 6.1 调度配置

```yaml
sync_jobs:
  - name: enterprise_incremental_sync
    schedule: "0 2 * * *"
    type: incremental_parallel
    modules: 17
    max_concurrency: 5
    timeout: 3600s
    retry_per_module: 3
    on_failure: alert_pm

  - name: enterprise_full_rebuild
    schedule: "0 3 * * 0"
    type: full
    timeout: 7200s
    retry: 1
    on_failure: alert_architect

  - name: manual_sync
    type: on_demand
    endpoint: POST /internal/sync/enterprise
    params: [mode=incremental|full, module=<module_name>, codes=[]]
```

### 6.2 监控指标

| 指标 | 采集方式 | 告警阈值 |
|------|---------|---------|
| 各模块同步耗时 | 模块日志 | 单模块 > 30min 告警 |
| 各模块增量记录数 | 模块日志 | 突增 >10倍 告警 |
| 各模块失败数 | 模块日志 | >0 告警 |
| ES 文档总数 | `_count` API | 下降 >5% 告警 |
| 各模块水位线延迟 | 对比 now - last_sync | >25h 告警 |
| ES 索引大小 | `_stats` API | 监控趋势 |
| ES 查询延迟 | Slow log | >1s 告警 |
| ES 版本冲突数 | `_stats` indexing | 突增告警 |

### 6.3 健康检查

```python
# GET /internal/sync/health
{
  "status": "healthy",
  "modules": {
    "reg_info": {"last_sync": "2026-07-02T02:00:00Z", "count": 152, "status": "success"},
    "bid_info": {"last_sync": "2026-07-02T02:05:00Z", "count": 1240, "status": "success", "duration_sec": 320},
    "patent":   {"last_sync": "2026-07-02T02:08:00Z", "count": 567, "status": "success", "duration_sec": 480}
  },
  "es_index": {"doc_count": 1574, "size_mb": 45.2}
}
```

---

## 7. 错误处理

### 7.1 单模块失败不影响其他模块

```python
async def run_one(module: SyncModule):
    async with semaphore:
        try:
            await module.run()
        except Exception as e:
            logger.error(f"Module {module.name} failed: {e}")
            record_module_failure(module.name, str(e))
```

### 7.2 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| PG 查询超时 | 增量数据量大 | 加索引；分批查；超时 60s |
| ES 版本冲突 | 多模块同时写同一文档 | retry_on_conflict=5 自动重试 |
| ES 连接拒绝 | ES 线程池满 | 指数退避重试 3 次；降低并发数 |
| 水位线丢失 | 水位线表被清 | 回退到 `now() - interval '2 days'` |
| 专利名称映射缺失 | assignee 未清洗 | 跳过专利模块，其余正常 |
| 单模块全失败 | 源表结构变更等 | 记录失败，次日手动重跑该模块 |

---

## 8. 数据一致性保障

| 场景 | 一致性 | 说明 |
|------|--------|------|
| 每日增量同步 | **最终一致**（T+1） | 凌晨 02:00 各模块并行同步前一天的变更 |
| 全量重建 | **最终一致**（T+1） | 每周日全量校准 |
| 手动触发 | **准实时**（秒级） | 指定企业立即同步 |
| 实时同步（Phase 2） | **近实时**（秒级延迟） | PG WAL → ES |

---

## 9. 部署架构

```
gkx-search-service（FastAPI）
├── app/
│   ├── api/                       # REST API
│   │   ├── search.py              # 搜索接口
│   │   ├── detail.py              # 详情接口
│   │   └── sync.py                # 同步管理接口
│   ├── sync/                      # 同步模块
│   │   ├── modules/               # 17 个独立模块
│   │   │   ├── base.py            # SyncModule 基类
│   │   │   ├── reg_info.py
│   │   │   ├── tag_info.py
│   │   │   ├── bid_info.py        # script 追加
│   │   │   ├── patent.py          # script 追加
│   │   │   └── ...                # 其余 13 个模块
│   │   ├── full_rebuild.py        # 全量重建
│   │   ├── watermark.py           # 水位线管理
│   │   └── scheduler.py           # 调度器（APScheduler）
│   ├── es/                        # ES 客户端
│   │   ├── client.py              # ES 连接
│   │   ├── scripts.py             # Painless 脚本预编译
│   │   ├── queries.py             # 查询模板
│   │   └── index_manager.py       # 索引/别名管理
│   └── config.py                  # 配置
├── requirements.txt
└── Dockerfile
```

---

## 10. 性能预估

| 指标 | 测试库（1574 企业） | 生产预估（~1500 万企业） |
|------|-------------------|-------------------|
| 单模块扫描增量 | ~1s | ~5-30min（取决于增量量） |
| 17 模块并行总耗时 | ~15s | ~30-60min（受最慢模块限制，通常 bid/patent） |
| script 局部更新 | ~3ms/企业 | ~5-20ms/企业 |
| 全量重建 | ~80s | ~8-12h（并行灌入） |
| ES 版本冲突率 | <0.1% | <1%（凌晨低峰期） |
| ES 搜索延迟（_source 过滤） | <10ms | <100ms |
| ES 索引大小 | ~100MB | ~60-120GB |

### 10.1 为什么新方案更快？

| 对比项 | 旧方案（全文档重写） | 新方案（script 局部更新） |
|--------|-------------------|------------------------|
| 增量检测 | 17 张表串行扫描 | 17 张表并行扫描 |
| 数据组装 | 每个变更企业查全部 17 张表 | 每个模块只查自己的 1 张表 |
| ES 写入 | 全文档 index（含未变更字段） | script 只写变更字段 |
| 大 nested | GET 全文档 → 改 → PUT 全文档 | script 追加新增项（无需读全文档） |
| 模块间依赖 | 串行，一个慢全慢 | 并行，互不依赖 |
| 单模块失败 | 全部回滚 | 只该模块失败，其余成功 |

### 10.2 单文档体积预估

| 企业类型 | nested 总量 | 文档体积 | 说明 |
|---------|------------|---------|------|
| 中小企业 | < 100 条 | 5-10 KB | bids/patents 少 |
| 中大型企业 | 500-5000 条 | 20-80 KB | 有一定量招投标/专利 |
| 大型企业 | 3万-8万 条 | 100-500 KB | bids 3万 + patents 5万 |

> 司法明细走 PG 不灌 ES，避免单文档膨胀到十几兆。

---

## 11. 待补充

- [ ] 实时同步（PG WAL）方案细化（Phase 2）
- [ ] ES 集群配置（分片/副本/内存/磁盘）
- [ ] IK + 拼音插件安装文档
- [ ] 智能检索 NL 解析的 prompt 模板（ai-service）
- [ ] 产业选项（13 项）→ 产业链数据映射

---

*v1.0：增量更新重构为按源表独立模块并行同步 + Painless script 局部更新。17 个模块各自扫描自己的源表增量，各自只更新自己的 ES 字段，互不覆盖。refresh_interval 保持 30s 不变。全量重建仍用 Bulk index 全文档写入新索引。*
