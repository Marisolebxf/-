---
name: gkx-ent-stat-cover
description: >
  One-by-one human-gated rewrite of ENT STAT/COMPUTE metric seed + calc-logic
  (COVER-STAT-L01). Shared field rules only; each metric still needs human
  confirm. Use when ENT-SYNTH-METRIC-COVER-STAT-L01, 一条一过, source_tables
  DWD<-ods, 国内外一起算, is_mock, 空字段无法计算, 分场景计算,
  demo vs 生产, calc_logic_ref, or 企业指标逐条改 seed.
---

# 企业 STAT 一条一过（人确认，非自动流水线）

任务：`ENT-SYNTH-METRIC-COVER-STAT-L01`。规约真源：`agent-delivery/data-lineage-policy.md`。本 skill **只固定共用护栏**；口径/公式/是否并国外 **每条不一样**，必须人拍。

**禁止**：整批改 55 条；未点头就写 YAML；把本叶做成全自动脚本。

## 每条流程

1. 按 seed 登记顺序取下一条（STAT/COMPUTE）。国内外规则后追加的，已落盘条要先回看再往下。
2. 对照：现 seed、细稿 `metrics/calc-logic/ENT/{id}.md`、项目 DWD DDL、王惠底稿。
3. ODS **只探针**（live `gkx` @ `CONNECTION.md`；demo ODS 未同步则不查 demo）。看有没有数、有没有列。密码不进仓。
4. **空值检查（强制）**：计算用到的 ODS/DWD 列若全空、全 NULL、全 0 占位，或仅有 DWD mock 填数而 ODS 无有效值 → **不能当能算完**。拟改当场披露缺口。`formula` **先写目标口径**（怎么算），再写 **当前无法执行** + 原因。禁止只写「无法计算」把口径抹掉；禁止只靠 `is_mock` 或细稿藏缺口。DWD 有列但源空 ≠ 接通。
5. **先拟改清单**（现状 → 拟改；不改的也写明；缺口必须出现在拟改里）。等用户点头。
6. 点头后再改 `cfg_metric-ENT-seed.yaml` + 对应细稿。**企业细稿只在 `metrics/calc-logic/ENT/`**，文件名=`{metric_id}.md`（如 `M_ENT_PATENT_GRANT_COUNT.md`）。没有就新建；有历史就改/加，不另开路径。seed 写 `calc_logic_ref: "metrics/calc-logic/ENT/{metric_id}.md"`。矩阵 D3/D4 本波默认不升。未要求不 commit。
7. **落盘后立刻把变更结果列给用户再审**，不等用户来问。未过第二审，不开始下一条。对照至少含：
   - 改了哪些文件
   - 8 件套字段 **改前 → 改后**（`definition` / `formula` / `source_tables` / `source_systems` / `is_mock` / `version`；有则含 `calc_logic_ref`）
   - 国内外是否 UNION、选产业怎么处理
   - 细稿补了什么（探针、缺口、**落表目标或「无独立目标表」**）；**没改的也写「未动」**（尤其 D3/D4、矩阵）
   - 源列空/占位时：`formula` 是否 **口径仍在** + **当前无法执行**（不能只写无法计算，也不能只写 SQL）
   - 稍复杂 / 分场景 / demo 与生产算法不同：细稿是否已写实现方案（见下方）
   - 用户说改再改；说过了再下一条。

## 共用字段（条条一样）

| 字段 | 写什么 |
|------|--------|
| `source_tables` | **血缘链**：`项目DWD <- ods: 三方表`。左端必须是 `gkxlumenx_dwd` 表名（`enterprise_*` / `enterprise_forg_*`），不写库名前缀。右端 ODS 表名，不写 `gkx.`。禁止把 `gkx.dwd_*` 当计算 FROM。 |
| `source_systems` | 要素库中文名（国内机构要素库 / 国外机构要素库 / 产业链要素库）。不写库名、表名、行数探针、`Mock @ batch`。 |
| `formula` | **先写目标口径**（落左端 DWD 字段：怎么算、GROUP BY、除零）。源空/缺列时 **口径仍保留**，后面加 **当前无法执行** + 原因。禁止用「无法计算」替换口径；禁止用待建列、DWD mock 填数假装已接通。 |
| 落表 | **每条必须有目标表/目标列**（结果写哪）。源表 ≠ 目标表。现网没有 → 细稿标 **缺口：无独立目标表**，`formula` 点名建议表且写「当前无此表」。禁止把查询源表说成已落库。本波不改 GDF DDL。 |
| `is_mock` | 跟矩阵 D4：`live` 才能 `false`；本波默认 `true`。ODS 有样例行不够改。 |
| `calc_logic_ref` | 必填。企业只写 `metrics/calc-logic/ENT/{metric_id}.md`。字段对照、探针、**分场景实现**、**落表/无表缺口**写 md，不进 8 件套。 |

