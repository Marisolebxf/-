# 产业链关键环节识别 · 功能点覆盖（chain.keynodes / L21）

> catalog `chain.keynodes` · 50897 · path `#/chain/keynodes`  
> 用例 `API-产业链关键环节识别-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/chain.json`（页 `chain.keynodes`）  
> 功能点键：`L21 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐，本轮未读 `work/L21.md`）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.keynodes.main | GET | /innov/v1/industry/{chainId}/key-nodes | API-00350～00359 | catalog `unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L21 \| chain.keynodes.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00350、00352、00353、00354、00358 | 已覆盖 | 合法主路径 + 非法/缺 path + 备选 id |
| L21 \| chain.keynodes.main \| high_end_index \| 算法输出-high_end_index高端化指数体 | catalog high_end_index | API-00358、00359 | 契约占位 | unavailable；成功形态预备，不写 sample 分值 |
| L21 \| chain.keynodes.main \| _empty \| 关键环节识别无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L21 \| chain.keynodes.main \| _fail \| 关键环节识别查询失败 | 契约错误态 | API-00352、00353、00356、00351、00355 | 已覆盖 | 非法 id、缺 path、鉴权、畸形 id |
| L21 \| chain.keynodes.main \| etl_clean_standardize \| 多源指标标准化清洗 | 需规段一采集清洗 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| keynode_indicator_threshold \| 关键环节指标与权重阈值 | 需规指标体系 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| keynode_model_identify \| 识别模型训练与关键环节定位 | 需规计算分析阶段 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| strategic_importance_analysis \| 战略重要性及产业影响分析 | 需规战略重要性 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| link_influence_evaluation \| 环节影响力评估 | 需规（2）影响力 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| dynamic_keynode_refresh \| 动态监测与结果更新 | 需规动态监测 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| strategic_importance_report \| 战略重要性分析报告 | 需规（2）战略报告 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| viz_link_structure \| 可视化环节结构图支撑 | 需规（2）结构图 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| link_type_query_scope \| 产业标签与环节类型查询语义 | 需规（3）调用方式 | — | 无对应功能点 | req_only |
| L21 \| chain.keynodes.main \| analysis_report_export \| 分析报告与数据导出 | 需规（3）导出 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 3（chainId、high_end_index 占位、_fail） |
| 未覆盖 | 1（_empty） |
| 无对应功能点（req_only） | 10 |
| API 用例条数 | 10（00350～00359） |
| 金样 | API-00350 |
