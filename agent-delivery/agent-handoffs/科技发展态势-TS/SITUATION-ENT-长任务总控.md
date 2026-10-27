# SITUATION-ENT · 长任务总控（科技全域态势 · 企业维度数据跑通）

> **日期**：2026-10-27  
> **授权**：`human:李伟`（本管线监管人；**授权句已生效（2026-10-27）：「后续认领不必再问」**）  
> **目标**：科技全域态势页（`lumen-ui-science-pc` views/situation）企业维度数据在 `USE_MOCK=false` 下全链路真实闭环：前端 → 网关 → `gkxlumen-display` → `gkxlumen-element` → demo 库 DWD/ADS；**UI 与实现效果零改动**（契约可改）。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)（本文件与规约冲突处以本文件已拍板项为准；规约红线不可豁免）。

---

## 0. 裁定记录（2026-10-27 授权人拍板）

| # | 裁定项 | 结论 |
|---|--------|------|
| U1 | influence 端点 | **A 纳入一期**（补齐 `/v1/situation/influence`） |
| U2 | 企业影响力数据源 | **A 用 `ads.enterprise_score` 现成数据**；口径与正式指标（`M_INNOV_ENTERPRISE_INFLUENCE`，D4=mock 算法未上线）的差异记缺口，不提前改绿 |
| U3 | 对象级企业点位 | **A 一期实现**（map objectPoints 从 enterprise_score 坐标出，替换现空态+emptyReason） |
| U4 | USE_MOCK 切换 | **A 全局 false**；timeline/events/cluster/compare 四端点打真实 404 → 允许空态（写进走查清单） |
| U5 | 契约基准 | **lumen 现实现为真源**（`types/situation.ts` + `defineApi` 双轨），不对齐 API-TS-M1 草案 |
| U6 | 验收方式 | **仅本地联调 + 人工走查**（授权人裁定：不设段 E，E1 以 §4 人工走查清单代替；这是对规约 §11.2「只认 K8s 已发布」的显式豁免，仅本管线有效） |
| U7 | 走查清单 | 见本文件 §4 草案（5 条，授权人可改行内期望） |
| U8 | 就绪度角标 | **不纳入本管线**；D9 角标/评审层另派单 |

## 0.1 边界铁律（本管线最高约束）

- **可改**：接口契约（路径/字段/DTO，改一版 bump 一版，同步 `types/situation.ts` + mock 种子）；`gkxlumen-display`/`gkxlumen-element` 实现；前端 `src/api/`、`src/mock/`、`src/types/`、`models/` 数据装配层。
- **不可改**：`views/situation/**` 视图结构与组件、`styles/demo-situation.css`、Arco 用法 —— **验收时 diff 必须为零**。数值从 mock 演示值变为真实值（如企业总数 92,000 → 189,115）**不算**效果变化。
- 数据只读 `demo_gkxlumenx_*`；**禁止写正式 `gkxlumenx_*`**；读空出诚实空态，禁止造假数。

---

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| A0 | `lumen-svc-platform`（只读核验） | — | 数据/环境体检叶（element 六端点 curl + 库行数核对 + 网关/token 核验） | 产出体检报告即过，不写代码 |
| C1 | `lumen-svc-platform` | `origin/dev` | element 企业端点核验补强（含 U3 object-points 新端点） | 前序 A0 有 handoff |
| C2 | `lumen-svc-platform` | `origin/dev` | display `/v1/situation/map`、`/overview` 联调（objectPoints 接线 + Feign 降级路径） | C1 ≥ integration |
| C3 | `lumen-svc-platform` | `origin/dev` | `/v1/situation/influence` 契约冻结 + 实现（一 REST 路径一叶） | C2 ≥ integration |
| D1 | `lumen-ui-science-pc` | `origin/dev` | 前端契约适配 + `USE_MOCK=false` 切换叶（api/types/mock/数据装配，视图零 diff） | C2/C3 ≥ integration |
| E（豁免） | — | — | 不设 E0/E1；以 §4 人工走查清单收口（U6 裁定） | D1 ≥ pending_test 后走查 |

厚包：`SITUATION-ENT-总派单.md` · 契约真源：`SITUATION-ENT-API-CONTRACT-01.md` · 走查清单：本文件 §4  
挂接：`工程过程/04-系统集成/05-展示系统集成/WBS.md` §4.3（WBS-05-18-01～05，DS-01 科技全域态势）

