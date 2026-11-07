# TS-L2-M10-ENT-SIGNOFF-DATA · 维护管理 · 关键实体与关系 · 数据会签

- 角色：`agent:data-agent`（数据角色会签人）
- 日期：2026-11-07
- 对象：`TS-L2-M10-ENT-ARCH.md`（主审 §1/§2/§4/§6）；交叉核对 `SCI-INT-A03.yaml` write_back_design_draft（:25–116）与 cards（seq 41–47、INT-A-TECH-203）、`SCI-INT-C02.yaml` INT-C-TECH-180/181/182（:4465–4718）、`data/data-design/storage/README.md`、`TS-L2-M10-LAYER-DATA.md`（分区1 对照）
- 监管：`human:刘剑锋`
- 范围：**只读核对**。不改被审文件，不动 task-registry / WBS，不建库、不建表、不灌数，不 git 提交
- 结论：**有条件同意**（必修 2 项 + 边界补强 1 项 + 事实修正 3 处，见 §0）

## 0. 结论与条件

**有条件同意。** 架构方向正确：消费 A03 写回链路不重造、Python 单写者、Java 只读 ADS、不建 cfg_ 与分区1 区隔干净、回滚走反向变更集不物理覆盖——以上全部与存储真源（`storage/README.md` 决策 #7 / §5 职责矩阵）和 A03 草案一致，数据视角无架构性反对。但稿作为 DATA 分册的直接上游，**存储落点信息有缺口**，须补齐后才可转「同意会签」：

| # | 级别 | 条件 | 证据 |
|---|---|---|---|
| C1 | 必修 | **store 表清单漏 2 张运行必需新表 + Demo 落点缺失**。§1 图 store 节点只列「graph_change_set/log/version + 主表 + Nebula gkx_chain + ADS 投影」（`TS-L2-M10-ENT-ARCH.md:39`），但正文自己引用的两个机制没有物理落点：① tombstone（墓碑标记，人工删除后阻止自动层复活）——§4 图与 §1 要点 3 都依赖它，A03 明确「manual 层 tombstone 表（新）」（`SCI-INT-A03.yaml:272`）；② 冲突队列（自动层新值撞人工覆盖时挂起待人工确认）——§1 要点 3 依赖，A03 merge_rule「进冲突队列待人工确认」（`SCI-INT-A03.yaml:56`）。DATA 分册按 §1 清单定建表范围会漏建。另：全文只写 `gkx_chain`，未写 Demo 落点 `demo_gkx_chain`（storage README 决策 #7 与 A03 premise 均有，`SCI-INT-A03.yaml:29`），P2 联调在 demo 环境，落点不能缺。改法：§1 store 节点与 §6 补「tombstone 表（node/edge 两类）+ 冲突队列承载（形态待 DN-A03-03）+ Demo=demo_gkx_chain / demo_* 实例」 | ENT-ARCH:39 vs A03:272/:54–56；storage README:20/:95–106 |
| C2 | 必修 | **§2 首版档隐含掉写者归属决策（OI-A03-05/DN-07）**。首版可做档声称「仅需本叶会签确认自建先行，不需甲方」（`TS-L2-M10-ENT-ARCH.md:58`），但变更三表/主表**落哪个库、谁建 DDL、谁写**取决于 OI-A03-05：由 Python 写（推荐，单写者）还是 Java 业务库（需李伟裁定，DN-07）（`SCI-INT-A03.yaml:114`、`:51`）。这是李伟的结构裁定不是甲方决策，放在两档之外就成了悬空前提；若李伟裁向 Java 业务库，三表库名/写者/DDL 归属全变，首版返工。改法：首版档显式加一句「按 A03 推荐方案 Python 单写者 + 我方数据域库先行；DN-07 若推翻则迁移（成本=三表搬库）」。§7 关注点 5 只把 DN-07 标在门面模块（:112），与 A03 的 DN-07 双义用法（门面落点 `SCI-INT-A03.yaml:136`/`:1099` + 写者归属 `:51`/`:114`/`:504`）对不上另一半，建议两条都列 | ENT-ARCH:57–58/:112 vs A03:51/:114/:504/:136 |
| C3 | 边界补强 | **VID 并存（重点 ④）稿的边界只覆盖了写侧自身，四个交叉点不够 DATA 分册落地**（详见 §4）：读侧合并策略、impact 预检口径、新建查重是否扫存量图、auto 层 Job 首版行为。建议在 §2 注记下显式裁定或声明兜底（如「首版读侧仅见增量边」）。另注意：A03 OI-A03-02 原文是「写回上线前**须切** tech:{technology_id}（C04）」（`SCI-INT-A03.yaml:111`），本稿实质放宽为「首版增量先行、全量切换留 C04」——属边界演进而非沿用，§7.4 列会签是对的，本会签在 §4 给出数据视角的确认意见与附带条件 | ENT-ARCH:61 vs A03:111 |

