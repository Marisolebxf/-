# CHAIN-ALGO-STAT-39-L01 · 口径分析规则与记录

> 任务：`CHAIN-ALGO-STAT-39-L01`（definition，只分析不实现）  
> 监管：`human:李伟`  
> parent：`CHAIN-HZW-THREE-TRACK-L01`  
> 实现另叶：`CHAIN-ALGO-STAT-39-IMPL-L01`（本叶 done + 李伟确认后才可开工）  
> 规则重立：2026-08-26（清空此前全部分析草稿）

---

## 1. 本叶做什么

只做人核：**这条指标口径是什么、能不能当 STAT/COMPUTE 落地、数从哪来、缺什么。**  
不写 `demo-algo-science` / Java / 前端。不刷读路径。不把草稿当已确认。

唐绍祖 MODEL/GRAPH 不在本叶。实现等分析齐并确认后走 IMPL 叶，且只动 demo，不写 lumen。

---

## 2. 逐条规则（必须按此顺序，缺一步不准下结论）

对清单里的 **一个** `metric_id`：

1. **读进度表整行**
  文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
   动作：按指标ID精确匹配，把该行 **全部列** 原样记入记录（空值写「（空）」）。  
   禁止只摘口径摘要。
2. **读需求来源整行**
  文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
   动作：  
  - 「指标目录」该 ID **全部列**；  
  - 「需求来源明细」该 ID **每一行全部列**（多条来源就多行）。  
   禁止只写「05 seq xx」一句话代替整行。
3. **两表对齐后再分析**
  必须对照：口径摘要、缺口说明、算法类型、合同/差集、决策清单、开放项、定义/结构/源/接入、综合就绪、卡点、需规分册/序号/页面/文件。  
   两表打架要写明打在哪一列，以哪份为准须李伟拍，AI 不得私自抹平。
4. **再读行内指向的需规文件**（明细「需规文件」列），只用来解释本 ID，不把整包需规都算进这一条。
5. **再核 ODS → DWD → ADS**（行数报告 / 项目表是否存在）。未核验不得写成 none 或已齐。
6. **demo 只读对照**，证明「现在代码在干什么」，不能当口径真源，也不能当已经实现。
7. **批量分析、统一拍板**（2026-08-26 `human:李伟`）。按 A→B→C→D→E 顺序完成全部 39 条分析，不再逐条等待回复；全部跑完后由李伟逐条核对并拍「确认 / 挂起」。
  已挂起的 A1/A2 保留原状态；其余先标「待确认」。  
   **2026-08-27** `human:李伟`：A1–A3、A7–A14、B15–B21、**B23** 已确认；**A4、A5、A6 挂起**（资讯源）；**B22 挂起**（政策相关先挂起）。  
   **2026-08-28 晚** `human:李伟`：**DWD/ADS 纠错，错误全改状态**。禁读 ODS。改挂起：A3、A7、A12、B20、B23（无机构/国家/论文 DWD）。路径改写仍确认：A1–A2、A8–A11（A8/A9 **仅企业**）、A13、B15–B19、B21、C32、E38、E39。  
   禁止跳号、禁止把关联指标提前混入当前条；批量执行不等于合并指标。
8. **MCP / seed** 只允许作补充。与 xlsx 冲突时 **xlsx 优先**，并在记录里写冲突。
9. **废表名不算源缺失**（2026-08-26 `human:李伟`）：口径/seed 里出现的表若现行库已不建，**禁止**写进「缺口/缺失」。只写 **已替换为现行表 X**，或 **从口径去除**。真缺失只登记：现网有效行不够、缺字段、无 Mapping 作业、决策未拍。
10. **同类问题跟 A1**（2026-08-26 `human:李伟`）：废表名只替换；增量 = `entity_rel`（`entity_id=org_id`）JOIN `enterprise_base.registration_date` + 环比；去重不用企业名。后续同类不重问。
  **指标分析禁止读 ODS**（2026-08-28 `human:李伟`）：只认项目 DWD + ADS。纠错见 **§7**。  
    **DWD 纠错改状态**（2026-08-28 晚 `human:李伟`）：无机构主表 → **A3/A12/B23 挂起**；国内企业无 country → **A7 挂起**；无论文 DWD → **B20 挂起**。A8/A9 对象改为 **仅企业**（机构随 A3 挂起剔除）。
  **A1/A2 卡片分工**（2026-08-27 `human:李伟`）：同一 JOIN；A1 = 各年**期末存量** `COUNT(成立年 ≤ Y)`；A2 = **当年新增** `COUNT(成立年 = Y)`。不再把两卡都做成当年新增。  
    **A3 机构**（2026-08-27 `human:李伟`）：集合选 **乙**（机构要素库另挂链，不从企业 tags 筛 `org_type`）；本卡交 **当年成立**（需规 95（3）字面，机构版 A2）。**不另做**机构期末存量卡，也不新建 `INSTITUTION_NEW_COUNT`。后续深圳机构等跟本条，不重问甲/乙、存量/新增。  
    **资讯源 CHAIN-NEWS-SRC-01**（2026-08-27 `human:李伟`）：`dwd_industry_chain_news_info` 只是**合规交付表、无利用价值**，不当产业链资讯 ODS 真源。  
    **2026-09-01** `human:淮政玮`**（李伟转述）**：产业链「要素库维护」六表 **可用作产业链资讯**。A4 真源 = `industry_analysis_`*（入站 `dwd_industry_analysis_*`）。**不要**灌 `industry_chain_news_event`（双真源）。`enterprise_news` 仍是企业维，不当 A4。A5/A6 继续挂起。挂链 `industry_code`→INB 未齐则 OPEN，禁止编 INB。  
    **A7 全球分布**（2026-08-27 `human:李伟`）：跟需规 95（5）= **每个国家**的企业+机构**主体数**（不是 `COUNT DISTINCT` 国家个数）。对象 = 链上企业（拼企业库国家）+ A3 乙机构（拼机构库国家）。覆盖国家个数可派生，不另建卡。后续全国/深圳分布默认同结构（按地理切片数主体，不去重区域个数），只换地理粒度。  
    **A8 全国分布**（2026-08-27 `human:李伟`）：跟需规 95（6）切到 **省**（不切市）。对象同 A7。xlsx/YAML 的 DISTINCT 省/市作废。  
    **A9 深圳分布**（2026-08-27 `human:李伟`）：跟需规 95（9）按**区**切片数企业+乙机构。深圳圈定 = 地理字段 `city=深圳市`（不是 4403，也不是「深圳」无「市」）。后续深圳条默认跟本条。xlsx DISTINCT 区/县个数作废。  
    **A10 深圳企业数**（2026-08-27 `human:李伟`）：**当前一个数**（甲）= `city=深圳市` 的链上企业去重，无年轴。不是 A1 按年切片，对象只有企业。  
    **A11 深圳企业占比**（2026-08-27 `human:李伟`）：`A10 / 当前链上企业去重 × 100`（甲）。分母**不是** A1 按年期末存量。YAML 公式改掉对 A1 的直接相除。  
    **A12 深圳机构数**（2026-08-27 `human:李伟`）：**A3 乙** + **A10 甲**（当前一个数、无年轴）+ `city=深圳市`。不用 `org_type=机构`、不用企业名去重。  
    **A13 产业链总数**（2026-08-27 `human:李伟`）：**全库** `COUNT(DISTINCT chain_id)`（最新批次快照）。05·117 只作需规挂靠，**不是**全景模型本体；MODEL/GRAPH 归唐绍祖，不塞进本 ID。  
    **A14 基础指标模型封面**（2026-08-27 `human:李伟`）：`M_CHAIN_BASE_95_1` = 05·95 九维**文件夹/封面**，不是可算 KPI。seed 留作需求追溯；**从 IMPL 清单剔除、不进 ADS**。后续遇到 `M_*_BASE_*_1` 这类叶子同名占位，默认同样处理，不重问。  
    **B15 市场规模**（2026-08-27 `human:李伟`）：跟 **QC06**。链上企业年报营收加总（只企业）。不是外购市调、不是 ODS 直灌。年报字段/境外营收/统计年跟 ENT Lead，不挡口径。后续增长率默认跟本条分子。  
    **B16 市场增长率**（2026-08-27 `human:李伟`）：**同比** `(B15当年 − B15上年) / B15上年 × 100`。需规 95（1）「环比」作废。缺上年则空，不伪造。  
    **B17 投融资事件数**（2026-08-27 `human:李伟`）：跟 **DWD Step2 §4.6**。源 = `dwd_org_financing_info`（× 挂接），COUNT 链上融资事件。不用资讯表。QC07/Q054 旧叙事不挡口径。后续区域融资条默认跟本条源。  
    **B18 区域融资事件**（2026-08-27 `human:李伟`）：**最优解**。保留 QC11 商业力预设叶子（不倒灌招标）。= **B17 × 评价** `region_codes` **切片 COUNT**。不是 126 模型，不是金额。后续区域指数叶子默认「链级已拍 STAT × 评价区域」，不重问身份。  
    **B19 区域营收**（2026-08-27 `human:李伟`）：**最优解**。= **B15 × 评价** `region_codes` **切片**。门户 MARKET_SIZE 不得直接顶替。  
    **B20 高校论文**（2026-08-27 `human:李伟`）：**甲**。论文要素库 × A3 乙**高校** × 高校所在地 ∈ 评价区域，COUNT 篇。不上主题 NLP。后续成果类叶子默认「要素库 × 已拍主体挂接」，不重问主题挂链。  
    **B21 区域专利**（2026-08-27 `human:李伟`）：**甲**。`dwd_patent` × 链上企业（申请人/受让人）× 评价区域，COUNT。E38 到号再对齐，本条不替 E38 拍板。  
    **政策相关先挂起**（2026-08-28 `human:李伟`）：本 39 条里政策专卡 = **B22** `M_CHAIN_REG_POLICY_COVERAGE`。公式、政策-链挂接、政策要素库活数 **源洗通后再拍**。后续再碰到政策专名叶子默认挂起，不重问。瓶颈五维里的「政策」类型仍走 QC04，不在此次挂起范围。  
    **B23 科研机构**（2026-08-28 `human:李伟`）：**甲**。A3 乙里科研院所+高校，**当前 COUNT**（不是当年成立）× 评价区域。密度不单做。全景机构数不得直接顶替。  
    **B24 服务机构**（2026-08-28 `human:李伟`）：**挂起**。服务类码表 / 是否走机构库类型筛 **源与类型口径洗通后再拍**。后续再碰到服务机构专名叶子默认挂起，不重问。不把 `M_SVC_`* 搬进本卡。  
    **B25 人才结构**（2026-08-28 `human:李伟`）：**挂起**。本 39 条里人才专卡 = **B25** `M_CHAIN_REG_TALENT_STRUCTURE`。结构维、人才-链挂接 **源洗通后再拍**。后续再碰到人才专名叶子默认挂起，不重问。瓶颈五维里的「人才」类型仍走 QC04，不在此次挂起范围。  
    **C26 瓶颈堵点数**（2026-08-28 `human:李伟`）：口径 **甲**（已打标节点 COUNT；识别归 125）。同日晚改 **挂起**：现无标签不可算，等 125 落标后再排 IMPL。  
    **C27 瓶颈严重度**（2026-08-28 `human:李伟`）：**挂起**。0–100 / MAX 分值、打分模型 **125 落分后再拍**。  
    **需模型、现不可做先挂起**（2026-08-28 `human:李伟`）：依赖 125/124/121/129/127 等 MODEL 打标或打分、当前交不出数的 STAT，一律挂起，不重问「等模型再 STAT」。本批另挂：**C28** 类型分布、**C29** 卡脖子、**C30** 高价值占比、**C31** 重点布局推荐、**C33** 深圳优势排名、**C34** 关键环节覆盖率、**C35** 深圳产业问题数。不覆盖：D36/D37 COMPUTE 公式叶；E38/E39 专利/产品挂接 COUNT。  
    **C32 深圳产业链完整度**（2026-08-28 `human:李伟`）：**甲**。按**节点覆盖**：深圳有主体挂上的环节数 / 全链环节数 × 100。深圳圈定跟 A9（`city=深圳市`）。不按产值、不另做企业覆盖卡。QC01 甲方若改口径再覆盖。不升 118 模型。  
    **D36 产业集中度**（2026-08-28 `human:李伟`）：**挂起**。HHI / CR_N / N 值 **QC02 锁口径后再拍**。124 模型不进本卡。后续再碰到集中度指数叶子默认挂起，不重问。  
    **D37 国际化程度**（2026-08-28 `human:李伟`）：**挂起**。三维权重 / 贸易源 **口径锁后再拍**。不把 05·95 正文没有的公式塞进本卡。后续再碰到国际化指数叶子默认挂起，不重问。  
    **E38 产业链关联专利数**（2026-08-28 `human:李伟`）：**甲**。跟 B21：`dwd_patent` × 链上企业（申请人/受让人信用代码），全链 COUNT DISTINCT，无评价区域。不上主题/IPC 挂链。废名 `industry_chain_patent` 只替换、不建四表。  
    **E39 产业链关联产品数**（2026-08-28 `human:李伟`）：**乙**。现行表 **无** `product_id`。源 = `dwd_org_industry_product_tags`，去重 = 规范化后的 `product_name` **COUNT DISTINCT**。须写明：同名碰撞、不能识别跨企业同一产品。禁止用 Demo 合成键 `p:{credit}:{行id}` 当产品主键。产品 UID 冻结后可改键，不挡本条确认。

---



## 3. 每条记录必须具备的块

```
### 序号 · metric_id · 指标名称（待确认 | 已确认 | 挂起）

**指标描述**：进度表口径摘要（xlsx 原文；已确认口径以条内「口径一句」为准）

1) 进度表：文件 + excel 行号 + 全列
2) 需求来源·目录：excel 行号 + 全列
3) 需求来源·明细：每条 excel 行号 + 全列
4) 结合分析（基于上面三块，不是另起一套口径）
   - 口径一句
   - ODS / DWD / ADS
   - **算法是否满足**（单独写：类型够不够、现有算法能不能交这个数）
   - **算法缺口**（单独写：缺的是算法还是数据/口径；禁止把废表名当算法缺口）
   - 可实现（是 / 否 / 条件是）
   - 缺口（数据/映射/决策，不含废表名）
   - 需要李伟确认的问题
```

---



## 4. 分析顺序

默认按下面 39 条顺序。李伟指定分组时，从该组第一条未挂起/未确认的 ID 开始（例如「做基础 A」= 从 `M_CHAIN_ENTERPRISE_COUNT` 起，不先做瓶颈）。

**A 基础计数 / 分布**

1. `M_CHAIN_ENTERPRISE_COUNT` 产业链关联企业数
2. `M_CHAIN_ENTERPRISE_NEW_COUNT` 新增关联企业数
3. `M_CHAIN_INSTITUTION_COUNT` 产业链关联机构数
4. `M_CHAIN_NEWS_COUNT` 动态资讯数
5. `M_CHAIN_HOT_NEWS_COUNT` 热门资讯数
6. `M_CHAIN_NEWS_SENTIMENT_RATIO` 资讯正面情感占比
7. `M_CHAIN_GLOBAL_REGION_COUNT` 全球分布区域数
8. `M_CHAIN_NATIONAL_REGION_COUNT` 全国分布区域数
9. `M_CHAIN_SZ_REGION_COUNT` 深圳产业分布区域数
10. `M_CHAIN_SZ_ENTERPRISE_COUNT` 深圳产业链企业数
11. `M_CHAIN_SZ_ENTERPRISE_RATIO` 深圳产业链企业占比
12. `M_CHAIN_SZ_INSTITUTION_COUNT` 深圳产业链机构数
13. `M_CHAIN_TOTAL_COUNT` 产业链总数
14. `M_CHAIN_BASE_95_1` 产业链基础指标模型构建

**B 市场 / 投融资 / 区域 STAT**

1. `M_CHAIN_MARKET_SIZE` 市场规模
2. `M_CHAIN_MARKET_GROWTH` 市场增长率
3. `M_CHAIN_INVEST_COUNT` 投融资事件数
4. `M_CHAIN_REG_FINANCING` 融资事件
5. `M_CHAIN_REG_REVENUE` 营收
6. `M_CHAIN_REG_PAPERS` 高校论文
7. `M_CHAIN_REG_PATENT` 专利
8. `M_CHAIN_REG_POLICY_COVERAGE` 政策覆盖率
9. `M_CHAIN_REG_RESEARCH_ORG` 科研机构
10. `M_CHAIN_REG_SERVICE_ORG` 服务机构
11. `M_CHAIN_REG_TALENT_STRUCTURE` 人才结构

**C 瓶颈 / 关键 / 深圳统计**

1. `M_CHAIN_BOTTLENECK_COUNT` 瓶颈堵点数
2. `M_CHAIN_BOTTLENECK_SEVERITY` 瓶颈严重度
3. `M_CHAIN_BOTTLENECK_TYPE_DIST` 瓶颈类型分布
4. `M_CHAIN_CHOKE_LINK_COUNT` 卡脖子环节数
5. `M_CHAIN_HIGH_VALUE_RATIO` 高价值环节占比
6. `M_CHAIN_LAYOUT_RECOMMEND_COUNT` 重点布局推荐数
7. `M_CHAIN_SZ_COMPLETENESS` 深圳产业链完整度
8. `M_CHAIN_SZ_ADVANTAGE_RANK` 深圳优势排名
9. `M_CHAIN_SZ_KEY_NODE_COVERAGE` **深圳关键环节覆盖率
10. `M_CHAIN_SZ_PROBLEM_COUNT` 深圳产业问题数

**D COMPUTE**

1. `M_CHAIN_CONCENTRATION_INDEX` 产业集中度
2. `M_CHAIN_INTERNATIONALIZATION_INDEX` 产业链国际化程度

**E 缺口 STAT**

1. `M_CHAIN_PATENT_COUNT` 产业链关联专利数
2. `M_CHAIN_PRODUCT_COUNT` 产业链关联产品数



### 4.1 第一波（产业链底层 + 企业相关）

只认项目 DWD：链 `industry_chain_*` + 企业 `enterprise_*`。不读 ODS。机构 / 国家 / 论文 / 模型 / 资讯专卡不进本波。

**公共 JOIN**：`industry_chain_entity_rel`（`entity_type=enterprise`，`entity_id=org_id`）→ `enterprise_base`。深圳圈定 `city=深圳市`。去重 `org_id`。

**进 IMPL（16 条）**


| 序号  | metric_id                       | 名称     | 口径                                      | DWD                                                |
| --- | ------------------------------- | ------ | --------------------------------------- | -------------------------------------------------- |
| A1  | `M_CHAIN_ENTERPRISE_COUNT`      | 关联企业数  | 期末存量 `YEAR(registration_date)≤Y` + 存量环比 | `entity_rel` × `enterprise_base.registration_date` |
| A2  | `M_CHAIN_ENTERPRISE_NEW_COUNT`  | 新增关联企业 | 当年新增 `=Y` + 新增环比                        | 同 A1                                               |
| A8  | `M_CHAIN_NATIONAL_REGION_COUNT` | 全国分布   | 按**省**切企业数（仅企业，不含机构）                    | `enterprise_base.province`                         |
| A9  | `M_CHAIN_SZ_REGION_COUNT`       | 深圳分布   | `city=深圳市` 再按**区**切企业数                  | `enterprise_base.district`                         |
| A10 | `M_CHAIN_SZ_ENTERPRISE_COUNT`   | 深圳企业数  | 当前一个数，仅企业                               | `city=深圳市`                                         |
| A11 | `M_CHAIN_SZ_ENTERPRISE_RATIO`   | 深圳企业占比 | A10 / 当前链上企业                            | 同 A10                                              |
| A13 | `M_CHAIN_TOTAL_COUNT`           | 产业链总数  | `COUNT(DISTINCT chain_id)`              | `industry_chain`（注意 `chain_tier`）                  |
| B15 | `M_CHAIN_MARKET_SIZE`           | 市场规模   | 链上企业年报营收 SUM                            | `enterprise_finance_history.revenue`               |
| B16 | `M_CHAIN_MARKET_GROWTH`         | 市场增长率  | B15 同比；缺上年则空                            | 派生 B15                                             |
| B17 | `M_CHAIN_INVEST_COUNT`          | 投融资事件数 | 链上企业融资事件 COUNT                          | `enterprise_financing` × 挂接                        |
| B18 | `M_CHAIN_REG_FINANCING`         | 区域融资   | B17 × 评价区域                              | 企业 `city`/`province`                               |
| B19 | `M_CHAIN_REG_REVENUE`           | 区域营收   | B15 × 评价区域                              | 同 B15 地理                                           |
| B21 | `M_CHAIN_REG_PATENT`            | 区域专利   | 链上企业专利 COUNT                            | `enterprise_patent_detail.patent_id` × 区域          |
| C32 | `M_CHAIN_SZ_COMPLETENESS`       | 深圳完整度  | 深圳有企业挂上的节点 / 全链节点                       | `industry_chain_node` + `entity_rel` + `city`      |
| E38 | `M_CHAIN_PATENT_COUNT`          | 关联专利数  | 同 B21，全链无区域                             | 同 B21                                              |
| E39 | `M_CHAIN_PRODUCT_COUNT`         | 关联产品数  | 规范化 `product_name` 去重                   | `enterprise_industry_product`（无 `product_id`）      |


**本波不排**


| 序号              | 原因                             |
| --------------- | ------------------------------ |
| A14             | 封面，不进 ADS                      |
| A3 / A12 / B23  | 无机构主数据 DWD                     |
| A7              | 国内 `enterprise_base` 无 country |
| A4–A6           | 资讯源挂起                          |
| B20             | 无论文 DWD                        |
| B22 / B24 / B25 | 政策 / 服务 / 人才                   |
| C26–C31、C33–C35 | 需模型                            |
| D36 / D37       | 指数公式未锁                         |


落 ADS：`industry_chain_metric_fact` / `series` / `dist` / `region_dist`（按形态）。实现另叶 `CHAIN-ALGO-STAT-39-IMPL-L01`。

### 4.2 资讯能不能洗（淮政玮 2026-08-25；**2026-09-01 源改乙**）

**已拍不用**：产业链要素库 `dwd_industry_chain_news_info`（合规交付、无利用价值）。禁止灌 `industry_chain_news_event`、禁止当 A4 源。

**2026-09-01** `human:淮政玮`**（李伟转述）**：算法台「要素库维护」对应的 **行业分析六表可用作产业链资讯**。A4 不再走甲 `enterprise_news`。设计表 `industry_chain_news_event` **本期闲置**，六表 **不要往里洗**。指标读 `industry_analysis_documents`（挂链用 `_industries`）。A5/A6 仍挂起。

**可用两路（要素库入站 → GDF → 项目 DWD 后再计；指标不扫 ODS）**


| 路         | 要素库（入站）                                                                                                         | 项目 DWD                                                                   | 怎么挂到链                                                                                                                      | 洗出来的语义                     |
| --------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 甲 机构/企业资讯 | 国内机构「重点资讯」`dwd_org_important_news_info`（`org_id` / `external_id` / `news_title` / `news_date` / `news_content`） | 现成：`enterprise_news`（`org_id` + 标题/日期/正文/链接，约 2 万行）                      | `enterprise_news.org_id` = `entity_rel.entity_id`（链上企业）                                                                    | **链上企业相关资讯**，不是「写产业链的行业新闻」 |
| 乙 行业分析    | 「行业分析要素库」六表                                                                                                     | `industry_analysis_documents` + `_companies` / `_industries` / `_topics` | 公司：`company_name_local` 对 `enterprise_base` 再挂链（`company_id` 不是 `org_id`）。行业：`industry_code`→INB **尚无对照表**。主题码不能当 chain_id | **研报/分析文档**，粒度不是动态资讯       |


**结论（2026-09-01 叠加 Mapping）**

- 废表 / `news_event`：不当 A4。
- **乙**（分析六表）：淮政玮曾放开作资讯真源；**李伟关闭 B2** 后项目 DWD **没有**这六张，A4 **不能**按乙解挂。
- **甲**（`enterprise_news` × 链上企业）：与第一波同构、企业包可洗；**未拍之前继续挂起**。
- A5/A6：无热度/情感字段，继续挂起。



### 4.3 算法台账「要素库维护」是什么（资讯相关）

位置：**GKX 系统和算法** → **产业链分析算法库** → `/chain/indana`「要素库维护（Mock）」。页面：`demo-ui-system-test` `IndanaCrudPage.vue`。

**它维护的是行业分析六表，不是产业链资讯四表。**


| 页面上的                                    | 项目 DWD                                                             | 对应淮政玮「可用」              |
| --------------------------------------- | ------------------------------------------------------------------ | ---------------------- |
| 主表 document_id / 标题 / 摘要 / 正文 / 来源 / 日期 | `industry_analysis_documents`                                      | 行业分析要素库 `documents`    |
| 页签：公司 / 行业 / 主题 / 类型 / 国家               | `_companies` `_industries` `_topics` `_content_types` `_countries` | 截图里的三张关联表 + 另两张        |
| 标签「只写 Demo DWD 六表 · 非三方入站」              | Demo 可 CRUD；live 面禁用新增编辑                                           | 正式入站仍走 GDF，本页是联调台 Mock |
| AI 填表（GLM）                              | 按主题生成研报草稿再保存                                                       | 不是机构重点资讯               |


**和资讯指标的关系**

- **不是** `dwd_industry_chain_news_info`，也 **不是** 机构「重点资讯」`dwd_org_important_news_info` / `enterprise_news`。
- 语义 = **研报/分析文档**（§4.2 乙）。动态资讯 A4 若解挂应走 **甲** `enterprise_news` × 链上企业，**不要**把本页六表 COUNT 当成 `M_CHAIN_NEWS_COUNT`。
- 本页 `industry_code` / `topic_code` **没有**接到 INB `chain_id`，保存后仍不能按产业链切 A4。
- A5 热门 / A6 情感：本页无热度、情感字段，洗不出来。

**台账里这页真正能做的**：给企业图谱/抽边准备行业分析正文（entan 文档详情也读这六表）；给以后「链相关研报数」打草稿。**不能**替代已废的链资讯表去交动态资讯三卡。

**2026-08-28** `human:李伟`**：A5/A6 继续挂起，只盯 A4。问：要素库维护能不能洗进 DWD 资讯表？**

**不能。** 本页保存只写 `industry_analysis_`* 六表，没有作业把它灌进 `enterprise_news`。


|       | 要素库维护写出                                          | A4 要用的资讯 DWD                                                             |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------ |
| 表     | `industry_analysis_documents`（+ 公司/行业子表）         | `enterprise_news`                                                        |
| 主键/挂接 | `document_id`；公司是 `company_name`，**不是** `org_id` | `org_id`（与 `enterprise_base` / `entity_rel` 同套）                          |
| 粒度    | 一篇研报                                             | 一条企业重点资讯                                                                 |
| 入站真源  | 行业分析要素库（乙）或本页 Mock/GLM                           | GDF：`dwd_org_important_news_info` → `enterprise_news`（甲，已有 Mapping §3.5） |
| live  | 写按钮禁用                                            | 只读消费                                                                     |


硬灌会缺 `org_id`、把研报当快讯、污染企业资讯。A4 解挂路径仍是 **甲**：现成 `enterprise_news` × 链上企业 COUNT；**不经过**本页。

### 4.4 指标前置 Mapping（2026-09-01）

STAT/IMPL **等 Mapping 洗进项目 DWD 后再做**。`human:李伟` 2026-09-01 确认先完成当前可做 Mapping；**已 push** `origin/dev` `59e4e42`（尚未建表或灌数）：

- 真源：`data-design/产业链/产业链域-ETL-Mapping明细-源表到DWD.md`
- 派单包：`data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v1/`

可独立执行：

- `CHAIN-B1-TREE`：链树 → `industry_chain` / `node` / `node_rel`；
- `CHAIN-B3-ENTITY-REL`：企业挂接 → `entity_rel`（`entity_id=org_id`），仅本作业依赖企业包 `enterprise_base`。

`CHAIN-B2-INDANA` **不执行**：行业分析六表不同构写入项目 DWD。`industry_chain_news_event` 继续闲置，禁止写入。

自动化校验：通用 `parse_workpack.py` 尚未识别 CHAIN 字段矩阵（Wave B=0）；GDF 按 09 人工配置。禁止把空 Wave B 当作 Mapping 已执行。

### 4.5 Mapping 落地后口径复核（2026-09-01 · 继续指标分析）

39 条分析记录已齐（确认或挂起）。本小节只对照 **CHAIN 09** + 企业包依赖，不重抄 xlsx。

