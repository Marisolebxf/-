# ENT-YIJI-INFER-LLM-L01 · 图边 LLM 旁路（语料 DWD industry_analysis_*）

> 内容按本次实测与代码实写。03 as-built：**§1.4.3** 补一句（默认正则；`backend=llm` 图边专用，语料=DWD `industry_analysis_*`，不是四要素 IE）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务派单；开工时已 `in_progress`；仓 `demo-algo-ent-analysis` + `demo-ui-system-test` GraphView；禁止 commit/push |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：正则 `infer.py` 零改动；LLM 另文件；llm_client 用 urllib 不新加 httpx；未混入 `run_llm_ods.py` 50 户路径 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 问题清单

- Demo 库六表可能仍未建（OPEN-CHAIN-INDANA-01）：本叶提供 `scripts/run_indana_dwd.py --apply` **仅 demo**。
- 未对 K8s / GraphView 现网点「推理入图」做联调（接口已挂、待联调）。
- LLM 无 Key：HTTP **501** + honesty，不编边。

## 修改内容

- `entan/yiji_sim/infer.py` 正则原样保留；`ENTAN_YIJI_INFER_BACKEND=rule|llm` 默认 rule。
- 新增 `infer_llm.py` + `prompts/infer_triples_v0.1.txt` + `fixtures/llm_triples.json`；解析后走 `infer.build_catalog` / `_resolve`。
- `entan/common/llm_client.py`：对齐 tech_news OpenAI 兼容，stdlib urllib，禁止跨仓 import。
- `corpus.py`：读 `industry_analysis_documents`（及 companies/industries）；`corpus_id=document_id`。
- `scripts/mysql/demo_dwd_industry_analysis.sql`（真源头注释）+ `scripts/run_indana_dwd.py`。
- API：`GET /v1/graph/industry-analysis/documents`、`POST /v1/graph/infer`。
- GraphView：正则/LLM、persist、文档下拉、「推理入图」、五步过程面板；「模拟新增企业入库」未改成抽边入口。
- 03 §1.4.3 补一句。

## 测试结果

- `python scripts/run_yiji_sim.py --offline --self-check` → **OK** `nodes=8 fact=8 infer=3 drops=1 ledger=11`
- `python scripts/run_yiji_sim.py --backend llm --offline --self-check` → 同上 + `yiji_sim llm offline self_check OK infer=3 drops=1`（无 Paper 点）
- `python scripts/run_indana_dwd.py --self-check` → **OK** 六表名
- `python scripts/run_indana_dwd.py --apply` → 写入 `demo_gkxlumenx_dwd` statements=18（未碰正式库）
- 本机 `run_graph_infer(backend=rule, persist=false, document_id=DOC-HW-PKG)` → extracts=2（located_in + produces）；CUT-D7 skip
- 本机无 Key：`backend=llm` → http_status=501、步骤2=501、infer_edges=[]
- GraphView / K8s 现网：**未联调**

## 遗留风险

- OPEN-CHAIN-INDANA-01：现网 demo DWD 可能仍无六表；GET documents 返空列表 + honesty。
- 无 Key 时 LLM 路径 501，前端步骤 2 显示 501。
- persist=true 依赖 Nebula；失败写 honesty.persist_error，不装成功。

## CI/CD（必填）

- 分支：工作区未提交（用户禁止 commit/push）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未做
- dev 测试 URL / 命令：本地 `--offline --self-check`

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用既有 FastAPI instrument
- 新接口走现有 TraceHeaderMiddleware
- Tempo / Loki：无新抽样

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ `infer_llm.py` / `corpus.py` |
| 调用链前端→Java→Python | ✅ demo 前端直连既有 `/entan/v1`；未改 Java；未直连 nGQL 出 Java |
| 图谱 Nebula，禁止 Neo4j | ✅ persist 仍走 `persist_graph` |
| D12 不改 lumen / 不打 demo 当正式 | ✅ 只动 demo-algo-ent-analysis + demo-ui-system-test |
| 禁止直连供应方 gkx | ✅ 只读 demo DWD `industry_analysis_*` |
| 禁止素表 documents / 资讯表冒充 | ✅ |
| 禁止新依赖 transformers/spaCy | ✅ urllib |
| 禁止新建 ods_news_event | ✅ |
| 禁止改 /tech-news | ✅ |
| CUT-D7 persist=false 预览 | ✅ 步骤 skip |

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/yiji_sim/infer_llm.py`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/corpus.py`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/pipeline.py`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/prompts/infer_triples_v0.1.txt`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/fixtures/llm_triples.json`
- `repos/demo-algo-ent-analysis/entan/common/llm_client.py`
- `repos/demo-algo-ent-analysis/api/main.py`
- `repos/demo-algo-ent-analysis/scripts/run_indana_dwd.py`
- `repos/demo-algo-ent-analysis/scripts/mysql/demo_dwd_industry_analysis.sql`
- `repos/demo-ui-system-test/src/views/entan/components/GraphView.vue`
- `repos/demo-ui-system-test/src/api/entan/index.ts`
- `agent-delivery/agent-handoffs/产品整体定义/跨系统-知识图谱/03-详细设计.md`
- 本 handoff

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 105000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 3.10 |
| cost_warn | green |