事实性修正（随稿纠错，非阻断但应改）：

| # | 修正 | 证据 |
|---|---|---|
| F1 | Python 内部路径少了 `sci` 段：稿 §1 图写 `POST /internal/v1/tech/graph/changes`（`TS-L2-M10-ENT-ARCH.md:38`），上游 A03 全部卡与 flow_draft 均为 `/internal/v1/sci/tech/graph/changes`（`SCI-INT-A03.yaml:62`/`:137` 等 10+ 处）。稿自称「全部沿 A03 草案」，路径引用应一致（最终冻结归 API 分册） | ENT-ARCH:38 vs A03:62/:137 |
| F2 | §13 行「LAYER 是业务库配置 CRUD（cfg_\* 四表 **+ cms**）」——LAYER 四份分册（ARCH/DATA/API/METRIC）grep 无任何 cms 表述，「+ cms」无出处，建议删 | ENT-ARCH:13 |
| F3 | §3 G4 排序参数写 `sortBy=strength\|time`，A03 INT-A-TECH-210 请求为 `sort_by(strength\|time\|name)`，少 name | ENT-ARCH:70 vs A03:712 |

C1/C2 回填后由 data-agent 在本页追记一行确认即可转「同意会签」，无需重开签。

## 1. 库归属与写者（审查重点 ①）

**现状**：§1 store 节点与 §6 表格只写「MySQL 变更三表 + 主表」，**库名一律未写**。核对上游：

- A03 master_data_ownership「变更集/修改历史/版本/审计」：我方新表（名待定），写者=Python（单写者），decision=DN-07（`SCI-INT-A03.yaml:49–51`）
- C02 INT-C-TECH-180 技术点主表：「项目 DWD / ADS（新表，结构升级）」「建议 dwd/ads technology_master，名待定」（`SCI-INT-C02.yaml:4489`/`:4513`）——即主数据本身就有 DWD 持有 + ADS 镜像两层含混待拍
- 既有 ADS `graph_node`/`graph_edge` 在 `gkxlumenx_ads`（`storage/ENT/stores/mysql/ads.md:42`，图镜像兜底 1 跳，生产者=Nebula 同步旁路）

**裁定**：稿不写库名是分工正确的（「列/表定义归 DATA」），但 DATA 分册需要稿提供两个决策输入而非零输入：① DN-07 写者归属的先行默认（C2）；② ADS 投影复用还是新建（§3）。此外沿分区1 会签 C2 的教训（`TS-L2-M10-LAYER-SIGNOFF-DATA.md` 条件 C2：`gkxlumenx_config` 与 Java 平台库重名），ENT 三表定库名前必须对照 `algo-mysql-connection-info.md` 的 Java 平台库清单查重——本会签不代拍，列入 §7 输入清单 D1。

另注：LAYER v3 裁定「Java 可以建业务表、写业务数据」（`TS-L2-M10-LAYER-DATA.md:29`）开过口子，**该先例不适用于 ENT**——ENT 写的是图谱投影/主数据/变更集，非业务配置表，且 Nebula 单写者（Python）是铁律（storage README §5）。DATA 分册不应以 LAYER v3 为据把变更三表排给 Java。

## 2. 「不建 cfg_」区隔核对（审查重点 ②）

**区隔干净，无误杀。** 逐一排查 ENT 七叶（41–47）有无隐性配置需求：

| 候选配置需求 | 实际归属 | 结论 |
|---|---|---|
| 技术领域分类体系（最像配置的一项） | C02 dim_tech_domain 维表（INT-C-TECH-181，DIM 层，选型 OI-C02-02 甲方） | 正确不进 cfg_，维表归数据域 |
| 关系类型枚举（update_edge 类型） | 来自 105 产出约定（JX-A03-02），代码枚举 | 无表需求 |
| 要素类型（人/机构/论文/专利） | 请求参数（A03 INT-A-TECH-210 entity_types） | 无表需求 |
| G4 排序选项 | 请求参数 | 无表需求 |
| 属性编辑覆盖层（DN-A03-04） | 数据（覆盖值），非配置 | 正确 |