**CHAIN 包实际洗进项目 DWD 的**：`industry_chain` / `node` / `node_rel` / `entity_rel`（企业 `org_id`）。  
**CHAIN 包明确不洗**：`industry_analysis_`*、`news_event`、产品 tags。  
**本包不洗、认企业包**：`enterprise_base` / 年报 / 融资 / 专利 / 产品。

#### 第一波 16 条（对照 09）


| 序号            | metric_id   | Mapping 后     | 依赖                                                                       |
| ------------- | ----------- | ------------- | ------------------------------------------------------------------------ |
| A1/A2         | 企业存量/新增     | **可 STAT**    | B3 `entity_rel` + 企业包 `enterprise_base.registration_date`                |
| A8/A9/A10/A11 | 省/区/深圳企业/占比 | **可 STAT**    | 同上 + `province`/`city`/`district`                                        |
| A13           | 链总数         | **可 STAT**    | 仅 B1 `industry_chain`                                                    |
| B15/B16       | 市场规模/同比     | **可 STAT**    | B3 + 企业包年报 `enterprise_finance_history`                                  |
| B17/B18       | 投融资/区域融资    | **可 STAT**    | B3 + 企业包 `enterprise_financing`                                          |
| B19           | 区域营收        | **可 STAT**    | 同 B15 × 区域                                                               |
| B21/E38       | 区域/全链专利     | **可 STAT**    | B3 + 企业包 `enterprise_patent_detail`                                      |
| C32           | 深圳完整度       | **可 STAT**    | B1 节点 + B3 + `city=深圳市`                                                  |
| E39           | 产品数         | **可 STAT（乙）** | 企业包 `enterprise_industry_product.product_name`；CHAIN 产品 tags **不洗**、不当主键 |


IMPL 闸门：GDF **B1 完成** 才能算 A13；**B3 +** `enterprise_base` 才能算其余 15 条。年报/融资/专利/产品缺行是企业包债，不是 CHAIN 09 缺字段。

#### 资讯 A4/A5/A6（仍挂起）


| 路                          | 09 之后                     | A4                 |
| -------------------------- | ------------------------- | ------------------ |
| 废链资讯四表 / `news_event`      | 禁止洗                       | 不可                 |
| 乙 行业分析六表                   | **B2 不写项目 DWD**           | 项目侧无表可读；**本期不可解挂** |
| 甲 `enterprise_news` × 链上企业 | 不在 CHAIN 09；企业包已有 Mapping | 李伟未拍进 A4；**继续挂起**  |


A5/A6：六表与企业资讯均无热度/情感字段，继续挂起。

#### 仍挂起、本轮 Mapping 不解

A3/A7/A12/B20/B23（机构/国家/论文）；B22/B24/B25；C26–C31、C33–C35；D36/D37。无新源，不重开分析。

#### 需要李伟拍（解下一刀）

1. 第一波 16 条：是否 **等 GDF B1/B3 抽样回签后再派 IMPL**（推荐），还是先写 Demo 模拟 SQL。
2. A4：继续挂起，或改走 **甲** `enterprise_news` × `entity_rel`（乙六表本期不算源）。

### 4.6 资讯三卡整理（2026-09-07）

只整理 **A4/A5/A6**。不扫 ODS。不把 Demo `news_event` 当可算源。不把「要素库维护」六表 COUNT 当成动态资讯。

**三张卡**

| 序号 | metric_id | 名称 | 状态 | 本卡交什么 |
|------|-----------|------|------|------------|
| A4 | `M_CHAIN_NEWS_COUNT` | 动态资讯数 | 挂起 | 链相关资讯去重 COUNT（需规 95（7）的「最新资讯」计数） |
| A5 | `M_CHAIN_HOT_NEWS_COUNT` | 热门资讯数 | 挂起 | A4 集合上的热点子集 COUNT（95（7）浏览量/评论阈值；seed 写成 `heat_score≥80`，两套未拍） |
| A6 | `M_CHAIN_NEWS_SENTIMENT_RATIO` | 资讯正面情感占比 | 挂起 | A4 集合上正面条数 / 总条数 × 100（需规 95（7）**无**情感专核；要 NLP 分类叶） |

**禁止当源（已拍）**

- `dwd_industry_chain_news_info`（合规交付、无利用价值）
- 项目表 `industry_chain_news_event`（闲置，禁止灌）
- xlsx/seed 废名 `industry_chain_news` / `news_id`（只替换，不当真源）

**两条候选路（只能选一条当 A4 真源）**

| | 甲 | 乙 |
|---|---|---|
| 表 | 企业包 `enterprise_news`（`org_id`）× `entity_rel`（链上企业） | 行业分析六表 `industry_analysis_documents` + `_industries` 等 |
| 语义 | **链上企业相关资讯**（机构重点资讯），不是「写产业链的行业新闻」 | **研报/分析文档**，粒度不是快讯 |
| 项目 DWD | 有表、与第一波同构 | **B2 已关**，项目侧无这六张可读 |
| 挂链 | `org_id` = `entity_rel.entity_id` | `industry_code`→INB **无对照**；主题码不能当 `chain_id` |
| 热度/情感列 | 无 | 无 |

淮政玮 2026-09-01 曾放开乙作资讯真源；李伟关 B2 后 **乙本期不可解挂**。甲有表、未拍进 A4，故三卡仍挂。

**算法**

- A4：STAT 够，无模型。卡在「数什么、从哪张表挂到 INB」。
- A5：最后一公里是 STAT；热度输入没有。需规要浏览量/评论，seed 要 NLP 分。源未定前 **不拍阈值**。
- A6：占比是 STAT；分类是 NLP（可另叶，仍走 Python `/internal`）。源未定前 **不拍**「另叶 vs 本卡」。

**建议拍板（只动 A4；A5/A6 继续挂）**

1. A4 真源选 **甲**：`COUNT(DISTINCT 资讯业务键)`，`enterprise_news.org_id` ∈ 该链 `entity_rel`（`entity_type=enterprise`）。语义写明「链上企业资讯」，不要写成行业快讯全集。
2. 数窗口：跟 A1 同类，先交 **最新快照**；按发布时间切片后补，本条不挡确认。
3. 去重键：用 `enterprise_news` 现有业务键（标题+日期+org 或表内 id），**不用**废名 `news_id`。
4. A5/A6：**继续挂起**，直到甲表出现热度列/情感标签，或另开 NLP 叶。不要用六表、不要编 `heat_score`。
5. 乙六表：留给「链相关研报数」另卡（若以后要做），**不进** `M_CHAIN_NEWS_COUNT`。

拍完 A4=甲之后：口径确认可进分析叶；IMPL 跟第一波一样只读 Demo DWD，不扫 ODS。xlsx/seed 仍写废表名，交 data-agent 正式化，本叶不改 YAML。

---

---



## 5. 逐条分析记录



### A1 · `M_CHAIN_ENTERPRISE_COUNT` · 产业链关联企业数（已确认）

**指标描述**：纳入产业链要素库的关联企业去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_enterprise 全量，按 enterprise_code 去重。

> 2026-08-27 `human:李伟`：**确认（解挂）**。卡片交 **各年期末存量**（当年新增累加）：`COUNT(成立年 ≤ Y)` + 存量环比。当年新增留给 A2。  
> 2026-08-26 曾挂起（与 A2 分工未拍）；材料核对仍有效。  
> **问题 1 已拍**：不要锁成 xlsx「最新批次快照去重」（无年轴）；按年切。  
> **取数路径已拍**（2026-08-26 晚）：产业链挂接企业 → `credit_code` 匹配企业要素库成立日。企业库列：`dwd_org_base_info.incorporation_date`（信用代码现列名 `external_id`，Mapping 钉死）。不把产业链四表缺成立年写成算法缺口。

**问题 1 落盘（按年期末存量）**

- 目标：按年 **期末存量** STAT + 存量环比。年 Y = 链上企业中 `YEAR(incorporation_date) ≤ Y` 的去重家数。需规 95（2）「每年成立数量 + 环比」落在 **A2**；本 ID 名称是关联企业数，交累计盘子。
- 与现状：xlsx / seed / demo 仍是无年轴快照去重 → **文档与实现错位**，正式化时改口径，本叶不改 YAML。
- 取数：挂接表 `dwd_org_industry_tags`（链 + `credit_code`）JOIN 企业要素库成立日；DWD 现行边表仍是 `industry_chain_entity_rel`。

分析日：2026-08-26。MCP `metric-registry` 本会话未挂载；kit/readiness 用同仓 `scripts/lib/metric-registry-lib.mjs` 的 `getMetric`（与 MCP 同一读口，未整文件打开 YAML）。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **117**


| 列         | 值                                                                                         |
| --------- | ----------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_ENTERPRISE_COUNT                                                                  |
| 指标名       | 产业链关联企业数                                                                                  |
| 决策清单中的编号  | （空）                                                                                       |
| 域         | 产业链                                                                                       |
| 模块        | E2 产业链（待四维评估）                                                                             |
| 模块说明      | 产业链                                                                                       |
| 专题维度Owner | 李伟                                                                                        |
| 算法类型      | STAT                                                                                      |
| 合同集合      | F∩L                                                                                       |
| 差集判定      | mapped                                                                                    |
| 语义层开发阶段   | 未标                                                                                        |
| 验收单元      | —                                                                                         |
| 四维评估      | 待评估                                                                                       |
| 定义状态      | 已对齐                                                                                       |
| 开放项       | （空）                                                                                       |
| 结构支撑      | 待评估                                                                                       |
| 结构缺口      | （空）                                                                                       |
| 结构判定      | —                                                                                         |
| 源映射       | 齐备                                                                                        |
| 源缺口       | （空）                                                                                       |
| 接入状态      | Mock                                                                                      |
| 接入阶段      | （空）                                                                                       |
| 综合就绪      | 待接入（Mock）                                                                                 |
| 卡点责任方     | 李伟                                                                                        |
| 更新频率      | daily                                                                                     |
| 口径摘要      | 纳入产业链要素库的关联企业去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_enterprise 全量，按 enterprise_code 去重。 |
| 缺口说明      | （空）                                                                                       |
| 更新日期      | 2026-08-25                                                                                |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **35**


| 列        | 值                                                                                         |
| -------- | ----------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_ENTERPRISE_COUNT                                                                  |
| 指标名      | 产业链关联企业数                                                                                  |
| 决策清单中的编号 | （空）                                                                                       |
| 域        | 产业链                                                                                       |
| 模块       | CHAIN                                                                                     |
| 算法类型     | STAT                                                                                      |
| D1定义     | —                                                                                         |
| D4接入     | —                                                                                         |
| 需求来源条数   | 1                                                                                         |
| 需求回填     | 已回填                                                                                       |
| 来源系统     | 专题系统                                                                                      |
| 主来源分册    | 05 算法库需规                                                                                  |
| 主来源序号    | 95                                                                                        |
| 主来源名称    | 产业链基础指标模型构建                                                                               |
| 主来源简述    | 产业链 / 基础指标：产业链基础指标模型构建                                                                    |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                                        |
| 全部来源     | 05·95 产业链基础指标模型构建                                                                         |
| 口径摘要     | 纳入产业链要素库的关联企业去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_enterprise 全量，按 enterprise_code 去重。 |
| 更新日期     | 2026-08-25                                                                                |


Sheet：`汇总`：无本 ID。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **38**（仅 1 行）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_ENTERPRISE_COUNT                          |
| 指标名      | 产业链关联企业数                                          |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 产业链 / 基础指标：产业链基础指标模型构建                            |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-PANORAMA                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**两表对齐**

- 口径摘要、算法类型 STAT、F∩L/mapped、需规 05·95、页面全景：两表一致。
- 打架 1：进度表「定义状态=已对齐 / 源映射=齐备 / 接入=Mock」；需求来源「D1=— / D4=—」。以 xlsx 进度表列为人读，但 MCP/`getMetric` 返回 `found.matrix=false`（矩阵无本 ID），故需求来源 D1/D4 空更诚实。进度表「源映射=齐备」与矩阵缺失、库表旧名、现网 `is_deleted=0` 为 0 **打架**。
- 打架 2：xlsx 口径对象表 `dwd.industry_chain_enterprise` + 键 `enterprise_code`；seed kit `source_tables` 仍写 `ods: dwd_org_industry_chain_dtl` + `ads: chain_overview`。现网 `SHOW TABLES`：**两旧名都不存在**。
- 决策清单编号两表皆空。`客户决策清单跟踪表.md` **没有**单独挂本 ID；Q053 管编码（INB），不裁定本条「存量 vs 新成立」。

**需规（只解释本 ID）**

`基础指标.md` 序号 95 是九维能力包。（2）「产业企业规模」原文是：对接产业库，**计算每年该产业链的企业成立数量，并环比增长率**。  
xlsx/seed 口径是：**最新批次快照、要素库关联企业去重总数（存量）**。  
→ 需规字面 ≠ 进度表口径。年度新成立更靠近下一条 `M_CHAIN_ENTERPRISE_NEW_COUNT`（本条不展开）。

**MCP / seed 补充（xlsx 优先）**

- kit：STAT；definition/formula 与进度表口径摘要同文；`version=0.1.0`；`source_systems=Mock @ batch=mock_20260623`。
- readiness：矩阵缺失 → 不能把进度表 D3「齐备」当成矩阵真源。
- extras.mapping_status=`✅`（seed 侧），与现网有效行=0、无 CHAIN GDF 派单包冲突。

**ODS → DWD → ADS（已核）**


| 层                      | 结论                                                                                                                                                                   |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 约定 ODS                 | 产业链四表之一：`dwd_org_industry_tags`（产业关联企业信息），业务键 `credit_code`。**不是** kit 里的 `dwd_org_industry_chain_dtl`。                                                              |
| 三方 `gkx` 现网 2026-08-26 | `dwd_org_industry_tags`：`COUNT(*)=20000`，`is_deleted=0` → **0**（与行数报告「0（全表 20,000）」一致）。按供应方取数约定（默认 `is_deleted=0`）**当前算不出企业**。                                       |
| 产品表（非本指标 ODS）          | `dwd_org_industry_product_tags` 现网 `is_deleted=0` = 20000；不要拿来顶本指标。                                                                                                  |
| 项目 DWD v5              | 现行对象表 = `industry_chain_entity_rel`（`entity_type=enterprise`，`entity_id=credit_code`）。旧名 `industry_chain_enterprise` **已替换，不记缺失**。正式 GDF CHAIN Mapping 派单包仍无（只有企业域）。 |
| ADS v2                 | 应落 `industry_chain_metric_fact.metric_id=M_CHAIN_ENTERPRISE_COUNT`。Java 只读 ADS。                                                                                      |
| Demo 库                 | 2026-08-26 改读 `**111.198.38.90:34306**`（MySQL 8.0.46）。库：`demo_gkxlumenx_ods/dwd/ads`。`10.50.11.76` 本机超时，不以它为准。                                                     |


**demo 对照（非口径真源）· 该实例实测**

- ODS `dwd_org_industry_tags`：**0 行**（`dwd_org_industry_product_tags` 也是 0）。图谱 ODS `dwd_industry_chain_info`=1273。
- DWD 现行：`industry_chain_entity_rel` 254 行；`entity_type=enterprise` 且 `is_deleted=0` → **7 行 / 去重 entity_id=4**；`product` 247。`industry_chain` 未删=49。旧名 `industry_chain_enterprise` 不建、不记缺。
- ADS `industry_chain_metric_fact` 本 ID：49 行（按链切片）；最大 `INB1701`/`INB170101`=**4**（与 DWD 去重 4 一致），多数链为 0。
- 含义：demo 企业数 **不是**从 demo ODS tags 灌上来的（tags 空），是 DWD/ADS 上的少量样例；代码路径仍是 ADS fact，无行回落 DWD `COUNT(DISTINCT entity_id)`。
- 写：`ads_v2.py`；读：`read_v2.py` `enterprise_stats`。去重键 `entity_id`，不是 `enterprise_code`。

**口径一句（已确认）**

到年 Y 年底，该链上已成立的关联企业去重家数（成立年 ≤ Y）+ 相对上年的存量环比。  
xlsx 仍写无年轴快照——文档债，确认后交 data-agent，本叶不改 YAML。

**算法是否满足**


| 项            | 结论                                                                                 |
| ------------ | ---------------------------------------------------------------------------------- |
| 类型           | STAT + 环比足够，不必 MODEL。                                                              |
| 按期末存量口径（已确认） | **算法类型满足，现实现不满足**。Demo/xlsx 是无年轴 `COUNT DISTINCT`，没有 `成立年 ≤ Y`、没有存量环比。             |
| 输入（已拍路径）     | 成立年不在产业链四表，走企业库 `incorporation_date`（`credit_code`↔`external_id`）。四表缺列 **不是**算法缺口。 |
| 废表名          | 已替换 `industry_chain_entity_rel`，不是算法缺口。                                            |


**算法缺口**

- **无新模型缺口。**
- 现实现未做按年期末存量/存量环比（demo 仍是无年轴快照）= 实现债，等 IMPL 叶，本叶不写代码。
- Mapping 要写：`credit_code`↔`external_id`，年=`incorporation_date`。这是工厂键，不是算法缺口。

**可实现**

路径已拍：**条件是**（类型够）。GDF/模拟 GDF 写上跨域 JOIN；ADS 按年 series（值 = 累计家数）；demo 现未按此实现。  
与 A2 拆卡 **已拍**（本条存量 / A2 新增）。`is_deleted` 取数不挡口径确认。

**口径文档债（不是源缺失）**

- 旧表名替换为 `industry_chain_entity_rel` ← `dwd_org_industry_tags`。
- 进度表口径摘要需从「最新批次快照全量去重」改为「按年期末存量（成立年 ≤ Y）」（**已确认**，data-agent 正式化，本叶不改 YAML）。

**缺口（真缺，不含废表名）**

- 无 CHAIN GDF 09 Mapping 作业（JOIN 未进工厂）。
- 矩阵无本 ID（进度表 D3「齐备」过满）。
- 挂接表按约定 `is_deleted=0` 现网 0 行（接入，不是算法）。
- Demo 未按增量路径实现。

**需要李伟确认的问题**

1. ~~xlsx 快照 vs 按年~~ **已拍：按年切，不锁无年轴快照。**
2. ~~旧表名~~ **已拍：替换** `entity_rel`**。**
3. ~~成立日来源~~ **已拍：企业库** `incorporation_date`**。**
4. ~~与 A2 分工~~ **已拍（2026-08-27）：本 ID = 各年期末存量；A2 = 当年新增。**
5. 挂接 `is_deleted=0` 为 0：live 等供应方 / demo 继续 Mock —— **不挡本条口径确认**，IMPL 再处理。
6. YAML：**已确认**，交 data-agent 正式化；本叶不改。

**2026-08-27 核对小结**

- 两 xlsx 全列、需规 95（2）、分层、demo 实测：分析有效。
- 后半「无成立年所以不可实现」已作废。
- **本条已确认**：期末存量 `COUNT(成立年 ≤ Y)` + 存量环比。YAML/Demo 实现债不挡确认。

---



### A2 · `M_CHAIN_ENTERPRISE_NEW_COUNT` · 新增关联企业数（已确认）

**指标描述**：按年份分组新增产业链关联企业数；统计窗口为逐年，按 chain_score 首次出现年份或注册年份归集去重。

> 2026-08-27 `human:李伟`：**确认（解挂）**。卡片交 **当年新增**：`COUNT(成立年 = Y)` + 新增环比（需规 95（2）字面）。A1 交期末存量，不重复。  
> 2026-08-26 曾挂起。取数同 A1：挂接 `credit_code` → 企业库 `external_id` → `incorporation_date`。`chain_score`/入链年/四表内成立年从口径去掉。废表名只替换。

分析日：2026-08-26。kit 仍走 `getMetric`（矩阵无本 ID）。Demo 读 `111.198.38.90:34306`。废表名按规则 9 只写替换。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **118**


| 列         | 值                                                      |
| --------- | ------------------------------------------------------ |
| 指标ID      | M_CHAIN_ENTERPRISE_NEW_COUNT                           |
| 指标名       | 新增关联企业数                                                |
| 决策清单中的编号  | （空）                                                    |
| 域         | 产业链                                                    |
| 模块        | E2 产业链（待四维评估）                                          |
| 模块说明      | 产业链                                                    |
| 专题维度Owner | 李伟                                                     |
| 算法类型      | STAT                                                   |
| 合同集合      | F∩L                                                    |
| 差集判定      | mapped                                                 |
| 语义层开发阶段   | 未标                                                     |
| 验收单元      | —                                                      |
| 四维评估      | 待评估                                                    |
| 定义状态      | 已对齐                                                    |
| 开放项       | （空）                                                    |
| 结构支撑      | 待评估                                                    |
| 结构缺口      | （空）                                                    |
| 结构判定      | —                                                      |
| 源映射       | 齐备                                                     |
| 源缺口       | （空）                                                    |
| 接入状态      | Mock                                                   |
| 接入阶段      | （空）                                                    |
| 综合就绪      | 待接入（Mock）                                              |
| 卡点责任方     | 李伟                                                     |
| 更新频率      | daily                                                  |
| 口径摘要      | 按年份分组新增产业链关联企业数；统计窗口为逐年，按 chain_score 首次出现年份或注册年份归集去重。 |
| 缺口说明      | （空）                                                    |
| 更新日期      | 2026-08-25                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **36**


| 列        | 值                                                      |
| -------- | ------------------------------------------------------ |
| 指标ID     | M_CHAIN_ENTERPRISE_NEW_COUNT                           |
| 指标名      | 新增关联企业数                                                |
| 决策清单中的编号 | （空）                                                    |
| 域        | 产业链                                                    |
| 模块       | CHAIN                                                  |
| 算法类型     | STAT                                                   |
| D1定义     | —                                                      |
| D4接入     | —                                                      |
| 需求来源条数   | 1                                                      |
| 需求回填     | 已回填                                                    |
| 来源系统     | 展示+专题                                                  |
| 主来源分册    | 05 算法库需规                                               |
| 主来源序号    | 95                                                     |
| 主来源名称    | 产业链基础指标模型构建                                            |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：新增关联企业数。           |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                     |
| 全部来源     | 05·95 产业链基础指标模型构建                                      |
| 口径摘要     | 按年份分组新增产业链关联企业数；统计窗口为逐年，按 chain_score 首次出现年份或注册年份归集去重。 |
| 更新日期     | 2026-08-25                                             |


Sheet：`汇总`：无本 ID。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **39**（仅 1 行）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_ENTERPRISE_NEW_COUNT                      |
| 指标名      | 新增关联企业数                                           |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示+专题                                             |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：新增关联企业数。      |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW, CHAIN-TOPIC-PANORAMA       |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**两表对齐**

- 口径摘要、STAT、F∩L/mapped、05·95：两表一致。
- 打架：进度表定义已对齐/源齐备/Mock；需求来源 D1/D4=—（`found.matrix=false`）。进度表「源缺口（空）」与「无年份字段」打架。
- 来源系统本条是 **展示+专题**（A1 仅专题）；页面多 `CHAIN-PORTAL-OVERVIEW`。
- 决策清单编号空；无单独 QC。

**需求**

仍是 `ALGO-CHAIN-BASE-95`。95（2）「产业企业规模」原文 = 每年成立数量 + 环比。本 ID 的 xlsx 口径比 A1 更贴近（2），但是归年规则写成 `**chain_score` 首次出现年 或 注册年**，需规只说注册/成立，没有 `chain_score`。

**MCP / seed**

- formula：`COUNT(DISTINCT enterprise_code) GROUP BY YEAR(首次关联时间)`
- `source_tables` 仍写旧名 → **替换**为 `industry_chain_entity_rel` ← `dwd_org_industry_tags`，不记缺表。
- 矩阵无本 ID。

**ODS → DWD → ADS**


| 层                    | 结论                                                                                                                                        |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| ODS                  | 挂接：`dwd_org_industry_tags`（链 + `credit_code`）。成立日不在四表，走企业要素库 `dwd_org_base_info.incorporation_date`（键 `external_id`，已拍）。                  |
| 三方 `gkx`             | 同 A1：`is_deleted=0` → 0 行。                                                                                                                |
| DWD                  | 现行 `industry_chain_entity_rel`。Demo 列无 `chain_score`、无注册年。有 `valid_from`/`created_time`（治理列）。旧名 `industry_chain_enterprise` **已替换，不记缺失**。 |
| ADS                  | 应落 fact 或 series，`metric_id=M_CHAIN_ENTERPRISE_NEW_COUNT`。                                                                                |
| Demo `111.198.38.90` | ADS fact/series 本 ID **0 行**。`chainan/llm_ods` **0 处**引用本 metric_id。                                                                      |


**算法是否满足**


| 项        | 结论                       |
| -------- | ------------------------ |
| 类型       | STAT + 环比，满足。            |
| 取数路径（已拍） | **可以落地**：挂接表企业 × 企业库成立日。 |
| Demo     | 未按此路径实现。                 |


**算法缺口**

- **无新模型缺口。**
- Mapping 要写：`credit_code` ↔ `external_id`，年 = `incorporation_date`。这是工厂键，不是算法缺口。
- `chain_score` / 四表内成立年：**从口径去掉**（已改走企业库），不当缺表。

**可实现**

**条件是（路径已拍）**：GDF/模拟 GDF 写上跨域 JOIN；ADS 按年 series；demo 现未实现。

**口径文档债（不是源缺失）**

- 旧表名替换为 `entity_rel` ← tags；公式去重键 `credit_code`。
- `chain_score`、xlsx「首次关联时间」：从口径去掉，改成立日。

**缺口（真缺）**

- 跨域 JOIN 尚未进 GDF Mapping。
- Demo 未实现本 metric_id。
- 矩阵无本 ID；无 CHAIN GDF 09。

**需要李伟确认的问题**

1. ~~注册年 vs 入链年~~ **已拍：工商成立日（同 A1）。**
2. ~~与 A1 重复~~ **已拍（随 A1）：本条当年新增，A1 期末存量。**
3. ~~确认/挂起~~ **已拍（2026-08-27）：确认。**

**口径一句（已确认）**

年 Y 该链上**当年新成立**的关联企业去重家数（成立年 = Y）+ 相对上年的新增环比。  
xlsx 仍写 `chain_score` 首次年或注册年、seed 写「首次关联时间」——文档债，确认后交 data-agent，本叶不改 YAML。

**2026-08-27 核对小结**

- 两 xlsx 全列、需规 95（2）、分层、demo 0 行 0 代码：分析有效。
- **本条已确认**：当年新增 `COUNT(成立年 = Y)` + 新增环比。YAML/Demo/GDF 债不挡确认。

---

（A2 已确认。下一条 A3。）

### A3 · `M_CHAIN_INSTITUTION_COUNT` · 产业链关联机构数（已确认）

**指标描述**：产业链关联科研机构/高校去重总数；对象范围 dwd.industry_chain_enterprise 中 org_type=机构 的记录，按 enterprise_name 去重。

