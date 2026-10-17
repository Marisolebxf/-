# 区域产业创新成果综合评价 · 功能点覆盖（comp.industry-outcome / L52）

> catalog `comp.industry-outcome` · 50897 · path `#/industry-comp/industry-outcome`  
> 用例 `API-区域产业创新成果综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.industry-outcome`）  
> 功能点键：`L52 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/region-industry-outcome` 为本页独占；与同模块 `region-tech-outcome` 等其它 outcome path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.industry-outcome.main | GET | /comp/v1/comp/region-industry-outcome | API-00659～00663 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L52 \| comp.industry-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-00659、00661 | 已覆盖 | 主路径占位 + 非法 region |
| L52 \| comp.industry-outcome.main \| year \| 算法输入-year年份 | catalog year | API-00659、00662 | 已覆盖 | 主路径占位 + 非法 year |
| L52 \| comp.industry-outcome.main \| index \| 算法输出-index产业创新成果指数 | catalog index | API-00663 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L52 \| comp.industry-outcome.main \| _empty \| 产业成果评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L52 \| comp.industry-outcome.main \| _fail \| 产业成果评价查询失败 | 契约错误态 | API-00660、00661、00662 | 已覆盖 | 鉴权、非法 region、非法 year |
| L52 \| comp.industry-outcome.main \| etl_clean_standardize \| 多源产业创新数据清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| three_dim_indicators_threshold \| 三维度创新指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| standardize_weight_synthesis \| 四导向指标标准化与加权合成 | 需规标准化权重 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| dimension_sub_eval_results \| 分维度创新评价结果 | 需规（2）分维评价 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| trend_compare_strength_weakness \| 趋势对比与优短板识别 | 需规趋势对比 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| comprehensive_eval_report \| 综合评价与自动化报告 | 需规（2）综合报告 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| index_trend_viz_semantics \| 指标分析与趋势可视化语义 | 需规（3）趋势可视化 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| analysis_dimension_time_datasource_scope \| 分析维度时间数据源查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| continuous_custom_realtime_refresh \| 持续监测定制与结果刷新 | 需规（3）监测刷新 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| index_dimension_report_outputs \| 指数分维报告三类输出 | 需规（2）三类输出 | — | 无对应功能点 | req_only |
| L52 \| comp.industry-outcome.main \| api_sdk_industry_policy_platform \| API SDK 与产业政策平台对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、year、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00659～00663） |
| 金样 | API-00659 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00659 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
