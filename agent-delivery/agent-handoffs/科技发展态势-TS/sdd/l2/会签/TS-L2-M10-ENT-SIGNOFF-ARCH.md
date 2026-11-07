# TS-L2-M10-ENT-SIGNOFF-ARCH · 维护管理 · 关键实体与关系 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-07
- 对象：`TS-L2-M10-ENT-ARCH`（定义稿，2026-11-07 落盘，待架构、接口、算法、数据四角色会签）
- 对照：`SCI-INT-A03.yaml` write_back_design_draft + cards（卡 200–221）· `SCI-INT-A03.md` §6/§7 · 对照文档 A.3.1/A.4 · `architecture-baseline.md` D2/D3/D7/D12/D15/D18、§2.2 · `data/data-design/storage/README.md`（决策 #7、写者表 L92）· SRS `科学技术全景.md` 序 41–47（L365 起）
- 监管：`human:刘剑锋`
- 范围：只读核对，不改被审稿，不动 task-registry / WBS，不 git commit/push。格式对齐 `TS-L2-M10-LAYER-SIGNOFF-ARCH`（2026-11-06）先例

## 结论

**有条件同意会签**。核心链路（FE → Java 门面 topic 侧 → Python 单写者 → 主表/变更集三表 → Nebula gkx_chain + ADS 投影）、OI-A03-01 两档拆解方向、G1–G5 裁定主体、与 LAYER 的模式区隔均成立；A03 草案转述基本忠实（一处端点转述偏差 + 一处 LAYER 模式表述瑕疵，见事实备注）。以下 5 条条件不要求改被审稿正文（C1 含一处 draft 图加注），均为会签边界与后续单动作；条件闭合前本稿不标 done：

| # | 条件 | 责任落点 | 时点 |
|---|---|---|---|
| C1 | **对外路径与 D15 调和必须显式闭环**：SEQ 图 `fe → gw → javaf` 直调 `POST /topic/v1/tech/graph/changes`，无 display BFF 节点，与 D15「展示聚合 BFF `/display/v1/**` 单入口」及 D4（science-pc 走 `/display/** + /innov`）字面冲突；且同一 M10 页面 LAYER 分区对外走 `/display/v1/situation/maintain/**`，同页两分区两种入口风格。此为沿袭详设 11 §11.1 / OI-A03-06 的既定未闭冲突，本会签不替拍板，但**按图即契约**（LAYER C3 先例）SEQ 图现状会被误实现为展示前端直调 topic 路由。要求：(a) `display` BFF 代理/Feign 聚合到 topic 领域服务（D15 全链，LAYER 同构），或 (b) 详设 11 口径升级为基线注记（展示维护页直调 `/topic/v1/{element}/graph/**` 例外 + 网关/鉴权/trace 一致性说明）。闭合前 SEQ 图对外路径边加注「draft，门面层级待 OI-A03-06/DN-07」 | ARCH 稿维护方加图注（draft 图一处注记，不动正文）；路径终裁随 DN-07（human:李伟）+ OI-A03-06 | API 分册（`TS-L2-M10-ENT-API`）路径冻结前 |
| C2 | **VID 新旧并存的读侧口径必须定义，不允许无映射双写**：存量技术点 VID=`tech:{名称}`（存量边挂其上），首版增量按 `tech:{technology_id}` 写——对**存量技术点**做挂接/属性编辑时若按新规则 UPSERT，同一逻辑技术点将出现双节点（旧名称 VID 持有 105 自动边、新 ID VID 持有人工增量边），读侧（序 41 推荐 / 全景现状 / impact 预检）不合并即漏数/重复。稿 §2 注记只划了写侧「存量边不迁移」，未定义读侧合并与 hang/update 目标 VID 解析。要求 API/DATA 分册给出：对存量技术点的操作按其现行 VID 写边（或单点 VID 切换），并定义新旧 VID 读侧 union 口径。另：D6（2026-10-15）现只重灌 `demo_gkx_chain`，稿写回目标写正式 `gkx_chain`——首版联调 space 落点与 space 可配置须在 DATA/实现单明确 | `TS-L2-M10-ENT-API` / `TS-L2-M10-ENT-DATA` 起草时定，报监管人 | API/DATA 分册冻结前 |
| C3 | **A03 草案消费标记**：`write_back_design_draft` 头部自标 `status: draft（未评审；不是定论…）`，本稿将其升级为正式架构后，须在 A03 签收/归档环节加一行消费注记（「已被 TS-L2-M10-ENT-ARCH 采纳升级，2026-11-07 架构会签」），防止双真源漂移（一处读来未评审、一处已是正式架构）。不要求改本稿，也不改 A03 卡片实质内容 | A03 签收环节（PM/product-agent）或 ENT-API 引用时注记 | A03 任务签收前 |
| C4 | **序 42 自动建联缺口登记**：SRS 42 明文「添加的实体自动与相关技术节点建立关联关系，系统智能计算关联强度」，G2 首版不做 → 首版挂接后新实体在全景图中孤立，需用户手动建联；demo 演示态（maintainModel 添加即带 strength）反而有自动建联观感，验收易起争议。须 PM 在客户决策清单/验收口径登记该缺口（依赖 JX-A03-03，本来全部待确认，首版不做现实成立）。同时 G4 行只列 `sortBy`，SRS 41 字面还要求类型筛选与搜索——A03 卡 216 契约草案已含 `entity_types/keyword/time_range` 全参数，API 分册沿卡 216 全参数实现即可，勿按 G4 行截窄 | PM 登记缺口；API 分册沿卡 216 | API 分册冻结前 / 验收口径确认前 |
| C5 | **41 首版数据策略与 D9 裁定显式化**：(a) 105 未交付时推荐列表二选一——空态 + PendingBadge（A03 卡 216 test_points 原文，零 mock，合规）**或** D18 mock 替代（新建 ADS 表 + Python 灌数 + Java 只读 + MockBadge 三要素补齐进稿），不得隐式；(b) METRIC 分册不得按 §6「全 N/A」了事——卡 216 test_points 已明确「关联强度旁 ⓘ 指向 M_TECH_GRAPH_105_1，D4=mock 显示 MockBadge」，strength 是用户可见数值，倾向沿 A03 挂 `M_TECH_GRAPH_105_1` 走 D9 八件套 | METRIC 分册（`agent:algorithm-agent`）+ API 分册 | METRIC 分册标 done 前 |

