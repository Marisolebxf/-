# 区域创新要素综合分析 · 功能点覆盖（comp.element-synthesis / L59）

> catalog `comp.element-synthesis` · 50897 · path `#/industry-comp/element-synthesis`  
> 用例 `API-区域创新要素综合分析-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.element-synthesis`）  
> 功能点键：`L59 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/element-synthesis` 为本页独占；与同模块 `element-type`、`element-layer`、`element-domain` 等其它 path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.element-synthesis.main | GET | /comp/v1/comp/element-synthesis | API-00694～00698 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L59 \| comp.element-synthesis.main \| region \| 算法输入-region区域标签 | catalog region | API-00694、00696、00697 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L59 \| comp.element-synthesis.main \| index \| 算法输出-index区域创新要素综合指数 | catalog index | API-00698 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L59 \| comp.element-synthesis.main \| _empty \| 要素综合评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L59 \| comp.element-synthesis.main \| _fail \| 要素综合评价查询失败 | 契约错误态 | API-00695、00696、00697 | 已覆盖 | 鉴权、非法 region、空 region |
| L59 \| comp.element-synthesis.main \| regional_multisource_standardize \| 区域多源统计与创新数据标准化 | 需规（1）多源预处理 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| topic_library_cross_compare \| 各领域专题库综合对比与指标提取 | 需规专题库对比 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| type_layer_domain_threshold_weight \| 类型层次领域阈值权重指标体系 | 需规阈值权重体系 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| weighted_normalize_synthesis \| 加权评分归一化综合指数 | 需规加权归一化 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| type_domain_subscore_rank \| 类型领域分项评分与排序 | 需规（2）分项排序 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| advantage_weakness_report \| 创新优势与不足分析报告 | 需规（2）优不足报告 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| trend_phase_strength_weakness \| 趋势分析阶段优短板揭示 | 需规趋势优短板 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| trend_strategy_advice \| 发展趋势分析与策略建议 | 需规（2）策略建议 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| regional_industry_input_semantics \| 区域基础与行业领域输入语义 | 需规（2）输入结构 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| region_time_datasource_scope \| 区域标签时间数据源查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| dynamic_param_datasource_refresh \| 参数动态调整与数据源更新 | 需规动态更新 | — | 无对应功能点 | req_only |
| L59 \| comp.element-synthesis.main \| batch_viz_monitor_policy_push \| 批量对比可视化与监测政策对接 | 需规（3）批量对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（region、_fail；index 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00694～00698） |
| 金样 | API-00694 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00694 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
