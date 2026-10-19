# 企业评估（异步） · 功能点覆盖（entan.eval-async）

> catalog `entan.eval-async` · path `/entan/eval-async`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.eval-async`（工程增强，非 60 六级）。不改 `work/`。  
> B 线用例：`API-企业评估（异步）-用例.md`（第二轮 **API-01139**～**01140**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.eval-async.mock | POST | （空） | API-01139～01140 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`mode` 与 sampleResponse 内 technology / business / competitiveness 嵌套字段及 responseFields 的 `task_id` 都挂在同一接口的 2 条用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.eval-async.mock \| 异步评估契约 | API-01139～01140 | 无对应功能点 | 工程增强页。01139 主流程 mode=technology，预期按 sampleResponse 逐字段（含嵌套与 task_id）；01140 缺 mode，预期 message 或 msg 指出缺少 mode。path 以 catalog 原文为空。备注注明文档未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（异步评估契约） |
| API 用例数 | 2 |
| 主流程 | 1（API-01139） |
| 反向 | 1（API-01140） |
| 编号 | API-01139～01140 |
| A 线 Lxx | 无 |
