# 企业基础指标 · 功能点覆盖（entan.basic / L02）

> catalog `entan.basic` · path `#/entan/basic`  
> **用例册**：`FUNC-企业基础指标-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00026`～**00058**，共 **33** 条，第三轮）  
> A 线范围：**L02**（`fp-split-by-api-run/work/L02.md`，50 行）  
> 功能点键：`L02 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.basic.filters | GET | /entan/v1/meta/filters | FUNC-00026 | unavailable；金样 |
| entan.basic.key-enterprises | GET | /entan/v1/key-enterprises | FUNC-00027～00035 | unavailable |
| entan.basic.type-distribution | GET | /entan/v1/type-distribution | FUNC-00036～00038 | unavailable |
| entan.basic.domain-distribution | GET | /entan/v1/domain-distribution | FUNC-00039～00041 | unavailable |
| entan.basic.new-enterprises | GET | /entan/v1/new-enterprises | FUNC-00042～00044 | unavailable |
| entan.news.stats | GET | /entan/v1/news/stats | FUNC-00045～00047 | unavailable |
| entan.news.list | GET | /entan/v1/news | FUNC-00048～00056 | unavailable |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L02 \| entan.basic.filters \| industries \| 算法输出-industries行业选项 | catalog industries | FUNC-00026 | 已覆盖 | 正向 body 含 industries array |
| L02 \| entan.basic.filters \| cities \| 算法输出-cities城市选项 | catalog cities | FUNC-00026 | 已覆盖 | 同上 |
| L02 \| entan.basic.filters \| domains \| 算法输出-domains领域选项 | catalog domains | FUNC-00026 | 已覆盖 | 同上 |
| L02 \| entan.basic.filters \| years \| 算法输出-years年份选项 | catalog years | FUNC-00026 | 已覆盖 | 同上 |
| L02 \| entan.basic.filters \| _empty \| 筛选项无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空枚举构造条件 |
| L02 \| entan.basic.filters \| _fail \| 筛选项查询失败 | 契约错误态 | — | 未覆盖 | 无参接口无单参反向 |
| L02 \| entan.basic.key-enterprises \| industry \| 算法输入-industry行业 | catalog industry | FUNC-00027、00914、00918 | 已覆盖 | 全参/省略/非法 |
| L02 \| entan.basic.key-enterprises \| city \| 算法输入-city城市 | catalog city | FUNC-00027、00915、00919 | 已覆盖 | |
| L02 \| entan.basic.key-enterprises \| scale \| 算法输入-scale企业规模 | catalog scale | FUNC-00027、00916、00920 | 已覆盖 | |
| L02 \| entan.basic.key-enterprises \| limit \| 算法输入-limit条数上限 | catalog limit | FUNC-00027、00917、00921 | 已覆盖 | |
| L02 \| entan.basic.key-enterprises \| enterprise_name \| 算法输出-enterprise_name企业名称 | catalog enterprise_name | FUNC-00027 | 已覆盖 | 正向 body 字段 |
| L02 \| entan.basic.key-enterprises \| key_score \| 算法输出-key_score重点得分 | catalog key_score | FUNC-00027 | 已覆盖 | |
| L02 \| entan.basic.key-enterprises \| _empty \| 重点企业无数据空态 | 契约空结果 | FUNC-00028 | 部分覆盖 | 省略 industry 正向允许空 array |
| L02 \| entan.basic.key-enterprises \| _fail \| 重点企业查询失败 | 契约错误态 | FUNC-00032～00921 | 已覆盖 | 四参数各 1 反向 |
| L02 \| entan.basic.type-distribution \| year \| 算法输入-year统计年份 | catalog year | FUNC-00036、00923、00924 | 已覆盖 | |
| L02 \| entan.basic.type-distribution \| rows \| 算法输出-rows类型分布行集 | catalog rows | FUNC-00036 | 已覆盖 | |
| L02 \| entan.basic.type-distribution \| _empty \| 类型分布无数据空态 | 契约空结果 | FUNC-00037 | 部分覆盖 | 不传 year 正向允许空 rows |
| L02 \| entan.basic.type-distribution \| _fail \| 类型分布查询失败 | 契约错误态 | FUNC-00038 | 已覆盖 | 非法 year |
| L02 \| entan.basic.domain-distribution \| year \| 算法输入-year统计年份 | catalog year | FUNC-00039、00926、00927 | 已覆盖 | |
| L02 \| entan.basic.domain-distribution \| rows \| 算法输出-rows领域分布行集 | catalog rows | FUNC-00039 | 已覆盖 | 含 growth_rate |
| L02 \| entan.basic.domain-distribution \| _empty \| 领域分布无数据空态 | 契约空结果 | FUNC-00040 | 部分覆盖 | |
| L02 \| entan.basic.domain-distribution \| _fail \| 领域分布查询失败 | 契约错误态 | FUNC-00041 | 已覆盖 | |
| L02 \| entan.basic.new-enterprises \| domain \| 算法输入-domain领域标签 | catalog domain | FUNC-00042、00929、00930 | 已覆盖 | |
| L02 \| entan.basic.new-enterprises \| rows \| 算法输出-rows新增企业行集 | catalog rows | FUNC-00042 | 已覆盖 | |
| L02 \| entan.basic.new-enterprises \| _empty \| 新增企业无数据空态 | 契约空结果 | FUNC-00043 | 部分覆盖 | |
| L02 \| entan.basic.new-enterprises \| _fail \| 新增企业查询失败 | 契约错误态 | FUNC-00044 | 已覆盖 | |
| L02 \| entan.news.stats \| news_type \| 算法输入-news_type资讯类型 | catalog news_type | FUNC-00045、00932、00933 | 已覆盖 | 全量+融资+非法 |
| L02 \| entan.news.stats \| stat_month \| 算法输出-stat_month统计月份 | catalog stat_month | FUNC-00045 | 已覆盖 | |
| L02 \| entan.news.stats \| type_name \| 算法输出-type_name类型名称 | catalog type_name | FUNC-00045 | 已覆盖 | |
| L02 \| entan.news.stats \| news_count \| 算法输出-news_count资讯条数 | catalog news_count | FUNC-00045 | 已覆盖 | |
| L02 \| entan.news.stats \| total_amount \| 算法输出-total_amount金额合计 | catalog total_amount | FUNC-00045 | 已覆盖 | |
| L02 \| entan.news.stats \| growth_rate \| 算法输出-growth_rate增长率 | catalog growth_rate | FUNC-00045 | 已覆盖 | |
| L02 \| entan.news.stats \| _empty \| 资讯统计无数据空态 | 契约空结果 | FUNC-00046 | 部分覆盖 | 单类型无数据时可空 array |
| L02 \| entan.news.stats \| _fail \| 资讯统计查询失败 | 契约错误态 | FUNC-00047 | 已覆盖 | |
| L02 \| entan.news.list \| news_type \| 算法输入-news_type资讯类型 | catalog news_type | FUNC-00048、00935、00939 | 已覆盖 | |
| L02 \| entan.news.list \| keyword \| 算法输入-keyword关键词 | catalog keyword | FUNC-00048、00936、00940 | 已覆盖 | |
| L02 \| entan.news.list \| page \| 算法输入-page页码 | catalog page | FUNC-00048、00937、00941 | 已覆盖 | |
| L02 \| entan.news.list \| size \| 算法输入-size页大小 | catalog size | FUNC-00048、00938、00942 | 已覆盖 | |
| L02 \| entan.news.list \| list \| 算法输出-list资讯列表 | catalog list | FUNC-00048 | 已覆盖 | |
| L02 \| entan.news.list \| _empty \| 资讯明细无数据空态 | 契约空结果 | FUNC-00050 | 部分覆盖 | keyword 过滤无命中可空 list |
| L02 \| entan.news.list \| _fail \| 资讯明细查询失败 | 契约错误态 | FUNC-00053～00942 | 已覆盖 | 四参数反向 |
| L02 \| （无 endpoint） \| etl_clean_standardize \| 统一预处理与清洗 | 需规总述清洗 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| metric_validity_check \| 指标有效性验证 | 需规有效性验证 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| mq_result_sync \| 消息队列结果同步 | 需规数据同步 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| scheduled_refresh_monitor \| 定期更新与监测 | 需规更新监测 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| key_enterprise_threshold_rule \| 专利与技术交易阈值筛选 | 需规（1）阈值 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| type_dist_count_share_growth \| 类型数量占比与环比 | 需规（2）占比环比 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| domain_dist_growth_rate \| 产业链技术链环比 | 需规（3）环比 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| news_ma_coop_product_metrics \| 并购合作新品细化指标 | 需规（4）细化指标 | — | 未覆盖 | req_only |
| L02 \| （无 endpoint） \| new_enterprise_growth_rate \| 新增数量环比趋势 | 需规（5）环比 | — | 未覆盖 | req_only |

---

## 3. 矩阵摘要

| 状态 | 行数 |
|------|------|
| 已覆盖 | 33 |
| 部分覆盖 | 8 |
| 未覆盖 | 9 |
| **合计** | **50** |

- catalog 7 个 endpoint 均有对应用例；`responseFields` 与主要输出 field 已挂接正向用例。
- `_empty` 7 行：**部分覆盖** 6 + **未覆盖** 1（filters 无参无 _fail/_empty 专用用例）。
- req_only 9 行：**未覆盖**（无 HTTP endpoint）。
