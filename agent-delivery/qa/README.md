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

## 总集拆分（专题系统 · 战略分析五级）

| 项 | 内容 |
|------|------|
| 任务 | `QA-KJZTFWXT-FUNCLIST-SPLIT-L01` |
| 输入 | 原始文档功能清单 v1.2 · sheet 科技专题服务系统 |
| **当前功能点** | `total-set/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v8.xlsx`（1298 条；5 个四级 / 32 个五级） |
| 拆分原则 v1 | `total-set/KJZTFWXT/科技专题战略分析-最细颗粒度功能点拆分原则-v1.md` |
| 五级工作稿 | `total-set/KJZTFWXT/fp-split-run/`（`work/` `review/` `prompts/`） |
| 合表脚本 | `agent-delivery/scripts/_merge_fp_split_work.py` |
| 派单包 | `agent-handoffs/QA/QA-KJZTFWXT-FUNCLIST-SPLIT-L01-派单包.md` |
| handoff | `agent-handoffs/QA/QA-KJZTFWXT-FUNCLIST-SPLIT-L01.md` |

## 总集执行（企业分析 R0）

| 项 | 内容 |
|------|------|
| 任务 | `QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01` |
| 测试环境 | http://111.198.38.90:50892/ |
| 输入 | 原 `科技专题战略分析-v1.3` 企业分析用例册已随试验稿删除；后续执行以 v8 功能点表另开任务为准 |
| 派单包 | `agent-handoffs/QA/QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01-派单包.md` |


## 新建模块用例

1. 复制模板 → `test-cases/{系统码}/{模块}/FUNC-{模块}-用例.md`
2. 从 USM 拉故事与验收场景，回填 bid 章节与 catalog ID
3. 在 `code-registry.yaml` 占用下一序号
