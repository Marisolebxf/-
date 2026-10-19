# 重点布局产业推荐 · 功能点覆盖（chain.layout / L26）

> catalog `chain.layout` · path `#/chain/layout`  
> A 线真源：`fp-split-by-api-run/work/L26.md`  
> B 线用例：`API-重点布局产业推荐-用例.md`（第二轮 **API-01304**～**01307**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.hotspot.recommendation | GET | /innov/v1/industry/{chainId}/recommendation | API-01304、01305 | unavailable |
| chain.layout.m_chain_deep_129_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | API-01306、01307 | available |

---

## 功能点 → 用例矩阵（挂 L26.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L26 \| chain.hotspot.recommendation \| chainId \| 算法输入-chainId产业标识 | API-01304、01305 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L26 \| chain.hotspot.recommendation \| recommend_index \| 算法输出-recommend_index产业推荐指数 | API-01304 | 已覆盖 | 主流程断言 recommend_index（number，示例 84.2）；规则来源 catalog recommend_index |
| L26 \| chain.hotspot.recommendation \| recommend_level \| 算法输出-recommend_level重点布局推荐等级 | API-01304 | 已覆盖 | 同条主流程断言 recommend_level（string，示例 优先布局）；规则来源 catalog recommend_level |
| L26 \| chain.hotspot.recommendation \| _empty \| 布局推荐无数据空态 | — | 未覆盖 | 描述写 INB1701 无推荐，无稳定空态构造条件；规则来源 契约空结果 |
| L26 \| chain.hotspot.recommendation \| _fail \| 布局推荐查询失败 | API-01305 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 API-01304 的预期同时断言 sampleResponse 中未单独挂 L26 行的 `advantage_score`、`opportunity_score`、`policy_match_score`、`rank_overall`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L26.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多源产业数据标准化清洗，规则来源 需规（1）采集清洗）、`scale_growth_potential_advantage`（规模增长率潜力与优劣势识别，规则来源 需规分析阶段）、`advantage_problem_fusion`（优势与问题识别结果融合，规则来源 需规优势+问题输入）、`expert_recommend_strategy`（专家推荐策略参数驱动，规则来源 需规专家策略）、`index_rank_layout_select`（指数排名筛选重点布局产业，规则来源 需规排名筛选）、`dynamic_strategy_refresh`（策略动态优化与结果刷新，规则来源 需规动态优化）、`ranking_trend_layout_outputs`（排名清单趋势图表与布局报告，规则来源 需规（2）四类输出）、`demand_tag_region_category`（需求标签区域与产业类别范围，规则来源 需规（3）调用范围）、`trend_monitor_report_export`（趋势监测与报告导出，规则来源 需规（3）监测导出）。

---

## B 线独有（catalog 有、L26 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L26 \| chain.layout.m_chain_deep_129_1 \| — \| 重点布局产业推荐模型 | API-01306、01307 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint，以及 responseFields 的 recommend_level、recommend_index）与缺 chainId；L26 未给该 endpoint 挂 field 行 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2（API-01304 重点布局产业推荐、API-01306 重点布局产业推荐模型） |
| 反向 | 2（API-01305、API-01307，均为缺 chainId） |
| 编号 | API-01304～01307 |
| L26 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L26 req_only | 9（无对应功能点） |
