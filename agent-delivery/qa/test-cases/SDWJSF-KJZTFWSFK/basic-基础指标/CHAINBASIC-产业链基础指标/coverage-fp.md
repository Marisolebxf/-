# 产业链基础指标 · 功能点覆盖（chain.basic / L01）

> catalog `chain.basic` · 50897 · path `#/chain/basic`  
> **用例册**：`API-产业链基础指标-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00001`～`00023`，共 **23** 条）  
> A 线范围：**L01**（`fp-split-by-api-run/work/L01.md`）  
> 功能点键：`L01 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.basic.list | GET | /innov/v1/industry/list | API-00001、00002 | live |
| chain.basic.market-stats | GET | /innov/v1/industry/market-stats | API-00003～00005 | live |
| chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | API-00006～00008 | live |
| chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | API-00009 | unavailable |
| chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | API-00010～00012 | live |
| chain.basic.global-dist | GET | /innov/v1/industry/global-dist | API-00013 | unavailable |
| chain.basic.national-dist | GET | /innov/v1/industry/national-dist | API-00014～00016 | live |
| chain.basic.news-stats | GET | /innov/v1/industry/news-stats | API-00017 | unavailable |
| chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | API-00018～00020 | live |
| chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | API-00021～00023 | live |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L01 \| chain.basic.list \| chain_id \| 算法输出-chain_id产业标识 | catalog chain_id | API-00001 | 已覆盖 | 金样断言 string 型 chain_id |
| L01 \| chain.basic.list \| chain_name \| 算法输出-chain_name产业名称 | catalog chain_name | API-00001 | 已覆盖 | 金样断言 string 型 chain_name |
| L01 \| chain.basic.list \| _empty \| 列表查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空列表构造条件 |
| L01 \| chain.basic.list \| _fail \| 列表查询失败 | 契约错误态 | — | 未覆盖 | 无参列表无可构造单点失败态，待执行期网关/上游故障复核 |
| L01 \| chain.basic.market-stats \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00003、00004、00005 | 已覆盖 | 合法/缺省/非法 |
| L01 \| chain.basic.market-stats \| statYear \| 算法输入-statYear统计年份 | catalog statYear | API-00003 | 已覆盖 | MKT-01 含 statYear；省略可选见 MKT-03 |
| L01 \| chain.basic.market-stats \| total_revenue \| 算法输出-total_revenue总营收 | catalog total_revenue | API-00003 | 已覆盖 | 断言 number 型存在，不写具体金额 |
| L01 \| chain.basic.market-stats \| _empty \| 市场规模无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据年份/产业条件 |
| L01 \| chain.basic.market-stats \| _fail \| 市场规模查询失败 | 契约错误态 | API-00004、00005 | 已覆盖 | 缺必填与非法 chainId |
| L01 \| chain.basic.enterprise-stats \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00006、00007、00008 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| statYear \| 算法输入-statYear统计年份 | catalog statYear | API-00006 | 已覆盖 | ENT-01 含 statYear |
| L01 \| chain.basic.enterprise-stats \| enterprise_count \| 算法输出-enterprise_count企业数 | catalog enterprise_count | API-00006 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| _empty \| 企业规模无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.enterprise-stats \| _fail \| 企业规模查询失败 | 契约错误态 | API-00007、00008 | 已覆盖 | |
| L01 \| chain.basic.institution-stats \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00009 | 契约占位 | endpoint unavailable |
| L01 \| chain.basic.institution-stats \| institution_count \| 算法输出-institution_count机构数 | catalog institution_count | API-00009 | 契约占位 | 禁止 sample 数值作通过条件 |
| L01 \| chain.basic.institution-stats \| _empty \| 机构规模无数据空态 | 契约空结果 | API-00009 | 契约占位 | 与不可用契约合并验收 |
| L01 \| chain.basic.institution-stats \| _fail \| 机构规模查询失败 | 契约错误态 | API-00009 | 契约占位 | |
| L01 \| chain.basic.investment-stats \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00010、00011、00012 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| total_amount \| 算法输出-total_amount投融资金额 | catalog total_amount | API-00010 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| _empty \| 投融资规模无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.investment-stats \| _fail \| 投融资规模查询失败 | 契约错误态 | API-00011、00012 | 已覆盖 | |
| L01 \| chain.basic.global-dist \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00013 | 契约占位 | unavailable |
| L01 \| chain.basic.global-dist \| country \| 算法输出-country国家地区 | catalog country | API-00013 | 契约占位 | |
| L01 \| chain.basic.global-dist \| _empty \| 全球分布无数据空态 | 契约空结果 | API-00013 | 契约占位 | |
| L01 \| chain.basic.global-dist \| _fail \| 全球分布查询失败 | 契约错误态 | API-00013 | 契约占位 | |
| L01 \| chain.basic.national-dist \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00014、00015、00016 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| province \| 算法输出-province省份 | catalog province | API-00014 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| _empty \| 全国分布无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.national-dist \| _fail \| 全国分布查询失败 | 契约错误态 | API-00015、00016 | 已覆盖 | |
| L01 \| chain.basic.news-stats \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00017 | 契约占位 | unavailable |
| L01 \| chain.basic.news-stats \| news_count \| 算法输出-news_count资讯数 | catalog news_count | API-00017 | 契约占位 | |
| L01 \| chain.basic.news-stats \| _empty \| 动态资讯无数据空态 | 契约空结果 | API-00017 | 契约占位 | |
| L01 \| chain.basic.news-stats \| _fail \| 动态资讯查询失败 | 契约错误态 | API-00017 | 契约占位 | |
| L01 \| chain.basic.sz-elements \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00018、00019、00020 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| enterprise_count \| 算法输出-enterprise_count深圳企业数 | catalog enterprise_count | API-00018 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| institution_count \| 算法输出-institution_count深圳机构数 | catalog institution_count | API-00018 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| _empty \| 深圳要素无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.sz-elements \| _fail \| 深圳要素查询失败 | 契约错误态 | API-00019、00020 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00021、00022、00023 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| district \| 算法输出-district行政区 | catalog district | API-00021 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| _empty \| 深圳分布无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.sz-dist \| _fail \| 深圳分布查询失败 | 契约错误态 | API-00022、00023 | 已覆盖 | |
| L01 \| （无 endpoint） \| etl_clean_standardize \| 统一预处理与清洗 | 需规总述清洗 | — | 未覆盖 | A 线 req_only，无 catalog endpoint |
| L01 \| （无 endpoint） \| metric_validity_check \| 指标有效性验证 | 需规有效性验证 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| mq_result_sync \| 消息队列结果同步 | 需规数据同步 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| scheduled_refresh_monitor \| 定期更新与监测 | 需规更新监测 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| market_growth_rate \| 市场规模环比增长率 | 需规（1）环比 | — | 未覆盖 | catalog 未列 growth 字段 |
| L01 \| （无 endpoint） \| enterprise_growth_rate \| 企业规模环比增长率 | 需规（2）环比 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| institution_growth_rate \| 机构规模环比增长率 | 需规（3）环比 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| investment_growth_rate \| 投融资环比增长率 | 需规（4）环比 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| global_ent_inst_total \| 各国企业与机构总数 | 需规（5）总数 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| national_ent_inst_total \| 各省企业与机构总数 | 需规（6）总数 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| national_dist_growth_rate \| 全国分布环比增长率 | 需规（6）环比 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| news_hot_threshold_rule \| 热点阈值判定规则 | 需规（7）热点判定 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| news_hot_count_avg \| 热点数量与指标均值 | 需规（7）热点统计 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| sz_elements_aggregate \| 深圳综合产业要素 | 需规（8）要素汇总 | — | 未覆盖 | req_only |
| L01 \| （无 endpoint） \| sz_dist_ent_inst_growth \| 各区企机构与增长率 | 需规（9）区级趋势 | — | 未覆盖 | req_only |

---

## 3. 统计（交卷）

| 状态 | 条数 |
|------|------|
| 已覆盖 | 32 |
| 契约占位 | 12 |
| 未覆盖 | 14 |
| 待 A 线合表核对 | 0 |

| 项 | 值 |
|----|-----|
| API 用例条数 | **23** |
| 编号闭区间 | **API-00001**～**API-00023** |
| `_empty` 未覆盖（live 空态行） | **7**（list、market-stats、enterprise-stats、investment-stats、national-dist、sz-elements、sz-dist；unavailable 三类 _empty 走契约占位不计入） |
| 50897 试调 | **成功**（产业链列表主路径，见用例 §0） |
