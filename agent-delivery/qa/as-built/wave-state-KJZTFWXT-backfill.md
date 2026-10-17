# 脚本补齐波 · 父控进度台账（KJZTFWXT · 2026-10-15 开波）

> 父：qa-agent 父控。三角色编排真源：`script-backfill-playbook.md`。派单只认 `script-backfill-queue-KJZTFWXT.md`。
> 开波扫描：FUNC=774 scripts=703 gap=72 + health REWORK=2 → queue=74。
> 闸门：eval-business=fail / eval-tech=fail / org-capability=fail / bottleneck=partial，其余 14 入口 pass。

## 状态图例

- `待派` / `写稿中` / `写完` / `验收中` / `pass` / `fail→回炉` / `回炉中`

## 第 1 批（写稿 4 并行 · REWORK 优先）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 状态 | 验收 |
|---------|----------|------|---------|------|------|------|
| P0-05 | ent-eval-business | REWORK | FUNC-00943 | W1 `0ec0b4cc` | 三稿交卷（单条双分支机检；coverage L48 残留已清；自检 pass 13.1s） | 排队 V6 |
| P0-07 | ent-eval-tech | GAP | FUNC-00906 | W2 `4f326397` | 交卷（D2：Tab→下拉，父接受） | **pass**（V1） |
| P0-06 | svc-org-field | GAP | FUNC-00644 | W3 `a6421f32` | 交卷（D1×2：tag close/弹窗取消，父接受） | **pass**（V3） |
| P0-06 | ent-eval-business | REWORK | FUNC-00944 | W5 `423b575c` | 交卷（结果态实跑：恢复结果直达 view=result；D1 路径偏差） | **pass**（V5） |
| P0-06 | svc-org-trend | GAP | FUNC-00660 | W4 `553e256a` | 交卷（B 档：expect-1 实断 ✓，2/3 归环境债 ticket；D1×2） | **pass**（V4） |

## 专项（不占写稿并发）

| 事项 | Agent | 状态 |
|------|-------|------|
| runner 解析器顶格列表假 pass | T1 `3083bcbc` | ✅ 交卷：parseYaml 3 处（顶格列表/跨行引号折叠/'' 转义）；774 YAML 对账 0 真失败、457 顶格存量复活、eval-tech/business --check 断言数全 >0 |
| runner skip 分类缺口（V4 发现：SUMMARY 机械 fail=1） | — | 候选小单（未派） |
| runner `-> ` 折叠块标量吞字段（W6 发现） | — | 并入 T1 已修的跨行引号折叠邻近区，验收阶段一并回归观察 |
| 块标量内嵌套缩进拉平（T1 残留风险 1） | — | 挂起备忘（现网 assert 单行风格不受影响） |

## 待人类决策 / 随批回告

- **git 入库**：run-scripts.mjs 工作区混有 ① 2026-10-14 拆分波的 cases-v1 载入改造（前波遗留未提交）② 本波 T1/W1 的 parseYaml 修复——两套逻辑变更同文件，提交拆分/顺序需人拍板；本波铁律禁 push，未动 git。
- ~~coverage.md L48 预置清单残留~~ ✅ 已清（W5-r `423b575c`：P0-05/P0-06 双双移出+备注，失效场景文案同步删）
- **用例修订单回告（D2/D1）**：eval-tech 00906（Tab→下拉）、eval-business 00943（过程态→附录 E 直达结果）、org-field 00644（tag close/弹窗取消）、org-trend 00660（结果壳承载/深链 tab=records 不渲染）——随批整理回告。

## 父裁决记录

