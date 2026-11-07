# TS-L2-M10-ENT-SIGNOFF-API · 维护管理 · 关键实体与关系 · 接口会签

- 角色：`agent:api-agent`
- 日期：2026-11-07
- 对象：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（主审，重点 §0 范围 / §6 核查表 / §7 会签点）；交叉核对 `SCI-INT-A03.yaml`（write_back_design_draft + 22 卡 contract_draft）、FE as-built（`repos/lumen-ui-science-pc/src/views/situation/maintain/maintainModel.ts` L523-679、`src/types/maintain.ts` L127-185）、需规序 41–47（`bid-reference/srs/02-科技信息展示系统/科技发展态势/科学技术全景.md` L365-468）、网关路由事实（`repos/lumen-svc-platform/helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml`）、先例 `TS-L2-M10-LAYER-API.md`（分册骨架）
- 监管：`human:刘剑锋`
- 范围：只读核对。不改被审稿，不动 task-registry / WBS，不 git 操作。ENT-ARCH 是定义稿（不写 OpenAPI 字段），本页核它给 API 分册留的底是否齐、映射是否对；DTO/错误码终裁归 `TS-L2-M10-ENT-API`

## 结论

**有条件同意**。条件 1 条（op 命名与 A03 契约源不一致，三处一行级更正）；备注 7 条（不阻塞，落 API 分册/接线单/在册决策）。条件清掉后，本叶可作为 ENT API 分册的架构底座。

## 条件（会签生效前需修订 ARCH 稿）

1. **op 名三处与 A03 不符**（A03 是 ops[] 枚举的唯一上游草案，ARCH §6 是 D18 核查表，分册会照抄）：
   - §0 序 44（L22）与 §6 叶 44（L102）写 `op=delete_edge`——A03 中 `delete_edge` 是**技术–技术边** op（INT-A-TECH-205，srs seq 37，属已排除的 34–40 分区）；本页「实体关系删除」对应 **`op=delete_entity_edge`**（INT-A-X-218，A03 L921-925，request=[base_version, edge_key]，response 带 edge_source(auto|manual)）。
   - §0 序 46（L24）、§3 G1（L67）与 §6 叶 46（L103）写 `op=update_edge`——**A03 全文不存在此 op**（grep `op=` 全集 10 个，见核对一）；「实体关系编辑（合作/引用/影响+强度+时间范围）」对应 **`op=update_entity_edge`**（INT-A-X-220，A03 L1008-1012，patch(rel_type, strength_manual, time_range)——G1 要补的强度/时间范围 A03 草案已含）。
   - §6 叶 45（L102）写「update_node patch（三方实体=覆盖层）」——三方实体属性编辑是独立 op **`update_entity_overlay`**（INT-A-X-219，A03 L964-968），request=[entity_type, entity_id, patch(display_name, type, description, importance_level)]，与 update_node 的 [technology_id, patch(...)] 形状不同；现写法会诱导分册用 update_node 承载三方实体。§0 序 45（L23）本身写法正确（update_node 限定技术点、覆盖层另述），只是没落 op 名。

## 核对一：op 全集核对（审查重点 ①）

A03 `op=` 全集（grep 实证，10 个）：`add_node / delete_node / add_edge / delete_edge / update_node / hang_entities / unhang_entities / delete_entity_edge / update_entity_overlay / update_entity_edge`。

按本叶范围（序 41–47）应收 7 个写 op，与 §6 逐行对：

| op（A03） | 对应叶 | §6 覆盖 | 判定 |
|---|---|---|---|
| hang_entities | 42 | ✓（L99） | 一致 |
| unhang_entities | 43 | ✓（L100） | 一致 |
| delete_node（+cascade+impact） | 43（技术点本体） | ✓（L100） | 一致 |
| update_node | 45（技术点） | ✓（L102 前半） | 一致 |
| delete_entity_edge | 44 | ✗ 写成 delete_edge | 条件 1 |
| update_entity_overlay | 45（三方实体） | ✗ 未落 op 名 | 条件 1 |
| update_entity_edge | 46 | ✗ 写成不存在的 update_edge | 条件 1 |
| add_node / add_edge / delete_edge | 34–40（报价划掉） | 未收 | 正确未收（delete_edge 系 44 误引，非有意收录） |
| ops[] 批量 + validate/preview | 47 | ✓（L104） | 方向一致；validate/preview 双卡归并见核对三 |

