# 深圳问题识别 · 功能点覆盖（chain.sz-problem / L24）

> catalog `chain.sz-problem` · 50897 · path `#/chain/sz-problem`  
> 用例 `API-深圳问题识别-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/chain.json`（页 `chain.sz-problem`）  
> 功能点键：`L24 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.sz-problem.main | GET | /innov/v1/industry/{chainId}/shenzhen | API-00379～00383 | catalog `unavailable`；§0 **未试调**；本批为 **金样 5 条** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L24 \| chain.sz-problem.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00379、00381、00382 | 已覆盖 | 主路径占位 + 非法/缺 path |
| L24 \| chain.sz-problem.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | catalog panorama.enterprise_count | — | **未覆盖** | unavailable 金样批未写 live 成功形态；升档后补 |
| L24 \| chain.sz-problem.main \| panorama.nodes \| 算法输出-panorama.nodes深圳环节节点 | catalog panorama.nodes | — | **未覆盖** | 同上 |
| L24 \| chain.sz-problem.main \| _empty \| 深圳问题识别无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L24 \| chain.sz-problem.main \| _fail \| 深圳问题识别查询失败 | 契约错误态 | API-00380、00381、00382、00383 | 已覆盖 | 鉴权、非法 id、缺 path、畸形 id |
| L24 \| chain.sz-problem.main \| etl_clean_standardize \| 深全国多源数据清洗一致化 | 需规（1）采集清洗 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| negative_indicator_threshold \| 负面评价指标与权重阈值 | 需规指标体系 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| negative_evaluation_model \| 负面评价模型训练与优化 | 需规分析阶段模型 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| sz_national_problem_compare \| 深全国同类指标对比 | 需规深全国对比 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| problem_risk_list \| 问题与风险清单 | 需规（2）问题清单 | — | 无对应功能点 | req_only（样例 problem 非 responseFields） |
| L24 \| chain.sz-problem.main \| priority_ranking_report \| 优先级排序报告 | 需规（2）优先级 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| targeted_solution_suggest \| 针对性解决方案建议 | 需规（2）解决方案 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| viz_analysis_chart \| 可视化分析图表数据 | 需规（2）可视化 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| dynamic_problem_refresh \| 动态监测与结果更新 | 需规动态监测 | — | 无对应功能点 | req_only |
| L24 \| chain.sz-problem.main \| industry_domain_report_export \| 产业标签与报告导出 | 需规（3）调用导出 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 2（chainId、_fail） |
| 未覆盖（契约 field / _empty） | 3（enterprise_count、nodes、_empty） |
| 无对应功能点（req_only） | 10 |
| API 用例条数 | 5（00379～00383） |
| 金样 | API-00379 |
