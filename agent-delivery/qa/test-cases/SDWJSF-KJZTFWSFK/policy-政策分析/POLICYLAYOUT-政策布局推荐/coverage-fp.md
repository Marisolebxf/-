# 政策布局推荐 · 功能点覆盖（policy.layout / L40）

> catalog `policy.layout` · path `#/policy/layout`  
> A 线真源：`fp-split-by-api-run/work/L40.md`  
> B 线用例：`FUNC-政策布局推荐-用例.md`（第三轮 **FUNC-00653**～**FUNC-00659**）  
> 联调台 https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.layout.main | GET | /policy/v1/policy/analysis/layout | FUNC-00653～00657 | unavailable |

---

## 功能点 → 用例矩阵（挂 L40.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L40 \| policy.layout.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | FUNC-00653、00654、00656 | 已覆盖 | 主路径不传 + 补传 440000 + 非法 scope_code |
| L40 \| policy.layout.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | FUNC-00653、00655、00657 | 已覆盖 | 主路径 limit=20 + 省略 + 非法 limit=-1 |
| L40 \| policy.layout.main \| layout_rec_cnt \| 算法输出-layout_rec_cnt布局推荐条数 | catalog layout_rec_cnt | FUNC-00653 | 已覆盖 | 主流程逐字段断言 layout_rec_cnt（number）；备选 00654、00655 同结构。文档标记未交付 |
| L40 \| policy.layout.main \| _empty \| 布局推荐无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L40 \| policy.layout.main \| _fail \| 布局推荐查询失败 | 契约错误态 | FUNC-00656、00657 | 已覆盖 | 两参数各 1 条非法反向，预期 message 或 msg |
| （页面清单） \| policy.layout \| 接口信息 / 算法测试 | catalog 页签 | FUNC-00658、00659 | 已覆盖 | 单接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L40.md 中 `opportunity_gap_db_integrate`、`opportunity_gap_modules`、`expert_strategy_case_fusion`、`policy_kb_retrieval_semantic`、`weighted_priority_layout_rank`、`layout_effect_optimize_outputs`、`deploy_monitor_dynamic_tune`、`weight_db_filter_strategy_scope`、`region_industry_theme_scope`、`api_sdk_policy_mgmt_flow` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

sampleResponse 另有 `scope_name`、`recommendations`，已写入正向预期；A 线未把这两项单列 field_key。

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（布局推荐） |
| FUNC 用例数 | 7 |
| 主流程 | 1（FUNC-00653） |
| 备选-参数组合 | 2（FUNC-00654、00655） |
| 反向 | 2（FUNC-00656、00657） |
| 清单 | 2（FUNC-00658、00659） |
| 编号 | FUNC-00653～00659 |
| 旧 API 册 | API-01441～01445 作废，见 FUNC 册 §4 |