> 2026-08-27 `human:李伟`：**确认**。  
> **机构集合 = 乙**：机构要素库（国内机构）**另挂链**，不从企业挂接表筛 `org_type`。字段对照：[国内机构要素库](https://docs.qq.com/sheet/DWWxaRUF6b1JCakFF?tab=8qlf48)（腾讯文档「版权人才、企业机构、政策数据汇总表」· tab 国内机构要素库）。入站表名 / 注册日列 Mapping 钉死（分析稿举例 `dwd_org_heis_info`，以入站真源为准）。  
> **卡片 = 当年成立**：`COUNT(成立年 = Y)` + 新增环比（需规 95（3）字面，同 A2）。**没有**机构期末存量卡。  
> 去重用机构代码不用名；废表名只替换；DWD 挂接走 `industry_chain_entity_rel` 且需 `**entity_type=institution`（或等价机构边）**——现网/Demo 还没有，属 Mapping/实现债。

分析日：2026-08-26。同类问题已按 A1 处理，不重问。kit：`getMetric`。Demo：`111.198.38.90:34306`。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **123**


| 列         | 值                                                                                           |
| --------- | ------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_INSTITUTION_COUNT                                                                   |
| 指标名       | 产业链关联机构数                                                                                    |
| 决策清单中的编号  | （空）                                                                                         |
| 域         | 产业链                                                                                         |
| 模块        | E2 产业链（待四维评估）                                                                               |
| 模块说明      | 产业链                                                                                         |
| 专题维度Owner | 李伟                                                                                          |
| 算法类型      | STAT                                                                                        |
| 合同集合      | F∩L                                                                                         |
| 差集判定      | mapped                                                                                      |
| 语义层开发阶段   | 未标                                                                                          |
| 验收单元      | —                                                                                           |
| 四维评估      | 待评估                                                                                         |
| 定义状态      | 已对齐                                                                                         |
| 开放项       | （空）                                                                                         |
| 结构支撑      | 待评估                                                                                         |
| 结构缺口      | （空）                                                                                         |
| 结构判定      | —                                                                                           |
| 源映射       | 齐备                                                                                          |
| 源缺口       | （空）                                                                                         |
| 接入状态      | Mock                                                                                        |
| 接入阶段      | （空）                                                                                         |
| 综合就绪      | 待接入（Mock）                                                                                   |
| 卡点责任方     | 李伟                                                                                          |
| 更新频率      | daily                                                                                       |
| 口径摘要      | 产业链关联科研机构/高校去重总数；对象范围 dwd.industry_chain_enterprise 中 org_type=机构 的记录，按 enterprise_name 去重。 |
| 缺口说明      | （空）                                                                                         |
| 更新日期      | 2026-08-25                                                                                  |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **46**


| 列        | 值                                                                                           |
| -------- | ------------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_INSTITUTION_COUNT                                                                   |
| 指标名      | 产业链关联机构数                                                                                    |
| 决策清单中的编号 | （空）                                                                                         |
| 域        | 产业链                                                                                         |
| 模块       | CHAIN                                                                                       |
| 算法类型     | STAT                                                                                        |
| D1定义     | —                                                                                           |
| D4接入     | —                                                                                           |
| 需求来源条数   | 1                                                                                           |
| 需求回填     | 已回填                                                                                         |
| 来源系统     | 专题系统                                                                                        |
| 主来源分册    | 05 算法库需规                                                                                    |
| 主来源序号    | 95                                                                                          |
| 主来源名称    | 产业链基础指标模型构建                                                                                 |
| 主来源简述    | 产业链 / 基础指标：产业链基础指标模型构建                                                                      |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                                          |
| 全部来源     | 05·95 产业链基础指标模型构建                                                                           |
| 口径摘要     | 产业链关联科研机构/高校去重总数；对象范围 dwd.industry_chain_enterprise 中 org_type=机构 的记录，按 enterprise_name 去重。 |
| 更新日期     | 2026-08-25                                                                                  |


Sheet：`汇总`：无本 ID。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **49**（仅 1 行）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_INSTITUTION_COUNT                         |
| 指标名      | 产业链关联机构数                                          |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 产业链 / 基础指标：产业链基础指标模型构建                            |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-PANORAMA                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**两表对齐**：口径/STAT/05·95/全景一致。进度表 D3 齐备 vs 矩阵缺失，同 A1。xlsx 去重键 `enterprise_name`、对象旧表 `industry_chain_enterprise`、`org_type=机构`。

**需求**：95（3）产业机构规模 = 每年机构成立 + 环比。xlsx 写成快照按名去重。**已拍：跟需规（3）/A2，当年成立；不锁 xlsx 存量。**

**跟 A1 同样处理（不重问）**

- 旧表 → `industry_chain_entity_rel`，不记缺失。
- 增量：挂接主体 + 信用代码拼要素库成立日 + 环比。
- 去重用代码，不用 `enterprise_name`。
- `chain_score` 不进本条。

**本条特有（已拍）**

挂接表 `dwd_org_industry_tags` 是产业关联**企业**，无机构类型列。Demo `entity_rel` 只有 `enterprise`/`product`。  
**乙**：机构要素库另挂链（对照腾讯文档国内机构要素库）。成立/注册日走**机构库**，不拼企业库 `incorporation_date`。YAML 的 `org_type=机构` + 按名去重 **作废**。

**ODS → DWD → ADS**


| 层      | 结论                                                                                          |
| ------ | ------------------------------------------------------------------------------------------- |
| ODS 挂接 | **乙**：机构要素库 × 链。企业 tags **不算**本条对象。注册年走机构库列（Mapping 钉死）。                                    |
| DWD    | `entity_rel` 增加机构边 `entity_type=institution`（或等价）；现无。旧名 `industry_chain_enterprise` 只替换不记缺。 |
| ADS    | 应落本 `metric_id`（fact/series）。                                                               |
| Demo   | ADS **0 行**；代码 **0 引用**。                                                                    |


**算法是否满足**


| 项    | 结论                                            |
| ---- | --------------------------------------------- |
| 类型   | STAT+环比，满足（同 A1）。                             |
| 增量路径 | 类型够。机构挂接选 **乙**（已拍）。现缺机构边 + 机构库 Mapping，不是模型。 |
| Demo | 未实现。                                          |


**算法缺口**

- 无新模型缺口。
- Mapping：机构要素库挂链（`entity_type=institution`）；注册年 = 机构库注册/成立列；去重 = 机构代码。  
- YAML `org_type=机构` / `COUNT(DISTINCT enterprise_name)` / 废表名：文档债，确认后 data-agent 改，本叶不改 YAML。

**可实现**

**条件是（口径已拍）**：GDF/模拟 GDF 写上机构库挂链 + 注册年；ADS 按年 series（值 = 当年成立家数）。Demo 现未实现。

**需要李伟确认的问题（仅特有）**

1. ~~机构集合甲/乙~~ **已拍：乙**（机构要素库另挂链）。对照 [国内机构要素库](https://docs.qq.com/sheet/DWWxaRUF6b1JCakFF?tab=8qlf48)。
2. ~~存量 vs 当年成立~~ **已拍：当年成立**（需规 95（3）/A2）。不另做机构存量卡。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

年 Y 该链上**当年新成立**的关联机构去重家数（机构库注册年 = Y）+ 相对上年的新增环比。对象 = 机构要素库另挂到该链的机构，不是企业 tags 里筛出来的高校。

**2026-08-27 核对小结**

- 材料有效。特有问题 1、2 已拍。
- **本条已确认**：乙 + 当年成立。YAML/Demo/机构边 Mapping 债不挡确认。

---

（A3 已确认。以下 A4–E39 为批量续写，统一待核对。）

### 批量续写说明（A4–E39）

2026-08-26 `human:李伟`：先按规则把 39 条跑完再逐个核对拍板。A1/A2 仍为挂起；A3 及以下均为待确认。
并行子任务因账号账单中断，本段由主会话续写。xlsx 全列来自同日 dump；kit 来自 `getMetric`；Demo 读 `111.198.38.90:34306`。

共性（不在每条重复展开）：无 CHAIN GDF 09 派单包；绝大多数 `found.matrix=false`；进度表「源映射齐备」常过满；Java 只读 ADS。

### A4 · `M_CHAIN_NEWS_COUNT` · 动态资讯数（挂起）

**指标描述**：产业链相关资讯去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_news 全量，按 news_id 去重。

> 2026-08-27 `human:李伟`：**挂起**（不计入已确认）。  
> **开放项 CHAIN-NEWS-SRC-01**：ODS `dwd_industry_chain_news_info` 只是合规交付表，**没有利用价值**，不能当本指标可算源。后期探：从**机构维度资讯**、**行业分析要素库**能否洗出产业链资讯。洗通之前不算「源齐备」。  
> 快照总数 vs 按发布时间：源未定，**暂不拍**。热点判定仍归 A5。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `49` fact / `95` series；代码：ads_v2.py, read_v2.py。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **133**


| 列         | 值                                                                     |
| --------- | --------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_NEWS_COUNT                                                    |
| 指标名       | 动态资讯数                                                                 |
| 决策清单中的编号  | （空）                                                                   |
| 域         | 产业链                                                                   |
| 模块        | E2 产业链（待四维评估）                                                         |
| 模块说明      | 产业链                                                                   |
| 专题维度Owner | 李伟                                                                    |
| 算法类型      | STAT                                                                  |
| 合同集合      | F∩L                                                                   |
| 差集判定      | mapped                                                                |
| 语义层开发阶段   | 未标                                                                    |
| 验收单元      | —                                                                     |
| 四维评估      | 待评估                                                                   |
| 定义状态      | 已对齐                                                                   |
| 开放项       | （空）                                                                   |
| 结构支撑      | 待评估                                                                   |
| 结构缺口      | （空）                                                                   |
| 结构判定      | —                                                                     |
| 源映射       | 齐备                                                                    |
| 源缺口       | （空）                                                                   |
| 接入状态      | Mock                                                                  |
| 接入阶段      | （空）                                                                   |
| 综合就绪      | 待接入（Mock）                                                             |
| 卡点责任方     | 李伟                                                                    |
| 更新频率      | daily                                                                 |
| 口径摘要      | 产业链相关资讯去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_news 全量，按 news_id 去重。 |
| 缺口说明      | （空）                                                                   |
| 更新日期      | 2026-08-25                                                            |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **58**


| 列        | 值                                                                     |
| -------- | --------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_NEWS_COUNT                                                    |
| 指标名      | 动态资讯数                                                                 |
| 决策清单中的编号 | （空）                                                                   |
| 域        | 产业链                                                                   |
| 模块       | CHAIN                                                                 |
| 算法类型     | STAT                                                                  |
| D1定义     | —                                                                     |
| D4接入     | —                                                                     |
| 需求来源条数   | 1                                                                     |
| 需求回填     | 已回填                                                                   |
| 来源系统     | 展示系统                                                                  |
| 主来源分册    | 05 算法库需规                                                              |
| 主来源序号    | 95                                                                    |
| 主来源名称    | 产业链基础指标模型构建                                                           |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：动态资讯数。                            |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                    |
| 全部来源     | 05·95 产业链基础指标模型构建                                                     |
| 口径摘要     | 产业链相关资讯去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain_news 全量，按 news_id 去重。 |
| 更新日期     | 2026-08-25                                                            |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **61**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_NEWS_COUNT                                |
| 指标名      | 动态资讯数                                             |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：动态资讯数。        |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：最新批次，产业链资讯按资讯ID去重计数（xlsx）。对应需规 95（7）资讯维的计数部分，不含热点判定。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT dwd.industry_chain_news.news_id)`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_news <- ods: dwd_industry_chain_news_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：ODS `dwd_industry_chain_news_info`（三方现网约 1.2 万行）→ DWD 现行 `industry_chain_news_event`（旧名 `industry_chain_news` 只替换）→ ADS `industry_chain_metric_fact`/`_series`。

**算法是否满足**：STAT 够：COUNT DISTINCT。Demo 已写 ADS fact 49 / series 95（`ads_v2.py`/`read_v2.py`）。

**算法缺口**：无模型缺口。去重键用资讯业务键（DWD `event_id`/`source_news_id`），不用废名 `news_id` 表。

**可实现**：条件是：Mapping 钉资讯去重键；demo 路径已通。Demo ODS 该表 0 行、DWD 有 130 行，与三方现网不是同一灌数。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：矩阵无本 ID；无 CHAIN GDF 09；Demo ODS 资讯空。

**需要李伟确认的问题（仅特有）**

1. ~~快照 vs 按发布时间~~ **挂起未拍**（源先不定，数窗口后补）。
2. 热点阈值：**不在本条**（A5）。
3. ~~确认/挂起~~ **已拍：挂起。** 开放项 **CHAIN-NEWS-SRC-01**（合规资讯表无利用价值 → 机构维资讯 + 行业分析要素库后期洗数）。

**口径一句（挂起）**

xlsx/YAML 仍写「最新批次按 news_id 去重」。**不当已确认**。真源不走 `dwd_industry_chain_news_info`；替代路径未探明。

**2026-08-27 核对小结**

- 材料仍有效。Demo 现灌的合规表路径**不算**可落地源。
- **本条挂起**：CHAIN-NEWS-SRC-01。不改 YAML、不写洗数。

**2026-09-01 Mapping 复核**

- CHAIN 09 **禁止**灌 `industry_chain_news_event`；**B2 不写** `industry_analysis_`*。乙路本期没有项目 DWD 可读。
- 甲 `enterprise_news` 不在本包。未拍之前 A4 **继续挂起**。xlsx 废名 `industry_chain_news` 只替换、不当源。

---



### A5 · `M_CHAIN_HOT_NEWS_COUNT` · 热门资讯数（挂起）

**指标描述**：pending_data_lead：热度评分达到阈值的资讯计数；阈值待甲方确认，临时默认 heat_score>=80。

> 2026-08-27 `human:李伟`：**挂起**（跟 A4，CHAIN-NEWS-SRC-01）。合规资讯表不当可算源。浏览量/评论 vs NLP `heat_score`、阈值是否锁 80：**源洗通后再拍**。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **122**


| 列         | 值                                                                                         |
| --------- | ----------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_HOT_NEWS_COUNT                                                                    |
| 指标名       | 热门资讯数                                                                                     |
| 决策清单中的编号  | （空）                                                                                       |
| 域         | 产业链                                                                                       |
| 模块        | E2 产业链（待四维评估）                                                                             |
| 模块说明      | 产业链                                                                                       |
| 专题维度Owner | 李伟                                                                                        |
| 算法类型      | STAT                                                                                      |
| 合同集合      | F∩L                                                                                       |
| 差集判定      | mapped                                                                                    |
| 语义层开发阶段   | 未标                                                                                        |
| 验收单元      | —                                                                                         |
| 四维评估      | 待评估                                                                                       |
| 定义状态      | 已对齐                                                                                       |
| 开放项       | （空）                                                                                       |
| 结构支撑      | 待评估                                                                                       |
| 结构缺口      | （空）                                                                                       |
| 结构判定      | —                                                                                         |
| 源映射       | 待评估                                                                                       |
| 源缺口       | （空）                                                                                       |
| 接入状态      | Mock                                                                                      |
| 接入阶段      | （空）                                                                                       |
| 综合就绪      | 待结构设计                                                                                     |
| 卡点责任方     | 李伟                                                                                        |
| 更新频率      | daily                                                                                     |
| 口径摘要      | pending_data_lead：热度评分达到阈值的资讯计数；阈值待甲方确认，临时默认 heat_score>=80。                              |
| 缺口说明      | 热门资讯数=热度评分≥80的资讯计数。热度阈值临时默认80，正式阈值待甲方确认。基于 NLP 热度评分。formula 待 algorithm-agent。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                                |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **45**


| 列        | 值                                                            |
| -------- | ------------------------------------------------------------ |
| 指标ID     | M_CHAIN_HOT_NEWS_COUNT                                       |
| 指标名      | 热门资讯数                                                        |
| 决策清单中的编号 | （空）                                                          |
| 域        | 产业链                                                          |
| 模块       | CHAIN                                                        |
| 算法类型     | STAT                                                         |
| D1定义     | —                                                            |
| D4接入     | —                                                            |
| 需求来源条数   | 1                                                            |
| 需求回填     | 已回填                                                          |
| 来源系统     | 展示系统                                                         |
| 主来源分册    | 05 算法库需规                                                     |
| 主来源序号    | 95                                                           |
| 主来源名称    | 产业链基础指标模型构建                                                  |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：热门资讯数。                   |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                           |
| 全部来源     | 05·95 产业链基础指标模型构建                                            |
| 口径摘要     | pending_data_lead：热度评分达到阈值的资讯计数；阈值待甲方确认，临时默认 heat_score>=80。 |
| 更新日期     | 2026-08-25                                                   |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **48**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_HOT_NEWS_COUNT                            |
| 指标名      | 热门资讯数                                             |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：热门资讯数。        |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：热度分≥阈值的资讯计数，临时 heat_score≥80，阈值待甲方。需规 95（7）写浏览量/评论数阈值，与 seed 的 heat_score 打架。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT news_id) WHERE heat_score >= 80`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_news.heat_score <- ods: dwd_industry_chain_news_info.heat_score']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：资讯 ODS 约定列无浏览量、评论数、heat_score。DWD `industry_chain_news_event` 亦无热度列（映射未写）。ADS 本 ID 0 行。

**算法是否满足**：最后一公里 STAT 计数够。热度分本身不是 STAT：需规偏阅读指标，seed 偏 NLP 热度。

**算法缺口**：缺热度输入列/模型。阈值未拍（缺口说明已写临时 80）。不把废表当缺口。

**可实现**：否（无热度字段）。条件：拍热度定义（浏览评论 vs NLP）并落 DWD 列后再 STAT。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：热度字段未进四表/DWD；阈值待甲方；Demo 未实现；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~同源挂起~~ **已拍：挂起**（CHAIN-NEWS-SRC-01，同 A4）。
2. ~~热度定义/阈值 80~~ **挂起未拍**（源洗通后再拍）。
3. ~~确认/挂起~~ **已拍：挂起。**

**口径一句（挂起）**

xlsx/YAML 仍写 `heat_score≥80` 计数。**不当已确认**。真源不走合规资讯表；热度列两套都还没有。

**2026-08-27 核对小结**

- 材料有效。**本条挂起**（CHAIN-NEWS-SRC-01）。不改 YAML、不写洗数。

---



### A6 · `M_CHAIN_NEWS_SENTIMENT_RATIO` · 资讯正面情感占比（挂起）

**指标描述**：产业链相关资讯中正面情感占比（%）；基于 NLP 情感分析结果统计。

> 2026-08-27 `human:李伟`：**挂起**（跟 A4/A5，CHAIN-NEWS-SRC-01）。合规资讯表不当可算源。情感分类是否另立算法叶、本 ID 是否只做占比：**源洗通后再拍**。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **134**


| 列         | 值                                                                                           |
| --------- | ------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_NEWS_SENTIMENT_RATIO                                                                |
| 指标名       | 资讯正面情感占比                                                                                    |
| 决策清单中的编号  | （空）                                                                                         |
| 域         | 产业链                                                                                         |
| 模块        | E2 产业链（待四维评估）                                                                               |
| 模块说明      | 产业链                                                                                         |
| 专题维度Owner | 李伟                                                                                          |
| 算法类型      | STAT                                                                                        |
| 合同集合      | F∩L                                                                                         |
| 差集判定      | mapped                                                                                      |
| 语义层开发阶段   | 未标                                                                                          |
| 验收单元      | —                                                                                           |
| 四维评估      | 待评估                                                                                         |
| 定义状态      | 已对齐                                                                                         |
| 开放项       | （空）                                                                                         |
| 结构支撑      | 待评估                                                                                         |
| 结构缺口      | （空）                                                                                         |
| 结构判定      | —                                                                                           |
| 源映射       | 待评估                                                                                         |
| 源缺口       | （空）                                                                                         |
| 接入状态      | Mock                                                                                        |
| 接入阶段      | （空）                                                                                         |
| 综合就绪      | 待结构设计                                                                                       |
| 卡点责任方     | 李伟                                                                                          |
| 更新频率      | daily                                                                                       |
| 口径摘要      | 产业链相关资讯中正面情感占比（%）；基于 NLP 情感分析结果统计。                                                          |
| 缺口说明      | 资讯正面情感占比=正面情感资讯数/总资讯数*100。依赖 NLP 情感分析结果。情感分类阈值与准确率待评估。formula 待 algorithm-agent。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                                  |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **59**


| 列        | 值                                                                                 |
| -------- | --------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_NEWS_SENTIMENT_RATIO                                                      |
| 指标名      | 资讯正面情感占比                                                                          |
| 决策清单中的编号 | （空）                                                                               |
| 域        | 产业链                                                                               |
| 模块       | CHAIN                                                                             |
| 算法类型     | STAT                                                                              |
| D1定义     | —                                                                                 |
| D4接入     | —                                                                                 |
| 需求来源条数   | 1                                                                                 |
| 需求回填     | 已回填                                                                               |
| 来源系统     | 展示系统                                                                              |
| 主来源分册    | 05 算法库需规                                                                          |
| 主来源序号    | 95                                                                                |
| 主来源名称    | 产业链基础指标模型构建                                                                       |
| 主来源简述    | M_CHAIN_* 已在 seed 登记，属 B 轨，禁止 missing。资讯原料对上 05 seq 95 产业动态资讯。 05 无独立情感分类专核；NLP … |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                                |
| 全部来源     | 05·95 产业链基础指标模型构建                                                                 |
| 口径摘要     | 产业链相关资讯中正面情感占比（%）；基于 NLP 情感分析结果统计。                                                |
| 更新日期     | 2026-08-25                                                                        |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **62**（第 1 条）


| 列        | 值                                                                                 |
| -------- | --------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_NEWS_SENTIMENT_RATIO                                                      |
| 指标名      | 资讯正面情感占比                                                                          |
| 决策清单中的编号 | （空）                                                                               |
| 域        | 产业链                                                                               |
| 模块       | CHAIN                                                                             |
| 分册       | 05                                                                                |
| 分册名称     | 05 算法库需规                                                                          |
| 系统       | 展示系统                                                                              |
| 序号       | 95                                                                                |
| 需规名称     | 产业链基础指标模型构建                                                                       |
| 简要描述     | M_CHAIN_* 已在 seed 登记，属 B 轨，禁止 missing。资讯原料对上 05 seq 95 产业动态资讯。 05 无独立情感分类专核；NLP … |
| 需规ID     | ALGO-CHAIN-BASE-95                                                                |
| 角色       | 算法库叶                                                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW                                                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md                                 |
| 回填状态     | 已回填                                                                               |




#### 4) 结合分析

**口径一句**：xlsx：正面情感资讯占比。需规 95（7）未单列情感分类。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（COUNT(sentiment='positive') / COUNT(*) * 100）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_news.sentiment <- NLP', 'dwd.industry_chain_news <- ods: dwd_industry_chain_news_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：资讯 ODS 无 sentiment。NLP 属 Python 算法，结果应落 DWD/ADS 后再 STAT。Demo 0 行 0 代码。

**算法是否满足**：占比是 STAT。情感分类不是本叶 STAT，属 NLP/模型（可交算法，但仍须 Python `/internal`）。

**算法缺口**：缺情感标签列与分类阈值。无新公式缺口。

**可实现**：条件是：先有情感分类产出，本叶只做占比。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：无情感字段；需规无独立情感专核；Demo 未实现；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~同源挂起~~ **已拍：挂起**（CHAIN-NEWS-SRC-01）。
2. ~~占比 STAT vs 情感分类另叶~~ **挂起未拍**（源洗通后再拍）。
3. ~~确认/挂起~~ **已拍：挂起。**

**口径一句（挂起）**

xlsx/YAML 仍写 NLP 正面占比。**不当已确认**。需规 95（7）无情感专核。

**2026-08-27 核对小结**

- 材料有效。**本条挂起**（CHAIN-NEWS-SRC-01）。

---



### A7 · `M_CHAIN_GLOBAL_REGION_COUNT` · 全球分布区域数（已确认）

**指标描述**：产业链关联企业/机构覆盖的全球国家/地区去重数；按企业总部所在国家/地区 DISTINCT 计数。

> 2026-08-27 `human:李伟`：**确认**。交 **每个国家**的企业+机构主体数（需规 95（5）），不锁 xlsx「覆盖国家个数」。对象 = 链上企业（企业库国家列）+ A3 乙机构（机构库国家列）。YAML `headquarters_province/city` 不作全球键。覆盖国家个数可从切片派生。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **120**


| 列         | 值                                                 |
| --------- | ------------------------------------------------- |
| 指标ID      | M_CHAIN_GLOBAL_REGION_COUNT                       |
| 指标名       | 全球分布区域数                                           |
| 决策清单中的编号  | （空）                                               |
| 域         | 产业链                                               |
| 模块        | E2 产业链（待四维评估）                                     |
| 模块说明      | 产业链                                               |
| 专题维度Owner | 李伟                                                |
| 算法类型      | STAT                                              |
| 合同集合      | F∩L                                               |
| 差集判定      | mapped                                            |
| 语义层开发阶段   | 未标                                                |
| 验收单元      | —                                                 |
| 四维评估      | 待评估                                               |
| 定义状态      | 已对齐                                               |
| 开放项       | （空）                                               |
| 结构支撑      | 待评估                                               |
| 结构缺口      | （空）                                               |
| 结构判定      | —                                                 |
| 源映射       | 齐备                                                |
| 源缺口       | （空）                                               |
| 接入状态      | Mock                                              |
| 接入阶段      | （空）                                               |
| 综合就绪      | 待接入（Mock）                                         |
| 卡点责任方     | 李伟                                                |
| 更新频率      | daily                                             |
| 口径摘要      | 产业链关联企业/机构覆盖的全球国家/地区去重数；按企业总部所在国家/地区 DISTINCT 计数。 |
| 缺口说明      | （空）                                               |
| 更新日期      | 2026-08-25                                        |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **39**


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_GLOBAL_REGION_COUNT                       |
| 指标名      | 全球分布区域数                                           |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 算法类型     | STAT                                              |
| D1定义     | —                                                 |
| D4接入     | —                                                 |
| 需求来源条数   | 1                                                 |
| 需求回填     | 已回填                                               |
| 来源系统     | 专题系统                                              |
| 主来源分册    | 05 算法库需规                                          |
| 主来源序号    | 95                                                |
| 主来源名称    | 产业链基础指标模型构建                                       |
| 主来源简述    | 产业链 / 基础指标：产业链基础指标模型构建                            |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                |
| 全部来源     | 05·95 产业链基础指标模型构建                                 |
| 口径摘要     | 产业链关联企业/机构覆盖的全球国家/地区去重数；按企业总部所在国家/地区 DISTINCT 计数。 |
| 更新日期     | 2026-08-25                                        |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **42**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_GLOBAL_REGION_COUNT                       |
| 指标名      | 全球分布区域数                                           |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 产业链 / 基础指标：产业链基础指标模型构建                            |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：关联企业/机构总部国家/地区去重。需规 95（5）全球分布。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT region_code) WHERE scope='global'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl', 'dwd.enterprise.headquarters_province/city']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：挂接 tags 无国家列。同 A1：挂接 `credit_code` 拼企业/国外机构要素库地理字段。旧表名替换为 `entity_rel`。Demo 0。

**算法是否满足**：STAT DISTINCT 够。

**算法缺口**：无模型缺口。缺的是国家字段 Mapping（企业库/国外机构库哪一列）。

**可实现**：条件是：钉国家列并 JOIN 挂接。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：四表无国家；JOIN 未进 GDF；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~各国主体数 vs 覆盖国家个数~~ **已拍：各国主体数**（需规 95（5））。
2. ~~对象~~ **已拍：企业 + A3 乙机构**（企业库国家 + 机构库国家，Mapping 钉列）。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

按国家切片，该链上企业+机构（乙）去重主体数。国家列：企业库、机构库各钉一列。xlsx「DISTINCT 国家个数」作废；个数可派生。

**2026-08-27 核对小结**

- **本条已确认**。YAML/GDF/Demo 债不挡确认。

---



### A8 · `M_CHAIN_NATIONAL_REGION_COUNT` · 全国分布区域数（已确认）

**指标描述**：产业链关联企业/机构覆盖的全国省/市去重数；按企业总部所在省/市 DISTINCT 计数。

> 2026-08-27 `human:李伟`：**确认**。切到 **省**（需规 95（6））。按省切片数企业+乙机构主体，同 A7 结构。不锁 xlsx/YAML 的 DISTINCT 市。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **132**


| 列         | 值                                             |
| --------- | --------------------------------------------- |
| 指标ID      | M_CHAIN_NATIONAL_REGION_COUNT                 |
| 指标名       | 全国分布区域数                                       |
| 决策清单中的编号  | （空）                                           |
| 域         | 产业链                                           |
| 模块        | E2 产业链（待四维评估）                                 |
| 模块说明      | 产业链                                           |
| 专题维度Owner | 李伟                                            |
| 算法类型      | STAT                                          |
| 合同集合      | F∩L                                           |
| 差集判定      | mapped                                        |
| 语义层开发阶段   | 未标                                            |
| 验收单元      | —                                             |
| 四维评估      | 待评估                                           |
| 定义状态      | 已对齐                                           |
| 开放项       | （空）                                           |
| 结构支撑      | 待评估                                           |
| 结构缺口      | （空）                                           |
| 结构判定      | —                                             |
| 源映射       | 齐备                                            |
| 源缺口       | （空）                                           |
| 接入状态      | Mock                                          |
| 接入阶段      | （空）                                           |
| 综合就绪      | 待接入（Mock）                                     |
| 卡点责任方     | 李伟                                            |
| 更新频率      | daily                                         |
| 口径摘要      | 产业链关联企业/机构覆盖的全国省/市去重数；按企业总部所在省/市 DISTINCT 计数。 |
| 缺口说明      | （空）                                           |
| 更新日期      | 2026-08-25                                    |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **57**


