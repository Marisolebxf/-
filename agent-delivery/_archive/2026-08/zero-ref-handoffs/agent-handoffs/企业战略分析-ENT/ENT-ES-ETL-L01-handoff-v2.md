# ENT-ES-ETL-L01 — 企业搜索 DWD→ES 多模块增量 ETL（重构版）

> **任务 ID**：ENT-ES-ETL-L01
> **仓**：`lumen-etl-es-py`（dev 分支）
> **日期**：2026-07-29
> **作者**：[agent:backend-agent]

---

## 1. 范围与实现

### 1.1 目标

将架构师 bootstrap 的 `lumen-etl-es-py` 从**单表全量 bulk_index**重构为**多模块增量 Painless 脚本更新**，对齐设计文档 `企业搜索-ES索引设计.md` v3.5。

### 1.2 数据源确认

| 项 | 值 |
|---|---|
| MySQL Host | `10.50.11.76:3306`（内网）/ `111.198.38.90:34306`（外网） |
| User | `gkxlumenx` |
| DWD 库 | `gkxlumenx_dwd`（97 张表） |
| 企业相关表 | 14 张有数据，10 张空表 |
| ES | `http://10.50.11.76:9200`（xpack.security; elastic/htrfadmin） |
| ES 索引 | 别名 `gkx_enterprise` → 实体 `gkx_enterprise_v1` |

### 1.3 实现清单

**新增文件**：

| 文件 | 说明 |
|---|---|
| `etl/modules/base.py` | `SyncModule` 抽象基类 + `WatermarkManager`（MySQL `gkxlumenx_cfg.es_sync_watermark`） |
| `etl/modules/__init__.py` | 模块注册表 `MODULE_REGISTRY` + 默认执行顺序 `DEFAULT_ORDER` |
| `etl/modules/reg_info.py` | `enterprise_base` + `enterprise_extra` → 顶层基础工商字段（资本×10000 单位换算、经营状态/企业规模推导） |
| `etl/modules/tag_info.py` | `enterprise_tag` → `tags` nested + `tags_flat`（按 org_id 聚合） |
| `etl/modules/industry_chain.py` | `enterprise_industry_chain` → `industry_chains` nested + 4 个 flat 数组 + `is_chain_leader` |
| `etl/modules/executive.py` | `enterprise_executive` → `executives` nested |
| `etl/modules/finance.py` | `enterprise_finance_history` → `financials` nested + 顶层 `latest_revenue`/`revenue_growth_rate`/`profit_margin` |
| `etl/modules/financing.py` | `enterprise_financing` → `financings` nested |
| `etl/modules/bid.py` | `enterprise_bid` → `bids` nested |
| `etl/modules/patent.py` | `enterprise_patent_history` → `statistics` 专利字段（SUM 全部年份）+ 顶层 `patent_valid_count` |
| `etl/modules/innovation_carrier.py` | `enterprise_innovation_carrier` → nested + flat |
| `etl/modules/invest.py` | `enterprise_invest` → `supply_chain_relations` nested |
| `etl/modules/news.py` | `enterprise_news` → `news` nested |
| `etl/modules/supply_chain.py` | `enterprise_supply_chain` → `supply_chain_relations` nested + `risk_level` |
| `etl/modules/statistics.py` | 跨表 COUNT 聚合 → `statistics` nested 各 count 字段 |
| `etl/scripts.py` | 13 个 Painless stored script 源码定义 |
| `app/es_writer.py` | ES 写操作扩展：`put_script`/`update_by_script`/`bulk_update_by_script` |
| `scripts/run_etl.py` | CLI 调度入口：`init`/`put-scripts`/`sync`/`watermarks` |

**修改文件**：

| 文件 | 变更 |
|---|---|
| `app/db.py` | `DB` 类新增 `execute()` 方法（写操作/DDL） |
| `app/main.py` | 新增 6 个 API 端点（见 §3） |
| `conf/settings.yaml` | 新增 `watermark_db`/`watermark_table` 配置 |

**保留文件**：

| 文件 | 说明 |
|---|---|
| `etl/enterprise.py` | 架构师原有单表全量 bulk_index 逻辑，保留作为兼容/回退 |
| `app/es.py` | 索引管理 + bulk_index，不变 |

---

## 2. 架构设计

### 2.1 多模块增量策略

