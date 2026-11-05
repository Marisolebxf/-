# LUMEN-INTEL-SDD-SIGNOFF-L01 · SYNTH SDD 四方会签（架构侧）

- 日期：2026-11-05
- claimed_by：`agent:arch-agent`（架构会签执行）；supervised_by：`human:徐滕强`
- claim_type：`coordinator_dispatch`（长任务总控 §A 段）
- Epic：E8-综合智能分析
- 审对象：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/`（总册 v1.0.5-draft + 三 L2 + reconciliation v1.0.4）
- 依据：`architecture-baseline.md` D1–D18 · `data-lineage-policy.md` v1.6（D9/D16）· `SYNTH-SDD-IMPL-长任务总控.md`（已拍板项不重开）· metric-registry MCP 实查（2026-11-05）
- 边界：只审详设；不写业务仓代码；不替算法/数据/产品拍板；不替甲方拍板 `Q-SYNTH-*`（全部保持 🟡）；不改 SDD 设计口径本身

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 状态 | in_progress → 本 handoff 落盘后转 integration（AV-0） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类：架构会签评审，不写代码；公约要求交付的 D1–D18 自检 / handoff / 待确认清单均已交付） |

## 一、范围与实现

四方会签代办（总册 §9 + 三 L2 §会签）中架构行已逐册落盘；同时以算法/数据/产品视角做合规性走查（只标矛盾与缺失，不替角色拍板）；blocked 项写明解锁条件；D1–D18 逐条自检。**不修改 SDD 设计口径本身**；发现的真矛盾以保留意见 + 待确认清单方式回写 handoff，留待对应角色确认。

### 1.1 逐册会签结论

| 册 | 稿本 | 架构结论 | 落盘位置 |
|---|---|---|---|
| 总册 `综合智能分析-系统详细设计说明书.md` | v1.0.5-draft | **可签**（附保留意见 AR-1~AR-7） | §9 会签·架构行 |
| `SYNTH-L2-VIT-AI-TABLES.md` | v1.0.5 | **可签**（附保留意见 AR-6） | §8 会签·架构行 |
| `SYNTH-L2-ELEM.md` | v1.0.5 | **可签**（附保留意见 AR-8） | §9 会签·架构行 |
| `SYNTH-L2-COLLAB.md` | v1.0.7 | **可签**（附保留意见 AR-9） | §9 会签·架构行 |
| `reconciliation/九叶功能覆盖矩阵.md` | v1.0.4 | 参照件，未单列会签表；发现旧口径残留见 AR-5 | 本 handoff |
| 附属 `调用链与边界.md` / `表落点与gapfill说明.md` | 对齐 v1.0.5 | 抽查无矛盾 | 本 handoff |

没有「不可签」册。v1.0.5 退回改稿已把上一轮架构硬伤（`*_ai` 落库、gapfill 图、权重常量、集群派生、服务端 PDF、depth/year 规划正文）全部收敛到合规口径。

### 1.2 指标就绪度实查（会签证据，metric-registry MCP 2026-11-05）

- SYNTH 域注册表共 **46 条**命中 `M_SYNTH`：D1 全部 `aligned`，D4 全部 `mock`（含上游 `M_SYNTH_182_1`–`191_1` 十条 MIXED）。
- SDD 总册 §5「指标库 SYNTH 域现 46 条，D1 全 aligned，D4 现多为 mock；缺 `M_SYNTH_ELEM_FOUR_DIM_SCORE`」**与注册表实查一致** ✅。
- ⚠️ 发现文档间矛盾：`客户决策清单跟踪表.md` Q-SYNTH-01 备注列写 `M_SYNTH_VIT_INDEX`（D1 missing）/ `M_SYNTH_VIT_INDICATOR`（D1 draft），与注册表实查（D1 aligned）不一致——客户决策清单备注为过时信息，以 MCP 实查为准；建议 PM retro 时修正该备注（本任务不改客户决策清单，避免越权）。

## 二、保留意见清单（AR-1 ~ AR-9，均不挡签）

| # | 册/位置 | 意见 | 建议 |
|---|---|---|---|
| AR-1 | 总册 vs `SYNTH-SDD-IMPL-长任务总控.md` §1.2 | 总控「已拍板项」仍写「库 `gkxlumenx_ai` + `gkxlumenx_gapfill`」，而 SDD v1.0.5 已废止 `_ai`、结果改落 `demo_gkxlumenx_ads`/`gkxlumenx_ads`。下游 agent 若先读总控会拿到旧库口径 | coordinator 更新总控 §1.2 一行字（`_ai` → ADS），并把 B/C/D 段厚包指向 v1.0.5 SDD；属文档同步，不是设计变更 |
| AR-2 | 总控 §4 金路径 #5 vs 协同册 v1.0.7 | 金路径故事 5 期望「默认三元组图谱 nodes/edges **非空**无重复」，但协同册现行口径是三窗 0 行空图 `reason=no_year_on_source`（源无年、禁灌演示行）。E1 冒烟按金路径跑必红 | 总控金路径 #5 期望改为「空图 + `no_year_on_source` + 无重复（有行时）」；非空验收移到 C-05 解锁后的 `COLLAB-C05-SRC` 验收单。同 TC-4 |
| AR-3 | VIT 册 §3 / 总册 §4 | 活力叶 `cache_key`（条件+profile 最新成功快照索引）没有像协同 `synth_collab_batch_meta` 那样的持久化落表；仅依赖任务链内存/任务表映射，重启后「按 cache_key 取最新」的行为未定义（指定 `snapshotId` 读旧批不受影响——ID 含批次） | 在活力实现单（`LUMEN-INTEL-VIT-FP-SNAP-L01`）明确 cache_key 的持久介质（复用任务表 or 补一张小 meta 表由 data-agent 评估）；若判定「重启后 404 引导重跑」可接受，写明即可 |
| AR-4 | 总册 §11.2 | 「保留最近 3 批，更早由清理任务删除（owner：data-agent）」只有一句；且清理旧批与「`snapshotId` 不可变、旧 ID 仍可读」存在张力——清理会让更早 snapshotId 失效 | 在 DDL 单（ELEM-DDL/COLLAB-DDL 范围）补清理任务定义：频率、按 `calc_batch_created_at`、保护被 `synth_collab_batch_meta` 引用的批次；「不可变」声明改为「保留期内不可变/可回溯」 |
| AR-5 | `九叶功能覆盖矩阵.md`（v1.0.4，2026-11-05） | 正文行残留 v1.0.5 前旧口径两处：①137 行「9 张 `_ai` 表（四维表注册后建）」「表结构预定义」——现行=ADS 8 张、四维连表结构都不预定义（只留候选方向给唐绍祖参考）；②139 行「gapfill node/edge（预填→C-05 换源）」——现行=ADS node/edge 本期 0 行、无 gapfill 图；③140/汇总「预填先行/就绪待实算」须按协同 0 行口径读 | reconciliation 由起草人出 v1.0.5 对齐版（不构成本会签前置；三册正文为准） |
| AR-6 | VIT 册 §2 | 五张表各自定义了「整批写/同批读」，但没写**跨表同批**的一致性要求：`synth_vit_index/dim_score/weight/rank/indicator` 同一 `calc_batch_id` 必须同批成功或同批失败，否则快照装包跨五表取「最新 succeeded 批」可能拼出半批 | 实现单验收加一条：seed 以同 `calc_batch_id` + 同 `calc_batch_created_at` 写五表；任一表校验失败整批同置 `failed`（等价于总册 §11.2「整批写」跨表推广） |
| AR-7 | 总册 §11.1 | 「指标结果（当前必建）17 张」按 DDL 建表口径成立，但**灌数预期不同**：活力 5 + 要素 8 预填 `is_mock=1` 有行；协同 4 张本期 0 行（源无年）。防实现单误读为「17 张全部要灌出行」 | 在 DDL 派单话术里写明「建 17 张、灌 13 张、协同 4 张本期 0 行」 |
| AR-8 | ELEM 册 §2 全景 | 要素全景（136）首版装包直查 DWD（多表聚合 + TopN），无超时/预算约定；默认三元组数据量大时快照首屏可能被拖慢（全景与三透镜共用 `batch-snapshot`） | 实现时预约定：全景聚合查询 timeout（如 3s）超时降级 `panorama=[]`+`reason=panorama_timeout`，不阻塞三透镜主区块；是否上缓存表仍按册「超时再议、另裁定」 |
| AR-9 | COLLAB 册 §2 batch_meta | `cache_key` 新批成功时「旧行 `is_latest` 置 0、新行置 1」跨行更新未约定事务边界；两个并发成功发布可能产生 0/1 竞态 | seed/发布侧同一 `cache_key` 的 is_latest 翻转包在单事务内（或 UPDATE...WHERE is_latest=1 原子改指）；DDL 唯一键已含 snapshotId 无冲突，仅执行顺序约束 |

## 三、待四方确认清单（TC-1 ~ TC-5；非架构可单方裁定项，留对应角色确认）

| # | 待确认 | 归属角色 | 说明 |
|---|---|---|---|
| TC-1 | 总控金路径 #5 期望改写（同 AR-2） | coordinator + 监管人徐滕强 | 涉及段 E 冒烟判定基线，须监管人确认改法 |
| TC-2 | 活力五表跨批一致性的实现单验收条款（同 AR-6） | 算法（seed 实现方）+ 数据（DDL） | 建议条款已给出，采纳与否由实现单认领时定 |
| TC-3 | 136 全景模块形态（工作台 Tab/卡片）与全景超时降级策略（同 AR-8） | 产品 | 册内已标「产品确认形态」；超时降级建议需产品认可「全景失败不阻塞三透镜」 |
| TC-4 | 总控金路径 #5 与协同空图口径对齐（同 AR-2/AR-5③） | coordinator + 产品 | 与 TC-1 同一件事的文档面 |
| TC-5 | 算法/数据/产品三行会签 | 算法 lead 唐绍祖线 / data-agent / 产品 | 本 handoff 只完成架构行；四方齐才达 SIGNOFF done（总控 §A 段状态门） |

## 四、blocked 项与解锁条件（不挡会签）

| blocked 项 | 现状 | 解锁条件 | 解锁后动作（已按总控 §E 排单） |
|---|---|---|---|
| 137② 要素四维打分 | `M_SYNTH_ELEM_FOUR_DIM_SCORE` 未注册（MCP 实查确认），公式五要素未定稿 → 不建表、不灌数、不出数；接口 `evaluationDimensions=[]`+`reason=metric_not_registered`；FE 红问号缺失态 | `human:唐绍祖` 完成公式五要素定稿（指标体系/公式/归一化/权重/缺失规则）→ METRIC-OPEN 注册 → D1 aligned | `FOURDIM-OPEN → FOURDIM-DDL → FOURDIM-WIRE`：注册 → 建 ADS 表 `synth_elem_four_dim_score`（走 ADS 结果表，非 gapfill）→ FE 接线断言切换 |
| 139/140/141 图谱与协同真值（C-05 贴源） | 联合专利/合作项目/人才流动源无年份维度，1y/3y/5y 窗三窗空图；node/edge 本期 0 行；`synth_collab_*` 指标行不灌 | C-05：①源侧提供关系事件年份/时间戳；②产业 taxonomy 与主体标签映射核验；③贴源报告 + readiness matrix 闭合（GDF + data-agent） | `COLLAB-C05-SRC`：换源实查写入 node/edge、灌 `synth_collab_*` 指标行、图谱非空验收（届时金路径 #5 原期望恢复） |

以上 blocked 均为「外部条件未满足的诚实空态」，不违反 D18：空态是**读 ADS 表后的结果**（表已建、代码路径真实 SELECT），不是接口写死 JSON。会签不因 blocked 项保留。

## 五、产物清单

- 总册会签·架构行（§9）：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/综合智能分析-系统详细设计说明书.md`
- VIT 册会签·架构行（§8）：`sdd/l2/SYNTH-L2-VIT-AI-TABLES.md`
- ELEM 册会签·架构行（§9）：`sdd/l2/SYNTH-L2-ELEM.md`
- COLLAB 册会签·架构行（§9）：`sdd/l2/SYNTH-L2-COLLAB.md`
- 本 handoff：`agent-delivery/agent-handoffs/LUMEN-INTEL-SDD-SIGNOFF-L01.md`
- git：上述 5 个文件，commit 不 push（交 coordinator 统一推）

