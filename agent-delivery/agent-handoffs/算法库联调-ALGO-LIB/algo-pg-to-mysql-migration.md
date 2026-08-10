# PG → MySQL 彻底迁移文档（全项目去 PG · 重新灌数据版）

> **状态**：✅ 已放行执行（2026-07-23）
> **决策人 / 监管人**：用户
> **执行人**：待认领（建议任务 `E-ALGO-PG-PURGE`）
> **目标**：**整个项目彻底切换 MySQL，不保留任何 PostgreSQL——就像 PG 从未出现过。**
> **数据策略**：❌ 不迁移 PG 现有数据；✅ 在空 MySQL 上由各模块 `run_all` **重新灌数据**（已评估 4 模块可行，见 §5）。
> **连接真源**：所有数据库连接/账号/建库 SQL/环境变量见 **`algo-mysql-connection-info.md`**（敏感附件）。
> **关联**：`innov-java-pg-cutover-checklist.md`（本次反转 + 退役）；`realdata` 路径本波退役（§6）。

---

## 0. 背景与决策

- 生产（总集）最终统一 **TDSQL（MySQL 兼容）**；开发/联调阶段全部收敛到 **MySQL 8.0**（实例 `192.168.88.43:3306`，实测 8.0.41）。
- **彻底去 PG**：Python + Java + Helm + PG 遗留脚本/依赖/文档，全部清理归零。
- **放弃 PG 存量数据**（原 `117.50.223.145/demo_gdf_data`），改为空库重灌——因为 4 模块 mock 均自包含、可复现（§5）。
- `realdata`（连甲方 GP）不在真实调用链，本波**退役删除**（§6）。
- 连接参数、账号、建库/授权 SQL、各模块 env 契约 → 全部集中在 **`algo-mysql-connection-info.md`**，本文件不重复敏感值。

### 0.1 范围

| 域 | 处理 |
|----|------|
| Python 算法（innov / chainan / entan / polan 灌数据） | ✅ db 层 PG→MySQL（§7）+ 空库重灌（§5） |
| Python `realdata`（连甲方 GP `gkx_szc_ods`） | 🗑️ **退役删除**（§6） |
| Java `demo-svc-platform/gkx-innov` | ✅ PG→MySQL（pom + yml + SQL 方言，§7.3） |
| Java `lumen-svc-platform/gkxlumen-innov` | ❌ **不存在**（已确认，无需处理） |
| Helm（两仓 `*_PG_*`） | ✅ → `*_MYSQL_*`（§7.4） |
| PG 遗留（脚本/依赖/DDL/文档） | ✅ 清理或退役（§9） |
| 甲方 GP 源库/镜像/抽数脚本、PG 数据迁移脚本 | ❌ 本波不做（不迁数据、realdata 退役） |
| 实例上旧 `innov` 库 | ⚠️ 历史遗留，勿用勿覆盖 |

---

## 1. 现状盘点

### 1.1 DB 连接层文件（改造入口）

| 仓 | 文件 | 现驱动 | 关键 PG 逻辑 |
|---|---|---|---|
| demo-algo-science | `innov/common/db.py` | psycopg2 | `upsert`(ON CONFLICT)+`_load_pks`(pg 系统表)+`Json`；读 `scripts/sql/pg/schema_pg.sql` 建表 |
| demo-algo-science | `chainan/common/db.py` | psycopg2 | 与 innov 同构 |
| demo-algo-science | `innov/common/tables.py` + `scripts/sql/pg/innov_table_map.yaml` | — | 旧表名→`schema.table` qualify 层 |
| demo-algo-ent-analysis | `entan/common/db.py` | pg8000 | `insert`+`truncate(RESTART IDENTITY CASCADE)`；读 4 个 PG DDL 建表 |
| demo-algo-ent-analysis | `polan/common/db.py` | **pg8000 / sqlite 双后端** | 统一 `_schema_spec()` 生成 DDL；`_adapt` 改写；`_PG_TYPE`/`_SQLITE_TYPE` |
| demo-algo-ent-analysis | `entan/realdata/db.py`、`innov/realdata/pg_db.py` | psycopg2 | 甲方 GP → 🗑️ 删除 |

### 1.2 Java / Helm PG 分布

| 位置 | 现状 |
|---|---|
| `demo-svc-platform/gkx-innov` `application.yml`+`pom.xml` | `jdbc:postgresql://117.50…/demo_gdf_data`，只读 |
| `demo-svc-platform/helm/gkx-platform/values.yaml` | `INNOV_PG_*`（innov/innovPy/entan 多段） |
| `lumen-svc-platform/helm/gkxlumen-platform/values.yaml` | `ENTAN_PG_*`（542–554 行） |

### 1.3 PG 专属逻辑（改造重点）

