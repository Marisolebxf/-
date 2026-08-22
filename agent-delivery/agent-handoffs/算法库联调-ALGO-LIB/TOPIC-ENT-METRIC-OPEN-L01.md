# TOPIC-ENT-METRIC-OPEN-L01 · 专题企业 METRIC-OPEN（LOOP Round 2）

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、本叶不标 done。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行 Round 2。名词见 `task-claiming-guide.md` |

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

对照给人说明 **§8.4 甲** + LOOP 协议 Round 2：

- 覆盖一页：`TOPIC-ENT-05`（05.3 十招标叶子进算法差集者）。
- ④ **kit**（非整页 N/A）；历程 CMS / 筛选壳 / 运营 / 展示门户 / 图谱无独立核 **N/A + 依据**。
- 只列 `TEMP_TOPIC_ENT_*`。禁止发明正式 `M_*` 写入 seed。
- 禁止挂展示 `ENT-MOD-*-METRIC-OPEN`；禁止消费 `cfg_metric-ENT-seed` 60 个 `M_ENT_*`。
- 供应链 = A 面 G1/G2；招引 / 培育 / 痛难点 = G3 Job。
- `owner_semantic=human:淮政玮`；公式/`algorithm_type` `pending_cosign: human:唐绍祖`。
- A2 catalog **正文不改**（Round 17）；指针追加 `METRIC-OPEN-LOOP-a2-patch.yaml` 一条 `TOPIC-ENT-05`。
- 不挡 `ALGO-LIB-METRIC-DEPS-L01`。未开工 Round 3。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。本工作流口径挂淮政玮（给人说明文首）。
- 无 TRACE `owner_semantic` 可改；会签栏以本核对记录为准。
- 未新建 `Q-TOPIC-ENT-*`、未改客户决策清单：展示 Q010～Q019 不改挂；专题债留 ENT-B03…B12。
- 未改 Round 1 SVCCHAIN 产物。

## 产物清单

| 产物 | 路径 |
|------|------|
| 核对记录 | `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/METRIC-OPEN-TOPIC-ENT-核对记录.md` |
| 机器卡 | `metrics/request/_work/open-loop/TOPIC-ENT-METRIC-OPEN-L01.yaml` |
| A2 patch | `metrics/request/_work/METRIC-OPEN-LOOP-a2-patch.yaml`（追加 `TOPIC-ENT-05` present） |
| 赋号卡 | `metrics/request/_work/id-assign/TOPIC-ENT-METRIC-OPEN-L01.yaml` |
| 赋号 Question | `metrics/request/_work/id-assign/TOPIC-ENT-METRIC-OPEN-L01-questions.yaml` |
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/TOPIC-ENT-METRIC-OPEN-L01.md` |

## 验收证据

- 机器卡 `pages[]` 长度 = 1，`page_id=TOPIC-ENT-05`，`metric_open_status: present`，`kit_or_na: kit`。
- OPEN 阶段 `demands` 曾为 `TEMP_TOPIC_ENT_*`。Wave A 已换成 `M_*`（可留 `temp_id` 对照）；12/12 赋号。
- patch `entries` 含 `TOPIC-ENT-05` + `keep_library_missing: true`。
- 未改 `metrics/registry/`；未改 A2 catalog 正文；未改共享 QUESTIONS / LOOP-state。
- 会签通过（口径草稿；公式 pending）。赋号草稿；类型未签。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 未写 Java/Python 业务代码 |
| 调用链 | ✅ N/A（定义叶）；文内维持 前端→Java→ADS / Job / A 面图 |
| 图谱 Nebula | ✅ 未引入 Neo4j；供应链标 A 面当前图 |
| 可观测 | ✅ N/A |
| CI/CD | ✅ `cicd: skip` |
| D12 demo/lumen | ✅ 未改业务仓 |
| D8/D9/D10 | ✅ 核对记录含 ⓘ / 角标 / 开放项；不跳过 |

## 遗留风险

- 公式未签 + 类型未签 → 门 1 仍仅有条件闭合。
- 新 `M_*` / reuse ID 若被误写入 seed 即违规。
- 展示 Q010～Q019 与 `Q-MO-ENT-01`…`10` 并存，禁止混挂、禁止升 🟢。

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
| actual_tokens | 108000 |
| model_used | grok-4.6 |
| actual_cost | 0.90 |
| cost_warn | green |

## 下一步

LOOP-state Round 2 → `done`；`current` → `TOPIC-TECH-METRIC-OPEN-L01`。**本会话不开工 Round 3。** 状态留 `in_progress` 等 coordinator AV。

---

## 赋号（METRIC-ID-ASSIGN Wave A · 2026-08-22）

- 12/12 `TEMP_*` 已赋号，0 废弃。reuse **5**，新号 **7**（`VARIANT=TOPIC`），Q **10**（`Q-MO-ENT-01`…`10`，全 🟡）。
- 建议类型：STAT 4 / MODEL 6 / MIXED 1 / GRAPH 1。全部 `suggested_unsigned`，未派唐绍祖。
- reuse（also_in 本页，非整页改挂 60 个）：`M_ENT_TECH_POWER_SCORE`、`M_ENT_BUSINESS_POWER_SCORE`、`M_ENT_ATTRACTION_INDEX`、`M_ENT_CULTIVATION_INDEX`、`M_ENT_COMPETITIVENESS_SCORE`。
- 新号：`M_ENT_TYPE_DIST_TOPIC`、`M_ENT_REGIONAL_COUNT_TOPIC`、`M_ENT_DOMAIN_DIST_TOPIC`、`M_ENT_SZ_LIST_TOPIC`、`M_ENT_CITY_COMPARE_TOPIC`、`M_ENT_SUPPLY_STRUCT_TOPIC`、`M_ENT_PAINPOINT_TOPIC`。
- 产物：核对记录 §9；机器卡 demands 已换 `M_*`；`metrics/request/_work/id-assign/TOPIC-ENT-METRIC-OPEN-L01.yaml` + `-questions.yaml`。
- **未改** seed / 展示 catalog / LOOP-state / `METRIC-SEMANTIC-QUESTIONS.md` / A2 missing。
- 状态仍 `in_progress`。note：赋号草稿；类型未签。
