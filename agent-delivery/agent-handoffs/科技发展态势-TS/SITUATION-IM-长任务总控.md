# SITUATION-IM · 长任务总控（创新监测三页 · 数据打通 + 评审就绪）

> **日期**：2026-10-28
> **授权**：`human:李伟`（本管线监管人；**授权句已生效（2026-10-28）：「后续认领不必再问」**）
> **目标**：创新监测三页（DS-04 全球 / DS-05 湾区 / DS-06 深圳）在 `USE_MOCK=false` 下，从「裸 fetch 不存在的路由 + 一次性 dataset」跑成「**真实后端端点 + 筛选联动 + 诚实空态 + 指标血缘/就绪度角标**」的可用闭环。
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)（v1.13；本文件与规约冲突处以本文件已拍板项为准，规约红线不可豁免）
> **同构前序**：`SITUATION-ENT-长任务总控.md`（DS-01 企业维度，2026-10-27）
> **挂接 WBS**：`工程过程/04-系统集成/05-展示系统集成/WBS.md` **§4.4 · WBS-05-19 子任务 05-19-01～23**

---

## 0. 裁定记录（2026-10-28 授权人拍板）

> **开工前勾选（C1–C10）已毕**（同一天，`human:李伟`）：**C1=①**（角标不算 UI 改动，须满足 §0.1 三条）· **C2=①**（授权无 MCP 时直接改 `task-registry.yaml` + 注明）· **C4=①**（`SITUATION-IM-API-CONTRACT-01.md` 作本期施工真源）· **C10=走查签收 `human:李伟`**；**C3 / C5 / C6 / C7 / C8 / C9 按默认①**。明细 `SITUATION-IM-开工前勾选表.md`。**本管线无开工前阻塞项，可直接建 A0 单。**

| # | 裁定项 | 结论 |
|---|--------|------|
| U1 | 链路归属 | **A 严守调用链铁律**：三页一律走 `/display/**`，由 `gkxlumen-display` 经 `RemoteInnovClient` 聚合 `gkxlumen-innov`。**禁止前端直连 `/innov/**`** |
| U2 | 端点命名与粒度 | **采用契约草案命名**（`global-innovation` / `bay-innovation` / `shenzhen-innovation`）+ **区块端点粒度（15 个只读）** + **统一 POST**。真源 = `SITUATION-IM-API-CONTRACT-01.md` |
| U3 | innov 数据源 | **启用**。`RemoteInnovClient` 扩只读方法属本次范围，不再算结构升级；**innov 侧需新增 `/internal/*` 端点**时才升级 `human:李伟` |
| U4 | UI 改动面 | **A 放宽到「接线层 + 角标挂载点」**，见 §0.1 边界铁律（与 ENT 的「diff 为零」不同：本管线允许角标挂载，但禁止任何实现效果变化） |
| U5 | 写面端点 | **本次只做只读**。`alerts/{id}/read`、`monitor/subscriptions`、`push-records`、`carriers/{carrier_id}` 全部 **deferred** |
| U6 | 评审 / 就绪度 | **纳入**（**显式覆盖 ENT U8「不纳入」**） |
| U7 | 就绪度真源 | 已有 `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml`（**143 条**，验收单元 `DS-04-*`；D1 aligned 143；D3 full 9 / partial 122 / none 12；**D4 全 mock**）。本次不是重新登记指标，是「映射 → 只读镜像 → 评审层 → 三页挂载」 |
| U8 | 诚实性（不得改绿） | `D4=mock` → 所有统计数字**必挂 🧪**；`D2=provisional` → **必带「待核验」**；**禁止把任何一维提前翻绿** |
| U9 | catalog 过渡态 | `gkxlumen-metrics` 现**只有** `cfg_metric-ENT-seed.json`（无 INNOV seed）→ 走**过渡态只读镜像**（集中单文件 + 头注释真源路径与同步任务号），catalog 含 INNOV 后切换 |
| U10 | `views/innov` 隐藏页 | **不动 / 不删 / 不复用**（已核实：仅 `src/router/routes.ts:21-30` 定义、`showInMenu:false`、全仓无跳转引用、与三页零共用代码）。挂技术债红线 |
| U11 | git | **每叶停本地**：commit 可做、**严禁 push**；走查通过后由 `human:李伟` 人工推送 |
| U12 | pilot 顺序 | **先 M6 深圳**（地域锁死、Tab 与统计数字最少）跑通「真端点 + 评审角标」双链路 → M5 → M4 |
| **U13** | **innov 侧新增端点** | `human:李伟` **2026-10-28 批准**：允许在 `gkxlumen-innov` 新增 `/internal/*` 只读端点补齐 A0 §4.1 七项缺失能力。**纪律**：逐叶按需、不批量造；`@Inner(true)` + display 侧 `@NoToken` 配对；无源列一律空态 + `emptyReason`（= C3=①），禁止伪造数值。见契约 §4.6 |

