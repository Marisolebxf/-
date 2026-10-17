# 发展战略引导力 · 功能点覆盖（policy.guide）

> catalog `policy.guide` · 50897 · path `/policy/guide`  
> 用例 `API-发展战略引导力-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `policy.guide.main` 入参/出参及契约哨兵为准  
> 功能点键：`policy.guide | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.guide.main | GET | /policy/v1/policy/analysis/guide | API-000514～API-000518 | catalog `status=unavailable`；§0 **未试调**；C7 读 C1+C6 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| policy.guide \| policy.guide.main \| scope_code \| 算法输入-scope_code范围编码 | catalog scope_code | API-000514、API-000516 | 部分覆盖 | GUIDE-01 不传 scope；非法 scope 见 GUIDE-02 / API-000516 |
| policy.guide \| policy.guide.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000514、API-000517 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| policy.guide \| policy.guide.main \| rows \| 算法输出-rows组合分行 | catalog rows | API-000514、API-000518 | 契约占位 | unavailable，禁止 sample 分值/区域名作通过条件 |
| policy.guide \| policy.guide.main \| _empty \| 引导力无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| policy.guide \| policy.guide.main \| _fail \| 引导力查询失败 | 契约错误态 | API-000514、API-000515、API-000516、API-000517 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| policy.guide \| \| foresight_system_target_eval \| 前瞻性系统性针对性评估 | 需规（展示 1.1.1.1.4.1.7.4.1） | — | 未覆盖 | req_only；三性口径待甲方确认（PG-D01 / Q-MO-DS07-05） |
| policy.guide \| \| strategy_plan_doc_collect \| 发展战略规划与产业政策收集 | 需规收集分析 | — | 未覆盖 | req_only；catalog 无专叶入参 |
| policy.guide \| \| strategy_key_content_path_goal \| 关键内容实施路径预期目标展示 | 需规字段展示 | — | 未覆盖 | req_only；8a 未声明对应 responseFields |
| policy.guide \| \| domain_scope_gate \| 特定领域未选不可评估 | 需规校验 | — | 未覆盖 | req_only；本 endpoint 仅 scope_code/limit |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`rows`） |
| 未覆盖 | 5（含 `_empty` 1 + req_only 4） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000514～API-000518 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
