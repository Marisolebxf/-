# ENT METRIC-OPEN · ready_to_sign 签收检查纪要

> **签收人**：human:淮政玮  
> **日期**：2026-08-03  
> **范围**：企业维 6 条 `*-METRIC-OPEN-L01`（status=ready_to_sign）  
> **依据**：`产品定义评审规程.md` §1.4.2 方案 B；§3.2 METRIC-OPEN 执行模型；`ENT-SEMANTIC-DUAL-SIGNOFF-方案B-派单说明.md`  
> **结论**：**全部不签收 → `needs-revision`**；不新建独立 FIX leaf（缺签属原任务未闭合）

---

## 1. 签收闸门（本次使用）

| # | 闸门 | 通过标准 |
|---|------|----------|
| G1 | 三件套落盘 | 核对记录 + data-gap-catalog + handoff（分析模块另须 cfg_metric 或书面 N/A） |
| G2 | 算法共签 | 唐绍祖 §6 栏 ✅（或算法 N/A + 依据） |
| G3 | 口径主责 | **王惠** §6 栏 ✅（方案 B 铁律；缺一不可） |
| G4 | 开放项纪律 | 🟡/❌ 不伪闭合；客户决策清单已挂 |
| G5 | cost | handoff 四字段齐全（文档任务可标 N/A 有据） |

> 已 done 的 COMPARE/EVAL/RISK 按方案 B 派单说明 **不回溯**；本批自 SEARCH/RECRUIT 交接及 KEYPANO 起均须双签。

---

## 2. 逐条结论

| Task ID | 产物 | 唐绍祖 | 王惠 | 其他缺口 | 裁定 |
|---------|------|--------|------|----------|------|
| `ENT-MOD-SEARCH-METRIC-OPEN-L01` | ✅ 三件套齐 | ✅ 07-22 | ❌ 无栏/无签 | note 已写「待王惠复核」；监管已改王惠 | **打回** |
| `ENT-MOD-RECRUIT-METRIC-OPEN-L01` | ✅ 三件套齐 | ✅「待确认」 | ❌ 无签 | 算法收尾有 §6 共签说明，口径侧仍缺 | **打回** |
| `ENT-MOD-KEYPANO-METRIC-OPEN-L01` | ✅ 核对+catalog+handoff | ✅ 07-29 | ❌ 无签 | cfg_metric  defer 下游，须在核对记录写清 N/A/ defer 依据；`supervised_by` 未落王惠 | **打回** |
| `ENT-MOD-STAR-METRIC-OPEN-L01` | ✅ 核对+catalog+handoff | ✅ 07-29 | ❌ 无签 | 方案 B 新建即应双签；仅唐绍祖 | **打回** |
| `ENT-MOD-SHENZHEN-METRIC-OPEN-L01` | ✅ 核对+catalog+handoff | ⏳ **待签署** | ❌ 无签 | cfg_metric 未列入产出；会签表未闭合 | **打回** |
| `ENT-MOD-OPS-METRIC-OPEN-L01` | ✅ CMS 适配三件套 | 🟡 待签 | 🟡 待签 | cost 实际 token 未填；双签栏均待签 | **打回** |

**本批签收数：0 / 6**

---

## 3. 返工要求（闭合后方可再进 ready_to_sign）

### 3.1 六条共性（方案 B）

1. 核对记录 §6 改为双签表：
   - `口径主责 | human:王惠 | 日期 | ✅`
   - `算法共签 | human:唐绍祖 | 日期 | ✅`（或「算法 N/A + 依据」）
2. registry：`supervised_by: human:王惠`；`owner_semantic` / `cosigner_algorithm` 与方案 B 派单说明一致
3. handoff 补一句：「王惠口径会签 + 唐绍祖算法共签已闭合」

### 3.2 分条补强

| Task | 额外必补 |
|------|----------|
| SEARCH | 王惠复核口径/开放项（Q033–Q037）后签字即可；产物本身可沿用 |
| RECRUIT | 王惠签；唐绍祖「待确认」改为明确 ✅ |
| KEYPANO | 王惠签；cfg_metric 更新或书面 defer 路径（ALGO-METRIC-ALIGN）写入核对记录 |
| STAR | 王惠签；确认 CMS 侧指标归属 OPS 的 N/A 依据仍成立 |
| SHENZHEN | **唐绍祖先签**；王惠签；补 cfg_metric 相关条目或 N/A 依据 |
| OPS | 王惠 + 唐绍祖双签；补 cost 四字段（可标文档任务 N/A） |

### 3.3 不建独立 FIX leaf 的理由

- 缺口主因是 **会签未闭合**，不是新增功能范围
- 打回原 leaf → `needs-revision` → 补签 → 再走 integration/ready_to_sign 即可
- 若补签时发现实质口径错误需重写核对记录，仍在原 leaf 返工；仅当出现「需另开工程对齐」时再由 coordinator 建 `*-FIX-*` / `*-ALGO-METRIC-ALIGN-*`

---

## 4. 对下游影响