## 0.1 边界铁律（本管线最高约束）

**可改**：

1. **接口契约**（路径 / 字段 / DTO；改一版 bump 一版，同步 `types/*.ts` 与 mock 种子，禁两处漂移）—— 契约真源 `SITUATION-IM-API-CONTRACT-01.md`。
2. 后端实现：`gkxlumen-display`（含 `RemoteInnovClient` 扩只读方法）、`gkxlumen-element`。
3. 前端**接线层**：`src/api/situation/**`、`src/types/**`、新增 `views/situation/{三页}/models/**` 装配层、`src/stores/**`（页级）。
4. **评审层**：`src/review/**`、`src/components/lineage/**`、`src/stores/review.ts`、readiness 只读镜像。
5. **角标挂载点**：tabs 中**单行插入** `<ReviewMetricBadges>` / `<MetricSpecHint>`。

**不可改**：`views/situation/**` 的视图结构、组件层级、布局、样式、`styles/*.css`、Arco 用法、**任何实现效果**。数值由 mock 演示值变为真实值、或增加「ⓘ / 🧪 / 待核验」标记，**不算效果变化**。

> **角标为何不算 UI 改动**（U4 的解释性定义，逐叶须满足全部三条）：① 挂点是既有数字节点旁的兄弟节点，**不改变布局流与尺寸**（不加换行、不改 padding/间距表）；② 评审模式关闭时 **DOM 零残留**；③ 不引入新颜色/新字号/新控件，复用 `src/components/lineage/*` 既有样式与 Arco 组件。三条任一不满足即视为效果改动，**该叶退回**。
>
> ✅ **`human:李伟` 2026-10-28 书面认可上述定义（勾选表 C1=①）** —— R0/R1/R2/R3 四叶照常执行，但每叶验收仍逐条核这三条。

## 0.2 已拍板（执行 agent 不必现场选型）

| 项 | 值 |
|---|---|
| 仓 / 分支 | `lumen-svc-platform` / `lumen-ui-science-pc` / `gkx-orchestration`，均 `origin/dev` |
| 库 | 只读 `demo_gkxlumenx_*`；**禁止写正式 `gkxlumenx_*`** |
| 调用链 | 前端 → `/display/**` → display →(Feign)→ element / innov → demo 库 |
| 数据/环境 | 走 U6 同款豁免：**本地联调 + 人工走查**（网关 `192.168.88.50` 不可达，ENT A0 已实测） |
| 废作清单 | 无（本管线新建） |
| 升级人 | `human:李伟` |
| 锁 | `lock_hours=24`（lease 过期同一监管人续领，不改设计） |

---

## 1. 段 / 叶表

