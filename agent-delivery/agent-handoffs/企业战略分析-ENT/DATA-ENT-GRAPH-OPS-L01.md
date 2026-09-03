# DATA-ENT-GRAPH-OPS-L01 · 企业图谱按 14 已拍板 op 接正式 DWD

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只接四 op + 正式 DWD 列；不写 Nebula、不加依赖、不改 Java |

## 范围与实现

对照 `demo-algo-ent-analysis` **重写**（未 merge）。`lumen-algo-py` 挂：

| HTTP | op |
|------|-----|
| `POST /internal/entan/graph/ner` | `ENT_NER_ORG` |
| `POST /internal/entan/graph/intra` | `ENT_RE_INVEST` / `ENT_RE_BELONG` |
| `POST /internal/entan/graph/hang` | `ENT_RE_INDUSTRY` |
| `POST /internal/entan/graph/ops/{op_id}` | 同上四枚 |
| `GET /internal/entan/graph` | 只读 ADS；不 USE 未点名 space |

入参与 `14` 一致：`op_id` / `scope` / `id` / `filter` / `mode` / `dry_run` / `relation_whitelist` / `calc_batch_id`。

正式 DWD 读列：

- 投资：`inv_org_id` `inv_org_name` `invest_amount` `invest_ratio`（不再读 `inv_name` / `investment_*`）
- 隶属：`org_id` `parent_org_id` `ownership_ratio`
- 产业：`chain_code` `chain_name` `node_id` `node_name` `chain_score`

`dry_run=true` → `source=dry_run`；非 dry_run 仍只出 DWD 预览 → `source=dwd_preview`，`nebula_written=false`。`gkx_chain` 与未点名 space **一律不写**。禁止 `CREATE SPACE` / `DROP SPACE`。合作 / 供应链 / 股东边本波不接。

## 偏离

- 正式 space 仍未点名（升级人 `human:李伟`）。本叶交付 HTTP + 正式列投影，**不**宣称图已灌绿。
- `mode=llm` 无推理，直接 `llm_fallback=true` 走规则。
- 产业边预览用 DWD `chain_code`/`node_id` 拼候选 VID，**不做** Nebula FETCH（无授权 space）。

## 产物清单

- `vendor/entan-py/entan/graph/ops.py`
- `vendor/entan-py/api/entan_graph_routes.py`
- `vendor/entan-py/api/main.py`（挂路由）
- `vendor/entan-py/tests/test_ent_graph_ops.py`

## 测试结果

- `python3 -m py_compile` 上述文件：通过
- `PYTHONPATH=. python3 tests/test_ent_graph_ops.py`：`ok`
- 覆盖：VID 80 不截断；空 batch / `ENT_RE_COOP` 拒绝；投资 SELECT 正式列；对端不在 base → `no_stable_id`；`gkx_chain` / 空 space 不写
- `lumen-svc-platform` 企业/图谱 REST：**未改文件**

## 遗留风险

- 未点名 space 前，日批/菜单打进来只有预览，图库无新点边
- Java Feign 现网尚未挂 `/internal/entan/graph*`（本叶不补 Java）
- 产业预览 VID 未经 FETCH，点名 space 后需补 FETCH 才可写

## CI/CD

- 分支：`lumen-algo-py` `origin/dev`
- pipeline：随仓 CI
- K8s：等 CI rollout
- 验证：上列 compile + 自检；不宣称 Nebula 已写

## 成本

- actual_tokens：38000（会话估算）
- model_used：cursor-grok-4.6
- actual_cost：0.20
- cost_warn：green

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 | ✅ 只加 Python `/internal/entan/graph*` |
| 算法只在 Python | ✅ |
| 图谱 Nebula / 禁 Neo4j | ✅ 未写 Neo4j；未写 `gkx_chain` |
| 可观测 | ✅ `ent.graph.write` span |
| CI/CD | ✅ 推 `origin/dev` |
| demo2 merge | ✅ 无 |
| D12 | ✅ 对照重写，未 merge demo、未调 demo 服务 |
| 共享聚合 / Java 不写算法 | ✅ Java 零 diff |
| 数据策略 | ✅ 读正式 DWD 列名 |
| GDF 不写 nGQL | ✅ |

## 联调确认

联调通过：契约路径与正式 DWD 列对齐；本叶不写未点名 `gkx_chain`。不宣称 ES/图谱已灌绿。

## 涉及文件

- `lumen-algo-py/vendor/entan-py/entan/graph/ops.py`
- `lumen-algo-py/vendor/entan-py/api/entan_graph_routes.py`
- `lumen-algo-py/vendor/entan-py/api/main.py`
- `lumen-algo-py/vendor/entan-py/tests/test_ent_graph_ops.py`