无漏叶（41–47 每行都有裁定）；漏/错集中在 op 名。另：FE as-built 的 `addPanoramaRelation`（maintainModel.ts L628-652，手动新建实体间关系）**在 A03 无对应 op、SRS 41–47 无对应需规行**——属 demo 超需规功能，分册须显式放弃或补 op（沿 LAYER §0「显式放弃」先例），见备注 6。

## 核对二：演示态 → 契约映射可行性（审查重点 ②）

| 演示态（as-built） | 契约（A03） | 判定 |
|---|---|---|
| `recommend[]`（id/name/type/strength/year/description，maintainModel.ts L530-536） | GET recommend-entities：entity_id/entity_type/name/strength/year/in_panorama/metric_id（A03 L707-713） | 可行。缺 description（demo 卡片展示用）——分册补或显式放弃（备注 5）；in_panorama 可替代 demo 的按名去重判断（A03 L809 已注明正式须按 entity_id 去重） |
| 筛选/排序（ENTITY_TYPES 六值含「全部/技术点」） | request entity_types[人,机构,论文,专利] + sort_by(strength\|time\|name) | 可行。枚举差集：契约无「技术点」（备注 5）；G4 写 sortBy=strength\|time 漏了 name（A03 L711 有，备注 4） |
| keyword 搜索 | INT-A-X-214 `?keyword=` + scope(list\|global)（DN-A03-08 在册） | 可行，范围待 DN |
| `panoramaEntities[]` + hang | op=hang_entities：hung[]/skipped_already_in[]/edges_created[]（A03 L796-797） | 可行。demo importance 由 strength≥0.88 推断是 Mock 行为，分册写死来源（overlay patch 或不返回） |
| `panoramaRelations[]`（type/strength/timeRange，types L179-185） | update_entity_edge patch(rel_type, strength_manual, time_range) | 可行，G1 字段与 demo `PanoramaRelationDraft`（type/strength/timeRange）逐字对上 |
| 删除实体级联删关系（L596-608） | unhang downstream 只写「实体–技术边」（A03 L881） | SRS-43（L408）原文是「同时删除与该实体相关的**所有关系**」——分册把 unhang 级联范围写全到实体–实体边（备注 3） |

结论：映射可行，形状缺口全数可落分册，无架构级障碍。

## 核对三：读端点缺口清单（审查重点 ③，API 分册必须收录）

稿内只有方向（§6 叶 41「Java GET」、impact、validate）。逐端点核对 A03 后的分册读端点清单：

| # | 端点（沿 A03 草案） | 依据 | 状态 |
|---|---|---|---|
| R1 | `GET /topic/v1/tech/graph/{technology_id}/recommend-entities`（含 keyword 变体） | A03 INT-A-X-213/214（L707/L751） | 草案齐，分册补 description 取舍 |
| R2 | **全景现状读**（当前技术点已挂实体+边，维护页两栏右栏数据源） | A03 无卡（读面归 A02）；ARCH 调用图 L42 自己写了「读：…全景现状…」但无路径 | **缺口，分册必定义**（如 `GET .../tech/graph/{technology_id}/panorama`，或声明复用 A02 读面+挂接表拼装并写明拼装方）。同时是 projection_status 对外暴露的载体（核对四） |
| R3 | `GET /topic/v1/tech/graph/nodes/{id}/impact` | A03 INT-A-TECH-202（L227） | 草案齐；实体侧删除确认框的影响说明走 op 响应 impact_note（A03 L926），若要提交前预检需扩展本端点——分册定 |
| R4 | `POST /topic/v1/tech/graph/changes:validate` vs `POST .../changes:preview`（dry_run） | A03 **两卡并存**：INT-A-TECH-201 validate=名称规范化+查重（L183）；INT-A-X-221 preview=dry_run 演算 diff（L1051）。ARCH §6 叶 47 归并成一句「validate 返回影响面+计数」 | 分册须归一：建议 preview 承载叶 47 预览统计、validate 保留名称查重（34–40 用），两码事别混一个端点 |
| R5 | **发布动作落点** | A03 INT-A-TECH-209：publish 在 `POST /topic/v1/tech/graph/versions`（L529）；ARCH 调用图边注「changes（draft→approve→publish）」暗示 changes 端点自带发布 | 两处不一致。分册必须一处写死（建议沿 A03：versions 承载 publish，changes 只到 change_set 受理/审核）；否则 41–47 的写永远到不了 Nebula，链路断在半截 |
| R6 | `GET /topic/v1/tech/graph/conflicts`（可选） | A03 INT-A-TECH-211（L617，可选），DN-A03-03 在册 | 首版可不做，分册标 reserved |

