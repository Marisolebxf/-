# 算法库后端模型 · A 线功能点覆盖（policy.deep）

> **catalog_page_id**：`policy.deep` · path `#/policy/deep`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.deep`（原因：不扩六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **B 线用例**：`FUNC-算法库后端模型-用例.md`（第三轮 **FUNC-00739**～**FUNC-00745**）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.deep`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| policy.deep.models | GET | /policy/v1/policy/analysis/focus | FUNC-00739～00743 | unavailable |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。title「后端模型」的 sampleResponse（`rows` 及行内 `model`、`model_name`、`metric_id`、`index`）与 responseFields 的 `rows` 都挂在主流程上；与 sample 相反的传/不传挂备选；每个参数恰好 1 条非法反向。catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| policy.deep.models \| 后端模型 | FUNC-00739、00740、00741、00742、00743 | 无对应功能点 | 00739 主流程 sampleRequest（scope_code=440300、limit=50），断言 rows 及六行 model/model_name/metric_id/index；00740 省略 scope_code；00741 省略 limit；00742、00743 分别非法 scope_code、limit。文档标记未交付 |
| （页面清单） \| policy.deep \| 接口信息 / 算法测试 | FUNC-00744、00745 | 已覆盖 | 单接口页清单 2 条 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| title 数 | 1 |
| FUNC 用例数 | 7 |
| 主流程 | 1 |
| 备选-参数组合 | 2 |
| 反向 | 2 |
| 清单 | 2 |
| 编号 | FUNC-00739～00745 |
| A 线 Lxx | 无 |
| 旧 API 册 | API-01513～01517 作废，见 FUNC 册 §4 |