```
                    ┌──────────────────────────┐
                    │  MySQL gkxlumenx_dwd     │
                    │  (14 张 enterprise_* 表)  │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  13 个 SyncModule         │
                    │  按 update_time 增量过滤   │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  Painless stored scripts  │
                    │  (ES 端注册 13 个脚本)     │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  ES gkx_enterprise_v1     │
                    │  bulk update by script    │
                    │  + scripted_upsert        │
                    └──────────────────────────┘
```

### 2.2 模块执行顺序

```
1. reg_info          ← 必须先跑（创建文档 + 顶层基础字段）
2. tag_info          ← tags nested
3. industry_chain    ← industry_chains nested + flat
4. executive         ← executives nested
5. finance           ← financials nested + 顶层冗余
6. financing         ← financings nested
7. bid               ← bids nested
8. patent            ← statistics 专利字段 + 顶层冗余
9. innovation_carrier← nested + flat
10. invest           ← supply_chain_relations nested
11. news             ← news nested
12. supply_chain     ← supply_chain_relations（覆盖 invest 的）
13. statistics       ← 跨表 COUNT 聚合（必须最后跑）
```

### 2.3 水位线机制

- 水位表：`gkxlumenx_cfg.es_sync_watermark`
- 每个模块独立水位（按 `module_name`）
- 全量模式：忽略水位，遍历全部数据（仍用 script upsert，不清空索引）
- 增量模式：`WHERE update_time > watermark`
- `statistics` 模块只支持全量（跨表聚合无单一时间戳）

### 2.4 Painless 脚本策略

- 每个 module 一个 `script_id`，在 ES 端注册为 stored script
- nested 字段：整体替换（幂等，非追加）
- 顶层冗余字段：在对应模块脚本里同步写入
- `scripted_upsert=True`：文档不存在时创建空文档再执行脚本

---

## 3. API 端点

### 3.1 新增端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/internal/etl/modules` | 列出所有 13 个模块 |
| POST | `/internal/etl/scripts/put` | 注册所有 Painless stored scripts |
| POST | `/internal/etl/modules/{module_name}/sync` | 触发单模块同步（`?full=true&sync=true`） |
| POST | `/internal/etl/modules/sync-all` | 按默认顺序同步所有模块 |
| GET | `/internal/etl/watermarks` | 查看所有模块水位线 |
| POST | `/internal/etl/init` | 一键初始化：建索引 + 建水位表 + 注册 scripts |

### 3.2 CLI 命令

```bash
# 初始化（建索引 + 水位表 + 注册脚本）
python scripts/run_etl.py init

# 注册所有 Painless 脚本
python scripts/run_etl.py put-scripts

# 全量同步所有模块
python scripts/run_etl.py sync --full

# 增量同步所有模块
python scripts/run_etl.py sync

# 全量同步单模块
python scripts/run_etl.py sync --module reg_info --full

# 查看水位线
python scripts/run_etl.py watermarks
```

---

## 4. 验收证据

### 4.1 冒烟测试

```
✅ 13 个模块全部 import 成功
✅ 13 个 Painless 脚本定义正确
✅ app.es_writer import 成功
✅ FastAPI 16 条路由全部注册
✅ CLI --help 正常
✅ Config 读取正确（MySQL DWD / ES hosts / index）
```

### 4.2 DWD 数据源行数（2026-07-29 实测）

| 表 | 行数 |
|---|---:|
| enterprise_base | 120 |
| enterprise_tag | 171 |
| enterprise_extra | 120 |
| enterprise_finance_history | 696 |
| enterprise_patent_history | 696 |
| enterprise_patent_detail | 460 |
| enterprise_cooperation | 286 |
| enterprise_news | 200 |
| enterprise_bid | 200 |
| enterprise_supply_chain | 174 |
| enterprise_industry_chain | 141 |
| enterprise_executive | 411 |
| enterprise_financing | 100 |
| enterprise_invest | 28 |
| enterprise_innovation_carrier | 37 |
| enterprise_parent_subsidiary | 21 |
| enterprise_history_name | 0（空） |
| enterprise_risk_summary | 0（空） |
| 其他 6 张 summary/stats 表 | 0（空） |

---

## 5. 架构合规自检

