# 文本解析 · 智能摘要 · 功能点覆盖（policy.parse）

> catalog `policy.parse` · 50897 · path `/policy/parse`  
> 用例 `API-文本解析·智能摘要-用例.md`  
> A 线真源：无独立 `work/Lxx.md`（`_l6-to-catalog-map.yaml`：`policy.parse` 不扩六级）  
> 功能点键：`catalog | policy.parse.main | field_key | 功能点中文`（待 A 线合表后可改前缀）  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.parse.main | GET | /policy/v1/policy/text/parse | API-000499～API-000503 | catalog `status=unavailable`；与 `policy.text` 页共用 path 但 catalog 页独立 |

---

## 2. 功能点 → 用例（catalog 契约行）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| catalog \| policy.parse.main \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | API-000499、API-000501 | 部分覆盖 | PAR-01 列表模式不传 policy_id；非法 id 见 PAR-02 / API-000501；单政策 PAR-04 待 available 后补 |
| catalog \| policy.parse.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000499、API-000502 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| catalog \| policy.parse.main \| summary \| 算法输出-summary摘要 | catalog responseFields | API-000503 | 契约占位 | unavailable，禁止 sample 摘要文案作通过条件 |
| catalog \| policy.parse.main \| _empty \| 文本解析无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| catalog \| policy.parse.main \| _fail \| 文本解析查询失败 | 契约错误态 | API-000499、API-000500、API-000501、API-000502 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |

---

## 3. A 线 req_only / 未扩六级说明

| 项 | 状态 | 说明 |
|----|------|------|
| 独立 Lxx by-api 表 | 无 | `_l6-to-catalog-map` 未为 `policy.parse` 生成 work 行 |
| D1 结构化要素（条款/对象/条件等） | 无对应 HTTP 顶层字段 | catalog 摘要写「D1 结构化要素 + 摘要」；契约仅列 `summary`，不发明拆分 endpoint |
| DS-11-012 智能摘要与结论推送 | 读面承接 | 关联 metric `M_POLICY_DS_11_POLICY_EVAL_012`；无独立 API 字段，待 A 线扩表登记 req_only |
| `policy.text` 工程合页 | 路径去重 | 同 path `/policy/v1/policy/text/parse` 亦挂在 `policy.text`；B 线按 **本 catalog 页** 验收，不混写 `policy.text` 用例 |

---

## 4. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（`limit`、`_fail`） |
| 部分覆盖 | 1（`policy_id`） |
| 契约占位 | 1（`summary`） |
| 未覆盖 | 5（含 `_empty` 1 + req_only 口径 4 类合并登记） |

---

## 5. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000499～API-000503 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
