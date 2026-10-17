# 文本解析 · 匹配 · 推演 · 功能点覆盖（policy.text）

> catalog `policy.text` · 50897 · path `/policy/text`  
> 用例册：`API-文本解析·匹配·推演-用例.md`（API-000484～000498）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `policy.text`（`_l6-to-catalog-map.yaml`：parse/match/simulate 合页）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| policy.text.parse | GET | /policy/v1/policy/text/parse | API-000484～000488 | catalog `status=unavailable`；§0 **未试调** |
| policy.text.match | GET | /policy/v1/policy/match | API-000489～000493 | catalog `status=unavailable` |
| policy.text.simulate | GET | /policy/v1/policy/simulate | API-000494～000498 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| 工程增强 \| policy.text.parse \| policy_id \| 算法输入-policy_id政策标识 | catalog policy_id | API-000484、000486 | 部分覆盖 | 列表主路径 + 非法 ID 哨兵 |
| 工程增强 \| policy.text.parse \| limit \| 算法输入-limit条数 | catalog limit | API-000484、000487 | 部分覆盖 | 主路径 limit=20 + 非正整数失败 |
| 工程增强 \| policy.text.parse \| title \| 算法输出-title政策标题 | catalog title | API-000484、000488 | 契约占位 | unavailable，禁止 sample 标题文案作通过条件 |
| 工程增强 \| policy.text.parse \| _empty \| 解析列表无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法入参必空」试调证据 |
| 工程增强 \| policy.text.parse \| _fail \| 文本解析查询失败 | 契约错误态 | API-000484、000485、000486、000487 | 已覆盖 | 含不可用、鉴权与入参失败 |
| 工程增强 \| policy.text.match \| subject_id \| 算法输入-subject_id主体标识 | catalog subject_id | API-000489 | 部分覆盖 | 主路径未传 subject_id（列表态）；单 ID 成功路径待 available 后补 |
| 工程增强 \| policy.text.match \| subject_type \| 算法输入-subject_type主体类型 | catalog subject_type | API-000489、000491 | 部分覆盖 | enterprise 主路径 + 枚举外失败 |
| 工程增强 \| policy.text.match \| limit \| 算法输入-limit条数 | catalog limit | API-000489、000492 | 部分覆盖 | 主路径 + 非正整数失败 |
| 工程增强 \| policy.text.match \| match_score \| 算法输出-match_score匹配度 | catalog match_score | API-000489、000493 | 契约占位 | 禁止 sample 0.86 等作通过条件 |
| 工程增强 \| policy.text.match \| _empty \| 匹配结果无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定空排行构造 |
| 工程增强 \| policy.text.match \| _fail \| 政策匹配查询失败 | 契约错误态 | API-000489、000490、000491、000492 | 已覆盖 | 含不可用、鉴权与入参失败 |
| 工程增强 \| policy.text.simulate \| scope_code \| 算法输入-scope_code省级编码 | catalog scope_code | API-000494、000496 | 部分覆盖 | SIM-01 含 440300；非法 scenario 组合仍带 scope |
| 工程增强 \| policy.text.simulate \| scenario_id \| 算法输入-scenario_id推演情景 | catalog scenario_id | API-000494、000496 | 部分覆盖 | 主路径未传情景 + 枚举外失败 |
| 工程增强 \| policy.text.simulate \| limit \| 算法输入-limit条数 | catalog limit | API-000494、000497 | 部分覆盖 | 主路径 + 非正整数失败 |
| 工程增强 \| policy.text.simulate \| simulated_value \| 算法输出-simulated_value推演值 | catalog simulated_value | API-000494、000498 | 契约占位 | 禁止 sample 推演值作通过条件 |
| 工程增强 \| policy.text.simulate \| _empty \| 推演结果无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定空推演构造 |
| 工程增强 \| policy.text.simulate \| _fail \| 效果推演查询失败 | 契约错误态 | API-000494、000495、000496、000497 | 已覆盖 | 含不可用、鉴权与入参失败 |

---

## 3. A 线 work 检索说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `policy.text` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 3 endpoint、`unavailable`×3 |
| B 线待 A 线合表 | 状态可先 **待 A 线合表核对**；本页 endpoint 用例仍有效 |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | **3** |
| API 用例数 | **15** |
| 编号闭区间 | API-000484～000498 |
| 契约 field 键（含 _empty/_fail，按 endpoint） | parse 5 + match 6 + simulate 6 = **17** 行 |
| `_empty` 未覆盖 | **3**（每 endpoint 1） |
| 异常-鉴权 | API-000485、000490、000495 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