- 驱动 `psycopg2`/`pg8000` → `pymysql`；游标 `RealDictCursor`/`cur.description` → `pymysql.cursors.DictCursor`
- `ON CONFLICT (...) DO UPDATE SET x=EXCLUDED.x` → `ON DUPLICATE KEY UPDATE x=VALUES(x)`
- `psycopg2.extras.Json(v)` → `json.dumps(v, ensure_ascii=False)`
- `_load_pks` 查 `pg_index/pg_class` → 查 `information_schema.key_column_usage`（或 db 端建表已定义 PK，靠 `ON DUPLICATE KEY`）
- `TRUNCATE ... RESTART IDENTITY CASCADE` → `SET FOREIGN_KEY_CHECKS=0; TRUNCATE ...; SET FOREIGN_KEY_CHECKS=1`
- `CREATE SCHEMA` → `CREATE DATABASE`；标识符 `"col"` → `` `col` ``；`bigserial`→`bigint AUTO_INCREMENT`；`numeric`→`decimal`；`timestamp DEFAULT now()`→`datetime DEFAULT CURRENT_TIMESTAMP`；`jsonb/text(存JSON)`→`json`/`longtext`
- Java SQL：`to_char()`→`DATE_FORMAT()`
- ✅ 占位符 `%s`：psycopg2/pg8000/pymysql 通用，不改

---

## 2. Schema 组织（PG schema → MySQL database）⭐

MySQL `database.table` 语法 == PG `schema.table`。映射（详见连接文件 §1.1）：

| PG schema | MySQL database |
|---|---|
| `ads` | `gkxlumenx_ads` |
| `dwd` | `gkxlumenx_dwd` |
| `dim` | `gkxlumenx_dim` |
| `gkx_cfg` | `gkxlumenx_cfg` |
| `ods` | `gkxlumenx_ods` |

改造集中三处：① `innov_table_map.yaml`/`qualify` 目标值加 `gkxlumenx_` 前缀；② entan/polan 的 schema 变量默认值改为 `gkxlumenx_*`；③ DDL 建库 + db.py 驱动。

---

## 3. DDL 方言转换（PG → MySQL 8.0）

| PG | MySQL 8.0 | 注意 |
|---|---|---|
| `CREATE SCHEMA IF NOT EXISTS "ads"` | 库已由 root 预建（连接文件 §4），DDL 内**去掉建 schema**，或 `CREATE DATABASE IF NOT EXISTS` | |
| 标识符 `"col"` | 反引号 `` `col` `` | 保留字（`rank`/`level`）必加 |
| `bigserial PRIMARY KEY` | `bigint NOT NULL AUTO_INCREMENT PRIMARY KEY` | |
| `numeric`/`numeric(p,s)` | `decimal(38,10)` / `decimal(p,s)` | 无标度统一 `decimal(38,10)` |
| `text`（存 JSON） | `json` 或 `longtext` | polan `_schema_spec` 的 `json` 型 → MySQL `json` |
| `text`（大正文） | `longtext` | report/content |
| `timestamp DEFAULT now()` | `datetime DEFAULT CURRENT_TIMESTAMP` | |
| `boolean` | `tinyint(1)` | |
| 表尾 | `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4` | |

各仓 DDL 产物：
- demo-algo-science：新增 `scripts/sql/mysql/schema_mysql.sql`（由 `schema_pg.sql` 转），`innov/common/db.py` 的 `init_schema` 改读它
- demo-algo-ent-analysis（entan）：`scripts/schema_{dwd_patch,ads,ent_score,cfg}.sql` 转 MySQL 方言（`ads.realdata_*` 表定义保留）
- demo-algo-ent-analysis（polan）：**无需手写 DDL**，在 `polan/common/db.py` 新增 `_MYSQL_TYPE` 映射 + mysql 分支，`_schema_spec()` 自动生成（§7.2）

---

## 4. 数据库连接信息

👉 **全部集中在 `algo-mysql-connection-info.md`**（敏感附件）：目标 MySQL（实例/root/应用用户 `gkxlumenx`）、源 PG（退役对象）、Nebula、5 库映射、建库+建用户+授权 SQL、各模块 env 契约、连通性自检脚本。

本文件不再重复敏感值；执行时以连接文件为准。

---

## 5. 各模块「灌数据」机制与步骤 ⭐（可行性已评估，供执行 AI 照做）

> 结论：**4 模块直接在空 MySQL 上跑 `run_all` 重新灌数据全部可行**。依据：所有 mock 生成器**自包含**（固定 seed、不读外部文件/不联网/不连 PG）；**API 依赖的表全部由 `run_all` 产出**，无空表缺口；`realdata` 退役无影响（唯一被 API 读的 `ads.realdata_enterprise_risk` 由 `entan/depth` mock 产出）。
>
> **前置铁律**：灌数据必须在**各模块 db 层改成 MySQL 之后**（§7）执行——因为 `run_all` 直接往 MySQL 写。顺序不能反。
> **建表内嵌**：各 `run_all` 首步即 `init_schema`（建表），故只需先建好 5 个**空 database**（连接文件 §4），无需手工逐表建。

