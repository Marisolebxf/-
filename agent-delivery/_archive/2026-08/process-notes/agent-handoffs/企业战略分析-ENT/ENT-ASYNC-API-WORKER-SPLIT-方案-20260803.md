# 算法侧异步架构落地方案（API/Worker 拆分 + MySQL 建表）

> 日期：2026-08-03  
> 提出人：唐绍祖（算法侧）  
> 对齐人：徐滕强（架构/Python svc）  
> 背景：滕强要求“异步不能影响同步”，同步收单接口与真正的异步分析必须资源隔离。

---

## 1. 结论

1. 算法侧代码已经按 **API 进程 + Worker 进程** 拆分，不需要重写异步框架。
2. 当前主要缺口是 **部署没有真正拆开**：Worker 没有独立 Deployment，MySQL 任务表也没有建。
3. 本次先完成：MySQL 建表、API/Worker 独立部署、回调可靠性、science filter 模式修正。
4. 如后续需要更强解耦，再评估算法侧引入 RabbitMQ；本期继续用 MySQL 任务表 + Worker 轮询。

---

## 2. 执行状态（2026-08-03 更新）

| 项 | 状态 |
|---|---|
| MySQL 三张任务表 | ✅ 已建并验证 |
| entan/science API + Worker 部署清单 | ✅ 已提交 `deploy/k8s/` |
| CI 热更新同时更新 API/Worker | ✅ 已改 `.gitlab-ci.yml` |
| Worker 健康检查端口 | ✅ 已实现 `:8001/healthz` |
| Webhook 重试 + callback_url 必填 | ✅ 已实现 |
| 对外状态统一 running | ✅ 已实现 |
| science filter 候选解析 | ✅ 已实现 |
| camelCase 权重兼容 | ✅ 已实现 |
| Worker 按 analysis_type 隔离 | ✅ 已实现 |
| 本地部署冒烟 | ✅ science + entan 全链路通过 |
| dev Helm 落地 | ⏳ 待运维在 demo-svc-platform / lumen-svc-platform 执行 |

---

## 3. 已执行项

已按 `database_env.yaml` 中的外网 MySQL 连接，在 `gkxlumenx_cfg` 库执行：

```text
gkxlumenx_cfg.analysis_task
gkxlumenx_cfg.analysis_task_node
gkxlumenx_cfg.analysis_task_retry
```

DDL 来源：

```text
repos/demo-algo-ent-analysis/scripts/mysql/async_task_schema.sql
```

已通过 `SHOW TABLES` 验证三张表存在。两个算法仓共用这套表，不需要重复建。

---

## 4. 目标部署形态

### 3.1 企业评估（demo-algo-ent-analysis）

| 组件 | Deployment | 启动命令 | Service | 说明 |
|---|---|---|---|
| API | `demo-platform-entan-py` | `uvicorn api.main:app --host 0.0.0.0 --port 8000` | `demo-platform-entan-py:8000` | 只写 MySQL、立即返回 task_id |
| Worker | `demo-platform-entan-py-worker` | `python -m worker.main` | 不暴露 | 轮询任务、执行分析、发 Webhook |

### 3.2 风险洞察 / 引育推荐（demo-algo-science）

| 组件 | Deployment | 启动命令 | Service | 说明 |
|---|---|---|---|
| API | `demo-platform-innov-py` | `uvicorn api.main:app --host 0.0.0.0 --port 8000` | `demo-platform-innov-py:8000` | 只写 MySQL、立即返回 task_id |
| Worker | `demo-platform-innov-py-worker` | `python -m worker.main` | 不暴露 | 轮询任务、执行分析、发 Webhook |

### 3.3 资源建议

```yaml
# API：轻量，保证收单不被计算拖垮
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 1Gi

# Worker：重负载，可独立扩缩容
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2
    memory: 4Gi
```

Worker 内存/CPU 上限需要联调压测后调整，不能直接当最终值。

### 3.4 Worker 关键环境变量

```text
ENTAN_MYSQL_HOST / ENTAN_MYSQL_PORT / ENTAN_MYSQL_USER / ENTAN_MYSQL_PASSWORD
ENTAN_MYSQL_CFG_DB=gkxlumenx_cfg

INNOV_MYSQL_HOST / INNOV_MYSQL_PORT / INNOV_MYSQL_USER / INNOV_MYSQL_PASSWORD
INNOV_MYSQL_CFG_DB=gkxlumenx_cfg

GKX_ALGO_GLOBAL_CONCURRENCY=3
GKX_ALGO_TASK_TIMEOUT=3600
GKX_ALGO_MAX_RETRIES=3
GKX_ALGO_WORKER_POLL_INTERVAL=2
GKX_ALGO_WORKER_TIMEOUT_INTERVAL=60
```

### 3.5 部署 YAML 参考（Worker）

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-platform-entan-py-worker
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-platform-entan-py-worker
  template:
    metadata:
      labels:
        app: demo-platform-entan-py-worker
    spec:
      containers:
        - name: app
          image: harbor.htmisoft.net/gkx/gkx-entan-py:<tag>
          command: ["python", "-m", "worker.main"]
          envFrom:
            - configMapRef:
                name: demo-platform-entan-py
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2
              memory: 4Gi