| 列        | 值                                             |
| -------- | --------------------------------------------- |
| 指标ID     | M_CHAIN_NATIONAL_REGION_COUNT                 |
| 指标名      | 全国分布区域数                                       |
| 决策清单中的编号 | （空）                                           |
| 域        | 产业链                                           |
| 模块       | CHAIN                                         |
| 算法类型     | STAT                                          |
| D1定义     | —                                             |
| D4接入     | —                                             |
| 需求来源条数   | 1                                             |
| 需求回填     | 已回填                                           |
| 来源系统     | 专题系统                                          |
| 主来源分册    | 05 算法库需规                                      |
| 主来源序号    | 95                                            |
| 主来源名称    | 产业链基础指标模型构建                                   |
| 主来源简述    | 产业链 / 基础指标：产业链基础指标模型构建                        |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                            |
| 全部来源     | 05·95 产业链基础指标模型构建                             |
| 口径摘要     | 产业链关联企业/机构覆盖的全国省/市去重数；按企业总部所在省/市 DISTINCT 计数。 |
| 更新日期     | 2026-08-25                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **60**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_NATIONAL_REGION_COUNT                     |
| 指标名      | 全国分布区域数                                           |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 产业链 / 基础指标：产业链基础指标模型构建                            |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：总部省/市去重。需规 95（6）全国分布。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT headquarters_city) WHERE scope='national'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl', 'dwd.enterprise.headquarters_city <- ods: dwd_org_reg_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 A1 JOIN：`dwd_org_base_info.province/city`。Demo 映射曾用合成 `ext.city`，不当口径真源。

**算法是否满足**：STAT 够。

**算法缺口**：无模型缺口。省/市列走企业库 Mapping。

**可实现**：条件是：挂接+企业库省市 JOIN（同 A1 处理）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：GDF 未写该 JOIN；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~省 vs 市~~ **已拍：省**（需规 95（6））。
2. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

按省切片，该链上企业+乙机构去重主体数。省市列走企业库/机构库 Mapping。xlsx「DISTINCT 省/市个数」作废。

**2026-08-27 核对小结**

- **本条已确认**。YAML/GDF/Demo 债不挡确认。

---



### A9 · `M_CHAIN_SZ_REGION_COUNT` · 深圳产业分布区域数（已确认）

**指标描述**：深圳产业链关联企业/机构覆盖的区/县去重数；按深圳下辖区划 DISTINCT 计数。

> 2026-08-27 `human:李伟`：**确认**。按**区**切片数企业+乙机构（需规 95（9））。深圳 = `city=深圳市`。不锁 YAML 的 DISTINCT 区 + `city=深圳`。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **147**


| 列         | 值                                          |
| --------- | ------------------------------------------ |
| 指标ID      | M_CHAIN_SZ_REGION_COUNT                    |
| 指标名       | 深圳产业分布区域数                                  |
| 决策清单中的编号  | （空）                                        |
| 域         | 产业链                                        |
| 模块        | E2 产业链（待四维评估）                              |
| 模块说明      | 产业链                                        |
| 专题维度Owner | 李伟                                         |
| 算法类型      | STAT                                       |
| 合同集合      | F∩L                                        |
| 差集判定      | mapped                                     |
| 语义层开发阶段   | 未标                                         |
| 验收单元      | —                                          |
| 四维评估      | 待评估                                        |
| 定义状态      | 已对齐                                        |
| 开放项       | （空）                                        |
| 结构支撑      | 待评估                                        |
| 结构缺口      | （空）                                        |
| 结构判定      | —                                          |
| 源映射       | 齐备                                         |
| 源缺口       | （空）                                        |
| 接入状态      | Mock                                       |
| 接入阶段      | （空）                                        |
| 综合就绪      | 待接入（Mock）                                  |
| 卡点责任方     | 李伟                                         |
| 更新频率      | daily                                      |
| 口径摘要      | 深圳产业链关联企业/机构覆盖的区/县去重数；按深圳下辖区划 DISTINCT 计数。 |
| 缺口说明      | （空）                                        |
| 更新日期      | 2026-08-25                                 |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **99**


| 列        | 值                                             |
| -------- | --------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_REGION_COUNT                       |
| 指标名      | 深圳产业分布区域数                                     |
| 决策清单中的编号 | （空）                                           |
| 域        | 产业链                                           |
| 模块       | CHAIN                                         |
| 算法类型     | STAT                                          |
| D1定义     | —                                             |
| D4接入     | —                                             |
| 需求来源条数   | 1                                             |
| 需求回填     | 已回填                                           |
| 来源系统     | 专题系统                                          |
| 主来源分册    | 05 算法库需规                                      |
| 主来源序号    | 95                                            |
| 主来源名称    | 产业链基础指标模型构建                                   |
| 主来源简述    | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业分布区域数。 |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                            |
| 全部来源     | 05·95 产业链基础指标模型构建                             |
| 口径摘要     | 深圳产业链关联企业/机构覆盖的区/县去重数；按深圳下辖区划 DISTINCT 计数。    |
| 更新日期     | 2026-08-25                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **107**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_REGION_COUNT                           |
| 指标名      | 深圳产业分布区域数                                         |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业分布区域数。     |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：深圳下辖区县去重。需规 95（9）深圳产业分布。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT headquarters_district) WHERE headquarters_city='深圳'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise', 'dwd.enterprise.headquarters_district <- ods: dwd_company_location_tags']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：企业库有 `city`/`area`。挂接无区县。Demo `ext.district` 为合成。

**算法是否满足**：STAT 够。

**算法缺口**：无模型缺口。区县列 Mapping。

**可实现**：条件是：先筛深圳再 DISTINCT 区。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：区县 JOIN 未进 GDF；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~切区 vs DISTINCT 区县~~ **已拍：按区切片数主体**（需规 95（9））。
2. ~~深圳圈定~~ **已拍：**`city=深圳市`。后续深圳条默认跟本条。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

先筛 `city=深圳市`，再按区切片，该链上企业+乙机构去重主体数。区列 Mapping 钉死。xlsx「DISTINCT 区/县个数」作废。

**2026-08-27 核对小结**

- **本条已确认**。YAML 仍写 `city=深圳`（无「市」）和 DISTINCT 区，确认后改。GDF/Demo 债不挡确认。

---



### A10 · `M_CHAIN_SZ_ENTERPRISE_COUNT` · 深圳产业链企业数（已确认）

**指标描述**：总部在深圳且属目标产业链的企业去重数；按 headquarters_city=深圳 + chain_id 筛选 COUNT。

> 2026-08-27 `human:李伟`：**确认**。交 **当前一个数**（甲）：`city=深圳市` 的链上企业去重。不跟 A1 做按年序列。YAML `city=深圳` 确认后改成深圳市。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `49` fact / `0` series；代码：ads_v2.py, read_v2.py。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **98**


| 列         | 值                                                              |
| --------- | -------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_ENTERPRISE_COUNT                                    |
| 指标名       | 深圳产业链企业数                                                       |
| 决策清单中的编号  | （空）                                                            |
| 域         | 产业链                                                            |
| 模块        | CHAIN-SZ                                                       |
| 模块说明      | 产业链分析 / 深圳                                                     |
| 专题维度Owner | 李伟                                                             |
| 算法类型      | STAT                                                           |
| 合同集合      | F∩L                                                            |
| 差集判定      | mapped                                                         |
| 语义层开发阶段   | 未标                                                             |
| 验收单元      | CHAIN-SZ-PANORAMA                                              |
| 四维评估      | 已评估                                                            |
| 定义状态      | 已对齐                                                            |
| 开放项       | （空）                                                            |
| 结构支撑      | 待首评                                                            |
| 结构缺口      | （空）                                                            |
| 结构判定      | 初判                                                             |
| 源映射       | 部分缺口                                                           |
| 源缺口       | Mock 阶段可从 chain_enterprise 聚合；正式 ODS 字段级映射待 data-agent 核验      |
| 接入状态      | Mock                                                           |
| 接入阶段      | 源同步:未开始                                                        |
| 综合就绪      | 待结构设计                                                          |
| 卡点责任方     | 李伟                                                             |
| 更新频率      | daily                                                          |
| 口径摘要      | 总部在深圳且属目标产业链的企业去重数；按 headquarters_city=深圳 + chain_id 筛选 COUNT。 |
| 缺口说明      | （空）                                                            |
| 更新日期      | 2026-08-25                                                     |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **89**


| 列        | 值                                                              |
| -------- | -------------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ENTERPRISE_COUNT                                    |
| 指标名      | 深圳产业链企业数                                                       |
| 决策清单中的编号 | （空）                                                            |
| 域        | CHAIN-SZ                                                       |
| 模块       | CHAIN-SZ                                                       |
| 算法类型     | STAT                                                           |
| D1定义     | 已对齐                                                            |
| D4接入     | Mock                                                           |
| 需求来源条数   | 2                                                              |
| 需求回填     | 已回填                                                            |
| 来源系统     | 专题系统                                                           |
| 主来源分册    | 05 算法库需规                                                       |
| 主来源序号    | 95                                                             |
| 主来源名称    | 产业链基础指标模型构建                                                    |
| 主来源简述    | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链企业数。                   |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                             |
| 全部来源     | 04·35 深圳产业链企业数                                                 |
| 口径摘要     | 总部在深圳且属目标产业链的企业去重数；按 headquarters_city=深圳 + chain_id 筛选 COUNT。 |
| 更新日期     | 2026-08-25                                                     |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **95**（第 1 条）


| 列        | 值                           |
| -------- | --------------------------- |
| 指标ID     | M_CHAIN_SZ_ENTERPRISE_COUNT |
| 指标名      | 深圳产业链企业数                    |
| 决策清单中的编号 | （空）                         |
| 域        | CHAIN-SZ                    |
| 模块       | CHAIN-SZ                    |
| 分册       | 04                          |
| 分册名称     | 04 专题需规                     |
| 系统       | 专题系统                        |
| 序号       | 35                          |
| 需规名称     | 深圳产业链企业数                    |
| 简要描述     | 总部在深圳且属目标产业链的企业去重数。         |
| 需规ID     | （空）                         |
| 角色       | 页面使用                        |
| 页面       | CHAIN-TOPIC-SHENZHEN        |
| 需规文件     | （空）                         |
| 回填状态     | 已回填                         |


Sheet：`需求来源明细` · excel 行号 **96**（第 2 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ENTERPRISE_COUNT                       |
| 指标名      | 深圳产业链企业数                                          |
| 决策清单中的编号 | （空）                                               |
| 域        | CHAIN-SZ                                          |
| 模块       | CHAIN-SZ                                          |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链企业数。      |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：总部深圳且在链上的企业去重。需规 95（8）（9）。明细两行：04 seq 35 页面使用（需规文件空）+ 05·95。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT enterprise_code) WHERE headquarters_city='深圳' AND chain_id IN(:chains)`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl', 'dwd.enterprise.headquarters_city <- ods: dwd_org_reg_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 A1 挂接 + 企业库城市。Demo ADS fact 49 行，`ads_v2.py` 用合成 ext.city==深圳，非口径真源。进度表源映射=部分缺口。

**算法是否满足**：STAT 够。Demo 有样例实现，但是合成地理。

**算法缺口**：无模型缺口。去重用 credit_code（规则 10）。

**可实现**：条件是：城市 JOIN 用企业库，不用合成 ext。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：04 明细需规文件为空；地理 JOIN 未正式化；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~深圳圈定~~ **跟 A9：**`city=深圳市`**。**
2. ~~当前快照 vs 按年~~ **已拍：甲，当前一个数。**
3. ~~04 需规文件空~~ **不挡确认**，认 04 简述 + 05·95。
4. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

总部 `city=深圳市`、且挂在该链上的企业去重家数（当前快照，无年轴）。去重信用代码。不是企业+机构。

**2026-08-27 核对小结**

- **本条已确认**。YAML/GDF/Demo 合成地理债不挡确认。

---



### A11 · `M_CHAIN_SZ_ENTERPRISE_RATIO` · 深圳产业链企业占比（已确认）

**指标描述**：深圳产业链关联企业数占全国该产业链企业总数比例；直接聚合计算。

> 2026-08-27 `human:李伟`：**确认**。分母 = **当前**链上企业去重（甲），与 A10 同一窗口。不拿 A1 按年存量做分母。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **99**


| 列         | 值                               |
| --------- | ------------------------------- |
| 指标ID      | M_CHAIN_SZ_ENTERPRISE_RATIO     |
| 指标名       | 深圳产业链企业占比                       |
| 决策清单中的编号  | （空）                             |
| 域         | 产业链                             |
| 模块        | CHAIN-SZ                        |
| 模块说明      | 产业链分析 / 深圳                      |
| 专题维度Owner | 李伟                              |
| 算法类型      | STAT                            |
| 合同集合      | F∩L                             |
| 差集判定      | mapped                          |
| 语义层开发阶段   | 未标                              |
| 验收单元      | CHAIN-SZ-ADVANTAGE              |
| 四维评估      | 已评估                             |
| 定义状态      | 已对齐                             |
| 开放项       | （空）                             |
| 结构支撑      | 待首评                             |
| 结构缺口      | （空）                             |
| 结构判定      | 初判                              |
| 源映射       | 部分缺口                            |
| 源缺口       | 派生自深圳企业数/全国企业数                  |
| 接入状态      | Mock                            |
| 接入阶段      | 源同步:未开始                         |
| 综合就绪      | 待结构设计                           |
| 卡点责任方     | 李伟                              |
| 更新频率      | daily                           |
| 口径摘要      | 深圳产业链关联企业数占全国该产业链企业总数比例；直接聚合计算。 |
| 缺口说明      | （空）                             |
| 更新日期      | 2026-08-25                      |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **90**


| 列        | 值                                             |
| -------- | --------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ENTERPRISE_RATIO                   |
| 指标名      | 深圳企业份额                                        |
| 决策清单中的编号 | （空）                                           |
| 域        | CHAIN-SZ                                      |
| 模块       | CHAIN-SZ                                      |
| 算法类型     | STAT                                          |
| D1定义     | 已对齐                                           |
| D4接入     | Mock                                          |
| 需求来源条数   | 1                                             |
| 需求回填     | 已回填                                           |
| 来源系统     | 专题系统                                          |
| 主来源分册    | 05 算法库需规                                      |
| 主来源序号    | 95                                            |
| 主来源名称    | 产业链基础指标模型构建                                   |
| 主来源简述    | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链企业占比。 |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                            |
| 全部来源     | 05·95 产业链基础指标模型构建                             |
| 口径摘要     | 深圳产业链关联企业数占全国该产业链企业总数比例；直接聚合计算。               |
| 更新日期     | 2026-08-25                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **97**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ENTERPRISE_RATIO                       |
| 指标名      | 深圳企业份额                                            |
| 决策清单中的编号 | （空）                                               |
| 域        | CHAIN-SZ                                          |
| 模块       | CHAIN-SZ                                          |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链企业占比。     |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：深圳企业数 / 全国该链企业数。派生 STAT。

**MCP/seed**：type=`STAT`；formula=`M_CHAIN_SZ_ENTERPRISE_COUNT / M_CHAIN_ENTERPRISE_COUNT * 100`；definition 与进度表口径对照见上。source_tables=['派生自 M_CHAIN_SZ_ENTERPRISE_COUNT, M_CHAIN_ENTERPRISE_COUNT']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：依赖 A1/A10 两个计数。ADS 本 ID 0。

**算法是否满足**：除法 STAT 够。

**算法缺口**：无独立模型。分母是否含机构未写，默认仅企业（跟 xlsx）。

**可实现**：条件是：A1 与 A10 可算之后直接派生。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：上游计数未正式落地；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~分母窗口~~ **已拍：甲**，当前链上企业去重，不与 A1 按年相除。
2. ~~对象/深圳圈定~~ **跟 A10/A9。**
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

`A10（city=深圳市 当前企业） / 当前链上企业去重 × 100`。YAML 写的 `A10/A1` 作废。

**2026-08-27 核对小结**

- **本条已确认**。上游 A1/A10 实现债不挡确认。

---



### A12 · `M_CHAIN_SZ_INSTITUTION_COUNT` · 深圳产业链机构数（已确认）

**指标描述**：总部在深圳且属目标产业链的科研机构/高校去重数；口径同 M_CHAIN_SZ_ENTERPRISE_COUNT 加 org_type=机构。

> 2026-08-27 `human:李伟`：**确认**。跟 **A3 乙** + **A10 甲**（当前一个数）+ `city=深圳市`。xlsx/YAML 的 `org_type=机构` 作废。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **146**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_INSTITUTION_COUNT                                           |
| 指标名       | 深圳产业链机构数                                                               |
| 决策清单中的编号  | （空）                                                                    |
| 域         | 产业链                                                                    |
| 模块        | E2 产业链（待四维评估）                                                          |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 未标                                                                     |
| 验收单元      | —                                                                      |
| 四维评估      | 待评估                                                                    |
| 定义状态      | 已对齐                                                                    |
| 开放项       | （空）                                                                    |
| 结构支撑      | 待评估                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | —                                                                      |
| 源映射       | 齐备                                                                     |
| 源缺口       | （空）                                                                    |
| 接入状态      | Mock                                                                   |
| 接入阶段      | （空）                                                                    |
| 综合就绪      | 待接入（Mock）                                                              |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | daily                                                                  |
| 口径摘要      | 总部在深圳且属目标产业链的科研机构/高校去重数；口径同 M_CHAIN_SZ_ENTERPRISE_COUNT 加 org_type=机构。 |
| 缺口说明      | （空）                                                                    |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **91**


| 列        | 值                                                                      |
| -------- | ---------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_INSTITUTION_COUNT                                           |
| 指标名      | 深圳产业链机构数                                                               |
| 决策清单中的编号 | （空）                                                                    |
| 域        | 产业链                                                                    |
| 模块       | CHAIN                                                                  |
| 算法类型     | STAT                                                                   |
| D1定义     | —                                                                      |
| D4接入     | —                                                                      |
| 需求来源条数   | 1                                                                      |
| 需求回填     | 已回填                                                                    |
| 来源系统     | 专题系统                                                                   |
| 主来源分册    | 05 算法库需规                                                               |
| 主来源序号    | 95                                                                     |
| 主来源名称    | 产业链基础指标模型构建                                                            |
| 主来源简述    | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链机构数。                           |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                     |
| 全部来源     | 05·95 产业链基础指标模型构建                                                      |
| 口径摘要     | 总部在深圳且属目标产业链的科研机构/高校去重数；口径同 M_CHAIN_SZ_ENTERPRISE_COUNT 加 org_type=机构。 |
| 更新日期     | 2026-08-25                                                             |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **98**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_INSTITUTION_COUNT                      |
| 指标名      | 深圳产业链机构数                                          |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-TOPIC-SHENZHEN 复用算法库叶。本指标：深圳产业链机构数。      |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：总部深圳 + 机构。同 A3 + 深圳切片。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT enterprise_name) WHERE headquarters_city='深圳' AND org_type='机构'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 A3：tags 无 org_type。Demo 0。

**算法是否满足**：STAT 够。机构集合未定则算不出。

**算法缺口**：无模型缺口。机构挂接同 A3 特有问题。

**可实现**：条件是：A3 机构源拍板 + 深圳地理 JOIN。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：机构挂接未定；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~结构跟已拍~~ **已拍：A3 乙 + A10 甲 +** `city=深圳市`**。**
2. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

`city=深圳市`、且挂在该链上的 **A3 乙机构**去重数（当前快照，无年轴）。去重机构代码。不用 `org_type=机构`。

**2026-08-27 核对小结**

- **本条已确认**。xlsx/YAML `org_type=机构` / `city=深圳` / 按名去重作废。机构边/GDF/矩阵债不挡确认。

---



### A13 · `M_CHAIN_TOTAL_COUNT` · 产业链总数（已确认）

**指标描述**：纳入要素库的产业链去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain 全量，按 chain_id 去重。

> 2026-08-27 `human:李伟`：**确认**。全库 `COUNT(DISTINCT chain_id)`。05·117 只作需规挂靠，不是全景模型本体。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **149**


| 列         | 值                                                                                                                             |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_TOTAL_COUNT                                                                                                           |
| 指标名       | 产业链总数                                                                                                                         |
| 决策清单中的编号  | （空）                                                                                                                           |
| 域         | 产业链                                                                                                                           |
| 模块        | E2 产业链（待四维评估）                                                                                                                 |
| 模块说明      | 产业链                                                                                                                           |
| 专题维度Owner | 李伟                                                                                                                            |
| 算法类型      | STAT                                                                                                                          |
| 合同集合      | F∩L                                                                                                                           |
| 差集判定      | mapped                                                                                                                        |
| 语义层开发阶段   | 未标                                                                                                                            |
| 验收单元      | —                                                                                                                             |
| 四维评估      | 待评估                                                                                                                           |
| 定义状态      | 已对齐                                                                                                                           |
| 开放项       | （空）                                                                                                                           |
| 结构支撑      | 待评估                                                                                                                           |
| 结构缺口      | （空）                                                                                                                           |
| 结构判定      | —                                                                                                                             |
| 源映射       | 待评估                                                                                                                           |
| 源缺口       | （空）                                                                                                                           |
| 接入状态      | Mock                                                                                                                          |
| 接入阶段      | （空）                                                                                                                           |
| 综合就绪      | 待结构设计                                                                                                                         |
| 卡点责任方     | 李伟                                                                                                                            |
| 更新频率      | daily                                                                                                                         |
| 口径摘要      | 纳入要素库的产业链去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain 全量，按 chain_id 去重。                                                           |
| 缺口说明      | 产业链总数=纳入要素库的产业链去重总数，按 chain_id 去重。数据源可用但 formula 待 algorithm-agent 统一从 ads:chain_panorama 或 dwd:industry_chain 聚合。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                                                                    |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **103**


| 列        | 值                                                                   |
| -------- | ------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_TOTAL_COUNT                                                 |
| 指标名      | 产业链总数                                                               |
| 决策清单中的编号 | （空）                                                                 |
| 域        | 产业链                                                                 |
| 模块       | CHAIN                                                               |
| 算法类型     | STAT                                                                |
| D1定义     | —                                                                   |
| D4接入     | —                                                                   |
| 需求来源条数   | 1                                                                   |
| 需求回填     | 已回填                                                                 |
| 来源系统     | 专题系统                                                                |
| 主来源分册    | 05 算法库需规                                                            |
| 主来源序号    | 117                                                                 |
| 主来源名称    | 产业链全景模型构建                                                           |
| 主来源简述    | 产业链 / 深度分析：产业链全景模型构建                                                |
| 主来源需规ID  | ALGO-CHAIN-DEEP-117                                                 |
| 全部来源     | 05·117 产业链全景模型构建                                                    |
| 口径摘要     | 纳入要素库的产业链去重总数；统计窗口为最新批次快照，对象范围 dwd.industry_chain 全量，按 chain_id 去重。 |
| 更新日期     | 2026-08-25                                                          |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **111**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_TOTAL_COUNT                               |
| 指标名      | 产业链总数                                             |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 117                                               |
| 需规名称     | 产业链全景模型构建                                         |
| 简要描述     | 产业链 / 深度分析：产业链全景模型构建                              |
| 需规ID     | ALGO-CHAIN-DEEP-117                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-PANORAMA                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：要素库产业链按 chain_id 去重总数。需求 05·117 全景模型（深度分析.md）。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT dwd.industry_chain.chain_id)`；definition 与进度表口径对照见上。source_tables=['ads: chain_panorama', 'dwd.industry_chain <- ods: dwd_industry_chain_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：DWD 现行 `industry_chain`（Demo 未删 49 行）。ADS 本 ID 0。117 是全景模型，本指标只是链条数 STAT。

**算法是否满足**：作为 STAT 链条数：够。作为 117 全景模型：不够（MODEL/GRAPH 归唐绍祖）。

**算法缺口**：若只交链条数则无算法缺口。若要交 117 全景则越界本叶。

**可实现**：STAT 链条数：条件是（可落）。全景模型：本叶否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：指标身份把 117 模型缩成一条 STAT；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~全库链条数 vs 117 全景壳~~ **已拍：全库链条数。** 117 只作需规挂靠。
2. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

要素库最新批次快照，`COUNT(DISTINCT chain_id)`（全库链条数，不是单链上下文，也不是 117 全景模型本体）。

**2026-08-27 核对小结**

- **本条已确认**。矩阵/ADS/Wave0 mock 债不挡确认。MODEL/GRAPH 不进本 ID。

---



### A14 · `M_CHAIN_BASE_95_1` · 产业链基础指标模型构建（已确认）

**指标描述**：产业链基础指标模型构建：对应算法库 SRS ALGO-CHAIN-BASE-95，统计窗口与对象范围以需规文本为准。

> 2026-08-27 `human:李伟`：**确认（封面）**。不是可算 KPI。IMPL 剔除、不进 ADS；seed 只留需求追溯。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **53**


| 列         | 值                                                          |
| --------- | ---------------------------------------------------------- |
| 指标ID      | M_CHAIN_BASE_95_1                                          |
| 指标名       | 产业链基础指标模型构建                                                |
| 决策清单中的编号  | （空）                                                        |
| 域         | 产业链                                                        |
| 模块        | CHAIN                                                      |
| 模块说明      | 产业链                                                        |
| 专题维度Owner | 李伟                                                         |
| 算法类型      | STAT                                                       |
| 合同集合      | L−F                                                        |
| 差集判定      | 未挂页                                                        |
| 语义层开发阶段   | 定义中                                                        |
| 验收单元      | ALGO-CHAIN-BASE-95                                         |
| 四维评估      | 已评估                                                        |
| 定义状态      | 草案                                                         |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                     |
| 结构支撑      | 待首评                                                        |
| 结构缺口      | （空）                                                        |
| 结构判定      | 初判                                                         |
| 源映射       | 待ODS                                                       |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。         |
| 接入状态      | Mock                                                       |
| 接入阶段      | 源同步:未开始                                                    |
| 综合就绪      | 待口径确认                                                      |
| 卡点责任方     | 李伟                                                         |
| 更新频率      | pending                                                    |
| 口径摘要      | 产业链基础指标模型构建：对应算法库 SRS ALGO-CHAIN-BASE-95，统计窗口与对象范围以需规文本为准。 |
| 缺口说明      | （空）                                                        |
| 更新日期      | 2026-08-25                                                 |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **9**


| 列        | 值                                                                                                  |
| -------- | -------------------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_BASE_95_1                                                                                  |
| 指标名      | 产业链基础指标模型构建                                                                                        |
| 决策清单中的编号 | （空）                                                                                                |
| 域        | 产业链                                                                                                |
| 模块       | CHAIN                                                                                              |
| 算法类型     | STAT                                                                                               |
| D1定义     | 草案                                                                                                 |
| D4接入     | Mock                                                                                               |
| 需求来源条数   | 1                                                                                                  |
| 需求回填     | 已回填                                                                                                |
| 来源系统     | 算法库                                                                                                |
| 主来源分册    | 05 算法库需规                                                                                           |
| 主来源序号    | 95                                                                                                 |
| 主来源名称    | 产业链基础指标模型构建                                                                                        |
| 主来源简述    | 需支持产业指标体系构建、指标体系分析模型及工具，提供产业链基础指标、技术基础指标、企业基础指标、人才基础指标、科研机构基础指标、政策基础指标、服务机构基础指标等… 本指标：产业链基础指标模型构建。 |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                                                 |
| 全部来源     | 05·95 产业链基础指标模型构建                                                                                  |
| 口径摘要     | 产业链基础指标模型构建：对应算法库 SRS ALGO-CHAIN-BASE-95，统计窗口与对象范围以需规文本为准。                                         |
| 更新日期     | 2026-08-25                                                                                         |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **9**（第 1 条）


| 列        | 值                                                                                                  |
| -------- | -------------------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_BASE_95_1                                                                                  |
| 指标名      | 产业链基础指标模型构建                                                                                        |
| 决策清单中的编号 | （空）                                                                                                |
| 域        | 产业链                                                                                                |
| 模块       | CHAIN                                                                                              |
| 分册       | 05                                                                                                 |
| 分册名称     | 05 算法库需规                                                                                           |
| 系统       | 算法库                                                                                                |
| 序号       | 95                                                                                                 |
| 需规名称     | 产业链基础指标模型构建                                                                                        |
| 简要描述     | 需支持产业指标体系构建、指标体系分析模型及工具，提供产业链基础指标、技术基础指标、企业基础指标、人才基础指标、科研机构基础指标、政策基础指标、服务机构基础指标等… 本指标：产业链基础指标模型构建。 |
| 需规ID     | ALGO-CHAIN-BASE-95                                                                                 |
| 角色       | 算法库叶                                                                                               |
| 页面       | （空）                                                                                                |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md                                                  |
| 回填状态     | 已回填                                                                                                |




#### 4) 结合分析

**口径一句**：xlsx：对应 ALGO-CHAIN-BASE-95 整包，窗口以需规文本为准。D1=草案。页面空。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：不是单点 KPI，是九维能力包封面。

**算法是否满足**：不能当作一条 STAT 落地。九维已拆到 A/B 各 ID。

**算法缺口**：无独立公式。保留则与 95 下各指标重复。

**可实现**：否（不应单算）。建议正式化时作废或改为需求包封面、不进 ADS。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：D1 草案；无页面；与已拆指标重复。

**需要李伟确认的问题（仅特有）**

1. ~~身份~~ **已拍：封面**（05·95 文件夹，不单算）。
2. ~~IMPL 剔除~~ **已拍：剔除实现清单，不进 ADS**；seed 留追溯。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

不是数字。九维已拆到 A1–A13 / B 组各 ID；本 ID 只作 95 需求包封面。

**2026-08-27 核对小结**

- **本条已确认**。后续同类叶子同名占位跟本条，不重问。

---



### B15 · `M_CHAIN_MARKET_SIZE` · 市场规模（已确认）

**指标描述**：产业链下全部关联企业的年报营收合计（仅企业，不计机构/人才等）；单位默认亿元（展示换算在 ADS）。统计年与 ENT 年报字段对齐。非 ODS 直灌、非外购市调默认口径。

> 2026-08-27 `human:李伟`：**确认**。口径跟 QC06：链上企业年报营收加总（只企业）。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：algo_demo.py, read_v2.py。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **130**


| 列         | 值                                                                                                                                       |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_MARKET_SIZE                                                                                                                     |
| 指标名       | 市场规模                                                                                                                                    |
| 决策清单中的编号  | QC06                                                                                                                                    |
| 域         | 产业链                                                                                                                                     |
| 模块        | E2 产业链（待四维评估）                                                                                                                           |
| 模块说明      | 产业链                                                                                                                                     |
| 专题维度Owner | 李伟                                                                                                                                      |
| 算法类型      | STAT                                                                                                                                    |
| 合同集合      | F∩L                                                                                                                                     |
| 差集判定      | mapped                                                                                                                                  |
| 语义层开发阶段   | 未标                                                                                                                                      |
| 验收单元      | —                                                                                                                                       |
| 四维评估      | 待评估                                                                                                                                     |
| 定义状态      | 草案                                                                                                                                      |
| 开放项       | QC06                                                                                                                                    |
| 结构支撑      | 待评估                                                                                                                                     |
| 结构缺口      | （空）                                                                                                                                     |
| 结构判定      | —                                                                                                                                       |
| 源映射       | 待评估                                                                                                                                     |
| 源缺口       | （空）                                                                                                                                     |
| 接入状态      | Mock                                                                                                                                    |
| 接入阶段      | （空）                                                                                                                                     |
| 综合就绪      | 待口径确认                                                                                                                                   |
| 卡点责任方     | 李伟                                                                                                                                      |
| 更新频率      | yearly                                                                                                                                  |
| 口径摘要      | 产业链下全部关联企业的年报营收合计（仅企业，不计机构/人才等）；单位默认亿元（展示换算在 ADS）。统计年与 ENT 年报字段对齐。非 ODS 直灌、非外购市调默认口径。                                                   |
| 缺口说明      | 产业链市场规模=链下全部关联企业年报营收合计（仅企业，不计机构/人才）。非 ODS 直灌，需跨 ENT 域聚合后落 ADS。ENT 年报字段名与统计年细节待与 ENT/数据 Lead 对齐后冻结(QC06)。计算方式已架构确认(2026-08-07 human:李伟)。 |
| 更新日期      | 2026-08-25                                                                                                                              |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **55**


| 列        | 值                                                                                     |
| -------- | ------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_MARKET_SIZE                                                                   |
| 指标名      | 市场规模                                                                                  |
| 决策清单中的编号 | QC06                                                                                  |
| 域        | 产业链                                                                                   |
| 模块       | CHAIN                                                                                 |
| 算法类型     | STAT                                                                                  |
| D1定义     | —                                                                                     |
| D4接入     | —                                                                                     |
| 需求来源条数   | 1                                                                                     |
| 需求回填     | 已回填                                                                                   |
| 来源系统     | 展示+专题                                                                                 |
| 主来源分册    | 05 算法库需规                                                                              |
| 主来源序号    | 95                                                                                    |
| 主来源名称    | 产业链基础指标模型构建                                                                           |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：市场规模。                                             |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                                                    |
| 全部来源     | 05·95 产业链基础指标模型构建                                                                     |
| 口径摘要     | 产业链下全部关联企业的年报营收合计（仅企业，不计机构/人才等）；单位默认亿元（展示换算在 ADS）。统计年与 ENT 年报字段对齐。非 ODS 直灌、非外购市调默认口径。 |
| 更新日期     | 2026-08-25                                                                            |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **58**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_MARKET_SIZE                               |
| 指标名      | 市场规模                                              |
| 决策清单中的编号 | QC06                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示+专题                                             |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：市场规模。         |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW, CHAIN-TOPIC-PANORAMA       |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx/缺口说明：链下全部关联企业年报营收合计（仅企业）。QC06 已有李伟 2026-08-07 默认此口径。需规 95（1）写对接产业库销售额，与「年报营收加总」部分打架，以已拍 QC06 为准。

**MCP/seed**：type=`STAT`；formula=`SUM(ent_annual_revenue) WHERE enterprise_code IN (SELECT entity_id FROM industry_chain_entity_rel WHERE chain_id=:chain_id AND entity_type='enterprise' AND valid_to IS NULL AND is_deleted=0) AND fiscal_year=:stat_year`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_entity_rel', 'ENT域企业年报营收表（字段名与 ENT DWD 对齐后冻结）']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：挂接 tags + 企业库年报 `dwd_org_annual_financial_info`（非产业链四表直灌）。ADS 0。代码有引用但 fact 空。

**算法是否满足**：STAT SUM 够。

**算法缺口**：无模型缺口。年报字段名/统计年 Mapping（缺口说明已标待与 ENT 对齐）。

**可实现**：条件是：挂接×年报 JOIN、统计年冻结。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：年报字段未冻；GDF 跨域作业未派；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~计算方式~~ **已拍：QC06**（年报营收加总，只企业）。
2. ~~字段/统计年~~ **不挡确认**，跟 ENT Lead。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

链上企业（`entity_type=enterprise`）年报营收 SUM；单位亿元在 ADS 换算。不含机构。不是市调、不是 ODS 直灌。

**2026-08-27 核对小结**

- **本条已确认**。GDF/年报字段/矩阵债不挡确认。

---



### B16 · `M_CHAIN_MARKET_GROWTH` · 市场增长率（已确认）

**指标描述**：产业链市场规模同比增长率；依赖 M_CHAIN_MARKET_SIZE 相邻两年计算结果。

> 2026-08-27 `human:李伟`：**确认**。同比，不是环比。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **129**


| 列         | 值                                                                                                     |
| --------- | ----------------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_MARKET_GROWTH                                                                                 |
| 指标名       | 市场增长率                                                                                                 |
| 决策清单中的编号  | QC06                                                                                                  |
| 域         | 产业链                                                                                                   |
| 模块        | E2 产业链（待四维评估）                                                                                         |
| 模块说明      | 产业链                                                                                                   |
| 专题维度Owner | 李伟                                                                                                    |
| 算法类型      | STAT                                                                                                  |
| 合同集合      | F∩L                                                                                                   |
| 差集判定      | mapped                                                                                                |
| 语义层开发阶段   | 未标                                                                                                    |
| 验收单元      | —                                                                                                     |
| 四维评估      | 待评估                                                                                                   |
| 定义状态      | 草案                                                                                                    |
| 开放项       | QC06                                                                                                  |
| 结构支撑      | 待评估                                                                                                   |
| 结构缺口      | （空）                                                                                                   |
| 结构判定      | —                                                                                                     |
| 源映射       | 待评估                                                                                                   |
| 源缺口       | （空）                                                                                                   |
| 接入状态      | Mock                                                                                                  |
| 接入阶段      | （空）                                                                                                   |
| 综合就绪      | 待口径确认                                                                                                 |
| 卡点责任方     | 李伟                                                                                                    |
| 更新频率      | yearly                                                                                                |
| 口径摘要      | 产业链市场规模同比增长率；依赖 M_CHAIN_MARKET_SIZE 相邻两年计算结果。                                                         |
| 缺口说明      | 市场增长率依赖相邻两年 M_CHAIN_MARKET_SIZE 计算结果。(当年规模-上年规模)/上年规模*100。若某年数据缺失则增长率无法计算。QC06 ENT 年报字段冻结前仅展示 mock 值。 |
| 更新日期      | 2026-08-25                                                                                            |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **54**


| 列        | 值                                             |
| -------- | --------------------------------------------- |
| 指标ID     | M_CHAIN_MARKET_GROWTH                         |
| 指标名      | 市场增长率                                         |
| 决策清单中的编号 | QC06                                          |
| 域        | 产业链                                           |
| 模块       | CHAIN                                         |
| 算法类型     | STAT                                          |
| D1定义     | —                                             |
| D4接入     | —                                             |
| 需求来源条数   | 1                                             |
| 需求回填     | 已回填                                           |
| 来源系统     | 展示系统                                          |
| 主来源分册    | 05 算法库需规                                      |
| 主来源序号    | 95                                            |
| 主来源名称    | 产业链基础指标模型构建                                   |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：市场增长率。    |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                            |
| 全部来源     | 05·95 产业链基础指标模型构建                             |
| 口径摘要     | 产业链市场规模同比增长率；依赖 M_CHAIN_MARKET_SIZE 相邻两年计算结果。 |
| 更新日期     | 2026-08-25                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **57**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_MARKET_GROWTH                             |
| 指标名      | 市场增长率                                             |
| 决策清单中的编号 | QC06                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：市场增长率。        |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：市场规模同比。(当年-上年)/上年。依赖 B15。

**MCP/seed**：type=`STAT`；formula=`(M_CHAIN_MARKET_SIZE(y)-M_CHAIN_MARKET_SIZE(y-1))/NULLIF(M_CHAIN_MARKET_SIZE(y-1),0)*100`；definition 与进度表口径对照见上。source_tables=['ADS/指标引擎基于 M_CHAIN_MARKET_SIZE']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 B15。ADS 0。

**算法是否满足**：环比/同比 STAT 够。

**算法缺口**：无独立模型。缺上年则空，不伪造。

**可实现**：条件是：B15 至少两年可算。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：同 B15。

**需要李伟确认的问题（仅特有）**

1. ~~分子~~ **跟 B15。**
2. ~~同比 vs 环比~~ **已拍：同比。**
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

`(B15(y) − B15(y−1)) / B15(y−1) × 100`。上年缺失则空。

**2026-08-27 核对小结**

- **本条已确认**。上游年报 Mapping 债不挡确认。

---



### B17 · `M_CHAIN_INVEST_COUNT` · 投融资事件数（已确认）

**指标描述**：pending_data_lead(QC07)：产业链相关投融资事件去重计数；数据源同 M_CHAIN_INVEST_TOTAL。

> 2026-08-27 `human:李伟`：**确认**。跟 DWD：`dwd_org_financing_info` × 挂接，COUNT 事件。不用资讯表。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=False。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **125**


| 列         | 值                                                                                           |
| --------- | ------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_INVEST_COUNT                                                                        |
| 指标名       | 投融资事件数                                                                                      |
| 决策清单中的编号  | QC07                                                                                        |
| 域         | 产业链                                                                                         |
| 模块        | E2 产业链（待四维评估）                                                                               |
| 模块说明      | 产业链                                                                                         |
| 专题维度Owner | 李伟                                                                                          |
| 算法类型      | STAT                                                                                        |
| 合同集合      | 未分拣                                                                                         |
| 差集判定      | third_party                                                                                 |
| 语义层开发阶段   | 未标                                                                                          |
| 验收单元      | —                                                                                           |
| 四维评估      | 待评估                                                                                         |
| 定义状态      | 草案                                                                                          |
| 开放项       | QC07                                                                                        |
| 结构支撑      | 待评估                                                                                         |
| 结构缺口      | （空）                                                                                         |
| 结构判定      | —                                                                                           |
| 源映射       | 待评估                                                                                         |
| 源缺口       | （空）                                                                                         |
| 接入状态      | Mock                                                                                        |
| 接入阶段      | （空）                                                                                         |
| 综合就绪      | 待口径确认                                                                                       |
| 卡点责任方     | 李伟                                                                                          |
| 更新频率      | weekly                                                                                      |
| 口径摘要      | pending_data_lead(QC07)：产业链相关投融资事件去重计数；数据源同 M_CHAIN_INVEST_TOTAL。                           |
| 缺口说明      | 投融资事件数与 INVEST_TOTAL 同源，当前 ODS 投融资表为空(Q054)。需甲方确认投融资数据来源后(QC07)方可正式展示。Wave0 该指标置灰显示「数据筹备中」。 |
| 更新日期      | 2026-08-25                                                                                  |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **48**


| 列        | 值                                                                 |
| -------- | ----------------------------------------------------------------- |
| 指标ID     | M_CHAIN_INVEST_COUNT                                              |
| 指标名      | 投融资事件数                                                            |
| 决策清单中的编号 | QC07                                                              |
| 域        | 产业链                                                               |
| 模块       | CHAIN                                                             |
| 算法类型     | STAT                                                              |
| D1定义     | —                                                                 |
| D4接入     | —                                                                 |
| 需求来源条数   | 0                                                                 |
| 需求回填     | 未回填                                                               |
| 来源系统     | （空）                                                               |
| 主来源分册    | （空）                                                               |
| 主来源序号    | （空）                                                               |
| 主来源名称    | （空）                                                               |
| 主来源简述    | （空）                                                               |
| 主来源需规ID  | （空）                                                               |
| 全部来源     | （空）                                                               |
| 口径摘要     | pending_data_lead(QC07)：产业链相关投融资事件去重计数；数据源同 M_CHAIN_INVEST_TOTAL。 |
| 更新日期     | 2026-08-25                                                        |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **51**（第 1 条）


| 列        | 值                    |
| -------- | -------------------- |
| 指标ID     | M_CHAIN_INVEST_COUNT |
| 指标名      | 投融资事件数               |
| 决策清单中的编号 | QC07                 |
| 域        | 产业链                  |
| 模块       | CHAIN                |
| 分册       | （空）                  |
| 分册名称     | （空）                  |
| 系统       | （空）                  |
| 序号       | （空）                  |
| 需规名称     | （空）                  |
| 简要描述     | （空）                  |
| 需规ID     | （空）                  |
| 角色       | （空）                  |
| 页面       | （空）                  |
| 需规文件     | （空）                  |
| 回填状态     | 未回填                  |




#### 4) 结合分析

**口径一句**：xlsx：投融资事件去重，数据源同 INVEST_TOTAL；QC07/Q054。需求来源目录/明细本 ID 各列均为（空）（未回填）。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT news_id) WHERE news_type='financing'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_news <- ods: dwd_industry_chain_news_info(融资类)']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：正式 ODS `dwd_org_financing_info`（Q054 空表叙事仍在流图）。Demo 投资事件为合成 mock，ADS 本 ID 0。

