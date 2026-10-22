# DEVOPS-LUMEN-TOPIC-PY-SHOW-L01 · lumen-topic-py — 新增 gkx_show_service 展示系统 Python 服务骨架（架构/部署复刻 gkx_search_service）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent`（架构会话代行，授权来源 human:徐滕强 2026-10-22 会话直接授权） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 骨架最小实现：仅 main/deps/meta 样板 + 部署三件套 + 4 用例；未加未请求的抽象；D12 隔离自检纳入测试 |

## 任务背景

给展示系统增加底层 Python 服务，与专题系统 `gkx_search_service` 隔离（D12）。空项目骨架，供研发同学后续开发业务接口。项目名经用户拍板：`gkx_show_service`（对齐仓内 `gkx_search_service`/`gkx_svc_service`/`gkx_ai_service` 命名惯例）。

## 修改内容

- `gkx_show_service/`：FastAPI 骨架
  - `main.py`：app 入口，`/healthz` + `/` 根信息 + `/internal/gkx-show/**` 前缀；复用 `gkx_common` observability（JSON 日志 + OTel Trace 中间件）与 response（`{code,msg,data}` 包络）；`RealDataUnavailable` → 503 异常处理器（禁静默回退 Mock，对齐 search 模式）
  - `views/meta.py`：`POST /internal/gkx-show/meta/ping` 样板（研发新增业务接口参考）
  - `deps.py`：`RealDataUnavailable` 占位（接库时参照 `gkx_search_service/deps.py`）
- `docker/Dockerfile.show`：镜像 `gkxlumen-show-service`，端口 **8082**（search 8080 / ai 8081 之外顺延），python-algo-base + opentelemetry-instrument，与 Dockerfile.search 同模式；不需要 COPY conf/（骨架不触发 AppConfig）
- `k8s/dev-show-py.yaml`：bootstrap（Service+Deployment `gkxlumen-platform-show-py`，ClusterIP:8082，探针 /healthz）；**骨架期 env 最小化**：仅 GKX_MOCK_ENABLED + OTEL 全套；未放任何 MySQL/ES 凭证（对齐 D14，研发接库时走 K8s Secret——存量 dev-search-py.yaml 明文口令是历史债，本单不扩散该模式）
- `.gitlab-ci.yml`：`py:smoke` PYMODS 与 pytest 列表加入 show；新增 `py:image:show` 与 `deploy:show-py`（HEALTH_PORT=8082）；头注释补 show-py 行
- `tests/test_gkx_show_boot.py`：4 用例——healthz / 根信息 / ping 包络 / **D12 隔离自检**（show 进程路由不得含 `/internal/gkx-search`、`/internal/gkx-svc`）
- `docs/DEPLOY-K8S.md`：资源命名表补 show 条目 + 新增「展示系统 gkx-show-service（独立进程）」章节

## 与参考项目的对照（完全复刻 gkx_search_service 模式）

| 维度 | gkx_search_service（参考） | gkx_show_service（本单） |
|------|---------------------------|--------------------------|
| 进程/端口 | 独立 uvicorn :8080 | 独立 uvicorn :8082 |
| 路由前缀 | /internal/gkx-search/** | /internal/gkx-show/** |
| 镜像 | gkxlumen-search-service | gkxlumen-show-service |
| K8s 资源 | gkxlumen-platform-search-py | gkxlumen-platform-show-py |
| 共享层 | gkx_common（同仓复用） | gkx_common（同仓复用） |
| 路由互挂 | 挂载 gkx-svc | **零互挂**（测试强制） |
| env 策略 | 明文口令进 git（历史债） | 最小化 + Secret 待接库（D14 合规） |

## 测试结果

- `pytest tests/test_gkx_show_boot.py`：**4 passed**（healthz / root / ping / D12 隔离）
- `GKX_MOCK_ENABLED=1 python -c "import gkx_show_service.main"`：OK（兼容 CI smoke 环境）
- `k8s/dev-show-py.yaml` / `.gitlab-ci.yml`：YAML 解析合法

## CI/CD（必填）

- 分支：`dev`（直推，2026-08-17 human:淮政玮 确认的仓分支策略）
- commit：`4b867f8`（`feat(show): 新增 gkx_show_service 展示系统 Python 服务骨架 [agent:devops-agent]`）
- pipeline URL / ID：pipeline **2702**（https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/2702）—— `py:smoke` success、`py:image:show` success
- 部署 namespace / 镜像 tag：`zhipu-tts` / `harbor.test.com/zp-tts/gkxlumen-show-service:4b867f89`
- K8s rollout：**成功**（`service/gkxlumen-platform-show-py created`、`deployment.apps/gkxlumen-platform-show-py created`、`deployment successfully rolled out`）
- dev 测试 URL / 命令与结果：deploy job 内 in-pod 探活 `wget http://127.0.0.1:8082/healthz` → `{"status":"ok","service":"gkx-show-service","mock_enabled":false,"data_source":"none","writes_ads":false}`；集群内 DNS `http://gkxlumen-platform-show-py:8082`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-show-service`
- OTLP endpoint：`http://gkxlumen-platform-otel-collector:4318`（traces/metrics/logs 全 otlp，与 search-py 同链路）

## 架构合规自检（公约 §2 铁律逐条）

| 铁律 | 结果 |
|------|------|
| D1 算法只在 Python | ✅ 本服务即 Python；未引入 Java 算法 |
| D2 调用链 前端→Java→Python /internal/* | ✅ 路由前缀 /internal/gkx-show/**，供 Java Feign；不经网关直暴 |
| D3 NebulaGraph | ✅ 骨架未接图谱；后续接时用 gkx_common.nebula（10.50.75.136:9669） |
| D4 可观测性 | ✅ OTel instrument + TraceHeaderMiddleware + JSON 日志（必加项已加） |
| D12 demo/lumen 隔离 | ✅ 独立进程/镜像/K8s 资源；测试强制零互挂；不碰 demo 制品 |
| D14 对象存储 | ✅ 骨架未接桶；K8s YAML 无凭证进 git |
| CI/CD push→绿→K8s dev rollout | ✅ pipeline 2702 全绿 + rollout 成功 + 探活 ok |

## 遗留风险 / 后续

- 骨架期 `/healthz` 恒 ok（未探测依赖）；研发接数据源后需参照 `gkx_search_service.healthz` 增加依赖探测，避免假活
- `gkx_show_service/deps.py` 目前只有异常类占位；接 MySQL/ES 时补 get_xxx 依赖注入函数
- K8s env 目前最小化；接库时**必须**走 K8s Secret（勿照抄 dev-search-py.yaml 的明文口令历史债）
- Java 侧 Feign 对接、网关路由未做（属后续业务单；本单边界 = Python 骨架 + 部署验证）
- 本机到 K8s apiserver（172.18.3.194:6443）网络不通，K8s 侧证据以 CI deploy job 日志为准（rollout + in-pod 探活均成功）

## 涉及文件

- `gkx_show_service/__init__.py` `main.py` `deps.py` `views/__init__.py` `views/meta.py`
- `docker/Dockerfile.show`
- `k8s/dev-show-py.yaml`
- `.gitlab-ci.yml`（smoke/image/deploy 三处 + 头注释）
- `tests/test_gkx_show_boot.py`
- `docs/DEPLOY-K8S.md`