| 依赖方 | 影响 |
|--------|------|
| `*-PDR-G1-RECLOSE` / 门 1 完整闭合 | 继续阻塞至对应 METRIC-OPEN = done |
| `DG-ENT-SEARCH` 附条件「METRIC-OPEN → done」 | **未闭合**；SEARCH 须王惠补签后由淮政玮再签收 |
| V1 / UX 并行 | **不阻塞**（规程 §3.2） |

---

## 5. 签字

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| PM / 签收 | 淮政玮 | **6 条全部打回 needs-revision；0 签收** | 2026-08-03 |

---

## 6. 排除签名 · 实质工作结果复核（2026-08-03 追加）

> **范围**：只评 §3.2 交付物质量（核对记录 / catalog / cfg_metric / 开放项纪律 / 不伪闭合），**不计**王惠/唐绍祖双签。

### 6.1 闸门（实质）

| # | 闸门 | 标准 |
|---|------|------|
| S1 | 核对记录结构 | 适用性 #4/#5、算法口径、贴源矩阵、开放项、PDR-05/06 |
| S2 | data-gap-catalog | 缺口指标有 `pending_hint`（≥80 字达数字段级），可作 UI 文案真源 |
| S3 | cfg_metric | 分析模块相关 metric 落种子，或书面 N/A / defer 有路径 |
| S4 | 开放项纪律 | 🟡/❌ 不伪闭合；Q/GAP 挂客户决策清单且 **语义不错挂** |
| S5 | 范围边界 | 不写算法实现代码；CMS vs 分析边界说清 |

### 6.2 逐条实质结论

| Task | 实质裁定 | 要点 |
|------|----------|------|
| **RECRUIT** | ✅ **满足** | 三件套齐；cfg_metric 5 指标已更新且标 semantic_revision；Q015/GAP-01～05 不伪闭合；pending_hint 达标 |
| **SHENZHEN** | ✅ **满足**（诚实部分闭合） | 3 统计型可闭 + 4 开放有据；catalog 7 条齐全；商业力 metric_id 缺口如实 ❌；不伪闭合 Q014/Q016 |
| **OPS** | ✅ **满足**（框架适配合格） | CMS 写侧 N/A 有据；15 能力 × 基础设施矩阵完整；catalog 按 capability 适配；Q-OPS/Q041/048/049/050 已挂 |
| **SEARCH** | ⚠️ **基本满足，有实质瑕疵** | 核对+catalog+handoff 齐；不伪闭合 Q033～；**Q037 错挂**（决策清单=空态推荐≤30，核对/catalog 写成「明星企业定义」——后者更近 Q041/Q048）；§3 贴源矩阵仅 5 行 vs catalog 9 条；「12 metric」表述与 TRACE `metrics_required:3` / catalog 不一致 |
| **KEYPANO** | ⚠️ **核对强，种子弱** | 8 指标口径/嵌套地域/不造算法 质量高；开放项诚实；**cfg_metric 无任何 `M_ENT_KEYPANO_*`**（handoff 写 defer ALGO-ALIGN，但 §3.2 / 同类 DoD 要求种子更新或书面 N/A——defer 可接受须在核对记录显式登记 defer 任务 ID） |
| **STAR** | ⚠️ **基本满足，有实质瑕疵** | CMS/数据边界清晰；catalog 5 条数据侧齐；**cfg_metric 无 `M_ENT_STAR_*`**；**同 SEARCH 的 Q037 错挂**（明星定义应挂 Q041/Q048，非空态推荐 Q037） |

### 6.3 实质合格汇总（排除签名）

| 裁定 | 条数 | Task |
|------|------|------|
| ✅ 实质可过 | 3 | RECRUIT、SHENZHEN、OPS |
| ⚠️ 实质有瑕需返工 | 3 | SEARCH（Q037 错挂 + 矩阵不全）、KEYPANO（cfg_metric）、STAR（cfg_metric + Q037） |
| ❌ 实质不合格 | 0 | — |

### 6.4 相对「仅补签即可」的修正

此前打回以双签为主。实质复核后：

- **RECRUIT / SHENZHEN / OPS**：补双签后即可再提签收（SHENZHEN 另须唐绍祖完成算法共签栏；实质内容本次判过）。
- **SEARCH / STAR**：补签前须 **改正 Q037 引用**（拆清「空态推荐≤30」vs「明星认定口径」），并补齐 SEARCH §3 矩阵与 catalog 对齐。
- **KEYPANO**：补签前须 **写入 cfg_metric 8 条** 或在核对记录写明 `defer → {task-id}` + N/A 依据。

### 6.5 签字（实质复核）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| PM | 淮政玮 | 排除签名后：**3 过 / 3 有瑕 / 0 不合格** | 2026-08-03 |

---

## 7. 全量 METRIC-OPEN 盘点与催促清单（2026-08-03）

> registry 内 `*METRIC-OPEN*` 真 leaf **9 条**（另 1 条 `ENT-MOD-EVAL-READINESS-UI-L01` 为 FE 消费 METRIC-OPEN，非定义轨本身）。

