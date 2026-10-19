# 区域创新活力综合分析 · 功能点覆盖（comp.vitality / L55）

> catalog `comp.vitality` · path `#/industry-comp/vitality`  
> A 线真源：`fp-split-by-api-run/work/L55.md`（只读，未改）  
> B 线用例：`API-区域创新活力综合分析-用例.md`（第二轮 **API-01802**～**01804**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.vitality`

> **path 独占**：`GET /comp/v1/comp/region-vitality` 为本页「创新活力」独占，与同模块其它 `region-*` path 分开验收。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.vitality.main | GET | /comp/v1/comp/region-vitality | API-01802、01803、01804 | unavailable |

---

## 功能点 → 用例矩阵（挂 L55.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L55 \| comp.vitality.main \| region \| 算法输入-region区域标签 | catalog region | API-01802、01803、01804 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L55 \| comp.vitality.main \| index \| 算法输出-index区域创新活力指数 | catalog index | API-01802、01803 | 已覆盖 | 主流程与备选断言 index（number，示例 76.4）及 sampleResponse 同层字段。文档标记未交付 |
| L55 \| comp.vitality.main \| _empty \| 创新活力无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L55 \| comp.vitality.main \| _fail \| 创新活力查询失败 | 契约错误态 | API-01804 | 部分覆盖 | 仅非法 region 的 message 或 msg；可选省略按备选正向，不把「不传」写成失败。上游或网关失败未单开 |

sampleResponse 另有 `rank`、`yoy`、`cov`、`radar`（科技活力、产业活力、人才活力、政策活力）、`bar_items`、`pie_items`、`rows`（name、score、rank、tag、note），已写入 01802、01803 正向预期；A 线未单列这些 field_key。responseFields 仅声明 `index`。

---

## req_only 行（无 endpoint 挂接）

L55.md 中下列 12 行 `endpoint_id` 为空、`catalog_status=req_only`，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L55 \| \| etl_clean_standardize \| 四主题库综合清洗标准化 | 需规（1）数据标准化 | — | 无对应功能点 | req_only |
| L55 \| \| four_dim_indicators_threshold \| 四维活力指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L55 \| \| standardize_weight_synthesis \| 指标标准化与加权活力指数合成 | 需规（4）指数计算 | — | 无对应功能点 | req_only |
| L55 \| \| dimension_sub_scoring_weights \| 单维度评分与权重分布 | 需规（2）单维评分权重 | — | 无对应功能点 | req_only |
| L55 \| \| trend_strength_weakness \| 趋势分析与优短板识别 | 需规（4）趋势优短板 | — | 无对应功能点 | req_only |
| L55 \| \| structured_eval_report \| 结构化评估与战略建议报告 | 需规（5）结果输出 | — | 无对应功能点 | req_only |
| L55 \| \| trend_forecast_strategy \| 趋势预测与策略建议 | 需规（2）趋势策略 | — | 无对应功能点 | req_only |
| L55 \| \| index_trend_viz_semantics \| 指标分析与趋势可视化语义 | 需规（3）趋势可视化 | — | 无对应功能点 | req_only |
| L55 \| \| region_time_dimension_scope \| 区域时间分析维度查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L55 \| \| auto_compute_realtime_refresh \| 自动运算与实时监控刷新 | 需规（3）监测刷新 | — | 无对应功能点 | req_only |
| L55 \| \| index_dimension_report_outputs \| 指数分维报告策略四类输出 | 需规（2）四类输出 | — | 无对应功能点 | req_only |
| L55 \| \| api_sdk_strategy_platform \| API SDK 与发展战略系统对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`region`、`index`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 12 |
| L55 矩阵行 | 16 |
| API 用例 | 3（01802～01804；主流程 1、备选 1、反向 1） |
| 金样 | API-01802 |