## 六、验收证据

- metric-registry MCP 实查（2026-11-05）：`metric-query(q=M_SYNTH, domain=综合, limit=60)` → 46 条，D1 全 aligned、D4 全 mock，`M_SYNTH_ELEM_FOUR_DIM_SCORE` 不在列——SDD §5 / ELEM §4 挂接表与注册表一致。
- `客户决策清单跟踪表.md` Q-SYNTH-01/02/03/C-01~C-05/E-02/V-01/V-02 均仍 🟡：SDD 未拍板任何 Q-SYNTH-*，合规（§四 blocked 与 §三 TC 不含口径拍板）。
- 四册会签表 grep 核验：架构行已落、算法/数据/产品行保持「未签」原状（ELEM 册算法行保留「137② METRIC-OPEN 注册：唐绍祖牵头」原注记）。

## 七、架构合规自检（D1–D18 逐条）

> 范围=SDD 四册设计稿（非代码）；「✅」=设计稿合规，「➖」=本 SDD 不涉及该维度，标注理由。

| # | 决策 | 结论 | 依据（SDD 落点） |
|---|---|---|---|
| D1 | Java 聚合拓扑方案 A（共享 `gkxlumen-topic`/`metrics`） | ✅ | 总册 §3：FE→gateway→`gkxlumen-topic`/`topic-async`→Python `/internal/*`；只走专题链，未另造独立算法调用 |
| D2 | 算法库统一出口（注册后经 `/internal/*` 调用） | ✅ | 总册 §5：21/22 挂库指标；缺的第 22 条（四维）明确「未注册不接数、不派实现单」；`legacy_unknown`/`weight_profile` 属同核已注册指标装包，不新增未注册算法 |
| D3 | 契约面=ADS；Java 只读；Java 不写 ADS | ✅ | 总册 §11：结果/图事实/batch_meta 全在 `demo_gkxlumenx_ads`/`gkxlumenx_ads`；Java 只透传+装包代理，读 ADS 发生在 Python 侧 |
| D4 | 双前端职责切分 | ➖ | 本 SDD 仅 lumen-ui-topic；未引入展示侧页面 |
| D5 | 网关路由划分 | ✅ | 全部走 `/topic/**`（同步快照/图谱查询）与 `/topicAsync/topic/v1/analysis/tasks`（异步） |
| D6 | 横切统一（OTel / NebulaGraph 协议 / 缓存键） | ✅/➖ | 总册 §3「Java 不写 nGQL」+协同册 §1「不做 Nebula 导出」：本期图谱读 ADS 事实表、不经 Nebula，不违 D6（未来换源若走 Nebula 再按 graph-engine 评审）；观测三册 §观测 均有埋点/trace 要求 |
| D7 | 数据契约先行 + Mock 先行（Python 写 Mock 至 ADS） | ✅ | D18 模式：entan-py 灌 `is_mock=1` 行进 ADS；`USE_MOCK=false` 禁前端 fixture（总册 §8） |
| D8 | 前端规范唯一来源（Design.md/Arco） | ➖ | 本 SDD 为后端+表+契约详设，页面差距审计仅登记 FE 待办（136 全景区/139 industry 控件），不涉及视觉 token；FE 改造单另带 §14 对照 |
| D9 | 数据血缘（8 件套 / ⓘ / 🧪 / 就绪度只读） | ✅ | 三册 METRIC 表全部只读消费注册表状态；`is_mock=1` 行页面 🧪；D4 改 live 条件=实算+缺项闭合（VIT 册 §4 / 总册 §11.5）；未自填就绪度 |
| D10 | 交互规范唯一来源 | ➖ | 同 D8；SDD 未定义新交互模式，137② 红问号缺失态符合血缘规约 D1 missing 图标语义 |
| D11 | demo-ui-system-test 豁免 | ➖ | 未涉及该仓 |
| D12 | demo/lumen 隔离 | ✅ | 总册 §3 明令禁止 Feign/helm/前端指向 `demo-*`；实现全部在 `lumen-algo-py`(`vendor/entan-py`)/`lumen-svc-platform`/`lumen-ui-topic`；无 merge demo→lumen |
| D13 | Kafka 消息总线 | ✅/➖ | 异步任务回传沿用既有 `#102–#109` 链路（topic-async-service），SDD 未新增消息语义，未触碰 RabbitMQ |
| D14 | 对象存储桶 | ✅/➖ | 报告=前端快照渲染 PDF 本地生成，服务端不写文件存储（协同册 §3.3），不触碰 RustFS；LLM 策略无表无文件 |
| D15 | 展示 Python 门面独立 | ➖ | 本 SDD 全部走专题链（gkxlumen-topic→entan-py），不经 show-service |
| D16 | gapfill 边界 | ✅ | `gkxlumenx_gapfill` 只保留活力既有 3 张输入缺项（表落点说明 §2）；废止 gapfill 图；「全景 DWD 直查无表」「四维不建表」未新造 gapfill；D16「缺项闭合+实算后 D4 改 live」已写进总册 §11.5 |
| D17 | 合规/合理（唐绍祖锁定闭包） | ➖/✅ | SDD 未触碰锁定闭包与 `-合规/-合理` 成对改名场景；活力三档权重为已注册口径并存，非锁定闭包修改 |
| D18 | 架构签收=可实现（新建 ADS 表+Python 灌行+接口读表；禁写死 mock） | ✅ | 每张表写明表名/灌数方（entan-py seed）/读取接口（`/topic/v1/synth/**` 与 `/internal/v1/synth/**`）——D18 三要素齐；禁止接口写死 JSON、装包禁权重常量、缺行 null+reason（总册 §8/§11.4）；空图/空态是读表结果；v1.0.5 已废止 `*_ai` 自我豁免与「接口动态推导 mock」残留 |