### 5.1 创新监测 innov（demo-algo-science）

- **入口**：`scripts/run_all.py` 的 `main()`（`STEPS`，11 步）
- **步骤链**：`seed_dims`（建表+维表）→ `generate_ods`（mock ODS）→ P1 机构贯通 → P2 事件直转 → P3 资讯NLP → P5 图谱 → P6 赋分 → P4 重要性 → P7 指数 → P8 预测/突变 → P9 报告
- **写库点**：`innov/common/db.py` 的 `upsert()`（走 `ON CONFLICT`→改 `ON DUPLICATE KEY UPDATE`）
- **产出库表**：`gkxlumenx_dim.dim_*`、`gkxlumenx_ods.ods_*`、`gkxlumenx_dwd.dwd_event_std`、`gkxlumenx_ads.ads_innovation_event/ads_node_influence/ads_carrier_index/ads_city_index/ads_impact_prediction/ads_topic_burst/ads_report` 等 + 图谱 `dwm_graph_node/edge`
- **mock 参数**：`conf/settings.yaml` `mock.seed=20260611`（可复现）

### 5.2 产业链 chainan（demo-algo-science）

- **入口**：`scripts/run_all.py` 的 `main_chain()`（`CHAIN_STEPS`，17 步）；**推荐用 `main_all()`**（先 innov 全量再 chainan）
- **步骤链**：`chain_mock` → A 基础 → M1 全景 → M2 深圳链 → M3 路线图 → M4 热点 → M5 深圳优势 → M6 周期 → M7 阶段 → M8 关键节点 → **M8b 节点打分** → M9 断点 → M10 区域指数 → M10b 竞争力 → M11 深圳问题 → M12 深圳机遇 → M13 布局推荐
- **写库点**：`chainan/common/db.py`（与 innov 同构）
- **⚠️ 跨模块依赖**：M8b（`chainan/graph/scoring.py`）关联 `dim_tech_domain`（由 innov `seed_dims` 产）。**必须先跑 innov**——用 `main_all()` 保证顺序；勿单独只跑 `main_chain()`
- **产出库表**：`gkxlumenx_dwd.gkx_chain_dwd_*`、`gkxlumenx_ads.ads_chain_*`（全景/路线图/热点/周期/阶段/关键节点/断点/区域指数/竞争力/深圳问题/机遇/布局 等）
- **mock 参数**：`conf/settings.yaml` `chainan_mock.seed=20260623`

### 5.3 企业分析 entan（demo-algo-ent-analysis）

- **入口**：`scripts/run_all.py` 的 `main()`（`STEPS`，9 步）
- **步骤链**：`init_schema`（读 4 个 DDL 建表）→ `mock.run`（贴源 dwd 9 表）→ A 基础指标 → B 实体识别+图谱 → **B+ Nebula 灌入（失败不阻断）** → M 成员初始化（失败不阻断）→ C1 技术力 → C2 商业力 → D 深度分析（A1评分/A2排名/A3诊断/A4中心性/B1风险）
- **写库点**：`entan/common/db.py` 的 `insert()` + `truncate()`（`RESTART IDENTITY CASCADE`→FK 开关方案）
- **产出库表**：`gkxlumenx_dwd.enterprise*`（9 表）；`gkxlumenx_ads.enterprise_profile/enterprise_type_dist/enterprise_domain_dist/enterprise_news_stat/new_enterprise_stat/key_enterprise/entity_recognition/graph_node/graph_edge/graph_membership/tech_power/biz_power/enterprise_score/enterprise_ranking/enterprise_diagnosis/enterprise_centrality/realdata_enterprise_risk`
- **realdata 说明**：API 唯一读的 `ads.realdata_enterprise_risk` 由 D 步 `entan/depth/pipeline.py` mock 产出 ✅；其它 `realdata_*` 表无 API 消费，退役无影响
- **mock 参数**：`conf/settings.yaml` `mock.seed=20260613`

### 5.4 政策分析 polan（demo-algo-ent-analysis）

- **入口**：`scripts/run_all_policy.py` 的 `main()`（`STEPS`，15 步）；后端由 `POLAN_DB_BACKEND` 决定（改造后设 `mysql`）
- **步骤链**：`init_schema`（spec 自动建表）→ `seed_models`（cfg_model_registry）→ `mock`（dwd.policy_base_info）→ A 基础指标 → B NER/RE 图谱 → **B+ Nebula（未启用则跳过）** → C1 焦点 → C2 力度 → C3 效果 → C4 短板 → C5 机遇 → C6 布局 → D1 文本解析 → D2 匹配 → D3 推演
- **写库点**：`polan/common/db.py`（**双后端已抽象**）——加 mysql 分支即可（§7.2）
- **产出库表**：`gkxlumenx_dwd.policy_base_info`；`gkxlumenx_ads.policy_*`（level/type/timeseries/national/sz/focus/intensity/effect/metric_timeseries/entity/graph_node/graph_edge/text_parse/match/simulate）；`gkxlumenx_cfg.cfg_model_registry`
- **本地调试**：`POLAN_DB_BACKEND=sqlite` 零依赖可先验证流水线逻辑

