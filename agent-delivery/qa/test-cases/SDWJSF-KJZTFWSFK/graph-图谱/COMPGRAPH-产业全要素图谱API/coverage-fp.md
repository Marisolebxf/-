# 产业全要素图谱 API · 功能点覆盖（comp.graph / L13）

> catalog `comp.graph` · 50897 · path `/industry-comp/graph`  
> **用例册**：`API-产业全要素图谱API-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000704`～`000733`，共 **30** 条）  
> A 线范围：**L13**（产业全要素图谱 API 服务开发，39 行含 2 req_only）  
> 功能点键：`L13 | endpoint_id | field_key | 功能点中文`  
> **A 线核对**：`grep comp.graph fp-split-by-api-run/work/L13.md`

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.graph.browse | GET | /industry-comp/v1/comp/graph | API-000704, API-000705, API-000706, API-000707, API-000708 | available |
| comp.graph.entities | GET | /industry-comp/v1/comp/graph/entities | API-000709, API-000710, API-000711, API-000712, API-000713 | available |
| comp.graph.relations | GET | /industry-comp/v1/comp/graph/relations | API-000714, API-000715, API-000716, API-000717, API-000718 | available |
| comp.graph.viz | GET | /industry-comp/v1/comp/graph/viz | API-000719, API-000720, API-000721, API-000722, API-000723 | available |
| comp.graph.similar | POST | /industry-comp/v1/comp/graph/similar | API-000724, API-000725, API-000726, API-000727, API-000728 | available |
| comp.graph.metrics | GET | /industry-comp/v1/comp/graph/metrics | API-000729, API-000730, API-000731, API-000732, API-000733 | available |

---