不收：`GET /topic/v1/tech/domains`（INT-A-TECH-201，建点用，ENT 41–47 无建点）。

## 核对四：错误模型（审查重点 ④）

- **乐观锁 409**：A03 L77 与 ARCH §1 要点 4 表述一致（base_version 不符 → 409+差异列表，前端提示合并）。方向清晰；**差异列表的字段形状未定**（current_version? 冲突 ops 清单?）——分册职责，列入输入清单。前端状态机可判：409 后本地栈不丢（A03 INT-A-TECH-200 test「前端保留本地草稿不丢编辑」同语义）。
- **projection_pending**：A03 L70/L534/L555 与 ARCH §1 要点 2 一致（MySQL 已提交、Nebula 失败 → 版本标 pending+补偿重放，页面读旧版标「图谱更新中」）。对前端的状态机含义**方向清晰、暴露面未定**：「图谱更新中」标志从哪个读端点带回（建议 R2 全景现状读的 meta 字段）、projection_status 枚举集合（ok|projection_pending|failed?）、pending 期间能否继续提交（base_version 已推进，应可继续）——三项归分册写死。
- 判定：定义稿层面语义无矛盾，可直接进分册，无架构级歧义。

## 核对五：DN-07 与路径前缀冻结（审查重点 ⑤）

- **控制器路径 `/topic/v1/tech/graph/**` 可先行冻结**，三源一致：详设 11 复用 `/topic/v1/{element}/graph/**`（A03 premise L30）；A03 全部 22 卡同前缀；topic 侧模块惯例（`gkxlumen-topic-enterprise/chain/svc/policy` 内部服务路径统一 `/topic/v1/**`，SmartSearchService.java L61-65、gateway 注释 L36-64 实证）。
- **对外完整 URL 不可在 DN-07 落定前单点冻结**：网关现有通用路由 `Path=/topic/** → lb://gkxlumen-topic`（gateway-dev.yml L74-77）——承载模块若是 gkxlumen-topic（ARCH §7.5 候选），外网即 `/topic/v1/tech/graph/**` 与 A03 逐字一致；若 DN-07 落在其他/新模块，按 enterprise/chain/svc/policy 先例外网多一段模块别名（`/{alias}/topic/v1/tech/**`），内网控制器路径不变。对分册的建议：**冻路径形状、URL 前缀留一个 FE BASE 常量位**，DN-07 落定只改一处，不构成冻结障碍。
- **一处需架构/网关侧一句话确认**：gateway-dev.yml L24 注释明文「前端禁止直连 innov/topic/metrics；展示侧三域数据一律经 display 聚合后返回」，而 ARCH 调用图是 FE 直打 `/topic/v1/...`。ARCH §5 已裁定「ENT 走 topic 侧 Java 门面而非 display」（合规依据成立），但网关注释未同步——分册冻结前需要网关策略补一句「维护页写操作走 topic 门面豁免此条」，否则实现单与网关口径打架。这属于 DN-07 的附属动作，不阻塞本叶。

## 事实错误清单

1. op 名三处（条件 1，证据见上：ARCH L22/L24/L67/L102/L103 vs A03 L921-925/L964-968/L1008-1012）。
2. 其余核过无硬伤：序 41–47 的需规引用（SRS L365-468 逐行比对）与 §0 裁定对应关系正确；§6 叶 41「真读」、42–47 写侧判定与 A03 dep_kind 一致；D15/D2/D18 引用与 `architecture-baseline.md` L134/L142 原文相符；FE as-built 引用（maintainModel.ts L523 起、types L127 起）与稿述「演示壳保持、接线单只改数据源」一致。

