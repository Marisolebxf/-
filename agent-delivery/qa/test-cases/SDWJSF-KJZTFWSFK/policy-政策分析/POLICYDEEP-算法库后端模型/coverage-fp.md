# 算法库后端模型 · 功能点覆盖（policy.deep）

> catalog `policy.deep` · 50897 · path `/policy/deep`  
> 用例 `API-算法库后端模型-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `policy.deep.models` 入参/出参及契约哨兵为准  
> 功能点键：`policy.deep | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.deep.models | GET | /policy/v1/policy/analysis/deep | API-000524～API-000528 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| policy.deep \| policy.deep.models \| scope_code \| 算法输入-scope_code省市区编码 | catalog scope_code | API-000524、API-000526 | 部分覆盖 | DEEP-01 合法 scope_code=440300；非法 scope 见 DEEP-02 / API-000526 |
| policy.deep \| policy.deep.models \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000524、API-000527 | 已覆盖 | 主路径 limit=50 + 非正整数失败 |
| policy.deep \| policy.deep.models \| rows \| 算法输出-rows后端模型索引列表 | catalog rows | API-000528 | 契约占位 | unavailable，禁止 sample 六大模型 index 作通过条件 |
| policy.deep \| policy.deep.models \| _empty \| 后端模型索引无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| policy.deep \| policy.deep.models \| _fail \| 后端模型索引查询失败 | 契约错误态 | API-000524、API-000525、API-000526、API-000527 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| policy.deep \| \| six_model_aggregate_index \| 焦点力度效果短板机遇布局六大模型聚合索引 | catalog 页摘要 / metricIds | API-000524、API-000528 | 部分覆盖 | 仅 HTTP 契约；单模型算法语义见各子页 endpoint，本页 req_only 细项不展开 |
| policy.deep \| \| model_metric_id_cross_ref \| 模型行 metric_id 与指标注册表交叉引用 | 样例 metric_id 字段 | — | 未覆盖 | req_only；catalog responseFields 未声明 metric_id |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 2（`scope_code`、six_model_aggregate_index） |
| 契约占位 | 1（`rows`） |
| 未覆盖 | 2（含 `_empty` 1 + req_only 1） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000524～API-000528 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