- 2026-10-15 15:5x · W1 交卷报「10-14 闸门 fail 当日不复现（开始分析恢复 enabled）」。父裁决：P0-05 不留必红的门控断言，改回**过程态实跑**（tier 保持 B、不回 gold、删 skip 字段）；eval-business 环境反转事实同步给 W5，按探针结果两分支处置。W1 顺带发现的 runner 顶格缩进假 pass 隐患已要求全部写手用 2 格缩进格式规避；全目录解析抽检留给验收阶段。
- 2026-10-15 15:5x · W2 交卷：D2 偏差（用例「五档 Tab」vs 现场 Arco 下拉）父接受，脚本跟现场；eval-tech 预检同样恢复。runner 顶格缺陷与 W1 独立互证 → 开 T1 专项修工具（存量缩进回炉待 T1 修完+父评估影响面再定，不混入本波派单）。
- 2026-10-15 16:0x · W3 交卷：D1×2（移除=arco-tag-close-btn；弹窗取消限 modal footer + container 卸载关闭断言）父接受。
- 2026-10-15 16:0x · W1 二次交卷：4 点全机检、自检实跑 pass（真发起评估任务）。
- 2026-10-15 16:0x · W4 交卷：父裁决接受 B 档处置——expect-1 实断 + expect-2/3 带 ticket `ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD`（结果快照无年序列 payload，环境债非产品缺陷；「数据到位自动转实跑」路径符合期望未发生必红）。D1 新发现「深链 tab=records 分析记录列表不渲染」记为用例修订回告项（验收后随批处理，不阻塞）。验收判定口径：skip 两条以「SKIP Marker + ticket 齐全 + expect-1 实跑通过」为 pass 依据。
- 2026-10-15 16:0x · W5 交卷：分支②（环境恢复）成立——探针 gate_precheck_pass=true、restore_count=7，改写为「最近评估→恢复结果直达 view=result」结果态实跑（D1 路径偏差：用例前置「过程态发起」改「恢复历史任务」；analysis_fp 指纹不可手拼深链）。其提请的「P0-05 是否回炉」为过时信息（已裁决+验收中）。探针脚本落 `tools/_probe-p006-result.mjs`（与 W1 的 `_probe-p005-gate.mjs` 同落点，非 fixtures/scout）——属一次性探针脚本惯例位置（`_` 前缀），证据 JSON/PNG 已进 fixtures/scout；不改判，随批备注。
- 验收排队（串行）：**以 `verify-ledger-KJZTFWXT-backfill.md` 为唯一真源**（本行废弃）。
- ⚠️ 2026-10-15 17:12 · **检测到并行父控会话**（V3′/V4′/V5、W1 三稿、V6 由另一会话完成；本会话所派 V3 `01dd7e3f` 与 W1 回炉 resume 经用户停止）。本会话**停止派单**，避免双父同仓冲突；等人类裁决唯一父控后续波。本会话产物仅 T1（已交付验证）。

## 第 2 批（写稿 4 并行 · queue v2 从 svc-org-capability 起）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 状态 | 验收 |
|---------|----------|------|---------|------|------|------|
| P0-05 | svc-org-capability | GAP | FUNC-00673 | W6 `f675535c` | 交卷（配置态权重 4 断言；自检 pass；D0；发现 runner 不吃 `-> ` 折叠块记备忘） | **pass**（V10） |

**第 2 批结果（2026-10-15 收口）：4/4 全 pass**（eval-tech P0-09、org-trend P0-07、org-field P0-07、org-capability P0-05）。
**累计**：第 1 批 5 + 第 2 批 4 = **9 条全部独立验收 pass**；expect 解析 bug（T1）已修并全量核验。

## 第 3 批（2026-10-15 17:24 刷 queue 后开派，gap 69→65）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 交卷 | 验收 |
|---|---|---|---|---|---|---|
| P0-06 | svc-org-capability | GAP | FUNC-00674 | W7 `300727a2` | 交卷（4/4 自检全过、零 allow_skip：改 40 前后模型区外逐字等值无本地重算、恢复 25 复原、后端签发结果实开且缺分不发明分 canvas=0；探针 2 轮在案） | **pass**（V12：4/4 真实执行、0 归票、基准一致 1/1） |
| P0-13 | ent-eval-tech | GAP | FUNC-00914 | W8 `3a5beb92` | 交卷（2/2 自检 pass：URL view=result+task_id、结果区标题+得分呈现数值不钉死；双分支复用 P0-09 已验证写法；00914 移出 skip 清单、coverage 22→23） | **pass**（V13 真红 C6 → W8-r 三分支回炉 → V13-r 复验过：乙分支指纹直达，2/2 真实执行）→ **第 3 批收口 4/4** |
| P0-08 | svc-org-field | GAP | FUNC-00648 | W9 `4220638f` | 交卷（图型 switch 实勘可点且 checked 真实互斥；矩阵态无独立渲染诚实空→allow_skip 同票 ENV-SVC-ORG-FIELD-HEATMAP-EMPTY；上下文以 task_id+筛选+结论区代理；自检 n/a 归票 exit 0） | **pass**（V11 父代收=正式回传一致） |
| P0-08 | svc-org-trend | GAP | FUNC-00662 | W10 `ffa7393a` | 交卷（expect-0 结果壳+明细区块可达绿；expect-1/2 断言内 SKIP Marker→fail C6 归票同票 ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD；明细表诚实空实证 tbody=0/svc_org_link=0；数据到位自动转实跑抽屉可达+滚动保留） | V14 `b53ff09f` 验收中 |

