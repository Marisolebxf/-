# DS-07-METRIC-OPEN-L01 · 展示科技创新评估 METRIC-OPEN（LOOP Round 14 / 波 B）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 14。名词见 `task-claiming-guide.md`。DoD「淮政瑎」是错字，owner_semantic=`human:淮政玮` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 14 + catalog `ds_id=DS-07`：

- 覆盖 4 页：`DS-07-POLICY-GUARD` / `INDUSTRY-POTENTIAL` / `TECH-INNOV` / `SCI-CREATE`。
- ④：**4/4 kit**。页内 N/A：POLICY 优化建议（seq 158）；TECH 空间分布（seq 144）。
- OPEN 卡面曾用 `TEMP_DS07_*`；赋号后升 `M_INNOV_*` 草稿。禁止写入 seed。
- **POLICY-GUARD 不是 E7 政策专题**：未消费 `POLICY-METRIC-OPEN-L01` / `METRIC-OPEN-E7-DS10-12` / DS-10～12；未另开 TOPIC-POLICY。
- 禁止改挂 `M_POLICY_*` / `M_CHAIN_*` / `M_SVC_*` / `M_SYNTH_*` / `M_ENT_*`；禁止混写 DS-03 / DS-08 / 专题 TECH/ORG / SYNTH。
- 已 mapped 不得改挂为本页正式 ID。库 missing **9 行保持**。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 18）；指针只写分叶 `DS-07-METRIC-OPEN-L01-a2-patch.yaml`。
- **未改**共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q0xx`、未改客户决策清单：⑤ = 核对记录 §4 + A2 `semantic_debt`。
- metric-registry MCP 本会话未挂载；未整文件读 seed。形近 ID 以 A2 `b_track_lookalikes` / `srs05_do_not_map` 为准，一律不消费。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/METRIC-OPEN-DS-07-科技创新评估-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/DS-07-METRIC-OPEN-L01.yaml` |
| A2 patch（分叶） | `metrics/request/_work/open-loop/DS-07-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/DS-07-METRIC-OPEN-L01.yaml` |
| 叶级 Q | `metrics/request/_work/id-assign/DS-07-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/DS-07-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 4，全部 `metric_open_status: present`、`kit_or_na: kit`。
- OPEN 阶段 `demands` 曾为 `TEMP_DS07_*`；**赋号后**已换成 `M_INNOV_*`（保留 `temp_id` 对照）。未写入 seed。
- TECH-INNOV `M_INNOV_TINN_FORECAST` 标 501 pending，`keep_library_missing: true`。SCI 预测 **无** 501。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 LOOP 文件 / QUESTIONS.md。
- 未消费政策 OPEN；未改挂 `M_POLICY_*`。
- 会签通过（口径草稿；公式 pending；类型未签）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端 `/display` → Java → ADS；中心性可选 graph/view |
| 图谱 Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 无正式 `M_*` → 门 1 仅有条件闭合。
- TEMP_ 若被误写入 seed 即违规；Round 18 仍须 `keep_library_missing`。
- 501 若被当成 mapped 即伪闭合（仅 TECH seq 145 通道）。
- POLICY-GUARD 若被挂到 E7/DS-10～12 OPEN 即范围串页。

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
| actual_tokens | 150000 |
| model_used | grok-4.6 |
| actual_cost | 1.10 |
| cost_warn | green |

## 赋号（METRIC-ID-ASSIGN · 草稿 · 类型未签）

- **赋号 22**（TEMP 22 条，0 废弃）· **reuse 0** · **新编 22**（全部 `M_INNOV_*`）
- **Q 6**：Q-MO-DS07-01…06（叶级 yaml；未写共享 QUESTIONS.md / 跟踪表）
- **建议类型**：STAT 7 / MIXED 3 / MODEL 12；全部 `suggested_unsigned`
- ELEMENT=`INNOV`；POLICY-GUARD 不进 POLICY 域、不改挂 `M_POLICY_*` / TOPIC-POLICY
- 预测：TINN `M_INNOV_TINN_FORECAST` 501 pending + MODEL，**不是覆盖证明**；SCI 预测无 501；9 行 missing 保持
- 未改 seed、未改展示 catalog/pages、未改 LOOP-state / 共享 QUESTIONS；未派唐绍祖

## 下一步

状态留 `integration`。**赋号草稿；类型未签。不标 done。** 共享 QUESTIONS / LOOP-state 由 coordinator 合流。
