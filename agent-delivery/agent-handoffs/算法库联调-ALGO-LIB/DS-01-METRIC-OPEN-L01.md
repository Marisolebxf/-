# DS-01-METRIC-OPEN-L01 · 展示科技全域态势 METRIC-OPEN（LOOP Round 8）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领且 `in_progress`；本会话 product-agent 代执行 Round 8。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 8：

- 覆盖 catalog `ds_id=DS-01` 四页：`DS-01-FACTORS` / `DS-01-LAYERS` / `DS-01-MAP` / `DS-01-EVENTS`。
- ④：**FACTORS kit** · **LAYERS N/A+依据** · **MAP N/A+依据** · **EVENTS kit**。
- 只列 `TEMP_DS01_*`；服务机构影响力 **impl** 指向已有 `M_SVC_ORG_TECH_SCORE`。禁止发明正式 `M_*` 写入 seed。
- 专题 7 条 missing **不重列**。禁止 `M_ENT_*` / `M_SYNTH_ELEM_*` / `M_CHAIN_ACADEMIC_POWER` / `M_CHAIN_PATENT_COUNT` 顶替。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- SRS 02 **顶 PACK**；**FDS 不顶**。
- A2 catalog **正文不改**（Round 18）；指针写入本叶 `DS-01-METRIC-OPEN-L01-a2-patch.yaml`。**未改** `LOOP-state.yaml` 与共享 `METRIC-OPEN-LOOP-a2-patch.yaml`。
- 不改其它 DS OPEN。不挡 `ALGO-LIB-METRIC-DEPS-L01`。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以核对记录为准。
- 未新建 `Q0xx`、未改客户决策清单：沿用 SD-FACT-01…05、EVT-B01…03。
- 共享 LOOP 状态 / 合流 patch 由 coordinator 写，本叶不碰。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-01-科技全域态势-核对记录.md`（含 §赋号表） |
| 机器卡 | `metrics/request/_work/open-loop/DS-01-METRIC-OPEN-L01.yaml` |
| A2 patch（本叶） | `metrics/request/_work/open-loop/DS-01-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-01-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/DS-01-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-01-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 4，覆盖 FACTORS / LAYERS / MAP / EVENTS，`metric_open_status: present`。
- FACTORS / EVENTS `kit_or_na: kit`；LAYERS / MAP `na_with_reason`。
- **赋号**：`demands` 已换 `M_*`（保留 `temp_id`）；20/20 TEMP 已赋；reuse 1；类型全部 `suggested_unsigned`。
- 本叶 patch `entries` 含四页 + `keep_library_missing: true`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改 LOOP-state / 共享 a2-patch / QUESTIONS.md。
- 会签通过（口径草稿；公式 pending）。**赋号草稿；类型未签。不标 done。**

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java `/display/v1/**`→ADS；GIS 配置+坐标 |
| 图谱 Nebula | ✅ 未引入 Neo4j；关联核对照 seq 116，不改挂 B 轨图指标 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；图层地图无数字则无 ⓘ 义务；不跳过 |

## 遗留风险

- 公式未签 + 类型未签 → 门 1 仅有条件闭合。赋号草稿未入 seed。
- TEMP_ / 草稿 `M_*` 若被误写入 seed 即违规；Round 18 仍须保持库 missing。
- SD-FACT-05 / 事件三核口径 / 服务机构 reuse 技术力差：Q-MO-DS01-03/04/06–08，待甲方。

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

## 赋号（METRIC-ID-ASSIGN · 草稿 · 类型未签）

- **赋号 20**（TEMP 20 条，0 废弃）· **reuse 1**（`M_SVC_ORG_TECH_SCORE`，B 轨已有、seed MCP miss）· **新编 19**（`M_INNOV_*`）
- **Q 8**：Q-MO-DS01-01…08（叶级 yaml；未写共享 QUESTIONS.md / 跟踪表）
- **建议类型**：STAT 4 / GRAPH 2 / MODEL 14；全部 `suggested_unsigned`
- ELEMENT=`INNOV`；未用 `IC`；LAYERS/MAP 不赋号
- 未改 seed、未改展示 catalog/pages、未改 LOOP-state / 共享 QUESTIONS

## 下一步

状态留 `in_progress`。**赋号草稿；类型未签。不标 done。** 共享 QUESTIONS / LOOP-state 由 coordinator 合流。本会话不开工其它 DS OPEN。