**算法是否满足**：事件 COUNT DISTINCT 是 STAT，够。

**算法缺口**：无模型缺口。缺事件源表有效行/采购确认（QC07）。

**可实现**：否（源未确认且正式表空）。Demo mock 不当 live。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：GDF 跨域作业/现网行数核验；需求来源未回填；矩阵缺失。不是「没有融资表」。

**需要李伟确认的问题（仅特有）**

1. ~~资讯表~~ **不作源。**
2. ~~DWD 路径~~ **已拍：**`dwd_org_financing_info` **× 挂接。**
3. ~~确认/挂起~~ **已拍：确认。** QC07/Q054 旧叙事不挡口径。

**口径一句（已确认）**

链上企业融资事件去重 COUNT。源 = 金融要素库 `dwd_org_financing_info`（企业域 `enterprise_financing` 同表），挂链 `entity_rel`/tags。金额合计不在本 ID。

**2026-08-27 核对小结**

- **本条已确认**。行数/GDF 债不挡确认。

---



### B18 · `M_CHAIN_REG_FINANCING` · 融资事件（已确认）

**指标描述**：区域内产业相关融资事件 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-27 `human:李伟`：**确认（最优解）**。B17 × 评价区域切片 COUNT。保留叶子，不倒灌招标。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **77**


| 列         | 值                                                                        |
| --------- | ------------------------------------------------------------------------ |
| 指标ID      | M_CHAIN_REG_FINANCING                                                    |
| 指标名       | 融资事件                                                                     |
| 决策清单中的编号  | （空）                                                                      |
| 域         | 产业链                                                                      |
| 模块        | CHAIN                                                                    |
| 模块说明      | 产业链                                                                      |
| 专题维度Owner | 李伟                                                                       |
| 算法类型      | STAT                                                                     |
| 合同集合      | F∩L                                                                      |
| 差集判定      | mapped                                                                   |
| 语义层开发阶段   | 定义中                                                                      |
| 验收单元      | TOPIC-REG-011                                                            |
| 四维评估      | 已评估                                                                      |
| 定义状态      | 草案                                                                       |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                   |
| 结构支撑      | 待首评                                                                      |
| 结构缺口      | （空）                                                                      |
| 结构判定      | 初判                                                                       |
| 源映射       | 待ODS                                                                     |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                       |
| 接入状态      | Mock                                                                     |
| 接入阶段      | 源同步:未开始                                                                  |
| 综合就绪      | 待口径确认                                                                    |
| 卡点责任方     | 李伟                                                                       |
| 更新频率      | pending                                                                  |
| 口径摘要      | 区域内产业相关融资事件 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                      |
| 更新日期      | 2026-08-25                                                               |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **71**


| 列        | 值                                                                        |
| -------- | ------------------------------------------------------------------------ |
| 指标ID     | M_CHAIN_REG_FINANCING                                                    |
| 指标名      | 融资事件                                                                     |
| 决策清单中的编号 | （空）                                                                      |
| 域        | 产业链                                                                      |
| 模块       | CHAIN                                                                    |
| 算法类型     | STAT                                                                     |
| D1定义     | 草案                                                                       |
| D4接入     | Mock                                                                     |
| 需求来源条数   | 1                                                                        |
| 需求回填     | 已回填                                                                      |
| 来源系统     | 专题系统                                                                     |
| 主来源分册    | 05 算法库需规                                                                 |
| 主来源序号    | 126                                                                      |
| 主来源名称    | 区域产业指数模型                                                                 |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                      |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                      |
| 全部来源     | 05·126 区域产业指数模型                                                          |
| 口径摘要     | 区域内产业相关融资事件 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                               |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **75**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_FINANCING                             |
| 指标名      | 融资事件                                              |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内融资事件。公式未签。需求 05·126 区域产业指数模型。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：区域指数是 MODEL；本条若只计区域内事件则 STAT。投融资源同 B17。

**算法是否满足**：事件计数 STAT 够；指数模型不够（越界 126）。

**算法缺口**：无独立模型。源债跟 B17。

**可实现**：条件是：B17 可算 + 企业地理对上评价 `region_codes`。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：GDF/行数同 B17；QC11 维度名仍 🟡（不挡本条）。

**需要李伟确认的问题（仅特有）**

1. ~~最优解~~ **已拍。**
2. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

B17 融资事件，按本次评价 `region_codes` 切企业地理后 COUNT。不是 126 模型，不是金额。门户全链 COUNT 不得直接顶替。

**2026-08-27 核对小结**

- **本条已确认**。QC11/QC05 不挡叶子口径。

---



### B19 · `M_CHAIN_REG_REVENUE` · 营收（已确认）

**指标描述**：区域内相关企业营收规模 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-27 `human:李伟`：**确认（最优解）**。B15 × 评价区域切片。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **82**


| 列         | 值                                                                        |
| --------- | ------------------------------------------------------------------------ |
| 指标ID      | M_CHAIN_REG_REVENUE                                                      |
| 指标名       | 营收                                                                       |
| 决策清单中的编号  | （空）                                                                      |
| 域         | 产业链                                                                      |
| 模块        | CHAIN                                                                    |
| 模块说明      | 产业链                                                                      |
| 专题维度Owner | 李伟                                                                       |
| 算法类型      | STAT                                                                     |
| 合同集合      | F∩L                                                                      |
| 差集判定      | mapped                                                                   |
| 语义层开发阶段   | 定义中                                                                      |
| 验收单元      | TOPIC-REG-010                                                            |
| 四维评估      | 已评估                                                                      |
| 定义状态      | 草案                                                                       |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                   |
| 结构支撑      | 待首评                                                                      |
| 结构缺口      | （空）                                                                      |
| 结构判定      | 初判                                                                       |
| 源映射       | 待ODS                                                                     |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                       |
| 接入状态      | Mock                                                                     |
| 接入阶段      | 源同步:未开始                                                                  |
| 综合就绪      | 待口径确认                                                                    |
| 卡点责任方     | 李伟                                                                       |
| 更新频率      | pending                                                                  |
| 口径摘要      | 区域内相关企业营收规模 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                      |
| 更新日期      | 2026-08-25                                                               |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **76**


| 列        | 值                                                                        |
| -------- | ------------------------------------------------------------------------ |
| 指标ID     | M_CHAIN_REG_REVENUE                                                      |
| 指标名      | 营收                                                                       |
| 决策清单中的编号 | （空）                                                                      |
| 域        | 产业链                                                                      |
| 模块       | CHAIN                                                                    |
| 算法类型     | STAT                                                                     |
| D1定义     | 草案                                                                       |
| D4接入     | Mock                                                                     |
| 需求来源条数   | 1                                                                        |
| 需求回填     | 已回填                                                                      |
| 来源系统     | 专题系统                                                                     |
| 主来源分册    | 05 算法库需规                                                                 |
| 主来源序号    | 126                                                                      |
| 主来源名称    | 区域产业指数模型                                                                 |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                      |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                      |
| 全部来源     | 05·126 区域产业指数模型                                                          |
| 口径摘要     | 区域内相关企业营收规模 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                               |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **80**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_REVENUE                               |
| 指标名      | 营收                                                |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内企业营收。126。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 B15 营收加总 + 区域切片。

**算法是否满足**：SUM STAT 够。

**算法缺口**：公式未签。区域切分字段同地理 JOIN。

**可实现**：条件是：B15 可算并加区域。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；年报 JOIN 未冻。

**需要李伟确认的问题（仅特有）**

1. ~~身份/最优解~~ **已拍。**
2. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

B15（QC06 年报营收加总，只企业），按本次评价 `region_codes` 切企业地理。门户 MARKET_SIZE 不得直接顶替。

**2026-08-27 核对小结**

- **本条已确认**。年报字段债跟 B15，不挡确认。

---



### B20 · `M_CHAIN_REG_PAPERS` · 高校论文（已确认）

**指标描述**：区域内高校论文产出 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-27 `human:李伟`：**确认（甲）**。论文要素库 × A3 乙高校 × 评价区域，COUNT 篇。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **78**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_PAPERS                                                     |
| 指标名       | 高校论文                                                                   |
| 决策清单中的编号  | （空）                                                                    |
| 域         | 产业链                                                                    |
| 模块        | CHAIN                                                                  |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 定义中                                                                    |
| 验收单元      | TOPIC-REG-016                                                          |
| 四维评估      | 已评估                                                                    |
| 定义状态      | 草案                                                                     |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                 |
| 结构支撑      | 待首评                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | 初判                                                                     |
| 源映射       | 待ODS                                                                   |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                     |
| 接入状态      | Mock                                                                   |
| 接入阶段      | 源同步:未开始                                                                |
| 综合就绪      | 待口径确认                                                                  |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | pending                                                                |
| 口径摘要      | 区域内高校论文产出 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                    |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **72**


| 列        | 值                                                                      |
| -------- | ---------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_PAPERS                                                     |
| 指标名      | 高校论文                                                                   |
| 决策清单中的编号 | （空）                                                                    |
| 域        | 产业链                                                                    |
| 模块       | CHAIN                                                                  |
| 算法类型     | STAT                                                                   |
| D1定义     | 草案                                                                     |
| D4接入     | Mock                                                                   |
| 需求来源条数   | 1                                                                      |
| 需求回填     | 已回填                                                                    |
| 来源系统     | 专题系统                                                                   |
| 主来源分册    | 05 算法库需规                                                               |
| 主来源序号    | 126                                                                    |
| 主来源名称    | 区域产业指数模型                                                               |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                    |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                    |
| 全部来源     | 05·126 区域产业指数模型                                                        |
| 口径摘要     | 区域内高校论文产出 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                             |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **76**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_PAPERS                                |
| 指标名      | 高校论文                                              |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内高校论文。126。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：论文在论文要素库，非产业链四表。需论文×机构×链×区域 Mapping。

**算法是否满足**：计数 STAT 够。

**算法缺口**：无模型。缺论文-链挂接规则。

**可实现**：否（挂接未定）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：跨域论文 Mapping 无；draft。

**需要李伟确认的问题（仅特有）**

1. ~~身份~~ **跟 B18。**
2. ~~挂链~~ **已拍：甲**（高校机构，不主题 NLP）。
3. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

论文要素库 × A3 乙高校 × 高校所在地 ∈ 评价 `region_codes`，COUNT 篇。

**2026-08-27 核对小结**

- **本条已确认**。论文 Mapping/GDF 债不挡确认。

---



### B21 · `M_CHAIN_REG_PATENT` · 专利（已确认）

**指标描述**：区域内产业相关专利 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-27 `human:李伟`：**确认（甲）**。`dwd_patent` × 链上企业受让人 × 评价区域，COUNT。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **79**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_PATENT                                                     |
| 指标名       | 专利                                                                     |
| 决策清单中的编号  | （空）                                                                    |
| 域         | 产业链                                                                    |
| 模块        | CHAIN                                                                  |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 定义中                                                                    |
| 验收单元      | TOPIC-REG-012                                                          |
| 四维评估      | 已评估                                                                    |
| 定义状态      | 草案                                                                     |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                 |
| 结构支撑      | 待首评                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | 初判                                                                     |
| 源映射       | 待ODS                                                                   |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                     |
| 接入状态      | Mock                                                                   |
| 接入阶段      | 源同步:未开始                                                                |
| 综合就绪      | 待口径确认                                                                  |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | pending                                                                |
| 口径摘要      | 区域内产业相关专利 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                    |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **73**


| 列        | 值                                                                      |
| -------- | ---------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_PATENT                                                     |
| 指标名      | 专利                                                                     |
| 决策清单中的编号 | （空）                                                                    |
| 域        | 产业链                                                                    |
| 模块       | CHAIN                                                                  |
| 算法类型     | STAT                                                                   |
| D1定义     | 草案                                                                     |
| D4接入     | Mock                                                                   |
| 需求来源条数   | 1                                                                      |
| 需求回填     | 已回填                                                                    |
| 来源系统     | 专题系统                                                                   |
| 主来源分册    | 05 算法库需规                                                               |
| 主来源序号    | 126                                                                    |
| 主来源名称    | 区域产业指数模型                                                               |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                    |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                    |
| 全部来源     | 05·126 区域产业指数模型                                                        |
| 口径摘要     | 区域内产业相关专利 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                             |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **77**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_PATENT                                |
| 指标名      | 专利                                                |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内产业专利。126。与 E38 专利数同族。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：专利要素库，非四表。

**算法是否满足**：计数 STAT 够。

**算法缺口**：无模型。缺专利-链挂接。

**可实现**：否（挂接未定）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：跨域专利 Mapping 无；draft。

**需要李伟确认的问题（仅特有）**

1. ~~身份~~ **跟 B18。**
2. ~~挂链~~ **已拍：甲**（链上企业受让人，不上 IPC）。
3. ~~E38~~ **不提前拍死。**
4. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

专利要素库 × 链上企业（申请人/受让人）× 企业所在地 ∈ 评价 `region_codes`，COUNT。全景专利数不得直接顶替。

**2026-08-27 核对小结**

- **本条已确认**。GDF/Mapping 债不挡确认。

---



### B22 · `M_CHAIN_REG_POLICY_COVERAGE` · 政策覆盖率（挂起）

**指标描述**：区域内产业政策覆盖率 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-28 `human:李伟`：**挂起**。政策相关先挂起；公式甲/乙不拍。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **80**


| 列         | 值                                                                       |
| --------- | ----------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_POLICY_COVERAGE                                             |
| 指标名       | 政策覆盖率                                                                   |
| 决策清单中的编号  | （空）                                                                     |
| 域         | 产业链                                                                     |
| 模块        | CHAIN                                                                   |
| 模块说明      | 产业链                                                                     |
| 专题维度Owner | 李伟                                                                      |
| 算法类型      | STAT                                                                    |
| 合同集合      | F∩L                                                                     |
| 差集判定      | mapped                                                                  |
| 语义层开发阶段   | 定义中                                                                     |
| 验收单元      | TOPIC-REG-019                                                           |
| 四维评估      | 已评估                                                                     |
| 定义状态      | 草案                                                                      |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                  |
| 结构支撑      | 待首评                                                                     |
| 结构缺口      | （空）                                                                     |
| 结构判定      | 初判                                                                      |
| 源映射       | 待ODS                                                                    |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                      |
| 接入状态      | Mock                                                                    |
| 接入阶段      | 源同步:未开始                                                                 |
| 综合就绪      | 待口径确认                                                                   |
| 卡点责任方     | 李伟                                                                      |
| 更新频率      | pending                                                                 |
| 口径摘要      | 区域内产业政策覆盖率 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                     |
| 更新日期      | 2026-08-25                                                              |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **74**


