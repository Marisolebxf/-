# 段 E · 派单条

> 厚包：[`DEMO-CHAIN-E-总派单.md`](./DEMO-CHAIN-E-总派单.md) · 总控：[`DEMO-CHAIN-ABCD-长任务总控.md`](./DEMO-CHAIN-ABCD-长任务总控.md)  
> 规约：[`长任务执行规约.md`](../../长任务执行规约.md) §11

| 项 | 值 |
|---|---|
| 环境 | K8s `dev` 已发布前端（禁止 localhost） |
| 监管 | `human:淮政玮` |
| 强度 | ponytail full |
| 锁 | 24h |

| ID | 执行 | 依赖 | 一句话 |
|---|---|---|---|
| `LUMEN-CHAIN-E-DEVOPS-L01` | devops-agent | D WORKSPACE 联调闸门 | 三服务 rollout 健康 |
| `LUMEN-CHAIN-E-QA-SMOKE-L01` | qa-agent | E0 | 五条 USM 金路径；不改代码 |

修单不预建；E1 FAIL 后按缺陷包 `task-create` `bugfix`。
