# ZMATE-RPT · 门 1 PDR 核对表（PDR-01～14）

> **任务**：`ZMATE-RPT-PDR-G1-L01`  
> **模块**：ZMATE 战略报告创作（Zmate 战略咨询报告创作工作台 · **Demo 样机定义包**）  
> **规程**：`agent-delivery/产品定义评审规程.md` §5 / §5.2  
> **轨道**：Track-MS（中屏 `medium_1440_1920`）  
> **起草**：`agent:product-agent` · 2026-11-16  
> **监管人 / 签收**：`human:淮政玮`（**禁止代签**；签收区留空）  
> **ponytail**：`off`（定义任务）

## 0. 输入齐备（四件套）

| 件 | 路径 | 前置任务态 |
| --- | --- | --- |
| USM | `…/ZMATE-战略报告创作/USM-ZMATE-战略报告创作.md` | `ZMATE-RPT-USM-L01` · integration |
| TRACE | `…/ZMATE-战略报告创作/TRACE-ZMATE-战略报告创作.yaml` | `ZMATE-RPT-TRACE-L01` · integration |
| IA | `…/ZMATE-战略报告创作/IA-ZMATE-战略报告创作.md` | `ZMATE-RPT-IA-L01` · integration |
| Wireframe | `…/ZMATE-战略报告创作/Wireframe-ZMATE-战略报告创作.md` | `ZMATE-RPT-WF-L01` · integration |

**包性质**：非专题八域叶子扩 scope；产品功能点自编号 `RPT-01…12`；`acceptance_catalog: null`；本阶段 `demo-ui-topic` 纯前端样机。多项条件检查项可 `N/A` + 依据。

---

## 1. 覆盖摘要（纪要用）

| 项 | 值 |
| --- | --- |
| 本包叶子应覆盖 | 12（`RPT-01…12`） |
| 已映射 | 12（`coverage_summary.leaves_mapped == leaves_required`） |
| 排除叶子（有据） | ZHIKU-SP-50/51/52、PORTAL-STRATEGY-REC、TOPIC-05-STRAT-WORKSPACE |
| 指标 / METRIC-OPEN | **不适用**（见 PDR-05/06 N/A） |
| 开放项 | 6（ROLE×2 / HANG / V1 / EXPORT / DEMO）— **未**入客户决策清单 → PDR-07 ❌ |
| DEMO tier | TRACE `planned_tier: DEMO` 已标；非 catalog 应付点，demo-fallback「如需」暂缓 |
| IA 重组 | 有（USM 差异说明：Graph 分站 / 排除门户与八域 / 收窄本台） |
| screen_tier | medium_1440_1920 · Track-MS（体验 Owner 待指定） |

---

## 2. PDR-01～14 逐条核对

