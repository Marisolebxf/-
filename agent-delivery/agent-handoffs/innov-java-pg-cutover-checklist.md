# Java innov 切 PG（demo_gdf_data / 117.50）改造清单

> **状态（2026-07-15）**：`demo-svc-platform` 的 `gkx-innov` + Helm `innov`/`innovPy` **已完成切 PG**。  
> 待办：部署后冒烟；可选同步 `gkxlumen-innov`。  
> 表名映射真源：`repos/demo-algo-science/scripts/sql/pg/innov_table_map.yaml`

## 0. 范围与不做

| 做 | 不做（本清单） |
|----|----------------|
| `demo-svc-platform/gkx-innov` JDBC + SQL + Helm | 改前端（仍只调 Java） |
| Helm `innov` + `innovPy` 环境变量对齐 `INNOV_PG_*` | 改平台库 `gkxx_boot` 等非 innov DS |
| 同步镜像改 `lumen-svc-platform/gkxlumen-innov`（可选第二波） | 产业链 Java 查库（本就 Feign → Python） |

---

## 1. 现状对照

| 组件 | 当前 |
|------|------|
| Python 科技/产业链 | ✅ `INNOV_PG_*` → `demo_gdf_data` |
| Python 企能 | ✅ `ENTAN_PG_*` → 同库 |
| Java `gkx-innov` | ❌ `INNOV_MYSQL_*` → `192.168.88.43/innov` |
| Helm innov / innovPy | ❌ 仍注入 `INNOV_MYSQL_*` |
| 访问方式 | JdbcTemplate 内联 SQL（无 MyBatis）；只读 |

Java **实际查询 19 张**旧表（无 `ods_*` / `gkx_chain_*`）。

---

## 2. 表名映射（Java 必改 19 张）

| 旧 MySQL | PG（1B+2B） |
|----------|-------------|
| `ads_innovation_event` | `ads.innovation_event` |
| `ads_event_relation` | `ads.event_relation` |
| `ads_node_influence` | `ads.node_influence` |
| `ads_innovation_point_map` | `ads.innovation_point_map` |
| `ads_carrier_index` | `ads.carrier_index` |
| `ads_city_index` | `ads.city_index` |
| `ads_report` | `ads.report` |
| `ads_impact_prediction` | `ads.impact_prediction` |
| `ads_topic_burst` | `ads.topic_burst` |
| `dim_event_type` | `dim.event_type` |
| `dim_city` | `dim.city` |
| `dim_admin_division` | `dim.admin_division` |
| `dim_carrier` | `dim.carrier` |
| `dim_tech_domain` | `dim.tech_domain` |
| `cfg_index_weight` | `gkx_cfg.index_weight` |
| `cfg_degrade_switch` | `gkx_cfg.degrade_switch` |
| `dwm_graph_node` | `dwd.graph_node` |
| `dwm_graph_edge` | `dwd.graph_edge` |
| `dwm_org_achievement_year` | `dwd.org_achievement_year` |

注意：`dwm_*` → **`dwd` schema**；`cfg_*` → **`gkx_cfg`**（不是 `cfg.`）。

---

## 3. 文件级改造清单（demo 优先）

### 3.1 依赖与配置

- [x] [`gkx-innov/pom.xml`](e:/gkx-lumen/repos/demo-svc-platform/gkx-innov/pom.xml) — 已换 postgresql  
- [x] [`gkx-innov/src/main/resources/application.yml`](e:/gkx-lumen/repos/demo-svc-platform/gkx-innov/src/main/resources/application.yml)  

```yaml
spring:
  datasource:
    driver-class-name: org.postgresql.Driver
    url: jdbc:postgresql://${INNOV_PG_HOST:117.50.223.145}:${INNOV_PG_PORT:5432}/${INNOV_PG_DATABASE:demo_gdf_data}
    username: ${INNOV_PG_USER:postgres}
    password: ${INNOV_PG_PASSWORD:kwaidoo123}
    hikari:
      read-only: true
```

### 3.2 SQL / DAO（按文件勾选）

- [x] `EventController.java` — 表名 + `DATE_FORMAT` → `to_char`
- [x] `GraphController.java` — `dwm_*`→`dwd.*`；`` `rank` `` → `"rank"`
- [x] `CarrierController.java` / `CityController.java` / `ForecastController.java`
- [x] `DictController.java` — 健康检查展示名已改为 `ads.*`
- [x] `InnovDao.java` — 兼容 `PGobject` / jsonb

### 3.3 Helm

- [x] [`helm/gkx-platform/values.yaml`](e:/gkx-lumen/repos/demo-svc-platform/helm/gkx-platform/values.yaml) — `innov` + `innovPy` 已切 `INNOV_PG_*` → `117.50` / `demo_gdf_data`

| 旧 Env | 新 Env |
|--------|--------|
| `INNOV_MYSQL_HOST` | `INNOV_PG_HOST` |
| `INNOV_MYSQL_PORT` | `INNOV_PG_PORT` |
| `INNOV_MYSQL_DB` | `INNOV_PG_DATABASE` |
| `INNOV_MYSQL_USER` | `INNOV_PG_USER` |
| `INNOV_MYSQL_PASSWORD` | `INNOV_PG_PASSWORD` |

`INNOV_CHAIN_ALGO_BASE_URL` **保留**（与 DB 无关）。

---

## 4. 第二波（lumen，可延后）

- [ ] `lumen-svc-platform/gkxlumen-innov`（与 demo 同构；Helm 默认 `enabled: false`）
- [ ] `helm/gkxlumen-platform/values.yaml` 中 innov / innovPy env  
- 无 chain 包；改法同 §3

---

## 5. 风险与验收

| 风险 | 处理 |
|------|------|
| 读写分叉（现状） | Java 未切完前，页面数据可能旧于 Python 新写 |
| `DATE_FORMAT` | 改为 `to_char(event_time,'YYYY-MM-DD')` 等 |
| jsonb | `InnovDao` 兼容 `PGobject` |
| `GROUP BY` 别名 | stats SQL 在 PG 上实测 |
| 企能表误伤 | Java 只读 innov 映射表；勿改 `dwd.enterprise` 等 |

**冒烟清单**

1. 事件列表 / 统计（Event）  
2. 图谱节点边（Graph）  
3. 载体指数 / 城市指数  
4. 预测与突变  
5. Dict / health（表名展示正确）  
6. 产业链 Tab（仍走 Feign → Python，确认 base URL）  
7. 企能页面不受影响（同库不同表）

---

## 6. 建议实施顺序

1. 对 19 张目标表做 `COUNT(*)` 抽样对账（相对 MySQL 旧库或 migrate_report）  
2. pom + `application.yml`  
3. Controller SQL + InnovDao jsonb  
4. Helm innov + innovPy  
5. 本地/K8s 冒烟 §5  
6. 同步 lumen（可选）  
7. 文档退役 `INNOV_MYSQL_*`；旧 MySQL `innov` 保留回滚窗口后再下线  

---

## 7. 预估工作量

| 项 | 量级 |
|----|------|
| demo Java + Helm | 0.5～1 人日 |
| 冒烟与修方言 | 0.5 人日 |
| lumen 同步 | 0.5 人日 |

**监管人 / 认领**：实施前按 `task-claiming-guide` 认领（建议挂在平台/API 相关 task 或新建 `E-INNOV-*-PG-CUTOVER`）。
