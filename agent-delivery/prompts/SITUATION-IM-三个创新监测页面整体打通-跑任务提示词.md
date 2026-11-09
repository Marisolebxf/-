# 三个创新监测页面整体打通 · 跑任务提示词

> **用法**：本文件整段复制到**新会话**作为第一条消息即可开工。
> **形态**：`SITUATION-ENT`（科技全域态势·企业维度打通）的同构延伸，长任务模式。
> **授权人**：`human:李伟`（默认，可改） · **锁**：`lock_hours=24`
> **编写日期**：2026-10-28 · **裁定版本 v2**（2026-10-28 `human:李伟` 拍板，见 §0.0）
> 依据：`长任务执行规约.md` v1.13 · 前序手串：`agent-handoffs/科技发展态势-TS/`

**无开工前待办**：§0.0（U1–U12）与开工前勾选（C1–C10）**已于 2026-10-28 由 `human:李伟` 全部拍板**，明细见 `agent-handoffs/科技发展态势-TS/SITUATION-IM-开工前勾选表.md`。**复制本文件即可开工，不必再问。**

---

## 0. 角色、授权与工作节奏

### 0.0 裁定清单（本次已拍板，逐叶不得自行取舍）

| # | 裁定项 | 结论 |
|---|---|---|
| U1 | 链路归属 | **A 严守调用链铁律**：三页一律走 `/display/**`，由 `gkxlumen-display` 经 `RemoteInnovClient` 聚合 innov。**禁止前端直连 `/innov/**`** |
| U2 | 端点命名与粒度 | **采用契约草案命名**（`global-innovation` / `bay-innovation` / `shenzhen-innovation`）+ **区块端点粒度**（§2.3 的 15 个只读端点）+ **统一 POST**。以新建的 `SITUATION-IM-API-CONTRACT-01.md` 为本次真源（§6.0） |
| U3 | innov 数据源 | **启用**。`RemoteInnovClient` 扩只读方法是本次范围内的既定动作，不再算「结构升级」；但 **innov 侧需新增 `/internal/*` 端点**时才升级 `human:李伟` |
| U4 | UI 改动面 | **A 放宽到「接线层 + 角标挂载点」**（见 §1 边界）。**禁止**改视图结构/布局/样式/组件层级 |
| U5 | 写面端点 | **本次只做只读**。M4 的 `alerts/{id}/read`、`monitor/subscriptions`、`push-records`，以及详情型 `carriers/{carrier_id}`，**全部 deferred**（契约里保留条目并注明二期） |
| U6 | 评审 / 就绪度 | **纳入**（**显式覆盖 ENT U8「不纳入」**）。详见 U7–U9 |
| U7 | 就绪度真源 | 已有 `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml`（**143 条**，验收单元 `DS-04-*`；`D1 aligned 143`；`D3 full 9 / partial 122 / none 12`；**`D4 全部 mock`**）。本次**不是重新登记指标**，而是「映射 → 只读镜像 → 评审层 → 三页挂载」 |
| U8 | 诚实性（不得改绿） | `D4=mock` → 三页所有统计数字**必挂 🧪 MockBadge**；`D2=provisional` → **必带「待核验」字样**；**禁止把任何一维提前翻绿**（沿用 ENT U2 精神） |
| U9 | catalog 过渡态 | `gkxlumen-metrics` 目前**只有** `cfg_metric-ENT-seed.json`，**无 INNOV seed** → 本次走**过渡态只读镜像**（集中单文件，头注释注明 yaml 真源路径 + 同步任务号）；catalog 含 INNOV 后切换，切换条件写进 `src/review/README.md` |
| U10 | `views/innov` 隐藏页 | **不动不删不复用**（已核实：仅在 `src/router/routes.ts:21-30` 定义、`showInMenu:false`、全仓无任何跳转引用、与三页不共用任何代码）。挂 §3.3-7 技术债红线 |
| U11 | git | **每叶停本地**：commit 可做、**严禁 push**，走查通过后由 `human:李伟` 人工推送（仓级人工验收闸门 + ENT 总控 §1.6） |
| U12 | pilot 顺序 | **先 M6 深圳**（地域锁死、Tab 最少、统计数字最少）跑通「真端点 + 评审角标」双链路，再 M5 → M4（M4 最后：含 D2 轮询语义） |

### 0.1 你是谁

你是本管线的执行 agent，允许在一会话内跨三个仓推进，但**提交时按仓切角色前缀**：

