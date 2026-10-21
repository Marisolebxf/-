# 区域创新要素层次综合评价 · 功能点覆盖（comp.element-layer / L57）

> catalog `comp.element-layer` · path `#/industry-comp/element-layer`  
> A 线真源：`fp-split-by-api-run/work/L57.md`（只读，未改）  
> B 线用例：`FUNC-区域创新要素层次综合评价-用例.md`（第三轮 **FUNC-01060**～**01064**；旧 API-01808～01810 作废）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.element-layer`

> **path 独占**：`GET /comp/v1/comp/element-layer` 为本页「要素层次」独占，与同模块 `element-type`、`element-domain`、`element-synthesis` 分开验收。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.element-layer.main | GET | /comp/v1/comp/element-layer | FUNC-01060～01062 | unavailable |
| （页面清单） | — | — | FUNC-01063、01064 | — |

---

## 功能点 → 用例矩阵（挂 L57.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L57 \| comp.element-layer.main \| region \| 算法输入-region区域标签 | catalog region | FUNC-01060、01061、01062 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L57 \| comp.element-layer.main \| index \| 算法输出-index区域创新要素层次指数 | catalog index | FUNC-01060、01061 | 已覆盖 | 主流程与备选断言 index（number，示例 69.8） |
| L57 \| comp.element-layer.main \| _empty \| 要素层次评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件 |
| L57 \| comp.element-layer.main \| _fail \| 要素层次评价查询失败 | 契约错误态 | FUNC-01062 | 部分覆盖 | 仅非法 region |
| （页面清单） \| comp.element-layer \| 接口信息 / 算法测试 | 联调台 tab | FUNC-01063、01064 | 已覆盖 | 单接口页清单 2 条 |

---

## 统计

| 项 | 值 |
|------|------|
| FUNC 用例 | 5（01060～01064） |
| 金样 | FUNC-01060 |