分区1 对照：LAYER 的 cfg_ 四表全是「展示层开关型配置」（图层/分组/数据源登记/要素显示），ENT 全部是图谱写回数据，两套模式在表清单层面零交集。§5「不建 cfg_*」与 LAYER-DATA §1 的库界声明互不冲突。**此条通过。**

## 3. ADS 投影一致性（审查重点 ③）

稿 §1/§6「ADS graph_node/graph_edge 投影（Java 只读）」与存储真源的**规则面**完全一致：ADS=契约面、Python 写、Java 只读（storage README §5 职责矩阵 `:89`）；entan incremental.py 先例（ADS graph_node/edge + Nebula INSERT/DELETE VERTEX + graph_membership 状态表）被 A03 现状核对引用（`SCI-INT-A03.yaml:16`），稿 §0 序 42 也引同一先例。

**缺口在实例面**：A03 用词是「graph_node/graph_edge **同类表**供 Java 只读」（`SCI-INT-A03.yaml:55`）——「同类」暗示可能是新建同构表而非复用 `gkxlumenx_ads.graph_node/graph_edge`（该表是企业维 as-built，「图镜像兜底 1 跳」，结构是否承载技术点节点/边未核）。复用还是新建（新建则库名表名待定）是 DATA 分册必收决策（§7 输入 D3）。Java 只读路径本身无问题：§6 叶 41 读 ADS 投影或经 Python 查图，两条都在规矩内。

## 4. VID 并存增量投影边界（审查重点 ④）

稿 §2 注记（`TS-L2-M10-ENT-ARCH.md:61`）：存量 Nebula VID=`tech:{名称}`，首版写回用新规则 `tech:{technology_id}`，存量边不迁移，只投影本页写回增量，全量切换留 C04。**写侧自身边界清楚**；且相对 A03 OI-A03-02「写回上线前须切」是放宽，方向可接受（先闭环后迁移，符合决策 #5「先全链路闭环后性能」精神）。但数据视角看，双 VID 并存期有四个交叉点稿未覆盖，每个都直接产生脏边/悬挂边（边指向不存在的点）或图内重复：

1. **读侧合并策略未定**：同一逻辑技术点在图中同时存在两个 VID，本页新写边挂在新 VID 上；M2 全景图/M10 现状图若从存量名称 VID 出发查邻居，看不到新边；不合并则用户感知「加了边图上没有」。要么声明「首版读侧仅见增量边（挂接的本页产物）」，要么定合并规则（按主表 aliases 映射两 VID）。
2. **impact 预检口径未定**：序 43 影响预检（A03 INT-A-TECH-202「Nebula 查该点全部边与被引用的实体/快照数」，`SCI-INT-A03.yaml:228`）在双 VID 期查哪个 VID？只查新 VID 会漏存量边 → 统计偏小 → 用户确认删除后存量边残留成悬挂边。至少 impact 要同时报「存量同名 VID 边数」。
3. **新建查重边界未定**：INT-A-TECH-201 duplicate_candidates 只查新建主表；不扫存量 Nebula 名称 VID。存量图已有「tech:人工智能」时人工再建「人工智能」→ 产生 `tech:{technology_id}` 新点，图内出现同义重复点（脏数据主源）。建议首版提交查重同时匹配存量 VID 名称（Python 查图，一次 GO 查询成本）。
4. **auto 层首版行为未定**：104/105 若按全量产出投影（A03 layers.auto「每次 Job 全量或增量产出」，`:53`），会撞存量名称 VID 点——跳过还是重建未定；JX-A03-01（104 以我方 technology_id 锚定输出）是前提且未确认。若首版 104/105 不上（P2 联调范围无自动层），应在 §5 明示「首版无 auto 层 merge」，tombstone 表可降级为首版只建结构不启用。

**会签意见**：边界演进本身同意（附上述 4 点须落 DATA/API 分册，其中 1、3 建议回填 ARCH 稿一句话裁定）。悬挂边清理责任归 Python 单写者（补偿重放同一通道），DATA 分册表设计中 change_log 的 before/after 应记 VID 粒度，便于 C04 全量切换时对账。

