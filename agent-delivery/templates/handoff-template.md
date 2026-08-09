# {task-id} · {title}

> 格式参考 `正式文件/` 与 `templates/`；**内容**按本次实测与代码实写，勿抄 V6 原文。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:{真名}` 或 `agent:{role}` |
| supervised_by | `human:{真名}`（用 Agent 时必填，与 git commit `[human:…]` 同一人） |
| claim_type | `pull` / `coordinator_dispatch` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` / `lite` / `ultra` / `off` / `N/A`（定义·文档类） |
| 说明 | 与派单 `/goal` 强度行一致；`ultra`/`off` 须一句理由；确认未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律。见 [`ponytail-usage.md`](../ponytail-usage.md) |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `mcp` / `proxy` / `skip` |
| 说明 | 可选；缺行不拒收。`skip` 须一句理由（如本机未挂载）。见手册 §9.0b · [`Headroom团队使用说明.md`](../Headroom团队使用说明.md) |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | V6 §…（仅对照章节名，不摘录正文） |
| 时序图版式 | seq-7m34p §…（若涉及） |

## 问题清单

- ...

## 修改内容

- ...

## 测试结果

- ...

## 遗留风险

- ...

## CI/CD（必填）

- 分支：
- commit：
- pipeline URL / ID：
- 部署 namespace / 镜像 tag：
- K8s rollout：成功 / 失败
- dev 测试 URL / 命令与结果：

## 可观测性（建议）

- OTEL_SERVICE_NAME：
- traceId（dev 抽样）：
- Tempo / Loki：有 / 无

## 涉及文件

- ...
