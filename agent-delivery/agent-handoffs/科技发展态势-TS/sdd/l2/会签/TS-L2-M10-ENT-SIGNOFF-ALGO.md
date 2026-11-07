# TS-L2-M10-ENT-SIGNOFF-ALGO · 维护管理 · 关键实体与关系 · 算法会签

- 角色：`agent:algorithm-agent`
- 日期：2026-11-07
- 对象：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（主审 §0 范围裁定 / §3 G1–G5 / §6 D18 核查表）+ 交叉 `展示系统三要素集成-SCI-INT/产物/SCI-INT-A03.yaml`（22 卡 + write_back_design_draft）+ 需规《科学技术全景.md》序 41–47 原文
- 事实源：`agent-delivery/metrics/registry/metric-srs-map.yaml`（正/负向挂接证据）、`metrics/metric-evidence-map.json`、`metrics/calc-logic/TECH/M_TECH_GRAPH_105_1.md`
- 监管：`human:刘剑锋`
- 范围：只读核对。不改被审文件，不动 task-registry / 指标注册表，不 git。格式对齐 `TS-L2-M10-LAYER-SIGNOFF-ALGO.md`（2026-11-06）先例，方法论沿用其负向证据法

## 结论

**同意会签**。架构裁定（四段链采纳、G2 首版不做、VID 增量不迁移）从算法/指标视角无推翻性错误。但 §6 的 metric 预期**必须收窄**：叶 41 走不了「全 N/A」分支，只能走「沿 A03 卡」分支且挂 `M_TECH_GRAPH_105_1`；另有三处操作计数口径缝隙与一条 strength_manual 合并语义保护要求，作为给 METRIC 分册的硬输入带下去。附 3 条非阻断建议（S1–S3），不要求改被审稿正文。

## 逐项核对

### 1. §6 预期「推荐列表强度=算法输入非展示指标，全 N/A 或沿 A03 卡」——半成立：叶 41 关闭「全 N/A」分支

- **需规证据**（`bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md` L378）：「算法自动计算并**展示**…每个实体**显示**名称、类型、**关联强度**等基本信息，支持按…关联强度…排序和筛选」。「展示/显示」字样直接命中——关联强度既是排序输入（算法输入）**又是渲染在列表上的数字（展示数字）**，二者兼是。D9 血缘约束的正是展示端数字，所以列表上的 strength 需要 ⓘ。
- **A03 卡证据**：`INT-A-X-213`（L697）`metric_ids: [M_TECH_GRAPH_105_1]`，test_points（L732）明写「D9：关联强度旁 ⓘ 指向 M_TECH_GRAPH_105_1，D4=mock 显示 MockBadge」——A03 已按展示数字挂接，不是 N/A。
- **既有挂接正向证据**：`metric-srs-map.yaml` L5443 起 `M_TECH_GRAPH_105_1` 条目，srs_refs 已含 **seq 41**（page_use，page_ids=[DS-02-MAINTAIN-ENTITY]，L5465–5476）与 05 seq 105 algo_leaf（page_ids 含 DS-02-MAINTAIN-ENTITY，L5495）——注册事实源早已给序 41 挂了指标。
- **负向证据**（同分区1 方法论）：metric-srs-map.yaml 引用《科学技术全景.md》共 10 处，落在维护段（序 41–47）的只有上述 seq 41 一处；**序 42–47 无任何既有挂接**——叶 42–47 走 N/A 有据。
- 判定：稿 §6 括号内「推荐列表强度=算法输入非展示指标」的**定性不成立**；「全 N/A」分支对叶 41 关闭。因稿同句给了「或沿 A03 指标卡」另一分支、且指标挂接细化本就归 METRIC 分册，不构成驳回点，但 METRIC 分册落笔必须按 §6 本会签「预期挂接表」收窄，不得照抄全 N/A。

### 2. G2（智能关联强度）首版不做——算法侧同意，无指标注册缺口，附两条边界