| 列        | 值                                                                       |
| -------- | ----------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_POLICY_COVERAGE                                             |
| 指标名      | 政策覆盖率                                                                   |
| 决策清单中的编号 | （空）                                                                     |
| 域        | 产业链                                                                     |
| 模块       | CHAIN                                                                   |
| 算法类型     | STAT                                                                    |
| D1定义     | 草案                                                                      |
| D4接入     | Mock                                                                    |
| 需求来源条数   | 1                                                                       |
| 需求回填     | 已回填                                                                     |
| 来源系统     | 专题系统                                                                    |
| 主来源分册    | 05 算法库需规                                                                |
| 主来源序号    | 126                                                                     |
| 主来源名称    | 区域产业指数模型                                                                |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                     |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                     |
| 全部来源     | 05·126 区域产业指数模型                                                         |
| 口径摘要     | 区域内产业政策覆盖率 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                              |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **78**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_POLICY_COVERAGE                       |
| 指标名      | 政策覆盖率                                             |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内产业政策覆盖率。126。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：政策要素库。覆盖率公式未签（有政策企业占比？还是发文量？）。

**算法是否满足**：若定义为占比/计数则 STAT 够。

**算法缺口**：公式未签。政策-链挂接未定。

**可实现**：否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；政策挂接。

**需要李伟确认的问题（仅特有）**

1. ~~公式甲/乙~~ **不拍。已挂起。**
2. 政策-链挂接、要素库活数：**源洗通后再拍**（跟资讯 CHAIN-NEWS-SRC-01 同类处理）。

**2026-08-28 核对小结**

- **本条挂起**（政策相关）。xlsx/页面分析仍有效，不当已确认口径。

---



### B23 · `M_CHAIN_REG_RESEARCH_ORG` · 科研机构（已确认）

**指标描述**：区域内科研机构规模或密度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

> 2026-08-28 `human:李伟`：**确认（甲）**。乙机构里科研院所+高校，当前 COUNT × 评价区域。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **81**


| 列         | 值                                                                         |
| --------- | ------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_RESEARCH_ORG                                                  |
| 指标名       | 科研机构                                                                      |
| 决策清单中的编号  | （空）                                                                       |
| 域         | 产业链                                                                       |
| 模块        | CHAIN                                                                     |
| 模块说明      | 产业链                                                                       |
| 专题维度Owner | 李伟                                                                        |
| 算法类型      | STAT                                                                      |
| 合同集合      | F∩L                                                                       |
| 差集判定      | mapped                                                                    |
| 语义层开发阶段   | 定义中                                                                       |
| 验收单元      | TOPIC-REG-015                                                             |
| 四维评估      | 已评估                                                                       |
| 定义状态      | 草案                                                                        |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                    |
| 结构支撑      | 待首评                                                                       |
| 结构缺口      | （空）                                                                       |
| 结构判定      | 初判                                                                        |
| 源映射       | 待ODS                                                                      |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                        |
| 接入状态      | Mock                                                                      |
| 接入阶段      | 源同步:未开始                                                                   |
| 综合就绪      | 待口径确认                                                                     |
| 卡点责任方     | 李伟                                                                        |
| 更新频率      | pending                                                                   |
| 口径摘要      | 区域内科研机构规模或密度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                       |
| 更新日期      | 2026-08-25                                                                |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **75**


| 列        | 值                                                                         |
| -------- | ------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_RESEARCH_ORG                                                  |
| 指标名      | 科研机构                                                                      |
| 决策清单中的编号 | （空）                                                                       |
| 域        | 产业链                                                                       |
| 模块       | CHAIN                                                                     |
| 算法类型     | STAT                                                                      |
| D1定义     | 草案                                                                        |
| D4接入     | Mock                                                                      |
| 需求来源条数   | 1                                                                         |
| 需求回填     | 已回填                                                                       |
| 来源系统     | 专题系统                                                                      |
| 主来源分册    | 05 算法库需规                                                                  |
| 主来源序号    | 126                                                                       |
| 主来源名称    | 区域产业指数模型                                                                  |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                       |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                       |
| 全部来源     | 05·126 区域产业指数模型                                                           |
| 口径摘要     | 区域内科研机构规模或密度 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                                |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **79**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_RESEARCH_ORG                          |
| 指标名      | 科研机构                                              |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内科研机构规模或密度。126。与 A3 机构同族。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 A3 机构源未定 + 区域。

**算法是否满足**：计数/密度 STAT 够。

**算法缺口**：无模型。机构挂接同 A3。

**可实现**：条件是：A3 源 + 区域。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；机构源。

**需要李伟确认的问题（仅特有）**

1. ~~身份~~ **跟 B18。**
2. ~~对象/形态~~ **已拍：A3 乙 + A12 当前 COUNT。**
3. ~~含高校~~ **已拍：甲**（科研院所+高校）。密度不单做。
4. ~~确认/挂起~~ **已拍：确认。**

**口径一句（已确认）**

A3 乙机构中科研院所+高校，当前去重 COUNT，所在地 ∈ 评价 `region_codes`。不是当年成立，不是密度。全景机构数不得直接顶替。

**2026-08-28 核对小结**

- **本条已确认**。机构边债跟 A3，不挡确认。

---



### B24 · `M_CHAIN_REG_SERVICE_ORG` · 服务机构（挂起）

**指标描述**：区域内产业服务机构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **83**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_SERVICE_ORG                                                |
| 指标名       | 服务机构                                                                   |
| 决策清单中的编号  | （空）                                                                    |
| 域         | 产业链                                                                    |
| 模块        | CHAIN                                                                  |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 定义中                                                                    |
| 验收单元      | TOPIC-REG-018                                                          |
| 四维评估      | 已评估                                                                    |
| 定义状态      | 草案                                                                     |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                 |
| 结构支撑      | 待首评                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | 初判                                                                     |
| 源映射       | 待ODS                                                                   |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                     |
| 接入状态      | Mock                                                                   |
| 接入阶段      | 源同步:未开始                                                                |
| 综合就绪      | 待口径确认                                                                  |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | pending                                                                |
| 口径摘要      | 区域内产业服务机构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                    |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **77**


| 列        | 值                                                                      |
| -------- | ---------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_SERVICE_ORG                                                |
| 指标名      | 服务机构                                                                   |
| 决策清单中的编号 | （空）                                                                    |
| 域        | 产业链                                                                    |
| 模块       | CHAIN                                                                  |
| 算法类型     | STAT                                                                   |
| D1定义     | 草案                                                                     |
| D4接入     | Mock                                                                   |
| 需求来源条数   | 1                                                                      |
| 需求回填     | 已回填                                                                    |
| 来源系统     | 专题系统                                                                   |
| 主来源分册    | 05 算法库需规                                                               |
| 主来源序号    | 126                                                                    |
| 主来源名称    | 区域产业指数模型                                                               |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                    |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                    |
| 全部来源     | 05·126 区域产业指数模型                                                        |
| 口径摘要     | 区域内产业服务机构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                             |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **81**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_SERVICE_ORG                           |
| 指标名      | 服务机构                                              |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内产业服务机构。126。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：无产业链服务机构四表。需机构类型口径。

**算法是否满足**：计数 STAT 够。

**算法缺口**：服务机构类型未定义。

**可实现**：否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；类型口径。

**需要李伟确认的问题（仅特有）**

1. **身份跟 B18，不重问**：支撑力预设叶子。页面：**不映射** `M_SVC_`*（不把服务专题六类指标搬过来）。
2. **形态跟 B23**：当前 COUNT × 评价区域，不是当年成立。
3. ~~服务机构从哪筛（甲/乙）~~ **不拍。已挂起。**
4. 服务类码表、机构库类型筛：**源与类型口径洗通后再拍**。不把 `M_SVC_`* 搬进本卡。

**2026-08-28 核对小结**

- 两 xlsx 全列、TOPIC-REG-018：材料核对仍有效。
- **本条已挂起**（2026-08-28 `human:李伟`）。IMPL 不排本 ID。

---



### B25 · `M_CHAIN_REG_TALENT_STRUCTURE` · 人才结构（挂起）

**指标描述**：区域内产业人才结构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **84**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_REG_TALENT_STRUCTURE                                           |
| 指标名       | 人才结构                                                                   |
| 决策清单中的编号  | （空）                                                                    |
| 域         | 产业链                                                                    |
| 模块        | CHAIN                                                                  |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 定义中                                                                    |
| 验收单元      | TOPIC-REG-017                                                          |
| 四维评估      | 已评估                                                                    |
| 定义状态      | 草案                                                                     |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                 |
| 结构支撑      | 待首评                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | 初判                                                                     |
| 源映射       | 待ODS                                                                   |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                     |
| 接入状态      | Mock                                                                   |
| 接入阶段      | 源同步:未开始                                                                |
| 综合就绪      | 待口径确认                                                                  |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | pending                                                                |
| 口径摘要      | 区域内产业人才结构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                    |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **78**


| 列        | 值                                                                      |
| -------- | ---------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_TALENT_STRUCTURE                                           |
| 指标名      | 人才结构                                                                   |
| 决策清单中的编号 | （空）                                                                    |
| 域        | 产业链                                                                    |
| 模块       | CHAIN                                                                  |
| 算法类型     | STAT                                                                   |
| D1定义     | 草案                                                                     |
| D4接入     | Mock                                                                   |
| 需求来源条数   | 1                                                                      |
| 需求回填     | 已回填                                                                    |
| 来源系统     | 专题系统                                                                   |
| 主来源分册    | 05 算法库需规                                                               |
| 主来源序号    | 126                                                                    |
| 主来源名称    | 区域产业指数模型                                                               |
| 主来源简述    | 产业链 / 深度分析：区域产业指数模型                                                    |
| 主来源需规ID  | ALGO-CHAIN-DEEP-126                                                    |
| 全部来源     | 05·126 区域产业指数模型                                                        |
| 口径摘要     | 区域内产业人才结构 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                             |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **82**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_REG_TALENT_STRUCTURE                      |
| 指标名      | 人才结构                                              |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 126                                               |
| 需规名称     | 区域产业指数模型                                          |
| 简要描述     | 产业链 / 深度分析：区域产业指数模型                               |
| 需规ID     | ALGO-CHAIN-DEEP-126                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-REGIONAL                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN draft：区域内产业人才结构。126。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：人才要素库，非四表。结构=学历/职称分布，公式未签。

**算法是否满足**：分布 STAT 够。

**算法缺口**：结构维未签。人才-链挂接未定。

**可实现**：否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；人才 Mapping。

**需要李伟确认的问题（仅特有）**

1. ~~结构维（学历/职称/技能标签）~~ **不拍。已挂起。**
2. 人才-链挂接、人才要素库活数：**源洗通后再拍**。

**2026-08-28 核对小结**

- 两 xlsx 全列、TOPIC-REG-017：材料核对仍有效。
- **本条已挂起**（2026-08-28 `human:李伟`）。IMPL 不排本 ID。瓶颈五维「人才」不在此次挂起范围。

---



### C26 · `M_CHAIN_BOTTLENECK_COUNT` · 瓶颈堵点数（挂起）

**指标描述**：pending_data_lead(QC04)：产业链中识别出的瓶颈/堵点数；瓶颈类型细分口径(5维是否完整)待甲方确认。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **107**


| 列         | 值                                                                                       |
| --------- | --------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_BOTTLENECK_COUNT                                                                |
| 指标名       | 瓶颈堵点数                                                                                   |
| 决策清单中的编号  | QC04                                                                                    |
| 域         | 产业链                                                                                     |
| 模块        | E2 产业链（待四维评估）                                                                           |
| 模块说明      | 产业链                                                                                     |
| 专题维度Owner | 李伟                                                                                      |
| 算法类型      | STAT                                                                                    |
| 合同集合      | F∩L                                                                                     |
| 差集判定      | mapped                                                                                  |
| 语义层开发阶段   | 未标                                                                                      |
| 验收单元      | —                                                                                       |
| 四维评估      | 待评估                                                                                     |
| 定义状态      | 草案                                                                                      |
| 开放项       | QC04                                                                                    |
| 结构支撑      | 待评估                                                                                     |
| 结构缺口      | （空）                                                                                     |
| 结构判定      | —                                                                                       |
| 源映射       | 待评估                                                                                     |
| 源缺口       | （空）                                                                                     |
| 接入状态      | Mock                                                                                    |
| 接入阶段      | （空）                                                                                     |
| 综合就绪      | 待口径确认                                                                                   |
| 卡点责任方     | 李伟                                                                                      |
| 更新频率      | weekly                                                                                  |
| 口径摘要      | pending_data_lead(QC04)：产业链中识别出的瓶颈/堵点数；瓶颈类型细分口径(5维是否完整)待甲方确认。                           |
| 缺口说明      | 产业链瓶颈环节数=被判定为瓶颈的节点计数。瓶颈类型分技术/人才/市场/资本/政策五维，各维度判定阈值待甲方确认(QC04)。Wave0 使用 mockgen 伪随机瓶颈数据。 |
| 更新日期      | 2026-08-25                                                                              |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **10**


| 列        | 值                                                             |
| -------- | ------------------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_COUNT                                      |
| 指标名      | 瓶颈堵点数                                                         |
| 决策清单中的编号 | QC04                                                          |
| 域        | 产业链                                                           |
| 模块       | CHAIN                                                         |
| 算法类型     | STAT                                                          |
| D1定义     | —                                                             |
| D4接入     | —                                                             |
| 需求来源条数   | 1                                                             |
| 需求回填     | 已回填                                                           |
| 来源系统     | 专题系统                                                          |
| 主来源分册    | 05 算法库需规                                                      |
| 主来源序号    | 125                                                           |
| 主来源名称    | 产业瓶颈堵点识别模型                                                    |
| 主来源简述    | 产业链 / 深度分析：产业瓶颈堵点识别模型                                         |
| 主来源需规ID  | ALGO-CHAIN-DEEP-125                                           |
| 全部来源     | 05·125 产业瓶颈堵点识别模型                                             |
| 口径摘要     | pending_data_lead(QC04)：产业链中识别出的瓶颈/堵点数；瓶颈类型细分口径(5维是否完整)待甲方确认。 |
| 更新日期     | 2026-08-25                                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **10**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_COUNT                          |
| 指标名      | 瓶颈堵点数                                             |
| 决策清单中的编号 | QC04                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 125                                               |
| 需规名称     | 产业瓶颈堵点识别模型                                        |
| 简要描述     | 产业链 / 深度分析：产业瓶颈堵点识别模型                             |
| 需规ID     | ALGO-CHAIN-DEEP-125                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：xlsx：被判定为瓶颈的节点计数；五维阈值 QC04。需求 05·125 瓶颈识别模型。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT id) FROM dwd.industry_bottleneck`；definition 与进度表口径对照见上。source_tables=['dwd.industry_bottleneck <- 算法判定', 'dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：识别是 MODEL（唐绍祖）。本叶 STAT 只计已打标节点。Demo 0。

**算法是否满足**：计数 STAT 够；识别模型不够（越界 125）。

**算法缺口**：本叶无识别算法。缺节点瓶颈标签表/字段。

**可实现**：STAT：条件是模型先落标签。本叶单独否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC04 🟡；125 模型未交；矩阵缺失。

**需要李伟确认的问题（仅特有）**

1. ~~身份（等 125 打标后再 STAT）~~ **已拍：甲**。本卡 = 已打标节点 COUNT；识别不在本叶。
2. 五维阈值 **不在本条拍**（QC04）。

**口径一句（已确认）**

已打标瓶颈节点去重 COUNT。识别归 05·125 / 唐绍祖。五维阈值跟 QC04。

**2026-08-28 核对小结**

- 口径甲记下：已打标节点 COUNT；识别归 125。
- **同日晚改挂起**（`human:李伟`：需模型、现不可做）。IMPL 不排。五维阈值仍 QC04。

---



### C27 · `M_CHAIN_BOTTLENECK_SEVERITY` · 瓶颈严重度（挂起）

**指标描述**：pending_data_lead(QC04)：产业链瓶颈的严重度评分（0-100，取最高严重度）；评分口径同 QC04。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **108**


| 列         | 值                                                                              |
| --------- | ------------------------------------------------------------------------------ |
| 指标ID      | M_CHAIN_BOTTLENECK_SEVERITY                                                    |
| 指标名       | 瓶颈严重度                                                                          |
| 决策清单中的编号  | QC04                                                                           |
| 域         | 产业链                                                                            |
| 模块        | E2 产业链（待四维评估）                                                                  |
| 模块说明      | 产业链                                                                            |
| 专题维度Owner | 李伟                                                                             |
| 算法类型      | STAT                                                                           |
| 合同集合      | F∩L                                                                            |
| 差集判定      | mapped                                                                         |
| 语义层开发阶段   | 未标                                                                             |
| 验收单元      | —                                                                              |
| 四维评估      | 待评估                                                                            |
| 定义状态      | 草案                                                                             |
| 开放项       | QC04                                                                           |
| 结构支撑      | 待评估                                                                            |
| 结构缺口      | （空）                                                                            |
| 结构判定      | —                                                                              |
| 源映射       | 待评估                                                                            |
| 源缺口       | （空）                                                                            |
| 接入状态      | Mock                                                                           |
| 接入阶段      | （空）                                                                            |
| 综合就绪      | 待口径确认                                                                          |
| 卡点责任方     | 李伟                                                                             |
| 更新频率      | weekly                                                                         |
| 口径摘要      | pending_data_lead(QC04)：产业链瓶颈的严重度评分（0-100，取最高严重度）；评分口径同 QC04。                  |
| 缺口说明      | 瓶颈严重度评分(0-100)取产业链中最高严重度瓶颈。五维（技术/人才/市场/资本/政策）各维度判定阈值与权重待甲方确认(QC04)。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                     |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **11**


| 列        | 值                                                             |
| -------- | ------------------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_SEVERITY                                   |
| 指标名      | 瓶颈严重度                                                         |
| 决策清单中的编号 | QC04                                                          |
| 域        | 产业链                                                           |
| 模块       | CHAIN                                                         |
| 算法类型     | STAT                                                          |
| D1定义     | —                                                             |
| D4接入     | —                                                             |
| 需求来源条数   | 1                                                             |
| 需求回填     | 已回填                                                           |
| 来源系统     | 专题系统                                                          |
| 主来源分册    | 05 算法库需规                                                      |
| 主来源序号    | 125                                                           |
| 主来源名称    | 产业瓶颈堵点识别模型                                                    |
| 主来源简述    | 产业链 / 深度分析：产业瓶颈堵点识别模型                                         |
| 主来源需规ID  | ALGO-CHAIN-DEEP-125                                           |
| 全部来源     | 05·125 产业瓶颈堵点识别模型                                             |
| 口径摘要     | pending_data_lead(QC04)：产业链瓶颈的严重度评分（0-100，取最高严重度）；评分口径同 QC04。 |
| 更新日期     | 2026-08-25                                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **11**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_SEVERITY                       |
| 指标名      | 瓶颈严重度                                             |
| 决策清单中的编号 | QC04                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 125                                               |
| 需规名称     | 产业瓶颈堵点识别模型                                        |
| 简要描述     | 产业链 / 深度分析：产业瓶颈堵点识别模型                             |
| 需规ID     | ALGO-CHAIN-DEEP-125                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：最高严重度 0-100。QC04。125。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（MAX(severity_score) FROM dwd.industry_bottleneck）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_bottleneck <- 算法判定']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 C26，取 MAX(severity)。

**算法是否满足**：MAX 是 STAT/简单聚合。分值模型越界。

**算法缺口**：缺严重度打分模型与阈值。

**可实现**：否（先模型）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC04；模型未交。

**需要李伟确认的问题（仅特有）**

1. ~~MAX / 等 125 落分~~ **不拍。已挂起。**
2. 0–100 与打分模型：**125 落分后再拍**。

**2026-08-28 核对小结**

- QC04 / 05·125 材料核对仍有效。
- **本条已挂起**（2026-08-28 `human:李伟`）。IMPL 不排本 ID。C26 同批改挂起。

---



### C28 · `M_CHAIN_BOTTLENECK_TYPE_DIST` · 瓶颈类型分布（挂起）

**指标描述**：pending_data_lead(QC04)：按瓶颈类型（技术/人才/市场/资本/政策）的分布统计；类型口径同 QC04。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **109**


| 列         | 值                                                                      |
| --------- | ---------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_BOTTLENECK_TYPE_DIST                                           |
| 指标名       | 瓶颈类型分布                                                                 |
| 决策清单中的编号  | QC04                                                                   |
| 域         | 产业链                                                                    |
| 模块        | E2 产业链（待四维评估）                                                          |
| 模块说明      | 产业链                                                                    |
| 专题维度Owner | 李伟                                                                     |
| 算法类型      | STAT                                                                   |
| 合同集合      | F∩L                                                                    |
| 差集判定      | mapped                                                                 |
| 语义层开发阶段   | 未标                                                                     |
| 验收单元      | —                                                                      |
| 四维评估      | 待评估                                                                    |
| 定义状态      | 草案                                                                     |
| 开放项       | QC04                                                                   |
| 结构支撑      | 待评估                                                                    |
| 结构缺口      | （空）                                                                    |
| 结构判定      | —                                                                      |
| 源映射       | 待评估                                                                    |
| 源缺口       | （空）                                                                    |
| 接入状态      | Mock                                                                   |
| 接入阶段      | （空）                                                                    |
| 综合就绪      | 待口径确认                                                                  |
| 卡点责任方     | 李伟                                                                     |
| 更新频率      | weekly                                                                 |
| 口径摘要      | pending_data_lead(QC04)：按瓶颈类型（技术/人才/市场/资本/政策）的分布统计；类型口径同 QC04。         |
| 缺口说明      | 瓶颈类型分布按技术/人才/市场/资本/政策五维统计各类型瓶颈数量。类型口径与判定标准同 QC04。Wave0 mockgen 产出分布数据。 |
| 更新日期      | 2026-08-25                                                             |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **12**


| 列        | 值                                                              |
| -------- | -------------------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_TYPE_DIST                                   |
| 指标名      | 瓶颈类型分布                                                         |
| 决策清单中的编号 | QC04                                                           |
| 域        | 产业链                                                            |
| 模块       | CHAIN                                                          |
| 算法类型     | STAT                                                           |
| D1定义     | —                                                              |
| D4接入     | —                                                              |
| 需求来源条数   | 1                                                              |
| 需求回填     | 已回填                                                            |
| 来源系统     | 专题系统                                                           |
| 主来源分册    | 05 算法库需规                                                       |
| 主来源序号    | 125                                                            |
| 主来源名称    | 产业瓶颈堵点识别模型                                                     |
| 主来源简述    | 产业链 / 深度分析：产业瓶颈堵点识别模型                                          |
| 主来源需规ID  | ALGO-CHAIN-DEEP-125                                            |
| 全部来源     | 05·125 产业瓶颈堵点识别模型                                              |
| 口径摘要     | pending_data_lead(QC04)：按瓶颈类型（技术/人才/市场/资本/政策）的分布统计；类型口径同 QC04。 |
| 更新日期     | 2026-08-25                                                     |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **12**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_BOTTLENECK_TYPE_DIST                      |
| 指标名      | 瓶颈类型分布                                            |
| 决策清单中的编号 | QC04                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 125                                               |
| 需规名称     | 产业瓶颈堵点识别模型                                        |
| 简要描述     | 产业链 / 深度分析：产业瓶颈堵点识别模型                             |
| 需规ID     | ALGO-CHAIN-DEEP-125                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：五维类型分布。QC04。125。

**MCP/seed**：type=`STAT`；formula=`COUNT(*) GROUP BY bottleneck_type FROM dwd.industry_bottleneck`；definition 与进度表口径对照见上。source_tables=['dwd.industry_bottleneck <- 算法判定']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：GROUP BY 类型的 STAT。

**算法是否满足**：分布 STAT 够。类型体系未拍则不能交。

**算法缺口**：类型枚举/阈值 QC04。

**可实现**：否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC04。

**需要李伟确认的问题（仅特有）**

1. ~~GROUP BY 类型~~ **不拍。已挂起。**
2. 类型字段：**125 落标后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C29 · `M_CHAIN_CHOKE_LINK_COUNT` · 卡脖子环节数（挂起）

**指标描述**：瓶颈∧severity=高；⊆ 瓶颈数；与图谱角标同计数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **54**


| 列         | 值                                                                                         |
| --------- | ----------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_CHOKE_LINK_COUNT                                                                  |
| 指标名       | 卡脖子环节数                                                                                    |
| 决策清单中的编号  | （空）                                                                                       |
| 域         | 产业链                                                                                       |
| 模块        | CHAIN                                                                                     |
| 模块说明      | 产业链                                                                                       |
| 专题维度Owner | 李伟                                                                                        |
| 算法类型      | STAT                                                                                      |
| 合同集合      | F∩L                                                                                       |
| 差集判定      | mapped                                                                                    |
| 语义层开发阶段   | 定义中                                                                                       |
| 验收单元      | TOPIC-DIAG-017                                                                            |
| 四维评估      | 已评估                                                                                       |
| 定义状态      | 草案                                                                                        |
| 开放项       | GAP-ALGO-TYPE-UNSIGNED                                                                    |
| 结构支撑      | 待首评                                                                                       |
| 结构缺口      | （空）                                                                                       |
| 结构判定      | 初判                                                                                        |
| 源映射       | 待ODS                                                                                      |
| 源缺口       | 身份已入 seed；三方 ODS 字段尚未核验。未核 ≠ 已确认缺口，禁止写成 none/full。                                        |
| 接入状态      | Mock                                                                                      |
| 接入阶段      | 源同步:未开始                                                                                   |
| 综合就绪      | 待口径确认                                                                                     |
| 卡点责任方     | 李伟                                                                                        |
| 更新频率      | pending                                                                                   |
| 口径摘要      | 瓶颈∧severity=高；⊆ 瓶颈数；与图谱角标同计数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 缺口说明      | （空）                                                                                       |
| 更新日期      | 2026-08-25                                                                                |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **14**


| 列        | 值                                                                                         |
| -------- | ----------------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_CHOKE_LINK_COUNT                                                                  |
| 指标名      | 卡脖子环节数                                                                                    |
| 决策清单中的编号 | （空）                                                                                       |
| 域        | 产业链                                                                                       |
| 模块       | CHAIN                                                                                     |
| 算法类型     | STAT                                                                                      |
| D1定义     | 草案                                                                                        |
| D4接入     | Mock                                                                                      |
| 需求来源条数   | 1                                                                                         |
| 需求回填     | 已回填                                                                                       |
| 来源系统     | 专题系统                                                                                      |
| 主来源分册    | 05 算法库需规                                                                                  |
| 主来源序号    | 125                                                                                       |
| 主来源名称    | 产业瓶颈堵点识别模型                                                                                |
| 主来源简述    | 产业链 / 深度分析：产业瓶颈堵点识别模型                                                                     |
| 主来源需规ID  | ALGO-CHAIN-DEEP-125                                                                       |
| 全部来源     | 05·125 产业瓶颈堵点识别模型                                                                         |
| 口径摘要     | 瓶颈∧severity=高；⊆ 瓶颈数；与图谱角标同计数 统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签，本条仅为 OPEN draft 身份。 |
| 更新日期     | 2026-08-25                                                                                |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **14**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_CHOKE_LINK_COUNT                          |
| 指标名      | 卡脖子环节数                                            |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 125                                               |
| 需规名称     | 产业瓶颈堵点识别模型                                        |
| 简要描述     | 产业链 / 深度分析：产业瓶颈堵点识别模型                             |
| 需规ID     | ALGO-CHAIN-DEEP-125                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：OPEN：瓶颈∧severity=高，⊆ 瓶颈数。125。

**MCP/seed**：type=`STAT`；formula=`pending_cosign: human:唐绍祖（未签）`；definition 与进度表口径对照见上。source_tables=['pending_ods']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：C26 的高严重度子集。

**算法是否满足**：过滤计数 STAT 够。

**算法缺口**：「高」阈值未签。识别越界模型。

**可实现**：否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：draft；QC04。

**需要李伟确认的问题（仅特有）**

1. ~~与 C26 是否只差严重度阈值~~ **不拍。已挂起。**
2. 「高」阈值 / 125 子集：**模型落标后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C30 · `M_CHAIN_HIGH_VALUE_RATIO` · 高价值环节占比（挂起）

**指标描述**：pending_data_lead(QC02)：高价值环节数占全部环节数比例；高价值判定口径同 QC02。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **121**


| 列         | 值                                                     |
| --------- | ----------------------------------------------------- |
| 指标ID      | M_CHAIN_HIGH_VALUE_RATIO                              |
| 指标名       | 高价值环节占比                                               |
| 决策清单中的编号  | QC02                                                  |
| 域         | 产业链                                                   |
| 模块        | E2 产业链（待四维评估）                                         |
| 模块说明      | 产业链                                                   |
| 专题维度Owner | 李伟                                                    |
| 算法类型      | STAT                                                  |
| 合同集合      | F∩L                                                   |
| 差集判定      | mapped                                                |
| 语义层开发阶段   | 未标                                                    |
| 验收单元      | —                                                     |
| 四维评估      | 待评估                                                   |
| 定义状态      | 草案                                                    |
| 开放项       | QC02                                                  |
| 结构支撑      | 待评估                                                   |
| 结构缺口      | （空）                                                   |
| 结构判定      | —                                                     |
| 源映射       | 待评估                                                   |
| 源缺口       | （空）                                                   |
| 接入状态      | Mock                                                  |
| 接入阶段      | （空）                                                   |
| 综合就绪      | 待口径确认                                                 |
| 卡点责任方     | 李伟                                                    |
| 更新频率      | weekly                                                |
| 口径摘要      | pending_data_lead(QC02)：高价值环节数占全部环节数比例；高价值判定口径同 QC02。 |
| 缺口说明      | （空）                                                   |
| 更新日期      | 2026-08-25                                            |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **42**


| 列        | 值                                                     |
| -------- | ----------------------------------------------------- |
| 指标ID     | M_CHAIN_HIGH_VALUE_RATIO                              |
| 指标名      | 高价值环节占比                                               |
| 决策清单中的编号 | QC02                                                  |
| 域        | 产业链                                                   |
| 模块       | CHAIN                                                 |
| 算法类型     | STAT                                                  |
| D1定义     | —                                                     |
| D4接入     | —                                                     |
| 需求来源条数   | 1                                                     |
| 需求回填     | 已回填                                                   |
| 来源系统     | 专题系统                                                  |
| 主来源分册    | 05 算法库需规                                              |
| 主来源序号    | 124                                                   |
| 主来源名称    | 产业链关键环节识别模型                                           |
| 主来源简述    | 产业链 / 深度分析：产业链关键环节识别模型                                |
| 主来源需规ID  | ALGO-CHAIN-DEEP-124                                   |
| 全部来源     | 05·124 产业链关键环节识别模型                                    |
| 口径摘要     | pending_data_lead(QC02)：高价值环节数占全部环节数比例；高价值判定口径同 QC02。 |
| 更新日期     | 2026-08-25                                            |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **45**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_HIGH_VALUE_RATIO                          |
| 指标名      | 高价值环节占比                                           |
| 决策清单中的编号 | QC02                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 124                                               |
| 需规名称     | 产业链关键环节识别模型                                       |
| 简要描述     | 产业链 / 深度分析：产业链关键环节识别模型                            |
| 需规ID     | ALGO-CHAIN-DEEP-124                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：高价值环节数/全部环节。QC02。需求 05·124 关键环节识别模型。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（高价值环节数 / 全部环节数 * 100）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain <- ods: dwd_industry_chain_info', 'dwd.industry_chain_enterprise']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：关键环节 MODEL 后 STAT 占比。Demo 映射曾用合成 stage，不当口径。

**算法是否满足**：占比 STAT 够；何谓高价值越界 124/QC02。

**算法缺口**：缺 is_high_value/关键环节标签。

**可实现**：STAT 条件是标签先落。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC02 🟡；124 未交。

**需要李伟确认的问题（仅特有）**

1. ~~高价值是否等同关键环节（QC02）~~ **不拍。已挂起。**
2. 124 / QC02 标签：**模型落标后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C31 · `M_CHAIN_LAYOUT_RECOMMEND_COUNT` · 重点布局推荐数（挂起）

**指标描述**：pending_data_lead(QC09)：算法推荐的重点布局产业链/环节数；推荐算法权重与阈值待甲方确认。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **128**


| 列         | 值                                                                          |
| --------- | -------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_LAYOUT_RECOMMEND_COUNT                                             |
| 指标名       | 重点布局推荐数                                                                    |
| 决策清单中的编号  | QC09                                                                       |
| 域         | 产业链                                                                        |
| 模块        | E2 产业链（待四维评估）                                                              |
| 模块说明      | 产业链                                                                        |
| 专题维度Owner | 李伟                                                                         |
| 算法类型      | STAT                                                                       |
| 合同集合      | F∩L                                                                        |
| 差集判定      | mapped                                                                     |
| 语义层开发阶段   | 未标                                                                         |
| 验收单元      | —                                                                          |
| 四维评估      | 待评估                                                                        |
| 定义状态      | 草案                                                                         |
| 开放项       | QC09                                                                       |
| 结构支撑      | 待评估                                                                        |
| 结构缺口      | （空）                                                                        |
| 结构判定      | —                                                                          |
| 源映射       | 待评估                                                                        |
| 源缺口       | （空）                                                                        |
| 接入状态      | Mock                                                                       |
| 接入阶段      | （空）                                                                        |
| 综合就绪      | 待口径确认                                                                      |
| 卡点责任方     | 李伟                                                                         |
| 更新频率      | weekly                                                                     |
| 口径摘要      | pending_data_lead(QC09)：算法推荐的重点布局产业链/环节数；推荐算法权重与阈值待甲方确认。                   |
| 缺口说明      | 重点布局推荐数=布局优先级评分≥阈值的产业链/环节数。推荐算法权重与阈值待甲方确认(QC09)。当前临时多因子等权+阈值60。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                 |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **52**


| 列        | 值                                                                                |
| -------- | -------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_LAYOUT_RECOMMEND_COUNT                                                   |
| 指标名      | 重点布局推荐数                                                                          |
| 决策清单中的编号 | QC09                                                                             |
| 域        | 产业链                                                                              |
| 模块       | CHAIN                                                                            |
| 算法类型     | STAT                                                                             |
| D1定义     | —                                                                                |
| D4接入     | —                                                                                |
| 需求来源条数   | 1                                                                                |
| 需求回填     | 已回填                                                                              |
| 来源系统     | 展示系统                                                                             |
| 主来源分册    | 05 算法库需规                                                                         |
| 主来源序号    | 129                                                                              |
| 主来源名称    | 重点布局产业推荐模型                                                                       |
| 主来源简述    | 05 seq 129。B 轨已有。门户 IA 不运行推荐 Job，只读已发布结果。不扫 CHAIN-TOPIC-SHENZHEN。QC09 见 POV-B05。 |
| 主来源需规ID  | ALGO-CHAIN-DEEP-129                                                              |
| 全部来源     | 05·129 重点布局产业推荐模型                                                                |
| 口径摘要     | pending_data_lead(QC09)：算法推荐的重点布局产业链/环节数；推荐算法权重与阈值待甲方确认。                         |
| 更新日期     | 2026-08-25                                                                       |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **55**（第 1 条）


| 列        | 值                                                                                |
| -------- | -------------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_LAYOUT_RECOMMEND_COUNT                                                   |
| 指标名      | 重点布局推荐数                                                                          |
| 决策清单中的编号 | QC09                                                                             |
| 域        | 产业链                                                                              |
| 模块       | CHAIN                                                                            |
| 分册       | 05                                                                               |
| 分册名称     | 05 算法库需规                                                                         |
| 系统       | 展示系统                                                                             |
| 序号       | 129                                                                              |
| 需规名称     | 重点布局产业推荐模型                                                                       |
| 简要描述     | 05 seq 129。B 轨已有。门户 IA 不运行推荐 Job，只读已发布结果。不扫 CHAIN-TOPIC-SHENZHEN。QC09 见 POV-B05。 |
| 需规ID     | ALGO-CHAIN-DEEP-129                                                              |
| 角色       | 算法库叶                                                                             |
| 页面       | CHAIN-PORTAL-OVERVIEW                                                            |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md                                |
| 回填状态     | 已回填                                                                              |




#### 4) 结合分析

**口径一句**：优先级≥阈值的链/环节数。QC09。需求 05·129 重点布局推荐模型。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT chain_id) WHERE 布局优先级评分 >= 阈值`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain', 'dwd.industry_region_index', 'dwd.industry_bottleneck']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：推荐 MODEL 后 STAT 计数。Demo 0。

