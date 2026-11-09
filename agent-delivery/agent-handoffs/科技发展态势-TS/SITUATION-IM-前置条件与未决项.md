# SITUATION-IM · 前置条件与未决项（开工前置一张表）

> 用途：长任务**开工前**由 `human:李伟` 一次性过目；A0 叶据此核验，C/D/R 段据此判断能否 unlocking。
> 日期：2026-10-28 · 上位：[`SITUATION-IM-长任务总控.md`](./SITUATION-IM-长任务总控.md)
> 口径：**Part A 已具备** = 可直接用；**Part B 缺口** = 开工前必须补，否则该叶 `blocked`；**Part C 未决** = 必须监管人拍板，agent 不得自行选择。

---

## Part A · 已具备（证据确凿，不用再问）

| # | 条件 | 现状 / 证据 |
|---|---|---|
| A1 | 三页前端已复刻到位 | `FE-TS-04A` / `05A` / `06A` 均 integration；`views/situation/{global-innovation,bay-innovation,shenzhen-innovation}/index.vue` 齐备（126 / 163 / 112 行）。⚠️ `FE-TS-06A` 模块目录**无同名 handoff 文件** |
| A2 | 后端骨架可跑 | `gkxlumen-display` 7099 local permitAll、`gkxlumen-element` 7082，ENT 管线已跑通（含 Feign 降级、`@NoToken`/`@Inner` 配对） |
| A3 | 本地联调环境 | `.env.development`：`VITE_APP_API_URL=http://127.0.0.1:7099`（:10）、`VITE_APP_USE_MOCK=false`（:16）、`VITE_ENABLE_MOCK_AUTH=true`（:17，不挂 Bearer，**走查无需假 token**） |
| A4 | 前端端口 | **3000**（`.env.development:3` + `vite.config.ts:37`） |
| A5 | 企业侧数据源 | `dwd.enterprise_base` 189,115、`ads.enterprise_score` 189,115、`enterprise_domain_dist` 30、`enterprise_type_dist` 35；`ads.tech_power`（transfer/cooperation）可用（`SituationController.java:357-359`） |
| A6 | 就绪度真源 | `agent-delivery/metrics/registry/metric-readiness-matrix-INNOV.yaml`（143 条，验收单元 `DS-04-*`，D1 aligned 143 / D3 full 9·partial 122·none 12 / D4 全 mock） |
| A7 | 评审参考实现 | `lumen-ui-topic/src/review/`（`feature.ts` + `index.ts` + `README.md`）可作迁移模板 |
| A8 | 前端已有评审底座（部分） | `src/components/lineage/MetricSpecHint.vue`、`MockBadge.vue` 已存在；三页零星挂载（`InnovationRealtime.vue` 6 处、`tech-trend-components.ts` 7 处、`IndicatorTab.vue` 2 处） |
| A9 | 契约草案 | `API-TS-M4/M5/M6.md`（前缀 `global-innovation` / `bay-innovation` / `shenzhen-innovation`）—— 本次命名沿用它们 |
| A10 | WBS 挂点 | `WBS-05-19`（创新监测三页，监管人孔东）已有行，可挂子任务 05-19-01～23 |
| A11 | git 纪律 | 仓级「人工验收闸门」已生效：默认只 commit 不 push |

---

## Part B · 开工前缺口（不补全则该叶 `blocked`）

| # | 缺口 | 为什么必须先要有 | 谁补 / 怎么补 | 阻塞哪些叶 |
|---|---|---|---|---|
| B1 | **`gkxlumen-innov` 端点清单未知**（`RemoteInnovClient` 只有 `health()`，`:24`） | U3 已启用 innov，但不知道能调什么、返回什么、有无行数 | **A0 首项**：curl 探活 + 拉端点清单 + 三张表（`dwm_org_achievement_year` / `ads_node_influence` / `dim_tech_domain`）行数 | 全部 C 段 |
| B2 | **innov 侧是否需新增 `/internal/*` 端点**未知 | 需新增 = 结构升级项 → `blocked` + 升级 `human:李伟` | A0 判定后升级 | C6–C10、C11–C15（重 innov 的块） |
| B3 | **算法侧 `/internal/*` 是否就位**（指标体系 / SWOT / 城市对标四维 / 缺口斜率外推） | 没算法就不能伪造；只能空态 + `emptyReason` | A0 核验 + 若未就位按口径降级（需 C3 拍板的占位口径） | C5 / C7 / C8 / C9 / C12 / C14 |
| B4 | **无 `SITUATION-IM-data-gap-catalog.yaml`** | AGENTS.md 要求 `pending_hint` 缺口长文案**禁前端硬编码**，必须有真源文件。现存同类模式在 `agent-handoffs/产品整体定义/*/{模块}-data-gap-catalog.yaml`（14 份），**科技发展态势-TS 模块一份都没有** | R0 叶新建 `科技发展态势-TS/SITUATION-IM-data-gap-catalog.yaml`，内容从 INNOV 矩阵的 `d2_gap` / `d3_gap` / `d4_note` 提取 | R0、R1–R3 |
| B5 | **registry 任务未建**（本会话无 task MCP 工具） | 规约 §3-1：无 ID 不许改业务仓代码 | coordinator 走总控 §0.3 路径 2，**每份 handoff 与 commit 写明「无 MCP、经监管人当场指示」** | 全部叶（动手前） |
| B6 | **契约会签归口未定**：本次的 `SITUATION-IM-API-CONTRACT-01.md` 与 `BE-TS-CONTRACT-02`（WBS-05-15，声称「批 3 前冻 M4/M5/M6」）是什么关系 | 两份都在声称 M4/M5/M6 的路径，会出现双真源 | 见 C4，**必须 `human:李伟` 定** | C 段全部（命名合法性） |
| B7 | **天地图内网瓦片可达性未确认**（R1） | 三页都有地图区块，不可达则该块受限 | A0 ⑥；不可达则按 C9 裁定降级 | C1 / C6 / C11（地图落点区块） |
| B8 | **`views/innov` 违规存量未登记为正式技术债单** | U10 只说不动，但没登记到任何跟踪件 | 本次 handoff 挂一笔 + WBS 尾注；迁移另开单 | 无（不阻塞） |
| B9 | **`FE-TS-06A` 缺 handoff 文件** | 下游核对 M6 页面范围时无真源 | 本次**不补建**（历史件），在 WBS 与本文件如实标明 | 无（不阻塞，但 D1 范围需以页面实物为准） |

