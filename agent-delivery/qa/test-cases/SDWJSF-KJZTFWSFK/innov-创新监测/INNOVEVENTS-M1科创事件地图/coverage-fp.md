# M1 科创事件地图 · 功能点覆盖（innov.events）

> catalog `innov.events` · 50897 · path `/innov/events`  
> 用例册：`API-科创事件地图-用例.md`（API-00859～00888）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.events`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.events.list | GET | /innov/v1/events | API-00859～00863 | 无 `mode` 或 `mode`≠geo；catalog `status=running`；§0 **未试调** |
| innov.events.geo | GET | /innov/v1/events | API-00864～00868 | 必填 `mode=geo`；与 list **同 path**，验收以 `endpoint_id` 区分 |
| innov.events.heatmap | GET | /innov/v1/events/heatmap | API-00869～00873 | 可选 `startTime`/`endTime` |
| innov.events.detail | GET | /innov/v1/events/{eventId} | API-00874～00878 | path 必填 `eventId` |
| innov.events.relations | GET | /innov/v1/events/{eventId}/relations | API-00879～00883 | path 必填 `eventId` |
| innov.events.types | GET | /innov/v1/dict/event-types | API-00884～00888 | 无查询参数 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.events \| innov.events.list \| pageNum \| 算法输入-页码 | catalog pageNum | API-00859、00862 | 已覆盖 | 主路径 + 负值越界 |
| innov.events \| innov.events.list \| pageSize \| 算法输入-页大小 | catalog pageSize | API-00859、00861 | 已覆盖 | 主路径 + 非正整数 |
| innov.events \| innov.events.list \| startTime \| 算法输入-开始时间 | catalog startTime | API-00859 | 部分覆盖 | 主路径省略；带时间窗见 EVT-LST-05 待试调后补 |
| innov.events \| innov.events.list \| endTime \| 算法输入-结束时间 | catalog endTime | — | 未覆盖 | 无独立用例；与 startTime 组合待试调 |
| innov.events \| innov.events.list \| eventTypes \| 算法输入-事件类型CSV | catalog eventTypes | — | 未覆盖 | 无稳定非法 CSV 试调证据 |
| innov.events \| innov.events.list \| importanceLevels \| 算法输入-重要性CSV | catalog importanceLevels | API-00863 | 部分覆盖 | 枚举外 1/2/3 |
| innov.events \| innov.events.list \| keyword \| 算法输入-关键词 | catalog keyword | — | 未覆盖 | 本轮无独立用例 |
| innov.events \| innov.events.list \| total \| 算法输出-总数 | catalog total | API-00859、00863 | 已覆盖 | number 形态；禁止 sample total=3 |
| innov.events \| innov.events.list \| list \| 算法输出-事件列表 | catalog list | API-00859、00863 | 已覆盖 | array 形态；禁止 sample 标题/评分 |
| innov.events \| innov.events.list \| _empty \| 列表无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「合法筛选必空 list」证据 |
| innov.events \| innov.events.list \| _fail \| 列表查询失败 | 契约错误态 | API-00860、00861、00862、00863 | 已覆盖 | 全页鉴权 + 分页单缺陷 |
| innov.events \| innov.events.list \| M_INNOV_EVENT_COUNT \| 事件规模 metric | catalog metricIds | API-00859 | 部分覆盖 | 金样挂 metric_id；不对具体事件数断言 |
| innov.events \| innov.events.geo \| mode \| 算法输入-geo模式 | catalog mode required | API-00864、00865、00866 | 已覆盖 | geo 主路径 + 缺/非法 mode |
| innov.events \| innov.events.geo \| type \| 算法输出-GeoJSON类型 | catalog type | API-00864、00867 | 已覆盖 | string 形态 |
| innov.events \| innov.events.geo \| features \| 算法输出-点位Feature | catalog features | API-00864、00867 | 已覆盖 | array 形态；禁止 sample 坐标作通过条件 |
| innov.events \| innov.events.geo \| _empty \| 点位无数据空态 | 契约空结果 | — | 未覆盖 | 无试调证明 mode=geo 必空 features |
| innov.events \| innov.events.geo \| _fail \| 点位查询失败 | 契约错误态 | API-00865、00866、00868 | 已覆盖 | 入参单缺陷 + 错误 HTTP 方法；鉴权见 API-00860 |
| innov.events \| innov.events.geo \| map_viz \| 联调台地图点位 | catalog viz map | — | 未覆盖 | UI/Leaflet，非 REST 契约叶 |
| innov.events \| innov.events.heatmap \| startTime \| 算法输入-开始时间 | catalog startTime | API-00869、00872 | 部分覆盖 | 主路径省略 + 非法格式 |
| innov.events \| innov.events.heatmap \| endTime \| 算法输入-结束时间 | catalog endTime | API-00872 | 部分覆盖 | 与非法 startTime 组合 |
| innov.events \| innov.events.heatmap \| lng \| 算法输出-经度 | catalog lng | API-00869、00871 | 已覆盖 | 元素 number；样例为顶层数组或 data 数组 observed |
| innov.events \| innov.events.heatmap \| lat \| 算法输出-纬度 | catalog lat | API-00869、00871 | 已覆盖 | 同上 |
| innov.events \| innov.events.heatmap \| weight \| 算法输出-权重 | catalog weight | API-00869、00871 | 已覆盖 | 禁止 sample weight=92 作通过条件 |
| innov.events \| innov.events.heatmap \| _empty \| 热力无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定必空数组证据 |
| innov.events \| innov.events.heatmap \| _fail \| 热力查询失败 | 契约错误态 | API-00872、00873 | 已覆盖 | 时间非法 + 错误 path；鉴权见 API-00860 |
| innov.events \| innov.events.detail \| eventId \| 算法输入-事件ID | catalog eventId | API-00874、00875、00876、00878 | 已覆盖 | example + 非法/空 + 列表依赖 |
| innov.events \| innov.events.detail \| eventId \| 算法输出-事件ID | catalog eventId | API-00874、00877 | 已覆盖 | string 形态 |
| innov.events \| innov.events.detail \| importanceDetail \| 算法输出-评分分项 | catalog importanceDetail | API-00874、00877 | 已覆盖 | array 形态；样例 title/summary 非 responseFields |
| innov.events \| innov.events.detail \| _empty \| 详情无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定「合法 id 必空详情」证据 |
| innov.events \| innov.events.detail \| _fail \| 详情查询失败 | 契约错误态 | API-00875、00876 | 已覆盖 | 非法/空 eventId；鉴权见 API-00860 |
| innov.events \| innov.events.relations \| eventId \| 算法输入-事件ID | catalog eventId | API-00879、00880、00881、00883 | 已覆盖 | 主路径 + 非法/空 + 不存在 id |
| innov.events \| innov.events.relations \| relType \| 算法输出-关系类型 | catalog relType | API-00879、00882 | 已覆盖 | 元素 string |
| innov.events \| innov.events.relations \| relName \| 算法输出-关联对象 | catalog relName | API-00879、00882 | 已覆盖 | 元素 string；样例 relDesc/score 非 responseFields |
| innov.events \| innov.events.relations \| _empty \| 关联无数据空态 | 契约空结果 | — | 未覆盖 | 无试调证明合法 id 必空关联数组 |
| innov.events \| innov.events.relations \| _fail \| 关联查询失败 | 契约错误态 | API-00880、00881、00883 | 已覆盖 | eventId 单缺陷；鉴权见 API-00860 |
| innov.events \| innov.events.types \| eventType \| 算法输出-类型编码 | catalog eventType | API-00884、00886 | 已覆盖 | 元素 string |
| innov.events \| innov.events.types \| nameZh \| 算法输出-中文名 | catalog nameZh | API-00884、00886 | 已覆盖 | 元素 string；样例 color 非 responseFields |
| innov.events \| innov.events.types \| _empty \| 字典无数据空态 | 契约空结果 | — | 未覆盖 | 无参字典，无稳定必空构造 |
| innov.events \| innov.events.types \| _fail \| 字典查询失败 | 契约错误态 | API-00885、00887 | 已覆盖 | 未知查询 + 错误方法；鉴权见 API-00860 |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵，约） |
|------|-------------------------------|
| 已覆盖 | 22 |
| 部分覆盖 | 5 |
| 未覆盖 | 11（含 `_empty`×6、keyword/eventTypes 等） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **30**（6 endpoint × 5） |
| 编号闭区间 | **API-00859**～**API-00888** |
| 金样 | **API-00859**（完整信封） |
| 全页鉴权 | **1**（**API-00860**） |
| `_empty` 未覆盖 | **6** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 **6** endpoint、`running`×6 |

---

## 5. 金样与烟测

| 项 | 编号 |
|----|------|
| 金样（全册信封） | API-00859 |
| 全页鉴权代表 | API-00860 |
| 烟测建议 | API-00859、00864、00869、00874、00879、00884 |
