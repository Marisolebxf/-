# 文本解析 · 智能摘要 · A 线功能点覆盖（policy.parse）

> **catalog_page_id**：`policy.parse` · path `#/policy/parse`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.parse`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **B 线用例**：`FUNC-文本解析·智能摘要-用例.md`（第三轮 **FUNC-00681**～**FUNC-00692**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.parse`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.parse.main | GET | /policy/v1/policy/text/parse | FUNC-00681～00685 | unavailable |
| policy.parse.m_policy_text_parse | POST | /policy/v1/polan/metric/M_POLICY_TEXT_PARSE/compute | FUNC-00686～00690 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.parse.main \| 文本解析 | FUNC-00681、00682、00683、00684、00685 | 无对应功能点 | 00681 主流程 sampleRequest（不传 policy_id、limit=20），断言 policy_id、title、summary、metric_id；00682 传入 policy_id；00683 省略 limit；00684 非法 policy_id；00685 非法 limit。文档标记未交付 |
| （无 Lxx） \| policy.parse.m_policy_text_parse \| 政策文本解析 | FUNC-00686、00687、00688、00689、00690 | 无对应功能点 | 00686 主流程 sampleRequest（不传 policy_id、limit=20），断言 metric_id、hint 及 responseFields 的 summary；00687 传入 policy_id；00688 省略 limit；00689 非法 policy_id；00690 非法 limit |
| （页面清单） \| policy.parse \| 接口信息 / 算法测试 | FUNC-00691、00692 | 已覆盖 | 双接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 12 |
| 主流程 | 2 |
| 备选-参数组合 | 4 |
| 反向 | 4 |
| 清单 | 2 |
| 编号 | FUNC-00681～00692 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01465～01474 作废，见 FUNC 册 §4 |
