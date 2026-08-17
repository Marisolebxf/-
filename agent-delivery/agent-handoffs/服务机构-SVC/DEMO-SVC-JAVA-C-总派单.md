# 段 C · SVC Java（lumen-svc-platform）总派单

> **监管**：`human:侯佳伟` · 总控已授权  
> **仓**：`${GKX_ROOT}/repos/lumen-svc-platform` · `origin/dev`  
> **执行**：`api-agent` · **强度**：ponytail **full**  
> **总控**：[DEMO-SVC-ABCD-长任务总控.md](./DEMO-SVC-ABCD-长任务总控.md)

## 0. 模块落点（已拍板，勿问）

| 能力 | 落点 | 不要 |
|------|------|------|
| 服务机构查询/门户/分析读面 | **新建 `gkxlumen-topic-svc`**（api+biz），对齐 `gkxlumen-topic-chain` | 塞进裸 `gkxlumen-topic`；复制 demo 透传 |
| 生成分析 Job | **扩展 `gkxlumen-topic-async-service`** | 新建第三套任务微服务 |
| Feign | **仅** `lumen-topic-py` `/internal/gkx-svc/**` | Feign `lumen-algo-py` 或 `demo-svc-topic-py` |
| ADS | Java **只读** `demo_gkxlumenx_ads`（联调） | 扫 DWD；写 ADS；直连 nGQL |

父 POM / boot / 网关：`/topic/v1/service/**` + `/topic/v1/service-portal/**` → svc 服务。

## 叶

| ID | 依赖（联调闸门） | 一句话 |
|----|------------------|--------|
| `LUMEN-SVC-JAVA-FACADE-L01` | MIDDLE-SEARCH | 专题前端经 Java 查机构/门户/画像壳 |
| `LUMEN-SVC-JAVA-JOB-L01` | MIDDLE-TASK + SVCAN-BOOT | 分析任务进 async-service；签发 snapshot；wait_view |

## /goal 头

```
任务：{ID}
仓：lumen-svc-platform · origin/dev
监管：human:侯佳伟 · coordinator_dispatch · lock 24h
强度：ponytail full
必读：总控 · 本总派单 · CHAIN JAVA-C 总派单（切法对照）
```
