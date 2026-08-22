# DS-04-METRIC-OPEN-L01 · 展示全球创新监测 METRIC-OPEN（LOOP Round 11）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 11。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 11 + catalog `ds_id=DS-04`：

- 覆盖 6 页：`DS-04-ACHIEVE-OVERVIEW` / `ACHIEVE-DETAIL` / `MONITOR` / `REALTIME` / `CITY` / `CARRIER-RANK`。
- ④：**5 kit + 1 整页 N/A**（DETAIL）。预测 **501 pending**，差集 **missing**，不伪闭合 mapped。
- 只列 `TEMP_DS04_*`。禁止发明正式 `M_*` 写入 seed。
- 禁止改挂 `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*`；禁止混挂 DS-05/06/08。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针只写分叶 `DS-04-METRIC-OPEN-L01-a2-patch.yaml`。
- **未改**共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q0xx`、未改客户决策清单：⑤ = 核对记录 §4 + A2 `semantic_debt`。
- metric-registry MCP 本会话未挂载；未整文件读 seed。形近 ID 以 A2 `b_track_lookalikes` / `srs05_do_not_map` 为准，一律不消费。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-04-全球创新监测-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-04-METRIC-OPEN-L01.yaml` |
| A2 patch（分叶） | `metrics/request/_work/open-loop/DS-04-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-04-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-04-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-04-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 6，全部 `metric_open_status: present`。
- kit：OVERVIEW / MONITOR / REALTIME / CITY / CARRIER-RANK；N/A：ACHIEVE-DETAIL。
- `demands` 均为 `TEMP_DS04_*`，**零**正式 `M_*`。
- REALTIME `TEMP_DS04_RT_IMPACT_FORECAST` 标 501 pending，`keep_library_missing: true`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 LOOP 文件。
- 会签通过（口径草稿；公式 pending）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端 `/innov` → Java innov → ADS/ES |
| 图谱 Nebula | ✅ 未引入 Neo4j；seq 69 标可选 graph/view |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 无正式 `M_*` → 门 1 仅有条件闭合。
- TEMP_ 若被误写入 seed 即违规；Round 18 仍须 `keep_library_missing`。
- 501 若被当成 mapped 即伪闭合。
- CITY 三维 vs 186 四维（CITY-B03）待甲方，不发明三维 `M_*`。

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
| actual_tokens | 160000 |
| model_used | grok-4.6 |
| actual_cost | 1.20 |
| cost_warn | green |

## 下一步

状态留 `in_progress` 等 coordinator AV。**本会话不标 done、不改 LOOP-state。** Round 18 才回写 A2 catalog 指针。

---

## 赋号追加（METRIC-ID-ASSIGN-LOOP · 2026-08-22）

| 项 | 值 |
|----|-----|
| 执行 | product-agent；监管 `human:淮政玮` |
| 赋号份数 | **13**（= 机器卡 `TEMP_DS04_*`；DETAIL 不造 ID） |
| 复用份数 | **0**（CITY/载体 ≠ `M_SYNTH_*` / DS-06 口径，禁止改挂） |
| Q 份数 | **5**（`Q-MO-DS04-01`…`05`，叶级 yaml；未写共享 QUESTIONS） |
| 建议类型分布 | STAT 2 / MODEL 6 / MIXED 4 / third_party 1 |
| 501 | `M_INNOV_IMPACT_FORECAST` 仍 pending；MODEL **不是**覆盖证明；missing 不改 |
| 未改 | seed / 展示 catalog / `METRIC-SEMANTIC-QUESTIONS.md` / LOOP-state |
| MCP note | 赋号草稿；类型未签 |

产物：核对记录 §赋号表；机器卡 demands→`M_*`；`id-assign/DS-04-METRIC-OPEN-L01.yaml` + `-questions.yaml`。
