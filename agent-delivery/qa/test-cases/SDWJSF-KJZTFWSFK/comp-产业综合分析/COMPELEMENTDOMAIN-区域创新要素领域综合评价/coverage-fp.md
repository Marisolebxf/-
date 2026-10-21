# 区域创新要素领域综合评价 · 功能点覆盖（comp.element-domain / L58）

> catalog `comp.element-domain` · path `#/industry-comp/element-domain`  
> A 线真源：`fp-split-by-api-run/work/L58.md`（只读，未改）  
> B 线用例：`FUNC-区域创新要素领域综合评价-用例.md`（第三轮 **FUNC-01065**～**01069**；旧 API-01811～01813 作废）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-domain`

> **path 独占**：`GET /comp/v1/comp/element-domain` 为本页 title「要素领域」独占，与同模块其它 `element-*` path 分开验收。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.element-domain.main | GET | /comp/v1/comp/element-domain | FUNC-01065～01067 | unavailable |
| （页面清单） | — | — | FUNC-01068、01069 | — |

---

## 功能点 → 用例矩阵（挂 L58.md）

同一 field 多条场景挂在同一组 FUNC 号上，不按 field_key 各写一条用例。`要素领域` 的 sampleResponse 另有 `top`、`gap`、`cov`、`radar`（集成电路 / 新能源 / 生物医药 / 人工智能 / 超高清）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`，已写入 01065、01066 正向预期；A 线未单列这些 field_key。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L58 \| comp.element-domain.main \| region \| 算法输入-region区域标签 | catalog region | FUNC-01065、01066、01067 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L58 \| comp.element-domain.main \| index \| 算法输出-index区域创新要素领域指数 | catalog index | FUNC-01065、01066 | 已覆盖 | 主流程与备选断言 index（number，示例 71.2）。文档标记未交付 |
| L58 \| comp.element-domain.main \| _empty \| 要素领域评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L58 \| comp.element-domain.main \| _fail \| 要素领域评价查询失败 | 契约错误态 | FUNC-01067 | 部分覆盖 | 仅非法 region；可选省略按备选正向，不把「不传」写成失败 |
| （页面清单） \| comp.element-domain \| 接口信息 / 算法测试 | 联调台 tab | FUNC-01068、01069 | 已覆盖 | 单接口页清单 2 条，不点击调用 |

---

## req_only 行（无 endpoint 挂接）

L58.md 下列 12 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L58 \| （req_only） \| kg_domain_multisource_etl \| 产业知识图谱多源领域要素采集清洗 | 需规（1）多源采集 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| domain_five_dimension_indicators \| 产业技术领域五维指标与阈值权重 | 需规五维指标阈值 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| industry_tech_coverage_structure \| 产业技术领域覆盖结构量化 | 需规覆盖结构量化 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| weighted_domain_index_synthesis \| 加权指数法合成领域指数 | 需规加权指数法 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| dimension_scores_strength_weakness \| 分维度得分与优短板判定 | 需规（2）分维优短板 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| historical_trend_forecast \| 历史对比与趋势预测 | 需规（2）趋势预测 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| strategic_resource_guidance \| 战略建议与资源配置指引 | 需规（2）战略建议 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| graph_tech_element_input_semantics \| 图谱技术领域与创新要素输入语义 | 需规（2）输入结构 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| region_industry_tech_scope \| 区域产业技术领域查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| online_monitor_cross_compare \| 在线监测横向比较与动态研判 | 需规（3）监测比较 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| index_dimension_list_forecast_advice \| 指数分维清单预测建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | 不单开用例 |
| L58 \| （req_only） \| api_sdk_decision_support \| API SDK 与区域决策支持对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开用例 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`region`、`index`、页面清单） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 12 |
| L58 矩阵行 | 16 |
| FUNC 用例 | 5（01065～01069；主流程 1、备选 1、反向 1、清单 2） |
| 金样 | FUNC-01065 |