> **同仓 Convoy**：`lumen-svc-platform` 与 `lumen-ui-science-pc` 各自同时只派 **1 张** coding 单。

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:李伟`，`claim_type=coordinator_dispatch`，升 ready 后直接认领开工。
2. **已拍板不回问**：仓、分支、数据源（U2）、点位（U3）、切换策略（U4）、契约基准（U5）、验收方式（U6）。
3. **QC / 甲方 🟡**：诚实降级（空值、emptyReason、缺口记录），不停工等纪要。
4. **结构歧义**（新表、改主键、新 ES 索引）：该叶 `blocked` + 升级 `human:李伟`（总控可改升级人）；同段其它不依赖该点的叶继续。
5. **缺数据**：读空则空态；禁止无闸门写正式库；禁止用旧表冒充口径。
6. **git 策略**（⚠️ 待授权人签署，二选一）：
   - **默认（仓级人工验收闸门）**：每叶完工 **停在本地工作区**（commit 可做、**严禁 push**），全部走查通过后由监管人人工推送；
   - **或明示授权「完工即推」**：按长任务规约 push `origin/dev`，commit `[agent:<role>]`，禁止 force。
   未签署前一律按默认执行。
7. 每叶 handoff（`ponytail:` + cost 四字段）；`ready_to_sign→done` 可积压，不卡主链。
8. 单叶 cost >$10 暂停复盘，>$20 hard stop。

锁：`lock_hours=24`。lease 过期同一监管人续领，不改设计。

---

## 2. 依赖（联调闸门，见规约 §6.2）

```text
A0 体检 ──→ C1 element（object-points）──→ C2 display map/overview ──→ C3 influence ──→ D1 前端切换
                                          └────────────────────────→ D1（map 部分可先行，influence 到 C3 ≥ integration）
D1 ≥ pending_test ──→ §4 人工走查（人工验收闸门：改动停本地等确认）
```

- 解锁条件 = 前序有 handoff 且 ≥ `integration`/`pending_test` + 契约已交（读 `SITUATION-ENT-API-CONTRACT-01.md`）。
- 废作施工（不要派、不要当依赖）：无（本管线为新建，无旧 task-id）。

## 3. 开工顺序

1. A0：体检（网关 192.168.88.50:9999 可达性、element 六端点 curl、`{dwd}.enterprise_base`/`{ads}.enterprise_score`/两张 dist 表行数、真 token 获取方式核验）。
2. C1 → C2 → C3（`lumen-svc-platform` 串行，一 REST 路径一叶）。
3. D1：`lumen-ui-science-pc` 契约适配 + `.env` 切 `VITE_APP_USE_MOCK=false`；三绿（type-check/自检/build）；`views/situation/**` diff 为零自检。
4. §4 人工走查（监管人执行）；红项按缺口/修单处理，仍停本地。

卡住只允许：真环境不通、正式库误写风险、结构升级项、cost 硬闸。

---

## 4. 人工走查清单（代替 E1 · 期望未发生=红）

> 走查地址：本地 `pnpm dev`（U6 豁免：不要求 K8s 已发布）。**期望未发生必红**；空态只有本行写明才算过。红项处理参照规约 §11.4 分类思路（本地走查以缺口记录 + 修单收口，不走 CI）。

| # | 检查项 | 期望（未发生=红） | 允许的空态 |
|---|--------|-------------------|-----------|
| 1 | 地图 · 要素 chips | 企业 chip 数 = **189,115**（读库实测口径）；其余 10 要素 count=0 | 其余要素 0 值为**期望**，非空态 |
| 2 | 地图 · 对象级点位 | 企业点位（华为等高分企业坐标）可见、可点开详情（U3）；`objectPointsEmptyReason` 不再出现 | 点位坐标缺失的企业不出点，不冒充 |
| 3 | 总览 · KPI 五值 + 趋势 + 分布 | 企业总数/高新/专精特新/瞪羚/独角兽 = 库内真实值；新增趋势、领域/类型分布出真实曲线/占比 | — |
| 4 | 影响力 Tab · 企业榜 | 榜单来自 `/v1/situation/influence` 真实数据（`enterprise_score` 口径，记缺口：正式算法未上线）；过滤重算语义与 demo 一致 | — |
| 5 | 其余四端点 | timeline/events/cluster/compare 打真实 404 时页面**诚实空态、无报错弹窗、不白屏**（U4 裁定） | 四端点空态为**期望** |

P1 不挡闭环：报告下载、导出、非企业要素的任何数据补充。

---

## 5. 已知缺口（交付时随 handoff 披露，不在本管线关闭）

1. influence 用 `enterprise_score` 占位，正式指标 `M_INNOV_ENTERPRISE_INFLUENCE` D4=mock（算法服务未上线），矩阵不翻转。
2. ENT 域 96 条 D4 全 mock；就绪度角标/评审层未建（U8 另派单）。
3. 4 张企业汇总 ADS 表（region_summary 等）0 行未产出，区域/趋势靠 `enterprise_base` 实时聚合。
4. ADS `status=draft`，现行实线跑 Demo 库，D12 禁产品站调 demo-*。
5. `lumen-etl-es-py` 本地不可访问，ES 侧链路未核实。
