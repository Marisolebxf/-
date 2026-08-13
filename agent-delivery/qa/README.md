# QA 工作区索引

> 正式规范：[`../qa-test-case-spec.md`](../qa-test-case-spec.md)（v1.0）  
> 模板：[`../templates/test-case-template.md`](../templates/test-case-template.md) · [`../templates/test-record-template.md`](../templates/test-record-template.md)

## 已确认规则

- 功能类型码 = **FUNC**
- GKX 扩展列 = **主表右侧**

## 目录

| 路径 | 用途 |
|------|------|
| `test-cases/` | 按系统码 / 模块存放用例 MD |
| `test-records/` | 按系统码 / 轮次存放执行记录 MD |
| `evidence/` | 截图与三联查导出 |
| `code-registry.yaml` | 系统码与当前最大序号台账 |

## 用例库

执行仓：**lumen-ui-topic**（`VITE_APP_USE_MOCK=false`，走 Java `/topic/v1`；INTEG：`http://192.168.88.50:30892`）。

| 模块 | 文件 | 编号 | 状态 | 入口 |
|------|------|------|------|------|
| 企业查询 SEARCH | `test-cases/KJZTFWXT/SEARCH/FUNC-企业查询-用例.md` | 00001–00014, 00030–00045 | **v1.2**（字段/页签勾选）· ENT-MOD-SEARCH-QA-ACCEPT-L01 | `/enterprise/enterprise-search` |
| 对比篮 COMPARE | `test-cases/KJZTFWXT/COMPARE/FUNC-对比篮-用例.md` | 00015–00029 | v1.0 试点 | `/enterprise/enterprise-compare` |
| SEARCH 记录 | `test-records/KJZTFWXT/SEARCH/FUNC-企业查询-记录-待填.md` | — | 待人工填 | — |

## 总集 Excel（科技专题战略分析）

| 版本 | 目录 |
|------|------|
| v1.0 | `total-set/KJZTFWXT/科技专题战略分析-v1.0/` |
| v1.1 | `total-set/KJZTFWXT/科技专题战略分析-v1.1/` |
| v1.2 | `total-set/KJZTFWXT/科技专题战略分析-v1.2/` |
| **v1.3（当前）** | `total-set/KJZTFWXT/科技专题战略分析-v1.3/` |

v1.1：非通用约 1300 + 通用质量属性，总约 1700；步骤/预期结合功能清单需规 + `bid-reference` §1.1.1.2.4.2 设计方案。

v1.2：功能点优先按 **demo-ui-topic 原型** 拆分；需规仍全覆盖。`_gen_zt_testcases_v12.py`。

v1.3：功能清单定数量（非通用 1300 + 通用 396 = 1696）；要点来自 **产品定义八件套**（USM/TRACE/IA/UX）；与原型冲突以 **demo-ui-topic** 为准。索引 `total-set/KJZTFWXT/product-pack-index-zt-strategy.yaml`；生成 `_gen_zt_testcases_v13.py`。列 = 总集 17 列 + 右侧 GKX 扩展列。


## 总集执行（企业分析 R0）

| 项 | 内容 |
|------|------|
| 任务 | `QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01` |
| 测试环境 | http://111.198.38.90:50892/ |
| 输入 | `total-set/KJZTFWXT/科技专题战略分析-v1.3/6.国际科技信息中心项目_企业分析_测试用例.xlsx`（538 条） |
| R0 记录空壳 | `total-set/KJZTFWXT/科技专题战略分析-v1.3/7.国际科技信息中心项目_企业分析_测试记录-R0.xlsx` |
| 生成脚本 | `_gen_ent_test_record_shell.py` |
| 派单包 | `agent-handoffs/QA/QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01-派单包.md` |


## 新建模块用例

1. 复制模板 → `test-cases/{系统码}/{模块}/FUNC-{模块}-用例.md`
2. 从 USM 拉故事与验收场景，回填 bid 章节与 catalog ID
3. 在 `code-registry.yaml` 占用下一序号
