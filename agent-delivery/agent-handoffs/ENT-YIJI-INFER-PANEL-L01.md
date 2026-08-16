# ENT-YIJI-INFER-PANEL-L01 · 抽出结果明细（0 条也展示）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 续修：过程区只显示 extracts=0 / 请刷新 GET /v1/graph，抽出 0 条时表格被藏掉 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过诚实空结果；正则 infer.py 三条规则未改语义，只加扫描明细与中文原因 |

## 问题清单

- `DOC-PAPER` 正文含「论文/专利号」，三条规则均未命中，drop `unresolved_no_paper_vertex`。这是诚实空结果，不是接口失败。
- 旧 UI 用 `v-if="inferExtracts.length"` 把明细表藏掉，用户只看到 5 步计数。
- 现网步骤文案曾是英文计数 +「请刷新 GET /v1/graph」，需前后端一起滚到 `origin/dev`。

## 修改内容

- `demo-algo-ent-analysis`：`run_infer` / `build_bundle` / `POST /v1/graph/infer` 增加 `attempts`（每篇 × 三条规则的命中、span、捕获组）、`drops[].reason_zh`、`document.body_preview`。
- `demo-ui-system-test` `GraphView.vue`：抽出结果区始终展示语料、规则扫描、三元组（空态说明）、丢弃原因+原文、预览边。
- 未改正则三条规则；未改 `/tech-news`；未新开 Java。

## 测试结果

- `python -m entan.yiji_sim.selfcheck`：`yiji_sim self_check OK nodes=8 fact=8 infer=3 drops=1 ledger=11`
- 自检断言：N102 三条规则均未命中；`unresolved_no_paper_vertex` 带 `reason_zh` 与 `span`。
- 现网验收（滚完 CI 后）：http://192.168.88.50:30889 `#/entan/graph` 选 `DOC-PAPER` → 预览推理，应看到正文摘录、规则扫描 3 行未命中、抽出 0、丢弃 1 条中文原因。

## 遗留风险

- 未写「联调通过」。K8s 未发布前现网仍是旧 5 步文案。
- `GET /v1/graph` 仍只投影当前图，抽出明细只在 `POST /v1/graph/infer` 响应与面板里。

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` / `demo-ui-system-test` 的 `origin/dev`
- commit：algo `b039ca7`；ui `2edd677`（编排仓 handoff 本地 `d18ecd5`，origin/dev 落后未推）
- pipeline URL：https://gitlab.htmisoft.net/gkx-lumen/demo-algo-ent-analysis/-/pipelines?ref=dev ；https://gitlab.htmisoft.net/gkx-lumen/demo-ui-system-test/-/pipelines?ref=dev
- 部署：`demo-platform-entan-py` + `gkx-demo-ui` NodePort 30889
- K8s rollout：提交 push 后由 CI 触发
- 验收 URL：http://192.168.88.50:30889

## 可观测性（建议）

- 推理走既有 `request.ts` 拦截器，501/失败带 `__traceId`
- 无新 OTEL 服务名

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/yiji_sim/infer.py`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/pipeline.py`
- `repos/demo-algo-ent-analysis/entan/yiji_sim/selfcheck.py`
- `repos/demo-ui-system-test/src/views/entan/components/GraphView.vue`

## 架构合规自检

- 算法只在 Python ✅
- 前端 → 网关 → entan `/v1/graph/infer`，未越层 ✅
- 图谱 Nebula，未引入 Neo4j ✅
- D12：改动仅 demo-* ✅
- 语料仍为 `industry_analysis_*` ✅
