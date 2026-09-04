# 12 — DWD → Elasticsearch 更新逻辑

> **读者**：GDF 了解边界与门禁；**实施写库** = `lumen-etl-es-py`，不是 GDF CDC、不是 Java/前端。  
> **真源**：`data-design/企业/企业搜索-ES更新机制.md`（v2.3）+ `storage/ENT/etl/pipeline-dwd-to-es.md`。  
> **本波补记（2026-09-02）**：财务各年 `financials.total_assets` / `total_liabilities` = 该年年末存量（万元，与 DWD 同口径）；列表取最新一年。禁止用营收推资产。  
> **调度**：日批由 **GDF 按表成功后触发模块**，不是本侧 crontab 当正式钟。握手见 [`15`](15-GDF触发调度与回执.md)：**当前用 §6.1**，§4 目标未上线。`OPEN-ENT-FLOW-01` **未关**。

## 0. 一句话

GDF 洗完该模块对应的 DWD 表 → **异步触发**该 ES 模块 → `lumen-etl-es-py` 按自己的水位 + Painless 局部更新 → **当前轮询 status 关单**（`15` §6.1）。国内 `reg_info` / 国外 `forg_reg_info` 负责 upsert 建文档，其余模块只碰自己的字段。GDF **不写 ES**，只调度。

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
| 内部 API | `/internal/etl/modules/{module}/sync`（只经 Java；`sync=false` 默认异步） |
| GDF 角色 | 表作业成功后触发模块；**当前**飞书值班 + 本侧转发 + 轮询 status（`15` §6.1）；目标才是 Java + callback |
| 不做 | GDF 直写 ES；GDF 直连 Python；Java 自己拼文档写 ES |

索引 mapping 细表仍以 `data-design/企业/企业搜索-ES索引设计.md` 为准，本卷不复制全文。司法类明细不灌 ES（只留 `risk_flags` / `risk_level` 等检索字段）。

---

## 2. 为什么按模块局部更新

全文档 PUT 会覆盖其他模块刚写的字段。Painless `ctx._source.xxx = params.xxx` 是文档级排队串行，各模块只碰自己的字段。

- **没有**「一个脚本更新全部 ES 维度」。  
- 13 个国内现网模块 + 4 个国外模块，各自水位、互不覆盖。另有 `former_names`（Q-WP3-14，`DATA-ENT-ES-FORMER-L01` **已写模块**；未跑 sync ≠ 代码未上）。  
- 首次：国内 `reg_info` 先跑（建空 nested）；国外 `forg_reg_info` 先跑。其余才能日批。`statistics` 最后。  
- **日常**：GDF **按模块分开触发**（§3 一行一次）。现网 Python 进程内单飞，未补 `OPEN-ENT-ETL-JOBID` 前不要并行打两个模块。

```
首次国内：reg_info(full) → 其他模块按表成功分别触发 → 日终 statistics
首次国外：forg_reg_info(full) → 其余国外模块按表成功分别触发
日常：GDF 表 success → 按 `15` §6.1 触发该行 module（async）→ 轮询 status；目标才走 callback
```

---

## 3. 模块触发清单（GDF 一行一枪，分开列）

每行 = 一个异步任务。GDF 只在「触发条件」满足后 POST 该 `module`。内部路径：`POST /internal/etl/modules/{module}/sync?full=false&sync=false`。对外路径见 `15`（未落号）。

**不触发**：`enterprise_patent_org_rel`（无 ES 模块）；司法明细表（ES 只留 risk 计数，走 `statistics`）；仅 ODS、未洗 DWD 的表。

### 3.1 国内 · 写 `gkx_enterprise_v1`（13 个，分开触发）