| # | 检查项 | 结论 | 证据路径 | 缺口 |
| --- | --- | --- | --- | --- |
| PDR-01 | 本模块所有 bid 叶子已在 TRACE `compliance_refs` 映射 | ✅ | TRACE `source_manifest`（SRS 战略咨询报告生成 + 核增写作四叶 included）；`stories[*].compliance_refs` → `RPT-01…12`；角色锚点 §1.1.1.2.4.2 | 本包为自编号产品叶，非 catalog `P-/DS-`；挂靠见 OPEN-ZMATE-HANG-01 |
| PDR-02 | 无静默删除/遗漏（每叶有 route 或 REMOVED+PM） | ✅ | `leaves` / `compliance_refs` 均有 `provisional_route` 或正式 route 指向；`leaves_excluded_with_reason` 五条有 reason | TRACE 仍写 `/zmate/report/…` provisional；IA/WF 已定 `/zmate-strategy-demo…` — **须签收后回填 TRACE route / `wireframe_frames`**（不挡「有 route」判定） |
| PDR-03 | `coverage_summary.leaves_mapped == leaves_required` | ✅ | TRACE `coverage_summary`：`leaves_required: 12` / `leaves_mapped: 12` | 无 |
| PDR-04 | 活跃 scope_units 仍在 52~64（±10%）内 | N/A | 本包声明：Demo 样机定义包，**不**扩/不占专题八域活跃 scope；`RPT-*` 不进 `scope-baseline` 计数 | 若门 1 后并入 catalog / 基线，须另做 ±10% 核算 |
| PDR-05 | 统计字段 → metric_id + wireframe 第 6 列；无则 N/A | N/A | WF 无 KPI 统计字段第 6 列清单；仅示意「指标需求四态」与溯源 `metric_id_or_gap`；TRACE `metric_seed: null` | 正式 seed / 第 6 列 = GAP-ZMATE-RPT-03（门 1 后） |
| PDR-06 | 语义卡达 §3.4；不适用则 N/A | N/A | 完整 METRIC-OPEN / 口径草稿卡 **不适用** Demo 样机；USM/WF 已写四态诚实、禁假 live、Judge Default-FAIL | 真后端波次再开 METRIC-OPEN；禁伪闭合 D1–D4 |
| PDR-07 | 有开放项须同步客户决策清单；无则 N/A | ❌ | USM「开放项」+ TRACE `coverage_summary.open_questions` 共 6 条已列；`客户决策清单跟踪表.md` **无** `OPEN-ZMATE-*` / `Q-ZMATE-*` 命中 | **须补登**决策表（或门 1 纪要逐条拍板闭合后回填）后方可改 ✅ |
| PDR-08 | DEMO/INTEG 已标 tier +（如需）demo-fallback | ✅ | TRACE 模块与各 `compliance_refs`：`planned_tier: DEMO`；`DEC-ZMATE-DEMO-BOUNDARY` | 非 acceptance-catalog 应付叶 → `demo-fallback-registry`「如需」**暂不登记**；入 catalog 后补 `DEMO-ZMATE-RPT` |
| PDR-09 | USM 含主路径 walkthrough + 验收场景 | ✅ | USM「场景 walkthrough」主路径 A/B/C + 异常降级表；验收 `ZMATE-USM-01…13` | 无 |
| PDR-10 | IA 重组已在 USM「差异说明」记录 | ✅ | USM「与 bid-reference / 建设方案差异说明」；IA §7 对照（Graph 分站、排除门户/八域、V1 最短路径） | 无 |
| PDR-11 | 与 `architecture-baseline` 无冲突（调用链/仓边界） | ✅ | USM/IA/TRACE：Demo 落 `demo-ui-topic`；禁直连 `lumen-*`（D12）；算法/真后端不在本定义包交付 | 体验 Owner 未指定不影响铁律自检；真链阶段再核 Java→Python |
| PDR-12 | 权限/降级态已识别（L0–L4 如有） | ✅ | USM 异常与降级路径表；WF §2 六态（empty/locked/awaiting_gate/running/failed/compliance_fail）；角色待映射 OPEN-ZMATE-ROLE-01/02 | 正式 L0–L4 / 导出权益未映射（Demo 角色切换示意） |
| PDR-13 | 涉数据则对齐 GDF；不涉则 N/A | N/A | 本阶段不涉贴源 / Mapping / ADS 调度；纯前端 Mock / 四态示意 | 真取数波次再对 GDF |
| PDR-14 | TRACE 标明 screen_tiers 与轨道负责人 | ✅ | TRACE：`screen_tier: medium_1440_1920`；`delivery_track: Track-MS`；`owner_compliance` / `owner_semantic` / `supervisor` 已填 | 字段名为单数 `screen_tier`（语义等价）；**`owner_experience: 待业务确认`**（GAP-ZMATE-RPT-02）— 建议签收前指定或纪要临时代 |

### 附加（Track-MS · 非正式本单强制范围）

| # | 项 | 结论 | 依据 |
| --- | --- | --- | --- |
| PDR-15 | V1 高保真首轮反馈入联合修订清单；跳过则 N/A | N/A | 本阶段仅线框级 Wireframe，**未**开 UI-HIFI；V1 非门 1 硬前置（规程 2026-07-28）。未签收不得开 UI-HIFI / FE-DEMO（任务 DoD） |

