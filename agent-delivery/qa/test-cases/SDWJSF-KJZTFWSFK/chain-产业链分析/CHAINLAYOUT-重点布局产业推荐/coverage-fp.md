# 重点布局产业推荐 · 功能点覆盖（chain.layout / L26）

> catalog `chain.layout` · path `#/chain/layout`  
> A 线真源：`fp-split-by-api-run/work/L26.md`  
> B 线用例：`FUNC-重点布局产业推荐-用例.md`（第三轮 **FUNC-00515**～**00520**）  
> 历史 R2 API 册：`API-重点布局产业推荐-用例.md`（**API-01304**～**01307**，第三轮不复用编号）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.hotspot.recommendation | GET | /innov/v1/industry/{chainId}/recommendation | FUNC-00515、00516 | unavailable |
| chain.layout.m_chain_deep_129_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | FUNC-00517、00518 | available |
| （页面清单） | — | — | FUNC-00519、00520 | — |

---

## 功能点 → 用例矩阵（挂 L26.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L26 \| chain.hotspot.recommendation \| chainId \| 算法输入-chainId产业标识 | FUNC-00515、00516 | 已覆盖 | 合法 chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L26 \| chain.hotspot.recommendation \| recommend_index \| 算法输出-recommend_index产业推荐指数 | FUNC-00515 | 已覆盖 | 主流程断言 recommend_index（number，示例 84.2）；规则来源 catalog recommend_index |
| L26 \| chain.hotspot.recommendation \| recommend_level \| 算法输出-recommend_level重点布局推荐等级 | FUNC-00515 | 已覆盖 | 同条主流程断言 recommend_level（string，示例 优先布局）；规则来源 catalog recommend_level |
| L26 \| chain.hotspot.recommendation \| _empty \| 布局推荐无数据空态 | — | 未覆盖 | 描述写 INB1701 无推荐，无稳定空态构造条件；规则来源 契约空结果 |
| L26 \| chain.hotspot.recommendation \| _fail \| 布局推荐查询失败 | FUNC-00516 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 FUNC-00515 的预期同时断言 sampleResponse 中未单独挂 L26 行的 `advantage_score`、`opportunity_score`、`policy_match_score`、`rank_overall`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L26.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B 线记 **无对应功能点**，不单独开 FUNC 用例：

`etl_clean_standardize`（多源产业数据标准化清洗，规则来源 需规（1）采集清洗）、`scale_growth_potential_advantage`（规模增长率潜力与优劣势识别，规则来源 需规分析阶段）、`advantage_problem_fusion`（优势与问题识别结果融合，规则来源 需规优势+问题输入）、`expert_recommend_strategy`（专家推荐策略参数驱动，规则来源 需规专家策略）、`index_rank_layout_select`（指数排名筛选重点布局产业，规则来源 需规排名筛选）、`dynamic_strategy_refresh`（策略动态优化与结果刷新，规则来源 需规动态优化）、`ranking_trend_layout_outputs`（排名清单趋势图表与布局报告，规则来源 需规（2）四类输出）、`demand_tag_region_category`（需求标签区域与产业类别范围，规则来源 需规（3）调用范围）、`trend_monitor_report_export`（趋势监测与报告导出，规则来源 需规（3）监测导出）。

---

## B 线独有（catalog 有、L26 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L26 \| chain.layout.m_chain_deep_129_1 \| — \| 重点布局产业推荐模型 | FUNC-00517、00518 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint，以及 responseFields 的 recommend_level、recommend_index）与缺 chainId；L26 未给该 endpoint 挂 field 行 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00519、00520 | 无对应功能点 | 2 接口下拉与 method/path 刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6 |
| 主流程 | 2（FUNC-00515 重点布局产业推荐、FUNC-00517 重点布局产业推荐模型） |
| 反向 | 2（FUNC-00516、00518，均为缺 chainId） |
| 清单 | 2（FUNC-00519、00520） |
| 编号 | FUNC-00515～00520 |
| L26 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L26 req_only | 9（无对应功能点） |
