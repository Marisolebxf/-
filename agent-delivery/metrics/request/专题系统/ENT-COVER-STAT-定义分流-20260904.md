# COVER-STAT 55 条：定义分流（2026-09-04）

任务：`ENT-SYNTH-METRIC-COVER-STAT-L01`（ENT STAT 47 + ENT COMPUTE 2 + SYNTH STAT 6 = 55）。  
只分流**定义**。真缺列 / 缺表 / ODS 空 / 无目标表 **不进本单「请算法定」**。  
团队临时默认标 🟡，不升甲方 🟢，不升 D3/D4。

| 桶 | 条数 | 含义 |
|---|---|---|
| A 口径已清 | 14 | D1=`aligned`，本轮不当定义问题 |
| B 团队已钉 / 本轮就按此算 | 29 | 公式已写，只差签字或数据 |
| C 请算法先定 | 12 | 没有可执行口径，或和已拍板 Q 打架 |

---

## A · 口径已清（14）

剩下是数据、落表或上游 MODEL 出数，不发给算法改定义。

`M_ENT_TOTAL_COUNT` · `NEW_COUNT_Y` · `SZ_COUNT` · `SZ_CHAIN_POSITION` · `DOMAIN_COVERAGE_COUNT` · `AVG_RD_INVESTMENT` · `DEV_HISTORY` · `PATENT_TOTAL` · `PATENT_GRANT_COUNT` · `REVENUE_LATEST` · `REVENUE_GROWTH_RATE` · `PROFIT_MARGIN` · `MARKET_SHARE` · `TYPE_RATIO`

---

## B · 本轮团队默认（29）——先按这个算

这些不是「没定义」，是 D1 还 `draft`/`missing`（未会签 / 甲方 🟡）。**本轮锁定如下，不再空着等。** 和甲方纪要冲突再改。

| ID | 中文 | 本轮默认 |
|---|---|---|
| `M_ENT_HIGH_TECH_COUNT` | 高企数量 | `tag_code='high_tech'`；只国内；码在就算；中文 org_tag 项目映射，不算无法执行；D1 已 aligned（2026-09-04） |
| `M_ENT_TYPE_COUNT` | 各类型企业数 | 六码：`foreign/high_tech/sme/listed/little_giant/little_giant_pro`；一企可多类，禁止六类 SUM 当总数 |
| `M_ENT_TYPE_MATCH_COUNT` | 匹配企业总数 | 产业 ∩ 六码；未选不计算；多选并集再交；中文映射不算无法执行；D1 已 aligned（2026-09-04） |
| `M_ENT_TYPE_DIST_TOPIC` | 重点类型分布 | 对象=`KEY_TOTAL` 名单；只四码 `foreign/high_tech/sme/listed`；不并专精特新/小巨人 |
| `M_ENT_KEY_TOTAL` | 重点企业总数 | 国内专利总量（跟 `PATENT_TOTAL`）≥ **50**；选产业是 API；标签/技术交易额不进 |
| `M_ENT_KEYPANO_*`（7） | 重点概览 | 二次 STAT，对象=`KEY_TOTAL` ∩ 上链；选链/区/类型是 API；区域键=全国+省+市+县+gba/yrd/jjj；热门城市并入市 |
| `M_ENT_DOMAIN_COVERAGE_BREADTH` | 覆盖广度 | `DOMAIN_COVERAGE_COUNT / 15`（15=激活集群） |
| `M_ENT_DOMAIN_DIST_TOPIC` | 领域分布 | 年×`cluster_id` 去重家数；上链 L0→`industry_cluster_map` |
| `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT` | 覆盖未来产业数 | 只数 `CL-FUT-01`～`05`，0～5 |
| `M_ENT_REGIONAL_COUNT` | 区域企业数 | 国内 `COUNT DISTINCT` 主档；区划键 2/4/6 位 |
| `M_ENT_REGIONAL_COUNT_TOPIC` | 区域数量占比 | 家数/当期集合；规模=数量，不算营收 |
| `M_ENT_SZ_LIST_TOPIC` | 深圳清单+角色 | 深圳=`region_id LIKE '4403%'`；角色=`node_stage` |
| `M_ENT_BASE_97_4` | 重点资讯月统计 | `COUNT(*) FROM enterprise_news` 按年-月；不按企、不挂 `KEY_TOTAL` |
| `M_ENT_RESEARCHER_COUNT` | 全球科研人数 | 最新年国内 `development_employee` ∪ 国外 `rd_staff` 再 SUM |
| `M_ENT_STAR_ENTERPRISE_COUNT` | 明星企业数 | CMS 已发布名单 `COUNT DISTINCT`；禁止专利≥50 / `tag_code=star` / TopN |
| `M_ENT_SUPPLIER_COUNT` | 供应商数量 | 1-hop `relation_type='supplier'` 去重；不筛层级 |
| `M_ENT_RD_INVESTMENT_RATIO` | 研发投入占比 | 按企 `rd/revenue*100`，最近完整年；除零该企空 |
| `M_ENT_TECH_RANK` | 技术力排名 | 可比集内 `RANK` 技术力分；无分不进榜；同分并列 |
| `M_ENT_COMPETITIVENESS_RANK` | 竞争力排名 | 同上，键=竞争力分 |
| `M_SYNTH_VIT_RANK` / `ELEM_RANK` | 活力/要素排名 | 可比集 `RANK` 对应 INDEX；无指数不进榜。**指数公式本身不在本 55 条** |
| `M_ENT_RECOMMEND_COUNT` | 推荐企业数 | 二次 COUNT，挂 `ATTRACTION_INDEX`+`CULTIVATION_INDEX`，不挂 SCORE |
| `M_ENT_CITY_AVG_TECH_POWER` | 城市平均技术力 | 上游出分后 `AVG` 按 `LEFT(region_id,4)` |