## 5. 版本快照与回滚的存储含义（审查重点 ⑤）

稿 §1 要点 5 与 A03 version_and_rollback_draft（`SCI-INT-A03.yaml:73–79`）一致：回滚=反向变更集再走发布（新版本，不物理覆盖），Nebula 只存 published，历史存 MySQL diff、每 N 版一次全量快照。存储含义拆给 DATA 分册：

| 项 | 含义 | 缺口 |
|---|---|---|
| `graph_version.change_set_ids[]` | 数组列：MySQL 落 JSON 还是关联表（多对多） | 归 DATA 设计，倾向关联表（可索引、可追溯单变更集归属多版本——回滚场景正是） |
| 每 N 版全量快照 | 需快照表 + 体积随图规模 × (版本数/N) 增长 | **N 无归属决策人**（A03 只写「N 待定」`SCI-INT-A03.yaml:75`，稿全文未提 N）——建议 DATA 分册自拟默认（如 N=50）报监管人确认，列入 §7 输入 D5 |
| diff 存储 | change_log 已有 before/after，版本 diff 可聚合推导，无需独立物化 | 归 DATA；若物化需增量表 |
| 回滚产生新版本 | 存储只增不减，保留期=DN-A03-06（稿 §2 已列待拍板档 ✓） | 无缺口 |
| **redirect（旧 ID→新 ID）** | A03 id_stability「合并/拆分写 redirect」（`SCI-INT-A03.yaml:79`）；INT-A-TECH-201 查重提示用户「合并或仍新建」（`:207`）——选「合并」就需要 redirect 落点+边迁移 | **稿全文无 redirect/合并语义**（§0 裁定表与 §5 不做清单均未提）。建议二选一：显式进 §5「首版不做合并后端，查重命中只提示仍新建」，或补 merge op。现状是隐性需求悬空 |

## 6. 事实核对汇总

- 序号对应：稿 §6 叶 41–47 与 A03 excel_rows 44–50 / seq 41–47 逐一核对**无错位**（A03:693/778/865/907/950/994/1037）
- §1 要点 1–4（会话编辑/发布事务/合并规则/乐观锁）逐条与 A03 flow_draft + merge_rule 一致，无走样
- G3 预览形态：稿用 `changes:validate`，A03 内部两种形态并存（INT-A-TECH-201 `:validate` `:183` 与批量卡 `dry_run=true` `:1052`）——稿选其一不算错，API 分册统一即可，不列条件
- 状态机：稿 §1 图 fe 边标「draft→approve→publish」把审核画成必经；A03 审核步骤为可选（DN-A03-02，`SCI-INT-A03.yaml:64–66`）。轻微走样，change_set.status 值域归 DATA/API（§7 输入 D7），建议稿图改为 draft→(approve)→publish
- F1–F3 见 §0 表

## 7. 给 DATA 分册（TS-L2-M10-ENT-DATA）的输入

### 7.1 库名/形态决策项清单（稿侧或监管人拍板，DATA 分册不能自决）

| # | 决策项 | 依赖/候选 | 现状 |
|---|---|---|---|
| D1 | 变更三表 + tombstone + 冲突队列 + 主表落哪个库 | DN-07 写者归属（李伟）；候选 gkxlumenx_dwd / gkxlumenx_ads / 新库；**定名前对照 `algo-mysql-connection-info.md` Java 平台库清单查重（LAYER C2 教训）**；Demo 对应 demo_* 实例 | ENT-ARCH 未写，A03 待定 |
| D2 | 技术点主表分层：DWD 持有 + ADS 镜像两层，还是单层 | C02 INT-C-TECH-180「建议 dwd/ads technology_master，名待定」 | 待定 |
| D3 | ADS 投影复用 `gkxlumenx_ads.graph_node/graph_edge` 还是新建同构表 | 复用需核 as-built 结构承载技术点；新建需定库表名 | A03「同类表」措辞含混 |
| D4 | Demo 投影落点 | demo_gkx_chain + demo ADS 实例（结构同正式，storage README §5.1） | ENT-ARCH 缺失（C1） |
| D5 | 快照频率 N + change_set_ids[] 落列形态 | A03「N 待定」无归属人；建议 DATA 拟默认报监管人 | 待定 |
| D6 | 合并/拆分（redirect）首版做否 | INT-A-TECH-201「合并或仍新建」的后端承载 | ENT-ARCH 未裁定（§5） |
| D7 | change_set.status 值域（draft/approved/rejected/published/projection_pending…）+ 是否引 gkxlumen-flow | DN-A03-02；A03 flow candidates unknown | 归 DATA+API 共拟 |
| D8 | 保留期（版本/审计） | DN-A03-06，在册不阻塞首版 | 待甲方/PM |