---

## Part C · 长任务不确定条件（必须 `human:李伟` 拍板，agent 不得自决）

> 已拍板项见总控 §0（U1–U12），此处**只列开工前仍未定或需书面确认的**。
> **勾选落在 [`SITUATION-IM-开工前勾选表.md`](./SITUATION-IM-开工前勾选表.md)**（每项填一个数字即可，留空=按默认）。

> ✅ **2026-10-28 `human:李伟` 勾选完毕**（结果见勾选表）：明示 C1=①（角标不算 UI 改动）· C2=①（授权 registry 直接改 + 注明）· C4=①（IM 契约作本期施工真源）· C10=李伟（走查签收人）；**C3 / C5 / C6 / C7 / C8 / C9 按默认①**。**本表现在是留痕件，不再是阻塞项** —— coordinator 可直接建 A0 单开工。

| # | 未决项 | 选项 | 建议 |
|---|---|---|---|
| C1 | **「评审角标」是否算 UI/实现效果改动**（U4 的解释性定义） | ① 不算（满足总控 §0.1 三条：不改布局流 / 关闭后 DOM 零残留 / 不引新样式）② 算 → R 段整体延后二期，主线仍做 | 建议 ①；但需你书面认可这三条判定标准，否则 R 段每叶都会被质疑 |
| C2 | **registry 路径授权**（§0.3 路径 2） | ① 授权「无 MCP 时直接改 `task-registry.yaml`，并在 handoff/commit 写明」② 另想办法 | 建议 ①，与前序 ENT 管线一致 |
| C3 | **算法未就位时的占位口径** | ① 空态 + `emptyReason` + 口径注释（推荐）② 暂缓该端点 ③ 由前端出 demo 值 | 建议 ①（诚实性红线） |
| C4 | **契约双真源归口** | ① `SITUATION-IM-API-CONTRACT-01.md` 作本期施工真源，会签时回灌 `BE-TS-CONTRACT-02` ② 直接改oadmap ordering | 建议 ①，并在 `BE-TS-CONTRACT-02` 批 3 会签前把偏离表送 `human:李伟` 确认 |
| C5 | **Open Item：M4 `realtime` 的 D2 轮询（首版 30s）本次做否** | ① pilot 后定 ② 本次不做，只出静态快照 ③ 本次做 | 建议 ①：pilot 跑完看链路能力再定，避免第一叶就背上轮询复杂度 |
| C6 | **TODO ②：是否顺手改 `.env`**（加 `.env.*.local` 不入库、主干改回网关地址） | ① 改 ② 不改，挂遗留 | 建议 ①（10 分钟的事，但会让 clone 的人不再静默白屏） |
| C7 | **pilot 若 innov 侧全空**（A0 结果悲观） | ① 接受「全空态交付」，把三页做成诚实空态样 ② 暂停管线升级 ③ 回到 demo 演示态 | 建议 ①：这本身就是本次要解决的「诚实性」问题，但需你先认可「空态也算交付」 |
| C8 | **同仓 Convoy 的例外**：是否允许 R0 与 C1 并行（两仓各一张） | ① 允许（推荐）② 严格串行 | 建议 ①，R0 不阻塞主链 |
| C9 | **天地图不可达时的地图降级形态** | ① 空地图 + 文案 ② 静态底图 ③ 保留 demo 坐标但不发请求 | 建议 ①；不可选 ③（会变成 fixture 填数） |
| C10 | **走查谁执行**：U6 豁免后的人工走查清单由谁签 | ① `human:李伟` ② 孔东（FE 监管）③ 两者都要 | 建议 ①（与总控授权人一致），FE 视角可让孔东旁站 |

---

## Part D · 建议的开工顺序

```text
0. human:李伟 勾 C1–C10（半页纸，一次过）
1. coordinator 建单 A0（registry 路径按 C2）
2. A0 出体检报告 → 若 B2/B3 命中，先升级 human:李伟 决策，再放行 C 段
3. R0 与 C1 并行（C8）
4. C1–C5 → D1 → R1：pilot 一页走查通过后才放 M5 / M4（§3 pilot 闸门）
5. M5 → M4，最后一页走查完 → 停本地，等人工推送
```
