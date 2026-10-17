# 区域创新协同分析 · 功能点覆盖（comp.synergy / L60）

> catalog `comp.synergy` · 50897 · path `#/industry-comp/synergy`  
> 用例 `API-区域创新协同分析-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.synergy`）  
> 功能点键：`L60 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/innov-synergy` 为本页独占；与同模块 `region-vitality`、`element-synthesis` 等其它 path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.synergy.main | GET | /comp/v1/comp/innov-synergy | API-00699～00703 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L60 \| comp.synergy.main \| region \| 算法输入-region区域标签 | catalog region | API-00699、00701、00702 | 已覆盖 | 主路径占位 + 非法 region + 空 region |
| L60 \| comp.synergy.main \| index \| 算法输出-index区域创新协同指数 | catalog index | API-00703 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L60 \| comp.synergy.main \| nodes \| 算法输出-nodes创新网络节点 | catalog nodes | API-00703 | 部分覆盖 | 成功信封下 array 形态；元素 schema 与 live 非空语义待升档 |
| L60 \| comp.synergy.main \| edges \| 算法输出-edges合作关系边 | catalog edges | API-00703 | 部分覆盖 | 成功信封下 array 形态；元素 schema 与 live 非空语义待升档 |
| L60 \| comp.synergy.main \| _empty \| 创新协同无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L60 \| comp.synergy.main \| _fail \| 创新协同查询失败 | 契约错误态 | API-00700、00701、00702 | 已覆盖 | 鉴权、非法 region、空 region |
| L60 \| comp.synergy.main \| etl_clean_standardize \| 多源合作关系采集与预处理 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| innov_synergy_network_model \| 区域创新协同网络建模 | 需规（1）网络建模 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| completeness_centrality_density \| 完整度中心度密度三类指标 | 需规三类核心指标 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| weighted_calibrate_synthesis \| 综合加权与历史数据校准 | 需规（1）指数合成 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| structured_analysis_report \| 结构化分析报告输出 | 需规（2）分析报告 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| synergy_strength_weakness_diag \| 协同优势与不足诊断 | 需规（2）优劣势诊断 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| trend_change_analysis \| 趋势变化分析 | 需规（2）趋势分析 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| cross_region_longitudinal_semantics \| 横向对比与纵向趋势语义 | 需规（1）对比趋势 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| network_viz_semantics \| 创新网络可视化展示语义 | 需规调用展示 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| region_time_scope \| 区域标签与时间范围查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| auto_monitor_strategy_integration \| 自动化监测与策略生成对接 | 需规（3）系统对接监测 | — | 无对应功能点 | req_only |
| L60 \| comp.synergy.main \| api_sdk_policy_platform \| API SDK 与政策规划平台集成 | 需规（3）API SDK | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 4（region、_fail；index/nodes/edges 形态部分） |
| 未覆盖（契约 field / _empty） | 4（index/nodes/edges live 语义、_empty） |
| 无对应功能点（req_only） | 12 |
| API 用例条数 | 5（00699～00703） |
| 金样 | API-00699 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00699 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
