# DS-02-METRIC-OPEN-L01 · 展示科学技术全景 METRIC-OPEN（LOOP Round 9）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 9。名词见 `task-claiming-guide.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；USM/TRACE/A2 pages 按原文精读，不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义精读；本叶不压缩会签原文 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶无拓扑、无调用链改边 |
| 会签态 | N/A |
| 说明 | OPEN 语义卡 + 开放项登记，无 Mermaid 契约图 |

---

## 范围与实现

对照给人说明 **§8.4 甲** + LOOP 协议 Round 9 + SRS 02 科学技术全景：

- 覆盖 catalog `ds_id=DS-02` 五页：`TECHGRAPH` / `ENTITY` / `PATH` / `MAINTAIN-GRAPH` / `MAINTAIN-ENTITY`。
- ④：TECHGRAPH / ENTITY / PATH / MAINTAIN-ENTITY **kit**；MAINTAIN-GRAPH **整页 na_with_reason**（维护面偏 n/a_ops，本五级无算法生成句）。
- 只列 `TEMP_DS02_*` 对照；赋号草稿见 §赋号表。禁止发明正式 `M_*` **写入 seed**。
- **禁止**把本页指标改挂 `TOPIC-TECH` OPEN；同源可 mapped 同一 05 叶（104/105/130/96），不同页。论文/专利同口径预共享 `M_TECH_PAPER_PATENT_CNT`，本页非唯一宿主。
- PATH 501 未注册 ≠ 整页 N/A；中心度三行库 **missing 保持**。ENTITY 影响力 **missing 保持**。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针写入本叶私有 `DS-02-METRIC-OPEN-L01-a2-patch.yaml`（**不**改共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`）。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。未改 TOPIC-TECH 文件。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- ⑤ **N/A**：无 `DS-02-data-gap-catalog.yaml`、无本模块 `Q0xx`；不新建、不改客户决策清单。语义债留 A2 `TG-B*` / `ENT-B*` / `PATH-B*`。
- 并行约束：未写共享 LOOP 文件（由 coordinator 合流）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-02-科学技术全景-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-02-METRIC-OPEN-L01.yaml` |
| A2 patch（本叶） | `metrics/request/_work/open-loop/DS-02-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-02-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/DS-02-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-02-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 5，均 `metric_open_status: present`。
- `kit_or_na`：TECHGRAPH/ENTITY/PATH/MAINTAIN-ENTITY = `kit`；MAINTAIN-GRAPH = `na_with_reason`。
- `demands` 为 `M_TECH_*` + `temp_id` 对照；MAINTAIN-GRAPH `demands: []`。
- 赋号卡 items = 10 TEMP；唯一 ID 9；Q 5；类型 GRAPH 8 / STAT 1 / MODEL 1（均 unsigned）。
- 本叶 patch `entries` 仍含五 `page_id` + `keep_library_missing: true`（本轮未改 patch）。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改 TOPIC-TECH；未改共享 LOOP / QUESTIONS。
- 会签通过（口径草稿；**赋号草稿；类型未签**；公式 pending）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java BFF→ADS / Nebula A 面 |
| 图谱 Nebula | ✅ 未引入 Neo4j；读面 A 技术点网 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 赋号未入 seed → 门 1 仅有条件闭合。
- `M_TECH_*` 草稿若被写入 seed 或把 TOPIC-TECH OPEN 改挂为本页唯一即违规。
- PATH 三行 + ENTITY 影响力若被赋号改成 mapped = 伪闭合。

## CI/CD（必填）

- 分支：不提交（用户禁止 commit）
- commit：无
- pipeline URL / ID：`cicd: skip`
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL：N/A（定义叶）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## Cost（估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 145000 |
| model_used | grok-4.6 |
| actual_cost | 1.20 |
| cost_warn | green |

## 下一步

状态留 `integration`。**不**改 OPEN 叶为 done。赋号草稿；类型未签。Round 18 才回写展示 catalog 指针。不写 seed / 共享 QUESTIONS / LOOP-state。

---

## 赋号（2026-08-22 METRIC-ID-ASSIGN loop）

| 项 | 值 |
|----|-----|
| TEMP 赋号 | **10/10** |
| 唯一 `M_*` | **9**（MENT 复用 TOP5） |
| 复用 | **2**（`M_TECH_PAPER_PATENT_CNT` 预共享 TOPIC-TECH 同口径；`M_TECH_ENTITY_TOP5` 页内同源不同面） |
| Q | **5**（`Q-MO-DS02-01`…`05`，全 🟡；仅叶级 yaml） |
| MAINTAIN-GRAPH | **0 ID**（整页 n/a_ops） |
| 库 missing | **4 行保持**（INFLUENCE + PATH 三行）；赋号 ≠ mapped |
| 建议类型（未签） | GRAPH **8** / STAT **1** / MODEL **1** |
| ELEMENT | `TECH` |
| 路径中心性 | 偏 GRAPH（`M_TECH_PATH_CENTRALITY`）；不改挂 SVC/SYNTH/ENT 中心性 |

产物：核对记录 §赋号表；机器卡 demands 已换 `M_*`（保留 temp_id）；`id-assign/DS-02-METRIC-OPEN-L01.yaml` + `-questions.yaml`。