## 逐关注点核对（任务书审查重点 ①–⑦ / 稿 §7 ①–⑥）

| # | 关注点 | 架构表态 |
|---|---|---|
| ① | A03 草案升级引用的正当性（draft 未评审被采纳为正式架构） | **成立，附 C3**。分两层：(a) **技术形态层**（四段链、Python 单写者、三层 auto/manual/published、字段级合并、乐观锁 409、projection_pending 补偿、反向变更集回滚）——这些是技术决策，属架构角色权限；本项目评审机制即「四角色会签 + 监管人签收」（LAYER 先例同款），本会签 + `human:刘剑锋` 签收即构成事实上的评审闭环，无需 A03 先单独过评。(b) **未决项层**——结构项 OI-A03-05（写者归属 DN-07）与口径项（9 条 DN/OI）不因本稿采纳而视为已决：稿 §7-5 明确 DN-07 未定只锁「topic 侧」、§2 待拍板档列全 6 项且声明不替甲方拍板，与 A03 原规划升级路径（结构项→human:李伟、口径项→甲方）不冲突。**结论：采纳动作合规，但要 C3 的消费标记防状态漂移**。范围核对：稿声明消费「18 张写回卡 + 三要素卡，ready_to_sign」与 A03 handoff §1/§5（22 卡、18 张 write_back、ready_to_sign）及 registry 状态一致 ✓ |
| ② | OI-A03-01 分档可行性（自建主表先行 / 甲方拍板） | **方向成立，附 C2**。返工风险可控：C02 结论「当前无人持有主数据」+ 草案推荐我方自建（选项 A），若甲方最终选 B（久新持有），草案已预留 `jx_tech_id→technology_id` 映射层，自建表降级为映射/投影中间层不白做；变更集三表/版本/审计无论选项 A/B 都需要。改名不换 ID + redirect（C02 id_alignment_draft.versioning）覆盖合并/拆分；条件化要求：主表设计留外部 ID 对齐字段 + redirect 表，写入实现单（并入 C2 的 API/DATA 动作）。VID 增量不迁移边界的技术风险实在（存量技术点双节点、读侧漏数），稿只划了写侧边界没划读侧口径 → C2 |
| ③ | §1 四段链与 D2/D3/D7/D15 自洽（Java 零写 nGQL、display 不直连） | **主体成立，附 C1**。storage 真源（README L92：Nebula 写者 Python，Java 禁直连 nGQL；决策 #7：一张 G 正式 `gkx_chain`）与稿一致 ✓；稿 §1 图 `javadoc（零写 nGQL）`、`py（单写者）`、Java 读只走 ADS 投影或经 Python 查图——D3 字面「仅读 `*_ads`」由 D15「领域服务 Feign 调 Python 算法层是合规路径」覆盖 ✓；D2 不误引（图谱写回是数据操作非算法调用，未来 G2 智能关联接入时才需注册出口）✓；D12 链路无 demo-* ✓。**唯一张力在 D15 入口层级**：稿跳过 display BFF 直调 `/topic/v1/**`（沿袭详设 11/OI-A03-06 未闭冲突，非本稿新引入），§5「display 不直连 Python（D15，ENT 走 topic 侧）」是对 D15 的窄用——D15 原文允许的恰恰是 display→Feign→领域服务→Python 全链 → C1 |
| ④ | G1–G5 裁定合理性 | **G1/G3/G4/G5 成立，G2 成立但须缺口登记（C4）**。G1 补 strength_manual+time_range 与 SRS 46 字面（类型/强度/时间范围）对齐 ✓；G3 ops[] 天然批量 + validate 预检统计覆盖 SRS 47「预览+结果统计」✓；G4 排序做 ✓ 但须沿卡 216 全参数（筛选/搜索，C4 后半）；G5 键盘通道不涉后端成立——按 §1「编辑在会话」，Delete/Ctrl+Z/Y 作用于会话内撤销栈与未提交状态，无需后端变更，归接线单无后端依赖漏项 ✓。G2 首版不做的依据（Python 无模型、JX-A03-03 待确认）真实，但 SRS 42 字面不满足且 demo 有自动建联观感 → C4 缺口登记，防验收争议 |
| ⑤ | §6 D18 核查表逐叶齐备性 | **42–47 齐备，41 附 C5**。写目标（op 名逐叶明确）、写者（§1 Python 单写者 + §2 首版档三表+主表）、接口（`POST /topic/v1/tech/graph/changes` + `GET .../impact` + `changes:validate`）三要素在稿内可拼齐 ✓；ADS 投影表 graph_node/graph_edge 与 A03 一致 ✓。41 读叶缺首版数据策略：105 未交付时「空态+PendingBadge」或 D18 mock 表三要素未显式二选一（卡 216 有降级契约但稿未引）→ C5(a)。另稿预期「全 N/A」与卡 216 D9 处理（ⓘ+MockBadge 挂 M_TECH_GRAPH_105_1）矛盾 → C5(b) |
| ⑥ | 两图与正文一致性 | **基本一致，附 C1 + 两条备注**。SEQ 图读写双边、节点职责与 §1 要点 1–5 一致 ✓；DATA 图 merge 优先级简写「manual>tombstone>auto」与 §1 要点 3 语义一致（图注简写可接受）✓。偏差：(a) SEQ 图对外直调 topic 无 display 节点 → C1；(b) SEQ 图 Python 端点 `/internal/v1/tech/graph/changes` 漏 `sci` 段（A03 原文 `/internal/v1/sci/tech/graph/changes`，yaml L62）→ 事实备注 R1；(c) DATA 图 `cs → pub → merge → published` 把发布画在 merge 之前，A03 草案语义是发布时 merge(auto run, manual)——效果等价（发布=merge+投影），非阻塞，API 分册行文时统一即可 |
| ⑦ | 事实错误给证据 | **无实质性事实错误**，两处轻微瑕疵见下「事实备注」R1/R2；范围引用（序 41–47 七叶、34–40 划掉、FE-TS-10A 锁定不重做）与 SRS 原文、对照文档 A.3/A.3.1、registry note 逐条对得上 ✓；§0 逐叶裁定与 SRS 41–47 功能描述逐条比对无错配（43「保留在推荐列表」= unhang 摘挂语义正确，卡 205 同款；45 三方实体覆盖层 = DN-A03-04 口径正确）✓ |