## 2. 功能点 → 用例（L13 主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L13 \| comp.graph.browse \| center \| 算法输入-center稳定 VID | catalog center | API-000704, API-000706, API-000707, API-000708 | 部分覆盖 | 主路径+非法 center；§0未试调 |
| L13 \| comp.graph.browse \| hops \| 算法输入-hops邻域跳数 | catalog hops | API-000704, API-000706 | 部分覆盖 | 主路径+非法 hops |
| L13 \| comp.graph.browse \| limit \| 算法输入-limit节点上限 | catalog limit | API-000704, API-000707 | 部分覆盖 | 主路径+limit 越界 |
| L13 \| comp.graph.browse \| nodes \| 算法输出-nodes节点 | catalog nodes | API-000704 | 已覆盖 | 金样断言 array 形态 |
| L13 \| comp.graph.browse \| edges \| 算法输出-edges边 | catalog edges | API-000704 | 已覆盖 | 金样断言 array 形态 |
| L13 \| comp.graph.browse \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | API-000704 | 已覆盖 | 金样断言 string 形态 |
| L13 \| comp.graph.browse \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.browse \| _fail \| 调用失败 | 契约错误态 | API-000706, API-000707, API-000708 | 已覆盖 | 入参失败哨兵 |
| L13 \| comp.graph.entities \| q \| 算法输入-q关键词或 VID | catalog q | API-000709, API-000710, API-000711, API-000712, API-000713 | 部分覆盖 | 主路径+缺/空/非法组合 |
| L13 \| comp.graph.entities \| sort \| 算法输入-sort | catalog sort | API-000709, API-000712, API-000713 | 部分覆盖 | 主路径+非法 sort+组合 |
| L13 \| comp.graph.entities \| size \| 算法输入-size页大小 | catalog size | API-000709, API-000713 | 部分覆盖 | 主路径含 size；备选 ENT-05 |
| L13 \| comp.graph.entities \| items \| 算法输出-items已有点 | catalog items | API-000709 | 已覆盖 | 主路径断言 array |
| L13 \| comp.graph.entities \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.entities \| _fail \| 调用失败 | 契约错误态 | API-000710, API-000711, API-000712 | 已覆盖 | 缺 q/空 q/非法 sort |
| L13 \| comp.graph.relations \| src \| 算法输入-src源稳定 VID | catalog src | API-000714, API-000715, API-000717, API-000718 | 部分覆盖 | 主路径+缺/非法 src |
| L13 \| comp.graph.relations \| dst \| 算法输入-dst对端 VID | catalog dst | API-000714, API-000718 | 部分覆盖 | REL-05 组合 |
| L13 \| comp.graph.relations \| rel \| 算法输入-rel已上图边类型 | catalog rel | API-000714, API-000718 | 部分覆盖 | REL-05 组合 |
| L13 \| comp.graph.relations \| direction \| 算法输入-direction | catalog direction | API-000714, API-000716, API-000718 | 部分覆盖 | 主路径+非法 direction |
| L13 \| comp.graph.relations \| edges \| 算法输出-edges已有边 | catalog edges | API-000714 | 已覆盖 | 主路径断言 array |
| L13 \| comp.graph.relations \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.relations \| _fail \| 调用失败 | 契约错误态 | API-000715, API-000716, API-000717 | 已覆盖 | 入参失败哨兵 |
| L13 \| comp.graph.viz \| layout \| 算法输入-layout | catalog layout | API-000719, API-000720, API-000722, API-000723 | 部分覆盖 | graph/wordcloud+非法 |
| L13 \| comp.graph.viz \| limit \| 算法输入-limit上限 | catalog limit | API-000719, API-000721, API-000723 | 部分覆盖 | 主路径+越界+组合 |
| L13 \| comp.graph.viz \| nodes \| 算法输出-nodes图节点 | catalog nodes | API-000719, API-000722 | 已覆盖 | 主路径+wordcloud 备选 |
| L13 \| comp.graph.viz \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.viz \| _fail \| 调用失败 | 契约错误态 | API-000720, API-000721 | 已覆盖 | 非法 layout/limit |
| L13 \| comp.graph.similar \| a \| 算法输入-a名称或 VID | catalog a | API-000724, API-000725, API-000727, API-000728 | 部分覆盖 | 主路径+缺 a |
| L13 \| comp.graph.similar \| b \| 算法输入-b名称或 VID | catalog b | API-000724, API-000726, API-000727, API-000728 | 部分覆盖 | 主路径+缺 b |
| L13 \| comp.graph.similar \| mode \| 算法输入-mode | catalog mode | API-000724, API-000727, API-000728 | 部分覆盖 | rule+非法+省略 |
| L13 \| comp.graph.similar \| score \| 算法输出-score0–1 | catalog score | API-000724, API-000728 | 已覆盖 | 主路径+省略 mode |
| L13 \| comp.graph.similar \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.similar \| _fail \| 调用失败 | 契约错误态 | API-000725, API-000726, API-000727 | 已覆盖 | 缺 a/b/非法 mode |
| L13 \| comp.graph.metrics \| center \| 算法输入-center中心 VID | catalog center | API-000729, API-000731, API-000733 | 部分覆盖 | 省略/非法/组合 |
| L13 \| comp.graph.metrics \| limit \| 算法输入-limit子图上限 | catalog limit | API-000729, API-000730, API-000732, API-000733 | 部分覆盖 | 主路径+越界+组合 |
| L13 \| comp.graph.metrics \| density \| 算法输出-density密度 | catalog density | API-000729, API-000732, API-000733 | 已覆盖 | 主路径+备选 |
| L13 \| comp.graph.metrics \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空构造 |
| L13 \| comp.graph.metrics \| _fail \| 调用失败 | 契约错误态 | API-000730, API-000731 | 已覆盖 | limit/center 失败 |
| L13 \| （页级） \| ext_integration_semantic \| 外部系统集成调用 | 需规 | — | 不纳入 | req_only |
| L13 \| （页级） \| knowledge_expand_semantic \| 知识扩充应用场景 | 需规 | — | 不纳入 | req_only |

---

## 3. §I 计数

| 指标 | 值 |
|------|-----|
| API 用例 | 30（000704～000733） |
| catalog endpoint | 6 |
| L13 矩阵行（含 req_only） | 39 |
| `_empty` 未覆盖 | 6 |
| req_only 不纳入 | 2 |
| 金样 | API-000704 |
| 鉴权代表 | API-000705 |
| FUNC | 0 |
| code-registry / run-log | 未改（父控） |
