# 效果推演 · 实施路径 · 功能点覆盖（policy.simulate）

> catalog `policy.simulate` · 50897 · path `/policy/simulate`  
> 用例 `API-效果推演·实施路径-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `policy.simulate.main` 入参/出参及契约哨兵为准  
> 功能点键：`policy.simulate | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.simulate.main | GET | /policy/v1/policy/simulate | API-000509～API-000513 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| policy.simulate \| policy.simulate.main \| scope_code \| 算法输入-scope_code省级范围编码 | catalog scope_code | API-000509 | 部分覆盖 | SIM-01 不传 scope_code；SIM-04 无独立用例 |
| policy.simulate \| policy.simulate.main \| scenario_id \| 算法输入-scenario_id推演情景 | catalog scenario_id | API-000509、API-000511 | 已覆盖 | 主路径默认全情景 + 枚举外失败 |
| policy.simulate \| policy.simulate.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000509、API-000512 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| policy.simulate \| policy.simulate.main \| simulated_value \| 算法输出-simulated_value推演值 | catalog simulated_value | API-000509、API-000513 | 契约占位 | unavailable，禁止 sample 推演值作通过条件 |
| policy.simulate \| policy.simulate.main \| _empty \| 效果推演无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| policy.simulate \| policy.simulate.main \| _fail \| 效果推演查询失败 | 契约错误态 | API-000509、API-000510、API-000511、API-000512 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| policy.simulate \| \| implementation_path \| 实施路径读面与阶段清单 | 需规（DS-11-015 / 展示 DS-12） | — | 未覆盖 | req_only；catalog 本 endpoint 未声明实施路径字段 |
| policy.simulate \| \| curve_time_series \| 推演曲线时间序列 | 需规情景弹性曲线 | — | 未覆盖 | req_only；样例为表形态，曲线字段待契约登记 |
| policy.simulate \| policy.text 工程合页 | 路径去重 | — | 说明 | 同 path `/policy/v1/policy/simulate` 亦挂在 `policy.text` 合页；B 线按 **本 catalog 页** 验收，不混写 `policy.text` 用例编号 |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`scenario_id`、`limit`、`_fail`） |
| 部分覆盖 | 1（`scope_code`） |
| 契约占位 | 1（`simulated_value`） |
| 未覆盖 | 3（含 `_empty` 1 + req_only 2） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000509～API-000513 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
