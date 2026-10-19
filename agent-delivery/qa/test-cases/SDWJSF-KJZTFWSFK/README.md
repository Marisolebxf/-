# 科技专题服务算法库 · 测试用例工作区

> **系统码**：`SDWJSF/KJZTFWSFK`（用例编号内 `/`）  
> **编排**：[`algo-lib-api-case-playbook.md`](../../algo-lib-api-case-playbook.md)（**编写思路真源 = 该文 §编写方法论**）· 总索引 [`algo-lib-playbook-index.md`](../../algo-lib-playbook-index.md)  
> **接口文档**：`repos/lumen-ui-algo-apiview/src/catalog/*.json`（50897 下拉框与请求/响应说明的源码，编写时不打开页面）  
> **规范**：[`qa-test-case-spec.md`](../../../qa-test-case-spec.md)

## 目录约定

| 层 | 规则 | 示例 |
|----|------|------|
| 模块层 | catalog `modules[].id` + 中文 | `basic-基础指标`、`chain-产业链分析` |
| 页目录 | `entry_id` 大写缩写 + `entries[].title` | `CHAINBASIC-产业链基础指标` |
| 用例册 | **仅** `API-{页短名}-用例.md` | 编号类型 **API** |

**不**建 `shell-系统壳/`、**不**建 FUNC 册，**不**写登录、Token、401/424。功能点列用 catalog `endpoints[].title` 原文。

## 金样（S1 首批）

| catalog_page_id | 路径 | A 线 | 状态 |
|-----------------|------|------|------|
| `chain.basic` | `basic-基础指标/CHAINBASIC-产业链基础指标/` | L01 | 第一轮 `API-00001`～`00023` **作废**，第二轮覆盖重写 |

第一轮全库 `API-00001`～`00888` 作废。`科技专题服务算法库-API测试用例.xlsx` 的「功能测试用例」已按第二轮册重写为 `API-00889`～`02210`（1322 条）。测试步骤已写入各册附录 A 的参数赋值，打开表即可看到具体入参。返工规则见 [`algo-lib-api-case-playbook.md`](../../algo-lib-api-case-playbook.md) **§长任务返工**。`run-log.md` 批 1～22 只记录第一轮。

## 取号

`code-registry.yaml` → `SDWJSF/KJZTFWSFK`：**仅 `next_seq.API`**。第二轮从 **889** 起，不复用 `00001`～`00888`。写完册后回写 `modules` 与 `next_seq`。