| 段 | 仓 | 草案号 · 任务 ID | 叶 | 状态门 |
|----|----|---|---|---|
| A0 | `lumen-svc-platform`（只读核验）+ `gkx-orchestration` | WBS-05-19-01 · `SITUATION-IM-A0-L01` | 数据/环境/指标映射体检（**不写代码**） | 体检报告出=过；含 innov 端点清单 + metric_id 映射表 |
| R0 | `lumen-ui-science-pc` | WBS-05-19-02 · `SITUATION-IM-R0-L01` | 评审底座：`src/review/` + 组件升级 + readiness 只读镜像 | `type-check` 0 / build 通过 / 关闭评审 DOM 零泄漏 |
| C1–C5 | `lumen-svc-platform` | WBS-05-19-03～07 · `SITUATION-IM-C1..C5-L01` | **pilot · M6 深圳 5 端点**（carriers / indicator-systems / field-distribution / city-benchmark / operation-timeline） | 前序 A0/R0；同仓串行 |
| D1 | `lumen-ui-science-pc` | WBS-05-19-08 · `SITUATION-IM-D1-L01` | M6 前端装配接线（api + models + 页级 store + 空态） | C1–C5 ≥ integration |
| R1 | `lumen-ui-science-pc` | WBS-05-19-09 · `SITUATION-IM-R1-L01` | M6 角标挂载 | D1 ≥ integration |
| C6–C10 | `lumen-svc-platform` | WBS-05-19-10～14 · `SITUATION-IM-C6..C10-L01` | M5 湾区 5 端点 | pilot 验过 ≥ integration |
| D2 / R2 | `lumen-ui-science-pc` | WBS-05-19-15 · `SITUATION-IM-D2-L01` / WBS-05-19-16 · `SITUATION-IM-R2-L01` | M5 前端接线 / 角标 | C6–C10 ≥ integration |
| C11–C15 | `lumen-svc-platform` | WBS-05-19-17～21 · `SITUATION-IM-C11..C15-L01` | M4 全球 5 端点 | pilot 验过 ≥ integration |
| D3 / R3 | `lumen-ui-science-pc` | WBS-05-19-22 · `SITUATION-IM-D3-L01` / WBS-05-19-23 · `SITUATION-IM-R3-L01` | M4 前端接线 / 角标 | C11–C15 ≥ integration |
| E（豁免） | — | — | 不设 E0/E1，以 §4 人工走查清单收口（同 U6 豁免） | 全部 ≥ pending_test 后走查 |

**合计 23 叶**（A0 1 + R0 1 + C 15 + D 3 + R 3）。

> **同仓 Convoy**：`lumen-svc-platform` 与 `lumen-ui-science-pc` **各自同时只派 1 张 coding 单**（前后端可并行各一张）。一 REST 路径一叶，禁止合并成一厚包。

---

## 2. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:李伟`，`claim_type=coordinator_dispatch`，升 ready 后直接认领开工（授权句已生效）。
2. **已拍板不回问**：U1–U12 全部事项（链路 / 命名 / 粒度 / innov 启用 / 改动面 / 只读 / 评审 / 真源 / 不改绿 / 过渡态 / 隐藏页 / git / pilot 顺序）。
3. **QC / 甲方 🟡**：诚实降级（空态、`emptyReason`、缺口记录），不停工等纪要。
4. **结构歧义**（新表、改主键、新 ES 索引、**innov 侧需新增 `/internal/*` 端点**）：该叶 `blocked` + 升级 `human:李伟`；同段其它不依赖该点的叶继续。
   - ✅ **2026-10-28 `human:李伟` 已批准 innov 侧新增 `/internal/*`**（U13），逐叶按需、不批量造；纪律见 U13 与契约 §4.6。此后**不再因为「需 innov 新增端点」而 blocked**，但**新增表 / 改主键 / 新 ES 索引**仍须按本条升级。
5. **缺数据**：读空则空态；禁止无闸门写正式库；禁止用旧表冒充口径。
6. **git**：每叶停本地（commit 可做、**严禁 push**），走查通过后监管人人工推。
7. 每叶 handoff（`ponytail:` + cost 四字段）；`ready_to_sign→done` 可积压，不卡主链。
8. 单叶 cost >$10 暂停复盘，>$20 hard stop。
9. **卡住只允许**：真环境不通、正式库误写风险、结构升级项、cost 硬闸。

---

## 3. 依赖（联调闸门）

```text
A0 体检 ──┬──→ R0 评审底座（可与 C 段并行） ──→ R1/R2/R3 挂在各页 D 之后
          └──→ C1–C5 (M6) ──→ D1 (M6 FE) ──→ R1 (M6 角标)
                                 └── pilot 链路验过 ──→ C6–C10 (M5) ──→ D2 ──→ R2
                                                   └──→ C11–C15 (M4) ──→ D3 ──→ R3
R1/R2/R3 ≥ pending_test ──→ §4 人工走查（人工验收闸门：改动停本地等确认）
```

- 解锁条件 = 前序有 handoff 且 ≥ `integration` / `pending_test` + 契约已 bump。
- **pilot 闸门**：C1–C5 → D1 → R1 必须先跑通并走查一页，**确认「端点 → 装配 → 角标」链路成立后才放行 M5/M4 的 C 段**（避免 15 个端点按错误范式批量复制）。

---

## 4. 人工走查清单（代替 E1 · 期望未发生=红）