| 仓 | 角色前缀 | 分支 |
|---|---|---|
| `lumen-svc-platform`（后端 display / element） | `[agent:be]` | `origin/dev` |
| `lumen-ui-science-pc`（前端） | `[agent:fe]` | `origin/dev` |
| `gkx-orchestration`（WBS / handoff / registry） | `[agent:coord]` | `origin/dev` |

禁止 force push；禁止一次同时改两个 lumen 仓未完成就跳仓（同仓串行）；**默认不 push**（U11）。

### 0.2 授权（默认 A）

- **A（默认，长任务模式）**：本文件 §0.0 与 §1–§7 已拍板项不必再逐叶问我。`supervised_by=human:李伟`，`claim_type=coordinator_dispatch`。只在 §3.3 红线（结构升级 / 正式库风险 / 无人值守例外）停下。
- **B**：每叶做完向我报备，我点头再进下一叶。

### 0.3 派单体系的现实约束（重要，别卡在这）

规约要求 registry 经 **MCP** `task-create` / `task-claim` / `task-update-status` 落库，禁止手改 `task-registry.yaml`。

但**本 IDE 会话里没有该类 MCP 工具**（前序任务已核实）。处理方式，二选一并按实情写进 handoff：

1. 若本会话有 task MCP → 严格走 MCP，禁止手改 registry。
2. 若无（前序情况）→ 允许直接改文件，**但必须**在每份 handoff 与 commit message 里写明「因无该 MCP 工具、经监管人当场指示，按文件直接更新」，并在 §7 自检清单里如实勾相应项。前序先例：`gkx-orchestration` 的 `[agent:coord] docs(registry): 科技全域态势 8 叶走查签收（human:李伟）`。

> ✅ **本管线已走路径 2**：`human:李伟` 于 **2026-10-28 当场书面授权**（勾选表 C2=①）：本会话确无 task MCP 工具，coordinator **直接更新 `task-registry.yaml`**，但**每个** handoff 与 commit message 必须写明上述字样。**不要再纠结要不要手改、也不要为此停下来回问监管人。**

**没有 registry ID 不许改业务仓代码**——这是硬红线。

---

## 1. 目标（一句话）

> **让「全球创新监测、湾区创新监测、深圳创新监测」三个页面从「裸 fetch 不存在的路由 + 全量 dataset」改造成「真实后端端点 + 筛选联动 + 诚实空态 + 就绪度/血缘角标」，达到与已打通的科技全域态势总览页同等的可用性与合规性。**

**不在本次范围**：三页的视觉复刻与布局重做（前置 `FE-TS-04A` / `FE-TS-05A` / `FE-TS-06A` 已完成并签收）。若发现某区块 UI 明显缺件，**另开补单**，不许在本任务里顺手重构视觉。

**改动边界（U4，diff 只允许这五类，验收逐项核）**：

| 允许 | 说明 |
|---|---|
| `src/api/situation/*` | 删裸 fetch → `defineApi` 双轨 |
| `views/situation/{三页}/models/**` | **新增**数据装配层（拼回现有 Dataset 形状） |
| `index.vue` 的取数处 | 仅数据源换成装配层的那几行 |
| **角标挂载点** | tabs 中**单行插入** `<ReviewMetricBadges>` / `<MetricSpecHint>`，**不改结构/布局/样式/CSS** |
| `types/*.ts` | 入出参类型 + per-block `emptyReason` + `metric_id` |

除此之外的一切 diff（尤其 `styles/*.css`、模板结构、组件层级、Arco 用法）**一律退回**。

---

## 2. 现状（已核实，精确到文件行）

### 2.1 三个页面

| 页面 | 入口 | Tab 区块 |
|---|---|---|
| 全球创新监测 | `src/views/situation/global-innovation/index.vue`（126 行） | detail / realtime / ranking / monitor / city |
| 湾区创新监测 | `src/views/situation/bay-innovation/index.vue`（163 行） | overview / capacity / analysis(SWOT) / indicators + 预警中心抽屉 |
| 深圳创新监测 | `src/views/situation/shenzhen-innovation/index.vue`（112 行） | carrier / indicator / domain / compare |

> 菜单名是「**湾区**创新监测」（`src/router/menu.ts`），不要用「大湾区」到处命名；契约前缀是 `bay-innovation`。

### 2.2 病灶（三条）

