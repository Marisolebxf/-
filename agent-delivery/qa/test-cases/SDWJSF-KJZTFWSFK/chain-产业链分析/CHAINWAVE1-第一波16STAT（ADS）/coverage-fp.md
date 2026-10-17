# 第一波 16 STAT（ADS）· A 线功能点覆盖（chain.wave1）

> **catalog_page_id**：`chain.wave1` · path `/chain/wave1`  
> **A 线真源**：`fp-split-by-api-run/work/L*.md` 检索 **`chain.wave1` 无命中**（待六级 by-api 合表后回填 Lxx）  
> **用例册**：`API-第一波16STAT-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00263`～`00311`，共 49 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.wave1`  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.wave1.m_chain_total_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TOTAL_COUNT/compute | available | 263、264、265、266 |
| chain.wave1.m_chain_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_COUNT/compute | available | 267、268、269 |
| chain.wave1.m_chain_enterprise_new_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_NEW_COUNT/compute | available | 270、271、272 |
| chain.wave1.m_chain_national_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_NATIONAL_REGION_COUNT/compute | available | 273、274、275 |
| chain.wave1.m_chain_sz_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_REGION_COUNT/compute | available | 276、277、278 |
| chain.wave1.m_chain_sz_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_COUNT/compute | available | 279、280、281 |
| chain.wave1.m_chain_sz_enterprise_ratio | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_RATIO/compute | available | 282、283、284 |
| chain.wave1.m_chain_market_size | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_SIZE/compute | available | 285、286、287 |
| chain.wave1.m_chain_market_growth | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_GROWTH/compute | available | 288、289、290 |
| chain.wave1.m_chain_invest_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_INVEST_COUNT/compute | available | 291、292、293 |
| chain.wave1.m_chain_reg_financing | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_FINANCING/compute | available | 294、295、296 |
| chain.wave1.m_chain_reg_revenue | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_REVENUE/compute | available | 297、298、299 |
| chain.wave1.m_chain_reg_patent | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_PATENT/compute | available | 300、301、302 |
| chain.wave1.m_chain_sz_completeness | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_COMPLETENESS/compute | available | 303、304、305 |
| chain.wave1.m_chain_patent_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PATENT_COUNT/compute | available | 306、307、308 |
| chain.wave1.m_chain_product_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PRODUCT_COUNT/compute | available | 309、310、311 |

---

## 2. 功能点 → 用例矩阵（catalog 可测行 · 待 A 线 Lxx 对齐）

键：`L?? | endpoint_id | field_key | 功能点（A 线）`（A 线合表前以 catalog 字段代填）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| catalog \| chain.wave1.m_chain_total_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 263、264、265、266 | 已覆盖 | W01-01/02/03 |
| catalog \| chain.wave1.m_chain_total_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 263 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_total_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 263 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_total_count \| value \| 算法输出-value载荷 | catalog data.value | 263 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_total_count \| _fail \| STAT计算失败 | 契约错误态 | 266 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_total_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_enterprise_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 267、268、269 | 已覆盖 | W02-01/02/03 |
| catalog \| chain.wave1.m_chain_enterprise_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 267 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_enterprise_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 267 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_enterprise_count \| value \| 算法输出-value载荷 | catalog data.value | 267 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_enterprise_count \| _fail \| STAT计算失败 | 契约错误态 | 269 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_enterprise_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 270、271、272 | 已覆盖 | W03-01/02/03 |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 270 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 270 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| value \| 算法输出-value载荷 | catalog data.value | 270 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| _fail \| STAT计算失败 | 契约错误态 | 272 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_enterprise_new_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_national_region_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 273、274、275 | 已覆盖 | W04-01/02/03 |
| catalog \| chain.wave1.m_chain_national_region_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 273 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_national_region_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 273 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_national_region_count \| value \| 算法输出-value载荷 | catalog data.value | 273 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_national_region_count \| _fail \| STAT计算失败 | 契约错误态 | 275 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_national_region_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_sz_region_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 276、277、278 | 已覆盖 | W05-01/02/03 |
| catalog \| chain.wave1.m_chain_sz_region_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 276 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_sz_region_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 276 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_sz_region_count \| value \| 算法输出-value载荷 | catalog data.value | 276 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_sz_region_count \| _fail \| STAT计算失败 | 契约错误态 | 278 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_sz_region_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 279、280、281 | 已覆盖 | W06-01/02/03 |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 279 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 279 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| value \| 算法输出-value载荷 | catalog data.value | 279 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| _fail \| STAT计算失败 | 契约错误态 | 281 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_sz_enterprise_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 282、283、284 | 已覆盖 | W07-01/02/03 |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 282 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 282 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| value \| 算法输出-value载荷 | catalog data.value | 282 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| _fail \| STAT计算失败 | 契约错误态 | 284 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_sz_enterprise_ratio \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_market_size \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 285、286、287 | 已覆盖 | W08-01/02/03 |
| catalog \| chain.wave1.m_chain_market_size \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 285 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_market_size \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 285 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_market_size \| value \| 算法输出-value载荷 | catalog data.value | 285 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_market_size \| _fail \| STAT计算失败 | 契约错误态 | 287 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_market_size \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_market_growth \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 288、289、290 | 已覆盖 | W09-01/02/03 |
| catalog \| chain.wave1.m_chain_market_growth \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 288 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_market_growth \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 288 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_market_growth \| value \| 算法输出-value载荷 | catalog data.value | 288 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_market_growth \| _fail \| STAT计算失败 | 契约错误态 | 290 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_market_growth \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_invest_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 291、292、293 | 已覆盖 | W10-01/02/03 |
| catalog \| chain.wave1.m_chain_invest_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 291 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_invest_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 291 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_invest_count \| value \| 算法输出-value载荷 | catalog data.value | 291 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_invest_count \| _fail \| STAT计算失败 | 契约错误态 | 293 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_invest_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_reg_financing \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 294、295、296 | 已覆盖 | W11-01/02/03 |
| catalog \| chain.wave1.m_chain_reg_financing \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 294 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_reg_financing \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 294 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_reg_financing \| value \| 算法输出-value载荷 | catalog data.value | 294 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_reg_financing \| _fail \| STAT计算失败 | 契约错误态 | 296 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_reg_financing \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_reg_revenue \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 297、298、299 | 已覆盖 | W12-01/02/03 |
| catalog \| chain.wave1.m_chain_reg_revenue \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 297 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_reg_revenue \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 297 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_reg_revenue \| value \| 算法输出-value载荷 | catalog data.value | 297 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_reg_revenue \| _fail \| STAT计算失败 | 契约错误态 | 299 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_reg_revenue \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_reg_patent \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 300、301、302 | 已覆盖 | W13-01/02/03 |
| catalog \| chain.wave1.m_chain_reg_patent \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 300 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_reg_patent \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 300 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_reg_patent \| value \| 算法输出-value载荷 | catalog data.value | 300 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_reg_patent \| _fail \| STAT计算失败 | 契约错误态 | 302 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_reg_patent \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_sz_completeness \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 303、304、305 | 已覆盖 | W14-01/02/03 |
| catalog \| chain.wave1.m_chain_sz_completeness \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 303 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_sz_completeness \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 303 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_sz_completeness \| value \| 算法输出-value载荷 | catalog data.value | 303 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_sz_completeness \| _fail \| STAT计算失败 | 契约错误态 | 305 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_sz_completeness \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_patent_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 306、307、308 | 已覆盖 | W15-01/02/03 |
| catalog \| chain.wave1.m_chain_patent_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 306 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_patent_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 306 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_patent_count \| value \| 算法输出-value载荷 | catalog data.value | 306 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_patent_count \| _fail \| STAT计算失败 | 契约错误态 | 308 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_patent_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |
| catalog \| chain.wave1.m_chain_product_count \| chain_id \| 算法输入-chain_id产业链标识 | catalog chain_id | 309、310、311 | 已覆盖 | W16-01/02/03 |
| catalog \| chain.wave1.m_chain_product_count \| metric_id \| 算法输出-metric_id | catalog data.metric_id | 309 | 已覆盖 | |
| catalog \| chain.wave1.m_chain_product_count \| metric_name_zh \| 算法输出-metric_name_zh | catalog data.metric_name_zh | 309 | 已覆盖 | 金样另断言 |
| catalog \| chain.wave1.m_chain_product_count \| value \| 算法输出-value载荷 | catalog data.value | 309 | 已覆盖 | 不断言样例 shape 枚举值 |
| catalog \| chain.wave1.m_chain_product_count \| _fail \| STAT计算失败 | 契约错误态 | 311 | 已覆盖 | 非法 chain_id |
| catalog \| chain.wave1.m_chain_product_count \| _empty \| STAT无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定可构造必空条件；本轮未试调 |

---

## 3. req_only / 不投影

| 项 | 说明 |
|----|------|
| `viz` / KPI 联调台图表 | 不投影 API 断言 |
| Python `/internal/*` | 黑盒不测 |
| ADS 表内具体行数 | 禁止写入预期数值 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 49 |
| 用例编号起止 | API-00263～API-00311 |
| endpoint 数 | 16 |
| 金样 | API-00263 |
| 异常-鉴权 | API-00264 |
| `_empty` 未覆盖 | 16 行（每 endpoint 1 行，无稳定构造） |
| 试调 | 本轮未试调（§0 已声明） |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINWAVE1-第一波16STAT（ADS）/` |