---

## 3. 开放项汇总

| ID | 问题 | 建议默认 | 谁拍板 | 决策表 |
| --- | --- | --- | --- | --- |
| OPEN-ZMATE-ROLE-01 | 是否另建「写作操作岗」 | 否；沿用四类服务对象 | 业务 + 权限 | ❌ 未同步 |
| OPEN-ZMATE-ROLE-02 | 个人模板库管理角色 | 复用系统管理 / 待确认 | 业务 | ❌ 未同步 |
| OPEN-ZMATE-HANG-01 | 父包挂靠 | 高端智库生成 + 专题切片交叉引用 | **门 1 监管人** | ❌ 未同步 |
| OPEN-ZMATE-V1-01 | Demo 是否强制辩完才出报告 | V1 可跳过辩论但须可点验协作；V2 强制绑 slice | 产品会签 | ❌ 未同步 |
| OPEN-ZMATE-EXPORT-01 | 导出与 ENT-EXPORT 对齐时机 | 门 1 后 ARCH/实现波次 | 架构 + 前端 | ❌ 未同步 |
| OPEN-ZMATE-DEMO-01 | 旧 L01–L08 废稿 vs 局部复用 | 默认废稿，按 WF 重做 | 会签 | ❌ 未同步 |

---

## 4. 其他缺口（非 PDR ❌，建议联合修订）

| ID | 摘要 | 建议动作 |
| --- | --- | --- |
| GAP-TRACE-ROUTE | TRACE provisional `/zmate/report/*` 与 IA/WF `/zmate-strategy-demo*` 不一致；`wireframe_frames: []`；`GAP-ZMATE-RPT-01` 文案仍写「IA/WF 未交付」过时 | 签收后 product 回填 TRACE |
| GAP-ZMATE-RPT-02 | 体验 Owner 未指定 | 签收前指定或纪要临时代 |
| GAP-ZMATE-RPT-03 | 正式 metric seed 未建 | 真后端 / METRIC-OPEN 波次 |
| GAP-PDR-07 | 开放项未进客户决策清单 | 补 `Q-ZMATE-*` 或门 1 纪要闭合后回填 |

---

## 5. 起草结论（**非签收**）

| 项 | 内容 |
| --- | --- |
| 四件套 | 齐（USM/TRACE/IA/WF 均已 integration） |
| ✅ | PDR-01、02、03、08、09、10、11、12、14 |
| N/A | PDR-04、05、06、13（+ PDR-15） |
| ❌ | **PDR-07（1 条）** — 开放项未同步客户决策清单 |
| 建议监管人处置 | **有条件闭合**：签收时确认 OPEN 默认值，并责成补登决策表 / 回填 TRACE route；或先补 PDR-07 再签完整闭合。**禁止**未签收开 UI-HIFI / FE-DEMO |

> 本表为 product-agent **起草核对**，不构成门 1 通过。正式结论以监管人签收 +（如需）合规/体验/语义/架构列席纪要为准。

---

## 6. 签收区（留给 human:淮政玮 · 禁止代签）

| 项 | 填写 |
| --- | --- |
| 监管人姓名 | `human:淮政玮` |
| 签收日期 | ________________ |
| 签字 | ________________ |
| 结论勾选 | ☐ 完整闭合　☐ 有条件闭合（条件见下）　☐ 不闭合（退回） |
| 有条件闭合时：条件 / deadline | ________________ |
| 备注 | ________________ |

| 列席（可选 · 按规程 §5.1） | 姓名 | 签字 | 日期 |
| --- | --- | --- | --- |
| 合规 Owner | 郭万迎 | | |
| 体验 Owner | （待指定 / 高颖） | | |
| 语义 Owner | 何老师 | | |
| 架构师 | 徐滕强 / 李伟 | | |