`M_ENT_KEYPANO_*` 七条：`MATCH_COUNT` / `TYPE_COUNT` / `REGIONAL_COUNT` / `QUAL_DISTRIBUTION` / `TYPE_STRUCTURE` / `REGIONAL_DISTRIBUTION` / `ENTERPRISE_LIST`。

---

## C · 请算法同事先定（12）——直接转发本文件

没有唯一可执行口径，或和已登记 Q 打架。请算法（完整度一并问唐绍祖）给**一条可执行默认**，我们再写 seed。  
每条回：判定规则 / 公式 / 分母 / 禁止项。临时默认可以，标未甲方签。**不要等数据**；不要改上面 A/B。`RECOMMEND_COUNT` 阈值本波不拍。

下面按**问题类型**排，12 条都在这一个节里。

### 权重（2）

`VIT_RANK` / `ELEM_RANK` 公式已有，等 INDEX 出数，不占本问。

| ID | 现稿 | 请定 |
|---|---|---|
| `M_SYNTH_VIT_WEIGHT` | 科技/产业/人才/政策口头各 25%。Q-SYNTH-V-01 | 四维各几成、合计、能否展示 |
| `M_SYNTH_ELEM_WEIGHT` | 类型/层次/领域口头等权。Q-SYNTH-E-01 | 三维各几成、合计 |

请填：VIT 科技= 产业= 人才= 政策= ；ELEM 类型= 层次= 领域= ；展示=是/否

### 协同（2）

源表未建是数据问题，先写规则。Q-SYNTH-C-01。

| ID | 请定 |
|---|---|
| `M_SYNTH_COLLAB_COMPLETENESS` | 主体全集（企/院/人）？有效合作边？分母是否含无关系主体？ |
| `M_SYNTH_COLLAB_RELATION_INPUT` | 联合专利 / 合作项目 / 人才流动：匹配键、去重、有效性门槛 |

请填：全集= ；有效边= ；分母含无边主体=含/不含 ；专利/项目/人才各写匹配+去重+门槛

### 密度分母（2）

分子已钉（家数跟 `REGIONAL_COUNT`）。只问分母。Q012 / Q016。

| ID | 现稿 | 请定 |
|---|---|---|
| `M_ENT_CITY_DENSITY` | 市层家数 / `code_region.area`；全国行不算 | 面积还是建成区/人口/GDP |
| `M_ENT_REGIONAL_DENSITY` | 同区划键 / area；国外不算 | 两条是否同一套；area≤0 该区空？ |

请填：分母=面积/建成区/人口/GDP ；全国行=不算/算 ；空或≤0=该区空 ；两条同一套=是/否

### 产业链完整度（1）

`M_ENT_CHAIN_COMPLETENESS` · QC01 · 请唐绍祖看。现稿 `k/K×100`，K=INB 叶子（声称 954），默认全目录、不加权、祖先不上卷。

请填：K=INB 叶子 是/否 ；默认=全目录/选链 ；权重=无/有 ；祖先不上卷=确认

### 创新型企业（1）

`M_ENT_INNOVATIVE_COUNT` · Q011。官方认定，还是专精特新∪小巨人∪单项冠军∪创新型中小企业？**必须给 `tag_code`**，禁止再 `tag_name` 模糊含。

请填：选项=官方认定/四类并集 ；码= ；曾获过期=算/不算

### 核心供应商（1）

`M_ENT_CORE_SUPPLIER_COUNT`。现稿 `supplier` 且 `risk_level=高`，偏离 Q017 已闭合的投资 TOP5。禁止读 `is_core_supplier`。

请填：选项=risk 高 / 投资 TOPN（N= ）

### 短板条数（1）

`M_ENT_SHORTBOARD_COUNT` · Q014。相对同业更差的 L3 个数（资产负债率反向）。空值不判。MODEL 未出分是数据，**分组是定义**。

请填：同业=同链/国标行业/同规模 ；空值=不判 ；L3 跟 SCORE=是/另附

### 招引 / 培育 demo 分（2）

`M_ENT_ATTRACT_SCORE`、`M_ENT_CULTIVATE_SCORE` 与 INDEX **并行**。Q018 已禁痛点转分。

请填：本波=废弃 SCORE 只留 INDEX / 都留 ；ATTRACT 公式+区域/风险挂谁= ；CULTIVATE 恢复项用什么（或两项平均）=  

---

## 不请算法定（避免误派）

- 明星企业：已钉 CMS 已发布名单；缺的是 CMS 表，不是公式。  
- 高企是否含过期认定：灌数规则，Q010/Q011 旁路，不挡 `tag_code='high_tech'`。  
- 无目标 ADS 表：实现/落表，不是口径。  
- `KEY_TOTAL` N=50：团队临时已钉；升 🟢 是甲方 Q038，不是算法另开公式。

---

维护：`human:徐滕强` 监管。C 桶回填后走 COVER-STAT 一条一过写 seed，禁止整批改 YAML。

---

## B 剩余 27 条（2026-09-04 下午）

HIGH_TECH / TYPE_MATCH 已定。其余只核计算口径。

**可直接定（21）**：2026-09-04 已升 D1=`aligned`（只改矩阵 D1，D3/D4 未动）。`RECOMMEND_COUNT` 阈值未拍，D1 不动。

**要讨论（6）** 2026-09-04 已拍：`REGIONAL_COUNT` 省市县都出、国外按国家合并；RANK 未选产业=全国有分进榜（查询窗口）；`RECOMMEND_COUNT` **阈值暂不拍**；`VIT/ELEM_RANK` 默认北上广深杭南武重宁+成都合肥（宁=宁波，可追加）。