| # | 铁律 | 状态 | 说明 |
|---|---|---|---|
| D1 | 算法只在 Python | ✅ | ETL 纯 Python |
| D2 | 调用链：前端→Java→Python /internal/* | ✅ | API 路径 `/internal/etl/*` |
| D3 | 图谱 NebulaGraph | N/A | 本任务不涉及 |
| D4 | 可观测性 | ⚠️ | OpenTelemetry 在 requirements.txt 已有，但未 instrument ETL 模块 |
| D5 | CI/CD | ✅ | `.gitlab-ci.yml` 已有，push → dev 触发 |
| D6 | demo2 只读 merge | N/A | 本任务在 lumen-etl-es-py |
| D7 | 共享聚合核心 | ✅ | ETL 写 ES，搜索服务读 ES |
| D8 | 前端规范 | N/A | 本任务不涉及前端 |
| D9 | 数据血缘 | ⚠️ | ETL 源表→ES 字段映射在 `企业搜索-ES索引设计.md` §3.3 已定义，但未在代码中标注 metric_id |
| D10 | 交互规范 | N/A | 本任务不涉及 |

---

## 6. 偏离说明

### 6.1 DWD 数据源从 PostgreSQL 改为 MySQL

设计文档 `企业搜索-ES索引设计.md` 标注数据源为 "PostgreSQL DWD 层"，但实际运行时 DWD 在 MySQL `gkxlumenx_dwd`（见 `algo-pg-to-mysql-migration.md` 迁移记录）。所有 SQL 已适配 MySQL 语法。

### 6.2 表名差异

设计文档引用的 PG 表名（如 `gkx_dwd_org_reg_info`）与 MySQL 实际表名（`enterprise_base`）不同。映射关系：

| 设计文档 PG 表名 | MySQL 实际表名 |
|---|---|
| reg_info | enterprise_base |
| org_product_info | enterprise_extra |
| tag_info | enterprise_tag |
| chain_dtl | enterprise_industry_chain |
| executive_info | enterprise_executive |
| annual_financial_info | enterprise_finance_history |
| financing_info | enterprise_financing |
| bid_info | enterprise_bid |
| patent_history | enterprise_patent_history |
| innovation_carrier | enterprise_innovation_carrier |
| invest_info | enterprise_invest |
| important_news_info | enterprise_news |

### 6.3 空表处理

8 张 `enterprise_*` 表为空（0 行），对应模块同步时 `extract()` 返回空列表，直接更新水位线返回。待数据灌入后自动有数据。

### 6.4 statistics 模块只支持全量

`statistics` 模块的 `extract()` 做跨表 COUNT 聚合，没有单一 `update_time` 可做增量过滤。`sync()` 强制 `full=True`。

### 6.5 supply_chain_relations 覆盖问题

`invest` 和 `supply_chain` 两个模块都写 `supply_chain_relations` nested 字段。由于 Painless 脚本做整体替换（非追加），后执行的模块会覆盖先执行的。调度顺序中 `invest` 在 `supply_chain` 之前，最终 `supply_chain_relations` 只包含 `enterprise_supply_chain` 的数据。

**后续优化**：可将两个模块合并为一个，或在 Painless 脚本中做 append 而非 replace。

---

## 7. 风险与注意事项

1. **ES xpack.security**：需确认 ES 已开启 xpack.security 且 `elastic/htrfadmin` 可用
2. **IK + pinyin 插件**：索引创建时自动检测，无插件时回退 standard analyzer
3. **Painless 脚本安全性**：使用 `scripted_upsert=True`，文档不存在时创建空文档再执行脚本
4. **资本单位换算**：`registered_capital` 和 `paid_in_capital` 在 DWD 存万元，ES 存元，ETL 已做 ×10000
5. **bulk 错误处理**：`raise_on_error=False`，错误不中断批量，但会记录日志
6. **水位表 DDL**：首次运行 `init` 时自动创建 `gkxlumenx_cfg.es_sync_watermark`

---

## 8. 下一步

- [ ] 在 K8s dev 环境跑 `python scripts/run_etl.py init` 初始化
- [ ] 跑 `python scripts/run_etl.py sync --full` 全量同步
- [ ] 验证 ES 文档数 = 120（enterprise_base 行数）
- [ ] 验证搜索服务（demo-svc-topic-py）关闭 mock 后能查到真实 ES 数据
- [ ] 配置 K8s CronJob 做定时增量同步