## 备注（不阻塞）

1. **DN-A03-04 被当已决写**：§0 序 45 把「三方实体=本地覆盖层」写成裁定，但 §2 待拍板清单未列 DN-A03-04（A03 L1086 在册、owner=甲方+主数据 owner）。分册冻 update_entity_overlay 的 op 形状安全（改的只是 downstream），建议 ARCH §2 补登一行保持台账一致。
2. **首版挂接对象来源缺前置**：34（建点）报价划掉、自建主表从 0 起（C02 INT-C-TECH-180 rows=0）、存量 TRSGraph 点 VID=tech:{名称} 无 technology_id——三者叠加，首版 ENT 页可能出现「有 hang op、无可挂技术点」。建议 ARCH 或 DATA 补一句「存量技术点批量导入主表并分配 technology_id」为首版前置（DN-07/数据侧动作），并顺带裁定 41–47 可否操作未导入的存量点。不影响 API 形状，影响 P2 联调可测性。
3. **unhang 级联范围**：见核对二末行，分册把级联写全（SRS-43 原文「所有关系」）。
4. **G4 漏 name**：ARCH §3 G4 写 sortBy=strength|time，A03 L711 是 strength|time|name，分册取三值。
5. **枚举差集**：demo ENTITY_TYPES 含「全部/技术点」，契约 entity_types 四值（人/机构/论文/专利）；recommend 响应缺 demo 在用的 description。两处接线单/分册二选一写死，沿 LAYER §0 差异表先例显式声明。
6. **addPanoramaRelation 无 op 承载**：见核对一末段，分册 §8「不做」显式放弃（或后续补 add_entity_edge，首版不建议）。
7. **hang 返回 strength 语义**：A03 INT-A-X-216 已有「105 边复用边权 / 无证据 strength=null 标待计算、不填 0」的降级口径，分册照抄写死即可。

## 给 API 分册（TS-L2-M10-ENT-API）的输入清单

**A. 读端点**：核对三 R1–R6（R2 全景现状读、R5 发布落点是两个必答题）。
**B. op 参数冻结建议**：
1. ops[] 封闭枚举 = A03 十 op，按本叶范围收 7 个（核对一表），条件 1 的三处名更正先行回填；
2. `edge_key` 形状沿 A03 INT-A-TECH-204（src,dst,rel_type,rank）；`time_range` 年粒度（A03 granularity time: year）；`client_op_id` 幂等键从 add_node 扩展到全部 op（重试安全）；
3. `ops[]` 单批上限定数（A03 INT-A-X-221 gap「上限未定」，建议 ≤50，超限 400）；批量部分失败语义沿 A03（failed_items 清单，版本 stats 与成功数一致）；
4. `technology_id` 类型早冻（十 op 每个都带，自建主表先行档即可定，INT64 或字符串二选一）；`entity_id` 对齐 C01/C03/C02 主数据（在册，分册留对齐注记）；
5. unhang 级联、hang strength、G4 sortBy 三值——备注 3/7/4。
**C. 错误模型**：409 差异列表字段、projection_status 枚举+暴露端点（挂 R2）、pending 期间可继续提交的语义（核对四）。
**D. 风格对齐 LAYER-API**：沿其骨架（§0 as-built 差异表 / 总则 / 资源分组 / 错误码汇总 / 枚举冻结 / 不做），ENT 册加一节「op 枚举与请求形状」（本叶无对应物，图谱写回特有）；§0 差异表把本页备注 5/6 的 demo 超需规项显式列「放弃」。

## 签收边界

- 本页是接口角色会签意见，不把任何任务标 done；签收归监管 `human:刘剑锋`。
- 条件 1 的修订由 ENT-ARCH 认领人（`agent:arch-agent`）落笔，本角色不代改被审稿。
- OI-A03-01 分档、G2 首版不做、「一张 G」作用域（OI-A03-03）属架构/算法/甲方角色会签范围，本页仅确认接口视角无异议。