**父裁（2026-10-15）**：P0-13 金样候选**认可但本波维持 tier B**；gold 提升留待 queue 清零后的 gold 盘点批统一处理（避免批次中途改 smoke 面）。判定依据：catalog「金样」指规格核心性，tier A 须入 smoke 且本波 gold 名单已锁。

**父裁 2（2026-10-15，W9 提请）**：capability 三入口 D2 偏差——**接受为 as-built**：篮非空时「去检索/管理」不可见属源码实证的产品结构事实（`a-alert v-if=!basketOrgs.length` 分支互斥），case 已按双兼容分支如实机检、未硬造三入口常显假绿；FUNC 预期 1 的语义（三入口可达）由空篮分支承载、带入语义由非空分支承载，合并不损失覆盖。偏差随 ticket `ASBUILT-SVCCAP-TRI-ENTRY-D2` 进 handoff 偏离说明，是否推动产品侧对齐（FUNC 改口径或前端改常显）留 PDR 盘点，QA 层不阻塞。tier B 维持（同裁 1 口径）。

**父裁 3（2026-10-15，W8 org-field P0-10 提请）**：设计红=缺陷单口径——FUNC-00650 预期②「同条件当天已成功时直接打开既有结果不重跑」实测不满足（同指纹再发起仍新建 092→093，探针+自检双证），属**产品缺陷非写稿缺陷**：case 断言如实表达 FUNC 预期、红点唯一来源=复用三判据、其余 4 段真实机检绿。裁定：此类「设计红」**不派回炉**（回炉无意义），case 交付判 pass 的条件=验收复跑红点与交卷一致（仅复用三判据红）+ 缺陷票 `D3-SVCORG-SAME-DAY-REUSE-MISSING` 在案（第五工作区侧票，与 D3-SVCSZ/SVCGRAPH/SVCSHORT/SVCCULT 四票并注同根因 `decideAnalysisTaskGate` 指纹等值性）；缺陷本身转票跟踪，随 handoff 汇总报 PM。验收口径在 V21 单中列明。

**父裁 4（2026-10-15，W9 eval-tech P0-14 提请）**：
- **P0-13 回炉建议——接受，列入回炉队列**：慢态「原地渲染 URL 不迁移」下 P0-13 现骨架会假性超窗（V13-r 复验时命中乙分支指纹直达未暴露该路径，但暴露面真实存在）。P0-14 已实证慢态形态（20~40s 原地渲染、canvas 晚挂）并扩为双形态收口——P0-13 按同法补慢态分支。**不阻塞本批收口**：P0-13 本体（三分支+E.5 语义）已验过，慢态是补充路径；列入第 6 批回炉单（W8-r2），复验时若环境呈快态则慢态分支走 observed 注记即可。
- **环境间歇抖动（浮层/确定按钮自愈型）——不开新票**：与既有「时点性形态变化」同型，记 wave-state 备忘；连续跑批间歇建议 ≥30s，第 6 批派单附注。

