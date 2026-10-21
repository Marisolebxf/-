# 政策文本处理 · 功能点覆盖（policy.text）

> **catalog_page_id**：`policy.text` · path `#/policy/text`（侧栏在「工程增强」）  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.text`（原因：parse/match/simulate 合页；60 条无独立六级）。不改 `work/`。  
> **B 线用例**：`FUNC-政策文本处理-用例.md`（第三轮 **FUNC-00660**～**FUNC-00680**，共 21 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.text`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.text.parse | GET | /policy/v1/policy/text/parse | FUNC-00660～00664 | unavailable |
| policy.text.match | GET | /policy/v1/policy/match | FUNC-00665～00671 | unavailable |
| policy.text.simulate | GET | /policy/v1/policy/simulate | FUNC-00672～00678 | unavailable |
| （页面清单） | — | — | FUNC-00679、00680 | — |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行。每个 title 的 sampleResponse 与 responseFields 挂在该接口主流程；可选参数与 sample 相反的传/不传挂备选；每个参数恰好 1 条反向。三接口 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.text.parse \| 文本解析 | FUNC-00660～00664 | 已覆盖 | 00660 主流程 sampleRequest（limit=20，不传 policy_id）；00661 传入 policy_id；00662 省略 limit；00663～00664 非法 policy_id、limit |
| （无 Lxx） \| policy.text.match \| 政策匹配 | FUNC-00665～00671 | 已覆盖 | 00665 主流程 sampleRequest；00666～00668 备选；00669～00671 非法 subject_id、subject_type、limit |
| （无 Lxx） \| policy.text.simulate \| 效果推演 | FUNC-00672～00678 | 已覆盖 | 00672 主流程 sampleRequest；00673～00675 备选；00676～00678 非法 scope_code、scenario_id、limit |
| （页面清单） \| policy.text \| 接口信息 / 算法测试 | FUNC-00679、00680 | 已覆盖 | 3 接口页清单 2 条（含切换步骤） |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 21 |
| 主流程 | 3（FUNC-00660、00665、00672） |
| 备选-参数组合 | 8（FUNC-00661、00662、00666～00668、00673～00675） |
| 反向 | 8（FUNC-00663、00664、00669～00671、00676～00678） |
| 清单 | 2（FUNC-00679、00680） |
| 编号 | FUNC-00660～00680 连续 |
| 旧 API 册 | `engineering-工程增强/POLICYTEXT-文本解析·匹配·推演/API-文本解析·匹配·推演-用例.md`（API-01446～01464 仅作对照，B 线以本 FUNC 册为准） |
