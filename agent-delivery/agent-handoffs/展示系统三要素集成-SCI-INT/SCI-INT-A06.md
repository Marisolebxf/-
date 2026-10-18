# SCI-INT-A06 handoff · 全球创新监测（载体排行 / 监测分析 / 城市）系统集成项

- 角色：agent:product-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 日期：2026-10-18 · 仓：gkx-orchestration（origin/dev，本叶未 commit / push）
- ponytail: N/A（分析叶）

## 1. 范围与实现

| 项 | 内容 |
|---|---|
| SRS 真源 | `bid-reference` → 科技发展态势/全球创新监测.md excel_rows **76–91**（16 叶；rows 59–75 属 A05，未触碰） |
| DS 页面 | DS-04-CARRIER-RANK（76–79）· DS-04-MONITOR（80–85）· DS-04-CITY（86–91） |
| 产物 | `产物/SCI-INT-A06.yaml`：29 张 page 卡，int_id 号段 500–532 |
| 指标 | 15 个 metric_id 全部经 MCP `user-metric-registry` metric-get 核对（algorithm_type / D1 / D4），均为 d1=draft、d4=mock、D3 pending_ods |

卡片分布：ORG 6 · TECH 6 · TAL 1 · X 16（X 包含跨要素和非三要素）。

每个 SRS 行的卡数：76:3 · 77:3 · 78:2 · 79:2 · 80:2 · 81:2 · 82:2 · 83:1 · 84:1 · 85:2 · 86:2 · 87:1 · 88:1 · 89:2 · 90:1 · 91:2。

### 核心结论

1. **本页不依赖久新**。P00 中 JIUXIN 共 51 行，没有 DS-04 行，所以全部卡的 `jiuxin_row_id` 都是 null，需要久新提供的能力为 0。架构级初稿 §1 写的「ORG 模型 99/149/153」被 DS-04-CARRIER-RANK 页面映射明确禁止，本叶以页面映射为准，冲突记在 INT-A-ORG-500 的 conflicts 里，与 C03 OI-C03-11 同口径。载体指数和城市指数是否改由久新提供，单列为 DN-A06-08，待确认，默认我方自建。
2. **三要素关联点**：
   - 载体：属 ORG，依赖 C03 的 org_uid。
   - 创新点发现和价值评估：属 TECH，依赖 C02 技术点；C02 目前无主数据。
   - 城市要素里的人才：属 TAL，依赖 C01 scholar_id，或改用智库封装的人才指数。
3. **「载体=机构」口径**：直接引用 C03 OI-C03-02（科研机构无统一主数据，草案自建 org_uid，待甲方拍板），本叶不另拍板，记为 DN-A06-01。
4. **订阅和智能推送的归属**：
   - 服务归属：属我方平台服务，由 Java gkxlumen-innov 持有订阅规则、推送记录、监测配置和关注点。
   - 规则引擎：确定性规则匹配，不是算法，不经 Python，也不涉及久新。
   - 消息通道候选：gkxlumen-upms 已有 SysMessage（站内信）和 `sendEmail`（MailUtil）。innov 能否经 Feign 复用待确认，邮件是否启用记为 DN-A06-09。
   - 与 A05 INT-A-X-413（DN-A05-06）应合并为同一服务，用 rule_type 区分订阅类型。
   - 「智能」是否意味着个性化推荐算法，记为 DN-A06-06。草案默认是规则匹配，并按页面映射禁止挂 seq140 / M_SVC_REC_*。
5. **后端现状**：gkxlumen-innov 已有以下接口，均只读 ADS：
   - `/innov/v1/carriers/{rank,index-method,compare,{id}}`
   - `/innov/v1/cities/{rank,compare,index-method,{code},{code}/advice}`
   - `/innov/v1/forecast/bursts`
   - `/innov/v1/graph/points/{id}/mapping`

   但这些接口读的 ADS 表在仓内没有 DDL，lumen-algo-py 和 lumen-etl-es-py 中也找不到写这些表的任务，表是否存在、是否有数据均未知（unknown）。lumen-algo-py 没有载体指数、城市指数、创新点发现、价值评估的路由。

## 2. 偏离与冲突（as-built）

| # | 冲突 | 处理 |
|---|---|---|
| C1 | 初稿 §1 写「DS-04 依赖 ORG 99/149/153」，页面映射禁止 | 以页面映射为准；记在 500 conflicts |
| C2 | lumen 前端调用 `/situation/v1/innovation/dataset`：网关没有 `/situation/**` 路由，Java 也没有实现；真实读面在 `/innov/v1/*` | 记在 503 和 529；DN-A06-07（草案：前端拆开调用已有的资源接口） |
| C3 | 前端自己算分：`carrierRankingModel` 加权算指数、`cityModel` 计分、政策建议用模板拼接 | 违反「算法只在 Python」；记在 500/502/521/527 |
| C4 | 价值评估 `evalScore = Math.random()`，是伪数 | 违反 D9 / IP-13 诚实性；记在 514 |
| C5 | 载体指数：前端用四项权重，MCP 是三维（资源/产出/能力）。城市指数：MCP 三维、CityController 注释写「四子指数」、前端又是另一套权重 | 记在 500/521/522（CITY-B03 欠账） |
| C6 | 价值评估归展示自建还是专题战略分析（半成品行40），写者未定 | DN-A06-05 |
| C7 | DS-04-CITY 把 seq83 判为 other_system，registry 中是 STAT | 以 MCP 为准；记在 520 gaps |