**例外（默认不开，须人点头）**：二次 STAT/COMPUTE 左端允许结果表，右端写 `metric: {ID}`，不写 ODS。须写明依赖：先有上游出数，再做本条。本波已开：
- RANK/AVG 挂 MODEL：`M_ENT_TECH_RANK`、`M_ENT_CITY_AVG_TECH_POWER`（均 `tech_power <- metric: M_ENT_TECH_POWER_SCORE`）；`M_ENT_COMPETITIVENESS_RANK`（`ads_ent_competitiveness_score <- metric: M_ENT_COMPETITIVENESS_SCORE`；口径 RANK，生产禁止请求路径全表窗口）。同类商业力排名未点头不准套。不改 SCORE/MODEL 叶。
- 短板 COUNT 挂竞争力 L3：`M_ENT_SHORTBOARD_COUNT`（`ads_ent_competitiveness_score <- metric: M_ENT_COMPETITIVENESS_SCORE`；用 L3+同业均值，不用总分）。
- 密度挂 COUNT：`M_ENT_CITY_DENSITY`（`enterprise_region_summary <- metric: M_ENT_REGIONAL_COUNT`）。区域密度未点头改挂则仍自写 COUNT，不准套。
- 招引 / 培育 demo 二次 COMPUTE：`M_ENT_ATTRACT_SCORE`、`M_ENT_CULTIVATE_SCORE`。禁止 `ads.enterprise_score` / diagnosis mock 假接通。培育恢复项不得挂 Q018 痛点转分。
- 推荐企业数二次 COUNT：`M_ENT_RECOMMEND_COUNT`（`metric: M_ENT_ATTRACTION_INDEX`、`metric: M_ENT_CULTIVATION_INDEX`）。禁止挂 SCORE。禁止数 demo `svc_*`。
- 重点概览匹配数二次 COUNT：`M_ENT_KEYPANO_MATCH_COUNT`（`enterprise_industry_chain` + `key_enterprise <- metric: M_ENT_KEY_TOTAL`；全量 `chain_code×node_stage` 预聚合；选链是 API 过滤，不进口径）。
- 重点概览覆盖类型数二次 COUNT：`M_ENT_KEYPANO_TYPE_COUNT`（六类 `enterprise_tag.tag_code` + 名单 + 上链；全量链×链位；选链是 API 过滤）。
- 重点概览覆盖区域数二次 COUNT：`M_ENT_KEYPANO_REGIONAL_COUNT`（省+市+县 + `region_scope` 复合区域；热门城市不另开键；全量链预聚合；选链是 API 过滤）。
- 重点概览整链资质分布二次 COUNT：`M_ENT_KEYPANO_QUAL_DISTRIBUTION`（六类 `tag_code` × 全国/省/市/县/复合区域；格子不可加；全量立方；选链/选区是 API 过滤）。
- 重点概览类型分布二次 COUNT：`M_ENT_KEYPANO_TYPE_STRUCTURE`（链×链位×六类家数；无区域维；全量预聚合；选链/链位是 API 过滤）。
- 重点概览区域分布二次 COUNT：`M_ENT_KEYPANO_REGIONAL_DISTRIBUTION`（整链按全国/省/市/县+复合区域 COUNT 家数；热门城市并入市；选链/选区是 API 过滤）。
- 重点概览企业清单二次 STAT：`M_ENT_KEYPANO_ENTERPRISE_LIST`（成员表 `org_id+chain+stage`；名称/六类标签/`region_id` 查询 JOIN；CMS 不进口径；选链/分页是 API）。
- 重点名单根 STAT：`M_ENT_KEY_TOTAL`（只国内；专利总量≥**50**，件数跟 `PATENT_TOTAL`；技术交易额/标签不进；N=50 团队临时，Q038 不升 🟢）。
- 专题领域分布 STAT：`M_ENT_DOMAIN_DIST_TOPIC`（`COUNT(DISTINCT org_id) FROM enterprise_industry_chain`，L0→`industry_cluster_map`，`GROUP BY` 年+集群；同比同格；选产业是 API）。
- 专题区域数量占比 STAT：`M_ENT_REGIONAL_COUNT_TOPIC`（只国内；家数 `COUNT(DISTINCT org_id) FROM enterprise_base`；占比=区域/当期集合；规模=数量，不挂营收；选产业是 API；不 reuse 展示 `REGIONAL_COUNT`）。
- 专题深圳清单 STAT：`M_ENT_SZ_LIST_TOPIC`（只国内；深圳=`region_id LIKE '4403%'` 跟 `SZ_COUNT`；成员 `(org_id,chain_code,node_stage)`；角色=上中下游；选链是 API；不 reuse `SZ_CHAIN_POSITION`；Q076 团队暂定 D，仍 🟡）。
- 专题重点类型分布二次 STAT：`M_ENT_TYPE_DIST_TOPIC`（对象=`key_enterprise <- metric: M_ENT_KEY_TOTAL`；四类 `tag_code` foreign/high_tech/sme/listed；占比分母=当期名单去重；选产业是 API；不并专精特新/小巨人；不 reuse `TYPE_COUNT`；Q072 A + Q038 仍 🟡）。
- 重点资讯月总数 STAT：`M_ENT_BASE_97_4`（`COUNT(*) FROM enterprise_news GROUP BY` 年-月；环比上月；不按 `org_id` 分组；不挂 `KEY_TOTAL`；融资/并购不进；选产业是 API；企业时间线走 `DEV_HISTORY`）。
- 覆盖未来产业数 STAT：`M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`（同 `DOMAIN_COVERAGE_COUNT` 管道，只数 `cluster_group='fut'` / `CL-FUT-01`～`05`，上限 5；选产业不进口径；不 reuse 覆盖领域数；Q068 仍 🟡）。
- 全球科研人数 STAT：`M_ENT_RESEARCHER_COUNT`（最新年 `development_employee` ∪ `rd_staff` 再 SUM；选产业成员表半连接；禁从业人数/RD 金额；① formula 与有数分开；② 空置率/无列不进无法执行；目标建议 `enterprise_researcher_year_sum`，当前无此表；Q-E32-01 仍 🟡）。
- 明星企业数 STAT：`M_ENT_STAR_ENTERPRISE_COUNT`（CMS `star_roster_item` 已发布名单 `COUNT(DISTINCT enterprise_code)`；选产业是 API；≠ `KEY_TOTAL` / `tag_code=star_enterprise` / honor / TopN；目标建议 `ads.ent_star_roster_count`，当前无此表；Q048/Q041 仍 🟡）。
- 高企数量 STAT：`M_ENT_HIGH_TECH_COUNT`（只国内；`enterprise_tag.tag_code='high_tech'`；不按产业滤；码在就算；禁止 `tag_name` 模糊含；目标建议 `ads.ent_high_tech_count`，当前无此表；Q010 仍 🟡）。
- 平均研发投入 STAT：`M_ENT_AVG_RD_INVESTMENT`（选定未来产业内 AVG；输入=`ads.ent_rd_latest` + `enterprise_industry_chain`；查询半连接 `DISTINCT org_id` 后再 AVG；多选=并集去重；未选不计算；国外无上链不并；禁止上市财务 / 各产业 sum/n 加总 / 无过滤 JOIN；① DWD 有列即可写；② ODS 空不进无法执行；快照表当前无；Q068 仍 🟡）。
- 研发投入占比 STAT：`M_ENT_RD_INVESTMENT_RATIO`（按企 `rd_investment/revenue*100`，最近完整年；不挂产业；该企除零=该企业无法计算；① formula 与有没有数分开；② ODS 空/mock 不进无法执行；目标建议 `ads.ent_rd_ratio_latest`，当前无此表）。
- 供应商数量 STAT：`M_ENT_SUPPLIER_COUNT`（按企 `COUNT DISTINCT related_org_id` WHERE `relation_type='supplier'`；一级=边自身；① DWD 边表能数；② ODS 无源/mock 不进无法执行；目标建议 `enterprise_supply_summary`，当前无此表；Q017）。
- 产业链完整度 STAT：`M_ENT_CHAIN_COMPLETENESS`（`k/K*100`，K=INB 叶子，k=地区企业环节∩叶子；默认全目录；K=0 该次无法计算；① 上链表+叶子目录能写；② `node_id` 空/链码未对 INB 不进无法执行；QC01 仍 🟡）。
- 链中角色 STAT：`M_ENT_SZ_CHAIN_POSITION`（叶子 JOIN `chain_node.position` 按游 COUNT；对不上进 unlabeled；① 能写；② 缺口必标：CH 非 INB、`node_id` 空、`region_id` 缺列、ODS 无 position；不写无法执行）。
- **缺口铁律（2026-08-31）**：缺列 / 缺维 / 缺目录 / 未灌 / 无目标表，一律标「缺口」，**禁止**写成「当前无法执行」。`formula` 只写怎么算。
- 深圳企业数 STAT：`M_ENT_SZ_COUNT`（`region_id LIKE '4403%'`；选产业 JOIN 上链；① 能写；缺口：主档无 `region_id`）。
- 城市平均技术力二次 STAT：`M_ENT_CITY_AVG_TECH_POWER`（`AVG(tech_power_index) GROUP BY LEFT(region_id,4)`；依赖 SCORE；缺口：无 `region_id`、SCORE 未出分）。
- 专利授权量 STAT：`M_ENT_PATENT_GRANT_COUNT`（按 `first_assignee_org_id` COUNT 授权；缺口：DWD 待补第一人两列）。
- SYNTH 活力/要素排名二次 STAT：`M_SYNTH_VIT_RANK`（`<- metric: M_SYNTH_VIT_INDEX`）、`M_SYNTH_ELEM_RANK`（`<- metric: M_SYNTH_ELEM_INDEX`）；`RANK()` 于当前对比范围；无指数不进榜；同分并列；选范围是 API；指数未出数当前无法执行。细稿在 `metrics/calc-logic/SYNTH/`。WEIGHT / RELATION_INPUT / COMPLETENESS 不套本条。
- **六类类型判定（2026-08-30 人点头）**：外资/高新/小微/上市/专精特新/小巨人一律 `enterprise_tag.tag_code`（`foreign`/`high_tech`/`sme`/`listed`/`little_giant`/`little_giant_pro`）。禁止 `enterprise_type` / `is_listed` / `org_size` / `sme_tech`。① DWD 标签关系可算完；② ODS→DWD 灌数另写，不进「无法执行」。