1. **real 分支是裸 fetch，且目标路由全仓不存在**（0 命中）：

   - `src/api/situation/globalInnovation.ts:15` → `fetch('/situation/v1/innovation/dataset')`
   - `src/api/situation/bayAreaInnovation.ts:15` → `fetch('/situation/v1/bay-area/innovation/dataset')`
   - `src/api/situation/shenzhenInnovation.ts:15` → `fetch('/situation/v1/shenzhen-innovation/dataset')`

   同目录 `src/api/situation/index.ts:8` 的注释已经点明：`原 /situation/v1/** 后端全仓无此路由（0 命中），故改走 /display。`

2. **入参一律 `{}`**（三处 `index.vue` 调用），没有任何筛选（无地域 / 无时间 / 无关键词），也不参与 `regionPaths`。

3. **三页都没有 store**，类型各自为政：`types/bayArea.ts`、`types/shenzhenInnovation.ts`、`types/situation.ts`（`GlobalInnovationDataset`）。

### 2.3 目标范式

#### 前端参照物

已打通的 `src/views/situation/overview/index.vue`：

- 状态由 `useSituationStore`（`src/stores/situation.ts:15-52`）持有：`regionKey / fieldValues / factorValues / keyword / timeRange{startYear,endYear}`
- 细粒度多端点：`fetchSituationMap / Overview / Timeline / Events / Influence / Compare / Cluster`（`api/situation/index.ts:41-83`）
- 统一 `request` 封装 + `BASE_URL`，**不是裸 fetch**：`const BASE = '/display/v1/situation'`（`api/situation/index.ts:36`）
- **数据装配在 `overview/models/`（图表/口径纯函数），视图只消费** —— 三页照此套（`models/` 层是本次唯一允许的新增装配面）

> **命名陷阱（务必看清）**：store 里叫 **`regionKey`（string，单值）**，`types/situation.ts:250` 的请求体字段叫 **`regionPaths`（`string[][]`，级联）**。两者不是同一个东西，照抄时别混写；传参与后端口径以 **`regionPaths`** 为准。

> **特别注意**：现有 `useSituationStore` 是 M1 的全局筛选（`factorValues` = 11 要素、`fieldValues` = 学科领域）。三页语义不同（M5 锁定湾区 11 城、M6 锁深圳 + 行政区），**不要硬套 M1 的 `factorValues`**；各页按 §2.3 端点表里的真实维度建**页级** store 或扩展项，且 mcIndices（领域/城区枚举）从数据层取，不在前端写死。

#### 后端参照物

照 `SituationController`（`@RequestMapping("/v1/situation")`）的写法，**并补齐三条铁律**：

```java
@PostMapping("/xxx")
public R<Map<String,Object>> xxx(@RequestBody(required=false) Map<String,Object> params) {
    Scope scope = scopeOf(params);            // 唯一入参翻译层：regionPaths / activeRegionKey / timeRange / searchTerm
    try { ... elementClient.xxx(...) ... innovClient.xxx(...) }   // Feign 调 element / innov
    catch (Exception ex) { log.warn("[...] 降级: {}", ex); }      // 保持结构完整，不 5xx
    // ① 空则填 emptyReason（分区降级：逐块兜，不许整包失败）
    // ② 回写 scopeLabelOf(scope) 说明实际生效范围
    // ③ ⚠️ 所有序列化数值强转 int / double（防平台 Jackson 把 Long 转 String，ECharts 画不出曲线）
    //    —— 沿用 SituationController L384-410 既有写法
    // ④ 每块带 metric_id，供前端查就绪度（禁止前端硬编码状态）
    return R.ok(data);
}
```

最短可抄示例：`gkxlumen-display/.../controller/SituationController.java:326-350`（`/influence`，约 25 行）。
此外再看 `SituationController.java:45-50`（FACTORS 常量冻结写法）与 `:310-324`（「哪些入参真的生效」诚实声明注释的正确写法 —— **每个新端点都要写这段**）。

#### 端点清单（U2，本次唯一口径）