### 5.5 灌数据执行命令（改造完成后，仓根目录执行）

```bash
# ① demo-algo-science：innov + chainan 一次全灌（main_all 保证 innov 先于 chainan）
cd e:\gkx-lumen\repos\demo-algo-science
#   先设 §5 env（见连接文件 §5.1）：INNOV_MYSQL_HOST/PORT/USER/PASSWORD
python -c "import sys; sys.path.insert(0,'scripts'); import run_all; run_all.main_all()"

# ② demo-algo-ent-analysis：企业分析 entan
cd e:\gkx-lumen\repos\demo-algo-ent-analysis
#   先设 env（连接文件 §5.2）：ENTAN_MYSQL_*
python scripts/run_all.py

# ③ demo-algo-ent-analysis：政策分析 polan
#   先设 env（连接文件 §5.3）：POLAN_DB_BACKEND=mysql + POLAN_MYSQL_*
python scripts/run_all_policy.py
```

> 全程幂等可重跑（各步 truncate/upsert）。灌完按 §11 验收（各库表非空 + API 出数）。

---

## 6. `realdata` 路径退役

`run_realdata_ent.py` / `innov/realdata/` / `entan/realdata/` 不在真实调用链（手动离线脚本，API/pipeline 零 import；前端只有 `entanHelp.ts` 一句血缘文案）。**删除**：`innov/realdata/`、`entan/realdata/`、`scripts/run_realdata_ent.py`、`database_env.yaml`。`ads.realdata_enterprise_risk`（API 需要）由 `entan/depth` mock 产出，不受影响。

---

## 7. 详细改造清单

### 7.1 demo-algo-science（Python）
- [ ] `requirements.txt`：删 `psycopg2-binary`，留 `pymysql`
- [ ] `innov/common/db.py` + `chainan/common/db.py`：psycopg2→pymysql；游标；`upsert` 的 `ON CONFLICT`→`ON DUPLICATE KEY UPDATE`；`_load_pks`→`information_schema`；`Json`→`json.dumps`；连接改读 `INNOV_MYSQL_*`（建议抽公共基类）
- [ ] `innov/common/tables.py` + `innov_table_map.yaml`：目标值加 `gkxlumenx_` 前缀（建议另存 `mysql_table_map.yaml`）
- [ ] 生成 `scripts/sql/mysql/schema_mysql.sql`（§3）；`init_schema` 改读它
- [ ] `conf/settings.yaml`：`db.pg_*` → `db.mysql_*`（值见连接文件；host 192.168.88.43、user gkxlumenx）
- [ ] 🗑️ 删 `innov/realdata/` + `scripts/run_realdata_ent.py`（§6）；清理 `scripts/sql/pg/`、`migrate_innov_mysql_to_pg.py`

### 7.2 demo-algo-ent-analysis（Python）
- [ ] `requirements.txt`：删 `pg8000`/`psycopg2`，加/留 `pymysql`
- [ ] `entan/common/db.py`：pg8000→pymysql；`insert`/`query`/`init_schema` 适配；`truncate` 的 `RESTART IDENTITY CASCADE`→`SET FOREIGN_KEY_CHECKS=0`+`TRUNCATE`+`=1`；schema 变量默认值 `dwd/ads/gkx_cfg`→`gkxlumenx_dwd/ads/cfg`，改读 `ENTAN_MYSQL_*`
- [ ] `polan/common/db.py`：新增 `_MYSQL_TYPE`（`pk`→`bigint AUTO_INCREMENT PRIMARY KEY`、`text_pk`→`varchar(64) PRIMARY KEY`、`int`→`bigint`、`num`→`decimal(38,10)`、`text`→`longtext`、`date`→`date`、`ts`→`datetime DEFAULT CURRENT_TIMESTAMP`、`json`→`json`）；`__init__` 加 `backend=="mysql"` 分支（pymysql 连接 + `_paramstyle="%s"`）；`_adapt` 加 mysql 改写（`schema.table` → `` `gkxlumenx_x`.`table` `` 或直接反引号库名，`%s` 保留）；`init_schema` mysql 用 `CREATE DATABASE IF NOT EXISTS`；`truncate` mysql 用 FK 开关；backend 选择识别 `POLAN_DB_BACKEND=mysql`/`POLAN_MYSQL_HOST`
- [ ] 🗑️ 删 `entan/realdata/`（§6）
- [ ] entan DDL：`schema_{dwd_patch,ads,ent_score,cfg}.sql` → MySQL 方言（`ads.realdata_*` 定义保留）
- [ ] `conf/settings.yaml`：`db.pg_*` → `db.mysql_*`

