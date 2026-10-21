# 服务机构基础指标 · 功能点覆盖（svc.basic / L04）

> catalog `svc.basic` · path `#/industry-service/basic`  
> A 线真源：`fp-split-by-api-run/work/L04.md`  
> B 线用例：`FUNC-服务机构基础指标-用例.md`（第三轮 **FUNC-00080**～**FUNC-00099**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.basic.indicators | GET | /entan/v1/svc/indicators | FUNC-00080～00082 | unavailable |
| svc.basic.indicators-layout | GET | /entan/v1/svc/indicators | FUNC-00083～00085 | unavailable |
| svc.basic.indicators-global | GET | /entan/v1/svc/indicators | FUNC-00086～00088 | unavailable |
| svc.basic.indicators-invest | GET | /entan/v1/svc/indicators | FUNC-00089～00091 | unavailable |
| svc.basic.indicators-new | GET | /entan/v1/svc/indicators | FUNC-00092～00094 | unavailable |
| svc.basic.indicators-sz | GET | /entan/v1/svc/indicators | FUNC-00095～00097 | unavailable |
| （页面清单） | — | — | FUNC-00098、00099 | — |

---

## 功能点 → 用例矩阵（挂 L04.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L04 \| svc.basic.indicators \| kind \| 算法输入-kind指标类型 | FUNC-00080、00081、00082 | 已覆盖 | sample kind=all + 省略 kind + 非法 kind |
| L04 \| svc.basic.indicators \| layout \| 算法输出-layout产业布局体 | FUNC-00080、00081 | 已覆盖 | 全维度主流程与省略 kind 断言 layout 元素字段 |
| L04 \| svc.basic.indicators \| global \| 算法输出-global全球分布体 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| invest \| 算法输出-invest投融资体 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| new \| 算法输出-new新增动态体 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| sz_scale \| 算法输出-sz_scale深圳规模体 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| sz_dist \| 算法输出-sz_dist深圳分布体 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| org_total \| 算法输出-org_total机构总数 | FUNC-00080、00081 | 已覆盖 | responseFields 有该键；sampleResponse 无示例值 |
| L04 \| svc.basic.indicators \| pt_global_total \| 算法输出-pt_global_total全球平台总量 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| org_new_count \| 算法输出-org_new_count机构新增数 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_type_dist \| 算法输出-pt_type_dist类型分布 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_region \| 算法输出-pt_region区域分布 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_scale_dist \| 算法输出-pt_scale_dist规模分布 | FUNC-00080、00081 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| _empty \| 指标查询无数据空态 | — | 未覆盖 | 无稳定空块构造条件 |
| L04 \| svc.basic.indicators \| _fail \| 指标查询失败 | FUNC-00082 | 部分覆盖 | 仅非法 kind 反向（message/msg） |

---

## B 线独有 endpoint（L04 未列 endpoint_id）

后五个下拉标题与 `svc.basic.indicators` 同 path，A 线仍只挂全维度一行。下列用例不另开 field 行，记 **无对应功能点**。

| endpoint_id | 用例编号 | 说明 |
|-------------|----------|------|
| svc.basic.indicators-layout | FUNC-00083、00084、00085 | 主流程 kind=layout；备选省略 kind；反向非法 kind |
| svc.basic.indicators-global | FUNC-00086、00087、00088 | 主流程 kind=global |
| svc.basic.indicators-invest | FUNC-00089、00090、00091 | 主流程 kind=invest |
| svc.basic.indicators-new | FUNC-00092、00093、00094 | 主流程 kind=new |
| svc.basic.indicators-sz | FUNC-00095、00096、00097 | 主流程 kind=sz |

---

## req_only 行（无 endpoint 挂接）

L04.md 中 `etl_clean_standardize`、`metric_validity_check`、`mq_result_sync`、`scheduled_refresh_monitor`、`layout_growth_rate`、`global_dist_trend`、`invest_growth_rate`、`invest_timeseries_analysis`、`new_org_growth_rate`、`sz_scale_growth_rate`、`sz_scale_capability_breakdown`、`sz_dist_growth_rate`、`sz_dist_type_share_analysis` 共 **13** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。
