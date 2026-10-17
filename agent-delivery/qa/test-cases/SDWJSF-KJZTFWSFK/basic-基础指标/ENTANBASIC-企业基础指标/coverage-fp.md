# 企业基础指标 · 功能点覆盖（entan.basic / L02）

> catalog `entan.basic` · 50897 · path `#/entan/basic`  
> **用例册**：`API-企业基础指标-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00063`～`00074`，共 **12** 条）  
> A 线范围：**L02**（`fp-split-by-api-run/work/L02.md`，50 行）  
> 功能点键：`L02 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.basic.filters | GET | /entan/v1/meta/filters | API-00063、00064 | unavailable；金样+鉴权 |
| entan.basic.key-enterprises | GET | /entan/v1/key-enterprises | API-00065、00071 | unavailable |
| entan.basic.type-distribution | GET | /entan/v1/type-distribution | API-00066、00072 | unavailable |
| entan.basic.domain-distribution | GET | /entan/v1/domain-distribution | API-00067 | unavailable |
| entan.basic.new-enterprises | GET | /entan/v1/new-enterprises | API-00068 | unavailable |
| entan.news.stats | GET | /entan/v1/news/stats | API-00069、00073 | unavailable |
| entan.news.list | GET | /entan/v1/news | API-00070、00074 | unavailable |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L02 \| entan.basic.filters \| industries \| 算法输出-industries行业选项 | catalog industries | API-00063 | 契约占位 | 金样断言 array 形态；endpoint unavailable |
| L02 \| entan.basic.filters \| cities \| 算法输出-cities城市选项 | catalog cities | API-00063 | 契约占位 | 同上 |
| L02 \| entan.basic.filters \| domains \| 算法输出-domains领域选项 | catalog domains | API-00063 | 契约占位 | 同上 |
| L02 \| entan.basic.filters \| years \| 算法输出-years年份选项 | catalog years | API-00063 | 契约占位 | 同上 |
| L02 \| entan.basic.filters \| _empty \| 筛选项无数据空态 | 契约空结果 | — | 未覆盖 | unavailable + 未试调，无稳定空枚举构造 |
| L02 \| entan.basic.filters \| _fail \| 筛选项查询失败 | 契约错误态 | — | 未覆盖 | 无参接口无可构造单点失败态，待网关/上游故障复核 |
| L02 \| entan.basic.key-enterprises \| industry \| 算法输入-industry行业 | catalog industry | API-00065 | 契约占位 | KEY-01 含 industry |
| L02 \| entan.basic.key-enterprises \| city \| 算法输入-city城市 | catalog city | API-00065 | 契约占位 | KEY-01 含 city |
| L02 \| entan.basic.key-enterprises \| scale \| 算法输入-scale企业规模 | catalog scale | API-00065 | 契约占位 | KEY-01 含 scale |
| L02 \| entan.basic.key-enterprises \| limit \| 算法输入-limit条数上限 | catalog limit | API-00065、00071 | 部分覆盖 | 合法组合+非法 limit；live 后补截断策略 |
| L02 \| entan.basic.key-enterprises \| enterprise_name \| 算法输出-enterprise_name企业名称 | catalog enterprise_name | API-00065 | 契约占位 | 禁止 sample 名称作通过条件 |
| L02 \| entan.basic.key-enterprises \| key_score \| 算法输出-key_score重点得分 | catalog key_score | API-00065 | 契约占位 | |
| L02 \| entan.basic.key-enterprises \| _empty \| 重点企业无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果条件 |
| L02 \| entan.basic.key-enterprises \| _fail \| 重点企业查询失败 | 契约错误态 | API-00071 | 部分覆盖 | 非法 limit；若现场仍成功空列表需标部分覆盖 |
| L02 \| entan.basic.type-distribution \| year \| 算法输入-year统计年份 | catalog year | API-00066、00072 | 部分覆盖 | TYP-01/TYP-02 |
| L02 \| entan.basic.type-distribution \| rows \| 算法输出-rows类型分布行集 | catalog rows | API-00066 | 契约占位 | |
| L02 \| entan.basic.type-distribution \| _empty \| 类型分布无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空态年份 |
| L02 \| entan.basic.type-distribution \| _fail \| 类型分布查询失败 | 契约错误态 | API-00072 | 部分覆盖 | 非法 year |
| L02 \| entan.basic.domain-distribution \| year \| 算法输入-year统计年份 | catalog year | API-00067 | 契约占位 | DOM-01 |
| L02 \| entan.basic.domain-distribution \| rows \| 算法输出-rows领域分布行集 | catalog rows | API-00067 | 契约占位 | |
| L02 \| entan.basic.domain-distribution \| _empty \| 领域分布无数据空态 | 契约空结果 | — | 未覆盖 | |
| L02 \| entan.basic.domain-distribution \| _fail \| 领域分布查询失败 | 契约错误态 | API-00067 | 契约占位 | 与不可用契约合并 |
| L02 \| entan.basic.new-enterprises \| domain \| 算法输入-domain领域标签 | catalog domain | API-00068 | 契约占位 | NEW-01 |
| L02 \| entan.basic.new-enterprises \| rows \| 算法输出-rows新增企业行集 | catalog rows | API-00068 | 契约占位 | |
| L02 \| entan.basic.new-enterprises \| _empty \| 新增企业无数据空态 | 契约空结果 | — | 未覆盖 | |
| L02 \| entan.basic.new-enterprises \| _fail \| 新增企业查询失败 | 契约错误态 | API-00068 | 契约占位 | |
| L02 \| entan.news.stats \| news_type \| 算法输入-news_type资讯类型 | catalog news_type | API-00069、00073 | 部分覆盖 | 全量+非法类型 |
| L02 \| entan.news.stats \| stat_month \| 算法输出-stat_month统计月份 | catalog stat_month | API-00069 | 契约占位 | |
| L02 \| entan.news.stats \| type_name \| 算法输出-type_name类型名称 | catalog type_name | API-00069 | 契约占位 | |
| L02 \| entan.news.stats \| news_count \| 算法输出-news_count资讯条数 | catalog news_count | API-00069 | 契约占位 | |
| L02 \| entan.news.stats \| total_amount \| 算法输出-total_amount金额合计 | catalog total_amount | API-00069 | 契约占位 | |
| L02 \| entan.news.stats \| growth_rate \| 算法输出-growth_rate增长率 | catalog growth_rate | API-00069 | 契约占位 | |
| L02 \| entan.news.stats \| _empty \| 资讯统计无数据空态 | 契约空结果 | — | 未覆盖 | |
| L02 \| entan.news.stats \| _fail \| 资讯统计查询失败 | 契约错误态 | API-00073 | 部分覆盖 | 非法 news_type |
| L02 \| entan.news.list \| news_type \| 算法输入-news_type资讯类型 | catalog news_type | API-00070 | 契约占位 | NLST-01 |
| L02 \| entan.news.list \| keyword \| 算法输入-keyword关键词 | catalog keyword | API-00070 | 契约占位 | NLST-01 不传 keyword |
| L02 \| entan.news.list \| page \| 算法输入-page页码 | catalog page | API-00070、00074 | 部分覆盖 | 合法 page + 非法 page |
| L02 \| entan.news.list \| size \| 算法输入-size页大小 | catalog size | API-00070 | 契约占位 | NLST-01 |
| L02 \| entan.news.list \| list \| 算法输出-list资讯列表 | catalog list | API-00070 | 契约占位 | |
| L02 \| entan.news.list \| _empty \| 资讯明细无数据空态 | 契约空结果 | — | 未覆盖 | |
| L02 \| entan.news.list \| _fail \| 资讯明细查询失败 | 契约错误态 | API-00074 | 部分覆盖 | 非法 page |
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
| 契约占位 | 28 |
| 部分覆盖 | 8 |
| 未覆盖 | 14 |
| **合计** | **50** |

- catalog `responseFields` 均已挂接用例号（金样或契约占位）。
- `_empty` 共 7 行：**未覆盖**（原因见上表）。
- req_only 9 行：**未覆盖**（无 HTTP endpoint）。
