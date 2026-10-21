# 产业瓶颈堵点识别 · 功能点覆盖（chain.bottleneck / L22）

> catalog `chain.bottleneck` · path `#/chain/bottleneck`  
> A 线真源：`fp-split-by-api-run/work/L22.md`  
> B 线用例：`FUNC-产业瓶颈堵点识别-用例.md`（第三轮 **FUNC-00467**～**00472**；历史 API-01270～01273 作废）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.bottleneck.main | GET | /innov/v1/industry/{chainId}/bottlenecks | FUNC-00467、00468 | unavailable |
| chain.bottleneck.m_chain_deep_125_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_125_1/compute | FUNC-00469、00470 | available |

---

## 功能点 → 用例矩阵（挂 L22.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L22 \| chain.bottleneck.main \| chainId \| 算法输入-chainId产业标识 | API-01270、01271 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L22 \| chain.bottleneck.main \| severity \| 算法输出-severity严重度 | API-01270 | 已覆盖 | 主流程断言 severity（string）；规则来源 catalog severity |
| L22 \| chain.bottleneck.main \| overall_score \| 算法输出-overall_score综合得分 | API-01270 | 已覆盖 | 同条主流程断言 overall_score（number）；规则来源 catalog overall_score |
| L22 \| chain.bottleneck.main \| _empty \| 瓶颈堵点识别无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且无瓶颈数据」构造条件；规则来源 契约空结果 |
| L22 \| chain.bottleneck.main \| _fail \| 瓶颈堵点识别查询失败 | API-01271 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 API-01270 的预期同时断言 sampleResponse 中未单独挂 L22 行的 `tech_score`、`talent_score`、`market_score`、`capital_score`、`policy_score` 及 `suggestions[].name`、`suggestions[].advice`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L22.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。B 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（多源瓶颈信息标准化清洗，规则来源 需规段一采集清洗）、`bottleneck_five_dim_threshold`（五维指标与权重阈值体系，规则来源 需规评价体系）、`dimension_bottleneck_identify`（各维指标计算与堵点类型标注，规则来源 需规分析阶段）、`bottleneck_cause_impact_path`（成因影响与解决路径分析，规则来源 需规系统分析）、`bottleneck_list_semantic`（产业瓶颈堵点清单语义，规则来源 需规（2）堵点清单）、`solution_recommendation`（解决方案建议，规则来源 需规（2）解决方案）、`dynamic_bottleneck_refresh`（动态跟踪与结果更新，规则来源 需规动态跟踪）、`bottleneck_analysis_report`（瓶颈成因分析报告，规则来源 需规（2）分析报告）、`trend_warning_chart_data`（趋势预警图表数据，规则来源 需规（2）趋势预警）、`domain_query_export`（产业标签与领域类别查询及导出，规则来源 需规（3）调用方式）。

`solution_recommendation` 按 L22 仍记无对应功能点。catalog `sampleResponse` 顶层另有 `suggestions`，已写入 API-01270 预期，不改 A 线、不另开行。

---

## B 线独有（catalog 有、L22 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L22 \| chain.bottleneck.m_chain_deep_125_1 \| — \| 产业瓶颈堵点识别模型 | API-01272、01273 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L22 未给该 endpoint 挂 field 行 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4 |
| 主流程 | 2（API-01270 瓶颈堵点、API-01272 产业瓶颈堵点识别模型） |
| 反向 | 2（API-01271、API-01273，均为缺 chainId） |
| 编号 | API-01270～01273 |
| L22 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L22 req_only | 10（无对应功能点） |
