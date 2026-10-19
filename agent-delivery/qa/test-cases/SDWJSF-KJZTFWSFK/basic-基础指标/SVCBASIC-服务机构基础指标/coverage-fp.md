# 服务机构基础指标 · 功能点覆盖（svc.basic / L04）

> catalog `svc.basic` · path `#/industry-service/basic`  
> A 线真源：`fp-split-by-api-run/work/L04.md`  
> B 线用例：`API-服务机构基础指标-用例.md`（第二轮 **API-01518**～**01535**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.basic.indicators | GET | /entan/v1/svc/indicators | API-01518～01520 | unavailable |
| svc.basic.indicators-layout | GET | /entan/v1/svc/indicators | API-01521～01523 | unavailable |
| svc.basic.indicators-global | GET | /entan/v1/svc/indicators | API-01524～01526 | unavailable |
| svc.basic.indicators-invest | GET | /entan/v1/svc/indicators | API-01527～01529 | unavailable |
| svc.basic.indicators-new | GET | /entan/v1/svc/indicators | API-01530～01532 | unavailable |
| svc.basic.indicators-sz | GET | /entan/v1/svc/indicators | API-01533～01535 | unavailable |

---

## 功能点 → 用例矩阵（挂 L04.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L04 \| svc.basic.indicators \| kind \| 算法输入-kind指标类型 | API-01518、01519、01520 | 已覆盖 | sample kind=all + 省略 kind + 非法 kind |
| L04 \| svc.basic.indicators \| layout \| 算法输出-layout产业布局体 | API-01518、01519 | 已覆盖 | 全维度主流程与省略 kind 断言 layout 元素字段 |
| L04 \| svc.basic.indicators \| global \| 算法输出-global全球分布体 | API-01518、01519 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| invest \| 算法输出-invest投融资体 | API-01518、01519 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| new \| 算法输出-new新增动态体 | API-01518、01519 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| sz_scale \| 算法输出-sz_scale深圳规模体 | API-01518、01519 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| sz_dist \| 算法输出-sz_dist深圳分布体 | API-01518、01519 | 已覆盖 | 同条全维度正向 |
| L04 \| svc.basic.indicators \| org_total \| 算法输出-org_total机构总数 | API-01518、01519 | 已覆盖 | responseFields 有该键；sampleResponse 无示例值 |
| L04 \| svc.basic.indicators \| pt_global_total \| 算法输出-pt_global_total全球平台总量 | API-01518、01519 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| org_new_count \| 算法输出-org_new_count机构新增数 | API-01518、01519 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_type_dist \| 算法输出-pt_type_dist类型分布 | API-01518、01519 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_region \| 算法输出-pt_region区域分布 | API-01518、01519 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| pt_scale_dist \| 算法输出-pt_scale_dist规模分布 | API-01518、01519 | 已覆盖 | 同条全维度正向；sample 无示例值 |
| L04 \| svc.basic.indicators \| _empty \| 指标查询无数据空态 | — | 未覆盖 | 无稳定空块构造条件 |
| L04 \| svc.basic.indicators \| _fail \| 指标查询失败 | API-01520 | 部分覆盖 | 仅非法 kind 反向（message/msg） |

---

## B 线独有 endpoint（L04 未列 endpoint_id）

后五个下拉标题与 `svc.basic.indicators` 同 path，A 线仍只挂全维度一行。下列用例不另开 field 行，记 **无对应功能点**。

| endpoint_id | 用例编号 | 说明 |
|-------------|----------|------|
| svc.basic.indicators-layout | API-01521、01522、01523 | 主流程 kind=layout；备选省略 kind；反向非法 kind |
| svc.basic.indicators-global | API-01524、01525、01526 | 主流程 kind=global |
| svc.basic.indicators-invest | API-01527、01528、01529 | 主流程 kind=invest |
| svc.basic.indicators-new | API-01530、01531、01532 | 主流程 kind=new |
| svc.basic.indicators-sz | API-01533、01534、01535 | 主流程 kind=sz |

---

## req_only 行（无 endpoint 挂接）

L04.md 中 `etl_clean_standardize`、`metric_validity_check`、`mq_result_sync`、`scheduled_refresh_monitor`、`layout_growth_rate`、`global_dist_trend`、`invest_growth_rate`、`invest_timeseries_analysis`、`new_org_growth_rate`、`sz_scale_growth_rate`、`sz_scale_capability_breakdown`、`sz_dist_growth_rate`、`sz_dist_type_share_analysis` 共 **13** 行无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
