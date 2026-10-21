# 产业战略重要性分析 · 功能点覆盖（chain.strategic-importance）

> catalog `chain.strategic-importance` · path `/chain/strategic-importance`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `chain.strategic-importance`（60 条无对应六级）。不改 `work/`。  
> B 线用例：`FUNC-产业战略重要性分析-用例.md`（第三轮 **FUNC-00527**～**00530**；历史 API-01312～01313 作废）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.strategic-importance.main | GET | /innov/v1/industry/{chainId}/strategic-importance | FUNC-00527、00528 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`chainId` 与 sampleResponse 的 `rows` 及行内 `node_name`、`position`、`importance_score`（responseFields 仅 `rows`）都挂在同一接口的 2 条用例上。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| chain.strategic-importance.main \| 战略重要性 | API-01312、01313 | 无对应功能点 | 01312 主流程 path chainId=INB170101，按 sampleResponse 断言 rows 及行内字段；01313 缺 chainId。备注注明文档未交付 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（战略重要性） |
| API 用例数 | 2 |
| 主流程 | 1（API-01312） |
| 反向 | 1（API-01313） |
| 编号 | API-01312～01313（连续用满） |
| A 线 Lxx | 无 |
| 作废旧号 | API-000404～000408 |
