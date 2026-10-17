# 企业发展痛难点识别 · 功能点覆盖（entan.pain-points / L29）

> catalog `entan.pain-points` · 50897 · path `/entan/pain-points`  
> **用例册**：`API-企业发展痛难点识别-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00095`～`00104`，共 **10** 条）  
> A 线范围：**L29**（`fp-split-by-api-run/work/L29.md`）  
> 功能点键：`L29 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.pain-points.count | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | API-00095～00098、00103 | catalog `status=unavailable` |
| entan.pain-points.severity | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | API-00099～00102、00104 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L29 \| entan.pain-points.count \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00096、00097、00098 | 部分覆盖 | 缺省/空集合/非法；live 合法集合成功校验待 endpoint available 后补 |
| L29 \| entan.pain-points.count \| dimension_cards \| 算法输出-dimension_cards维度卡片体 | catalog dimension_cards | API-00095 | 契约占位 | unavailable，禁止 sample 卡片数值作通过条件 |
| L29 \| entan.pain-points.count \| _empty \| 痛难点反映企业数无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法非空集合必空」试调证据 |
| L29 \| entan.pain-points.count \| _fail \| 痛难点反映企业数计算失败 | 契约错误态 | API-00095、00096、00097、00098 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| L29 \| entan.pain-points.severity \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00100、00101、00102、00104 | 部分覆盖 | 含类型错误单缺陷 |
| L29 \| entan.pain-points.severity \| dimension_cards \| 算法输出-dimension_cards维度卡片体 | catalog dimension_cards | API-00099 | 契约占位 | 同上 |
| L29 \| entan.pain-points.severity \| _empty \| 痛难点严重度无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L29 \| entan.pain-points.severity \| _fail \| 痛难点严重度计算失败 | 契约错误态 | API-00099、00100、00101、00102、00104 | 已覆盖 | |
| L29 \| （无 endpoint） \| etl_clean_standardize \| 多源经营及人力资源数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| painpoint_indicator_threshold \| 四维度核心指标与判定阈值 | 需规指标体系 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| painpoint_model_identify \| 痛难点识别模型训练与瓶颈堵点定位 | 需规计算分析阶段 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| painpoint_metric_compute \| 痛难点反映企业数与严重度指标计算 | 需规量化评估 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| improvement_suggestion_generate \| 针对性改进建议生成 | 需规改进建议 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| bottleneck_list_semantic \| 瓶颈清单输出语义 | 需规（2）瓶颈清单 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| dynamic_painpoint_refresh \| 动态监测与结论更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| painpoint_analysis_report \| 企业发展痛难点分析报告 | 需规（2）分析报告 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业标识或名称查询语义 | 需规（3）调用方式 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| viz_painpoint_data \| 痛难点可视化数据支撑 | 需规（3）可视化 | — | 未覆盖 | req_only |
| L29 \| （无 endpoint） \| analysis_report_export \| 分析报告与数据导出 | 需规（3）导出 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（双 endpoint `_fail` 契约行） |
| 部分覆盖 | 2（双 endpoint `enterprise_codes`） |
| 契约占位 | 2（双 endpoint `dimension_cards`） |
| 未覆盖 | 13（含 `_empty` 2 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 10 |
| 编号 | API-00095～API-00104 |
| `_empty` 未覆盖 | 2 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
