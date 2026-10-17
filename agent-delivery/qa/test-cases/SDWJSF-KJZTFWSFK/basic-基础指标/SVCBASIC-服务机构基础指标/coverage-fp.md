# 服务机构基础指标 · 功能点覆盖（svc.basic / L04）

> catalog `svc.basic` · 50897 · path `#/industry-service/basic`  
> **用例册**：`API-服务机构基础指标-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00529`～`00533`，共 **5** 条）  
> A 线范围：**L04**（`fp-split-by-api-run/work/L04.md`，28 行）  
> 功能点键：`L04 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.basic.indicators | GET | /entan/v1/svc/indicators | API-00529～00533 | unavailable；金样+鉴权+形态+kind |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L04 \| svc.basic.indicators \| kind \| 算法输入-kind指标类型 | catalog kind | API-00529、00531、00532、00533 | 部分覆盖 | all/stat21/非法 kind |
| L04 \| svc.basic.indicators \| layout \| 算法输出-layout产业布局体 | catalog layout | API-00529、00531 | 契约占位 | IND-01 array 形态 |
| L04 \| svc.basic.indicators \| global \| 算法输出-global全球分布体 | catalog global | API-00529、00531 | 契约占位 | IND-01 array 形态 |
| L04 \| svc.basic.indicators \| invest \| 算法输出-invest投融资体 | catalog invest | API-00529 | 契约占位 | kind=all 块存在性未单列断言 |
| L04 \| svc.basic.indicators \| new \| 算法输出-new新增动态体 | catalog new | API-00529 | 契约占位 | kind=all 覆盖 |
| L04 \| svc.basic.indicators \| sz_scale \| 算法输出-sz_scale深圳规模体 | catalog sz_scale | API-00529 | 契约占位 | kind=all 覆盖 |
| L04 \| svc.basic.indicators \| sz_dist \| 算法输出-sz_dist深圳分布体 | catalog sz_dist | API-00529 | 契约占位 | kind=all 覆盖 |
| L04 \| svc.basic.indicators \| org_total \| 算法输出-org_total机构总数 | catalog org_total | API-00529、00532 | 契约占位 | IND-02 object 形态 |
| L04 \| svc.basic.indicators \| pt_global_total \| 算法输出-pt_global_total全球平台总量 | catalog pt_global_total | API-00532 | 契约占位 | kind=stat21 形态参考 |
| L04 \| svc.basic.indicators \| org_new_count \| 算法输出-org_new_count机构新增数 | catalog org_new_count | API-00529 | 契约占位 | 未单列 array 断言 |
| L04 \| svc.basic.indicators \| pt_type_dist \| 算法输出-pt_type_dist类型分布 | catalog pt_type_dist | API-00532 | 契约占位 | IND-02 array 形态 |
| L04 \| svc.basic.indicators \| pt_region \| 算法输出-pt_region区域分布 | catalog pt_region | API-00529 | 契约占位 | 未单列用例 |
| L04 \| svc.basic.indicators \| pt_scale_dist \| 算法输出-pt_scale_dist规模分布 | catalog pt_scale_dist | API-00529 | 契约占位 | 未单列用例 |
| L04 \| svc.basic.indicators \| _empty \| 指标查询无数据空态 | 契约空结果 | — | 未覆盖 | unavailable + 未试调，无稳定空块构造 |
| L04 \| svc.basic.indicators \| _fail \| 指标查询失败 | 契约错误态 | API-00533 | 部分覆盖 | 非法 kind；若现场仍成功空块需标部分覆盖 |
| L04 \| （无 endpoint） \| etl_clean_standardize \| 统一预处理与清洗 | 需规总述清洗 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| metric_validity_check \| 指标有效性验证 | 需规有效性验证 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| mq_result_sync \| 消息队列结果同步 | 需规数据同步 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| scheduled_refresh_monitor \| 定期更新与监测 | 需规更新监测 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| layout_growth_rate \| 产业布局服务规模环比增长率 | 需规（1）环比 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| global_dist_trend \| 各国数量对比与分布趋势 | 需规（2）分布趋势 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| invest_growth_rate \| 投融资规模环比增长率 | 需规（3）环比 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| invest_timeseries_analysis \| 投融资时间序列分析 | 需规（3）时序 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| new_org_growth_rate \| 机构新增数量环比增长率 | 需规（4）环比 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| sz_scale_growth_rate \| 深圳规模环比增长率 | 需规（5）环比 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| sz_scale_capability_breakdown \| 深圳服务能力多维分析 | 需规（5）能力分析 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| sz_dist_growth_rate \| 各区机构数量环比增长率 | 需规（6）环比 | — | 未覆盖 | req_only |
| L04 \| （无 endpoint） \| sz_dist_type_share_analysis \| 各区机构类型占比分析 | 需规（6）类型分布 | — | 未覆盖 | req_only |

catalog 另列 `pt_sz_total`、`pt_sz_type_dist`、`pt_sz_region`、`sz_compare`：本册 5 条套餐未单列形态用例，执行期若 kind=stat21 返回则记入 as-built。

---

## 3. 统计（交卷）

| 状态 | 条数 |
|------|------|
| 契约占位 | 11 |
| 部分覆盖 | 2 |
| 未覆盖 | 15 |

| 项 | 值 |
|----|-----|
| API 用例条数 | **5** |
| 编号闭区间 | **API-00529**～**API-00533** |
| endpoint 数 | **1**（5 条/endpoint） |
| `_empty`（indicators 稳定空态） | **未覆盖** 1 行 |
| 50897 试调 | **未试调**（见用例 §0） |
| FUNC 条数 | **0** |
| code-registry | **未回写**（父控 no registry） |

---

## 4. 无对应 A 线功能点的用例

无（本册 5 条均可挂接 L04 catalog 行或契约哨兵）。