## 分场景与 demo / 生产（稍复杂指标强制）

8 件套 `formula` 只留**一条目标口径**。下面这些**不进 seed**，必须写进 `calc_logic_ref` 细稿：

- 要用**场景**区分算法：单企画像 / 列表批量 / 筛选合计 / 最新一年 vs 累计等。每个场景写：入口、过滤、粒度、SQL 或步骤。
- **demo 数据量少、生产数据量大**时算法通常不同（demo 可全表扫；生产要按 `org_id`/年分区、预聚合、禁止全表 `GROUP BY`）。细稿分两小节写实现，标明各自适用库（`demo_gkxlumenx_*` vs `gkxlumenx_*`），不要假装一套 SQL 两边都能扛。
- 场景之间口径不能打架；和 seed `formula` 不一致要写明为什么（实现优化，不是改口径）。

细稿没有「分场景 / 实现方案」节就补上。路径固定：

`agent-delivery/metrics/calc-logic/ENT/{metric_id}.md`

示例：`calc_logic_ref: "metrics/calc-logic/ENT/M_ENT_PATENT_GRANT_COUNT.md"`。禁止写到别的模块目录，禁止用中文文件名另起一份。

## 国内外（架构师：有些统计要一起算）

- 有对等项目 DWD 表才 UNION（如主档 `enterprise_base` ∪ `enterprise_forg_base`）。
- 无对等表（如国外标签）：不造表，细稿写明，本条只国内。
- 港澳台 ≠ 国外。国外高校/科研表不是企业主档。
- 选产业过滤：国外无上链表则暂不并入该过滤结果。

## 不要动

- `task-registry.yaml`（走 MCP）
- 整文件当 8 件套答案去读 seed/矩阵（查身份用 `gkx-metric-lookup`）
- 本波 MODEL/GRAPH；本波不因 ODS 有数升 D3 `full` / D4 `live`
