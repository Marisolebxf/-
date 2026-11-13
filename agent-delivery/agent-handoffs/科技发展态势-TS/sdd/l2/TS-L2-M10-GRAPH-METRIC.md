# TS-L2-M10-GRAPH-METRIC · 维护管理 · 维护技术图谱 · 后台指标设计

- 任务：`TS-L2-M10-GRAPH-METRIC`
- 日期：2026-11-13
- 状态：**v2.1，会签条件已回应（含 v2.1 清理）**。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:algorithm-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 34–40（`bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md:260–363`）
- 上游：
  - `sdd/l2/TS-L2-M10-GRAPH-ARCH.md`（v2，2026-11-13 监管人签收；下称 **ARCH**）
  - `会签/TS-L2-M10-GRAPH-L2-裁定.md`（下称 **裁定**）
  - `会签/TS-L2-M10-GRAPH-L2-SIGNOFF-ARCH.md`（下称 **ARCH-SIGN**）
  - `会签/TS-L2-M10-GRAPH-L2-SIGNOFF-DATA.md`（下称 **DATA-SIGN2**）
  - `会签/TS-L2-M10-GRAPH-L2-SIGNOFF-API.md`（下称 **API-SIGN**）
  - `会签/TS-L2-M10-GRAPH-L2-SIGNOFF-PRODUCT.md`（下称 **PROD-SIGN**）
  - `会签/TS-L2-M10-GRAPH-SIGNOFF-ALGO.md`（ALGO-C5 / S2；下称 **ALGO-SIGN**）
  - `会签/TS-L2-M10-GRAPH-SIGNOFF-DATA.md`（DATA-S4；下称 **DATA-SIGN**）
  - `sdd/l2/TS-L2-M10-ENT-METRIC.md`（格式与边界先例；下称 **ENT-METRIC**）
  - `会签/TS-L2-M10-ENT-SIGNOFF-ALGO.md`（DN-A03-09 豁免先例；下称 **ENT-SIGN**）
  - `agent-delivery/data-lineage-policy.md`（D9；下称 **POLICY**）
- 查询：本会话无 metric MCP。`M_TECH_*` 的身份与 D1–D4 只读引用 `metrics/registry/metric-readiness-matrix-TECH.yaml`（下称 **MATRIX**）和 `metrics/registry/metric-srs-map.yaml`（下称 **SRSMAP**）的已落行，未改注册表。`M_TECH_GRAPH_105_1` 公式签署状态沿用 ENT 前置注记，不在本页重开。

本叶只写 34–40 的指标挂接。**结论：34–40 不挂任何 `metric_id`。** 七叶原文是人工编辑器，没有「算法自动生成 / 推荐补边」句（`metrics/request/展示系统/pages/DS-02-MAINTAIN-GRAPH.yaml:59-69`，下称 **PAGE**）；页面上出现的数字全部是操作回执类计数，按 **「DN-A03-09 建议范围，待 PM / 数据 Lead 确认」** 处理（裁定 A8），不写成无依据的 N/A。计数类共**九类**：35-3 四项（技术点关系 / 实体关系 / 实体挂接 / 全景隐藏存量关系）、39-1、40-3、40-4、publish `results`、rollback `results`。不新注册 `metric_id`，不改 D4，不替 `DS-02-METRIC-OPEN-L01` 拍板。

## 0. 读码核对（2026-11-13，只读）

| # | 事实 | 代码位置 | 对本册的意义 |
|---|---|---|---|
| 1 | 点 `strength` 取自 Nebula `tech_point.weighted_degree`，原样输出 | `lumen_common/algorithms/tech_graph_read.py:178-197`（下称 **read**） | 维护层没有写 `weighted_degree` 的字段，叠加也不重算 |
| 2 | 边 `weight` 取自 `tech_rel.relation_confidence_score` | read:281、read:300-302 | 人工边不填 `weight`，只放 `strengthManual`（ARCH:143） |
| 3 | 实体边强度取 `tech_has_*.relation_strength`，落 `relationStrength` / `weight` | read:374-394 | 41–47 的实体面；34–40 不产生这类边 |
| 4 | 节点 id = `technology_node_id or vid`；关系端点用该 id | read:181、read:291-299 | 人工边端点映射的口径基准（ARCH:136） |
| 5 | Nebula 关系为无向 MATCH，默认只取 `HIGH/MEDIUM` | read:269-272 | 35-3 全景隐藏数必须同口径（ARCH:200） |
| 6 | `timeline` 只聚合 `relations[].year` | read:499-516 | 人工边不填 `year`，不进时间轴（ARCH:143） |
| 7 | `relationTypeOptions` 从 relations 自动汇总 | read:533-539 | 三个中文类型会进图例 / 筛选，但不进指标（ARCH:146） |
| 8 | S4 分数种子直接分页扫 Nebula `tech_point` / 实体 tag，不调读图出口 | `scripts/seed/seed_technology_panorama_score.py:268-342`（下称 **SCORE**） | S4 不从叠加结果取数（ARCH:172；ALGO-SIGN S2） |
| 9 | 分数是 `sha256` 稳定 mock 值，不读任何库表 | SCORE:44-50 | 与人工层无输入关系 |
| 10 | Java 出口按 `subject_id` 回填三个分数；`centrality` 缺失写 null，`influence` 缺失不出现 | `SituationPanoramaService.java:249-258`、`:532-540`（下称 **PAN**） | 新建点 `tm:*` 拿不到分数，显示空，不补 0 |
| 11 | 主表 `importance_level` 默认 `'中'`，列可空 | `vendor/entan-py/scripts/mysql/tech_graph_maintain.sql:11`（下称 **DDL**） | 表单枚举，不是影响力算法分；种子须显式写 NULL |
| 12 | 现种子 `MASTER_SQL` 不写 `importance_level`，会吃到默认 `'中'` | `vendor/entan-py/scripts/seed_tech_graph_maintain.py:234-241`（下称 **SEED**） | 新 SEED-L01 必须显式写空（ARCH:102） |
| 13 | 版本行 operator 现写死 `"py"`；`results` 在请求时按影响行数现算 | `vendor/entan-py/api/tech_graph_maintain_routes.py:844`、`:866-884`（下称 **routes**） | 都是回执 / 元数据，不是指标；持久化落 `graph_version.publish_results`（DATA 新增列，同事务写入） |
| 14 | 版本 `stats` 现为 `{"ops":N}` 或旧扁平四键；新版本统一按 API §3.4 分组 JSON | routes:844、`:852-858`；裁定 B1 | 历史版本不回填，前端须兼容四种旧形状 |
| 15 | `graph_tech_edge` 新增 `strength_auto`（auto 原强度快照）；同库 `graph_entity_edge` 同名列注释为「指标只取此列」 | DDL:140；DATA §2.1:79 | 不可照抄该注释；`strength_auto` 不得被任何指标读取（裁定 B9） |

