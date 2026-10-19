# 区域产业创新成果综合评价 · 功能点覆盖（comp.industry-outcome / L52）

> catalog `comp.industry-outcome` · path `#/industry-comp/industry-outcome`  
> A 线真源：`fp-split-by-api-run/work/L52.md`（只读，未改）  
> B 线用例：`API-区域产业创新成果综合评价-用例.md`（第二轮 **API-01777**～**01781**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.industry-outcome`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.industry-outcome.main | GET | /comp/v1/comp/region-industry-outcome | API-01777、01778、01779、01780、01781 | unavailable |

---

## 功能点 → 用例矩阵（挂 L52.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L52 \| comp.industry-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-01777、01778、01780 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L52 \| comp.industry-outcome.main \| year \| 算法输入-year年份 | catalog year | API-01777、01779、01781 | 已覆盖 | 主路径 year=2025 + 省略可选 year + 非法 year=0 |
| L52 \| comp.industry-outcome.main \| index \| 算法输出-index产业创新成果指数 | catalog index | API-01777、01778、01779 | 已覆盖 | 主流程与两条备选断言 index（number，示例 66.3）及 sampleResponse 同层字段 |
| L52 \| comp.industry-outcome.main \| _empty \| 产业成果评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L52 \| comp.industry-outcome.main \| _fail \| 产业成果评价查询失败 | 契约错误态 | API-01780、01781 | 已覆盖 | 非法 region、非法 year；预期 message 或 msg 指出该参数非法 |

sampleResponse 另有 `rank`、`yoy`、`adv`、`radar`（产品服务、企业创新、服务机构）、`bar_items`、`pie_items`、`rows`（name、score、rank、tag、note），已写入 01777～01779 正向预期；A 线未单列这些 field_key。responseFields 仅声明 `index`。

---

## req_only 行（无 endpoint 挂接）

L52.md 中下列 11 行 `endpoint_id` 为空、`catalog_status=req_only`，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L52 \| \| etl_clean_standardize \| 多源产业创新数据清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L52 \| \| three_dim_indicators_threshold \| 三维度创新指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L52 \| \| standardize_weight_synthesis \| 四导向指标标准化与加权合成 | 需规标准化权重 | — | 无对应功能点 | req_only |
| L52 \| \| dimension_sub_eval_results \| 分维度创新评价结果 | 需规（2）分维评价 | — | 无对应功能点 | req_only |
| L52 \| \| trend_compare_strength_weakness \| 趋势对比与优短板识别 | 需规趋势对比 | — | 无对应功能点 | req_only |
| L52 \| \| comprehensive_eval_report \| 综合评价与自动化报告 | 需规（2）综合报告 | — | 无对应功能点 | req_only |
| L52 \| \| index_trend_viz_semantics \| 指标分析与趋势可视化语义 | 需规（3）趋势可视化 | — | 无对应功能点 | req_only |
| L52 \| \| analysis_dimension_time_datasource_scope \| 分析维度时间数据源查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L52 \| \| continuous_custom_realtime_refresh \| 持续监测定制与结果刷新 | 需规（3）监测刷新 | — | 无对应功能点 | req_only |
| L52 \| \| index_dimension_report_outputs \| 指数分维报告三类输出 | 需规（2）三类输出 | — | 无对应功能点 | req_only |
| L52 \| \| api_sdk_industry_policy_platform \| API SDK 与产业政策平台对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（`region`、`year`、`index`、`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| API 用例 | 5（01777～01781；主流程 1、备选 2、反向 2） |
| 金样 | API-01777 |