- SRS-42 原文（L393）「添加的实体自动与相关技术节点建立关联关系，系统智能计算关联强度」即 G2。稿裁定首版不做、`hang_entities` 仅挂接（§3 G2 行、§5）。
- **A03 拆卡核对**：智能关联相关的是 `INT-A-X-216`（L826 `metric_ids: [M_TECH_GRAPH_105_1]`，algorithm_type=third_party，Python 105 强度函数）。216 的 gaps（L849）写明「已有 105 边的对直接复用边权；无 105 边的对能否现算 unknown（JX-A03-03）」——首版砍掉的是**无 105 边对的现算分支**，不是指标本身。`M_TECH_GRAPH_105_1` 已注册且实存（`metrics/calc-logic/TECH/M_TECH_GRAPH_105_1.md`，维护者唐绍祖，20261027 批；metric-srs-map 挂接完备），**砍 G2 不产生指标缺口、不需要新号**。
- 边界 1：推荐列表→添加的实体对已有 105 边，挂接回执 `edges_created[(entity_id, technology_id, strength, source)]`（A03 215 L797）复用 105 快照边权——若前端把回执 strength 渲染出来，血缘同挂 `M_TECH_GRAPH_105_1`。
- 边界 2：无 105 边的对，A03 216 已留 decision_needed（强度显示「无」还是允许人工填）→ 人工填的值是 strength_manual，不进 M_TECH_* 口径（见 §4）。
- 后续 G2 算法单若做现算，函数即 JX-A03-03，输出仍归 105_1 口径（A03 213 gaps：「推荐」=按已有 105 边权截取，不另造推荐模型），无需预留新 metric_id。

### 3. A03 写回相关计数——稿 §6 有三处口径缝隙（METRIC 分册必须显式裁定，不能默认 N/A）

1. **221 批量回执统计**（succeeded/failed/skipped）：A03 已标 `metric_missing` + DN-A03-09 豁免待裁（L1064/L1069）。稿 §3 G3 行把「预览/统计做」提为能力、§6 却未提 DN-A03-09——叶 47 的 N/A 前提是豁免裁定通过，METRIC 分册必须沿 DN-A03-09 落笔。
2. **202 impact 预检计数**（edge_count/entity_link_count/snapshot_refs，L232）：稿 §0/§6 做了 impact 接口；A03 202 只标「编辑器写操作 n/a_ops」，**未标 metric_missing，DN-A03-09 的 cards 也只挂 221**——同类页面数字被 A03 遗漏。建议豁免裁定范围扩含 202。
3. **209 版本 stats**（+node/-node/+edge/-edge，L534）：稿 §1 要点 2/§4 数据流含 version stats；SRS-40 要求「查看各版本修改记录」，版本列表若展示 stats 数字即同类。A03 209 未标。
- 论证路径建议：三处均为「操作回执/预检/版本统计」类即时计数——不落指标事实表、无聚合口径、无更新频率，与 LAYER 先例 probe 时延同性质（TS-L2-M10-LAYER-METRIC §1 序 8 行 / LAYER-SIGNOFF-ALGO §3）。建议 DN-A03-09 一次性裁「操作回执类计数豁免 D9 ⓘ」，范围写全（221 回执 + 202 impact + 209 版本 stats + 47 validate dry_run 预览 diff 计数），避免逐卡返工。

### 4. strength_manual 与自动层 strength 的合并语义——口径保护条款缺失，METRIC 分册必须写死

- 稿 §1 要点 3 采纳 A03 merge 规则「manual > auto（字段级）」，§4 数据流 merge → published → **M2 全景图消费**。若边 strength 字段被人工值覆盖后投影进 published/ADS、而读面 M2 直接消费该投影，则 `M_TECH_GRAPH_105_1` / `M_TECH_EDGE_STRENGTH` / `M_TECH_ENTITY_TOP5` 的算法口径被污染。
- A03 三处已自我警示，稿采纳合并规则时**未携带**这三条读面保护：204 risks（L337「读面 M_TECH_EDGE_STRENGTH 若混入人工 strength 会污染算法口径」+ test_point「ⓘ 口径仍指向 105 自动权重」）、220 risks（L1029「人工 strength 覆盖 auto 边权后读面 M_TECH_ENTITY_TOP5 口径被污染 → 读面应取 auto 权重或明确标注人工」）、R-A03-08（L1101）。
- 会签输入（架构稿层面不强制改，读面口径归 METRIC/A02，但必须带下去）：
  1. **口径定义**：M_TECH_*_STRENGTH 系列 = auto 层（105/边权）口径；`strength_manual` 是编辑层字段，**永不进指标公式**。
  2. **实现建议**（供 DATA/API 分册参考）：边属性建议双字段或 effective+source 标记（strength_auto / strength_manual / source），读面指标计算只取 auto；UI 展示人工值时标注「人工」。
  3. 序 46（update_edge strength_manual）同款：维护页表单可回显人工值，读面 Top5 / 边权排序仍按 auto。

### 5. 事实错误排查

