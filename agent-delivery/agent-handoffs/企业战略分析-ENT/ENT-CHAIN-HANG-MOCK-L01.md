# ENT-CHAIN-HANG-MOCK-L01 · 企业上链 ENT↔CHAIN 挂点 + Demo mock

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务派单；专责企业上链；未改 `yiji_sim/infer*` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 独立脚本灌两表；复用 ENT 已有 `enterprise_industry_chain` 字段名；不改 facts/infer；`gdf_sim.map_entity_rel` 最小补丁。未用 YAGNI 跳过架构铁律。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 问题清单

- Demo 库若尚无 INB `industry_chain_node`，`--apply` 诚实不写（OPEN-ENT-HANG-01），不造树。
- ENT `gdf_sim.map_industry_chain` 仍会写 `IC-*` + 空 `node_id` 占位；本叶 `--apply` 覆盖能对齐的 `org_id`。
- CHAIN 灌数若先于 ENT `enterprise_base`，`map_entity_rel` 对企业行 skip（lookup 空表），产品行仍写 `p:{credit}:…`。

## 修改内容

- 设计：`storage/CHAIN/etl/pipeline-ent-hang.md`（过程 / 字段对照 / 失败语义 / 与 sim-process 接口）。
- ENT：`dwd-entity.md` §5、`pipeline-demo-mock.md` §7（不上全文复制）。
- Seeds：SEED-08 as-built、SEED-10 上链；CHAIN CHANGELOG 一行；**未翻签** `01-data-flow`。
- Mock：`demo-algo-ent-analysis/scripts/run_ent_chain_hang.py`（`--self-check` / `--apply`）。
- 独占补丁：`demo-algo-science/chainan/llm_ods/gdf_sim.py` `map_entity_rel`：能对上则 `entity_id=org_id`；lookup 失败 skip+log；无 lookup 暂留 credit + honesty。

## 测试结果

- `py -3 scripts/run_ent_chain_hang.py --self-check` → `ent_chain_hang self_check OK hung=3 dropped=1`（华为/中芯/SEED-08 样例挂 `INB1303*`；幽灵 credit drop；无 Paper 点；`facts.iter_located_in` 三边）。
- `map_entity_rel(..., org_by_credit=...)` 离线：对齐 → `org_id`；空 map → skip；`None` → 暂留 credit。
- `--apply` Demo：`demo_gkxlumenx_dwd` 写入 `enterprise_industry_chain=100`、`industry_chain_entity_rel=100`，`dropped=0`，`inb_nodes=96`。未联调前端 / yiji 推理全链，**不写「联调通过」**。
- 未跑无关全仓测试。禁止 commit/push。

## 遗留风险

- OPEN-ENT-HANG-01：无 INB 节点则不上链（本次 Demo apply 已见 96 个 INB 节点，暂未触发）。
- 正式库 `enterprise_industry_chain.org_id` NULL 债仍在；本叶只写 Demo。
- Nebula 投影不在本叶强制（`DEMO-CHAIN-PY-GRAPH-L01`）。

## CI/CD（必填）

- 分支：未 commit（任务禁止）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未做
- dev 测试 URL / 命令与结果：仓根 `demo-algo-ent-analysis`：`py -3 scripts/run_ent_chain_hang.py --self-check` 绿

## 可观测性（建议）

- OTEL_SERVICE_NAME：本叶为离线 ETL 脚本，无新 HTTP 服务
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `repos/demo-algo-ent-analysis/scripts/run_ent_chain_hang.py`（新增）
- `repos/demo-algo-science/chainan/llm_ods/gdf_sim.py`（`map_entity_rel` / apply lookup）
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-ent-hang.md`（新增）
- `agent-delivery/data/data-design/storage/CHAIN/etl/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/etl/pipeline-to-nebula.md`
- `agent-delivery/data/data-design/storage/CHAIN/stores/nebula/graph-chain.md`
- `agent-delivery/data/data-design/storage/CHAIN/seeds/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/CHANGELOG.md`
- `agent-delivery/data/data-design/storage/ENT/stores/mysql/dwd-entity.md`
- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-demo-mock.md`
- `agent-delivery/data/data-design/storage/ENT/etl/README.md`
- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-to-nebula.md`
- `agent-delivery/data/data-design/storage/ENT/seeds/README.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 脚本 + `gdf_sim.py` |
| 调用链 FE→Java→Python `/internal` | ✅ 本叶不新增越层；不改灌数按钮 |
| 图谱 Nebula，禁 Neo4j | ✅ 仅文档指针；不强制投影 |
| 可观测 | ✅ 无新服务；未加假埋点 |
| CI/CD | ✅ 禁止 commit；未改 pipeline |
| demo 不 merge lumen | ✅ 只动 demo-algo-* + 编排存储文 |
| D12 demo/lumen 隔离 | ✅ 只写 `demo_*`；`assert_demo_mysql_targets` |
| 禁 APPLY 正式库 | ✅ |
| 01-data-flow 不翻签 | ✅ |
| 不改 infer/GraphView LLM | ✅ |
| D8/D9/D10 | N/A 无 UI |

## 范围对照

招标/基线：企业挂产业链节点（ENT 店面表第 8 行 + CHAIN `industry_chain_entity_rel`）。偏离：无。as-built：org_id↔INB，对不齐 drop。

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 88000 |
| model_used | grok-4.6 |
| actual_cost | 0.53 |
| cost_warn | green |
| 口径 | algorithm 75/25 × Sonnet 公开价档近似（$3/$15 /$M）；source: session_estimate |