B01 没有「用户配置 / 订阅」集成模式，订阅类卡与 A05 一致，暂挂 IP-13，建议 B01 补这个模式。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A06.yaml`（29 卡 + open_items 12 + structure_escalation_summary）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A06-check.py`（自检脚本）
- 本 handoff
- 没有改动代码，没有改 seed 或矩阵，没有 commit。

## 4. 验收证据

| 项 | 值 |
|---|---|
| 范围 SRS 行 | 16（excel_row 76–91） |
| 已出卡 SRS 行 | 16 |
| 差集 | 0（`gap: []`） |

`python 产物/_work/A06-check.py` 实际输出：

```
scope_count=16 covered_rows=16 diff=[]
cards: 29 {'ORG': 6, 'X': 16, 'TECH': 6, 'TAL': 1}
cards_per_row: {76: 3, 77: 3, 78: 2, 79: 2, 80: 2, 81: 2, 82: 2, 83: 1, 84: 1, 85: 2, 86: 2, 87: 1, 88: 1, 89: 2, 90: 1, 91: 2}
jiuxin_cards: 0
metric_missing: 1
structure_escalation: ['INT-A-ORG-500', 'INT-A-ORG-501', 'INT-A-X-507', 'INT-A-X-510', 'INT-A-X-515', 'INT-A-TECH-516', 'INT-A-X-517', 'INT-A-X-521', 'INT-A-X-526']
decision_needed: 15 open_items: 12
patterns: {'IP-01': 11, 'IP-03': 1, 'IP-04': 6, 'IP-08': 1, 'IP-09': 2, 'IP-10': 1, 'IP-13': 7}
OK
```

脚本校验了以下各项：
- 号段 `INT-A-(TAL|TECH|ORG|X)-5\d\d`，且前缀与 dimension 一致
- srs.path 与 P00 一致；page_ref 与 excel_row 所属页一致
- IP 编号合法
- jiuxin_row_id 全部为 null（页面映射禁挂）
- 三要素卡 call_chain 四段非空
- java / python 段不含 `demo-`（D12）
- 有 metric_ids 的卡：algorithm_type 和 d1_d4 与 MCP 一致
- 无 metric_ids 的卡：algorithm_type ∈ {n/a_ops, other_system, UNKNOWN} 且 d1_d4 = n/a；若该卡是三要素卡且 dep_kind 含 metric，必须带 `metric_missing`
- int_id 不重复

## 5. 开放项（摘要，全量见 yaml `open_items`）

| 优先 | id | owner | 事项 |
|---|---|---|---|
| P0 | DN-A06-01 | 甲方 | 「创新载体」的类型范围（引用 C03 OI-C03-02） |
| P0 | DN-A06-07 | 架构 + 前端 | 前端保留聚合 dataset 契约，还是拆开调用 `/innov/v1/*`（现状下 USE_MOCK=false 整页无后端） |
| P0 | （升级 human:李伟） | — | carrier / city / report 系列 ADS 表在仓内无 DDL、无写者；订阅规则、推送记录、监测配置等新表 |
| P1 | DN-A06-06 / 09 | 甲方 / 运维 | 智能推送是否要推荐算法；邮件通道 |
| P1 | DN-A06-05 / 11 / 12 | 产品 / 甲方 | 价值评估归属；城市人才指数来源；政策建议的生成方式 |

## 6. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 卡内算法一律放在 lumen-algo-py 的 `/internal/*`；前端现有算法列为冲突（C3/C4），要求删除 |
| 2 调用链 前端→Java→Python | ✅ 全部卡 fe → `/innov/v1/*`（gateway）→ `/internal/v1/innov/*` 或 N/A；前端不直连 |
| 3 图谱只用 NebulaGraph TRSGraph | ✅ 513 读 TRSGraph 的 ADS 投影；Java 不写 nGQL。GraphController 直读 DWM 层表，沿用 B01 R4 列为风险 |
| 4 可观测 | ✅ 沿用 B01 IP 规定（Java Agent / Python span / 前端 observability），本叶未减配 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 7 Java 只读 ADS、不写算法 | ✅ 卡内 Java 只读 ADS 或做配置 CRUD；订阅规则匹配是确定性规则，不算算法 |
| 9 / 10 D8 / D9 | ✅ 统计数字均挂 metric_id；缺失的标 metric_missing（1 处）；三个 tab 无 ⓘ 的问题记为 gaps（529） |
| 12 D12 | ✅ 卡内链路不含 demo-*（脚本已断言）。⚠️ INNOV 指标 `extras.algo_server_location` 指向 repos/demo-algo-science，已在 500/512/514/521 的 risks 写明 lumen 必须重写、禁止回落 |
| 久新 | ✅ 不调用；前端不直连；DN-A06-08 待确认 |
| 业务口径 | ✅ 未替甲方拍板，全部写成 decision_needed / open_items |

## 7. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 420000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 8.5（USD，估算） |
| cost_warn | green |