### 7.2 表清单（DATA 分册建表范围基线；列定义本会签不代拟）

1. `graph_change_set`（ops[]、base_version、status、幂等键 client_op_id 线索在 A03 卡）
2. `graph_change_log`（before/after、trace_id；VID 粒度，供 C04 对账）
3. `graph_version`（+ 快照承载，形态随 D5；可能衍出关联表/快照表）
4. tombstone 表（node 边界 + edge 边界两类；首版可只建结构）
5. 冲突队列承载（独立表或 change_set 扩展，形态随 DN-A03-03）
6. 技术点主表 `technology_master`（随 D2 分层）
7. `dim_tech_domain`（C02 INT-C-TECH-181，本页只读引用，不在本分册建）
8. redirect 表（若 D6 做合并/拆分）
9. ADS 投影 `graph_node`/`graph_edge`（复用或新建随 D3；Java 只读）
10. 挂接状态表（候选，沿 entan `graph_membership` 先例——hang/unhang 的状态面是否独立成表待 DATA 定，A03 INT-A-TECH-207 引先例 `SCI-INT-A03.yaml:793`）

### 7.3 边界提醒

- VID 双 VID 并存期四交叉点（§4）落 DATA 分册时需逐条有答案；change_log 记 VID 粒度
- 写者铁律：MySQL 三表若 DN-07 裁给 Java，Nebula/ADS 仍只能 Python 写（不可整链路移交）
- 本会签不改动被审稿；C1/C2 回填后追记确认行即转同意

---
*会签人：agent:data-agent · 2026-11-07 · 只读核对，未动稿/未动 registry/未 git*

## 三分册会签（2026-11-07）

- 对象：`TS-L2-M10-ENT-DATA.md`（主审）· 交叉 `TS-L2-M10-ENT-API.md`、`TS-L2-M10-ENT-METRIC.md`；ARCH 稿（已监管人签收版）作对照
- 范围：仍只读核对，不改稿、不动 registry、不 git
- **结论：有条件同意。** §7 八决策项落地忠实度高（D1 查重声明经独立复核属实、D5/D6/D7 三处与 API 册同步无误），10 表基线主体落位；但 VID 四交叉点的 ③④ 落地有一处悬空一处自相矛盾、会签表清单第 10 项（挂接状态表）被无声跳过——3 项补裁定/注记后即可转「同意」，无需重开签。

### 决策项落地追踪（§7.1 八项 → DATA 分册 §0）

