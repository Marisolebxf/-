# SVC 引育推荐三条 MODEL 公式会签记录（2026-10-22 · human:唐绍祖）

> 会签人：`human:唐绍祖`（算法 Lead）｜会签日：2026-10-22｜落点：`cfg_metric-SVC-seed.yaml` + `metric-readiness-matrix-SVC.yaml`
> 范围：`M_SVC_REC_ATTRACT_SCORE`、`M_SVC_REC_CULTIVATE_SCORE`、`M_SVC_DEEP_181_1`
> 结论：**同意（agree with scope）**——按王惠四维、维度内与维度间**等权默认**签 `formula` + `algorithm_type=MODEL`；**不签「四维完整」**，页面/接口须按「试点口径、部分支持、未覆盖维度」标注。

## 一、为什么是这三条、为什么现在签

- 需求出处：算法库 SRS **180 / 181**（《科技专题服务算法库》产业服务·深度分析 §9.9 引入推荐模型 / §9.10 培育推荐模型），展示侧需规 §1.1.1.2.4.2.7.5 / 7.6。
- 三条 ID 的分工：
  | ID | 角色 | 与需求叶关系 |
  |---|---|---|
  | `M_SVC_DEEP_181_1` | 培育推荐**模型本体** | SRS 181 算法叶（ALGO-SVC-DEEP-181） |
  | `M_SVC_REC_CULTIVATE_SCORE` | 培育推荐**评分输出位** | 同一 181 叶的评分落点（双 ID） |
  | `M_SVC_REC_ATTRACT_SCORE` | 招引推荐**评分输出位** | SRS 180 叶的评分落点（模型本体为 `M_SVC_DEEP_180_1`，不在本次范围） |
- 为什么卡在这里：2026-08-31 王惠 20260829 底稿正式化入库后，三条矩阵 D1 一直是 `draft`，`d1_note` 原文为「formula/algorithm_type 待唐绍祖会签」；2026-10-16 的 STAT 21 条公式会签任务 DoD 明写「范围仅 SVC STAT 21 条，**不改 18 条 MODEL**」，故 MODEL 这批从未进会签。`Q-SVCCHAIN-05`（正式权重默认值、量化来源、名单入围阈值、推荐理由/培育建议规则）责任人是算法 Lead + 甲方。
- 现在签的直接触发：2026-10-22 接口调研确认 `POST /service/rec-list`（`kind=attract|cultivate`）各返 50 条、`data_source=real`，接口已通，只剩口径未签。

## 二、会签结论（逐条）

| 指标 | 签署的维度集（唯一真源） | 各维可算性（实测） | 本次**未覆盖** | 结论 |
|---|---|---|---|---|
| `M_SVC_REC_ATTRACT_SCORE` | 产业匹配度 / 技术领先性 / 发展潜力 / 对外合作意愿 | 产业匹配 23.25%（6,805/29,263，标签 12 个 vs 15 集群零交集）；技术领先仅发明专利占比可算（研发投入列全空）；发展潜力营收 5 家、净利 3 家；对外合作以投资边代理 | 政策匹配度、深圳连接度（需求 04/Bid 与 05 叶另有此二维） | 同意，限试点 |
| `M_SVC_REC_CULTIVATE_SCORE` | 现有规模 / 技术创新能力 / 服务成效 / 市场缺口 | 现有规模可算；市场缺口可算但分母降级为池内同行业营收；出分 169/14,033（1.20%） | 技术创新能力（研发人员/研发投入两列全空）、服务成效（两字段待建、无承载表）、产业相关度、政策匹配度 | 同意，限试点 |
| `M_SVC_DEEP_181_1` | 竞争力 / 产业相关度 / 政策匹配度 / 发展潜力 | 竞争力走专利代理（13,378 家）；产业相关度 10,778 家；政策匹配走标题近似（1.9 万条政策，分母 190）；发展潜力 673 家有财务、营收 CAGR 161 / 净利 127 | 无整维「未覆盖」，但两维为代理口径（竞争力、政策匹配） | 同意，限试点 |

**统一表述**：三条均为「试点口径 + 部分支持 + 结果面标注未覆盖/代理维度」，不得表述为「四维完整评分」，不得作为对外招商/培育名单承诺。

## 三、本次签死的统一条款

1. **权重**：维度内指标等权；维度间等权（各 1/4）。如需按评估重点调整，须另出权重变更单并 bump `version`，不得在页面配置区静默改权重。
2. **缺维规则**：缺维按**可用维均值**计入；可用维数 **< 2 不入排序**（不补 0、不造数、不以全库均值填充）。
3. **极值归一化**：`(x - min) / (max - min) × 100`，分母为**当期同池**的 min/max；跨期比较须重算，不得复用历史 min/max。
4. **增长率口径**（181 / CULTIVATE / ATTRACT 的发展潜力维）：取**最近两个正值年** CAGR，允许中间缺年、按实际年间隔折年；负值年跳过不补 0；上下截断 −95% ~ +300%；营收与净利各算，都有取平均。
5. **代理口径必须显式标注**（不得静默）：
   - 181 竞争力维：`0.6 × 专利数归一 + 0.4 × 发明专利占比归一`（年报研发两列全空，代理研发投入强度/研发人员占比）；
   - 181 与两条评分位的政策匹配：政策标题近似 + 分母 190（无 `svc_org_policy_hit` 命中表）；
   - ATTRACT 对外合作：以 `dwd_org_invest_info` 对外投资边代理项目数与覆盖区域数（`svc_coop_project_count` / `svc_coop_region_count` 待建）；
   - CULTIVATE 服务成效：仅在补齐 `svc_served_ent_count` / `svc_project_count` 前不得计入正式分数；如临时用 `dwd_org_important_news_info` 代理，结果面须标「代理」。
