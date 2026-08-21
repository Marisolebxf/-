# POLICY-NEBULA-PROJECT-CHAIN-L01 · 政策图谱投影一张 G

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `POLICY-NEBULA-PROJECT-CHAIN-L01` |
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| status at handoff | `in_progress`（交付后由 MCP 推进，不自行 done） |
| repo / branch | `demo-algo-ent-analysis` / `dev` |

## Ponytail

- ponytail: full
- 复用仓内 `nebula3-python`、连接池和 CHAIN 既有 VID/Tag 规则；未新增依赖、未另建政策本体。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 会签态 | `approved`（`human:淮政玮`，2026-08-21） |
| 图 diff | 已把图中 `polan → demo_gkx_chain` 实线落实为真实 loader + nGQL 读路径；`gkx_policy` 仍为虚线 as-built 且本叶零写入；`tech/talent` 仍不上图。源图无需改线。 |

## 范围与实现

1. `polan` 默认并强制 `space=demo_gkx_chain`、`vid_length=80`；运行时若配置 `gkx_chain`、`gkx_policy` 或其他 space 立即拒绝。
2. loader 只在已存在的 `demo_gkx_chain` 执行 `USE`，增量 `CREATE TAG IF NOT EXISTS policy` 和四类 `CREATE EDGE IF NOT EXISTS`；代码中无 `CREATE SPACE` / `DROP SPACE`。
3. 政策 VID 固定 `pol:{policy_id}`。产业、企业、机构只在稳定 ID 可解析且既有 `chain:/segment:/ent:/inst:` 顶点实际存在时挂边；无法对齐则计数跳过，不复制底图本体。`tech/talent` 本波跳过。
4. `/v1/policy/graph` 真实执行 Nebula nGQL 后才返回 `source=nebula`；探活或查询失败则回退 ADS/MySQL/SQLite 并返回真实后端名。
5. CI 在 demo API Deployment 上注入 `POLAN_NEBULA_*`，与同 Pod 的 `ENTAN_NEBULA_SPACE=demo_entan` 隔离，避免共享 `GKX_NEBULA_SPACE` 串库。

## 产物

- 代码 commit：[`32124a03d35428599bb375a74152953382c63a64`](https://gitlab.htmisoft.net/gkx-lumen/demo-algo-ent-analysis/-/commit/32124a03d35428599bb375a74152953382c63a64)
- 分支：`origin/dev`（已推送）
- 主要文件：
  - `polan/common/nebula.py`
  - `polan/graph/nebula_loader.py`
  - `polan/graph/nebula_query.py`
  - `api/policy_routes.py`
  - `conf/settings_policy.yaml`
  - `deploy/k8s/entan-api.yaml`
  - `.gitlab-ci.yml`
  - `tests/test_policy_nebula.py`

## 验收证据

### 自动测试

- `python -m pytest tests/test_analysis.py tests/test_policy_nebula.py -q`
- 结果：`42 passed`；仅 FastAPI 上游 HTTP 422 常量弃用告警 2 条。
- `python -m compileall -q polan api tests/test_policy_nebula.py`：通过。
- `git diff --check`、IDE lints：通过 / 0 error。

### Nebula 实投影与 nGQL

- `demo_gkx_chain` 实际 `USE`：`available=True`。
- 实投影结果：
  - `space=demo_gkx_chain`
  - policy 节点写入 `47655`
  - 政策边写入 `398`
  - 跳过：industry `850`、enterprise `20`、org `574`、service `3`、talent `5`；原因均为当前 ADS 镜像缺稳定挂接 ID 或本波明确不上图。
- 真实 nGQL 抽样：Top 3 政策中心返回 `nodes=24`、`edges=22`。

### CI / K8s / 可观测

- CI 产物镜像：`harbor.htmisoft.net/gkx/gkx-entan-py-api:32124a03`
- namespace / Deployment：`dev` / `demo-platform-entan-py`
- rollout：Pod `demo-platform-entan-py-c4c5779f8-xlnf2`，`1/1 Running`，`restart=0`
- Pod 环境：`POLAN_NEBULA_ENABLED=1`、`POLAN_NEBULA_HOSTS=192.168.88.43:9669`、`POLAN_NEBULA_SPACE=demo_gkx_chain`、`POLAN_GRAPH_BACKEND=nebula`
- K8s 服务实调：`GET /v1/policy/graph?limit=3` → HTTP 200，`source=nebula`、`nodes=24`、`edges=22`
- OTEL service：`gkx-entan-py`
- trace_id：`1854b8f4688ca5206b10e22cfdb1ed3e`
- span_id：`e9923b649e981239`

## 架构合规自检

- ✅ 算法只在 Python；未改 Java / 前端 / lumen
- ✅ Demo 调用链保持前端 → 网关 `gkx-policy` → Python `polan`
- ✅ 图谱仅 NebulaGraph；未引入 Neo4j
- ✅ 一张 G：政策仅投影 `demo_gkx_chain`
- ✅ 无写 `gkx_chain`；无 `CREATE/DROP gkx_policy`；无 `DROP SPACE demo_gkx_chain`
- ✅ 复用 CHAIN `chain/segment/enterprise/institution`，未复制本体
- ✅ API 只有真实 nGQL 成功才标 `source=nebula`，失败诚实回退
- ✅ D12：未让 lumen 调 demo 服务
- ✅ 可观测：K8s 实调日志含 trace/span

## 偏离说明

- 当前 `policy_graph_node.props` 的产业/企业/机构大多没有 `industry_link_code` / `org_id` 等稳定 ID，因此本轮主要落政策点及 policy→policy `cite` 边；未按名称猜测挂接，符合“对不齐则不上图”。
- approved 流图已准确表达目标，本叶未修改源图；本 handoff 记录 as-built 落实证据。

## Cost 回填

- actual_tokens: 80000
- model_used: GPT-5.6
- actual_cost: 0.40
- cost_warn: green
