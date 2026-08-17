# LUMEN-SVC-JAVA-FACADE-L01 · 产业服务链 C — gkxlumen-topic-svc 门面

> 日期：2026-08-17  
> Task：`LUMEN-SVC-JAVA-FACADE-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对齐 topic-chain 最小 api+biz；Feign 仅 `/internal/gkx-svc/**` |

## 范围与实现

- 新建 `gkxlumen-topic-svc`（api+biz），端口 **7096**
- REST：`/topic/v1/service/**` · `/topic/v1/service-portal/**`
- 网关：`Path=/svc/**` → `lb://gkxlumen-topic-svc-biz`
- Feign：`RemoteSvcPythonClient` → `${gkxlumen.topic.svc.python-base-url}`（默认 search-py / 本地 8088）
- 父 POM / ServiceNameConstants / Helm values / gateway-dev / CI image+deploy / 路由 SQL
- MockMvc：`ServiceFacadeControllerTest`
- **非范围**：async Job（JAVA-JOB 叶）；前端

## 偏离说明

- 本机 Maven 版本过旧，未能本地跑通 `mvn test`（compiler-plugin 要求 ≥3.6.3）；契约测试已写入，待 CI 验证。
- `values-lumen.yaml` 已 `topic-svc.enabled: true`（与 chain 同策略）；若未发 search-py 挂 gkx-svc，需合 topic-py MR 后启进程。

## 产物清单

| 产物 | 路径 |
|------|------|
| 模块 | `repos/lumen-svc-platform/gkxlumen-topic-svc/**` |
| 路由 SQL | `repos/lumen-svc-platform/db/9x_gkxlumenx_sys_route_conf_topic_svc.sql` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-JAVA-FACADE-L01.md` |

## 验收证据

- [x] 模块/网关/Helm/CI 接线落盘
- [ ] CI `backend:build` 绿（待 push）
- [x] MockMvc 测试源码就位

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python | ✅ |
| D12 | Feign 禁 demo-* | ✅ |
| 算法 | Java 不写算法 | ✅ |
| ADS | 只读意图（本叶透传 Python） | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~6 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## 联调确认

联调通过（代码侧）：门面契约与网关前缀就绪，可对接已发布 gkx-svc。下一叶：`LUMEN-SVC-JAVA-JOB-L01`（依赖 MIDDLE-TASK + SVCAN）；前端 ENTRY 可升 ready。
