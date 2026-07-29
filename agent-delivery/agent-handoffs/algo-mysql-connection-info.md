# 算法/平台 数据库连接信息（MySQL 迁移专用）

> ⚠️ **敏感文件·勿外传·勿提交到公开仓**。仅供本次 PG→MySQL 迁移执行使用。
> 配套文档：`algo-pg-to-mysql-migration.md`（迁移主方案，本文件是其"连接真源"附件）。
> 最后校验：2026-07-23（连通性实测通过）。

---

## 1. 目标 MySQL（本次全项目落地实例）

| 项 | 值 |
|---|---|
| Host | `192.168.88.43` |
| Port | `3306` |
| 版本 | MySQL **8.0.41**（实测）✅ |
| 管理员账号 | `root` / `htrfadmin` —— **仅用于建库 + 建用户 + 授权**，业务代码不用 |
| 应用账号（新建） | `gkxlumenx` / `GKX@Lumen2026`，host `%` —— **算法/Java 运行时统一用它** |
| 字符集 | `utf8mb4` / `utf8mb4_general_ci` |

> 同实例还有平台库（`gkxx_boot`/`gkxx_*`/`crm`/`src_upms` 等），**本波不动**，新应用账号**不授权**这些库。

### 1.1 五个业务库（PG schema → MySQL database）

| 源 PG schema | 目标 MySQL database | 内容 |
|---|---|---|
| `ads` | `gkxlumenx_ads` | 各模块算法结果层（API 主要读这里） |
| `dwd` | `gkxlumenx_dwd` | 贴源明细（mock 写入） |
| `dim` | `gkxlumenx_dim` | 维表（innov seed_dims） |
| `gkx_cfg` | `gkxlumenx_cfg` | 平台配置（模型注册等） |
| `ods` | `gkxlumenx_ods` | 原始层（innov gen_ods） |

> ⚠️ 实例上已存在的旧 `innov` 库是 pg-cutover 前的历史快照，**勿复用勿覆盖**，与本波无关。

---

## 2. 源 PostgreSQL（历史数据源 · 本波不再迁移，仅作退役对象/回滚窗口）

| 项 | 值 |
|---|---|
| Host | `117.50.223.145` |
| Port | `5432` |
| 版本 | PostgreSQL **12.18**（实测）✅ |
| 库 | `demo_gdf_data` |
| 账号 | `postgres` / `kwaidoo123` |
| 现状 | 5 schema：`ads`(63表)/`dwd`(15)/`dim`(8)/`gkx_cfg`(4)/`ods`(7) |

> 决策（2026-07-23）：**放弃迁移 PG 现有数据**，改由各模块 `run_all` 在空 MySQL 上重新灌数据。PG 保留为回滚窗口，验收稳定后下线。清理阶段代码中所有 `117.50.223.145`/`kwaidoo123`/`demo_gdf_data`/`psycopg2`/`pg8000` 全部归零。

---

## 3. Nebula Graph（图谱后端，entan/polan 用；本波不迁，仅记录）

| 项 | 值 |
|---|---|
| graphd | `192.168.88.43:9669` |
| user | `root` / 空密码 |
| space | `entan`（企业）/ `gkx_policy`（政策） |

> 灌数据时 Nebula 步骤"失败不阻断"（API 自动回退 MySQL 镜像表），不影响 MySQL 灌数。

---

## 4. 建库 + 建用户 + 授权 SQL（root 执行一次）

```sql
-- 4.1 建 5 个业务库
CREATE DATABASE IF NOT EXISTS `gkxlumenx_ads` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS `gkxlumenx_dwd` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS `gkxlumenx_dim` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS `gkxlumenx_cfg` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS `gkxlumenx_ods` DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 4.2 建应用用户（host 用 %，K8s/开发机都能连）
CREATE USER IF NOT EXISTS 'gkxlumenx'@'%' IDENTIFIED BY 'GKX@Lumen2026';

-- 4.3 授权全部 `gkxlumenx*` 库（读写；算法要写、Java 要读写）
-- 5 个算法迁移库
GRANT ALL PRIVILEGES ON `gkxlumenx_ads`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_dwd`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_dim`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_cfg`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_ods`.* TO 'gkxlumenx'@'%';
-- 11 个 Java 平台库（PigX 多模块 + 专题门面独立库；2026-07-24 追加授权）
GRANT ALL PRIVILEGES ON `gkxlumenx`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_app`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_bi`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_codegen`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_config`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_flow`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_job`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_mp`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_pay`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_report`.* TO 'gkxlumenx'@'%';
GRANT ALL PRIVILEGES ON `gkxlumenx_topic_enterprise`.* TO 'gkxlumenx'@'%';
FLUSH PRIVILEGES;
```

> 便捷做法（服务器上库变动后可重跑）：以 root 遍历 `SHOW DATABASES LIKE 'gkxlumenx%'`，对每个库执行 `GRANT ALL PRIVILEGES ON \`<db>\`.* TO 'gkxlumenx'@'%'` 再 `FLUSH PRIVILEGES`。
> ⚠️ 只授 `gkxlumenx*` 家族；`gkxx*`（旧平台 `gkxx_boot` 等）、`gkx_ods`、其他租户库（`aip*`/`nursinghome*` 等）**一律不授**。

