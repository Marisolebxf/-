# API-LUMEN-INNOV-2B-SQL-L01 · lumen innov 对齐正式 2B ADS

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（长任务总控） |
| 说明 | D12 余项：关掉 `INNOV_LEGACY_CATALOG`，Java SQL 落到 `gkxlumenx_*` 2B 名。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 一处 `InnovSql` + helm env；不逐控制器改 SQL；不新建库；不走 GDF。未用 YAGNI 跳过 D12。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | SQL 改写 + helm，不依赖检索。 |

## 问题清单

- lumen Java SQL 仍是 M1 未限定名（`ads_innovation_event` / `dwm_graph_node`），JDBC catalog=`innov`。
- Python `INNOV_LEGACY_CATALOG=1` 四层都指 `innov`，与正式 2B（`gkxlumenx_ads.innovation_event=230`）两套表并存。
- cfg：`gkxlumenx_cfg.index_weight=2` / `degrade_switch=5`（无 `gkxlumenx_gkx_cfg` 库）。账号 `gkxlumenx` 已有 `gkxlumenx_{ods,dwd,ads,dim,cfg}.*` GRANT。
- demo Java 已走全限定 2B + DataPlane，本叶不改 demo。

## 修改内容

| 项 | 旧 | 新 |
|----|----|----|
| Java SQL | 未限定 M1 名，依赖 catalog=`innov` | `InnovDao` 一律 `InnovSql.qualify` → `gkxlumenx_{ads,dwd,dim,cfg}.` 2B 名 |
| JDBC | `INNOV_MYSQL_DB=innov` | `gkxlumenx_ads` |
| helm `innovPy.env`（values + values-lumen） | 四层=`innov`，`LEGACY=1` | 四层=`gkxlumenx_*`，cfg=`gkxlumenx_cfg`，`LEGACY=0` |

## 测试结果

- `InnovSqlQualifyTest`（JUnit；本机无 mvn，用同规则 Python 镜像自检 **ok**）：
  - `ads_innovation_event` → `gkxlumenx_ads.innovation_event`
  - `dwm_graph_node` → `gkxlumenx_dwd.graph_node`
  - 已限定名幂等
  - `cfg_index_weight` / `dim_city` 正确
- 现网表：`gkxlumenx_ads.innovation_event=230`，`gkxlumenx_dwd.graph_node=472`，`gkxlumenx_dim.city=73`

## 遗留风险

- 现网要再点 **lumen-svc-platform `helm:deploy`**（Java 镜像 + overlay env）。不要点单服务 `deploy:innov`（盖不了 values 里的库开关）。
- `INNOV_RUN_ON_START=1` 关掉 LEGACY 后 innov-py 会写正式 `gkxlumenx_*`（符合「正式」）。`gkxlumenx_ods` 目前无 `innovation_event`，批处理首次跑会建表。
- 历史库 `innov` 的 M1 表仍在，作快照，运行时不再指向。
- demo `08f6ca9` `helm:deploy` 仍待点（Nacos hook），与本叶无关。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`e1fdff4`
- pipeline：点 **`helm:deploy`**
- 部署 ns=`dev` release `gkxlumen-platform`

## 可观测性（建议）

- 未改 OTel；Java `OTEL_SERVICE_NAME=gkxlumen-innov`

## 涉及文件

- `gkxlumen-innov/src/main/java/com/topcomm/gkxlumen/innov/support/InnovSql.java`
- `gkxlumen-innov/src/main/java/com/topcomm/gkxlumen/innov/support/InnovDao.java`
- `gkxlumen-innov/src/test/java/com/topcomm/gkxlumen/innov/support/InnovSqlQualifyTest.java`
- `gkxlumen-innov/src/main/resources/application.yml`
- `helm/gkxlumen-platform/values.yaml` · `values-lumen.yaml`
- `agent-delivery/architecture-baseline.md` v2.2.6

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| D12 lumen 不写 demo 库 | ✅ 四层指向 `gkxlumenx_*` |
| demo 不写正式 dwd/ads | ✅ 本叶不改 demo |
| 调用链 Java 只读 ADS | ✅ 仍只读；qualify 在 DAO |
| 算法只在 Python | ✅ 未在 Java 写算法 |
| D8/D9/D10 | N/A（无 UI） |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 50000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.45 |
| cost_warn | green |
