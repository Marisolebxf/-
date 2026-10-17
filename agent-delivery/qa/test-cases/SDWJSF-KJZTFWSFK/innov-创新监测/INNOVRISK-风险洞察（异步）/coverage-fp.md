# coverage-fp · innov.risk（风险洞察（异步））

> **catalog_page_id**：`innov.risk`  
> **契约**：`lumen-ui-algo-apiview/src/catalog/innov.json`  
> **A 线真源**：`fp-split-by-api-run/_l6-to-catalog-map.yaml`（`innov.*` 非 60 六级）；`fp-split-by-api-run/_catalog-snapshot.md` 登记 2 endpoint、`unavailable`×2、`local_mock`×2  
> **用例册**：`API-风险洞察（异步）-用例.md`（API-00734～00743）  
> **§0**：**未试调**

## 1. endpoint 覆盖

| endpoint_id | METHOD | path | 用例编号 | 说明 |
|-------------|--------|------|----------|------|
| innov.risk.supply | POST | （空） | API-00734～00738 | catalog `unavailable`；`sub_type=supply_chain`；出参契约 `key_nodes`、`break_risks` |
| innov.risk.pain | POST | （空） | API-00739～00743 | catalog `unavailable`；`sub_type=pain_points`；出参契约 `issues` |

## 2. 矩阵键（catalog 字段 / 哨兵）

| 矩阵键 | 语义 | 对应用例 | 覆盖 | 备注 |
|--------|------|----------|------|------|
| innov.risk.supply \| sub_type \| 算法输入-子类型 | catalog sub_type | API-00734、00736、00737、00738 | 已覆盖 | 主路径占位 + 缺省 + 跨 endpoint 枚举 + 空串 |
| innov.risk.supply \| key_nodes \| 算法输出-关键节点 | catalog key_nodes | — | 未覆盖 | unavailable 金样批不写 live 数值语义；待 endpoint available 后补字段形态条 |
| innov.risk.supply \| break_risks \| 算法输出-断链风险 | catalog break_risks | — | 未覆盖 | 同上 |
| innov.risk.supply \| _empty \| 供应链风险无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「sub_type=supply_chain 必空」试调证据 |
| innov.risk.supply \| _fail \| 供应链风险契约失败 | 契约错误态 | API-00734、00735、00736、00737、00738 | 已覆盖 | 含 unavailable、鉴权与 sub_type 单缺陷 |
| innov.risk.pain \| sub_type \| 算法输入-子类型 | catalog sub_type | API-00739、00741、00742、00743 | 已覆盖 | 主路径占位 + 缺省 + 跨 endpoint 枚举 + 空串 |
| innov.risk.pain \| issues \| 算法输出-共性问题 | catalog issues | — | 未覆盖 | unavailable 金样批不写 live 数值语义 |
| innov.risk.pain \| _empty \| 痛难点无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「sub_type=pain_points 必空」试调证据 |
| innov.risk.pain \| _fail \| 痛难点契约失败 | 契约错误态 | API-00739、00740、00741、00742、00743 | 已覆盖 | 含 unavailable、鉴权与 sub_type 单缺陷 |

## 3. 金样与烟测

| 项 | 编号 |
|----|------|
| 金样（供应链） | API-00734 |
| 金样（痛难点） | API-00739 |
| 烟测建议 | 跑全部金样（00734、00739） |

## 4. 统计摘要

| 指标 | 值 |
|------|-----|
| endpoint 数 | 2 |
| API 用例数 | 10 |
| `_fail` 行 | 2 / 2 已覆盖 |
| `_empty` 行 | 2 / 2 未覆盖 |
| responseFields 形态条 | 0（待 live 升档） |
