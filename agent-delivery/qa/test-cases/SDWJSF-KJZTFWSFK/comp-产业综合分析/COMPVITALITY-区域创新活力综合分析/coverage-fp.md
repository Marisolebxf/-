# 区域创新活力综合分析 · 功能点覆盖（comp.vitality / L55）

> catalog `comp.vitality` · 50897 · path `#/industry-comp/vitality`  
> 用例 `API-区域创新活力综合分析-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.vitality`）  
> 功能点键：`L55 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/region-vitality` 为本页独占；与同模块 `region-tech-outcome`、`region-industry-outcome` 等其它 path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.vitality.main | GET | /comp/v1/comp/region-vitality | API-00674～00678 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L55 \| comp.vitality.main \| region \| 算法输入-region区域标签 | catalog region | API-00674、00676、00677 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L55 \| comp.vitality.main \| index \| 算法输出-index区域创新活力指数 | catalog index | API-00678 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L55 \| comp.vitality.main \| _empty \| 创新活力无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L55 \| comp.vitality.main \| _fail \| 创新活力查询失败 | 契约错误态 | API-00675、00676、00677 | 已覆盖 | 鉴权、非法 region、空 region |
| L55 \| comp.vitality.main \| etl_clean_standardize \| 四主题库综合清洗标准化 | 需规（1）数据标准化 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| four_dim_indicators_threshold \| 四维活力指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| standardize_weight_synthesis \| 指标标准化与加权活力指数合成 | 需规（4）指数计算 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| dimension_sub_scoring_weights \| 单维度评分与权重分布 | 需规（2）单维评分权重 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| trend_strength_weakness \| 趋势分析与优短板识别 | 需规（4）趋势优短板 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| structured_eval_report \| 结构化评估与战略建议报告 | 需规（5）结果输出 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| trend_forecast_strategy \| 趋势预测与策略建议 | 需规（2）趋势策略 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| index_trend_viz_semantics \| 指标分析与趋势可视化语义 | 需规（3）趋势可视化 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| region_time_dimension_scope \| 区域时间分析维度查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| auto_compute_realtime_refresh \| 自动运算与实时监控刷新 | 需规（3）监测刷新 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| index_dimension_report_outputs \| 指数分维报告策略四类输出 | 需规（2）四类输出 | — | 无对应功能点 | req_only |
| L55 \| comp.vitality.main \| api_sdk_strategy_platform \| API SDK 与发展战略系统对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00674～00678） |
| 金样 | API-00674 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00674 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