**算法是否满足**：计数 STAT 够；推荐模型越界 129。

**算法缺口**：缺推荐分与阈值（临时 60/等权，未拍）。

**可实现**：本叶否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC09；129 未交。

**需要李伟确认的问题（仅特有）**

1. ~~等 129 打分后再计数~~ **不拍。已挂起。**
2. 推荐分 / 阈值：**129 落分后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C32 · `M_CHAIN_SZ_COMPLETENESS` · 深圳产业链完整度（已确认）

**指标描述**：pending_data_lead(QC01)：深圳覆盖的产业链环节数占全链环节数比例；完整度口径（按节点数/按企业覆盖/按产值覆盖）待甲方确认。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **145**


| 列         | 值                                                                                 |
| --------- | --------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_COMPLETENESS                                                           |
| 指标名       | 深圳产业链完整度                                                                          |
| 决策清单中的编号  | QC01                                                                              |
| 域         | 产业链                                                                               |
| 模块        | E2 产业链（待四维评估）                                                                     |
| 模块说明      | 产业链                                                                               |
| 专题维度Owner | 李伟                                                                                |
| 算法类型      | STAT                                                                              |
| 合同集合      | F∩L                                                                               |
| 差集判定      | mapped                                                                            |
| 语义层开发阶段   | 未标                                                                                |
| 验收单元      | —                                                                                 |
| 四维评估      | 待评估                                                                               |
| 定义状态      | 草案                                                                                |
| 开放项       | QC01                                                                              |
| 结构支撑      | 待评估                                                                               |
| 结构缺口      | （空）                                                                               |
| 结构判定      | —                                                                                 |
| 源映射       | 待评估                                                                               |
| 源缺口       | （空）                                                                               |
| 接入状态      | Mock                                                                              |
| 接入阶段      | （空）                                                                               |
| 综合就绪      | 待口径确认                                                                             |
| 卡点责任方     | 李伟                                                                                |
| 更新频率      | weekly                                                                            |
| 口径摘要      | pending_data_lead(QC01)：深圳覆盖的产业链环节数占全链环节数比例；完整度口径（按节点数/按企业覆盖/按产值覆盖）待甲方确认。         |
| 缺口说明      | 深圳产业链完整度=深圳覆盖环节数/全链环节数*100。完整度口径有三种（按节点数/按企业覆盖/按产值覆盖），待甲方确认(QC01)。当前临时按节点数覆盖比例计算。 |
| 更新日期      | 2026-08-25                                                                        |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **87**


| 列        | 值                                                                         |
| -------- | ------------------------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_COMPLETENESS                                                   |
| 指标名      | 深圳产业链完整度                                                                  |
| 决策清单中的编号 | QC01                                                                      |
| 域        | 产业链                                                                       |
| 模块       | CHAIN                                                                     |
| 算法类型     | STAT                                                                      |
| D1定义     | —                                                                         |
| D4接入     | —                                                                         |
| 需求来源条数   | 2                                                                         |
| 需求回填     | 已回填                                                                       |
| 来源系统     | 专题系统                                                                      |
| 主来源分册    | 05 算法库需规                                                                  |
| 主来源序号    | 118                                                                       |
| 主来源名称    | 深圳产业链模型构建                                                                 |
| 主来源简述    | 产业链 / 深度分析：深圳产业链模型构建                                                      |
| 主来源需规ID  | ALGO-CHAIN-DEEP-118                                                       |
| 全部来源     | 04·36 深圳产业链完整度                                                            |
| 口径摘要     | pending_data_lead(QC01)：深圳覆盖的产业链环节数占全链环节数比例；完整度口径（按节点数/按企业覆盖/按产值覆盖）待甲方确认。 |
| 更新日期     | 2026-08-25                                                                |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **92**（第 1 条）


| 列        | 值                            |
| -------- | ---------------------------- |
| 指标ID     | M_CHAIN_SZ_COMPLETENESS      |
| 指标名      | 深圳产业链完整度                     |
| 决策清单中的编号 | QC01                         |
| 域        | 产业链                          |
| 模块       | CHAIN                        |
| 分册       | 04                           |
| 分册名称     | 04 专题需规                      |
| 系统       | 专题系统                         |
| 序号       | 36                           |
| 需规名称     | 深圳产业链完整度                     |
| 简要描述     | 深圳覆盖环节数占全链环节数比例；口径 QC01 待甲方。 |
| 需规ID     | （空）                          |
| 角色       | 页面使用                         |
| 页面       | CHAIN-TOPIC-SHENZHEN         |
| 需规文件     | （空）                          |
| 回填状态     | 已回填                          |


Sheet：`需求来源明细` · excel 行号 **93**（第 2 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_COMPLETENESS                           |
| 指标名      | 深圳产业链完整度                                          |
| 决策清单中的编号 | QC01                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 118                                               |
| 需规名称     | 深圳产业链模型构建                                         |
| 简要描述     | 产业链 / 深度分析：深圳产业链模型构建                              |
| 需规ID     | ALGO-CHAIN-DEEP-118                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：深圳覆盖环节/全链环节。QC01 三种口径。需求 05·118 + 04 seq 36 页面使用（文件空）。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（深圳覆盖环节数 / 全链环节数 * 100）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl', 'dwd.industry_chain <- ods: dwd_industry_chain_info']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：节点表 `industry_chain_node` + 深圳企业覆盖。STAT 比率。

**算法是否满足**：比率 STAT 够。三种口径未拍则不能锁公式。

**算法缺口**：无模型（除非产值覆盖要营收）。缺 QC01 选择。

**可实现**：条件是：QC01 拍一种。节点覆盖可先做。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC01；04 文件空。

**需要李伟确认的问题（仅特有）**

1. ~~三种完整度选哪一种~~ **已拍：甲**（按节点覆盖）。
2. 产值/企业覆盖 **不另做卡**。QC01 甲方改口径再覆盖。

**口径一句（已确认）**

深圳有主体挂上的环节数 / 全链环节数 × 100。`city=深圳市` 跟 A9。不按产值。不升 118 模型。

**2026-08-28 核对小结**

- **本条已确认（甲）**。环节节点表 Mapping 不挡口径确认。

---



### C33 · `M_CHAIN_SZ_ADVANTAGE_RANK` · 深圳优势排名（挂起）

**指标描述**：pending_data_lead(QC08)：深圳在产业链中的优势排名（与对标城市比较）；对标城市集合同 QC08。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **96**


| 列         | 值                                                                                   |
| --------- | ----------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_ADVANTAGE_RANK                                                           |
| 指标名       | 深圳优势排名                                                                              |
| 决策清单中的编号  | QC08                                                                                |
| 域         | 产业链                                                                                 |
| 模块        | CHAIN-SZ                                                                            |
| 模块说明      | 产业链分析 / 深圳                                                                          |
| 专题维度Owner | 李伟                                                                                  |
| 算法类型      | STAT                                                                                |
| 合同集合      | F∩L                                                                                 |
| 差集判定      | mapped                                                                              |
| 语义层开发阶段   | 未标                                                                                  |
| 验收单元      | CHAIN-SZ-ADVANTAGE                                                                  |
| 四维评估      | 已评估                                                                                 |
| 定义状态      | 草案                                                                                  |
| 开放项       | QC08                                                                                |
| 结构支撑      | 待首评                                                                                 |
| 结构缺口      | （空）                                                                                 |
| 结构判定      | 初判                                                                                  |
| 源映射       | 部分缺口                                                                                |
| 源缺口       | 派生自 ADVANTAGE_SCORE                                                                 |
| 接入状态      | Mock                                                                                |
| 接入阶段      | 源同步:未开始                                                                             |
| 综合就绪      | 待口径确认                                                                               |
| 卡点责任方     | 李伟                                                                                  |
| 更新频率      | weekly                                                                              |
| 口径摘要      | pending_data_lead(QC08)：深圳在产业链中的优势排名（与对标城市比较）；对标城市集合同 QC08。                         |
| 缺口说明      | 深圳优势排名派生自 M_CHAIN_SZ_ADVANTAGE_SCORE 在对标城市中的排序。对标城市集合同 QC08（临时默认北上广深苏杭）。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                          |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **85**


| 列        | 值                                                           |
| -------- | ----------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ADVANTAGE_RANK                                   |
| 指标名      | 深圳优势排名                                                      |
| 决策清单中的编号 | QC08                                                        |
| 域        | CHAIN-SZ                                                    |
| 模块       | CHAIN-SZ                                                    |
| 算法类型     | STAT                                                        |
| D1定义     | 草案                                                          |
| D4接入     | Mock                                                        |
| 需求来源条数   | 1                                                           |
| 需求回填     | 已回填                                                         |
| 来源系统     | 专题系统                                                        |
| 主来源分册    | 05 算法库需规                                                    |
| 主来源序号    | 121                                                         |
| 主来源名称    | 深圳产业优势识别模型                                                  |
| 主来源简述    | 产业链 / 深度分析：深圳产业优势识别模型                                       |
| 主来源需规ID  | ALGO-CHAIN-DEEP-121                                         |
| 全部来源     | 05·121 深圳产业优势识别模型                                           |
| 口径摘要     | pending_data_lead(QC08)：深圳在产业链中的优势排名（与对标城市比较）；对标城市集合同 QC08。 |
| 更新日期     | 2026-08-25                                                  |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **89**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_ADVANTAGE_RANK                         |
| 指标名      | 深圳优势排名                                            |
| 决策清单中的编号 | QC08                                              |
| 域        | CHAIN-SZ                                          |
| 模块       | CHAIN-SZ                                          |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 121                                               |
| 需规名称     | 深圳产业优势识别模型                                        |
| 简要描述     | 产业链 / 深度分析：深圳产业优势识别模型                             |
| 需规ID     | ALGO-CHAIN-DEEP-121                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-SHENZHEN                              |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：对标城市中的排名，派生自优势分。QC08。需求 05·121 优势识别模型。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（RANK() OVER ORDER BY 优势评分 DESC）`；definition 与进度表口径对照见上。source_tables=['派生自 M_CHAIN_SZ_ADVANTAGE_SCORE']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：121 是 MODEL；本条 RANK 是 STAT/排序。Demo 0。

**算法是否满足**：排序够；优势分模型越界 121。

**算法缺口**：缺优势分与对标城市集。

**可实现**：本叶否（先 121）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC08；121 未交。

**需要李伟确认的问题（仅特有）**

1. ~~等 121 分数再排~~ **不拍。已挂起。**
2. 优势分 / 对标城市：**121 落分后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C34 · `M_CHAIN_SZ_KEY_NODE_COVERAGE` · 深圳关键环节覆盖率（挂起）

**指标描述**：pending_data_lead(QC02)：深圳覆盖的关键环节数占全链关键环节总数比例；关键环节判定口径同 QC02。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=False。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **101**


| 列         | 值                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_KEY_NODE_COVERAGE                                                                   |
| 指标名       | 深圳关键环节覆盖率                                                                                      |
| 决策清单中的编号  | QC02                                                                                           |
| 域         | 产业链                                                                                            |
| 模块        | CHAIN-SZ                                                                                       |
| 模块说明      | 产业链分析 / 深圳                                                                                     |
| 专题维度Owner | 李伟                                                                                             |
| 算法类型      | STAT                                                                                           |
| 合同集合      | L−F                                                                                            |
| 差集判定      | 未挂页                                                                                            |
| 语义层开发阶段   | 未标                                                                                             |
| 验收单元      | CHAIN-SZ-PANORAMA                                                                              |
| 四维评估      | 已评估                                                                                            |
| 定义状态      | 已对齐                                                                                            |
| 开放项       | （空）                                                                                            |
| 结构支撑      | 待首评                                                                                            |
| 结构缺口      | （空）                                                                                            |
| 结构判定      | 初判                                                                                             |
| 源映射       | 部分缺口                                                                                           |
| 源缺口       | coverage = covered_nodes/total_nodes，字段级口径待核验                                                  |
| 接入状态      | Mock                                                                                           |
| 接入阶段      | 源同步:未开始                                                                                        |
| 综合就绪      | 待结构设计                                                                                          |
| 卡点责任方     | 李伟                                                                                             |
| 更新频率      | weekly                                                                                         |
| 口径摘要      | pending_data_lead(QC02)：深圳覆盖的关键环节数占全链关键环节总数比例；关键环节判定口径同 QC02。                                  |
| 缺口说明      | 深圳关键环节覆盖率=深圳覆盖关键环节数/全链关键环节总数*100。关键环节判定阈值（企业数量Top20%还是其他标准）待甲方确认(QC02)。当前临时按 is_key_node=1 统计。 |
| 更新日期      | 2026-08-25                                                                                     |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **93**


| 列        | 值                                                             |
| -------- | ------------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_KEY_NODE_COVERAGE                                  |
| 指标名      | 深圳关键环节覆盖                                                      |
| 决策清单中的编号 | QC02                                                          |
| 域        | CHAIN-SZ                                                      |
| 模块       | CHAIN-SZ                                                      |
| 算法类型     | STAT                                                          |
| D1定义     | 已对齐                                                           |
| D4接入     | Mock                                                          |
| 需求来源条数   | 0                                                             |
| 需求回填     | 未回填                                                           |
| 来源系统     | （空）                                                           |
| 主来源分册    | （空）                                                           |
| 主来源序号    | （空）                                                           |
| 主来源名称    | （空）                                                           |
| 主来源简述    | （空）                                                           |
| 主来源需规ID  | （空）                                                           |
| 全部来源     | （空）                                                           |
| 口径摘要     | pending_data_lead(QC02)：深圳覆盖的关键环节数占全链关键环节总数比例；关键环节判定口径同 QC02。 |
| 更新日期     | 2026-08-25                                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **100**（第 1 条）


| 列        | 值                            |
| -------- | ---------------------------- |
| 指标ID     | M_CHAIN_SZ_KEY_NODE_COVERAGE |
| 指标名      | 深圳关键环节覆盖                     |
| 决策清单中的编号 | QC02                         |
| 域        | CHAIN-SZ                     |
| 模块       | CHAIN-SZ                     |
| 分册       | （空）                          |
| 分册名称     | （空）                          |
| 系统       | （空）                          |
| 序号       | （空）                          |
| 需规名称     | （空）                          |
| 简要描述     | （空）                          |
| 需规ID     | （空）                          |
| 角色       | （空）                          |
| 页面       | （空）                          |
| 需规文件     | （空）                          |
| 回填状态     | 未回填                          |




#### 4) 结合分析

**口径一句**：深圳覆盖关键环节/全链关键环节。QC02。需求来源目录/明细全空。

**MCP/seed**：type=`STAT`；formula=`pending_algorithm（深圳覆盖关键环节数 / 全链关键环节数 * 100）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl', 'dwd.industry_chain.is_key_node']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：同 C30 标签 + 深圳覆盖。

**算法是否满足**：比率 STAT 够。

**算法缺口**：关键环节标签未定。SRS 未回填。

**可实现**：条件是：QC02 + 标签。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：需求来源空；QC02。

**需要李伟确认的问题（仅特有）**

1. ~~是否补挂 05·124~~ **不拍。已挂起。**
2. 关键环节标签：**124 / QC02 落标后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### C35 · `M_CHAIN_SZ_PROBLEM_COUNT` · 深圳产业问题数（挂起）

**指标描述**：深圳在产业链中面临的问题/短板数量；基于瓶颈识别+深圳切片统计。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=True srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **104**


| 列         | 值                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_SZ_PROBLEM_COUNT                                                                       |
| 指标名       | 深圳产业问题数                                                                                        |
| 决策清单中的编号  | （空）                                                                                            |
| 域         | 产业链                                                                                            |
| 模块        | CHAIN-SZ                                                                                       |
| 模块说明      | 产业链分析 / 深圳                                                                                     |
| 专题维度Owner | 李伟                                                                                             |
| 算法类型      | STAT                                                                                           |
| 合同集合      | F∩L                                                                                            |
| 差集判定      | mapped                                                                                         |
| 语义层开发阶段   | 未标                                                                                             |
| 验收单元      | CHAIN-SZ-PROBLEM                                                                               |
| 四维评估      | 已评估                                                                                            |
| 定义状态      | 已对齐                                                                                            |
| 开放项       | （空）                                                                                            |
| 结构支撑      | 待首评                                                                                            |
| 结构缺口      | （空）                                                                                            |
| 结构判定      | 初判                                                                                             |
| 源映射       | 部分缺口                                                                                           |
| 源缺口       | 五维阈值待甲方；当前 mockgen 可产出                                                                         |
| 接入状态      | Mock                                                                                           |
| 接入阶段      | 源同步:未开始                                                                                        |
| 综合就绪      | 待结构设计                                                                                          |
| 卡点责任方     | 李伟                                                                                             |
| 更新频率      | weekly                                                                                         |
| 口径摘要      | 深圳在产业链中面临的问题/短板数量；基于瓶颈识别+深圳切片统计。                                                               |
| 缺口说明      | 深圳产业问题数=深圳在产业链中面临的问题/短板数量。基于瓶颈识别+深圳切片统计(region_code LIKE '4403%')。五维阈值待甲方(QC04)。Wave0 mockgen。 |
| 更新日期      | 2026-08-25                                                                                     |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **98**


| 列        | 值                                                          |
| -------- | ---------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_PROBLEM_COUNT                                   |
| 指标名      | 深圳产业问题数                                                    |
| 决策清单中的编号 | （空）                                                        |
| 域        | CHAIN-SZ                                                   |
| 模块       | CHAIN-SZ                                                   |
| 算法类型     | STAT                                                       |
| D1定义     | 已对齐                                                        |
| D4接入     | Mock                                                       |
| 需求来源条数   | 2                                                          |
| 需求回填     | 已回填                                                        |
| 来源系统     | 专题系统                                                       |
| 主来源分册    | 05 算法库需规                                                   |
| 主来源序号    | 127                                                        |
| 主来源名称    | 深圳问题识别模型                                                   |
| 主来源简述    | B轨 63 未列此 ID；seed 已注册，算法库「深圳问题识别模型」seq 127 已覆盖，不标 missing。 |
| 主来源需规ID  | ALGO-CHAIN-DEEP-127                                        |
| 全部来源     | 04·36 深圳产业问题数                                              |
| 口径摘要     | 深圳在产业链中面临的问题/短板数量；基于瓶颈识别+深圳切片统计。                           |
| 更新日期     | 2026-08-25                                                 |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **105**（第 1 条）


| 列        | 值                        |
| -------- | ------------------------ |
| 指标ID     | M_CHAIN_SZ_PROBLEM_COUNT |
| 指标名      | 深圳产业问题数                  |
| 决策清单中的编号 | （空）                      |
| 域        | CHAIN-SZ                 |
| 模块       | CHAIN-SZ                 |
| 分册       | 04                       |
| 分册名称     | 04 专题需规                  |
| 系统       | 专题系统                     |
| 序号       | 36                       |
| 需规名称     | 深圳产业问题数                  |
| 简要描述     | 深圳在目标产业链中的问题/短板数量。       |
| 需规ID     | （空）                      |
| 角色       | 页面使用                     |
| 页面       | CHAIN-TOPIC-SHENZHEN     |
| 需规文件     | （空）                      |
| 回填状态     | 已回填                      |


Sheet：`需求来源明细` · excel 行号 **106**（第 2 条）


| 列        | 值                                                          |
| -------- | ---------------------------------------------------------- |
| 指标ID     | M_CHAIN_SZ_PROBLEM_COUNT                                   |
| 指标名      | 深圳产业问题数                                                    |
| 决策清单中的编号 | （空）                                                        |
| 域        | CHAIN-SZ                                                   |
| 模块       | CHAIN-SZ                                                   |
| 分册       | 05                                                         |
| 分册名称     | 05 算法库需规                                                   |
| 系统       | 专题系统                                                       |
| 序号       | 127                                                        |
| 需规名称     | 深圳问题识别模型                                                   |
| 简要描述     | B轨 63 未列此 ID；seed 已注册，算法库「深圳问题识别模型」seq 127 已覆盖，不标 missing。 |
| 需规ID     | ALGO-CHAIN-DEEP-127                                        |
| 角色       | 算法库叶                                                       |
| 页面       | CHAIN-TOPIC-SHENZHEN                                       |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md          |
| 回填状态     | 已回填                                                        |




#### 4) 结合分析