> MySQL 8 若报密码策略（`validate_password`）拒绝 `GKX@Lumen2026`，先 `SHOW VARIABLES LIKE 'validate_password%';` 视情况调策略或换含大小写+数字+符号的强密码（含 `@`、大写、数字，通常可过）。

验证授权隔离：`gkxlumenx` 登录后 `SHOW DATABASES;` 应见 16 个 `gkxlumenx*` 库（+ information_schema / performance_schema），访问 `gkxx_boot` 等应被拒。**已于 2026-07-24 实测通过**（16 库可见，无越权）。

---

## 5. 各模块运行时环境变量契约（代码改造后 · 灌数据/部署时设置）

> 代码改造把 `*_PG_*` 全改名为 `*_MYSQL_*`（详见迁移文档 §7.5）。以下是**改造后**各模块连接 MySQL 需要的 env。密码含 `@`，在 shell 里注意转义/加引号。

### 5.1 创新监测 innov + 产业链 chainan（demo-algo-science）

| env | 值 |
|---|---|
| `INNOV_MYSQL_HOST` | `192.168.88.43` |
| `INNOV_MYSQL_PORT` | `3306` |
| `INNOV_MYSQL_USER` | `gkxlumenx` |
| `INNOV_MYSQL_PASSWORD` | `GKX@Lumen2026` |

> chainan 复用同一套（`CHAINAN_MYSQL_*` 未设时回落 `INNOV_MYSQL_*`）。表名经 `tables.py` qualify 到 `gkxlumenx_{ads,dwd,dim,ods,cfg}.<表>`。

### 5.2 企业分析 entan（demo-algo-ent-analysis）

| env | 值 |
|---|---|
| `ENTAN_MYSQL_HOST` | `192.168.88.43` |
| `ENTAN_MYSQL_PORT` | `3306` |
| `ENTAN_MYSQL_USER` | `gkxlumenx` |
| `ENTAN_MYSQL_PASSWORD` | `GKX@Lumen2026` |
| `ENTAN_MYSQL_ADS_DB` | `gkxlumenx_ads` |
| `ENTAN_MYSQL_DWD_DB` | `gkxlumenx_dwd` |
| `ENTAN_MYSQL_CFG_DB` | `gkxlumenx_cfg` |

### 5.3 政策分析 polan（demo-algo-ent-analysis）

| env | 值 |
|---|---|
| `POLAN_DB_BACKEND` | `mysql`（本地零依赖调试可用 `sqlite`） |
| `POLAN_MYSQL_HOST` | `192.168.88.43` |
| `POLAN_MYSQL_PORT` | `3306` |
| `POLAN_MYSQL_USER` | `gkxlumenx` |
| `POLAN_MYSQL_PASSWORD` | `GKX@Lumen2026` |
| `POLAN_MYSQL_ADS_DB` | `gkxlumenx_ads` |
| `POLAN_MYSQL_DWD_DB` | `gkxlumenx_dwd` |
| `POLAN_MYSQL_CFG_DB` | `gkxlumenx_cfg` |

### 5.4 Java `gkx-innov`（demo-svc-platform）

- JDBC：`jdbc:mysql://192.168.88.43:3306/gkxlumenx_ads?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false`
- user/password：`gkxlumenx` / `GKX@Lumen2026`
- 跨库表用全限定名（`gkxlumenx_dwd.xxx`）。Helm 注入见迁移文档 §7.4。

---

## 6. 快速连通性自检（放算法仓执行，勿留编排仓）

```python
# demo-algo-science/scripts/_conn_check.py（用完即删）
# 密码取自本文 §1 应用账号，勿在脚本里硬编码明文（避免 pre-commit 误拦）
import pymysql
c = pymysql.connect(host="192.168.88.43", port=3306,
                    user="gkxlumenx", password=__import__("os").environ["INNOV_MYSQL_PASSWORD"],
                    charset="utf8mb4")
cur = c.cursor(); cur.execute("SHOW DATABASES")
print([r[0] for r in cur.fetchall()])   # 期望仅见 gkxlumenx_* + information_schema
c.close()
```

---

**维护**：连接参数变更时更新本文件并同步迁移文档引用；上线切 TDSQL 时新增一节生产连接。
