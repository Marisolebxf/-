# 段 E · SVC 闭环冒烟总派单

> **监管**：`human:侯佳伟` · 总控已授权  
> **强度**：ponytail **full**（devops/qa）  
> **总控**：[DEMO-SVC-ABCD-长任务总控.md](./DEMO-SVC-ABCD-长任务总控.md) §4

## 铁律

- 只点 K8s **已发布**前端；禁 localhost  
- QA **不改**业务代码；期望未发生必红  
- 失败先分类 C1–C6；C1 由 coordinator 派修  

## 叶

| ID | 角色 | 一句话 |
|----|------|--------|
| `LUMEN-SVC-E-DEVOPS-L01` | devops-agent | 点名服务 deploy 绿 = E0 |
| `LUMEN-SVC-E-QA-SMOKE-L01` | qa-agent | 金路径冒烟；CI 可后补 `e2e:svc-gold` |

E0 点名：`lumen-ui-topic` · `gkxlumen-topic-svc` · `gkxlumen-topic-async-service` · `lumen-topic-py` · `lumen-algo-py`