```text
统一：POST /display/v1/situation/...（前端 BASE 写死 '/display/v1/situation'，不新建网关路由）

M4 全球创新监测
  /global-innovation/achievements         → innovations（成果列表 + 地图落点；detail / realtime 共用）
  /global-innovation/realtime             → 实时 KPI + 趋势 + 领域分布
  /global-innovation/carriers             → carriers（ranking + detail 的载体）
  /global-innovation/alerts               → alerts（monitor）
  /global-innovation/cities               → cities（city 五维 + 政策建议）

M5 湾区创新监测
  /bay-innovation/achievements            → points（11 城 67 点）
  /bay-innovation/capability              → capacities（四维 + 历史 + 构成）
  /bay-innovation/swot                    → swotData
  /bay-innovation/indicators              → indicators（6 指标 + 11 城构成 + 口径）
  /bay-innovation/alerts                  → alerts（预警中心）

M6 深圳创新监测
  /shenzhen-innovation/carriers           → carriers
  /shenzhen-innovation/indicator-systems  → indicators（10 系三级 + 构成 + 历史）
  /shenzhen-innovation/field-distribution → domains（8 领域 × 4 指标 + 空间集聚）
  /shenzhen-innovation/city-benchmark     → compareCities（8 城四维 + 缺口 + 外推）
  /shenzhen-innovation/operation-timeline → 运行监测时间轴
```

- **粒度原则**：按**数据块**切（不是按 Tab —— M4 的 `detail` 与 `realtime` 共用 `innovations`），共 **15 个只读端点**（M4 5 + M5 5 + M6 5）。这样才有分区降级：一块挂只有一块空 + `emptyReason`，不许整包失败。
- **统一 POST**：契约草案里 `realtime`/`capability`/`swot`/`indicators` 是 GET，本次一律改 POST（对齐 M1 同构写法），偏离记进契约《偏离表》。
- **deferred（本次不做，契约保留条目）**：`alerts/{id}/read`、`monitor/subscriptions`（GET/PUT）、`push-records`、`carriers/{carrier_id}`、`/available` 类探活。
- 前端配套：**新增 `models/` 装配层**用 `Promise.allSettled` 逐块拉取、逐块 catch，拼回现有 `GlobalInnovationDataset` / `BayAreaInnovationDataset` / `SzInnovationDataset` 形状 → **tabs 零改动**（U4）。

---

## 3. 数据边界与红线（最容易翻车的一节，逐条看）

### 3.1 现在真有数据的（可用）

| 表 / 视图 | 关键字段 | 归属 |
|---|---|---|
| `dwd.enterprise_base`（18.9w 行） | `org_id, enterprise_name, city, district, headquarters_lng/lat, registration_date, industry_category, patent_grant_count, is_high_tech / is_little_giant / is_gazelle / is_unicorn / is_listed / is_sme, revenue_growth_rate（**整列 NULL**，禁止拿来算增长）` | element |
| `ads.enterprise_score` | `org_id, score_total, metric_ids` | element |
| `ads.tech_power` | `transfer_score, cooperation_score`（**有**，独立信号，非 score 拷贝） | element |
| `ads.enterprise_domain_dist` / `type_dist` | `domain / stat_year / enterprise_count / ratio / growth_rate` | element |
| `dwm_org_achievement_year` | `paper_cnt, patent_apply_cnt` | **innov（U3 本次启用）** |
| `ads_node_influence`、`dim_tech_domain` | — | **innov（U3 本次启用）** |

- display 侧已有 `feign/RemoteInnovClient.java`，**当前只有 `health()`（:24）** —— 扩展只读方法是本次范围内的既定动作（U3）。
- `SituationController.java:357-361` 已注明各 clustering 维度谁有源谁没源，照其口径，不要重复造判断。

### 3.2 空表（禁止使用，禁止拿它冒充数据）

`enterprise_region_summary` / `industry_summary` / `growth_trend` / `industry_distribution` —— **全部 0 行。**

### 3.3 红线

