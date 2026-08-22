# METRIC-OPEN-DEBT-L01 · METRIC-OPEN 欠账收口

> 格式参考 `templates/handoff-template.md`。定义·文档类；**不写业务代码、不改 seed、不 `task-create`、不改本叶状态。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人已认领；本会话 product-agent 代执行定义交付。名词与流程见 `task-claiming-guide.md` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类；USM/TRACE/Wireframe/给人说明/血缘按原文精读，不以缩代码为目标 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 定义精读；本叶不压缩会签原文 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶无拓扑、无调用链改边 |
| 会签态 | N/A |
| 说明 | 定义欠账盘点 + 乙文档指针，无 Mermaid 契约图 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | 给人说明 §8.0 / §8.3 #3–5 / **§8.4 全文**；规程 §3.2 METRIC-OPEN；D9 v1.5 |
| 时序图版式 | N/A |

---

## 范围与实现

对照给人说明 **§8.4 甲/乙/丙/丁** 收口 METRIC-OPEN 欠账：

- **甲**：6 专题缺叶 + ZHIKU 补登记 → **只出建单清单**，本叶不 `task-create`。
- **乙**：POLICY / KEYPANO / SHENZHEN / COMPARE → **已改原叶文档**（见产物清单）。
- **丙**：原叶补条目清单（盘点表）；CHAIN **禁止** missing；SYNTH 保持 `ready_to_sign`。
- **丁**：A2 missing（专题 7 + 展示 70）**不是**缺 OPEN 叶，不进甲表。
- 态势 `DS-01`…`DS-09-METRIC-OPEN-L01` 保持 **backlog**；书面 SRS/详细设计顶 PACK **本叶不解锁**。
- 口径/8 件套/适用性：本工作流 `owner_semantic = human:淮政玮`；公式/`algorithm_type` 仍 `human:唐绍祖`。不替甲方 🟡→🟢。
- **不挡** `ALGO-LIB-METRIC-DEPS-L01`；不复活废作四叶；不签收 A2。

盘点全文：[`METRIC-OPEN-DEBT-L01-盘点.md`](./METRIC-OPEN-DEBT-L01-盘点.md)。

现网 MCP（2026-08-22）：`module=METRIC-OPEN` **26** 条；真正 `*-METRIC-OPEN-L01` = 原 15 + 态势 9 + 本 DEBT。甲表 7 个 ID **均未**在 registry。`metric-registry` MCP 本会话未挂载，未查 seed；本叶本来也不改 seed。

## 偏离说明

- 规程 §1.4.2 仍写王惠为日常口径主责。给人说明文首：**本工作流**口径改挂淮政玮。OPEN 纪要按梳理填写，**未改规程正文**。
- 甲表 `TOPIC-ENT/TECH/ORG/TALENT` 现网无独立专题 Epic，建议挂 `E-ALGO-LIB-DEMO`（邻近九新叶）；**禁止**把专题企业 OPEN 挂到 `ENT-MOD-*-METRIC-OPEN-L01`。coordinator 若另立专题 Epic 可改挂。
- A2 `E7-POLICY.yaml` 仍写 `metric_open_status: missing` /「严禁使用展示政策 OPEN」。本叶在核对记录写死应收口指针，**不改 A2 yaml、不签收 A2**（留给 `TOPIC-ALGO-GAP-L01` 回写）。
- COMPARE 派单包要求的 `ENT-COMPARE-data-gap-catalog.yaml` 仍缺；本叶只补核对记录（#5 指向 TRACE GAP-IMPL）。
- 未改 `task-registry.yaml`；未 `task-update-status` 本叶。

## 产物清单

| 产物 | 路径 |
|------|------|
| 本 handoff | `agent-handoffs/算法库联调-ALGO-LIB/METRIC-OPEN-DEBT-L01.md` |
| 盘点表 | `agent-handoffs/算法库联调-ALGO-LIB/METRIC-OPEN-DEBT-L01-盘点.md` |
| 乙 POLICY | `agent-handoffs/产品整体定义/METRIC-OPEN-E7-DS10-12-核对记录.md`（§1.2 TRACE/A2 指针） |
| 乙 KEYPANO | `agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/METRIC-OPEN-ENT-KEYPANO-核对记录.md`（封面 + §8 E-33） |
| 乙 SHENZHEN | `agent-handoffs/产品整体定义/E-25-深圳企业现状分析/METRIC-OPEN-ENT-SHENZHEN-核对记录.md`（§8 E-35 列） |
| 乙 COMPARE | `agent-handoffs/产品整体定义/ENT-COMPARE/METRIC-OPEN-ENT-COMPARE-核对记录.md`（**新建**） |

