# 段 E 缺陷包 · US-CHAIN-DIAG-03 → 04

> 规约：`长任务执行规约.md` §11.3 / §11.4 / §11.5.1。coordinator 确认分类后派修。  
> 关联 E1：`LUMEN-CHAIN-E-QA-SMOKE-L01.md`（原 ALL_PASS 已按「期望未发生必红」改判本条 FAIL）。

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `DEMO-CHAIN-ABCD-长任务总控.md` §4 #4 |
| 故事 ID | `US-CHAIN-DIAG-03` → `US-CHAIN-DIAG-04` |
| 已发布 URL | http://10.50.69.111:30892/industry-center/diagnosis?tab=key-link |
| 操作步骤 | 登录已发布前端 → 产业周期/关键环节 → 选集成电路 / 集成电路设计 → 开始分析 |
| 期望 | 配置→生成→过程→**succeeded 后 wait_view 点查看结果**；禁止自动跳结果。空态列：**无** |
| 实际现象 | Create 200，task `CHAIN-20260814-009`；events 节点 `freeze` **failed**（约 1s）；过程页红标失败，未到 succeeded，wait_view 未测到 |
| HTTP / 页面态 | Create/detail **非 5xx**；Job **failed** |
| **失败分类** | **C1 产品/代码**（coordinator 确认）。不是 C3 |
| **X-Trace-Id** | Create `521c5d529045618049844db2edf4bb11`；detail `67b8349bae7a310ca7de2702dd117c83` |
| Tempo | http://10.50.69.111:30201/api/traces/521c5d529045618049844db2edf4bb11 · Grafana http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf） 数据源 Tempo |
| Loki | algo-py OTLP collector DNS 残差，Create 链路 **无** Python span；Java async **200** `POST /internal/v1/analysis-jobs/CHAIN-20260814-009/stages` 与 `/complete` |
| 怀疑层 | **Python**（`key_link.node_freeze`）。Java 契约只校验 `factors.user_confirmed`（`ChainAnalysisAdapterImpl` + 单测无 `items`）；前端 `buildChainCreateRequest` 同样只带 `user_confirmed`，**不传三因子 items**。freeze 却要求 `REQUIRED_FACTORS ⊆ items[status=ready]` → 极可能 `VALIDATION_FACTORS_UNAVAILABLE` |
| 诚实空态？ | **否**（总控该行不允许把 Job failed 当空态） |

```text
/goal
你是经验丰富的 algorithm-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
监管：human:淮政玮
仓：lumen-algo-py · 分支 origin/dev
claim_type：coordinator_dispatch · lock 24h
必读：本缺陷包 + DEMO-CHAIN-ABCD-长任务总控.md §4 #4 + DEMO-CHAIN-PY-JOB-KEY-LINK-L01.md + observability.md §9
禁止：改无关仓；无闸门写正式库；问用户选仓；把失败收成诚实空态；新建 fullstack 角色。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
```
