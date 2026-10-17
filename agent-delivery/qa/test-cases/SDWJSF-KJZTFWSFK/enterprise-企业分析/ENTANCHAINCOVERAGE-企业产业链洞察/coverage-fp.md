# 企业产业链洞察 · 功能点覆盖（entan.chain-coverage）

> catalog `entan.chain-coverage` · 50897 · path `/entan/chain-coverage`  
> **用例册**：`API-企业产业链洞察-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00231`～`00248`，共 **18** 条）  
> A 线真源：`fp-split-by-api-run/_catalog-snapshot.md`（3 endpoint、3 unavailable）；`_l6-to-catalog-map.yaml` **不扩六级**，无 `work/Lxx.md`  
> 功能点键：`catalog | endpoint_id | field_key | 功能点中文`（与 snapshot 契约行对齐）

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.chain-coverage.keypano | POST | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | API-00231～00236 | catalog `status=unavailable` |
| entan.chain-coverage.diversification | POST | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | API-00237～00242 | catalog `status=unavailable` |
| entan.chain-coverage.coverage-depth | POST | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | API-00243～00248 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| catalog \| entan.chain-coverage.keypano \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00233、00234、00235、00236 | 部分覆盖 | 缺省/空集合/非法/类型；live 合法集合成功校验待 endpoint available 后补 |
| catalog \| entan.chain-coverage.keypano \| coverage_rate \| 算法输出-coverage_rate全景覆盖率 | catalog coverage_rate | API-00231 | 契约占位 | unavailable，禁止 sample 覆盖率作通过条件 |
| catalog \| entan.chain-coverage.keypano \| _empty \| 重点企业全景图无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 codes 下 coverage_rate 必空」构造证据 |
| catalog \| entan.chain-coverage.keypano \| _fail \| 重点企业全景图计算失败 | 契约错误态 | API-00231、00233、00234、00235、00236 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| catalog \| entan.chain-coverage.diversification \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00238、00239、00240、00241、00242 | 部分覆盖 | 含单元素集合备选 CCD-06 |
| catalog \| entan.chain-coverage.diversification \| value \| 算法输出-value多元化指数 | catalog value | API-00237 | 契约占位 | 样例在 `value.value`，仅强制 responseFields `value` |
| catalog \| entan.chain-coverage.diversification \| _empty \| 多元化指数无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| catalog \| entan.chain-coverage.diversification \| _fail \| 多元化指数计算失败 | 契约错误态 | API-00237、00238、00239、00240、00241 | 已覆盖 | |
| catalog \| entan.chain-coverage.coverage-depth \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00244、00245、00246、00247、00248 | 部分覆盖 | 含双元素集合备选 CCV-06 |
| catalog \| entan.chain-coverage.coverage-depth \| value \| 算法输出-value领域覆盖深度 | catalog value | API-00243 | 契约占位 | unavailable |
| catalog \| entan.chain-coverage.coverage-depth \| _empty \| 领域覆盖深度无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| catalog \| entan.chain-coverage.coverage-depth \| _fail \| 领域覆盖深度计算失败 | 契约错误态 | API-00243、00244、00245、00246、00247 | 已覆盖 | |

---

## 3. A 线 / 需规说明

| 项 | 状态 | 说明 |
|----|------|------|
| 独立 `work/Lxx.md` by-api 表 | 无 | `_l6-to-catalog-map`：`entan.chain-coverage` 不扩六级 |
| 关键词抽取 / 领域映射（Q013） | 无独立 HTTP 行 | 语义在 `sampleResponse` hint，不发明 API 用例 |
| 产业链层级表源 | 无独立 endpoint | 由 `M_ENT_DOMAIN_COVERAGE_DEPTH` compute 承载 |
| 全页鉴权 | API-00232 | diversification / coverage-depth 备注复用 |

---

## 4. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（三 endpoint `_fail` 契约行） |
| 部分覆盖 | 3（三 endpoint `enterprise_codes`） |
| 契约占位 | 3（coverage_rate / value / value） |
| 未覆盖 | 3（`_empty` ×3） |

---

## 5. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 18 |
| 编号 | API-00231～API-00248 |
| catalog endpoint 数 | 3 |
| `_empty` 未覆盖 | 3 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
