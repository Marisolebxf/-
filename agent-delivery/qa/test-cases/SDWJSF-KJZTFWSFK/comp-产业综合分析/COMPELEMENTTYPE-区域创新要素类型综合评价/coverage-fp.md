# 区域创新要素类型综合评价 · 功能点覆盖（comp.element-type / L56）

> catalog `comp.element-type` · 50897 · path `#/industry-comp/element-type`  
> 用例 `API-区域创新要素类型综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.element-type`）  
> 功能点键：`L56 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/element-type` 为本页独占；与同模块 `region-tech-outcome`、`region-vitality` 及其它 `element-*` path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.element-type.main | GET | /comp/v1/comp/element-type | API-00679～00683 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L56 \| comp.element-type.main \| region \| 算法输入-region区域标签 | catalog region | API-00679、00681、00682 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L56 \| comp.element-type.main \| index \| 算法输出-index区域创新要素类型指数 | catalog index | API-00683 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L56 \| comp.element-type.main \| _empty \| 要素类型评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L56 \| comp.element-type.main \| _fail \| 要素类型评价查询失败 | 契约错误态 | API-00680、00681、00682 | 已覆盖 | 鉴权、非法 region、空 region |
| L56 \| comp.element-type.main \| kg_multisource_seven_element_etl \| 产业知识图谱多源七要素清洗 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| seven_element_indicators_threshold \| 七要素指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| seven_element_dimension_scores \| 七要素维度量化评分 | 需规维度量化 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| weighted_normalize_synthesis \| 加权归一化要素类型指数 | 需规加权归一化 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| network_structure_synergy \| 创新网络结构分析与协同 | 需规结构协同 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| strength_weakness_inventory \| 要素配置优势与不足清单 | 需规（2）优不足清单 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| resource_optimization_advice \| 创新资源优化与结构调整建议 | 需规（2）优化建议 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| dimension_weight_analysis \| 分维量化评分与权重分析 | 需规（2）分维权重 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| region_time_element_scope \| 区域时间要素类别查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| structured_eval_trend_viz \| 结构化结果与趋势可视化 | 需规（3）趋势可视化 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| continuous_monitor_refresh \| 持续监测与结果刷新 | 需规（3）监测刷新 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| index_dimension_inventory_advice_outputs \| 指数分维清单建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | req_only |
| L56 \| comp.element-type.main \| api_sdk_regional_industry_platform \| API SDK 与区域经济监测平台对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 12 |
| API 用例条数 | 5（00679～00683） |
| 金样 | API-00679 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00679 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
