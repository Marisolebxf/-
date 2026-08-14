# DEMO-CHAIN-UI-SEED-ODS-L01 · 灌数主路径 llm_ods → 模拟 GDF → DWD v5 → ADS v2

> 口径：`storage/CHAIN/etl/pipeline-demo-mock.md` §5  
> 日期：2026-08-14  
> Task ID：`DEMO-CHAIN-UI-SEED-ODS-L01`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 A 段；lock 24h；结构歧义升级 `human:李伟`（本单未自创表） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 handoff / 只写 demo_* 闸门 / 调用链（算法只在 Python）/ ES·Nebula 失败不阻断。system-test 只改灌数按钮与状态，不改 BasicIndicators。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 监管拍板（已落地）

| # | 口径 | 落地 |
|---|---|---|
| 1 | 默认 append | `POST /internal/run-chain-pipeline` body `{mode}`；主按钮追加 |
| 2 | 两种 mode 都 TRUNCATE ADS 后按当前 DWD 全量重算 | `ads_v2.recalc_ads` |
| 3 | 主按钮追加 + 下拉 replace | `BasicPage.vue` split-button |

```text
append（默认）：保留 ODS/DWD 明细 → 新批次写入 demo ODS 四表 → 模拟 GDF INSERT demo DWD v5 → ADS v2 全量重算
replace：TRUNCATE 约定四表 ODS + 映射 DWD → 同路径 → ADS 全量重算
```

禁止 `init_schema()`（会打到正式库名）。旧 `mock_chain` 仅 `CHAIN_SEED_LEGACY_MOCKGEN=1`。

## 范围与实现

范围：Demo 灌数主路径（llm_ods → 约定 ODS 四表 → 模拟 GDF → DWD v5 → ADS v2）+ system-test 灌数据按钮 + **`/v1/chain/**` 改读新表**（补 2026-08-14 晚间缺口：列表/A1–A9 不再读正式库旧 `chain_*`）。

实现见下方 as-built 与修改内容。

## 偏离

- 正式库无 v5 `industry_chain` 时 `CREATE LIKE` 失败，改为仅在 `demo_gkxlumenx_dwd` 按 v5 DDL 建表（不碰正式库）。
- ES/Nebula 未启用 → `skipped`，不阻断（派单允许）。
- 投融资 ADS `INVEST_COUNT` 不写（QC07）；DWD 12 条标 `source_system=mock`。
- 旧 A/M1–M13 默认不跑。

## 产物清单

- 代码：`demo-algo-science` `ef09333`；`demo-ui-system-test` `b40aaa7`
- 编排 as-built：`storage/CHAIN/etl/pipeline-demo-mock.md` §5 等（orchestration `89dd7c4` / 会话报告另有 `5e8f890`）
- 本 handoff

## 前后对比

| 层 | as-is | as-built |
|---|---|---|
| 贴源 | `CHAIN_STEPS` 以 `mock_chain` 打头，qualify 写正式 `gkxlumenx_*` / 旧 `chain_*` | 默认 `chainan.llm_ods` → `demo_gkxlumenx_ods` 四表 |
| ODS→DWD | 无 | `gdf_sim.py` → `industry_chain_*` v5 |
| ADS | 旧 A/M 写 `ads.chain_*` | `ads_v2.py` 十表同步面；不写 CMS 历程/介绍 |
| 幂等 | mock 直写 | append 追加；replace 才清空四表+映射 DWD |
| UI | 单按钮，文案 `gkxlumenx_*` / `dwd.chain_*` | split-button；`ODS n｜DWD n｜ADS n`；只写 demo_*；**基础指标读 INB 新表** |
| 旁路 | mock_chain 即主路径 | 仅 `CHAIN_SEED_LEGACY_MOCKGEN=1` |

ODS 四表（角色=ODS，供应方表名带 `dwd_`）：`dwd_industry_chain_info` / `dwd_org_industry_tags` / `dwd_org_industry_product_tags` / `dwd_industry_chain_news_info`。键分别为 `industry_link_code` / `credit_code` / `credit_code` / `id`。**不用**不存在的 `dwd_org_industry_chain_dtl`。`chain_id`/`node_id`/`industry_id` = 供应方 INB（Q053）。

## 修改内容

### demo-algo-science

- `chainan/llm_ods/*`：schema 转调 `entan.llm_ods.schema`（K8s 回退 `_schema_parser.py` + vendor CSV）；`assert_demo_mysql_targets`；确定性 SEED-01～08；模拟 GDF；ADS v2；ES/Nebula fail-soft
- `scripts/run_all.py`：`--chain --mode --self-check`；主路径 `run_chain`；`--self-check` 不拉 innov/networkx
- `api/main.py`：body `{mode}`；去掉 chain `init_schema`；status 含 ods/dwd/ads/`current_step`/`projection`
- **`chainan/llm_ods/read_v2.py` + `api/main.py` `/v1/chain/**`：只读 demo DWD v5 / ADS v2（INB）；删除 `_q` 旧表路径**
- `tests/test_chain_read_v2.py`
- `conf/settings.yaml`：`ods_db/dwd_db/ads_db: demo_gkxlumenx_*`
- `tests/test_chain_llm_ods.py`

### demo-ui-system-test

- `src/views/chain/pages/BasicPage.vue`：对齐企业 split-button
- `src/api/chain/index.ts`：`runChainPipeline(mode)`
- `src/views/chain/components/BasicIndicators.vue` / `PanoramaGraph.vue` / `bidBasicIndicators.ts`：MetricHint / ADS 表名改 v2；A3/A4/A5 占位（不造假）

### gkx-orchestration

