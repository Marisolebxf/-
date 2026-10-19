# 政策基础指标 · 功能点覆盖（policy.basic / L03）

> catalog `policy.basic` · path `#/policy/basic`  
> A 线真源：`fp-split-by-api-run/work/L03.md`（20 行）  
> B 线用例：`API-政策基础指标-用例.md`（第二轮 **API-01314**～**01332**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.basic.metrics | GET | /policy/v1/policy/metrics | API-01314 | unavailable |
| policy.basic.indicators | GET | /policy/v1/policy/indicators | API-01315～01317 | unavailable |
| policy.basic.indicators-level | GET | /policy/v1/policy/indicators | API-01318～01320 | unavailable |
| policy.basic.indicators-type | GET | /policy/v1/policy/indicators | API-01321～01323 | unavailable |
| policy.basic.indicators-timeseries | GET | /policy/v1/policy/indicators | API-01324～01326 | unavailable |
| policy.basic.indicators-national | GET | /policy/v1/policy/indicators | API-01327～01329 | unavailable |
| policy.basic.indicators-sz | GET | /policy/v1/policy/indicators | API-01330～01332 | unavailable |

---

## 功能点 → 用例矩阵（挂 L03.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L03 \| policy.basic.metrics \| headline \| 算法输出-headline头部KPI | API-01314 | 已覆盖 | 主流程断言 headline 及六个 KPI 字段 |
| L03 \| policy.basic.metrics \| _empty \| 总览无数据空态 | — | 未覆盖 | 无参接口无稳定空总览构造 |
| L03 \| policy.basic.metrics \| _fail \| 总览查询失败 | — | 未覆盖 | 无参接口无单点入参反向 |
| L03 \| policy.basic.indicators \| kind \| 算法输入-kind指标维度 | API-01315、01316、01317 | 已覆盖 | sample kind=all + 省略 kind + 非法 kind |
| L03 \| policy.basic.indicators \| level \| 算法输出-level政策级别分布 | API-01315、01316 | 已覆盖 | 全维度主流程与省略 kind 断言 level 元素字段 |
| L03 \| policy.basic.indicators \| type \| 算法输出-type政策类型分布 | API-01315、01316 | 已覆盖 | 同条全维度正向 |
| L03 \| policy.basic.indicators \| timeseries \| 算法输出-timeseries发布时序 | API-01315、01316 | 已覆盖 | 同条全维度正向 |
| L03 \| policy.basic.indicators \| national \| 算法输出-national全国分布 | API-01315、01316 | 已覆盖 | 同条全维度正向 |
| L03 \| policy.basic.indicators \| sz \| 算法输出-sz深圳分布 | API-01315、01316 | 已覆盖 | 同条全维度正向 |
| L03 \| policy.basic.indicators \| _empty \| 五维指标无数据空态 | — | 未覆盖 | 无稳定空块构造 |
| L03 \| policy.basic.indicators \| _fail \| 五维指标查询失败 | API-01317 | 部分覆盖 | 仅非法 kind 反向（message/msg） |
| L03 \| （无 endpoint） \| etl_clean_standardize \| 统一预处理与清洗 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| metric_validity_check \| 指标有效性验证 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| mq_result_sync \| 消息队列结果同步 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| scheduled_refresh_monitor \| 定期更新与监测 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| level_growth_rate \| 政策级别环比趋势 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| type_growth_rate \| 政策类型环比增长率 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| timeseries_growth_rate \| 发布数量环比增长率 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| national_growth_rate \| 省级数量环比增长率 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| sz_growth_rate \| 区级分布环比增长率 | — | 未覆盖 | req_only |

---

## B 线独有 endpoint（L03 未列 endpoint_id）

后五个下拉标题与 `policy.basic.indicators` 同 path，A 线仍只挂全维度一行。下列用例不另开 field 行，记 **无对应功能点**。

| endpoint_id | 用例编号 | 说明 |
|-------------|----------|------|
| policy.basic.indicators-level | API-01318、01319、01320 | 主流程 kind=level；备选省略 kind；反向非法 kind |
| policy.basic.indicators-type | API-01321、01322、01323 | 主流程 kind=type |
| policy.basic.indicators-timeseries | API-01324、01325、01326 | 主流程 kind=timeseries |
| policy.basic.indicators-national | API-01327、01328、01329 | 主流程 kind=national |
| policy.basic.indicators-sz | API-01330、01331、01332 | 主流程 kind=sz |

---

## req_only 行（无 endpoint 挂接）

L03.md 中 `etl_clean_standardize`、`metric_validity_check`、`mq_result_sync`、`scheduled_refresh_monitor`、`level_growth_rate`、`type_growth_rate`、`timeseries_growth_rate`、`national_growth_rate`、`sz_growth_rate` 共 **9** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
