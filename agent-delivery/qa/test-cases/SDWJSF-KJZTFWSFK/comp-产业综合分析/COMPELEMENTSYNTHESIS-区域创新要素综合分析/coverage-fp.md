# 区域创新要素综合分析 · 功能点覆盖（comp.element-synthesis / L59）

> catalog `comp.element-synthesis` · path `#/industry-comp/element-synthesis`  
> A 线真源：`fp-split-by-api-run/work/L59.md`（只读，未改）  
> B 线用例：`API-区域创新要素综合分析-用例.md`（第二轮 **API-01814**～**01819**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-synthesis`

> **path 独占**：`GET /comp/v1/comp/element-synthesis` 为本页 title「要素综合」独占，与同模块其它 `element-*` path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute` 只挂 title「要素贡献度与影响路径」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.element-synthesis.main | GET | /comp/v1/comp/element-synthesis | API-01814～01816 | unavailable |
| comp.element-synthesis.m_synth_elem_contrib | POST | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | API-01817～01819 | available |

---

## 功能点 → 用例矩阵（挂 L59.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L59 \| comp.element-synthesis.main \| region \| 算法输入-region区域标签 | catalog region | API-01814、01815、01816 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L59 \| comp.element-synthesis.main \| index \| 算法输出-index区域创新要素综合指数 | catalog index | API-01814 | 已覆盖 | 主流程断言 index（number，示例 71.5）；备选 01815 同结构。文档标记未交付 |
| L59 \| comp.element-synthesis.main \| _empty \| 要素综合评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L59 \| comp.element-synthesis.main \| _fail \| 要素综合评价查询失败 | 契约错误态 | API-01816 | 部分覆盖 | 仅非法 region 的 message 或 msg；可选省略按备选正向，不把「不传」写成失败 |
| L59 \| （req_only） \| regional_multisource_standardize \| 区域多源统计与创新数据标准化 | 需规（1）多源预处理 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| topic_library_cross_compare \| 各领域专题库综合对比与指标提取 | 需规专题库对比 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| type_layer_domain_threshold_weight \| 类型层次领域阈值权重指标体系 | 需规阈值权重体系 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| weighted_normalize_synthesis \| 加权评分归一化综合指数 | 需规加权归一化 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| type_domain_subscore_rank \| 类型领域分项评分与排序 | 需规（2）分项排序 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| advantage_weakness_report \| 创新优势与不足分析报告 | 需规（2）优不足报告 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| trend_phase_strength_weakness \| 趋势分析阶段优短板揭示 | 需规趋势优短板 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| trend_strategy_advice \| 发展趋势分析与策略建议 | 需规（2）策略建议 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| regional_industry_input_semantics \| 区域基础与行业领域输入语义 | 需规（2）输入结构 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| region_time_datasource_scope \| 区域标签时间数据源查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| dynamic_param_datasource_refresh \| 参数动态调整与数据源更新 | 需规动态更新 | — | 无对应功能点 | 不单开 API 用例 |
| L59 \| （req_only） \| batch_viz_monitor_policy_push \| 批量对比可视化与监测政策对接 | 需规（3）批量对接 | — | 无对应功能点 | 不单开 API 用例 |

sampleResponse 中另有、A 线未单列的 field 已写入 API-01814 正向预期（备选 01815 同结构）：`type`、`layer`、`domain`、`radar`（类型 / 层次 / 领域）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`。不按这些字段各开一条用例。

---

## B 线独有 endpoint（L59 未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.element-synthesis.m_synth_elem_contrib | API-01817～01819 | 无对应功能点 | L59 只挂 GET `comp.element-synthesis.main`。01817 主流程 sampleRequest（region=440300），断言 metric_id、hint，并要求 responseFields 的 index；01818 省略 region；01819 非法 region |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（region、index） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| 无对应功能点 | 12（req_only）+ 1 个 B 线 endpoint（m_synth_elem_contrib，3 条用例） |
| L59 矩阵行 | 16 |
| API 用例 | 6（01814～01819，连续用满） |
| 主流程 | 2（01814 要素综合；01817 要素贡献度与影响路径） |
| 备选 | 2（01815、01818 不传 region） |
| 反向 | 2（01816、01819 非法 region） |
