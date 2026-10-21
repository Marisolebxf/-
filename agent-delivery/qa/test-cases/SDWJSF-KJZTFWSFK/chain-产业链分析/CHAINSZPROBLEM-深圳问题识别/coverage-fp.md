# 深圳问题识别 · 功能点覆盖（chain.sz-problem / L24）

> catalog `chain.sz-problem` · path `#/chain/sz-problem`  
> A 线真源：`fp-split-by-api-run/work/L24.md`  
> B 线用例：`FUNC-深圳问题识别-用例.md`（第三轮 **FUNC-00487**～**00492**）  
> 历史 R2 API 册：`API-深圳问题识别-用例.md`（**API-01284**～**01287**，第三轮不复用编号）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.sz-problem.main | GET | /innov/v1/industry/{chainId}/shenzhen | FUNC-00487、00488 | unavailable |
| chain.sz-problem.m_chain_deep_127_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_127_1/compute | FUNC-00489、00490 | available |
| （页面清单） | — | — | FUNC-00491、00492 | — |

---

## 功能点 → 用例矩阵（挂 L24.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L24 \| chain.sz-problem.main \| chainId \| 算法输入-chainId产业标识 | FUNC-00487、00488 | 已覆盖 | 合法 chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L24 \| chain.sz-problem.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | FUNC-00487 | 已覆盖 | 主流程断言 panorama.enterprise_count（number）；规则来源 catalog panorama.enterprise_count |
| L24 \| chain.sz-problem.main \| panorama.nodes \| 算法输出-panorama.nodes深圳环节节点 | FUNC-00487 | 已覆盖 | 同条主流程断言 panorama.nodes 及元素 node_name、position、enterprise_count；规则来源 catalog panorama.nodes |
| L24 \| chain.sz-problem.main \| _empty \| 深圳问题识别无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无问题识别数据」构造条件；规则来源 契约空结果 |
| L24 \| chain.sz-problem.main \| _fail \| 深圳问题识别查询失败 | FUNC-00488 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 FUNC-00487 的预期同时断言 sampleResponse 中未单独挂 L24 行的 `panorama.node_count`、`panorama.edges`、`panorama.district_dist`、`advantage`（含 advantages）、`problem`（含 problems）及 `opportunity`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L24.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B 线记 **无对应功能点**，不单独开 FUNC 用例：

`etl_clean_standardize`（深全国多源数据清洗一致化，规则来源 需规（1）采集清洗）、`negative_indicator_threshold`（负面评价指标与权重阈值，规则来源 需规指标体系）、`negative_evaluation_model`（负面评价模型训练与优化，规则来源 需规分析阶段模型）、`sz_national_problem_compare`（深全国同类指标对比，规则来源 需规深全国对比）、`problem_risk_list`（问题与风险清单，规则来源 需规（2）问题清单）、`priority_ranking_report`（优先级排序报告，规则来源 需规（2）优先级）、`targeted_solution_suggest`（针对性解决方案建议，规则来源 需规（2）解决方案）、`viz_analysis_chart`（可视化分析图表数据，规则来源 需规（2）可视化）、`dynamic_problem_refresh`（动态监测与结果更新，规则来源 需规动态监测）、`industry_domain_report_export`（产业标签与报告导出，规则来源 需规（3）调用导出）。

`problem_risk_list` 按 L24 仍记无对应功能点。catalog `sampleResponse` 另有 `problem.problems`，已写入 FUNC-00487 预期，不改 A 线、不另开行。

---

## B 线独有（catalog 有、L24 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L24 \| chain.sz-problem.m_chain_deep_127_1 \| — \| 深圳问题识别模型 | FUNC-00489、00490 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L24 未给该 endpoint 挂 field 行 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00491、00492 | 无对应功能点 | 2 接口下拉与 method/path 刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6 |
| 主流程 | 2（FUNC-00487 深圳问题识别、FUNC-00489 深圳问题识别模型） |
| 反向 | 2（FUNC-00488、00490，均为缺 chainId） |
| 清单 | 2（FUNC-00491、00492） |
| 编号 | FUNC-00487～00492 |
| L24 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L24 req_only | 10（无对应功能点） |
