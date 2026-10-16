# 服务链图谱分析 脚本→用例 覆盖表（R3 新写）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCGRAPH-服务链图谱分析/FUNC-服务链图谱分析-用例.md` v2.0（00707~）。
env-gate overall=pass（2026-10-14）；hang 空 → 禁点边结果态金样。

## 汇总（2026-10-15 声明收口后）

| 汇总 | 值 |
|------|-----|
| A 档金样 | **5**（`P0-01~P0-05`）· 零 allow_skip |
| B 档机检 | **16**（`P0-06~09`、`P0-19~30`）· 含 GAP 补齐 P0-09 |
| 机检合计 | **21** · skip 占比 **7/24≈29%**（P0-09 入列后同票 skip +1；口径沿 P0-30 波预警与父决策豁免，见下行） |
| 超配豁免 | **父决策 2026-10-15**：同票 `ENV-SVCGRAPH-HANG-EMPTY-001` 集中 skip（P0-06/07/08/28/30 + **P0-09**）同根因（画布 hang 空），修复一张票全部自动转实；原声明 00715 已改由 P0-09 承载；其余声明 4 条（00716/17/22/30）仍不扩大分母 |
| 声明不自动化 | **4**（00716/17/22/30；00715→P0-09，见下清单） |
| catalog / index.yaml | index `all:` 已挂 P0-09；catalog **未改**（子 agent 禁改） |

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档 | 可见动作 / skip ticket |
|---------|----------|---------------|---|----|------------------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00707 | 入口·路由与双 Tab | P0 | A | 直达 graph/tab=graph；主 Tab `/服务链图谱分析/` |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00708 | 配置区·产业集群 15 | P0 | A | 短名清单 + placeholder；禁结果态点边 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00712 | 结果态·关系网络图核心节点 | P0 | B | 历史「查看结果」深链；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（hang 空自动 n/a，修复后转实） |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00713 | 结果态·四类关系与图例带文字 | P0 | B | 历史「查看结果」深链 + 图例 off→on 往返；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（同 P0-06 渲染债，图例全不渲染自动 n/a，修复后转实） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00714 | 结果态·模式①/②节点构成差异 | P0 | B | 模式①历史深链（SVC-20260903-001，radio 回显①）+ 模式② fresh 构造深链（SVC-20260915-014，_probe-p008-fresh 实测起任务通但结果仍 hang 空）；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（同票渲染债自动 n/a，修复后转实） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00715 | 结果态·画布拖拽/缩放/平移 | P0 | B | 历史「查看结果」深链；allow_skip 探测 svc-eco-g6-graph；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（_probe-p009：g6Count=0/emptyVisible=true/interact 未尝试；修复后 expect 结构+wheel/drag 节点守恒自动转实，随动视觉 manual） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00716 | 结果态·机构节点下钻画像抽屉 | P0 | B | 历史「查看结果」深链；allow_skip 探测 svc-eco-g6-graph；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（_probe-p010：g6Count=0/emptyVisible=true/drawerVisible=false/click 未尝试；修复后 expect 结构+画布点节点开 .arco-drawer+画像详情自动转实） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00717 | 结果态·关联主体节点侧栏摘要 | P0 | B | 模式②深链（SVC-20261015-014）；allow_skip 探测 svc-eco-g6-graph；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（_probe-p011：mode2=true/g6Count=0/emptyVisible=true/actorVisible=false/click 未尝试；修复后 expect 模式②结构+扫点开 svc-eco-actor-summary+类型/非机构明示自动转实；三类依次点击 manual） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00722 | 结果态·聚焦机构 1 度邻域 | P0 | B | 历史「查看结果」深链；allow_skip 探测 svc-eco-clip-focus；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（_probe-p012：focusCount=0/filtersCount=0/g6Count=0/emptyVisible=true；聚焦挂 v-if=!parsed.empty；修复后 expect 结构+选定 eco_focus 1 度邻域+清除恢复且过滤勾选不变自动转实） |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00730 | 异常·子网过小统计空态 | P1 | B | 历史「查看结果」深链；allow_skip 探测 svc-eco-clip-filters；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（_probe-p013：filtersCount=0/g6Count=0/emptyVisible=true/size=0/0/dens 基线「子网过小」属 hang 空诚实空非过滤构造，禁止假绿；修复后 expect 过滤可操作+构造 N<2（优先 N=1，否则 N=0+已施加过滤，clipEcoGraph 0 边早退 D1）+密度「子网过小，不计算统计值」+无 NaN 自动转实；00729 图区空提示/00718 密度基线不吞并） |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00725 | 备选·分析记录与当天复用 | P1 | B | fresh 当天任务→记录列表/互斥→同日同条件再发起（复用判定）→记录「查看结果」→切回保留（4 绿+1 设计红）；ticket=D3-SVCGRAPH-SAME-DAY-REUSE-MISSING（同日同条件仍 POST 新建不复用，红即缺陷显性化；Q-ANALYSIS-01）；实跑 fail（20261015-…-p0-19-r2） |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00726 | 配置态·生态包三工作区隔离 | P0 | B | fresh 起分析→切 chain→切 shenzhen→切回 graph（隔离/不自动触发/找回 5 断言绿；「切回保留」1 断言设计红）；ticket=D3-SVCGRAPH-WS-SWITCH-STATE-LOST（切回后产业/模式/任务态不保留，红即缺陷显性化）；实跑 fail（20261015-…-p0-20-r2，5 绿+1 设计红） |
| P0-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00727 | 配置态·评审模式零泄漏 | P1 | B | 纯配置态开关往返（P3 路径开评审→两枚追溯按钮可见可点→关评审→reload 零泄漏→业务态不变）；实跑 pass（20261015-p0-21-r1），不触发 hang 空票 |
| P0-22 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00723 | 备选·变更条件重析 | P0 | B | fresh 首发（新一代信息技术+②）→查看结果→返回配置改选「新能源」（只更新草稿 0 POST，与 00710/00711 互证）→显式重析（不同指纹合法新建、过程页「产业领域：新能源」重算）→查看结果双分支（本轮诚实空：无可见点边）+零残留（旧 task_id/INB1701/旧产业名）；实跑 pass（20261015-p0-22-r1，4 断言绿）；结果画布受 ENV-SVCGRAPH-HANG-EMPTY-001 约束走诚实空分支，不造伪数据不盲 skip |
| P0-23 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00728 | 异常·无效机构参数 | P1 | B | fresh 首发→查看结果落结果态→task_id URL 手工拼 org=INVALID-ORG-404（画布 hang 空无 org 入口，D1）→goto 冷加载（新标签页 as-built 等价）→12s 观察窗轮询；实跑 pass（20261015-p0-23-r1，4 断言绿）：「机构不存在或已下线」Message 命中 + org 清参 + 其余 query 全保留（task_id/view=result 在）+ 终态 .arco-drawer 不可见（count=0）；双分支兜底（静默清参 D1 pass / 残留无处理红挂 D3-SVCGRAPH-INVALID-ORG-UNHANDLED，本轮均未触发）；异常路径与画布渲染解耦，不受 ENV-SVCGRAPH-HANG-EMPTY-001 影响 |
| P0-24 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00724 | 备选·机构参数直达恢复 | P1 | B | fresh 首发（新一代信息技术+②）→查看结果落结果态→页内探有效机构标识（search/orgs keyword 轮询→items[].org_id→profile/get 验卡，isProfileCard 口径；_probe-p024 实证首候选 539d5a4e…be5 有卡）→task_id URL 手工拼 org=<有效id>（画布 hang 空无 org 入口，D1 同 P0-23 拼参口径）→goto 冷加载（新标签页 as-built 等价）；实跑 pass（20261015-p0-24-r4，4 断言绿）：抽屉开启（settle 后标题「机构画像：一禾亿株生物种业（深圳）有限公司」）+ URL org 参数保留（与抽屉开启态绑定，预期①联立）+ task_id/view=result 保留 + 正文基本信息呈现（机构类型/所在地/行业）；防御双分支：探不得有效 org→SKIP-SIGNAL 红显性化（人工核环境后转 n/a 挂 ENV-SVCGRAPH-HANG-EMPTY-001）；有效 org 被误清参/抽屉不恢复→红挂 D3-SVCGRAPH-VALID-ORG-NOT-RESTORED（本轮均未触发）；as-built 时序：加载期抽屉标题为 fallback=orgId hex，profile 返回后换机构名（r3 实证，断言先 settle 轮询再判，P2 跨 tick）；与画布渲染解耦，不受 hang 空票影响 |
| P0-25 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00720 | 主流程·影响力诚实缺失 | P0 | B | fresh 首发（新一代信息技术+②）→查看结果落结果态（统计面板 hang 空下仍渲染，与画布解耦）→定位统计面板影响力位→验红问号（.metric-spec-card.is-missing + aria=指标未登记：生态影响力 + rgb(245,63,63) 红 + 诚实文案「不输出影响力评分」）→hover 红问号验治理引用卡（未登记（治理引用：GAP-SVC-GRAPH-INFLUENCE）+ 计算公式/未登记，无伪 8 件套特征）；实跑 pass（20261015-p0-25-r1，3 断言绿，r1 一次过）；防御分支：位缺失/无红问号/伪评分/伪口径→红挂 D3-SVCGRAPH-INFLUENCE-MISSING-BADGE（D9 铁律，本轮未触发）；红问号挂评审层（reviewMode 默认开 + P0-21 同款自适应开启兜底）；hover 非 click 属 D1 记档（a-trigger trigger=hover，D9 组件族约定）；GAP 编号/Q-SVCCHAIN-03 命中现场记 observed；不受 ENV-SVCGRAPH-HANG-EMPTY-001 影响 |
| P0-26 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00718 | 主流程·网络密度统计 | P0 | B | fresh 首发（新一代信息技术+②）→查看结果落结果态→定位统计面板「规模与密度」卡可见子网密度位→读规模行 N/E 验密度值一致（N<2 诚实空态「子网过小，不计算统计值」/ N≥2 公式 2E/(N(N-1)) 重算对照 toFixed(3) 容差）→hover 密度数值验 tooltip「N=节点数，E=边数」与规模行一致；实跑 pass（20261015-p0-26-r1，3 断言绿，r1 一次过）：本轮 hang 空 N=0/E=0 → 密度诚实空态 + tooltip「N=0，E=0」（父单预判分支①空态字面满足）；防御分支：密度位结构缺失→红挂 D3-SVCGRAPH-DENSITY-MISSING / 空子网输出伪数字→红挂 D3-SVCGRAPH-DENSITY-DISHONEST（均未触发）；N≥2 数值分支已内置，hang 空修复后自动覆盖；metric_id 口径差 D1 记档（用例册 M_SVC_GRAPH_DENSITY vs 现场挂点 M_SVC_RELATION_DENSITY+Q062，命名未收敛不判红）；密度位锚定「可见子网密度」行（双密度并排卡为 Java 通道无 N/E hover 语义，记档）；与画布解耦不受 ENV-SVCGRAPH-HANG-EMPTY-001 影响 |
| P0-27 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00719 | 主流程·中心性 TOP5 统计 | P0 | B | fresh 首发（新一代信息技术+②）→查看结果落结果态→定位统计面板「度中心性 TOP5」卡→同源联立验排行与可见子网一致（空子网→诚实空态「当前子网无服务机构」无伪排行 / 数据态→≤5 行「序号. 机构名 度 N」降序、度≥1、Σ行度数≤2E 联立）→数据态点击首行机构名验下钻开 .arco-drawer 机构画像抽屉（空态无行可点按父单分支①如实降级，下钻能力由 P0-24 org 直达独立实证互证不吞并）；实跑 pass（20261015-p0-27-r1，3 断言绿，r1 一次过）：本轮 hang 空 N=0/E=0 → TOP5 诚实空态「当前子网无服务机构」无伪排行（_probe-p027 写前探针定局分支①）；防御分支：TOP5 卡缺失→红挂 D3-SVCGRAPH-CENTRALITY-MISSING / 空子网伪排行→红挂 D3-SVCGRAPH-CENTRALITY-DISHONEST / 有行下钻失效→红挂 D3-SVCGRAPH-CENTRALITY-DRILLDOWN-BROKEN（均未触发）；数据态分支已内置（hang 空修复后自动覆盖）；M_SVC_GRAPH_CENTRALITY（D1 draft/D4 mock）就绪度记档，TOP5 h3 挂 requirement_trace 非 metric_spec 属现场 as-built 不判红；与画布解耦不受 ENV-SVCGRAPH-HANG-EMPTY-001 影响 |
| P0-28 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00721 | 主流程·关系与节点类型过滤 | P0 | B | 历史种子深链（SVC-20260903-001，0 POST）→allow_skip 探测过滤区容器（svc-eco-clip-filters）→n/a；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（过滤勾选组挂 v-if=!parsed.empty，hang 空挡渲染——写前探针 _probe-p028 实证 fresh SVC-20260915-077 结果态 filters_count=0 + 画布诚实空态在屏 + 统计范围声明在屏；源码链归因 D4 环境债非 D3 结构性缺失：过滤 UI/URL eco_nk·eco_et·localStorage 双持久化/统计同源重算逻辑完备，P0-06/07/08 同构先例）；修复后自动转实全链已内置 expect[0..3]（结构+初始全选清参→取消边类型验勾选态翻转+eco_et 即时写+统计范围声明+E 不增→取消节点类型 eco_nk 同构→reload 参数逐字+勾选态逐项+规模行稳定保留）；防御票 D3-SVCGRAPH-FILTER-MISSING / D3-SVCGRAPH-FILTER-NOT-PERSISTED（转实后判定，当前不预开）；实跑 n/a（20261015-p0-28-r1，allow_skip 命中 + observed.yaml 双源证据）；「关系类型→边类型从属/参与/供应/依赖、旧四类为 EDGE_MAP 映射键」D1 记档 |
| P0-29 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00731 | 异常·分析失败态局部错误与重试 | P1 | B | graph 配置态选定产业+模式确认→route.abort 拦截创建任务 POST（断链 connectionreset，glob+尾段正则不误伤轮询）→点「开始分析」POST 恰被拒 1 次→失败态断言（.arco-alert Network Error/traceId 在屏非白屏 + 页面壳骨架四项含图谱滤镜 + 产业回显 + 模式选中态保留 + URL 停配置态不漂移 + 「开始分析」仍可用=重试承载）→unroute 恢复点「开始分析」重试（POST 200 落 view=processing 捕获 task_id + analysis_fp=svc\|graph\| 在 URL + 过程页产业上下文保留 + Network Error 清除）→停引导态收尾留证；实跑 pass（20261015-p0-29-r1，5 断言绿，r1 一次过）：与姊妹仓 chain-shortboard P0-17/FUNC-00706 同构（graph/chain 共用 useSvcAnalysisJob，失败态同为壳层 a-alert）——写前探针 _probe-p029 实证断链可触发（aborted=1）走父单分支①全链断言，不援引「开放项 3」skip；重试入口无独立「重试」文案、「开始分析」即承载 D1 记档；防御票 D3-SVCGRAPH-FAILURE-STATE-MISSING（吞错/白屏/丢壳形态，两轮均未触发）；详情/统计失败子块文案：失败发生在创建任务阶段无可采，记 observed（结果态判定归 P0-06/22 不吞并）；不受 ENV-SVCGRAPH-HANG-EMPTY-001 影响 |
| P0-30 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00729 | 异常·过滤后空结果提示 | P1 | B | 历史种子深链（SVC-20260903-001，0 POST）→allow_skip 探测过滤区容器（svc-eco-clip-filters）→n/a；skip ticket=ENV-SVCGRAPH-HANG-EMPTY-001（过滤勾选组挂 v-if=!parsed.empty 且空态承载 svc-eco-clip-empty 挂 clipEmpty=!parsed.empty && clipped.edges===0，hang 空下双双不渲染——写前探针 _probe-p030 实证 filters_count=0 + clip_empty_el_count=0 + hang 空文案在屏 + 统计位在场 0/0 诚实空态无 NaN；源码链归因 D4 环境债非 D3 结构性缺失：空态提示 UI 与过滤逻辑完备，P0-06/07/08/28 同构先例）；修复后自动转实全链已内置 expect[0..3]（基线归零（localStorage 残留守卫）→枚举收窄构造无命中边（节点单类→节点单类×边单类交叉；「全部边类型取消」不可用——setClip* 防全空回落全选、URL 拼参同样回落（resolveListedSelection hit=0 回落），D1 记档；枚举尽不可构造→P030-SKIP-SIGNAL 红显性化人工核后转 n/a）→空态文案「当前过滤条件下无关系数据」在屏+hang 空文案分支互斥→空态下勾选态/URL eco_nk·eco_et 保留→统计位 0/0 同源联立+密度位非 NaN 类非数字+清 clip localStorage（P8））；防御票 D3-SVCGRAPH-FILTER-EMPTY-HINT-MISSING（转实后判定，当前不预开）；实跑 n/a（20261015-p0-30-r1，allow_skip 命中 + observed.yaml 双源证据）；⚠ B 档 skip 占比 6/23≈26% 超配预警（上限 25%），对冲/改「声明不自动化」由父决定；「子网过小」正向断言与单节点构造归 00730 不吞并 |

