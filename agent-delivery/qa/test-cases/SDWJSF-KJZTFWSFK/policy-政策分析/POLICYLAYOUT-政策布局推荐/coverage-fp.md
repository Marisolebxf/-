# 政策布局推荐 · 功能点覆盖（policy.layout / L40）

> catalog `policy.layout` · path `#/policy/layout`  
> A 线真源：`fp-split-by-api-run/work/L40.md`  
> B 线用例：`API-政策布局推荐-用例.md`（第二轮 **API-01441**～**01445**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.layout.main | GET | /policy/v1/policy/analysis/layout | API-01441～01445 | unavailable |

---

## 功能点 → 用例矩阵（挂 L40.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L40 \| policy.layout.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-01443、01444 | 已覆盖 | 01443 补传 440000；01444 非法 scope_code。主流程按 sampleRequest 不传 |
| L40 \| policy.layout.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-01441、01442、01445 | 已覆盖 | 主流程 limit=20 + 省略 + 非法 limit=-1 |
| L40 \| policy.layout.main \| layout_rec_cnt \| 算法输出-layout_rec_cnt布局推荐条数 | catalog layout_rec_cnt | API-01441 | 已覆盖 | 主流程逐字段断言 layout_rec_cnt（number）；备选 01442、01443 同结构。文档标记未交付 |
| L40 \| policy.layout.main \| _empty \| 布局推荐无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L40 \| policy.layout.main \| _fail \| 布局推荐查询失败 | 契约错误态 | API-01444、01445 | 已覆盖 | 两参数各 1 条非法反向，预期 message 或 msg |

---

## req_only 行（无 endpoint 挂接）

L40.md 中 `opportunity_gap_db_integrate`、`opportunity_gap_modules`、`expert_strategy_case_fusion`、`policy_kb_retrieval_semantic`、`weighted_priority_layout_rank`、`layout_effect_optimize_outputs`、`deploy_monitor_dynamic_tune`、`weight_db_filter_strategy_scope`、`region_industry_theme_scope`、`api_sdk_policy_mgmt_flow` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

sampleResponse 另有 `scope_name`、`recommendations`，已写入正向预期；A 线未把这两项单列 field_key。