## 1. 34–40 逐功能点：有没有展示指标

### 1.1 判定口径

本册把界面上的「数字」分三类，判定用语固定：

| 类别 | 定义 | 本册写法 |
|---|---|---|
| A 无数字 | 纯交互、表单字段、文案、状态 | `N/A（交互/字段）` |
| B 操作回执计数 | 用户操作的即时统计，不落指标事实表、无聚合口径、无更新频率 | `计数类，DN-A03-09 建议豁免` |
| C 算法指标 | 注册 `metric_id`、有 8 件套与 D1–D4 的数字 | 本二级为 **0 行** |

### 1.2 逐条

| 功能点 | ARCH §6 界面必见 | 有无数字 | 判定 | 依据 |
|---|---|---|---|---|
| 34-1 右键空白创建 | 右键菜单「添加节点」 | 无 | N/A（交互） | ARCH:193 |
| 34-2 工具栏按钮 | 按钮文案「添加节点」 | 无 | N/A（交互） | ARCH:194 |
| 34-3 弹窗字段 | 名称 / 分类 / 描述 / 重要性（高 / 中 / 低） | 无 | N/A（表单字段；重要性是枚举不是分值） | ARCH:195；DDL:11；DS02-PATH-METRIC:41-45（关键节点分不在此） |
| 34-4 指定位置 | 落点坐标，刷新后不变 | 无 | N/A（布局属性） | ARCH:196 |
| 34-5 唯一标识符 | 节点详情显示编号 | 无 | N/A（标识符不是统计） | ARCH:197 |
| 35-1 单击 / 框选 | 单选 + 框选多选 | 无 | N/A（交互） | ARCH:198 |
| 35-2 右键 / Delete | 右键「删除节点」+ Delete | 无 | N/A（交互） | ARCH:199 |
| 35-3 确认框提示关系 | 确认框四项关系计数 | **有：4 个** | **B 计数类，DN-A03-09 建议豁免**（工作集三项按 active 计；全景隐藏按 HIGH/MEDIUM 上限） | ARCH:200、ARCH:272；裁定 B15；PROD-API-C11 |
| 35-4 节点与关系移除 | 节点与连线消失 | 无 | N/A（结果态） | ARCH:201 |
| 36-1 Ctrl 选两点 | 依次选中两个节点 | 无 | N/A（交互） | ARCH:202 |
| 36-2 右键「添加关系」 | 右键菜单出现「添加关系」 | 无 | N/A（交互） | ARCH:203 |
| 36-3 类型 / 强度 / 时间 | 类型下拉、强度、起止年 | **有：人工强度回显** | 编辑值，不是指标；弹窗字段「关系强度（人工）」，悬浮 / 详情标「人工」，不挂 ⓘ | ARCH:204、ARCH:268-269；裁定 B20 |
| 36-4 显示连线 | 有向箭头 + 类型标签 | 无 | N/A（图形） | ARCH:205 |
| 37-1 点击高亮 | 选中态 | 无 | N/A（交互） | ARCH:206 |
| 37-2 右键 / Delete | 右键「删除关系」+ Delete | 无 | N/A（交互） | ARCH:207 |
| 37-3 确认后移除 | 确认框文案 | 无 | N/A（文案） | ARCH:208 |
| 38-1 双击 / 右键编辑 | 双击节点 + 右键「编辑属性」 | 无 | N/A（交互） | ARCH:209 |
| 38-2 四字段 | 名称 / 分类 / 描述 / 重要性 | 无 | N/A（表单字段，同 34-3） | ARCH:210 |
| 38-3 点保存更新 | 画布显示新值 +「已加入待保存改动」 | 无 | N/A（提示） | ARCH:211 |
| 39-1 自动记录修改 | 「未保存改动 N 项（本批上限 50）」 | **有：1 个（前端草稿净差 op 条数）** | **B 计数类，DN-A03-09 建议豁免** | ARCH:212；API-METRIC-C8 |
| 39-2 撤销 / 重做按钮 | 两个按钮 + 可用状态 | 无 | N/A（交互） | ARCH:213 |
| 39-3 Ctrl+Z / Ctrl+Y | 键盘快捷键 | 无 | N/A（交互） | ARCH:214 |
| 39-4 可追溯 | 恢复提示；版本详情逐条 | 无 | N/A（记录列表） | ARCH:215 |
| 40-1 保存 | 「保存图谱」→ 成功提示 → 刷新后仍在 | 无固定数字；若展示回执计数见 §2.2-8 | N/A（交互）；回执计数另列 | ARCH:216；PROD-METRIC-C5 |
| 40-2 创建新版本 | 版本说明输入 + 列表新增一行 | 无 | N/A（表单） | ARCH:217 |
| 40-3 回滚 | 确认框移除计数 + 分组计数 + 可再回滚提示 | **有：多组（目标快照 vs 当前工作集求差）** | **B 计数类，DN-A03-09 建议豁免** | ARCH:218、ARCH:111；裁定 B12 |
| 40-4 修改记录与操作人 | 版本列表（操作人、时间、类型、计数） | **有：该版本自身回执 `stats`** | **B 计数类，DN-A03-09 建议豁免** | ARCH:219、ARCH:99；裁定 B1 |
| 横切：real 轨不显示种子 | 只显示服务端数据；空态 | 无 | N/A（数据来源） | ARCH:220 |
| 横切：未登录只读 | 写控件禁用 + 顶部提示 | 无 | N/A（权限态） | ARCH:221 |