## 验收证据

- 盘点每行仅一种处置；甲 7 / 乙 4 / 丙 12（含与乙重叠的 POLICY）/ 丁 2 已分表。
- 乙四份文档已落盘；COMPARE 任务仍为 MCP `done`。
- 甲表 7 条字段齐，可立刻 `task-create` 成 **backlog**（见下）。
- 态势 9 叶未标 ready；未碰 `ALGO-LIB-METRIC-DEPS-L01`、废作四叶、seed。

## 架构合规自检（定义叶）

| 铁律 | 结论 |
|------|------|
| 算法只在 Python | ✅ 不写算法实现 |
| 调用链前端→Java→Python | ✅ 不越层、不改 Java/前端 |
| 图谱 Nebula / 禁 Neo4j | ✅ 不改图存储 |
| D9 8 件套 vs D1–D4 | ✅ 只动语义文档；`algorithm_type` 在套内；D1–D4 不进 8 件套；**不改** `metrics/registry/` seed/矩阵 |
| CI/CD | ✅ `cicd: skip`（设计/定义） |
| D12 demo/lumen | ✅ 不改业务仓 |
| 不替甲方拍板 | ✅ QPOL/Q0xx 保持 🟡 |
| FDS 不顶 PACK/OPEN | ✅ 甲表不 `depends_on` FDS；态势不解锁 |

## 问题清单

- A2 E7-POLICY / ENT-E33 / ENT-COMPARE catalog 指针尚未回写（属 A2 叶，本叶只给指针）。
- 专题 TECH/ORG/TALENT 功能 Owner 仍待指定；甲表 OPEN 执行 agent 仍为 `algorithm-agent` + `data-agent`。
- SYNTH 公式 pending：唐绍祖共签后才能从 `ready_to_sign` 往下。

## 修改内容

- 盘点 + 甲表建单清单。
- 乙：POLICY §1.2；KEYPANO E-33 罩住声明；SHENZHEN E-35 列；COMPARE 核对记录新建。
- 丙：补条目表（不重写 done 叶正文）。

## 测试结果

- N/A（定义文档）。MCP `task-get` / `task-query` 复核 OPEN 叶与邻近 Epic。

## 遗留风险

- 甲表无 PACK 即 backlog：有人误标 ready → 门 1 伪闭合。note 已写死。
- 专题企业若误挂 `E-ENT-SCRUM-PDR` / `ENT-MOD-*` OPEN → 与 A2 `TOPIC-ENT-05`「严禁使用展示 M_ENT_*」冲突。
- 书面顶 PACK 未批前，态势 9 叶长期 backlog，挡门 1。

## CI/CD（必填）

- 分支：编排仓 `dev`（本叶 **未 commit / 未 push**）
- commit：无
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A
- **cicd: skip**（设计/定义）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## Cost（必填四字段）

| 字段 | 值 |
|------|-----|
| actual_tokens | 98000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 3.2（估） |
| cost_warn | green |

## 涉及文件

- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/METRIC-OPEN-DEBT-L01.md`
- `agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/METRIC-OPEN-DEBT-L01-盘点.md`
- `agent-delivery/agent-handoffs/产品整体定义/METRIC-OPEN-E7-DS10-12-核对记录.md`
- `agent-delivery/agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/METRIC-OPEN-ENT-KEYPANO-核对记录.md`
- `agent-delivery/agent-handoffs/产品整体定义/E-25-深圳企业现状分析/METRIC-OPEN-ENT-SHENZHEN-核对记录.md`
- `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/METRIC-OPEN-ENT-COMPARE-核对记录.md`

---

## 给 coordinator 的下步

**立刻 `task-create` 成 backlog 的 7 条（是）**：甲表 6 + ZHIKU 字段已齐；无 PACK 故 `status=backlog`、`depends_on=[]`。缺的只是 MCP 建单本身（本叶禁止 `task-create`）。  
**不要**把 `DS-01`…`09-METRIC-OPEN-L01` 标 ready。  
**不要**建 `TOPIC-POLICY-METRIC-OPEN-L01`。  
建完后本叶走 AV（handoff 已在盘）；**不要**由本 product 会话把本叶打成 review/done。

### 共用字段（7 条均同，除非下表覆盖）

```
agent: algorithm-agent
collaborators: ["data-agent"]
repo: gkx-orchestration
delivery_phase: definition
task_type: definition
status: backlog
priority: P0
```

### 1. `SVCCHAIN-METRIC-OPEN-L01`

```json
{
  "id": "SVCCHAIN-METRIC-OPEN-L01",
  "title": "产业服务链 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E7-产业服务链分析",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "8",
  "difficulty": "L",
  "estimated_tokens": 90000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-SVCCHAIN-核对记录.md：覆盖机构分析/生态/招引/门户四页 ④语义卡 ⑤开放项（不适用则 N/A+依据）",
    "owner_semantic=human:淮政玮；公式/algorithm_type 共签 human:唐绍祖",
    "消费 request/专题系统/pages/SVCCHAIN-*.yaml 已有 M_SVC_ORG_*；禁止发明正式 M_* 写入 seed",
    "禁止挂展示 DS30-SVC 或 ENT-MOD OPEN；B 轨 29 个 M_SVC_* 不得打 missing",
    "无 PACK-L01 不得 ready；不挡 ALGO-LIB-METRIC-DEPS-L01"
  ],
  "note": "R1/R2/R2C 已声称五件套，可 backlog。无独立 SVCCHAIN-PACK-L01，depends_on 空。无 PACK 不得 ready。禁止挂错展示叶。FDS 不顶 OPEN。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/SVCCHAIN-ORG-ANALYSIS.yaml",
    "agent-delivery/metrics/request/专题系统/pages/SVCCHAIN-ECOSYSTEM.yaml",
    "agent-delivery/metrics/request/专题系统/pages/SVCCHAIN-RECOMMEND.yaml",
    "agent-delivery/metrics/request/专题系统/pages/SVCCHAIN-PORTAL.yaml",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 2. `TOPIC-ENT-METRIC-OPEN-L01`

```json
{
  "id": "TOPIC-ENT-METRIC-OPEN-L01",
  "title": "专题企业 TOPIC-ENT-05 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-ALGO-LIB-DEMO",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "8",
  "difficulty": "L",
  "estimated_tokens": 100000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-TOPIC-ENT-核对记录.md：覆盖 TOPIC-ENT-05 ④⑤；无统计则 N/A+依据",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖",
    "禁止挂展示 ENT-MOD-*-METRIC-OPEN；禁止消费 cfg_metric-ENT-seed 60 个 M_ENT_* 作为本页正式 ID",
    "边界真源 05.3-企业.md + SRS 04；不发明正式 M_* 写入 seed",
    "无 PACK 不得 ready"
  ],
  "note": "现网无专题企业 Epic，暂挂 E-ALGO-LIB-DEMO。禁止挂 E-ENT-SCRUM-PDR 的 ENT-MOD OPEN 叶。无 PACK（仅 05.3），depends_on 空，不得 ready。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/TOPIC-ENT-05.yaml",
    "agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3-企业.md",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 3. `TOPIC-TECH-METRIC-OPEN-L01`

```json
{
  "id": "TOPIC-TECH-METRIC-OPEN-L01",
  "title": "专题技术链 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-ALGO-LIB-DEMO",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "5",
  "difficulty": "M",
  "estimated_tokens": 60000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-TOPIC-TECH-核对记录.md：覆盖 TOPIC-TECH-05 ④⑤",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖；实现类倾向 third_party 不伪展开公式",
    "禁止发明 M_TECH_* 写入 seed；不消费展示 METRIC-OPEN",
    "与 JIUXIN-TECH-ORG-TALENT-L01 分责：本叶语义/适用性，九新叶交付形态",
    "无 PACK 不得 ready"
  ],
  "note": "registry 0。无 PACK（05.1）。邻近九新叶同 Epic。无 PACK 不得 ready。禁止挂错展示叶。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/TOPIC-TECH-05.yaml",
    "agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.1-技术链.md",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 4. `TOPIC-ORG-METRIC-OPEN-L01`

