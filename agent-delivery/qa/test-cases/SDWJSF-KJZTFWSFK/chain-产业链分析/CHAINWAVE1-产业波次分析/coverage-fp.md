# 产业波次分析 · 功能点覆盖（chain.wave1）

> **catalog_page_id**：`chain.wave1` · path `/chain/wave1`  
> **A 线**：**无对应 Lxx**。该页不在 60 六级挂接表。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 Lxx `pages` 与 `catalog_skip` 均无 `chain.wave1`。不改 `work/`。  
> **B 线用例**：`FUNC-产业波次分析-用例.md`（第三轮 **FUNC-00342**～**FUNC-00406**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.wave1`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.wave1.m_chain_total_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TOTAL_COUNT/compute | FUNC-00342、00343、00344 | available |
| chain.wave1.m_chain_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_COUNT/compute | FUNC-00345、00346、00347 | available |
| chain.wave1.m_chain_enterprise_new_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_NEW_COUNT/compute | FUNC-00348、00349、00350 | available |
| chain.wave1.m_chain_national_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_NATIONAL_REGION_COUNT/compute | FUNC-00351、00352、00353 | available |
| chain.wave1.m_chain_sz_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_REGION_COUNT/compute | FUNC-00354、00355、00356 | available |
| chain.wave1.m_chain_sz_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_COUNT/compute | FUNC-00357、00358、00359 | available |
| chain.wave1.m_chain_sz_enterprise_ratio | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_RATIO/compute | FUNC-00360、00361、00362 | available |
| chain.wave1.m_chain_market_size | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_SIZE/compute | FUNC-00363、00364、00365 | available |
| chain.wave1.m_chain_market_growth | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_GROWTH/compute | FUNC-00366、00367、00368 | available |
| chain.wave1.m_chain_invest_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_INVEST_COUNT/compute | FUNC-00369、00370、00371 | available |
| chain.wave1.m_chain_reg_financing | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_FINANCING/compute | FUNC-00372、00373、00374 | available |
| chain.wave1.m_chain_reg_revenue | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_REVENUE/compute | FUNC-00375、00376、00377 | available |
| chain.wave1.m_chain_reg_patent | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_PATENT/compute | FUNC-00378、00379、00380 | available |
| chain.wave1.m_chain_sz_completeness | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_COMPLETENESS/compute | FUNC-00381、00382、00383 | available |
| chain.wave1.m_chain_patent_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PATENT_COUNT/compute | FUNC-00384、00385、00386 | available |
| chain.wave1.m_chain_product_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PRODUCT_COUNT/compute | FUNC-00387、00388、00389 | available |
| chain.topic-panorama.m_chain_global_case_match | POST | /innov/v1/industry/chainan/metric/M_CHAIN_GLOBAL_CASE_MATCH/compute | FUNC-00390～00404 | available |

---

## 功能点 → 用例矩阵

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| chain.wave1.m_chain_total_count \| WAVE1 产业链环节总数 | FUNC-00342、00343、00344 | 无对应功能点 | 主流程空 body；传入 chain_id；非法 chain_id |
| （无 Lxx） \| chain.wave1.m_chain_enterprise_count \| WAVE1 链上企业数 | FUNC-00345、00346、00347 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_enterprise_new_count \| WAVE1 链上新增企业数 | FUNC-00348、00349、00350 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_national_region_count \| WAVE1 全国区域企业分布 | FUNC-00351、00352、00353 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_sz_region_count \| WAVE1 深圳区域企业分布 | FUNC-00354、00355、00356 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_sz_enterprise_count \| WAVE1 深圳企业数 | FUNC-00357、00358、00359 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_sz_enterprise_ratio \| WAVE1 深圳企业占比 | FUNC-00360、00361、00362 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_market_size \| WAVE1 产业市场规模 | FUNC-00363、00364、00365 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_market_growth \| WAVE1 产业市场增速 | FUNC-00366、00367、00368 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_invest_count \| WAVE1 投融资事件数 | FUNC-00369、00370、00371 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_reg_financing \| WAVE1 区域融资分布 | FUNC-00372、00373、00374 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_reg_revenue \| WAVE1 区域营收分布 | FUNC-00375、00376、00377 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_reg_patent \| WAVE1 区域专利分布 | FUNC-00378、00379、00380 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_sz_completeness \| WAVE1 深圳产业链完备度 | FUNC-00381、00382、00383 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_patent_count \| WAVE1 链上专利数 | FUNC-00384、00385、00386 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.wave1.m_chain_product_count \| WAVE1 链上产品数 | FUNC-00387、00388、00389 | 无对应功能点 | 同上 |
| （无 Lxx） \| chain.topic-panorama.m_chain_global_case_match \| 全球成功案例匹配 | FUNC-00390～00404 | 无对应功能点 | sampleRequest 主流程 + 6 备选 + 8 反向 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00405、00406 | 无对应功能点 | 下拉 17 项与 catalog title 一致 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 17 |
| title 数 | 17 |
| FUNC 用例数 | 65 |
| 主流程 | 17 |
| 备选-参数组合 | 22 |
| 反向 | 24 |
| 清单 | 2 |
| 编号 | FUNC-00342～00406 |
| A 线 Lxx | 无 |