| # | 落地判定 | 说明 |
|---|---|---|
| D1 | **✓ 属实** | 分册称「对照 algo-mysql-connection-info 查重——gkxlumenx_dwd 在五业务库清单内、非 Java 平台库」（DATA:17）。独立复核：五业务库表确含 `gkxlumenx_dwd`（algo-mysql-connection-info.md:27），Java 平台库 11 个（`gkxlumenx`/`_app`/`_bi`/`_codegen`/`_config`/`_flow`/`_job`/`_mp`/`_pay`/`_report`/`_topic_enterprise`，同文件 :83–94）无 dwd，无撞名；Python 写权有先例（entan env `ENTAN_MYSQL_DWD_DB=gkxlumenx_dwd`，:131）。措辞小瑕：「五业务库清单内无撞名」实际语义是「不与 Java 平台库撞名」，dwd 本身就是既有库，非新定名，建议改写以免误读（非必修）。**附带治理注记（N4）**：该文件 :76 授权注释明写「算法要写、**Java 要读写**」——`gkxlumenx` 账号对五个业务库 GRANT ALL，Java 零写 dwd 目前只是架构约定、权限层面拦不住；实现单若要硬隔离需收紧授权或加写审计 |
| D2 | ✓ | 两层（C02-180），真源 `dwd.technology_master` + ADS 镜像由 `graph_entity_node` 承担（DATA:18/:47） |
| D3 | **✓ 同意新建，理由成立但证据未附** | 分册选新建同构 `graph_entity_node/edge`（DATA:19）。我代核 as-built：既有 `gkxlumenx_ads.graph_node/graph_edge` 是企业维「图镜像兜底（1 跳）、Nebula 同步旁路」（ENT/stores/mysql/ads.md:42），语义/结构均非技术点投影，不含 strength 双列/overlay/version_id——新建判断正确，且 `graph_entity_*` 在 storage 树无撞名（已 grep）。建议分册把这条证据补进正文（现在只写「需核 as-built 承载」等于没核就裁了） |
| D4 | ✓ | demo_gkx_chain + demo ADS 实例（DATA:20/:56），与 storage README §5.1/决策 #7 一致 |
| D5 | ✓ | N=50 拟默认报监管人 + 关联表 `graph_version_change_set`（DATA:21/:36）——与本会签 §5 建议逐字对齐 |
| D6 | ✓ 双册同步 | DATA:22「首版不做（API 册同裁：查重命中只提示仍新建）」↔ API:95「不做合并/拆分 redirect…DATA 册同步裁定」，互指成立 |
| D7 | ✓ 一致（超集+留位） | DATA:23 四值 `draft/approved/published/rejected`；API:89 状态机只画 `draft→(approve)→published` 未画 rejected，但 API:94「不做审核流引擎（DN-A03-02 未决，status 字段留位）」覆盖——rejected 属留位值，非矛盾，备注即可 |
| D8 | ✓ | 沿 DN-A03-06 待拍板、表设计不预设（DATA:24） |

### 10 表基线对照（§7.2 十项 → DATA §1）

九项落位干净：change_set/log/version（+衍出关联表、快照表独立成行）、tombstone、冲突队列（reserved 建表不启用）、technology_master（external_ids JSON 返工护栏**已落主表**，DATA:32，对应 ARCH 会签 C2 条件②）、dim_tech_domain（只读不建）、redirect 随 D6 正确落空。**漏一项：**

- **A3（必修）挂接状态表未裁定。** 本会签 §7.2 第 10 项「沿 entan `graph_membership` 先例（A03 INT-A-TECH-207 引用，A03.yaml:793），hang/unhang 状态面是否独立成表**待 DATA 定**」——分册自称「建表基线 10 张（会签清单）」（DATA:28），但清单构成实为「9 张实体表 + ADS 一行」，第 10 项候选既没建也没裁「不做」，被无声跳过。改法：补一句话裁定——若不建，说明 hang 状态由「图/ADS 边的存在性 + change_log 审计」表达、不沿用 graph_membership 先例即可。

### VID 四交叉点落地评估（§4 → DATA §3）

- ①读合并按主表、②impact 经主表 union 后计数（DATA:55）：**口径本身对，但存在前提悬空——见 A1**。
- **A1（必修）③ 反转会签建议且未补替代护栏：** 本会签 §4.3 建议「首版提交查重同时匹配存量 VID 名称」，分册裁成「查重扫主表不扫存量图（图内重复点主源=主表）」（DATA:55）。问题：主表是自建先行、**存量 Nebula 技术点（`tech:{名称}`）并未灌入主表**，那么 ①② 的「经主表解析/union」无从解析存量名称 VID（主表里根本没有这条映射）——用户对存量同名技术点再新建，主表查重不命中 → 图内双点，①②③ 整条链悬空。二选一补齐：要么主表 seed 存量技术点清单（名称→technology_id 映射行），要么③改回扫存量图。不补则此裁定不成立。
- **A2（必修）④ 自相矛盾：** 「auto 层 Job 撞存量名称 VID：写前经主表 **redirect** 解析」（DATA:55）——但 D6 同页裁定首版**不做 redirect、连表都不建**（DATA:22/:66），④ 引用的解析机制不存在。改法：④ 改为「写前经主表名称/external_ids 映射解析」，或声明轻量映射随 auto Job 单建（redirect 表语义仍留 D6 终态）。
- 术语卫生（建议）：DATA:55 括号「D6 现只重灌 demo」沿自 ARCH:63，指 2026-10-15 的演练事件标识，与本分册 §0 决策项 D6（redirect）**同文档撞号**，建议改写为「2026-10-15 演练：现只重灌 demo_gkx_chain」。另 ARCH-C2 要求的「space 可配置」未明示（只落了 demo 落点），补一句「space 名经配置注入、默认 demo、正式待切换」更稳。

