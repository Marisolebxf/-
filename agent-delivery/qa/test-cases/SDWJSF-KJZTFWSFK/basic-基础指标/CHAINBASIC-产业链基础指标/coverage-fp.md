# 产业链基础指标 · 功能点覆盖（chain.basic / L01）

> catalog `chain.basic` · path `#/chain/basic`  
> A 线真源：`fp-split-by-api-run/work/L01.md`  
> B 线用例：`API-产业链基础指标-用例.md`（第二轮 **API-00889**～**00911**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.basic.list | GET | /innov/v1/industry/list | API-00889 | live |
| chain.basic.market-stats | GET | /innov/v1/industry/market-stats | API-00890～00893 | live |
| chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | API-00894～00897 | live |
| chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | API-00898、00899 | unavailable |
| chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | API-00900、00901 | live |
| chain.basic.global-dist | GET | /innov/v1/industry/global-dist | API-00902、00903 | unavailable |
| chain.basic.national-dist | GET | /innov/v1/industry/national-dist | API-00904、00905 | live |
| chain.basic.news-stats | GET | /innov/v1/industry/news-stats | API-00906、00907 | unavailable |
| chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | API-00908、00909 | live |
| chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | API-00910、00911 | live |

---

## 功能点 → 用例矩阵（挂 L01.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L01 \| chain.basic.list \| chain_id \| 算法输出-chain_id产业标识 | API-00889 | 已覆盖 | 主流程断言 chain_id（string） |
| L01 \| chain.basic.list \| chain_name \| 算法输出-chain_name产业名称 | API-00889 | 已覆盖 | 同条主流程 |
| L01 \| chain.basic.list \| _empty \| 列表查询无数据空态 | — | 未覆盖 | 无稳定空列表构造条件 |
| L01 \| chain.basic.list \| _fail \| 列表查询失败 | — | 未覆盖 | 无参列表无单点入参反向 |
| L01 \| chain.basic.market-stats \| chainId \| 算法输入-chainId产业标识 | API-00890、00892 | 已覆盖 | 合法 + 缺 chainId |
| L01 \| chain.basic.market-stats \| statYear \| 算法输入-statYear统计年份 | API-00890、00891、00893 | 已覆盖 | 全参 + 省略 + 非法 |
| L01 \| chain.basic.market-stats \| total_revenue \| 算法输出-total_revenue总营收 | API-00890 | 已覆盖 | 正向断言 total_revenue |
| L01 \| chain.basic.market-stats \| _empty \| 市场规模无数据空态 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.market-stats \| _fail \| 市场规模查询失败 | API-00892、00893 | 已覆盖 | 入参反向 message/msg |
| L01 \| chain.basic.enterprise-stats \| chainId \| 算法输入-chainId产业标识 | API-00894、00896 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| statYear \| 算法输入-statYear统计年份 | API-00894、00895、00897 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| enterprise_count \| 算法输出-enterprise_count企业数 | API-00894 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| _empty \| 企业规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.enterprise-stats \| _fail \| 企业规模查询失败 | API-00896、00897 | 已覆盖 | |
| L01 \| chain.basic.institution-stats \| chainId \| 算法输入-chainId产业标识 | API-00898、00899 | 已覆盖 | unavailable 仍写文档主/反向 |
| L01 \| chain.basic.institution-stats \| institution_count \| 算法输出-institution_count机构数 | API-00898 | 已覆盖 | |
| L01 \| chain.basic.institution-stats \| _empty \| 机构规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.institution-stats \| _fail \| 机构规模查询失败 | API-00899 | 部分覆盖 | 仅缺 chainId 反向 |
| L01 \| chain.basic.investment-stats \| chainId \| 算法输入-chainId产业标识 | API-00900、00901 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| total_amount \| 算法输出-total_amount投融资金额 | API-00900 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| _empty \| 投融资规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.investment-stats \| _fail \| 投融资规模查询失败 | API-00901 | 部分覆盖 | 仅缺 chainId |
| L01 \| chain.basic.global-dist \| chainId \| 算法输入-chainId产业标识 | API-00902、00903 | 已覆盖 | |
| L01 \| chain.basic.global-dist \| country \| 算法输出-country国家地区 | API-00902 | 已覆盖 | |
| L01 \| chain.basic.global-dist \| _empty \| 全球分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.global-dist \| _fail \| 全球分布查询失败 | API-00903 | 部分覆盖 | |
| L01 \| chain.basic.national-dist \| chainId \| 算法输入-chainId产业标识 | API-00904、00905 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| province \| 算法输出-province省份 | API-00904 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| _empty \| 全国分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.national-dist \| _fail \| 全国分布查询失败 | API-00905 | 部分覆盖 | |
| L01 \| chain.basic.news-stats \| chainId \| 算法输入-chainId产业标识 | API-00906、00907 | 已覆盖 | |
| L01 \| chain.basic.news-stats \| news_count \| 算法输出-news_count资讯数 | API-00906 | 已覆盖 | |
| L01 \| chain.basic.news-stats \| _empty \| 动态资讯无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.news-stats \| _fail \| 动态资讯查询失败 | API-00907 | 部分覆盖 | |
| L01 \| chain.basic.sz-elements \| chainId \| 算法输入-chainId产业标识 | API-00908、00909 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| enterprise_count \| 算法输出-enterprise_count深圳企业数 | API-00908 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| institution_count \| 算法输出-institution_count深圳机构数 | API-00908 | 已覆盖 | 同条主流程 |
| L01 \| chain.basic.sz-elements \| _empty \| 深圳要素无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.sz-elements \| _fail \| 深圳要素查询失败 | API-00909 | 部分覆盖 | |
| L01 \| chain.basic.sz-dist \| chainId \| 算法输入-chainId产业标识 | API-00910、00911 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| district \| 算法输出-district行政区 | API-00910 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| _empty \| 深圳分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.sz-dist \| _fail \| 深圳分布查询失败 | API-00911 | 部分覆盖 | |

---

## req_only 行（无 endpoint 挂接）

L01.md 中 `etl_clean_standardize`、`metric_validity_check`、`mq_result_sync` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
