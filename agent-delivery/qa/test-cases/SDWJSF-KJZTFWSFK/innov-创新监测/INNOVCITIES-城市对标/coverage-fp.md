# 城市对标 · 功能点覆盖（innov.cities）

> catalog `innov.cities` · 50897 · path `/innov/cities`  
> 用例册：`API-城市对标-用例.md`（API-00799～00818）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.cities`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.cities.rank | GET | /innov/v1/cities/rank | API-00799～00803 | catalog `status=running` · `runtime=java_api`；§0 **未试调** |
| innov.cities.compare | GET | /innov/v1/cities/compare | API-00804～00808 | 必填 `cityCodes`（CSV） |
| innov.cities.advice | GET | /innov/v1/cities/{cityCode}/advice | API-00809～00813 | path 必填 `cityCode` |
| innov.cities.method | GET | /innov/v1/cities/index-method | API-00814～00818 | 无查询参数 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.cities \| innov.cities.rank \| scope \| 算法输入-全球国内范围 | catalog scope | API-00799、00801、00802、00803 | 已覆盖 | global 主路径+非法/空+domestic 备选 |
| innov.cities \| innov.cities.rank \| list \| 算法输出-城市排名列表 | catalog list | API-00799、00803 | 已覆盖 | array 形态；禁止 sample 指数/排名数值 |
| innov.cities \| innov.cities.rank \| _empty \| 排行无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 scope 必空 list」证据 |
| innov.cities \| innov.cities.rank \| _fail \| 排行调用失败 | 契约错误态 | API-00800、00801、00802 | 已覆盖 | 鉴权+scope 单缺陷 |
| innov.cities \| innov.cities.compare \| cityCodes \| 算法输入-对标城市编码CSV | catalog cityCodes | API-00804、00806、00807、00808 | 已覆盖 | 合法 CSV+缺/空/非法 |
| innov.cities \| innov.cities.compare \| list \| 算法输出-对标城市列表 | catalog list | API-00804 | 已覆盖 | array 形态；样例 radar 非 responseFields |
| innov.cities \| innov.cities.compare \| _empty \| 对标无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 cityCodes 必空 list」证据 |
| innov.cities \| innov.cities.compare \| _fail \| 对标调用失败 | 契约错误态 | API-00805、00806、00807、00808 | 已覆盖 | 鉴权+cityCodes 失败语义 |
| innov.cities \| innov.cities.advice \| cityCode \| 算法输入-城市编码 | catalog cityCode | API-00809、00811、00813 | 已覆盖 | example+非法 id+依赖链 |
| innov.cities \| innov.cities.advice \| title \| 算法输出-建议标题 | catalog title | API-00809、00813 | 已覆盖 | string 形态 |
| innov.cities \| innov.cities.advice \| contentMd \| 算法输出-建议正文 | catalog contentMd | API-00809、00813 | 已覆盖 | string 形态 |
| innov.cities \| innov.cities.advice \| _empty \| 建议无正文空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 cityCode 必空正文」证据 |
| innov.cities \| innov.cities.advice \| _fail \| 建议调用失败 | 契约错误态 | API-00810、00811、00812 | 已覆盖 | 鉴权+非法/空 cityCode |
| innov.cities \| innov.cities.method \| weights \| 算法输出-四要素权重 | catalog weights | API-00814、00817、00818 | 已覆盖 | array 形态；禁止 sample 权重和为 1 |
| innov.cities \| innov.cities.method \| _empty \| 方法说明无数据空态 | 契约空结果 | — | 未覆盖 | 无参接口，无稳定必空构造 |
| innov.cities \| innov.cities.method \| _fail \| 方法接口调用失败 | 契约错误态 | API-00815、00816 | 已覆盖 | 鉴权+非法查询参数 |
| innov.cities \| \| M_INNOV_CITY_INDEX \| 城市创新指数 metric | catalog metricIds | API-00799、00803 | 部分覆盖 | 排行主路径/ domestic 备选挂 metric_id；不对指数分值断言 |
| innov.cities \| \| radar_viz_sample \| 对标雷达样例字段 | catalog viz radar | — | 未覆盖 | `radar` 不在 responseFields；归 UI/样例，非 REST 契约叶 |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵） |
|------|---------------------------|
| 已覆盖 | 12 |
| 部分覆盖 | 1（metric） |
| 未覆盖 | 5（`_empty`×4 + radar_viz_sample） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **20**（4 endpoint × 5） |
| 编号 | **API-00799**～**API-00818** |
| `_empty` 未覆盖 | **4** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 4 endpoint、`running`×4 |

---

## 5. 金样与烟测

| 项 | 编号 |
|----|------|
| 金样（全册信封） | API-00799 |
| 烟测建议 | API-00799、00804、00809、00814 |
