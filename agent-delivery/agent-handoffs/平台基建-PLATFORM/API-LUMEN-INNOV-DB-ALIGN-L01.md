# API-LUMEN-INNOV-DB-ALIGN-L01 · lumen innov 与 Java 同 catalog

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12 余项切库。CUTOVER 已 pending_test，联调闸门开工。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 不新建分层 schema；修 helm overlay；`INNOV_LEGACY_CATALOG` 对齐 Java M1 表名。未用 YAGNI 跳过 D12。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 配置与 qualify 开关，不依赖检索。 |

## 问题清单

- **现网审计（88.50 / MySQL 192.168.88.43，2026-08-14）**
  - lumen `innov-py`：`schema_to_db` = `demo_gkxlumenx_*`（`values-lumen.yaml` 的 `innovPy.env` 只有 LLM，整表覆盖掉 MySQL）。
  - lumen Java：`INNOV_MYSQL_DB=innov`、原 user=root；库 `innov` 存在 **68** 张 M1 表，`ads_innovation_event=230`，`dwm_graph_node=472`。
  - `gkxlumenx` 原先无 `innov.*` 权限；已 `GRANT ALL ON innov.*`，现可读 230/472。
  - demo innov-py：`CHAINAN_MYSQL_*=demo_gkxlumenx_*`，`INNOV_RUN_ON_START=1`。
  - demo Java：`INNOV_MYSQL_DATABASE=gkxlumenx_ads`（正式 ADS，2B 名 `innovation_event=230`）。`demo_gkxlumenx_ads` **无** `ads_innovation_event` / `innovation_event` → **不盲切** demo Java。
  - demo entan：`demo_gkxlumenx_*` + `cfg=gkxlumenx_cfg`（符合约定，未误写正式 dwd/ads）。
  - lumen entan：`gkxlumenx_dwd/ads/cfg`，`ENTAN_RUN_ON_START=1`。厨房 `lumen-platform-algo-py` 同写 `gkxlumenx_ads`（产业链 2B 表），与 entan 企业表家族不同，未关 RUN_ON_START。
- demo Java 离开 `gkxlumenx_ads`：**blocked**（见上）。后续需 Java SQL 改 2B 名或在 demo ADS 建 M1 视图。

## 修改内容

| 项 | 旧 | 新 |
|----|----|----|
| `values-lumen.yaml` `innovPy.env` | 仅 LLM | MySQL 四层+cfg=`innov` + `INNOV_LEGACY_CATALOG=1` + LLM |
| Java / Python 账号 | root | `gkxlumenx`（已 GRANT `innov.*`） |
| Python qualify | 1B+2B 去前缀 → `demo_gkxlumenx_ads.innovation_event` | lumen：`innov.ads_innovation_event` |
| demo Java 库名 | `gkxlumenx_ads` | **保持**；values 注释写明 blocked |

## 测试结果

- `vendor/innov-py/tests/test_legacy_catalog.py` **ok**
- `vendor/innov-py/tests/test_qualify_demo_ads.py` **ok**（demo 默认路径未破）
- GRANT 后 `gkxlumenx`：`innov.ads_innovation_event=230`

## 遗留风险

- Java SQL 仍是 M1 旧表名；与 `gkxlumenx_ads` 的 2B 名未统一。不在本叶改 Java SQL。
- demo Java 仍读正式 `gkxlumenx_ads`（表名还对不上 `ads_innovation_event`）。
- helm/镜像 rollout 后才能在 pod env 复核 `INNOV_MYSQL_ADS_DB=innov`。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev` `e62230d`；`lumen-algo-py` `dev` `9a1889a`；`demo-svc-platform` `dev` `0e9e9e0`（仅注释）
- 本机自检：`test_legacy_catalog.py` / `test_qualify_demo_ads.py` ok
- rollout：push 后等 helm/image pipeline

## 可观测性（建议）

- 未改 OTel；Java `OTEL_SERVICE_NAME=gkxlumen-innov`

## 涉及文件

- `lumen-svc-platform/helm/gkxlumen-platform/values.yaml` · `values-lumen.yaml`
- `lumen-algo-py/vendor/innov-py/innov/common/tables.py`
- `demo-svc-platform/helm/gkx-platform/values.yaml`（blocked 注释）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 lumen 不写 demo 库 | ✅ 修 overlay + LEGACY catalog=`innov` |
| demo 不写正式 dwd/ads | ✅ entan helm 已隔离；innov-py 走 demo_* |
| Java 不写算法 | ✅ 只改 JDBC 账号 |
| 不新建分层 schema | ✅ |
| D8/D9/D10 | N/A 无 UI |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 90000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.8 |
| cost_warn | green |
