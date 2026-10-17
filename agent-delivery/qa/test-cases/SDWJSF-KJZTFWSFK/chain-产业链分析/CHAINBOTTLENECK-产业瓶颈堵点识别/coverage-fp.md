# 产业瓶颈堵点识别 · 功能点覆盖（chain.bottleneck / L22）

> catalog `chain.bottleneck` · 50897 · path `/chain/bottleneck`  
> 用例 `API-产业瓶颈堵点识别-用例.md`  
> A 线范围：**L22**（`fp-split-by-api-run/work/L22.md`）  
> 功能点键：`L22 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.bottleneck.main | GET | /innov/v1/industry/{chainId}/bottlenecks | API-00051～API-00054 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L22 \| chain.bottleneck.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00053、API-00054 | 部分覆盖 | 非法 id 与缺 path；live 成功校验待 endpoint available 后补主路径 |
| L22 \| chain.bottleneck.main \| severity \| 算法输出-severity严重度 | catalog severity | API-00051 | 契约占位 | unavailable，禁止 sample 严重度文案作通过条件 |
| L22 \| chain.bottleneck.main \| overall_score \| 算法输出-overall_score综合得分 | catalog overall_score | API-00051 | 契约占位 | 同上 |
| L22 \| chain.bottleneck.main \| _empty \| 瓶颈堵点识别无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法 chainId 必空」试调证据，禁止编造年份/参数 |
| L22 \| chain.bottleneck.main \| _fail \| 瓶颈堵点识别查询失败 | 契约错误态 | API-00051、API-00053、API-00054 | 已覆盖 | 含 catalog 不可用与入参失败语义 |
| L22 \| \| etl_clean_standardize \| 多源瓶颈信息标准化清洗 | 需规段一采集清洗 | — | 未覆盖 | req_only，无 catalog endpoint |
| L22 \| \| bottleneck_five_dim_threshold \| 五维指标与权重阈值体系 | 需规评价体系 | — | 未覆盖 | req_only |
| L22 \| \| dimension_bottleneck_identify \| 各维指标计算与堵点类型标注 | 需规分析阶段 | — | 未覆盖 | req_only |
| L22 \| \| bottleneck_cause_impact_path \| 成因影响与解决路径分析 | 需规系统分析 | — | 未覆盖 | req_only |
| L22 \| \| bottleneck_list_semantic \| 产业瓶颈堵点清单语义 | 需规（2）堵点清单 | — | 未覆盖 | req_only |
| L22 \| \| solution_recommendation \| 解决方案建议 | 需规（2）解决方案 | — | 未覆盖 | req_only；sample 内 suggestions 非 responseFields |
| L22 \| \| dynamic_bottleneck_refresh \| 动态跟踪与结果更新 | 需规动态跟踪 | — | 未覆盖 | req_only |
| L22 \| \| bottleneck_analysis_report \| 瓶颈成因分析报告 | 需规（2）分析报告 | — | 未覆盖 | req_only |
| L22 \| \| trend_warning_chart_data \| 趋势预警图表数据 | 需规（2）趋势预警 | — | 未覆盖 | req_only |
| L22 \| \| domain_query_export \| 产业标签与领域类别查询及导出 | 需规（3）调用方式 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail` 行） |
| 部分覆盖 | 1（`chainId`） |
| 契约占位 | 2（`severity`、`overall_score`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 4 |
| 编号 | API-00051～API-00054 |
| `_empty` 未覆盖 | 1 |
| 试调 | 无 token 主路径 1 次（HTTP 424）；带 token 金样 **未试调**，执行期复核 |