### 7.1 总览

| 状态 | 条数 | ID |
|------|------|-----|
| `done` | 3 | COMPARE / EVAL / RISK（方案 B 前关单，不回溯） |
| `needs-revision` | 6 | SEARCH / RECRUIT / KEYPANO / STAR / SHENZHEN / OPS |
| **缺 leaf** | ≥1 | **E-32 OVERVIEW 无 METRIC-OPEN**（UI 已挂未注册指标） |

### 7.2 淮政玮催促清单（按人）

#### A. 王惠（口径主责 · 最高优先级）

| # | 催什么 | 关联 | 验收信号 |
|---|--------|------|----------|
| A1 | 对 RECRUIT / OPS（实质已过）做口径会签 | 两任务 `needs-revision` | 核对记录 §6 王惠 ✅ |
| A2 | 对 SEARCH / STAR / KEYPANO 会签前先看实质返工是否完成 | 见 B | 实质修完后再签 |
| A3 | **正式化未入种子指标**（readiness L02 已点名） | KEYPANO 8、STAR 若干、E-32 `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` / `M_ENT_RESEARCHER_COUNT` 等 | `cfg_metric-ENT-seed` 有条目或书面拒登理由 |
| A4 | SHENZHEN 口径会签（唐绍祖先签后） | SHENZHEN | §6 双签齐 |

#### B. 唐绍祖（算法共签 / 执行返工）

| # | 催什么 | 关联 | 验收信号 |
|---|--------|------|----------|
| B1 | **SHENZHEN**：会签栏仍 ⏳ → 签完 | `ENT-MOD-SHENZHEN-METRIC-OPEN-L01` | §6 唐绍祖 ✅ |
| B2 | **SEARCH**：改 Q037 错挂（空态≤30 vs 明星定义→Q041/Q048）；§3 矩阵对齐 catalog | SEARCH | note 三项瑕疵关闭 |
| B3 | **STAR**：同 Q037 错挂 + 落 `M_ENT_STAR_*` 种子或 N/A | STAR | cfg 或 defer 有据 |
| B4 | **KEYPANO**：落 `M_ENT_KEYPANO_*`×8 或核对记录写 `defer→task-id` | KEYPANO | seed / defer |
| B5 | **RECRUIT**：「待确认」改明确 ✅ | RECRUIT | §6 明确签署 |
| B6 | **OPS**：双签 + cost 四字段 | OPS | handoff cost 齐 |

#### C. coordinator / 编排（建单缺口）

| # | 催什么 | 理由 | 建议动作 |
|---|--------|------|----------|
| C1 | **新建 `ENT-MOD-OVERVIEW-E32-METRIC-OPEN-L01`** | E-32 V1 已 done、页面 ⓘ 显示「覆盖未来产业数」未入指标库；无 METRIC-OPEN leaf；阻塞门1完整闭合语义 | PACK 已隐含在 E-31 四件套；按 §9.1.1 补 METRIC-OPEN，`supervised_by: 王惠` |
| C2 | 确认 PROFILE / 非企业模块是否需 METRIC-OPEN | 方案 B 全模块适用；PROFILE 无独立 METRIC-OPEN | 书面 N/A（消费 SEARCH/EVAL）或补 leaf |
| C3 | SYS-COMPARE-WORKSPACE-METRIC-OPEN 仅建议稿 | 未入 registry | 不催执行；等 PACK 立项 |

#### D. 淮政玮本人（签收闸）

| # | 动作 | 前置 |
|---|------|------|
| D1 | RECRUIT / SHENZHEN / OPS 再提 `ready_to_sign` 后签收 → `done` | A+B 双签齐 |
| D2 | SEARCH / KEYPANO / STAR 实质修完 + 双签后再签收 | B2–B4 + A |
| D3 | `DG-ENT-SEARCH` 附条件「METRIC-OPEN→done」仍未勾 | SEARCH done 后勾选纪要 |

### 7.3 本周最短催促话术（可直接转发）

**→ 王惠**  
> 6 条 METRIC-OPEN 在 `needs-revision`。请优先给 RECRUIT/OPS 口径签；并排期把 KEYPANO/STAR/E-32 未入 `cfg_metric` 的指标正式化（截图：覆盖未来产业数 = 未入指标库）。

**→ 唐绍祖**  
> 请先签 SHENZHEN；再修 SEARCH/STAR 的 Q037 错挂、KEYPANO/STAR 种子缺口；RECRUIT「待确认」改明确 ✅；OPS 补 cost。

**→ coordinator**  
> 请建 `ENT-MOD-OVERVIEW-E32-METRIC-OPEN-L01`（E-32 缺 METRIC-OPEN，UI 已暴露未注册指标）。

### 7.4 签字

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| PM | 淮政玮 | 全量 9 leaf：3 done / 6 返工；**另缺 E-32 METRIC-OPEN**；催促按 §7.2 | 2026-08-03 |
