# 风险评分 · 功能点覆盖（entan.risk）

> catalog `entan.risk` · 50897 · path `/entan/risk`  
> 用例册：`API-风险评分-用例.md`（API-00152～00156）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `entan.risk`（`_l6-to-catalog-map.yaml`：工程增强，非 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| entan.risk.list | GET | /entan/v1/risk | API-00152～00156 | catalog `status=unavailable` |

---

## 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| 工程增强 \| entan.risk.list \| level \| 算法输入-level风险等级 | catalog level | API-00152、00154 | 部分覆盖 | unavailable 占位 + 枚举外 level；合法「高/中/低」主路径待 endpoint available 后补 |
| 工程增强 \| entan.risk.list \| limit \| 算法输入-limit返回数量 | catalog limit | API-00152、00155、00156 | 部分覆盖 | 非法类型与负值哨兵；合法 limit 成功校验待 available 后补 |
| 工程增强 \| entan.risk.list \| rows \| 算法输出-rows风险列表 | catalog rows | API-00152 | 契约占位 | 禁止 sample risk_score 作通过条件 |
| 工程增强 \| entan.risk.list \| _empty \| 风险列表无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法筛选下 rows 必空」构造证据 |
| 工程增强 \| entan.risk.list \| _fail \| 风险列表查询失败 | 契约错误态 | API-00152、00154、00155、00156 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |

---

## A 线 work 检索说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `entan.risk` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 1 endpoint、`unavailable`×1 |
| B 线待 A 线合表 | 状态可先 **待 A 线合表核对**；本页 endpoint 用例仍有效 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| API 用例数 | 5 |
| 契约 field 键（含 _empty/_fail） | 5 |
| 已覆盖（含契约占位 / _fail） | 4 键（level、limit、rows、_fail） |
| 未覆盖 | 1（_empty） |
| 异常-鉴权 | API-00153（endpoint 级，不单独挂 field 行） |
