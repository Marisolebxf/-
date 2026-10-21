# 企业培育潜力评估 · 功能点覆盖（entan.cultivate / L34）

> catalog `entan.cultivate` · path `#/entan/cultivate`  
> A 线真源：`fp-split-by-api-run/work/L34.md`  
> B 线用例：`FUNC-企业培育潜力评估-用例.md`（第三轮 **FUNC-00159**～**00162**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.cultivate.recommend | POST | /entan/v1/entan/metric/M_ENT_CULTIVATION_INDEX/compute | FUNC-00159、00160 | unavailable |
| （页面清单） | — | — | FUNC-00161、00162 | — |

---

## 功能点 → 用例矩阵（挂 L34.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L34 \| entan.cultivate.recommend \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | FUNC-00159、00160 | 已覆盖 | 规则来源 catalog enterprise_codes；合法全参 + 缺 enterprise_codes |
| L34 \| entan.cultivate.recommend \| rankings \| 算法输出-rankings培育推荐排名体 | FUNC-00159 | 已覆盖 | 规则来源 catalog rankings；主流程断言 value.result.rankings 及元素字段 |
| L34 \| entan.cultivate.recommend \| _empty \| 培育推荐无数据空态 | — | 未覆盖 | 规则来源 契约空结果；无稳定空结果构造条件 |
| L34 \| entan.cultivate.recommend \| _fail \| 培育推荐计算失败 | FUNC-00160 | 部分覆盖 | 规则来源 契约错误态；仅缺 enterprise_codes 反向 |
| L34 \| （无 endpoint） \| etl_clean_standardize \| 多源企业政策市场信息标准化清洗 | — | 未覆盖 | 规则来源 需规（1）采集清洗；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| triple_dimension_indicator_threshold \| 三维指标与阈值设定 | — | 未覆盖 | 规则来源 需规指标体系；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| historical_sample_model_train \| 历史样本模型训练与优化 | — | 未覆盖 | 规则来源 需规模型训练；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| weighted_cultivation_index_compute \| 加权培育推荐指数计算 | — | 未覆盖 | 规则来源 需规加权计算；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| threshold_rank_preferred_select \| 阈值筛选与企业排名优选 | — | 未覆盖 | 规则来源 需规排名优选；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| dynamic_policy_market_refresh \| 政策与市场数据动态更新 | — | 未覆盖 | 规则来源 需规动态监测；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| preferred_rank_industry_viz_outputs \| 优选排名与行业分布图输出 | — | 未覆盖 | 规则来源 需规（2）指数排名分布；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| analysis_report_semantic \| 详细分析报告语义 | — | 未覆盖 | 规则来源 需规（2）分析报告；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| industry_policy_scale_filter_scope \| 产业政策规模筛选语义 | — | 未覆盖 | 规则来源 需规（3）多维筛选；req_only，无对应功能点 |
| L34 \| （无 endpoint） \| api_sdk_platform_export \| API SDK 平台与导出 | — | 未覆盖 | 规则来源 需规（3）调用导出；req_only，无对应功能点 |

---

## req_only 行（无 endpoint 挂接）

L34.md 中 `etl_clean_standardize`、`triple_dimension_indicator_threshold`、`historical_sample_model_train`、`weighted_cultivation_index_compute`、`threshold_rank_preferred_select`、`dynamic_policy_market_refresh`、`preferred_rank_industry_viz_outputs`、`analysis_report_semantic`、`industry_policy_scale_filter_scope`、`api_sdk_platform_export` 共 **10** 条 **req_only** 无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。
