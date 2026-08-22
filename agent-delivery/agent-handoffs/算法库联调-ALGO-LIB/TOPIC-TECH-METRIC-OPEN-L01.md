# TOPIC-TECH-METRIC-OPEN-L01 · 专题技术链 METRIC-OPEN（LOOP Round 3）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 3。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 3：

- 覆盖一页：`TOPIC-TECH-05`（05.1 六招标叶子进算法差集者）。
- ④ **kit**（非整页 N/A）；可视化 / NER / ODS / 过滤壳 / 流程图 / 历程 CMS / 展示 DS-02 **N/A + 依据**。
- `TEMP_*` 已升正式草稿 6 个 `M_TECH_*`（§赋号表）；**禁止**写入 seed。
- 与 DS-02 论文/专利同口径共享 `M_TECH_PAPER_PATENT_CNT`；**禁止**把 DS-02 OPEN 改挂为本页唯一消费。
- 实现类 G3 = third_party，**不伪展开公式**。全景/深圳子图 = A 面 G1。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`（suggested_unsigned）。
- 与 `JIUXIN-TECH-ORG-TALENT-L01` 分责：本叶语义/适用性/赋号草稿；九新叶交付形态。
- A2 catalog **正文不改**；指针只写本叶 `TOPIC-TECH-METRIC-OPEN-L01-a2-patch.yaml`。
- **未改**共享 `METRIC-OPEN-LOOP-a2-patch.yaml`、`LOOP-state.yaml`、`METRIC-SEMANTIC-QUESTIONS.md`、展示 catalog、其它 OPEN。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q-TOPIC-TECH-*`、未改客户决策清单：Q068 不做且不升；展示 DS-02 不改挂；专题债留 TECH-B02…B06。
- 技术链功能实现 Owner 待指定；页面清单主责郭万迎（对九新），本叶不代替谈接口。
- 未改 Round 1/2 SVCCHAIN / TOPIC-ENT 产物。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-TECH-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-TECH-METRIC-OPEN-L01.yaml` |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-TECH-METRIC-OPEN-L01.yaml` |
| 叶级 Question | `metrics/request/_work/id-assign/TOPIC-TECH-METRIC-OPEN-L01-questions.yaml` |
| A2 patch（仅本叶） | `metrics/request/_work/open-loop/TOPIC-TECH-METRIC-OPEN-L01-a2-patch.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-TECH-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 1，`page_id=TOPIC-TECH-05`，`metric_open_status: present`，`kit_or_na: kit`。
- `demands` 均为 `M_TECH_*` + `temp_id` 对照，**零**写入 `metrics/registry/` seed。
- 赋号卡条数 = 6 = 原 TEMP 数；每条有 `algorithm_type_suggested`。
- 未改 A2 catalog 正文 / 展示 catalog / 共享 LOOP patch / LOOP-state / QUESTIONS.md。
- 会签：口径草稿 + 赋号草稿；公式/类型 pending。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java→ADS / Job / A 面图 |
| 图谱 Nebula | ✅ 未引入 Neo4j；全景标 A 面当前图 `entity_type=technology` |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 无正式 `M_*` + LLM 501 → 门 1 仅有条件闭合。
- TEMP_ 若被误写入 seed 即违规；赋号草稿不得当已会签 ID。
- 实现类散文若被下游抄成公式即违规（TECH-B06）。
- `Q-MO-TECH-01/02` 未升 🟢；唐绍祖可改类型。

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
| actual_tokens | 92000 |
| model_used | grok-4.6 |
| actual_cost | 0.76 |
| cost_warn | green |

## 赋号草稿（METRIC-ID-ASSIGN-LOOP · 本叶）

- 赋号 **6** / seed reuse **0** / 同口径共享 **1**（`M_TECH_PAPER_PATENT_CNT` ↔ DS-02 `TEMP_DS02_ENT_PAPER_PATENT`；不改挂 DS-02 OPEN）/ Q **2**（`Q-MO-TECH-01` 深圳综合独立号；`Q-MO-TECH-02` 五 Job 类型 third_party vs MODEL）
- 类型分布（`suggested_unsigned`）：**STAT 1**、**third_party 5**
- 新号：`M_TECH_HEAT_INDEX` / `M_TECH_POTENTIAL_SCORE` / `M_TECH_STAGE_JUDGE` / `M_TECH_SZ_ASSESS` / `M_TECH_CONVERT_BOTTLENECK`
- 碰撞：`domain=TECH` 与 `M_TECH_*` seed 均为 0；未改挂 `M_CHAIN_*`
- **未写** seed / 展示 catalog / `METRIC-SEMANTIC-QUESTIONS.md` / LOOP-state；**不派**唐绍祖
- MCP note：赋号草稿；类型未签。本叶 **不**标 done

| 字段 | 值 |
|------|-----|
| actual_tokens | 48000 |
| model_used | grok-4.6 |
| actual_cost | 0.40 |
| cost_warn | green |

## 下一步

状态留 `in_progress`。赋号草稿待 coordinator 合流；类型/公式仍 pending 唐绍祖。**不改 LOOP-state、不标 done。**
