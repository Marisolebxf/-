# 政策效果评估 · 功能点覆盖（policy.effect / L37）

> catalog `policy.effect` · 50897 · path `/policy/effect`  
> 用例 `API-政策效果评估-用例.md`  
> A 线范围：**L37**（`fp-split-by-api-run/work/L37.md`）  
> 功能点键：`L37 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.effect.main | GET | /policy/v1/policy/analysis/effect | API-000464～API-000468 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L37 \| policy.effect.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000464、API-000466 | 部分覆盖 | EFF-01 合法 scope_code=440300；非法 scope（EFF-02）见 API-000466；仅 limit 无 scope（EFF-04）本轮无独立用例 |
| L37 \| policy.effect.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000464、API-000467 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L37 \| policy.effect.main \| effect_score \| 算法输出-effect_score政策效果评估指数 | catalog effect_score | API-000468 | 契约占位 | unavailable，禁止 sample 指数作通过条件 |
| L37 \| policy.effect.main \| _empty \| 效果评估无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L37 \| policy.effect.main \| _fail \| 效果评估查询失败 | 契约错误态 | API-000464、API-000465、API-000466、API-000467 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L37 \| \| etl_clean_standardize \| 多源政策与经济社会环境数据标准化 | 需规（1）多源处理 | — | 未覆盖 | req_only |
| L37 \| \| exec_socio_env_dimensions \| 执行社会经济环境三维指标体系 | 需规三维指标 | — | 未覆盖 | req_only |
| L37 \| \| indicator_weight_compose \| 指标数值计算与权重分配 | 需规指标权重 | — | 未覆盖 | req_only |
| L37 \| \| weighted_effect_compute \| 加权综合生成效果评估指数 | 需规加权综合 | — | 未覆盖 | req_only |
| L37 \| \| dimension_evaluation_results \| 分维度评估结果输出 | 需规（2）分维度 | — | 未覆盖 | req_only |
| L37 \| \| improvement_performance_report \| 改进建议与绩效优化报告 | 需规（2）报告建议 | — | 未覆盖 | req_only |
| L37 \| \| policy_tag_time_stage_scope \| 政策标签时间区间与执行阶段查询 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L37 \| \| realtime_history_tracking \| 实时历史指数与持续效果追踪 | 需规持续追踪 | — | 未覆盖 | req_only |
| L37 \| \| api_sdk_platform_auto_eval \| API SDK 与平台自动化评估 | 需规（3）平台对接 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`effect_score`） |
| 未覆盖 | 10（含 `_empty` 1 + req_only 9） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000464～API-000468 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
