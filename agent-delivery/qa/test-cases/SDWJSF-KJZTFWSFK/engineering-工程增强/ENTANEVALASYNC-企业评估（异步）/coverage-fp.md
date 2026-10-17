# 企业评估（异步） · 功能点覆盖（entan.eval-async）

> catalog `entan.eval-async` · 50897 · path `/entan/eval-async`  
> 用例册：`API-企业评估（异步）-用例.md`（API-00157～00161）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `entan.eval-async`（`_l6-to-catalog-map.yaml`：工程增强，非 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| entan.eval-async.mock | POST | （空） | API-00157～00161 | catalog `status=unavailable` · `runtime=local_mock` |

---

## 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| 工程增强 \| entan.eval-async.mock \| mode \| 算法输入-mode评估类型 | catalog mode | API-00157、00159、00160、00161 | 部分覆盖 | unavailable 占位 + 缺省/枚举外/空串；合法三枚举 live 主路径待 path 发布且 available 后补 |
| 工程增强 \| entan.eval-async.mock \| task_id \| 算法输出-task_id任务标识 | catalog task_id | API-00157 | 契约占位 | 禁止 sample 各 mode 下 task_id 与评分示例作通过条件 |
| 工程增强 \| entan.eval-async.mock \| _empty \| 异步评估无任务空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 mode 下无 task」构造证据 |
| 工程增强 \| entan.eval-async.mock \| _fail \| 异步评估契约调用失败 | 契约错误态 | API-00157、00159、00160、00161 | 已覆盖 | 含 catalog 不可用、path 空与入参失败哨兵 |

---

## A 线 work 检索说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `entan.eval-async` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 1 endpoint、`unavailable`×1、`local_mock`×1 |
| B 线待 A 线合表 | 状态 **待 A 线合表核对**；本页 endpoint 用例仍有效 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| API 用例数 | 5 |
| 契约 field 键（含 _empty/_fail） | 4 |
| 已覆盖（含契约占位 / _fail） | 3 键（mode、task_id、_fail） |
| 未覆盖 | 1（_empty） |
| 异常-鉴权 | API-00158（endpoint 级，不单独挂 field 行） |
