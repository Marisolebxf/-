# DEMO-ENT-LLM-ODS-EXPAND-L01 · 企业 Demo 覆盖扩表合包

> 口径：`storage/ENT/etl/pipeline-demo-mock.md` · `storage/ENT/seeds/README.md`  
> 日期：2026-08-17  
> 格式参考 `templates/handoff-template.md`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 用户指示先签 TRIPLE 再开本单 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `build_offline_rows` / 既有 nebula_loader schema；未加 MinIO SDK。未用 YAGNI 跳过 handoff / 调用链。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 问题清单

- [x] 招投标只灌中标、缺采购角色
- [x] seeds 矩阵招投标/风险/MinIO/图谱仍写「待扩展」
- [x] Nebula space 未在 `demo_entan` / `demo_gkx_enterprise` 间定名
- [ ] 本机 `seed_demo_graph.py --apply`：graphd `192.168.88.43:9669` 超时（脚本/nGQL 已出，待内网补灌）
- [ ] 全链路强验收建议等 `DEMO-ENT-UI-SEED-ODS-L01` 待测合入

## 范围与实现

对照 seeds 矩阵扩 Demo 覆盖，不扩招标功能点。只写 `demo_gkxlumenx_ods` / `demo-gkx-analysis-results` / `demo_entan`。

| 块 | as-built |
|---|---|
| A 招投标 | `dwd_bid_base_out` + `dwd_bid_win_candidate_out`（relate_type=3 中标）+ `dwd_bid_purchase_agency_out`（relate_type=1 采购）；GDF `enterprise_bid.role` 含中标/采购 |
| A 产业链 | 既有 `dwd_org_tech_tag` + `gdf_sim.map_industry_chain`；上链仍 `run_ent_chain_hang.py` |
| A 风险 | `dwd_org_company_abnormal` / `company_punish` / `opt_judicial_case` 三类入 REQUIRED 与自检 |
| B 可选 | `stock_*`、`special_*`（港/台/澳）已纳入，不延期 |
| C MinIO | fixture HTML + `object-meta.json`；`scripts/seed_demo_minio.py` 拷到 `out/minio/...`；不连真实桶、密钥不入库 |
| D Nebula | **定名 `demo_entan`**（弃用 `demo_gkx_enterprise`）；`scripts/seed_demo_graph.py` 灌 1 条 `supply`；settings/K8s `ENTAN_NEBULA_SPACE=demo_entan` |

## 偏离说明

无招标范围偏离。`dwd_bid_target_item_out` 未灌（标的物明细非最低验收）。`dwd_org_risk_shixin` / `tax_punish` / `zhixing` 未纳入（三类风险已满）。直写 graphd 本机超时，以 `--self-check` / `--ngql-out` 为脚本验收，内网再 `--apply`。

## 产物清单

- `repos/demo-algo-ent-analysis`：`entan/llm_ods/generate.py` / `self_check.py` / `gdf_sim.py` / `demo_graph.py` / `fixtures/minio/**`；`scripts/seed_demo_minio.py` / `seed_demo_graph.py`；`conf/settings.yaml`；`deploy/k8s/entan-api.yaml` / `entan-worker.yaml`
- `gkx-orchestration`：`storage/ENT/seeds/README.md`；`storage/ENT/etl/pipeline-demo-mock.md`；本 handoff；TRIPLE 监管签收补记

## 验收证据

- `python scripts/run_llm_ods.py --self-check` → OK（含 bid 三表 + 三类风险 + `demo_entan` nGQL）
- `python scripts/seed_demo_minio.py --self-check` → OK
- `python scripts/seed_demo_graph.py --self-check` → OK（nodes=2, edges=1, space=demo_entan）
- `python test_llm_ods_gdf_sim.py` → OK
- `python test_llm_ods_profiles.py` → OK
- `--apply`：本机 graphd 超时，未写入；nGQL 可 `--ngql-out`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ |
| 前端 → Java → Python `/internal/*` | ✅ 本单不改前端、不越层 |
| 图谱 Nebula，禁止 Neo4j | ✅ space=`demo_entan` |
| 可观测 | ✅ 未删既有 OTel |
| CI/CD | ⬜ 未 push，无新 pipeline |
| demo2 不 merge lumen | ✅ 只改 demo-algo + 编排口径 |
| 共享聚合 / Java 不写算法 | ✅ |
| 数据策略 ADS 先行 / Mock | ✅ 写 demo ODS |
| D8 Design | N/A 无 UI |
| D9 指标 8 件套 | N/A 本单无新统计数字 |
| D10 交互规范 | N/A |
| D12 lumen 不调 demo 服务 | ✅ 未改 lumen |

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` 工作区（未 commit）；编排仓 handoff/口径待 commit
- commit：—
- pipeline URL / ID：—
- 部署 namespace / 镜像 tag：—
- K8s rollout：未发
- dev 测试 URL / 命令与结果：见验收证据（离线自检）

## 可观测性

- OTEL_SERVICE_NAME：沿用既有 entan API
- Tempo / Loki：未抽样

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 120000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 3.5 |
| cost_warn | green |

## 遗留风险

- 本机无法连 graphd，demo_entan 尚未在 88.43 落地
- 灌数 UI 主路径仍 `pending_test`，全链路强验收未做
- Helm 真源若另写 nebula space，需与 `ENTAN_NEBULA_SPACE=demo_entan` 对齐（bootstrap yaml 已加）

## 涉及文件

- `entan/llm_ods/generate.py` `self_check.py` `gdf_sim.py` `demo_graph.py` `README.md`
- `entan/llm_ods/fixtures/minio/**`
- `scripts/seed_demo_minio.py` `scripts/seed_demo_graph.py`
- `conf/settings.yaml` `deploy/k8s/entan-*.yaml` `entan/common/nebula.py`
- `agent-delivery/data/data-design/storage/ENT/seeds/README.md`
- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-demo-mock.md`
