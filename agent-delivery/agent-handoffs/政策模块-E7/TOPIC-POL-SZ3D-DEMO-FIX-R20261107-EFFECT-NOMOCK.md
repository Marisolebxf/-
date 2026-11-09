# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-NOMOCK · 合规演示去掉落地实效 Mock 角标

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 角标已在本单建档前按监管人要求去掉并推送。本单只补交接，不再改前端。状态停在待签收，不改为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只把落地实效维度和三项指标的 `mockGap` 设为 false。模板里的 Mock 分支留着，自检仍要求文件里有 MockBadge。没有新开一轮前端改动。 |

## 问题清单

- 配置区「落地实效性」以及落地执行率、受益覆盖广度、反馈满意度写死了 Mock 缺口。合规演示不能出现这几个字。

## 修改内容

- `policySzModel.mjs`：上述维度和三项 `mockGap: false`。配置区因此走「可用」，不渲染 Mock 缺口和 MockBadge。
- 空分仍然不是 0。没有改算法库按钮文案。
- 代码在 `lumen-ui-topic` commit `cf304e0`，推送 `03661ff..ad4e0d2`。本会话没有再推前端。

## 测试结果

- 当时 `policyShenzhen.selfcheck` 退出码 0，并断言维度和指标都没有 `mockGap: true`。
- 本会话未再改该仓，未重跑页面。

## 遗留风险

- `LUMEN-POLICY-SZ3D-FE-SRS-R20261107` 仍是 in_progress，其 DoD 文字还写着保留 Mock 角标。页面上的角标已经去掉。不要为了那句 DoD 把角标加回去。
- 分数要等结果板镜像读到缺项表之后才会从不可算变成实算。角标去掉不等于 D4 已改为 live。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`
- commit：`cf304e0`（推送范围 `03661ff..ad4e0d2`）
- pipeline URL / ID：该次推送已由前端 CI 接收，本会话未再打开
- 部署 namespace / 镜像 tag：未在本会话重核
- K8s rollout：未在本会话重核
- dev 测试 URL / 命令与结果：自检当时退出码 0

## 涉及文件

- `repos/lumen-ui-topic/src/config/policySzModel.mjs`
- `repos/lumen-ui-topic/src/views/policy/policyShenzhen.selfcheck.mjs`

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 10000 |
| model_used | grok-4.7 |
| actual_cost | 0.3 |
| cost_warn | green |