### 7.3 Java（仅 `demo-svc-platform/gkx-innov`）
- [x] `pom.xml`：`org.postgresql:postgresql` → `com.mysql:mysql-connector-j`（版本由 `gkx-common-bom` 管理，无需写 version）
- [x] `application.yml`：JDBC 改 `jdbc:mysql://${INNOV_MYSQL_HOST:192.168.88.43}:${INNOV_MYSQL_PORT:3306}/${INNOV_MYSQL_DATABASE:gkxlumenx_ads}?useUnicode=...&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true`，user `gkxlumenx`
- [x] 6 个 Controller：`schema.table`→`gkxlumenx_*.table`（53 处，脚本机械替换）；`EventController` `to_char`→`DATE_FORMAT` + fmt 串 `YYYY-MM`→`%Y-%m`；无 `"rank"` 双引号标识符
- [x] `InnovDao.java`：移除 `org.postgresql.util.PGobject` import 与分支，MySQL JSON 列走 `String` 反序列化
- [ ] 切库后重新构建镜像 + K8s dev rollout（CI）—— 待部署验证（本地无 mvn 环境，见 §12）

### 7.4 Helm
- [x] `demo-svc-platform/helm/gkx-platform/values.yaml`：3 段（Java `innov` / `innovPy` / `entanPy`）`INNOV_PG_*`/`ENTAN_PG_*` → `*_MYSQL_*`，指 192.168.88.43 / gkxlumenx；Python 段去掉不读的 `*_DATABASE`
- [x] `lumen-svc-platform/helm/gkxlumen-platform/values.yaml`：`ENTAN_PG_*`（542–554）→ `ENTAN_MYSQL_*`
- [x] 移除 `*_PG_{DWD,ADS}_SCHEMA`，改注入 `ENTAN_MYSQL_{DWD,ADS,CFG}_DB`（`gkxlumenx_*`）

### 7.5 环境变量重命名（值见连接文件 §5）

| 旧 | 新 |
|---|---|
| `INNOV_PG_HOST/PORT/USER/PASSWORD/DATABASE` | `INNOV_MYSQL_HOST/PORT/USER/PASSWORD` |
| `CHAINAN_PG_*` | `CHAINAN_MYSQL_*`（回落 `INNOV_MYSQL_*`） |
| `ENTAN_PG_*` / `ENTAN_PG_{DWD,ADS,CFG}_SCHEMA` | `ENTAN_MYSQL_*` / `ENTAN_MYSQL_{ADS,DWD,CFG}_DB` |
| `POLAN_PG_*` / `POLAN_DB_BACKEND=pg` | `POLAN_MYSQL_*` / `POLAN_DB_BACKEND=mysql` |

---

## 8. 专用 MySQL 用户与授权

👉 建库 + 建用户 `gkxlumenx` + 授权 5 库的完整 SQL 见 **连接文件 §4**。要点：应用账号仅授权 5 个 `gkxlumenx_*` 库，不碰平台库。

---

## 9. PG 遗留清理（"像没出现过"）

- [x] `demo-algo-science/scripts/sql/pg/` → 已删除；运行时用的 `innov_table_map.yaml` 迁至 `scripts/sql/mysql/`，`tables.py` 路径已更新
- [x] `demo-algo-science/scripts/migrate_innov_mysql_to_pg.py` + `scripts/_conv_pg_ddl_to_mysql.py`（临时）→ 已删除
- [x] `demo-algo-ent-analysis/scripts/_gen_entan_ddl.py`（临时，用 psycopg2 introspect）→ 已删除
- [x] `demo-algo-science/innov/realdata/` + `entan/realdata/` + `run_realdata_ent.py` → 已删除（§6；均离线路径，运行期零引用）
- [x] `demo-algo-science/db/dwd.sql`（Navicat PG 转储，含外网 IP）→ 已删除（被 `scripts/sql/mysql/schema_mysql.sql` 取代）
- [x] `requirements.txt`/`docker/requirements-base.txt`：去 `psycopg2-binary`/`pg8000`（保留 `pymysql`）；`pom.xml`：`org.postgresql`→`com.mysql:mysql-connector-j`
- [x] settings/application.yml/values.yaml/README/设计文档 残留 PG 描述与密钥（IP/口令）→ 已脱敏改 MySQL
- [x] in-scope 全仓 grep 归零：`psycopg2` / `pg8000` / `_PG_` / `demo_gdf_data` / `kwaidoo123` / `117.50.223.145` = 0
- [ ] `innov-java-pg-cutover-checklist.md` → 待标注 **SUPERSEDED**（保留历史；非阻断）