1. **禁止造假**。无数就空态（可见文案 + 非 5xx），不许构造系数、不许复制企业曲线当别的主题趋势、不许用 demo fixture 填数。`USE_MOCK=false` 时尤其如此。
2. **禁止静默兜底**为空数组却不给理由 —— 回填 `emptyReason`，页面显示「要素服务不可达（UNREACHABLE）…」这类诚实文案。**逐块兜**，不许整包 catch。
3. **11 要素里除 enterprise 目前全为 0**（`SituationController.java:45-50` 只是冻结的 key 常量）。三页的专利 / 论文 / 专家 / 项目类卡片，没真数据就**显示空态**。
4. **结构升级项**（新表、改主键、新 ES、**innov 侧需新增 `/internal/*` 端点**）：该叶 `blocked` + 升级 `human:李伟`，**同段其它叶继续跑**。`RemoteInnovClient` 本身扩只读方法**不算**结构升级（U3）。
5. 禁止无闸门写正式 `gkxlumenx_*`；联调只写 `demo_gkxlumenx_*`。
6. 前端禁止直连 Python；Java 不写算法；不为本任务新建 ES 索引。
7. **`@/api/innov` 与 `views/innov` 是违规存量**（前端直连 `/innov/**`，违反「前端只调 `/display/**`」调用链铁律）。本次**不得 import、不得复用、不得删除**；需要 innov 数据一律走 `display → RemoteInnovClient`。遗留迁移另开单，本次 handoff 挂一笔技术债。
8. **鉴权配对**：display 侧端点若标 `@NoToken`，下游 element / innov 必须配对 `@Inner`，不一致不许上线。
9. **评审红线**（U6–U9）：
   - 每个统计数字必有 ⓘ（`IconInfoCircle`）或 D1 missing 红问号（`IconQuestionCircle`）；找不到 `metric_id` 就出**红问号**，**禁止显示伪 8 件套**。
   - 就绪度状态只能来自「只读镜像 / catalog」，**禁止页面或组件手写状态**。
   - 排列顺序：数字 → [ⓘ/？] → [结构] → [⚠️/⏰] → [🧪/⟳]；同点最多 3 枚、间距 4px。
   - `pending_hint` 缺口长文案**禁止前端硬编码**（真源为 data-gap catalog）。
   - 关闭评审模式后 DOM 零泄漏（`metric_id` / `Q0xx` / `GAP-*` 字样全无）。

---

## 4. 环境与工具（本机已验证的事实）

### 4.1 端口与联调方式

| 服务 | 端口 | 备注 |
|---|---|---|
| 前端 dev server | **`3000`**（`.env.development:3` `VITE_APP_PORT=3000`；`vite.config.ts:37` `port: Number(env.VITE_APP_PORT) \|\| 3000`） | ⚠️ 不是 3600（前序文档里 3001/3600 均为手工指定或笔误，以本机配置为准） |
| `gkxlumen-display` | `7099` | local profile permitAll，直连本机 |
| `gkxlumen-element` | `7082` | display 经 Feign 调它 |

`.env.development` 现为 `VITE_APP_API_URL = http://127.0.0.1:7099`（:10）+ `VITE_APP_USE_MOCK=false`（:16）+ `VITE_ENABLE_MOCK_AUTH=true`（:17，不挂 Bearer，正好适配 display permitAll）。

### 4.2 `.env` 改造（**已裁定：做**，勾选表 C6=①）

现状值的含义：**别人 clone 后跑 `pnpm dev` 会静默直连自己机器的 7099**，没起本地后端就是白屏。**本次必须做掉这三步**：

1. `.gitignore` 加 `.env.*.local`
2. 新建 `.env.development.local`（不入库）：`VITE_APP_API_URL = http://127.0.0.1:7099`
3. `.env.development` 里该值改回网关地址，`VITE_APP_USE_MOCK=false` 保留

**注意第 3 步不能直接删这一行** —— `vite.config.ts` 的 proxy 没有兜底，`target` 为 `undefined` 会直接抛错。
本项已裁定为「改」（C6=①），**按上面三步做，不要跳过、也不要改成「先留着」。**（历史提示：TODO ② 曾长期未决，现已关闭。）

### 4.3 浏览器实跑（页面走查的唯一有效证据）

**当前不需要注假 token**：`VITE_ENABLE_MOCK_AUTH=true` + `VITE_APP_USE_MOCK=false` 组合下 `utils/request.ts` **不挂 Bearer**，正好适配 display local permitAll（`.env.development:13-17`）。

```bash
playwright-cli open http://127.0.0.1:3000/
playwright-cli goto http://127.0.0.1:3000/trend/tech-overall-situation   # 对照页，先确认基线
playwright-cli goto http://127.0.0.1:3000/trend/shenzhen-innovation      # pilot 页（U12）
```

> 若实际跑起来仍跳 `/login?redirect=...`，说明守卫与 `ENABLE_MOCK_AUTH` 语义有出入 —— **如实记录并按 §3.3 处理，不许绕过守卫硬测**。

常用子命令：`open` / `goto` / `find <文本>`（返回元素 ref）/ `click <ref>` / `hover <ref>` / `eval <函数>`。

**踩坑备忘**：
- PowerShell 下 `eval` 的参数必须**外层双引号、内部单引号**，否则会被拆成多参数报 `too many arguments`。
- `click` 用 CSS selector 若命中多个会 strict-mode 报错，先用 `find` 拿 ref。
- 纯 JS 的 `el.click()` 有时不触发 Arco 的事件，优先用 `click <ref>`（真实鼠标）。

