# 12 — DWD → Elasticsearch 更新逻辑

> **读者**：GDF 了解边界与门禁；**实施写库** = `lumen-etl-es-py`，不是 GDF CDC、不是 Java/前端。  
> **真源**：`data-design/企业/企业搜索-ES更新机制.md`（v2.3）+ `storage/ENT/etl/pipeline-dwd-to-es.md`。  
> **本波补记（2026-09-02）**：财务 `financials.total_assets` / `total_liabilities` 取 DWD **最新一年年末时点存量**，不与收入同维。  
> **调度 cron / DAG 正式名**：`OPEN-ENT-FLOW-01` **未关**，下表「建议时刻」只是错峰参考，**禁止写进启动会当已上线 crontab**。

## 0. 一句话

DWD 验收通过后，`lumen-etl-es-py` 按**模块**独立增量：每模块自己的水位线 + 有界时间片 + Painless **局部更新**自己的字段。国内 `reg_info` / 国外 `forg_reg_info` 负责 **upsert 建文档**，其余模块只 partial update。失败**不切别名**到半成品索引。

GDF **不写 ES**。GDF 要保证 Wave A/B 产出的 ODS/DWD 能被下表模块抽到。

---

## 1. 目标库与别名

产线检索别名：**`gkx_enterprise`**（只读/搜索）。ETL **写物理索引**，不写多索引别名。

```text
别名 gkx_enterprise
  ├── gkx_enterprise_v1          国内，IK
  └── gkx_enterprise_global_v1   国外，standard
```

- mapping 字段结构一致，分词器不同。  
- `_id = org_id`。  
- 国内 `country_code=CHN` + `region_id`；国外填各国代码。  
- 禁止把 Demo ES / `demo_gkxlumenx_*` 当产线目标。

| 写库方 | 值 |
|--------|-----|
| 仓 | `${GKX_ROOT}/repos/lumen-etl-es-py` |
| CLI | `scripts/run_etl.py` · `scripts/create_enterprise_index.py` |
| 模块基类 | `SyncModule`（`extract` / `build_params` / `build_script`） |
| 内部 API | `/internal/etl/*`（只经 Java 调 Python） |
| 不做 | GDF 直写 ES；Java REST 写 ES；前端写 ES |

索引 mapping 细表仍以 `data-design/企业/企业搜索-ES索引设计.md` 为准，本卷不复制全文。司法类明细不灌 ES（只留 `risk_flags` / `risk_level` 等检索字段）。

---

## 2. 为什么按模块局部更新

全文档 PUT 会覆盖其他模块刚写的字段。Painless `ctx._source.xxx = params.xxx` 是文档级排队串行，各模块只碰自己的字段。

- **没有**「一个脚本更新全部 ES 维度」。  
- 13 个国内模块 + 4 个国外模块，各自独立调度、各自水位、互不覆盖。  
- 首次：国内 `reg_info` 先跑（建空 nested）；国外 `forg_reg_info` 先跑。其余可并行。`statistics` 最后。  
- 日常：各模块独立增量，不串行等待。

```
首次国内：reg_info → (并行其余 11) → statistics
首次国外：forg_reg_info → (并行 forg_executive / forg_finance / forg_relations)
日常：各模块独立 CronJob / 手动 /internal/etl/modules/{name}/sync
```

---

## 3. 模块注册表（更新谁、怎么更）

### 3.1 国内（写 `gkx_enterprise_v1`）