> 走查地址：本地 `pnpm dev`（**端口 3000**，见 `.env.development:3` + `vite.config.ts:37`）。
> 当前 `VITE_ENABLE_MOCK_AUTH=true` + `USE_MOCK=false` 组合**不挂 Bearer**，适配 display local permitAll，**不需要注假 token**。

| # | 检查项 | 期望（未发生=红） | 允许的空态 |
|---|--------|-------------------|-----------|
| 1 | M6 深圳 · 四 Tab | 载体/指标/领域/城市对标出真数，或与 A0 体检报告的库级计数逐位吻合 | 算法类占位写明口径，不是白屏 |
| 2 | 筛选联动 | 改行政区 / 领域 / 时间后，**KPI 与图同步变化**（`regionPaths` 真的传下去；注意别传成 `regionKey`） | — |
| 3 | 诚实空态 | 无数据块显示**可见空态文案 + `emptyReason`**，不白屏、不报错弹窗、不静默空数组 | 空态本身为期望 |
| 4 | 逐块降级 | 单独断掉 innov / element，只有对应区块空且带理由，**其余区块照常显示** | — |
| 5 | 评审角标 | 每个统计数字有 ⓘ 或 D1 missing 红问号；`D4=mock` 出 🧪、`D2=provisional` 带「待核验」；**无一维被提前翻绿** | 未知指标的「红问号」为期望 |
| 6 | 评审开关 | 关闭评审模式后 DOM **零泄漏**（无 `metric_id` / `Q0xx` / `GAP-*` 字样） | — |
| 7 | 改动面 | `views/situation/**` diff 逐项落在 §0.1 允许五类；`styles/*.css` **零 diff** | — |
| 8 | 三绿 + console | `type-check` 0 / `pnpm build` 通过 / lint 0；浏览器 console 无 `pageerror` | — |
| 9 | 链路合规 | 全仓**未 import** `@/api/innov`；三页未出现任何 `/innov/v1` 直连请求 | — |

P1 不挡闭环：报告下载、导出、写面（订阅/已读/推送中心）。

---

## 5. 已知缺口（交付时随 handoff 披露，不在本管线关闭）

1. **Open Item**：M4 `realtime` 的 D2 轮询语义（草案首版 30s）是否本次实现 —— **待 pilot 结果定**，不定不实现。
2. 算法侧（指标体系 / SWOT / 城市对标四维 / 缺口斜率外推）若 `/internal/*` 未就位，端点降级为空态 + `emptyReason`，**不得用 demo 数值返回**。
3. `metric-readiness-matrix-INNOV.yaml` 为 `model_status: provisional` 且 D4 全 mock；本次只读消费，不改其判定。
4. `gkxlumen-metrics` 无 INNOV seed → 走 U9 过渡态镜像，catalog 到位后需回头切换。
5. 天地图 key 与内网瓦片可达性（R1）未确认，地图类区块可能受限。
6. `views/innov` + `@/api/innov` 违规存量（前端直连 `/innov/**`）未迁移，另开单。
7. 网关 `192.168.88.50` 不可达（ENT A0 实测），本管线一律本地联调，不据此写「已上线」。
8. `FE-TS-06A` 缺同名 handoff 文件（模块目录无 `FE-TS-06A.md`），本管线不补建该 handoff，只在 WBS 与本报告如实标明。

---

## 6. 文件索引

| 件 | 路径 |
|---|---|
| 本文件（总控） | `agent-handoffs/科技发展态势-TS/SITUATION-IM-长任务总控.md` |
| 厚包 / 总派单 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-总派单.md` |
| 契约真源 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-API-CONTRACT-01.md` |
| 前置条件与未决项 | `agent-handoffs/科技发展态势-TS/SITUATION-IM-前置条件与未决项.md` |
| **开工前勾选表（C1–C10）** | `agent-handoffs/科技发展态势-TS/SITUATION-IM-开工前勾选表.md` |
| 跑任务提示词 | `agent-delivery/prompts/SITUATION-IM-三个创新监测页面整体打通-跑任务提示词.md` |
| 就绪度真源 | `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml` |
| 决策纪要 | `工程过程/04-系统集成/05-展示系统集成/纪要/2026-10-28-SITUATION-IM-边界与裁定.md` |
| WBS 挂接 | `工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.4（WBS-05-19-01～23） |
| 逐叶 handoff | `agent-handoffs/科技发展态势-IM/{task-id}.md` |
