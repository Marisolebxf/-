# API handoff · E-PLATFORM-P0-L02 指标注册中心 gkxlumen-metrics

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L02 |
| Epic | E-PLATFORM-P0 |
| 角色 | api-agent |
| 仓库 | `lumen-svc-platform`（backend.lumen） |
| 分支 | `feat/E-PLATFORM-P0-L02` |
| 日期 | 2026-06-20 |
| **mvn / CI** | **deferred（PM pipeline waiver v2）** — 本地未跑 `mvn package`，未等待 CI 绿 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 产物 |
|--------|------|------|
| gkxlumen-metrics 模块存在 | ✅ | `gkxlumen-metrics/` |
| GET `/metrics/v1/catalog` 返回指标元数据 | ✅ | `MetricCatalogController` + `MetricCatalogService` |
| 指标字典表 + 口径/version 字段 | ✅ | `scripts/sql/gkx/gkx_cfg.sql`（cfg_metric D9 8 件套 + version） |
| OpenAPI 片段 | ✅ | `gkxlumen-metrics/docs/openapi-metrics-v1.yaml` |
| push → CI backend:build 绿 | ⏸️ **deferred** | PM waiver v2；待 L02b CI 稳定后由 devops/coordinator 触发 |

## 产物清单

| 路径 | 说明 |
|------|------|
| `gkxlumen-metrics/pom.xml` | 微服务模块（Undertow + JDBC + Nacos + common-security/data/log/swagger） |
| `gkxlumen-metrics/src/main/java/.../GkxlumenMetricsApplication.java` | 启动类，端口 7091 |
| `gkxlumen-metrics/.../controller/MetricCatalogController.java` | `GET /metrics/v1/catalog` |
| `gkxlumen-metrics/.../service/MetricCatalogService.java` | catalog 过滤 + auto/seed/db 数据源切换 |
| `gkxlumen-metrics/.../support/MetricsDao.java` | 只读 JdbcTemplate，snake→camel |
| `gkxlumen-metrics/src/main/resources/metrics/registry/cfg_metric-ENT-seed.json` | ENT 49 条种子（自 agent-delivery YAML 转换） |
| `gkxlumen-metrics/src/main/resources/application.yml` | gkx_cfg 数据源 + `METRICS_CATALOG_SOURCE` |
| `gkxlumen-metrics/openapi/openapi-metrics-v1.yaml` | OpenAPI 3 catalog 契约 |
| `gkxlumen-metrics/Dockerfile` | K8s 镜像（7091） |
| `scripts/sql/gkx/gkx_cfg.sql` | cfg_metric / cfg_metric_lineage DDL（对齐 P0-L01） |
| `pom.xml` | 父 reactor 注册 `<module>gkxlumen-metrics</module>` |

## API 契约摘要

**端点**：`GET /metrics/v1/catalog`

**过滤参数**（可组合）：

| 参数 | 说明 |
|------|------|
| `ids` | 逗号分隔 metric_id 精确匹配 |
| `element` | 要素域，如 ENT |
| `idPrefix` | metric_id 前缀，如 M_ENT_ |
| `mappingStatus` | ✅/🔧/⚠️/❌ |

**响应**：`R<{ total, element, seedVersion, batch, source, list[] }>`，`list[]` 含 D9 8 件套（metricId / metricNameZh / definition / formula / sourceTables / sourceSystems / updateFreq / version）及治理字段（mappingStatus / isMock / bidRef 等）。

**数据源策略**（Wave 0）：

| 模式 | 配置 | 行为 |
|------|------|------|
| auto（默认） | `gkxlumen.metrics.catalog-source=auto` | DB 可用读 `gkx_cfg.cfg_metric`，否则 fallback classpath 种子 |
| seed | `METRICS_CATALOG_SOURCE=seed` | 强制读 `cfg_metric-ENT-seed.json` |
| db | `METRICS_CATALOG_SOURCE=db` | 强制读 MySQL |

## 与 L03 并行隔离

| 区域 | L02（本任务） | L03 | 隔离 |
|------|--------------|-----|------|
| 模块 | `gkxlumen-metrics` | Python graph `/internal/graph/*` | 不同仓/语言 |
| merge 优先级 | L03 优先 | — | merge 时 L03 先合 |

## 架构合规自检（§2 十条）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 算法只在 Python | ✅ 仅读 cfg_metric 元数据，无 NLP/图算法 |
| 2 | 调用链不越层 | ✅ 对外 REST，读 gkx_cfg 只读 |
| 7 | 共享聚合核心 | ✅ gkxlumen-metrics 为指标注册出口 |
| 8 | D7 数据契约 + Mock | ✅ Wave 0 classpath 种子；DB 就绪后 auto 切换 |
| 10 | D9 血缘 8 件套 | ✅ catalog 返回 8 件套 + isMock 供 🧪 |
| 5 | 可观测性 | ✅ Helm gateway 已预置 `/metrics/**` 路由；OTEL 随 L02b 基座 |

## 偏离说明

| 项 | 说明 |
|----|------|
| mvn package / CI | PM pipeline waiver v2：本地 Maven 3.6 与 compiler-plugin 3.14 不兼容，**未跑构建**；CI 验证 deferred |
| cfg_metric 物理 INSERT | 49 条仍在 YAML/JSON 种子；DB INSERT 脚本待 data-agent Wave1 |
| `/metrics/v1/lineage/{id}` | 未在本任务范围；后续 task 扩展 |

## 接力清单

| 下游 | 动作 |
|------|------|
| **devops / coordinator** | CI 绿后启用 Helm `microservices.metrics.enabled=true` |
| **ui-agent P0-L07** | MetricSpecCard 调 `/metrics/v1/catalog?ids=` |
| **data-agent** | cfg_metric 49 条 INSERT → gkx_cfg；切 `METRICS_CATALOG_SOURCE=db` |
| **qa-agent P0-L05** | dev 网关 GET `/metrics/v1/catalog` 冒烟 |

## cost 回填

| 字段 | 值 |
|------|-----|
| estimated_tokens | 300_000 |
| actual_tokens | 120_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.24 |
| cost_warn | green |

## git

- 分支：`feat/E-PLATFORM-P0-L02`
- commit：`066643b`（主交付 `ceb9ae4` + OpenAPI `066643b`）
- push：✅ `origin/feat/E-PLATFORM-P0-L02`（2026-06-20）

---

*handoff · api-agent · E-PLATFORM-P0-L02 · mvn/CI deferred per PM waiver v2*
