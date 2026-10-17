# 科技发展规划 · 功能点覆盖（innov.tech-planning）

> catalog `innov.tech-planning` · 50897 · path `/innov/tech-planning`  
> 用例册：`API-科技发展规划-用例.md`（API-00824～00828）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.tech-planning`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| innov.tech-planning.metrics | GET | /innov/v1/innov/metrics | API-00824～00828 | catalog `status=unavailable`、`runtime=java_api`；§0 **未试调** |

---

## 2. 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| innov.tech-planning \| innov.tech-planning.metrics \| module \| 算法输入-module模块 slug | catalog module（query，可选） | API-00824、00826、00827、00828 | 部分覆盖 | 合法 slug + 非法 + 空 + 省略；catalog example=`tech-planning` |
| innov.tech-planning \| innov.tech-planning.metrics \| metrics \| 算法输出-metrics指标元数据清单 | catalog metrics | API-00824、00828 | 契约占位 | array 形态；禁止 sample 中 metric_id/name 具体条目作通过条件 |
| innov.tech-planning \| innov.tech-planning.metrics \| total \| 算法输出-total指标数 | catalog total | API-00824、00828 | 契约占位 | number 形态；禁止 sample total=13 作通过条件 |
| innov.tech-planning \| innov.tech-planning.metrics \| _empty \| 指标清单无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，endpoint unavailable，无稳定「合法 module 下 metrics 必空」证据 |
| innov.tech-planning \| innov.tech-planning.metrics \| _fail \| 指标清单查询失败 | 契约错误态 | API-00824、00825、00826、00827 | 已覆盖 | 含 catalog 不可用与 module 入参失败哨兵 |

---

## 3. A 线 / snapshot 说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `innov.tech-planning` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 **1** endpoint、`unavailable`×1（path 与 `GET /innov/v1/innov/metrics` 共用，本页以 `module=tech-planning` 区分） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **5**（1 endpoint × 5） |
| 编号闭区间 | **API-00824**～**API-00828** |
| 金样 | **API-00824**（完整信封 / 不可用契约占位） |
| 鉴权代表 | **API-00825**（全页引用） |
| `_empty` 未覆盖 | **1** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry / run-log | **未改**（父控回写） |
