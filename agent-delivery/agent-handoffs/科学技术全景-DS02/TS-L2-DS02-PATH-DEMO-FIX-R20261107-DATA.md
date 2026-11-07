# TS-L2-DS02-PATH-DEMO-FIX-R20261107-DATA · DS02 关键路径 LOOP · 覆盖不到（path_priority/正文/类型）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（LOOP 2026-11-07 首轮 PATH DATA） |
| 说明 | 不开工 `SYSINT-TECHGRAPH-02-L02`/`L03`。centrality overlay QUERY 挂 `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY`。D4 mock 不改绿。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只跑已文档化的 SCORE 灌数脚本补 `path_priority`；路径正文/类型/年份无列可写则挂 L02 + 用例回写，不另造字段。 |

## 结论

**部分完成**：`path_priority` **已闭合**（重跑 SCORE `--apply`）。  
**仍 blocked**：路径 `summary` / `pathType` / `timeLabel` —— hung-on **`SYSINT-TECHGRAPH-02-L02`**（现行边 schema 亦无这些属性，属无源，需用例回写或扩契约）。

## 缺口键与处置

### 1. `ads_technology_panorama_score.{path_id}.path_priority` — 已补

| 时点 | `path_priority` 行数 | 其它 |
|------|----------------------|------|
| 灌前 SELECT（pod） | **0** | centrality 19430，influence 252363 |
| 灌后 SELECT（pod） | **12891** | 同上 + path_priority 12891；`other_kinds=0` |

用例样本路径已有分：

| path_id | score_value |
|---------|-------------|
| `tep_8392b7f8d44d14cae932645cd242f5bd` | 70.459 |
| `tep_6cddc27aa4e88a50756093fd6d76ef86` | 75.406 |

脚本与执行：

- 仓：`lumen-algo-py`  
- 命令：`python scripts/seed/seed_technology_panorama_score.py --apply`  
- 环境：本机解析 `vendor/*/conf/settings.yaml` 口令（未打印）；连 `demo_gkxlumenx_ads` + Nebula `demo_gkx_chain`  
- 结果 JSON：`rows=284684`，`by_kind.path_priority=12891`，`ok=true`（约 164s）  
- 图侧前提：`tech_path_step` 边约 35018，`DISTINCT path_id` 12891（灌前已存在；SCORE-L01 当时因无路径步故 priority 为 0）

说明：pod 镜像内**无**该脚本文件；本次在开发机跑文档路径，未向业务镜像塞临时文件。D4 仍为 mock，未宣称 live。

### 2. `nebula.demo_gkx_chain.tech_path_step.{path_id}.summary|pathType|timeLabel` — 未补

| 项 | 实测 |
|----|------|
| `DESCRIBE EDGE tech_path_step` | 仅 `path_id`、`step_order` |
| `_EDGES["tech_path_step"].props` | 同上 |
| 读图 | `summary`/`timeLabel` 硬编码 `""`；无 `pathType` 投影 |

**挂 `SYSINT-TECHGRAPH-02-L02`**：路径步写入面属 L02。但现行 L02/schema **也不含** summary/pathType/timeLabel —— L02 按现稿做完仍无源。本单不开工扩列。

## 用例回写建议（勿静默改期望）

对象：`TS-L2-DS02-PATH-合规演示用例.md`

- 行 **28 重要性**：`path_priority` 已有行 → 可在下一轮验收改为可演（Java 叠分仍走 mock 表；带 MockBadge）。本 handoff 不改用例文件。  
- 行 **30 正文**、**31 类型/年份**：建议改为 **设计无资源 / 无源**，文案：

> `tech_path_step` 仅有 `path_id`/`step_order`；读图不返回技术意义正文、路径类型、年份。在扩 EDGE 属性与读契约前，不把空 `summary`/`pathType`/`timeLabel` 当作灌数遗漏。

## 修改内容

- 执行既有灌数脚本写 ADS（D18 mock 表），无改脚本、无改前端、无改读图。  
- 本 handoff。

## 测试结果

- `--check`：ok  
- `--apply`：ok，见上  
- pod 复核 `GROUP BY score_kind` + 两案 path_id SELECT：通过  

## 遗留风险 / DoD 开项

1. path_priority —— **闭**。  
2. summary/pathType/timeLabel —— **开**，hung-on L02 + 无源回写。  
3. QUERY centrality overlay —— 不归本单。  
4. 展示侧是否已读到新分数：依赖 Java display 叠表；本单只保证 ADS 行存在。

## CI/CD（必填）

- 灌数不经本次镜像发布；编排仓仅 handoff commit。  
- 业务仓无新 commit（脚本沿用 SCORE-L01：`828315a` 起已在 `dev`）。

## 架构合规自检

1. Python 灌 D18 mock，Java 只读。✅  
2. 未写 ODS/DWD/供应方库。✅  
3. D4 仍 mock。✅  
4. 未开工 L02/L03。✅  
5. Nebula 只读扫 path_id 对齐编号。✅  

## Cost 回填（建议）

- actual_tokens: ~12000  
- model_used: claude-sonnet-4.5  
- actual_cost: 0.06  
- cost_warn: green

## 人下一步

1. 下一轮 PATH 验收：核对行 28 `pathPriority` 非 null（MockBadge 仍在）。  
2. 确认 30/31 是否改「设计无资源」。  
3. 若要坚持路径正文/类型/年份：扩 `tech_path_step`（或路径顶点）属性并改读图——另派，勿塞进本 DATA。  
4. path_priority 已齐；本单整体仍勿 done，直至正文/类型开项处理完或用例回写签收。

## 监管人拍板 2026-11-07

human:淮政玮：**另开 Tag/Edge 扩列**（路径 summary/pathType/timeLabel）。登记 Q072；挂 `TS-L2-DS02-SCHEMA-EXPAND-L01`。`path_priority` 已闭合部分不变。
