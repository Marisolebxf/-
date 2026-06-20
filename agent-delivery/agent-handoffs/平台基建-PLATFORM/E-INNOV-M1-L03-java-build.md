# Java handoff · E-INNOV-M1-L03 gkxlumen-innov 模块移植

| 项 | 值 |
|---|---|
| 任务 | E-INNOV-M1-L03 |
| Epic | E-INNOV-M1 |
| 角色 | api-agent |
| 仓 | `F:/gkx-lumen/repos/lumen-svc-platform` |
| 分支 | `feat/E-INNOV-M1-L03` |
| 基线 | `feat/E-INNOV-M1-L02b` |
| 参考 | `F:/gkx-lumen/repos/demo-svc-platform/gkx-innov` |
| 日期 | 2026-06-20 |
| Pipeline | **deferred** — 见 `PIPELINE-WAIVER-2026-06-20.md` v2 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| 从 demo `gkx-innov` 移植为 `gkxlumen-innov` | ✅ | 包名 `com.topcomm.gkxlumen.innov`；依赖 `gkxlumen-common-*` |
| InnovDao 只读 ADS（主表 `ads_innovation_event`） | ✅ | `InnovDao` + `EventController` 等 Controller 仅 JdbcTemplate 查询，无写操作 |
| 禁止 NLP/模型/图谱算法 | ✅ | 无算法依赖；图谱相关接口只读 ADS/DWM 表，不直连 Nebula |
| `OTEL_SERVICE_NAME=gkxlumen-innov` | ✅ | `helm/gkxlumen-platform/values.yaml` → `microservices.innov.env` |
| `mvn package` / `backend:build` 绿 | 🟡 **deferred** | PM waiver v2：本地 mvn 与 GitLab CI 均不阻塞本任务签收 |
| push `feat/E-INNOV-M1-L03` | ✅ | 见下方 commit |

## 产物清单

### lumen-svc-platform

| 路径 | 说明 |
|------|------|
| `gkxlumen-innov/pom.xml` | 独立 Spring Boot 微服务模块 |
| `gkxlumen-innov/Dockerfile` | 7090 端口；OTel JavaAgent |
| `gkxlumen-innov/src/main/java/.../GkxlumenInnovApplication.java` | 入口；`@EnableGkxlumenResourceServer` |
| `gkxlumen-innov/src/main/java/.../support/InnovDao.java` | snake_case→camelCase；JSON 列反序列化 |
| `gkxlumen-innov/src/main/java/.../controller/*.java` | M1–M5 REST（events/graph/carriers/cities/forecast/dict） |
| `gkxlumen-innov/src/main/resources/application.yml` | innov 库只读 datasource；Nacos |
| `pom.xml` | 根模块列表新增 `<module>gkxlumen-innov</module>` |
| `helm/gkxlumen-platform/values.yaml` | `OTEL_SERVICE_NAME=gkxlumen-innov` |

### API 路由约定（L04 集成）

- 网关：`/innov/**` → `lb://gkxlumen-innov`，StripPrefix=1（已在 `configs/gkxlumen-gateway-dev.yml`）
- 本服务路径：`/v1/**`（如 `/v1/events`）

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 算法只在 Python | ✅ Java 无 NLP/推理/图谱计算 |
| D2 调用链 前端→Java→Python | ✅ 本模块只读 MySQL ADS |
| D3 NebulaGraph（禁止 Neo4j） | ✅ Java 不直连 nGQL |
| D4 可观测性 OTel | ✅ Dockerfile + helm OTEL_SERVICE_NAME |
| D6 demo2 只读 merge | ✅ 仅在 lumen 正式仓开发 |
| D8 前端规范 | N/A（本任务后端） |
| D9 数据血缘 | 🟡 Wave 0；统计接口待 UI 接 MetricSpecCard（L07+） |

## 测试结果

| 项 | 结果 |
|----|------|
| 本地 `mvn package` | **跳过**（PM PIPELINE-WAIVER-2026-06-20 v2） |
| GitLab `backend:build` | **未等待**（同 waiver） |
| 静态审查 | ✅ 无算法类依赖；InnovDao/EventController 仅 SELECT |

## 遗留与下一任务

- **L04** integration-agent：启用 helm `microservices.innov`、K8s dev 部署、网关 StripPrefix 冒烟
- **补验** qa-agent + devops-agent：waiver 关闭后跑 `mvn package` + CI + `:7090` 健康检查

## 涉及文件

- `F:/gkx-lumen/repos/lumen-svc-platform/gkxlumen-innov/**`
- `F:/gkx-lumen/repos/lumen-svc-platform/pom.xml`
- `F:/gkx-lumen/repos/lumen-svc-platform/helm/gkxlumen-platform/values.yaml`
