# 段 E 缺陷包（测试驱动调度）

> 复制到 `agent-handoffs/{模块}/{bugfix-task-id}.md` 的「问题清单」之前，或作为 QA handoff 附件。  
> **规约**：`长任务执行规约.md` §11。QA / 人填写；**coordinator 调度、不改业务代码**。分诊助手无提交权（§11.5.1）。  
> **禁止** C1 无 `X-Trace-Id` 开修。先填失败分类，C1 才派业务修。

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | |
| 故事 ID | 如 `US-CHAIN-DIAG-03` |
| 已发布 URL | **K8s dev 前端**，禁止 localhost |
| 操作步骤 | |
| 期望 | 总控该行原文 |
| 实际现象 | |
| HTTP / 页面态 | 5xx / 白屏 / 错跳 / Job failed / 空态 … |
| **失败分类** | C1 产品/代码 · C2 发布/环境 · C3 白名单空态 · C4 用例/总控错 · C5 结构/库闸 · C6 未知（QA 建议 / coordinator 确认） |
| **X-Trace-Id** | C1 必填；C2 可用 E0/rollout 证据代替 |
| Tempo | Grafana Explore 或 `observability.md` §9 链接 |
| Loki | 按 trace-id 搜到的错误摘要 |
| 怀疑层 | C1：FE / Java / Python / 发布-配错（devops）；C2：只写 E0 |
| 诚实空态？ | **仅 C3**（该行允许的空态命中）。期望未发生 = 否，不得标 C3 |

```text
/goal
你是经验丰富的{frontend|api|algorithm}-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + 长任务总控 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
```
