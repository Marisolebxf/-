# 区域创新要素层次综合评价 · 功能点覆盖（comp.element-layer / L57）

> catalog `comp.element-layer` · 50897 · path `#/industry-comp/element-layer`  
> 用例 `API-区域创新要素层次综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.element-layer`）  
> 功能点键：`L57 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I、§S1  

> **path 独占**：`GET /comp/v1/comp/element-layer` 为本页独占；与同模块 `element-type`、`element-domain`、`element-synthesis` 等其它 path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.element-layer.main | GET | /comp/v1/comp/element-layer | API-00684～00688 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L57 \| comp.element-layer.main \| region \| 算法输入-region区域标签 | catalog region | API-00684、00686、00687 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L57 \| comp.element-layer.main \| index \| 算法输出-index区域创新要素层次指数 | catalog index | API-00688 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L57 \| comp.element-layer.main \| _empty \| 要素层次评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L57 \| comp.element-layer.main \| _fail \| 要素层次评价查询失败 | 契约错误态 | API-00685、00686、00687 | 已覆盖 | 鉴权、非法 region、空 region |
| L57 \| comp.element-layer.main \| kg_multisource_etl \| 知识图谱多源要素数据清洗标准化 | 需规（1）图谱融合 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| seven_structure_indicators \| 七大结构指标体系与阈值 | 需规七大结构阈值 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| standardize_element_model \| 数据标准化与要素关联建模 | 需规标准化关联 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| weighted_layer_synthesis \| 维度权重加权合成层次指数 | 需规加权求和 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| dimension_compliance_eval \| 各结构维度评价与达标情况 | 需规（2）维度达标 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| strength_weakness_lists \| 优势要素与短板要素清单 | 需规（2）优短板清单 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| rank_compare_report \| 综合排名与对比分析报告 | 需规排名对比报告 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| weakness_optimization_path \| 短板优化建议与发展路径 | 需规（2）优化路径 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| maturity_balance_reflect \| 成熟度均衡度与优短板反映 | 需规成熟度均衡 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| region_time_dimension_scope \| 区域标签时间维度查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| auto_monitor_trend \| 自动化监测比较与趋势研判 | 需规（3）监测趋势 | — | 无对应功能点 | req_only |
| L57 \| comp.element-layer.main \| api_sdk_decision_platform \| API SDK 与决策平台对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00684～00688） |
| 金样 | API-00684 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00684 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