| # | module | GDF 洗完这些 DWD 才触发 | 更新的 ES | 写法 | 时长量级 | 备注 |
|---|--------|-------------------------|-----------|------|----------|------|
| 1 | `reg_info` | `enterprise_base` **且** `enterprise_extra` | 顶层工商（含 `region_id`） | script + **upsert 建文档** | 中 | **首次必须先于其他国内模块** |
| 2 | `tag_info` | `enterprise_tag` | `tags` / `tags_flat` | 整组替换 | 短 | |
| 3 | `industry_chain` | `enterprise_industry_chain` | `industry_chains` + flat | 整组替换 | 短 | |
| 4 | `executive` | `enterprise_executive` | `executives` | 整组替换 | 短 | |
| 5 | `finance` | `enterprise_finance_history` | `financials` | 整组替换 | 中 | 收入=期间；各年年末存量写入该年 `total_assets`/`total_liabilities`（万元，与 DWD 同口径） |
| 6 | `financing` | `enterprise_financing` | `financings` | 整组替换 | 中 | |
| 7 | `bid` | `enterprise_bid` | `bids` | 整组替换 | **长** | **Q-WP3-26**：读正式列 `bid_title`/`bid_amount`/`event_date`/`project_no`（`DATA-ENT-DWD-ALIGN-ETL-L01` 已改）。ES 仍写 `announcement_title`/`announcement_date`。表 success 后按 `15` §6.1 触发 |
| 8 | `patent` | `enterprise_patent_history` | `statistics` 专利计数 + 顶层冗余 | 字段覆盖 | 中 | **Q-WP3-16**：mapping 无 `patents` 字段；只写计数，明细留 DWD |
| 9 | `innovation_carrier` | `enterprise_innovation_carrier` | `innovation_carriers` + flat | 整组替换 | 短 | **本波不触发**：无三方源（`02` 已剔除 `dwd_org_innovation_carrier`）；ETL 模块保留，空表不灌 |
| 10 | `invest` | `enterprise_invest` | `supply_chain_relations` 投资段 | 按 `relation_type=投资方` 删补 | 中 | **Q-WP3-27**：读正式列 `inv_org_name`/`invest_amount`/`invest_ratio`（ETL 已改）。不 ADD `inv_external_id`。表 success 后按 `15` §6.1 触发 |
| 11 | `news` | `enterprise_news` | `news` | 整组替换 | 中 | **Q-WP3-25**：读正式列 `title`/`publish_time`/`summary`（ETL 已改）。`original_url` 已 ADD，现网 ES news 无对应键，不灌。表 success 后按 `15` §6.1 触发 |
| 12 | `supply_chain` | `enterprise_supply_chain` | `supply_chain_relations` 非投资段 | 保留投资段再合并 | 中 | **本波不触发（Q-WP3-18）**：无供应商-客户真源。股东不进本表。ETL 模块保留，空/mock 不灌 |
| 13 | `statistics` | 日终：上表相关模块回执 success | `statistics` + `risk_flags` 计数 | 字段覆盖；`org_id` 游标 | **长** | **不要当天第一枪** |
| 13a | `former_names` | `enterprise_history_name` | `former_names` | 整组替换 | 短 | **Q-WP3-14**：`DATA-ENT-ES-FORMER-L01` 已写模块；触发 `/internal/etl/modules/former_names/sync`。禁止编造 |

### 3.2 国外 · 写 `gkx_enterprise_global_v1`（4 个，分开触发）

| # | module | GDF 洗完这些 DWD 才触发 | 更新的 ES | 写法 | 备注 |
|---|--------|-------------------------|-----------|------|------|
| 14 | `forg_reg_info` | `enterprise_forg_base` **且** `enterprise_forg_extra` | 顶层名称/国家码 | upsert 建国外文档 | **国外首次先跑** |
| 15 | `forg_executive` | `enterprise_forg_executive` | `executives` | 整组替换 | |
| 16 | `forg_finance` | `enterprise_forg_finance_history` | `financials` + 部分 statistics | 整组替换 | |
| 17 | `forg_relations` | `enterprise_forg_invest` **且** `enterprise_forg_parent_subsidiary` | `supply_chain_relations` | **整组替换**（不与国内 invest/supply 合并脚本混用） | **Q-WP3-20**：投资段源=股东表洗入的 `forg_invest`。母子段仍等 `dwd_forg_subsidiary_info`；缺母子时**只触发投资段**，禁止空母子挡投资、禁止编母子 |

### 3.3 触发顺序（只约束依赖，不是 crontab）

1. 空索引 / 首次：`reg_info`（国内）或 `forg_reg_info`（国外）full。  
2. 日常：各行在自己的源表 success 后立刻异步触发，**不要**等全部 17 张表。  
3. `statistics` 放日终或放在当日已触发的明细模块都回执之后。  
4. 现网单飞：GDF 队列串行；目标多模块并行见 `15` §6。

### 3.4 字段级更新策略（现网 `etl/scripts.py`，2026-09-02）

对照 mapping 每个检索字段。策略：`containsKey` = 入参有键才覆盖（空值也会盖，若调用方传了 null）；`整组替换` = nested 整数组换掉；`按类型合并` = 只动一类 relation；`不灌` = 无模块、禁止编造。

**reg_info（`containsKey` 覆盖，缺键不动）：**  
`org_id` `_id` · `social_credit_code` · `name_cn` · `name_en` · `lerep` · `province` · `city` · `district` · `region_id` · `country_code` · `city_code` · `address` · `addr_lng` · `addr_lat` · `incorporation_year` · `incorporation_date` · `start_date` · `end_date` · `listing_status` · `listing_date` · `is_above_scale` · `latest_revenue`（兼写 `statistics[0]`）· `registered_capital_value`（万元→元×10000）· `capital_currency_code` · `registration_org` · `company_type` · `paid_in_capital_value` · `operating_status` · `enterprise_scale` · `stock_code` · `stock_noun` · `stock_type` · `listed_date` · `listed_status` · `industry_class` · `industry_class_name` · `main_activities` · `main_prod` · `description` · `business_scope` · `contact_phone` · `contact_email` · `data_source` · `edw_data_date` · `es_updated_at`（每次写）

