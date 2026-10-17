# 政策布局推荐 · 功能点覆盖（policy.layout / L40）

> catalog `policy.layout` · 50897 · path `/policy/layout`  
> 用例 `API-政策布局推荐-用例.md`  
> A 线范围：**L40**（`fp-split-by-api-run/work/L40.md`）  
> 功能点键：`L40 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.layout.main | GET | /policy/v1/policy/analysis/layout | API-000479～API-000483 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L40 \| policy.layout.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000479、API-000481 | 部分覆盖 | LAY-01 不传 scope；非法 scope 见 LAY-02 / API-000481 |
| L40 \| policy.layout.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000479、API-000482 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| L40 \| policy.layout.main \| layout_rec_cnt \| 算法输出-layout_rec_cnt布局推荐条数 | catalog layout_rec_cnt | API-000483 | 契约占位 | unavailable，禁止 sample 建议数作通过条件 |
| L40 \| policy.layout.main \| _empty \| 布局推荐无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| L40 \| policy.layout.main \| _fail \| 布局推荐查询失败 | 契约错误态 | API-000479、API-000480、API-000481、API-000482 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| L40 \| \| opportunity_gap_db_integrate \| 机遇短板结果与政策库整合 | 需规（1）整合关联 | — | 未覆盖 | req_only |
| L40 \| \| opportunity_gap_modules \| 机遇分析与短板识别模块 | 需规运行逻辑 1–2 | — | 未覆盖 | req_only |
| L40 \| \| expert_strategy_case_fusion \| 专家策略与案例文献融合 | 需规策略生成 | — | 未覆盖 | req_only |
| L40 \| \| policy_kb_retrieval_semantic \| 政策知识库集中检索语义 | 需规知识库构建 | — | 未覆盖 | req_only |
| L40 \| \| weighted_priority_layout_rank \| 加权评分与多维优先级排序 | 需规优先级排序 | — | 未覆盖 | req_only |
| L40 \| \| layout_effect_optimize_outputs \| 布局建议效果预测与优化策略输出 | 需规（2）三类输出 | — | 未覆盖 | req_only |
| L40 \| \| deploy_monitor_dynamic_tune \| 落实监测与动态参数优化 | 需规效果评估优化 | — | 未覆盖 | req_only |
| L40 \| \| weight_db_filter_strategy_scope \| 机遇短板权重与库筛选条件语义 | 需规（3）调用参数 | — | 未覆盖 | req_only |
| L40 \| \| region_industry_theme_scope \| 区域产业主题在线布局分析 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L40 \| \| api_sdk_policy_mgmt_flow \| API SDK 政策管理全流程对接 | 需规（3）系统联动 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`layout_rec_cnt`） |
| 未覆盖 | 11（含 `_empty` 1 + req_only 10） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000479～API-000483 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
