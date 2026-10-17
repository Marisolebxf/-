# 区域创新要素领域综合评价 · 功能点覆盖（comp.element-domain / L58）

> catalog `comp.element-domain` · 50897 · path `#/industry-comp/element-domain`  
> 用例 `API-区域创新要素领域综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.element-domain`）  
> 功能点键：`L58 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/element-domain` 为本页独占；与同模块 `element-type`、`element-layer`、`element-synthesis` 等其它 `element-*` path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.element-domain.main | GET | /comp/v1/comp/element-domain | API-00689～00693 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L58 \| comp.element-domain.main \| region \| 算法输入-region区域标签 | catalog region | API-00689、00691、00692 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L58 \| comp.element-domain.main \| index \| 算法输出-index区域创新要素领域指数 | catalog index | API-00693 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L58 \| comp.element-domain.main \| _empty \| 要素领域评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L58 \| comp.element-domain.main \| _fail \| 要素领域评价查询失败 | 契约错误态 | API-00690、00691、00692 | 已覆盖 | 鉴权、非法 region、空 region |
| L58 \| comp.element-domain.main \| kg_domain_multisource_etl \| 产业知识图谱多源领域要素采集清洗 | 需规（1）多源采集 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| domain_five_dimension_indicators \| 产业技术领域五维指标与阈值权重 | 需规五维指标阈值 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| industry_tech_coverage_structure \| 产业技术领域覆盖结构量化 | 需规覆盖结构量化 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| weighted_domain_index_synthesis \| 加权指数法合成领域指数 | 需规加权指数法 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| dimension_scores_strength_weakness \| 分维度得分与优短板判定 | 需规（2）分维优短板 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| historical_trend_forecast \| 历史对比与趋势预测 | 需规（2）趋势预测 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| strategic_resource_guidance \| 战略建议与资源配置指引 | 需规（2）战略建议 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| graph_tech_element_input_semantics \| 图谱技术领域与创新要素输入语义 | 需规（2）输入结构 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| region_industry_tech_scope \| 区域产业技术领域查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| online_monitor_cross_compare \| 在线监测横向比较与动态研判 | 需规（3）监测比较 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| index_dimension_list_forecast_advice \| 指数分维清单预测建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | req_only |
| L58 \| comp.element-domain.main \| api_sdk_decision_support \| API SDK 与区域决策支持对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 12 |
| API 用例条数 | 5（00689～00693） |
| 金样 | API-00689 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00689 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