### 1.3 汇总

- 29 行（27 个功能点 + 2 个横切）中，**24 行完全没有数字**。
- **5 行有数字**：35-3、36-3、39-1、40-3、40-4。
- 其中 **4 行是操作回执计数**（35-3、39-1、40-3、40-4），**1 行是人工编辑值**（36-3）。
- 这 4 行对应的操作回执计数展开为**九类**（§2.2）：35-3 四项、39-1、40-3、40-4、publish `results`、rollback `results`。publish / rollback 回执不在 ARCH §6「界面必见」列，但若前端渲染「成功 N 项」即同属计数类，规则一致。
- **挂算法指标的行 = 0**。本页因此没有 `metric_id`、没有 ⓘ 的 `MetricSpecCard`，也没有 D4 角标可挂。

## 2. 计数类数字：范围、界面与 DN-A03-09 豁免

### 2.1 为什么走豁免，不写成「全 N/A」

- 这九类数字都是**操作的即时回执 / 预检 / 版本统计**：不落指标事实表、没有跨期聚合、没有更新频率，与 LAYER probe 时延先例同性质（ENT-SIGN §3 论证路径；ENT-METRIC §2）。
- ENT 已把同类数字并进 DN-A03-09 建议范围（ENT-METRIC §2）；DATA-SIGN 的 DATA-S4 明确要求 GRAPH 侧由 METRIC / ALGO 写清，不能默认 N/A。ALGO-SIGN 的 ALGO-C5⑤ 要求「范围写全」。
- 因此本册的写法固定为：**不注册 `metric_id`，按「DN-A03-09 建议范围，待 PM / 数据 Lead 确认」处理**（裁定 A8）；裁定确认前，界面**不挂 ⓘ、不挂 MockBadge**，也不写「无依据 N/A」。

### 2.2 九类逐项

| # | 数字 | 界面位置 | 取数 / 来源 | 是否 ⓘ | 界面建议文案 |
|---|---|---|---|---|---|
| 1 | `tech_edge_count`（技术点关系） | 35-3 删除确认框 | 工作集 `graph_tech_edge` 中 `status='active'` 且 `(src=? OR dst=?)` 的边数，**双向都算**（ARCH:200；API §5.2；DATA §7.4；裁定 B15） | **否** | 「工作集内技术点关系 N 条」 |
| 2 | `edge_count`（实体关系） | 35-3 删除确认框 | 工作集实体关系统计，`impact` 扩字段（ARCH:200；API §5.2；DATA §7.4） | **否** | 「实体关系 N 条」 |
| 3 | `entity_link_count`（实体挂接） | 35-3 删除确认框 | 工作集人工挂接实体统计，`impact` 扩字段（ARCH:200；API §5.2；DATA §7.4） | **否** | 「挂接实体 N 个」 |
| 4 | `panorama_hidden_relation_count`（全景隐藏存量关系） | 35-3 删除确认框 | Nebula 只读计数，口径与全景默认读一致：无向 MATCH、`HIGH/MEDIUM`（read:269-272）；按该点关联总数 **gross** 计，是「最多将隐藏」的上限，不扣其他过滤；失败返回 `null`（ARCH:200、ARCH:253；API §5.2） | **否** | 「全景图中将隐藏存量关系 M 条（上限）」；`null` 时写「无法统计」，不用 0 冒充 |
| 5 | 未保存改动 `N` 项 | 39-1 工具栏常驻 | **前端草稿净差 op 条数**，与后端 `OPS_LIMIT=50` 同一口径（ARCH:212、ARCH:244；routes:42）；`changes:validate.op_count` 只用于预览，**不是** 39-1 的取数来源（API-METRIC-C8） | **否** | 「未保存改动 N 项（本批上限 50）」 |
| 6 | 回滚预览分组计数 | 40-3 回滚确认框 | 目标版本快照与当前工作集**求差**：`tech_nodes{added,updated,removed}`、`tech_edges{added,updated,removed}`、`entity_links{added,removed}`、`entity_edges{added,updated,removed}`、`entity_attrs{updated}`。`added`=目标有当前无（恢复）、`removed`=当前有目标无（移除）、`updated`=两边都有但值不同（还原），`total=added+removed+updated`；**不是目标版本自己的 `stats`**（ARCH:111、ARCH:218；API §4.3；DATA §5.3；裁定 B12） | **否** | 「将变更 X 项（恢复 A / 移除 R / 还原 U）」+ 分组明细 |
| 7 | 版本 `stats` | 40-4 版本列表每行 | 该版本**发布时的操作回执计数**，形状以 **API §3.4 分组 JSON 为唯一口径**（`tech_nodes` / `tech_edges` / `entity_links` / `entity_edges` / `entity_attrs`，组内按 API 键矩阵）；历史版本兼容 `{"ops":N}`、旧扁平四键、`{}`、`NULL`，原样显示、缺键不补 0（ARCH:99、ARCH:219；裁定 B1；API §3.4） | **否** | 版本统计用「新增 / 修改 / 删除」；按组中文摘要，如「技术点 新增2 / 删除1 / 修改3」 |
| 8 | `publish` 回执 `results`（succeeded / failed / failed_items） | 40-1 保存成功提示（若前端展示） | 发布回执；随版本持久化到 `graph_version.publish_results`，**同事务写入**（DATA §5.2；API §3.3）。历史版本 `results:null`（API §3.3 :189） | **否** | 「保存成功：N 项已生效，M 项未生效」；`M>0` 可展开中文原因；`failed_items` 是错误明细，不做聚合、不挂 ⓘ |
| 9 | `rollback` 回执 `results`（同结构） | 40-3 回滚成功提示（若前端展示） | 回滚回执，与 publish 同结构；同列 `graph_version.publish_results` 持久化，版本详情 / 审计可查（API §4.4；DATA §5.3；API-METRIC-C2） | **否** | 「回滚成功：N 项已生效，M 项未生效」；历史 `null` 不显示逐条结果 |

