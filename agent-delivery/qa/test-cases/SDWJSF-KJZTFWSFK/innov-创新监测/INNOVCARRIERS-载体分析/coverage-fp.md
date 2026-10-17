# 载体分析 · 功能点覆盖（innov.carriers）

> catalog `innov.carriers` · 50897 · path `/innov/carriers`  
> 用例册：`API-载体分析-用例.md`（API-00769～00783）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.carriers`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.carriers.rank | GET | /innov/v1/carriers/rank | API-00769～00773 | catalog `status=running` · `runtime=java_api`；§0 **未试调** |
| innov.carriers.detail | GET | /innov/v1/carriers/{carrierId} | API-00774～00778 | path 必填 `carrierId` |
| innov.carriers.method | GET | /innov/v1/carriers/index-method | API-00779～00783 | 无查询参数 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.carriers \| innov.carriers.rank \| pageNum \| 算法输入-页码 | catalog pageNum | API-00769、00772、00773 | 已覆盖 | 主路径+非法类型+省略可选 |
| innov.carriers \| innov.carriers.rank \| pageSize \| 算法输入-页大小 | catalog pageSize | API-00769、00771、00773 | 已覆盖 | 主路径+越界+省略可选 |
| innov.carriers \| innov.carriers.rank \| list \| 算法输出-排行列表 | catalog list | API-00769、00773 | 已覆盖 | array 形态；禁止 sample 指数/排名数值 |
| innov.carriers \| innov.carriers.rank \| _empty \| 排行无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法分页必空 list」证据 |
| innov.carriers \| innov.carriers.rank \| _fail \| 排行调用失败 | 契约错误态 | API-00770、00771、00772 | 已覆盖 | 鉴权+pageSize/pageNum 单缺陷 |
| innov.carriers \| innov.carriers.detail \| carrierId \| 算法输入-载体 ID | catalog carrierId | API-00774、00776、00778 | 已覆盖 | 合法 example+非法 id+依赖链备注 |
| innov.carriers \| innov.carriers.detail \| info \| 算法输出-基本信息 | catalog info | API-00774、00778 | 已覆盖 | object 形态 |
| innov.carriers \| innov.carriers.detail \| trend \| 算法输出-多期指数 | catalog trend | API-00774、00778 | 已覆盖 | array 形态 |
| innov.carriers \| innov.carriers.detail \| _empty \| 详情无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 carrierId 必空」证据 |
| innov.carriers \| innov.carriers.detail \| _fail \| 详情调用失败 | 契约错误态 | API-00775、00776 | 已覆盖 | 鉴权+非法 carrierId |
| innov.carriers \| innov.carriers.method \| methodDesc \| 算法输出-方法说明 | catalog methodDesc | API-00779、00782 | 已覆盖 | string 形态 |
| innov.carriers \| innov.carriers.method \| weights \| 算法输出-权重列表 | catalog weights | API-00779、00782、00783 | 已覆盖 | array 形态；禁止 sample 权重和为 1 |
| innov.carriers \| innov.carriers.method \| _empty \| 方法说明无数据空态 | 契约空结果 | — | 未覆盖 | 无参接口，无稳定必空构造 |
| innov.carriers \| innov.carriers.method \| _fail \| 方法接口调用失败 | 契约错误态 | API-00780、00781 | 已覆盖 | 鉴权+非法查询参数 |
| innov.carriers \| \| carrier_type_enum \| 载体类型 university/research/incubator | catalog 页 summary | — | 未覆盖 | 类型枚举在 list 元素字段，无单独 REST 入参；待 live 后从 list 元素抽检 |
| innov.carriers \| \| M_INNOV_CARRIER_INDEX \| 载体指数 metric | catalog metricIds | API-00769 | 部分覆盖 | 仅排行主路径挂 metric_id 列；不对指数分值断言 |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵） |
|------|---------------------------|
| 已覆盖 | 10 |
| 部分覆盖 | 1（metric） |
| 未覆盖 | 4（`_empty`×3 + carrier_type_enum） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **15**（3 endpoint × 5） |
| 编号 | **API-00769**～**API-00783** |
| `_empty` 未覆盖 | **3** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 3 endpoint、`running`×3 |

---

## 5. 金样与烟测

| 项 | 编号 |
|----|------|
| 金样（全册信封） | API-00769 |
| 烟测建议 | API-00769、00774、00779 |