**结论：0 项违反。** 重点四条铁律复核：①调用链无越层 ✅；②Java 零算法/零 nGQL/零写 ADS ✅；③图谱本期不涉 Nebula 写、读 ADS 事实表 ✅；④D16/D18 边界清晰、无「接口直接返回写死 mock」路径 ✅。

## 八、遗留风险

- 三行会签（算法/数据/产品）未齐前，SIGNOFF 不 done，B/C/D 段 DDL 不能开工（总控 §A 状态门）——本 handoff 不解除该门。
- AR-1（总控 `_ai` 旧口径）若不同步，下游 coding agent 有拿到旧库口径的现实风险，建议 coordinator 在升 B/C/D ready 前完成一行字修订。
- AR-2/TC-1 若不修订，段 E1 金路径故事 5 必红；失败分类会走 C1 派修浪费一轮。
- `synth_collab_batch_meta` 是协同叶「重启后按 snapshotId 恢复」的唯一真源，其落表时机（发布成功即写）与「缺任一列不得标 succeeded」约束在实现时须自检脚本断言（协同册验收 3 已含）。

## 九、CI/CD

- 分支：`origin/dev`（gkx-orchestration）
- commit：本次文档 commit（hash 见任务回复；不 push，交 coordinator 统一推）
- pipeline：无业务 CI（设计类 `cicd: skip`）；编排仓无 K8s rollout

## 十、涉及文件

- `agent-delivery/agent-handoffs/LUMEN-INTEL-SDD-SIGNOFF-L01.md`（本文件）
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/综合智能分析-系统详细设计说明书.md`（§9 架构行）
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-VIT-AI-TABLES.md`（§8 架构行）
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-ELEM.md`（§9 架构行）
- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-COLLAB.md`（§9 架构行）