---

## 5. 执行方案（分段 · 依赖闸门口径）

同 §6.2 联调闸门：下游可在前序有 handoff 且状态 ≥ `integration` 时开，**不等签收 done**。

```text
A0 体检（必有，决定后面所有叶的范围）
   ↓
R0 评审底座（fe，尽早做：后面的每一叶都要挂角标）
   ↓
C 段 后端端点（一 REST 路径一叶，同仓串行）  ── pilot 先 M6
   ↓
D 段 前端改造（一页/一能力一叶）            ── pilot 先 M6
   ↓
R1..R3 三页角标挂载（可随各页 D 段之后）
   ↓
人工走查（三页所有 Tab 实跑）→ 签收 → 【停在本地，等 human:李伟 人工推送】
```

### A0 · 数据体检（`SITUATION-IM-A0-L01`）

**不许跳过。** 产出一份体检报告，逐条回答：

1. 三页每个 Tab 需要的每个字段，分别有没有真数据？（对照 §3.1 / §3.2）
2. 哪些能真出数、哪些必须走空态？逐卡片列表 + 行数量级。
3. **innov 侧现有可用端点清单**（U3：curl `gkxlumen-innov` 探活 + 列出能直接支撑哪些数据块）；若某块必须 innov 新增 `/internal/*` → 标 `blocked` 升级。
4. 需要新增 SQL / DAO 方法的清单（表名 + 字段 + 过滤条件）。
5. **三页每个统计数字 ↔ `metric-readiness-matrix-INNOV.yaml` 的 `metric_id` 逐条映射表**；映射不上的点位列出来，走 D1 missing 红问号（U7）。
6. 是否触及结构升级项（§3.3-4）——触及就标 `blocked` 升级，其余照跑。

体检报告本身即是该叶 handoff，落到 `agent-handoffs/科技发展态势-IM/SITUATION-IM-A0-L01.md`。

### R0 · 评审底座叶（前端，`SITUATION-IM-R0-L01`）

必须先于/平行于 C 段开工（后续每叶都要用它）。产出：

- `src/review/`：`feature.ts`（总开关 `isReviewFeatureEnabled`）+ `index.ts`（唯一 barrel）+ `README.md`（**上线清理清单** —— 照 `lumen-ui-topic/src/review/` 三件套）
- `src/stores/review.ts`：评审模式切换 + 组件自闸
- 组件（已有底座，升级而非重写）：
  - `src/components/lineage/MetricSpecHint.vue`（**现存**：只有 4 项元数据、无就绪度区块、不自闸、ⓘ 是文本符号）→ 升级为 **8 件套 + version + 就绪度四行区块 + Arco `IconInfoCircle` + 自闸**
  - `src/components/lineage/MockBadge.vue`（**现存**）→ 补自闸
  - 新增：`SchemaGapBadge` / `PendingBadge`（含 `pending_ods` 蓝钟）/ `IngestingBadge` / `ReviewMetricBadges`（统一排列）
- **readiness 只读镜像**：从 `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml` 生成，**集中单文件**，头注释注明真源路径 + 同步任务号（U9 过渡态）
- DoD：开关关闭后 DOM 零泄漏；组件自闸；排列与间距合规（§3.3-9）

### C 段 · 后端端点（一 REST 路径一叶）

- 仿 `SituationController` 写法：入参走 `scopeOf`、Feign 调 element/innov、catch 降级、逐块 `emptyReason`、数值强转 `int/double`、`@NoToken` 与下游 `@Inner` 配对、`R.ok`。
- **每个端点都要写「哪些入参真的生效」的诚实声明注释**（照 `SituationController.java:310-324`）。
- 端点清单与顺序见 §2.3；**先做 M6 的 5 个**（pilot），再 M5 → M4。
- 每个端点自测：curl 至少 3 组入参（无筛选 / 有地域 / 有时间范围），数值与库级计数能对上，写进 handoff。

### D 段 · 前端改造

每组改造必须包含**全部五件**，缺一不算完成：