| 模块 | DWD 源表 | script_id | 更新的 ES 字段 | 方式 |
|------|----------|-----------|----------------|------|
| **reg_info** | `enterprise_base` + `enterprise_extra` | `gkx_reg_info` | 顶层工商 40+（含 `region_id`） | script + **upsert 建文档** |
| tag_info | `enterprise_tag` | `gkx_tag_info` | `tags` / `tags_flat` | script 整组替换 |
| industry_chain | `enterprise_industry_chain` | `gkx_industry_chain` | `industry_chains` + 3 个 flat | script |
| executive | `enterprise_executive` | `gkx_executive` | `executives` | script |
| finance | `enterprise_finance_history` | `gkx_finance` | `financials` | script；**资产/负债取最新一年年末存量** |
| financing | `enterprise_financing` | `gkx_financing` | `financings` | script |
| bid | `enterprise_bid` | `gkx_bid` | `bids` | script |
| patent | `enterprise_patent_history` | `gkx_patent` | `patents` | script |
| innovation_carrier | `enterprise_innovation_carrier` | `gkx_innovation_carrier` | `innovation_carriers` | script |
| invest | `enterprise_invest` | `gkx_invest` | `supply_chain_relations`（投资段） | script |
| news | `enterprise_news` | `gkx_news` | `news` | script |
| supply_chain | `enterprise_supply_chain` | `gkx_supply_chain` | `supply_chain_relations`（供应链段） | script |
| statistics | 多表聚合 | `gkx_statistics` | `statistics` | script；**无 `update_time`，按 `org_id` 游标** |

本波新增 DWD 表 **`enterprise_patent_org_rel` 不单独成 ES 模块**。ES `patents` 仍只吃 `enterprise_patent_history`。关系表给治理/图谱侧用，禁止为它另写一套 ES 脚本除非另出变更单。

### 3.2 国外（写 `gkx_enterprise_global_v1`）

| 模块 | DWD 源表 | script_id | 更新的 ES 字段 | 方式 |
|------|----------|-----------|----------------|------|
| **forg_reg_info** | `enterprise_forg_base` + `enterprise_forg_extra` | `gkx_forg_reg_info` | 顶层 `name_cn`/`name_en`/`country_code`… | script + **upsert** |
| forg_executive | `enterprise_forg_executive` | `gkx_forg_executive` | `executives` | script |
| forg_finance | `enterprise_forg_finance_history` | `gkx_forg_finance` | `financials` + statistics 最新员工/研发 | script |
| forg_relations | `enterprise_forg_invest` + `enterprise_forg_parent_subsidiary` | `gkx_forg_relations` | `supply_chain_relations` | script |

`dwd_forg_subsidiary_info` 现网缺失会阻塞 `enterprise_forg_parent_subsidiary` 洗数（见 `13`），进而阻塞 `forg_relations` 的母子段，不是改 ES 脚本能绕过的。

### 3.3 建议错峰（非正式 cron）

| 模块 | 时间字段 | 建议时刻（仅错峰） |
|------|----------|-------------------|
| reg_info | base 或 extra 的 `update_time` | 02:00 |
| tag_info … supply_chain | 各表 `update_time` | 02:10–03:00，错开 5 分钟 |
| statistics | 无；`org_id` 游标 | 03:30 |
| forg_reg_info | base 或 extra `update_time` | 03:10 |
| 其余国外 | `update_time` | 03:20–03:30 |

正式 DAG/crontab 名未关：`OPEN-ENT-FLOW-01`。

---

## 4. 水位线与增量

水位表：`gkxlumenx_cfg.es_sync_watermark`，**每个模块一行**。

关键列：`module_name`（PK）、`source_table`、`target_index`、`time_field`、`last_sync_time`、`sync_status`（idle/running/success/failed）、`update_mode`（full/incremental）、`retry_count`、`is_active`。

### 4.1 增量流程

```
1. sync_status = running，记 begin_time
2. 读本模块 last_sync_time
3. 增量：把 [last_sync_time, now()] 切成 10 分钟一片
   全量/首次：从 MIN(update_time) 起按 full_slice_days（默认 1 天）切片
   statistics：改用 org_id keyset 游标，禁止 extract(None) 拉全表
4. 逐片：
   a. WHERE update_time > slice_start AND update_time <= slice_end
   b. 一对多表按 org_id 聚合；一对一（reg_info/statistics）逐行
   c. bulk update（refresh=False）
   d. 水位推进到 slice_end
5. 全部片完成：统一 indices.refresh()；水位 = now()；success；retry_count=0
6. 失败：failed + error_msg；retry_count+1；**水位不推进**
```

