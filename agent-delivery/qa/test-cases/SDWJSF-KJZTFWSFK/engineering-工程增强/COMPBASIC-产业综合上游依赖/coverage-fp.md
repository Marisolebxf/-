# 产业综合上游依赖 · 功能点覆盖（comp.basic）

> catalog `comp.basic` · 50897 · path `/industry-comp/basic`  
> 用例册：`API-产业综合上游依赖-用例.md`（API-00649～00653）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `comp.basic`（`_l6-to-catalog-map.yaml`：上游依赖页，非 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | API-00649～00653 | catalog `status=unavailable`、`runtime=local_mock` |

---

## 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| 工程增强 \| comp.basic.upstream \| region \| 算法输入-region区域编码 | catalog region | API-00649、00651、00652 | 部分覆盖 | unavailable 占位 + 非法/空 region；合法省略 region 主路径待 endpoint available 后补 |
| 工程增强 \| comp.basic.upstream \| upstream \| 算法输出-upstream上游七维依赖 | catalog upstream | API-00649、00653 | 契约占位 | 禁止 sample 七维 ready 示例作通过条件 |
| 工程增强 \| comp.basic.upstream \| kpis \| 算法输出-kpis活力要素协同演示指数 | catalog kpis | API-00649、00653 | 契约占位 | 禁止 sample vitality/element/synergy 数值作通过条件 |
| 工程增强 \| comp.basic.upstream \| _empty \| 上游依赖无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 region 下 upstream 必空」构造证据 |
| 工程增强 \| comp.basic.upstream \| _fail \| 上游依赖查询失败 | 契约错误态 | API-00649、00651、00652 | 已覆盖 | 含 catalog 不可用与 region 失败哨兵 |

---

## A 线 work 检索说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `comp.basic` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 1 endpoint、`unavailable`×1、`local_mock`×1 |
| B 线待 A 线合表 | 状态可先 **待 A 线合表核对**；本页 endpoint 用例仍有效 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| API 用例数 | 5 |
| 契约 field 键（含 _empty/_fail） | 5 |
| 已覆盖（含契约占位 / _fail） | 4 键（region、upstream、kpis、_fail） |
| 未覆盖 | 1（_empty） |
| 异常-鉴权 | API-00650（endpoint 级，不单独挂 field 行） |
| 编号闭区间 | **API-00649**～**API-00653** |