## 第 4 批（2026-10-15 18:17 开派；验收槽在 W8-r 回炉期间复用）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 交卷 | 验收 |
|---|---|---|---|---|---|---|
| P0-07 | svc-org-capability | GAP | FUNC-00675 | W9 `e38038b5` | 交卷（双兼容分支机检：空篮三入口同屏实证+非空全量分支带入/幂等/移除仅本次 1/1；D2 偏差源码实证「去检索/管理仅空篮渲染」→ **父裁 2：接受 as-built**，ticket ASBUILT-SVCCAP-TRI-ENTRY-D2 随 handoff；篮漂移归既有 ENV-SVCCAP-BASKET-ORG-LT2-001） | **pass**（V17：非空分支 3/3 全过，D2 实测与父裁一致） |
| P0-09 | svc-org-field | GAP | FUNC-00649 | W10 `b2e1c539` | 交卷（**零归票真实机检**：探针证实筛选交互配置态可断与热力债无交集——15 项→键入收窄 1→清除恢复 15、URL 无任务参数；3 条双层断言：构造已选→收窄→恢复+不发起+已选不变；自检 3/3） | **pass**（V15：3/3 真实执行、零归票复核成立） |
| P0-09 | svc-org-trend | GAP | FUNC-00663 | W7 `c3348bb6` | 交卷（expect-0 面板可达+expect-3 未闭合口径标识实断绿：GAP-SVC-ORG-HEAT 红问号只显治理引用+Q-SVCCHAIN-02 badge+演示口径 note，不依赖年序列；expect-1/2 斜率星级/依据行同票 ENV-SVC-ORG-TREND-NO-SERIES-PAYLOAD 归票（no_series 诚实空实证星级=0 依据行=0 无伪 8 件套）；自检 2 实断+2 skip） | **pass**（V16：2 实断+2 skip 合法归票） |
| P0-13 | chain-bottleneck | GAP | FUNC-00611 | W8 `9ffc0d0b` | 交卷（实体目录 bottleneck 落位与既有 18 条同 index；三层探针坐实结果态不可达→两层 skip+新 ticket ENV-CHAIN-BOTTLENECK-NO-RESULT（与旧票同根可回炉合并）；allow_skip 4/19=21.1%≤25%；移交项①FUNC 册「自动化用例ID」列系统性错位（00611 写 P0-12 实为 00622 等）→ 留待专项批 ②CHAIN-20261015-008 失败记录留证） | **pass**（V18：n/a 合法归票+双保险在位）→ **第 4 批收口 4/4** |

**第 4 批结果（2026-10-15 收口）：4/4 全 pass**。**累计 19 条 pass**（第 1 批 5 + 第 2 批 4 + 第 3 批 6 + 第 4 批 4，其中第 3 批含 P0-13 一次回炉）。
queue 已刷：gap 65→57，rework=0。

## 第 5 批（2026-10-15 18:5x 开派，gap 57）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 交卷 | 验收 |
|---|---|---|---|---|---|---|
| P0-14 | ent-eval-tech | GAP | FUNC-00915 | W9 `b6d141d5` | 交卷（r5 全绿 3/3：结果态双形态收口（快态指纹直达/慢态原地渲染 20~40s canvas 晚挂）+雷达 X3 同词代理+≥2 家对比形态；零 allow_skip 0/24；PRECHECK-001 已复测 enabled 移出；**父裁 4**：①P0-13 慢态假性超窗→接受列第 6 批回炉（W8-r2 补慢态分支）②环境间歇抖动自愈型→不开票，第 6 批派单附「跑批间歇 ≥30s」） | **pass**（V22：快态 3/3，12s）→ **第 5 批收口 4/4** |

**第 5 批结果（2026-10-15 收口）：4/4 pass**（其中 org-field P0-10 为 pass 带缺陷票，D3 同根因票累计第五例）。**累计 23 条 pass + 1 带票 pass**（第 1 批 5 + 第 2 批 4 + 第 3 批 6 + 第 4 批 4 + 第 5 批 4；另 P0-13/eval-tech 一次回炉复验过）。
**待办移交第 6 批**：①W8-r2 回炉（eval-tech P0-13 补慢态分支）②coverage.md eval-tech 头部「23 条」旧批注清理③batch 间歇 ≥30s。

## 第 6 批（2026-10-15 19:5x 开派，gap 57→53；W8-r2 占 eval-tech 目录，新写 3 条异目录 + 1 回炉）

