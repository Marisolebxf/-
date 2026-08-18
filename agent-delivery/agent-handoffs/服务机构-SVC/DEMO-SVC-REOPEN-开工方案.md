# 服务机构施工 · 整条重开工方案（草案 · 待授权）

> **日期**：2026-08-18（v0.2，按侯佳伟口径修订：50100 先当灌数/算法底座，产品长任务等底座齐再开）  
> **监管 / 拟授权人**：`human:侯佳伟`  
> **签收**：`ready_to_sign → done` 仍是 `human:淮政玮`（chore 豁免）  
> **前置**：范围 3 停机已完成（`DEMO-SVC-ABORT-L01` = done）  
> **本文件不是授权句**。落成「新长任务总控」并写明「后续认领不必再问」之前，**禁止派单、禁止建叶**。  
> **转交**：[`DEMO-SVC-停机转交-侯佳伟.md`](./DEMO-SVC-停机转交-侯佳伟.md)  
> **规约**：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13 · 禁止 force

---

## 0. 一句话

服务机构 **先把 Demo 底座做齐，再开 50892 产品长任务**。

1. **底座站** = [50100「产业服务算法库」](http://111.198.38.90:50100/)（`demo-ui-system-test` · `/industry-service/*`）  
   按最新 `storage/SVC` 契约 **在本站真正灌数**；图谱与后续菜单 **从设计表算出并回写 Demo 库**；算法未定稿时 **用已评审原型的示例算法顶上**，不空转。  
2. **产品站** = [50892 专题](http://111.198.38.90:50892/)（`lumen-ui-topic`）  
   **底座退出门绿之前禁止开** lumen C/D/E 长任务（Java REST / 门户复刻 / 段 E）。

**不是**复活旧 A，**不是**缺陷包，**不是** 50100 继续吃前端 Mock。  
产品五件套与 `demo-ui-topic` 已评审原型 **不重做**（底座与施工只消费公式/交互口径）。CHAIN 不动。

---

## 0.1 三站不要混

| 站 | URL | 角色 | 本轮 |
|----|-----|------|------|
| **50100 产业服务算法库** | http://111.198.38.90:50100/ | 灌数台 + 十模型/图谱出数 | **底座主战场** |
| **50892 专题** | http://111.198.38.90:50892/ | 产品前端 | **底座绿后** 才开 C/D/E |
| **30999 原型** | https://skxdemo.unicomcn.tech:30999/ | `demo-ui-topic` 已评审交互/示例算法 | **只读对照**；D12 禁 merge 进 lumen |

**URL 纠偏（必读）**：  
`https://skxdemo.unicomcn.tech:30999/industry-center/overview` 是 **产业链分析（CHAIN）**，不是产业服务。  
**产业服务链分析** 在同站 **`/service-center/*`** 与 **`/service-portal/*`**（查询 / 服务链分析 / 机构分析 / 招引培育）。  
示例算法只从 **service-center** 纯函数层搬，**禁止**把 CHAIN `industry-center` 的诊断/全景算法抄进 SVC。

---

## 0.2 现状诊断（现行草案的缺口）

对照代码与停机结果，v0.1 方案有这些会卡住的问题：

| # | 问题 | 证据 | 若不改的后果 |
|---|------|------|----------------|
| 1 | 把 50100 与 50892 写在同一条 A→E 里，产品段会抢跑 | v0.1 §3 DAG 在 A3 后直接 B/C/D/E | 底座无契约表、无回写 ADS，50892 只能 Mock 或空页 |
| 2 | 「灌数」写成 A2 CLI/`svcseed`，50100 只当读面 | v0.1 §3.1 | 违反「真正灌数在 50100」；联调台按钮与真源脱节 |
| 3 | 50100 菜单是早期壳：十模型走 `CatalogModelPage` + `svcModelCatalog.ts` **前端 Mock**；图谱 `GraphView.vue` 写死演示节点 | `index.vue` 仍标「演示 Mock」；router 非 basic/graph 全走 Catalog | 与 Demo 库无关，灌了也看不见 |
| 4 | 灌数后端已被 ABORT 卸掉 | `entan/svcseed.py`、`api/svc_routes.py` 已删；`BasicPage` 仍调 `POST /entan/internal/svc/run-pipeline` | 50100「灌数据」按钮必挂 |
| 5 | 算法未定稿被当成 B 段阻塞 | Q060~Q063 🟡；唐绍祖设计 ready_to_sign 未实现 | 图谱/短板/技术力/招引会无限等甲方 |
| 6 | 未规定「页面出数 = 写设计表」 | 原型公式在前端 fixture；50100 不写 ADS | 底座不完整，产品长任务无法启动 |
| 7 | 图空间口径可能打架 | 算法设计写 `gkx_service`；存储决策 #7 一张 `G_科创` / Demo `demo_gkx_chain` | S1 不写死会再平行图 |
| 8 | 两套 Python（`demo-algo-ent-analysis` vs 日后 `lumen-algo-py svcan`）未约定何时分叉 | v0.1 把十模型直接丢给 lumen B | 50100 出不了数，或公式后来对不齐 |

以上全部在本 v0.2 用 **两阶段 DAG + 代理算法白名单 + 50100 写库铁律** 收口。

---

## 1. 为什么不能直接重跑 A / 也不能直接开 50892

| 事实 | 后果 |
|------|------|
| `storage/SVC/` S1–S4 已按范围 3 整树删除 | 无 DWD/ADS 契约，灌数没有落点 |
| 旧 A 退出门曾认 24 家 fixture / Gate-0 | 再跑等于重复错路径 |
| Java `gkxlumen-topic-svc`、Python `gkx_svc_service`/`svcan`、前端 service-* 已按路径卸除 | 产品中后段代码不在 |
| 旧 `DEMO-SVC-*` / `LUMEN-SVC-*` 已废作 | 禁止当 `depends_on`、禁止复活旧 ID |
| 50100 仍是 Mock 壳 + 断掉的 pipeline API | **必须先修算法库并接到 Demo 库** |

转交里「重跑 A 主路径 = ODS→DWD」= **底座灌数引擎的抽取策略**，不是跳过存储，也不是跳过 50100。

---

## 2. 已拍板（写入新总控后不回问）

| # | 项 | 决定 |
|---|-----|------|
| 1 | 库 | 只写 `demo_gkxlumenx_*`；禁正式 `gkxlumenx_*` |
| 2 | ODS | 共用现有 `demo_gkxlumenx_ods`，不新建 ODS 实例；禁 DROP 33 张约定表 |
| 3 | 抽取 | 主路径 = ODS → SVC DWD（`entan.svcseed` 升主）；禁 `SELECT enterprise_*`；禁复制 `dwd_org_base_info` 全列 |
| 4 | 圈定 | Demo 临时规则 `svc_rule_demo_kw_v1`（`name_cn` + `industry_l*_name`） |
| 5 | 主体 | 机构权威在 ENT；禁止 SVC 平行 `svc_org_base`；hang `org_id` |
| 6 | fixture | 24 家 `seed_svc_demo_mock.py` **旁路**，不得当底座退出门 |
| 7 | Q-SVC-010 / Q060~Q063 | 🟡 不伪闭合 live；Demo 用临时基线 + UI「待核验」 |
| 8 | 调用链 | **产品站**：前端 → Java REST → Python `/internal/*`；D12 禁 lumen 调 `demo-*`。**50100**：沿 ENT 算法台惯例直连 `demo-algo-ent-analysis` `/entan/internal/svc/*`，只读写 Demo 库 |
| 9 | 共用仓 | 只动 SVC 路径；`storage/CHAIN` / `gkxlumen-topic-chain` / `views/chain.py` / 产业链页 **不动** |
| 10 | git | `origin/dev` 直推；禁止 force；commit `[agent:<role>]` 或 `[human:侯佳伟]` |
| 11 | 看板 | 旧施工叶留 ID 审计；新 DAG **必须新 ID** |
| 12 | 文档 | 废作 handoff **不删** |
| **13** | **灌数真源** | **只认 50100「产业服务算法库 · 基础指标」上的灌数据按钮**（`append`/`replace`）。CLI/`svcseed` 是按钮背后的同一引擎，允许 CI/过夜调用，**不得**另做一套只写库、50100 读不到的路径 |
| **14** | **出数铁律** | 图谱及后续菜单的每次「运行/重算」必须 **读 S 契约表 → 算法（正式或代理）→ 回写 Demo ADS/图**。禁止页面用 `svcModelCatalog` / GraphView 内置节点充数；`USE_MOCK` 类开关在底座阶段默认关 |
| **15** | **代理算法** | 唐绍祖未实现或甲方未定稿时，**移植** `demo-ui-topic` `service-center` 已评审纯函数（见 §4），写入 Python（禁止只留在前端）。角标 🧪 + `pending_client`。不因此停工 |
| **16** | **两阶段** | **阶段 F（底座）绿** 才允许建 **阶段 P（50892 产品长任务）** 的 C/D/E。阶段 P 的 B（`lumen-algo-py svcan`）可与 F 公式冻结后并行移植，但 **不得先于 F 开产品前端** |
| **17** | **一张图** | SVC 实体/边 **hang 进** Demo `demo_gkx_chain`（决策 #7），不新建平行 `gkx_service` space。算法设计里的 `gkx_service` 视为历史别名，S1 流图改挂 |

结构歧义升级 `human:李伟`。环境卡点微信 `human:淮政玮`。

---

## 3. DAG（新总控两张表，不要合成一条抢跑）

### 阶段 F · 底座（50100 + Demo 库）—— **本轮先授权这一张**

```text
S   storage/SVC 重建
    S1 流图会签 → S2 源/ETL → S3 DWD+ADS 细表（含图谱 hang、模型回写表）→ S4 入口
    无会签流图不得把细表标 approved，也不得开 F-SEED

F-SEED  恢复 50100 灌数链路（同一引擎）
    · demo-algo-ent-analysis：svcseed + /entan/internal/svc/run-pipeline + /status
    · demo-ui-system-test：BasicPage 接到新契约（去掉「演示 Mock 已落地」假绿标）
    · 只写 demo_gkxlumenx_dwd/ads；圈定 svc_rule_demo_kw_v1
    · 退出：50100 点「灌数据」成功；基础指标读到与 DWD 同一批 org_id（空态诚实）

F-ALGO  十模型 + 图谱：按 S 表出数并回写
    · 有正式公式用 SVC-ALGO-DESIGN-L01
    · 否则用 §4 代理算法（原型 service-center）
    · 菜单页从 CatalogModelPage/Mock 改为读 ADS；GraphView 改为读 hang 后的图/关系表
    · 每页「运行」写回设计表（短板/关系/技术力/招引/培育）

F-GATE  底座退出门（现场 50100，不是 50892）
    · 契约表有 A2 命中行（不认 fixture 24 家）
    · 基础指标 / 图谱 / 短板 / 关系 / 六类技术力 / 招引 / 培育 均能从 Demo 库出数或诚实空态
    · 禁止前端 fixture 填菜单
    · 公式冻结清单（代理 vs 正式）入库，供阶段 P 移植
```

联调闸门：前序 handoff + ≥ `integration`/`pending_test` 即可开下一叶，不等签收 `done`。  
同仓一次一张 coding：`demo-algo-ent-analysis` 与 `demo-ui-system-test` 可并行（不同仓）；S 在编排仓。

### 阶段 P · 产品长任务（50892）—— **F-GATE 绿之后另开总控/续页，本次不建叶**

```text
B  lumen-topic-py /internal/gkx-svc + lumen-algo-py svcan
   （移植 F-GATE 冻结公式；禁止另发明一套权重）
C  lumen-svc-platform 一 REST 一叶（可重建 gkxlumen-topic-svc）
D  lumen-ui-topic SHELL + WAITVIEW + 一 USM 一叶（五维；USE_MOCK=false）
E  新 E0/E1；金路径真实 US-SVC-* ；旧 E ready_to_sign 不算完成
```

**禁止**：F-GATE 未绿就派 lumen 前端复刻、就当 Gate-0/E 已完成。

---

## 3.1 50100 菜单 × 设计表 × 出数（阶段 F 必覆盖）

外网站：[GKX 系统和算法 · 50100](http://111.198.38.90:50100/)  
菜单真源：`demo-ui-system-test` `industryServiceMenuConfig.ts`  
算法设计：`SVC-ALGO-DESIGN-L01`（`docs/产业服务算法设计说明.md`，**设计不废**；实现被 ABORT 卸掉）

| 菜单 | 路径 | 模型 / 能力 | 读 | 写（运行后必须落库） | 阶段 |
|------|------|-------------|---------|----------------------|------|
| 基础指标 | `/industry-service/basic` | 布局/分布/投融资/新增/深圳… | ADS `svc_*` | **灌数据** 写 ODS→DWD→基础 ADS | F-SEED |
| 产业服务图谱 | `/industry-service/graph` | 全要素图 hang | 图/关系 ADS | 节点边投影进 `demo_gkx_chain` 或契约关系表 | F-ALGO |
| 服务链短板分析 | `/gap` | `SVC_SERVICE_CHAIN_GAP` | DWD 覆盖 + 环节 | 短板结果 ADS | F-ALGO |
| 服务关系链 | `/relation` | `SVC_SERVICE_RELATION_CHAIN` | 关系边 | 强度/层次/密度 ADS | F-ALGO |
| 六类技术力 | `/tech-*` | `SVC_*_TECH_POWER` | 机构+指标 | `svc_tech_power_score` 类 ADS | F-ALGO |
| 引入推荐 | `/attract` | `SVC_ATTRACTION_RECOMMEND` | 候选+短板 | 招引名单 ADS | F-ALGO |
| 培育推荐 | `/cultivate` | `SVC_CULTIVATION_RECOMMEND` | 本土机构 | 培育名单 ADS | F-ALGO |

F-GATE：上表每一行 50100 能打开，且数字/图与 Demo 库一致（或空态 + 待核验，禁止 Mock 填满）。

50892 以后只做 **同一批 ADS 的产品读面**，不再灌第二套数。

---

## 4. 代理算法白名单（算法未定也不停工）

真源目录（只读，禁止 merge 进 lumen）：

`${GKX_ROOT}/repos/demo-ui-topic/src/app/pages/service-center/`

| 50100 / 模型 | 原型示例（函数/任务） | 临时口径（已在客户决策清单） | 诚实性 |
|--------------|----------------------|------------------------------|--------|
| 短板 `SVC_SERVICE_CHAIN_GAP` | `serviceEcosystemModel.computeStageStats`；任务 `service_eco_chain`「服务链短板分析」 | Q061：原型规则 0 家=空白、≤1=薄弱、均深&lt;55=瓶颈；清单另有 &lt;45/≥70 草案——**S3/F-ALGO 必须写清采用哪套**，推荐先用原型可核对规则，清单阈值作对照行 | 🧪 + 待核验 |
| 图谱 / 关系链 | `buildEcoGraph` + 密度/中心性；任务 `service_eco_graph` | Q062；边权未定时用原型关系类型 + 度中心性 | 挂 `demo_gkx_chain`，禁 Neo4j |
| 六类技术力 | `serviceOrgAnalysisFlow` capability：维度加权雷达；`DEFAULT` 等权 | Q060 项目临时基线：五维等权；缺字段 org_id 确定性代理 + mock 角标 | 禁止当正式评级 |
| 招引 | `computeAttractList` + `DEFAULT_ATTRACT_WEIGHTS`（35/30/20/15） | Q063 | 理由只引用行内可核对分数 |
| 培育 | `computeCultivateList` + `DEFAULT_CULTIVATE_WEIGHTS`（25/30/25/20） | Q063 | 同上 |
| 领域覆盖（若基础指标/分析需要） | `coverage-analysis` 广度×深度矩阵 | 非招标十模型核心，可作基础指标附属 | 可选 |

落地要求：

1. **移植到 Python**（`demo-algo-ent-analysis`，例如 `svcan/` 或 `entan/svc_models.py`），50100 调 API 出数；禁止只把 TS 纯函数抄进 Vue。  
2. 配置进 yaml（权重/阈值），标 `pending_client` + `proxy_from: demo-ui-topic@<commit>`。  
3. 唐绍祖正式实现到位后：**换引擎、不换表**（同一 ADS 列）；F-GATE 公式冻结表改一列即可。  
4. **不要**用 `industry-center` 的产业链诊断算法顶 SVC。

---

## 5. 段 S · 存储（先于灌数；阶段 F 第一刀）

同构 `storage/ENT` / `storage/CHAIN`。写作顺序强制：

`00-context` → **`01-data-flow`（架构师会签）** → `sources` → `etl`（含 `ods-to-dwd-mapping`）→ `stores`（DWD+ADS+**模型回写表**+**图 hang**）→ `seeds` 索引 → 改 `storage/README.md` 加回 SVC 行。

| 叶（建议新 ID） | 角色 | DoD 要点 |
|-----------------|------|----------|
| `ARCH-SVC-STORAGE-S1-L02` | architect | 流图：ODS 共用、圈定规则、ENT hang `org_id`、禁止平行主体表、**一张 `demo_gkx_chain`**、50100 写库/50892 只读；**会签前 F-SEED 不开** |
| `DATA-SVC-STORAGE-S2-L02` | data | sources + ETL 指针 + Demo 主路径（模拟 GDF）；细表 draft |
| `DATA-SVC-STORAGE-S3-L02` | data | `stores/mysql/dwd-svc.md` + `ads.md`（**含十模型结果表**）；Java 只读 ADS |
| `DATA-SVC-STORAGE-S4-L02` | data | README 入口；legacy `data-design/服务机构/` 只标历史对照 |

S1 会签 Owner：架构师（结构升级 `human:李伟`）。签收仍淮政玮。

**抽边界写进 F-SEED，不另开变更总控**：`svc_rule_demo_kw_v1` / 禁复制 ENT 全列 / 灌数只走 50100 按钮 写在新总控「已拍板」+ F-SEED `/goal`。

---

## 6. 阶段 F 建议细叶（授权后建；全部新 ID）

| 建议 ID | 仓 | 做什么 |
|---------|-----|--------|
| `DEMO-SVC-LAB-SEED-L01` | `demo-algo-ent-analysis` | 恢复 `svcseed` + `run-pipeline`/`status`；只认 S 契约；禁 enterprise_* |
| `DEMO-SVC-LAB-UI-SEED-L01` | `demo-ui-system-test` | 基础指标页接新 status/pipeline；去掉假绿 Mock 标；灌数帮助文案改 ODS→SVC DWD |
| `DEMO-SVC-LAB-GRAPH-L01` | algo + 50100 UI | 图谱读 hang；运行则投影边；禁 GraphView 内置 mock |
| `DEMO-SVC-LAB-MODELS-L01` | algo | 十模型 Python：正式或 §4 代理；写 ADS |
| `DEMO-SVC-LAB-UI-MODELS-L01` | 50100 UI | 各菜单离开 `CatalogModelPage`，改读 ADS + 触发重算 |
| `DEMO-SVC-LAB-GATE-L01` | data + 现场 | F-GATE 证据：50100 截图/接口 + 表行数；公式冻结清单 |

可按仓串行合并（UI 两叶可合成一张若监管人要求少单），但 **DoD 不得砍**：灌数按钮、图谱非 Mock、十模型写库、F-GATE。

强度：coding 叶 `ponytail full`。

---

## 7. 阶段 P（F-GATE 之后才展开，此处只留指针）

产品真源（只读）：

- `产品整体定义/E7-产业服务链分析/` 四叶子五件套  
- 原型：`demo-ui-topic` `service-portal` / `service-center`（D12 禁 merge）

| 段 | 仓 | 切法 | 退出门 |
|----|-----|------|--------|
| B | `lumen-topic-py` + `lumen-algo-py` | 移植 F 冻结公式 | `/internal/gkx-svc` 可测 |
| C | `lumen-svc-platform` | 一 path 一叶 | OpenAPI 对齐 USM |
| D | `lumen-ui-topic` | 故事：门户 / 查询 / 分析 / 生态 / 招引 + SHELL/WAITVIEW | 五维；`USE_MOCK=false` |
| E | devops + qa | 新 E0/E1 | 已发布 50892；期望未发生必红 |

CHAIN P0 D 若仍占 `lumen-ui-topic` 则串行，禁止整仓 reset。

---

## 8. 废作（新总控必须抄一份）

目录 `agent-handoffs/服务机构-SVC/` 里 **现行只认**：本方案（待升总控）、停机转交、停机总控、`DEMO-SVC-ABORT-L01`。

其余旧总控 / 段派单 / A–E 叶 / S1–S4 旧 handoff = **废作留档，不删、不派**。  
`SVC-DATA-ANALYSIS-L01*`、产品五件套、`TOPIC-SVCCHAIN-R*`、`SVC-ALGO-DESIGN-L01` = 不废（施工消费 / 定义闭环）。

---

## 9. 开工当日动作（授权句落盘后）

1. 本文件升格为 `DEMO-SVC-REOPEN-长任务总控.md`，头上写授权句；**总控范围写死阶段 F**，阶段 P 另页或等 F-GATE 再续授权。  
2. MCP 建 `ARCH-SVC-STORAGE-S1-L02`（ready）→ claim 24h · `coordinator_dispatch` · `supervised_by=human:侯佳伟`。  
3. 同仓一次一张 coding；S 在编排仓，不与 CHAIN 前端抢坑。  
4. S1 会签前 **禁止** 建 F-SEED / 十模型叶。  
5. F-GATE 前 **禁止** 建 lumen C/D/E。

### 建议授权句（阶段 F）

> 授权：`human:侯佳伟`。按《服务机构施工 · 整条重开工方案》v0.2 开新长任务总控，**范围仅阶段 F（底座）**。  
> 先重建 `storage/SVC` S1–S4；再在 50100 产业服务算法库恢复灌数并接到 `demo_gkxlumenx_*`；图谱与十模型按契约表出数回写；算法未定稿则移植 30999 产业服务链分析（`service-center`）示例算法，禁止用产业链 `industry-center`。  
> 底座退出门绿之前不开 50892 产品 C/D/E。全部新 ID。后续认领不必再问聊天。禁止 force。签收仍 `human:淮政玮`。

---

## 10. 不做

- 不派旧 C/D 细叶、不复活 `DEMO-SVC-A-RECLOSE` / Gate-0 / 旧 E `ready_to_sign` 当本轮完成  
- 不删废作 handoff  
- 不碰 CHAIN / 不把 `industry-center` 算法当 SVC  
- 不重做 USM/IA（除非侯佳伟认定 `TOPIC-SVCCHAIN-R*` 与施工缠死，另写一句进总控）  
- 不在 50100 用 Catalog/Graph 内置 Mock 冒充已灌数  
- 不在 F-GATE 前开 lumen 前端复刻长任务  
- 不写正式 `gkxlumenx_*`、不 DROP ODS 33 表、不新建平行主体表/平行图空间  

---

## 11. 请侯佳伟拍板的仅剩 2 项（不挡写总控草稿）

1. **短板阈值**：原型（0 / ≤1 / 均深&lt;55）还是客户清单 Q061 草案（&lt;45 / ≥70）？建议 Demo 先用原型，清单作对照列。  
2. **阶段 P 总控**：F-GATE 后再单独授权，还是本总控预留「F 绿自动续 P」？建议 **分开**，避免产品段再次抢跑。

其余（灌数在 50100、代理算法、两阶段、一张图 hang）已按本次口头口径写入 §2，授权总控后不再回问。
