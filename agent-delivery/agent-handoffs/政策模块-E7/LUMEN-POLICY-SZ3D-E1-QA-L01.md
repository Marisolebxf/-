# LUMEN-POLICY-SZ3D-E1-QA-L01 · 深圳政策现状已发布金路径

> 只测 http://10.50.69.111:30892 。未改业务代码。金路径 4 红，其余四条过。缺陷包：`LUMEN-POLICY-SZ3D-E1-DEFECT-C1.md`。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | E0 已是 ready_to_sign，点名镜像已在 dev。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 只做已发布页冒烟，没有改代码。 |

## 金路径

| # | 期望 | 结果 |
|---|------|------|
| 1 | 三张卡可见；无二级勾选；无一级权重步进器 | 过。`policy-sz3d-fixed-cards` 的 `support/fit/effect` 都在。卡内勾选 0、输入 0。页上另有对比篮勾选，不可见，不是指标勾选。页脚 class 名仍带 weight，文案是「请完成分析锚点选择」。无「一键均分」「指标体系构建」。 |
| 2 | 未选锚点禁用；选中合法产业后可提交 | 过。未选时按钮禁用。选中半导体与集成电路后页脚「锚点已选，可开始分析」，`POST /api/topicAsync/topic/v1/analysis/tasks` 返回 200，任务 `POLICY-20261025-010`，`reused=false`。 |
| 3 | 支持力度含深圳条数、层级均值、分数、名次；档位不是 0；文案含非资金强度 | 过。结果板：分 32.6694，名次 5，条数 879，层级均值 0.4579。档位不可算：无金额列。文案含「非资金强度」和「市级备案多会拉低层级分」。 |
| 4 | 换产业后支持力度城市截面分数不变；适配性范围变化 | 红。分数不变成立（010 与 011 都是 32.6694）。适配性没有变：两条都是「未提供链名」。见缺陷包。 |
| 5 | 落地实效整卡空；页面无综合分 | 过。实效卡「不可算 / 实施日、支持对象、反馈全缺」。结果页正文没有「综合」。`result_payload` 无 `composite`。 |

创建请求没有 `weights`、没有 `selected_indicators`。过程五步在已发布过程页都显示已完成，然后停在「查看分析结果」，没有自动跳进结果。

## 架构合规

| 铁律 | 结果 |
|------|------|
| 只测已发布 lumen 前端 | ✅ 30892，不是 localhost，不是 30888 |
| QA 不改代码 | ✅ |
| 期望未发生必红 | ✅ 第 4 条已红并附缺陷包 |
| C1 带 X-Trace-Id | ✅ `cd3b7cdd8c4c4e9199458eabbdf590e8` |

## 遗留

- 不把本叶当成产品通过。修完适配性名称后再复测第 4 条。
- 未派修单。下一张应是前端 bugfix：具体产业同时提交 `industry_name` 与 `industry_vid`。

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 40000 |
| model_used | grok-4.7 |
| actual_cost | 0.08 |
| cost_warn | green |
| 说明 | source: session_estimate。按本叶登记估算 40000，比例沿用 C 叶 60000 token ≈ $0.12。 |
