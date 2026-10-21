# 匹配推送 · A 线功能点覆盖（policy.match）

> **catalog_page_id**：`policy.match` · path `#/policy/match`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.match`（原因：不扩六级）。不改 `work/`。  
> **B 线用例**：`FUNC-政策匹配推送-用例.md`（第三轮 **FUNC-00693**～**FUNC-00708**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.match`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.match.main | GET | /policy/v1/policy/match | FUNC-00693～00699 | unavailable |
| policy.match.m_policy_match | POST | /policy/v1/polan/metric/M_POLICY_MATCH/compute | FUNC-00700～00706 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.match.main \| 政策匹配 | FUNC-00693、00694、00695、00696、00697、00698、00699 | 无对应功能点 | 00693 主流程 sampleRequest（subject_type=enterprise、limit=20、不传 subject_id），断言 data 元素 rank_no、subject_name、policy_title、match_score、metric_id；00694 传入 subject_id；00695 省略 subject_type；00696 省略 limit；00697～00699 分别非法 subject_id、subject_type、limit。文档标记未交付 |
| （无 Lxx） \| policy.match.m_policy_match \| 政策匹配推送 | FUNC-00700、00701、00702、00703、00704、00705、00706 | 无对应功能点 | 00700 主流程 sampleRequest，断言 metric_id、hint 与 responseFields 的 match_score；00701 传入 subject_id；00702 省略 subject_type；00703 省略 limit；00704～00706 分别非法 subject_id、subject_type、limit |
| （页面清单） \| policy.match \| 接口信息 / 算法测试 | FUNC-00707、00708 | 已覆盖 | 双接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 16 |
| 主流程 | 2 |
| 备选-参数组合 | 6 |
| 反向 | 6 |
| 清单 | 2 |
| 编号 | FUNC-00693～00708 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01475～01488 作废，见 FUNC 册 §4 |
