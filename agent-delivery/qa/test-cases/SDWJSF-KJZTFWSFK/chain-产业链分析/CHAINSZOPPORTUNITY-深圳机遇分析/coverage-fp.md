# 深圳机遇分析 · 功能点覆盖（chain.sz-opportunity / L25）

> catalog `chain.sz-opportunity` · path `#/chain/sz-opportunity`  
> A 线真源：`fp-split-by-api-run/work/L25.md`  
> B 线用例：`API-深圳机遇分析-用例.md`（第二轮 **API-01288**～**01295**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.sz-opportunity.main | GET | /innov/v1/industry/{chainId}/shenzhen | API-01288、01289 | unavailable |
| chain.sz-opportunity.m_chain_deep_128_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | API-01290、01291 | available |
| chain.sz-opportunity.m_chain_sz_opportunity_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | API-01292、01293 | available |
| chain.sz-opportunity.m_chain_sz_opportunity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | API-01294、01295 | available |

---

## 功能点 → 用例矩阵（挂 L25.md）

多条 field 挂同一用例。不按 field 另开用例。advantage、problem、opportunity 及 panorama 内 node_count、edges、district_dist 等嵌套字段同挂 API-01288，L25 无独立 field 行。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L25 \| chain.sz-opportunity.main \| chainId \| 算法输入-chainId产业标识 | API-01288、01289 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L25 \| chain.sz-opportunity.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | API-01288 | 已覆盖 | 主流程按 sampleResponse 断言 panorama.enterprise_count（number）；规则来源 catalog panorama.enterprise_count |
| L25 \| chain.sz-opportunity.main \| panorama.nodes \| 算法输出-panorama.nodes深圳机遇环节节点 | API-01288 | 已覆盖 | 同条主流程断言 panorama.nodes 及元素 node_name、position、enterprise_count；规则来源 catalog panorama.nodes |
| L25 \| chain.sz-opportunity.main \| _empty \| 深圳机遇分析无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无机遇数据」构造条件；规则来源 契约空结果 |
| L25 \| chain.sz-opportunity.main \| _fail \| 深圳机遇分析查询失败 | API-01289 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L25.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多维区域数据清洗一致化）、`mining_advantage_constraints`（优势产业与制约因素识别）、`advantage_problem_fusion`（优势与问题结果融合）、`expert_strategy_config`（专家策略配置驱动）、`ml_opportunity_predict`（机器学习机遇预测推荐）、`strategy_plan_resource_talent`（发展规划与资源人才策略）、`opportunity_policy_innovation_outputs`（机遇清单与方向政策创新输出）、`dynamic_monitor_refresh`（动态监测与策略更新）、`industry_tag_report_export`（产业标签与报告导出）。

---

## B 线独有（catalog 有、L25 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L25 \| chain.sz-opportunity.m_chain_deep_128_1 \| — \| 深圳机遇分析模型 | API-01290、01291 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint 与 responseFields panorama.enterprise_count、panorama.nodes）与缺 chainId；L25 未给该 endpoint 挂 field 行 |
| L25 \| chain.sz-opportunity.m_chain_sz_opportunity_count \| — \| 深圳产业机遇数 | API-01292、01293 | 无对应功能点 | 同上；metric_id=M_CHAIN_SZ_OPPORTUNITY_COUNT |
| L25 \| chain.sz-opportunity.m_chain_sz_opportunity_score \| — \| 深圳产业机遇评分 | API-01294、01295 | 无对应功能点 | 同上；metric_id=M_CHAIN_SZ_OPPORTUNITY_SCORE |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 4 |
| title 数 | 4 |
| API 用例数 | 8 |
| 主流程 | 4（API-01288 深圳机遇分析、API-01290 深圳机遇分析模型、API-01292 深圳产业机遇数、API-01294 深圳产业机遇评分） |
| 反向 | 4（API-01289、01291、01293、01295，均为缺 chainId） |
| 编号 | API-01288～01295 |
| L25 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L25 req_only | 9（无对应功能点） |
| B 线独有 endpoint | 3（无对应功能点） |