## 本轮不自动化（声明 + ticket）

| 用例编号 | 原因 | ticket |
|----------|------|--------|
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00715 | ~~原声明不自动化~~ → **已由 P0-09 承载**（B 档 allow_skip + 同票，见主表） | `ENV-SVCGRAPH-HANG-EMPTY-001` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00716 | 机构节点下钻抽屉依赖画布服务机构节点可点击——画布 hang 空挡（filters_count=0、节点不可交互）不可构造 | `ENV-SVCGRAPH-HANG-EMPTY-001` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00717 | ~~原声明不自动化~~ → **已由 P0-11 承载**（B 档 allow_skip + 同票，见主表） | `ENV-SVCGRAPH-HANG-EMPTY-001` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00722 | ~~原声明不自动化~~ → **已由 P0-12 承载**（B 档 allow_skip + 同票，见主表） | `ENV-SVCGRAPH-HANG-EMPTY-001` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00730 | ~~原声明不自动化~~ → **已由 P0-13 承载**（B 档 allow_skip + 同票，见主表） | `ENV-SVCGRAPH-HANG-EMPTY-001` |

> 2026-10-15 父决策：以上 5 条不再写 case（「本轮后续叶或声明不自动化」取声明路径），ticket 与机检 skip 同挂 `ENV-SVCGRAPH-HANG-EMPTY-001`（P0-28/P0-30 探针实证 filters_count=0、画布诚实空态在屏）；修复该票后如需自动化另行立项，不计本轮分母。