一对多（bid/patent/finance/tag…）= `is_aggregate=true`，片内按 `org_id` 回查完整明细再整体替换 nested。一对一 = `is_aggregate=false`。

### 4.2 禁止

- `extract(None)` 一次拉全表。  
- 索引删除重建当日常增量（`recreate=true` 现网会报错，须人工换新物理索引再切别名）。  
- 半成品索引挂上 `gkx_enterprise`。  
- 用别名当写目标。

---

## 5. Painless 怎么更新

服务启动预编译 stored script，同步时 bulk：

```text
_op_type=update
_index=gkx_enterprise_v1 | gkx_enterprise_global_v1
_id=org_id
script.id=gkx_{module}
upsert= 仅 reg_info / forg_reg_info 带初始空 nested
```

| 场景 | 写法 |
|------|------|
| 顶层字段 | `ctx._source.field = params.field` |
| nested 数组 | 整组替换 `ctx._source.tags = params.tags` |
| 条件写 | `if (params.containsKey('field'))` 避免空值盖旧值 |

`reg_info` 首次 upsert 必须带空数组：`tags` / `industry_chains` / `executives` / `financials` / `financings` / `bids` / `innovation_carriers` / `supply_chain_relations` / `news` / `statistics=[{}]` / `risk_flags={}`，供后续模块 partial update。

### 5.1 reg_info 派生（写 ES 时算，不回写 DWD）

| ES 字段 | 逻辑 |
|---------|------|
| `operating_status` | 注销 / 迁出 / 吊销 / 在营 |
| `enterprise_scale` | 优先 DWD `org_size`；否则注册资本兜底 |
| `listing_status` | Q059 |
| `is_above_scale` | 营收万元 ≥ 2000（Q058） |
| `registered_capital_value` | DWD 万元 → ES 元（×10000） |
| `incorporation_year` | 注册日前年 |
| `addr_lng` / `addr_lat` | 优先总部，兜底 extra |

### 5.2 本波财务口径（覆盖旧「收入同维」误解）

- 收入 / 利润类 = **期间流量**。  
- `total_assets` / `total_liabilities` = **年末时点存量**，取 DWD 该企业**最新一年**一行写入 `financials`。  
- **不能**用营收推总资产。源 ODS 有列才洗进 DWD；DWD 没有这两列则 ES 不得编造。

---

## 6. 全量与 mapping 变更

触发：`POST /internal/etl/modules/{name}/sync?full=true` 或 `sync-all?full=true`。

建议顺序：

1. `POST /internal/etl/init` — 建/校验物理索引 + 水位表 + 注册 scripts（**不删索引**）  
2. 国内 `reg_info` full  
3. 国外 `forg_reg_info` full  
4. `sync-all` 其余模块  

mapping 要变：人工建新物理索引 → 灌数校验 → 再改别名 → 下线旧索引。禁止日常 DROP。

常用只读/执行接口：`/internal/etl/status` · `/modules` · `/watermarks` · `/modules/{name}/sync` · `/modules/sync-all`。`sync=false` 异步；`full=false` 走水位。

---

## 7. 门禁（对 GDF / 对 ETL）

1. Wave B 对应 DWD 表验收通过后才允许该模块 bulk。  
2. 失败不发布半成品索引。  
3. ADS / 指标权威不因 ES 失败被改写。  
4. DWD 缺表/缺列按 `02` / `13` 书面阻塞，禁止 ETL 用 fixture 填 ES。  
5. `OPEN-ENT-FLOW-01`（cron/DAG 名）、`OPEN-ENT-FLOW-04`（SLA）保持独立，关闭不是本叶 DoD。

---

## 8. GDF 要做什么 / 不要做什么

- **要**：Wave A/B 产出带 `update_time` 的 DWD；`enterprise_base.region_id`、可空 `enterprise_code`、财务存量两列按 `10/` / `13` 具备；缺源书面报。  
- **不要**：GDF 作业连 ES；Java 检索服务补写索引；把 `enterprise_patent_org_rel` 当成必须灌 ES 的源。
