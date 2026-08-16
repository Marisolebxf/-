# ENT-YIJI-INDANA-DETAIL-L01 · 行业分析要素库文档详情（新窗口六表）

> 内容按本次实测与代码实写。监管口头：企业图谱下拉【详情】新窗口打开，展示 `industry_analysis_*` 六表字段结构 + 该 `document_id` 行。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 同会话增量；Demo 前端直连 entan `/v1/graph*`，未新开 Java |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `corpus.py` 六表清单；详情 = SHOW FULL COLUMNS + SELECT *；未新依赖；侧栏不挂菜单项 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 问题清单

- 现网需等 `demo-algo-ent-analysis` + `demo-ui-system-test` 新一轮 CI 绿后才能点【详情】。
- 未写「联调通过」。

## 修改内容

- `entan/yiji_sim/corpus.py`：`load_document_bundle` 读六表结构+行；缺表 honesty。
- `GET /v1/graph/industry-analysis/documents/{document_id}`。
- GraphView：下拉每项【详情】+ 工具栏【详情】→ `window.open` `/entan/indana/:documentId`。
- 新页 `IndanaDocumentDetail.vue`：每表先结构后数据。

## 测试结果

- `python scripts/run_indana_dwd.py --self-check` → OK 六表名
- `import api.main` → IMPORT-OK
- 本机 `load_document_bundle(DOC-HW-PKG)` → honesty=None；documents 1/24 列，companies 1/13，industries 2/12，topics/content_types/countries 各 1/12；title=先进封装量产
- GraphView / K8s 现网详情：**未联调**

## 遗留风险

- 浏览器拦截弹窗时需允许本站弹窗。
- 正文 `body` 可能很长，表格用 overflow tooltip。

## CI/CD（必填）

- 分支：`dev`（push 后填 SHA）
- pipeline：push 后看 GitLab `dev`
- 部署：`demo-platform-entan-py` + `gkx-demo-ui`
- K8s / 现网：待滚完

## 可观测性（建议）

- 新 GET 走既有 FastAPI TraceHeaderMiddleware
- 详情页未单加埋点（与 GraphView 同栈）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 读库在 corpus |
| 调用链 前端→Java→Python | ✅ Demo 既有直连 entan `/v1/graph*`，本叶不新开 Java |
| Nebula | ✅ 未改 |
| D12 demo/lumen | ✅ 只改 demo-* |
| 表名 | ✅ 仅 `industry_analysis_*`，禁止素表 `documents` |

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/yiji_sim/corpus.py`
- `repos/demo-algo-ent-analysis/api/main.py`
- `repos/demo-algo-ent-analysis/scripts/run_indana_dwd.py`
- `repos/demo-ui-system-test/src/api/entan/index.ts`
- `repos/demo-ui-system-test/src/router/index.ts`
- `repos/demo-ui-system-test/src/views/entan/components/GraphView.vue`
- `repos/demo-ui-system-test/src/views/entan/components/IndanaDocumentDetail.vue`
