# 产业链关键环节识别 · 功能点覆盖（chain.keynodes / L21）

> catalog `chain.keynodes` · path `#/chain/keynodes`  
> A 线真源：`fp-split-by-api-run/work/L21.md`  
> B 线用例：`API-产业链关键环节识别-用例.md`（第二轮 **API-01266**～**01269**）  
> C 线用例：`FUNC-产业链关键环节识别-用例.md`（第三轮 **FUNC-00461**～**00466**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | API 用例 | FUNC 用例 | catalog status |
|-------------|--------|------|----------|-----------|----------------|
| chain.keynodes.main | GET | /innov/v1/industry/{chainId}/key-nodes | API-01266、01267 | FUNC-00461、00462 | unavailable |
| chain.keynodes.m_chain_deep_124_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute | API-01268、01269 | FUNC-00463、00464 | available |

---

## 功能点 → 用例矩阵（挂 L21.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L21 \| chain.keynodes.main \| chainId \| 算法输入-chainId产业标识 | API-01266、01267；FUNC-00461、00462 | 已覆盖 | 合法 chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L21 \| chain.keynodes.main \| high_end_index \| 算法输出-high_end_index高端化指数体 | API-01266；FUNC-00461 | 已覆盖 | 主流程断言数组元素 high_end_index（number，responseFields）；规则来源 catalog high_end_index |
| L21 \| chain.keynodes.main \| _empty \| 关键环节识别无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无关键环节」构造条件；规则来源 契约空结果 |
| L21 \| chain.keynodes.main \| _fail \| 关键环节识别查询失败 | API-01267；FUNC-00462 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L21.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B/C 线记 **无对应功能点**，不单独开用例：

`etl_clean_standardize`（多源指标标准化清洗）、`keynode_indicator_threshold`（关键环节指标与权重阈值）、`keynode_model_identify`（识别模型训练与关键环节定位）、`strategic_importance_analysis`（战略重要性及产业影响分析）、`link_influence_evaluation`（环节影响力评估）、`dynamic_keynode_refresh`（动态监测与结果更新）、`strategic_importance_report`（战略重要性分析报告）、`viz_link_structure`（可视化环节结构图支撑）、`link_type_query_scope`（产业标签与环节类型查询语义）、`analysis_report_export`（分析报告与数据导出）。

---

## B/C 线独有（catalog 有、L21 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L21 \| chain.keynodes.m_chain_deep_124_1 \| — \| 产业链关键环节识别模型 | API-01268、01269；FUNC-00463、00464 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L21 未给该 endpoint 挂 field 行 |
| （页面清单）接口信息 / 算法测试 | FUNC-00465、00466 | 无对应功能点 | 联调台 tab 与 catalog 下拉一致性 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4（API-01266～01269） |
| FUNC 用例数 | 6（FUNC-00461～00466） |
| FUNC 主流程 | 2（00461 关键环节、00463 产业链关键环节识别模型） |
| FUNC 反向 | 2（00462、00464，均为缺 chainId） |
| FUNC 清单 | 2（00465 接口信息、00466 算法测试） |
| L21 挂接行 | 4（已覆盖 2、部分覆盖 1、未覆盖 1） |
| L21 req_only | 10（无对应功能点） |