### API / METRIC 交叉

- **R2/DTO↔列 对齐良好**：GraphCurrent 的 edges[](edge_key,rel_type,strength_auto,strength_manual,source,time_range)（API:69）↔ `graph_entity_edge` 列（DATA:48）逐列对上；base_version/projection_status ↔ graph_version（§4 事务补偿双方一致：MySQL 先提交→Nebula 失败→pending+补偿重放，API:83 的 503 读仍可用=DATA:60 的「读上一版」）。R6 conflicts ↔ graph_conflict_queue「reserved 空实现但表建」完全同步（API:62/DATA:38）。
- **A4（建议补注记）挂接实体在 ADS 无承载表**：GraphCurrent.entities[]（entity_id/entity_type/display_name/overlay 已套用）在 DATA §2 没有落点——`graph_entity_node` 的字段形状是技术点的（technology_id/name_cn/category，DATA:47），挂接实体若复用该表则列不匹配。需注记：实体节点投影是并入 graph_entity_node（加 object_type 扩列）、还是第三张投影表、还是仅作边的 endpoint 属性带出。
- 幂等键 client_op_id 未在 change_set 表行出现（DATA:33）——API 定为每 op 必带、可落在 ops JSON 内，可接受；若要表级去重索引（唯一约束/生成列）归实现单，注记一句即可。
- METRIC 三列口径三册一致：`strength_auto/manual/source` 贯穿 DATA:48（列）、API:73（DTO）、METRIC §3（「manual 永不进指标公式」），保护条款闭环 ✓。METRIC:47 提的「A03 213/216 `M_TECH_ENTITY_TOP5` 与 DS 映射不一致，报 data-agent 正式化」——收下，作为本会签人后续待办（不属 DATA 分册缺陷）。

### 新发现汇总（证据：文件:行）

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| A1 | 必修 | ③ 查重不扫存量图 + 主表未 seed 存量点 → ①②「经主表 union」悬空 | DATA:55；对照 A03 OI-A03-02（A03.yaml:111）存量 VID 现状 |
| A2 | 必修 | ④「经主表 redirect 解析」与 D6「首版不做 redirect（不建表）」自相矛盾 | DATA:55 vs DATA:22/:66 |
| A3 | 必修 | 会签 §7.2 第 10 项挂接状态表（graph_membership 先例）未裁定、被无声跳过 | DATA:28–41 vs 本页 §7.2:119；A03.yaml:793 |
| A4 | 建议 | GraphCurrent.entities[] 的实体节点在 ADS 投影无承载表 | API:69 vs DATA:47 |
| N1 | 建议 | graph_change_log 未注记 VID 粒度（本会签 §4 明确要求 before/after 记 VID 供 C04 对账） | DATA:34 vs 本页 §4:71 |
| N2 | 建议 | §3 括号「D6」与 §0 决策项 D6 撞号；space 可配置未明示 | DATA:55/:22；ARCH:63；ARCH 会签 C2:17 |
| N3 | 建议 | D3 新建理由成立但未附 as-built 证据（已代核：ENT ads.md:42 企业图镜像兜底，语义不符，新建正确） | DATA:19 vs ENT/stores/mysql/ads.md:42 |
| N4 | 治理注记 | `gkxlumenx` 账号五业务库 GRANT ALL 且注释「Java 要读写」——Java 零写 dwd 是约定非权限隔离，硬隔离需收紧授权 | algo-mysql-connection-info.md:76/:83–94 |
| N5 | 提醒 | `graph_snapshot` 与 CHAIN 域 ADS 既有 graph_snapshot 同实例跨库同名（dwd vs ads），跨库工具查询易混，建议注记或改名 | DATA:39 vs CHAIN/stores/mysql/ads.md:45/:48 |

**闭合条件**：A1–A3 由 DATA 分册补三句裁定/注记（A1 二选一、A2 改措辞、A3 一句裁不做或落表），回填后本会签人在本节追记一行确认即转「同意」；A4/N1–N5 建议随稿顺手改，不阻断。

---
*三分册会签：agent:data-agent · 2026-11-07 · 只读核对，未动分册稿/未动 registry/未 git*
