# 政策基础指标 · 功能点覆盖（policy.basic / L03）

> catalog `policy.basic` · 50897 · path `#/policy/basic`  
> **用例册**：`API-政策基础指标-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000409`～`000418`，共 **10** 条）  
> A 线范围：**L03**（`fp-split-by-api-run/work/L03.md`，20 行）  
> 功能点键：`L03 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.basic.metrics | GET | /policy/v1/policy/metrics | API-000409～000413 | unavailable；金样+鉴权+形态 |
| policy.basic.indicators | GET | /policy/v1/policy/indicators | API-000414～000418 | unavailable；金样+kind 组合 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L03 \| policy.basic.metrics \| headline \| 算法输出-headline头部KPI | catalog headline | API-000409、000411 | 契约占位 | 金样+object 形态；禁止 sample KPI 数值 |
| L03 \| policy.basic.metrics \| _empty \| 总览无数据空态 | 契约空结果 | API-000412 | 契约占位 | 无稳定空总览构造；执行期记录 |
| L03 \| policy.basic.metrics \| _fail \| 总览查询失败 | 契约错误态 | API-000413 | 部分覆盖 | 无参接口无单缺陷；待网关/上游复核 |
| L03 \| policy.basic.indicators \| kind \| 算法输入-kind指标维度 | catalog kind | API-000414、000415、000416、000417、000418 | 部分覆盖 | all/单维/非法 kind |
| L03 \| policy.basic.indicators \| level \| 算法输出-level政策级别分布 | catalog level | API-000414、000415 | 契约占位 | IND-01/02；样例含 level_name 等未单列断言 |
| L03 \| policy.basic.indicators \| type \| 算法输出-type政策类型分布 | catalog type | API-000414 | 契约占位 | kind=all 块存在性；单维 type 未单列用例 |
| L03 \| policy.basic.indicators \| timeseries \| 算法输出-timeseries发布时序 | catalog timeseries | API-000414、000416 | 契约占位 | IND-01/03 array 形态 |
| L03 \| policy.basic.indicators \| national \| 算法输出-national全国分布 | catalog national | API-000414、000418 | 契约占位 | IND-01/05 |
| L03 \| policy.basic.indicators \| sz \| 算法输出-sz深圳分布 | catalog sz | API-000414 | 契约占位 | kind=all 覆盖；单维 sz 未单列用例 |
| L03 \| policy.basic.indicators \| _empty \| 五维指标无数据空态 | 契约空结果 | — | 未覆盖 | unavailable + 未试调，无稳定空块构造 |
| L03 \| policy.basic.indicators \| _fail \| 五维指标查询失败 | 契约错误态 | API-000417 | 部分覆盖 | 非法 kind；若现场仍成功空块需标部分覆盖 |
| L03 \| （无 endpoint） \| etl_clean_standardize \| 统一预处理与清洗 | 需规总述清洗 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| metric_validity_check \| 指标有效性验证 | 需规有效性验证 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| mq_result_sync \| 消息队列结果同步 | 需规数据同步 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| scheduled_refresh_monitor \| 定期更新与监测 | 需规更新监测 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| level_growth_rate \| 政策级别环比趋势 | 需规（1）环比 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| type_growth_rate \| 政策类型环比增长率 | 需规（2）环比 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| timeseries_growth_rate \| 发布数量环比增长率 | 需规（3）环比 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| national_growth_rate \| 省级数量环比增长率 | 需规（4）环比 | — | 未覆盖 | req_only |
| L03 \| （无 endpoint） \| sz_growth_rate \| 区级分布环比增长率 | 需规（5）环比 | — | 未覆盖 | req_only |

---

## 3. 统计（交卷）

| 状态 | 条数 |
|------|------|
| 契约占位 | 7 |
| 部分覆盖 | 3 |
| 未覆盖 | 10 |

| 项 | 值 |
|----|-----|
| API 用例条数 | **10** |
| 编号闭区间 | **API-000409**～**API-000418** |
| endpoint 数 | **2**（各 5 条） |
| `_empty`（indicators 稳定空态） | **未覆盖** 1 行 |
| 50897 试调 | **未试调**（见用例 §0） |
| FUNC 条数 | **0** |

---

## 4. 无对应 A 线功能点的用例

无（本册 10 条均可挂接 L03 catalog 行或契约哨兵）。
