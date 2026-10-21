# 企业创新能力评估 · 功能点覆盖（entan.innovation）

> catalog `entan.innovation` · path `/entan/innovation`  
> A 线：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.innovation`（与 L31 相邻但不扩六级）。不改 `work/`。  
> B 线用例：`FUNC-企业创新能力评估-用例.md`（第三轮 **FUNC-00320**～**00323**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | FUNC-00320、00321 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。`enterprise_codes` 与 sampleResponse / responseFields 字段都挂在同一接口的 2 条接口向用例上；另 2 条页面清单用例覆盖接口信息 / 算法测试 tab。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| entan.innovation.rank \| 创新能力指数（企业集合） | FUNC-00320、00321 | 无对应功能点 | 与 L31 相邻但不扩六级。00320 主流程全参；00321 缺 enterprise_codes。备注注明文档未交付 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00322、00323 | 无对应功能点 | 单接口页下拉 1 项与 catalog title 一致 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1（创新能力指数（企业集合）） |
| FUNC 用例数 | 4 |
| 主流程 | 1（FUNC-00320） |
| 备选-参数组合 | 0 |
| 反向 | 1（FUNC-00321） |
| 清单 | 2（FUNC-00322、00323） |
| 编号 | FUNC-00320～00323 |
| A 线 Lxx | 无 |
