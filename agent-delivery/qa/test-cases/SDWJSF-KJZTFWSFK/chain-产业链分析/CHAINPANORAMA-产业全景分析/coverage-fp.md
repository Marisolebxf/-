# 产业全景分析 · 功能点覆盖（chain.panorama / L05+L06+L14）

> catalog `chain.panorama` · path `#/chain/panorama`  
> A 线真源：`fp-split-by-api-run/work/L05.md`、`L06.md`、`L14.md`  
> B 线用例：`FUNC-产业全景分析-用例.md`（第三轮 **FUNC-00407**～**00427**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | FUNC-00407～00421 | running |
| chain.panorama.main | GET | /chain/v1/chain/{chainId}/panorama | FUNC-00422、00423 | running |
| chain.panorama.m_chain_deep_117_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_117_1/compute | FUNC-00424、00425 | available |
| （页面清单） | — | — | FUNC-00426、00427 | — |

---

## 功能点 → 用例矩阵（挂 L05 / L14）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L05 \| chain.panorama.ops \| op_id \| 算法输入-op_id | FUNC-00407、00414 | 已覆盖 | sampleRequest + 缺 op_id |
| L05 \| chain.panorama.ops \| scope \| 算法输入-scope | FUNC-00407、00415 | 已覆盖 | sampleRequest + 缺 scope |
| L05 \| chain.panorama.ops \| id \| 算法输入-id | FUNC-00407、00408、00416 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| filter \| 算法输入-filter | FUNC-00409、00417 | 已覆盖 | 备选传入 + 非法 |
| L05 \| chain.panorama.ops \| mode \| 算法输入-mode | FUNC-00407、00410、00418 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| dry_run \| 算法输入-dry_run | FUNC-00407、00411、00419 | 已覆盖 | 传入 + 省略 + 非法 |
| L05 \| chain.panorama.ops \| relation_whitelist \| 算法输入-relation_whitelist | FUNC-00412、00420 | 已覆盖 | 备选传入 + 非法 |
| L05 \| chain.panorama.ops \| dest_types \| 算法输入-dest_types | FUNC-00413、00421 | 已覆盖 | 备选传入 + 非法 |
| L05 \| chain.panorama.ops \| written_nodes 等输出字段 | FUNC-00407 | 已覆盖 | 主流程逐字段断言 |
| L05 \| chain.panorama.ops \| _empty \| 查询无数据空态 | FUNC-00407 | 已覆盖 | sampleResponse 空数组写在主流程预期 |
| L05 \| chain.panorama.ops \| _fail \| 调用失败 | FUNC-00414～00421 | 已覆盖 | 8 条入参反向 |
| L14 \| chain.panorama.main \| chainId \| 算法输入-chainId | FUNC-00422、00423 | 已覆盖 | 合法 + 缺 chainId |
| L14 \| chain.panorama.main \| nodes / edges \| 算法输出 | FUNC-00422 | 已覆盖 | 主流程逐字段断言 |
| L14 \| chain.panorama.main \| _empty \| 查询无数据空态 | FUNC-00422 | 已覆盖 | 空 nodes/edges 写在主流程预期 |
| L14 \| chain.panorama.main \| _fail \| 调用失败 | FUNC-00423 | 已覆盖 | 缺 chainId |
| L14 \| chain.panorama.m_chain_deep_117_1 \| chainId \| 算法输入 | FUNC-00424、00425 | 无对应功能点 | L14 未给该 endpoint 挂 field 行；按 catalog 写 2 条接口向用例 |
| （页面清单） \| 接口信息 / 算法测试 | FUNC-00426、00427 | 无对应功能点 | 3 接口下拉与 method/path 刷新 |

L05 `entity_recog_pipeline`、L06 关系流水线、L14 需规-only 行等 **7+** 条仍记 **无对应功能点**，不单独开用例。

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 3 |
| title 数 | 3 |
| FUNC 用例数 | 21 |
| 主流程 | 3（00407、00422、00424） |
| 备选-参数组合 | 6（00408～00413） |
| 反向 | 10（00414～00421、00423、00425） |
| 清单 | 2（00426、00427） |
| 编号 | FUNC-00407～00427 |
| A 线 Lxx | L05（ops）、L14（main）；L06 与 ops 共挂 weak |
