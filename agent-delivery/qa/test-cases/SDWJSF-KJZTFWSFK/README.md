# 科技专题服务算法库 · 测试用例工作区

> **系统码**：`SDWJSF/KJZTFWSFK`（用例编号内 `/`）  
> **编排**：[`algo-lib-api-case-playbook.md`](../../algo-lib-api-case-playbook.md)（**编写思路真源 = 该文 §编写方法论**）· 总索引 [`algo-lib-playbook-index.md`](../../algo-lib-playbook-index.md)  
> **接口文档**：`repos/lumen-ui-algo-apiview/src/catalog/*.json`（联调台 `https://edu.itic-sci.com/dma/algovwz/` 下拉框与请求/响应说明的源码；`50897` 已停用。编写时不打开页面）  
> **规范**：[`qa-test-case-spec.md`](../../../qa-test-case-spec.md)

## 目录约定

| 层 | 规则 | 示例 |
|----|------|------|
| 模块层 | catalog `modules[].id` + 中文 | `basic-基础指标`、`chain-产业链分析` |
| 页目录 | `entry_id` 大写缩写 + `entries[].title` | `CHAINBASIC-产业链基础指标` |
| 用例册 | **`FUNC-{页短名}-用例.md`** | 编号类型 **FUNC**（2026-10-19 起） |

**不**建 `shell-系统壳/`，**不**单列登录用例。登录只写前置条件。功能点用 catalog `endpoints[].title`，去掉自行添加的 `A1`/`A2`。功能模块/子功能模块/功能项/子功能项 = 需规三级到六级；无六级写「待挂需规」。

## 金样（S1 首批）

| catalog_page_id | 路径 | A 线 | 状态 |
|-----------------|------|------|------|
| `chain.basic` | `basic-基础指标/CHAINBASIC-产业链基础指标/` | L01 | 第三轮改写为 `FUNC-产业链基础指标-用例.md` |

`API-00001`～`02210` 全部作废。工作区与交付目录里现有的 1322 条 API 表是评审前过渡稿。第三轮规则见 [`algo-lib-api-case-playbook.md`](../../algo-lib-api-case-playbook.md) **§长任务返工**。`run-log.md` 已有批次只记录旧轮。

## 取号

`code-registry.yaml` → `SDWJSF/KJZTFWSFK`：**`next_seq.FUNC`**（当前为 1，第三轮从 **FUNC-00001** 起）。不要再取 `next_seq.API`。写完册后回写 `modules` 与 `next_seq.FUNC`。
