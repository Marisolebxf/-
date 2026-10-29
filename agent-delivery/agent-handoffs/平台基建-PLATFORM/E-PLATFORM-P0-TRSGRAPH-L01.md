# E-PLATFORM-P0-TRSGRAPH-L01 · TRSGraph graphd 切换（配置统一指向新库，只重灌 demo_gkx_chain）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-15 淮政玮领取，架构师身份开工。锁定 4 小时。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改各仓已有配置和代码里的 host 默认值。未新增依赖，未改 nGQL，未把口令写入 git。 |

## 范围与实现

- 图客户端默认 graphd 改为 `10.50.75.136:9669`。覆盖 `lumen-algo-py`（chain settings、`graph_project.py`、vendor/entan-py）、`demo-algo-ent-analysis`（settings、k8s、CI、entan/polan 默认 host）、`demo-algo-science`、`demo-svc-topic-py`、`lumen-topic-py`。地址、账号、space 在各仓已有配置文件。口令字段留空，只认 `GKX_NEBULA_PASSWORD` / `LUMEN_ALGO_NEBULA_PASSWORD`。
- 用现有 `project_graph` 从 `10.50.11.76` 的 demo DWD 重灌 `demo_gkx_chain`。返回 `source=nebula`，写入点 157、边 200。随后在新库 `MATCH (v:chain) RETURN id(v) LIMIT 3` 读回 `chain:INB1710`、`chain:INB180102`、`chain:INB1701`。
- 未拷贝旧库文件，未建 `gkx_chain`，未迁 `entan` / `demo_entan` 数据，未改 Java / 前端。
- 运行中的 Pod 尚未 rollout，仍带着旧的 `GKX_NEBULA_HOSTS`。本单未提交、未部署。

## 偏离

- 旧库 `demo_gkx_chain` 此前约 11.4 万点、13.9 万边。本次 DWD 投影只有 chain 43、segment 114、enterprise 0、institution 0，边 belongs_to 114、depends_on 86。`industry_chain_entity_rel` 319 行与事件关系 130 行被现有映射跳过（product / event 无 Tag，企业 belongs_to 与环节 belongs_to 撞名）。差集是加载器口径，不是 TRSGraph 写失败。
- 灌链附带的 industry index rebuild 走了进程内内存 store（本次未设 `MILVUS_URI`），进程退出后不保留。

## 产物清单

- 各仓 settings.yaml、k8s、`.gitlab-ci.yml`、`.env.example`、代码默认 host
- `agent-delivery/paths.yaml`、`repo-registry.yaml`、`graph-engine.md`、`architecture-baseline.md` v2.2.17
- 本 handoff

## 验收证据

- 重灌命令：`python -m lumen_common.algorithms.chain.graph_project`（工作目录 `repos/lumen-algo-py`）。结果 `status=ok`，`space=demo_gkx_chain`，`vertices_written=157`，`edges_written=200`，`source=nebula`。
- 读回：`USE demo_gkx_chain` 成功；`MATCH (v:chain) RETURN id(v) LIMIT 3` 返回三个 chain vid。
- 代码与配置检索：`repos` 与 `.cursor` 下已无 `10.50.75.136:9669` / `192.168.88.44:9669`。历史 handoff、验收文档、归档未改。

## 架构合规自检

1. 算法只在 Python ✅
2. 调用链仍是前端 → Java → Python；Java 未接 graphd ✅
3. 图谱仍是 Nebula 协议 / nGQL，无 Neo4j，无亿集查图 API ✅
4. 可观测埋点未改，既有 OTel 配置保留 ✅
5. CI/CD 本单未提交、未 rollout ✅（设计切换先落配置；部署留待口令 Secret 注入后）
6. demo 未 merge 进 lumen；各仓只改自己的配置 ✅
7. 方案 A 保持：前端不直连 graphd ✅
8. 重灌数据来自 demo DWD，未拷贝 3.8 存储文件 ✅

## Cost 回填

- actual_tokens: 未从计费接口取值
- model_used: grok-4.7
- actual_cost: 0
- cost_warn: green

## 测试结果

- DWD 干跑与实写均连上 `10.50.11.76` 的 demo MySQL，表读取无 `table_errors`。
- 新库读回 3 个 chain vid。`SUBMIT JOB STATS` 已提交，未等待统计作业完成。

## 遗留风险

- 已发布 Pod 仍指向旧 graphd，旧库写入尚未从运行面停掉。下次发布必须先有 `GKX_NEBULA_PASSWORD` Secret，否则新地址会因空口令认证失败。
- `entan` / `demo_entan` 在新库没有数据。指向新库后，这些读路径会失败并按原逻辑回退。
- 点数与旧库不一致。若业务要旧库那 11 万企业点，需要单独确认加载口径，不能靠本次 `project_graph`。

## CI/CD（必填）

- 分支：各仓工作区未提交
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未执行
- dev 测试 URL / 命令与结果：本机直连 `10.50.75.136:9669`，读回 chain vid 见验收证据

## 涉及文件

- `repos/lumen-algo-py/conf/settings.yaml`
- `repos/lumen-algo-py/lumen_common/algorithms/chain/graph_project.py`
- `repos/lumen-algo-py/vendor/entan-py/conf/settings.yaml`
- `repos/lumen-algo-py/vendor/entan-py/conf/settings_policy.yaml`
- `repos/lumen-algo-py/vendor/entan-py/polan/common/config.py`
- `repos/lumen-algo-py/vendor/entan-py/entan/common/nebula.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/common/nebula.py`
- `repos/demo-algo-ent-analysis/conf/settings.yaml`
- `repos/demo-algo-ent-analysis/conf/settings_policy.yaml`
- `repos/demo-algo-ent-analysis/polan/common/config.py`
- `repos/demo-algo-ent-analysis/entan/common/nebula.py`
- `repos/demo-algo-ent-analysis/polan/common/nebula.py`
- `repos/demo-algo-ent-analysis/deploy/k8s/entan-api.yaml`
- `repos/demo-algo-ent-analysis/.gitlab-ci.yml`
- `repos/demo-algo-science/conf/settings.yaml`
- `repos/demo-algo-science/chainan/graph/nebula_schema.py`
- `repos/demo-svc-topic-py/conf/settings.yaml`
- `repos/demo-svc-topic-py/k8s/dev-search-py.yaml`
- `repos/demo-svc-topic-py/.env.example`
- `repos/demo-svc-topic-py/gkx_common/nebula.py`
- `repos/lumen-topic-py/conf/settings.yaml`
- `repos/lumen-topic-py/k8s/dev-search-py.yaml`
- `repos/lumen-topic-py/.env.example`
- `repos/lumen-topic-py/gkx_common/nebula.py`
- `agent-delivery/paths.yaml`
- `agent-delivery/repo-registry.yaml`
- `agent-delivery/graph-engine.md`
- `agent-delivery/architecture-baseline.md`
