# 深圳创新监测 · 功能点覆盖（innov.sz-monitoring）

> catalog `innov.sz-monitoring` · 50897 · path `/innov/sz-monitoring`  
> 用例册：`API-深圳创新监测-用例.md`（API-00839～00843）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.sz-monitoring`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | API-00839～00843 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| innov.sz-monitoring \| innov.sz-monitoring.metrics \| module \| 算法输入-module模块 slug | catalog module（query，可选） | API-00839、00841、00842 | 部分覆盖 | sz-monitoring 主路径占位 + 非法 + 空；省略 module 见 SMON-04 待试调 |
| innov.sz-monitoring \| innov.sz-monitoring.metrics \| metrics \| 算法输出-metrics指标元数据清单 | catalog metrics | API-00839、00843 | 契约占位 | array 形态；禁止 sample 7 条或 metric_id 数值 |
| innov.sz-monitoring \| innov.sz-monitoring.metrics \| total \| 算法输出-total指标数 | catalog total | API-00839、00843 | 契约占位 | number 形态；禁止 total=7 作通过条件 |
| innov.sz-monitoring \| innov.sz-monitoring.metrics \| _empty \| 指标清单无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 module 必空 metrics」证据 |
| innov.sz-monitoring \| innov.sz-monitoring.metrics \| _fail \| 指标清单查询失败 | 契约错误态 | API-00839、00840、00841、00842 | 已覆盖 | 含 unavailable 占位、鉴权与 module 单缺陷 |

---

## 3. A 线 / snapshot 说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `innov.sz-monitoring` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 **1** endpoint、`unavailable`×1（path 与 `GET /innov/v1/innov/metrics` 共用，本页以 `module=sz-monitoring` 区分） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **5** |
| 编号闭区间 | **API-00839**～**API-00843** |
| 金样 | **API-00839**（完整信封） |
| 鉴权代表 | **API-00840** |
| `_empty` 未覆盖 | **1** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry / run-log | **未改**（父控回写） |
