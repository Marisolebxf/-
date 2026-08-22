# TOPIC-ORG-METRIC-OPEN-L01 · 专题科研机构 METRIC-OPEN（LOOP Round 4）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 4。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 4：

- 覆盖一页：`TOPIC-ORG-05`（05.4 十招标叶子进算法差集者）。
- ④ **kit**（非整页 N/A）；历程 CMS / 筛选壳 / 门户 / 运营 / 图谱无独立核 / 服务机构 **N/A + 依据**。
- 只列 `TEMP_TOPIC_ORG_*`。禁止发明正式 `M_ORG_*` 写入 seed。
- **禁止**消费产业服务链 OPEN 与 `M_SVC_ORG_*` / `M_SVC_REC_*`；禁止 `M_CHAIN_INSTITUTION_*` 形近 ID 顶替。
- 公式 **第三方不展开**；技术力 = 【算法补】差集 `third_party`，不是 missing。
- 合作链 = A 面 G1；引入 / 扶持 / 优势 / 痛点 = G3 Job。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 17）；指针写入本叶 `TOPIC-ORG-METRIC-OPEN-L01-a2-patch.yaml`。**未改**共享 `LOOP-state.yaml` / `METRIC-OPEN-LOOP-a2-patch.yaml`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。未开工其它 OPEN 叶。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q-TOPIC-ORG-*`、未改客户决策清单。
- 功能实现 Owner 按给人说明 **待指定**，未猜填郭万迎为功能 Owner（九新对接仍可回指 `JIUXIN-TECH-ORG-TALENT-L01`）。
- 05 seq 99(4) 正文混入「服务机构」字样：仍判科研机构新增核，**未**因此挂 `M_SVC_ORG_NEW_COUNT`。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-ORG-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-ORG-METRIC-OPEN-L01.yaml` |
| A2 patch（本叶） | `metrics/request/_work/open-loop/TOPIC-ORG-METRIC-OPEN-L01-a2-patch.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-ORG-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-ORG-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ORG-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 1，`page_id=TOPIC-ORG-05`，`metric_open_status: present`，`kit_or_na: kit`。
- `demands` 11 条均为 `M_ORG_*` + `temp_id` 对照，**零** `M_SVC_ORG_*` 改挂，**reuse=0**。
- 赋号卡条数 = 11 = 原 TEMP 数；建议类型全非 UNKNOWN；叶级 Q 9 条。
- 本叶 patch `entries` 含 `TOPIC-ORG-05` + `keep_library_missing: true`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 LOOP / QUESTIONS；未改展示 catalog。
- 会签通过（口径草稿；公式 pending；类型 suggested_unsigned）。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java `/topic/v1/institution/**`→ADS / Job / A 面图 |
| 图谱 Nebula | ✅ 未引入 Neo4j；合作链标 A 面当前图 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 无正式 `M_*` + third_party 不展开 → 门 1 仅有条件闭合。
- TEMP_ 若被误写入 seed 或 A2 `metric_id` 即违规；Round 17 仍禁止 `M_SVC_ORG_*` / `M_ORG_*`。
- 技术力【算法补】若被改判 missing 或挂服务机构 TECH_SCORE 即违规。
- 功能实现 Owner 待指定，前端/Java 派单前须真人点名。

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
| actual_tokens | 115000 |
| model_used | grok-4.6 |
| actual_cost | 0.95 |
| cost_warn | green |

## 下一步

本叶四份产物已落盘。**禁止**本会话改 `LOOP-state.yaml` / 共享 `METRIC-OPEN-LOOP-a2-patch.yaml`（coordinator 合流）。状态留 `in_progress` 等 coordinator AV。**不标 done。**

---

## 赋号草稿（METRIC-ID-ASSIGN loop · 2026-08-22）

- **赋号 11** = 机器卡 `TEMP_TOPIC_ORG_*` 全数；**reuse 0**（seed 无 ORG 域；11 个新号均 missing）；**废弃 0**。
- **Q 9**：`Q-MO-ORG-01`…`09`，仅叶级 `id-assign/TOPIC-ORG-METRIC-OPEN-L01-questions.yaml`；未写共享 QUESTIONS / 客户决策清单 / LOOP-state / seed / 展示 catalog。
- **建议类型（未签）**：STAT 3 · COMPUTE 1 · MIXED 1 · GRAPH 1 · MODEL 5。关注度由 OPEN 草稿 STAT 改为建议 COMPUTE（新增数+增速合成）。
- **ELEMENT=`ORG`**。禁止改挂 `M_SVC_ORG_*` / `M_SVC_REC_*` / `M_CHAIN_*` / `M_ENT_*` 形近 ID（赋号卡 `lookalike_note` 可 mapped 说明）。
- 机器卡 `demands` 已换成 `metric_id` + `temp_id` 对照。核对记录 **§8 赋号表**。
- MCP note：「赋号草稿；类型未签」。**不标 done。**