### 2.3 统一规则（会签后由实现单遵守）

1. **不挂 ⓘ、不挂 MockBadge、不注册 ID**。这些数字没有 8 件套，挂 ⓘ 会打开一张空卡。
2. **0、取不到、合法 null 三者分开**。35-3 的 M 取不到必须是 `null` → 「无法统计」，不能返回 0；**40-3 的 `counts:null` 是合法态**（无快照 / 超限），接口返回 200，界面不显示分组计数，显示 `not_rollbackable_reason`（`no_snapshot` / `snapshot_oversize`）的中文原因并置灰回滚；其余计数取不到才按失败处理（不渲染），不显示 0（API-METRIC-C4；PROD-METRIC-C4）。
3. **同口径**。39-1 的 N 与后端 50 上限同口径（op 条数，一个 `delete_node` 可带多个点，ARCH:244）；35-3 的 M 与 §4.2「已删存量边」的过滤同口径（无向、HIGH/MEDIUM，ARCH:139、ARCH:200）；`tech_edge_count` 只计 `status='active'`、双向都算（裁定 B15）；40-3 的 `total` 是差异处数，不是「移除数」。
4. **40-3 与 40-4：同一套分组键 + 同一个快照求差函数，不是同一份数据**。40-4 的 `stats` 是**该版本自己**的发布回执；40-3 的 `counts` 是**目标快照与当前工作集求差**。真正同源的是 40-3 的 `counts` 与**回滚产生的新版本**的 `stats`（同一求差函数）；**禁止拿目标版本 `stats` 直接充当预览计数**（裁定 B12；API-METRIC-C1；DATA-METRIC-C4）。
5. **两套时态、两套文案**。版本统计用「新增 / 修改 / 删除」；回滚预览用「恢复 / 还原 / 移除」，不得把回滚语境的 `added` 译成「新增」。界面不出现 `stats` / `counts` / `results` / `failed_items` / `succeeded` 等字段名（裁定 B19；PROD-METRIC-C3）。
6. **历史版本兼容**。`stats` 四种旧形状（`{"ops":N}`、旧扁平四键、`{}`、`NULL`）原样显示，`{"ops":N}` 显示「N 项改动」，扁平键显示「技术点 +a/−b · 关系 +c/−d」，空 / 无法识别显示「—」，缺组不补 0；不回填历史 `stats`（API-METRIC-C6；DATA-API-S6）。
7. **未裁定前的措辞**：文档与页卡写「按 DN-A03-09 建议范围，待 PM / 数据 Lead 确认」；不写「已豁免」，也不写「N/A」（裁定 A8）。

## 3. 人工强度保护条款：五句落成可核查规则

### 3.1 ARCH §9 五句 → 可核查规则

| 句 | ARCH 原文要义 | 落成的规则（可核查） | 证据 |
|---|---|---|---|
| 1 | 人工强度永不进任何指标公式 | `strength_manual` **和 `strength_auto`** 均不得出现在 `weight`（`relation_confidence_score`）、点 `strength`（`weighted_degree`）、S4 影响力 / 中心度 / 路径优先级的任何计算或回填中；人工强度只走 `strength_manual` | ARCH:268；read:194-197、read:281、read:300-302；SCORE:44-50；裁定 B9；DATA-METRIC-C1 |
| 2 | 界面标「人工」，不挂 auto 口径 ⓘ | 36-3 弹窗字段标「关系强度（人工）」；画布关系标签常驻只显示类型，强度与「人工」放悬浮提示 / 关系详情（如「强度 7.5 · 人工」）；种子边标「存量」；**不挂 ⓘ**；如需信息入口，用文字「人工编辑值，不参与自动指标」，不接 `MetricSpecCard` | ARCH:269；裁定 B20；PROD-METRIC-C1 |
| 3 | 存量 `weight` / `strength` 身份不变，本叶不拍板 | 不把两者注册成新指标，也不改其图属性身份；「加权度身份」问题留在 `DS-02-METRIC-OPEN-L01` | ARCH:270；`科学技术全景-DS02/sdd/l2/TS-L2-DS02-GRAPH-METRIC.md:39-51`（下称 **DS02-GM**）；`metrics/request/_work/open-loop/DS-02-METRIC-OPEN-L01.yaml:112-121`（下称 **OPEN**） |
| 4 | 新点无度、无 S4 分数，显示空不补 0 | 新建点（`tm:{id}`）在 nodes 里不得有 `strength`；Java 出口 `centrality` 为 null、`influence` 不出现，前端按空显示 | ARCH:271；ARCH:140；PAN:532-540 |
| 5 | 操作类计数并入 DN-A03-09 | **九类**计数按 §2 处理；不注册、不挂 ⓘ、不写无依据 N/A | ARCH:272；§2 |

### 3.2 字段清单：哪些字段不得被指标读取

| 字段 | 性质 | 规则 |
|---|---|---|
| `graph_tech_edge.strength_manual` | 人工编辑强度 | 任何指标 / 分数脚本不得读取；不映射到 `weight`、`strength`、S4 |
| `graph_tech_edge.strength_auto` | auto 原强度快照（DATA 新增） | **任何指标 / 分数脚本不得读取**；不映射到 `weight`、`strength`、S4；不得照抄 `graph_entity_edge` 同名列「指标只取此列」的注释；人工强度只走 `strength_manual`（裁定 B9；DATA-METRIC-C1） |
| `graph_tech_edge.time_from` / `time_to` | 人工时间范围 | 只做关系标签 / 详情显示；不写 `year`，因此不进 `timeline`（read:499-516） |
| `graph_tech_edge.rel_type`（包含 / 依赖 / 促进） | 人工关系类型 | 只做显示与筛选；不映射成 `M_TECH_EDGE_STRENGTH` 的 `relation_type`。种子边英文码是显示原码，**不作为指标维度**、不拆 `relation_type` 维度；列宽见 DATA 册，本册不写死（DATA-METRIC-S6） |
| `graph_tech_edge.source`（auto / manual） | 来源标记 | 只用于「存量 / 人工」标注与删除过滤；不进口径 |
| `technology_master.importance_level` | 表单枚举（高 / 中 / 低） | 不是 `M_TECH_ENTITY_INFLUENCE` 或 `M_TECH_PATH_KEYNODE` 的分值；种子点写 NULL，不把默认「中」当人工评定（DDL:11；ARCH:102） |
| `technology_master.category` / `description` / `name_cn` / `name_en` | 显示覆盖值 | 非空才覆盖 Nebula 原值（ARCH:137）；不参与任何指标 |
| `technology_master.layout_x` / `layout_y`、`graph_entity_node.layout_x` / `layout_y` | 画布坐标（DATA 定名） | 布局属性，不是度量；不参与任何指标（裁定 B2；DATA-METRIC-S1） |

