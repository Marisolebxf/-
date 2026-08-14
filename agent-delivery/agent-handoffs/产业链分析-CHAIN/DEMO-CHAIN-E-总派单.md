# 段 E · 产业链闭环冒烟总派单

> **日期**：2026-08-14  
> **监管**：`human:淮政玮`（无人值守，见 [A–E 总控](./DEMO-CHAIN-ABCD-长任务总控.md)）  
> **规约**：[`长任务执行规约.md`](../../长任务执行规约.md) §11  
> **缺陷包**：[`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)  
> **薄条**：[`DEMO-CHAIN-E-派单条.md`](./DEMO-CHAIN-E-派单条.md)

本段 **2 张固定单** + 按需 bugfix。禁止给 A–D 每一叶再派 QA。QA **不改业务代码**。只认 **K8s dev 已发布** `lumen-ui-topic`。

---

## 0. 已拍板

| 项 | 值 |
|----|-----|
| 粒度 | 整条 A–D **末尾一次** |
| 环境 | 禁止 localhost / `pnpm dev` |
| 金路径 | 总控 §4 五条 |
| 修 bug | 缺陷包（必含 `X-Trace-Id`）测试驱动 **coordinator** 派 frontend / api / algorithm |
| 循环 | 同一故事最多 3 轮；cost $10/$20 硬闸 |

---

## 1. E0 · `LUMEN-CHAIN-E-DEVOPS-L01`

**执行**：`devops-agent`  
**依赖**：`LUMEN-CHAIN-FE-WORKSPACE-L01`（联调闸门即可，不等 `done`）  
**一句话**：本次冒烟需要的镜像已在 `dev` 健康发布。

点名服务：

- `lumen-ui-topic`
- `lumen-svc-platform`（chain 门面 + async-service）
- `lumen-algo-py`

核对：Pipeline 绿或 waiver；`kubectl rollout` 健康；URL 是 lumen 不是 `demo-*`；库 `demo_gkxlumenx_*`。未绿 `blocked`，E1 不开工。不写业务代码。

---

## 2. E1 · `LUMEN-CHAIN-E-QA-SMOKE-L01`

**执行**：`qa-agent`  
**依赖**：E0  
**一句话**：已发布前端走五条 USM 金路径。

金路径见总控 §4。**期望未发生必红**。红了先 **失败分类 C1–C6**（规约 §11.4）：#4 未到 succeeded → **C1 FAIL**，不得标 C3。C1 → 缺陷包 → coordinator 派修 → 再 E0 → 只复测失败故事。

---

## 3. `/goal` 头

```text
/goal
监管：human:淮政玮
强度：ponytail full
必读：DEMO-CHAIN-ABCD-长任务总控.md §4 · 长任务执行规约.md §11 · observability.md §9
禁止：改业务代码（E0/E1）；localhost 当证据；无 X-Trace-Id 开修；逐叶再派 QA。
```

E0：`claimed_by=agent:devops-agent` · E1：`claimed_by=agent:qa-agent` · `lock_hours=24`