```json
{
  "id": "TOPIC-ORG-METRIC-OPEN-L01",
  "title": "专题科研机构 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-ALGO-LIB-DEMO",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "5",
  "difficulty": "M",
  "estimated_tokens": 60000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-TOPIC-ORG-核对记录.md：覆盖 TOPIC-ORG-05 ④⑤",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖；third_party 不伪展开",
    "禁止用 M_SVC_ORG_* / M_CHAIN_INSTITUTION_* 顶替科研机构；不发明 M_ORG_* 写入 seed",
    "无 PACK 不得 ready"
  ],
  "note": "registry 0。无 PACK（05.4）。禁止挂产业服务链 OPEN。无 PACK 不得 ready。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/TOPIC-ORG-05.yaml",
    "agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.4-科研机构.md",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 5. `TOPIC-TALENT-METRIC-OPEN-L01`

```json
{
  "id": "TOPIC-TALENT-METRIC-OPEN-L01",
  "title": "专题人才 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-ALGO-LIB-DEMO",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "8",
  "difficulty": "L",
  "estimated_tokens": 100000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-TOPIC-TALENT-核对记录.md：覆盖 TOPIC-TALENT-05 ④⑤",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖；与展示 DS-13～16 分叶勿混",
    "禁止消费展示人才 METRIC-OPEN；不发明正式 M_* 写入 seed",
    "无 PACK 不得 ready"
  ],
  "note": "与 DS13-16-TALENT 分叶。本批不建展示人才 OPEN。无 PACK（05.5）不得 ready。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/TOPIC-TALENT-05.yaml",
    "agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.5-人才.md",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 6. `TOPIC-QUERY-METRIC-OPEN-L01`

```json
{
  "id": "TOPIC-QUERY-METRIC-OPEN-L01",
  "title": "专题查询 — 指标语义卡+开放项核对（METRIC-OPEN）",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-TOPIC-SEARCH",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "5",
  "difficulty": "M",
  "estimated_tokens": 60000,
  "depends_on": [],
  "definition_of_done": [
    "METRIC-OPEN-TOPIC-QUERY-核对记录.md：有统计数字则 ④语义卡；壳/检索可 N/A+依据，禁止口头 N/A",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖",
    "不对 05 八维 mapped/missing；禁止发明 M_* 写入 seed",
    "无 PACK 不得 ready"
  ],
  "note": "邻近实现叶 epic=E-TOPIC-SEARCH。有统计数字就不能口头 N/A。无 PACK 不得 ready。n/a_ops 不进九新清单。",
  "design_refs": [
    "agent-delivery/metrics/request/专题系统/pages/TOPIC-QUERY.yaml",
    "agent-delivery/bid-reference/srs/04-科技专题服务系统/科技专题数据查询/",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```

### 7. `ZHIKU-METRIC-OPEN-L01`

```json
{
  "id": "ZHIKU-METRIC-OPEN-L01",
  "title": "高端智库 — 指标语义卡+开放项核对（METRIC-OPEN）补登记",
  "agent": "algorithm-agent",
  "collaborators": ["data-agent"],
  "epic": "E-ZHIKU-PROTOTYPE-110",
  "repo": "gkx-orchestration",
  "delivery_phase": "definition",
  "task_type": "definition",
  "status": "backlog",
  "priority": "P0",
  "effort_points": "5",
  "difficulty": "M",
  "estimated_tokens": 40000,
  "depends_on": [],
  "definition_of_done": [
    "消费已有 METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md，补齐 ④⑤ 会签栏（不是从零做）",
    "owner_semantic=human:淮政玮；公式共签 human:唐绍祖",
    "演示态 🔴 不得转正；Q-ZHIKU-* 保持 🟡 待登客户决策清单",
    "无 PACK 不得 ready；不改 seed"
  ],
  "note": "核对记录已在盘，补登记 registry 叶。无 PACK 不得 ready。禁止另开 E-ZHIKU-METRIC-OPEN-L01 撞车（本 ID 即登记名）。",
  "design_refs": [
    "agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/METRIC-OPEN-E-ZHIKU-新型高端智库-核对记录.md",
    "agent-delivery/产品定义评审规程.md §3.2",
    "agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md §8.4"
  ]
}
```