未脚本化残留：**无**——原 5 条（00715~00717、00722、00730）已走上「本轮不自动化」声明清单，不再写 case、不扩大机检分母。注：00709/00710/00711 已由前波落 P0-03/P0-04/P0-05（cases 已存在，coverage 主表行由该波收尾补）；00724 已由 P0-24 承载（2026-10-15，org 直达恢复与画布解耦可实跑）；00720 已由 P0-25 承载（2026-10-15，统计面板与画布解耦可实跑，影响力诚实缺失红问号形态）；00718 已由 P0-26 承载（2026-10-15，密度位与画布解耦可实跑，N<2 诚实空态+N≥2 公式对照双分支，实跑 pass）；00719 已由 P0-27 承载（2026-10-15，TOP5 位与画布解耦可实跑，空子网诚实空态+数据态排行/下钻双分支，实跑 pass）；00721 已由 P0-28 承载（2026-10-15，过滤勾选组挂 v-if=!parsed.empty 被 hang 空挡渲染 → allow_skip n/a 挂 ENV-SVCGRAPH-HANG-EMPTY-001，修复后 expect 全链自动转实，写前探针 _probe-p028 双源证据）；**00731 已由 P0-29 承载（2026-10-15，route.abort 断链与画布渲染解耦可实跑——写前探针 _probe-p029 实证 aborted=1 失败态稳定复现，实跑 pass r1 一次过，与姊妹仓 P0-17 同构不依赖画布数据）**；**00729 已由 P0-30 承载（2026-10-15，过滤后空结果提示——过滤区与空态承载同挂 parsed.empty 前提被 hang 空挡渲染 → allow_skip n/a 挂 ENV-SVCGRAPH-HANG-EMPTY-001，修复后 expect 全链自动转实：枚举收窄构造无命中边（节点单类→节点×边交叉；全取消不可用因 setClip* 防全空回落，URL 拼参同样回落）→ 空态文案「当前过滤条件下无关系数据」在屏+分支互斥 → 勾选/URL 参数保留 → 统计位 0/0 非 NaN+清 clip localStorage（P8），写前探针 _probe-p030 双源证据 + 统计位当前态由探针承载；防御票 D3-SVCGRAPH-FILTER-EMPTY-HINT-MISSING / P030-SKIP-SIGNAL（数据形态不可构造，转实后才有判定机会）；实跑 n/a（20261015-p0-30-r1）；⚠ B 档 skip 占比 6/23≈26% 超配预警（上限 25%）——探针实证必须 skip 如实交卷，对冲/改「声明不自动化」路径由父决定）**。

## 收口纪要（2026-10-15）

- 父决策收口：剩余 5 条（00715/16/17/22/30）不再写 case，声明不自动化挂 `ENV-SVCGRAPH-HANG-EMPTY-001`（见上声明清单）；P0-30 保留，skip 超配（6/23≈26% 超 25% 上限）豁免记录于汇总表；用例册 5 行「自动化用例ID」列回填「声明不自动化：ENV-SVCGRAPH-HANG-EMPTY-001」；`cases/` 与 `index.yaml` 未动。入口闭环：机检 20（P0-01~08、P0-19~30）+ 声明 5 = 用例册 25 条（00707~00731）全覆盖。
