# 区域创新要素类型综合评价 · 功能点覆盖（comp.element-type / L56）

> catalog `comp.element-type` · path `#/industry-comp/element-type`  
> A 线真源：`fp-split-by-api-run/work/L56.md`（只读，未改）  
> B 线用例：`API-区域创新要素类型综合评价-用例.md`（第二轮 **API-01805**～**01807**，R2-批18）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-type`

> **path 独占**：`GET /comp/v1/comp/element-type` 为本页「要素类型」独占，与同模块其它 `element-*` / `region-*` path 分开验收。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.element-type.main | GET | /comp/v1/comp/element-type | API-01805～01807 | unavailable |

---

## 功能点 → 用例矩阵（挂 L56.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。`要素类型` 的 sampleResponse 另有 `cov`、`weak`、`rank`、`radar`（人才 / 企业 / 政策 / 服务机构 / 科研机构 / 资金 / 空间）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`，已写入 01805、01806 正向预期；A 线未单列这些 field_key。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L56 \| comp.element-type.main \| region \| 算法输入-region区域标签 | catalog region | API-01805、01806、01807 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L56 \| comp.element-type.main \| index \| 算法输出-index区域创新要素类型指数 | catalog index | API-01805、01806 | 已覆盖 | 主流程与备选断言 index（number，示例 73.5）。文档标记未交付 |
| L56 \| comp.element-type.main \| _empty \| 要素类型评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L56 \| comp.element-type.main \| _fail \| 要素类型评价查询失败 | 契约错误态 | API-01807 | 部分覆盖 | 仅非法 region；可选省略按备选正向，不把「不传」写成失败 |

---

## req_only 行（无 endpoint 挂接）

L56.md 下列 13 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L56 \| （req_only） \| kg_multisource_seven_element_etl \| 产业知识图谱多源七要素清洗 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| seven_element_indicators_threshold \| 七要素指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| seven_element_dimension_scores \| 七要素维度量化评分 | 需规维度量化 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| weighted_normalize_synthesis \| 加权归一化要素类型指数 | 需规加权归一化 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| network_structure_synergy \| 创新网络结构分析与协同 | 需规结构协同 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| strength_weakness_inventory \| 要素配置优势与不足清单 | 需规（2）优不足清单 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| resource_optimization_advice \| 创新资源优化与结构调整建议 | 需规（2）优化建议 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| dimension_weight_analysis \| 分维量化评分与权重分析 | 需规（2）分维权重 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| region_time_element_scope \| 区域时间要素类别查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| structured_eval_trend_viz \| 结构化结果与趋势可视化 | 需规（3）趋势可视化 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| continuous_monitor_refresh \| 持续监测与结果刷新 | 需规（3）监测刷新 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| index_dimension_inventory_advice_outputs \| 指数分维清单建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | 不单开 API 用例 |
| L56 \| （req_only） \| api_sdk_regional_industry_platform \| API SDK 与区域经济监测平台对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 API 用例 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`region`、`index`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 13 |
| L56 矩阵行 | 17 |
| API 用例 | 3（01805～01807；主流程 1、备选 1、反向 1） |
| 金样 | API-01805 |
