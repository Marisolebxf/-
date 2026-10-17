# 科技创新评估 · 功能点覆盖（innov.tech-evaluation）

> catalog `innov.tech-evaluation` · 50897 · path `/innov/tech-evaluation`  
> 用例册：`API-科技创新评估-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00819`～`00823`，共 **5** 条）  
> A 线范围：**无** 独立 `Lxx.md`（`fp-split-by-api-run/_catalog-snapshot.md`：1 endpoint、`status=unavailable`）  
> 功能点键：`innov.tech-evaluation | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.tech-evaluation.metrics | GET | /innov/v1/innov/metrics | API-00819～00823 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.tech-evaluation \| innov.tech-evaluation.metrics \| module \| 算法输入-module模块slug | catalog module | API-00819、00821、00822、00823 | 部分覆盖 | MET-01 本页 slug；MET-02 省略；MET-03 非法 module |
| innov.tech-evaluation \| innov.tech-evaluation.metrics \| metrics \| 算法输出-metrics指标元数据清单 | catalog metrics | API-00819、00821 | 契约占位 | unavailable；仅断言 array 形态，禁止 sample 24 条验收 |
| innov.tech-evaluation \| innov.tech-evaluation.metrics \| total \| 算法输出-total指标数 | catalog total | API-00819、00821 | 契约占位 | 仅断言 number 形态，禁止 total=24 验收 |
| innov.tech-evaluation \| innov.tech-evaluation.metrics \| _empty \| 指标清单无数据空态 | 契约空结果 | — | 未覆盖 | unavailable + 未试调，无稳定「合法 module 必空 metrics」构造 |
| innov.tech-evaluation \| innov.tech-evaluation.metrics \| _fail \| 指标清单查询失败 | 契约错误态 | API-00819、00820、00823 | 已覆盖 | 含 catalog 不可用语义、鉴权失败、非法 module |
| innov.tech-evaluation \| \| calc_logic_ref \| 口径公式见 calc-logic | catalog summary | — | 未覆盖 | req_only；非 HTTP responseFields |
| innov.tech-evaluation \| \| metric_signoff \| 指标 mock/待会签 | catalog formula_status | — | 未覆盖 | req_only；元素字段未列入 responseFields |

样例 `metrics` 元素内 `metric_id`、`name`、`algorithm_type`、`formula_status`、`pending_ref`：本轮无独立形态用例，执行期若成功返回则记入 as-built，不扩写通过条件。

---

## 3. 统计（交卷）

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail`） |
| 部分覆盖 | 1（`module`） |
| 契约占位 | 2（`metrics`、`total`） |
| 未覆盖 | 3（含 `_empty` 1 + req_only 2） |

| 项 | 值 |
|----|-----|
| API 用例条数 | **5** |
| 编号闭区间 | **API-00819**～**API-00823** |
| endpoint 数 | **1**（5 条/endpoint） |
| `_empty`（指标清单稳定空态） | **未覆盖** 1 行 |
| 50897 试调 | **未试调**（见用例 §0） |
| FUNC 条数 | **0** |
| code-registry | **未回写**（父控 no registry） |

---

## 4. 无对应 A 线功能点的用例

无（本册 5 条均可挂接 catalog 入参/出参或契约哨兵）。