```

science 侧把名字换成 `demo-platform-innov-py-worker`、镜像换成 `gkx-innov-py` 即可。

---

## 5. 任务项清单

| # | 任务项 | 负责方 | 说明 | 验收标准 |
|---|---|---|---|
| 1 | MySQL 建表 | 算法侧 / DBA | 在 `gkxlumenx_cfg` 建 `analysis_task` / `analysis_task_node` / `analysis_task_retry` | 三表存在，字段与 `async_task_schema.sql` 一致 |
| 2 | entan API/Worker 部署拆分 | 运维 / Java 编排 | Helm 增加 `demo-platform-entan-py-worker`，API 保持 `demo-platform-entan-py` | API 与 Worker 分别可用，Worker 无 Service |
| 3 | science API/Worker 部署拆分 | 运维 / Java 编排 | Helm 增加 `demo-platform-innov-py-worker`，API 保持 `demo-platform-innov-py` | API 与 Worker 分别可用，Worker 无 Service |
| 4 | Worker 资源配额与 HPA | 运维 | 按 §3.3 配置 requests/limits，后续压测调整 | 计算任务不影响 API 响应 |
| 5 | CI 热更新适配 | 运维 / 算法侧 | `.gitlab-ci.yml` deploy 同时更新 API 与 Worker Deployment | push 后两个 Deployment 都滚动更新 |
| 6 | 回调可靠性 | 算法侧 | `callback_url` 必填校验；`_fire_webhook` 失败重试；`callback_attempts` 落库 | 回调失败可重试，最终可达滕强侧 |
| 7 | science filter 模式修正 | 算法侧 | `selectionMode=filter` 允许 `filters` 传入，算法侧筛选候选企业 | REC 类任务可创建并成功 |
| 8 | 对外状态对齐 | 算法侧 | `create-and-start` 响应 `status` 对外统一为 `running` | 契约与 Java/Python 一致 |
| 9 | 本地/联调冒烟 | 算法侧 + 滕强 | 本地起 API + Worker，调用 `create-and-start`，观察节点、Webhook、结果 | 全链路成功 |
| 10 | dev 部署验证 | 运维 + 算法侧 | dev 环境验证 `/healthz`、任务创建、Worker 消费、回调 | REC 任务不再卡 running |

---

## 6. 代码修改项

### 5.1 回调可靠性

当前 `_fire_webhook` 是单次 `urllib` POST，失败只写日志，不重试。

修改目标：

```text
1. create-and-start 缺少 callback_url 时返回失败，或明确允许并记录无回调模式。
2. _fire_webhook 失败后按 1s/5s/15s 重试 3 次。
3. 仍失败则保留任务终态，并将回调状态写入 analysis_task，由周期任务重投。
```

### 5.2 science filter 模式

当前 `create_and_start` 强制 `enterprise_codes` 必填，但引育推荐 `filter` 模式请求只有 `filters`。

修改目标：

```text
selectionMode=filter 时：
  - 允许 enterprise_codes 为空
  - 算法侧根据 filters 查询候选企业池
  - compute 阶段再执行 attraction/cultivation
```

### 5.3 对外状态

```text
算法内部状态保留 pending；
create-and-start 响应、GET /gdf/tasks/{task_id} 对滕强/Java 统一返回 running。
```

---

## 7. 验证方案

### 6.1 本地冒烟

```bash
# entan
uvicorn api.main:app --port 8000
python -m worker.main

# science
uvicorn api.main:app --port 8000
python -m worker.main
```

然后调用：

```bash
curl -X POST http://127.0.0.1:8000/gdf/tasks/create-and-start \
  -H "Content-Type: application/json" \
  -d '{"task_id":"SMOKE-001","analysis_type":"enterprise_eval","sub_type":"technology","enterprise_codes":["ORG00000050"],"callback_url":"http://127.0.0.1:9090/callback"}'
```

验证：

```text
1. 返回 task_id，状态 running。
2. Worker 日志出现抢占任务。
3. 节点从 pending 变为 running/success。
4. 回调端点收到 step_started / step_completed / task_completed。
5. task_completed 带完整 result。
```

### 6.2 dev 环境验证

```bash
kubectl -n dev get pods | grep -E "entan|innov"
kubectl -n dev logs deploy/demo-platform-entan-py-worker --tail=50
curl http://demo-platform-entan-py:8000/healthz
curl http://demo-platform-innov-py:8000/healthz
```

### 6.3 存量 REC 任务

```text
REC-20260731-001 / REC-20260731-002 当前没有真正进入算法执行，
建议在链路修复前直接取消关闭，修复后再新建任务验证。
```

---

## 8. 后续可选优化

1. 算法侧从 MySQL 轮询升级为 RabbitMQ，获得更可靠的投递和背压控制。
2. Worker 多实例并发控制从进程内信号量升级为 Redis 分布式锁。
3. Worker 增加轻量 HTTP health 端口，便于 K8s liveness/readiness 探测。
4. 回调事件增加确认/死信机制，保证终态事件最终必达。
