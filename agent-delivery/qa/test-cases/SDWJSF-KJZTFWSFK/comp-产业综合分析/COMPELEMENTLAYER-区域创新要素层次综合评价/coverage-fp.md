# 区域创新要素层次综合评价 · 功能点覆盖（comp.element-layer / L57）

> catalog `comp.element-layer` · path `#/industry-comp/element-layer`  
> A 线真源：`fp-split-by-api-run/work/L57.md`（只读，未改）  
> B 线用例：`API-区域创新要素层次综合评价-用例.md`（第二轮 **API-01808**～**01810**，R2-批18）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-layer`

> **path 独占**：`GET /comp/v1/comp/element-layer` 为本页「要素层次」独占，与同模块 `element-type`、`element-domain`、`element-synthesis` 分开验收。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.element-layer.main | GET | /comp/v1/comp/element-layer | API-01808～01810 | unavailable |

---

## 功能点 → 用例矩阵（挂 L57.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。`要素层次` 的 sampleResponse 另有 `balance`、`hit`、`rank`、`radar`（基础层 / 支撑层 / 应用层）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`，已写入 01808、01809 正向预期；A 线未单列这些 field_key。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L57 \| comp.element-layer.main \| region \| 算法输入-region区域标签 | catalog region | API-01808、01809、01810 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__。catalog `required=false`，不传按备选正向 |
| L57 \| comp.element-layer.main \| index \| 算法输出-index区域创新要素层次指数 | catalog index | API-01808、01809 | 已覆盖 | 主流程与备选断言 index（number，示例 69.8）。文档标记未交付 |
| L57 \| comp.element-layer.main \| _empty \| 要素层次评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L57 \| comp.element-layer.main \| _fail \| 要素层次评价查询失败 | 契约错误态 | API-01810 | 部分覆盖 | 仅非法 region；可选省略按备选正向，不把「不传」写成失败 |

---

## req_only 行（无 endpoint 挂接）

L57.md 下列 12 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L57 \| （req_only） \| kg_multisource_etl \| 知识图谱多源要素数据清洗标准化 | 需规（1）图谱融合 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| seven_structure_indicators \| 七大结构指标体系与阈值 | 需规七大结构阈值 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| standardize_element_model \| 数据标准化与要素关联建模 | 需规标准化关联 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| weighted_layer_synthesis \| 维度权重加权合成层次指数 | 需规加权求和 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| dimension_compliance_eval \| 各结构维度评价与达标情况 | 需规（2）维度达标 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| strength_weakness_lists \| 优势要素与短板要素清单 | 需规（2）优短板清单 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| rank_compare_report \| 综合排名与对比分析报告 | 需规排名对比报告 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| weakness_optimization_path \| 短板优化建议与发展路径 | 需规（2）优化路径 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| maturity_balance_reflect \| 成熟度均衡度与优短板反映 | 需规成熟度均衡 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| region_time_dimension_scope \| 区域标签时间维度查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| auto_monitor_trend \| 自动化监测比较与趋势研判 | 需规（3）监测趋势 | — | 无对应功能点 | 不单开 API 用例 |
| L57 \| （req_only） \| api_sdk_decision_platform \| API SDK 与决策平台对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 API 用例 |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`region`、`index`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 12 |
| L57 矩阵行 | 16 |
| API 用例 | 3（01808～01810；主流程 1、备选 1、反向 1） |
| 金样 | API-01808 |