> **保留项（有意为之，非违规）**：
> - `demo-algo-ent-analysis/scripts/schema_{cfg,ads,policy_ads}.sql`：PG 方言 DDL **交付物**（供 data/Java 侧参考），运行时不读；注释已去密钥，标注运行时以 `scripts/mysql/schema_mysql.sql` 为准。
> - `demo-svc-topic-py`（专题服务 Python）仍用 `pg8000`：**不在本次方案范围**（方案只含 science/entan/polan + Java gkx-innov + Helm），需单独立项评估。
> - `lumen-svc-platform` 框架层 `DsJdbcUrlEnum`/`common-bom` 的 postgresql 可选驱动：PigX 多数据源通用能力，与本迁移无关，不动。
> - `lumen-ui-topic/.env.development` 的 `111.198.38.90` 是专题系统 **API 网关地址**（非 DB），保留。

---

## 10. 待确认（已全部确认 ✅）

1. ✅ 应用用户 `gkxlumenx` / `GKX@Lumen2026`，host `%`。
2. ✅ Java `gkx-innov` 切库后可立刻重新部署（dev rollout）。
3. ✅ 放弃 PG 存量数据，改空库重灌（4 模块可行性已评估）。

---

## 11. 执行顺序（重灌路线）

1. ~~确认~~ ✅
2. 认领任务（`gkx-task-claim-supervision`，建 `E-ALGO-PG-PURGE`）
3. root 建 5 个空库 + 建 `gkxlumenx` 用户授权（连接文件 §4）
4. 改 db 层 + DDL 转方言（§7.1 / §7.2）—— **必须先于灌数据**
5. 跑灌数据（§5.5）：
   - a. demo-algo-science `run_all.main_all()`（innov+chainan）→ 冒烟
   - b. demo-algo-ent-analysis `run_all.py`（entan）→ 冒烟
   - c. demo-algo-ent-analysis `run_all_policy.py`（polan，backend=mysql）→ 冒烟
6. 改 Java（§7.3）→ 构建 + dev rollout 冒烟
7. 改 Helm（§7.4）→ dev 部署验证
8. 删 realdata（§6）+ PG 遗留清理（§9）+ grep 归零
9. handoff（cost 回填）+ 退役旧 pg-cutover 文档

---

## 12. 冒烟验收清单

- [x] 5 算法库建成 + `gkxlumenx` 用户授权（2026-07-24 追加授权全部 11 个 Java 平台库 `gkxlumenx*`，实测 16 库可见、`gkxx*`/其他租户库被拒）
- [ ] **灌数据全绿**（改完 db 层后）：
  - [ ] innov+chainan：`run_all.main_all()` 无异常；`gkxlumenx_dim/ods/ads` 关键表 `COUNT(*)>0`（`ads_innovation_event`、`ads_chain_panorama` 等）
  - [ ] entan：`run_all.py` 无异常（Nebula/成员步骤告警可接受）；`ads.enterprise_score/ranking/diagnosis/centrality/realdata_enterprise_risk`、`ads.enterprise_type_dist` 等非空
  - [ ] polan：`run_all_policy.py`（mysql）无异常；`ads.policy_*` 非空、`gkx_cfg.cfg_model_registry` 非空
- [ ] API 出数正常；前端 4 个 Demo 按钮链路通
- [ ] Java `gkx-innov` dev 健康检查 + Controller 出数（方言/表名正确）
- [ ] §9 grep 全部归零

---

## 13. 风险与回滚

| 风险 | 处理 |
|------|------|
| MySQL 保留字（`rank`/`level` 等） | DDL/SQL 一律反引号 |
| jsonb→json 强校验/保序差异 | `_norm_row`/`pj()`/`j()` 回归；`json` 型统一 `json.dumps(ensure_ascii=False)` |
| entan `TRUNCATE CASCADE` 无等价 | `SET FOREIGN_KEY_CHECKS=0` + 按序 TRUNCATE + `=1` |
| chainan 依赖 innov 维表 | 统一用 `main_all()`，勿单跑 `main_chain()` |
| Nebula 未连通 | 步骤"失败不阻断"，API 回退 MySQL 镜像表，不影响灌数 |
| MySQL 8 密码策略拒绝 | 见连接文件 §4 说明 |
| 误用旧 `innov` 库 | 只新建 `gkxlumenx_*`，不碰旧库 |
| 需要回退 | 源 PG 117.50 迁前**保留为回滚窗口**；出问题回退代码+指回 PG；验收稳定后再下线并清理 |

---

**作者标记**：本文档由 `[agent:coordinator]` 起草，监管人已放行执行。连接敏感信息见 `algo-mysql-connection-info.md`。

---

## 14. 追加纳入：`demo-svc-topic-py`（专题服务 / gkx-search-service）as-built

> 监管人 2026-07-24 追加"纳入"；只读服务，部署默认 Mock（k8s `GKX_MOCK_ENABLED=1`，未注入 DB env）。