## D18 逐叶核查（稿 §6）

| 叶 | 裁定 | 写目标 | 写者/接口 | 判定 |
|---|---|---|---|---|
| 41 | 真读 | ADS 投影 / Python 查图 | Java GET（topic 侧，路径 API 冻结） | 附 C5（首版数据策略 + D9 裁定） |
| 42 | 真写 | hang_entities | `POST …/graph/changes` | 齐备；G2 缺口 → C4 |
| 43 | 真写 | unhang_entities / delete_node cascade | 同上 + `GET …/impact` | 齐备（impact 预检接口在 §0/§6 两处一致） |
| 44 | 真写 | delete_edge | 同上 | 齐备 |
| 45 | 真写 | update_node patch（三方实体=覆盖层） | 同上 | 齐备（DN-A03-04 口径正确挂待拍板档） |
| 46 | 真写 | update_edge（含强度/时间） | 同上 | 齐备（G1 补齐） |
| 47 | 真写+读 | ops[] 批量 + validate | 同上 + `changes:validate` | 齐备（G3） |

注：本二级写路径为真实图谱写回（非 mock 场景），D18 替代条款仅在 41 读叶的 105 未交付场景触发 → C5(a) 二选一。

## 链路与铁律核对

| 项 | 判定 |
|---|---|
| 调用链四段（FE → gw → Java topic 侧门面 → Feign /internal → Python 单写者 → 主表/Nebula/ADS） | 与 A03 卡 call_chain、storage 真源一致 ✓；对外入口层级待 C1 闭环 |
| Java 零写 nGQL / 不直连 Nebula；读只走 ADS 投影或经 Python | D3/D15 + storage README L92 ✓ |
| D12：无 demo-* 依赖；34–40 不做；FE-TS-10A 锁定期不动 maintain 目录、接线单只改数据源 | 与对照文档 A.3.1 边界、A.4 备忘一致 ✓ |
| D13/D14/D17：无消息总线、无对象存储、不触算法闭包 | ✓（稿内无相关引入） |
| 与 LAYER 模式区隔（图谱写回 vs 业务库配置 CRUD，两套不混用） | 成立——LAYER v3 终版为 cfg_* 四表 Java 直读直写（LAYER-ARCH §3/会签 v3），ENT 走 Python 单写者图谱链，区隔论点不受 LAYER v3 演变影响；表述瑕疵见 R2 |
| 「一张 G」作用域（OI-A03-03）未替拍板 | ✓ 稿 §2 待拍板档在册（写回 gkx_chain 与专题共图的影响留 DN-A03-07） |