- 稿 §6 L94「本二级为图谱写回功能，**无统计数字输出**」：字面与叶 41 矛盾（需规 L378 显示关联强度；A03 213 挂 105_1 且有 D9 test_point）。因同句括号给了「或沿 A03 指标卡」分支，判为**表述瑕疵而非事实错误**；METRIC 分册以本会签 §6 表的收窄结论为准。
- 稿头 L9「18 张写回卡 + 三要素卡」：A03 `card_count: 22`（L19）；dep_kind 含 write_back 的 16 张；18 = 22−4（扣除 207 纯前端撤销栈、213 推荐读卡、214 搜索、216 强度算法卡）。「18 张写回卡」与 16/22 两个自然口径均对不上，疑为 22−4 粗算。非阻断，建议更正为「22 卡（16 张写回 + 读卡/算法卡/前端卡）」。
- 稿头称 A03「ready_to_sign」：A03 文件内无 ready_to_sign 字段；write_back_design_draft `status: draft（未评审）`（L26）。稿 §1「A03 已设计 draft，本叶采纳为正式架构」实为把 draft 升格——本叶会签即是对该 draft 的架构背书之一，会签人须知此点（已在本次会签中背书，见 §2）。
- 其余核对一致：G4 排序 `sortBy=strength|time` 与 A03 213 `sort_by(strength|time|name)`（L711）一致；序 43「保留在推荐列表」（L408）与 A03 217 `still_in_recommend[]`（L884）一致；序 44「实体节点保持不变」（L423）与 A03 218 test_point「实体节点保留」一致；序 46 人工可改「关系强度、时间范围」（L453）与 G1 补齐 strength_manual+time_range 一致；G5 键盘通道纯前端与 A03 207 test_point（D10 键盘可达）一致。

## 6. 给 METRIC 分册的输入（预期挂接表）

| 叶 | A03 卡 | 预期挂接 | 依据 |
|---|---|---|---|
| 41 | INT-A-X-213 | **M_TECH_GRAPH_105_1**（展示数字=关联强度，ⓘ 必须，D4 按 A03 d1=draft/d4=mock） | 需规 L378；A03 213 L697/L732；metric-srs-map L5465–5476 既有挂接 |
| 42 | 215 / 216 | 无新号；挂接回执 `edges_created[].strength` 若显示 → 同挂 M_TECH_GRAPH_105_1；G2 现算不做（无 105 边对强度为空，显示「无」还是人工填待产品） | A03 215 L797；216 L826/L849 |
| 43 | 217 / 202 | 写操作 N/A（MENT-D03）；**impact 预检计数并入 DN-A03-09 豁免裁定**（A03 202 未标，缝隙） | 稿 §0 impact 接口；A03 202 L232 |
| 44 | 218 | N/A（n/a_ops） | A03 218 L934 |
| 45 | 219 | N/A（表单字段；importance_level 非影响力算法分） | A03 219 L977（MENT-D05） |
| 46 | 220 | N/A（表单字段）；**strength_manual 不进 M_TECH_*_STRENGTH 口径**（保护条款，见本会签 §4） | A03 220 L1021/L1029 |
| 47 | 221 | metric_missing：批量回执统计豁免待 DN-A03-09；validate dry_run 预览 diff 计数同入 | A03 221 L1064/L1069 |
| 跨叶（SRS-40 版本面） | 209 | 版本 stats 数字若展示 → 并入 DN-A03-09 裁定 | A03 209 L534 |

前置注记：`M_TECH_GRAPH_105_1` 本地 calc-logic 实存（维护者唐绍祖，20261027 批，更新频率 pending）；A03 所记「formula 未签（pending_cosign 唐绍祖）、source_tables=pending_ods」出自 2026-10-18 MCP metric-get，本会话无 metric MCP 无法在线复核——METRIC 分册落笔前应确认公式签署状态是否有更新。另 A03 213/216 均记 `M_TECH_ENTITY_TOP5` 与 DS 映射挂 105_1 不一致待 data-agent 正式化（L724/L852），METRIC 分册沿 A03 挂 105_1 时须同步销掉该歧义。

## 建议（非阻断，不设闭合时点）

- **S1**：METRIC 分册禁止用「全 N/A」表述叶 41；ENT-ARCH §6 括号内「算法输入非展示指标」定性建议在后续修订机会更正为「排序输入兼展示数字，沿 A03 卡挂 M_TECH_GRAPH_105_1」。
- **S2**：DN-A03-09 豁免裁定范围一次性写全（221 回执 + 202 impact + 209 版本 stats + 47 validate 预览计数），并援引 LAYER probe 时延先例作论证。
- **S3**：稿头「18 张写回卡」数字修正（见 §5）。

## 签收边界

- 本页不把 ENT-ARCH 稿、不把任何任务标 done；签收归监管人 `human:刘剑锋`。
- 不要求改被审稿正文；S1–S3 是输入非条件。
- 读面（M2/A02）Top5 与边权展示的挂接归 A02 二级，本页只约束「维护侧写入不得污染读面口径」（§4 保护条款）。
- G2 智能关联现算留算法侧后续单（JX-A03-03 依赖），届时口径仍归 105_1，不新开号。