**决策（监管人拍板）**：topic-py 的 `dwd.*` 表**并入共享库 `gkxlumenx_dwd`**；运行时**复用 `gkxlumenx` 账号**（该账号已授权 `gkxlumenx_dwd`，无需补授权）。

**已改（`origin/dev`，commit `…8d50f64`）**：
- `gkx_common/db.py`：`pg8000` → `pymysql`（`charset=utf8mb4`；`execute(sql, params or None)` 规避 `%` 解析）。
- `gkx_common/config.py`：`GKX_PG_*` → `GKX_MYSQL_*`（默认 `192.168.88.43:3306` / `gkxlumenx` / 库 `gkxlumenx_dwd`；新增 `mysql_dwd_db`/`mysql_ads_db`）。
- `gkx_search_service/views/*.py`（12 文件）+ `gkx_common/mock.py`：SQL/注释 `dwd.` → `gkxlumenx_dwd.`；`NULLS LAST` 移除（MySQL DESC 天然 NULL 末位）。仅 `dwd.*` 被引用，无 `ads.*` 表。
- **2026-07-29 补记**：行政区划企业检索码表落地为 **`gkxlumenx_dim.code_region`**（源 PG `dim.admin_division`，非 DWD）。见 `agent-delivery/data/ddl/gkxlumenx_dim_code_region.sql` + `agent-handoffs/企业战略分析-ENT/DATA-DIM-CODE-REGION-MIGRATE-2026-07-29.md`。
- `gkx_ai_service/sql/evaluation.sql`：PG DDL → MySQL 8.0（`ads.`→`gkxlumenx_ads.`、`JSONB`→`JSON`、`BIGSERIAL`→`BIGINT AUTO_INCREMENT`、`` `rank` `` 反引号、索引内联 `KEY`、`COMMENT ON`→表 `COMMENT=`、`ON CONFLICT DO NOTHING`→`INSERT IGNORE`）。仅交付物，运行时用内存 store。
- `conf/settings.yaml` / `.env.example` / `requirements.txt`（`pg8000`→`pymysql`）；`docs/API-接口文档.md` 脱敏。
- 校验：全仓 PG token grep 归零；12 核心模块 import OK；`py_compile` 通过；config 加载正确。

**未改/保留**：Helm `searchPy`（demo-svc-platform）与 k8s 均无 DB env（Mock 运行），无需改。`gkx_common/nebula*.py` 属 NebulaGraph（架构铁律 D3 认可），非 PG。`gkx_ai_service` 的 `httpx` 依赖缺失为预装环境问题，与本迁移无关。

## 15. entan 企业表激进重建：`enterprise_id`(bigint) → `org_id`(varchar) + canonical DWD 48 表 as-built

> 监管人 2026-07-24 拍板"很激进地把旧版企业相关表全部废除"，按权威文档从零重建；数据从零重生（不迁移）。
> 权威来源：`agent-delivery/data/data-design/企业/DWD表结构设计-企业模块.md`（48 表，`org_id` 业务主键）+ `agent-delivery/agent-handoffs/产品整体定义/E-31-企业发展/ADS-facts-contract-E31.md`。
> 决策：`recon=unify` / `dwd_loader=entan_gen`（entan mockgen 产出全套 canonical DWD）/ `ads_naming=保留 entan 分析产物但 re-key 到 org_id`。

**废除的旧企业表**（bigint `enterprise.id` 主键体系）：`enterprise` / `enterprise_business_tag` / `enterprise_industry` / 旧 `enterprise_finance_history` / `enterprise_patent_history` / `enterprise_cooperation` / `enterprise_supply_chain` / `enterprise_parent_subsidiary` / `enterprise_news`（旧结构）。

