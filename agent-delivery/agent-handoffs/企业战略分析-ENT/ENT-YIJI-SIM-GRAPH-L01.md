# ENT-YIJI-SIM-GRAPH-L01 · Demo yiji-sim 企业维实体/事实/推理落 Nebula

> 内容按本次实测与代码实写。as-built **已嵌入** CROSS-KG `03-详细设计.md` §1.4.3 第 7 节。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人派子智能体开工；仓 `demo-algo-ent-analysis`；禁止 commit/push |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：B2 规则抽到 `entan/yiji_sim`；`nebula_loader` 收成 persist；未新开写 graphd 路径；未加 NLP 依赖 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | CROSS-KG 03 §1.4.3 / §1.4.4 · graph-engine.md §2 |

## 问题清单

- Demo DWD 无 `industry_chain_entity_rel`：用最小账本 `enterprise_graph_rel`，不伪造 CHAIN 全套。
- `enterprise_industry_chain` bootstrap 可能无 `org_id`：`fetch_tables` 回退 `enterprise_code` join。
- 现网 Nebula space 配置为 `entan`（已复用）；规范名 `demo_entan` 用环境变量切换。
- G2 社群 / 相似专家未注册 → **501**（仅文档 + `g2_http_status`）；`find_path` 已有。
- `incremental.add_enterprise` 仍走旧 1 跳公式，未并入 `located_in`（画像增量编辑旁路）。

## 修改内容

- 新建 `entan/yiji_sim/`：`pipeline` / `facts` / `entities` / `infer` / `writeback` / `persist` / `selfcheck`；场景矩阵 `scene_coverage.md`；fixture `fixtures/news_batch.json`。
- 入口 `scripts/run_yiji_sim.py`；`python -m entan.yiji_sim --offline --self-check`。
- CUT-D7 DDL：`scripts/mysql/demo_dwd_enterprise_graph_rel.sql`。
- `entity.py` B2 改调 `facts.fetch_tables` + `entities.assemble_fact_graph`（ADS 旧 UI 不断）。
- `nebula_loader`：新增 Tag `chain_node`/`technology`、Edge `located_in`/`produces`；默认 `build_and_persist`，`--from-ads` 回退。
- `scripts/run_all.py` `load_nebula_safe`：先 yiji-sim，失败再 ADS，均失败不阻断。
- `incremental.py`：`PT_MAP` 改从 `facts` 导入（一套规则）。
- `/v1/graph`、`/v1/graph/path` 成功时附 `honesty.capability=yiji-sim`。
- **已改** CROSS-KG `03-详细设计.md` §1.4.3 第 7 节（父会话嵌入 as-built）。

## 测试结果

- `python scripts/run_yiji_sim.py --offline --self-check` → **OK**（nodes=8 fact=8 infer=3 drops=1 ledger=11）。
- `python -m entan.yiji_sim --offline --self-check` → **OK**。
- `--offline --sql-out`：SQL 含 `valid_from` / `batch_id` / `origin='infer'`。
- `--apply`：本机连上 `demo_gkxlumenx_dwd`，writeback=439。
- `--apply --persist`：Nebula space=`entan` available，persist 节点=159 边=439，`source=nebula`。
- 未跑 CI；未 push。

## 遗留风险

- 增量编辑路径无 `located_in`，与全量 yiji-sim 子图可能不一致。
- 推理规则为确定性正则（Mock），不是注册 NLP；准生产须换亿集脚本运行时。
- live DWD 企业名对不齐 fixture「华为/清华大学」时 infer 命中少（本次 live infer_edges=1），属对齐 drop，不是失败。
- PG 查询回退仍在 API；lumen 禁用（graph-engine §5.5）。

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` 工作区未提交（用户禁止 commit/push）
- commit：无
- pipeline URL / ID：无（未 push，不编造绿）
- 部署 namespace / 镜像 tag：无
- K8s rollout：未做
- dev 测试 URL / 命令与结果：见「测试结果」本地命令

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用既有 API 探活；本叶为离线建图脚本，未新加 exporter
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ `entan/yiji_sim` |
| 调用链前端→Java→Python | ✅ 本叶不改前端/Java；不直连 nGQL 出 Java |
| 图谱 Nebula，禁止 Neo4j | ✅ space `entan`（配置复用） |
| D12 不改 lumen / 不打 demo 当正式 | ✅ 只动 demo-algo-ent-analysis + 编排 handoff/embed |
| CUT-D7 推理先回写 DWD 再 persist | ✅ `enterprise_graph_rel` origin=infer |
| 禁止直连供应方 gkx | ✅ 只读 demo DWD + fixture |
| 禁止第三条写 graphd | ✅ persist 调用 `nebula_loader._load_*` |
| 禁止论文/专利当点 | ✅ N102 drop；技术点=环节名 |
| 禁止抄亿集 76 URL | ✅ |

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/yiji_sim/**`
- `repos/demo-algo-ent-analysis/entan/graph/entity.py`
- `repos/demo-algo-ent-analysis/entan/graph/nebula_loader.py`
- `repos/demo-algo-ent-analysis/entan/graph/incremental.py`
- `repos/demo-algo-ent-analysis/scripts/run_yiji_sim.py`
- `repos/demo-algo-ent-analysis/scripts/run_all.py`
- `repos/demo-algo-ent-analysis/scripts/mysql/demo_dwd_enterprise_graph_rel.sql`
- `repos/demo-algo-ent-analysis/docs/nebula-space-schema.md`
- `repos/demo-algo-ent-analysis/api/main.py`（honesty.capability）
- `agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-YIJI-SIM-GRAPH-L01.md`
- `agent-delivery/agent-handoffs/产品整体定义/跨系统-知识图谱/_embed-ENT-YIJI-SIM.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 2.80 |
| cost_warn | green |