补充：**`graph_tech_edge` 不登记为任何 `metric_id` 的源表**；`strength_manual` / `strength_auto` 不进任何 8 件套；计数类不注册 `metric_id`（DATA-METRIC-S3）。

### 3.3 公式 / 读面清单：哪些计算不得引入人工层

| 计算 / 出口 | 现状来源 | 规则 |
|---|---|---|
| `relations[].weight` | `tech_rel.relation_confidence_score`（read:281、read:300-302） | 只读 Nebula 存量边；人工边只放 `strengthManual`，不写 `weight`（ARCH:143） |
| `nodes[].strength` | `tech_point.weighted_degree`（read:194-197） | 只读 Nebula 点属性；不得用工作集边重算度，不得把人工边计入度 |
| 实体边 `relationStrength` / `weight` | `tech_has_*.relation_strength`（read:374-394） | 41–47 的实体面；34–40 不新增、不改写 |
| S4 `influence` / `centrality` / `path_priority` | ADS `ads_technology_panorama_score`，按 `subject_id` 回填（PAN:249-258；`JdbcPanoramaScores.java:33/78-101`） | 新点无行 → 空；不得为 `tm:` 点补 mock 分数 |
| `keyPathOptions` | `tech_path_step`（read:444-496） | 人工边不造路径；删点只整条剔除路径（ARCH:138） |
| `timeline` | `relations[].year`（read:499-516） | 人工边无 `year`，不改变时间轴口径（ALGO-C11 选②） |
| `relationTypeOptions` / `factorItems` | 从 relations / nodes / records 汇总（read:527-539） | 三个中文类型会进图例；不构成指标，不驱动新增下拉（ARCH:146、ARCH:204） |
| 图结构 / 边数 / 路径数类指标 | DWD / ADS | **必须在 DWD / ADS 侧算，不得改为从读图出口实时统计**；否则删一条种子边就会改动本应稳定的指标数字（ARCH §9；§4.1） |

### 3.4 种子与分数脚本：哪些不得读人工层

| 脚本 | 现有行为 | 必须遵守 |
|---|---|---|
| `seed_technology_panorama_score.py`（S4 分数） | `_graph_rows` 直接分页扫 Nebula `tech_point` 与实体 tag（SCORE:268-342）；`mock_value` 只做哈希（SCORE:44-50）；`--check` 用内联 fixture（SCORE:117-135） | **脚本级 fail-closed 断言**：只允许 Nebula 连接；出现读取 `technology_master` / `graph_tech_edge` / 带 `overlay` 的读图结果即抛错退出；不得改为调用 `read_graph`；`--check` 保持 fixture-only。实现单必须加，不接受仅文档约束（ARCH:172；ALGO-SIGN S2；DATA-METRIC-C2；ARCH-METRIC-C3 升级为必修） |
| 新 `TS-L2-M10-GRAPH-SEED-L01` | 需新写：从 `demo_gkx_chain` 取 ≤50 点及其间 `tech_rel`，写主表 + `graph_tech_edge`（ARCH:102） | 只写工作集；不写 `ads_technology_panorama_score`；不写 `weighted_degree`；`importance_level` 显式 NULL（现 `MASTER_SQL` 省略该列会吃默认「中」，SEED:234-241）；`strength_auto` 仅作历史快照写入，**不产分数**；不写 Nebula（DATA-METRIC-C1） |
| as-built `seed_tech_graph_maintain.py` | 只读 `tech_has_*` 实体边（SEED:51-56、SEED:91-101） | 维持；不新增分数写入 |
| entan 写链 | 不写 Nebula（ARCH:70-75） | 35-3 的 Nebula 计数只读，显式 `USE demo_gkx_chain`，只做 MATCH / count（ARCH:73） |

### 3.5 交付验收断言（转成实现单可执行项）

| # | 断言 | 落点 |
|---|---|---|
| 1 | `strength_manual` / `strength_auto` 不出现在 `weight` / `strength` / S4 的读取或计算路径 | 算法单测 / 静态检查 |
| 2 | `graph_tech_edge` 不被登记为任何 metric 的源表；`strength_manual` / `strength_auto` 不在任何 8 件套 | 注册表核对 |
| 3 | 新点 `tm:{id}` 无 `strength`、`centrality:null`、`influence` 不出现 | `tests/test_tech_graph_read.py` |
| 4 | S4 分数种子读取工作集表或 `overlay` 结果时 fail-closed；`--check` fixture-only | 脚本断言 / CI |
| 5 | 九类计数不挂 ⓘ / MockBadge，不出现 D4 角标；40-3 `counts:null` 显示不可回滚原因并置灰 | 前端验收 |
| 6 | 历史 `stats` 四种旧形状正常显示、缺组不补 0 | 前端验收 |

## 4. 全景叠加后，已签收口径复核

前提：叠加只**追加字段**，不改已有字段值；`overlay_factory=None` 时输出与今天逐字节一致（ARCH:125、ARCH:152）。以下逐项。