| CASE_ID | entry_id | kind | FUNC_ID | 写手 | 交卷 | 验收 |
|---|---|---|---|---|---|---|
| P0-13(回炉) | ent-eval-tech | REWORK | FUNC-00914 | W8-r2 `e44e87ca` | 排队 | — |
| P0-10 | svc-org-trend | GAP | FUNC-00664 | W9 `288ba654` | 排队 | — |
| P0-09 | svc-org-capability | GAP | FUNC-00678 | W10 `d4cb8a5d` | 排队 | — |
| P0-11 | svc-portal | GAP | FUNC-01315 | W7 `3be9c68a` | 排队 | — |
| P0-08 | svc-org-capability | GAP | FUNC-00677 | W10 `25cfefdc` | 交卷（自检 3/3 零 allow_skip：同源呈现 as-built=chart-switch 单选互斥机检、雷达 radio 数据驱动、ⓘ 评审门控 MetricSpecCard、无分诚实空态+两任务交叉验证；数据态证据（两视图同显/维度轴）补测归新 ticket ENV-SVCCAP-NO-SCORE-RESULT） | **pass**（V20：3/3 真实执行、基准一致 1/1） |
| P0-14 | chain-bottleneck | GAP | FUNC-00612 | W7 `b52e3fb3` | 交卷（两层 skip 同票 ENV-CHAIN-BOTTLENECK-NO-RESULT 不另开；探针 probe-p014.json 坐实今日仍全失败；三断言：图谱载体（无载体→fail 防截断假绿）/节点健康度文案/三档至少两档；--check 20 条 0 错；allow_skip 5/20=25.0%≤25% 贴线） | **pass**（V19：n/a 合法归票，双坐实） |
| P0-10 | svc-org-field | GAP | FUNC-00650 | W8 `f82ec1ab` | 交卷（5 段双层 expect；①列表 5 列 ②记录行直达 0 POST ③④变更显式重析（新 task_id≠首发）4 段真实机检绿；**⑤同条件当天复用设计红**：同指纹再发起仍新建（092→093）→ 缺陷票 D3-SVCORG-SAME-DAY-REUSE-MISSING（与 sz/graph/short/cultivate 四票同根因 decideAnalysisTaskGate 指纹等值性）→ **父裁 3：设计红不回炉，验收判据=红点一致+票在案**） | **pass 带缺陷票**（V21：红点分布一致+票在案+零假绿） |

> 注：第 4 批移交项①（FUNC 册「自动化用例ID」列系统性错位，如 00611 行写 P0-12 实为 00622、00614 行写 P0-05 同错位）为全册回写问题，queue 清零后另派专项批。
| P0-09 | ent-eval-tech | GAP | FUNC-00913 | W2 `4f326397` | 交卷（双分支移植；实勘甲分支为主路径 15~20s 迁 result；零新增偏差） | **pass**（V7 `4abc22b1` PING 超时中断→父代收，机跑落盘完整+静态父代核） |
| P0-07 | svc-org-field | GAP | FUNC-00647 | W7 `5f558941` | 交卷（热力图诚实空→X3 代理+归票 ticket；ⓘ/角标可实断；D1×2+D4） | **pass**（V9，skip 归票路径） |
| P0-07 | svc-org-trend | GAP | FUNC-00661 | W8 `1622d0bf` | 交卷（诚实空分支：expect-0 实断 + hover/ⓘ 归票同 ticket；数据到位转实跑保留） | **pass**（V8） |

## 已完成

### 第 1 批（全部独立验收 pass · 2026-10-15 收口）

| CASE_ID | entry_id | kind | 稿次 | 验收 |
|---------|----------|------|------|------|
| P0-07 | ent-eval-tech | GAP | 1 稿 | V1 pass |
| P0-06 | svc-org-field | GAP | 1 稿 | V3 pass |
| P0-06 | svc-org-trend | GAP | 1 稿 | V4 pass（skip 带票归环境债） |
| P0-06 | ent-eval-business | REWORK | 1 稿 | V5 pass |
| P0-05 | ent-eval-business | REWORK | 3 稿（V2 fail→双分支回炉） | V6 pass |

## 验收串行队列（全局 =1）

（空 · 2026-10-15 18:15 V14 与 W11 回炉均经用户手动停止，未出 verdict）

### 在途冻结（用户停止，待人类指示后再动）

| 件 | 对象 | 停止时状态 |
|----|------|-----------|
| V14 `86ccf4cf` | org-trend P0-08（FUNC-00662）验收 | 已派出即停，无 verdict、无 run 落盘 |
| W11 `2dfe00fa` | eval-tech P0-13（FUNC-00914）三分支回炉 | 已派出即停，cases/P0-13.yaml 维持 V13 fail 原稿 |

- P0-13 当前事实：ledger #13 = fail（C4），回炉未执行——续波时优先补派回炉。
- org-trend P0-08 当前事实：W10 已交卷、未验收——续波时补派验收（判定口径已在本台账 W4 裁决行）。

## 已完成

（无）