**重建（`demo-algo-ent-analysis`，`origin/main`）**：
- **DDL** `scripts/mysql/schema_mysql.sql`：新增 canonical 企业 DWD（`enterprise_base` 含 §4.1 契约字段 + entan 分析快照/派生扩展列；`enterprise_extra`/`history_name`/`tag_dict`/`enterprise_tag`/`finance_history`/`patent_history`/`patent_detail`/`executive`/`bid`/`news`/`industry_chain`/`financing`/`innovation_carrier`/`invest`/`cooperation`/`supply_chain`/`parent_subsidiary` + 汇总 6 + 风险 `risk_type_dict`/`enterprise_risk_summary`/24 张 `risk_*`），全部 `org_id`(varchar64) 主键/外键。entan 分析 ADS（`enterprise_score`/`ranking`/`diagnosis`/`centrality`/`tech_power`/`biz_power`/`entity_recognition`/`graph_node|edge|membership`/`key_enterprise`/`realdata_enterprise_risk` 等）键位 `enterprise_id|enterprise_code` → `org_id`。
- **mockgen** `entan/mockgen/generate.py`：主键 `org_id=f"ORG{n:08d}"`，`enterprise_code`=统一社会信用代码；产出全套 canonical DWD；随机种子 `hash()` → `zlib.crc32()`（确定性）；`enterprise_executive` 按 `(org_id,name,position)` 去重满足 `uk_exec`。
- **算法** re-key 全改 `org_id`：`basic/indicators`、`graph/entity`+`graph/incremental`、`eval/tech_power`+`eval/biz_power`、`depth/pipeline`（A1评分→`enterprise_score` 对齐设计§4.15 / A2排名 / A3诊断 / A4中心性 / B1风险）、`graph/nebula_query`（vid 用 org_id 字符串）。
- **DDL 重建机制** `entan/common/db.py`：`init_schema(reset=False)`；`reset=True`（仅 `run_all` 首步）先 `DROP` entan 独占且结构变更的表（`enterprise*`/`risk_*`/`tag_dict`/entan 分析 ADS + 废除表），再 `CREATE`；中途 `_ensure_schema` 用默认 `reset=False`（非破坏，避免清空已灌数据）。`scripts/run_all.py` 首步改 `init_schema(reset=True)`。**不触碰** chain_*/policy_*/event_std/graph_node|edge(dwd)/national_policy* 等他模块表。
- **FastAPI** `/entan/v1/*`：路径参数与键位 `enterprise_id`(number)/`enterprise_code` → `org_id`(string)（`api/main.py`：`/tech-power/{org_id}`、`/biz-power/{org_id}`、`/enterprises/{org_id}/report`、`/graph?center=org_id`、`/graph/path` source/target 字符串、`/graph/nodes` body `org_id`、DELETE `/graph/nodes/{org_id}`；`api/entan_analysis_routes.py` score/ranking/diagnosis/centrality/risk 输出 `org_id`；`api/entan_evaluation_routes.py` precheck/compute 以 `org_id` 匹配 canonical DWD/ADS）。
- **前端** `demo-ui-system-test`（`origin/main`）：`src/api/entan/index.ts` 全部 `enterpriseId:number` → `orgId:string`；组件 `TechPower.vue`/`BizPower.vue`（`row.org_id`/`cur.value.org_id`）、`GraphView.vue`（`centers:string[]`、选项/候选 `e.org_id`/`c.org_id`、`_eid` 保留字符串、"PostgreSQL 兜底"→"MySQL 兜底"）；`entanHelp.ts` 血缘文案表名/键位（`dwd.enterprise`→`dwd.enterprise_base`、`enterprise_id`→`org_id`、`enterprise_industry`→`enterprise_industry_chain`）。
- **清理**：删除过时 PG 期 `scripts/schema_dwd_patch.sql` / `scripts/schema_ads.sql`（未被 `init_schema` 引用）。

**验证证据（本地 MySQL `192.168.88.43` 全量重跑）**：
- `python scripts/run_all.py` 绿；关键落库计数：`enterprise_base=120`/`extra=120`/`finance_history=696`/`patent_history=696`/`executive=411`/`industry_chain=141`/`cooperation=286`/`supply_chain=174`/`parent_subsidiary=21`/`invest=28`/`financing=100`/`bid=200`/`news=200`/`enterprise_tag=171`/`tag_dict=7`；ADS `enterprise_score=120`/`ranking=720`/`diagnosis=120`/`centrality=114`/`tech_power=120`/`biz_power=120`/`entity_recognition=120`/`graph_node=144`/`graph_edge=576`/`key_enterprise=83`/`realdata_enterprise_risk=39`。样本键位 `org_id='ORG00000001'` + `enterprise_code`。
- FastAPI（uvicorn 起服）逐个 `/entan/v1/*` 以 `org_id`(ORG00000050) 请求全部 `code=0` 有数据（含 `tech-power/{org_id}`、`biz-power/{org_id}`、`enterprises/{org_id}/report`、`graph?center=org_id`、`evaluation/compute`）。
- 一致性：entan 全仓业务代码 `enterprise_id` 归零（仅剩 `api/main.py` 一处 `body.get("enterprise_id")` 向后兼容回退；`chain_*` 表的 `enterprise_id` 属产业链模块本地键，非企业模块，不在废除范围）。

**已知/未尽**：
- **风险 24 张 `risk_*` DWD 明细 + `enterprise_risk_summary`/`risk_type_dict` 目前空表**（结构就绪、`org_id` 键）；entan 风险视图走已计算的 `ads.realdata_enterprise_risk`(=39)，不依赖这些明细。按既定"结构完整+轻量"策略暂不灌，如 topic/data 侧需要可另开 mockgen 轻量填充任务。
- **E31 `ent_*` ADS**（`ent_key_qual_scale` 等）本次不由 entan 产出（归 data/topic），仅保证 canonical DWD 源就位。
- entan `docs/*.md` 与 `算法设计说明.md` 仍含旧 `enterprise_id` 叙述（历史设计文档），属 doc-agent 后续清理，不影响运行。