**整组替换：**  
`tags`/`tags_flat` ← `tag_info` · `industry_chains`+4 个 flat ← `industry_chain`（另 `containsKey`：`is_chain_leader`/`chain_position_text`/`supply_chain_role`/`core_tech_tags_flat`）· `executives` ← `executive` / `forg_executive` · `financials` ← `finance` / `forg_finance`（并 `containsKey` 写 latest_* / 增长率）· `financings` ← `financing` · `bids` ← `bid` · `news` ← `news` · `innovation_carriers`+flat ← `innovation_carrier`

**按类型合并：**  
`supply_chain_relations`：`invest` 只删补 `relation_type=投资方`；`supply_chain` 保留投资段换其余；国外 `forg_relations` **整组替换**（不与国内脚本混用）。

**patent 模块：** 不写 `patents` nested。只 `containsKey` 写 `statistics.patent_*` / `high_value_patent` 与顶层 `patent_valid_count` / `high_value_patent_count`。

**statistics 模块：** `containsKey` 写 `statistics.*` 计数、`risk_flags.abnormal/shixin/zhixing` + `has_*`；顶层 latest/增长率/专利数用 `*_top` 键。

**不灌 / 无模块（禁止 GDF 或 ETL 编造）：**  
`logo_url` · `website` · `patents`（nested 明细，走 DWD）· `tech_score` · `business_score` · `competitiveness_score` · `postal_code`（国内 reg_info 现网不写；国外 `forg_reg_info` 写）· 司法明细 · `enterprise_patent_org_rel` · `enterprise_chain_patent`（Q-WP3-19 源表缺失，不灌）  
`former_names`：**本期要灌**（Q-WP3-14）；`DATA-ENT-ES-FORMER-L01` 已加模块，可触发 `/internal/etl/modules/former_names/sync`。

索引/更新机制长文只作对照。**禁止**抄其中 `settings.yaml` 口令。作业以本卷 + `15` 为准。

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
| nested 数组 | 整组替换 `ctx._source.tags = params.tags`（投资/供应链见 §3 合并例外） |
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
- `total_assets` / `total_liabilities` = **年末时点存量**，按 `data_year` 写入该年 `financials` 元素（与 DWD 同口径万元）；列表/筛选取最新一年。  
- **不能**用营收推总资产。源 ODS 有列才洗进 DWD；DWD 没有这两列则 ES 不得编造。

---

## 6. 全量（人工 / 例外，不是日常 GDF 日批）

日常禁止 `sync-all`。全量只用于空索引或书面批准：

1. `POST /internal/etl/init` — 建/校验物理索引 + 水位表 + 注册 scripts（**不删索引**）  
2. 国内 `reg_info` full  
3. 国外 `forg_reg_info` full  
4. 再按 §3 逐模块 full（仍异步；关单走 `15` §6.1）

mapping 要变：人工建新物理索引 → 灌数校验 → 再改别名 → 下线旧索引。禁止日常 DROP。

查询：`GET /internal/etl/status` · `/modules` · `/watermarks`。`sync=false` 异步；`full=false` 走水位。

---

## 7. 门禁（对 GDF / 对 ETL）

1. 该行源表当日 Wave B **success** 才触发该模块（见 `15`）。  
2. 失败不发布半成品索引。  
3. ADS / 指标权威不因 ES 失败被改写。  
4. DWD 缺表/缺列按 `02` / `13` 书面阻塞，禁止 ETL 用 fixture 填 ES。  
5. 触发已受理 ≠ ES 已更新；**当前**关单看本侧飞书终态（`15` §6.1）。  
6. `OPEN-ENT-FLOW-01/04`、`OPEN-ENT-GDF-TRIGGER` / `CALLBACK` / `ETL-JOBID` 保持点名，关闭不是本叶 DoD。

---

## 8. GDF 要做什么 / 不要做什么

- **要**：Wave A/B 洗数；按 §3 **一行一枪**通知本侧（`15` §6.1）；忙则隔 15min。  
- **finance**：两库已 ADD `main_business_revenue` / `total_profit` / `total_fixed_assets`；`finance.py` 已改读 `net_profit`→ES `pure_profit`（停 `total_profit` 双写）。表 success 后按 `15` §6.1 触发；未洗行为 NULL，不假装灌绿。
- **不要**：直连 ES / Python；`sync=true`；日常 `sync-all`；表失败仍触发；把受理当成功；把 `enterprise_patent_org_rel` 当成 ES 模块。
