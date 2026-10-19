# 政策效果评估 · 功能点覆盖（policy.effect / L37）

> catalog `policy.effect` · path `#/policy/effect`  
> A 线真源：`fp-split-by-api-run/work/L37.md`  
> B 线用例：`API-政策效果评估-用例.md`（第二轮 **API-01426**～**01430**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.effect.main | GET | /policy/v1/policy/analysis/effect | API-01426～01430 | unavailable |

---

## 功能点 → 用例矩阵（挂 L37.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L37 \| policy.effect.main \| scope_code \| 算法输入-scope_code范围编码 | API-01426、01427、01429 | 已覆盖 | 主流程不传；EFF-02 补传 440000；EFF-04 非法 |
| L37 \| policy.effect.main \| limit \| 算法输入-limit结果条数上限 | API-01426、01428、01430 | 已覆盖 | sampleRequest limit=20；EFF-03 省略；EFF-05 非法 -1 |
| L37 \| policy.effect.main \| effect_score \| 算法输出-effect_score政策效果评估指数 | API-01426 | 已覆盖 | 主流程逐字段断言 effect_score（number）；同条含 sampleResponse 的 scope_name、scope_code、impl_effect |
| L37 \| policy.effect.main \| _empty \| 效果评估无数据空态 | — | 未覆盖 | 无稳定「合法入参必空」条件，不单开空态用例 |
| L37 \| policy.effect.main \| _fail \| 效果评估查询失败 | API-01429、01430 | 已覆盖 | 两参数各 1 条非法反向，预期为 message 或 msg |
| L37 \| \| etl_clean_standardize \| 多源政策与经济社会环境数据标准化 | — | 未覆盖 | req_only，无 catalog endpoint |
| L37 \| \| exec_socio_env_dimensions \| 执行社会经济环境三维指标体系 | — | 未覆盖 | req_only |
| L37 \| \| indicator_weight_compose \| 指标数值计算与权重分配 | — | 未覆盖 | req_only |
| L37 \| \| weighted_effect_compute \| 加权综合生成效果评估指数 | — | 未覆盖 | req_only |
| L37 \| \| dimension_evaluation_results \| 分维度评估结果输出 | — | 未覆盖 | req_only |
| L37 \| \| improvement_performance_report \| 改进建议与绩效优化报告 | — | 未覆盖 | req_only |
| L37 \| \| policy_tag_time_stage_scope \| 政策标签时间区间与执行阶段查询 | — | 未覆盖 | req_only |
| L37 \| \| realtime_history_tracking \| 实时历史指数与持续效果追踪 | — | 未覆盖 | req_only |
| L37 \| \| api_sdk_platform_auto_eval \| API SDK 与平台自动化评估 | — | 未覆盖 | req_only |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（scope_code、limit、effect_score、_fail） |
| 部分覆盖 | 0 |
| 未覆盖 | 10（_empty 1 + req_only 9） |

L37 共 14 行。B 线用例 5 条，不按 field 拆行。`code-registry` 由父控回写。
