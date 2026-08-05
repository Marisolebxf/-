# ENT-ALGO-RESULT-PAYLOAD-PATCH-L01 — Handoff

> 任务编码：ENT-ALGO-RESULT-PAYLOAD-PATCH-L01
> 标题：企业分析结果 JSON 契约漏写字段补丁
> 执行人：human:唐绍祖
> 监管人：human:唐绍祖
> 日期：2026-08-05
> 状态：ready_to_sign（待淮政玮/徐腾强签收）

---

## 1. 任务背景

架构裁决后的最小契约补丁。API-ENT-ANALYSIS-RESULT-CONTRACT-UI-GAPS.md 标出多处 B 类缺口（契约缺内容），本补丁仅处理其中「已有中间结果或预检事实可直接回写」的三项兼容加法。

设计参考：
- `agent-handoffs/企业战略分析-ENT/API-ENT-ANALYSIS-RESULT-CONTRACT-UI-GAPS.md` §1.5 / §3.1
- `agent-handoffs/企业战略分析-ENT/API-ENT-ANALYSIS-RESULT-CONTRACT.md` §2.1

## 2. 补丁内容

### 补丁 1：supply_chain keyNodes[]/breakRisks[] 补充 id

**问题**：`keyNodes[]` / `breakRisks[]` 只有 `name`，无节点 `id`；前端点击侧栏行↔高亮图节点只能按 name 模糊匹配，同名节点无法精确联动。

**修复**：`keyNodes[].id` 和 `breakRisks[].id` 直接取自 `graph.nodes[].id`，保证稳定关联。

### 补丁 2：supply_chain influenceScore 回写 graph.nodes[]

**问题**：影响力分数仅在 `keyNodes[].influenceScore`，`graph.nodes[]` 无分数字段；前端节点圆大小无法按影响力缩放。

**修复**：仅 `is_key=True` 且 `depth>=1` 的图节点回写 `influence_score`（与 keyNodes 中的值一致）。非关键节点不编造分数；depth=0 中心企业不写。

### 补丁 3：evaluation result 新增 result.dataQuality[]

**问题**：企业评估结果仅 `diagnosisRows[].confidence` 三档，无 per-enterprise coverage/blocked/missingMetricIds；前端质量面板与排名筛选无法用结果 JSON 填充。

**修复**：新建 `entan/eval/data_quality.py` 模块，`compute_data_quality()` 复用预检逻辑（与 `entan_evaluation_routes._precheck_enterprises` 同源），在 `_compute_eval_result` 末尾插入 `result["data_quality"]`。DB 不可达时 try/except 返回空列表，不阻断评估主流程。

## 3. 变更文件

| 文件 | 变更类型 | 说明 |
|---|---|---|
| `repos/demo-algo-ent-analysis/innov/analysis/supply_chain.py` | 修改 | keyNodes[]/breakRisks[] 加 id；influenceScore 回写 nodes[] |
| `repos/demo-algo-ent-analysis/entan/eval/data_quality.py` | 新建 | compute_data_quality() 模块 |
| `repos/demo-algo-ent-analysis/entan/common/async_task_manager.py` | 修改 | _compute_eval_result 末尾插入 dataQuality 计算 |
| `repos/demo-algo-ent-analysis/tests/test_eval_data_quality.py` | 新建 | 22 项测试 |
| `repos/demo-algo-ent-analysis/tests/test_analysis.py` | 修改 | 补充 keyNodes/breakRisks id 断言 |
| `repos/demo-algo-science/innov/analysis/supply_chain.py` | 无变更 | 迁移桩，不动 |
| `repos/demo-algo-science/tests/test_analysis.py` | 无变更 | 迁移桩 skip，不动 |

## 4. 向后兼容

- 不删除、不改名任何既有 API 路径、请求字段、响应字段与层级
- Java-facing contract 保持向后兼容
- 旧消费者忽略新增字段即可正常工作

## 5. 测试

```
tests/test_eval_data_quality.py: 22 passed
tests/test_analysis.py: 34 passed
合计: 56 passed
```

## 6. 成本

| 字段 | 值 |
|---|---|
| estimated_tokens | 120000 |
| actual_tokens | ~85000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.64 |
| cost_warn | green |

## 7. 未实现项（DoD 明确排除）

- edges.strength
- nodes.owner（A/B/shared 归属）
- 非关键节点 influenceScore
- riskCredit 明细
- risk taxonomy（riskType 枚举）
- 政策方向（policyDirections）
- 趋势/营收/对标序列

以上须另行完成产品口径或真实数据源决策，不在本补丁范围。

## 8. 架构合规自检

- [x] 不新增 API 路径
- [x] 不删除/不改名既有字段
- [x] 不使用 RNG/Mock/固定样例补值
- [x] dataQuality 复用既有预检事实逻辑
- [x] influenceScore 仅回写已计算值，不编造
- [x] try/except 保护，DB 不可达不阻断主流程