**口径一句**：深圳问题/短板数=瓶颈识别+深圳切片。需求 05·127 + 04 seq 36。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT id) FROM dwd.industry_bottleneck WHERE region_code LIKE '4403%'`；definition 与进度表口径对照见上。source_tables=['dwd.industry_bottleneck <- 算法判定', 'dwd.industry_chain_enterprise']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：127 是 MODEL。STAT 计已打标问题。

**算法是否满足**：计数够；识别越界 127。

**算法缺口**：缺问题标签。QC04 五维。

**可实现**：本叶否。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC04；127 未交；04 文件空。

**需要李伟确认的问题（仅特有）**

1. ~~问题是否复用瓶颈五维深圳切片~~ **不拍。已挂起。**
2. 127 / 问题标签：**模型落标后再拍**。

**2026-08-28 核对小结**

- **本条已挂起**（需模型、现不可做）。IMPL 不排。

---



### D36 · `M_CHAIN_CONCENTRATION_INDEX` · 产业集中度（挂起）

**指标描述**：pending_data_lead(QC02)：产业链企业分布的集中度指数（HHI 或 CR_N）；口径与 N 值待甲方确认。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **113**


| 列         | 值                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_CONCENTRATION_INDEX                                                                               |
| 指标名       | 产业集中度                                                                                                     |
| 决策清单中的编号  | QC02                                                                                                      |
| 域         | 产业链                                                                                                       |
| 模块        | E2 产业链（待四维评估）                                                                                             |
| 模块说明      | 产业链                                                                                                       |
| 专题维度Owner | 李伟                                                                                                        |
| 算法类型      | COMPUTE                                                                                                   |
| 合同集合      | F∩L                                                                                                       |
| 差集判定      | mapped                                                                                                    |
| 语义层开发阶段   | 未标                                                                                                        |
| 验收单元      | —                                                                                                         |
| 四维评估      | 待评估                                                                                                       |
| 定义状态      | 草案                                                                                                        |
| 开放项       | QC02                                                                                                      |
| 结构支撑      | 待评估                                                                                                       |
| 结构缺口      | （空）                                                                                                       |
| 结构判定      | —                                                                                                         |
| 源映射       | 待评估                                                                                                       |
| 源缺口       | （空）                                                                                                       |
| 接入状态      | Mock                                                                                                      |
| 接入阶段      | （空）                                                                                                       |
| 综合就绪      | 待口径确认                                                                                                     |
| 卡点责任方     | 李伟                                                                                                        |
| 更新频率      | weekly                                                                                                    |
| 口径摘要      | pending_data_lead(QC02)：产业链企业分布的集中度指数（HHI 或 CR_N）；口径与 N 值待甲方确认。                                           |
| 缺口说明      | 产业集中度采用 HHI（各企业市场份额平方和）或 CR_N（TopN企业市场份额之和）。N 值选择（CR5/CR10/CR20）与口径（HHI vs CR_N）待甲方确认(QC02)。Wave0 暂用 HHI。 |
| 更新日期      | 2026-08-25                                                                                                |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **17**


| 列        | 值                                                               |
| -------- | --------------------------------------------------------------- |
| 指标ID     | M_CHAIN_CONCENTRATION_INDEX                                     |
| 指标名      | 产业集中度                                                           |
| 决策清单中的编号 | QC02                                                            |
| 域        | 产业链                                                             |
| 模块       | CHAIN                                                           |
| 算法类型     | COMPUTE                                                         |
| D1定义     | —                                                               |
| D4接入     | —                                                               |
| 需求来源条数   | 1                                                               |
| 需求回填     | 已回填                                                             |
| 来源系统     | 专题系统                                                            |
| 主来源分册    | 05 算法库需规                                                        |
| 主来源序号    | 124                                                             |
| 主来源名称    | 产业链关键环节识别模型                                                     |
| 主来源简述    | 产业链 / 深度分析：产业链关键环节识别模型                                          |
| 主来源需规ID  | ALGO-CHAIN-DEEP-124                                             |
| 全部来源     | 05·124 产业链关键环节识别模型                                              |
| 口径摘要     | pending_data_lead(QC02)：产业链企业分布的集中度指数（HHI 或 CR_N）；口径与 N 值待甲方确认。 |
| 更新日期     | 2026-08-25                                                      |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **18**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_CONCENTRATION_INDEX                       |
| 指标名      | 产业集中度                                             |
| 决策清单中的编号 | QC02                                              |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 专题系统                                              |
| 序号       | 124                                               |
| 需规名称     | 产业链关键环节识别模型                                       |
| 简要描述     | 产业链 / 深度分析：产业链关键环节识别模型                            |
| 需规ID     | ALGO-CHAIN-DEEP-124                               |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-TOPIC-DIAGNOSIS                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/深度分析.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：HHI 或 CR_N。QC02。需求 05·124。类型 COMPUTE（本叶负责）。

**MCP/seed**：type=`COMPUTE`；formula=`pending_algorithm（HHI = SUM(企业市场份额^2) 或 CR_N = TopN企业市场份额之和）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise <- ods: dwd_org_industry_chain_dtl.chain_score']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：份额=企业营收/市场规模（B15 拆到企业）。无份额则算不出。

**算法是否满足**：COMPUTE 公式够（HHI/CR_N）。不升 MODEL。

**算法缺口**：N 值/HHI vs CR_N 未拍。缺企业份额（依赖年报 JOIN）。

**可实现**：条件是：QC02 锁口径 + B15 企业份额可算。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：QC02；份额源。

**需要李伟确认的问题（仅特有）**

1. ~~锁 HHI 还是 CR_N~~ **不拍。已挂起。**
2. HHI / CR_N / N：**QC02 锁口径后再拍**。124 不进本卡。

**2026-08-28 核对小结**

- **本条已挂起**（2026-08-28 `human:李伟`）。IMPL 不排本 ID。

---



### D37 · `M_CHAIN_INTERNATIONALIZATION_INDEX` · 产业链国际化程度（挂起）

**指标描述**：pending_data_lead：产业链国际化程度指数；基于海外企业/专利/贸易数据，口径与权重待确认。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=True。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **124**


| 列         | 值                                                                                                   |
| --------- | --------------------------------------------------------------------------------------------------- |
| 指标ID      | M_CHAIN_INTERNATIONALIZATION_INDEX                                                                  |
| 指标名       | 产业链国际化程度                                                                                            |
| 决策清单中的编号  | （空）                                                                                                 |
| 域         | 产业链                                                                                                 |
| 模块        | E2 产业链（待四维评估）                                                                                       |
| 模块说明      | 产业链                                                                                                 |
| 专题维度Owner | 李伟                                                                                                  |
| 算法类型      | COMPUTE                                                                                             |
| 合同集合      | F∩L                                                                                                 |
| 差集判定      | mapped                                                                                              |
| 语义层开发阶段   | 未标                                                                                                  |
| 验收单元      | —                                                                                                   |
| 四维评估      | 待评估                                                                                                 |
| 定义状态      | 已对齐                                                                                                 |
| 开放项       | （空）                                                                                                 |
| 结构支撑      | 待评估                                                                                                 |
| 结构缺口      | （空）                                                                                                 |
| 结构判定      | —                                                                                                   |
| 源映射       | 待评估                                                                                                 |
| 源缺口       | （空）                                                                                                 |
| 接入状态      | Mock                                                                                                |
| 接入阶段      | （空）                                                                                                 |
| 综合就绪      | 待算法实现                                                                                               |
| 卡点责任方     | 李伟                                                                                                  |
| 更新频率      | weekly                                                                                              |
| 口径摘要      | pending_data_lead：产业链国际化程度指数；基于海外企业/专利/贸易数据，口径与权重待确认。                                               |
| 缺口说明      | 产业链国际化程度=海外企业占比*w1+海外专利占比*w2+进出口数据*w3。基于海外企业/专利/贸易数据，口径与权重待确认。formula 待 algorithm-agent。Wave0 mock。 |
| 更新日期      | 2026-08-25                                                                                          |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **47**


| 列        | 值                                                     |
| -------- | ----------------------------------------------------- |
| 指标ID     | M_CHAIN_INTERNATIONALIZATION_INDEX                    |
| 指标名      | 产业链国际化程度                                              |
| 决策清单中的编号 | （空）                                                   |
| 域        | 产业链                                                   |
| 模块       | CHAIN                                                 |
| 算法类型     | COMPUTE                                               |
| D1定义     | —                                                     |
| D4接入     | —                                                     |
| 需求来源条数   | 1                                                     |
| 需求回填     | 已回填                                                   |
| 来源系统     | 展示系统                                                  |
| 主来源分册    | 05 算法库需规                                              |
| 主来源序号    | 95                                                    |
| 主来源名称    | 产业链基础指标模型构建                                           |
| 主来源简述    | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：产业链国际化程度。         |
| 主来源需规ID  | ALGO-CHAIN-BASE-95                                    |
| 全部来源     | 05·95 产业链基础指标模型构建                                     |
| 口径摘要     | pending_data_lead：产业链国际化程度指数；基于海外企业/专利/贸易数据，口径与权重待确认。 |
| 更新日期     | 2026-08-25                                            |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **50**（第 1 条）


| 列        | 值                                                 |
| -------- | ------------------------------------------------- |
| 指标ID     | M_CHAIN_INTERNATIONALIZATION_INDEX                |
| 指标名      | 产业链国际化程度                                          |
| 决策清单中的编号 | （空）                                               |
| 域        | 产业链                                               |
| 模块       | CHAIN                                             |
| 分册       | 05                                                |
| 分册名称     | 05 算法库需规                                          |
| 系统       | 展示系统                                              |
| 序号       | 95                                                |
| 需规名称     | 产业链基础指标模型构建                                       |
| 简要描述     | 页面 CHAIN-PORTAL-OVERVIEW 复用算法库叶。本指标：产业链国际化程度。     |
| 需规ID     | ALGO-CHAIN-BASE-95                                |
| 角色       | 算法库叶                                              |
| 页面       | CHAIN-PORTAL-OVERVIEW                             |
| 需规文件     | bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/产业链/基础指标.md |
| 回填状态     | 已回填                                               |




#### 4) 结合分析

**口径一句**：海外企业/专利/贸易加权。权重待确认。类型 COMPUTE。需求挂 05·95（基础包，需规无独立国际化公式）。

**MCP/seed**：type=`COMPUTE`；formula=`pending_algorithm（海外企业占比*w1+海外专利占比*w2+进出口数据*w3）`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_enterprise', 'dwd.industry_chain_patent <- ods: dwd_org_industry_chain_pat_dtl']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：海外企业需国外机构或地理国家；专利/贸易跨域。Demo 0。

**算法是否满足**：加权和 COMPUTE 够。三维与权重未签则不能交正式值。

**算法缺口**：权重/维度未拍。95 正文未写该指数。

**可实现**：否（口径未签）。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：维度权重；贸易数据是否在范围内。

**需要李伟确认的问题（仅特有）**

1. ~~三维等权临时默认~~ **不拍。已挂起。**
2. 权重 / 贸易源：**口径锁后再拍**。95 不塞进本公式。

**2026-08-28 核对小结**

- **本条已挂起**（2026-08-28 `human:李伟`）。IMPL 不排本 ID。

---



### E38 · `M_CHAIN_PATENT_COUNT` · 产业链关联专利数（已确认）

**指标描述**：产业链关联专利去重总数；对象范围 dwd.industry_chain_patent 全量，按 patent_id 去重。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=False。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **136**


| 列         | 值                                                             |
| --------- | ------------------------------------------------------------- |
| 指标ID      | M_CHAIN_PATENT_COUNT                                          |
| 指标名       | 产业链关联专利数                                                      |
| 决策清单中的编号  | （空）                                                           |
| 域         | 产业链                                                           |
| 模块        | E2 产业链（待四维评估）                                                 |
| 模块说明      | 产业链                                                           |
| 专题维度Owner | 李伟                                                            |
| 算法类型      | STAT                                                          |
| 合同集合      | F−L                                                           |
| 差集判定      | missing                                                       |
| 语义层开发阶段   | 未标                                                            |
| 验收单元      | —                                                             |
| 四维评估      | 待评估                                                           |
| 定义状态      | 已对齐                                                           |
| 开放项       | （空）                                                           |
| 结构支撑      | 待评估                                                           |
| 结构缺口      | （空）                                                           |
| 结构判定      | —                                                             |
| 源映射       | 齐备                                                            |
| 源缺口       | （空）                                                           |
| 接入状态      | Mock                                                          |
| 接入阶段      | （空）                                                           |
| 综合就绪      | 待接入（Mock）                                                     |
| 卡点责任方     | 李伟                                                            |
| 更新频率      | daily                                                         |
| 口径摘要      | 产业链关联专利去重总数；对象范围 dwd.industry_chain_patent 全量，按 patent_id 去重。 |
| 缺口说明      | （空）                                                           |
| 更新日期      | 2026-08-25                                                    |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **61**


| 列        | 值                                                             |
| -------- | ------------------------------------------------------------- |
| 指标ID     | M_CHAIN_PATENT_COUNT                                          |
| 指标名      | 产业链关联专利数                                                      |
| 决策清单中的编号 | （空）                                                           |
| 域        | 产业链                                                           |
| 模块       | CHAIN                                                         |
| 算法类型     | STAT                                                          |
| D1定义     | —                                                             |
| D4接入     | —                                                             |
| 需求来源条数   | 0                                                             |
| 需求回填     | 未回填                                                           |
| 来源系统     | （空）                                                           |
| 主来源分册    | （空）                                                           |
| 主来源序号    | （空）                                                           |
| 主来源名称    | （空）                                                           |
| 主来源简述    | （空）                                                           |
| 主来源需规ID  | （空）                                                           |
| 全部来源     | （空）                                                           |
| 口径摘要     | 产业链关联专利去重总数；对象范围 dwd.industry_chain_patent 全量，按 patent_id 去重。 |
| 更新日期     | 2026-08-25                                                    |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **64**（第 1 条）


| 列        | 值                    |
| -------- | -------------------- |
| 指标ID     | M_CHAIN_PATENT_COUNT |
| 指标名      | 产业链关联专利数             |
| 决策清单中的编号 | （空）                  |
| 域        | 产业链                  |
| 模块       | CHAIN                |
| 分册       | （空）                  |
| 分册名称     | （空）                  |
| 系统       | （空）                  |
| 序号       | （空）                  |
| 需规名称     | （空）                  |
| 简要描述     | （空）                  |
| 需规ID     | （空）                  |
| 角色       | （空）                  |
| 页面       | （空）                  |
| 需规文件     | （空）                  |
| 回填状态     | 未回填                  |




#### 4) 结合分析

**口径一句**：xlsx：dwd.industry_chain_patent 按 patent_id 去重。需求来源空。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT dwd.industry_chain_patent.patent_id)`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_patent <- ods: dwd_org_industry_chain_pat_dtl']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：v5/Demo DWD **无** `industry_chain_patent` 物理表（废名替换，不记缺表）。专利走专利要素库 × 链挂接。ADS 0。

**算法是否满足**：COUNT DISTINCT STAT 够。

**算法缺口**：无模型。缺专利如何挂链。

**可实现**：条件是：钉专利-链 Mapping。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：需求来源空；专利挂接未定。

**需要李伟确认的问题（仅特有）**

1. ~~专利挂链申请人还是主题/IPC~~ **已拍：甲**（跟 B21，信用代码）。

**口径一句（已确认）**

`dwd_patent` × 链上企业（申请人/受让人），全链 COUNT DISTINCT。无区域切片。不上主题 NLP。废名专利四表只替换。

**2026-08-28 核对小结**

- **本条已确认（甲）**。与 B21 同源，B21 到区域、本卡全链。需求来源空不挡。

---



### E39 · `M_CHAIN_PRODUCT_COUNT` · 产业链关联产品数（已确认）

**指标描述**：产业链关联产品去重总数；对象范围 dwd.industry_chain_product 全量，按 product_id 去重。

分析日：2026-08-26。规则 9/10 已应用。`getMetric`：seed=True matrix=False srs=False。Demo `0` fact / `0` series；代码：无。

#### 1) 进度表

文件：`agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`  
Sheet：`指标与数据开发进度` · excel 行号 **139**


| 列         | 值                                                               |
| --------- | --------------------------------------------------------------- |
| 指标ID      | M_CHAIN_PRODUCT_COUNT                                           |
| 指标名       | 产业链关联产品数                                                        |
| 决策清单中的编号  | （空）                                                             |
| 域         | 产业链                                                             |
| 模块        | E2 产业链（待四维评估）                                                   |
| 模块说明      | 产业链                                                             |
| 专题维度Owner | 李伟                                                              |
| 算法类型      | STAT                                                            |
| 合同集合      | F−L                                                             |
| 差集判定      | missing                                                         |
| 语义层开发阶段   | 未标                                                              |
| 验收单元      | —                                                               |
| 四维评估      | 待评估                                                             |
| 定义状态      | 已对齐                                                             |
| 开放项       | （空）                                                             |
| 结构支撑      | 待评估                                                             |
| 结构缺口      | （空）                                                             |
| 结构判定      | —                                                               |
| 源映射       | 齐备                                                              |
| 源缺口       | （空）                                                             |
| 接入状态      | Mock                                                            |
| 接入阶段      | （空）                                                             |
| 综合就绪      | 待接入（Mock）                                                       |
| 卡点责任方     | 李伟                                                              |
| 更新频率      | daily                                                           |
| 口径摘要      | 产业链关联产品去重总数；对象范围 dwd.industry_chain_product 全量，按 product_id 去重。 |
| 缺口说明      | （空）                                                             |
| 更新日期      | 2026-08-25                                                      |




#### 2) 需求来源·目录

文件：`agent-delivery/metrics/registry/export/指标需求来源.xlsx`  
Sheet：`指标目录` · excel 行号 **64**


| 列        | 值                                                               |
| -------- | --------------------------------------------------------------- |
| 指标ID     | M_CHAIN_PRODUCT_COUNT                                           |
| 指标名      | 产业链关联产品数                                                        |
| 决策清单中的编号 | （空）                                                             |
| 域        | 产业链                                                             |
| 模块       | CHAIN                                                           |
| 算法类型     | STAT                                                            |
| D1定义     | —                                                               |
| D4接入     | —                                                               |
| 需求来源条数   | 0                                                               |
| 需求回填     | 未回填                                                             |
| 来源系统     | （空）                                                             |
| 主来源分册    | （空）                                                             |
| 主来源序号    | （空）                                                             |
| 主来源名称    | （空）                                                             |
| 主来源简述    | （空）                                                             |
| 主来源需规ID  | （空）                                                             |
| 全部来源     | （空）                                                             |
| 口径摘要     | 产业链关联产品去重总数；对象范围 dwd.industry_chain_product 全量，按 product_id 去重。 |
| 更新日期     | 2026-08-25                                                      |


Sheet：`汇总`：无本 ID（批量已核）。

#### 3) 需求来源·明细

Sheet：`需求来源明细` · excel 行号 **67**（第 1 条）


| 列        | 值                     |
| -------- | --------------------- |
| 指标ID     | M_CHAIN_PRODUCT_COUNT |
| 指标名      | 产业链关联产品数              |
| 决策清单中的编号 | （空）                   |
| 域        | 产业链                   |
| 模块       | CHAIN                 |
| 分册       | （空）                   |
| 分册名称     | （空）                   |
| 系统       | （空）                   |
| 序号       | （空）                   |
| 需规名称     | （空）                   |
| 简要描述     | （空）                   |
| 需规ID     | （空）                   |
| 角色       | （空）                   |
| 页面       | （空）                   |
| 需规文件     | （空）                   |
| 回填状态     | 未回填                   |




#### 4) 结合分析

**口径一句**：xlsx：dwd.industry_chain_product 按 product_id 去重。需求来源空。

**MCP/seed**：type=`STAT`；formula=`COUNT(DISTINCT dwd.industry_chain_product.product_id)`；definition 与进度表口径对照见上。source_tables=['dwd.industry_chain_product <- ods: dwd_org_industry_chain_prod_dtl']。矩阵缺失则需求来源 D1/D4 空更诚实。

**ODS → DWD → ADS**：ODS `dwd_org_industry_product_tags` 存在。DWD 现行写入 `industry_chain_entity_rel` 且 `entity_type=product`（Demo 247）。旧名 product 表只替换。ADS 0。

**算法是否满足**：STAT 够。Demo 边表已有产品实体，未写本 metric_id。

**算法缺口**：无模型。产品 UID 映射文档仍标未冻（`p:{credit}:{id}`）。去重键用稳定产品 ID。

**可实现**：条件是：冻结产品 UID 后 COUNT DISTINCT。

**口径文档债（不是源缺失）**：旧名 `industry_chain_enterprise` / `industry_chain_news` / `industry_chain_patent` / `industry_chain_product` / `dwd_org_industry_chain_dtl` 只替换为现行 `entity_rel` / `news_event` / 跨域要素库，或从口径去除。

**缺口（真缺）**：需求来源空；产品 UID 未冻；ADS 未写。

**需要李伟确认的问题（仅特有）**

1. ~~产品去重按产品名还是合成 UID~~ **已拍：乙**（规范化 `product_name`）。
2. 现行表无 `product_id`。禁止 `p:{credit}:{行id}` 当主键。

**口径一句（已确认）**

`enterprise_industry_product.product_name`（规范化）COUNT DISTINCT。无 `product_id`。同名视为同一产品。禁止 Demo 合成键 `p:{org}:{行id}`。不读 ODS `dwd_org_industry_product_tags`。

**2026-08-28 核对小结**

- **本条已确认（乙）**。李伟指出表内无产品 ID，分析已改：不把合成键当真源。

---



## 6. 39 条核对总表（2026-08-28）

**已确认（可进 IMPL，A14 除外）**


| 序号      | ID                        | 口径要点                           |
| ------- | ------------------------- | ------------------------------ |
| A1      | ENTERPRISE_COUNT          | 期末存量 COUNT(成立年≤Y)              |
| A2      | ENTERPRISE_NEW_COUNT      | 当年新增 COUNT(成立年=Y)              |
| A3      | INSTITUTION_COUNT         | 乙机构库另挂链；当年成立                   |
| A7–A9   | GLOBAL/NATIONAL/SZ_REGION | 按国家/省/区切主体数；深圳 city=深圳市        |
| A10–A12 | SZ 企业/占比/机构               | 当前一个数；A11=A10/当前链上企业           |
| A13     | TOTAL_COUNT               | 全库 DISTINCT chain_id           |
| A14     | BASE_95_1                 | 封面；**IMPL 剔除、不进 ADS**          |
| B15–B16 | MARKET_SIZE/GROWTH        | QC06 营收加总；同比                   |
| B17–B19 | INVEST / REG 融资/营收        | 融资事件 COUNT；区域=链级×region_codes  |
| B20–B21 | REG 论文/专利                 | 要素库×主体挂接×区域                    |
| B23     | REG_RESEARCH_ORG          | 乙里科研院所+高校，当前 COUNT×区域          |
| C32     | SZ_COMPLETENESS           | 节点覆盖比率                         |
| E38     | PATENT_COUNT              | 跟 B21，全链无区域                    |
| E39     | PRODUCT_COUNT             | 乙：product_name 去重，无 product_id |


**挂起（IMPL 不排）**


| 序号              | 原因                      |
| --------------- | ----------------------- |
| A4–A6           | 资讯源无利用价值                |
| B22             | 政策专卡                    |
| B24             | 服务机构类型未钉                |
| B25             | 人才结构                    |
| C26–C31、C33–C35 | 需 MODEL、现不可做（C26 甲口径记下） |
| D36–D37         | 指数公式未锁                  |


（39 条核对齐。本叶不改 YAML。IMPL 另叶 `CHAIN-ALGO-STAT-39-IMPL-L01`，只动已确认且非封面条。）

---



## 7. DWD / ADS 纠错（2026-08-28，禁止读 ODS）

对照真源：CHAIN DWD v5 `industry_chain_*`；ENT DWD v3.1 `enterprise_*`；ADS v2 `industry_chain_metric_*` 等。供应方 `dwd_*` = ODS，本段不当源。

**ADS**：只是指标落点（`metric_fact` / `series` / `dist` / `region_dist` / `region_scorecard`）。业务口径在 DWD 算完再写入。现网多数 `M_CHAIN_`* ADS 仍空，不能反推口径。

### 7.1 和 E39 同类：表里没有分析用过的键 / 用了 ODS 表名


| 条          | 分析里写过的（错）                                                          | DWD 实际                                                                                                                                                                      | 业务口径还能否成立                               |
| ---------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| A1/A2      | `dwd_org_base_info.incorporation_date`、`credit_code`/`external_id` | 挂接 = `industry_chain_entity_rel`（`entity_type=enterprise`，`entity_id=org_id`）JOIN `enterprise_base.registration_date`（**不是** incorporation_date）。键是 **org_id**，不是信用代码直接当实体键 | 成立年切片仍成立，**路径必须改**                      |
| A3/A12/B23 | 「机构要素库」挂链                                                          | v5 允许 `entity_type=institution`；storage **没有**机构主数据 DWD。Demo 上链只写企业 `org_id`。机构成立日/类型/国家 **DWD 无表可拼**                                                                       | 乙集合 **现不可算**，与 E39 同类缺口                 |
| A7         | 拼「企业库国家」                                                           | 国内 `enterprise_base` 只有 `province`/`city`/`district`，**无 country**。国家在 `enterprise_forg_`*                                                                                  | 「按国家切主体」国内盘 **拼不出国家列**                  |
| A8–A10     | city/省/区                                                           | `enterprise_base.province/city/district` 有。深圳 `city=深圳市` 可对这三列                                                                                                              | A8–A10 **企业侧**路径成立                      |
| B15/B16    | 年报营收                                                               | `enterprise_finance_history.revenue` + `data_year`。**禁止**灌 `industry_chain_market_observation`                                                                              | 成立；表名从 ODS 年报改为本表                       |
| B17        | `dwd_org_financing_info`                                           | ENT：`enterprise_financing`（`org_id`+`event_date`）。CHAIN：`industry_chain_investment_event`（Demo 多为 mock）                                                                     | COUNT 事件仍成立，**必须改 DWD 表名**；不要扫 ODS      |
| B20        | 论文要素库                                                              | CHAIN/ENT DWD **无论文表**                                                                                                                                                      | 与 E39 同类：**DWD 无源**，已确认条应改挂起或等机构/成果 DWD |
| B21/E38    | `dwd_patent`                                                       | `enterprise_patent_detail.patent_id`（UK `org_id+patent_id`）× 链上 `org_id`                                                                                                    | 有 `patent_id`，比产品好。不要写 `dwd_patent`     |
| E39        | 一度写合成 UID / ODS tags                                               | `enterprise_industry_product` 有 `product_name`，**无 product_id**；as-built 行数曾为 **0**。`entity_rel` 产品行 `entity_id` 设计要 `product_uid`（未冻）                                      | 乙（按名去重）仍成立；算的是 **DWD 产品名**，不是 ODS       |




### 7.2 路径成立、分析表述过时（改 JOIN，不改业务句）


| 条   | DWD 怎么算                                                                                               | 注意                                  |
| --- | ----------------------------------------------------------------------------------------------------- | ----------------------------------- |
| A13 | `industry_chain` COUNT DISTINCT `chain_id`                                                            | 区分 L0/L1（`chain_tier`），IMPL 不要把节点当链 |
| C32 | 分母 `industry_chain_node`（该链节点）；分子 = 有 `entity_rel` 企业且 `enterprise_base.city=深圳市` 覆盖到的 `node_id`      | 不读 ODS；不升 118                       |
| B18 | B17 事件 × 区域。融资 DWD 有 `event_date`；CHAIN 投资事件有可选 `region_code`，否则跟融资企业 `enterprise_base.city/province` | 不要用资讯表                              |
| B19 | B15 × 同一套地理列                                                                                          | 同上                                  |
| A11 | A10 / 当前链上企业，两边都是 `entity_rel`+`enterprise_base`                                                      | 不读 ODS                              |




### 7.3 挂起条（本轮不重算 IMPL）

A4–A6 资讯：DWD 有 `industry_chain_news_event`，但已拍合规源无利用价值，仍挂起。  
C26–C31/C33–C35：标签在 `industry_chain_model_result_detail`，现不灌，挂起正确。  
B22/B24/B25：政策/服务/人才 DWD 主数据未齐，挂起正确。  
D36/D37：公式未锁，挂起正确。

### 7.4 建议李伟拍的纠错（只动路径/状态，不改已拍业务句）

1. **A1/A2/A8–A11/B15–B19/B21/E38/E39/C32**：业务句保留；IMPL 一律改走 **§7.1–7.2 DWD 表**，作废分析稿里的 `dwd_org_`* / `dwd_patent` / `incorporation_date`。
2. **A3/A12/B23**：DWD 无机构主表 → 建议 **改挂起**（与「现不可做」同规则）。
3. **A7**：国内企业无国家列 → 建议 **改挂起**，或收成「只切已有 country 的国外机构表」（需另拍）。
4. **B20**：DWD 无论文表 → 建议 **改挂起**。

未拍前不改 YAML。已写入规则 10：指标分析禁止读 ODS。