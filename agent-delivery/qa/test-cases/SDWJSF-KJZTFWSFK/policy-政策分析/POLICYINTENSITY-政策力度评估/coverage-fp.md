# 政策力度评估 · 功能点覆盖（policy.intensity / L36）

> catalog `policy.intensity` · 50897 · path `/policy/intensity`  
> 用例 `API-政策力度评估-用例.md`  
> A 线范围：**L36**（`fp-split-by-api-run/work/L36.md`）  
> 功能点键：`L36 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.intensity.main | GET | /policy/v1/policy/analysis/intensity | API-000459～API-000463 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L36 \| policy.intensity.main \| scope_type \| 算法输入-scope_type范围类型 | catalog scope_type | API-000459 | 部分覆盖 | INT-01 合法 province；非法枚举（INT-04）本轮无独立用例 |
| L36 \| policy.intensity.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000461 | 部分覆盖 | 非法/不存在 scope_code；与 scope_type 组合合法但空 code 见 INT-01 |
| L36 \| policy.intensity.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000459、API-000462 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L36 \| policy.intensity.main \| intensity_index \| 算法输出-intensity_index政策力度指数 | catalog intensity_index | API-000463 | 契约占位 | unavailable，禁止 sample 指数作通过条件 |
| L36 \| policy.intensity.main \| _empty \| 力度评估无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L36 \| policy.intensity.main \| _fail \| 力度评估查询失败 | 契约错误态 | API-000459、API-000460、API-000461、API-000462 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L36 \| \| etl_clean_standardize \| 多源政策数据标准化清洗 | 需规（1） | — | 未覆盖 | req_only |
| L36 \| \| effect_coverage_cost_dimensions \| 效果覆盖成本三维指标体系 | 需规三维指标 | — | 未覆盖 | req_only |
| L36 \| \| weighted_intensity_compute \| 权重赋值与综合加权计算 | 需规加权计算 | — | 未覆盖 | req_only |
| L36 \| \| threshold_grade_classify \| 阈值分类分级 | 需规阈值分级 | — | 未覆盖 | req_only |
| L36 \| \| horizontal_vertical_track \| 横向对比与纵向趋势跟踪 | 需规对比趋势 | — | 未覆盖 | req_only |
| L36 \| \| dimension_analysis_report \| 力度维度分析报告语义 | 需规（2）维度报告 | — | 未覆盖 | req_only |
| L36 \| \| intensity_ranking_semantic \| 政策力度排行榜语义 | 需规（2）排行榜 | — | 未覆盖 | req_only |
| L36 \| \| trend_predict_outputs \| 趋势变化图与预测分析语义 | 需规（2）趋势预测 | — | 未覆盖 | req_only |
| L36 \| \| policy_category_time_scope \| 政策类别与时间区间查询语义 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L36 \| \| api_sdk_embed_export \| API SDK 嵌入与导出 | 需规（3）调用嵌入 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 2（`scope_type`、`scope_code`） |
| 契约占位 | 1（`intensity_index`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000459～API-000463 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