## 事实备注（非阻塞，不改正文）

1. **R1 端点转述偏差**：稿 §1 SEQ 图 Python 端点 `/internal/v1/tech/graph/changes`，A03 原文为 `/internal/v1/sci/tech/graph/changes`（`SCI-INT-A03.yaml` L62；cards 内部链同）。路径均 draft、API 分册冻结时收敛，但属转述不忠实，稿维护方顺带修正。
2. **R2 LAYER 模式表述**：稿首段「LAYER 是业务库配置 CRUD（cfg_* 四表 + cms）」——LAYER 四稿及会签仅涉 cfg_* 四表，无 cms 表述出处（疑为 cfg_tech_datasource 的 CMS 类数据源联想）。区隔论点不受影响，建议删「+ cms」。
3. **R3 合并规则双重身份**：§1 要点 3 将 manual > auto 采纳为正式，§2 又把 DN-A03-03（人工 vs 104/105 优先级）列待拍板档——机制（可配置 merge）已定、参数（优先级方向）待甲方，不矛盾但建议实现单把合并优先级做成显式配置项，避免拍板后改正文。

## 签收边界

- 本页是架构角色会签，不把本稿、不把任何任务标 done；签收仍由监管人 `human:刘剑锋` 做。
- 留 API/DATA 分册：C1 路径终裁（随 DN-07/OI-A03-06）、C2 VID 读写口径与联调 space、C4 后半（沿卡 216 全参数）、C5(a) 41 数据策略、R1 端点收敛。
- 留 METRIC 分册：C5(b) strength 的 D9 裁定（沿卡 216 挂 M_TECH_GRAPH_105_1）。
- 留 PM/客户决策清单：C4 前半（序 42 自动建联首版不做缺口登记）；C3 的 A03 消费注记随 A03 签收环节。
- 留实现单：主表外部 ID 对齐字段 + redirect 表（② 的返工护栏）、合并优先级配置化（R3）、C2 的 space 可配置。
- C1–C5 不要求改被审稿正文；C1 的图注与 R1/R2 是 draft 稿/图顺带修正，由稿维护方在 API 分册引用前完成。
