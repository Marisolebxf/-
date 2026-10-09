# CHAIN-ALGO-STAT-39-IMPL-L01 · 产业链第一波16条STAT — Demo ADS落地（ads_v2）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |
| 说明 | 李伟确认建单并认领后开工 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 ads_v2 / DemoDB；大 JOIN 改为 org 分批聚合，未新增依赖 |

## 范围与实现

- 仓：`repos/demo-algo-science`
- 入口：`chainan/llm_ods/ads_v2.py` → `recalc_ads` → `_compute_wave1`
- 只读 Demo DWD：`industry_chain_entity_rel` × `enterprise_base` / `enterprise_finance_history` / `enterprise_financing` / `enterprise_patent_detail` / `enterprise_industry_product`
- 写入 Demo ADS：`industry_chain_metric_fact` / `industry_chain_metric_series` / `industry_chain_metric_dist`（+ 既有 scorecard/topn/snapshot）
- 深圳口径：`city='深圳市'`
- 禁止：扫 ODS；用 `entity_rel` 的 product 边顶 E39；mock 投资顶 B17

### 第一波 16 条落点

| metric_id | ADS 形态 | Demo 抽检（batch `wave1-1788403404`） |
|---|---|---|
| M_CHAIN_TOTAL_COUNT | fact | n=1，值=53 |
| M_CHAIN_ENTERPRISE_COUNT | fact+series | fact n=303；series n=3333 |
| M_CHAIN_ENTERPRISE_NEW_COUNT | series | n=3333 |
| M_CHAIN_NATIONAL_REGION_COUNT | dist | n=303（Demo 挂接企业省多为广东） |
| M_CHAIN_SZ_REGION_COUNT | dist | n=1944 |
| M_CHAIN_SZ_ENTERPRISE_COUNT | fact | n=303，max=5556 |
| M_CHAIN_SZ_ENTERPRISE_RATIO | fact | n=303，max=1 |
| M_CHAIN_MARKET_SIZE | fact+series | fact n=269；series n=2078 |
| M_CHAIN_MARKET_GROWTH | series | n=2078 |
| M_CHAIN_INVEST_COUNT | fact | n=303，max=10064（表有行，非 0） |
| M_CHAIN_REG_FINANCING | dist | n=303 |
| M_CHAIN_REG_REVENUE | dist | n=2078 |
| M_CHAIN_REG_PATENT | dist | n=303 |
| M_CHAIN_SZ_COMPLETENESS | fact | n=303 |
| M_CHAIN_PATENT_COUNT | fact | n=303，max=29810 |
| M_CHAIN_PRODUCT_COUNT | fact | n=303，**全 0**（`enterprise_industry_product` 0 行，诚实写 0） |

## 关键修复

1. 大 JOIN 读超时 → org 分批聚合（finance/financing/patent/product）再滚到链；`dbconn` 读超时 300s
2. `data_year` 存 `'2025.0'` 导致市场类指标被 `isdigit()` 滤光 → 增加 `_year_key()` 解析

## 验收证据

- Demo：`111.198.38.90:34306` / `demo_gkxlumenx_dwd` → `demo_gkxlumenx_ads`
- `recalc_ads` 约 60s 完成；返回行数 fact=2550 / series=10903 / dist=4931
- E39 产品表空 → ADS 写 0；未用 product 边顶数
- B17 融资表有 ~3 万行 → 按 COUNT 实算，非 mock

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ |
| 调用链未越层 | ✅（本叶只写 Demo ADS） |
| 不扫 ODS | ✅ |
| 诚实空结果 | ✅ E39=0 |
| D12 demo/lumen 隔离 | ✅ 只动 demo-algo-science |

## 偏离说明

- 专利按 org DISTINCT 再求和到链：Demo 近似（跨企同号极少）；产品按 product_name 跨企 set 去重
- 全国区域 dist 当前以省名为 bucket；Demo 挂接企业省分布极偏广东

## 产物清单

- `repos/demo-algo-science/chainan/llm_ods/ads_v2.py`
- `repos/demo-algo-science/chainan/llm_ods/dbconn.py`（read/write timeout 300）
- 本 handoff

## 四步端到端补齐（2026-09-03）

| 步 | 状态 | 证据 |
|---|---|---|
| 1 部署 innov-py | 已推 demo-algo-science 64686a6 → origin/dev | 等 CI deploy:innov-py 热更新 |
| 2 灌数验收 | **待 CI 后人工点** | 中台 http://111.198.38.90:50100/#/chain/basic 触发灌数；确认 ADS 由 
un-chain-pipeline→seed→ds_v2.recalc_ads 写出 |
| 3 读接口 | 已完成 | 
ead_v2 市场/企业/投资/全国区/深圳区优先 ADS；metrics.WAVE1_ADS 16 条 + catalog；POST /v1/chainan/metric/{id}/compute |
| 4 测试台 + basic | 已推 | demo-svc-platform 482f909 透传 /v1/industry/chainan/**；lumen-ui-algo-apiview 29c56b9：chain.wave1 16 条 + basic 标 available |

### 新增/变更产物

- chainan/llm_ods/ads_v2.py / dbconn.py / ddl.py / 
ead_v2.py
- chainan/metrics/metrics.py / catalog.py（+16 WAVE1）
- Java：ChainAlgoClient / ChainService / ChainController chainan 透传
- 测试台：src/catalog/chain.json wave1 组

### 验收操作（CI 绿后）

1. 50100 Demo 平面点灌数，抽检 ADS industry_chain_metric_fact 的 calc_batch_id 为流水线批次
2. 50897 打开「第一波 16 STAT」，对 INB120401 调 compute，期望 data_source=real
3. basic 页市场/企业/投资/深圳要素读数非 mock
