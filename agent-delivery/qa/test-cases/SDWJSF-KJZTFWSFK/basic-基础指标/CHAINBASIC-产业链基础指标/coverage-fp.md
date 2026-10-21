# 产业链基础指标 · 功能点覆盖（chain.basic / L01）

> catalog `chain.basic` · path `#/chain/basic`  
> A 线真源：`fp-split-by-api-run/work/L01.md`  
> B 线用例：`FUNC-产业链基础指标-用例.md`（第三轮 **FUNC-00001**～**00025**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.basic.list | GET | /innov/v1/industry/list | FUNC-00001 | available |
| chain.basic.market-stats | GET | /innov/v1/industry/market-stats | FUNC-00002～00005 | available |
| chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | FUNC-00006～00009 | available |
| chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | FUNC-00010、00011 | unavailable |
| chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | FUNC-00012、00013 | available |
| chain.basic.global-dist | GET | /innov/v1/industry/global-dist | FUNC-00014、00015 | unavailable |
| chain.basic.national-dist | GET | /innov/v1/industry/national-dist | FUNC-00016、00017 | available |
| chain.basic.news-stats | GET | /innov/v1/industry/news-stats | FUNC-00018、00019 | unavailable |
| chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | FUNC-00020、00021 | available |
| chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | FUNC-00022、00023 | available |
| （页面清单） | — | — | FUNC-00024、00025 | — |

---

## 功能点 → 用例矩阵（挂 L01.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L01 \| chain.basic.list \| chain_id \| 算法输出-chain_id产业标识 | FUNC-00001 | 已覆盖 | 主流程断言 chain_id（string） |
| L01 \| chain.basic.list \| chain_name \| 算法输出-chain_name产业名称 | FUNC-00001 | 已覆盖 | 同条主流程 |
| L01 \| chain.basic.list \| _empty \| 列表查询无数据空态 | — | 未覆盖 | 无稳定空列表构造条件 |
| L01 \| chain.basic.list \| _fail \| 列表查询失败 | — | 未覆盖 | 无参列表无单点入参反向 |
| L01 \| chain.basic.market-stats \| chainId \| 算法输入-chainId产业标识 | FUNC-00002、00004 | 已覆盖 | 合法 + 缺 chainId |
| L01 \| chain.basic.market-stats \| statYear \| 算法输入-statYear统计年份 | FUNC-00002、00003、00005 | 已覆盖 | 全参 + 省略 + 非法 |
| L01 \| chain.basic.market-stats \| total_revenue \| 算法输出-total_revenue总营收 | FUNC-00002 | 已覆盖 | 正向断言 total_revenue |
| L01 \| chain.basic.market-stats \| _empty \| 市场规模无数据空态 | — | 未覆盖 | 无稳定空数据条件 |
| L01 \| chain.basic.market-stats \| _fail \| 市场规模查询失败 | FUNC-00004、00005 | 已覆盖 | 入参反向 message/msg |
| L01 \| chain.basic.enterprise-stats \| chainId \| 算法输入-chainId产业标识 | FUNC-00006、00008 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| statYear \| 算法输入-statYear统计年份 | FUNC-00006、00007、00009 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| enterprise_count \| 算法输出-enterprise_count企业数 | FUNC-00006 | 已覆盖 | |
| L01 \| chain.basic.enterprise-stats \| _empty \| 企业规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.enterprise-stats \| _fail \| 企业规模查询失败 | FUNC-00008、00009 | 已覆盖 | |
| L01 \| chain.basic.institution-stats \| chainId \| 算法输入-chainId产业标识 | FUNC-00010、00011 | 已覆盖 | unavailable 仍写文档主/反向 |
| L01 \| chain.basic.institution-stats \| institution_count \| 算法输出-institution_count机构数 | FUNC-00010 | 已覆盖 | |
| L01 \| chain.basic.institution-stats \| _empty \| 机构规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.institution-stats \| _fail \| 机构规模查询失败 | FUNC-00011 | 部分覆盖 | 仅缺 chainId 反向 |
| L01 \| chain.basic.investment-stats \| chainId \| 算法输入-chainId产业标识 | FUNC-00012、00013 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| total_amount \| 算法输出-total_amount投融资金额 | FUNC-00012 | 已覆盖 | |
| L01 \| chain.basic.investment-stats \| _empty \| 投融资规模无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.investment-stats \| _fail \| 投融资规模查询失败 | FUNC-00013 | 部分覆盖 | 仅缺 chainId |
| L01 \| chain.basic.global-dist \| chainId \| 算法输入-chainId产业标识 | FUNC-00014、00015 | 已覆盖 | |
| L01 \| chain.basic.global-dist \| country \| 算法输出-country国家地区 | FUNC-00014 | 已覆盖 | |
| L01 \| chain.basic.global-dist \| _empty \| 全球分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.global-dist \| _fail \| 全球分布查询失败 | FUNC-00015 | 部分覆盖 | |
| L01 \| chain.basic.national-dist \| chainId \| 算法输入-chainId产业标识 | FUNC-00016、00017 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| province \| 算法输出-province省份 | FUNC-00016 | 已覆盖 | |
| L01 \| chain.basic.national-dist \| _empty \| 全国分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.national-dist \| _fail \| 全国分布查询失败 | FUNC-00017 | 部分覆盖 | |
| L01 \| chain.basic.news-stats \| chainId \| 算法输入-chainId产业标识 | FUNC-00018、00019 | 已覆盖 | |
| L01 \| chain.basic.news-stats \| news_count \| 算法输出-news_count资讯数 | FUNC-00018 | 已覆盖 | |
| L01 \| chain.basic.news-stats \| _empty \| 动态资讯无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.news-stats \| _fail \| 动态资讯查询失败 | FUNC-00019 | 部分覆盖 | |
| L01 \| chain.basic.sz-elements \| chainId \| 算法输入-chainId产业标识 | FUNC-00020、00021 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| enterprise_count \| 算法输出-enterprise_count深圳企业数 | FUNC-00020 | 已覆盖 | |
| L01 \| chain.basic.sz-elements \| institution_count \| 算法输出-institution_count深圳机构数 | FUNC-00020 | 已覆盖 | 同条主流程 |
| L01 \| chain.basic.sz-elements \| _empty \| 深圳要素无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.sz-elements \| _fail \| 深圳要素查询失败 | FUNC-00021 | 部分覆盖 | |
| L01 \| chain.basic.sz-dist \| chainId \| 算法输入-chainId产业标识 | FUNC-00022、00023 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| district \| 算法输出-district行政区 | FUNC-00022 | 已覆盖 | |
| L01 \| chain.basic.sz-dist \| _empty \| 深圳分布无数据空态 | — | 未覆盖 | |
| L01 \| chain.basic.sz-dist \| _fail \| 深圳分布查询失败 | FUNC-00023 | 部分覆盖 | |

---

## req_only 行（无 endpoint 挂接）

L01.md 中 `etl_clean_standardize`、`metric_validity_check`、`mq_result_sync` 等 **req_only** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

---

## B 线页面清单（无 A 线 field 键）

| 场景 | 用例编号 | 状态 |
|------|----------|------|
| 接口信息-清单 | FUNC-00024 | 已覆盖 |
| 算法测试-清单 | FUNC-00025 | 已覆盖 |
