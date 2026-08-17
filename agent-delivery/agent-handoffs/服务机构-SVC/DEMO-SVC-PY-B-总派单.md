# 段 B · SVC Python（中间层 + svcan）总派单

> **监管**：`human:侯佳伟` · 总控已授权  
> **仓**：`lumen-topic-py`（中间层）· `lumen-algo-py`（svcan）· `origin/dev`  
> **强度**：ponytail **full**  
> **总控**：[DEMO-SVC-ABCD-长任务总控.md](./DEMO-SVC-ABCD-长任务总控.md)

## 铁律

- 中间层：`/internal/gkx-svc/**`；算法：`svcan/` + 任务契约  
- 不对前端暴露 `/internal`；不自签 `result_snapshot_id`（Job 真源 Java）  
- 同仓 Convoy：同时只一张 coding 单  

## 叶

| ID | 仓 | 一句话 |
|----|-----|--------|
| `DEMO-SVC-PY-MIDDLE-BOOT-L01` | lumen-topic-py | `/internal/gkx-svc/**` 骨架 + 健康检查 + Mock 包络 |
| `DEMO-SVC-PY-MIDDLE-SEARCH-L01` | lumen-topic-py | 搜索/门户/画像读 ADS·ES（或 Mock）稳定契约 |
| `DEMO-SVC-PY-MIDDLE-TASK-L01` | lumen-topic-py | 任务 create/status/callback 适配 → algo |
| `DEMO-SVC-PY-SVCAN-BOOT-L01` | lumen-algo-py | `svcan/` 启动 + 样板键（短板/图可后扩） |

## /goal 头

```
任务：{ID}
仓：{lumen-topic-py|lumen-algo-py} · origin/dev
监管：human:侯佳伟 · coordinator_dispatch · lock 24h
强度：ponytail full
必读：总控 · 本总派单 · storage/SVC/stores/**
```
