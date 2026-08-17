# LUMEN-SVC-E-DEVOPS-GATEWAY-SVC-C1 · 网关已通；根因转 Python 路由挂载

> 日期：2026-08-17  
> Task：`LUMEN-SVC-E-DEVOPS-GATEWAY-SVC-C1`（根因重分类 → algorithm / topic-py）  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h（长任务） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小改动：同进程挂载已有 router；不新建 K8s Service、不改 Feign URL |

## 结论（重要）

**网关侧已通，无需再改 gateway/Nacos `/svc` 路由。**

外网证据（`http://111.198.38.90:50892`）：

| 探测 | 结果 | 含义 |
|------|------|------|
| POST `/api/svc/topic/v1/service/health` | **405** `path=/topic/v1/service/health` | StripPrefix 已剥 `/svc`，打到 `gkxlumen-topic-svc`；health 为 GET |
| GET `/api/svc/topic/v1/service/health` | HTTP 200 · `code=1` · `msg={"detail":"Not Found"}` | Java 门面已通；Feign 下游 FastAPI **404** |
| `/api/chain` health | 200 ok | 对照链正常 |

**根因**：`python-base-url` / Helm `GKXLUMEN_TOPIC_SVC_PYTHON_BASE_URL` = `http://gkxlumen-platform-search-py:8080`，但 search-py 只跑 `gkx_search_service.main`，**未挂载** `/internal/gkx-svc/**`（该前缀在独立包 `gkx_svc_service`，镜像亦未 COPY）。Feign POST `/internal/gkx-svc/health` → FastAPI `{"detail":"Not Found"}` → Java `R.failed` 原样回传。

| 核对项 | 结果 |
|--------|------|
| Feign 路径 | ✅ `RemoteSvcPythonClient` → `/internal/gkx-svc/**`（POST） |
| Nacos/Helm base URL | ✅ 指向 `gkxlumen-platform-search-py:8080`（与 enterprise 同策略） |
| K8s 服务名 | ✅ `gkxlumen-platform-search-py` 存在；**缺的是路由挂载** |
| Python 路由 | ❌ 修复前未在 search 进程注册；已修 |

## 修改内容

1. `gkx_search_service/main.py`：`include_router` boot/search/task（`gkx_svc_service.views`）
2. `docker/Dockerfile.search`：`COPY gkx_svc_service/`
3. `tests/test_gkx_svc_mounted_on_search.py`：search app 上 health / search/orgs / portal/overview
4. `docs/DEPLOY-K8S.md`：注明同进程挂载约定

**未改**：gateway、Nacos `python-base-url`、Java Feign（接线正确）。

## 测试结果

- 本地：`pytest tests/test_gkx_svc_mounted_on_search.py tests/test_gkx_svc_boot.py` → **13 passed**
- 外网修前：GET health → `detail Not Found`（已复现）
- 外网修后：待 search-py **image + deploy** 滚出后复测：
  - GET `/api/svc/topic/v1/service/health` → `code=0`，`data.domain=svc`
  - POST `/api/svc/topic/v1/service-portal/overview` → `code=0`（可 mock）
  - POST `/api/svc/topic/v1/service/search/orgs` → `code=0`，`items` 列表（可 mock）

## CI/CD

- 仓：`lumen-topic-py` · 分支 `dev`
- commit：`85a8fd9`（+ 后续 DEPLOY 文档若另 commit）
- 需滚出：`py:image:search` → `deploy:search-py`（或等价 FULL_PIPELINE）
- 部署后验证基址：http://111.198.38.90:50892/

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→Python `/internal/*` | ✅ 未越层 |
| D12 | 禁止 Feign demo-* | ✅ 仍指向 lumen search-py |
| 可观测 | TraceHeaderMiddleware 仍在 search app | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~3 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 遗留风险

- search-py 镜像未滚出前外网仍 Not Found
- gkx-svc 读面仍为 Mock 包络（诚实空/待核验可接受）；ADS 真数另叶
- 本机无 task-registry MCP；registry 状态请 coordinator 代写 integration / 关 GATEWAY 网关假因

## 联调确认

联调确认：网关 `/svc` 已通；根因=Python search-py 未挂 `/internal/gkx-svc/**`；代码已修，等 deploy 后外网 POST overview / search/orgs 不应再 `detail Not Found`。