1. **API 层**：删裸 fetch，改 `defineApi` 双轨 + `request` 封装 + `BASE='/display/v1/situation'`
2. **装配层**：新增 `models/useXxxDataset.ts`，`Promise.allSettled` 逐块拉 + 逐块 catch → 拼回现有 Dataset 形状；`index.vue` 只换数据源那几行（U4）
3. **筛选联动**：建**页级** store（或扩展），按各页真实维度传参并进 watch key
   - M4：城市 / 领域 / 关键词 / 建成年区间
   - M5：城市（锁湾区 11 城）/ 类型 / 领域 / 时间
   - M6：行政区（锁深圳）/ 类型 / 领域 / 创新价值
   - ⚠️ **不要**照抄 M1 的 `factorValues`（11 要素）—— 三页语义不同，套上去就是假联动
4. **类型**：入出参类型写进对应 `types/*.ts` 作为**唯一真源**，并同步 bump `SITUATION-IM-API-CONTRACT-01.md`（§6.0）
5. **空态**：每个区块都要有可见空态文案 + `emptyReason` 透传，不许白屏、不许 5xx、不许静默空数组

### R1..R3 · 三页角标挂载（随各页 D 段之后）

按 A0 产出的映射表，逐个统计数字挂 `metric_id` + ⓘ/红问号 + 角标；挂不上的列进 handoff 遗留（不许跳过，也不许显伪 8 件套）。

---

## 6. 交付与留痕

### 6.0 契约真源（本次新建，必先于 C 段开工）

`agent-delivery/agent-handoffs/科技发展态势-TS/SITUATION-IM-API-CONTRACT-01.md`（本次已起草骨架）

- **本次不再纠结 API-TS-M4/M5/M6 草案，也不再新造路径名**：命名采用草案前缀，实装差异写进本契约的《偏离表》，并 bump 版本。
- 改契约 → 先 bump 契约文档版本 → 再同步 `types/*.ts` 与 mock 种子（`defineApi` 双轨两侧对齐），**禁两处漂移**。
- 每份 C/D 叶 handoff 必须回写本契约的《实装对照表》一行。

### 6.1 任务 ID

```text
SITUATION-IM-A0-L01        体检
SITUATION-IM-R0-L01        评审底座（review 层 + 组件 + readiness 镜像）
SITUATION-IM-C1..C15-L01   后端端点（一 REST 路径一叶；顺序 M6 → M5 → M4）
SITUATION-IM-D1..D3-L01    前端打通（一页一叶）
SITUATION-IM-R1..R3-L01    三页角标挂载（随各页 D 段之后）
```

每条字段至少含：`title / agent / epic / priority / repo / status / depends_on / supervised_by=human:李伟 / claimed_by / claim_type / lock_until`，以及签收时的 `sign_off`。若 `epic` 另有约定以 registry 现行为准，并在 §7 记一笔。

### 6.2 handoff

每叶一份，路径 `agent-handoffs/科技发展态势-IM/{task-id}.md`，套 `templates/handoff-template.md`，必含 `ponytail:` 与 cost 四字段、以及五类内容：改了什么 / 为什么这么改 / 验证了什么（贴实测数字）/ 遗留 / 下叶要注意的坑。