| # | 口径 / 数字 | 来源 | 结论 | 理由 |
|---|---|---|---|---|
| 1 | `relations[].weight` | `tech_rel.relation_confidence_score` | **不受影响** | 人工边用 `strengthManual`，不写 `weight`（ARCH:143）；存量边即使被软删，只是该条不再出现，已有 weight 值不被改写；`M_TECH_EDGE_STRENGTH` 的注册对象是 IPC4 共类网络边，不是 `tech_point` 边（DS02-GM:30；MATRIX:464 d3_gap） |
| 2 | `nodes[].strength` | `tech_point.weighted_degree` | **不受影响** | 维护页没有写 `weighted_degree` 的字段；叠加仍走 `_point_node` 读 Nebula 原值（read:194-197）；新建点无该属性（ARCH:140、ARCH:271） |
| 3 | `keyPathOptions`（关键路径） | `tech_path_step` | **口径不变，可见集合可能变小** | 删点导致含该点的整条路径不显示（ARCH:138）；人工边不造路径（ARCH:143）。这是显示集合变化，不是指标定义或取值变化；`M_TECH_PATH_PRIORITY` 的注册对象是深圳 238 个 IPC4 点（DS02-PATH-METRIC:33） |
| 4 | S4 `influence` | `ads_technology_panorama_score` 按 subject_id | **不受影响** | 只按读图 id 回填；新点 `tm:*` 无行 → 字段不出现（PAN:532-540）；分数种子不读人工层（SCORE:268-342） |
| 5 | S4 `centrality` | 同上 | **不受影响** | 新点 `tm:*` 无行 → `centrality: null`（PAN:250、PAN:536-537）；前端按空显示，不是 0 |
| 6 | S4 `path_priority` | 同上 | **不受影响** | 路径被删点剔除后，对应 score 行仍在表里，只是不显示；口径与取值不变 |
| 7 | `M_TECH_GRAPH_STRUCT` | DWD / IPC4 共现骨干图 | **不受影响** | 注册口径对象是 200 个 IPC4 域（DS02-GM:29；MATRIX:618 d3_gap）；维护层改的是 `tech_point`，不同对象；D4 维持 mock |
| 8 | `M_TECH_EDGE_STRENGTH` | IPC4 共类网络边权 | **不受影响** | 同上（DS02-GM:30；MATRIX:464）；人工强度与 `strength_auto` 均不进公式 |
| 9 | `M_TECH_GRAPH_105_1` | seq 105 技术实体关系抽取 | **不受影响** | `srs_refs` 含 seq 18 / 22 / 26 / 41 / 51 与 05-105，**无 34–40**（SRSMAP:5443-5530）；人工强度不进口径（ENT-METRIC:40） |
| 10 | `M_TECH_PATH_CENTRALITY` / `M_TECH_PATH_PRIORITY` / `M_TECH_PATH_KEYNODE` | 深圳 238 个 IPC4 点 | **不受影响** | 注册对象与本页 `demo_gkx_chain` 的 `tech_point` 不是同一套点，本页不调用其计算（DS02-PATH-METRIC:33、:41-45）；D4 维持 mock |
| 11 | `M_TECH_ENTITY_TOP5` / `REL` / `INFLUENCE` / `PAPER_PATENT_CNT` | 实体面（41–47） | **不受影响** | 34–40 不新增实体边、不改实体属性；不在本页挂接 |
| 12 | `relationTypeOptions` / `timeline` / `factorItems` | 读图出口汇总 | **不是指标，但有可见变化** | 人工边会让图例多出三个中文类型（read:533-539；ARCH:146）；`timeline` 不变（人工边无 `year`）；`factorItems` 仍只有「技术点」（read:527-532） |

### 4.1 唯一需要提醒的「可见集合」变化

- 删除存量点 / 删除种子边后，全景页会少点、少边、少路径。**这不是口径变化**，是「已发布工作集」的显示结果；但已签收全景页的用户可见数字（图例项、路径条数）会变。
- 实现护栏：任何「图结构 / 边数 / 路径数」类数字都必须继续在 DWD / ADS 侧算，**不得改为从读图出口实时统计**。否则删一条种子边就会改动一个本应稳定的指标数字。这条已在 §4 第 7、8、10 行按「不同对象」挡住，实现单不得绕过。

## 5. `DS-02-MAINTAIN-GRAPH.yaml` 建议同步（只给 diff 描述，不改文件）

| # | 位置 | 现状 | 建议改动 |
|---|---|---|---|
| 1 | `updated`（PAGE:5） | `"2026-08-24"` | 改为 `"2026-11-13"` |
| 2 | 头部注释（PAGE:14-26 之后） | 无 GRAPH-ARCH 指针 | 追加 3 行：① 34–40 已按 GRAPH-ARCH 实现为草稿栈 + changes/publish + versions/rollback，仍是 `n/a_ops`；② 九类数字按「DN-A03-09 建议范围，待 PM / 数据 Lead 确认」处理；③ 人工强度是编辑值，详见本册路径 |
| 3 | `maintain_ruling`（PAGE:59-69） | 只写七叶是人工编辑器 | 末尾追加一段：流程变为「草稿栈（撤销/重做不发请求）→ 保存即发布 → 版本列表/详情/回滚」；七叶维持 `n/a_ops`，不新增 `M_*`、不改 D4；界面数字（35-3 四项、39-1、40-3、40-4、publish / rollback `results`）一律按操作回执计数处理，不挂 ⓘ / MockBadge；`strengthManual` 只在 36-3 回显并标「人工」 |
| 4 | `demands[MGRAPH-D02]` 缺口说明（PAGE:170-180） | 只写级联删关系 | 追加：35-3 的两个计数是删除预检，不是指标；`tech_edge_count` 只计 `status='active'` 且双向；`panorama_hidden_relation_count` 取不到显示「无法统计」，不用 0 |
| 5 | `demands[MGRAPH-D06]` 缺口说明（PAGE:218-228） | 只写编辑会话历史 | 追加：39-1「未保存改动 N 项（本批上限 50）」按前端草稿净差 op 条数计，与后端 50 上限同口径；是会话计数，不是指标 |
| 6 | `demands[MGRAPH-D07]` 缺口说明（PAGE:230-240） | 只写 CMS/协作版本 | 追加：40-3 回滚分组计数、40-4 版本 `stats`、publish / rollback `results` 同属 DN-A03-09 建议范围；版本列表「改动计数」不挂 ⓘ；40-3 与 40-4 是同一套分组键 + 同一求差函数，不是同一份数据 |
| 7 | `semantic_layer.metric_open_note`（PAGE:140-143） | 写「本页 kit N/A…」 | 追加一句：34–40 无算法生成句，维持 `n/a_ops`；九类计数按「DN-A03-09 建议范围，待 PM / 数据 Lead 确认」处理，不注册 `metric_id` |
| 8 | `items` 的 `建议取值/取值口径`（PAGE:268、:336、:353） | 「无指标；编辑器写操作 / 编辑会话历史 / CMS 协作版本」 | 分别在 002、006、007 行末尾追加「九类计数按 DN-A03-09 建议范围，不挂 ⓘ」 |
| 9 | `semantic_layer` 之后（可选） | 无 | 新增一个小块 `metric_guardrails`：`source: sdd/l2/TS-L2-M10-GRAPH-METRIC.md`、`no_metric_id: true`、`no_d4_change: true`、`count_exemption: DN-A03-09（建议范围，九类，待 PM / 数据 Lead 确认）`、`manual_strength: 编辑值，不进 M_TECH_* / S4，UI 标「人工」`、`stats_shape: API §3.4 分组 JSON` |

