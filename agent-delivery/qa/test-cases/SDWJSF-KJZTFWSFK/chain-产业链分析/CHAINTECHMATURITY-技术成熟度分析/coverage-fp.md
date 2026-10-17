# 技术成熟度分析 · 功能点覆盖（chain.tech-maturity）

> **catalog_page_id**：`chain.tech-maturity` · path `/chain/tech-maturity`  
> **用例册**：`API-技术成熟度分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00399`～`00403`，共 5 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.tech-maturity`  
> **A 线真源**：`fp-split-by-api-run/work/L*.md` **无六级对应**（`_l6-to-catalog-map.yaml`：`chain.tech-maturity` · 60 条无对应六级）

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | catalog status | 用例编号 |
|-------------|--------|------|----------------|----------|
| chain.tech-maturity.main | GET | /innov/v1/industry/{chainId}/tech-maturity | unavailable | 00399、00400、00401、00402、00403 |

---

## 2. 功能点 → 用例矩阵（B 线 catalog 契约 field · 待 A 线合表）

键：`产业链分析 | endpoint_id | field_key | 功能点（catalog / 契约）`  
**合表前状态**：各行 **待 A 线合表核对**；A 线 `work/Lxx.md` 落地后可将键前缀改为 `Lxx | …` 并回填规则来源。

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| 产业链分析 \| chain.tech-maturity.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | 00399、00401 | 已覆盖 · 待 A 线合表核对 | 合法 example 契约请求 + 非法 id |
| 产业链分析 \| chain.tech-maturity.main \| tech_maturity_score \| 算法输出-tech_maturity_score技术成熟度评分 | catalog responseFields | 00399、00402 | 契约占位 · 待 A 线合表核对 | endpoint unavailable；不得用 sample 评分 70 作通过条件；接通后改主流程断言 |
| 产业链分析 \| chain.tech-maturity.main \| trend \| 算法输出-trend年度公开专利量 | catalog responseFields | 00399、00403 | 契约占位 · 待 A 线合表核对 | 同上；空数组与 _fail 执行期区分 |
| 产业链分析 \| chain.tech-maturity.main \| _empty \| 技术成熟度分析无数据空态 | 契约空结果 | — | **未覆盖** · 待 A 线合表核对 | 无稳定可构造「合法 chainId 且无专利趋势可算」条件；§0 未试调，禁止编造必空参数 |
| 产业链分析 \| chain.tech-maturity.main \| _fail \| 技术成熟度分析查询失败 | 契约错误态 | 00401 | 已覆盖 · 待 A 线合表核对 | 非法 chainId；鉴权失败见 00400 |

> **样例字段说明**：catalog `sampleResponse` 另有 `stage`（阶段文案），未列入 `responseFields`；B 线不设单独 field 行，接通后若 A 线合表纳入再补矩阵。

---

## 3. A 线 work 检索说明

| 项 | 结果 |
|----|------|
| `_l6-to-catalog-map.yaml` | `chain.tech-maturity` · **60 条无对应六级** |
| `work/*.md` 检索 `chain.tech-maturity` / `tech-maturity` | **待 A 线合表**（本子任务未展开 60 条 by-api 行） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 1 endpoint、`unavailable`×1 |
| B 线待 A 线合表 | 矩阵状态含 **待 A 线合表核对**；本页 endpoint 用例仍有效 |

---

## 4. 计数

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 用例编号起止 | API-00399～API-00403 |
| catalog endpoint 数 | 1 |
| 契约 field 键（含 _empty/_fail） | 5 |
| 已覆盖（含契约占位 / _fail） | 4 键 |
| 未覆盖 | 1（_empty） |
| 异常-鉴权 | API-00400（endpoint 级，不单独挂 field 行） |
| `_empty` 未覆盖 | 1 行（见矩阵） |
| 试调 | **未试调**（§0）；父控禁止 curl |
| 产物路径 | `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/chain-产业链分析/CHAINTECHMATURITY-技术成熟度分析/` |
| code-registry | **未回写**（父控约束） |