### 6.3 过程文档

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/WBS.md` 增变更记录行，**一行一事，含根因与实测数据**
- 同步「进度 / 流程流冰」两处（照前序做法）
- `task-registry.yaml` 更新（见 §0.3 的两种路径）

### 6.4 git

- 三仓 commit message 按 §0.1 前缀
- **默认不 push（U11）**：每叶停本地，走查通过后由 `human:李伟` 人工推送
- 若某仓确需先行整合看到仅存的自动化等待列表，**先取得 `human:李伟` 明示书面授权**才可 push，push 前 `git pull --rebase origin dev`
- **`gkx-orchestration` 的 registry 例外**：4 万行文件双侧末尾追加会导致 **rebase 把条目字段交错对齐**，拼出损坏 YAML。遇冲突改 **merge**：取远端版本作基底，再把本任务条目整体追加；校验「相对远端纯新增、0 删除、无重复条目、无冲突标记」后再提交
- 该仓 pre-commit hook 依赖 bash，本机默认 `bash` 可能命中损坏的 WSL。若命令因此挂起，用 Git 自带 bash 事后补跑，**不要默认 `--no-verify`**；确需跳过必须在汇报里说明并补跑

---

## 7. 交付前自检（逐条打勾，不许跳）

- [ ] 三页每个 Tab 在 `USE_MOCK=false` 下页面实跑过，截图或实测数值进 handoff
- [ ] 有真数据的卡片：数值与库级计数能对上
- [ ] 无数卡的：显示**可见空态**且带 `emptyReason`，不是白屏、不是 5xx、不是静默空数组
- [ ] 地域 / 时间筛选改动后，三页的 KPI 与图**同步变化**（重点验 `regionPaths` 有没有真的传下去；注意别把 `regionKey` 当 `regionPaths` 传）
- [ ] **逐块降级**：单独断掉某数据源，只有对应区块空 + 有理由，其余区块照常显示
- [ ] **Long→int 自检**：所有序列化数值字段为 `int`/`double`，ECharts 曲线能画出来
- [ ] **每个统计数字**有 ⓘ 或红问号；`metric_id` 能落回 INNOV 矩阵；找不到的一律红问号（无伪 8 件套）
- [ ] **就绪度诚实**：`D4=mock` 出 🧪、`D2=provisional` 带「待核验」，无任何一维被提前翻绿
- [ ] **评审关闭后 DOM 零泄漏**（无 `metric_id` / `Q0xx` / `GAP-*` 字样）
- [ ] **diff 清单化**：`views/situation/**` 的改动逐项落在 §1 允许的五类之内，`styles/*.css` 零 diff
- [ ] 未 import / 未复用 `@/api/innov` 与 `views/innov`（U10）
- [ ] `type-check` exit 0、`pnpm build` 通过、lint 0
- [ ] 浏览器 console 无 `pageerror`
- [ ] 每叶有 registry ID + handoff + AV；§0.3 路径如实勾选项
- [ ] 三仓**已 commit、`dirty=0`**，临时脚本 / 日志 / `.playwright-cli/` 已清理；**未 push**（U11）

---

## 8. 前序踩过的坑（直接复用，别重蹈）

1. **地图联动**：定位策略是 >1 点 fitBounds、=1 点定位、0 点回落；fit padding 要**按容器比例自适应**（demo 的 128px 留白在 420px 面板上会把 zoom 压到 2，视觉仍是世界地图）。已有封装 `src/components/map/TiandituMap.vue`，三页地图**复用它**，禁止页面里再 `new L.map`。
2. **地图跟随滞后一拍**：判断数据更新**不要用 `focusPositions.length`**（深圳→南山点数恒为 1，长度不变导致补 fit 不触发），要用**坐标签名**（点数 + 首尾点）+ 记录已适配签名。
3. **Arco Cascader 只能选叶子**：`cascader-option.js` 只在 `option.isLeaf` 时回调选中，父节点点击仅展开，**没有 `change-on-select`**（按 antd 习惯加是无效属性）。要支持「选整个深圳市」只能靠数据层补一个「XX（全市）」叶子子项。
4. **统计指标与图脱节**：按钮高亮 / 面板标题 / 实际渲染三处状态必须收口到一个 `effectiveChartType`；「数量统计」取 `rawValue`（家）而不是百分比 `value`；增长趋势用真年度序列，不要拿分布占比冒充时间趋势。
5. **百分比口径**：占比合计必须 100.00%（最大余数法），同时保留 `rawValue` 给数量口径。
6. **地域筛选，不生效**（已修，但仍要验）：历史坑是「每个端点各认一半入参，各漏一半」导致 KPI 不动。修法是**并入唯一翻译层 `scopeOf`**（`SituationController.java:310-324`）。**三页新端点必须一开始就走 `scopeOf`，禁止各自解析地域**。
7. **`regionKey` ≠ `regionPaths`**：store 存前者、请求体传后者（`string[][]`），混写会导致筛选永远不生效。
8. **demo 冻结种子的 germane**：mock 种子保持双轨不删，`USE_MOCK=false` **零 fixture 填数**；`Math.random` / `Date.now` 一律禁止。

---

## 9. 一句话汇总给你的下个会话

> 照 `SITUATION-ENT` 的模式但不照它的 UI 零改动粒度：把三张创新监测页从「裸 fetch 不存在的路由 + 全量 dataset + 无筛选」改造成「`/display/v1/situation/{global|bay|shenzhen}-innovation/*` 区块端点（15 个只读、统一 POST）+ `models/` 装配层 + 页级筛选联动 + 诚实空态 + 就绪度角标」；innov 数据经 `RemoteInnovClient` 聚合、绝不前端直连 `/innov/**`；先 A0 体检 + R0 评审底座，再以 **M6 深圳**为 pilot 按「一 REST 路径一叶」做后端、「一页一叶」做前端；无数就空态、D4 全 mock 必挂 🧪，绝不允许造假或提前翻绿；每叶建单 + handoff + 实测证据；**全部停在本地，走查通过后由 `human:李伟` 人工推送**。