不改项（明确）：

- `srs02_boundary`（PAGE:28-41）与 `leaf_count: 7`、`seq: 34-40` 不动。
- 七条 `demands` 的 `差集判定: n/a_ops`、`metric_id: null`、`A1需规ID: null` 不动。
- `metric_open_status: present`、`kit_or_na`、`semantic_debt` 不动。
- `scope_exclusions` 与 `srs05_do_not_map` 不动。

## 6. 边界：不新注册、不改 D4、不替 OPEN 拍板

| 边界 | 本册做法 |
|---|---|
| 不新注册 `metric_id` | 34–40 原文无算法生成句；`M_TECH_*` 已覆盖读面。登记走 data-agent 的 seed / 矩阵，本册只给判定与证据 |
| 不改 D4 | 相关指标（`M_TECH_GRAPH_STRUCT` / `M_TECH_EDGE_STRENGTH` / `M_TECH_PATH_*` / `M_TECH_GRAPH_105_1`）均维持 `mock`（MATRIX:464、:592、:618、:817、:842、:867）。本页计数不是指标，没有 D4 可改 |
| 不替 `DS-02-METRIC-OPEN-L01` 拍板 | `weight` / `strength`（加权度）是否挂已有 ID 或按 D1 missing 显红问号，留在 OPEN（DS02-GM:51；OPEN:112-121）。本册只确认叠加不改这两者的取值与身份，不给结论 |
| `graph_tech_edge` 不作任何指标源表 | 该表只是维护工作集；`M_TECH_EDGE_STRENGTH` 等的注册对象是 IPC4 共类网络边，不是本表（DS02-GM:30）。`strength_manual` / `strength_auto` 不进任何 8 件套（DATA-METRIC-S3） |
| 不重开 DS02 已签收口径 | 读图侧结论以 `TS-L2-DS02-GRAPH-METRIC` / `TS-L2-DS02-PATH-METRIC` 为准；本册只追加「维护层不改口径」的论证 |

## 7. 会签关注点（v2 剩余）

1. **DN-A03-09 九类范围待裁**：35-3 四项、39-1、40-3、40-4、publish `results`、rollback `results`。裁定 A8 明确由协调方写请示单、监管人转交 PM / 数据 Lead；回执前文档统一写「建议范围，待确认」。
2. **「显示集合变小」是否知会 DS02 监管人 `human:淮政玮`**：删存量点 / 删种子边后全景少点少边少路径，不是口径变化，但已签收页面的可见条数会变（PROD-METRIC-C6 知会项、ARCH §4.5）。
3. **40-3 / 40-4 求差函数必须在实现单写死**：裁定 B12 已定「同一套分组键 + 同一个快照求差函数」；`tech_edges.updated` 已在 API v2 定为确定键，API / DATA 的实现单只需明确求差函数的落点。
4. **S4 分数种子断言**：已从「建议」升级为必修（DATA-METRIC-C2）；实现单必须包含 fail-closed 断言与 `--check` fixture-only。
5. **`weight` / `strength` 身份问题**：本册按 ARCH §9-3 不拍板，仍留在 `DS-02-METRIC-OPEN-L01`。若审稿身份认为应在本次收口，需要明确改派。
6. **历史 `stats` 四种旧形状的界面兼容**：不回填、缺组不补 0，由 FE 实现单按 §2.3-6 落地。

## 8. 会签回应（v2 / v2.1 清理）