6. **名单入围阈值 / 截断规则**：本条**未签**（属 `Q-SVCCHAIN-05` 甲方项），页面继续按演示规则 + 🧪⚠️，不得把「前 N 名」「四档」当验收口径。
7. **不动的三轴**：D2 结构支撑、D3 源映射、D4 接入状态**均不因本次会签变绿**；`D4` 维持 `mock`，`D3` 维持 `pending_ods`。

## 四、明确不签的部分（待甲方 / 待供方）

| 事项 | 归属 | 状态 |
|---|---|---|
| 两套四维名冲突：04/Bid 与王惠版 vs 05 模型叶（180/181） | 甲方裁定（`REC-B01` / `REC-B02`） | 未定。本次签王惠版为口径真源，05 叶维度名视为展示别名，不另造 ID |
| 正式权重默认值、量化来源、名单入围阈值、推荐理由/培育建议生成规则 | `Q-SVCCHAIN-05`（甲方） | 未定，本次只签「等权默认」作试点 |
| 机构 × 领域（× 六环节）服务记录 | 供方 `SVC-P0-3` | 未交付 |
| 年报研发两列、连续两年营收/净利、从业人数、资产 | 供方 `SVC-P0-2` / `SVC-P1-2..4` | 覆盖极薄或整列空 |
| 政策命中表 `svc_org_policy_hit` | 项目侧落建 | 待建 |
| gkx 口径改写稿回仓 | data-agent | `local-workspace/.../20261021_指标整体开发进度调研/第三方库指标计算过程/` 有稿，**未提交进 `agent-delivery/metrics/calc-logic/SVC/`** |

> **重要边界**：本次签的是**口径框架 + 默认权重 + 缺维/截断规则**，`calc-logic/SVC/` 现存三份仍是 20260829 王惠版（`source_tables` 指向 `demo_*`）。签字不等于认可 demo 实现，也不等于认可 gkx 改写稿的实测值；gkx 稿回仓后须做一次「签署版 ↔ 实现版」对照复核。

## 五、回写清单（本次已落盘）

- `agent-delivery/metrics/registry/cfg_metric-SVC-seed.yaml`
  - 三条 `pending_cosign` 写入会签结论；`M_SVC_DEEP_181_1` 的 `pending_ref` 从 `GAP-ALGO-TYPE-UNSIGNED` 改为 `Q-SVCCHAIN-05`（类型已签，余项转甲方）。
- `agent-delivery/metrics/registry/metric-readiness-matrix-SVC.yaml`
  - 三条 `d1_note` 改为会签说明；`lifecycle_stage: open → formula_signed`；`d1_def_status` 维持 `draft`（源表仍 demo 面，不升 `aligned`）。
- `agent-delivery/客户决策清单跟踪表.md`：`Q-SVCCHAIN-05` 的「待办」列改为「算法侧试点口径已签，待甲方」。
- `agent-delivery/metrics/calc-logic/SVC/{M_SVC_REC_ATTRACT_SCORE,M_SVC_REC_CULTIVATE_SCORE,M_SVC_DEEP_181_1}.md`：追加「会签记录」章节，指向本文件。

## 六、依据与证据

- 口径真源：`agent-delivery/metrics/calc-logic/SVC/`（三份，20260829 王惠版）
- 就绪度：`agent-delivery/metrics/registry/metric-readiness-matrix-SVC.yaml`（三条原 `d1_note`）
- 需求映射：`agent-delivery/metrics/registry/metric-srs-map.yaml`（180/181 → ALGO-SVC-DEEP-180/181）
- 页面欠账：`agent-delivery/metrics/request/专题系统/pages/SVCCHAIN-RECOMMEND.yaml` `semantic_debt` REC-B01 / REC-B02 / REC-B03 / REC-B04
- 甲方问题：`agent-delivery/客户决策清单跟踪表.md` `Q-SVCCHAIN-05`
- 供方缺口：`agent-delivery/data/third-party-source/question/服务机构维度/SVC-SUPPLIER-QUESTIONS.md`（SVC-P0-2 / SVC-P1-3 / SVC-P1-4）
- 实测（gkx 口径，未回仓）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_181_1.md`（深圳池 25,597；四维覆盖 13,378 / 10,778 / 10,778 / 161+127；合成 10,811 家）
- 实测（demo 口径）：`local-workspace/docs/tasks/investiage/20261020_指标整体开发进度调研/开发库指标计算过程/`（深圳池 14,033；CULTIVATE 出分 169；ATTRACT 外部池 29,263）
- 接口现状：`local-workspace/docs/tasks/investiage/20261022_产业链服务机构分析接口调研/产业链服务机构分析接口调研报告.md`（rec-list 50 条、`data_source=real`、权重待 Q-SVCCHAIN-05）
- 先例：`7d78ff25`（2026-10-16 STAT 21 条公式会签落盘，同格式）

## 七、解挂 / 升级条件

- `lifecycle_stage: formula_signed → source_mapped`：三条 `source_tables` 从 `demo_*` 换成正式 ODS/DWD 实链（或登记诚实缺口），gkx 改写稿回仓并经 data-agent 核验。
- `D1: draft → aligned`：8 件套 9 项齐（含 `source_tables` 合格值），不靠「签了公式」单条跳档。
- `Q-SVCCHAIN-05` 闭环：甲方确认正式权重、量化来源、名单入围阈值、推荐理由/培育建议生成规则；四维名冲突同时裁定。
- `D4: mock → live`：Python 侧出真数并灌 ADS，页面验收按「试点口径」文案与角标先行。
