# 条件保障力 · 功能点覆盖（policy.guard）

> catalog `policy.guard` · 50897 · path `/policy/guard`  
> 用例 `API-条件保障力-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `policy.guard.main` 入参/出参及契约哨兵为准  
> 功能点键：`policy.guard | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.guard.main | GET | /policy/v1/policy/analysis/guard | API-000519～API-000523 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| policy.guard \| policy.guard.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000519、API-000521 | 部分覆盖 | GUARD-01 合法 scope_code=440000；非法 scope（GUARD-02）见 API-000521；仅 limit 无 scope（GUARD-04）本轮无独立用例 |
| policy.guard \| policy.guard.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000519、API-000522 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| policy.guard \| policy.guard.main \| rows \| 算法输出-rows组合分行列表 | catalog rows | API-000519、API-000523 | 契约占位 | unavailable，禁止 sample 行内 effect_score 作通过条件 |
| policy.guard \| policy.guard.main \| _empty \| 条件保障力无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| policy.guard \| policy.guard.main \| _fail \| 条件保障力查询失败 | 契约错误态 | API-000519、API-000520、API-000521、API-000522 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| policy.guard \| \| custom_metric_weights \| 用户自定义指标权重 | 需规（1.1.1.1.4.1.7.4.6 综合评估） | — | 未覆盖 | req_only；catalog 8a 未声明权重入参 |
| policy.guard \| \| composite_score_ranking \| 综合得分与排名展示 | 需规综合评估与排名 | — | 未覆盖 | req_only；本 endpoint 为 C7 组合读面，未单列排名契约 |
| policy.guard \| \| policy_optimization_advice \| 政策优化建议输出 | 需规七叶之建议叶 | — | 未覆盖 | req_only；非本 endpoint 范围 |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`rows`） |
| 未覆盖 | 4（含 `_empty` 1 + req_only 3） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000519～API-000523 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
