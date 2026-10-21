# 深圳机遇识别 · 功能点覆盖（chain.sz-opportunity / L25）

> catalog `chain.sz-opportunity` · path `#/chain/sz-opportunity`  
> A 线真源：`fp-split-by-api-run/work/L25.md`  
> B 线用例：`FUNC-深圳机遇识别-用例.md`（第三轮 **FUNC-00493**～**00502**）  
> 历史 R2 API 册：`../CHAINSZOPPORTUNITY-深圳机遇分析/API-深圳机遇分析-用例.md`（**API-01288**～**01295**，第三轮不复用编号）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.sz-opportunity.main | GET | /innov/v1/industry/{chainId}/shenzhen | FUNC-00493、00494 | unavailable |
| chain.sz-opportunity.m_chain_deep_128_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | FUNC-00495、00496 | available |
| chain.sz-opportunity.m_chain_sz_opportunity_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | FUNC-00497、00498 | available |
| chain.sz-opportunity.m_chain_sz_opportunity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | FUNC-00499、00500 | available |
| （页面清单） | — | — | FUNC-00501、00502 | — |

---

## 功能点 → 用例矩阵（挂 L25.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L25 \| chain.sz-opportunity.main \| chainId \| 算法输入-chainId产业标识 | FUNC-00493、00494 | 已覆盖 | 合法 chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L25 \| chain.sz-opportunity.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | FUNC-00493 | 已覆盖 | 主流程断言 panorama.enterprise_count（number）；规则来源 catalog panorama.enterprise_count |
| L25 \| chain.sz-opportunity.main \| panorama.nodes \| 算法输出-panorama.nodes深圳机遇环节节点 | FUNC-00493 | 已覆盖 | 同条主流程断言 panorama.nodes 及元素 node_name、position、enterprise_count；规则来源 catalog panorama.nodes |
| L25 \| chain.sz-opportunity.main \| _empty \| 深圳机遇分析无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无机遇数据」构造条件；规则来源 契约空结果 |
| L25 \| chain.sz-opportunity.main \| _fail \| 深圳机遇分析查询失败 | FUNC-00494 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 FUNC-00493 的预期同时断言 sampleResponse 中未单独挂 L25 行的 `panorama.node_count`、`panorama.edges`、`panorama.district_dist`、`advantage`（含 advantages）、`problem`（含 problems）及 `opportunity`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L25.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B 线记 **无对应功能点**，不单独开 FUNC 用例：

`etl_clean_standardize`（多维区域数据清洗一致化，规则来源 需规（1）采集清洗）、`mining_advantage_constraints`（优势产业与制约因素识别，规则来源 需规分析阶段识别）、`advantage_problem_fusion`（优势与问题结果融合，规则来源 需规模型构建融合）、`expert_strategy_config`（专家策略配置驱动，规则来源 需规专家策略）、`ml_opportunity_predict`（机器学习机遇预测推荐，规则来源 需规 ML 预测推荐）、`strategy_plan_resource_talent`（发展规划与资源人才策略，规则来源 需规策略建议）、`opportunity_policy_innovation_outputs`（机遇清单与方向政策创新输出，规则来源 需规（2）四类输出）、`dynamic_monitor_refresh`（动态监测与策略更新，规则来源 需规动态监测）、`industry_tag_report_export`（产业标签与报告导出，规则来源 需规（3）调用导出）。

---

## B 线独有（catalog 有、L25 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L25 \| chain.sz-opportunity.m_chain_deep_128_1 \| — \| 深圳机遇分析模型 | FUNC-00495、00496 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint 与 responseFields panorama.enterprise_count、panorama.nodes）与缺 chainId |
| L25 \| chain.sz-opportunity.m_chain_sz_opportunity_count \| — \| 深圳产业机遇数 | FUNC-00497、00498 | 无对应功能点 | 同上；metric_id=M_CHAIN_SZ_OPPORTUNITY_COUNT |
| L25 \| chain.sz-opportunity.m_chain_sz_opportunity_score \| — \| 深圳产业机遇评分 | FUNC-00499、00500 | 无对应功能点 | 同上；metric_id=M_CHAIN_SZ_OPPORTUNITY_SCORE |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00501、00502 | 无对应功能点 | 4 接口下拉与 method/path 刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| FUNC 用例数 | 10 |
| 主流程 | 4（FUNC-00493 深圳机遇分析、00495 深圳机遇分析模型、00497 深圳产业机遇数、00499 深圳产业机遇评分） |
| 反向 | 4（FUNC-00494、00496、00498、00500，均为缺 chainId） |
| 清单 | 2（FUNC-00501、00502） |
| 编号 | FUNC-00493～00502 |
| L25 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L25 req_only | 9（无对应功能点） |
