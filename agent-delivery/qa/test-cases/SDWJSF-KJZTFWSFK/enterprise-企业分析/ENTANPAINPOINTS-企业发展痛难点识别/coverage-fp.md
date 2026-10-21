# 企业发展痛难点识别 · 功能点覆盖（entan.pain-points / L29）

> catalog `entan.pain-points` · path `#/entan/pain-points`  
> A 线真源：`fp-split-by-api-run/work/L29.md`  
> B 线用例：`FUNC-企业发展痛难点识别-用例.md`（第三轮 **FUNC-00117**～**00126**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.pain-points.count | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | FUNC-00117、00118 | unavailable |
| entan.pain-points.severity | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | FUNC-00119、00120 | unavailable |
| entan.pain-points.count.m_ent_painpoint_gap | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | FUNC-00121、00122 | available |
| entan.pain-points.count.m_ent_painpoint_topic | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | FUNC-00123、00124 | available |

页面清单（接口信息 / 算法测试）：FUNC-00125、00126（无单独 endpoint_id）。

---

## 功能点 → 用例矩阵（挂 L29.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L29 \| entan.pain-points.count \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | FUNC-00117、00118 | 已覆盖 | 合法全参 + 缺 enterprise_codes |
| L29 \| entan.pain-points.count \| dimension_cards \| 算法输出-dimension_cards维度卡片体 | catalog dimension_cards | FUNC-00117 | 已覆盖 | 主流程断言 value.dimension_cards 及子字段 |
| L29 \| entan.pain-points.count \| _empty \| 痛难点反映企业数无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造；不单开空态用例 |
| L29 \| entan.pain-points.count \| _fail \| 痛难点反映企业数计算失败 | 契约错误态 | FUNC-00118 | 部分覆盖 | 仅缺 enterprise_codes |
| L29 \| entan.pain-points.severity \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | FUNC-00119、00120 | 已覆盖 | 合法全参 + 缺 enterprise_codes |
| L29 \| entan.pain-points.severity \| dimension_cards \| 算法输出-dimension_cards维度卡片体 | catalog dimension_cards | FUNC-00119 | 已覆盖 | 主流程断言 value.dimension_cards 及子字段 |
| L29 \| entan.pain-points.severity \| _empty \| 痛难点严重度无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造 |
| L29 \| entan.pain-points.severity \| _fail \| 痛难点严重度计算失败 | 契约错误态 | FUNC-00120 | 部分覆盖 | 仅缺 enterprise_codes |
| L29 \| （无 endpoint） \| etl_clean_standardize \| 多源经营及人力资源数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| painpoint_indicator_threshold \| 四维度核心指标与判定阈值 | 需规指标体系 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| painpoint_model_identify \| 痛难点识别模型训练与瓶颈堵点定位 | 需规计算分析阶段 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| painpoint_metric_compute \| 痛难点反映企业数与严重度指标计算 | 需规量化评估 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| improvement_suggestion_generate \| 针对性改进建议生成 | 需规改进建议 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| bottleneck_list_semantic \| 瓶颈清单输出语义 | 需规（2）瓶颈清单 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| dynamic_painpoint_refresh \| 动态监测与结论更新 | 需规动态监测 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| painpoint_analysis_report \| 企业发展痛难点分析报告 | 需规（2）分析报告 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业标识或名称查询语义 | 需规（3）调用方式 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| viz_painpoint_data \| 痛难点可视化数据支撑 | 需规（3）可视化 | — | 未覆盖 | 无对应功能点（req_only） |
| L29 \| （无 endpoint） \| analysis_report_export \| 分析报告与数据导出 | 需规（3）导出 | — | 未覆盖 | 无对应功能点（req_only） |

---

## B 线独有（catalog 有、L29 未列 endpoint）

| endpoint_id | title | 对应用例编号 | 状态 | 说明 |
|-------------|-------|--------------|------|------|
| entan.pain-points.count.m_ent_painpoint_gap | 痛难点改进差距 | FUNC-00121、00122 | 已覆盖 | 无对应功能点；主流程 + 缺 enterprise_codes |
| entan.pain-points.count.m_ent_painpoint_topic | 发展痛难点诊断 | FUNC-00123、00124 | 已覆盖 | 无对应功能点；主流程 + 缺 enterprise_codes |

L29 只挂 `entan.pain-points.count` 与 `entan.pain-points.severity`。改进差距、发展痛难点诊断以 catalog JSON 为准写入用例，矩阵反表记无对应功能点。

---

## 覆盖统计

| 维度 | 计数 |
|------|------|
| A 线表行（L29） | **19** |
| 已覆盖 | **4**（enterprise_codes×2、dimension_cards×2） |
| 部分覆盖 | **2**（`_fail`×2，仅缺参反向） |
| 未覆盖 | **13**（`_empty`×2 + req_only×11） |
| catalog endpoint 数 | **4**（A 线 2 + B 线独有 2） |
| FUNC 用例数 | **10**（主流程 4、反向 4、清单 2） |
| 编号 | FUNC-00117～FUNC-00126 |