| 来源 | 编号 | 级别 | 处置 | 落地 / 理由 |
|---|---|---|---|---|
| 裁定 | A8 | 拍板 | 采纳 | §0、§2.1、§2.3-7、§7-1：统一写「按 DN-A03-09 建议范围，待 PM / 数据 Lead 确认」；范围九类 |
| 裁定 | B1 | 统一口径 | 采纳 | §2.2-7、§2.3-4、§2.3-6：`stats` 以 API §3.4 分组 JSON 为唯一口径；历史四种旧形状兼容 |
| 裁定 | B2 | 统一口径 | 采纳 | §3.2：坐标列改 `layout_x` / `layout_y` |
| 裁定 | B9 | 统一口径 | 采纳 | §3.1-1、§3.2：`strength_auto` 进黑名单，不得照抄实体边注释 |
| 裁定 | B12 | 统一口径 | 采纳 | §2.2-6、§2.2-7、§2.3-4、§7-3：同分组键 + 同求差函数，不是同一份数据 |
| 裁定 | B15 | 统一口径 | 采纳 | §2.2-1、§2.3-3：`tech_edge_count` 只计 active、双向 |
| 裁定 | B20 | 统一口径 | 采纳 | §3.1-2：弹窗「关系强度（人工）」、悬浮/详情「人工」、不挂 ⓘ |
| ARCH-SIGN | ARCH-METRIC-C1 | 必修 | 采纳 | §3.1-1、§3.2：补 `strength_auto` 黑名单 |
| ARCH-SIGN | ARCH-METRIC-C2 | 建议 | 采纳 | §2.2-7、§2.3-4：引用 API §3.4 冻结键，保留「预览与版本列表同结构」（原单所指 §3.3/§3.5 在本稿对应 §2.2/§2.3 计数规则，按实质落点处理） |
| ARCH-SIGN | ARCH-METRIC-C3 | 建议 | 采纳（升级为必修） | §3.4、§3.5：按 DATA-METRIC-C2 写 fail-closed 断言，不再只作技术债 |
| DATA-SIGN2 | DATA-METRIC-C1 | 必修 | 采纳 | §3.1-1、§3.2、§3.4：`strength_auto` 全链路禁读；SEED-L01 仅作快照 |
| DATA-SIGN2 | DATA-METRIC-C2 | 必修 | 采纳 | §3.4、§3.5：S4 脚本级 fail-closed 断言；`--check` fixture-only |
| DATA-SIGN2 | DATA-METRIC-C3 | 必修 | 采纳 | §2.2-1：`status='active'` + 双向 |
| DATA-SIGN2 | DATA-METRIC-C4 | 必修 | 采纳 | §2.3-4：改为「同一套分组键 + 同一快照差异函数」 |
| DATA-SIGN2 | DATA-METRIC-S1 | 建议 | 采纳 | §3.2：`layout_x` / `layout_y` |
| DATA-SIGN2 | DATA-METRIC-S2 | 建议 | **部分不采纳** | 拆分文案采纳（§2.2-6、§2.3-5）；但 `X` 用 `total`（含恢复项），不采用「X 只计 removed+updated」。理由：API §4.3 与 PROD 文案均以 `total=added+removed+updated` 为差异总数，只计两项会让确认框遗漏「恢复」量 |
| DATA-SIGN2 | DATA-METRIC-S3 | 建议 | 采纳 | §3.2 末、§6：`graph_tech_edge` 不作任何指标源表 |
| DATA-SIGN2 | DATA-METRIC-S4 | 建议 | 采纳 | §2.2-8：补 `graph_version.publish_results` 同事务持久化 |
| DATA-SIGN2 | DATA-METRIC-S5 | 建议 | 采纳 | §2.2-4：按 gross 计，文案「将隐藏（上限）」 |
| DATA-SIGN2 | DATA-METRIC-S6 | 建议 | **部分不采纳** | 「种子英文码不作指标维度」采纳（§3.2 改为「列宽见 DATA 册」）；不再写死具体列宽，理由是列宽归 DATA DDL（DATA v2 已定 `VARCHAR(64)`），指标册不应锁死实现宽度 |
| API-SIGN | API-METRIC-C1 | 必修 | 采纳 | §2.3-4、§7-3：改正「同源」表述，区分目标版本 `stats` 与预览 `counts` |
| API-SIGN | API-METRIC-C2 | 必修 | 采纳 | §2.2-9、§1.3、§3.1-5、§7-1：六类扩为七类，35-3 再扩四项后共九类，补 rollback `results` |
| API-SIGN | API-METRIC-C3 | 必修 | 采纳 | §2.2-6：按 API 键矩阵逐组写，不再「各拆增/删/改」 |
| API-SIGN | API-METRIC-C4 | 必修 | 采纳 | §2.3-2：`counts:null` 为合法态，显示不可回滚原因 |
| API-SIGN | API-METRIC-C5 | 建议 | 采纳 | §3.2：`layout_x` / `layout_y` |
| API-SIGN | API-METRIC-C6 | 建议 | 采纳 | §2.2-7、§2.3-6：历史 `{"ops":N}` / 扁平 / `{}` / NULL 兼容，缺键不补 0 |
| API-SIGN | API-METRIC-C7 | 建议 | 采纳 | §2.2-6、§2.3-5：「将变更 X 项（恢复 A / 移除 R / 还原 U）」 |
| API-SIGN | API-METRIC-C8 | 建议 | 采纳 | §2.2-5：39-1 为前端草稿净差 op 条数，`validate.op_count` 仅预览 |
| API-SIGN | API-METRIC-C9 | 建议 | 采纳 | §2.2-8：`results` 随版本持久化，历史 `null`，`failed_items` 不聚合 |
| PROD-SIGN | PROD-METRIC-C1 | 必修 | 采纳 | §3.1-2：固定「人工」标签落点，不挂 ⓘ |
| PROD-SIGN | PROD-METRIC-C2 | 必修 | 采纳 | §2.2-8：「保存成功：N 项已生效，M 项未生效」 |
| PROD-SIGN | PROD-METRIC-C3 | 必修 | 采纳（按 B12 解释） | §2.2-6、§2.2-7、§2.3-4、§2.3-5：同一套键结构，不要求同一份数据；两套时态文案 |
| PROD-SIGN | PROD-METRIC-C4 | 建议 | 采纳 | §2.3-2：0 / null / 取不到三类规则 |
| PROD-SIGN | PROD-METRIC-C5 | 建议 | 采纳 | §1.2 40-1 行改为「成功提示（无固定数字；若展示回执计数见 §2.2-8）」 |
| PROD-SIGN | PROD-METRIC-C6 | 建议 | 采纳 | §3.5：新增可执行验收断言 |
| PROD-SIGN | PROD-METRIC-C7 | 建议 | 采纳 | §5：九处 diff 全量保留，`updated` 改 2026-11-13，九类计数口径写入 |

> 不采纳仅两条，均为**部分不采纳**且不改变结论：DATA-METRIC-S2 的 `X` 口径、DATA-METRIC-S6 的列宽写死。其余条件全部采纳；ARCH-METRIC-C3 按更严的 DATA-METRIC-C2 落为必修断言。

> **v2.1 清理（2026-11-13）**：PROD-METRIC-C3 闭合——`tech_edges{added,updated,removed}` 去掉「若 API 补」；「撤回」统一为「移除」；35-3 扩为四项（技术点关系 / 实体关系 / 实体挂接 / 全景隐藏存量关系），计数类共九类；`rel_type` 列宽改为「见 DATA 册」；`tech_edges.updated` 定为确定键。