- `storage/CHAIN/etl/pipeline-demo-mock.md` §5 as-built
- `storage/CHAIN/seeds/README.md` 矩阵改为脚本入口
- `pipeline-ods-to-dwd.md` / `pipeline-dwd-to-ads.md` Demo 指针

## 测试结果

- `PYTHONPATH=. python tests/test_chain_read_v2.py` → `ok`（形变 + live list 为 INB 非 CH*）
- live：`list` 10 条 INB；`INB1303` A2 enterprise_count=72；A6/A9/A7/M1 有数；不再读 `gkxlumenx_dwd.chain`
- Demo MySQL（`settings.yaml` `192.168.88.43`，库 `demo_gkxlumenx_*`）**replace + append 实跑**：

| 项 | replace 后 | append 后 |
|---|---|---|
| demo ODS `dwd_org_industry_tags` | 104 | 128 |
| demo DWD `industry_chain` | 10 | 10（链结构去重） |
| demo DWD node / node_rel / entity_rel | 96 / 88 / 273 | 96 / 88 / 336 |
| demo ADS `industry_chain_metric_fact` | 52 | 52（全量重算） |
| `industry_chain_market_observation` | 0 | 0 |
| `industry_chain_milestone_event` | 0 | 0 |
| ADS `narrative` | 0 | 0 |
| 空节点 `INB13030212` | 1 节点 / 0 企业 | 同 |
| 深圳企业（entity_rel.ext.city） | 53 | 53 |
| `M_CHAIN_INVEST_COUNT` | 0（QC07 不造假） | 0 |
| 正式 `gkxlumenx_ods.dwd_org_industry_tags` | **20000 未变** | **20000 未变** |
| 正式 `gkxlumenx_dwd.chain`（旧表） | **8 未变** | **8 未变** |
| 正式 `gkxlumenx_dwd.industry_chain` | 不存在（CREATE LIKE 失败后按 v5 DDL 仅在 demo 建） | 同 |

投影：`elasticsearch.enabled=false` / `nebula.enabled=false` → status `skipped`（诚实，不阻断）。

## 遗留风险 / 开放项

| 项 | 说明 |
|---|---|
| OPEN-CHAIN-FLOW-01 | 正式 GDF DAG/cron 仍开；本单手工/API 灌数 |
| Q054 | DWD 投融资 12 条 `source_system=mock` 🧪；ADS 不写 INVEST_COUNT |
| CMS 历程/介绍 | 不灌；`narrative`/`conclusion` 空表 |
| Job Snapshot | 不写入 `graph_snapshot`（仅全景节点边） |
| 旧 A/M1–M13 | 默认不跑。**已改** `/v1/chain/list` 与 A1–A9 / M1 全景读 `demo_gkxlumenx_dwd.industry_chain` + ADS v2；Job 面 M3–M13 空包络不回落正式库旧表 |
| `relation_id` | v5 `VARCHAR(64)`，实体关系改短前缀 `er:`/`eer:`（未加列宽） |

## CI/CD

- 分支：`demo-algo-science` / `demo-ui-system-test` / `gkx-orchestration` 均为 `dev` → `origin/dev`
- commit：`demo-algo-science` `ef09333`；`demo-ui-system-test` `b40aaa7`；`gkx-orchestration` `89dd7c4`
- pipeline URL / ID：push 后由 CI 接管
- K8s rollout：demo-algo-science 随 CI；本会话未等绿
- 本地验收：`python scripts/run_all.py --self-check`；`run_seed('replace'|'append')`

## 可观测性

- OTEL_SERVICE_NAME：沿用 innov-py / chainan 已有 `TraceHeaderMiddleware`
- 本单未改埋点

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 模拟 GDF / ADS 重算在 `chainan/llm_ods` |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ UI 仍走 `/innov/v1/industry/internal/run-chain-pipeline` |
| 3 | 图谱 Nebula | ✅ 投影失败不阻断；未装客户端 → skipped |
| 4 | 可观测 | ✅ 未拆已有 OTel 中间件 |
| 5 | CI/CD | ✅ 按仓 push `origin/dev`；禁止 force |
| 6 | demo 不 merge lumen | ✅ 只改 demo-algo-science / demo-ui-system-test |
| 7 | Java 不写算法、不直连 nGQL | ✅ 本单无 Java |
| 8 | 只写 demo_* | ✅ `assert_demo_mysql_targets`；正式库行数未变 |
| 9 | D8 Design | N/A 管理端 Element Plus（D11 豁免）；只改灌数交互对齐企业 |
| 10 | D9 血缘 | ✅ ADS metric_id 用矩阵口径；QC07/市场规模不造假 |

## 涉及文件

- `repos/demo-algo-science/chainan/llm_ods/`
- `repos/demo-algo-science/scripts/run_all.py`
- `repos/demo-algo-science/api/main.py`
- `repos/demo-algo-science/conf/settings.yaml`
- `repos/demo-algo-science/tests/test_chain_llm_ods.py`
- `repos/demo-ui-system-test/src/views/chain/pages/BasicPage.vue`
- `repos/demo-ui-system-test/src/api/chain/index.ts`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/CHAIN/seeds/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-ods-to-dwd.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-dwd-to-ads.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~220000（估，含续会话） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 5.5 |
| cost_warn | green |

## 联调确认

脚本侧 **replace + append** 已在 `demo_gkxlumenx_*` 跑通，正式库 `gkxlumenx_ods.dwd_org_industry_tags=20000`、`gkxlumenx_dwd.chain=8` 未变。UI 发版与 K8s 服务是否已拉新镜像，待 `human:淮政玮` 确认后签收。本 agent **不**把任务标 `done`。
